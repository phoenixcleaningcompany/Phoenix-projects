# RT (Supermarkets & Retail) build — handover

Carries forward everything proven on the **DC (Delivery & Courier)** build (505
pages, all gates green: verify 505/505, worst pair 51.9%, 0 over-cap). RT is the
**same machine, new vocabulary**: 505 location pages, one per UK town, page
prefix `rt-`, canonical/og to `https://www.ineedworkwear.uk/rt-<slug>.html`.

DC itself was cloned from FS (Forestry) which was cloned from HM. Same lineage,
same scripts, same workflow. Read this, then **SPEC.md and the new CLAUDE.md**
for the RT-specific vocabulary/posture. The filesystem resets between sessions —
recreate the kit from the shipped files.

---

## 0. THE ONE BUG YOU MUST NOT REINHERIT (read this twice)

Every `_build.py` in this family was cloned down the chain, and the variant
selector `pick(key, salt, n)` historically used a **CRC32 checksum**:

```python
def pick(key, salt, n):
    return zlib.crc32((salt + '|' + str(key).lower()).encode()) % n   # BROKEN
```

CRC32 is a checksum, not a hash — its low-order bits (the only ones `% n` reads)
stay correlated with the input. Structurally similar keys (e.g. all 7-letter
town names) collide on the **same index in every pool at once**, so whole pages
come out near-identical and the worst-pair score explodes.

**The fix — port it verbatim:**

```python
import hashlib

def pick(key, salt, n):
    # md5 digest gives well-distributed bits; crc32 % n leaks correlated low
    # bits (e.g. all 7-letter town names collided on the same pool variant).
    h = hashlib.md5((salt + '|' + str(key).lower()).encode()).digest()
    return int.from_bytes(h[:4], 'big') % n
```

Keep the exact `salt + '|' + key` composition; only the bit-mixing changes.
md5 is fine — this is a distribution problem, not security.

**First thing in the RT session:** `grep -n crc32 rt_build.py`. If it's there,
patch it before building a single page. Also remove the now-unused `zlib` import
and add `hashlib`.

---

## 0b. THREE MORE FIXES THAT WERE NEEDED ON DC (check all of them)

1. **Clone-rename of the scorer import.** `diag_dc.py` imported `scodc_re`
   (a stale name) instead of `score_dc`; it crashed on import. After the bulk
   `fs_`→`rt_` rename, **also** do `s/score_fs/score_rt/; s/diag_fs/diag_rt/`
   and grep the diag script for its `import score_xx as S` line. Run
   `python3 diag_rt.py outputs/<a>.html outputs/<b>.html` once early to prove it
   imports.

2. **Hardcoded output dir.** `rt_build.py`'s `main()` will likely hardcode
   `outdir = '/mnt/user-data/outputs'`, which doesn't exist in a fresh sandbox.
   Make it fall back to a local dir:
   ```python
   outdir = os.environ.get('RT_OUTDIR') or ('/mnt/user-data/outputs'
            if os.path.isdir('/mnt/user-data/outputs') else 'outputs')
   os.makedirs(outdir, exist_ok=True)
   ```

3. **Display-name casing from the CSV.** `main()` derives the town display name
   with `' '.join(w.capitalize() for w in tk.split())`, which mangles
   hyphenated/multiword towns: `stoke-on-trent` → "Stoke-on-trent",
   `newcastle upon tyne` → "Newcastle Upon Tyne". Fix by resolving the display
   name from the CSV's exact spelling (verify keys off the CSV town, so this is
   strictly safer):
   ```python
   disp = {r[1].lower(): r[1] for r in _load_csv()}   # r[1] = Town column
   ...
   town = disp.get(tk, ' '.join(w.capitalize() for w in tk.split()))
   ```

---

## 1. What RT is (CONFIRM against the real SPEC before coding the gate)

