# TL research-agent brief (read fully, follow exactly)

You research UK towns for a "Travel, Tourism and Leisure workwear" SEO page
series and write a JSON file of genuinely-local, proper-noun-rich content.
**Do ALL the web research yourself. Do NOT spawn sub-agents.**

Working directory: `/home/user/Phoenix-projects`
Write your output to EXACTLY: `towns/<batch>_<group>.json` (e.g. `towns/b02_g3.json`) — you are told which.

For EACH town, produce a JSON object **keyed by the EXACT town name given**, with:

- `"region"`: a natural region phrase that reads after the word "across", e.g. "Hull and East Yorkshire", "Swansea and South West Wales".
- `"nearby"`: the **LOCKED triple given to you, VERBATIM, in that order**. Never change, reorder, or substitute it.
- `"s1_head"`: a short section heading like "Kitting the visitor economy of <county/region>" (vary wording slightly per town).
- `"s1loc"`: **EXACTLY 3 paragraphs** (a JSON list of 3 strings), each **55–90 words**, ALL proper-noun-rich and genuinely local, on three DISTINCT angles:
    1. the town's marquee visitor attractions and the scale of its visitor economy (named museums, landmarks, cathedrals, piers, seafronts, castles, stadiums as tour venues, waterfronts);
    2. the leisure and activity layer (named parks, activity/watersports centres, family attractions, arenas and theatres, festivals/events, shopping and leisure quarters);
    3. heritage plus the hotel and tour-operator trade plus airport/transport plus named neighbourhoods/quarters.
  Use REAL named places you can verify by research. Do NOT use the generic "the trade runs at every size / we serve the big and the small alike" framing — that is added elsewhere on the page. All three paragraphs must be about real local places. **Depth matters: a downstream gate rejects any town whose paragraphs are short or lack named places (needs 3 paras, ≥50 words each, ≥175 words total, ≥30 proper nouns). Aim comfortably above that.**
- `"kit_loc"`: a short phrase completing "...are the whole kit {loc}.", e.g. "across the city's attractions, parks and visitor sites" or "across the coast's attractions and activity sites". Generic-local, no named places.
- `"s2_intro"`: a single clause with **NO terminal punctuation** that names ONE of the nearby towns, in the style: "Whether you are a major <Town> attraction or hotel group, a heritage site or a small independent activity centre in <NearbyTown>". End on the nearby town name, no full stop.

## HARD RULES (a gate rejects violations — follow exactly)
- **ASCII ONLY.** No pound signs (write "pound"), no curly quotes, no em-dashes (use " - "), no accented letters (write "cafe").
- **NEVER use the "&" character.** Always write "and" (e.g. "Bed and Breakfast", "Victoria and Albert").
- **Do NOT use any of these words** (they belong to other series and fail the page): charity, volunteer, foodbank, gym, "spa day", athleisure, tracksuit, tabard, hoodie, clog, barber, hairdressing, scrubs, veterinary, kennel, cattery, equine, courier, telecoms, fibre, broadband, "garden centre", forecourt, "farm shop", "convenience store". Ordinary tourism words (park, attraction, museum, leisure, activity centre, season, hotel, pier, beach, harbour, castle) are all fine.
- `"s1loc"` is a list of EXACTLY 3 strings. `"nearby"` is EXACTLY the 3 towns given, verbatim.
- Output VALID JSON, UTF-8, one top-level object containing your towns keyed by exact name. Write ONLY the JSON to the file.

## EXAMPLE (one town — shape and quality bar)
```json
{
  "Birmingham": {
    "region": "Birmingham and the West Midlands",
    "nearby": ["Solihull", "West Bromwich", "Walsall"],
    "s1_head": "Kitting the visitor economy of the West Midlands",
    "s1loc": [
      "Birmingham runs one of the country's biggest visitor economies, drawing over 145 million visits a year. The marquee draws include Cadbury World, the National SEA LIFE Centre, the LEGOLAND Discovery Centre and the Thinktank science museum at Millennium Point, with the open-air Black Country Living Museum and Bournville just outside the core.",
      "The leisure and activity layer is just as busy. Cannon Hill Park, the canals and bars at Brindleyplace and Gas Street Basin, Resorts World and the Utilita Arena, the Bullring shopping quarter and venues like the Hippodrome keep family attractions, activity operators and event teams working across the year.",
      "Heritage and hospitality round it out, from the Jewellery Quarter and Birmingham Museum and Art Gallery to Aston Hall and Sarehole Mill, supported by a deep city-centre hotel trade and a wide tour-operator and guide scene, with Birmingham Airport and the NEC drawing visitors from the doorstep."
    ],
    "kit_loc": "across the city's attractions, parks and visitor sites",
    "s2_intro": "Whether you are a major Birmingham attraction or hotel group, a heritage site or a small independent activity centre in Solihull"
  }
}
```

When done: write the file, then reply with ONE line only:
`<batch>_<group> done: <town1>, <town2>, ... | triples confirmed`. Nothing else.
