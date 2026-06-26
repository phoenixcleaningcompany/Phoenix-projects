# TL Series — Travel, Tourism & Leisure Workwear (SPEC)

**Series #19 in the CW Hybrid matrix.** One HTML page per UK town for travel,
tourism and leisure workwear, built by `tl_build.py` from the hand-authored London
flagship `tl-london.html`. Full 505-town run (matrix says 200; overridden to the
full CSV like every series).

## Posture
- **Primary audience: Both. Page tone: Hybrid.** EQUAL weight to two buyers: large
  attractions, theme parks and holiday parks with big **seasonal** teams
  (procurement / **trade account**, managed reordering, season onboarding) AND small
  independent activity centres, attractions, museums and tour operators (**direct
  online, no account**).
- **Workwear depth: Medium. Local variation: Medium** — the 2 genuinely-local
  `s1loc` paragraphs carry real weight (research each town); generic shared paragraphs
  live in pools (OWNER / PRESENT / NARROW). **Seasonal** is the matrix's driving flag.

## Who wears it
Theme-park and holiday-park staff, activity-centre and watersports instructors,
visitor-attraction and museum staff, tour guides, leisure-site and campsite teams,
event and car-park staff. Big seasonal intakes each year.

## Leads / products
Lead = **polo**, co-lead = **fleece**, third = **softshell**. 8 cards: Polo Shirts
and T-Shirts / Fleeces and Mid-Layers / Softshell Jackets / Waterproofs and Outdoor
Jackets / Hi-Vis for Outdoor and Events / Gilets and Bodywarmers / Caps, Hats and
Accessories / Embroidery. Each card detail is **pooled 3 ways** via `build_grid()`.
- **softshell is TL CORE** (the third lead) — removed from the bleed list that CH2
  had blocked it in.
- No "tabard"/"hoodie"/"gym"/"spa" vocabulary (uses gilets, caps, "activity centre"
  and "leisure" to hold separation from RT/BH/sports).

## The differentiator — TWO JOBS: IDENTIFIABLE + ALL-WEATHER/SEASONAL
Identity block (id `#contract`): **"Identifiable, All-Weather and Ready for the
Season"**. (1) **Identifiable** — staff are the face of the visitor experience; a
branded polo/fleece makes them findable and approachable to guests at a busy park or
attraction, turning even a seasonal hire into a recognisable part of the team.
(2) **All-weather / seasonal** — outdoor work across a long season, so the kit
layers (polo → fleece → softshell → waterproof + outdoor hi-vis) and has to cope with
a big seasonal intake to onboard fast. Carried by the PRESENT pool (varied per town).

## Identity / section copy
- Hero subtitle: "Branded Workwear for Travel, Tourism and Leisure"
- h1: "{town} Travel, Tourism and Leisure Workwear"
- title: "{town} Travel, Tourism and Leisure Workwear" (London 43; fallbacks in build_title)
- CTA: "Browse Travel, Tourism and Leisure Workwear"
- EMB h2: "Branding for a Theme Park, a Holiday Park or an Independent Attraction"
- ACC h2 (Hybrid): "Trade Accounts for Large Attractions, Direct Online for Independents"
- WHY h2: "Why Tourism and Leisure Operators Choose iNeedWorkwear"
- Schema: "Travel, Tourism and Leisure Workwear" → /travel-tourism-leisure-workwear;
  serviceType "Travel, tourism and leisure workwear and embroidery supply";
  audience "Theme parks, holiday parks, activity centres, tourist attractions and tour operators".
- Stats: "Park or Independent"/Both Supplied · "Seasonal"/Intake Handled ·
  "All-Weather"/Outdoor Layers · "In-House"/Embroidery.

## Palette (aesthetic only — verifier does NOT check hexes)
Travel-azure **#1d70b8** (hover #155a92) primary; deep navy **#11243f** dark sections
(the airliner navy); amber **#f59e0b** in the pulse; sunny gold **#f5a623** accent;
sky #5eb3e8 / #93cdf0 SVG mids; bg #eef4fa, cards #dcebf7 border #b3d3ec, muted
#4a5a6a, hi-vis vest #f2d500. Tourist-sign brown #6b4a2e appears only in the
attraction-sign SVG. Fonts **Lora + Source Sans 3** (the ONE thing the verifier checks).

