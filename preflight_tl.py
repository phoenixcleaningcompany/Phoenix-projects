#!/usr/bin/env python3
"""preflight_tl.py - scan batch town JSON before building (handover section 5).

Usage: python3 preflight_tl.py 'towns/b01_*.json'   (default: towns/*.json)

Catches the things research agents reliably slip on: non-ASCII (pound sign,
curly quotes, em-dashes), the bare '&' character (B&B / V&A / "Bed & Breakfast"),
missing/!=3 nearby, s1loc not 2-3 paragraphs, cross-series bleed terms, and
nearby towns that are not on TL_towns.csv. Own-town bleed is exempted.
"""
import json, glob, re, csv, sys

# TL bleed list (mirrors verify_tl.py BLEED).
BLEED = ["hairnet", "hygiene coat", "BRCGS", "HACCP", "high-care", "snood", "beard net",
         "SIA", "BS 7858", "body armour", "ballistic", "stab vest", "epaulette", "door supervision",
         "COSHH", "colour-coded cleaning",
         "RCV", "refuse collection", "bin lorry", "kerbside collection", "HWRC",
         "solar panel", "EV charging", "EV charge", "heat pump", "MCS-certified", "MCS-registered",
         "Chapter 8", "National Highways", "sector scheme",
         "chainsaw", "EN ISO 11393", "EN 381", "tree surgery", "arborist", "LANTRA", "NPTC",
         "Ofsted", "KCSIE", "Care Quality Commission", "CQC", "Care Inspectorate",
         "gym", "athleisure", "club crest", "matchday", "tracksuit",
         "tabard", "convenience store", "garden centre", "forecourt", "farm shop", "stockroom",
         "multidrop", "owner-driver", "courier", "parcel round",
         "telecoms", "fibre", "broadband", "Openreach", "street cabinet",
         "charity", "foodbank", "volunteer",
         "barber", "hairdressing", "beautician", "clog", "hoodie", "spa day",
         "scrubs", "veterinary", "tunic", "vet nurse", "kennel", "cattery", "equine", "wellington"]

REQ = ["region", "nearby", "s1_head", "s1loc", "s2_intro"]  # snapshot + kit_loc optional (template fallback)

# Local-content DEPTH gate (anti-thin-content). Calibrated below the approved
# b01 floor (59 words/para, 189 total, 45 proper-nouns) so approved-level depth
# always passes while genuinely thin/generic towns are rejected before build.
S1LOC_PARAS = 3
PARA_MIN_WORDS = 50
TOTAL_MIN_WORDS = 175
PROPER_NOUN_MIN = 30


def proper_nouns(paras):
    """Heuristic count of named places: Capitalised words (len>1) not at sentence start."""
    text = ' '.join(paras)
    return len(re.findall(r'(?<![.!?]\s)(?<!^)\b[A-Z][a-zA-Z]+', text))

csv_towns = {r["Town"].strip().lower()
             for r in csv.DictReader(open("TL_towns.csv", encoding="utf-8-sig"))}

pattern = sys.argv[1] if len(sys.argv) > 1 else "towns/*.json"
issues = 0
n = 0
for f in sorted(glob.glob(pattern)):
    data = json.load(open(f, encoding="utf-8"))
    for k, v in data.items():
        n += 1
        blob = json.dumps(v, ensure_ascii=False)
        if any(ord(c) > 127 for c in blob):
            bad = sorted({c for c in blob if ord(c) > 127})
            print(f"NONASCII {k}: {bad}"); issues += 1
        if "&" in blob:
            print(f"AMP {k}: contains '&' (write 'and')"); issues += 1
        miss = [x for x in REQ if x not in v]
        if miss:
            print(f"FIELD {k}: missing {miss}"); issues += 1
        s1 = v.get("s1loc", [])
        if len(v.get("nearby", [])) != 3 or len(s1) != S1LOC_PARAS:
            print(f"SHAPE {k}: nearby={len(v.get('nearby', []))} s1loc={len(s1)} (need 3 + 3)"); issues += 1
        # DEPTH gate (anti-thin-content)
        if s1:
            wc = [len(p.split()) for p in s1]
            thin = [w for w in wc if w < PARA_MIN_WORDS]
            if thin:
                print(f"DEPTH {k}: paragraph(s) under {PARA_MIN_WORDS}w: {wc}"); issues += 1
            if sum(wc) < TOTAL_MIN_WORDS:
                print(f"DEPTH {k}: total s1loc {sum(wc)}w under {TOTAL_MIN_WORDS}"); issues += 1
            pn = proper_nouns(s1)
            if pn < PROPER_NOUN_MIN:
                print(f"DEPTH {k}: only ~{pn} proper-nouns (need >= {PROPER_NOUN_MIN}) - too generic"); issues += 1
        for t in BLEED:
            if t.lower() == k.lower():
                continue  # own-town exemption
            if re.search(r'\b' + re.escape(t) + r'\b', blob, re.I):
                print(f"BLEED {k}: '{t}'"); issues += 1
        for nb in v.get("nearby", []):
            if nb.lower() not in csv_towns:
                print(f"NEARBY-OFF-CSV {k}: '{nb}'"); issues += 1
print(f"\nentries={n} issues={issues}")
sys.exit(1 if issues else 0)
