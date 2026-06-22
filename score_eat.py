#!/usr/bin/env python3
"""score_eat.py - uniqueness scorer for EAT pages (diagnostic, not the gate).

Usage:  python3 score_eat.py [folder|globs]    default: /mnt/user-data/outputs

Strips chrome, SVG, JSON-LD and the (pooled, shared) cleaning-pivot section,
then masks the town name so pages are compared on EDITORIAL substance: the four
researched venues, the food-scene write-up, the visit notes and the FAQ. Those
are the real uniqueness lever.

Pass conditions (advisory):
  overall unique >= FLOOR (70.0)   and   worst pair dup <= MAX_PAIR (50.0)
Hard checks (verify_eat) are the binding gate; do not chase FLOOR at small N.
"""
import os, re, sys, glob
from itertools import combinations

FLOOR = 70.0
MAX_PAIR = 50.0
SHINGLE = 5


def _cut(html, open_pat, tag):
    """Remove every <tag> whose opening matches open_pat, through its balanced close."""
    out, i = [], 0
    op = re.compile(open_pat, re.I)
    tagre = re.compile(r'<(/?)' + tag + r'\b[^>]*>', re.I)
    while True:
        m = op.search(html, i)
        if not m:
            out.append(html[i:]); break
        out.append(html[i:m.start()])
        depth, j = 1, m.end()
        while depth and j < len(html):
            t = tagre.search(html, j)
            if not t:
                j = len(html); break
            depth += -1 if t.group(1) else 1
            j = t.end()
        i = j
    return "".join(out)


def strip(html):
    for tag in ("script", "style", "svg", "header", "footer"):
        html = re.sub(rf'<{tag}\b.*?</{tag}>', ' ', html, flags=re.I | re.S)
    # shared / pooled / chrome blocks
    html = _cut(html, r'<section[^>]*class="[^"]*\bhero\b', 'section')
    html = _cut(html, r'<section[^>]*id="kitchens"', 'section')      # pooled pivot
    html = _cut(html, r'<section[^>]*class="[^"]*\bcta-section\b', 'section')
    html = _cut(html, r'<section[^>]*class="[^"]*\brelated-section\b', 'section')
    html = _cut(html, r'<nav\b', 'nav')                               # jump links
    for cls in ("alert-band", "stat-row", "mid-cta", "cert-strip"):
        html = _cut(html, r'<div[^>]*class="[^"]*\b' + cls + r'\b', 'div')
    return re.sub(r'<[^>]+>', ' ', html)


def town_of(path):
    m = re.match(r'eat-(.+)\.html$', os.path.basename(path), re.I)
    return (m.group(1) if m else os.path.basename(path)).replace('-', ' ')


def normalise(text, town):
    text = text.lower()
    for form in {town.lower(), town.lower().replace(' ', '-'), town.lower().replace(' ', '')}:
        if form:
            text = text.replace(form, ' townx ')
    text = re.sub(r'[^a-z0-9 ]+', ' ', text)
    return re.sub(r'\s+', ' ', text).strip()


def shingles(text):
    w = text.split()
    return {' '.join(w[i:i + SHINGLE]) for i in range(len(w) - SHINGLE + 1)} if len(w) >= SHINGLE else set()


def collect(args):
    paths = []
    for a in args:
        if os.path.isdir(a):
            paths += sorted(glob.glob(os.path.join(a, "eat-*.html")))
        else:
            paths += sorted(glob.glob(a))
    return [p for p in dict.fromkeys(paths) if os.path.isfile(p)]


def main():
    args = sys.argv[1:] or ["/mnt/user-data/outputs"]
    paths = collect(args)
    if len(paths) < 2:
        if paths:
            sh = shingles(normalise(strip(open(paths[0], encoding='utf-8').read()), town_of(paths[0])))
            print(f"{os.path.basename(paths[0])}: {len(sh)} editorial shingles (need 2+ files to compare)")
        else:
            print("No eat-*.html files found.")
        sys.exit(0)

    docs = {}
    for p in paths:
        sh = shingles(normalise(strip(open(p, encoding='utf-8', errors='replace').read()), town_of(p)))
        if sh: docs[p] = sh
        else:  print(f"warn: {os.path.basename(p)} too short to score")

    names = list(docs)
    pair_rows, worst, worst_pair = [], 0.0, None
    for a, b in combinations(names, 2):
        inter = len(docs[a] & docs[b]); union = len(docs[a] | docs[b]) or 1
        d = 100.0 * inter / union
        pair_rows.append((d, a, b))
        if d > worst: worst, worst_pair = d, (a, b)

    uniq = {}
    for a in names:
        others = set().union(*(docs[b] for b in names if b != a)) if len(names) > 1 else set()
        uniq[a] = 100.0 * len(docs[a] - others) / (len(docs[a]) or 1)
    mean_dup = sum(r[0] for r in pair_rows) / len(pair_rows)
    overall = 100.0 - mean_dup

    print("Per-page uniqueness (editorial shingles unique to that page):")
    for a in names:
        print(f"  {uniq[a]:5.1f}%  {os.path.basename(a)}")
    print(f"\nMean pair dup  : {mean_dup:.1f}%")
    print(f"Overall unique : {overall:.1f}%   (floor {FLOOR:.0f}%)")
    print(f"Worst pair dup : {worst:.1f}%   (max {MAX_PAIR:.0f}%)")
    if worst_pair:
        print(f"   {os.path.basename(worst_pair[0])}  vs  {os.path.basename(worst_pair[1])}")
    over = [r for r in sorted(pair_rows, reverse=True) if r[0] > MAX_PAIR]
    if over:
        print(f"\nPairs over {MAX_PAIR:.0f}%:")
        for d, a, b in over:
            print(f"   {d:5.1f}%  {os.path.basename(a)} vs {os.path.basename(b)}")
    ok = overall >= FLOOR and worst <= MAX_PAIR
    print("\n==== " + ("PASS" if ok else "BELOW FLOOR (advisory)") + " ====")
    sys.exit(0)


if __name__ == "__main__":
    main()
