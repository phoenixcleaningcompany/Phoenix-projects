# CLAUDE.md — DC (Delivery & Courier Services) runbook

Read **SPEC.md** first. Per-session operating guide. Filesystem resets between
sessions — recreate the kit from these files as needed.

## What DC is
**Hybrid A/B** location pages for **couriers and delivery firms**, one per UK
town. Branded-uniform led (the driver is the brand on the doorstep). Polo +
hi-vis + softshell lead. Indigo palette. Identity block = "Branded, All-Weather
and Road-Ready: The Delivery Driver's Uniform"; branding section = "Your Driver
Is Your Brand on the Doorstep". The ordering section gives **equal billing** to a
fleet trade account AND an owner-driver ordering direct online. No nation
handling. Nearby = geographic. 14 .com + 1 community per page.

## Hybrid posture (important)
Like RE, neither route is subordinate. The "Ordering" section leads with the
fleet trade account (PO/volume/multi-depot) and the owner-driver direct-online
route as equal options. Keep that balance in any new pools — do not let it drift
into pure concierge (HM) or pure self-checkout (FS).

## Low-variation architecture (important)
DC is a Low-local-variation series. The two generic shared paragraphs ("uniform
before PPE", "layering system") come from **UNIFORM_POOL / LAYER_POOL** (4
town-templated variants each), appended by `s1_paras()`. Each town's `s1loc`
holds ONLY its 2 genuinely-local paragraphs. This keeps near-duplication down at
scale. When adding towns, write just the 2 local paras; never paste the generic
uniform/layering prose into `s1loc`.

## Session workflow
1. `cd /home/claude/dckit`. Ensure beside dc_build.py: **dc-london.html** (base
   template) and **DC_towns.csv**.
2. For each new town: **web-research first** — local logistics geography
   (motorway/distribution connectivity, carrier depots, same-day/owner-driver
   scene) — then add a `TOWNS[...]` entry: region, **nearby** (3
   geographically-close, all on CSV), snapshot, s1_head, s1loc (**2 local paras
   only**), kit_loc, s2_intro. Never author from memory.
3. Build: `python3 dc_build.py <slug> ...` → `/mnt/user-data/outputs/dc-<slug>.html`.
4. Verify: copy new files into `/home/claude/dcv/outputs/` then
   `python3 verify_dc.py outputs`. Must read `==== N/N pages passed all hard checks ====`.
5. Fix any word-count shortfall via str_replace, re-verify.
6. `python3 score_dc.py <dir>` for uniqueness (diagnostic, not a gate).
7. present_files: towns first, then scripts/docs.

## Generator architecture
dc_build.py extracts shared chrome (CSS, header, stats, garment row + 4 SVG
scenes, contact block, footer) from **dc-london.html** via `between()` /
`aria_block()` markers, then assembles each town from crc32-hashed prose pools +
the per-town TOWNS dict. Section order and 4 JSON-LD blocks fixed.
`signpost_town()` swaps the LONDON plank; SVG town swaps in `assemble()` (emb
'a {town} courier company logo', signpost aria + plank + 'every kind of {town}
delivery work' caption, premises 'serving couriers and delivery firms across
{town}'). `require_nearby()` hard-fails missing/off-CSV nearby.

## Pitfalls (learned)
- **ORG_BLOCK must be wrapped in its `<script type="application/ld+json">` tag.**
  build_head wraps it; verify check 16 enforces exactly 4 JSON-LD blocks.
- score_dc/diag_dc cloned from FS: after `fs_`→`dc_`, also explicitly
  `s/score_fs/score_dc/; s/diag_fs/diag_dc/`.
- **Do NOT add polo / softshell / fleece / hi-vis / EN ISO 20471 / courier /
  multidrop / owner-driver to the BLEED list** — they are DC's core vocabulary.
- DC blocks Chapter 8 / National Highways (HM's core) to stay separated, even
  though DC uses hi-vis for roadside work.
- Keep the generic uniform/layering paras in the POOLS, not in s1loc (see Low-
  variation architecture above) — this is what keeps the worst-pair score in
  range as the series grows.
- Overall uniqueness ~64% at small N. Pair cap (≤52%) is the binding guard and
  passes. Don't chase 77 at small N.

## Standing instruction
Hard checks (verify_dc) are the binding gate. Present score honestly. Code may
tune the uniqueness gate as the series scales. Never rebuild the flagship; only
ADD pages to /mnt/user-data/outputs/.
