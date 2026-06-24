# CLAUDE.md — RT (Supermarkets & Retail) runbook

Read **SPEC.md** first. Per-session operating guide. Filesystem resets between
sessions — recreate the kit from these files as needed.

## What RT is
**Concierge / Template A** retail-uniform pages, one per UK town, **targeting
independent retailers, convenience stores, forecourts, garden centres, farm shops
and small multi-store groups** — NOT the big chains (they tender centrally).
Staff-uniform led (the staff are the shopfront). Tabard + polo + fleece lead.
Burgundy palette. Identity block = "Your Staff Are Your Shopfront: A Consistent
Retail Uniform"; branding section = "Branding That Builds Trust on the Shop
Floor". Ordering is managed-trade-account-led with direct-online as the secondary
route for a single shop. No nation handling. Nearby = geographic. 14 .com + 1
community per page.

## Concierge posture (important)
Lead with the managed trade account (one contact, agreed pricing, uniform list on
file, reorders for new starters/seasonal staff, multi-store consistency); the
single-shop direct-online route is secondary. Do not let it drift into Hybrid
(equal billing) or self-checkout-led — RT is concierge.

## Independents-not-chains targeting (important)
The matrix note is explicit: major chains procure centrally via national tender,
so RT targets independents. OWNER_POOL and FAQ #4 carry this. Keep it in any new
pools — never address the page to a national supermarket chain's buying team.

## Low-variation architecture (important)
RT is a Low-local-variation series. The generic shared paragraphs come from
**SHOPFRONT_POOL / CONSIST_POOL / OWNER_POOL / KIT_POOL** (town-templated),
appended by `s1_paras()` as [local1, local2, OWNER, SHOPFRONT, CONSIST+KIT]. Each
town's `s1loc` holds ONLY its 2 genuinely-local paragraphs. This keeps near-
duplication down at scale. When adding towns, write just the 2 local paras; never
paste the generic shopfront/consistency/chains prose into `s1loc`.

## Session workflow
1. `cd /home/claude/rtkit`. Ensure beside rt_build.py: **rt-london.html** (base
   template) and **RT_towns.csv**.
2. For each new town: **web-research first** — local independent-retail scene
   (high streets, shopping parades, arcades/markets, convenience density, garden
   centres, farm shops) — then add a `TOWNS[...]` entry: region, **nearby** (3
   geographically-close, all on CSV), snapshot, s1_head, s1loc (**2 local paras
   only**), kit_loc, s2_intro. Never author from memory.
3. Build: `python3 rt_build.py <slug> ...` → `/mnt/user-data/outputs/rt-<slug>.html`.
4. Verify: copy new files into `/home/claude/rtv/outputs/` then
   `python3 verify_rt.py outputs`. Must read `==== N/N pages passed all hard checks ====`.
5. Fix any word-count shortfall via str_replace, re-verify.
6. `python3 score_rt.py <dir>` for uniqueness (diagnostic, not a gate).
7. present_files: towns first, then scripts/docs.

## Generator architecture
rt_build.py extracts shared chrome (CSS, header, stats, garment row + 4 SVG
scenes, contact block, footer) from **rt-london.html** via `between()` /
`aria_block()` markers, then assembles each town from crc32-hashed prose pools +
the per-town TOWNS dict. Section order and 4 JSON-LD blocks fixed.
`signpost_town()` swaps the LONDON plank; SVG town swaps in `assemble()` (emb
'a {town} retail company logo', signpost aria + plank + 'every kind of {town}
retail' caption, premises 'serving independent retailers across {town}'). The
shopfront fascia text "YOUR SHOP NAME" is generic — no swap. `require_nearby()`
hard-fails missing/off-CSV nearby.

## Pitfalls (learned)
- **ORG_BLOCK must be wrapped in its `<script type="application/ld+json">` tag.**
  build_head wraps it; verify check 16 enforces exactly 4 JSON-LD blocks.
- score_rt/diag_rt cloned from DC: after `dc_`→`rt_`, also explicitly
  `s/score_dc/score_rt/; s/diag_dc/diag_rt/`.
- **Do NOT add tabard / polo / fleece / safety shoes / hi-vis / cargo / retail /
  convenience store / garden centre to the BLEED list** — they are RT's core.
  "tabard" was specifically REMOVED from the inherited cleaning bleed line.
- RT blocks DC's signature (multidrop/owner-driver/softshell) and the other
  series' cores to stay separated, even though both use hi-vis.
- Keep the generic shopfront/consistency/chains paras in the POOLS, not in s1loc
  (see Low-variation architecture) — this is what keeps the worst-pair score in
  range as the series grows.
- Overall uniqueness ~62% at small N. Pair cap (≤52%) is the binding guard and
  passes (~38%). Don't chase 77 at small N.

## Standing instruction
Hard checks (verify_rt) are the binding gate. Present score honestly. Code may
tune the uniqueness gate as the series scales. Never rebuild the flagship; only
ADD pages to /mnt/user-data/outputs/.
