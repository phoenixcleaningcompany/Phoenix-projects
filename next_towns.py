#!/usr/bin/env python3
"""next_towns.py - batch planner / validator for the CH2 series (resume-safe).

Usage:
  python3 next_towns.py            # how many done, how many left
  python3 next_towns.py --done     # list slugs already in TOWNS (built)
  python3 next_towns.py 56         # next 56 town names by rank not yet in TOWNS
  python3 next_towns.py --slugs 56 # same, as ch2-<slug> filenames
  python3 next_towns.py --check    # validate every TOWNS nearby is on CH2_towns.csv

Progress = membership of TOWNS (seed literal + towns/*.json). London (rank 1) is
the hand-authored flagship and is never a build target.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ch2_build as B

def csv_rows():
    return sorted(B._load_csv(), key=lambda r: r[0])  # (rank, town, nation)

def done_slugs():
    return {B.slugify(k) for k in B.TOWNS}

def remaining():
    done = done_slugs()
    out = []
    for _r, town, _n in csv_rows():
        s = B.slugify(town)
        if s == 'london' or s in done:
            continue
        out.append(town)
    return out

def check():
    csv_names = {r[1].lower() for r in B._load_csv()}
    bad = 0
    for k, v in B.TOWNS.items():
        if B.slugify(k) == 'london':
            continue
        nb = v.get('nearby', [])
        if len(nb) != 3:
            print(f"  {k}: nearby has {len(nb)} (need 3)"); bad += 1
        for n in nb:
            if n.lower() not in csv_names:
                print(f"  {k}: nearby '{n}' not on CSV"); bad += 1
    print(f"--check: {'OK' if not bad else str(bad)+' problem(s)'} across {len(B.TOWNS)} towns")
    return bad

def main():
    a = sys.argv[1:]
    if a and a[0] == '--check':
        sys.exit(1 if check() else 0)
    if a and a[0] == '--done':
        for s in sorted(done_slugs()):
            print(s)
        return
    rem = remaining()
    if a and a[0] == '--slugs':
        n = int(a[1]) if len(a) > 1 else len(rem)
        for t in rem[:n]:
            print(f"ch2-{B.slugify(t)}")
        return
    if a and a[0].isdigit():
        for t in rem[:int(a[0])]:
            print(t)
        return
    total = len([r for r in csv_rows() if B.slugify(r[1]) != 'london'])
    print(f"done={len(done_slugs())-(1 if 'london' in done_slugs() else 0)}  "
          f"left={len(rem)}  buildable_total={total}")

if __name__ == '__main__':
    main()
