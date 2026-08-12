#!/usr/bin/env python3
"""
Same approach as the other England scrapers: visits each catering engineer's
website (home, /contact, /contact-us) and pulls an email from mailto: links
or plain-text patterns. Short timeout, stops trying further pages on a
connection-level failure (same host will fail the same way).

Usage:
  python3 find_emails.py --limit 0 --out found_emails_full.csv   # full run
  python3 find_emails.py --limit 0 --skip N --out found_emails_full.csv   # resume
"""
import argparse
import csv
import os
import re
import sys
import time
from urllib.parse import urljoin, urlparse

import requests

SOURCE = "catering_engineers_independent.csv"
EMAIL_RE = re.compile(r"[a-zA-Z0-9._+\-]{1,64}@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}")
MAILTO_RE = re.compile(r'mailto:([a-zA-Z0-9._+\-]{1,64}@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,})', re.IGNORECASE)
BAD_DOMAIN_SNIPPETS = ("sentry.io", "wixpress.com", "example.com", "godaddy.com", "cloudflare.com", "calendar.google.com")
CONTACT_PATHS = ("", "/contact", "/contact-us")
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
CA_BUNDLE = "/root/.ccr/ca-bundle.crt"


def normalize_url(raw: str) -> str:
    raw = raw.strip()
    if not raw:
        return ""
    if not raw.startswith("http://") and not raw.startswith("https://"):
        raw = "https://" + raw
    return raw


ALLOWED_TLDS = {
    'com', 'org', 'net', 'biz', 'info', 'me', 'uk',
    'co.uk', 'org.uk', 'net.uk', 'ltd.uk', 'plc.uk', 'gov.uk', 'ac.uk', 'sch.uk', 'nhs.uk',
}


def _valid_email_tld(email):
    email = email.lower()
    if email.count('@') != 1:
        return False
    domain = email.split('@', 1)[1]
    parts = domain.split('.')
    if len(parts) < 2:
        return False
    return '.'.join(parts[-2:]) in ALLOWED_TLDS or parts[-1] in ALLOWED_TLDS


def extract_emails(html: str):
    found = set(MAILTO_RE.findall(html)) | set(EMAIL_RE.findall(html))
    return {e for e in found if not any(bad in e.lower() for bad in BAD_DOMAIN_SNIPPETS) and _valid_email_tld(e)}


def find_email_for_site(base_url: str, timeout=4):
    parsed = urlparse(base_url)
    root = f"{parsed.scheme}://{parsed.netloc}"
    for path in CONTACT_PATHS:
        url = urljoin(root, path)
        try:
            resp = requests.get(url, headers=HEADERS, timeout=timeout, verify=CA_BUNDLE)
        except requests.RequestException:
            return None, None
        if resp.status_code >= 400:
            continue
        emails = extract_emails(resp.text)
        if emails:
            return sorted(emails)[0], url
    return None, None


def auto_commit(out_path, processed_count):
    """Commit+push progress periodically so a container restart can't lose
    more than COMMIT_EVERY rows -- this environment has restarted several
    times mid-run already, always wiping whatever wasn't yet committed."""
    import subprocess
    repo_root = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, cwd=os.path.dirname(os.path.abspath(out_path)) or "."
    ).stdout.strip()
    try:
        abs_out_path = os.path.abspath(out_path)
        subprocess.run(["git", "add", "-f", abs_out_path], cwd=repo_root, check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", f"Auto-checkpoint: {processed_count} catering engineer sites processed"],
            cwd=repo_root, check=True, capture_output=True,
        )
        subprocess.run(["git", "push"], cwd=repo_root, check=True, capture_output=True, timeout=30)
        print(f"  [auto-checkpoint committed+pushed at {processed_count}]", file=sys.stderr)
    except Exception as e:
        print(f"  [auto-checkpoint failed, continuing anyway: {e}]", file=sys.stderr)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=30)
    ap.add_argument("--out", default="found_emails_pilot.csv")
    ap.add_argument("--skip", type=int, default=0)
    ap.add_argument("--commit-every", type=int, default=100, help="0 disables auto-commit")
    args = ap.parse_args()

    with open(SOURCE, newline="", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if r["Website"].strip()]
    if args.skip:
        rows = rows[args.skip:]
    if args.limit:
        rows = rows[: args.limit]

    fieldnames = ["Town", "Name", "Address", "Phone", "Website", "Email", "Found on page"]
    write_header = not (args.skip and os.path.exists(args.out))
    mode = "a" if args.skip and os.path.exists(args.out) else "w"

    hits = 0
    with open(args.out, mode, newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if write_header:
            writer.writeheader()
        f.flush()
        for i, r in enumerate(rows, 1):
            url = normalize_url(r["Website"])
            email, found_on = find_email_for_site(url)
            status = "FOUND" if email else "none"
            if email:
                hits += 1
            print(f"[{i}/{len(rows)}] {status:5s} {r['Name'][:40]:40s} {url}", file=sys.stderr)
            writer.writerow({
                "Town": r["Town"], "Name": r["Name"], "Address": r["Address"],
                "Phone": r["Phone"], "Website": r["Website"],
                "Email": email or "", "Found on page": found_on or "",
            })
            f.flush()
            if args.commit_every and i % args.commit_every == 0:
                auto_commit(args.out, args.skip + i)
            time.sleep(0.3)

    if args.commit_every:
        auto_commit(args.out, args.skip + len(rows))
    print(f"\nDone. {hits}/{len(rows)} sites yielded an email ({hits/len(rows):.0%} this run).", file=sys.stderr)


if __name__ == "__main__":
    main()
