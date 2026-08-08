#!/usr/bin/env python3
"""
Dedupes pubs_full.csv and filters out known chain brands by keyword,
NOT by name-repeat count. The name-repeat approach used for restaurants
doesn't work for pubs: traditional pub names (Red Lion, Farmers Arms,
Royal Oak) repeat constantly across genuinely unrelated independent
pubs (false positives), while real chains (Toby Carvery, Harvester,
Brewers Fayre) often give each location a distinct name
("Harvester Gowerton" vs "Harvester Pontypool") so they never repeat
exactly and were missed entirely by a repeat-count filter.

CHAIN_KEYWORDS is a judgment call, not exhaustive -- covers the major
UK managed pub-restaurant chains likely to appear. Spot-check before
a full send.
"""
import csv
from collections import defaultdict

SOURCE = "pubs_full.csv"

CHAIN_KEYWORDS = [
    "wetherspoon", "toby carvery", "beefeater", "brewers fayre",
    "marston's inns", "harvester", "hungry horse", "sizzling pub",
    "vintage inn", "chef & brewer", "chef and brewer", "miller & carter",
    "miller and carter", "craft union", "stonegate", "ember inn",
    "greene king", "flaming grill", "crown carveries",
]


def is_chain(name: str) -> bool:
    lower = name.lower()
    return any(kw in lower for kw in CHAIN_KEYWORDS)


def main():
    with open(SOURCE, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    seen = {}
    for r in rows:
        key = (r["Name"], r["Address"])
        if key not in seen:
            seen[key] = r
    unique = list(seen.values())
    print(f"Raw rows: {len(rows)}  |  unique pubs: {len(unique)}")

    independent = [r for r in unique if not is_chain(r["Name"])]
    chains = [r for r in unique if is_chain(r["Name"])]

    for fname, recs in (("pubs_independent.csv", independent), ("pubs_chains.csv", chains)):
        with open(fname, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["Town", "Name", "Address", "Phone", "Website"])
            writer.writeheader()
            writer.writerows(recs)

    has_web = sum(1 for r in independent if r["Website"])
    print(f"\nIndependent/small: {len(independent)} ({has_web} with website, {has_web/len(independent):.0%})")
    print(f"Chains excluded (keyword match): {len(chains)}")


if __name__ == "__main__":
    main()
