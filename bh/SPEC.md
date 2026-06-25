# BH Series — Beauty, Hair & Spa Workwear (SPEC)

**Series #16 in the CW Hybrid matrix.** One HTML page per UK town for hair,
beauty and spa businesses. Prefix `bh-`. Canonical/og to
`https://www.ineedworkwear.uk/bh-<slug>.html`.

## Audience & posture — SELF-CHECKOUT / Template B
Audience = **Small Biz**, tone = **Self-checkout**. The ordering section is
**direct-online-led, no account** (the route most sole traders and small salons
use): browse, pick the few pieces you need, add sizes, send the logo once, check
out. A **trade account** is the secondary option for a larger salon, spa or
group. Workwear depth **Low**, local variation **Low**. (Matrix note: dominated
by sole traders and small salons; narrow range; HD already covers the individual-
worker audience, so BH addresses the **salon/barber/spa business**, not the
worker.)

## Lead products (verifier-enforced)
LEAD = **tunic**, CO_LEAD = **polo**, TRI_LEAD = **apron**. Deliberately narrow
8-card grid: Beauty and Spa Tunics / Salon and Barber Polo Shirts / Hairdressing
and Barber Aprons / Clogs and Salon Footwear / Salon Trousers and Leggings /
Sweatshirts and Hoodies / Headbands, Caps and Accessories / Embroidery, Names
and ID.

## Identity block — the differentiator
**"Look the Part: A Branded Uniform for Salons, Barbers and Spas"** (id
`#contract`) plus the branding section **"Branding for a One-Chair Barber or a
Small Salon Team"**. The thread: a salon uniform does **two jobs** — presentation
(beauty/hair/spa is personal and close-up; a clean branded tunic or polo is
reassurance made visible and turns a sole trader into a recognisable business)
and practical (aprons take colour/water/product and wipe clean; tunics/polos wash
well; clogs keep a stylist or therapist comfortable through long days on their
feet). A soft, presentation-led angle, NOT PPE. **No nation handling.**

## Palette / design
Purple/violet `#7e22ce` (hover `#6b21a8`) + deep violet-charcoal `#1d1430` +
amber `#f59e0b` highlight; SVG accent blush/rose `#ec4899` + cream. Distinct from
every prior series (teal/blue/slate/forest-green/indigo/burgundy). Page bg
`#f5eefb`, cards `#efe3f7`/`#ddc7ec`, muted `#6a5570`, stat values `#c026d3`,
links `#7e22ce`. Fonts Lora + Source Sans 3. 2 radial + 1 linear gradient. 5 SVG
scenes: salon garment row (tunic / polo / apron / clog), logo embroidery, town
signpost (SALON KIT / CHAIR AND TREATMENT ROOM), **salon-front premises scene**
(fascia "YOUR SALON NAME", window with styling chair + mirror, barber pole),
order-online laptop.

## Hard rules (verify_bh.py, 16 checks)
1. Exactly **14 .com hrefs + 1 co.uk/community**. 2. No JS (ld+json only).
3. No HTML entities. 4. No delivery-timescale claims ("standard lead times" OK).
5. Title ≤60, meta ≤160, no apostrophes in meta. 6. Fonts Lora + Source Sans 3.
7. Organization+Service schema only. 8. **4 JSON-LD blocks** — check 16.
9. Lead trio present (tunic/polo/apron). 10. Word count ≥ floor. 11. Dead-link
guard: every `bh-<slug>.html` link must be a CSV town (check 15).
12. **BLEED ban**: food (BRCGS/hairnet/hygiene coat), security (SIA/body armour/
epaulette), cleaning (COSHH/colour-coded cleaning), waste (RCV/refuse collection/
bin lorry/HWRC), renewables (solar panel/EV charging/heat pump/MCS), highways
(Chapter 8/National Highways/sector scheme), forestry (chainsaw/EN ISO 11393/
tree surgery/arborist/LANTRA/NPTC), care/edu (Ofsted/CQC), sports (athleisure/
club crest/matchday/tracksuit), **RT retail (tabard/convenience store/garden
centre/forecourt/farm shop/stockroom)** and **DC courier (softshell/multidrop/
owner-driver/courier)**.
**NOTE: "tunic", "polo", "apron", "clog", "salon", "barber", "beautician",
"spa", "hairdressing", "hoodie" are LEGAL for BH** (its core). **"tunic" was
REMOVED from the inherited cleaning bleed (BH core); "hoodie" was REMOVED
(salons sell branded hoodies; SF separation rests on athleisure/club crest/
matchday/tracksuit).**

