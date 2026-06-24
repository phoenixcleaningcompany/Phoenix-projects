#!/usr/bin/env python3
"""splice_batch.py - validate ALL research_*.py dicts and splice new towns.

Globs research_*.py (each defines NEW = {...}), validates every entry against
the RT hard rules, and splices any not-yet-present town into rt_build.py's TOWNS
before the closing brace. Idempotent (skips keys already in TOWNS). Non-fatal on
a bad entry: valid+new towns still splice; failures are listed for re-research.
"""
import csv, glob, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.join(HERE, "rt_build.py")
CSVP = os.path.join(HERE, "RT_towns.csv")
N_PARAS = 2
REQUIRED = ["region", "nearby", "snapshot", "s1_head", "s1loc", "kit_loc", "s2_intro"]
MARKER = "\n}\n\n# === CSV / nearby"


def load_csv_towns():
    rows = list(csv.DictReader(open(CSVP, encoding="utf-8-sig")))
    return {(r.get("Town") or r.get("town")).strip() for r in rows}


def load_research():
    merged = {}
    files = sorted(glob.glob(os.path.join(HERE, "research_*.py")))
    if not files:
        sys.exit("no research_*.py files found")
    for f in files:
        ns = {}
        try:
            exec(open(f, encoding="utf-8").read(), ns)
        except Exception as e:
            print(f"  WARN: {os.path.basename(f)} failed to exec: {e}")
            continue
        new = ns.get("NEW")
        if not isinstance(new, dict):
            print(f"  WARN: {os.path.basename(f)}: no NEW dict"); continue
        for k, v in new.items():
            if k not in merged:
                merged[k] = v
    return merged


def strings_of(entry):
    out = []
    for v in entry.values():
        if isinstance(v, str):
            out.append(v)
        elif isinstance(v, list):
            out.extend(x for x in v if isinstance(x, str))
    return out


def validate(key, entry, onCSV):
    errs = []
    if not isinstance(entry, dict):
        return ["not a dict"]
    if key != key.lower():
        errs.append("key not lowercase")
    if key not in {t.lower() for t in onCSV}:
        errs.append(f"key '{key}' not a lowercased CSV town")
    for f in REQUIRED:
        if f not in entry:
            errs.append(f"missing '{f}'")
    if errs:
        return errs
    nb = entry["nearby"]
    if not (isinstance(nb, list) and len(nb) == 3 and len(set(nb)) == 3):
        errs.append("nearby must be 3 unique")
    else:
        for n in nb:
            if n not in onCSV:
                errs.append(f"nearby '{n}' not on CSV")
    if not (isinstance(entry["s1loc"], list) and len(entry["s1loc"]) == N_PARAS):
        errs.append(f"s1loc must be {N_PARAS} paragraphs")
    for s in strings_of(entry):
        try:
            s.encode("ascii")
        except UnicodeEncodeError:
            errs.append(f"non-ASCII: {s[:30]!r}"); break
    for s in strings_of(entry):
        if '"' in s:
            errs.append(f'double-quote: {s[:30]!r}'); break
    for s in strings_of(entry):
        if any(c in s for c in "&<>"):
            errs.append(f"&/</>: {s[:30]!r}"); break
    si = entry["s2_intro"].rstrip()
    if si and si[-1] in ".,;:!?":
        errs.append("s2_intro trailing punctuation")
    return errs


def main():
    onCSV = load_csv_towns()
    research = load_research()
    src = open(BUILD, encoding="utf-8").read()
    sys.path.insert(0, HERE)
    import rt_build
    existing = set(rt_build.TOWNS)

    ok, block_lines, skipped, failed = [], [], [], []
    for key, entry in research.items():
        if key in existing:
            skipped.append(key); continue
        errs = validate(key, entry, onCSV)
        if errs:
            failed.append((key, errs)); continue
        ok.append(key)
        block_lines.append(f' {json.dumps(key)}: {json.dumps(entry, ensure_ascii=False)},\n')

    print(f"new OK={len(ok)}  skip(existing)={len(skipped)}  FAILED={len(failed)}")
    for k, errs in failed:
        print(f"  FAIL  {k}: {errs}")
    if not block_lines:
        print("nothing new to splice.")
        return 1 if failed else 0
    if src.count(MARKER) != 1:
        sys.exit(f"marker count {src.count(MARKER)} != 1")
    new_src = src.replace(MARKER, "\n" + "".join(block_lines) + "}\n\n# === CSV / nearby", 1)
    open(BUILD, "w", encoding="utf-8").write(new_src)
    print(f"spliced {len(ok)} town(s): {ok}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
