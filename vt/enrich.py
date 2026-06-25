#!/usr/bin/env python3
"""enrich.py - clear an over-cap pair by appending a researched sentence to a
town's s1loc paragraph, rewriting that town's SINGLE-LINE TOWNS entry in
vt_build.py in place (so you never hand-edit the giant source line).

Reads enrich.json:
  [{"key": "denton", "para": 0, "text": "One researched, proper-noun-rich sentence."}]

Only works on splicer-written single-line entries. The hand-authored multi-line
seed entries (london/birmingham/leeds) must be edited by hand. After running,
rebuild just that town and re-score.

Usage:  python3 enrich.py [enrich.json]
"""
import sys, json, re
import vt_build as B


def clean(text):
    text = text.strip()
    try:
        text.encode("ascii")
    except UnicodeEncodeError:
        return None, "non-ASCII"
    if any(c in text for c in '"&<>'):
        return None, 'contains " & < or >'
    return text, None


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "enrich.json"
    edits = json.load(open(path, encoding="utf-8"))
    src = open(B.__file__, encoding="utf-8").read()
    changed = 0
    for ed in edits:
        key = ed["key"].lower()
        para = int(ed["para"])
        text, err = clean(ed["text"])
        if err:
            print(f"SKIP {key}: {err}"); continue
        m = re.search(r'^(?P<indent> *)"' + re.escape(key) + r'": (?P<obj>\{.*\}),\s*$',
                      src, re.M)
        if not m:
            print(f"SKIP {key}: no single-line entry found (multi-line seeds are hand-edited)")
            continue
        obj = json.loads(m.group("obj"))
        s1 = obj.get("s1loc")
        if not isinstance(s1, list) or para >= len(s1):
            print(f"SKIP {key}: s1loc[{para}] missing"); continue
        s1[para] = s1[para].rstrip() + " " + text
        newline = f'{m.group("indent")}"{key}": {json.dumps(obj, ensure_ascii=False)},'
        src = src[:m.start()] + newline + src[m.end():]
        changed += 1
        print(f"ENRICHED {key} s1loc[{para}] (+{len(text.split())} words)")
    if changed:
        open(B.__file__, "w", encoding="utf-8").write(src)
    print(f"\n{changed} town(s) enriched. Rebuild + re-score them.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
