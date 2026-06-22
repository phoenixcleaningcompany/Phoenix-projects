# RESEARCH.md — EAT series research contract

This is the brief a **research sub-agent (Sonnet + WebSearch/WebFetch)** follows
to turn a town name into a complete, evidence-backed `TOWNS["<slug>"]` entry in
`towns_data.py`. Read SPEC.md for the product rules. Your job here is the part a
script cannot do: **finding real venues and proving they are open today.**

## The one rule that matters most
**Every venue must be confirmed CURRENTLY TRADING, by live web check, today.**
Having web access does not make this automatic — a general search will happily
surface a place from a 2021 "best of" list that has since closed. Confirming
closure is the single highest-value thing you do. Two real traps already caught
obvious Birmingham picks:
- *The Bartons Arms* — the city's finest pub interior, but closed again in July
  2025. Rejected.
- *Purnell's* — lost its Michelin star in October 2024 and the chef moved on.
  Rejected as "the" destination restaurant.
A page that sends a hospitality owner to a restaurant that shut last year is
worse than no page. When in doubt, pick the venue you *can* confirm is open.

## Trading-status check (do this for EACH of the four venues)
A venue passes only if you can answer YES to the live checks:
1. Does it have a **current** web presence — its own site, or a Google/Maps
   listing **not** marked "Permanently closed" / "Temporarily closed"?
2. Are there **recent** signals of life — reviews, posts, or events within the
   last few months; opening hours shown; bookings open?
3. For award claims (Michelin, AA, etc.), is the accolade **still current**?
   Check the official guide, not a blog. State the year.
4. Nothing in the last ~12 months reporting it closed, in administration, or
   relocated to a different town?

Record the strongest single URL you used as `source_url` (prefer the venue's own
site or its official Maps/guide listing) and today's date as `verified`
(`YYYY-MM-DD`). If you cannot satisfy the checks, **choose a different venue.**

## What to find (the four picks)
Four genuine **independents** (a brewery-tied pub is fine if named honestly,
e.g. Fuller's / Samuel Smith's), one per everyday category:
`Takeaway/Casual · Cafe · Restaurant · Pub`.
- The **tag may flex to the local signature** (Birmingham used "Balti House").
- Favour places with a real story: founding date, a signature dish, a notable
  room, a neighbourhood association. Specifics are the uniqueness engine.
- Avoid faceless chains. Spread them across the town's actual food districts.

## What else to capture
- **Food geography**: the named neighbourhoods/markets that define where the
  town eats, and the local signature dish if there is one. This feeds
  `food_scene`, `visit`, `snapshot`.
- **Nearby (3)**: three geographically close towns. **Each MUST be on
  `eat_towns.csv`** — check before writing, or the build hard-fails. Pick real
  neighbours, not the next biggest towns.
- **Meta**: a `meta_title` <=60 chars containing the town; a `meta_description`
  110-155 chars, **no apostrophes**, with light CTA language.
- **pivot_variant**: choose `high-volume` (big city / busy centre),
  `pub-town`, `coastal`, or `market-town`. Write a one-sentence
  `pivot_local_hook` tying the town's cooking to grease load (e.g. a balti
  seared over an open flame; a seaside fryer through summer).

## Output — append exactly this shape to towns_data.py
```python
TOWNS["<slug>"] = {
    "region": "...", "population": "...",
    "nearby": ["A", "B", "C"],                      # all on eat_towns.csv
    "meta_title": "Best Places to Eat in <Town>: Local Food Guide",   # <=60
    "meta_description": "...no apostrophes... Read the guide.",        # 110-155
    "trust_strip": "...",
    "snapshot": "For a fast answer: <v1> for ..., <v2> for ..., <v3> for ..., and <v4> for ...",
    "stats": [("...","..."), ("...","..."), ("...","..."), ("4","Hand-picked independents")],
    "pivot_variant": "high-volume",
    "pivot_local_hook": "...",
    "venues": [
        {"type":"Takeaway","name":"...","area":"...","cuisine":"...",
         "body":"~90-130 words, specific and researched",
         "known_for":"...","good_for":"...",
         "source_url":"https://...","verified":"YYYY-MM-DD"},
        # Cafe, Restaurant, Pub - same shape, each with source_url + verified
    ],
    "food_scene": ["para","para","para"],
    "visit": ["para","para"],
    "checklist": ["...","...","...","...","..."],
    "what_to_order": "...",
    "glance": [("Best for a quick bite","..."),("Best for an occasion","..."),("Best for atmosphere","...")],
    "faq": [("Q?","A."), ("Q?","A."), ("Q?","A."), ("Q?","A."), ("Q?","A."), ("Q?","A.")],
    # optional: "hero_svg": "<svg ...>...</svg>"  (else a generic fallback is used)
}
```
General-knowledge flagships (London) may instead set `"evidence_exempt": True`.
Everything else must carry `source_url` + `verified` on all four venues or the
build fails under `--require-evidence`.

## Then hand off to the build
Once the entry is appended, the orchestrator takes over (no web needed):
```
./make_town.sh <slug>
```
which runs `eat_build.py --require-evidence` → `verify_eat.py --require-evidence`
→ `score_eat.py`. If verify fails, fix the entry and re-run; never publish a page
that has not passed the gate.
