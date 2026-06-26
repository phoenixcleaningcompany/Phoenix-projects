# EV Series — Entertainment, Events & Festivals Workwear (SPEC)

**Series #25 in the CW Hybrid matrix.** One HTML page per UK town for entertainment,
events and festivals workwear, built by `ev_build.py` from the hand-authored London
flagship `ev-london.html`. Full 505-town run (matrix says 200/100; overridden to the
full CSV like every series).

## Posture
- **Primary audience: Both. Page tone: Hybrid.** EQUAL weight to two buyers: big
  concert venues, festival operators and event production companies with large
  **seasonal** crews (procurement / **trade account**, managed reordering, festival-
  season onboarding) AND small independent event crews, promoters and entertainers
  (**direct online, no account**).
- **Workwear depth: Medium. Local variation: Low** — 2 genuinely-local `s1loc`
  paragraphs per town; generic shared paragraphs live in pools (OWNER / PRESENT /
  NARROW). **Very seasonal** is the matrix's driving flag (festival season).

## Who wears it
Front-of-house: stewards, bar, box office, hospitality. Crew: stage crew, riggers,
production, load-in/breakdown. Concert venues, festival production, theatres. Big
seasonal festival-crew intakes.

## Leads / products
Lead = **polo**, co-lead = **hi-vis**, third = **fleece**. 8 cards: Polo Shirts and
T-Shirts (FOH) / Hi-Vis Vests and Jackets (crew/stage) / Fleeces and Mid-Layers /
Waterproofs and Outdoor Jackets / Crew and Cargo Trousers (riggers, tool pockets) /
Safety Boots and Footwear (rigging — matrix flag) / Caps, Beanies and Accessories /
Embroidery. Each card detail is **pooled 3 ways** via `build_grid()`.
- **NO softshell** — deliberately omitted and kept BLOCKED in bleed to separate EV
  from TL (which leads softshell). EV uses cargo trousers + safety boots for the crew
  side instead.

## The differentiator — TWO ENVIRONMENTS: FRONT-OF-HOUSE + CREW
Identity block (id `#contract`): **"Branded for Front-of-House, Built for the Crew"**.
(1) **Front-of-house** — the team is the most visible part of any event; a branded
polo makes stewards, bar, box-office and hospitality staff identifiable to the
audience (trust, crowd management, safety), turning even a casual/seasonal hire into a
recognisable part of the team. (2) **Crew/production/rigging** — hi-vis (visibility on
a busy, dark site near vehicles/forklifts), fleeces + waterproofs (cold nights, wet
fields), cargo trousers (tools) and safety boots (rigging) for the physical, outdoor,
often-overnight get-in and breakdown. Plus a **very seasonal** festival calendar with
a big crew intake. Carried by the PRESENT pool (varied per town).

## Identity / section copy
- Hero subtitle: "Branded Workwear for Entertainment, Events and Festivals"
- h1: "{town} Entertainment, Events and Festivals Workwear"
- title: "{town} Entertainment, Events and Festivals Workwear" (London 51; fallbacks "{town} Events and Festivals Workwear" / "{town} Events Workwear")
- CTA: "Browse Entertainment, Events and Festivals Workwear"
- EMB h2: "Branding for a Venue, a Festival or an Independent Event Crew"
- ACC h2 (Hybrid): "Trade Accounts for Venues and Festivals, Direct Online for Crews"
- WHY h2: "Why Event and Festival Operators Choose iNeedWorkwear"
- Schema: "Entertainment, Events and Festivals Workwear" → /entertainment-events-festivals-workwear;
  serviceType "Entertainment, events and festivals workwear and embroidery supply";
  audience "Event production companies, venues, festivals and event crews".
- Stats: "Venue or Crew"/Both Supplied · "Front-of-House"/and Crew · "Seasonal"/Intake Handled · "In-House"/Embroidery.

## Palette (aesthetic only — verifier does NOT check hexes)
Stage-light **magenta #d6207e** (hover #b01a68) primary; near-black indigo **#15121e**
dark sections; a **multi-colour pulse** linear-gradient magenta #d6207e → cyan #22b8e0
→ amber #f5b301 (the EV signature); cyan #22b8e0 accent; subtitle/faq accent light-pink
#f5a9d3; contract/faq links cyan #7dd3fc; bg #f4eff3, cards #efe2ed border #ddc3d7,
muted #574d57, hi-vis vest #f2d500. Wooden-sign brown #b9824a/#5a3a1a only in the
festival-sign SVG. Fonts **Lora + Source Sans 3** (the ONE thing the verifier checks).
Distinct from BH (violet) — EV is hotter magenta + near-black + cyan stage-light.

