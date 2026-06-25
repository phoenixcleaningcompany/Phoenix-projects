#!/usr/bin/env python3
"""next_towns.py - print the next N unbuilt BH towns in CSV rank order, grouped.

Unbuilt = on BH_towns.csv but NOT yet a key in bh_build.TOWNS, so git state IS
your progress (commit each batch and this always resumes correctly after a reset).

Usage:  python3 next_towns.py [N] [G]
        N = how many towns (default 56)   G = how many agent groups (default 8)
London (the flagship) is always skipped.
"""
import os, re, sys, csv

HERE = os.path.dirname(os.path.abspath(__file__))


def built_keys():
    src = open(os.path.join(HERE, "bh_build.py"), encoding="utf-8").read()
    block = src[src.index("TOWNS = {"):src.index("# === CSV / nearby")]
    return {k.lower() for k in re.findall(r'\n [ ]?"([^"]+)":\s*\{', block)}


def csv_rows():
    with open(os.path.join(HERE, "BH_towns.csv"), newline="", encoding="utf-8-sig") as f:
        return [(int(r["Rank"]), r["Town"].strip()) for r in csv.DictReader(f)]


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 56
    g = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    done = built_keys()
    rows = sorted(csv_rows())
    remaining = [t for _, t in rows if t.lower() not in done and t.lower() != "london"]
    batch = remaining[:n]
    print(f"REMAINING (unbuilt): {len(remaining)}   |   this batch: {len(batch)}")
    if not batch:
        print("Nothing to build - all CSV towns are in TOWNS.")
        return
    groups = [[] for _ in range(g)]
    for i, t in enumerate(batch):           # round-robin by rank = even spread
        groups[i % g].append(t)
    for i, grp in enumerate(groups):
        if grp:
            print(f"\n-- group {i} ({len(grp)}): " + " | ".join(grp))


if __name__ == "__main__":
    main()
