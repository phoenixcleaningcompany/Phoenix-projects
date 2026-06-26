#!/usr/bin/env python3
"""preflight_ev.py - validate per-batch towns/*.json BEFORE building.

Run on every batch before ev_build.py. Catches the things the agents get wrong
(off-CSV keys/nearby, wrong paragraph count, non-ASCII, bare &, HTML entities,
bleed drift) so the build/verify gate never sees them.

Usage:
  python3 preflight_ev.py 'towns/b00_*.json'
  python3 preflight_ev.py towns           (all json in towns/)
  python3 preflight_ev.py towns/b01_g3.json
Needs EV_towns.csv beside it. Imports BLEED + slug from verify_ev.
"""
import csv, glob, json, os, re, sys
import verify_ev as V

PARA_MIN, PARA_MAX = 2, 3          # s1loc: 2 local paras baseline, 3 when enriched
WORD_LO, WORD_HI   = 28, 140        # per local paragraph
REQUIRED = ["region", "nearby", "snapshot", "s1_head", "s1loc", "kit_loc", "s2_intro"]
ENTITY = re.compile(r"&(?:#\d+|#x[0-9a-fA-F]+|[a-zA-Z][a-zA-Z0-9]{1,30});")
BARE_AMP = re.compile(r"&(?!amp;)")


def slug(name):
    return V.slug(name)


def csv_map():
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, "EV_towns.csv")
    if not os.path.exists(path):
        path = "EV_towns.csv"
    m = {}
    with open(path, newline="", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            m[slug(r["Town"])] = r["Town"].strip()
    return m


def strings(v):
    out = []
    for val in v.values():
        if isinstance(val, str):
            out.append(val)
        elif isinstance(val, list):
            out += [x for x in val if isinstance(x, str)]
    return out


def collect(args):
    paths = []
    for a in args:
        if os.path.isdir(a):
            paths += sorted(glob.glob(os.path.join(a, "*.json")))
        else:
            paths += sorted(glob.glob(a))
    return [p for p in dict.fromkeys(paths) if os.path.isfile(p)]


def main():
    args = sys.argv[1:] or ["towns"]
    paths = collect(args)
    if not paths:
        sys.exit("ERROR: no JSON files matched.")
    names = csv_map()
    csv_slugs = set(names)
    n = fails = 0
    for p in paths:
        try:
            data = json.load(open(p, encoding="utf-8"))
        except Exception as e:
            print(f"[FAIL] {p}: not valid JSON ({e})")
            fails += 1
            continue
        for key, v in data.items():
            n += 1
            ks = slug(key)
            errs = []
            if ks not in csv_slugs:
                errs.append(f"key '{key}' not on EV_towns.csv")
            for fld in REQUIRED:
                if not v.get(fld):
                    errs.append(f"missing/empty field '{fld}'")
            nb = v.get("nearby") or []
            if len(nb) != 3:
                errs.append(f"nearby must list exactly 3 (got {len(nb)})")
            for t in nb:
                if slug(t) not in csv_slugs:
                    errs.append(f"nearby '{t}' not on CSV")
                if slug(t) == ks:
                    errs.append(f"nearby '{t}' is the town itself")
            s1 = v.get("s1loc") or []
            if not (PARA_MIN <= len(s1) <= PARA_MAX):
                errs.append(f"s1loc must be {PARA_MIN}-{PARA_MAX} paragraphs (got {len(s1)})")
            for i, para in enumerate(s1):
                w = len(para.split())
                if not (WORD_LO <= w <= WORD_HI):
                    errs.append(f"s1loc[{i}] is {w} words (want {WORD_LO}-{WORD_HI})")
            blob = " ".join(strings(v))
            try:
                blob.encode("ascii")
            except UnicodeEncodeError as e:
                bad = blob[e.start:e.start + 1]
                errs.append(f"non-ASCII char {bad!r} (use straight quotes / plain text)")
            if ENTITY.search(blob):
                errs.append("HTML entity in copy (write the literal character)")
            if BARE_AMP.search(blob):
                errs.append("bare '&' in copy (write 'and')")
            own = names.get(ks, key)
            scan = re.sub(r"\b" + re.escape(own) + r"\b", " ", blob, flags=re.I)
            hit = [t for t in V.BLEED if re.search(r"\b" + re.escape(t) + r"\b", scan, re.I)]
            if hit:
                errs.append(f"BLEED term(s) in copy: {hit[:4]}")
            print(f"[{'PASS' if not errs else 'FAIL'}] {key}")
            for e in errs:
                print(f"    {e}")
            fails += bool(errs)
    print(f"\n==== {n - fails}/{n} entries passed preflight ====")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
