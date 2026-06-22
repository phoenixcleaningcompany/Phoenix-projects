#!/usr/bin/env python3
"""verify_eat.py - QA hard gate for EAT ("Best Places to Eat in <Town>") pages.

Usage:  python3 verify_eat.py [folder]      default: /mnt/user-data/outputs
Needs:  eat_towns.csv beside this script (Rank, Town, Population, Nation).

Hard fails (block the page). Warn-only: word count.
These pages are STANDALONE web pages (WebPage schema, no byline) that lead the
"best places to eat in <town>" query and pivot softly to TR19 kitchen
extraction cleaning. The verifier enforces structure, schema, link wiring,
dead-link safety and cross-series bleed.
"""
import csv, os, re, sys, json, datetime

WORD_MIN = 1200
REQUIRE_EVIDENCE = False      # set by --require-evidence
EVIDENCE_STALE_DAYS = 180
MIN_PHX_LINKS = 8

# Other-series vocabulary that must never appear (template bleed). EAT's own
# core words (restaurant, cafe, pub, takeaway, chef, kitchen, TR19, grease,
# extraction, ductwork, canopy, plenum, baffle, Fire Safety Order, HSE, EHO)
# are deliberately NOT blocked.
BLEED = [
    "polo shirt", "fleece", "hi-vis", "hi vis", "high-vis", "softshell",
    "chainsaw", "arborist", "tree surgery", "EN ISO 11393", "embroider",
    "workwear", "landscaping", "grounds maintenance",
    "SIA", "body armour", "stab vest", "door supervision", "epaulette",
    "RCV", "refuse collection", "bin lorry", "HWRC",
    "solar panel", "heat pump", "MCS-certified", "MCS-registered", "EV charging",
    "Chapter 8", "National Highways", "sector scheme",
    "Ofsted", "KCSIE", "hairnet", "tabard", "tunic",
]
DELIVERY = [r"next[\s-]?day\s+deliver", r"same[\s-]?day\s+deliver",
            r"\b(?:24|48)[\s-]?hour\s+deliver", r"deliver(?:y|ed)?\s+(?:with)?in\s+\d+"]

REQUIRED_LD = ["WebPage", "ItemList", "FAQPage", "Organization", "BreadcrumbList"]


def slug(name):
    s = name.lower().replace("&", " and ")
    s = re.sub(r"['()]", "", s)
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", s)).strip("-")


def load_towns():
    path = None
    for p in ("eat_towns.csv", os.path.join(os.path.dirname(os.path.abspath(__file__)), "eat_towns.csv"),
              "FS_towns.csv"):
        if os.path.exists(p):
            path = p; break
    if not path:
        cands = [f for f in os.listdir(".") if f.lower().endswith(".csv")]
        if not cands: sys.exit("ERROR: no CSV found.")
        path = cands[0]; print(f"NOTE: using {path}")
    towns = set()
    with open(path, newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            r = {k.lower().strip(): (v or "").strip() for k, v in row.items()}
            n = r.get("town") or r.get("name")
            if n: towns.add(n)
    return towns


def find_town(fname, title, towns):
    low = fname.lower()
    for t in sorted(towns, key=len, reverse=True):
        if f"eat-{slug(t)}." in low or slug(t) == low.replace("eat-", "").replace(".html", ""):
            return t
    for t in sorted(towns, key=len, reverse=True):
        if title and t.lower() in title.lower():
            return t
    return None


def meta_desc(txt):
    m = (re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']*)["\']', txt, re.I)
         or re.search(r'<meta[^>]*content=["\']([^"\']*)["\'][^>]*name=["\']description["\']', txt, re.I))
    return m.group(1) if m else None


