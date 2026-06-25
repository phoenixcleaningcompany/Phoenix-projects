# BH (Beauty, Hair & Spa) build — handover

Carries forward everything proven on the **RT (Supermarkets & Retail)** build
(505 pages, all gates green: **verify 505/505, worst pair 51.9%, 0 over-cap,
overall-unique 67.6%**). BH is the **same machine, new vocabulary**: 505 location
pages, one per UK town, page prefix `bh-`, canonical/og to
`https://www.ineedworkwear.uk/bh-<slug>.html`.

RT was cloned from DC (Delivery & Courier), which came from FS (Forestry) from HM.
Same lineage, same scripts, same workflow. Read this, then **the BH SPEC.md and
CLAUDE.md** for the BH-specific vocabulary/posture. The filesystem resets between
sessions — recreate the kit from the shipped files.

> The fastest start: take the **RT kit zip** delivered at the end of the RT build,
> rename `rt_`→`bh_` / `RT_`→`BH_` across filenames and code, drop in the BH
> flagship `bh-london.html` + `BH_towns.csv`, set the BH lead/BLEED words in
> `verify_bh.py` from the BH SPEC, and run the §0/§0b checks below before building.

---

## 0. THE ONE BUG YOU MUST NOT REINHERIT (read twice)

The variant selector `pick(key, salt, n)` historically used **CRC32**:

```python
def pick(key, salt, n):
    return zlib.crc32((salt + '|' + str(key).lower()).encode()) % n   # BROKEN
```

CRC32 is a checksum, not a hash — `% n` reads only its low-order bits, which stay
correlated with the input. Structurally similar keys (e.g. all 7-letter town
names) collide on the **same pool index at once**, so whole pages come out
near-identical and the worst-pair score explodes.

**The fix — port verbatim:**

```python
import hashlib
def pick(key, salt, n):
    # md5 gives well-distributed bits; crc32 % n leaks correlated low bits
    # (e.g. all same-length town names collided on the same pool variant).
    h = hashlib.md5((salt + '|' + str(key).lower()).encode()).digest()
    return int.from_bytes(h[:4], 'big') % n
```

Keep the exact `salt + '|' + key` composition; only the bit-mixing changes. md5 is
fine — this is distribution, not security.

**First thing in the BH session:** `grep -n crc32 bh_build.py`. If present, patch
before building a single page; remove the now-unused `zlib` import, add `hashlib`.
*(On RT this was already fixed in the shipped kit — but check anyway.)*

---

## 0b. THREE CLONE-RENAME FIXES (RT still shipped with all three — check BH)

