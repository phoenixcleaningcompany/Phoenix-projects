#!/usr/bin/env python3
"""next_towns.py - print the next N unbuilt VT towns (CSV rank order), grouped
into G agent groups (round-robin by rank so each group gets a population spread).

unbuilt = a town on VT_towns.csv that is NOT yet a key in vt_build.TOWNS (and is
not the London flagship). The TOWNS dict in vt_build.py is therefore the progress
ledger - git state IS progress, so this resumes correctly after any context or
filesystem reset.

Usage:  python3 next_towns.py [N] [G]      defaults N=56 G=8
"""
import sys
import vt_build as B


def main():
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 56
    G = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    built = {k.lower() for k in B.TOWNS} | {"london"}
    rows = sorted(B._load_csv(), key=lambda r: r[0])          # by population rank
    unbuilt = [town for _, town, _ in rows if town.lower() not in built]
    batch = unbuilt[:N]
    groups = [[] for _ in range(G)]
    for i, town in enumerate(batch):
        groups[i % G].append(town)

    print(f"REMAINING (unbuilt, excl. flagship): {len(unbuilt)}")
    print(f"BUILT (in TOWNS, excl. flagship): {len(built) - 1}")
    print(f"This batch: {len(batch)} towns into {min(G, len(batch))} groups\n")
    for i, g in enumerate(groups):
        if g:
            print(f"group {i} ({len(g)}): " + ", ".join(g))
    return 0


if __name__ == "__main__":
    sys.exit(main())
