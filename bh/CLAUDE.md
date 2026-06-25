# CLAUDE.md — BH (Beauty, Hair & Spa) runbook

Read **SPEC.md** first. Per-session operating guide. Filesystem resets between
sessions — recreate the kit from these files as needed.

## What BH is
**Self-checkout / Template B** salon-uniform pages, one per UK town, for **hair,
beauty and spa businesses** (salons, barbers, beauticians, nail techs, spas).
Sole-trader / small-salon buyer. Tunic + polo + apron lead, narrow range. Purple/
blush palette. Identity block = "Look the Part: A Branded Uniform for Salons,
Barbers and Spas"; branding section = "Branding for a One-Chair Barber or a Small
Salon Team". Ordering is direct-online-led (no account), with a trade account as
the secondary route for a larger salon or group. No nation handling. Nearby =
geographic. 14 .com + 1 community per page.

## Self-checkout posture (important)
Lead with order-direct-online-no-account (the route most sole traders and small
salons use); the trade account is the secondary option for a larger salon/spa/
group. Do not let it drift into concierge (trade-account-led) — BH is
self-checkout, like FS.

## Targets the salon business, not the worker
The matrix notes HD already covers the individual-worker audience. BH addresses
the salon/barber/spa *business* (the owner buying a uniform). Keep it that way.

## Low-variation architecture (important)
BH is Low-variation with a narrow range. The generic shared paragraphs come from
**OWNER_POOL / PRESENT_POOL / NARROW_POOL / KIT_POOL** (town-templated), appended
by `s1_paras()` as [local1, local2, OWNER, PRESENT, NARROW+KIT]. Each town's
`s1loc` holds ONLY its 2 genuinely-local paragraphs. Do NOT paste the generic
sole-trader/present/narrow prose into `s1loc`.

## Variant selector — md5 only
`pick()` uses md5 (`hashlib.md5(...).digest()[:4]` % n). **Never revert to
zlib.crc32** — crc32 low bits correlate, collapsing same-length town names onto
identical pool vectors at scale. If you ever see `crc32` in pick(), patch it
before building a single page.

## Session workflow
1. `cd /home/claude/bhkit`. Ensure beside bh_build.py: **bh-london.html** (base
   template) and **BH_towns.csv**.
2. For each new town: **web-research first** — local salon/barber/spa scene
   (high-street density, named districts, the independent/sole-trader mix) — then
   add a `TOWNS[...]` entry: region, **nearby** (3 geographically-close, all on
   CSV), snapshot, s1_head, s1loc (**2 local paras only**), kit_loc, s2_intro.
   Never author from memory.
3. Build: `python3 bh_build.py <slug> ...` → `/mnt/user-data/outputs/bh-<slug>.html`.
4. Verify: copy new files into `/home/claude/bhv/outputs/` then
   `python3 verify_bh.py outputs`. Must read `==== N/N pages passed all hard checks ====`.
5. Fix any word-count shortfall via str_replace, re-verify.
6. `python3 score_bh.py <dir>` for uniqueness (diagnostic, not a gate).
7. present_files: towns first, then scripts/docs.

## Generator architecture
bh_build.py extracts shared chrome (CSS, header, stats, garment row + 4 SVG
scenes, contact block, footer) from **bh-london.html** via `between()` /
`aria_block()` markers, then assembles each town from md5-hashed prose pools + the
per-town TOWNS dict. Section order and 4 JSON-LD blocks fixed. `signpost_town()`
swaps the LONDON plank; SVG town swaps in `assemble()` (emb 'a {town} salon
logo', signpost aria + plank + 'every kind of {town} salon' caption, premises
'serving salons and spas across {town}'). The salon-front fascia "YOUR SALON
NAME" is generic — no swap. `require_nearby()` hard-fails missing/off-CSV nearby.

## Pitfalls (learned)
- **ORG_BLOCK must be wrapped in its `<script type="application/ld+json">` tag.**
  build_head wraps it; verify check 16 enforces exactly 4 JSON-LD blocks.
- score_bh/diag_bh cloned from RT: after `rt_`→`bh_`, also explicitly
  `s/score_rt/score_bh/; s/diag_rt/diag_bh/`.
- **Do NOT add tunic / polo / apron / clog / salon / barber / spa / hoodie to the
  BLEED list** — they are BH's core. "tunic" and "hoodie" were specifically
  REMOVED from the inherited bleed.
- BH blocks RT's retail signatures (tabard/convenience store/garden centre/
  forecourt/farm shop/stockroom) and DC's courier signatures (softshell/multidrop/
  owner-driver/courier) to stay separated.
- Keep the generic present/narrow/sole-trader paras in the POOLS, not in s1loc.
- BH is the densest-scaffold series (narrow range). Headroom was added: product
  cards are pooled (3 variants each via `build_grid`, picked per-town) and FAQ/
  WHY/PRESENT/NARROW are 6 variants, taking worst-pair to ~37% (was 45%). To add
  more, widen CON/ACC/EMB/ORD to 6 - but new CON_P3 variants must carry exactly
  1 .com link and new ACC_P4 variants exactly 2, or the 14-link total breaks.
  Pair cap is the binding guard; don't chase 77 at small N.

## Standing instruction
Hard checks (verify_bh) are the binding gate. Present score honestly. Code may
tune the uniqueness gate as the series scales. Never rebuild the flagship; only
ADD pages to /mnt/user-data/outputs/.
