#!/usr/bin/env python3
"""
Pulls hotels per Welsh town from Google Places API (New) Text Search
(https://places.googleapis.com/v1/places:searchText).

Reads the API key from the PLACES_API_KEY environment variable -- never
hardcode it in this file or any committed output.

Handles pagination (Places API New returns up to 20 per page, with a
nextPageToken for more -- there's a short mandatory delay before a page
token becomes valid, handled below).

Usage:
  PLACES_API_KEY=xxx python3 fetch_restaurants.py --towns towns_pilot.txt --out restaurants_pilot.csv
"""
import argparse
import csv
import json
import os
import time

import requests

API_URL = "https://places.googleapis.com/v1/places:searchText"
FIELD_MASK = "places.displayName,places.formattedAddress,places.nationalPhoneNumber,places.websiteUri,nextPageToken"
CA_BUNDLE = "/root/.ccr/ca-bundle.crt"


def search_town(api_key, town, max_pages=3):
    results = []
    page_token = None
    for page in range(max_pages):
        body = {"textQuery": f"hotels in {town}, Wales"}
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
        time.sleep(2)  # page tokens need a short delay before they're valid
    return results


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--towns", required=True, help="text file, one town per line")
    ap.add_argument("--out", required=True)
    ap.add_argument("--max-pages", type=int, default=3)
    ap.add_argument("--skip-towns", type=int, default=0, help="skip this many already-processed towns and append to --out")
    args = ap.parse_args()

    api_key = os.environ.get("PLACES_API_KEY")
    if not api_key:
        raise SystemExit("Set PLACES_API_KEY environment variable")

    with open(args.towns) as f:
        towns = [line.strip() for line in f if line.strip()]
    if args.skip_towns:
        towns = towns[args.skip_towns:]

    fieldnames = ["Town", "Name", "Address", "Phone", "Website"]
    write_header = not (args.skip_towns and os.path.exists(args.out))
    mode = "a" if args.skip_towns and os.path.exists(args.out) else "w"

    total_rows = 0
    total_with_website = 0
    request_count = 0
    with open(args.out, mode, newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if write_header:
            writer.writeheader()
        f.flush()
        for town in towns:
            places = search_town(api_key, town, max_pages=args.max_pages)
            request_count += min(args.max_pages, max(1, (len(places) + 19) // 20))
            print(f"{town}: {len(places)} results")
            for p in places:
                row = {
                    "Town": town,
                    "Name": p.get("displayName", {}).get("text", ""),
                    "Address": p.get("formattedAddress", ""),
                    "Phone": p.get("nationalPhoneNumber", ""),
                    "Website": p.get("websiteUri", ""),
                }
                writer.writerow(row)
                total_rows += 1
                if row["Website"]:
                    total_with_website += 1
            f.flush()
            time.sleep(0.3)

    print(f"\nTotal restaurants written this run: {total_rows}")
    if total_rows:
        print(f"With website: {total_with_website} ({total_with_website/total_rows:.0%})")
    print(f"Approx API requests used this run: {request_count}")


if __name__ == "__main__":
    main()
