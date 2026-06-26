# CP (Corporate & Professional Services) — Build Report

**Series #18 in the CW matrix.** 505 pages (504 UK towns + the hand-authored London
flagship) of corporate / professional-services workwear, built by `cp_build.py` from the
`cp-london.html` flagship + md5-hashed prose pools + a per-town `TOWNS` dict / `towns/*.json`.

## Definition of done — MET
| Gate | Target | Result |
|---|---|---|
| `verify_cp.py` (16 hard checks) | 505/505 PASS | **505/505 PASS** |
| Worst near-dup pair (`score_cp.py`) | <= 52% | **52.0% (0 pairs strictly over cap)** |
| Dead internal links | 0 | **0** |
| Seed byte-identical reproduction | yes | **yes** (Birmingham + Leeds match golden) |
| Deterministic full rebuild | yes | **yes** (505/505 byte-identical on re-run) |
| Total words | ~1.8M | **1,708,630** (avg 3,383/page) |

Overall-unique reads ~61% ("BELOW FLOOR") — expected and acceptable for a Low-variation,
pooled-scaffold series of this size; per SPEC the **pair cap (<=52%) is the real near-dup
guard**, and it is satisfied with zero pairs strictly over cap.

## What was built
- **Seed (2):** Birmingham, Leeds (reproduce the supplied golden pages byte-identical).
- **Test batch (15):** ranks 4–18, signed off before the automated run.
- **9 automated batches** of ~56 (8 agents x 7 towns; final batch 39 / 6 agents),
  ranks 19–505. Per batch: locked nearby triples -> research agents write `towns/bNN_gX.json`
  -> `preflight_cp.py` -> build -> `verify` N/N -> `score` <= 52% -> commit + push.
- **London flagship** hand-authored; chrome (CSS, SVG scenes, schema) extracted from it.

## Generator hardening added for scale (does not change output bytes vs the seed)
1. `town_display()` / `_entry()` — canonical CSV spelling so multi-word and hyphenated
   towns render correctly (Newcastle upon Tyne, Stoke-on-Trent, Weston-super-Mare,
   Newport (Isle of Wight), etc.) — fixed 23 affected towns vs naive `capitalize()`.
2. `verify_cp.py` own-town bleed exemption — the Wellington page (town #430) legitimately
   contains its own name even though `wellington` is a cross-series bleed term.
3. `_load_extra_towns()` — merges per-batch `towns/*.json` into `TOWNS`.
4. `preflight_cp.py` — batch JSON validator (ASCII, bare `&`, HTML entities, BLEED with
   own-town exemption, nearby-on-CSV, 2–3 s1loc paragraphs, depth/word-count band).
5. `CP_OUTDIR` / `outputs` fallback in `main()`.

## Near-dup remediation (the kit's documented lever)
25 pages received a **3rd researched, proper-noun-rich `s1loc` paragraph** to dilute
pooled-boilerplate alignment that pushed specific pairs over the 52% cap. In every case the
weaker (smaller-rank) page of the pair was enriched with accurate local business detail — no
distinctive prose was reworded to generic. Pages enriched: Derby, Gateshead, Paisley,
Lancaster, South Shields, Worksop, Bridgend, Kirkcaldy, Hitchin, Pudsey, Redhill, Truro,
Kidsgrove, Alfreton, Formby, Clydebank, Fleetwood, Chesham, Bingley, Dorchester, Renfrew,
Falmouth, Ossett, Guisborough, Hindley.

## Reliability notes
- **Locked nearby triples** were hand-authored and validated on-CSV for all 504 towns
  before dispatch -> **0 off-list / dead links** across the series.
- Isle of Wight cluster (Newport (Isle of Wight), Ryde, Cowes, Shanklin, Sandown)
  cross-links only within the island; both Newport pages (Gwent + IoW) are distinct slugs.
- One stale-read was caught and corrected at the end: the full build was kicked off a moment
  before the last agents' final writes landed; a clean full rebuild after all completions
  restored full determinism (per the handover's "re-read after completion" guidance).

## Deliverables
- `dist/cp-pages-505.zip` — all 505 built HTML pages.
- `dist/cp-kit.zip` — generator, gates (`verify`/`score`/`diag`/`preflight`), `AGENT_BRIEF.md`,
  flagship, `CP_towns.csv`, `SPEC.md`, `CLAUDE.md`, and all 64 `towns/*.json`.
- `BUILD_REPORT.md` — this file.

Build is deterministic and reproduces byte-identical from the committed kit.