RT = workwear for **supermarket / convenience / retail** staff. Likely buyers:
store/shop-floor teams, checkout/till, stockroom/warehouse, click-and-collect
and home-delivery pickers, café/deli/bakery counters. Confirm the **hybrid A/B
posture** in SPEC — DC gave equal billing to a fleet **trade account** and an
**owner-driver ordering direct online**; RT's two routes are probably a
**multi-store/head-office trade account** vs an **independent shop / single
store ordering direct**. Keep both routes co-equal; do not let it drift to pure
concierge or pure self-checkout.

**Set these in `verify_rt.py` from the real SPEC — DO NOT guess:**
- `LEAD` / `CO_LEAD` / `TRI_LEAD` — the three lead products. (DC was
  polo / hi-vis / softshell. RT will differ — likely **polo / tabard or apron /
  fleece or sweatshift**, but confirm.) verify hard-fails if any lead word is
  absent from a page, so the prose pools must use all three naturally.
- The **distinctive vocabulary spine** (DC's was "branded all-weather courier
  identity / EN ISO 20471 hi-vis"). RT's is the thing that makes pages read
  specific — branded retail uniform / store identity / customer-facing.
- The **BLEED list** — bans OTHER series' core vocab so series stay separated.
  Carry over the bans for FS (chainsaw/EN ISO 11393/arborist), HM (Chapter 8/
  National Highways/sector scheme), DC if it's a separate live series
  (courier/multidrop/owner-driver — but ONLY if SPEC says to separate them),
  plus security/cleaning/care/sports bleed. **CRITICAL LESSON: never put RT's
  OWN core words in the BLEED list.** On FS the build initially banned its own
  vocab and every page failed. Whatever RT's lead/spine words are
  (tabard, apron, till, checkout, retail, etc.), keep them OUT of BLEED.
- **Delivery-timescale regex (check 9):** it bans *our* shipping promises
  ("next-day delivery", "deliver within N"). For RT this is unlikely to clash,
  but if any RT prose talks about the store's own home-delivery/click-and-collect,
  re-read the regex so legitimate retail prose doesn't trip it. (On DC, which is
  literally about delivery, we kept prose to "standard lead times" and avoided
  "same-day **delivery**" — "same-day firms" was fine, "same-day delivery"
  would have tripped it.)

**Nearby = geographic** (3 close towns, all on the CSV). 14 `.com` links + 1
community link per page. 4 JSON-LD blocks (FAQ + Org + Service + Breadcrumb).

---

## 2. The kit (recreate beside `rt_build.py`)

| File | Role |
|---|---|
| `rt_build.py` | generator: reads flagship `rt-london.html`, extracts shared chrome via `between()`/`aria_block()` markers, assembles each town from **md5**-hashed prose pools + inline `TOWNS` dict |
| `rt-london.html` | flagship base template AND the London page — **never rebuild it**, only add other pages; copy it into `outputs/` at the very end |
| `RT_towns.csv` | `Rank, Town, Population, Nation` — population-ranked, 505 rows. (DC's CSV had the same 505 towns; RT's may be identical — confirm.) |
| `verify_rt.py` | **hard gate** — the binding pass/fail |
| `score_rt.py` | dup scorer (diagnostic + the 52% pair cap) |
| `diag_rt.py` | over-cap-pair diagnostic → names the weaker page + ~N words to add |
| `PROMPT_TEMPLATE.md` | shared brief every research agent reads (see §8) |
| `splice_batchNN.py` | per-batch splicer (see §7) |

---

## 3. The gates

**`verify_rt.py` (HARD — the only binding gate). Per page:**
- exactly **14** `ineedworkwear.com` links + exactly **1** community link
- **4** JSON-LD blocks (`script type="application/ld+json"`) — FAQ+Org+Service+Breadcrumb
- no JavaScript (script tag / `javascript:` / `on*=`), no HTML entities
- meta description present, ≤160 chars, **unique** across the set
- town in `<title>` and `<h1>`; unique title; filename slug matches
- no banned delivery-timescale claims (see §1)
- **BLEED list** clean (other series' vocab only — never RT's own)
- lead trio present (`LEAD`/`CO_LEAD`/`TRI_LEAD`)
- nearby/internal links point only to slugs on the CSV (no dead links)

