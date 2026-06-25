#!/usr/bin/env python3
"""diag_vt.py - over-cap-pair diagnostic for the TC series.

When score_tc.py reports a pair over the 52% cap, this isolates exactly what
the two pages share: it takes the shared 5-gram shingles of the pair and
SUBTRACTS the shingles of a third (control) page, so corpus-constant
boilerplate drops out and only the variant sentences the pair collided on
remain, stitched into readable runs.

Fix per SPEC 8.3: add researched, proper-noun-rich local detail to the weaker
page's s1loc (~40-70 words moves a pair ~2-3 points). Do NOT reword distinctive
local prose into generic phrasing.

Usage:
  python3 diag_vt.py                      # worst over-cap pair in outputs/
  python3 diag_vt.py outputs              # worst over-cap pair in a folder
  python3 diag_vt.py tc-a.html tc-b.html  # a specific pair (control auto-picked)
  python3 diag_vt.py tc-a.html tc-b.html tc-c.html   # explicit control = c
"""
import os, sys, glob
from itertools import combinations
import score_tc as S


def load(path):
    txt = open(path, encoding='utf-8', errors='replace').read()
    return S.shingles(S.normalise(S.strip(txt), S.town_of(path)))


def stitch(shared):
    if not shared:
        return []
    grams = sorted(shared)
    runs, used = [], set()
    for g in grams:
        if g in used:
            continue
        words = g.split()
        used.add(g)
        while True:
            tail = ' '.join(words[-(S.SHINGLE - 1):])
            nxt = next((h for h in grams if h not in used and h.startswith(tail + ' ')), None)
            if not nxt:
                break
            words.append(nxt.split()[-1]); used.add(nxt)
        runs.append(' '.join(words))
    runs.sort(key=lambda r: len(r.split()), reverse=True)
    return runs


def collect(args):
    paths = []
    for a in args:
        if os.path.isdir(a):
            paths += sorted(glob.glob(os.path.join(a, "tc-*.html")))
        elif os.path.isfile(a):
            paths.append(a)
        else:
            paths += sorted(glob.glob(a))
    return [p for p in dict.fromkeys(paths) if os.path.isfile(p)]


def dup(sa, sb):
    inter = len(sa & sb); union = len(sa | sb) or 1
    return 100.0 * inter / union, inter, union


def main():
    args = sys.argv[1:] or ["outputs"]
    files = [a for a in args if os.path.isfile(a) and a.endswith('.html')]
    if len(files) >= 2:
        a, b = files[0], files[1]
        control = files[2] if len(files) >= 3 else None
        pool = collect(["outputs"]) if not control else []
    else:
        paths = collect(args)
        if len(paths) < 2:
            sys.exit("need at least 2 tc-*.html files")
        docs = {p: load(p) for p in paths}
        worst = max(combinations(paths, 2), key=lambda ab: dup(docs[ab[0]], docs[ab[1]])[0])
        a, b = worst
        control = None
        pool = paths

    sa, sb = load(a), load(b)
    d, inter, union = dup(sa, sb)
    print(f"pair: {os.path.basename(a)}  vs  {os.path.basename(b)}")
    print(f"raw pairwise dup: {d:.1f}%   (shared {inter}, union {union}, cap {S.MAX_PAIR:.0f}%)")

    shared = sa & sb
    if control is None:
        cand = [p for p in pool if os.path.abspath(p) not in (os.path.abspath(a), os.path.abspath(b))]
        control = cand[0] if cand else None
    if control:
        sc = load(control)
        specific = shared - sc
        print(f"control page (boilerplate subtracted): {os.path.basename(control)}")
        print(f"pair-specific shared shingles: {len(specific)}  (of {len(shared)} total shared)")
    else:
        specific = shared
        print("no control page available - showing all shared shingles")

    runs = stitch(specific)
    print(f"\ncolliding runs the pair specifically shares ({len(runs)} runs):")
    for r in runs[:40]:
        print(f"   [{len(r.split()):>2}] {r}")

    target = S.MAX_PAIR / 100.0
    need = max(0, int(round(inter / target - union)))
    weaker = a if len(sa) <= len(sb) else b
    print(f"\nto clear {S.MAX_PAIR:.0f}%: add ~{need} unique shingles (~{need} researched words)"
          f" to the weaker page ({os.path.basename(weaker)}).")
    print("Add proper-noun-rich local detail to its s1loc; do not reword to generic phrasing (SPEC 8.3).")


if __name__ == "__main__":
    main()
