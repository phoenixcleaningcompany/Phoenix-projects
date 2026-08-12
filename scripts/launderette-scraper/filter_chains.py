#!/usr/bin/env python3
"""
Dedupes launderettes_full.csv and filters out national chains/franchises.

Unlike the pub/restaurant lists, this trade has very few real chains -- most
repeated names (Launderette, The Launderette, Bubbles, The Wash House, etc.)
are generic descriptive names independent operators happen to share, not
actual chains (the same false-positive trap the pub scraper hit early on --
see wales-pub-scraper notes). Confirmed real chains, checked against their
actual addresses before excluding:
  - Revolution Laundry / Revolution Launderette -- national self-service chain
  - Timpson -- national multi-service franchise (shoes/keys/dry cleaning)
  - Johnsons (The) Cleaners -- national dry cleaning chain
  - Elis -- large B2B industrial linen/laundry services company, not a public
    launderette at all (checked every "Elis" row -- all same company)
  - Morrisons -- supermarket, a query mismatch not a launderette
"""
import csv

SOURCE = "launderettes_full.csv"

CHAIN_EXACT_NAMES = {
    "elis", "morrisons", "timpson",
}

CHAIN_SUBSTRINGS = [
    "revolution laundry", "revolution launderette", "launderette revolution",
    "johnsons the cleaners", "johnsons cleaners",
]


def is_chain(name: str) -> bool:
    n = name.strip().lower()
    if n in CHAIN_EXACT_NAMES:
        return True
    return any(kw in n for kw in CHAIN_SUBSTRINGS)


def main():
    with open(SOURCE, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

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
    independent = [r for r in unique if not is_chain(r["Name"])]

    print(f"Excluded as national chain: {len(chains)}")
    print(f"Kept as independent/local: {len(independent)}")

    fieldnames = ["Country", "Town", "Name", "Address", "Phone", "Website"]
    with open("launderettes_independent.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(independent)
    with open("launderettes_chains.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(chains)

    has_web = sum(1 for r in independent if r["Website"])
    print(f"Independent list with website: {has_web} ({has_web/len(independent):.0%})")

    print("\nTop excluded chain names:")
    from collections import Counter
    c = Counter(r["Name"] for r in chains)
    for name, count in c.most_common(10):
        print(f"  {count:3d}  {name}")


if __name__ == "__main__":
    main()
