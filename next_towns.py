#!/usr/bin/env python3
"""next_towns.py - resume-safe batch planner for the TL series.

Progress == membership of tl_build.TOWNS (seed literal + towns/*.json). The
build is deterministic, so after any context reset / filesystem rebuild this
reports exactly what is done and what is left, in population-rank order.

Usage:
  python3 next_towns.py              # summary: done / left
  python3 next_towns.py N            # next N town names by rank (not yet built)
  python3 next_towns.py --slugs N    # next N as tl- slugs (build args)
  python3 next_towns.py --done       # list the towns already in TOWNS
  python3 next_towns.py --check      # validate every nearby in TOWNS is on CSV
"""
import sys
import tl_build as b

LONDON = "london"  # flagship: hand-authored, never a build target


def csv_order():
    # [(rank, town, nation)] sorted by rank
    return sorted(b._load_csv(), key=lambda r: r[0])


def done_slugs():
    return {b.slugify(k) for k in b.TOWNS}


def main():
    rows = csv_order()
    done = done_slugs()
    # "left" = on CSV, not London, not already in TOWNS
    left = [(r, t, n) for (r, t, n) in rows
            if b.slugify(t) != LONDON and b.slugify(t) not in done]
    built = [(r, t, n) for (r, t, n) in rows
             if b.slugify(t) != LONDON and b.slugify(t) in done]

    args = sys.argv[1:]

    if args and args[0] == "--check":
        bad = 0
        csv_names = {t.lower() for (_r, t, _n) in rows}
        for k, T in b.TOWNS.items():
            nb = T.get("nearby") or []
            if len(nb) != 3:
                print(f"SHAPE {k}: nearby has {len(nb)} (need 3)"); bad += 1
            for x in nb:
                if x.lower() not in csv_names:
                    print(f"OFF-CSV {k}: nearby '{x}' not on TL_towns.csv"); bad += 1
        print(f"checked {len(b.TOWNS)} towns; nearby issues = {bad}")
        sys.exit(1 if bad else 0)

    if args and args[0] == "--done":
        for r, t, n in built:
            print(f"{r:>3}  {t}")
        print(f"\n{len(built)} built, {len(left)} left (of {len(rows) - 1} towns, London excluded)")
        return

    if args and args[0] == "--slugs":
        n = int(args[1]) if len(args) > 1 else 56
        for r, t, _n in left[:n]:
            print(f"tl-{b.slugify(t)}")
        return

    if args and args[0].lstrip("-").isdigit():
        n = int(args[0])
        for r, t, _n in left[:n]:
            print(f"{r:>3}  {t}")
        return

    # default summary
    print(f"TOTAL towns (excl. London flagship): {len(rows) - 1}")
    print(f"BUILT (in TOWNS): {len(built)}")
    print(f"LEFT:  {len(left)}")
    if left:
        nxt = left[:10]
        print("\nnext up (by rank):")
        for r, t, _n in nxt:
            print(f"  {r:>3}  {t}")


if __name__ == "__main__":
    main()
