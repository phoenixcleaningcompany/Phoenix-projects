# DC Series — Delivery & Courier Services Workwear (SPEC)

**Series #13 in the CW Hybrid matrix.** One HTML page per UK town for couriers
and delivery firms. Prefix `dc-`. Canonical/og to
`https://www.ineedworkwear.uk/dc-<slug>.html`.

## Audience & posture — HYBRID A/B (like RE)
Audience = **Both**, tone = **Hybrid**: the ordering section gives **equal
billing** to a **fleet/depot operator on a trade account** (PO ordering, volume
pricing, multi-depot consistency) AND an **owner-driver / small courier firm
ordering direct online** (no account, fast). Neither is subordinate. Workwear
depth **Medium**, local variation **Low** (delivery operates similarly
everywhere) — so the differentiation is brand/uniform-led, not heavy compliance.

## Lead products (verifier-enforced)
LEAD = **polo** (embroidered polos), CO_LEAD = **hi-vis** (hi-vis vests),
TRI_LEAD = **softshell**. 8-card grid: Embroidered Polo Shirts and T-Shirts /
Softshell and Branded Jackets / Fleeces and Mid-Layers / Waterproof Jackets and
Coats / Hi-Vis Vests and Tops / Safety Boots and Footwear / Caps, Beanies and
Accessories / Embroidery, Names and ID.

## Identity block — the differentiator
**"Branded, All-Weather and Road-Ready: The Delivery Driver's Uniform"** (id
`#contract`) plus the branding section **"Your Driver Is Your Brand on the
Doorstep"**. The thread: the driver is the most visible, most frequent face of a
courier firm, so the kit is a **branded uniform first** (embroidered polos /
softshells / fleeces), framed as a **year-round layering system** (summer polo →
fleece → softshell → winter waterproof, hi-vis vest over the top), with hi-vis to
**EN ISO 20471** for roadside/depot visibility and safety boots for loading. This
is a brand-and-visibility angle, NOT a heavy-PPE compliance one. **No nation
handling.**

## Palette / design
Indigo `#4338ca` (hover `#3730a3`) + charcoal `#0f172a` + amber `#f59e0b`
highlight; SVG hi-vis `#f2d500`. Distinct from every prior series (teal/blue/
slate/forest-green). Page bg `#eef0f8`, cards `#e5e7f5`/`#c9cdee`, muted
`#4a4d80`, links `#4338ca`. Fonts Lora + Source Sans 3. 2 radial + 1 linear
gradient. 5 SVG scenes: delivery garment row (polo / softshell / hi-vis vest /
safety boot), logo embroidery, town signpost (COURIER KIT / ROAD AND DEPOT),
**delivery van and parcels premises scene**, order-online laptop.

## Hard rules (verify_dc.py, 16 checks)
1. Exactly **14 .com hrefs + 1 co.uk/community**. 2. No JS (ld+json only).
3. No HTML entities. 4. No delivery-timescale claims ("standard lead times" OK).
5. Title ≤60, meta ≤160, no apostrophes in meta. 6. Fonts Lora + Source Sans 3.
7. Organization+Service schema only. 8. **4 JSON-LD blocks** — check 16.
9. Lead trio present (polo/hi-vis/softshell). 10. Word count ≥ floor. 11.
Dead-link guard: every `dc-<slug>.html` link must be a CSV town (check 15).
12. **BLEED ban**: food (BRCGS/hairnet/hygiene coat), security (SIA/body armour/
epaulette), cleaning (COSHH/tabard/tunic), waste (RCV/refuse collection/bin
lorry/HWRC), renewables (solar panel/EV charging/heat pump/MCS), highways
(Chapter 8/National Highways/sector scheme), forestry (chainsaw/EN ISO 11393/
tree surgery/arborist/LANTRA/NPTC), care/edu (Ofsted/CQC), sports.
**NOTE: "polo", "softshell", "fleece", "hi-vis", "EN ISO 20471", "courier",
"delivery", "multidrop", "owner-driver", "safety boots", "waterproofs", "cap"
are LEGAL for DC** (its core) — not blocked. (hi-vis/EN ISO 20471 are shared with
HM, but DC blocks Chapter 8/National Highways to keep the two separated.)

## Nearby = GEOGRAPHIC (global rule)
3 hand-authored, web-verified, geographically-close towns, all on DC_towns.csv.
`require_nearby()` raises on missing/<3/off-CSV — no rank/auto fallback.
London → Croydon/Bromley/Ilford. Birmingham → Solihull/West Bromwich/Walsall.
Leeds → Bradford/Pudsey/Dewsbury.

## Low-variation handling (important for this series)
Because local variation is Low, the two generic paragraphs every town shares —
the "uniform before PPE" para and the "layering system" para — live in
**UNIFORM_POOL and LAYER_POOL (4 variants each, town-templated)**, NOT in the
per-town `s1loc`. Each town's `s1loc` holds only its 2 genuinely-local
paragraphs (logistics geography, carrier/owner-driver mix). This keeps cross-town
duplication down as the series scales. Do NOT push generic uniform/layering prose
back into `s1loc`.

## Uniqueness
Floors: overall ≥77%, worst pair ≤52%. **Pair cap is the binding near-duplicate
guard** and passes (~36%). Overall ~64% at small N (heavy shared scaffold; DC is
naturally more templated than high-variation series), climbs with town count.
Hard checks (verify_dc) are the binding gate. Code may tune the gate as it
scales; do not chase 77 at small N.

## Research mandate
Every town web-researched for its local logistics geography (motorway/distribution
connectivity, carrier depots, same-day/owner-driver scene) even though variation
is Low — name something real. London flagship is the general-knowledge exception.
Birmingham: edge of the logistics Golden Triangle, M5/M6/M40/M42 + rail + airport,
carrier depots at Aston/Tyburn/Erdington, dense same-day/owner-driver scene.
Leeds: M1/M62/M621 crossroads of the North, Stourton/Gelderd Road hubs + the
Wakefield/Normanton/Castleford M62 belt, legal/financial document couriers +
retail fulfilment.

## Files
dc-london.html (flagship/base) · dc_build.py · verify_dc.py · score_dc.py ·
diag_dc.py · DC_towns.csv (505) · SPEC.md · CLAUDE.md. Build:
`python3 dc_build.py <slug...>` → /mnt/user-data/outputs/. Never rebuild the
flagship; only ADD pages.
