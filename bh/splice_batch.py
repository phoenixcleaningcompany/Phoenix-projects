#!/usr/bin/env python3
"""splice_batch.py - validate research_*.py NEW dicts and splice valid+new
towns into bh_build.py's TOWNS dict. Non-fatal per entry: a bad town is
reported and skipped; the rest of the batch still splices.

Each research file defines  NEW = { "<key>": {7 fields}, ... }.
Validation (reject on any):
  - required 7 fields present: region, nearby, snapshot, s1_head, s1loc,
    kit_loc, s2_intro
  - nearby = exactly 3 unique strings, each VERBATIM in BH_towns.csv Town column
  - s1loc = exactly 2 strings
  - all string values ASCII-only; no inner "  ; no & < >
  - key == its lowercased CSV town spelling
  - s2_intro has no trailing punctuation
Entries are serialized one-per-line via json.dumps and inserted before the
"# === CSV / nearby" marker. Idempotent: keys already in TOWNS are skipped.

Usage:  python3 splice_batch.py [research_glob]   (default research_*.py)
"""
import os, re, sys, csv, glob, json

HERE = os.path.dirname(os.path.abspath(__file__))
REQ = ["region", "nearby", "snapshot", "s1_head", "s1loc", "kit_loc", "s2_intro"]
MARKER = "\n}\n\n# === CSV / nearby"


def csv_towns():
    out = {}
    with open(os.path.join(HERE, "BH_towns.csv"), newline="", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            t = r["Town"].strip()
            out[t.lower()] = t
    return out


def ascii_clean(s):
    return all(ord(c) < 128 for c in s) and '"' not in s and not any(c in s for c in "&<>")


def existing_keys(src):
    block = src[src.index("TOWNS = {"):src.index("# === CSV / nearby")]
    return {k.lower() for k in re.findall(r'\n [ ]?"([^"]+)":\s*\{', block)}


def validate(key, e, towns, have):
    errs = []
    if key != key.lower():
        errs.append("key not lowercase")
    if key not in towns:
        errs.append(f"key '{key}' not a CSV town")
    if key in have:
        return ["already in TOWNS (skip)"]
    for f in REQ:
        if f not in e:
            errs.append(f"missing field '{f}'")
    if errs:
        return errs
    nb = e["nearby"]
    if not (isinstance(nb, list) and len(nb) == 3 and len(set(nb)) == 3):
        errs.append("nearby must be 3 unique towns")
    else:
        for n in nb:
            if n.lower() not in towns:
                errs.append(f"nearby '{n}' not on CSV")
            elif towns[n.lower()] != n:
                errs.append(f"nearby '{n}' wrong CSV spelling (want '{towns[n.lower()]}')")
    if not (isinstance(e["s1loc"], list) and len(e["s1loc"]) == 2):
        errs.append("s1loc must be exactly 2 paragraphs")
    for f in REQ:
        vals = e[f] if isinstance(e[f], list) else [e[f]]
        for v in vals:
            if not isinstance(v, str):
                errs.append(f"{f}: non-string value"); continue
            if not ascii_clean(v):
                errs.append(f"{f}: non-ASCII or contains \" & < >")
    if isinstance(e.get("s2_intro"), str) and e["s2_intro"].rstrip() and e["s2_intro"].rstrip()[-1] in ".!?,;:":
        errs.append("s2_intro has trailing punctuation")
    return errs


def main():
    pat = sys.argv[1] if len(sys.argv) > 1 else "research_*.py"
    towns = csv_towns()
    src = open(os.path.join(HERE, "bh_build.py"), encoding="utf-8").read()
    have = existing_keys(src)

    accepted, skipped = {}, []
    for path in sorted(glob.glob(os.path.join(HERE, pat))):
        ns = {}
        try:
            exec(open(path, encoding="utf-8").read(), ns)
        except Exception as ex:
            skipped.append((os.path.basename(path), f"exec error: {ex}")); continue
        NEW = ns.get("NEW", {})
        for key, e in NEW.items():
            errs = validate(key, e, towns, set(have) | set(accepted))
            if errs:
                skipped.append((key, "; ".join(errs)))
            else:
                accepted[key] = {f: e[f] for f in REQ}

    if accepted:
        lines = "".join(' "%s": %s,\n' % (k, json.dumps(accepted[k], ensure_ascii=False))
                         for k in accepted)
        src = src.replace(MARKER, "\n" + lines + "}\n\n# === CSV / nearby", 1)
        open(os.path.join(HERE, "bh_build.py"), "w", encoding="utf-8").write(src)

    print(f"SPLICED {len(accepted)} new town(s): {', '.join(accepted) or '(none)'}")
    if skipped:
        print(f"\nSKIPPED {len(skipped)}:")
        for k, why in skipped:
            print(f"  - {k}: {why}")
    sys.exit(0)


if __name__ == "__main__":
    main()
