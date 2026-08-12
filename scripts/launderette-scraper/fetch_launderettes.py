#!/usr/bin/env python3
"""
Pulls launderettes per town from Google Places API (New) Text Search.
Single query phrasing per town: "launderettes in {town}, {country}".

Reads the API key from the PLACES_API_KEY environment variable -- never
hardcode it in this file or any committed output.

Auto-commits/pushes the output file every --commit-every towns.

Usage:
  PLACES_API_KEY=xxx python3 fetch_launderettes.py --towns towns_wales.txt --country Wales --out launderettes_full.csv
  PLACES_API_KEY=xxx python3 fetch_launderettes.py --towns towns_england.txt --country England --out launderettes_full.csv --append
"""
import argparse
import csv
import os
import subprocess
import sys
import time

import requests

API_URL = "https://places.googleapis.com/v1/places:searchText"
FIELD_MASK = "places.displayName,places.formattedAddress,places.nationalPhoneNumber,places.websiteUri,nextPageToken"
CA_BUNDLE = "/root/.ccr/ca-bundle.crt"


def search_town(api_key, town, country, max_pages=3):
    results = []
    page_token = None
    for _ in range(max_pages):
        body = {"textQuery": f"launderettes in {town}, {country}"}
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


def auto_commit(out_path, processed_count):
    repo_root = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True,
        cwd=os.path.dirname(os.path.abspath(out_path)) or "."
    ).stdout.strip()
    try:
        abs_out_path = os.path.abspath(out_path)
        subprocess.run(["git", "add", "-f", abs_out_path], cwd=repo_root, check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", f"Auto-checkpoint: launderettes, {processed_count} towns processed"],
                        cwd=repo_root, check=True, capture_output=True)
        subprocess.run(["git", "push"], cwd=repo_root, check=True, capture_output=True, timeout=30)
        print(f"  [checkpoint committed and pushed at {processed_count} towns]", file=sys.stderr)
    except Exception as e:
        print(f"  [auto-checkpoint failed, continuing anyway: {e}]", file=sys.stderr)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--towns", required=True, help="text file, one town per line")
    ap.add_argument("--country", required=True, choices=["Wales", "England"])
    ap.add_argument("--out", required=True)
    ap.add_argument("--max-pages", type=int, default=3)
    ap.add_argument("--skip-towns", type=int, default=0)
    ap.add_argument("--append", action="store_true", help="append to --out even if --skip-towns is 0")
    ap.add_argument("--commit-every", type=int, default=25, help="0 disables auto-commit")
    args = ap.parse_args()

    api_key = os.environ.get("PLACES_API_KEY")
    if not api_key:
        raise SystemExit("Set PLACES_API_KEY environment variable")

    with open(args.towns) as f:
        towns = [line.strip() for line in f if line.strip()]
    if args.skip_towns:
        towns = towns[args.skip_towns:]

    do_append = (args.skip_towns or args.append) and os.path.exists(args.out)
    fieldnames = ["Country", "Town", "Name", "Address", "Phone", "Website"]
    write_header = not do_append
    mode = "a" if do_append else "w"

    total_rows = 0
    total_with_website = 0
    request_count = 0
    with open(args.out, mode, newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if write_header:
            writer.writeheader()
        f.flush()
        for i, town in enumerate(towns, 1):
            places = search_town(api_key, town, args.country, max_pages=args.max_pages)
            request_count += min(args.max_pages, max(1, (len(places) + 19) // 20))
            print(f"[{args.country}] {town}: {len(places)} results")
            for p in places:
                row = {
                    "Country": args.country,
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

            processed = args.skip_towns + i
            if args.commit_every and processed % args.commit_every == 0:
                f.flush()
                auto_commit(args.out, processed)

    print(f"\nTotal rows written this run: {total_rows}")
    if total_rows:
        print(f"With website: {total_with_website} ({total_with_website/total_rows:.0%})")
    print(f"Approx API requests used this run: {request_count}")

    if args.commit_every:
        auto_commit(args.out, args.skip_towns + len(towns))


if __name__ == "__main__":
    main()
