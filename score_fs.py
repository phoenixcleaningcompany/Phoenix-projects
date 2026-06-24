#!/usr/bin/env python3
"""scofs_re.py - sentence-level uniqueness scorer for FS (Forestry, Arboriculture & Tree Surgery) workwear pages.

Usage:  python3 scofs_re.py outputs/fs-*.html
        python3 scofs_re.py outputs            (folder = all fs-*.html)

Strips chrome, SVG and JSON-LD, then masks ONLY the town name so towns are
compared on editorial substance. Real local nouns (office estates, business
districts, NHS trusts, universities, councils, retail and industrial sites)
count as genuine unique content - the main uniqueness lever.

Pass conditions:
  - overall unique  >= FLOOR     (default 77.0)
  - worst pair dup  <= MAX_PAIR  (default 52.0)
"""
import os, re, sys, glob
from itertools import combinations

FLOOR = 77.0
MAX_PAIR = 52.0
SHINGLE = 5
MIN_WORDS = 5

CHROME = ["fs-header", "fs-trust-strip", "fs-stats", "fs-jump-links",
          "fs-cta-bar", "fs-contact-block", "fs-footer", "fs-nearby",
          "fs-contract", "fs-product-grid"]


def remove_div(html, cls):
    out, i = [], 0
    pat = re.compile(r'<div[^>]*class="[^"]*\b' + re.escape(cls) + r'\b[^"]*"[^>]*>', re.I)
    while True:
        m = pat.search(html, i)
        if not m:
            out.append(html[i:]); break
        out.append(html[i:m.start()])
        depth, j = 1, m.end()
        tag = re.compile(r'<(/?)div\b[^>]*>', re.I)
        while depth and j < len(html):
            t = tag.search(html, j)
            if not t:
                j = len(html); break
            depth += -1 if t.group(1) else 1
            j = t.end()
        i = j
    return "".join(out)


def footer_tag(html):
    return re.sub(r'<footer\b.*?</footer>', ' ', html, flags=re.I | re.S)


def strip(html):
    html = re.sub(r'<script\b.*?</script>', ' ', html, flags=re.I | re.S)
    html = re.sub(r'<style\b.*?</style>', ' ', html, flags=re.I | re.S)
    html = re.sub(r'<svg\b.*?</svg>', ' ', html, flags=re.I | re.S)
    html = re.sub(r'<div class="fs-illust-caption">.*?</div>', ' ', html, flags=re.I | re.S)
    html = footer_tag(html)
    for c in CHROME:
        html = remove_div(html, c)
    text = re.sub(r'<[^>]+>', ' ', html)
    return text


def town_of(path):
    base = os.path.basename(path)
    m = re.match(r'fs-(.+)\.html$', base, re.I)
    return (m.group(1) if m else base).replace('-', ' ')


def normalise(text, town):
    text = text.lower()
    for form in {town.lower(), town.lower().replace(' ', '-'), town.lower().replace(' ', '')}:
        if form:
            text = text.replace(form, ' townx ')
    text = re.sub(r'[^a-z0-9 ]+', ' ', text)
    return re.sub(r'\s+', ' ', text).strip()


def shingles(text):
    w = text.split()
    if len(w) < SHINGLE:
        return set()
    return {' '.join(w[i:i + SHINGLE]) for i in range(len(w) - SHINGLE + 1)}


def collect(args):
    paths = []
    for a in args:
        if os.path.isdir(a):
            paths += sorted(glob.glob(os.path.join(a, "fs-*.html")))
        else:
            paths += sorted(glob.glob(a))
    return [p for p in dict.fromkeys(paths) if os.path.isfile(p)]


def main():
    args = sys.argv[1:] or ["outputs"]
    paths = collect(args)
    if len(paths) < 2:
        print(f"Need at least 2 fs-*.html files to compare (found {len(paths)}).")
        if paths:
            sh = shingles(normalise(strip(open(paths[0], encoding='utf-8').read()), town_of(paths[0])))
            print(f"  {os.path.basename(paths[0])}: {len(sh)} shingles (single file, nothing to compare)")
        sys.exit(0)

    docs = {}
    for p in paths:
        sh = shingles(normalise(strip(open(p, encoding='utf-8', errors='replace').read()), town_of(p)))
        if sh:
            docs[p] = sh
        else:
            print(f"warn: {os.path.basename(p)} too short to score")

    names = list(docs)
    worst = 0.0
    worst_pair = None
    pair_rows = []
    for a, b in combinations(names, 2):
        inter = len(docs[a] & docs[b])
        union = len(docs[a] | docs[b]) or 1
        dup = 100.0 * inter / union
        pair_rows.append((dup, a, b))
        if dup > worst:
            worst, worst_pair = dup, (a, b)

    uniq = {}
    for a in names:
        others = set()
        for b in names:
            if b != a:
                others |= docs[b]
        only = docs[a] - others
        uniq[a] = 100.0 * len(only) / (len(docs[a]) or 1)
    mean_dup = sum(r[0] for r in pair_rows) / len(pair_rows)
    overall = 100.0 - mean_dup

    print("Per-page uniqueness (shingles unique to that page in this set):")
    for a in names:
        print(f"  {uniq[a]:5.1f}%  {os.path.basename(a)}")
    print(f"\nMean pair dup  : {mean_dup:.1f}%")
    print(f"Overall unique : {overall:.1f}%   (floor {FLOOR:.0f}%, = 100 - mean pair dup)")
    print(f"Worst pair dup : {worst:.1f}%   (max  {MAX_PAIR:.0f}%)")
    if worst_pair:
        print(f"   {os.path.basename(worst_pair[0])}  vs  {os.path.basename(worst_pair[1])}")

    over = [r for r in sorted(pair_rows, reverse=True) if r[0] > MAX_PAIR]
    if over:
        print(f"\nPairs over {MAX_PAIR:.0f}% dup:")
        for dup, a, b in over:
            print(f"   {dup:5.1f}%  {os.path.basename(a)}  vs  {os.path.basename(b)}")

    ok = overall >= FLOOR and worst <= MAX_PAIR
    print("\n==== " + ("PASS" if ok else "BELOW FLOOR") + " ====")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
