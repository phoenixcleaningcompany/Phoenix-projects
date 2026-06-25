#!/usr/bin/env python3
"""splice_batch.py - splice researched VT town entries into vt_build.py's TOWNS.

Globs research_*.py files (each defining `NEW = {key: entry, ...}`), validates
every entry, and writes each VALID + genuinely-NEW town into vt_build.py's TOWNS
dict as a SINGLE-LINE entry (so enrich.py can later rewrite it). Non-fatal per
bad entry: it is reported and skipped, the rest still splice. Idempotent: a key
already in TOWNS is skipped.

This does NOT check the BLEED list - that is verify_vt.py's job. ALWAYS run
`python3 verify_vt.py outputs` after a batch, not just the splicer.

Usage:  python3 splice_batch.py 'research_b01g*.py'
        python3 splice_batch.py                       # default research_*.py
"""
import sys, glob, re, json
import vt_build as B

REQUIRED = ["region", "nearby", "snapshot", "s1_head", "s1loc", "kit_loc", "s2_intro"]
N_S1LOC = 2
STR_FIELDS = ["region", "snapshot", "s1_head", "kit_loc", "s2_intro"]

_CSV = B._load_csv()
CSV_VERBATIM = {r[1] for r in _CSV}                 # exact spelling
CSV_LOWER = {r[1].lower(): r[1] for r in _CSV}      # lower -> exact


def _ascii(s):
    try:
        s.encode("ascii"); return True
    except (UnicodeEncodeError, AttributeError):
        return False


def _bad(s):
    return any(c in s for c in '"&<>')


def validate(key, e):
    errs = []
    if key != key.lower():
        errs.append("key must be lowercase")
    if key not in CSV_LOWER:
        errs.append(f"key '{key}' is not a lowercased CSV town")
    missing = [f for f in REQUIRED if f not in e]
    if missing:
        return [f"missing field(s): {missing}"] + errs
    nb = e["nearby"]
    if not isinstance(nb, list) or len(nb) != 3 or len(set(nb)) != 3:
        errs.append("nearby must be 3 unique towns")
    else:
        off = [n for n in nb if n not in CSV_VERBATIM]
        if off:
            errs.append(f"nearby off-CSV (verbatim): {off}")
    s1 = e["s1loc"]
    if not isinstance(s1, list) or len(s1) != N_S1LOC:
        errs.append(f"s1loc must be exactly {N_S1LOC} paragraphs")

    strings = [e.get(f, "") for f in STR_FIELDS]
    if isinstance(s1, list):
        strings += s1
    if isinstance(nb, list):
        strings += nb
    for s in strings:
        if not isinstance(s, str):
            errs.append("non-string field value"); continue
        if not _ascii(s):
            errs.append(f"non-ASCII text: {s[:40]!r}")
        if _bad(s):
            errs.append(f'contains " & < or >: {s[:40]!r}')

    si = e.get("s2_intro", "")
    if isinstance(si, str) and si.rstrip() and si.rstrip()[-1] in ".,;:!?":
        errs.append("s2_intro has trailing punctuation")
    return errs


def load_new(path):
    ns = {}
    exec(open(path, encoding="utf-8").read(), ns)
    return ns.get("NEW", {})


def main():
    pattern = sys.argv[1] if len(sys.argv) > 1 else "research_*.py"
    files = sorted(glob.glob(pattern))
    if not files:
        print(f"No files match {pattern!r}"); return 1

    existing = {k.lower() for k in B.TOWNS}
    spliced, skipped, rejected = {}, [], []
    for path in files:
        try:
            new = load_new(path)
        except Exception as ex:                       # bad file: report, continue
            rejected.append((path, f"failed to load: {ex}")); continue
        for key, entry in new.items():
            k = str(key).lower()
            if k in existing or k in spliced:
                skipped.append(k); continue
            errs = validate(k, entry)
            if errs:
                rejected.append((k, "; ".join(errs))); continue
            spliced[k] = entry

    if spliced:
        src = open(B.__file__, encoding="utf-8").read()
        m = re.search(r"\nTOWNS\s*=\s*\{", src)
        close = src.index("\n}\n", m.end())           # column-0 brace ends TOWNS
        lines = "".join(f' "{k}": {json.dumps(e, ensure_ascii=False)},\n'
                        for k, e in spliced.items())
        src = src[:close + 1] + lines + src[close + 1:]
        open(B.__file__, "w", encoding="utf-8").write(src)

    print(f"\n==== splice summary ====")
    print(f"spliced (new): {len(spliced)}  -> {sorted(spliced)}")
    print(f"skipped (already in TOWNS): {len(skipped)}")
    if rejected:
        print(f"REJECTED: {len(rejected)}")
        for k, why in rejected:
            print(f"   {k}: {why}")
    print("\nNow: build, copy flagship into outputs/, then run verify_vt.py outputs.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