Must read `==== N/N pages passed all hard checks ====`.

**`score_rt.py` (dup). Binding number = worst-pair ≤ 52.0%.**
- 5-gram shingle Jaccard; strips chrome/SVG/JSON-LD/footer + the heavily-pooled
  chrome divs; masks only the town name so pages compare on editorial substance.
- `MAX_PAIR = 52.0%` is the real guard and passes with md5 + the workflow below.
- `FLOOR = 77.0%` overall-unique is **secondary and structurally unreachable at
  this scale** (~66-68% with a heavy shared product scaffold). DO NOT chase it.
  Report it honestly; it is not a gate. (FS shipped 66.8%, DC 68.1% overall —
  that is the expected shape.)

**`diag_rt.py outputs <a>.html <b>.html`** — subtracts a control page's shingles
to isolate the pair-specific overlap and prints "~N researched words to add to
the weaker page." Use it on any over-cap pair (§6).

---

## 4. Session workflow (the proven loop — 30-town batches)

1. Recreate the kit; ensure `rt-london.html` + `RT_towns.csv` sit beside `rt_build.py`.
2. **Patch the hash bug (§0) and the three fixes (§0b)** before building anything.
   Build the 1-2 in-dict sample towns, copy the flagship into `outputs/`, run
   `verify_rt.py outputs` (expect N/N) and `score_rt.py outputs` to confirm the
   kit works end to end. Commit the patched kit.
