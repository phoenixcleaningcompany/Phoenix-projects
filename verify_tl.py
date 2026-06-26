#!/usr/bin/env python3
"""verify_tl.py - QA for TL (Travel, Tourism & Leisure) workwear pages.

Usage:  python3 verify_vt.py [folder]     default folder: outputs/
Needs:  TL_towns.csv in repo root (Rank, Town, Population, Nation)

Self-checkout / Template B series (small-biz buyer: vet practices, kennels,
catteries, groomers, equine). Hard fails: links (14 .com + 1 community), JS,
entities, meta length, town in title/h1, delivery claims, cross-series bleed,
lead products (polo + fleece + softshell), duplicate title/description, dead
nearby links, 4 JSON-LD blocks. Warn only: word count (12), filename slug (14).

VT spans TWO environments: clinical (scrubs/tunics/polos) and hands-on/outdoor
(fleeces/waterproofs/safety shoes/wellingtons). polo, fleece, softshell, waterproof, hi-vis,
waterproof, vet, veterinary, kennel, cattery, equine, animal, wellington,
safety shoes, grooming salon and apron are LEGAL VT vocabulary (groomers work
in grooming salons) and are NOT bleed.
Check 10 blocks BH salon signatures (salon/barber/spa/hairdressing/beautician/
clog/hoodie) plus the inherited food/security/cleaning/waste/renewables/
highways/forestry/care/sports/retail/courier bleed.
"""
import csv, os, re, sys

WORD_MIN = 1200
LEAD = "polo"   # TC lead (polos)
CO_LEAD = "fleece"   # co-lead (fleeces)
TRI_LEAD = "softshell" # third lead (softshells)

# Hard exclusions. Body-armour/ballistic terms are BANNED outright (everyday
# workwear only). The rest guard against other-series template bleed.
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

DELIVERY = [r"next[\s-]?day\s+deliver", r"same[\s-]?day\s+deliver",
            r"\b(?:24|48)[\s-]?hour\s+deliver",
            r"deliver(?:y|ed)?\s+(?:with)?in\s+\d+"]


def slug(name):
    s = name.lower().replace("&", " and ")
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", s)).strip("-")


