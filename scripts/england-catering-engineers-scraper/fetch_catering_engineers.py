#!/usr/bin/env python3
"""
Pulls catering engineers / commercial catering equipment servicing
businesses per England town from Google Places API (New) Text Search.

Runs BOTH query phrasings per town (the pilot showed they only overlap
~35% -- each catches businesses the other misses):
  Query A: "catering engineers in {town}, England"
  Query B: "commercial catering equipment repair in {town}, England"

Reads the API key from the PLACES_API_KEY environment variable -- never
hardcode it in this file or any committed output.

Auto-commits/pushes the output file every --commit-every towns, since this
is a long run and the execution environment restarts unpredictably.

Usage:
  PLACES_API_KEY=xxx python3 fetch_catering_engineers.py --towns ../england_towns_full.txt --out catering_engineers_full.csv --commit-every 25
  PLACES_API_KEY=xxx python3 fetch_catering_engineers.py --towns ../england_towns_full.txt --out catering_engineers_full.csv --skip-towns 150   # resume
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


def auto_commit(out_path, processed_count):
    repo_root = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True,
        cwd=os.path.dirname(os.path.abspath(out_path)) or "."
    ).stdout.strip()
    try:
        abs_out_path = os.path.abspath(out_path)
        subprocess.run(["git", "add", "-f", abs_out_path], cwd=repo_root, check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", f"Auto-checkpoint: catering engineers, {processed_count} towns processed"],
                        cwd=repo_root, check=True, capture_output=True)
        subprocess.run(["git", "push"], cwd=repo_root, check=True, capture_output=True, timeout=30)
        print(f"  [checkpoint committed and pushed at {processed_count} towns]", file=sys.stderr)
    except Exception as e:
        print(f"  [auto-checkpoint failed, continuing anyway: {e}]", file=sys.stderr)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--towns", required=True, help="text file, one town per line")
    ap.add_argument("--out", required=True)
    ap.add_argument("--max-pages", type=int, default=3)
    ap.add_argument("--skip-towns", type=int, default=0, help="skip this many already-processed towns and append to --out")
    ap.add_argument("--commit-every", type=int, default=0, help="git add/commit/push the --out file every N towns")
    args = ap.parse_args()

    api_key = os.environ.get("PLACES_API_KEY")
    if not api_key:
        raise SystemExit("Set PLACES_API_KEY environment variable")

    with open(args.towns) as f:
        towns = [line.strip() for line in f if line.strip()]
    if args.skip_towns:
        towns = towns[args.skip_towns:]

    fieldnames = ["Town", "Query", "Name", "Address", "Phone", "Website"]
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
        for i, town in enumerate(towns, 1):
            for label, template in QUERIES.items():
                places = search(api_key, template.format(town=town), max_pages=args.max_pages)
                request_count += min(args.max_pages, max(1, (len(places) + 19) // 20))
                print(f"[{label}] {town}: {len(places)} results")
                for p in places:
                    row = {
                        "Town": town,
                        "Query": label,
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
