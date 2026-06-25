# TC Series — Telecoms & Network Installation Workwear (SPEC)

**Series #33 in the CW Hybrid matrix.** One HTML page per UK town for telecoms
and network installation workwear, built by `tc_build.py` from the hand-authored
London flagship `tc-london.html`. Full 505-town run (matrix says 200; overridden
to the full CSV like every series).

## Posture
- **Primary audience: Both. Page tone: Hybrid (DC-style).** EQUAL weight to two
  buyers: large installation contractors with **fleets** of engineers (procurement
  / **trade account**, managed reordering, held kit list, onboarding) AND small
  **subcontractors / sole-trader installers** (**direct online, no account**).
  Never tilt the page to one side — the identity and ordering blocks name both.
- **Workwear depth: Medium. Local variation: Low** (generic shared paragraphs live
  in pools — OWNER / PRESENT / NARROW — not in per-town `s1loc`, which holds only
  2 genuinely-local paragraphs).

## Who wears it
Field engineers building and maintaining fibre, broadband and mobile/5G networks:
FTTP/FTTH fibre rollout (Openreach, CityFibre, alt-nets), Virgin Media / nexfibre,
structured cabling (Cat5e/Cat6/fibre) for offices and schools, CCTV and security
networks, satellite and aerial. Work happens in vans, at street cabinets, up poles,
in joint boxes and on customer premises.

## Leads / products
Lead = **polo**, co-lead = **hi-vis**, third = **softshell**. 8 cards:
Polo Shirts and T-Shirts / Cargo Trousers and Work Trousers / Hi-Vis Vests and
Jackets / Softshell Jackets / Fleeces and Mid-Layers / Waterproofs and Outdoor
Jackets / Safety Boots and Footwear / Embroidery. Each card detail is **pooled 3
ways** and picked per-town via `build_grid()`.

## The differentiator — THREE JOBS AT ONCE
Identity block (id `#contract`): **"Branded, Hi-Vis and All-Weather: Kit for the
Field Engineer"**. The kit earns its place three ways: (1) **branded / identifiable**
— an engineer on a doorstep or at a cabinet looks like a legitimate contractor, not
a stranger; (2) **visible** — hi-vis to **EN ISO 20471** for roadside and street
works near traffic; (3) **weatherproof / practical** — softshells, fleeces,
waterproofs for all-weather outdoor work, cargo trousers for tools, safety boots
underfoot. This three-jobs message is carried by the PRESENT pool (varied per town).

## Identity / section copy
- Hero subtitle: "Branded Workwear for Telecoms and Network Engineers"
- h1: "{town} Telecoms and Network Installation Workwear"
- title: "{town} Telecoms and Network Workwear" (London 36; fallbacks in build_title)
- CTA: "Browse Telecoms and Network Workwear"
- EMB h2: "Branding for a Contractor Fleet or a Sole-Trader Installer"
- ACC h2 (Hybrid): "Trade Accounts for Fleets, Direct Online for Subcontractors"
- WHY h2: "Why Telecoms and Network Installers Choose iNeedWorkwear"
- Schema: "Telecoms and Network Installation Workwear" → /telecoms-network-installation-workwear;
  serviceType "Telecoms and network installation workwear and embroidery supply";
  audience "Telecoms contractors, network installers and field engineers".

## Palette (aesthetic only — verifier does NOT check hexes)
Network-cyan **#0891b2** (hover #0e7490) primary; slate-navy **#0f2233** dark
sections; amber **#f59e0b** pulse highlight; **signal-orange #f97316** as the
fibre/cable accent in SVGs; bright cyan #22d3ee / #67e8f9 SVG mids; bg #eef4f7,
cards #dceef3 border #b9dbe6, muted #4a5d66, hi-vis vest #f2d500. Fonts **Lora +
Source Sans 3** (the ONE thing the verifier checks).

