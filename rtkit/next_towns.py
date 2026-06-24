#!/usr/bin/env python3
"""next_towns.py - print the next N unbuilt towns (CSV rank order), grouped.

Unbuilt = on RT_towns.csv but not yet a key in rt_build.TOWNS. Git state (the
TOWNS dict) is the single source of progress truth, so this is resume-safe.

Usage: python3 next_towns.py [N] [GROUPS]   (default N=48, GROUPS=8)
Prints: remaining count, then GROUPS lines, each "g{i}: Town | Town | ...".
"""
import csv, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import rt_build  # noqa

N = int(sys.argv[1]) if len(sys.argv) > 1 else 48
GROUPS = int(sys.argv[2]) if len(sys.argv) > 2 else 8

rows = list(csv.DictReader(open(os.path.join(HERE, "RT_towns.csv"), encoding="utf-8-sig")))
built = set(rt_build.TOWNS)  # lowercased keys
remaining = [(int(r["Rank"]), r["Town"].strip()) for r in rows
             if r["Town"].strip().lower() not in built and r["Town"].strip().lower() != "london"]
remaining.sort()
total_remaining = len(remaining)
batch = [t for _, t in remaining[:N]]

print(f"REMAINING={total_remaining}  TAKING={len(batch)}  BUILT={len(built)}")
# round-robin into GROUPS so each agent gets a spread of ranks (mix big/small towns)
buckets = [[] for _ in range(GROUPS)]
for i, t in enumerate(batch):
    buckets[i % GROUPS].append(t)
for i, b in enumerate(buckets, 1):
    if b:
        print(f"g{i}: " + " | ".join(b))
