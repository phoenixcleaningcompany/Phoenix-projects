#!/usr/bin/env python3
"""Splice a batch of research dicts into dc_build.py TOWNS.

Loads research_<BATCH>g{i}.py (each defining NEW = {...}), validates the DC
schema, then inserts the entries before the TOWNS-closing brace. Sed this file
per batch:  sed 's|b4|bNN|; s|range(1, 7)|range(1, K)|' splice_batch1.py > splice_batchNN.py
"""
import json, csv

BATCH  = "b4"
GROUPS = range(1, 7)        # 6 groups
BUILD  = "dc_build.py"
REQ    = ["region", "nearby", "snapshot", "s1_head", "s1loc", "kit_loc", "s2_intro"]

rows  = list(csv.DictReader(open("DC_towns.csv", encoding="utf-8-sig")))
onCSV = {(r.get("Town") or r.get("town")).strip() for r in rows}

merged = {}
for i in GROUPS:
    path = f"research_{BATCH}g{i}.py"
    ns = {}
    exec(open(path, encoding="utf-8").read(), ns)
    NEW = ns.get("NEW")
    assert isinstance(NEW, dict), f"{path}: NEW missing or not a dict"
    for k, v in NEW.items():
        assert k == k.lower(), f"{path}: key not lowercased: {k!r}"
        if k in merged:
            print(f"warn: duplicate key {k!r} across groups; keeping first")
            continue
        merged[k] = v

def walk_strings(v):
    if isinstance(v, str):
        yield v
    elif isinstance(v, list):
        for x in v:
            yield from walk_strings(x)
    elif isinstance(v, dict):
        for x in v.values():
            yield from walk_strings(x)

errs = []
for k, e in merged.items():
    if not isinstance(e, dict):
        errs.append(f"{k}: entry not a dict"); continue
    for f in REQ:
        if f not in e:
            errs.append(f"{k}: missing field {f}")
    nb = e.get("nearby", [])
    if not (isinstance(nb, list) and len(nb) == 3 and len(set(nb)) == 3):
        errs.append(f"{k}: nearby must be 3 unique towns")
    for n in (nb if isinstance(nb, list) else []):
        if n not in onCSV:
            errs.append(f"{k}: nearby '{n}' not on CSV")
    s1 = e.get("s1loc", [])
    if not (isinstance(s1, list) and len(s1) == 2):
        errs.append(f"{k}: s1loc must be exactly 2 paragraphs")
    for s in walk_strings(e):
        if any(ord(c) > 127 for c in s):
            errs.append(f"{k}: non-ASCII char in: {s[:60]!r}")
        if '"' in s:
            errs.append(f"{k}: double-quote inside value: {s[:60]!r}")
    si = e.get("s2_intro", "")
    if si.rstrip().endswith((".", ",", ";", ":")):
        errs.append(f"{k}: s2_intro must have NO trailing punctuation")

if errs:
    print("VALIDATION FAILED:")
    for x in errs:
        print("  -", x)
    raise SystemExit(1)

src = open(BUILD, encoding="utf-8").read()
marker = "\n}\n\n# === CSV / nearby"
assert marker in src, "TOWNS close marker not found in dc_build.py"

added, skipped = [], []
block = ""
for k, e in merged.items():
    if f'\n "{k}":' in src:
        skipped.append(k); continue
    block += f' "{k}": {json.dumps(e, ensure_ascii=False)},\n'
    added.append(k)

if block:
    src = src.replace(marker, "\n" + block + "}\n\n# === CSV / nearby", 1)
    open(BUILD, "w", encoding="utf-8").write(src)

print(f"spliced {len(added)} town(s): {', '.join(added)}")
if skipped:
    print(f"skipped {len(skipped)} already-present: {', '.join(skipped)}")
