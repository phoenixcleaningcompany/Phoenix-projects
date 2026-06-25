#!/usr/bin/env python3
"""next_towns.py - batch planner / validator for the TC series.

Progress is defined by membership of tc_build.TOWNS, so this resumes
correctly after any reset. London (rank 1) is the hand-authored flagship and
is never a build target.

Usage:
  python3 next_towns.py [N]          # next N towns by rank not yet in TOWNS
  python3 next_towns.py --done       # how many built / remaining
  python3 next_towns.py --check      # validate every TOWNS nearby is on CSV (3, geographic)
  python3 next_towns.py --slugs [N]  # space-joined CLI args for tc_build.py
"""
import sys, csv, os
import tc_build as B

HERE = os.path.dirname(os.path.abspath(__file__))


def csv_rows():
    for p in (os.path.join(HERE, 'TC_towns.csv'), 'TC_towns.csv'):
        if os.path.exists(p):
            with open(p, newline='', encoding='utf-8-sig') as f:
                return [(int(r['Rank']), r['Town'].strip(), (r.get('Nation') or '').strip())
                        for r in csv.DictReader(f)]
    sys.exit('TC_towns.csv not found')


def built_slugs():
    return {B.slugify(k) for k in B.TOWNS}


def remaining():
    done = built_slugs()
    out = []
    for rank, town, _nat in sorted(csv_rows()):
        if town.lower() == 'london':
            continue
        if B.slugify(town) not in done:
            out.append((rank, town))
    return out


def check():
    csv_names = {t.lower() for _r, t, _n in csv_rows()}
    bad = []
    for key, T in B.TOWNS.items():
        nb = T.get('nearby') or []
        if len(nb) != 3:
            bad.append((key, f'nearby count {len(nb)} (need 3)'))
        for n in nb:
            if n.lower() not in csv_names:
                bad.append((key, f'nearby off-CSV: {n!r}'))
    if bad:
        for k, m in bad:
            print(f'BAD  {k}: {m}')
        print(f'\n{len(bad)} problem(s)')
        sys.exit(1)
    print(f'OK - all {len(B.TOWNS)} TOWNS have 3 on-CSV nearby links')


def main():
    a = sys.argv[1:]
    if a and a[0] == '--check':
        return check()
    if a and a[0] == '--done':
        done = len(built_slugs()) - (1 if 'london' in built_slugs() else 0)
        rem = len(remaining())
        print(f'built {done} towns, {rem} remaining (of 504)')
        return
    slugs = a and a[0] == '--slugs'
    if slugs:
        a = a[1:]
    n = int(a[0]) if a else 56
    nxt = remaining()[:n]
    if slugs:
        print(' '.join(f'"{t}"' for _r, t in nxt))
    else:
        for rank, town in nxt:
            print(f'{rank:4d}  {town}')


if __name__ == '__main__':
    main()
