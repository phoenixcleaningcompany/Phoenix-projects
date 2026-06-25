# CLAUDE.md — TC (Telecoms & Network Installation) runbook

Read **SPEC.md** first. Per-session operating guide. The filesystem resets between
sessions, so the kit is recreated from these committed files.

## What this kit is
A generator (`tc_build.py`) that builds one HTML page per UK town from the
hand-authored London flagship `tc-london.html` + md5-hashed prose pools + a lean
per-town `TOWNS` dict. **Hybrid** posture (fleets on trade accounts + subbies direct
online, equal weight). Lead polo / hi-vis / softshell. Output → `/mnt/user-data/outputs/`.

## Files
- `tc-london.html` — hand-authored flagship (the ONE general-knowledge page; names
  Openreach/CityFibre/Virgin Media in its local para). Chrome is extracted from it.
- `tc_build.py` — generator. `tc-<slug>.html` per town. md5 `pick`; headroom baked in.
- `verify_tc.py` — 16 hard checks (binding gate). Run before every delivery.
- `score_tc.py` / `diag_tc.py` — uniqueness diagnostics (NOT a gate).
- `TC_towns.csv` — 505 towns (Rank, Town, Population, Nation).
- `SPEC.md` / `CLAUDE.md`.

## Per-session setup (filesystem reset)
1. `cp /mnt/user-data/outputs/tc-london.html .` beside `tc_build.py`.
2. Ensure `TC_towns.csv` is beside it (and in the verify-staging dir).
3. The generator reads `tc-london.html` for chrome; never rebuild the flagship.

## Adding towns (the "Go" / batch rhythm)
1. **Web-research each new town first** (mandatory) — real local telecoms/network
   context: full-fibre build (Openreach/CityFibre/alt-nets), commercial structured
   cabling, CCTV, the mix of big build contractors + small subbies/ex-BT sole traders.
2. Add a `TOWNS[slug]` entry: region, **nearby** (3 geographically-close towns, all on
   CSV), snapshot, s1_head, **s1loc** (exactly 2 genuinely-local paragraphs, proper-noun
   rich), kit_loc, s2_intro. Everything else comes from pools.
3. `python3 tc_build.py <slug> [<slug> ...]` → writes to outputs.
4. `python3 verify_tc.py outputs` → must be N/N PASS. **Never ship a FAIL.**
5. Optional: `python3 score_tc.py outputs` and `diag_tc.py outputs` to watch spread.
6. **Never clear previous batches from outputs** — all pages accumulate for one download.

## Hard gate (verify_tc.py)
14 .com + 1 community, no JS, no entities, no delivery claims, no Chapter 8, title ≤60,
meta ≤160 (no apostrophe), town in title+h1, lead trio (polo+hi-vis+softshell), 4 JSON-LD,
dead-link guard, cross-series bleed. **softshell is CORE, not bleed.** If a new town trips
bleed, it has drifted into another series' vocabulary — fix the copy, don't weaken the list.

## Critical invariants
- **md5 selector only** (never crc32).
- **14 .com + 1 community** exact. Link-bearing pools (CON_P3=1, ACC_P4=2, SELF=1,
  SORTED=1) — any new variant carries the same link count.
- **Hybrid balance**: every page must name both the fleet/trade-account route and the
  subbie/direct-online route. Do not let pooled variants drift to one side.
- **Nearby geographic**, hand-authored, on CSV. No rank fallback.
- **Openreach/CityFibre/Virgin Media** only in the London flagship; pooled town content
  stays generic ("the major fibre and mobile networks").
- Embroidery scene is the **standard hoop reskinned cyan** — the realistic embroidery
  machine is **VT-only**, do not backport.

## Turn shorthand
"Go" / "next batch N" → research the towns, add TOWNS entries, build, verify N/N, present
(towns first, then a one-line score). Keep prose minimal; the verify gate is the contract.
