# VT (Veterinary & Animal Care) — build report

**Status: COMPLETE — 505/505 pages green.**

## Result
- **505 pages** built: 504 UK town pages + the London flagship, one `vt-<slug>.html` each.
- **verify_vt.py (the binding gate): 505/505 pass all 16 hard checks.**
- **score_vt.py: worst pair 51.7%** (vt-derby vs vt-gateshead) — under the 52.0% cap, **zero over-cap pairs**.
- Overall-unique **67.1%** — the expected structural ceiling for this pooled-scaffold series (BH shipped 68.4%); the 77% floor is unreachable at this scale and is reported as a diagnostic, not chased.
- **0 dead nearby links** — every `vt-*.html` nearby link across the corpus points to a built page on the CSV.
- ~2.36M words total across the corpus.

## How it was built
Recreated the kit from the handover, applied the §0b fixes (output-dir fallback,
CSV display-casing), and authored the four missing helpers
(`next_towns.py`, `splice_batch.py`, `enrich.py`, `PROMPT_TEMPLATE.md`).
`pick()` confirmed on md5 (the §0 CRC32 bug was absent).

Built in **10 batches** (seed + 9 × ~56 towns), population-rank order, London last:
each batch = `next_towns` → 8 parallel `general-purpose` research agents (real web
research, one `research_bNNg{i}.py` each) → `splice_batch` (validated, non-fatal
per entry) → build → `verify_vt` → `score_vt` → enrich any over-cap pair → commit + push.

Every batch: **56/56 (or 48/48) entries valid, 0 rejected by the splicer.**

## Enrichments (over-cap pairs cleared via enrich.py)
Only **2** pairs ever crossed/approached the cap, both cleared with one researched,
proper-noun-rich sentence on the weaker page (per SPEC 8.3):
1. **Gateshead** (vs Derby, 52.8% → pair to 51.7%) — batch 2.
2. **Whitley Bay** (vs Kidsgrove, 51.98% edge → restored margin) — batch 8.

## Notable disambiguations handled correctly
Newport (Welsh) vs `Newport (Isle of Wight)` (full parenthetical key); Sutton
(S-London borough) vs Sutton Coldfield / Sutton-in-Ashfield; Rothwell = West
Yorkshire; Chapeltown = Sheffield; Gosforth = Newcastle; Wellington = Somerset;
Hythe = Hampshire; Hull (not Kingston upon Hull); exact spellings for
Stoke-on-Trent, Newcastle upon Tyne, Bishop's Stortford, Houghton le Spring,
Grays Thurrock, Thornton Cleveleys, etc. The full Isle of Wight cluster
(Newport IoW / Ryde / Cowes / Shanklin / Sandown) cross-links only within the island.

## Deliverables
- `dist/vt-pages-505.zip` — the 505 built HTML pages.
- `dist/vt-kit.zip` — generator + gates + helpers + flagship + CSV + docs + all 74 research files.

## Reproducing
The built HTML regenerates deterministically from `vt_build.py` (md5 pools):
`cd vt && VT_OUTDIR=outputs python3 vt_build.py && cp vt-london.html outputs/`.
Progress = towns in `vt_build.TOWNS`, so `next_towns.py` resumes correctly after any reset.
