# CLAUDE.md — EAT series runbook ("Best Places to Eat in <Town>")

Read **SPEC.md** first. Per-session operating guide. The filesystem can reset
between sessions — recreate the kit from these files as needed.

## What EAT is
Standalone cPanel location pages for **Phoenix Cleaning Company**, one per UK
town, prefix `eat-`. Each page is a genuine four-pick local food guide
(Takeaway/Casual, Cafe, Restaurant, Pub) that soft-pivots, ~70% down, to **TR19
kitchen extraction cleaning**. They are STANDALONE WEB PAGES (WebPage schema, no
byline/dateline) — not blog posts. Charcoal + copper Phoenix palette, Barlow
Condensed + Inter. Nearby = geographic. Phoenix link wiring is fixed by the
builder.

## Why the model works (and its one risk)
The four venues + food-scene + FAQ are REAL, DISTINCT, RESEARCHED facts, so
uniqueness scores very high (London vs Birmingham ~96% overall, ~4% pair dup) —
far better than paraphrase-pooled workwear/forestry series. The standing risk is
that this is a doorway-page network; the only durable defence is that every page
is genuinely useful for the food query on its own. Apply the test: *would a local
bookmark this just for the food?* If not, the page is not done.

## The research mandate (NON-NEGOTIABLE)
**Never author venues from memory.** For each town, web-research and CONFIRM EACH
VENUE IS CURRENTLY TRADING. Closures and lost accolades are common and have
already caught obvious picks — e.g. Birmingham's Bartons Arms (finest interior,
but closed again 07/2025) and Purnell's (lost its Michelin star 10/2024). Both
were correctly rejected. Capture per venue: real name, area/street, founding
date where notable, signatures; and the town's wider food geography (named
neighbourhoods, markets, the local signature dish). London is the
general-knowledge exception.

## Session workflow (fully autonomous in Claude Code)
The Code agent has WebSearch/WebFetch and the Sonnet research sub-agents inherit
it, so research, build and QA all run in Code - no chat/Code split.

1. `cd` to the kit. Ensure present: `eat_build.py`, `towns_data.py`,
   `eat_chrome.css`, `eat_towns.csv`, `eat_hero_london.svg`, the QA scripts,
   `RESEARCH.md`, `make_town.sh`.
2. **Research the town (sub-agent, web).** Spawn a research sub-agent with
   **RESEARCH.md** as its brief. It web-searches, **confirms each venue is
   currently trading today**, captures `source_url` + `verified` per venue,
   finds the food geography and three CSV-validated nearby towns, and appends a
   `TOWNS["<slug>"] = {...}` entry to `towns_data.py` (schema at the top of that
   file).
3. **Build + gate + score in one command:** `./make_town.sh <slug> [<slug> ...]`
   runs `eat_build.py --require-evidence` -> `verify_eat.py --require-evidence`
   -> `score_eat.py`, and exits non-zero if the verify gate fails. (Use
   `./make_town.sh --no-evidence <slug>` to skip the source/verified gate; not
   recommended for new towns.)
4. If verify FAILs, fix the `towns_data.py` entry and re-run. If a score pair is
   over 50%, run `python3 diag_eat.py` and add real local detail to the weaker
   page - never reword to generic.
5. Upload the passing `eat-<slug>.html` files to cPanel. **Do not upload the
   `eat-<slug>.evidence.json` sidecars** - they are your local audit trail.

## The evidence gate (why it exists)
Web access makes accurate research *possible*, not *automatic* - a
general-purpose agent told "find four good restaurants" will return a name from
an old listicle. `--require-evidence` forces every non-exempt town's four venues
to carry a `source_url` and a `verified` date, writes an auditable
`eat-<slug>.evidence.json`, and fails the build/verify if any is missing.
General-knowledge flagships (London) set `evidence_exempt: True`. This is the
mechanism that designs the closure trap out of an autonomous pipeline.

## Generator architecture
`eat_build.py` embeds the chrome (loads `eat_chrome.css`; topbar/footer/cert-
strip/CTA/extraction-SVG are Python constants) and assembles each town from its
`TOWNS` entry. Section order is fixed: hero → alert → jump-nav → Where to Eat
(snapshot + intro pool + stats) → The Four Picks (venue cards + glance) → Food
Scene (+ mid-CTA) → **pivot #kitchens** (pooled by `pivot_variant` + spliced
`pivot_local_hook`) → Planning + What to Order → FAQ → cert strip → CTA →
nearby grid → footer. 5 JSON-LD blocks: WebPage + ItemList + FAQPage +
Organization + BreadcrumbList. `require_nearby()` hard-fails on missing/<3/off-
CSV nearby. crc32 `pick()` rotates the small pools (intro + pivot phrasing).

## What is pooled vs researched
- **Researched, never pooled** (the uniqueness engine): the 4 venues,
  food_scene, visit, what_to_order, faq, snapshot, glance.
- **Pooled scaffold** (scorer strips it): the cleaning-pivot section, plus
  chrome. `pivot_variant` ∈ {high-volume, pub-town, coastal, market-town}; the
  `pivot_local_hook` keeps same-variant towns from reading identically.

## Pitfalls (learned)
- `json.dumps` emits `"@type": "X"` WITH a space — any schema regex must allow
  `:\s*`.
- Pivot legislation string is "Regulatory Reform (Fire Safety) Order 2005"
  (not "Fire Safety Order 2005"); verify_eat checks the full phrase.
- Do NOT add eat/cleaning words (restaurant, cafe, pub, chef, kitchen, TR19,
  grease, extraction, ductwork, canopy, plenum, baffle, HSE, EHO) to BLEED —
  they are EAT's core vocabulary. BLEED guards only OTHER series (workwear /
  forestry / security / waste / renewables / highways / care-edu).
- meta_description must have NO apostrophes (verify_eat fails on one).
- Never silently rebuild a signed-off flagship; only ADD pages. (London is the
  flagship and is regenerated by the kit for structural consistency — if you
  hand-edit it, keep it in sync with the generator.)

## Standing instruction
Hard checks (verify_eat) are the binding gate. Present the uniqueness score
honestly. Accuracy of venues and TR19/legislation references is paramount — a
wrong recommendation or a closed venue is worse than a missing page.