3. Build in **batches of 30 towns**, population-rank order, **skipping London**
   (London = flagship, added LAST). Per batch:
   1. Pull the next 30 unbuilt towns from the CSV (exclude anything in `TOWNS`).
   2. **Pick 3 nearby per town and VALIDATE every candidate against the CSV
      BEFORE launching research** (§5 — this is the #1 time-sink and #1 failure).
   3. Launch **6 background `general-purpose` agents x 5 towns** (last batch is
      22 towns / 5 groups). Each reads `PROMPT_TEMPLATE.md`, does its OWN web
      searches, NEVER authors from memory, writes `research_bNNg{i}.py` as
      `NEW = {...}`, and returns **only a one-line confirmation** (NOT the dict —
      that bloats your context across 17 batches; the file is the source of truth).
   4. When all return: run the splicer (validates + inserts), build, copy the
      flagship into `outputs/`, `verify_rt.py outputs` (must be N/N),
      `score_rt.py outputs`.
   5. **Diag-enrich** any over-cap pair (§6); rebuild those towns; re-score.
   6. Commit + push the batch.
4. After all 504 town pages: confirm `rt-london.html` is in `outputs/` (copied,
   never rebuilt). Final `verify_rt.py outputs` = 505/505, final score.
5. Zip `outputs/*.html` (505 pages) + a kit zip; deliver via SendUserFile.

**Cadence that worked on DC:** ~30 towns/batch, 17 batches (16x30 + 1x22).
Six research agents ~2-3 min each, run in parallel; you get a notification per
agent. Commit each batch so progress survives context resets.

---

## 5. Nearby validation — the biggest time sink, do it UP FRONT

`require_nearby()` HARD-FAILS any nearby town not on the CSV, and verify fails on
dead internal links. **Many obvious neighbours are NOT on the 505-row CSV** (it's
population-ranked, so smaller adjacent towns are absent). On DC roughly a third
of first-guess neighbours per batch weren't on the CSV.

**Always run this BEFORE launching research agents** (took DC to 0 nearby
failures across all 17 batches):

```python
import csv, json
rows = list(csv.DictReader(open('RT_towns.csv', encoding='utf-8-sig')))
onCSV = {(r.get('Town') or r.get('town')).strip() for r in rows}
prop = { "TownA": ["Near1","Near2","Near3"], ... }   # your 30, 3 each
bad = False
for t, ns in prop.items():
    if t not in onCSV: print("TOWN NOT ON CSV:", repr(t)); bad = True
    if len(set(ns)) != 3: print("nearby dup/count:", t); bad = True
    for n in ns:
        if n not in onCSV: print(f"  {t}: '{n}' NOT on CSV"); bad = True
print("ALL OK" if not bad else "FIX NEEDED")
if not bad: json.dump(prop, open('batchNN_nearby.json','w'))
```

**Exact-string traps (the CSV spelling is law — these bit us on DC):**
`Newport (Isle of Wight)` (full parenthetical), `Houghton le Spring` (no
hyphens), `Bishop's Stortford` (apostrophe), `Weston-super-Mare`,
`Stockton-on-Tees`, `Newcastle-under-Lyme`, `Newcastle upon Tyne`,
`Kingston upon Thames`, `Welwyn Garden City`, `Hull` (not "Kingston upon Hull"),
`Stratford-upon-Avon`, `Ashton-under-Lyne`, `Grays Thurrock`. Whatever string the
CSV uses must appear in the `nearby` list verbatim.

For remote towns (Aberdeen, Inverness, Elgin, far Cornwall/Cumbria, Norwich,
Cambridge, Isle of Wight) you sometimes have only 1-2 genuinely-close CSV towns;
use the nearest regional city/cities as the rest. That's fine — the only hard
rule is "on the CSV."

---

## 5b. TOWN-KEY / SLUG EDGE CASES (these caused real verify failures on DC)

The TOWNS key must be the **lowercased exact CSV spelling**, because the build's
display lookup and slug both derive from it. Three towns broke on DC because the
research agent dropped a character from the key:

- **Apostrophe:** key must be `"bishop's stortford"` (not `"bishops stortford"`).
  Wrong key → slug `bishops-stortford`, but other towns link to
  `bishop-s-stortford.html` (slugify turns `'` into `-`) → dead link + title-check
  failure.
- **Space vs hyphen:** key must be `"potters bar"` (not `"potters-bar"`).
- **Parenthetical:** key must be `"newport (isle of wight)"` (full), which
  slugifies to `newport-isle-of-wight`.

**Mitigation:** after agents return, before splicing, assert every key is in the
CSV's lowercased set; if not, fix the key string. The splicer can do this check
(see §7). The slugify rule is: lowercase, `&`→`and`, every run of non-alnum →
single `-`, strip leading/trailing `-`.

---

## 6. Dup-enrichment loop (clearing an over-cap pair)

Worst-pair creeps toward the 52% cap as N grows; you'll hit it occasionally (DC
hit it in ~4 of 17 batches). Fix:

1. `python3 diag_rt.py outputs/rt-<a>.html outputs/rt-<b>.html` → it names the
   **weaker page** and ~N words to add.
2. **Web-verify NEW local proper nouns** for that town (named retail/business
   parks, industrial estates, high streets, shopping centres, store clusters,
   road corridors, postcodes) and expand that town's `s1loc` in `rt_build.py` —
   real specifics, NOT generic reword (SPEC 8.3).
3. **The efficient move learned on DC: add ONE solid ~70-90-word proper-noun-rich
   sentence to the weaker page** rather than nibbling. That drops a pair ~2-2.5pp.
   ~50-60 unique shingles ≈ ~1.5pp. A 59% pair needs ~250 unique words total to
   clear — budget accordingly.
4. If still over after enriching the weaker page (a "sticky" pair sharing many
   pooled-section variants), **enrich BOTH pages of the pair** — attacking both
   sides drops the Jaccard fastest. On DC the worst case (Enfield/Lichfield 59%)
   took ~3 rounds across both pages to clear; most took one.

**When editing `rt_build.py` after a Bash grep:** the Edit tool requires a real
**Read** of the exact line first (a grep does not satisfy it, and the file may
have changed since). Read the line, then Edit.

---

## 6b. THE BIGGEST UNIQUENESS LEVER (do this from batch 1, not after pain)

