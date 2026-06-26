# CLAUDE.md — CP (Corporate & Professional Services) runbook

Read **SPEC.md** first. Per-session operating guide. The filesystem resets between
sessions, so the kit is recreated from these committed files.

## What this kit is
A generator (`cp_build.py`) that builds one HTML page per UK town from the
hand-authored London flagship `cp-london.html` + md5-hashed prose pools + a lean
per-town `TOWNS` dict. **Concierge / procurement** posture (a managed account, not the
big-vs-small hybrid split), with **on-brand + account-managed** running through every
page and a narrow, occasion-driven range. Lead polo / softshell / fleece. Output →
`/mnt/user-data/outputs/`.

## Files
- `cp-london.html` — hand-authored flagship (the ONE general-knowledge page; names the
  City/Canary Wharf/Inns of Court/magic-circle/Shoreditch fintech in its local para).
  Chrome is extracted from it, including the realistic embroidery machine, the corporate
  monument sign and the office/bank building.
- `cp_build.py` — generator. `cp-<slug>.html` per town. md5 `pick`; headroom baked in.
- `verify_cp.py` — 16 hard checks (binding gate). Run before every delivery.
- `score_cp.py` / `diag_cp.py` — uniqueness diagnostics (NOT a gate).
- `CP_towns.csv` — 505 towns (Rank, Town, Population, Nation).
- `SPEC.md` / `CLAUDE.md`.

## Per-session setup (filesystem reset)
1. `cp /mnt/user-data/outputs/cp-london.html .` beside `cp_build.py`.
2. Ensure `CP_towns.csv` is beside it (and in the verify-staging dir).
3. The generator reads `cp-london.html` for chrome; never rebuild the flagship.

## Adding towns (the "Go" / batch rhythm)
1. **Web-research each new town first** (mandatory) — real corporate / professional-
   services context: the banks, law firms, accountancies, consultancies, insurers and
   tech firms present; the business district(s); any notable HQs. The 2 local paras
   should be genuinely town-specific and proper-noun rich.
2. Add a `TOWNS[slug]` entry: region, **nearby** (3 geographically-close towns, all on
   CSV), snapshot, s1_head, **s1loc** (exactly 2 local paragraphs), kit_loc, s2_intro.
   Everything else comes from pools.
3. `python3 cp_build.py <slug> [<slug> ...]` → writes to outputs.
4. `python3 verify_cp.py outputs` → must be N/N PASS. **Never ship a FAIL.**
5. Optional: `python3 score_cp.py outputs` and `diag_cp.py outputs` to watch spread.
6. **Never clear previous batches from outputs** — all pages accumulate for one download.

## Hard gate (verify_cp.py)
14 .com + 1 community, no JS, no entities, no delivery claims, title ≤60, meta ≤160
(no apostrophe), town in title+h1, lead trio (polo+softshell+fleece), 4 JSON-LD,
dead-link guard, cross-series bleed. **softshell is NOT blocked here** (CP core). If a
new town trips bleed, it has drifted into another series' vocabulary — fix the copy.

## Critical invariants
- **md5 selector only** (never crc32).
- **14 .com + 1 community** exact. Link-bearing pools (CON_P3=1, ACC_P4=2, SELF=1,
  SORTED=1) — any new variant carries the same link count.
- **Concierge framing**: every page must keep the *managed account* (single point of
  contact, held brand pack, managed reorders) and *on-brand* (exact logo/colours,
  embroidered to guidelines) framing, and the *brand-exercise-not-daily-uniform* angle.
  Do NOT introduce a "direct online for the little guy" hybrid lower tier.
- **Nearby geographic**, hand-authored, on CSV. No rank fallback.
- **Named firms/banks** (HSBC, Big Four, DLA Piper, etc) only in town local paras;
  pooled content stays generic ("banks, law firms, accountancies and tech companies").
- **AVOID in copy:** "charity" (use fundraising/sponsored/community); festival/stage/
  crew/front-of-house/concert (EV signatures); **"wellington"** (boots bleed term — do
  not name Wellington Place/Street; use the city centre / King Street instead).
- SVG chrome: the **monument sign** swaps the centred "{TOWN}" text via `sign_town()`
  (x=230, y=138, centred stack — never clashes with the strapline) + aria + caption;
  the **office building** swaps its aria + caption; the **machine** swaps `a London
  corporate logo` → town. Garment row + order = no swap.

## Turn shorthand
"Go" / "next batch N" → research the towns, add TOWNS entries, build, verify N/N,
present (towns first, then a one-line score). Keep prose minimal; the verify gate is
the contract.
