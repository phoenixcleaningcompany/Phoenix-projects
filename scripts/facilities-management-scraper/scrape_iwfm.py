#!/usr/bin/env python3
"""
Scrapes IWFM's (Institute of Workplace and Facilities Management) public
supplier directory (https://www.iwfm.org.uk/suppliers.html) for FM
companies -- the UK trade body for facilities management, equivalent role
to TPI for block management. Same situation as TPI: plain server-rendered,
paginated (?category=&region=&page=), no bot protection, Cloudflare
email-obfuscation decoded the same standard reversible way.

Categories: FM Management (143570002) and FM Service Supplier (143570003)
-- the two closest to "facilities management companies" as a lead type.
Skipped: Product Supplier, Recruitment, Consultant, End User.

Regions: London, South West, South, North, Midlands, Home Counties, East,
Wales (England/Wales only -- Scotland, Ireland, UAE, No Region excluded).

Result count text on the site is "N RESULTS", "SINGLE RESULT", or
"NO RESULTS" -- handled explicitly rather than assumed.
"""
import csv
import re
import time
from urllib.parse import quote

import requests

BASE = "https://www.iwfm.org.uk/suppliers.html"
CATEGORIES = {
    "143570002": "FM Management",
    "143570003": "FM Service Supplier",
}
REGIONS = {
    "143570003": "London",
    "143570009": "South West",
    "143570008": "South",
    "143570006": "North",
    "143570004": "Midlands",
    "143570001": "Home Counties",
    "143570000": "East",
    "143570011": "Wales",
}
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
CA_BUNDLE = "/root/.ccr/ca-bundle.crt"

LISTING_RE = re.compile(
    r'<div class="directory-listing-item.*?<h4>(.*?)</h4>(.*?)(?=<div class="directory-listing-item|$)',
    re.DOTALL,
)
WEBSITE_RE = re.compile(r'font-icon-desktop.*?<a href="(http[^"]+)"', re.DOTALL)
PHONE_RE = re.compile(r'font-icon-phone.*?<div class="dd">([0-9+ ]+)</div>', re.DOTALL)
CFEMAIL_RE = re.compile(r'data-cfemail="([0-9a-f]+)"')


def decode_cfemail(hexstr: str) -> str:
    b = bytes.fromhex(hexstr)
    key = b[0]
    return "".join(chr(c ^ key) for c in b[1:])


def result_count(html: str) -> int:
    if "NO RESULTS" in html:
        return 0
    if "SINGLE RESULT" in html:
        return 1
    m = re.search(r"(\d+)\s+RESULTS", html)
    return int(m.group(1)) if m else 0


def fetch(cat_id: str, region_id: str, page: int) -> str:
    url = f"{BASE}?category={cat_id}&region={region_id}&page={page}"
    resp = requests.get(url, headers=HEADERS, timeout=15, verify=CA_BUNDLE)
    resp.raise_for_status()
    return resp.text


def parse_listings(html: str, category_name: str, region_name: str):
    for name, block in LISTING_RE.findall(html):
        site_m = WEBSITE_RE.search(block)
        phone_m = PHONE_RE.search(block)
        cf_m = CFEMAIL_RE.search(block)
        yield {
            "Name": name.strip(),
            "Category": category_name,
            "Region": region_name,
            "Website": (site_m.group(1).strip() if site_m else ""),
            "Phone": (phone_m.group(1).strip() if phone_m else ""),
            "Email": (decode_cfemail(cf_m.group(1)) if cf_m else ""),
        }


def scrape(cat_id, cat_name, region_id, region_name):
    html = fetch(cat_id, region_id, 1)
    total = result_count(html)
    if total == 0:
        print(f"  {cat_name} / {region_name}: 0 results")
        return []
    results = list(parse_listings(html, cat_name, region_name))
    page = 2
    while len(results) < total:
        html = fetch(cat_id, region_id, page)
        new = list(parse_listings(html, cat_name, region_name))
        if not new:
            break
        results.extend(new)
        page += 1
        time.sleep(0.4)
    print(f"  {cat_name} / {region_name}: {total} results, {len(results)} parsed")
    return results


def main():
    all_results = []
    seen = set()
    for cat_id, cat_name in CATEGORIES.items():
        for region_id, region_name in REGIONS.items():
            for r in scrape(cat_id, cat_name, region_id, region_name):
                key = (r["Name"], r["Category"])
                if key not in seen:
                    seen.add(key)
                    all_results.append(r)
            time.sleep(0.4)

    fieldnames = ["Name", "Category", "Region", "Phone", "Email", "Website"]
    with open("iwfm_members.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_results)

    has_email = sum(1 for r in all_results if r["Email"])
    has_phone = sum(1 for r in all_results if r["Phone"])
    print(f"\nTotal unique companies: {len(all_results)}")
    if all_results:
        print(f"With email: {has_email} ({has_email/len(all_results):.0%})")
        print(f"With phone: {has_phone} ({has_phone/len(all_results):.0%})")


if __name__ == "__main__":
    main()
