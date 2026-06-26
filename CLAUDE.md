# CLAUDE.md — CH2 (Charity & Volunteer) runbook

Read **SPEC.md** first. Per-session operating guide. The filesystem resets between
sessions, so the kit is recreated from these committed files.

## What this kit is
A generator (`ch2_build.py`) that builds one HTML page per UK town from the
hand-authored London flagship `ch2-london.html` + md5-hashed prose pools + a lean
per-town `TOWNS` dict. **Hybrid** posture (national charities on trade accounts +
small volunteer groups/foodbanks direct online, no minimum, equal weight). Lead
polo / hi-vis / fleece. Budget-conscious throughout. Output → `/mnt/user-data/outputs/`.

## Files
- `ch2-london.html` — hand-authored flagship (the ONE general-knowledge page; names
  Trussell Trust/Felix Project/City Harvest in its local para). Chrome is extracted
  from it, including the realistic Barudan-style embroidery machine scene.
- `ch2_build.py` — generator. `ch2-<slug>.html` per town. md5 `pick`; headroom baked in.
- `verify_ch2.py` — 16 hard checks (binding gate). Run before every delivery.
- `score_ch2.py` / `diag_ch2.py` — uniqueness diagnostics (NOT a gate).
- `CH2_towns.csv` — 505 towns (Rank, Town, Population, Nation).
- `SPEC.md` / `CLAUDE.md`.

## Per-session setup (filesystem reset)
1. `cp /mnt/user-data/outputs/ch2-london.html .` beside `ch2_build.py`.
2. Ensure `CH2_towns.csv` is beside it (and in the verify-staging dir).
3. The generator reads `ch2-london.html` for chrome; never rebuild the flagship.

## Adding towns (the "Go" / batch rhythm)
1. **Web-research each new town first** (mandatory) — real local charity/volunteer
   context: the big food-redistribution and foodbank networks (FareShare, Trussell),
   named local charities, charity-shop presence, community/mutual-aid groups, and the
   mix of national charities + tiny volunteer-run projects.
2. Add a `TOWNS[slug]` entry: region, **nearby** (3 geographically-close towns, all on
   CSV), snapshot, s1_head, **s1loc** (exactly 2 genuinely-local paragraphs, proper-
   noun rich), kit_loc, s2_intro. Everything else comes from pools.
3. `python3 ch2_build.py <slug> [<slug> ...]` → writes to outputs.
4. `python3 verify_ch2.py outputs` → must be N/N PASS. **Never ship a FAIL.**
5. Optional: `python3 score_ch2.py outputs` and `diag_ch2.py outputs` to watch spread.
6. **Never clear previous batches from outputs** — all pages accumulate for one download.

## Hard gate (verify_ch2.py)
14 .com + 1 community, no JS, no entities, no delivery claims, title ≤60, meta ≤160
(no apostrophe), town in title+h1, lead trio (polo+hi-vis+fleece), 4 JSON-LD,
dead-link guard, cross-series bleed. **softshell is BLOCKED** (CH2 never uses it). If
a new town trips bleed, it has drifted into another series' vocabulary — fix the copy,
don't weaken the list.

## Critical invariants
- **md5 selector only** (never crc32).
- **14 .com + 1 community** exact. Link-bearing pools (CON_P3=1, ACC_P4=2, SELF=1,
  SORTED=1) — any new variant carries the same link count.
- **Hybrid balance + budget**: every page must name both the national-charity/trade-
  account route and the local-group/direct-online/no-minimum route, and keep the
  affordable / every-pound-off-the-cause framing. Do not drift to one side.
- **No "tabard"** (use aprons) and **no "hoodie"** (use sweatshirts/zip tops).
- **Nearby geographic**, hand-authored, on CSV. No rank fallback.
- **Trussell / FareShare / named charities** only in town local paras; pooled content
  stays generic ("the big food-redistribution and foodbank networks").
- Embroidery scene is the **realistic Barudan-style machine** (CH2 uses it; matches
  uploaded photo). aria swaps `a London charity logo` → town.

## Turn shorthand
"Go" / "next batch N" → research the towns, add TOWNS entries, build, verify N/N,
present (towns first, then a one-line score). Keep prose minimal; the verify gate is
the contract.
