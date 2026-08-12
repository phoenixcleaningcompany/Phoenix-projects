#!/usr/bin/env python3
"""
Given the CQC England independent/small-chain list (which has name/phone/
website but no email), visits each site's homepage and a couple of likely
contact pages, and pulls out any email address found (mailto: links or
plain-text email patterns).

Free, but slow and imperfect: many sites won't publish an email, some will
block automated requests, some emails will be generic (info@) rather than
a named contact. Run the pilot first (--limit) to see the real hit rate
before committing to the full list.

Usage:
  python3 find_emails.py --limit 30            # pilot
  python3 find_emails.py --limit 0 --out found_emails.csv   # full run (0 = no limit)
"""
import argparse
import csv
import re
import sys
import time
from urllib.parse import urljoin, urlparse

import requests

SOURCE = "independent_and_small_chain.csv"
EMAIL_RE = re.compile(r"[a-zA-Z0-9._+\-]{1,64}@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}")
MAILTO_RE = re.compile(r'mailto:([a-zA-Z0-9._+\-]{1,64}@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,})', re.IGNORECASE)
BAD_DOMAIN_SNIPPETS = ("sentry.io", "wixpress.com", "example.com", "godaddy.com", "cloudflare.com", "calendar.google.com")
CONTACT_PATHS = ("", "/contact", "/contact-us")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}


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
            resp = requests.get(url, headers=HEADERS, timeout=timeout, verify="/root/.ccr/ca-bundle.crt")
        except requests.RequestException:
            # connection-level failure (timeout, refused, DNS, TLS) -- same host will
            # almost certainly fail the same way on every other path, so stop early
            # instead of burning the timeout again for each remaining path.
            return None, None
        if resp.status_code >= 400:
            continue
        emails = extract_emails(resp.text)
        if emails:
            return sorted(emails)[0], url
    return None, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=30)
    ap.add_argument("--out", default="found_emails_pilot.csv")
    ap.add_argument("--skip", type=int, default=0, help="skip this many already-processed rows and append to --out")
    args = ap.parse_args()

    with open(SOURCE, newline="", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if r["Service's website (if available)"].strip()]

    if args.skip:
        rows = rows[args.skip:]
    if args.limit:
        rows = rows[: args.limit]

    hits = 0
    fieldnames = ["Name", "Postcode", "Phone number", "Website", "Email", "Found on page"]
    import os
    write_header = not (args.skip and os.path.exists(args.out))
    mode = "a" if args.skip and os.path.exists(args.out) else "w"
    with open(args.out, mode, newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if write_header:
            writer.writeheader()
        f.flush()
        for i, r in enumerate(rows, 1):
            url = normalize_url(r["Service's website (if available)"])
            email, found_on = find_email_for_site(url)
            status = "FOUND" if email else "none"
            if email:
                hits += 1
            print(f"[{i}/{len(rows)}] {status:5s} {r['Name'][:40]:40s} {url}", file=sys.stderr)
            writer.writerow({
                "Name": r["Name"], "Postcode": r["Postcode"], "Phone number": r["Phone number"],
                "Website": r["Service's website (if available)"], "Email": email or "",
                "Found on page": found_on or "",
            })
            f.flush()
            time.sleep(0.3)

    print(f"\nDone. {hits}/{len(rows)} sites yielded an email ({hits/len(rows):.0%}). Written to {args.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
