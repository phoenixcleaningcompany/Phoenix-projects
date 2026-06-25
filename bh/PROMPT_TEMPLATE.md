# BH research-agent brief (read this first, every batch)

You research and author per-town data for the BH (Beauty, Hair & Spa) workwear
location pages for iNeedWorkwear. You will WRITE one Python file
`research_bNNg{i}.py` of the form `NEW = { "<key>": {7 fields}, ... }` and return
ONLY a one-line confirmation per town (key + all-7-fields-present + the two s1loc
word counts + the 3 nearby). Do NOT paste the dict back.

## Posture (from SPEC.md / CLAUDE.md - do not drift)
Self-checkout / Template B. Audience = the salon/barber/spa BUSINESS (owner
buying a uniform), not the individual worker. Lead = order direct online, no
account (most are sole traders / small salons); a trade account is the secondary
route for a larger salon or group. Soft, presentation-led angle, NOT PPE.

## Do your own web research
Every local claim must be web-verified with REAL proper nouns: named salon/barber
districts, high streets, parades, arcades, quarters, the independent/sole-trader
mix. NEVER author from memory. London is the only general-knowledge exception.

## The 7 fields (gold-standard reference = the Leeds entry in bh_build.py TOWNS)
- `region`: "<Town> and <its region>".
- `nearby`: exactly 3 geographically-closest towns that appear VERBATIM in the
  BH_towns.csv `Town` column (the CSV is population-ranked, so many obvious
  neighbours are NOT on it - pick the nearest ones that ARE). This is for the
  nearby-links list ONLY - never put shopping areas/streets here.
- `snapshot`: copy the Leeds snapshot verbatim except the town name and the
  "from X to Y" middle clause (two real local contrasts). Keep the second
  sentence ("The trade is mostly sole traders...trade account.") word-for-word.
- `s1_head`: short region-flavoured headline; must differ town to town.
- `s1loc`: EXACTLY 2 paragraphs, ~70-95 words each, LOCAL CONTENT ONLY. Para 1 =
  geography of the local salon scene (named districts/streets/clusters). Para 2 =
  the operator mix (independents, named areas, mobile beauticians). Do NOT write
  the generic "no procurement department / order direct" prose - the generator
  appends that from its pools.
- `kit_loc`: short phrase slotted into a pool sentence, e.g. "across the city's
  salons, barber chairs and treatment rooms".
- `s2_intro`: "Whether you are a <real district> salon, a <real district> barber,
  a mobile beautician or a nail studio across <Town>" - NO trailing punctuation.

## Vary openings (biggest uniqueness lever)
Vary the Para-1 opening sentence STRUCTURE town to town (mix "<Town> is...",
"Set on the...", "Beyond the chains in..., <Town>...", "A major... centre,
<Town>...") and vary the Para-2 closing beat. For a tight geographic cluster in
one batch, differentiate hard using each town's OWN distinct centres/streets.

## HARD output constraints (a validator rejects violations, non-fatal per town)
- ASCII ONLY. Transliterate accents. Straight `'` and `-`. No curly quotes/dashes.
- No double-quote `"` inside any string value (apostrophes are fine).
- No `&` `<` `>` anywhere - write the word "and", never "&".
- `s1loc` exactly 2 strings; `nearby` exactly 3; key = lowercased exact CSV
  spelling (watch traps: `Weston-super-Mare`, `Newcastle upon Tyne`,
  `Bishop's Stortford`, `Newport (Isle of Wight)`, `Houghton le Spring`).
- Keep BH vocabulary (tunic/polo/apron/clog/salon/barber/beautician/spa/
  hairdressing/hoodie are core); EXCLUDE other series' vocab (security SIA/body
  armour, cleaning COSHH, food hairnet/BRCGS, courier multidrop/softshell,
  retail tabard/forecourt, etc.). No delivery-timescale promises ("standard lead
  times" is fine).
