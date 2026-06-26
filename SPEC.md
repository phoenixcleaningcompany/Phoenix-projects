# CH2 Series — Charity & Volunteer Workwear (SPEC)

**Series #26 in the CW Hybrid matrix.** One HTML page per UK town for charity,
non-profit and volunteer workwear, built by `ch2_build.py` from the hand-authored
London flagship `ch2-london.html`. Full 505-town run (matrix says 200; overridden
to the full CSV like every series).

**Prefix `ch2-`** — deliberately distinct from the existing care-home `CH` series
(which lives at `ineedworkwear.co.uk/care-home-{slug}`). CH2 canonicals are
`https://www.ineedworkwear.uk/ch2-{slug}.html`.

## Posture
- **Primary audience: Both. Page tone: Hybrid.** EQUAL weight to two buyers:
  national charities with **shops and branches** (procurement / **trade account**,
  managed reordering, held kit list, branch roll-out) AND small local **volunteer
  groups / foodbanks** (**direct online, no account, NO MINIMUM**). Never tilt the
  page to one side.
- **Workwear depth: Low. Local variation: Low** (generic shared paragraphs live in
  pools — OWNER / PRESENT / NARROW — not in per-town `s1loc`, which holds only 2
  genuinely-local paragraphs).
- **Budget-conscious is the matrix's driving flag.** Every page states the trade-off:
  every pound spent on kit is a pound not spent on the cause, so the kit is
  affordable branded basics with no minimum. "No Minimum" / "Fair Prices" stats.

## Who wears it
Charity-shop volunteers, foodbank and pantry teams, community-group and mutual-aid
volunteers, fundraisers, event marshals, litter-pickers and conservation volunteers,
soup kitchens and community-meal crews — from national charities down to one-room
volunteer-run projects.

## Leads / products
Lead = **polo**, co-lead = **hi-vis**, third = **fleece**. 8 cards (deliberately
narrow): Polo Shirts and T-Shirts / Hi-Vis Vests and Waistcoats / Fleeces and
Mid-Layers / Waterproofs and Outdoor Jackets / Sweatshirts and Zip Tops / Aprons for
Shops and Kitchens / Caps, Beanies and Accessories / Embroidery. Each card detail is
**pooled 3 ways** and picked per-town via `build_grid()`.
- **No "tabard"** (RT signature — used "Aprons" instead) and **no "hoodie"** (BH
  signature — used "Sweatshirts and Zip Tops") to hold cross-series separation.

## The differentiator — RECOGNISABLE, TRUSTED, AFFORDABLE
Identity block (id `#contract`): **"Recognisable, Trusted and Affordable: Kit for
Volunteers"**. Charity workwear really has one job, done on a tight budget: make the
volunteer instantly **recognisable and official** to the public, donors and the
people they help (trust + safeguarding at a foodbank, collection, shop or event),
and do it **affordably** because every pound on kit is a pound off the cause — a
narrow range of branded basics, no minimum, not an expensive uniform programme.
Branding/embroidery is the whole point. This message is carried by the PRESENT pool.

## Identity / section copy
- Hero subtitle: "Branded Workwear for Charities, Non-Profits and Volunteers"
- h1 + title: "{town} Charity and Volunteer Workwear" (London 37)
- CTA: "Browse Charity and Volunteer Workwear"
- EMB h2: "Branding for a National Charity or a Local Volunteer Group"
- ACC h2 (Hybrid): "Trade Accounts for Charities, Direct Online for Volunteer Groups"
- WHY h2: "Why Charities and Volunteer Groups Choose iNeedWorkwear"
- Schema: "Charity and Volunteer Workwear" → /charity-volunteer-workwear;
  serviceType "Charity and volunteer workwear and embroidery supply";
  audience "Charities, non-profits, foodbanks and volunteer groups".
- Stats: "Charity or Group"/Both Supplied · "No Minimum"/Order Any Quantity ·
  "Fair Prices"/Budget-Friendly · "In-House"/Embroidery.

## Palette (aesthetic only — verifier does NOT check hexes)
Warm community **emerald #059669** (hover #047857) primary; charcoal-teal **#0f2922**
dark sections; amber **#f59e0b** in the pulse; **coral #fb7185** as the warm human
accent (hearts, awnings, logo patches); bright emerald #34d399 / #6ee7b7 SVG mids;
bg #eef5f1, cards #dcefe7 border #b3ddca, muted #4a5d54, hi-vis vest #f2d500. Fonts
**Lora + Source Sans 3** (the ONE thing the verifier checks). Chosen vivid emerald +
coral to read warm/community and to separate from the prior darker/forest greens.

