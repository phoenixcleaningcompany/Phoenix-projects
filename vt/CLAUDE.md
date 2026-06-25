# CLAUDE.md — VT (Veterinary & Animal Care) runbook

Read **SPEC.md** first. Per-session operating guide. Filesystem resets between
sessions — recreate the kit from these files as needed.

## What VT is
**Self-checkout / Template B** veterinary and animal care pages, one per UK town,
for **vet practices, kennels, catteries, dog groomers and equine yards** (mostly
small businesses and sole traders). Scrubs + polo + fleece lead. Teal-green + tan
palette. Differentiator = **two environments**: clinical (scrubs/tunics/polos)
and hands-on/outdoor (fleeces/waterproofs/safety shoes/wellingtons). Identity =
"From the Consulting Room to the Kennels and Yard"; branding section = "Branding
for a Practice, a Kennels or a Mobile Groomer". Ordering is direct-online-led (no
account), trade account secondary for a larger practice/group. No nation handling.
Nearby = geographic. 14 .com + 1 community per page.

## Self-checkout posture (important)
Lead with order-direct-online-no-account (most buyers are small practices/sole
traders); the trade account is the secondary option for a larger practice, group
or multi-site operator. Do not let it drift into concierge (trade-account-led).

## Two-environments is the spine
The clinical/outdoor split is the whole identity. Keep PRESENT_POOL (the
two-environments para) front and centre - it is what separates VT from a generic
uniform series. Clinical = scrubs/tunics/polos (hygiene, owner reassurance);
outdoor = fleeces/waterproofs/safety shoes/wellingtons (kennels/yard/field).

## Low-variation + headroom architecture (important)
Generic shared paragraphs come from **OWNER(6)/PRESENT(6)/NARROW(6)/KIT(6)**
pools (town-templated), appended by `s1_paras()` as [local1, local2, OWNER,
PRESENT, NARROW+KIT]. Each town's `s1loc` holds ONLY its 2 genuinely-local
paragraphs. Do NOT paste the generic two-environments/narrow/sole-trader prose
into `s1loc`. Product cards are pooled **3 variants each** via `build_grid`;
FAQ/WHY at 6 variants. This headroom is why VT's worst pair sits ~31% (best of
the Low-variation set) - keep it.

## Variant selector — md5 only
`pick()` uses md5. **Never revert to zlib.crc32** - crc32 low bits correlate,
collapsing same-length town names onto identical pool vectors at scale. If you
ever see `crc32` in pick(), patch it before building a single page.

## Session workflow
1. `cd /home/claude/vtkit`. Ensure beside vt_build.py: **vt-london.html** (base
   template) and **VT_towns.csv**.
2. For each new town: **web-research first** - local vet/animal-care scene
   (practices and groups, kennels/catteries, rescues, groomers, equine/farm on
   the rural edge) - then add a `TOWNS[...]` entry: region, **nearby** (3
   geographically-close, all on CSV), snapshot, s1_head, s1loc (**2 local paras
   only**), kit_loc, s2_intro. Never author from memory.
3. Build: `python3 vt_build.py <slug> ...` → `/mnt/user-data/outputs/vt-<slug>.html`.
4. Verify: copy new files into `/home/claude/vtv/outputs/` then
   `python3 verify_vt.py outputs`. Must read `==== N/N pages passed all hard checks ====`.
5. Fix any word-count shortfall via str_replace, re-verify.
6. `python3 score_vt.py <dir>` for uniqueness (diagnostic, not a gate).
7. present_files: towns first, then scripts/docs.

## Generator architecture
vt_build.py extracts shared chrome (CSS, header, stats, **dog-in-cone scene** in
the garment-row slot + 4 SVG scenes, contact block, footer) from **vt-london.html**
via `between()` / `aria_block()` markers, then assembles each town from md5-hashed
prose pools + the per-town TOWNS dict. SVG town swaps in `assemble()`: emb 'a
{town} vet practice logo', signpost aria + LONDON plank (via signpost_town) + 'every
kind of {town} animal care' caption, premises 'serving vets and animal care across
{town}'. The dog scene and the practice fascia "YOUR PRACTICE NAME" are generic -
no swap. `require_nearby()` hard-fails missing/off-CSV nearby.

## Image policy (learned this build)
Two scenes are VT-only to stop cross-build duplication: the **dog-in-cone** (lead)
and the **realistic embroidery machine**. Per Damien: the embroidery machine stays
**VT-only** (do NOT retrofit other series); the **single dog is fine** identical on
all pages (mascot, no per-town variants needed).

## Pitfalls (learned)
- **ORG_BLOCK must be wrapped in its `<script type="application/ld+json">` tag.**
  build_head wraps it; verify check 16 enforces exactly 4 JSON-LD blocks.
- score_vt/diag_vt cloned from BH: after `bh_`→`vt_`, also explicitly
  `s/score_bh/score_vt/; s/diag_bh/diag_vt/`.
- **Do NOT add scrubs/tunic/polo/fleece/waterproof/vet/kennel/cattery/equine/
  animal/wellington/grooming/apron to the BLEED list** - they are VT core.
  **"salon" is intentionally LEGAL** (dog grooming salons) - only BH's
  hair/beauty terms (barber/hairdressing/beautician/clog/hoodie/spa day) are
  blocked.
- Keep the generic two-environments/narrow/sole-trader paras in the POOLS, not
  in s1loc.
- VT's worst pair (~31%) is the best of the Low-variation set thanks to the
  built-in headroom (pooled cards + 6-variant FAQ/WHY/PRESENT/NARROW). Keep it.

## Standing instruction
Hard checks (verify_vt) are the binding gate. Present score honestly. Never
rebuild the flagship; only ADD pages to /mnt/user-data/outputs/.
