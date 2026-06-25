# VT Series — Veterinary & Animal Care Workwear (SPEC)

**Series #24 in the CW Hybrid matrix.** One HTML page per UK town for veterinary
and animal care businesses. Prefix `vt-`. Canonical/og to
`https://www.ineedworkwear.uk/vt-<slug>.html`.

## Audience & posture — SELF-CHECKOUT / Template B
Audience = **Small Biz**, tone = **Self-checkout**. Buyers are vet practices,
kennels, catteries, dog groomers (salon + mobile) and equine yards - **mostly
small businesses and sole traders**. The ordering section is **direct-online-led,
no account** (the route most use): browse, pick the few pieces you need, add
sizes, send the logo once, check out. A **trade account** is the secondary option
for a larger practice, veterinary group or multi-site operator. Workwear depth
**Low**, local variation **Low**.

## The differentiator — TWO ENVIRONMENTS
This is what makes VT its own series. The same business works across:
- **Clinical** (consulting/operating room): scrubs, tunics, polos - wash hot,
  look professional, reassure a worried owner their animal is in clean, capable
  hands. The side the owner sees; carries the practice's trust.
- **Hands-on / outdoor** (kennels, catteries, grooming room, stables, fields):
  fleeces for warmth, waterproofs for the wet and wash-down, safety shoes and
  wellingtons for muck, paws and hooves.
Identity block (id `#contract`) = **"From the Consulting Room to the Kennels and
Yard"**; branding section = **"Branding for a Practice, a Kennels or a Mobile
Groomer"**. The value proposition: one supplier for both sides, branded the same.
**No nation handling.**

## Lead products (verifier-enforced)
LEAD = **scrubs**, CO_LEAD = **polo**, TRI_LEAD = **fleece**. 8-card grid:
Veterinary Scrubs / Tunics and Vet Nurse Tops / Polo Shirts and T-Shirts /
Fleeces and Mid-Layers / Waterproofs and Outdoor Jackets / Safety Shoes and
Wellingtons / Aprons, Caps and Accessories / Embroidery, Names and ID.

## Palette / design
Teal-green `#0f766e` (hover `#115e54`) + charcoal `#0f172a` + amber `#f59e0b`
highlight; SVG accents teal `#14b8a6`/`#2dd4bf` + warm tan `#b45309` + cream.
Page bg `#eef4f2`, cards `#e1efe9`/border `#c2ddd4`, muted `#4a635c`, stat values
`#0d9488`, links `#0f766e`, dark-section accent `#5eead4`, nearby bg `#e1ece8`.
Distinct from every prior series (teal-green clinical + tan animal-care warmth).
Fonts Lora + Source Sans 3. 2 radial + 1 linear gradient.

## SVG scenes (5) - two are VT-ONLY, not the shared templates
To stop images duplicating across builds, two scenes are bespoke to VT:
1. **Dog in a vet recovery cone** (the lead image, replaces the generic garment
   row) - brown/cream sitting dog in a translucent cone, teal collar, soft mint
   ground with faint plant and bowl. **No town reference - pure shared chrome
   (identical on every page; it is a mascot, by design).**
2. **Realistic multi-needle embroidery machine + blue hoop** (replaces the
   generic embroidery-hoop scene) - white machine head, threads descending, silver
   needle bar, bright-blue tubular hoop holding a navy garment with a part-stitched
   logo, blue pantograph arm. **VT-ONLY - do not retrofit to other series.** Keeps
   the swappable aria-label "a London vet practice logo" for per-town personalising.
The remaining 3 (signpost VET KIT / CLINIC AND KENNELS, vet-practice premises with
paw-print sign + vet-cross plaque, order-online laptop) are town-personalised.

