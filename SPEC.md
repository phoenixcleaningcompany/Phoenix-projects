# HM Series — Highway Maintenance & Roadworks Workwear (SPEC)

**Series #17 in the CW Hybrid matrix.** Procurement / Template A (Concierge).
One HTML page per UK town for highway maintenance teams and roadworks
contractors. Prefix `hm-`. Canonical/og to
`https://www.ineedworkwear.uk/hm-<slug>.html`.

## Audience & posture
Buyer = **procurement / depot or fleet manager** at a **local authority highways
department** OR a **term-maintenance / roadworks contractor** (council and
National Highways networks). Concierge tone: trade accounts, PO ordering,
volume pricing, multi-depot frameworks, plus a fast direct-online route for a
single depot or small works contractor. Medium local variation — research each
town's council highways arrangement, the motorway network and contractor mix.

## Lead products (verifier-enforced)
LEAD = **hi-vis** (Class 3), CO_LEAD = **safety boots**, TRI_LEAD =
**waterproofs**. 8-card grid: Class 3 Hi-Vis Jackets and Vests / Hi-Vis Trousers
and Coveralls / Safety Boots and Footwear / Waterproofs and Winter Layers /
Cargo and Work Trousers / Hard Hats, Gloves and Site PPE / Embroidered Polo
Shirts / Embroidery, Names and ID.

## Identity block — the differentiator
**"Chapter 8 and Sector Scheme Compliant Teams: Class 3 Hi-Vis for the
Highway"** (id `#contract`): work happens alongside live, often high-speed
traffic, governed by **Chapter 8 of the Traffic Signs Manual** and **EN ISO
20471 Class 3** conspicuity (a full jacket+trousers ensemble). The signature
detail running through the whole page: **branding is placed OFF the certified
retroreflective and background material** so the Class 3 rating is never
compromised; hi-vis is replaced not patched once below standard; sector-scheme
(NHSS) / audit context. **No nation handling.** This is what separates HM from
WM (refuse hi-vis) — roadworks/Chapter 8/National Highways, not bin rounds.

## Palette / design
Tarmac-slate `#334155` (hover `#1e293b`) + charcoal `#0f172a` + amber `#f59e0b`
highlight; **hi-vis-yellow `#f2d500` SVG garments** give the page its colour;
links `#1d6fa5`. Page bg `#eef1f4`, cards `#e6eaef`/`#cdd5de`. Fonts Lora +
Source Sans 3. 2 radial + 1 linear gradient. 5 SVG scenes: Class 3 garment row
(hi-vis jacket / hi-vis trousers / safety boot / hard hat), hi-vis embroidery,
town signpost (CHAPTER 8 / ROAD AND VERGE), **roadworks premises scene**
(chevron arrow board, roadworks warning triangle, traffic cones, road
markings), order-online.

## Hard rules (verify_hm.py, 16 checks)
1. Exactly **14 .com hrefs + 1 co.uk/community**. 2. No JS (ld+json only).
3. No HTML entities. 4. No delivery-timescale claims ("standard lead times" /
"we quote within twenty-four hours" OK). 5. Title ≤60, meta ≤160, no apostrophes
in meta. 6. Fonts Lora + Source Sans 3. 7. Organization+Service schema only.
8. **4 JSON-LD blocks** (FAQ+Org+Service+Breadcrumb) — check 16. 9. Lead trio
present (hi-vis/safety boots/waterproofs). 10. Word count ≥ floor. 11. Dead-link
guard: every `hm-<slug>.html` link must be a CSV town (check 15). 12. **BLEED
ban**: food-hygiene (BRCGS/hairnet/hygiene coat), security (SIA/body
armour/epaulette), cleaning (COSHH/tabard/tunic), waste (RCV/refuse
collection/bin lorry/HWRC), renewables (solar panel/EV charging/heat pump/MCS/
fall protection), care/edu (Ofsted/CQC), forestry/gas (Gas Safe/chainsaw/tree
surgery), sports. **NOTE: "Class 3", "EN ISO 20471", "hi-vis", "Chapter 8" are
LEGAL for HM** (its core) — the verifier deliberately does NOT block them (unlike
WM/RE which did, to keep them separated).

## Nearby = GEOGRAPHIC (global rule)
3 hand-authored, web-verified, geographically-close towns, all on HM_towns.csv.
`require_nearby()` raises on missing/<3/off-CSV — no rank/auto fallback.
London → Croydon/Bromley/Ilford. Birmingham → Solihull/West Bromwich/Walsall.
Leeds → Bradford/Pudsey/Dewsbury.

## Uniqueness
Floors: overall ≥77%, worst pair ≤52%. **Pair cap is the binding near-duplicate
guard** and passes comfortably (~34%). Overall ~67% at small N (heavy Chapter
8/scaffold, same family as WM/FB/RE), climbs with town count. Hard checks
(verify_hm) are the binding gate. Code may tune the gate as it scales; do not
chase 77 at small N.

## Research mandate
Every town web-researched (Medium local variation — still name real local
context: council highways arrangement/PFI, the motorway network + National
Highways, contractor mix). London flagship is the general-knowledge exception.
Birmingham: council highways under the Birmingham Highways Ltd PFI (Kier
Highways maintenance contractor in recent years, Tarmac surfacing; 2,500km
roads, 94,000 lighting columns), National Highways M5/M6/M42 + Spaghetti
Junction, WMCA funding. Leeds: in-house Connecting Leeds highways + long-running
street-lighting PFI, National Highways M1/M62/M621 with framework contractors,
WYCA funding.

## Files
hm-london.html (flagship/base) · hm_build.py · verify_hm.py · score_hm.py ·
diag_hm.py · HM_towns.csv (505) · SPEC.md · CLAUDE.md. Build:
`python3 hm_build.py <slug...>` → /mnt/user-data/outputs/. Never rebuild the
flagship; only ADD pages.