The pooled scaffold sections (the "your X is your brand" block, the ordering
block, the "why choose" block, the FAQ) are scored and have only 3-6 variants
each. Two towns that hash to the same variants across several pools start at a
high baseline similarity; an unlucky extra collision tips them over 52%. The
single most effective preventative — added on DC from batch 11 and it cut new
over-cap pairs to ~zero — is to instruct every research agent:

> **Vary the Para-2 (operator/staff-mix) opening and sentence structure town to
> town. Do NOT reuse the stock phrasing verbatim** (on DC: "National carriers run
> parcel depots ... a dense layer of independent ..."). Describe the mix in
> genuinely different words for each town.

Also: **VARY the Para-1 opening sentence structure** (mix "Set on...",
"{Town} is...", "On the {road}...", "A major {x} centre, {Town}...") and vary the
recurring closing beat. Use this from the FIRST batch.

---

## 6c. CLUSTER DIFFERENTIATION

When a batch contains a tight geographic cluster (on DC: Black Country —
Bilston/Sedgley/Tipton/Willenhall/Bloxwich/Kingswinford; Cornwall —
Newquay/Truro/Falmouth/Camborne; Wirral — Neston/Bromborough/Heswall; Isle of
Wight — Newport/Ryde/Cowes/Shanklin/Sandown), put the cluster in ONE research
agent's group and tell it explicitly to **differentiate hard using each town's
OWN distinct estates, roads, centres and postcodes** so the pages don't read
alike. This prevented cluster over-cap pairs on DC.

---

## 7. TOWNS schema + splice mechanics

DC was a **Low-local-variation** series: each town's `s1loc` held ONLY its
**2 genuinely-local paragraphs**; the generic shared paragraphs came from POOLS
appended by `s1_paras()`. **Confirm RT's variation level in SPEC** — it may be 2
local paras (like DC) or 4 (like FS). Match whatever the existing `TOWNS`
sample entries (London + the 1-2 seed towns) use; never paste generic pool prose
into `s1loc`.

Each `TOWNS` entry (keyed by **lowercased exact CSV town name**):

```python
"leeds": {
  "region": "Leeds and West Yorkshire",
  "nearby": ["Bradford", "Pudsey", "Dewsbury"],   # exactly 3, all on CSV
  "snapshot": "...one sentence, fixed opener/closer from SPEC...",
  "s1_head": "short region-flavoured headline (must differ across towns)",
  "s1loc": ["para1 (local geography)", "para2 (operator/staff mix)"],  # DC=2
  "kit_loc": "short phrase slotted into a pool sentence",
  "s2_intro": "Whether you ... across {Town}'s {real features}"  # NO trailing punctuation
}
```

**Splice script** (per batch; sed the previous one to repoint the research
files). It must:
- load the 6 `research_bNNg{i}.py` dicts (each defines `NEW = {...}`), merging;
- **validate** every entry: required fields present; `nearby` is 3 unique, all on
  CSV; `s1loc` is exactly the right paragraph count; **ASCII only**; **no inner
  `"`**; **no `&`, `<`, `>`** (these break verify's entity/JS checks); key equals
  its lowercased CSV spelling (§5b); `s2_intro` has no trailing punctuation;
- serialize each entry with `json.dumps(entry, ensure_ascii=False)` (valid Python
  since no inner double-quotes), one town per line, indented one space;
- insert before the TOWNS-closing brace by replacing the marker
  `"\n}\n\n# === CSV / nearby"` with `"\n" + block + "}\n\n# === CSV / nearby"`;
- skip keys already present (idempotent re-runs).

Keep `splice_batch1.py` and per batch do
`sed 's|b1|bNN|g' splice_batch1.py > splice_batchNN.py`. The **last batch had 22
towns / 5 groups**, so also sed `range(1, 7)` → `range(1, 6)`. (Watch the sed:
`s|b1|bNN|g` also rewrites the literal `b1` in comments — harmless.)

The DC splicer's validation block (ASCII / no `"` / no `&<>` / 2 paras / 3
nearby-on-CSV / no trailing punctuation) is in the delivered DC kit zip —
clone `splice_batch1.py` from it and rename `b1`→`bNN`, `DC_towns`→`RT_towns`.

---

## 8. PROMPT_TEMPLATE.md for the research agents

Shared brief every agent reads first. Must contain: a gold-standard reference
entry (use a built early RT town once you have one; until then adapt the SPEC's
sample), the verbatim snapshot opener/closer, the field rules, and HARD
CONSTRAINTS:
- **ASCII only** (transliterate accents; straight `'` and `-`; **no `&`** — write
  "and"; **no `<`/`>`**; no curly quotes/dashes).
- **No `"` inside any string value** (apostrophes fine).
- **s1loc = exactly N paragraphs** (N from SPEC; DC was 2), local content only —
  do NOT write the generic pool prose; the generator adds it.
- Agents do their **own** web searches; never author from memory; every local
  claim web-verified; real proper nouns (retail/business parks, shopping centres,
  high streets, industrial estates, store clusters, road corridors, postcodes)
  are the whole point.
- Correct national bodies where prose needs them (Wales: Natural Resources Wales;
  Scotland: relevant Scottish bodies) — though RT leans on retail/town-centre
  anchors more than nature bodies.
- Keep the hybrid posture from SPEC; don't drift to one route.
- EXCLUDE the other series' vocab (the BLEED list from §3).
- **VARY Para-1 and Para-2 openings** (§6b); for clusters, differentiate hard (§6c).
- **Write the result to `research_bNNg{i}.py` as `NEW = {...}` AND return only a
  one-line confirmation** (5 keys + s1loc word counts) — do NOT paste the dict.

Agent invocation that worked: `general-purpose`, `run_in_background: true`, 5
towns each, fixed validated nearby allow-list passed in the prompt, plus a
one-line local hint per town (real retail/estate/road anchors to verify+expand).

---

## 9. Pitfalls carried over (don't relearn these)

- **CRC32 → md5** (§0). The big one.
- **Clone-rename of the diag import** + outdir + display-casing (§0b).
- **ORG_BLOCK must be wrapped in its `<script type="application/ld+json">` tag** —
  verify enforces exactly 4 JSON-LD blocks; an unwrapped Org block fails it.
- **Don't BLEED your own core vocab** — keep RT's lead/spine words OUT of the
  BLEED list (the FS lesson).
- **Delivery-claim regex** — re-read it against real RT prose if RT mentions the
  store's own delivery/click-and-collect.
- **Town-key/slug edge cases** — apostrophes, spaces, parentheticals (§5b).
- **`&`/`<`/`>` in values** break verify (HTML-entity/JS checks) — splicer rejects
  them; tell agents to write "and" and avoid markup. (An agent rewrote "B&Q" as
  "B and Q" correctly once reminded.)
- **Nearby off-CSV** (§5) — validate up front, every batch.
- **Edit after grep** needs a real Read first (§6).
- **`__pycache__` / `dist/`** — add `.gitignore` (`__pycache__/`, `*.pyc`,
  `dist/`) early; don't commit caches or the deliverable zips.
- **Overall-unique ~66-68%** is the structural ceiling at this scale; the **52%
  pair cap** is the binding guard. Present the score honestly; don't chase 77%.
- **London is the flagship AND the London page** — never rebuild it; copy it into
  `outputs/` at the very end so the deliverable is 505/505.

---

## 10. Standing instruction

Hard checks (`verify_rt`) are the binding gate. The 52% pair cap is the binding
uniqueness guard. Present the overall-unique score honestly as a diagnostic;
don't chase the 77% floor. Never rebuild the flagship; only ADD pages. Build in
30-town batches, research-first, web-verified, nearby-validated up front, vary
Para-1/Para-2 from batch 1, commit each batch. Recreate the kit from the shipped
files each session — the filesystem resets.

— Handover written at the close of the DC build (505/505 green: verify 505/505,
worst pair 51.9%, 0 over-cap, overall-unique 68.1%).
