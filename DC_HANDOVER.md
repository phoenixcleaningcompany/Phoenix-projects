# DC (Delivery & Courier Services) build — handover

Carries forward everything proven on the **FS (Forestry / Arboriculture)** build
(505 pages, all gates green). DC is the **same machine, new vocabulary**: 505
Template-B location pages, one per UK town, page prefix `dc-`, canonical/og to
`https://www.ineedworkwear.uk/dc-<slug>.html`.

Read this first, then SPEC.md (when it lands) and the new CLAUDE.md. The
filesystem resets between sessions — recreate the kit from the shipped files.

---

## 0. THE ONE BUG YOU MUST NOT REINHERIT (read this twice)

Every `_build.py` in this family was cloned down the chain (HM → FS → DC). The
variant selector `pick(key, salt, n)` originally used a **CRC32 checksum**:

```python
def pick(key, salt, n):
    return zlib.crc32((salt + '|' + str(key).lower()).encode()) % n   # ❌ BROKEN
```

CRC32 is a checksum, not a hash — its low-order bits (the only ones `% n` reads)
stay correlated with the input. Structurally similar keys collide on the **same
index in every pool at once**, so whole pages come out near-identical. On FS,
every 7-letter town (`bristol`, `cardiff`, `glasgow`, `reading`, `swansea`)
produced an identical 23-pool vector → worst pair **83%**, ~20 over-cap pairs on
the first build.

**The fix — already in `fs_build.py`, port it verbatim:**

```python
import hashlib

def pick(key, salt, n):
    # md5 digest gives well-distributed bits; crc32 % n leaks correlated low
    # bits (e.g. all 7-letter town names collided on the same pool variant).
    h = hashlib.md5((salt + '|' + str(key).lower()).encode()).digest()
    return int.from_bytes(h[:4], 'big') % n
```

md5 is fine — this is a distribution problem, not security. Keep the exact same
`salt + '|' + key` composition; only the bit-mixing changes. On FS this took the
worst pair 83% → 48% on the spot.

