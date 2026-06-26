# CLAUDE.md — TL (Travel, Tourism & Leisure) runbook

Read **SPEC.md** first. Per-session operating guide. The filesystem resets between
sessions, so the kit is recreated from these committed files.

## What this kit is
A generator (`tl_build.py`) that builds one HTML page per UK town from the
hand-authored London flagship `tl-london.html` + md5-hashed prose pools + a lean
per-town `TOWNS` dict. **Hybrid** posture (big attractions on trade accounts +
small independents direct online, equal weight), **seasonal** framing throughout.
Lead polo / fleece / softshell. Output → `/mnt/user-data/outputs/`.

## Files
- `tl-london.html` — hand-authored flagship (the ONE general-knowledge page; names
  Cadbury World / SEA LIFE / LEGOLAND etc in its local para). Chrome is extracted from
  it, including the realistic embroidery machine, the attraction-sign and the aeroplane.
- `tl_build.py` — generator. `tl-<slug>.html` per town. md5 `pick`; headroom baked in.
- `verify_tl.py` — 16 hard checks (binding gate). Run before every delivery.
- `score_tl.py` / `diag_tl.py` — uniqueness diagnostics (NOT a gate).
- `TL_towns.csv` — 505 towns (Rank, Town, Population, Nation).
- `SPEC.md` / `CLAUDE.md`.

## Per-session setup (filesystem reset)
1. `cp /mnt/user-data/outputs/tl-london.html .` beside `tl_build.py`.
2. Ensure `TL_towns.csv` is beside it (and in the verify-staging dir).
3. The generator reads `tl-london.html` for chrome; never rebuild the flagship.

## Adding towns (the "Go" / batch rhythm)
1. **Web-research each new town first** (mandatory) — real local tourism/leisure
   context: the marquee visitor attractions, theme/holiday parks, activity centres,
   museums/heritage sites, the hotel and tour-operator trade, any airport. Medium
   variation means the 2 local paras should be genuinely town-specific and proper-noun
   rich.
2. Add a `TOWNS[slug]` entry: region, **nearby** (3 geographically-close towns, all on
   CSV), snapshot, s1_head, **s1loc** (exactly 2 local paragraphs), kit_loc, s2_intro.
   Everything else comes from pools.
3. `python3 tl_build.py <slug> [<slug> ...]` → writes to outputs.
4. `python3 verify_tl.py outputs` → must be N/N PASS. **Never ship a FAIL.**
5. Optional: `python3 score_tl.py outputs` and `diag_tl.py outputs` to watch spread.
6. **Never clear previous batches from outputs** — all pages accumulate for one download.

## Hard gate (verify_tl.py)
14 .com + 1 community, no JS, no entities, no delivery claims, title ≤60, meta ≤160
(no apostrophe), town in title+h1, lead trio (polo+fleece+softshell), 4 JSON-LD,
dead-link guard, cross-series bleed. **softshell is CORE here** (not bleed). If a new
town trips bleed, it has drifted into another series' vocabulary — fix the copy.

## Critical invariants
- **md5 selector only** (never crc32).
- **14 .com + 1 community** exact. Link-bearing pools (CON_P3=1, ACC_P4=2, SELF=1,
  SORTED=1) — any new variant carries the same link count.
- **Hybrid balance + seasonal**: every page must name both the big-attraction/trade-
  account route and the independent/direct-online route, and keep the seasonal-intake
  framing. Do not drift to one side.
- **Nearby geographic**, hand-authored, on CSV. No rank fallback.
- **Named attractions** (Cadbury World, Royal Armouries, etc) only in town local paras;
  pooled content stays generic ("major attractions, theme parks and hotel groups").
- SVG chrome: the **attraction sign** swaps the big "WELCOME TO {TOWN}" text via
  `sign_town()` + aria + caption; the **aeroplane** swaps its aria + caption; the
  **machine** swaps `a London tourism logo` → town. Garment row + order = no swap.

## Turn shorthand
"Go" / "next batch N" → research the towns, add TOWNS entries, build, verify N/N,
present (towns first, then a one-line score). Keep prose minimal; the verify gate is
the contract.
