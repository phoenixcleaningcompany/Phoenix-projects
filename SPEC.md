# FS Series — Forestry, Arboriculture & Tree Surgery Workwear (SPEC)

**Series #18 in the CW Hybrid matrix. First TEMPLATE B (self-checkout / small
business) in the run.** One HTML page per UK town for arborists, tree surgeons
and forestry contractors. Prefix `fs-`. Canonical/og to
`https://www.ineedworkwear.uk/fs-<slug>.html`.

## Audience & posture — TEMPLATE B (the key difference)
Buyer = **the tree surgeon themselves**: a **sole-trader arborist or small
crew**, not a procurement manager. Posture flips from the A-series concierge
(trade accounts / PO ordering / multi-depot) to **direct online self-checkout**:
no account, no minimum order, no quote to wait on. A trade account is mentioned
only as a secondary "if your team grows" line. The whole page is written to the
owner-operator who buys their own kit, gets the sizes and protection class right,
adds a logo and checks out. Local variation Medium, rural variation strong.

## Lead products (verifier-enforced)
LEAD = **chainsaw** (chainsaw trousers/PPE), CO_LEAD = **safety boots**,
TRI_LEAD = **helmet** (forestry helmet). 8-card grid: Chainsaw Trousers and
Protective Clothing / Chainsaw Boots and Safety Footwear / Forestry Helmets,
Visors and Ear Defenders / Chainsaw Gloves and Hand Protection / Hi-Vis Jackets
and Tops / Waterproofs and Base Layers / Embroidered Polo Shirts and Tops /
Embroidery, Names and ID.

## Identity block — the differentiator
**"Chainsaw-Rated, Climb-Ready PPE: EN ISO 11393 for Arborists"** (id
`#contract`): tree work is one of the highest-risk trades, so chainsaw
protection is the core of the range, not an add-on. Rated to **EN ISO 11393**
(the standard that replaced **EN 381**), **Type A** front protection for ground
work and **Type C** all-round for climbing/aerial work, usually **Class 1** for a
20 m/s chain speed, worn with a forestry helmet (mesh visor + ear defenders),
chainsaw boots and gloves. **No nation handling.**

## Palette / design
Forest green `#166534` (hover `#14532d`) + charcoal `#0f172a` + amber `#f59e0b`
highlight; **orange chainsaw-PPE SVG garments** `#e8651f` (orange chainsaw
trousers + orange forestry helmet with mesh visor) so it reads forestry, not
WM-green; SVG hi-vis `#f2d500`. Page bg `#eef4ef`, cards `#e2efe6`/`#c3dcca`,
muted `#3f6b50`, links `#166534`. Fonts Lora + Source Sans 3. 2 radial + 1
linear gradient. 5 SVG scenes: chainsaw garment row (chainsaw trousers / forestry
helmet / chainsaw boot / hi-vis), logo embroidery, town signpost (CHAINSAW PPE /
CLIMB AND GROUND), **woodland premises scene** (trees, stump with rings, stacked
cut logs), order-online laptop.

## Hard rules (verify_fs.py, 16 checks)
1. Exactly **14 .com hrefs + 1 co.uk/community**. 2. No JS (ld+json only).
3. No HTML entities. 4. No delivery-timescale claims ("standard lead times" OK).
5. Title ≤60, meta ≤160, no apostrophes in meta. 6. Fonts Lora + Source Sans 3.
7. Organization+Service schema only. 8. **4 JSON-LD blocks** (FAQ+Org+Service+
Breadcrumb) — check 16. 9. Lead trio present (chainsaw/safety boots/helmet).
10. Word count ≥ floor. 11. Dead-link guard: every `fs-<slug>.html` link must be
a CSV town (check 15). 12. **BLEED ban**: food-hygiene (BRCGS/hairnet/hygiene
coat), security (SIA/body armour/epaulette), cleaning (COSHH/tabard/tunic),
waste (RCV/refuse collection/bin lorry/HWRC), renewables (solar panel/EV
charging/heat pump/MCS), **highways (Chapter 8/National Highways/sector scheme —
blocked to separate FS from HM)**, care/edu (Ofsted/CQC), sports.
**NOTE: "chainsaw", "EN ISO 11393", "EN 381", "tree surgery", "arborist",
"LANTRA", "NPTC", "Type A", "Type C", "forestry helmet", "hi-vis", "safety
boots" are LEGAL for FS** (its core) — the verifier deliberately does NOT block
them.

## Nearby = GEOGRAPHIC (global rule)
3 hand-authored, web-verified, geographically-close towns, all on FS_towns.csv.
`require_nearby()` raises on missing/<3/off-CSV — no rank/auto fallback.
London → Croydon/Bromley/Ilford. Birmingham → Solihull/West Bromwich/Walsall.
Leeds → Bradford/Pudsey/Dewsbury.

## Uniqueness
Floors: overall ≥77%, worst pair ≤52%. **Pair cap is the binding near-duplicate
guard** and passes comfortably (~36%). Overall ~66% at small N (heavy chainsaw-
PPE/scaffold, same family as the other series), climbs with town count. Hard
checks (verify_fs) are the binding gate. Code may tune the gate as it scales; do
not chase 77 at small N.

## Research mandate
Every town web-researched (Medium/strong rural variation — name real local arb
context: the urban-forest/woodland character, named parks, council/park tree
work, the small-firm/sole-trader scene, NPTC/LANTRA/Arb Association, BS 3998 /
BS 5837). London flagship is the general-knowledge exception. Birmingham: 1m+
trees, UN Tree City of the World, Sutton Park NNR + Forest of Arden, leafy
suburbs (Edgbaston/Sutton Coldfield/Moseley), NPTC firms to BS 3998, ash dieback
work. Leeds: Roundhay Park/Temple Newsam/Meanwood Valley + White Rose Forest,
leafy suburbs (Roundhay/Chapel Allerton/Headingley/Alwoodley), NPTC/LANTRA/Arb
Association small firms, TPO/conservation-area work.

## Files
fs-london.html (flagship/base) · fs_build.py · verify_fs.py · score_fs.py ·
diag_fs.py · FS_towns.csv (505) · SPEC.md · CLAUDE.md. Build:
`python3 fs_build.py <slug...>` → /mnt/user-data/outputs/. Never rebuild the
flagship; only ADD pages.