## Hard rules (verify_vt.py, 16 checks)
1. Exactly **14 .com hrefs + 1 co.uk/community**. 2. No JS (ld+json only).
3. No HTML entities. 4. No delivery-timescale claims ("standard lead times" OK).
5. Title ≤60, meta ≤160, no apostrophes in meta. 6. Fonts Lora + Source Sans 3.
7. Organization+Service schema only. 8. **4 JSON-LD blocks** (check 16). 9. Lead
trio present (scrubs/polo/fleece). 10. Word-count floor. 11. Dead-link guard:
every `vt-<slug>.html` link must be a CSV town (check 15).
12. **BLEED ban**: inherited food/security/cleaning/waste/renewables/highways/
forestry/care(Ofsted,CQC)/sports/retail/courier bleed, PLUS **BH hair/beauty
signatures (barber, hairdressing, beautician, clog, hoodie, spa day)**.
**NOTE: scrubs, tunic, polo, fleece, waterproof, vet, veterinary, kennel,
cattery, equine, animal, wellington, safety shoes, grooming, apron and
"grooming salon" are LEGAL for VT (its core). "salon" is intentionally NOT
blocked - dog grooming salons are genuine VT vocabulary; only the BH-specific
hair/beauty terms above are blocked.**

## Nearby = GEOGRAPHIC (global rule)
3 hand-authored, web-verified, geographically-close towns, all on VT_towns.csv.
`require_nearby()` raises on missing/<3/off-CSV - no rank/auto fallback.
London → Croydon/Bromley/Ilford. Birmingham → Solihull/West Bromwich/Walsall.
Leeds → Bradford/Pudsey/Dewsbury.

## Low-variation + HEADROOM architecture (built in from the start)
Generic shared paragraphs live in POOLS, not per-town `s1loc`:
- **OWNER_POOL** (6) - "small practices/sole traders/no procurement, order direct".
- **PRESENT_POOL** (6, town-templated) - the **two-environments** signature para
  (clinical scrubs/tunics + outdoor fleeces/waterproofs/footwear).
- **NARROW_POOL** (6, town-templated) - narrow repeat-purchase range, logo on file.
- **KIT_POOL** (6) - the scrubs/tunics/polos/fleeces/waterproofs/footwear kit line.
`s1_paras()` = [local1, local2, OWNER, PRESENT, NARROW+KIT]. Each town's `s1loc`
holds only its **2 genuinely-local paragraphs** (the local vet/animal-care scene).
**Headroom** (baked in, learned from BH): product cards are pooled **3 variants
each** via `build_grid` (GRID_ORDER + per-card salts g0..g7); **FAQ, WHY,
PRESENT, NARROW pools are 6 variants**. Link-bearing pools (CON_P3=1 .com,
ACC_P4=2 .com, SELF=1, SORTED=1) left at their counts to protect the 14-link
total. Result: worst pair ~31% (best of the Low-variation set).

## Variant selector — md5 (NOT crc32)
`pick()` uses `hashlib.md5(...).digest()[:4]` % n. **Never revert to zlib.crc32**
- crc32 low bits correlate, collapsing same-length town names onto identical pool
vectors at scale (proven: 56 identical-vector pairs across 505 under crc32, 0
under md5).

## Uniqueness
Floors: overall ≥77%, worst pair ≤52%. **Pair cap is the binding near-duplicate
guard** and passes comfortably (~31%). Overall ~71% at small N, climbs with town
count. Hard checks (verify_vt) are the binding gate; do not chase 77 at small N.

## Research mandate
Every town web-researched for its local vet/animal-care scene (practices and
groups, kennels/catteries, rescues, groomers, equine/farm on the rural edge) even
though variation is Low - name something real. London flagship is the
general-knowledge exception. Birmingham: 115+ West Midlands practices, mostly
companion-animal independents (Broad Lane Vets) and groups, Birmingham Dogs Home's
own clinic/kennels/grooming, equine/farm on the green-belt fringe toward Sutton
Coldfield/Solihull. Leeds: Leeds Colton (best in West Yorkshire), Yorkshire Vets
(Armley/Horsforth/Morley), Vets4Pets (Kirkstall/Colton), Dogs Trust Leeds
(Harehills, 64 kennels + vet suite), equine toward Wetherby/Askham Bryan.

## Files
vt-london.html (flagship/base) · vt_build.py · verify_vt.py · score_vt.py ·
diag_vt.py · VT_towns.csv (505) · SPEC.md · CLAUDE.md. Build:
`python3 vt_build.py <slug...>` → /mnt/user-data/outputs/. Never rebuild the
flagship; only ADD pages.