def load_towns():
    path = "TL_towns.csv"
    if not os.path.exists(path):
        cands = [f for f in os.listdir(".") if f.lower().endswith(".csv")]
        if not cands:
            sys.exit("ERROR: no CSV found in repo root.")
        path = cands[0]
        print(f"NOTE: TL_towns.csv not found, using {path}")
    towns = {}
    with open(path, newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            r = {k.lower().strip(): (v or "").strip() for k, v in row.items()}
            name = r.get("town") or r.get("name") or ""
            if not name:
                continue
            towns[name] = (r.get("nation") or r.get("country") or "").lower()
    if not towns:
        sys.exit("ERROR: CSV loaded but no town column found.")
    return towns


def find_town(fname, title, towns):
    low = fname.lower()
    for t in sorted(towns, key=len, reverse=True):
        if slug(t) in low:
            return t
    for t in sorted(towns, key=len, reverse=True):
        if title and t.lower() in title.lower():
            return t
    return None


def meta_desc(txt):
    m = (re.search(r'<meta[^>]*name=["\']description["\'][^>]*'
                   r'content=["\']([^"\']*)["\']', txt, re.I)
         or re.search(r'<meta[^>]*content=["\']([^"\']*)["\'][^>]*'
                      r'name=["\']description["\']', txt, re.I))
    return m.group(1) if m else None


def check_file(path, towns, seen_desc, seen_title):
    txt = open(path, encoding="utf-8", errors="replace").read()
    fails, warns = [], []
    tm = re.search(r"<title[^>]*>(.*?)</title>", txt, re.I | re.S)
    title = tm.group(1).strip() if tm else ""
    town = find_town(os.path.basename(path), title, towns)

    com = len(re.findall(r'href=["\']https?://(?:www\.)?ineedworkwear\.com', txt, re.I))
    if com != 14:
        fails.append(f"1. ineedworkwear.com links = {com} (need exactly 14)")
    comm = len(re.findall(r'href=["\']https?://(?:www\.)?ineedworkwear\.co\.uk/community', txt, re.I))
    if comm != 1:
        fails.append(f"2. community links = {comm} (need exactly 1)")

    if (re.search(r"<script(?![^>]*application/ld\+json)", txt, re.I)
            or re.search(r"javascript:", txt, re.I)
            or re.search(r"<[^>]+\son[a-z]+\s*=", txt, re.I)):
        fails.append("3. JavaScript found (script tag / js: / on*= handler)")

    ents = re.findall(r"&(?:#\d+|#x[0-9a-fA-F]+|[a-zA-Z][a-zA-Z0-9]{1,30});", txt)
    if ents:
        fails.append(f"4. HTML entities found: {sorted(set(ents))[:5]}")

    desc = meta_desc(txt)
    if not desc:
        fails.append("5. meta description missing")
    elif len(desc) > 160:
        fails.append(f"5. meta description {len(desc)} chars (max 160)")
    if desc:
        if desc in seen_desc:
            fails.append(f"6. meta description duplicates {seen_desc[desc]}")
        seen_desc[desc] = os.path.basename(path)

    if not town:
        fails.append("7. could not match this file to any town on the CSV")
    else:
        if town.lower() not in title.lower():
            fails.append(f"7. title does not contain town '{town}'")
        h1 = re.search(r"<h1[^>]*>(.*?)</h1>", txt, re.I | re.S)
        h1t = re.sub(r"<[^>]+>", " ", h1.group(1)) if h1 else ""
        if not h1 or town.lower() not in h1t.lower():
            fails.append(f"8. h1 missing or does not contain '{town}'")

    for pat in DELIVERY:
        if re.search(pat, txt, re.I):
            fails.append("9. delivery timescale claim found")
            break

    town_l = (town or "").lower()
    hit = [term for term in BLEED
           if term.lower() != town_l
           and re.search(r"\b" + re.escape(term) + r"\b", txt, re.I)]
    if hit:
        fails.append(f"10. banned/bleed term(s) found (incl. security/cleaning/sports/care bleed): {hit[:4]}")

    if LEAD not in txt.lower():
        fails.append(f"11. lead product '{LEAD}' not mentioned")
    if CO_LEAD not in txt.lower():
        fails.append(f"11b. co-lead product '{CO_LEAD}' not mentioned")
    if TRI_LEAD not in txt.lower():
        fails.append(f"11c. third lead product '{TRI_LEAD}' not mentioned")

    words = len(re.sub(r"<[^>]+>", " ", txt).split())
    if words < WORD_MIN:
        warns.append(f"12. word count {words} below {WORD_MIN}")

    if title:
        if title in seen_title:
            fails.append(f"13. title duplicates {seen_title[title]}")
        seen_title[title] = os.path.basename(path)
    else:
        fails.append("13. <title> missing")

    if town and slug(town) not in os.path.basename(path).lower():
        warns.append(f"14. filename does not contain slug '{slug(town)}'")

    csv_slugs = {slug(t) for t in towns}
    n_ld = txt.count('script type="application/ld+json"')
    if n_ld != 4:
        fails.append(f"16. expected 4 JSON-LD blocks (FAQ+Org+Service+Breadcrumb), found {n_ld}")
    dead = sorted({s for s in re.findall(r'href=["\']tl-([a-z0-9-]+)\.html', txt, re.I)
                   if s.lower() not in csv_slugs})
    if dead:
        fails.append(f"15. nearby/internal link(s) not on CSV (dead links): {dead[:5]}")

    return town, fails, warns


def main():
    folder = sys.argv[1] if len(sys.argv) > 1 else "outputs"
    if not os.path.isdir(folder):
        sys.exit(f"ERROR: folder '{folder}' not found.")
    files = sorted(f for f in os.listdir(folder) if f.endswith(".html") and f.startswith("tl-"))
    if not files:
        sys.exit(f"ERROR: no tl-*.html files in {folder}/")
    towns = load_towns()
    seen_desc, seen_title, bad = {}, {}, 0
    for f in files:
        town, fails, warns = check_file(os.path.join(folder, f), towns, seen_desc, seen_title)
        print(f"\n[{'PASS' if not fails else 'FAIL'}] {f}" + (f"  ({town})" if town else ""))
        for x in fails: print(f"   FAIL  {x}")
        for x in warns: print(f"   warn  {x}")
        bad += bool(fails)
    print(f"\n==== {len(files) - bad}/{len(files)} pages passed all hard checks ====")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