def check_file(path, towns, seen_desc, seen_title):
    txt = open(path, encoding="utf-8", errors="replace").read()
    fails, warns = [], []
    base = os.path.basename(path)
    tm = re.search(r"<title[^>]*>(.*?)</title>", txt, re.I | re.S)
    title = tm.group(1).strip() if tm else ""
    town = find_town(base, title, towns)

    # 1 — boilerplate head
    if '<html lang="en"' not in txt:               fails.append("1. missing <html lang=\"en\">")
    if 'name="viewport"' not in txt:               fails.append("1. missing viewport meta")
    if 'rel="canonical"' not in txt:               fails.append("1. missing canonical")

    # 2 — title / meta
    if not title:                                  fails.append("2. <title> missing")
    elif not (30 <= len(title) <= 60):             fails.append(f"2. title {len(title)} chars (need 30-60)")
    desc = meta_desc(txt)
    if not desc:                                   fails.append("2. meta description missing")
    else:
        if not (110 <= len(desc) <= 155):          fails.append(f"2. meta description {len(desc)} chars (need 110-155)")
        if "'" in desc or "\u2019" in desc:        fails.append("2. meta description contains an apostrophe")

    # 3 — schema: exactly 5 blocks, all required types
    n_ld = txt.count('application/ld+json')
    if n_ld != 5:                                  fails.append(f"3. expected 5 JSON-LD blocks (WebPage+ItemList+FAQPage+Org+Breadcrumb), found {n_ld}")
    for t in REQUIRED_LD:
        if f'"@type":"{t}"' not in txt and f'"@type": "{t}"' not in txt:
            fails.append(f"3. JSON-LD missing @type {t}")

    # 4 — no JS
    if (re.search(r"<script(?![^>]*application/ld\+json)", txt, re.I)
            or re.search(r"javascript:", txt, re.I)
            or re.search(r"<[^>]+\son[a-z]+\s*=", txt, re.I)):
        fails.append("4. JavaScript found (script / js: / on*= handler)")

    # 5 — link wiring
    phx = len(re.findall(r'href=["\']https?://(?:www\.)?phoenixcleaningcompany\.com', txt, re.I))
    if phx < MIN_PHX_LINKS:                        fails.append(f"5. phoenixcleaningcompany.com links = {phx} (need >= {MIN_PHX_LINKS})")
    if "extractioncleaning.html" not in txt:       fails.append("5. extraction-cleaning service page not linked")
    if 'href="tel:' not in txt:                    fails.append("5. no tel: CTA")
    if 'href="mailto:' not in txt:                 fails.append("5. no mailto: CTA")
    main = re.search(r"<main>(.*?)</main>", txt, re.S)
    if not main or not re.search(r'href=["\']https?://(?:www\.)?phoenixcleaningcompany\.com', main.group(1), re.I):
        fails.append("5. no in-content (contextual) phoenixcleaningcompany.com link inside <main>")

    # 6 — headings
    h1 = re.findall(r"<h1[^>]*>(.*?)</h1>", txt, re.I | re.S)
    if len(h1) != 1:                               fails.append(f"6. expected exactly 1 H1, found {len(h1)}")
    elif town and town.lower() not in re.sub(r"<[^>]+>", " ", h1[0]).lower():
        fails.append(f"6. H1 does not contain town '{town}'")
    if len(re.findall(r"<h2", txt, re.I)) < 6:     fails.append("6. fewer than 6 H2 sections")
    if len(re.findall(r"<h3", txt, re.I)) < 4:     fails.append("6. fewer than 4 H3 (venue names should be H3)")
    if town and town.lower() not in title.lower(): fails.append(f"6. title does not contain town '{town}'")

    # 7 — four venues + FAQ
    tags = len(re.findall(r'class="venue-tag"', txt))
    if tags != 4:                                  fails.append(f"7. expected 4 venue cards, found {tags}")
    if 'id="faq"' not in txt:                      fails.append("7. FAQ section (id=faq) missing")
    q = len(re.findall(r'"@type":\s*"Question"', txt))
    if q < 3:                                       fails.append(f"7. FAQPage has {q} questions (need >= 3)")

    # 8 — the pivot
    if "insight-box" not in txt:                   fails.append("8. pivot .insight-box missing")
    if "TR19" not in txt:                          fails.append("8. TR19 reference missing from pivot")
    if "Regulatory Reform (Fire Safety) Order 2005" not in txt:
        fails.append("8. Fire Safety Order reference missing from pivot")

    # 9 — dead-link guard
    csv_slugs = {slug(t) for t in towns}
    dead = sorted({s for s in re.findall(r'href=["\']eat-([a-z0-9-]+)\.html', txt, re.I)
                   if s not in csv_slugs})
    if dead:                                       fails.append(f"9. nearby/internal link(s) not on CSV (dead links): {dead[:5]}")

    # 10 — bleed
    hit = [b for b in BLEED if re.search(r"\b" + re.escape(b) + r"\b", txt, re.I)]
    if hit:                                         fails.append(f"10. cross-series bleed term(s) found: {hit[:5]}")

    # 11 — delivery claims
    for pat in DELIVERY:
        if re.search(pat, txt, re.I):
            fails.append("11. delivery-timescale claim found"); break

    # 12 — word count (warn)
    words = len(re.sub(r"<[^>]+>", " ", re.sub(r"<(script|style|svg).*?</\1>", " ", txt, flags=re.I | re.S)).split())
    if words < WORD_MIN:                            warns.append(f"12. visible word count {words} below {WORD_MIN}")

    # 13 — corpus-unique title + desc
    if title:
        if title in seen_title:                    fails.append(f"13. title duplicates {seen_title[title]}")
        seen_title[title] = base
    if desc:
        if desc in seen_desc:                       fails.append(f"13. meta description duplicates {seen_desc[desc]}")
        seen_desc[desc] = base

    # 14 — evidence gate (only with --require-evidence): audit sidecar present + valid
    if REQUIRE_EVIDENCE:
        side = os.path.join(os.path.dirname(path), os.path.basename(path).replace(".html", ".evidence.json"))
        if not os.path.exists(side):
            fails.append("14. --require-evidence: missing eat-<slug>.evidence.json (rebuild with --require-evidence)")
        else:
            try:
                man = json.load(open(side, encoding="utf-8"))
            except Exception as e:
                man = None; fails.append(f"14. evidence sidecar unreadable: {e}")
            if man and not man.get("exempt"):
                vs = man.get("venues", [])
                if len(vs) != 4:
                    fails.append(f"14. evidence sidecar lists {len(vs)} venues (need 4)")
                today = datetime.date.today()
                for v in vs:
                    nm = v.get("name", "?")
                    if not re.match(r"^https?://", (v.get("source_url") or "")):
                        fails.append(f"14. venue '{nm}' has no valid source_url in evidence")
                    try:
                        d = datetime.date.fromisoformat((v.get("verified") or "").strip())
                        if (today - d).days > EVIDENCE_STALE_DAYS:
                            warns.append(f"14. venue '{nm}' verified {d} is stale (>{EVIDENCE_STALE_DAYS}d) - re-confirm trading")
                    except Exception:
                        fails.append(f"14. venue '{nm}' has no valid verified date in evidence")

    return town, fails, warns


def main():
    global REQUIRE_EVIDENCE
    argv = sys.argv[1:]
    if "--require-evidence" in argv:
        REQUIRE_EVIDENCE = True
        argv = [a for a in argv if a != "--require-evidence"]
    folder = argv[0] if argv else "/mnt/user-data/outputs"
    if not os.path.isdir(folder): sys.exit(f"ERROR: folder '{folder}' not found.")
    files = sorted(f for f in os.listdir(folder) if f.startswith("eat-") and f.endswith(".html"))
    if not files: sys.exit(f"ERROR: no eat-*.html in {folder}/")
    towns = load_towns()
    seen_desc, seen_title, bad = {}, {}, 0
    for f in files:
        town, fails, warns = check_file(os.path.join(folder, f), towns, seen_desc, seen_title)
        print(f"\n[{'PASS' if not fails else 'FAIL'}] {f}" + (f"  ({town})" if town else ""))
        for x in fails: print(f"   FAIL  {x}")
        for x in warns: print(f"   warn  {x}")
        bad += bool(fails)
    print(f"\n==== {len(files)-bad}/{len(files)} pages passed all hard checks ====")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
