# EAT Series — "Best Places to Eat in <Town>" (SPEC)

Phoenix Cleaning Company lead-generation doorway pages. **One HTML page per UK
town**, prefix `eat-`. Canonical/og to
`https://www.phoenixcleaningcompany.com/eat-<slug>.html`. The pages live as
**standalone files on cPanel** — not posts in a blog/CMS — so they must present
as self-contained web pages (header, on-page nav, CTA buttons, footer), NOT as
articles with bylines/datelines.

## Audience & posture
Two readerships, one page:
1. **Diners / locals** searching "best places to eat in <town>" — the page must
   genuinely earn that query with four real, researched, currently-trading
   independents (the editorial content).
2. **Hospitality owners** in that town — the soft pivot to **kitchen extraction
   cleaning** (TR19) is what turns a useful guide into a lead. The pivot is one
   section + CTAs + footer, never the bulk of the page.

The single strongest defence against Google's doorway/thin-content systems is
that **the food guide is independently useful**. Test every page: "would a local
bookmark this just for the food?"

## The four-pick format (the editorial spine)
Exactly **4 venues**, one per everyday category, all real independents (a
brewery-tied pub is fine if framed honestly, e.g. Fuller's / Sam's Smith's):
`Takeaway/Casual · Cafe · Restaurant · Pub`. The **venue tag may flex to the
local signature** (e.g. Birmingham "Balti House"). The four venues + food_scene
+ FAQ are the **uniqueness engine** — 100% web-researched, never pooled.

## Identity block — the pivot (id `#kitchens`)
"Behind the Pass: The Kitchens That Keep <Town> Fed" → the `.insight-box`
"Industry Insight" pivot to Phoenix. Must:
- sit ~70% through the page
- read as expert knowledge, not a sales pitch
- connect the town's food to extraction maintenance by a specific mechanism
  (use the per-town `pivot_local_hook`)
- carry accurate references: **TR19 Grease (BESA)**, **Regulatory Reform (Fire
  Safety) Order 2005**, **Health and Safety at Work etc. Act 1974**, **HSE**,
  **EHO**, and the frequency table (heavy 12-16h → 3 mo; moderate 6-12h → 6 mo;
  light 2-6h → 12 mo)
- mention the TR19 certificate / insurance point matter-of-factly
- pivot prose is POOLED by `pivot_variant` (high-volume / pub-town / coastal /
  market-town) + spliced `pivot_local_hook` so it is never corpus-constant.

## Palette / design (Phoenix house style)
Charcoal `#1D2433`, slate `#2E3D52`, copper `#C4793A` (hover `#A8642E`), bg
`#FAFAF7`, alt `#F0EEEA`. Fonts **Barlow Condensed** (display) + **Inter**
(body). Components: sticky topbar, hero (town SVG), alert band, jump links,
snapshot quick-answer, stat row, 4 venue cards, food-scene, mid-CTA, pivot
insight-box (+ extraction cross-section SVG, the one shared diagram), planning,
what-to-order, FAQ, cert strip, full CTA, related (nearby) grid, footer.

## Hard rules (verify_eat.py — the binding gate)
1. `<html lang="en">`, viewport, self-canonical present.
2. Title 30-60 chars, contains town. Meta description 110-155 chars, **no
   apostrophes**, includes CTA language.
3. **5 JSON-LD blocks**: WebPage + ItemList + FAQPage + Organization +
   BreadcrumbList. (NOT Article — these are standalone pages, not blog posts.)
4. No JavaScript (ld+json only). No on*= handlers.
5. Phoenix links: **>= 8** `phoenixcleaningcompany.com` hrefs, **>=1 in-content
   contextual** link in the article body, the extraction-cleaning service page
   linked at least once, and `tel:` + `mailto:` CTAs present.
6. Single H1 containing the town; H2s for each section; venue names are H3.
7. Four venue tags present; FAQ section with >= 3 Q&As matching FAQPage schema.
8. Pivot present: `.insight-box` + the TR19 reference + the Fire Safety Order.
9. **Dead-link guard**: every `eat-<slug>.html` link MUST be a CSV town
   (`require_nearby` already hard-fails at build; verify re-checks output).
10. **BLEED ban**: no other-series vocabulary —
    workwear/landscaping/forestry (polo, fleece, hi-vis, chainsaw, arborist,
    embroidery, EN ISO 11393), security (SIA, body armour), waste (RCV, HWRC),
    renewables (solar panel, heat pump, MCS), highways (Chapter 8, National
    Highways). **LEGAL for EAT** (its core): restaurant, cafe, pub, takeaway,
    chef, kitchen, TR19, grease, extraction, ductwork, canopy, plenum, baffle
    filter, Fire Safety Order, HSE, EHO — verifier does NOT block these.
11. No delivery-timescale claims (this is not e-commerce).
12. Word count >= 1200 (warn) — depth, not padding. London flagship runs long
    (4 deep venues); small market towns sit comfortably in 1200-1800.
13. Unique title + meta description across the corpus.

## Nearby = GEOGRAPHIC (global rule)
3 hand-authored, web-verified, geographically-close towns, all on
`eat_towns.csv`. `require_nearby()` raises on missing / <3 / off-CSV — no rank
or auto fallback. London → Croydon/Bromley/Watford. Birmingham →
Solihull/West Bromwich/Walsall.

## Uniqueness (score_eat.py — diagnostic, not the gate)
Floors: overall >= 70%, worst pair <= 50%. The EAT series scores HIGHER than the
workwear/forestry series because the four venues are real distinct facts, not
paraphrase pools — the pair cap passes comfortably. Hard checks (verify_eat) are
the binding gate; do not chase the overall floor at small N.

## Research mandate (NON-NEGOTIABLE)
Every town **web-researched live**; never author venues from memory. Confirm each
venue is **currently trading** (closures and lost stars are common — e.g.
Birmingham's Bartons Arms closed again 07/2025, Purnell's lost its star 10/2024,
both correctly rejected). Capture: real name, area/street, founding date where
notable, signatures, and the town's wider food geography (named neighbourhoods,
markets, the local signature dish). London is the general-knowledge exception.

## Files
eat-london.html (flagship/base) · eat_build.py · verify_eat.py · score_eat.py ·
diag_eat.py · towns_data.py · eat_chrome.css · eat_towns.csv (505) · SPEC.md ·
CLAUDE.md · RESEARCH.md (research contract) · make_town.sh (orchestrator).
Build: `python3 eat_build.py <slug...>` → /mnt/user-data/outputs/. Or run the
whole pipeline: `./make_town.sh <slug...>`. Only ADD pages; never silently
rebuild a signed-off flagship.

## Evidence gate (optional, recommended in Code)
`--require-evidence` makes the research auditable: every venue in a non-exempt
town must carry `source_url` + `verified` (YYYY-MM-DD) or the build hard-fails.
The builder writes an audit sidecar `eat-<slug>.evidence.json`; `verify_eat.py
--require-evidence` requires it and re-checks it (stale verifications warn).
General-knowledge flagships (London) set `evidence_exempt: True`. Web access
makes accurate research possible; the evidence gate is what stops an agent
inventing venues anyway. Sidecars stay local — do not upload them.
