#!/usr/bin/env python3
"""
Pilot: compares two Places API (New) Text Search query phrasings for the
catering-engineers vertical across a small town sample, before committing
to a full 446-town run.

  Query A: "catering engineers in {town}, England"
  Query B: "commercial catering equipment repair in {town}, England"

Reports, per query: total results, unique businesses (by Name+Address).
Reports overlap between A and B, and how many distinct businesses appear
under multiple towns (a proxy for "this is a regional player, not a
one-per-town independent" -- expected to be high for this vertical).

Usage:
  PLACES_API_KEY=xxx python3 pilot_compare_queries.py --towns towns_pilot.txt --out pilot_results.csv
"""
import argparse
import csv
import os
import time
from collections import Counter

import requests

API_URL = "https://places.googleapis.com/v1/places:searchText"
FIELD_MASK = "places.displayName,places.formattedAddress,places.nationalPhoneNumber,places.websiteUri,nextPageToken"
CA_BUNDLE = "/root/.ccr/ca-bundle.crt"

QUERIES = {
    "A_catering_engineers": "catering engineers in {town}, England",
    "B_equipment_repair": "commercial catering equipment repair in {town}, England",
}


def search(api_key, text_query, max_pages=3):
    results = []
    page_token = None
    for _ in range(max_pages):
        body = {"textQuery": text_query}
        if page_token:
            body["pageToken"] = page_token
        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": api_key,
            "X-Goog-FieldMask": FIELD_MASK,
        }
        resp = requests.post(API_URL, headers=headers, json=body, timeout=20, verify=CA_BUNDLE)
        resp.raise_for_status()
        data = resp.json()
        places = data.get("places", [])
        results.extend(places)
        page_token = data.get("nextPageToken")
        if not page_token or not places:
            break
        time.sleep(2)
    return results


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--towns", required=True)
    ap.add_argument("--out", default="pilot_results.csv")
    ap.add_argument("--max-pages", type=int, default=3)
    args = ap.parse_args()

    api_key = os.environ.get("PLACES_API_KEY")
    if not api_key:
        raise SystemExit("Set PLACES_API_KEY environment variable")

    with open(args.towns) as f:
        towns = [line.strip() for line in f if line.strip()]

    fieldnames = ["QueryLabel", "Town", "Name", "Address", "Phone", "Website"]
    rows = []
    per_query_seen = {label: set() for label in QUERIES}
    request_count = 0

    with open(args.out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for town in towns:
            for label, template in QUERIES.items():
                text_query = template.format(town=town)
                places = search(api_key, text_query, max_pages=args.max_pages)
                request_count += min(args.max_pages, max(1, (len(places) + 19) // 20))
                print(f"[{label}] {town}: {len(places)} results")
                for p in places:
                    name = p.get("displayName", {}).get("text", "")
                    addr = p.get("formattedAddress", "")
                    per_query_seen[label].add((name, addr))
                    row = {
                        "QueryLabel": label, "Town": town, "Name": name, "Address": addr,
                        "Phone": p.get("nationalPhoneNumber", ""),
                        "Website": p.get("websiteUri", ""),
                    }
                    rows.append(row)
                    writer.writerow(row)
                f.flush()
                time.sleep(0.3)

    print(f"\n=== Pilot summary ({len(towns)} towns) ===")
    print(f"Approx API requests used: {request_count}")
    for label in QUERIES:
        total = sum(1 for r in rows if r["QueryLabel"] == label)
        unique = len(per_query_seen[label])
        print(f"  {label}: {total} raw results, {unique} unique (Name+Address)")

    overlap = per_query_seen["A_catering_engineers"] & per_query_seen["B_equipment_repair"]
    a_only = per_query_seen["A_catering_engineers"] - per_query_seen["B_equipment_repair"]
    b_only = per_query_seen["B_equipment_repair"] - per_query_seen["A_catering_engineers"]
    print(f"\nOverlap between A and B: {len(overlap)}")
    print(f"A-only (missed by B): {len(a_only)}")
    print(f"B-only (missed by A): {len(b_only)}")

    all_names = Counter(r["Name"] for r in rows)
    repeats = {n: c for n, c in all_names.items() if c >= 3}
    print(f"\nBusinesses appearing under 3+ (town, query) combos (likely regional/national players, not local independents):")
    for name, c in sorted(repeats.items(), key=lambda x: -x[1])[:20]:
        print(f"  {c:2d}  {name}")


if __name__ == "__main__":
    main()
