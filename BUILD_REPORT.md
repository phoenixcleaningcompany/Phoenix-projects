# CH2 (Charity & Volunteer Workwear) — Build Report

**Status: COMPLETE.** Full 505-page series built, verified and pushed to
`claude/build-files-handover-doc-5b95ss`.

## Final scoreboard
- **Verify (binding gate): 505/505 pages PASS** all 16 hard checks.
- **Worst pair dup: 50.9%** (cap 52%, **0 pairs over**) — Milton Keynes vs Nottingham.
- **Overall unique: 66.0%** (diagnostic; 77% floor is not reachable at 505 pages with
  the pooled scaffold — expected per SPEC, and not a gate).
- **0 dead nearby links** — all 504 towns' nearby triples validated on `CH2_towns.csv`.
- Per page ~4.7k–4.9k words; ~2.4M words across the series.

## Coverage
504 UK towns (every buildable row on `CH2_towns.csv`) + the hand-authored London
flagship = 505 pages. Built in a seed (Birmingham, Leeds) + 10 batches by population
rank, London never a target. Isle of Wight cluster (Newport (Isle of Wight), Ryde,
Cowes, Shanklin, Sandown) cross-links only within the island.

## Method
Each town was individually web-researched by a `general-purpose` agent (8 groups of 7
per batch, agents writing their own validated `towns/bNN_*.json`). Every town carries
3 genuinely-local, proper-noun-rich paragraphs naming the real local FareShare /
food-redistribution operation, named Trussell and independent foodbanks, community
pantries, a community foundation or CVS, named local charities/hospices and real
districts. Nearby triples were pre-assigned from the CSV (geographic, hand-verified)
and locked per agent, so there were zero off-list links. Each batch: pre-flight scan
(ASCII / no `&` / fields / shape / bleed / nearby-on-CSV) -> build -> `verify` N/N ->
`score` -> commit + push.

## Kit changes made during the build (all committed)
The delivered kit was a seed (London + Birmingham + Leeds). To run the full series the
4 handover kit fixes were applied, plus pool/quality work:

1. **Output-dir fallback** (`CH_OUTDIR` / `outputs/`) instead of a hardcoded path.
2. **`towns/*.json` loader** merged into `TOWNS` at import (research agents write their
   own files; same data in -> identical pages out).
3. **Slug-robust display + lookup** (`town_display` / `_entry`) so mixed-case towns
   (Newcastle upon Tyne, Stoke-on-Trent, Houghton le Spring, Bishop's Stortford, the
   Welsh vs Isle of Wight Newports) render and match correctly. Added `snapshot` /
   `kit_loc` template fallbacks so batch JSON holds only genuinely-local fields.
4. **Own-town bleed exemption** in `verify_ch2.py` so a page whose town name is a bleed
   term (Wellington, Somerset) passes while the term still fails on every other page.
5. **`next_towns.py`** — resume-safe batch planner (`--done` / `N` / `--slugs` / `--check`).
6. **Pool widening 4 -> 6** on the EMB/CON/ACC section pools (link counts preserved:
   CON_P3 = 1, ACC_P4 = 2) for cross-page spread.
7. **3 local paragraphs per town** from batch 03 onward (the durable lever that kept the
   near-dup ceiling down as N grew); the early 2-paragraph towns (Derby, Gateshead,
   Dudley, Ipswich, Milton Keynes, Chelmsford, Sunderland, Dundee, Maidstone) were
   reactively enriched with a 3rd paragraph when they surfaced near the 52% cap.

## Reproduce / resume
The build is deterministic (md5 `pick`). After any filesystem reset:
`cp ch2-london.html` beside `ch2_build.py`, ensure `CH2_towns.csv` is present, then
`CH_OUTDIR=outputs python3 ch2_build.py` rebuilds all 505 pages byte-identically.
`python3 next_towns.py` reports progress; `verify_ch2.py outputs` is the gate.
Built HTML is gitignored (`outputs/`, `dist/`) and regenerates from the committed
generator + `towns/*.json`; nothing built needs to live in git.
