# RT Series — Supermarkets & Retail Workwear (SPEC)

**Series #14 in the CW Hybrid matrix.** One HTML page per UK town for retail
businesses. Prefix `rt-`. Canonical/og to
`https://www.ineedworkwear.uk/rt-<slug>.html`.

## Audience & posture — CONCIERGE / Template A, TARGETING INDEPENDENTS
Audience = **Procurement**, tone = **Concierge**. The ordering section is
**managed-trade-account-led** (one point of contact, agreed pricing, uniform
list held on file, reorders for new starters/seasonal staff, multi-store
consistency), with **direct online** as the secondary route for a single small
shop. Workwear depth **Medium**, local variation **Low**.

**CRITICAL targeting (matrix note):** the big chains procure uniforms centrally
through national tenders, so this series does NOT target them. It targets
**independent retailers, convenience stores, forecourts, garden centres, farm
shops and small multi-store retail groups** — the businesses that want a smart,
branded uniform without a corporate procurement department. The "independents,
not chains" message is carried by OWNER_POOL and the FAQ.

## Lead products (verifier-enforced)
LEAD = **tabard**, CO_LEAD = **polo**, TRI_LEAD = **fleece**. 8-card grid:
Embroidered Polo Shirts / Tabards and Aprons / Fleeces and Sweatshirts / Safety
Shoes and Footwear / Hi-Vis for Warehouse and Yard / Cargo and Stockroom
Trousers / Caps, Beanies and Accessories / Embroidery, Names and ID.

## Identity block — the differentiator
**"Your Staff Are Your Shopfront: A Consistent Retail Uniform"** (id `#contract`)
plus the branding section **"Branding That Builds Trust on the Shop Floor"**. The
thread: in retail the **staff are the brand** — a customer judges a shop in
seconds, so a clean, branded uniform signals a well-run, trustworthy business.
**Front of house** = embroidered polos, tabards and fleeces carrying the shop
name; **back of house** = safety shoes, hi-vis (warehouse/yard/delivery) and
cargo/stockroom trousers. One supplier kits both and keeps it consistent as staff
turn over. This is a brand-and-trust / staff-uniform angle, NOT a heavy-PPE one.
**No nation handling.**

## Palette / design
Burgundy/wine `#9d174d` (hover `#831843`) + charcoal `#0f172a` + amber `#f59e0b`
highlight; SVG hi-vis `#f2d500`. Distinct from every prior series (teal/blue/
slate/forest-green/indigo). Page bg `#f5eef1`, cards `#f3e3ea`/`#e6c7d3`, muted
`#7a5563`, links `#9d174d`. Fonts Lora + Source Sans 3. 2 radial + 1 linear
gradient. 5 SVG scenes: retail garment row (polo / tabard / fleece / safety
shoe), logo embroidery, town signpost (RETAIL KIT / TILL AND STOCKROOM),
**shopfront premises scene** (striped awning, "YOUR SHOP NAME" fascia, window,
door, OPEN sign), order-online laptop.

## Hard rules (verify_rt.py, 16 checks)
1. Exactly **14 .com hrefs + 1 co.uk/community**. 2. No JS (ld+json only).
3. No HTML entities. 4. No delivery-timescale claims ("standard lead times" OK).
5. Title ≤60, meta ≤160, no apostrophes in meta. 6. Fonts Lora + Source Sans 3.
7. Organization+Service schema only. 8. **4 JSON-LD blocks** — check 16.
9. Lead trio present (tabard/polo/fleece). 10. Word count ≥ floor. 11.
Dead-link guard: every `rt-<slug>.html` link must be a CSV town (check 15).
12. **BLEED ban**: food (BRCGS/hairnet/hygiene coat), security (SIA/body armour/
epaulette), cleaning (COSHH/colour-coded cleaning/tunic), waste (RCV/refuse
collection/bin lorry/HWRC), renewables (solar panel/EV charging/heat pump/MCS),
highways (Chapter 8/National Highways/sector scheme), forestry (chainsaw/EN ISO
11393/tree surgery/arborist/LANTRA/NPTC), courier (multidrop/owner-driver/
softshell — DC's signature), care/edu (Ofsted/CQC), sports.
**NOTE: "tabard", "polo", "fleece", "safety shoes", "hi-vis", "cargo",
"stockroom", "convenience store", "garden centre", "forecourt", "farm shop",
"shop floor", "retail" are LEGAL for RT** (its core). **"tabard" was REMOVED from
the inherited cleaning bleed line — it is RT core.** ("tunic" stays blocked — RT
uses tabards, not tunics.)

## Nearby = GEOGRAPHIC (global rule)
3 hand-authored, web-verified, geographically-close towns, all on RT_towns.csv.
`require_nearby()` raises on missing/<3/off-CSV — no rank/auto fallback.
London → Croydon/Bromley/Ilford. Birmingham → Solihull/West Bromwich/Walsall.
Leeds → Bradford/Pudsey/Dewsbury.

## Low-variation handling (important for this series)
Because local variation is Low, the generic shared paragraphs every town repeats
live in **POOLS, not in per-town `s1loc`**:
- **SHOPFRONT_POOL** — the "uniform is the shopfront / front vs back of house"
  para (4 variants, town-templated).
- **CONSIST_POOL** — the "consistent as the team turns over / managed account"
  para (4 variants, town-templated).
- **OWNER_POOL** — the "big chains tender centrally, this is for independents"
  targeting para (6 variants).
- **KIT_POOL** — the front/back-of-house kit summary line (6 variants).
Each town's `s1loc` holds only its **2 genuinely-local paragraphs** (local retail
geography — high streets, arcades, markets, convenience density, garden centres).
`s1_paras()` assembles: [local1, local2, OWNER, SHOPFRONT, CONSIST+KIT]. Do NOT
push the generic shopfront/consistency/chains prose back into `s1loc`.

## Uniqueness
Floors: overall ≥77%, worst pair ≤52%. **Pair cap is the binding near-duplicate
guard** and passes (~38%). Overall ~62% at small N (heavy shared retail scaffold),
climbs with town count. Hard checks (verify_rt) are the binding gate. Code may
tune the gate as it scales; do not chase 77 at small N.

## Research mandate
Every town web-researched for its local independent-retail scene (high streets,
shopping parades, arcades/markets, convenience density, garden centres, farm
shops) even though variation is Low — name something real. London flagship is the
general-knowledge exception. Birmingham: chains in the Bullring but a deep
independent scene in the suburbs (Kings Heath/Moseley/Stirchley/Harborne/
Bournville high streets, Jewellery Quarter arcades, convenience stores and
independent grocers, farmers' markets, Rag/Redbrick markets). Leeds: chains in
Trinity/Victoria but Victorian arcades + Kirkgate Market (Europe's largest
covered, birthplace of M&S) + Corn Exchange independents, suburban high streets
(Chapel Allerton/Headingley/Meanwood/Cross Gates/Farsley/Bramley), convenience
and garden/plant shops.

## Files
rt-london.html (flagship/base) · rt_build.py · verify_rt.py · score_rt.py ·
diag_rt.py · RT_towns.csv (505) · SPEC.md · CLAUDE.md. Build:
`python3 rt_build.py <slug...>` → /mnt/user-data/outputs/. Never rebuild the
flagship; only ADD pages.
