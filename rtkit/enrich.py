#!/usr/bin/env python3
"""enrich.py - append a researched, proper-noun-rich sentence to a town's s1loc.

Reads enrich.json (a list of {"key","para","text"}) and, for each, surgically
rewrites that town's single-line JSON entry in rt_build.py, appending `text` to
s1loc[para]. Used to clear over-cap pairs (SPEC 8.3 / handover §6): add real
local specifics to the weaker page(s), never reword to generic phrasing.

text MUST be ASCII, no double-quote, no & < > (same rules the splicer enforces).
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.join(HERE, "rt_build.py")


def main():
    spec = json.load(open(os.path.join(HERE, "enrich.json"), encoding="utf-8"))
    src = open(BUILD, encoding="utf-8").read()
    for item in spec:
        key, para, text = item["key"], item.get("para", 0), item["text"].strip()
        if not text.isascii() or '"' in text or any(c in text for c in "&<>"):
            sys.exit(f"bad text for {key}: must be ASCII, no double-quote, no &<>")
        pat = re.compile(r'^( ' + re.escape(json.dumps(key)) + r': )(\{.*\}),$', re.M)
        m = pat.search(src)
        if not m:
            sys.exit(f"entry not found in rt_build.py: {key}")
        entry = json.loads(m.group(2))
        if para >= len(entry["s1loc"]):
            sys.exit(f"{key}: s1loc has no para index {para}")
        p = entry["s1loc"][para].rstrip()
        entry["s1loc"][para] = p + (" " if not p.endswith(" ") else "") + text
        src = src[:m.start()] + m.group(1) + json.dumps(entry, ensure_ascii=False) + "," + src[m.end():]
        print(f"enriched {key} s1loc[{para}]  (+{len(text.split())} words)")
    open(BUILD, "w", encoding="utf-8").write(src)


if __name__ == "__main__":
    main()