## SVG scenes (5; town-swapped in assemble) — per Damien's brief
1. **garment row** — polo / fleece / softshell / waterproof (gold waterproof). NO town swap.
2. **embroidery — realistic Barudan-style machine** (house standard), TL recolour:
   blue hoop, navy garment, red threads, gold-sun + azure-dot emblem. aria swap
   `a London tourism logo` → `a {town} tourism logo`.
3. **attraction sign** (signpost slot) — brown tourist-board "WELCOME TO {TOWN}" sign
   with four white attraction icons + "All attractions nearby ->". Swap the big town
   text via `sign_town()`, aria `London tourism and attractions welcome sign`, caption
   `every kind of London attraction`.
4. **aeroplane** (premises slot) — cartoon airliner in a cloudy sky (navy tail with
   wing-and-star emblem, blue cheatline, window row, swept wing + engine pod). aria
   swap `serving operators across London`, caption `serving visitors across London`.
5. **order-online** laptop (azure). No town swap.

## Hard rules (enforced by verify_tl.py — 16 checks)
- Exactly **14 ineedworkwear.com hrefs + 1 ineedworkwear.co.uk/community** per page.
  Link-bearing pools: CON_P3 (1), ACC_P4 (2), SELF (1), SORTED (1).
- No JS (ld+json only). No HTML entities. No delivery-timescale claims.
- Title ≤60, meta ≤160, no apostrophes in meta. Fonts Lora + Source Sans 3.
- Exactly 4 JSON-LD blocks (FAQ + Organization + Service + Breadcrumb).
- Lead trio present (polo + fleece + softshell). Word floor. Dead-link guard (tl- on CSV).

## BLEED (cross-series separation)
Cloned from CH2's bleed, then:
- **REMOVE `softshell`** — it is TL core (third lead). Leaving it in would fail TL's pages.
- **ADD CH2 charity sigs** TL never uses: charity, foodbank, volunteer.
- KEEP TC telecoms sigs (telecoms/fibre/broadband/Openreach/street cabinet), VT animal,
  DC courier, HM Chapter 8, BH salon (barber/hoodie/clog/spa), RT tabard, sports
  (gym/tracksuit/matchday) and the inherited food/security/cleaning/waste/renewables/
  forestry/care bleed all blocked.
- TL CORE kept legal: polo, fleece, softshell, waterproof, hi-vis, gilet, bodywarmer,
  cap, embroidery, tourism, travel, leisure, attraction, theme park, holiday park,
  activity centre, visitor, season (and named attractions like Cadbury World / Royal
  Armouries appear ONLY in town local paras — the research/flagship exception).

## Headroom architecture
- Product cards pooled 3 variants each via `build_grid(town)` (GRID_ORDER + g0..g7).
- FAQ (7×6), WHY (4×6), PRESENT (6), NARROW (6) widened for spread.
- md5 selector (`pick`) — NEVER crc32.
- `s1_paras` = [local1, local2, OWNER (big-vs-independent), PRESENT (identifiable +
  all-weather/seasonal), NARROW+KIT].

## Uniqueness (score_tl.py / diag_tl.py — diagnostic, NOT a gate)
Floors: overall ≥77%, worst pair ≤52%. Current 3-town: overall **67.1%**, worst pair
**35.2%** (clears the 52% near-dup cap). Medium variation + richer local s1loc give a
healthy spread; it climbs as N grows. Hard checks (verify) are the binding gate.

## Nearby (global rule)
Geographic, hand-authored, all on TL_towns.csv. London → Croydon/Bromley/Ilford;
Birmingham → Solihull/West Bromwich/Walsall; Leeds → Bradford/Pudsey/Dewsbury.
`require_nearby` raises if missing/<3/off-CSV — no fallback.
