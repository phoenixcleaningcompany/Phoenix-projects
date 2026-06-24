# DC research brief — read this fully before authoring

You are researching **delivery & courier workwear** location-page data for UK
towns. You author ONE Python dict entry per town, keyed by the **lowercased**
town name. Every local claim must be **web-verified** — do your own web searches,
never author from memory. Real, named proper nouns (distribution parks,
industrial estates, named depots, road corridors, business parks) are the whole
point: they are what make each page unique.

## Gold-standard reference (a real, shipped DC town — match this shape exactly)

```python
"birmingham": {
  "region": "Birmingham and the West Midlands",
  "nearby": ["Solihull", "West Bromwich", "Walsall"],   # FIXED — given to you, use verbatim
  "snapshot": "iNeedWorkwear supplies embroidered polos, softshells, fleeces, waterproofs, hi-vis vests and safety boots to couriers and delivery firms across Birmingham, from owner-driver and multidrop couriers to same-day firms and the depot fleets clustered around the city's motorway network, all branded in-house with the company name, on a trade account for a fleet or ordered direct online for an owner-driver.",
  "s1_head": "Kitting the people who deliver the West Midlands, door to door",
  "s1loc": [
    "Birmingham sits at the heart of the UK's logistics network, on the edge of the Midlands distribution belt and wrapped by the M5, M6, M40 and M42, with rail and air freight through New Street and Birmingham Airport. That connectivity makes the city one of the busiest delivery markets in the country, and it keeps a vast community of couriers and delivery drivers moving parcels, pallets and same-day consignments across the West Midlands every day.",
    "The operations span the whole spectrum. National carriers run parcel depots across the city, in trade parks at Aston, Tyburn and Erdington and along the motorway corridors, while a dense layer of independent same-day and multidrop firms and owner-drivers handles urgent, document and last-mile work into every postcode from the city centre to Solihull, Walsall and the Black Country. Almost all of them wear something branded, and almost all of it works hard in all weathers."
  ],
  "kit_loc": "across the city's doorsteps, depots and motorway-side hubs",
  "s2_intro": "Whether you drive a single van, run a multidrop round or operate a depot fleet across Birmingham and the motorway network around it"
}
```

## Field rules

- **region**: e.g. "Glasgow and the west of Scotland" / "Leeds and West Yorkshire". Real regional name.
- **nearby**: the EXACT 3-town list given to you. Do not change spelling or substitute.
- **snapshot**: ONE sentence. Fixed opener `iNeedWorkwear supplies embroidered polos, softshells, fleeces, waterproofs, hi-vis vests and safety boots to couriers and delivery firms across {Town}, from owner-driver and multidrop couriers to same-day firms and the depot fleets ` + a SHORT real-geography clause (e.g. `along the M8 and around Hillington Park`) + fixed closer `, all branded in-house with the company name, on a trade account for a fleet or ordered direct online for an owner-driver.`
- **s1_head**: short region-flavoured headline, e.g. "Kitting the people who deliver Greater Glasgow, door to door". Must NOT be identical across towns.
- **s1loc**: **EXACTLY 2 paragraphs**, local content ONLY (do NOT write generic "uniform"/"layering" prose — the generator adds those).
  - **Para 1** (~60-90 words): the town's logistics geography — motorway/road corridors, distribution belts, named industrial estates / distribution parks / depots / ports / airports / business parks. Lead with real named places.
  - **Para 2** (~60-90 words): the operator mix — national carrier parcel depots vs the dense layer of independent same-day / multidrop firms and owner-drivers; tie to a real local sector or anchor (port, university, retail park, manufacturing). End on the recurring beat "Almost all of them wear something branded, and almost all of it works hard in all weathers." (you may vary this closing sentence's wording slightly).
- **kit_loc**: a short phrase slotted after "...safety boots and caps", e.g. "across the city's doorsteps, depots and motorway-side hubs" or town-specific like "across the city's docks, estates and ring-road hubs".
- **s2_intro**: starts "Whether you drive a single van, run a multidrop round or operate a depot fleet across {Town}" + a real local road/area clause. **NO trailing punctuation** (a tail clause is appended).

## HARD CONSTRAINTS (a violation fails the build)

1. **ASCII ONLY.** Transliterate any accents (e.g. write "Strathclyde", not accented forms). Use straight apostrophes `'` and straight hyphens `-`. NO curly quotes, NO en/em dashes, NO `&` (write "and"), NO `<` or `>`.
2. **NO double-quote `"` anywhere inside a string value.** Apostrophes are fine.
3. **s1loc = exactly 2 paragraphs.** Local only.
4. **No delivery-timescale claims about US.** Never write "next-day delivery", "same-day delivery", "delivery within N hours", "24-hour delivery". (You MAY describe the courier's trade: "same-day firms", "same-day couriers", "multidrop rounds" — just never the word "delivery"/"delivered" right after same-day/next-day, and never a timed delivery promise.)
5. **Stay in DC's lane. Do NOT use any of these words** (they belong to other series): chainsaw, tree surgery, arborist, EN ISO 11393, LANTRA, NPTC, Chapter 8, National Highways, sector scheme, RCV, refuse collection, bin lorry, kerbside collection, HWRC, SIA, body armour, ballistic, stab vest, epaulette, door supervision, COSHH, tabard, tunic, hairnet, hygiene coat, BRCGS, HACCP, solar panel, EV charging, heat pump, MCS, Ofsted, CQC, Care Quality Commission, gym, hoodie, tracksuit, matchday.
6. **DC's own vocab is REQUIRED and good**: hi-vis, EN ISO 20471, multidrop, last-mile, parcel(s), owner-driver, courier, delivery driver, depot, softshell, polo, fleece, waterproof, safety boots. Use them naturally.
7. **VARY the Para-1 opening sentence structure** town to town — do not start every town with "{Town} sits on...". Mix: "Set on the...", "{Town} is...", "On the {road}, {Town}...", "A major {x} centre, {Town}...".

## Output

Return a single Python dict literal named `NEW`, mapping each lowercased town key
to its entry, AND write the same content to the given file path. Example:

```python
NEW = {
  "glasgow": { ...full entry... },
  "sheffield": { ...full entry... },
}
```

Make sure it is valid Python (the splicer will `exec` it). Final message = the
dict (the file is the source of truth for splicing).
