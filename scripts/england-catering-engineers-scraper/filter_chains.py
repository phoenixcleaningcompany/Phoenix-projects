#!/usr/bin/env python3
"""
Dedupes catering_engineers_full.csv (same business often appears under both
query phrasings, and again under a neighbouring town search) and filters out
noise. This vertical's search terms are noisier than restaurants/pubs/hotels
because "catering equipment" text search also pulls in:
  - national wholesalers/distributors (Nisbets, JJ Foodservice, Bidfood, Bunzl...)
  - unrelated trades that happen to share vocabulary: cutlery/knife makers,
    domestic kitchen furniture fitters, generic domestic appliance repair,
    event/marquee hire, PAT testing
Keeps businesses whose name signals actual catering-equipment engineering/
installation/servicing work -- the kind of business that would have its own
technicians on customer sites and could plausibly refer duct cleaning work.
"""
import csv
from collections import defaultdict

SOURCE = "catering_engineers_full.csv"

CHAIN_KEYWORDS = [
    "nisbets", "jj foodservice", "bidfood", "bunzl", "booker", "brakes",
    "brake bros", "3663", "castell howell", "creed foodservice", "musgrave",
    "costco", "makro", "caterchoice", "cater-choice",
]

IRRELEVANT_KEYWORDS = [
    "knives", "knife", "cutlery", "granton",
    "kutchenhaus", "wren kitchens", "howdens", "wickes",
    "event hire", "marquee",
    "pat testing",
    "domestic gas", "domestic boiler", "boiler repair",
    "white goods", "appliance repair",
    "furniture", "canapes", "canapé",
]

POSITIVE_KEYWORDS = [
    "catering", "kitchen", "foodservice", "food service",
    "commercial cook", "commercial oven", "commercial fridge",
    "commercial refrigeration", "commercial kitchen",
]


def is_chain(name: str) -> bool:
    n = name.lower()
    return any(kw in n for kw in CHAIN_KEYWORDS)


def is_irrelevant(name: str) -> bool:
    n = name.lower()
    return any(kw in n for kw in IRRELEVANT_KEYWORDS)


def is_relevant(name: str) -> bool:
    n = name.lower()
    return any(kw in n for kw in POSITIVE_KEYWORDS)


def main():
    with open(SOURCE, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    # dedupe by (Name, Address), keep first occurrence, merge which queries matched
    seen = {}
    order = []
    for r in rows:
        key = (r["Name"], r["Address"])
        if key not in seen:
            seen[key] = r
            order.append(key)
    unique = [seen[k] for k in order]
    print(f"Raw rows: {len(rows)}  |  unique businesses (Name+Address): {len(unique)}")

    chains = [r for r in unique if is_chain(r["Name"])]
    irrelevant = [r for r in unique if not is_chain(r["Name"]) and is_irrelevant(r["Name"])]
    remaining = [r for r in unique if not is_chain(r["Name"]) and not is_irrelevant(r["Name"])]
    relevant = [r for r in remaining if is_relevant(r["Name"])]
    no_signal = [r for r in remaining if not is_relevant(r["Name"])]

    print(f"Excluded as national chain/wholesaler: {len(chains)}")
    print(f"Excluded as irrelevant trade (cutlery/furniture/event hire/PAT/domestic/appliance repair): {len(irrelevant)}")
    print(f"Kept -- name signals catering equipment engineering: {len(relevant)}")
    print(f"Dropped -- no catering/kitchen keyword in name (ambiguous, excluded to be safe): {len(no_signal)}")

    fieldnames = ["Town", "Query", "Name", "Address", "Phone", "Website"]
    with open("catering_engineers_independent.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(relevant)
    with open("catering_engineers_excluded.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames + ["ExcludeReason"])
        writer.writeheader()
        for r in chains:
            writer.writerow({**r, "ExcludeReason": "chain/wholesaler"})
        for r in irrelevant:
            writer.writerow({**r, "ExcludeReason": "irrelevant trade"})
        for r in no_signal:
            writer.writerow({**r, "ExcludeReason": "no catering/kitchen keyword"})

    has_web = sum(1 for r in relevant if r["Website"])
    print(f"\nKept list with website: {has_web} ({has_web/len(relevant):.0%})" if relevant else "")

    print("\nSample of kept businesses:")
    for r in relevant[:15]:
        print(f"  {r['Name'][:50]:50s} {r['Town']}")


if __name__ == "__main__":
    main()