## Nearby = GEOGRAPHIC (global rule)
3 hand-authored, web-verified, geographically-close towns, all on BH_towns.csv.
`require_nearby()` raises on missing/<3/off-CSV — no rank/auto fallback.
London → Croydon/Bromley/Ilford. Birmingham → Solihull/West Bromwich/Walsall.
Leeds → Bradford/Pudsey/Dewsbury.

## Low-variation handling (important for this series)
Because local variation is Low and the range is narrow, the generic shared
paragraphs every town repeats live in **POOLS, not in per-town `s1loc`**:
- **OWNER_POOL** — the "sole traders / no procurement department / order direct"
  self-checkout para (6 variants).
- **PRESENT_POOL** — the "uniform does two jobs: presentation + practical" para
  (4 variants, town-templated).
- **NARROW_POOL** — the "small repeat-purchase trade, narrow range, logo on file"
  para (4 variants, town-templated).
- **KIT_POOL** — the tunics/polos/aprons/clogs kit line (6 variants).
Each town's `s1loc` holds only its **2 genuinely-local paragraphs** (local salon/
barber/spa scene — high-street density, named districts, the independent mix).
`s1_paras()` assembles: [local1, local2, OWNER, PRESENT, NARROW+KIT]. Do NOT push
the generic present/narrow/sole-trader prose back into `s1loc`.

## Variant selector — md5 (NOT crc32)
`pick()` uses `hashlib.md5(...).digest()[:4]` % n. **Never revert to
zlib.crc32** — crc32's low bits correlate with the input, so same-length town
names collided on the same pool variant across all pools at once (proven: 56
identical-vector town-pairs across 505 under crc32, 0 under md5).

## Uniqueness
Floors: overall ≥77%, worst pair ≤52%. **Pair cap is the binding near-duplicate
guard** and passes comfortably (~37%, in line with RT/DC). Headroom was added on
top of the base build: the **product-card detail text is pooled (3 variants per
card, picked per-town via `build_grid`)** instead of fixed, and **FAQ, WHY,
PRESENT and NARROW pools were widened 4 -> 6 variants**. This took the worst pair
44.8% -> 36.6% and overall 61% -> 67%. Link-bearing pools (CON_P3, ACC_P4, SELF,
SORTED) were deliberately left at their counts to protect the 14-link total. Hard
checks (verify_bh) are the binding gate; do not chase 77 at small N. If even more
headroom is wanted at scale, widen CON/ACC/EMB/ORD to 6 as well (all link-free
except CON_P3/ACC_P4 - keep those fixed).

## Research mandate
Every town web-researched for its local salon/barber/spa scene (high-street
density, named districts, the independent/sole-trader mix) even though variation
is Low — name something real. London flagship is the general-knowledge exception.
Birmingham: one of the densest beauty/grooming markets outside London,
independent clusters in Kings Heath/Moseley/Harborne/Jewellery Quarter, Digbeth
creative barbers, Ladypool Road Asian beauty/nail trade. Leeds: city-centre
salons/barbers/day spas around Briggate/Corn Exchange/Victoria Gate, big suburban
clusters on Otley Road/North Lane (Headingley/Hyde Park), Chapel Allerton,
Roundhay, Horsforth.

## Files
bh-london.html (flagship/base) · bh_build.py · verify_bh.py · score_bh.py ·
diag_bh.py · BH_towns.csv (505) · SPEC.md · CLAUDE.md. Build:
`python3 bh_build.py <slug...>` → /mnt/user-data/outputs/. Never rebuild the
flagship; only ADD pages.
