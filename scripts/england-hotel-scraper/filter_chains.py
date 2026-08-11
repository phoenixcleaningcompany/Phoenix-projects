#!/usr/bin/env python3
"""
Dedupes hotels_full.csv (very heavy overlap between neighboring town
searches for this category -- even small villages hit the 60-result cap)
and filters chain brands by keyword, same reasoning as the pub filter:
hotel chains are heavily and consistently branded (Premier Inn, Holiday
Inn, Best Western) so keyword matching is reliable and simpler than
trying to infer chains from name repetition.
"""
import csv

SOURCE = "hotels_full.csv"

CHAIN_KEYWORDS = [
    "premier inn", "travelodge", "holiday inn", "best western", "ibis",
    "mercure", "novotel", "hilton", "marriott", "doubletree", "village hotel",
    "village urban resort", "macdonald hotel", "britannia hotel", "ramada",
    "days inn", "crowne plaza", "radisson", "hallmark hotel", "wetherspoon",
    "accor", "qhotels", "iq hotel",
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
    print(f"Raw rows: {len(rows)}  |  unique hotels: {len(unique)}")

    independent = [r for r in unique if not is_chain(r["Name"])]
    chains = [r for r in unique if is_chain(r["Name"])]

    for fname, recs in (("hotels_independent.csv", independent), ("hotels_chains.csv", chains)):
        with open(fname, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["Town", "Name", "Address", "Phone", "Website"])
            writer.writeheader()
            writer.writerows(recs)

    has_web = sum(1 for r in independent if r["Website"])
    print(f"\nIndependent/small: {len(independent)} ({has_web} with website, {has_web/len(independent):.0%})")
    print(f"Chains excluded (keyword match): {len(chains)}")


if __name__ == "__main__":
    main()
