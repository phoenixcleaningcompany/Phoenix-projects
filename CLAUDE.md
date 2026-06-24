# CLAUDE.md — FS (Forestry, Arboriculture & Tree Surgery) runbook

Read **SPEC.md** first. Per-session operating guide. Filesystem resets between
sessions — recreate the kit from these files as needed.

## What FS is
**Template B (self-checkout)** location pages for **sole-trader arborists and
small tree-surgery crews**, one per UK town. Chainsaw trousers + safety boots +
forestry helmet lead. Forest-green palette, orange chainsaw-PPE SVGs. Identity
block = "Chainsaw-Rated, Climb-Ready PPE: EN ISO 11393 for Arborists" (Type A
ground / Type C climbing). **The posture is direct online ordering — no account,
no minimum, no quote.** No nation handling. Nearby = geographic. 14 .com + 1
community per page.

## Template B vs the A-series (important)
This is the first self-checkout series. Do NOT bring over the concierge thread
(trade accounts / PO ordering / multi-depot frameworks as the main route). Here
the buyer is the owner-operator; the "How to Order" section is self-checkout-led,
with a trade account only as a brief "if your team grows" mention. Keep that
voice in any new pools.

## Session workflow
1. `cd /home/claude/fskit`. Ensure beside fs_build.py: **fs-london.html** (base
   template the generator reads) and **FS_towns.csv**.
2. For each new town: **web-research first** — the urban-forest/woodland
   character, named parks, the council/park tree work, the local small-firm/
   sole-trader scene, NPTC/LANTRA/Arb Association, BS 3998 / BS 5837 — then add a
   `TOWNS[...]` entry: region, **nearby** (3 geographically-close, all on CSV),
   snapshot, s1_head, s1loc (4 researched paras), kit_loc, s2_intro. Never author
   from memory.
3. Build: `python3 fs_build.py <slug> ...` → `/mnt/user-data/outputs/fs-<slug>.html`.
4. Verify: copy new files into `/home/claude/fsv/outputs/` then
   `python3 verify_fs.py outputs` — verify only sees files in that dir. Must read
   `==== N/N pages passed all hard checks ====`.
5. Fix any word-count shortfall via str_replace, re-verify.
6. `python3 score_fs.py <dir>` for uniqueness (diagnostic, not a gate).
7. present_files: towns first, then scripts/docs.

## Generator architecture
fs_build.py extracts shared chrome (CSS, header, stats, garment row + 4 SVG
scenes, contact block, footer) from **fs-london.html** via `between()` /
`aria_block()` string markers, then assembles each town from crc32-hashed prose
pools + the per-town TOWNS dict. Section order and 4 JSON-LD blocks fixed.
`signpost_town()` swaps the LONDON plank; SVG town swaps in `assemble()` (emb
'a {town} tree surgery company logo', signpost aria + plank + 'every kind of
{town} tree work' caption, premises 'serving arborists and tree surgeons across
{town}'). `require_nearby()` hard-fails missing/off-CSV nearby.

## Pitfalls (learned)
- **ORG_BLOCK must be wrapped in its `<script type="application/ld+json">` tag.**
  build_head wraps it; verify check 16 enforces exactly 4 JSON-LD blocks.
- score_fs/diag_fs cloned from HM: after `hm_`→`fs_`, also explicitly
  `s/score_hm/score_fs/; s/diag_hm/diag_fs/`.
- **Do NOT add chainsaw / EN ISO 11393 / tree surgery / arborist / LANTRA /
  NPTC / Type A / Type C to the BLEED list** — they are FS's core vocabulary.
- FS blocks **Chapter 8 / National Highways / sector scheme** (HM's core) so the
  two stay separated, even though FS uses hi-vis for roadside work.
- Keep the chainsaw-PPE EN ISO 11393 / Type A vs C thread and the self-checkout
  ordering voice — they are the page's distinctive points.
- Overall uniqueness ~66% at small N (heavy chainsaw scaffold). Pair cap (≤52%)
  is the binding guard and passes comfortably. Don't chase 77 at small N.

## Standing instruction
Hard checks (verify_fs) are the binding gate. Present score honestly. Code may
tune the uniqueness gate as the series scales. Never rebuild the flagship; only
ADD pages to /mnt/user-data/outputs/.
