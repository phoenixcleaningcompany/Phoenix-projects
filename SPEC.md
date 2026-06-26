# CP Series — Corporate & Professional Services Workwear (SPEC)

**Series #18 in the CW Hybrid matrix.** One HTML page per UK town for corporate and
professional services workwear, built by `cp_build.py` from the hand-authored London
flagship `cp-london.html`. Full 505-town run (matrix says 200/100 max; overridden to
the full CSV like every series).

## Posture — CONCIERGE / PROCUREMENT (not Hybrid)
- **Primary audience: Procurement. Page tone: Concierge.** This is NOT the big-vs-small
  hybrid split. The buyer is a procurement, office, HR or brand manager at a bank, law
  firm, accountancy, consultancy, insurer or technology company. The service is a
  **managed account**: a single point of contact, a held brand pack and kit list,
  managed reorders and multi-office rollouts, agreed pricing.
- **Workwear depth: Low. Local variation: Low.** 2 genuinely-local `s1loc` paragraphs
  per town; everything generic lives in pools (OWNER / PRESENT / NARROW).
- **The key insight (matrix note):** corporate workwear here is a **brand exercise, not
  a daily uniform** — a narrow range of branded kit for *away days, conferences,
  exhibitions, site/client visits, sponsored/fundraising events and new-starter welcome
  packs*, when staff step out of the suit.

## The differentiator — ON-BRAND + ACCOUNT-MANAGED
Identity block (id `#contract`): **"On-Brand, Account-Managed Corporate Kit"**.
(1) **On-brand** — corporate kit represents the firm in public, so it must match the
brand exactly: the right logo, the right colours, embroidered to the firm's guidelines,
reading as the brand and not as generic workwear; the brand pack is held on file.
(2) **Account-managed (concierge)** — because the kit is occasional rather than daily,
the value is the service: a single point of contact, a held kit list and brand pack,
agreed pricing and managed reorders, so procurement places one order and every office,
team and event comes back the same. Carried by the PRESENT and NARROW pools.

## Leads / products
Lead = **polo**, co-lead = **softshell**, third = **fleece** (softshell is CORE again,
removed from bleed). 8 cards: Polo Shirts and T-Shirts / Branded Corporate Shirts /
Softshell Jackets / Fleeces and Mid-Layers / Quarter-Zips and Sweatshirts / Gilets and
Bodywarmers / Caps and Accessories / Logo and Brand-Mark Embroidery. **No hi-vis,
safety boots or cargo** — deliberately narrow and corporate. Each card detail is pooled
3 ways via `build_grid()`.

## Identity / section copy
- Hero subtitle: "Branded Workwear for Corporate and Professional Services"
- h1 / title: "{town} Corporate and Professional Services Workwear" (London 51;
  fallbacks "{town} Corporate and Professional Workwear" / "{town} Corporate Workwear")
