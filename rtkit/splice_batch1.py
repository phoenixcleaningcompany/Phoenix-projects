#!/usr/bin/env python3
"""splice_batch1.py - validate batch-1 research dicts and splice into rt_build.py TOWNS.

Loads research_b1g*.py (each defines NEW = {...}), validates every entry against
the RT hard rules, then inserts new towns before the TOWNS-closing brace. Skips
keys already present (idempotent). Per batch: sed 's|b1|bNN|g' to repoint.
"""
import csv, glob, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.join(HERE, "rt_build.py")
CSVP = os.path.join(HERE, "RT_towns.csv")
N_PARAS = 2  # RT is Low-variation: s1loc holds exactly 2 local paragraphs
REQUIRED = ["region", "nearby", "snapshot", "s1_head", "s1loc", "kit_loc", "s2_intro"]
MARKER = "\n}\n\n# === CSV / nearby"


def load_csv_towns():
    rows = list(csv.DictReader(open(CSVP, encoding="utf-8-sig")))
    return {(r.get("Town") or r.get("town")).strip() for r in rows}


def load_research():
    merged = {}
    files = sorted(glob.glob(os.path.join(HERE, "research_b1g*.py")))
    if not files:
        sys.exit("no research_b1g*.py files found")
    for f in files:
        ns = {}
        exec(open(f, encoding="utf-8").read(), ns)
        new = ns.get("NEW")
        if not isinstance(new, dict):
            sys.exit(f"{os.path.basename(f)}: no NEW dict")
        for k, v in new.items():
            if k in merged:
                print(f"  warn: {k} defined in multiple files; keeping first")
                continue
            merged[k] = v
        print(f"loaded {os.path.basename(f)}: {list(new)}")
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
    if key != key.lower():
        errs.append("key not lowercase")
    csv_lower = {t.lower() for t in onCSV}
    if key not in csv_lower:
        errs.append(f"key '{key}' is not a lowercased CSV town")
    for f in REQUIRED:
        if f not in entry:
            errs.append(f"missing field '{f}'")
    if errs:
        return errs  # bail early; shape unknown
    nb = entry["nearby"]
    if not (isinstance(nb, list) and len(nb) == 3 and len(set(nb)) == 3):
        errs.append("nearby must be 3 unique towns")
    else:
        for n in nb:
            if n not in onCSV:
                errs.append(f"nearby '{n}' not on CSV")
    if not (isinstance(entry["s1loc"], list) and len(entry["s1loc"]) == N_PARAS):
        errs.append(f"s1loc must be exactly {N_PARAS} paragraphs")
    for s in strings_of(entry):
        try:
            s.encode("ascii")
        except UnicodeEncodeError:
            errs.append(f"non-ASCII in value: {s[:40]!r}")
            break
    for s in strings_of(entry):
        if '"' in s:
            errs.append(f"double-quote in value: {s[:40]!r}"); break
    for s in strings_of(entry):
        if any(c in s for c in "&<>"):
            errs.append(f"&/</> in value: {s[:40]!r}"); break
    si = entry["s2_intro"].rstrip()
    if si and si[-1] in ".,;:!?":
        errs.append("s2_intro has trailing punctuation")
    return errs


def main():
    onCSV = load_csv_towns()
    research = load_research()
    src = open(BUILD, encoding="utf-8").read()
    # existing keys: parse the TOWNS block conservatively
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

    print("\n--- validation ---")
    for k in ok:      print(f"  OK     {k}")
    for k in skipped: print(f"  skip   {k} (already in TOWNS)")
    for k, errs in failed:
        print(f"  FAIL   {k}: {errs}")
    if failed:
        sys.exit(f"\n{len(failed)} entr(y/ies) failed validation; fix and re-run. No splice.")
    if not block_lines:
        print("\nnothing new to splice."); return

    if src.count(MARKER) != 1:
        sys.exit(f"marker found {src.count(MARKER)} times; expected exactly 1")
    new_src = src.replace(MARKER, "\n" + "".join(block_lines) + "}\n\n# === CSV / nearby", 1)
    open(BUILD, "w", encoding="utf-8").write(new_src)
    print(f"\nspliced {len(block_lines)} town(s) into rt_build.py: {ok}")


if __name__ == "__main__":
    main()
