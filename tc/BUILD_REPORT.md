# TC (Telecoms & Network Installation) — build report

**Status: COMPLETE — 505/505 pages green.**

## Result
- **505 pages** built: 504 UK town pages + the London flagship, one `tc-<slug>.html` each.
- **verify_tc.py (the binding gate): 505/505 pass all 16 hard checks.**
- **score_tc.py: worst pair 51.4%** (tc-derby vs tc-gateshead) — under the 52.0% cap, **zero over-cap pairs**.
- Overall-unique **69.2%** (= 100 − mean pair dup) — the expected structural ceiling for this pooled-scaffold series; the 77% floor is a diagnostic, not a gate, and is unreachable at this scale.
- **0 dead nearby links** — every `tc-*.html` nearby link across the corpus points to a built page on the CSV.
- ~1.72M words total across the corpus.

## How it was built
Reproduced the kit from the handover and validated it end-to-end (seed pages
rebuild byte-identical; `pick()` confirmed on md5). Applied the §0b-style fixes:
**output-dir fallback** (`$TC_OUTDIR` → `/mnt/user-data/outputs` → local `outputs/`)
and **CSV display-casing** (page names derive from the CSV row, so
`Newcastle upon Tyne`, `Stoke-on-Trent`, `Houghton le Spring` keep their real
casing). Added a per-batch JSON loader (`tc/towns/*.json`) plus `next_towns.py`
(batch planner/validator) and `PROMPT_TEMPLATE.md` (the research-agent spec).

Built in **10 batches** (seed + 9 × ~56 towns), population-rank order, London last:
each batch = `next_towns` → 8 parallel `general-purpose` research agents (real web
research, each writing a validated `tc/towns/bNN_gX.json`) → pre-flight scan
(ASCII / bleed / fields / nearby-on-CSV) → build → `verify_tc` → `score_tc` →
commit + push.

Every batch: **56/56 (or 42/42) entries valid, 0 rejected.** No over-cap pair
ever arose (corpus worst held at 51.4%), so no enrichment was required.

## Notable disambiguations handled correctly
Newport (Welsh) vs `Newport (Isle of Wight)` (full parenthetical key); Sutton
(S-London borough) vs Sutton Coldfield / Sutton-in-Ashfield; Rothwell = West
Yorkshire; Chapeltown = Sheffield; Gosforth = Newcastle; Blackwood = Gwent;
Fulwood = Preston; Hythe = Hampshire; Nelson = Lancashire; Bangor / Buckley =
North Wales; exact spellings for Stoke-on-Trent, Newcastle upon Tyne,
Southend-on-Sea, Bishop's Stortford, Houghton le Spring, Grays Thurrock,
Thornton Cleveleys, etc. The full Isle of Wight cluster
(Newport IoW / Ryde / Cowes / Shanklin / Sandown) cross-links only within the island.

## Kit fixes applied (vs the handover copy)
1. **Output-dir fallback** in `tc_build.py` `main()` (was a hardcoded path that
   crashed on a fresh checkout).
2. **CSV display-casing** (`town_display` / slug-based `_entry` lookup).
3. **JSON batch loader** (`_load_extra_towns`) so batches 3–10 live as
   `tc/towns/*.json` data rather than growing the Python literal. Same data in →
   same pages out (md5-keyed `pick`, order-independent).
4. **verify_tc bleed exemption** for a page's own town name, so Wellington
   (Somerset) builds despite `wellington` being a TC bleed term — the term still
   fails on any other page.

## Deliverables
- `dist/tc-pages-505.zip` — the 505 built HTML pages.
- `dist/tc-kit.zip` — generator + gates + helpers + flagship + CSV + docs + all 70 town JSON batch files.

## Reproducing
The built HTML regenerates deterministically from `tc_build.py` (md5 pools):
`cd tc && python3 tc_build.py && cp tc-london.html outputs/`.
Progress = towns in `tc_build.TOWNS` (seed literal + `tc/towns/*.json`), so
`next_towns.py` resumes correctly after any reset.
