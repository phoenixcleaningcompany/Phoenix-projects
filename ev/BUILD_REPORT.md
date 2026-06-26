# EV (Entertainment, Events & Festivals) — Build Report

**Series #25 in the CW Hybrid matrix. Status: COMPLETE.**

## Definition of done — hit
- **505 / 505 pages pass `verify_ev.py`** (16 hard checks each).
- **Worst pair 52.0%**, **0 pairs strictly over the 52% cap** (`score_ev.py`).
- **0 dead links** (every `ev-<slug>` nearby/internal link resolves to a CSV town;
  enforced by verify check 15, all pages pass).
- **Byte-identical deterministic rebuild** (`EV_OUTDIR=/tmp/repro` + `filecmp` vs
  `outputs/`: 504 generated pages identical; London flagship is copied, not generated).
- **1,835,800 words** across the 505 pages.

## What was built
- **504 UK towns** (the full `EV_towns.csv`) + the hand-authored **London flagship**
  (`ev-london.html`), one `ev-<slug>.html` page each.
- Posture: **Hybrid** — equal weight to big venues/festivals on trade accounts and
  small independent crews ordering direct online. **Very seasonal** framing, a
  **front-of-house vs crew** split throughout. Leads: **polo / hi-vis / fleece**
  (no softshell, no hoodie — kept in bleed to separate from the TL series).

## Method
- Generator (`ev_build.py`) assembles each page from the London flagship's chrome +
  md5-hashed prose pools + a lean per-town entry (region, nearby triple, snapshot,
  `s1_head`, `s1loc` local paragraphs, `kit_loc`, `s2_intro`). The local `s1loc` block
  is the only genuinely-unique content; everything else is pooled boilerplate.
- **Seed (2 inline: Birmingham, Leeds) + a 15-town test batch (signed off) + 8 batches**
  of ~56 (b01–b08) + a final 39-town batch (b09, including the Isle of Wight cluster).
- Per batch: hand-authored + CSV-validated **locked nearby triples** → 8 background
  research agents wrote `towns/bNN_gX.json` (real web research, no agent-picked nearby)
  → `preflight_ev.py` → build → `verify_ev.py` N/N → `score_ev.py` ≤ 52%
  (3rd/4th/5th-paragraph enrichment on over-cap pairs) → commit + push.

## Duplicate-content lever
- Baseline 2 local paragraphs (test batch + b01–b04); from **b05 onward agents wrote
  3 local paragraphs** up front, which cut over-cap pairs per batch from ~38 to ~7.
- Enrichment remedy for residual over-cap pairs: add a researched, proper-noun-rich
  extra paragraph to the weaker (or the recurring partner) page.
- Final `s1loc` depth: **174 towns at 2 paras, 306 at 3, 21 at 4, 1 at 5.**
- Overall-unique reads ~58–60% ("BELOW FLOOR") — the expected pooled-scaffold ceiling.
  The pair cap (≤52%, 0 over) is the binding near-dup guard and is met.

## Kit hardening added during this build
- `town_display()` / `_entry()` — canonical CSV spelling (fixes "Newcastle upon Tyne",
  "Weston-super-Mare", "Newport (Isle of Wight)", etc.).
- `_load_extra_towns()` — merges per-batch `towns/*.json` into `TOWNS`.
- Own-town **and nearby-name** BLEED exemption in `verify` + `preflight` (the CSV town
  "Wellington" as a neighbour vs the `wellington` bleed word).
- `preflight_ev.py` — batch JSON validator (CSV keys, nearby triples, paragraph depth
  2–5, ASCII, bare-&, entities, bleed).
- `validate_triples.py` — pre-dispatch triple checker.
- `AGENT_BRIEF.md` — single source of truth for the research agents.
- Portable output dir (`EV_OUTDIR` / `./outputs`).

## Gates (run from `ev/`)
```
python3 preflight_ev.py 'towns/*.json'     # batch JSON validity
python3 ev_build.py                         # build all -> outputs/
python3 verify_ev.py outputs                # 505/505 PASS (binding gate)
python3 score_ev.py outputs                 # worst pair 52.0%, 0 over cap
```

## Deliverables
- `dist/ev-pages-505.zip` — the 505 built HTML pages.
- `dist/ev-kit.zip` — generator + gates + helpers + flagship + CSV + docs + all town
  JSON + triples (regenerates the pages byte-identically).
- `BUILD_REPORT.md` — this file.

## Notes
- Built HTML and `dist/` are gitignored; pages regenerate deterministically from the
  committed generator + `towns/*.json`. Every batch's town JSON and triples are committed.
- Commits may show "Unverified" on GitHub (placeholder signing key) — cosmetic.
