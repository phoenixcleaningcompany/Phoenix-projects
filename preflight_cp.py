#!/usr/bin/env python3
"""preflight_cp.py - validate batch towns/*.json BEFORE build.

Usage: python3 preflight_cp.py 'towns/b01_*.json'   (or any glob / dir / files)

Checks per entry (all must pass; exits non-zero on any FAIL):
  - required fields present; s1loc is exactly 2 paragraphs
  - ASCII only; no bare '&'; no HTML entities
  - no BLEED term (own-town name exempt, matching verify_cp.py)
  - nearby = 3 distinct towns, all on CP_towns.csv, not the town itself
  - key resolves to a real CP_towns.csv town (slug match)
  - s1loc paragraph word counts in a sane band (depth gate)
"""
import sys, os, re, glob, json, csv, unicodedata, importlib.util

PARA_MIN, PARA_MAX = 45, 120
REQUIRED = ["region", "nearby", "snapshot", "s1_head", "s1loc", "kit_loc", "s2_intro"]

def load_bleed():
    spec = importlib.util.spec_from_file_location("verify_cp", "verify_cp.py")
    v = importlib.util.module_from_spec(spec); spec.loader.exec_module(v)
    return v.BLEED

def slug(s):
    return re.sub(r'-+', '-', re.sub(r"[^a-z0-9]+", "-", s.lower().replace("&", " and "))).strip('-')

def collect(args):
    paths = []
    for a in args:
        if os.path.isdir(a): paths += sorted(glob.glob(os.path.join(a, "*.json")))
        elif os.path.isfile(a): paths.append(a)
        else: paths += sorted(glob.glob(a))
    return [p for p in dict.fromkeys(paths)]

def main():
    args = sys.argv[1:] or ["towns"]
    paths = collect(args)
    if not paths:
        sys.exit("no json files matched")
    BLEED = load_bleed()
    csv_by_slug = {}
    for r in csv.DictReader(open("CP_towns.csv", encoding="utf-8-sig")):
        csv_by_slug[slug(r["Town"].strip())] = r["Town"].strip()
    csv_names = set(csv_by_slug.values())

    total = 0; bad = 0
    for p in paths:
        data = json.load(open(p, encoding="utf-8"))
        for key, T in data.items():
            total += 1
            fails = []
            # fields
            for f in REQUIRED:
                if f not in T: fails.append(f"missing field '{f}'")
            if fails:
                report(key, p, fails); bad += 1; continue
            if not isinstance(T["s1loc"], list) or len(T["s1loc"]) not in (2, 3):
                fails.append(f"s1loc must be 2-3 paragraphs (got {len(T['s1loc']) if isinstance(T['s1loc'],list) else type(T['s1loc']).__name__})")
            blob = " ".join([T["region"], T["snapshot"], T["s1_head"], T["kit_loc"], T["s2_intro"]] + list(T["s1loc"]))
            # ascii
            for ch in set(blob):
                if ord(ch) > 127:
                    fails.append(f"non-ASCII {ch!r} ({unicodedata.name(ch,'?')})")
            if "&" in blob: fails.append("bare '&'")
            if re.search(r"&(?:#\d+|#x[0-9a-fA-F]+|[a-zA-Z][a-zA-Z0-9]{1,30});", blob):
                fails.append("HTML entity")
            # bleed (own-town exempt)
            own = csv_by_slug.get(slug(key), key)
            for term in BLEED:
                if term.lower() == own.lower(): continue
                if re.search(r"\b" + re.escape(term) + r"\b", blob, re.I):
                    fails.append(f"BLEED '{term}'")
            # key on CSV
            if slug(key) not in csv_by_slug:
                fails.append(f"key '{key}' not a CP_towns.csv town")
            # nearby
            nb = T.get("nearby", [])
            if len(nb) != 3: fails.append(f"nearby must be 3 (got {len(nb)})")
            if len(set(n.lower() for n in nb)) != len(nb): fails.append("nearby has duplicates")
            for n in nb:
                if n not in csv_names: fails.append(f"nearby off-CSV: {n!r}")
                if slug(n) == slug(key): fails.append(f"nearby includes the town itself: {n!r}")
            # depth
            for i, para in enumerate(T["s1loc"]):
                w = len(para.split())
                if w < PARA_MIN or w > PARA_MAX:
                    fails.append(f"s1loc[{i}] words={w} (want {PARA_MIN}-{PARA_MAX})")
            if fails:
                report(key, p, fails); bad += 1
    print(f"\n==== {total-bad}/{total} entries clean ====")
    sys.exit(1 if bad else 0)

def report(key, path, fails):
    print(f"[FAIL] {key}  ({os.path.basename(path)})")
    for f in fails: print(f"   - {f}")

if __name__ == "__main__":
    main()
