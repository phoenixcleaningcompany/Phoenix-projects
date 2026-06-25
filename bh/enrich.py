#!/usr/bin/env python3
"""enrich.py - clear an over-cap pair by appending a researched, proper-noun-rich
sentence to the weaker page's s1loc, without hand-editing bh_build.py.

Reads enrich.json: [{"key": "<town>", "para": 0|1, "text": "<~50-word sentence>"}]
For each instruction it finds the spliced single-line JSON entry for <key> in
bh_build.py's TOWNS, appends text to s1loc[para], and rewrites that line.

Only works on splicer-written single-line entries (the seed multi-line entries
birmingham/leeds are hand-edited instead). Real local specifics only (SPEC 8.3),
never generic reword. Re-run bh_build + score_bh after.

Usage:  python3 enrich.py [enrich.json]
"""
import os, re, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))


def ascii_ok(s):
    return all(ord(c) < 128 for c in s) and '"' not in s and not any(c in s for c in "&<>")


def main():
    jpath = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "enrich.json")
    instrs = json.load(open(jpath, encoding="utf-8"))
    src = open(os.path.join(HERE, "bh_build.py"), encoding="utf-8").read()
    done, fail = [], []
    for ins in instrs:
        key, para, text = ins["key"].lower(), int(ins["para"]), ins["text"].strip()
        if not ascii_ok(text):
            fail.append((key, "text has non-ASCII or \" & < >")); continue
        m = re.search(r'(\n [ ]?"%s": )(\{.*?\})(,\n)' % re.escape(key), src)
        if not m:
            fail.append((key, "single-line entry not found (hand-edit seed entries)")); continue
        try:
            obj = json.loads(m.group(2))
        except Exception as ex:
            fail.append((key, f"json parse: {ex}")); continue
        if para not in (0, 1) or len(obj.get("s1loc", [])) <= para:
            fail.append((key, "bad para index")); continue
        obj["s1loc"][para] = obj["s1loc"][para].rstrip() + " " + text
        newline = m.group(1) + json.dumps(obj, ensure_ascii=False) + m.group(3)
        src = src[:m.start()] + newline + src[m.end():]
        done.append(key)
    open(os.path.join(HERE, "bh_build.py"), "w", encoding="utf-8").write(src)
    print(f"ENRICHED {len(done)}: {', '.join(done) or '(none)'}")
    for k, why in fail:
        print(f"  - FAIL {k}: {why}")


if __name__ == "__main__":
    main()
