# EV batch-agent brief — read this in full before writing

You research UK towns and write **one JSON entry per town** for the EV
(Entertainment, Events & Festivals) workwear page series. Your entries are the
ONLY genuinely-unique content on each page; everything else is pooled boilerplate.
Accuracy and local specificity are the whole job.

## What you do
1. **Web-research each assigned town's live-events economy** (real, current 2024-2025):
   marquee arena(s)/biggest venues, key theatres & concert halls, the grassroots
   live-music venues it is known for, the big festivals **and their actual sites/parks**,
   and any events-production/staging cluster or flagship civic event.
2. Write the JSON entry per the schema below.
3. Write your group's file: `towns/bNN_gX.json` (e.g. `towns/b01_g3.json`), a single
   JSON object mapping each town key to its entry. **Do NOT spawn sub-agents.** Reply
   one line: the count written.

## JSON schema (every field required)
```json
{
  "<town key, lowercase, exactly as the CSV spells it>": {
    "region": "<Town> and <its county/area>",
    "nearby": ["<A>", "<B>", "<C>"],         // USE THE LOCKED TRIPLE GIVEN TO YOU, verbatim
    "snapshot": "iNeedWorkwear supplies branded polos, hi-vis, fleeces, waterproofs and safety boots to concert venues, festival operators, event production companies, theatres and independent event crews across <Town>, embroidered in-house with the operator name. The trade runs from big venues and festivals with large seasonal crews to small independent crews and promoters, so a larger operator can run a trade account for managed reordering and seasonal intake, while a small crew can order direct online with no account.",
    "s1_head": "<short local headline, e.g. 'Kitting the events trade of <area>'>",
    "s1loc": [
      "<LOCAL PARAGRAPH 1 — 55-90 words, proper-noun rich>",
      "<LOCAL PARAGRAPH 2 — 55-90 words, proper-noun rich>"
    ],
    "kit_loc": "across the city's venues, festivals and events",
    "s2_intro": "Whether you are a major <Town> venue or festival, a production company or a small independent event crew <local nod>"
  }
}
```

## The two `s1loc` paragraphs (the only thing that matters for uniqueness)
- **Para 1 — the venues/festivals para.** Name the real marquee arena/venue, 1-2
  theatres or concert halls, a grassroots room or two, and the big festival(s) **with
  their site** (e.g. "TRNSMT at Glasgow Green", "Parklife at Heaton Park"). This is the
  page's fingerprint — make it unmistakably this town.
- **Para 2 — the trade-shape para.** How the events trade runs at every size here: big
  venues/arenas/festival operators and production companies with large seasonal crews
  buying through procurement, AND independent crews/promoters/entertainers wanting a few
  branded pieces — so a supplier serves the big festival and the single crew alike. Give
  it a light local nod (a district, the wider county) but keep it mostly about the
  two-sizes-of-buyer shape.
- Each 55-90 words. Plain ASCII, straight quotes only. Factual: if unsure, omit — never
  invent a venue or festival. Use **timeless framing** ("hosts", "fills the summer",
  name the site) rather than claiming a specific future date — some festivals end or
  move.

## Hard rules (the build will reject violations)
- **No iNeedWorkwear links, no HTML, no URLs** anywhere in your text. Plain prose only.
- **ASCII only.** No curly quotes, em-dashes (use a comma or " - "), or accents.
- **No `&`** — write "and". No HTML entities.
- **No delivery-timescale claims** ("next-day", "within 48 hours", etc).
- **Use the locked nearby triple exactly as given** — do not pick your own.
- The town key must be the **CSV spelling, lowercased** (e.g. `newcastle upon tyne`,
  `weston-super-mare`).

## BLEED — banned vocabulary (these belong to OTHER series; do not use them)
softshell, hoodie; corporate / professional services / accountancy / consultancy /
law firm / procurement-as-a-service framing of YOUR copy (the word "procurement" is
fine only as "buy through procurement"); barber, hairdressing, spa day, clog; tourism,
theme park, holiday park, activity centre, tour operator, seaside, pier, visitor
attraction; veterinary, scrubs, kennel, cattery, equine, wellington; charity, foodbank,
volunteer; telecoms, fibre, broadband, Openreach; courier, multidrop; SIA, door
supervision, stab vest, body armour; gym, tracksuit, matchday; tabard, garden centre,
forecourt, farm shop; chainsaw, arborist; CQC, Ofsted; RCV, refuse, bin lorry; solar
panel, heat pump, EV charging; Chapter 8, National Highways.
**EV CORE (use freely):** polo, hi-vis, fleece, waterproof, cargo trousers, safety
boots, cap, beanie, embroidery, event, festival, stage, crew, rigging, venue,
production, front-of-house, steward, concert, seasonal. Named venues/festivals belong
ONLY in your two local paragraphs.
**Watch for real place-names that collide with bleed words** (e.g. a "Wellington
Street", a "Spa" town): rephrase to an equally-accurate alternative.

## Worked example (Birmingham)
```json
{
  "birmingham": {
    "region": "Birmingham and the West Midlands",
    "nearby": ["Solihull", "West Bromwich", "Walsall"],
    "snapshot": "iNeedWorkwear supplies branded polos, hi-vis, fleeces, waterproofs and safety boots to concert venues, festival operators, event production companies, theatres and independent event crews across Birmingham, embroidered in-house with the operator name. The trade runs from big arenas and festivals with large seasonal crews to small independent crews and promoters, so a larger operator can run a trade account for managed reordering and seasonal intake, while a small crew can order direct online with no account.",
    "s1_head": "Kitting the events capital of the Midlands",
    "s1loc": [
      "Birmingham is the Midlands' events capital. The canal-side Utilita Arena and bp pulse LIVE at the NEC handle the big arena tours, Symphony Hall hosts the City of Birmingham Symphony Orchestra, the O2 Academy and O2 Institute anchor the Digbeth music quarter, and the Hippodrome runs as the busiest single theatre in the UK, while open-air festivals like MADE in Birmingham at Luna Springs and the Mostly Jazz, Funk and Soul Festival at Moseley Park fill the summer.",
      "And the trade runs at every size. Major venues, arenas, festival operators and production companies run big crews and large seasonal teams and buy through procurement, while independent event crews, promoters and entertainers around Digbeth and the wider city need just a few branded pieces. A workwear supplier here has to serve the big festival and the single crew alike, which is why we run trade accounts and direct online ordering side by side."
    ],
    "kit_loc": "across the city's venues, festivals and events",
    "s2_intro": "Whether you are a major Birmingham arena or festival, a production company or a small independent event crew in Digbeth"
  }
}
```
After writing, the orchestrator runs `preflight_ev.py` on your file — fix anything it flags.
