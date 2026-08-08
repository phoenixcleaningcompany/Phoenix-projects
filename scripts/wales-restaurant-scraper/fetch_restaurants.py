#!/usr/bin/env python3
"""
Pulls restaurants per Welsh town from Google Places API (New) Text Search
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
        body = {"textQuery": f"restaurants in {town}, Wales"}
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
    args = ap.parse_args()

    api_key = os.environ.get("PLACES_API_KEY")
    if not api_key:
        raise SystemExit("Set PLACES_API_KEY environment variable")

    with open(args.towns) as f:
        towns = [line.strip() for line in f if line.strip()]

    rows = []
    request_count = 0
    for town in towns:
        places = search_town(api_key, town, max_pages=args.max_pages)
        request_count += min(args.max_pages, max(1, (len(places) + 19) // 20))
        print(f"{town}: {len(places)} results")
        for p in places:
            rows.append({
                "Town": town,
                "Name": p.get("displayName", {}).get("text", ""),
                "Address": p.get("formattedAddress", ""),
                "Phone": p.get("nationalPhoneNumber", ""),
                "Website": p.get("websiteUri", ""),
            })
        time.sleep(0.3)

    fieldnames = ["Town", "Name", "Address", "Phone", "Website"]
    with open(args.out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    has_website = sum(1 for r in rows if r["Website"])
    print(f"\nTotal restaurants: {len(rows)}")
    print(f"With website: {has_website} ({has_website/len(rows):.0%})" if rows else "0")
    print(f"Approx API requests used: {request_count}")


if __name__ == "__main__":
    main()
