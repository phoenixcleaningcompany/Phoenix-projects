#!/usr/bin/env python3
"""
Dedupes pubs_full.csv and filters chain brands by keyword, not
name-repeat count -- same fix applied to the pub/hotel lists. At England
scale, the name-repeat approach caught real chains (PizzaExpress, M&S
Foodhall, McDonald's) but also heavily false-flagged generic pub-restaurant
names (Red Lion, White Hart, Royal Oak, Crown, Swan) that repeat across
many unrelated independents nationwide, not because they're a chain.

CHAIN_KEYWORDS is a judgment call, not exhaustive -- covers major UK
restaurant/casual-dining chains likely to appear at national scale.
Spot-check before a full send.
"""
import csv

SOURCE = "pubs_full.csv"

CHAIN_KEYWORDS = [
    "pizzaexpress", "pizza express", "nando's", "nandos", "wagamama",
    "zizzi", "bella italia", "frankie & benny's", "frankie and benny's",
    "tgi friday", "harvester", "beefeater", "toby carvery",
    "miller & carter", "miller and carter", "chiquito", "las iguanas",
    "turtle bay", "wetherspoon", "prezzo", "ask italian", "cote brasserie",
    "côte brasserie", "franco manca", "byron", "five guys", "mcdonald's",
    "mcdonalds", "burger king", "kfc", "subway", "greggs", "popeyes",
    "chaiiwala", "costa coffee", "starbucks", "caffe nero", "caffè nero",
    "m&s foodhall", "morrisons cafe", "tesco cafe", "sainsbury's cafe",
    "yo! sushi", "yo sushi", "itsu", "leon", "pret a manger",
    "slim chickens", "wingstop", "rossopomodoro", "bill's restaurant",
    "browns restaurant", "the ivy asia", "the ivy collection", "gaucho",
    "banana tree", "carluccio's", "cafe rouge", "café rouge",
    "brasserie blanc", "loch fyne", "harry ramsden's", "papa john's",
    "domino's", "pizza hut", "cosy club", "wahaca",
    "greene king", "sizzling pub", "ember inn", "vintage inn",
    "chef & brewer", "chef and brewer", "craft union", "stonegate",
    "hungry horse", "marston's inns", "hallmark hotel", "flaming grill",
    "crown carveries", "brewers fayre",
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
    print(f"Raw rows: {len(rows)}  |  unique restaurants: {len(unique)}")

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
