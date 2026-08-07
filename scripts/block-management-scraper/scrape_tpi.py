#!/usr/bin/env python3
"""
Scrapes The Property Institute (TPI) public member directory
(https://www.tpi.org.uk/tpi-community/member-directory/) for block/property
management company members across England and Wales.

This is a plain server-rendered, paginated HTTP page (no bot protection, no
JS rendering needed) -- confirmed by direct curl testing. Company emails on
the page are Cloudflare email-obfuscated (data-cfemail hex attribute); this
is a standard, publicly documented, reversible XOR encoding that every
browser decodes automatically for real visitors (Cloudflare's own anti-spam
feature, not an access-control/security boundary) -- decoding it here
reproduces exactly what a browser already does, it does not bypass any
protection that blocks the request itself.

Regions covered (England + Wales only; Scotland excluded intentionally):
London, South West, South East, Wales, East of England, West Midlands,
East Midlands, Yorkshire, North West, North East.
"""
import csv
import re
import time
from urllib.parse import quote

import requests

BASE = "https://www.tpi.org.uk/tpi-community/member-directory/"
REGIONS = [
    "London", "South West", "South East", "Wales", "East of England",
    "West Midlands", "East Midlands", "Yorkshire", "North West", "North East",
]
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}
CA_BUNDLE = "/root/.ccr/ca-bundle.crt"

LISTING_RE = re.compile(
    r'<div class="member-listing member-listing__company-member">(.*?)</div>\s*</div>\s*</div>',
    re.DOTALL,
)
NAME_RE = re.compile(r'member-listing__member-name\s*">\s*(.*?)\s*</div>', re.DOTALL)
ADDRESS_RE = re.compile(r'member-listing__member-address">(.*?)</div>', re.DOTALL)
WEBSITE_RE = re.compile(r"<a href='(http[^']+)'>[^<]*</a>")
PHONE_RE = re.compile(r'href="tel:([0-9+ ]+)"')
CFEMAIL_RE = re.compile(r'data-cfemail="([0-9a-f]+)"')
PAGE_COUNT_RE = re.compile(r'aria-label="Go to Page 1">(\d+)</a>')


def decode_cfemail(hexstr: str) -> str:
    b = bytes.fromhex(hexstr)
    key = b[0]
    return "".join(chr(c ^ key) for c in b[1:])


def fetch(region: str, page: int) -> str:
    url = f"{BASE}?Region={quote(region)}&page={page}"
    resp = requests.get(url, headers=HEADERS, timeout=15, verify=CA_BUNDLE)
    resp.raise_for_status()
    return resp.text


def parse_listings(html: str):
    for block in LISTING_RE.findall(html):
        name_m = NAME_RE.search(block)
        addr_m = ADDRESS_RE.search(block)
        site_m = WEBSITE_RE.search(block)
        phone_m = PHONE_RE.search(block)
        cf_m = CFEMAIL_RE.search(block)
        yield {
            "Name": (name_m.group(1).strip() if name_m else ""),
            "Address": (addr_m.group(1).strip() if addr_m else ""),
            "Website": (site_m.group(1).strip() if site_m else ""),
            "Phone": (phone_m.group(1).strip() if phone_m else ""),
            "Email": (decode_cfemail(cf_m.group(1)) if cf_m else ""),
        }


def max_page_number(html: str) -> int:
    nums = [int(n) for n in re.findall(r'aria-label="Go to Page 1">(\d+)</a>', html)]
    return max(nums) if nums else 1


def scrape_region(region: str):
    results = []
    page = 1
    seen_names = set()
    while True:
        html = fetch(region, page)
        listings = list(parse_listings(html))
        if not listings:
            break
        new_count = 0
        for r in listings:
            key = (r["Name"], r["Address"])
            if key not in seen_names:
                seen_names.add(key)
                r["Region"] = region
                results.append(r)
                new_count += 1
        print(f"  {region} page {page}: {len(listings)} listings ({new_count} new)")
        if new_count == 0:
            break
        last_page = max_page_number(html)
        if page >= last_page:
            break
        page += 1
        time.sleep(0.5)
    return results


def main():
    all_results = []
    for region in REGIONS:
        print(f"Region: {region}")
        all_results.extend(scrape_region(region))

    fieldnames = ["Name", "Region", "Address", "Phone", "Email", "Website"]
    with open("tpi_members.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_results)

    has_email = sum(1 for r in all_results if r["Email"])
    has_phone = sum(1 for r in all_results if r["Phone"])
    print(f"\nTotal members: {len(all_results)}")
    print(f"With email: {has_email} ({has_email/len(all_results):.0%})" if all_results else "0")
    print(f"With phone: {has_phone} ({has_phone/len(all_results):.0%})" if all_results else "0")


if __name__ == "__main__":
    main()
