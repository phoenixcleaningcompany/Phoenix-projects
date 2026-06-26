# CP research-agent brief (single source of truth)

You research ONE UK town's corporate / professional-services economy and return a Python
`TOWNS` dict entry for `cp_build.py`. iNeedWorkwear supplies **branded polos, shirts,
softshells and fleeces** to **banks, law firms, accountancies, consultancies, insurers
and technology companies** — a managed, on-brand account (NOT a daily uniform). Corporate
kit here is a **brand exercise**: away days, conferences, exhibitions, site/client visits,
sponsored/fundraising events, new-starter welcome packs.

## What to produce, per town
A dict keyed by the lowercase slug-less town key (e.g. `"glasgow"`), with EXACTLY these fields:

```python
"glasgow": {
  "region": "<Town> and <wider area>",          # e.g. "Glasgow and the west of Scotland"
  "nearby": ["X","Y","Z"],                       # USE THE LOCKED TRIPLE I GIVE YOU, verbatim
  "snapshot": "<~70 words>",                     # see shape below
  "s1_head": "<short H2, ~6-9 words, town-specific>",
  "s1loc": [
     "<LOCAL PARAGRAPH 1 — 55-90 words, proper-noun rich>",
     "<LOCAL PARAGRAPH 2 — 55-90 words, proper-noun rich>",
  ],
  "kit_loc": "<short phrase, e.g. 'across the city centre and business district'>",
  "s2_intro": "Whether you are a <Town> bank, ... or a technology company",  # no trailing punctuation
},
```

### snapshot (one sentence + one)
Start: `iNeedWorkwear supplies branded polos, shirts, softshells and fleeces to banks, law
firms, accountancies, consultancies, insurers and technology companies across <Town>,
embroidered in-house to brand guidelines.` Then ONE town-specific clause about its scale as
a professional-services / financial / tech centre, then: `and we run it as a managed
account: a single point of contact, your brand pack held on file, and reorders kept
consistent across every office, team and event.`

### s1loc — the two genuinely-local paragraphs (the ONLY real uniqueness lever)
- **Paragraph 1 — the business/financial core + named firms.** The named business district(s)
  and quarters (e.g. Glasgow's International Financial Services District / Broomielaw); the
  real banks, law firms, accountancies, consultancies, insurers and tech employers PRESENT
  there; any notable HQs. Name real places and firms — this is the researched, flagship-style
  exception (named firms are allowed ONLY here, in s1loc).
- **Paragraph 2 — the people + why they buy branded kit.** Scale of the professional-services
  workforce, the universities / sectors feeding it, and the move into the "they wear suits but
  step into branded kit for conferences, away days, exhibitions and sponsored events" framing,
  bought by procurement / office / brand managers who care it matches the brand exactly.
- Proper-noun rich, factually accurate (web-research it), 55-90 words each.

## HARD RULES (a violation fails the verify gate — do not break these)
1. **ASCII only.** No curly quotes, no em-dashes (use " - " spaced hyphen), no pound sign
   (write "pound"), no accented characters. Write "and" — NEVER use `&`.
2. **No apostrophes problem:** apostrophes in body text are fine; just keep them straight `'`.
3. **No HTML entities** (`&amp;`, `&#39;` etc.) — write the literal ASCII character.
4. **No delivery-timescale claims** (no "next-day", "24 hour delivery", "delivered in 3 days").
5. **BLEED WORDS — BANNED anywhere on the page.** Do NOT use, even as a real local name —
   rephrase to an equally-accurate alternative:
   - `wellington` (boots bleed) — do NOT name Wellington Place/Street/College/Square; use
     "the city centre" / name a different quarter.
   - `charity` — use "fundraising", "sponsored" or "community".
   - `festival`, `stage`, `crew`, `rigging`, `front-of-house`, `steward`, `concert` (events bleed).
   - `tourism`, `theme park`, `holiday park`, `activity centre`, `tour operator`, `visitor`, `seaside`, `pier`.
   - sports: `gym`, `athleisure`, `club crest`, `matchday`, `tracksuit`.
   - `barber`, `hairdressing`, `beautician`, `clog`, `hoodie`, `spa day`/`spa`.
   - `scrubs`, `veterinary`, `tunic`, `vet nurse`, `kennel`, `cattery`, `equine`.
   - `telecoms`, `fibre`, `broadband`, `Openreach`; `foodbank`, `volunteer`; `courier`, `multidrop`;
     `tabard`, `convenience store`, `garden centre`, `forecourt`, `farm shop`, `stockroom`.
   - care/security/highways/forestry/cleaning/waste/renewables terms (CQC, SIA, Chapter 8,
     chainsaw, RCV, COSHH, solar panel, heat pump, etc.).
   - If your town's name or a key local landmark equals a bleed word, FLAG IT in your reply.
6. **CP CORE is legal and encouraged:** polo, shirt, softshell, fleece, quarter-zip, sweatshirt,
   gilet, bodywarmer, cap, embroidery, corporate, professional, bank, law firm, accountancy,
   consultancy, tech, away day, conference, exhibition, site visit, brand, account-managed.
7. **Lead trio** (polo, softshell, fleece) is carried by the pools — you don't need to force it.
8. **nearby** = the LOCKED triple given to you. Do not invent or change it. All three are on
   CP_towns.csv and geographically close.

## Output format
Reply with ONLY the Python dict entr(y/ies) — valid Python, ready to paste into `TOWNS`.
No prose, no markdown fences, no sub-agents. If you had to dodge a bleed collision, add a
single `# note:` comment line above the entry.
