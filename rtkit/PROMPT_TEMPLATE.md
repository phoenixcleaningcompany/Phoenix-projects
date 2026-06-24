# RT research brief — read this first, then research YOUR towns

You are researching UK towns for the **RT (Supermarkets & Retail) workwear**
page series (supplier: iNeedWorkwear). One HTML page per town is generated from
a per-town data entry plus shared prose pools. Your job: **web-research each
assigned town's independent-retail scene and return one data entry per town.**

## Posture (do not drift)
- Audience: **independent retailers, convenience stores, forecourts, garden
  centres, farm shops, small multi-store groups** — NOT the big supermarket
  chains (they tender uniforms centrally). The angle is "your staff are your
  shopfront": branded polos/tabards/fleeces front of house; safety shoes, hi-vis,
  stockroom trousers back of house.
- You are ONLY writing the **2 genuinely-local paragraphs** + a few short local
  fields per town. The generic "chains tender centrally / shopfront / consistency"
  prose is added automatically by the generator — DO NOT write it yourself.

## Research mandate
- Do your OWN web searches for every town. **Never author from memory.**
- Name **real** local retail geography: named high streets / shopping streets,
  Victorian arcades, covered/street markets, independent quarters, suburb/
  neighbourhood high streets, convenience-store density, garden centres, farm
  shops on the town fringe. Real proper nouns are the whole point — they are what
  make each page unique.

## HARD CONSTRAINTS (the splicer rejects violations)
1. **ASCII only.** Transliterate accents. Straight `'` apostrophe and `-` hyphen.
   **No `&`** — write "and". **No `<` or `>`.** No curly quotes/dashes.
2. **No `"` (double quote) inside any string value.** Apostrophes are fine.
3. **`s1loc` = exactly 2 paragraphs**, local content only (see structure below).
4. The dict **key** must be the **lowercased exact CSV spelling** of the town
   (provided to you per town — use it verbatim).
5. **`s2_intro` must have NO trailing punctuation** (no full stop / comma at end).
6. Use the **nearby list provided to you verbatim** (already CSV-validated) — do
   not invent your own nearby towns.

## Uniqueness (important — vary town to town)
- **Vary the Para-1 opening sentence structure** across towns: mix frames like
  "{Town} is ...", "Set on the ...", "A major ... centre, {Town} ...",
  "Beyond the chains in ..., {Town} ...". Do not reuse one stock opener.
- **Vary the Para-2 opening and the closing beat.** Para-2 ends on a line about
  staff being customer-facing and the businesses being independents not chains —
  but phrase it **differently for each town** (do not copy the reference verbatim).

## Entry schema (return one per town)
```python
"<lowercased exact CSV key>": {
  "region": "<Town> and <county/region>",
  "nearby": ["<Near1>", "<Near2>", "<Near3>"],   # use the provided list verbatim
  "snapshot": "<the fixed sentence below, only {Town} and the two 'from A to B' features change>",
  "s1_head": "<short region-flavoured headline, must differ across towns>",
  "s1loc": ["<para1: central retail geography>", "<para2: suburban high streets + convenience + garden/farm>"],
  "kit_loc": "across the <area>'s high streets, convenience stores and garden centres",
  "s2_intro": "Whether you run a <real neighbourhood> high-street shop, a convenience store, a garden centre or a small group of sites across <Town>"
}
```

### Fixed snapshot template (only the town + the two features vary)
> iNeedWorkwear supplies embroidered polos, tabards, fleeces, safety shoes,
> hi-vis and stockroom trousers to independent retailers, convenience stores,
> garden centres and farm shops across **{Town}**, from **{feature A}** to
> **{feature B}**, branded in-house with the shop name on a managed trade
> account, with artwork and sizes held on file so new starters and second stores
> are kitted in exactly the same uniform.

## GOLD-STANDARD REFERENCE (Leeds — already built; do NOT resubmit Leeds)
```python
"leeds": {
  "region": "Leeds and West Yorkshire",
  "nearby": ["Bradford", "Pudsey", "Dewsbury"],
  "snapshot": "iNeedWorkwear supplies embroidered polos, tabards, fleeces, safety shoes, hi-vis and stockroom trousers to independent retailers, convenience stores, garden centres and farm shops across Leeds, from the Victorian arcades and Kirkgate Market to the suburban high streets, branded in-house with the shop name on a managed trade account, with artwork and sizes held on file so new starters and second stores are kitted in exactly the same uniform.",
  "s1_head": "Kitting the shops that line Yorkshire's high streets",
  "s1loc": [
    "Leeds is one of the top retail cities in the UK, and beyond the chains in Trinity and Victoria Leeds sits a deep independent scene. The Victorian arcades, Grand, Queens, Thornton's and the County Arcade, and the Corn Exchange under its domed roof hold independent boutiques and homeware stores, while Kirkgate Market, one of the largest covered markets in Europe and the birthplace of Marks and Spencer, runs on independent traders, grocers and delis spanning generations.",
    "Beyond the centre, the suburban high streets carry the everyday independents: Chapel Allerton, Headingley, Meanwood, Cross Gates and out to Farsley and Bramley, full of family-run shops, bookshops, plant and refill stores and convenience stores, with farmers' and makers' markets and garden centres across West Yorkshire. Almost every one of these puts staff in front of customers in something branded, and almost all of them are independents rather than chains."
  ],
  "kit_loc": "across the city's high streets, convenience stores and garden centres",
  "s2_intro": "Whether you run a Chapel Allerton high-street shop, a convenience store, a garden centre or a small group of sites across Leeds"
}
```
(Note: write "and", never "&" — the reference shows "Marks and Spencer", not "M&S".)

## Output
- Write your towns to the file path you are given (e.g.
  `research_b1g1.py`) as a single assignment: `NEW = { ...your town entries... }`.
- The file must be valid Python (a dict literal). Use straight ASCII quotes.
- **Return ONLY a one-line confirmation** per town: the key, its 5 short field
  names present, and the word count of each s1loc paragraph. **Do NOT paste the
  full dict back** — the file is the source of truth.