**First thing to do in the DC session:** `grep -n crc32 dc_build.py`. If it's
there, patch it before building a single page. (And HM — the original — almost
certainly still has it; flagged separately, its kit wasn't in this session.)

---

## 1. What DC is (confirm against the real SPEC)

**Template B (self-checkout)** — buyer is an **owner-driver courier / multi-drop
driver / small man-and-van or last-mile firm**, ordering DIRECT online, no
account, no minimum, no quote. This buyer fits Template B even better than FS did
(huge self-employed/owner-driver population). Keep the self-checkout voice; a
trade account is a brief "if your fleet grows" mention only.

**Likely lead trio** (verify in SPEC before coding the verify gate):
- **hi-vis** (EN ISO 20471) — couriers loading/roadside/depot yards
- **safety boots** (EN ISO 20345)
- **polo / softshell** (branded driver identity)
…with waterproofs/softshells as all-weather multi-drop support. FS's trio was
`chainsaw` / `safety boots` / `helmet`; DC's will differ — set `LEAD`,
`CO_LEAD`, `TRI_LEAD` in `verify_dc.py` accordingly.

**Distinctive thread** (DC's equivalent of FS's "chainsaw cut-protection /
EN ISO 11393" spine): branded, all-weather **driver/courier identity** —
hi-vis to EN ISO 20471, embroidered/printed company name + driver ID, kit that
survives multi-drop wear, ordered direct by the owner-driver. Lock one
distinctive vocabulary spine and keep it on every page (it's what stops the
pages reading generic).

**Nearby = geographic** (3 close towns, all on the CSV). No nation handling
beyond using the right national bodies in prose. 14 `.com` links + 1 community
link per page. 4 JSON-LD blocks (FAQ + Org + Service + Breadcrumb).

---

## 2. The kit (recreate beside `dc_build.py`)

| File | Role |
|---|---|
| `dc_build.py` | generator: reads flagship `dc-london.html`, extracts shared chrome via `between()`/`aria_block()` markers, assembles each town from md5-hashed prose pools + inline `TOWNS` dict |
| `dc-london.html` | flagship base template the generator reads; **also IS the London page** — never rebuild it, only add other pages |
| `DC_towns.csv` | `Rank, Town, Population, Nation` — population-ranked, 505 rows |
| `verify_dc.py` | **hard gate** — the binding pass/fail |
| `score_dc.py` | dup scorer (diagnostic + the 52% pair cap) |
| `diag_dc.py` | pair-collision diagnostic → tells you ~N words to add to the weaker page |

**Clone gotcha:** when cloning from `fs_*`, after `fs_`→`dc_` also explicitly
`s/score_fs/score_dc/; s/diag_fs/diag_dc/` (the import-name rename bit us on the
HM→FS clone — `diag` imports the scorer by module name).

---

## 3. The gates

**`verify_dc.py` (HARD — the only binding gate). Per page it checks:**
- exactly **14** `ineedworkwear.com` links + exactly **1** community link
- **4** JSON-LD blocks (`script type="application/ld+json"`) — FAQ+Org+Service+Breadcrumb
- no JavaScript (script tag / `javascript:` / `on*=` handlers), no HTML entities
- meta description present, ≤160 chars, unique across the set
- town in `<title>` and `<h1>`; unique title; filename slug matches
- no delivery-timescale claims (**note:** DC is literally about delivery — the
  regex bans *our* delivery promises like "next-day delivery" of workwear, NOT
  the courier's trade. Re-read this regex carefully so legitimate courier prose
  doesn't trip it. May need loosening for DC.)
- **BLEED list** — bans OTHER series' core vocab so series stay separated. For
  DC: block chainsaw/tree-surgery/EN ISO 11393 (FS core), Chapter 8 / National
  Highways / sector scheme (HM core), food-hygiene/BRCGS, SIA/body-armour,
  COSHH/tabard, RCV/refuse, solar/EV/heat-pump, Ofsted/CQC, gym/tracksuit.
  **ALLOW** DC's own vocab: hi-vis, EN ISO 20471, multi-drop, last-mile, parcel,
  owner-driver, courier, depot. (FS's lesson: do NOT put your core words in the
  BLEED list.)
- lead trio present (`LEAD`/`CO_LEAD`/`TRI_LEAD`)
- nearby links point only to slugs on the CSV (no dead links)

Must read `==== N/N pages passed all hard checks ====`.

**`score_dc.py` (dup). Binding number = worst-pair ≤ 52.0%.**
- 5-gram shingle Jaccard, strips JSON-LD/SVG/footer + the chrome divs.
- `MAX_PAIR = 52.0%` is the real guard and passes comfortably with md5.
- `FLOOR = 77.0%` overall-unique is **secondary and structurally unreachable at
  this scale** (~66–67% with a heavy shared product scaffold). Do NOT chase it.
  Report it honestly; it is not a gate. (FS shipped at 66.8% overall / 51.9%
  worst-pair and that is the expected shape.)

**`diag_dc.py outputs <a>.html <b>.html`** — subtracts a control page's shingles
to isolate the pair-specific overlap and prints "~N researched words to add to
the weaker page." Use it on any over-cap pair.

---

## 4. Session workflow (the proven loop)

1. Recreate kit; ensure `dc-london.html` + `DC_towns.csv` sit beside `dc_build.py`.
2. **Patch the hash bug** (§0) before anything else.
3. Build in **batches of 30 towns**, population-rank order, skipping London
   (London = the flagship, added LAST). Per batch:
   1. Pull the next 30 unbuilt towns from the CSV (exclude anything already in
      `TOWNS`, exclude London).
   2. **Pick 3 nearby per town and VALIDATE every candidate against the CSV
      before launching research** (see §5 — this is the #1 time-sink).
   3. Launch **6 background `general-purpose` agents × 5 towns** (the IoW/Cornwall
      clusters: put close-together towns in one agent and tell it to differentiate
      hard). Each agent reads a shared `PROMPT_TEMPLATE.md`, does its OWN web
      searches, NEVER authors from memory, returns a Python `NEW = {...}` dict.
   4. When all 6 return: validate (ASCII-only, no inner `"`, 4 paras, nearby==fixed
      list), splice into `TOWNS`, build, `verify_dc.py outputs` (must be N/N),
      `score_dc.py outputs`.
   5. **Diag-enrich** any over-cap pair (§6), rebuild, re-score.
   6. Commit + push the batch.
4. After all 504 town pages: **copy the flagship `dc-london.html` into `outputs/`**
   (do not rebuild it), verify 505/505, final score, commit.
5. Zip `outputs/*.html` (the 505 pages) + a kit zip; deliver via SendUserFile.

**Cadence that worked:** ~30 towns/batch, 17 batches to clear 505. Research
agents run ~3 min each, 6 in parallel. Splice via a per-batch sed'd copy of the
splice script (§7).

---

## 5. Nearby validation — the biggest time sink, do it up front

`require_nearby()` HARD-FAILS on any nearby town not on the CSV, and verify
fails on dead internal links. **Many obvious neighbours are NOT on the 505-row
CSV** (it's population-ranked, so smaller adjacent towns are absent). On FS,
roughly half my first-guess neighbours per batch failed validation.

**Always run this BEFORE launching research agents:**

```python
import csv, json
rows = list(csv.DictReader(open('DC_towns.csv', encoding='utf-8-sig')))
onCSV = {(r.get('Town') or r.get('town')).strip() for r in rows}
prop = { "TownA": ["Near1","Near2","Near3"], ... }   # your 30 with 3 each
bad = False
for t, ns in prop.items():
    if t not in onCSV: print("TOWN NOT ON CSV:", repr(t)); bad = True
    if len(set(ns)) != 3: print("nearby dup/count:", t); bad = True
    for n in ns:
        if n not in onCSV: print(f"  {t}: '{n}' NOT on CSV"); bad = True
print("ALL OK" if not bad else "FIX NEEDED")
if not bad: json.dump(prop, open('batchNN_nearby.json','w'))
```

For failures, search the CSV for valid regional substitutes:
```python
towns = sorted((r.get('Town') or r.get('town')).strip() for r in rows)
def near(*subs): return [t for t in towns if any(s.lower() in t.lower() for s in subs)]
print(near('Winsford','Middlewich','Knutsford'))   # find what IS on the CSV
```
For remote towns (Elgin, IoW, far-Cornwall, far-Cumbria) you sometimes have only
2 genuinely-close CSV towns; use the nearest regional city as the 3rd. That's
fine — the only hard rule is "on the CSV."

**Exact-string traps:** the CSV's spelling is law. Watch e.g.
`Newport (Isle of Wight)` (full parenthetical), `Houghton le Spring` (no
hyphens), `Hull` (not "Kingston upon Hull"), `Kingston upon Thames`. Whatever
string the CSV uses is what must appear in the `nearby` list verbatim.

---

## 6. Dup-enrichment loop (clearing an over-cap pair)

Worst-pair creeps toward the 52% cap as N grows and you'll hit it occasionally
(FS hit it most batches near the end; one final pair needed two passes). Fix:

1. `python3 diag_dc.py outputs dc-<a>.html dc-<b>.html` → it names the **weaker
   page** and ~N words to add.
2. **Web-verify NEW local proper nouns** for that town (named depots/industrial
   estates/business parks/road corridors for DC), then expand that town's
   `s1loc` in `dc_build.py` — real specifics, NOT generic reword (SPEC 8.3).
3. Rebuild, re-score. If still marginal (52.x%), enrich the OTHER page of the
   pair too — attacking both sides drops the Jaccard fastest (that's how the
   final FS pair Hindley/Neston went 56.6 → 53.8 → 52.2 → clear).
4. A few proper-noun-rich sentences ≈ 50–60 unique shingles ≈ ~1.5pp off the
   pair. Budget accordingly.

When you must edit `dc_build.py` after a Bash grep: **Read the exact line first**
— a grep does not satisfy the Edit tool's "must Read before Edit" and the edit
will fail on a stale match.

---

## 7. TOWNS schema + splice mechanics

Each `TOWNS` entry (authored by the research agents, keyed by **lowercased** town
name — including any parenthetical, e.g. `"newport (isle of wight)"`):

```python
"leeds": {
  "region": "Leeds and West Yorkshire",
  "nearby": ["Bradford", "Pudsey", "Dewsbury"],   # exactly 3, all on CSV
  "snapshot": "...one sentence, fixed opener/closer...",
  "s1_head": "short region-flavoured headline",
  "s1loc": ["para1", "para2", "para3", "para4"],   # exactly 4, the P1–P4 arc
  "kit_loc": "short phrase",
  "s2_intro": "Whether you ... across {Town}'s {real features}"   # NO trailing punctuation
}
```

The P1–P4 arc (adapt the beats to courier work, not tree work): P1 local
character + community of mostly owner-driver/small-firm couriers dependent on the
kit; P2 local geography — NAME real distribution parks, industrial estates,
depots, road corridors, last-mile zones; P3 the trade run to standards
(EN ISO 20471 hi-vis etc.) + a real local logistics anchor; P4 firms mostly small
— owner-driver, man-and-van, two-van outfit on a NAMED local patch. **Vary the P1
and P4 opening sentence structure** so they're not verbatim across towns (a key
uniqueness lever).

**Splice script** (per batch, sed the previous one to repoint the research
files). It: loads the 6 `research_bNNg{i}.py` dicts, asserts ASCII / no inner
`"` / 4 paras / 3 nearby, serializes each with `json.dumps(s,
ensure_ascii=False)` for double-quoted values, and inserts before the marker
`"\n}\n\n# === CSV / nearby"` in `dc_build.py`. Keep a `splice_batch1.py` and do
`sed 's|research_b1g{i}|research_bNNg{i}|' ...` each batch. The last batch had 22
towns / 5 groups → also sed `range(1, 7)` → `range(1, 6)`.

---

## 8. PROMPT_TEMPLATE.md for the research agents

Shared brief every agent reads first. Must contain: a gold-standard reference
entry (use a built early DC town once you have one; until then adapt Leeds), the
verbatim snapshot opener/closer, the field rules, and HARD CONSTRAINTS:
- **ASCII only** (transliterate accents, no curly quotes/dashes).
- **No `"` inside any string value** (apostrophes fine).
- Agents do their **own** web searches; never author from memory; every local
  claim web-verified; real proper nouns are the whole point.
- Correct national bodies where prose needs them (Wales: NRW; Scotland: relevant
  Scottish bodies) — though DC leans on logistics anchors more than nature bodies.
- Keep the self-checkout / owner-driver voice; no procurement-framework framing.
- EXCLUDE the other series' vocab (the BLEED list from §3).
- VARY P1/P4 openings.

Agent invocation that worked: `general-purpose`, `run_in_background: true`, 5
towns each, fixed nearby allow-list passed in the prompt, plus a one-line local
hint per town (parks/estates → for DC: distribution parks, depots, road network,
business parks). Save to `research_bNNg{i}.py` AND return the dict as the final
message (belt-and-braces — the file is the source of truth for splicing).

---

## 9. Pitfalls carried over (don't relearn these)

- **CRC32 → md5** (§0). The big one.
- **ORG_BLOCK must be wrapped in its `<script type="application/ld+json">` tag** —
  verify enforces exactly 4 JSON-LD blocks; an unwrapped Org block fails it.
- **Clone rename**: `s/score_fs/score_dc/; s/diag_fs/diag_dc/` after the bulk
  `fs_`→`dc_` (module-name imports, not just filenames).
- **Don't BLEED your own core vocab** — keep hi-vis / EN ISO 20471 / multi-drop /
  courier / last-mile OUT of the BLEED list; they're DC's signature.
- **Delivery-claim regex**: DC's trade IS delivery — make sure the gate bans only
  *our* shipping promises, not the courier's work. Test it on real DC prose.
- **`__pycache__`**: add `.gitignore` (`__pycache__/`, `*.pyc`) early; don't
  commit it.
- **Nearby off-CSV** (§5) — validate up front, every batch.
- **Edit after grep** needs a real Read first (§6).
- **Overall-unique ~66%** is the structural ceiling at this scale; the **52% pair
  cap** is the binding guard. Present the score honestly; don't chase 77%.
- **London is the flagship AND the London page** — never rebuild it; copy it into
  `outputs/` at the very end so the deliverable is 505/505.

---

## 10. Standing instruction

Hard checks (`verify_dc`) are the binding gate. The 52% pair cap is the binding
uniqueness guard. Present the overall-unique score honestly as a diagnostic.
Never rebuild the flagship; only ADD pages. Build in 30-town batches,
research-first, web-verified, commit each batch. Recreate the kit from these
files each session — the filesystem resets.

— Handover written at the close of the FS build (505/505 green: verify 505/505,
worst pair 51.9%, 0 over-cap).