1. **Scorer import in the diag script.** `diag_rt.py` imported `scort_re` (a
   typo'd stale name) instead of `score_rt` — an **ImportError on startup**. After
   the bulk `rt_`→`bh_` rename, grep the diag script for its `import score_xx as S`
   line and fix it to `import score_bh as S`. Prove it: run
   `python3 diag_bh.py outputs/bh-<a>.html outputs/bh-<b>.html` once early.

2. **Hardcoded output dir.** `bh_build.py`'s `main()` will hardcode
   `outdir = '/mnt/user-data/outputs'`, which doesn't exist in a fresh sandbox.
   Make it fall back to a local dir:
   ```python
   outdir = os.environ.get('BH_OUTDIR') or ('/mnt/user-data/outputs'
            if os.path.isdir('/mnt/user-data/outputs') else 'outputs')
   os.makedirs(outdir, exist_ok=True)
   ```

3. **Display-name casing from the CSV.** `main()` derives the town display name
   with `' '.join(w.capitalize() for w in tk.split())`, which mangles
   hyphenated/multiword towns: `stoke-on-trent` → "Stoke-on-trent",
   `newcastle upon tyne` → "Newcastle Upon Tyne". Resolve it from the CSV's exact
   spelling instead (verify keys off the CSV town, so this is strictly safer):
   ```python
   disp = {r[1].lower(): r[1] for r in _load_csv()}   # r[1] = Town column
   ...
   town = disp.get(tk, ' '.join(w.capitalize() for w in tk.split()))
   ```

---

## 0c. TWO PIECES THE KIT DOESN'T SHIP — YOU MUST BUILD THEM (RT lesson)

The RT kit referenced `PROMPT_TEMPLATE.md` and a splicer but **did not ship
them**. They are in the **RT kit zip** now — clone and adapt. You also want the
two helpers I added on RT, which made the 505-page run resume-safe and cheap:

| File | Role | Status |
|---|---|---|
| `PROMPT_TEMPLATE.md` | the shared brief every research agent reads first (§8) | clone from RT, swap vocabulary |
| `splice_batch.py` | globs `research_*.py`, validates every entry, splices **only valid+new** towns, **non-fatal** on a bad entry | clone from RT |
| `next_towns.py` | prints the next N unbuilt towns (CSV rank order) grouped — **unbuilt = on CSV but not yet a key in `bh_build.TOWNS`**, so git state IS your progress | clone from RT |
| `enrich.py` | reads `enrich.json` (`[{"key","para","text"}]`) and appends a researched sentence to `TOWNS[key]['s1loc'][para]` to clear an over-cap pair | clone from RT |

These four turned the build into a tight loop (see §4). Don't rebuild them from
scratch — port them.

---

## 1. What BH is (CONFIRM against the real BH SPEC before coding the gate)

BH = workwear for **beauty, hair and spa** businesses. Likely buyers: hair
salons, barbershops, beauty salons, nail bars, spas, aesthetics/skin clinics,
tanning and lash/brow studios. Confirm the **posture** in SPEC (RT was Concierge /
Template A — managed-trade-account-led with single-shop direct-online secondary;
BH is probably similar, owner-operator salons + small multi-site groups — but
CONFIRM, do not assume).

**Set these in `verify_bh.py` from the real SPEC — DO NOT guess:**

- `LEAD` / `CO_LEAD` / `TRI_LEAD` — the three lead products. verify **hard-fails**
  if any lead word is absent from a page, so the prose pools must use all three
  naturally. (RT was tabard / polo / fleece. BH will differ — plausibly
  **tunic / apron / trousers** or **tunic / polo / gown**, but CONFIRM from SPEC.)
- The **distinctive vocabulary spine** — the thing that makes BH pages read
  specific (branded salon uniform / client-facing / "your team is your salon's
  first impression"-type angle). RT's was "your staff are your shopfront."
- The **BLEED list** — bans OTHER series' core vocab so series stay separated.
  **CRITICAL LESSON (cost FS a whole failed run, and RT had to remove `tabard`):
  never put BH's OWN core words in BLEED.** Whatever BH's lead/spine words are
  (**tunic, apron, salon, spa, barber, beauty, hair, nail, gown, smock**, etc.),
  keep them OUT of BLEED. In particular **`tunic` is almost certainly BH core** —
  it is blocked as cleaning-series bleed in RT, so it must be **removed from the
  inherited BLEED line** for BH (exactly as RT removed `tabard`). Carry over the
  OTHER series' bans (forestry chainsaw/arborist; highways Chapter 8/National
  Highways; courier multidrop/owner-driver/softshell; food hairnet/BRCGS;
  security SIA/body armour; waste/renewables/etc.) only per what the BH SPEC says
  to separate.
- **Delivery-timescale regex (check 9)** bans *our* shipping promises ("next-day
  delivery", "deliver within N"). Re-read it against real BH prose; keep prose to
  "standard lead times."

**Nearby = geographic** (3 close towns, all on the CSV). **14 `.com` + 1 community
link** per page. **4 JSON-LD blocks** (FAQ + Org + Service + Breadcrumb).

> RT verifier gaps worth fixing in BH while you're in there: (a) the BLEED list
> didn't actually enforce SPEC's courier ban (`multidrop`/`owner-driver`/
> `softshell`) — align list to SPEC; (b) stale clone docstrings (`verify_fs.py`,
> "SE", "no se-*.html files") — fix the script header and the empty-folder error
> message to say `bh-*.html`.

---

## 2. The kit (recreate beside `bh_build.py`)

| File | Role |
|---|---|
| `bh_build.py` | generator: reads flagship `bh-london.html`, extracts shared chrome via `between()`/`aria_block()` markers, assembles each town from **md5**-hashed prose pools + inline `TOWNS` dict |
| `bh-london.html` | flagship base template AND the London page — **never rebuild it**; copy it into `outputs/` at the very end |
| `BH_towns.csv` | `Rank, Town, Population, Nation` — 505 rows. (RT's was identical 505; BH's may match — confirm.) |
| `verify_bh.py` | **hard gate** — the binding pass/fail (16 checks) |
| `score_bh.py` | dup scorer (diagnostic + the 52% pair cap) |
| `diag_bh.py` | over-cap-pair diagnostic → names the weaker page + ~N words to add |
| `PROMPT_TEMPLATE.md` · `splice_batch.py` · `next_towns.py` · `enrich.py` | see §0c |

---

## 3. The gates

**`verify_bh.py` (HARD — the only binding gate). Per page:** exactly **14**
`.com` + **1** community link; **4** JSON-LD blocks; no JavaScript / HTML
entities; meta description present, ≤160, **unique**; town in `<title>` and
`<h1>`; unique title; filename slug matches; no delivery-timescale claims; **BLEED
clean** (other series' vocab only — never BH's own); **lead trio present**; nearby/
internal links only to slugs on the CSV. Must read
`==== N/N pages passed all hard checks ====`.

**`score_bh.py` (dup). Binding number = worst-pair ≤ 52.0%.**
- 5-gram shingle Jaccard; strips chrome/SVG/JSON-LD/footer + pooled chrome divs;
  masks only the town name.
- `MAX_PAIR = 52.0%` is the real guard — passes with md5 + the workflow below.
- `FLOOR = 77.0%` overall-unique is **secondary and structurally unreachable at
  this scale** (~66–68% with a heavy shared product scaffold). DO NOT chase it.
  Report honestly. (FS 66.8%, DC 68.1%, **RT 67.6%** — that is the expected shape.)

---

## 4. Session workflow (the PROVEN loop — what shipped RT, scaled up)

1. Recreate the kit; ensure `bh-london.html` + `BH_towns.csv` sit beside
   `bh_build.py`. Patch §0 + §0b + build the §0c files.
2. Build the 1–2 seed towns already in `TOWNS`, copy the flagship into `outputs/`,
   run `verify_bh.py outputs` (expect N/N) and `score_bh.py outputs`. Commit the
   patched kit. **Do one small sample batch end-to-end first to prove the pipeline
   before scaling** (this is what we did on RT and it caught issues cheaply).
3. Build in **batches of ~48–56 towns**, population-rank order, **skipping
   London** (flagship, added LAST). RT ran **8 background `general-purpose`
   agents × 6–7 towns** per batch — ~10 batches total. Per batch:
   1. `python3 next_towns.py 56 8` → prints REMAINING + 8 groups (round-robin by
      rank so each agent gets a spread).
   2. Launch **8 background agents in one message**. Each reads
      `PROMPT_TEMPLATE.md`, reads `BH_towns.csv`, does its OWN web searches, NEVER
      authors from memory, writes `research_bNNg{i}.py` as `NEW = {...}`, and
      returns **only a one-line confirmation per town** (key + 7 fields + s1loc
      word counts) — NOT the dict (that bloats your context across 10 batches; the
      file is the source of truth).
   3. When all 8 return: `python3 splice_batch.py` (validates + splices valid+new,
      reports any failures), then build all + copy flagship + `verify_bh.py
      outputs` (must be N/N) + `score_bh.py outputs`.
   4. **Diag-enrich** any over-cap pair (§6); rebuild; re-score.
   5. Commit + push the batch (`rt_build.py` equiv + that batch's research files).
4. After all 504 town pages: confirm the flagship is in `outputs/`. Final
   `verify_bh.py outputs` = **505/505**, final score.
5. Zip `outputs/*.html` (505) + a kit zip; deliver via SendUserFile.

**Cadence that worked on RT:** ~56 towns/batch, ~10 batches, 8 agents each ~2–3
min in parallel; a completion notification per agent. **Commit each batch so
progress survives context resets** — and because progress = "towns in TOWNS",
`next_towns.py` always resumes correctly after a reset.

---

## 5. Nearby validation — the SCALED approach (changed from RT's early batches)

`require_nearby()` HARD-FAILS any nearby town not on the CSV, and verify fails on
dead internal links. Hand-picking 3 nearby for 500 towns is infeasible, so on RT
(from batch 2 on) we pushed nearby selection **into the research agents** with a
hard validation gate:

- Give each agent the CSV and instruct: **NEARBY = 3 geographically-closest towns
  that appear VERBATIM in the `Town` column.** Many obvious neighbours are NOT on
  the 505-row CSV (it's population-ranked) — pick the nearest ones that ARE.
- `splice_batch.py` re-validates every nearby against the CSV and **rejects**
  off-CSV ones (non-fatal: the rest of the batch still splices; you re-research
  the failures). This caught **0 dead links across the whole RT build**.

**Exact-string traps (CSV spelling is law):** `Newport (Isle of Wight)` (full
parenthetical), `Houghton le Spring` (no hyphens), `Bishop's Stortford`
(apostrophe), `Weston-super-Mare`, `Stockton-on-Tees`, `Newcastle-under-Lyme`,
`Newcastle upon Tyne`, `Kingston upon Thames`, `Welwyn Garden City`, `Hull` (not
"Kingston upon Hull"), `Stratford-upon-Avon`, `Ashton-under-Lyne`, `Grays
Thurrock`, `Thornton Cleveleys`, `Thornaby-on-Tees`. Whatever string the CSV uses
must appear in `nearby` verbatim.

For remote towns (Aberdeen, Inverness, Elgin, far Cornwall/Cumbria, Norwich, Isle
of Wight) you sometimes have only 1–2 genuinely-close CSV towns; use the nearest
regional city/cities. Only hard rule: "on the CSV."

**One failure mode to pre-empt (happened on RT):** an agent put a town's *shopping
areas* (Romford → "Market Place / The Brewery / South Street") into `nearby`
instead of towns. The splicer caught it (not on CSV → rejected). When you give a
"use the town's own centre" hint for boroughs, say explicitly: **that hint is for
s1loc PROSE, not for the nearby list — nearby is always 3 CSV towns.**

---

## 5b. TOWN-KEY / SLUG EDGE CASES (caused real verify failures on the lineage)

The TOWNS key must be the **lowercased exact CSV spelling** (the build's display
lookup and slug both derive from it). RT handled these correctly by telling agents
the exact spelling per town and asserting in the splicer:

- **Apostrophe:** `"bishop's stortford"` (slug `bishop-s-stortford`).
- **Space vs hyphen:** `"potters bar"`, `"thornton cleveleys"`, `"grays thurrock"`.
- **Parenthetical:** `"newport (isle of wight)"` → slug `newport-isle-of-wight`.
- **No-hyphen oddity:** `"houghton le spring"`.

Slugify rule: lowercase, `&`→`and`, every run of non-alnum → single `-`, strip
leading/trailing `-`. The splicer asserts every key is in the CSV's lowercased
set; if not, fix the key string.

**Ambiguous town names — disambiguate in the agent prompt:** RT had Chapeltown
(Sheffield vs Leeds — CSV's is **Sheffield**), Rothwell (West Yorks vs Northants —
CSV's is **West Yorks**), Newport (Wales vs IoW — both on CSV, separate rows),
Wellington (Somerset), Gosforth (Newcastle). State which one in the prompt.

---

## 6. Dup-enrichment loop (clearing an over-cap pair)

Worst-pair creeps toward 52% as N grows; you WILL hit it occasionally (RT hit it
in **3 of 10 batches**: Lincoln/Maidstone, Amesbury/Brentwood, Clydebank/Solihull
— all unrelated towns that hashed to the same pool variants). Fix:

1. `python3 diag_bh.py outputs/bh-<a>.html outputs/bh-<b>.html` → names the
   **weaker page** and ~N words to add.
2. **Web-verify NEW local proper nouns** for the town(s) (named centres, arcades,
   markets, high streets, parades, retail/business parks) and add a **single solid
   ~50-55-word proper-noun-rich sentence** to the weaker page's `s1loc` via
   `enrich.py` (write `enrich.json`, run it, rebuild, re-score). One good sentence
   drops a pair ~2pp. Real specifics, NOT generic reword (SPEC 8.3).
3. If still over (a "sticky" pair sharing many pooled variants), **enrich BOTH
   pages.** On RT, enriching both sides of each over-cap pair cleared all three in
   one round each.

**When editing `bh_build.py` after a Bash grep:** the Edit tool requires a real
**Read** of the exact line first (grep does not satisfy it). `enrich.py` sidesteps
this by rewriting the town's single-line JSON entry programmatically.

---

## 6b. THE BIGGEST UNIQUENESS LEVER (do this from batch 1)

The pooled scaffold sections are scored and have only 3–6 variants each. Two towns
that hash to the same variants across several pools start at a high baseline; an
unlucky extra collision tips them over 52%. The single most effective preventative
is to instruct EVERY research agent:

> **VARY the Para-1 opening sentence structure town to town** (mix "{Town} is …",
> "Set on the …", "Beyond the chains in …, {Town} …", "A major … centre, {Town}
> …") **and VARY the Para-2 closing beat.** Do not reuse one stock opener verbatim.

RT used this from batch 1 and kept worst-pair at/under 51.9% the whole way. (Minor
slip seen: two towns both opened "Beyond the chains in …" — harmless under cap, but
tighten the instruction at scale.)

---

## 6c. CLUSTER DIFFERENTIATION

When a batch has a tight geographic cluster (RT examples: Black Country —
Bilston/Sedgley/Tipton/Willenhall/Bloxwich; Isle of Wight —
Newport/Ryde/Cowes/Shanklin/Sandown; Welsh Valleys; Tyne & Wear coast), put the
cluster in ONE agent's group and tell it to **differentiate hard using each town's
OWN distinct centres, streets, markets and postcodes** so the pages don't read
alike. This prevented cluster over-cap pairs on RT.

---

## 7. TOWNS schema + splice mechanics

RT is a **Low-local-variation** series: each town's `s1loc` holds ONLY its **2
genuinely-local paragraphs**; the generic shared paragraphs come from POOLS
appended by `s1_paras()` as `[local1, local2, OWNER, SHOPFRONT, CONSIST+KIT]`.
**Confirm BH's variation level in SPEC** — match whatever the seed `TOWNS` entries
use; never paste generic pool prose into `s1loc`.

Each `TOWNS` entry (keyed by **lowercased exact CSV town name**):

```python
"leeds": {
  "region": "Leeds and West Yorkshire",
  "nearby": ["Bradford", "Pudsey", "Dewsbury"],     # exactly 3, all on CSV
  "snapshot": "...fixed opener/closer from SPEC; only town + 'from A to B' vary...",
  "s1_head": "short region-flavoured headline (must differ across towns)",
  "s1loc": ["para1 (local geography)", "para2 (operator/mix)"],   # 2 paras (RT)
  "kit_loc": "short phrase slotted into a pool sentence",
  "s2_intro": "Whether you ... across <Town>'s <real features>"   # NO trailing punctuation
}
```

**`splice_batch.py` validation (port verbatim; reject on any):** required fields
present; `nearby` is 3 unique, all on CSV; `s1loc` exactly the right paragraph
count; **ASCII only**; **no inner `"`**; **no `&` `<` `>`** (these break verify's
entity/JS checks — tell agents to write "and", avoid markup); key equals its
lowercased CSV spelling; `s2_intro` no trailing punctuation. Serialize each entry
with `json.dumps(entry, ensure_ascii=False)` (valid Python since no inner
double-quotes), one town per line, inserted before the marker
`"\n}\n\n# === CSV / nearby"`. Idempotent: skip keys already in TOWNS.

> RT note: one agent's `M&S` → the splicer's `&` rule would reject it, but the
> *gold-standard Leeds* entry actually contains "M&S" (a bare `&` not forming an
> entity passes verify). To avoid mixed signals, the BH PROMPT_TEMPLATE should
> say **write "and", never "&"**, and use a gold-standard entry with no `&` in it.

---

## 8. PROMPT_TEMPLATE.md for the research agents

Shared brief every agent reads first. Must contain: a **gold-standard reference
entry** (use a built early BH town once you have one; until then adapt SPEC's
sample — and make sure it contains no `&`), the **verbatim snapshot opener/
closer**, the field rules, and HARD CONSTRAINTS:

- **ASCII only** (transliterate accents; straight `'` and `-`; **no `&`** — write
  "and"; **no `<`/`>`**; no curly quotes/dashes).
- **No `"` inside any string value** (apostrophes fine).
- **`s1loc` = exactly N paragraphs** (N from SPEC), local content only — do NOT
  write the generic pool prose; the generator adds it.
- Agents do their **own** web searches; never author from memory; every local
  claim web-verified; **real proper nouns** (salon districts, named high streets,
  shopping parades, arcades, business/retail parks, town-centre streets) are the
  whole point.
- **NEARBY = 3 towns chosen VERBATIM from the CSV `Town` column** (nearest that are
  on it). The "use the town's own centre" hint is for PROSE, not for nearby.
- Keep the BH posture from SPEC; don't drift. EXCLUDE other series' vocab (BLEED).
- **VARY Para-1 and Para-2 openings** (§6b); for clusters, differentiate hard (§6c).
- **Write `research_bNNg{i}.py` as `NEW = {...}` AND return only a one-line
  confirmation per town** (key + 7 fields + s1loc word counts) — do NOT paste the
  dict.

Agent invocation that worked: `general-purpose`, `run_in_background: true`, 6–7
towns each, the CSV path for nearby, plus a one-line disambiguation/anchor hint
per tricky town. Launch all 8 of a batch in a single message (parallel).

---

## 9. Pitfalls carried over (don't relearn these)

- **CRC32 → md5** (§0). The big one.
- **Clone-rename of the diag import** + outdir fallback + display-casing (§0b) —
  RT shipped with all three still broken; assume BH does too.
- **PROMPT_TEMPLATE + splicer + next_towns + enrich are NOT in the kit** — port
  them from the RT kit zip (§0c).
- **ORG_BLOCK must be wrapped in its `<script type="application/ld+json">` tag** —
  verify enforces exactly 4 JSON-LD blocks; an unwrapped Org block fails it.
- **Don't BLEED your own core vocab** — keep BH's lead/spine words (tunic, apron,
  salon, spa, barber, hair, beauty, nail, gown…) OUT of BLEED; **remove `tunic`
  from the inherited cleaning bleed line** (the FS/RT lesson).
- **Nearby selection lives in the agents now**, gated by the splicer's on-CSV
  check (§5). Tell agents nearby = CSV towns, not shopping areas.
- **`&`/`<`/`>` in values** break verify — splicer rejects them; agents write "and".
- **Town-key/slug edge cases + ambiguous names** — give exact spelling and which
  same-named town the CSV means (§5b).
- **Edit after grep** needs a real Read first; `enrich.py` avoids it (§6).
- **`.gitignore` early** (`__pycache__/`, `*.pyc`, `dist/`, `outputs/`,
  `enrich.json`) — don't commit caches or the deliverable zips. The built HTML is
  reproducible from `bh_build.py`, so committing the kit + research files is enough
  (RT did this; pages regenerate via `python3 bh_build.py`).
- **Overall-unique ~66–68%** is the structural ceiling; the **52% pair cap** is the
  binding guard. Present the score honestly; don't chase 77%.
- **London is the flagship AND the London page** — never rebuild it; copy into
  `outputs/` at the very end so the deliverable is 505/505.

---

## 10. Standing instruction

Hard checks (`verify_bh`) are the binding gate. The 52% pair cap is the binding
uniqueness guard; present overall-unique honestly as a diagnostic, don't chase the
77% floor. Never rebuild the flagship; only ADD pages. Build in ~56-town batches,
research-first, web-verified, nearby chosen from the CSV and splicer-validated,
vary Para-1/Para-2 from batch 1, commit each batch. Recreate the kit from the
shipped files each session — the filesystem resets.

— Handover written at the close of the RT build (**505/505 green: verify 505/505,
worst pair 51.9%, 0 over-cap, overall-unique 67.6%**). The RT kit zip is the
fastest starting point: rename, swap vocabulary, set the BH lead/BLEED words, run
§0/§0b/§0c, sample-batch once, then scale.