## SVG scenes (5; town-swapped in assemble) — per Damien's brief
1. **garment row** — polo (magenta) / hi-vis vest (yellow) / fleece (charcoal) /
   waterproof (cyan). NO town swap.
2. **embroidery — realistic Barudan-style machine** (house standard), EV recolour:
   blue hoop, near-black garment, red threads, magenta + cyan emblem. aria swap
   `a London event logo` → `a {town} event logo`.
3. **festival sign** (signpost slot) — wooden plank board "{TOWN}" + "MUSIC FESTIVAL"
   + "LIVE EVENTS ALL SEASON" strip, multi-colour bunting, two posts, sky + grass.
   Swap the big town text via `sign_town()` (y=104), aria `London music festival
   welcome sign`, caption `every London event`.
4. **DJ on stage** (premises slot) — dark stage with truss rig + legs, hanging line-
   array speaker stacks, crossing magenta/cyan/yellow spotlight beams, a DJ silhouette
   with headphones and raised arm at the decks (turntables + mixer + laptop), monitor
   wedges, a "STAGE" front band and a crowd row with raised arms. aria swap `serving
   event and festival crews across London`, caption `serving crews across London`.
5. **order-online** laptop (magenta). No town swap.

## Hard rules (enforced by verify_ev.py — 16 checks)
- Exactly **14 ineedworkwear.com hrefs + 1 ineedworkwear.co.uk/community** per page.
  Link-bearing pools: CON_P3 (1), ACC_P4 (2), SELF (1), SORTED (1).
- No JS (ld+json only). No HTML entities. No delivery-timescale claims.
- Title ≤60, meta ≤160, no apostrophes in meta. Fonts Lora + Source Sans 3.
- Exactly 4 JSON-LD blocks (FAQ + Organization + Service + Breadcrumb).
- Lead trio present (polo + hi-vis + fleece). Word floor. Dead-link guard (ev- on CSV).

## BLEED (cross-series separation)
Cloned from TL's bleed, then:
- **ADD `softshell` back** — EV does not use it; blocking it separates EV from TL
  (which leads softshell). Confirm the flagship never says softshell.
- **ADD TL signatures EV never uses**: tourism, theme park, holiday park, activity
  centre, tour operator.
- KEEP charity/foodbank/volunteer (CH2), TC telecoms sigs, VT animal, DC courier,
  HM Chapter 8, BH salon (barber/hoodie/clog/spa), RT tabard, sports (gym/tracksuit/
  matchday) and the inherited food/security/cleaning/waste/renewables/forestry/care
  bleed all blocked.
- AVOID in copy: softshell; security signatures (SIA, door supervision, stab vest);
  TL signatures (tourism, theme park). Use stewards / front-of-house / crew, venue /
  festival / stage / rigging.
- EV CORE kept legal: polo, hi-vis, fleece, waterproof, cargo, safety boots, cap,
  beanie, embroidery, event, festival, stage, crew, rigging, venue, production,
  front-of-house, steward, concert, seasonal (named venues like the O2 Academy /
  First Direct Arena appear ONLY in town local paras — the research/flagship exception).

## Headroom architecture
- Product cards pooled 3 variants each via `build_grid(town)` (GRID_ORDER + g0..g7).
- FAQ (7×6), WHY (4×6), PRESENT (6), NARROW (6) widened for spread.
- md5 selector (`pick`) — NEVER crc32.
- `s1_paras` = [local1, local2, OWNER (big-vs-independent), PRESENT (FOH + crew two
  environments), NARROW+KIT].

## Uniqueness (score_ev.py / diag_ev.py — diagnostic, NOT a gate)
Floors: overall ≥77%, worst pair ≤52%. Current 3-town: overall **65.4%**, worst pair
**37.5%** (clears the 52% near-dup cap). Climbs as N grows. Hard checks (verify) are
the binding gate.

## Nearby (global rule)
Geographic, hand-authored, all on EV_towns.csv. London → Croydon/Bromley/Ilford;
Birmingham → Solihull/West Bromwich/Walsall; Leeds → Bradford/Pudsey/Dewsbury.
`require_nearby` raises if missing/<3/off-CSV — no fallback.
