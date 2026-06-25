# VT research-agent brief — read this first, every time

You research UK towns for the **VT (Veterinary & Animal Care) workwear** page
series and write one `TOWNS` entry per town. **Never author from memory — do real
web searches for every town.** Your output file is the source of truth; keep your
chat reply to a one-line confirmation per town.

## What VT sells (vocabulary spine — use it naturally)
Branded workwear for **vet practices, veterinary nurses, kennels, catteries, dog
groomers (salon + mobile) and equine/large-animal yards** — mostly small
businesses and sole traders. The differentiator is **two environments**:
- **Clinical** — scrubs, tunics, polos (wash hot, hygiene, reassure a worried owner).
- **Hands-on / outdoor** — fleeces, waterproofs, safety shoes, wellingtons
  (kennels, catteries, grooming room, stables, fields).

Posture is **self-checkout**: order direct online, no account; a trade account is
the secondary option for a larger practice/group. Lead products = **scrubs, polo,
fleece**. Do NOT write delivery-timescale promises (no "next-day"/"within 48
hours"); "standard lead times" only.

## The fields you write (exactly these 7, per town)
```python
NEW = {
  "<key>": {
    "region":   "<Town> and <county/area>",          # e.g. "Leeds and West Yorkshire"
    "nearby":   ["TownA", "TownB", "TownC"],          # see NEARBY rules below
    "snapshot": "iNeedWorkwear supplies branded scrubs, tunics, polos, fleeces, waterproofs and safety footwear to vet practices, veterinary nurses, kennels, catteries, dog groomers and equine yards across <Town>, from ... to ..., embroidered in-house with the practice name. Veterinary and animal care is mostly small practices and sole traders, so the quickest route is to order direct online with no account, while a larger practice or group can set up a trade account.",
    "s1_head":  "Kitting the practices, kennels and yards of <area>",   # short, must differ town-to-town
    "s1loc": [
      "<PARA 1: the local vet/animal-care scene — named practices/groups, kennels/catteries, groomers, rescues, equine/farm on the rural edge, real place names>",
      "<PARA 2: the operator mix — overwhelmingly small/independent, sole traders, what the uniform must do across clinical + outdoor>"
    ],
    "kit_loc":  "across the city's consulting rooms, kennels and yards",  # short phrase slotted into a pool sentence
    "s2_intro": "Whether you are an independent practice in <place>, a boarding kennels toward <place>, a mobile groomer or an equine yard across <Town>"  # NO trailing punctuation
  },
}
```

## HARD CONSTRAINTS (the splicer rejects violations — non-fatal, but re-do rejects)
- **`key`** = the **lowercased exact CSV spelling** of the town (e.g.
  `"stoke-on-trent"`, `"newcastle upon tyne"`, `"newport (isle of wight)"`).
- **`nearby`** = **exactly 3 unique towns, each appearing VERBATIM in the
  `VT_towns.csv` `Town` column** — the 3 geographically-closest that are ON the CSV.
  Many obvious neighbours are NOT on the 505 list; pick the nearest ones that are.
  For remote towns use the nearest regional cities. Nearby is a town list, **never
  shopping streets or districts**.
- **`s1loc`** = **exactly 2 paragraphs**, each ~55–90 words, genuinely local.
  Do NOT include the generic two-environments / sole-trader / "narrow range"
  prose — that is added automatically from shared pools. s1loc is ONLY local colour.
- **ASCII only. No `"` (inner double quotes). No `&`, `<`, `>`.** Write "and",
  not "&". No curly quotes/dashes — plain ASCII apostrophes and hyphens only.
- **`s2_intro`** must have **no trailing punctuation** (a pool tail is appended).
- Every text field plain prose; no HTML, no links (links come from the template).

## BIGGEST UNIQUENESS LEVER — vary structure town to town
- **Vary the Para-1 OPENING sentence structure** across your towns: mix
  "{Town} is …", "Set on the …", "Beyond the chains in …, {Town} …",
  "A market town …, {Town} …". Do not reuse one stock opener verbatim.
- **Vary the Para-2 opening beat too** — do not copy "And the trade is
  overwhelmingly small and independent…" verbatim across towns.
- For a tight geographic cluster, differentiate hard using each town's OWN
  distinct centres, streets and neighbouring villages.

## Disambiguation traps (which row the CSV means)
Chapeltown = Sheffield · Rothwell = West Yorkshire · Gosforth = Newcastle ·
Wellington = Somerset · Newport (Wales) and Newport (Isle of Wight) are separate
rows · Sutton = the south-London borough (not Sutton Coldfield/-in-Ashfield) ·
Hull (not "Kingston upon Hull").

## GOLD-STANDARD ENTRY (match this depth and shape)
```python
NEW = {
  "leeds": {
    "region": "Leeds and West Yorkshire",
    "nearby": ["Bradford", "Pudsey", "Dewsbury"],
    "snapshot": "iNeedWorkwear supplies branded scrubs, tunics, polos, fleeces, waterproofs and safety footwear to vet practices, veterinary nurses, kennels, catteries, dog groomers and equine yards across Leeds, from the suburban practices to the rural fringe, embroidered in-house with the practice name. Veterinary and animal care is mostly small practices and sole traders, so the quickest route is to order direct online with no account, while a larger practice or group can set up a trade account.",
    "s1_head": "Kitting the practices, kennels and yards of Yorkshire",
    "s1loc": [
      "Leeds has more than forty veterinary practices across the city, a mix of independents and bigger groups spread through Kirkstall, Colton, Horsforth, Armley, Morley and Shadwell. Around them sits the wider animal-care trade: boarding kennels, catteries and grooming on the rural fringe toward Wetherby and Wharfedale, mobile and salon dog groomers across the suburbs, doggy daycare and animal rescues, with equine and livery yards out toward Harewood and the Dales edge.",
      "And the trade is overwhelmingly small and independent. The suburban practices, the one-van groomers, the family-run kennels and catteries and the livery yards around the city are mostly small teams and sole traders rather than national chains. Each of them faces owners in the consulting room and works hands-on in the kennels and yard, so the uniform has to be clinically clean and tough enough for the outdoor side."
    ],
    "kit_loc": "across the city's consulting rooms, kennels and yards",
    "s2_intro": "Whether you are an independent practice in Kirkstall, a boarding kennels toward Wetherby, a mobile groomer or an equine yard across Leeds"
  },
}
```

## Output
Write your assigned towns to **`research_<batch><group>.py`** (the filename your
orchestrator gives you, e.g. `research_b01g3.py`) as a single `NEW = {...}` dict
covering all your towns. Then reply with **one line per town only**: the key, a
tick that all 7 fields are present, the two s1loc word counts, and the 3 nearby
towns. Do not paste the dict into chat.
