# CLAUDE.md — HM (Highway Maintenance & Roadworks) runbook

Read **SPEC.md** first. Per-session operating guide. Filesystem resets between
sessions — recreate the kit from these files as needed.

## What HM is
Concierge / Template A location pages for **council highways teams and roadworks
contractors**, one per UK town. Class 3 hi-vis + safety boots + waterproofs lead.
Tarmac-slate palette, hi-vis-yellow SVGs. Identity block = "Chapter 8 and Sector
Scheme Compliant Teams" — the signature thread is **branding placed OFF the
certified reflective area** so Class 3 conspicuity holds. No nation handling.
Nearby = geographic. 14 .com + 1 community per page.

## Session workflow
1. `cd /home/claude/hmkit`. Ensure beside hm_build.py: **hm-london.html** (base
   template the generator reads) and **HM_towns.csv**.
2. For each new town: **web-research first** — the council highways arrangement
   (in-house vs PFI vs term contract), the motorway network + National Highways,
   the contractor mix — then add a `TOWNS[...]` entry: region, **nearby** (3
   geographically-close, all on CSV), snapshot, s1_head, s1loc (4 researched
   paras), kit_loc, s2_intro. Never author from memory. Frame contract details
   as "in recent years" to avoid staleness (highways contracts change).
3. Build: `python3 hm_build.py <slug> ...` → `/mnt/user-data/outputs/hm-<slug>.html`.
4. Verify: copy new files into `/home/claude/hmv/outputs/` then
   `python3 verify_hm.py outputs` — verify only sees files in that dir. Must read
   `==== N/N pages passed all hard checks ====`.
5. Fix any word-count shortfall via str_replace, re-verify.
6. `python3 score_hm.py <dir>` for uniqueness (diagnostic, not a gate).
7. present_files: towns first, then scripts/docs.

## Generator architecture
hm_build.py extracts shared chrome (CSS, header, stats, garment row + 4 SVG
scenes, contact block, footer) from **hm-london.html** via `between()` /
`aria_block()` string markers, then assembles each town from crc32-hashed prose
pools + the per-town TOWNS dict. Section order and 4 JSON-LD blocks fixed.
`signpost_town()` swaps the LONDON plank; SVG town swaps are regex/.replace in
`assemble()` (emb logo, signpost aria+plank+caption, premises aria).
`require_nearby()` hard-fails missing/off-CSV nearby.

## Pitfalls (learned)
- **ORG_BLOCK must be wrapped in its `<script type="application/ld+json">` tag.**
  build_head wraps it; verify check 16 enforces exactly 4 JSON-LD blocks.
- score_hm/diag_hm cloned from RE: after `re_`→`hm_`, also explicitly
  `s/score_re/score_hm/; s/diag_re/diag_hm/`.
- **Do NOT add "Class 3" / "EN ISO 20471" / "hi-vis" / "Chapter 8" to the BLEED
  list** — they are HM's core vocabulary (WM/RE block them; HM must not).
- Keep the "branding off the reflective area" thread — it is the page's
  distinctive compliance point and runs through range, embroidery, contract and
  FAQ.
- Overall uniqueness ~67% at small N (heavy Chapter 8/scaffold). Pair cap (≤52%)
  is the binding guard and passes comfortably. Don't chase 77 at small N.

## Standing instruction
Hard checks (verify_hm) are the binding gate. Present score honestly. Code may
tune the uniqueness gate as the series scales. Never rebuild the flagship; only
ADD pages to /mnt/user-data/outputs/.