## SVG scenes (5; town-swapped in assemble)
1. **garment row** — polo / hi-vis vest / softshell / safety boot. Pure chrome, NO town swap.
2. **embroidery hoop** (standard reskin, cyan; NOT the VT machine — that is VT-only).
   aria swap: `a London telecoms logo` → `a {town} telecoms logo`.
3. **signpost** — cyan plank LONDON + "TELECOMS KIT" / "FIELD ENGINEERS". Swap plank via
   `signpost_town()`, aria `London telecoms and network signpost`, caption `every kind of London telecoms`.
4. **telecoms-works premises** — telegraph pole + drop wires, grey-green street cabinet,
   orange fibre coil, cyan van with "YOUR COMPANY NAME". aria swap `serving network installers across London`.
5. **order-online** laptop (cyan). No town swap.

## Hard rules (enforced by verify_tc.py — 16 checks)
- Exactly **14 ineedworkwear.com hrefs + 1 ineedworkwear.co.uk/community** per page.
  Link-bearing pools: CON_P3 (1), ACC_P4 (2), SELF (1), SORTED (1); any new variant
  added to these MUST carry the same .com count.
- No JS (ld+json only). No HTML entities. No delivery-timescale claims. **No Chapter 8**
  (TC uses generic hi-vis to EN ISO 20471, not Chapter 8 — keeps separation from HM).
- Title ≤60, meta ≤160, no apostrophes in meta. Fonts Lora + Source Sans 3.
- Exactly 4 JSON-LD blocks (FAQ + Organization + Service + Breadcrumb).
- Lead trio present (polo + hi-vis + softshell). Word floor. Dead-link guard (tc- slugs on CSV).

## BLEED (cross-series separation)
Cloned from VT's bleed, then:
- **REMOVE `softshell`** — it is TC CORE (TRI_LEAD). Leaving it in would fail TC's own pages.
- **ADD VT animal/clinical sigs** TC never uses: scrubs, veterinary, tunic, vet nurse,
  kennel, cattery, equine, wellington.
- KEEP DC courier sigs (multidrop, owner-driver, courier, parcel round) blocked — TC uses
  "subcontractor / installer / engineer", never courier vocabulary.
- KEEP HM highways sigs (Chapter 8, National Highways, sector scheme) blocked.
- KEEP BH salon sigs (barber, hairdressing, beautician, clog, hoodie, spa day) + the
  inherited food/security/cleaning/waste/renewables/forestry/care/sports/retail bleed.
- TC CORE kept legal: polo, hi-vis, softshell, cargo, fleece, waterproof, safety boots,
  telecoms, network, fibre, broadband, cabling, engineer, installer (and Openreach /
  CityFibre / Virgin Media named ONLY in the London flagship local para — the
  general-knowledge flagship exception; pooled town content stays generic).

## Headroom architecture (baked in from the start)
- Product cards pooled 3 variants each via `build_grid(town)` (GRID_ORDER + g0..g7 salts).
- FAQ (7×6), WHY (4×6), PRESENT (6), NARROW (6) widened for spread.
- md5 selector (`pick`) — NEVER crc32 (low-bit correlation collides same-length towns).
- `s1_paras` = [local1, local2, OWNER (fleet-vs-subbie), PRESENT (three-jobs), NARROW+KIT].

## Uniqueness (score_tc.py / diag_tc.py — diagnostic, NOT a gate)
Floors: overall ≥77%, worst pair ≤52%. Current 3-town: overall **71.3%**, worst pair
**33.1%** (strongest series to date). Hard checks (verify) are the binding gate; pair
cap is the near-duplicate guard. Score climbs as N grows.

## Nearby (global rule)
Geographic, hand-authored, all on TC_towns.csv. London → Croydon/Bromley/Ilford;
Birmingham → Solihull/West Bromwich/Walsall; Leeds → Bradford/Pudsey/Dewsbury.
`require_nearby` raises if missing/<3/off-CSV — no fallback.
