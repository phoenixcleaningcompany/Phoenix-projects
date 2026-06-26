# CLAUDE.md — EV (Entertainment, Events & Festivals) runbook

Read **SPEC.md** first. Per-session operating guide. The filesystem resets between
sessions, so the kit is recreated from these committed files.

## What this kit is
A generator (`ev_build.py`) that builds one HTML page per UK town from the
hand-authored London flagship `ev-london.html` + md5-hashed prose pools + a lean
per-town `TOWNS` dict. **Hybrid** posture (big venues/festivals on trade accounts +
small independent crews direct online, equal weight), **very seasonal** framing, and
a front-of-house / crew split throughout. Lead polo / hi-vis / fleece. Output →
`/mnt/user-data/outputs/`.

## Files
- `ev-london.html` — hand-authored flagship (the ONE general-knowledge page; names the
  O2/Wembley/West End/BST Hyde Park/Notting Hill Carnival in its local para). Chrome is
  extracted from it, including the realistic embroidery machine, the festival sign and
  the DJ-stage scene.
- `ev_build.py` — generator. `ev-<slug>.html` per town. md5 `pick`; headroom baked in.
- `verify_ev.py` — 16 hard checks (binding gate). Run before every delivery.
- `score_ev.py` / `diag_ev.py` — uniqueness diagnostics (NOT a gate).
- `EV_towns.csv` — 505 towns (Rank, Town, Population, Nation).
- `SPEC.md` / `CLAUDE.md`.

## Per-session setup (filesystem reset)
1. `cp /mnt/user-data/outputs/ev-london.html .` beside `ev_build.py`.
2. Ensure `EV_towns.csv` is beside it (and in the verify-staging dir).
3. The generator reads `ev-london.html` for chrome; never rebuild the flagship.

## Adding towns (the "Go" / batch rhythm)
1. **Web-research each new town first** (mandatory) — real local events/festivals
   context: the marquee arenas/venues, the music/theatre scene, the big festivals (and
   their sites), any event-production/staging trade. The 2 local paras should be
   genuinely town-specific and proper-noun rich.
2. Add a `TOWNS[slug]` entry: region, **nearby** (3 geographically-close towns, all on
   CSV), snapshot, s1_head, **s1loc** (exactly 2 local paragraphs), kit_loc, s2_intro.
   Everything else comes from pools.
3. `python3 ev_build.py <slug> [<slug> ...]` → writes to outputs.
4. `python3 verify_ev.py outputs` → must be N/N PASS. **Never ship a FAIL.**
5. Optional: `python3 score_ev.py outputs` and `diag_ev.py outputs` to watch spread.
6. **Never clear previous batches from outputs** — all pages accumulate for one download.

## Hard gate (verify_ev.py)
14 .com + 1 community, no JS, no entities, no delivery claims, title ≤60, meta ≤160
(no apostrophe), town in title+h1, lead trio (polo+hi-vis+fleece), 4 JSON-LD,
dead-link guard, cross-series bleed. **softshell is BLOCKED here** (EV does not use
it — separates from TL). If a new town trips bleed, it has drifted into another
series' vocabulary — fix the copy.

## Critical invariants
- **md5 selector only** (never crc32).
- **14 .com + 1 community** exact. Link-bearing pools (CON_P3=1, ACC_P4=2, SELF=1,
  SORTED=1) — any new variant carries the same link count.
- **Hybrid balance + FOH/crew + seasonal**: every page must name both the big-venue/
  trade-account route and the independent-crew/direct-online route, keep the
  front-of-house vs crew split, and keep the seasonal-intake framing. Do not drift.
- **Nearby geographic**, hand-authored, on CSV. No rank fallback.
- **Named venues/festivals** (O2 Academy, First Direct Arena, Leeds Festival, etc) only
  in town local paras; pooled content stays generic ("major venues, festival operators
  and production companies").
- SVG chrome: the **festival sign** swaps the big "{TOWN}" text via `sign_town()` (y=104)
  + aria + caption; the **DJ stage** swaps its aria + caption; the **machine** swaps
  `a London event logo` → town. Garment row + order = no swap.
- Avoid softshell and security signatures (SIA / door supervision / stab vest) in copy.

## Turn shorthand
"Go" / "next batch N" → research the towns, add TOWNS entries, build, verify N/N,
present (towns first, then a one-line score). Keep prose minimal; the verify gate is
the contract.
