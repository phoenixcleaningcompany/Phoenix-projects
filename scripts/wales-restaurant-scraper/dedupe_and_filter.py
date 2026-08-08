#!/usr/bin/env python3
"""
Dedupes restaurants_full.csv (many entries appear under multiple
neighboring-town searches, since Google's search radius overlaps for
towns close together) and splits into independent/small-chain vs
large-chain, same logic as the care home lists -- avoid the heavy-use
national chains Phoenix doesn't want (Prezzo, Cosy Club, Slim Chickens,
etc.), keep independents and small local operators.

CHAIN_THRESHOLD: a name appearing at 4+ distinct addresses nationally is
treated as a chain. This only works now that we have full 216-town
coverage -- with just the 10-town pilot there wasn't enough data to tell
a real chain from two unrelated pubs sharing a common name.
"""
import csv
from collections import defaultdict, Counter

SOURCE = "restaurants_full.csv"
CHAIN_THRESHOLD = 4


def main():
    with open(SOURCE, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    # dedupe by (Name, Address), keep first occurrence
    seen = {}
    for r in rows:
        key = (r["Name"], r["Address"])
        if key not in seen:
            seen[key] = r
    unique = list(seen.values())
    print(f"Raw rows: {len(rows)}  |  unique restaurants: {len(unique)}")

    name_counts = Counter(r["Name"] for r in unique)
    chains = {name for name, c in name_counts.items() if c >= CHAIN_THRESHOLD}
    print(f"Names appearing at {CHAIN_THRESHOLD}+ distinct addresses (treated as chains): {len(chains)}")

    independent = [r for r in unique if r["Name"] not in chains]
    chain_rows = [r for r in unique if r["Name"] in chains]

    for fname, recs in (("restaurants_independent.csv", independent), ("restaurants_chains.csv", chain_rows)):
        with open(fname, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["Town", "Name", "Address", "Phone", "Website"])
            writer.writeheader()
            writer.writerows(recs)

    has_web = sum(1 for r in independent if r["Website"])
    print(f"\nIndependent/small: {len(independent)} ({has_web} with website, {has_web/len(independent):.0%})")
    print(f"Chains (excluded): {len(chain_rows)}")
    print("\nTop chain names excluded:")
    for name, c in name_counts.most_common(20):
        if name in chains:
            print(f"  {c:3d}  {name}")


if __name__ == "__main__":
    main()
