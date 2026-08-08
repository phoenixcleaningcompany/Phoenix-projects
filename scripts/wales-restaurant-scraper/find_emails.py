#!/usr/bin/env python3
"""
Same approach as scripts/england-care-scraper/find_emails.py: visits each
restaurant's website (home, /contact, /contact-us) and pulls an email from
mailto: links or plain-text patterns. Short timeout, stops trying further
pages on a connection-level failure (same host will fail the same way).

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

SOURCE = "restaurants_independent.csv"
EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}")
MAILTO_RE = re.compile(r'mailto:([a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,})', re.IGNORECASE)
BAD_DOMAIN_SNIPPETS = ("sentry.io", "wixpress.com", "example.com", "godaddy.com", "cloudflare.com")
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


def extract_emails(html: str):
    found = set(MAILTO_RE.findall(html)) | set(EMAIL_RE.findall(html))
    return {e for e in found if not any(bad in e.lower() for bad in BAD_DOMAIN_SNIPPETS)}


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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=30)
    ap.add_argument("--out", default="found_emails_pilot.csv")
    ap.add_argument("--skip", type=int, default=0)
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
            time.sleep(0.3)

    print(f"\nDone. {hits}/{len(rows)} sites yielded an email ({hits/len(rows):.0%} this run).", file=sys.stderr)


if __name__ == "__main__":
    main()