- CTA: "Browse Corporate and Professional Services Workwear"
- EMB h2: "Branding for a Bank, a Law Firm or a Tech Company"
- CON h3 (#contract): "On-Brand, Account-Managed Corporate Kit"
- ACC h2 (#accounts, concierge): "A Managed Account for Consistent, On-Brand Corporate Kit"
  (jump-link label "The Managed Account")
- WHY h2: "Why Corporate and Professional Firms Choose iNeedWorkwear"
- Schema: "Corporate and Professional Services Workwear" → /corporate-professional-services-workwear;
  serviceType "Corporate and professional services workwear and embroidery supply";
  audience "Banks, law firms, accountancies, consultancies and technology companies".
- Stats: "On-Brand"/To Your Guidelines · "Account-Managed"/One Point of Contact ·
  "Banks to Tech"/Every Sector · "In-House"/Embroidery.

## Palette (aesthetic only — verifier does NOT check hexes)
Premium **navy #1e2d50** (hover #15203c) primary; deep navy **#141d33** dark sections;
a navy→gold pulse linear-gradient navy #1e2d50 → gold #b08a3e → navy; **gold accent
#b08a3e / #c4a14e** (the CP signature — sets it apart from DC indigo and SE steel-blue);
subtitle/faq/footer headings gold #c4a14e; contract/faq dark links #d8c486; bg #f4f6fa,
cards #eef1f6 border #d4dae6, muted #4a5568. NO hi-vis colours. Fonts **Lora + Source
Sans 3** (the ONE thing the verifier checks).

## SVG scenes (5; town-swapped in assemble) — per Damien's brief
1. **garment row** — polo (navy) / branded shirt (white collared) / softshell (slate
   #41506e) / fleece (navy), gold logo patches. NO town swap.
2. **embroidery — realistic Barudan-style machine** (house standard), CP recolour:
   blue hoop, navy garment, red threads, gold #c4a14e + navy emblem. aria swap
   `a London corporate logo` → `a {town} corporate logo`.
3. **corporate monument sign** (signpost slot) — a sleek, professional freestanding
   sign: navy panel with a gold top accent bar, a gold growth-bars logo mark **centred
   on top**, the **town name centred** below it, a thin gold rule, then "PROFESSIONAL
   SERVICES" centred underneath, on a stone plinth flanked by faint office towers.
   IMPORTANT: this is a **centred stack** (logo / town / rule / strapline) precisely so
   the strapline never clashes with the logo and any town-name length stays clean.
   `sign_town()` swaps the centred town text at **x=230, y=138** (size by length:
   26/22/18/15/13, textLength cap >14 chars). aria `London corporate and professional
   services sign`, caption `every London office and team`.
4. **office / bank building** (premises slot) — a modern corporate HQ: a navy-framed
   glass curtain-wall tower (window grid), gold parapet and entrance bands, a glazed
   lobby with columns, a secondary glass block beside it, corporate trees and a clean
   plaza. aria swap `serving professional services firms across London`, caption
   `professional firms across London`.
5. **order-online** laptop (navy/gold). No town swap.

## Hard rules (enforced by verify_cp.py — 16 checks)
- Exactly **14 ineedworkwear.com hrefs + 1 ineedworkwear.co.uk/community** per page.
  Link-bearing pools: CON_P3 (1), ACC_P4 (2), SELF (1), SORTED (1).
- No JS (ld+json only). No HTML entities. No delivery-timescale claims.
- Title ≤60, meta ≤160, no apostrophes in meta. Fonts Lora + Source Sans 3.
- Exactly 4 JSON-LD blocks (FAQ + Organization + Service + Breadcrumb).
- Lead trio present (polo + softshell + fleece). Word floor. Dead-link guard (cp- on CSV).

## BLEED (cross-series separation)
Cloned from EV's bleed, then:
- **REMOVE `softshell`** — it is CP core again (EV had blocked it). Leaving it in would
  fail every CP page.
- **ADD EV signatures CP never uses**: festival, stage, crew, rigging, front-of-house,
  steward, concert. ("event" is deliberately NOT blocked — CP uses away days / events.)
- KEEP TL signatures (tourism, theme park, holiday park, activity centre, tour
  operator), charity/foodbank/volunteer (CP uses *fundraising/sponsored*, never the
  word "charity"), TC telecoms, VT animal, DC courier, HM Chapter 8, BH salon
  (barber/hoodie/clog/spa), RT tabard, sports (gym/tracksuit/matchday) and the inherited
  food/security/cleaning/etc bleed all blocked.
- **AVOID in copy:** "charity" (use fundraising/sponsored/community), festival/stage/
  crew/front-of-house/concert, and **"wellington"** (Leeds: Wellington Place/Street trips
  the *wellington*-boot bleed term — use "the city centre and King Street" instead).
- CP CORE kept legal: polo, shirt, softshell, fleece, quarter-zip, sweatshirt, gilet,
  bodywarmer, cap, embroidery, corporate, professional, bank, law firm, accountancy,
  consultancy, tech, away day, conference, exhibition, site visit, brand, account-managed.
  Named firms/banks (HSBC, Big Four, DLA Piper, etc) appear ONLY in town local paras
  (the research/flagship exception).

## Headroom architecture
- Product cards pooled 3 variants each via `build_grid(town)` (GRID_ORDER + g0..g7).
- FAQ (7×6), WHY (4×6), PRESENT (6), NARROW (6) widened for spread.
- md5 selector (`pick`) — NEVER crc32.
- `s1_paras` = [local1, local2, OWNER (brand-exercise-not-uniform), PRESENT (on-brand +
  occasions), NARROW+KIT (narrow range + held brand pack + managed reorders)].

## Uniqueness (score_cp.py / diag_cp.py — diagnostic, NOT a gate)
Floors: overall ≥77%, worst pair ≤52%. Current 3-town: overall **62.4%**, worst pair
**42.1%** (clears the 52% near-dup cap; tighter than higher-variation series because CP
is Low variation by design). Climbs as N grows. Hard checks (verify) are the gate.

## Nearby (global rule)
Geographic, hand-authored, all on CP_towns.csv. London → Croydon/Bromley/Ilford;
Birmingham → Solihull/West Bromwich/Walsall; Leeds → Bradford/Pudsey/Dewsbury.
`require_nearby` raises if missing/<3/off-CSV — no fallback.