## SVG scenes (5; town-swapped in assemble)
1. **garment row** — polo / hi-vis vest / fleece / apron (apron has a coral heart
   pocket). Pure chrome, NO town swap.
2. **embroidery — REALISTIC BARUDAN-STYLE MULTI-NEEDLE MACHINE** (Damien-specified,
   matching uploaded photo IMG_9671): white head, top rail with red thread cones,
   red threads to the needle bank, blue hoop (#229ed4) holding a navy garment, a
   part-stitched emblem in CH2 colours (coral heart + emerald stitch dots), blue
   pantograph. aria swap: `a London charity logo` → `a {town} charity logo`.
   NOTE: this extends the realistic machine beyond VT; CH2 uses it. Other series
   (incl. TC) currently keep the simple hoop unless told otherwise.
3. **signpost** — emerald plank LONDON + "VOLUNTEER KIT" / "CHARITIES". Swap plank via
   `signpost_town()`, aria `London charity and volunteer signpost`, caption
   `every kind of London volunteer`.
4. **charity-shop premises** — emerald fascia "YOUR CHARITY NAME", coral scalloped
   awning, heart in the window, donation box with coin slot. aria swap
   `serving volunteers across London`.
5. **order-online** laptop (emerald). No town swap.

## Hard rules (enforced by verify_ch2.py — 16 checks)
- Exactly **14 ineedworkwear.com hrefs + 1 ineedworkwear.co.uk/community** per page.
  Link-bearing pools: CON_P3 (1), ACC_P4 (2), SELF (1), SORTED (1); any new variant
  added to these MUST carry the same .com count.
- No JS (ld+json only). No HTML entities. No delivery-timescale claims.
- Title ≤60, meta ≤160, no apostrophes in meta. Fonts Lora + Source Sans 3.
- Exactly 4 JSON-LD blocks (FAQ + Organization + Service + Breadcrumb).
- Lead trio present (polo + hi-vis + fleece). Word floor. Dead-link guard (ch2- on CSV).

## BLEED (cross-series separation)
Cloned from TC's bleed, then:
- **ADD `softshell` back** — it is TC core (TC's third lead) and CH2 never uses it,
  so blocking it holds TC/CH2 separation. Also added TC telecoms sigs CH2 never uses:
  telecoms, fibre, broadband, Openreach, street cabinet.
- KEEP `tabard` (RT) and `hoodie` (BH) blocked — CH2 deliberately uses aprons and
  "sweatshirts and zip tops" instead.
- KEEP DC courier, HM Chapter 8 / National Highways, BH salon, VT animal/clinical
  (scrubs/veterinary/tunic/vet nurse/kennel/cattery/equine/wellington) and the
  inherited food/security/cleaning/waste/renewables/forestry/care/sports/retail bleed.
- CH2 CORE kept legal: polo, hi-vis, fleece, waterproof, sweatshirt, apron, cap,
  embroidery, charity, volunteer, foodbank, community, safeguarding (and Trussell
  Trust / FareShare / Felix Project / City Harvest named ONLY in town local paras —
  the general-knowledge flagship/research exception; pooled content stays generic).

## Headroom architecture (baked in from the start)
- Product cards pooled 3 variants each via `build_grid(town)` (GRID_ORDER + g0..g7).
- FAQ (7×6), WHY (4×6), PRESENT (6), NARROW (6) widened for spread.
- md5 selector (`pick`) — NEVER crc32.
- `s1_paras` = [local1, local2, OWNER (national-vs-local), PRESENT (recognisable-
  trusted-affordable), NARROW+KIT].

## Uniqueness (score_ch2.py / diag_ch2.py — diagnostic, NOT a gate)
Floors: overall ≥77%, worst pair ≤52%. Current 3-town: overall ~65%, worst pair
**39.9%** (clears the 52% near-dup cap). The narrow, repetitive charity vocabulary
(charity/volunteer/foodbank) keeps overall a little lower than wider series at N=3;
it climbs as N grows. Hard checks (verify) are the binding gate; the pair cap is the
near-dup guard.

## Nearby (global rule)
Geographic, hand-authored, all on CH2_towns.csv. London → Croydon/Bromley/Ilford;
Birmingham → Solihull/West Bromwich/Walsall; Leeds → Bradford/Pudsey/Dewsbury.
`require_nearby` raises if missing/<3/off-CSV — no fallback.
