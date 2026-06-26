#!/usr/bin/env python3
"""validate_triples.py - check locked nearby triples against EV_towns.csv BEFORE dispatch.
Usage: python3 validate_triples.py triples/bNN.json
JSON shape: {"<town key>": ["A","B","C"], ...}
Checks: each key on CSV; exactly 3 nearby; each nearby on CSV; none == self.
"""
import csv, json, os, re, sys

def slug(n):
    return re.sub(r'-+', '-', re.sub(r"[^a-z0-9]+", "-", n.lower().replace("&", " and "))).strip('-')

def csv_slugs():
    here = os.path.dirname(os.path.abspath(__file__))
    p = os.path.join(here, "EV_towns.csv")
    s = set()
    with open(p, newline="", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            s.add(slug(r["Town"]))
    return s

def main():
    data = json.load(open(sys.argv[1], encoding="utf-8"))
    cs = csv_slugs()
    bad = 0
    for key, nb in data.items():
        errs = []
        if slug(key) not in cs:
            errs.append(f"key not on CSV")
        if len(nb) != 3:
            errs.append(f"need 3 nearby, got {len(nb)}")
        for t in nb:
            if slug(t) not in cs:
                errs.append(f"nearby '{t}' not on CSV")
            if slug(t) == slug(key):
                errs.append(f"nearby '{t}' == self")
        if errs:
            bad += 1
            print(f"[FAIL] {key}: {'; '.join(errs)}")
    print(f"\n{len(data)-bad}/{len(data)} triples valid")
    sys.exit(1 if bad else 0)

if __name__ == "__main__":
    main()
