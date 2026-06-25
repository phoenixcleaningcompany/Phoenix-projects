# VT (Veterinary & Animal Care) build — handover

Carries forward everything proven on the **BH (Beauty, Hair & Spa)** build
(**505/505 pages, all gates green: verify 505/505, worst pair 51.5%, 0 over-cap,
overall-unique 68.4%**). VT is the **same machine, new vocabulary**: 505 location
pages, one per UK town, page prefix `vt-`, canonical/og to
`https://www.ineedworkwear.uk/vt-<slug>.html`.

Lineage: HM → FS → DC → RT → **BH → VT**. Same scripts, same workflow. Read this,
then **the VT SPEC.md and CLAUDE.md** for VT-specific vocabulary/posture. The
filesystem resets between sessions — recreate the kit from the shipped files.

> Fastest start: take the **BH kit zip** (`bh-kit.zip`) delivered at the close of
> the BH build. Rename `bh_`→`vt_` / `BH_`→`VT_` across filenames and code, drop
> in the VT flagship `vt-london.html` + `VT_towns.csv`, set the VT lead/BLEED
> words in `verify_vt.py` from the VT SPEC, then run the §0/§0b/§0c checks below
> before building. **The BH kit already contains working `next_towns.py`,
> `splice_batch.py`, `enrich.py`, `PROMPT_TEMPLATE.md` — port them, don't rebuild.**

---

## 0. THE ONE BUG YOU MUST NOT REINHERIT (read twice)

The variant selector `pick(key, salt, n)` must use **md5, not CRC32**.

```python
# BROKEN — crc32 is a checksum; "% n" reads only its low bits, which stay
# correlated with the input, so same-length town names collide on the SAME pool
# variant at once -> near-identical pages -> worst-pair score explodes.
def pick(key, salt, n):
    return zlib.crc32((salt + '|' + str(key).lower()).encode()) % n   # NO
```

```python
# CORRECT — port verbatim. Keep the exact "salt + '|' + key" composition.
import hashlib
def pick(key, salt, n):
    h = hashlib.md5((salt + '|' + str(key).lower()).encode()).digest()
    return int.from_bytes(h[:4], 'big') % n
```

**First thing in the VT session:** `grep -n crc32 vt_build.py`. If present, patch
before building a single page; ensure `import hashlib`, drop unused `zlib`.
*(BH shipped already on md5 — but check anyway; this is the most expensive bug in
the lineage.)*

---

## 0b. CLONE-RENAME FIXES — re-verify all three after the bh_→vt_ rename

These bit FS/RT and were still latent in the BH kit. After the bulk rename:

1. **Scorer import in the diag script.** `diag_bh.py` imported `scobh_re` (a stale
   wrong module name) instead of `score_bh` — an **ImportError on startup**. Grep
   the diag script's `import score_xx as S` line and set it to `import score_vt as S`.
   Prove it: run `python3 diag_vt.py outputs/vt-<a>.html outputs/vt-<b>.html` early.

2. **Hardcoded output dir.** `main()` will hardcode `/mnt/user-data/outputs`,
   absent in a fresh sandbox. Use the fallback:
   ```python
   outdir = os.environ.get('VT_OUTDIR') or ('/mnt/user-data/outputs'
            if os.path.isdir('/mnt/user-data/outputs') else 'outputs')
   os.makedirs(outdir, exist_ok=True)
   ```

3. **Display-name casing from the CSV.** `' '.join(w.capitalize() ...)` mangles
   `stoke-on-trent` → "Stoke-on-trent", `newcastle upon tyne` → "Newcastle Upon
   Tyne". Resolve from the CSV's exact spelling (verify keys off the CSV town):
   ```python
   disp = {r[1].lower(): r[1] for r in _load_csv()}
   town = disp.get(tk, ' '.join(w.capitalize() for w in tk.split()))
   ```

4. **Stale verifier header.** Fix the `verify_*.py` docstring/usage and the
   empty-folder error message to say `vt-*.html` (BH still said `verify_fs` /
   `se-*.html`). Cosmetic, but do it.

---

## 0c. THE FOUR HELPERS — PORT FROM THE BH KIT (don't rebuild)

These are NOT in the original lineage kit; they were authored on BH and are in
`bh-kit.zip`. Clone + rename `bh`→`vt`:

| File | Role |
|---|---|
| `next_towns.py` | prints the next N unbuilt towns (CSV rank order) grouped into G agent groups. **unbuilt = on CSV but not yet a key in `vt_build.TOWNS`**, so git state IS your progress — resumes correctly after any context reset. |
| `splice_batch.py` | globs `research_*.py`, validates every `NEW={...}` entry, splices **only valid+new** towns into `vt_build.py`'s TOWNS, **non-fatal** per bad entry (reports + skips; rest still splice). Idempotent. |
| `enrich.py` | reads `enrich.json` `[{"key","para","text"}]` and appends a researched sentence to `TOWNS[key]['s1loc'][para]` to clear an over-cap pair — without hand-editing the giant source line. |
| `PROMPT_TEMPLATE.md` | the shared brief every research agent reads first (field rules, hard constraints, gold-standard entry). Swap BH vocabulary for VT. |

`splice_batch.py` validation (keep verbatim, retune field list to VT): required
fields present; `nearby` = 3 unique, all on CSV (verbatim spelling); `s1loc` =
exactly the right paragraph count; **ASCII only**; **no inner `"`**; **no `&` `<`
`>`**; key == lowercased CSV spelling; `s2_intro` no trailing punctuation.

> The splicer does NOT check the BLEED list — `verify` does. On BH one page
> ("garden centre" in Stamford) passed the splicer and was caught only by
> `verify`. So **always run `verify_vt.py outputs` after every batch**, not just
> the splicer. (Optional hardening: add the BLEED scan to the splicer too.)

---

## 1. What VT is — CONFIRM EVERYTHING AGAINST THE REAL VT SPEC (do not assume)

VT = workwear for **veterinary and animal-care** businesses. Plausible buyers:
vet practices/surgeries, animal hospitals, vet nurses, dog groomers/grooming
salons, kennels/catteries, pet shops, boarding/daycare, shelters/rescues,
equine/farm-animal and large-animal vets, zoos/wildlife. **Do not lock any of
this from memory — read the SPEC.**

**Set these in `verify_vt.py` from the SPEC — DO NOT guess:**

- `LEAD` / `CO_LEAD` / `TRI_LEAD` — the three lead products. verify **hard-fails**
  if any lead word is absent from a page, so the prose pools must use all three
  naturally. (BH was tunic/polo/apron. VT will differ — *plausibly*
  **scrub top / polo / fleece**, or **tunic / scrubs / fleece**, but CONFIRM.)
- **The distinctive vocabulary spine** — the angle that makes VT pages read
  specific. (BH's was "your team is your salon's first impression / presentation
  + practical". VT's is likely a hygiene/practical + approachable-professional
  angle around the practice/surgery/grooming room — CONFIRM.)
- **The BLEED list** — bans OTHER series' core vocab so series stay separated.
  **CRITICAL, COST-A-FAILED-RUN LESSON: never put VT's OWN core words in BLEED.**
  Whatever VT's lead/spine words are (scrub/scrubs/tunic/polo/fleece/groomer/
  kennel/cattery/veterinary/practice/surgery…), keep them OUT of BLEED. In
  particular **`tunic`/`scrubs` are almost certainly VT core** — make sure they
  are not inherited from another series' bleed line (exactly as BH had to remove
  `tunic` from the cleaning-series bleed). Carry over the *other* series' bans
  (forestry chainsaw/arborist; highways Chapter 8/National Highways; courier
  multidrop/owner-driver/softshell; food hairnet/BRCGS; security SIA/body armour;
  waste RCV/HWRC; renewables solar/heat pump/MCS) **only per what the VT SPEC says
  to separate**, and consider whether VT must block **BH's** signatures
  (salon/barber/beauty/spa/clogs) and vice-versa — confirm in SPEC.
- **Delivery-timescale regex (check 9)** bans *our* shipping promises ("next-day
  delivery", "deliver within N"). Keep prose to "standard lead times."

**Posture (CONFIRM):** BH was **Self-checkout / Template B** (sole-trader /
small-shop buyer, order-direct-online-led, trade account secondary). VT could be
self-checkout (small grooming/independent practices) OR concierge / Template A
(corporate vet groups, trade-account-led). **Read the SPEC and match the seed
TOWNS entries — do not let it drift.**

**Constant across the lineage:** Nearby = **geographic** (3 close towns, all on
CSV). **14 `.com` + 1 community link** per page. **4 JSON-LD blocks** (FAQ + Org +
Service + Breadcrumb), and ORG_BLOCK must be wrapped in its own
`<script type="application/ld+json">` tag or check-16 fails.

---

## 2. The gates

**`verify_vt.py` (HARD — the only binding gate). Per page:** exactly **14** `.com`
+ **1** community link; **4** JSON-LD blocks; no JavaScript / HTML entities; meta
description present, ≤160, **unique** (and no apostrophes per BH SPEC — confirm for
VT); town in `<title>` and `<h1>`; unique title; no delivery-timescale claims;
**BLEED clean** (other series' vocab only — never VT's own); **lead trio present**;
nearby/internal `vt-<slug>.html` links only to CSV towns. Must read
`==== N/N pages passed all hard checks ====`.

**`score_vt.py` (dup). Binding number = worst-pair ≤ 52.0%.**
- 5-gram shingle Jaccard; strips chrome/SVG/JSON-LD/footer + pooled chrome divs;
  masks only the town name.
- `MAX_PAIR = 52.0%` is the real guard.
- `FLOOR = 77.0%` overall-unique is **secondary and structurally unreachable at
  this scale** (~66–68% with a heavy shared product scaffold). DO NOT chase it.
  Report honestly. (FS 66.8%, DC 68.1%, RT 67.6%, **BH 68.4%** — expected shape.)

---

## 3. Session workflow (the PROVEN loop — exactly what shipped BH)

1. Recreate the kit beside `vt_build.py`: `vt-london.html` (flagship) +
   `VT_towns.csv`. Apply §0 + §0b, port the §0c helpers, set VT lead/BLEED in
   `verify_vt.py`.
2. Build the seed town(s) already in `TOWNS`, copy the flagship into `outputs/`,
   run `verify_vt.py outputs` (expect N/N) and `score_vt.py outputs`. Commit the
   patched kit. **Run one small sample batch end-to-end first to prove the
   pipeline before scaling.**
3. Build in **batches of ~56 towns**, population-rank order, **skipping London**
   (flagship, added LAST). Per batch:
   1. `python3 next_towns.py 56 8` → REMAINING + 8 groups (round-robin by rank).
   2. Launch **8 background `general-purpose` agents in one message** (~7 towns
      each). Each reads `PROMPT_TEMPLATE.md` + `VT_towns.csv`, does its OWN web
      searches, NEVER authors from memory, writes `research_bNNg{i}.py` as
      `NEW = {...}`, and returns **only a one-line confirmation per town** (key +
      7 fields + s1loc word counts + 3 nearby) — NOT the dict (keeps your context
      lean across 10 batches; the file is the source of truth).
   3. When all 8 return: `python3 splice_batch.py 'research_bNNg*.py'`, then build
      all + copy flagship + `verify_vt.py outputs` (must be N/N) + `score_vt.py`.
   4. **Diag-enrich any over-cap pair** (§5); rebuild; re-score.
   5. Commit + push the batch (incl. its research files).
4. After all 504 town pages: confirm the flagship is in `outputs/`. Final
   `verify_vt.py outputs` = **505/505**, final score.
5. Zip `outputs/*.html` (505) + a kit zip; deliver via SendUserFile + a build
   report.

**Cadence that worked on BH:** ~56 towns/batch, 9–10 batches, 8 agents each ~2–4
min in parallel; a completion notification per agent. **Commit each batch** so
progress survives context resets — and because progress = "towns in TOWNS",
`next_towns.py` always resumes after a reset. (On a fresh remote session, a
git-status stop-hook may nag about untracked `research_*.py` between agent
completions — just commit a wip checkpoint each time you yield.)

**Per-town TOWNS schema** (key = lowercased exact CSV spelling), assembled by
`s1_paras()` as `[local1, local2, <generic pool paras>]`:
```python
"leeds": {
  "region": "Leeds and West Yorkshire",
  "nearby": ["Bradford", "Pudsey", "Dewsbury"],   # exactly 3, all on CSV
  "snapshot": "...fixed opener/closer; only town + 'from A to B' vary...",
  "s1_head": "short region-flavoured headline (must differ across towns)",
  "s1loc": ["para1 (local geography)", "para2 (operator/mix)"],   # 2 local paras only
  "kit_loc": "short phrase slotted into a pool sentence",
  "s2_intro": "Whether you are ... across <Town>"   # NO trailing punctuation
}
```
**Low-variation architecture (BH had this; confirm VT):** the generic shared
paragraphs live in **POOLS** (OWNER/PRESENT/NARROW/KIT-style), town-templated and
appended by `s1_paras()`. Each town's `s1loc` holds ONLY its 2 genuinely-local
paragraphs. **Never paste the generic pool prose into `s1loc`.**

---

## 4. Nearby = GEOGRAPHIC, validated by the splicer

`require_nearby()` HARD-FAILS any nearby not on the CSV, and verify fails on dead
internal links. Hand-picking 3 for 505 towns is infeasible, so nearby selection
lives **in the research agents**, gated by the splicer's on-CSV check (this gave
**0 dead links** across the whole BH build).

- Tell each agent: **NEARBY = the 3 geographically-closest towns that appear
  VERBATIM in the CSV `Town` column.** Many obvious neighbours are NOT on the
  population-ranked 505 (e.g. Nantwich, Saltcoats, Hazel Grove, Waltham Cross,
  Baldock, Romsey) — pick the nearest ones that ARE. The splicer rejects off-CSV
  nearby non-fatally; re-research the rejects.
- For remote towns (Aberdeen, Inverness, Elgin, far Cornwall/Cumbria, Norwich,
  Isle of Wight) you may have only 1–2 truly-close CSV towns; use the nearest
  regional cities. Only hard rule: "on the CSV."
- The "use the town's own centre" hint is for **s1loc PROSE only**, never the
  nearby list (an RT agent once put shopping streets in `nearby`).

**Exact-string traps (CSV spelling is law — key AND nearby must match verbatim):**
`Newcastle upon Tyne`, `Newcastle-under-Lyme`, `Stoke-on-Trent`,
`Weston-super-Mare`, `Bishop's Stortford` (apostrophe), `Houghton le Spring` (no
hyphens), `Newport (Isle of Wight)` (full parenthetical — distinct from Welsh
`Newport`), `Kingston upon Thames`, `Welwyn Garden City`, `Grays Thurrock`,
`Thornton Cleveleys`, `Thornaby-on-Tees`, `Stratford-upon-Avon`,
`Ashton-under-Lyne`, `Hull` (not "Kingston upon Hull").

**Ambiguous names — disambiguate in the agent prompt (which one the CSV means):**
Chapeltown (CSV = **Sheffield**), Rothwell (CSV = **West Yorkshire**), Gosforth
(CSV = **Newcastle**), Wellington (CSV = **Somerset**), Newport (Wales **and**
IoW are separate rows), Hythe (BH took **Hampshire/Waterside** by the ~20k pop),
Sutton (the **south-London borough**, not Sutton Coldfield/-in-Ashfield).

---

## 5. Dup-enrichment loop (clearing an over-cap pair)

The pooled scaffold creates a **plateau of unlucky pairs near ~51–52%** (on BH,
many pairs sat at 51.5% — masking the town name, two towns that hash to the same
pool variants across several pools start high). **This plateau is under cap and is
EXPECTED — do not chase it.** You only act on pairs that **exceed 52%** (BH hit
this in 2 of 10 batches: Denton/Rushden 52.6%, Beverley/Oadby 52.9%):

1. `python3 diag_vt.py outputs/vt-<a>.html outputs/vt-<b>.html` → names the
   **weaker page** (fewer shingles) and ~N words to add. (It auto-picks a third
   control page and subtracts shared boilerplate so you see the pair-specific
   collisions — usually pooled scaffold, not the local paras.)
2. **Web-verify NEW local proper nouns** for the weaker town (named centres,
   arcades, retail/business parks, high streets, parades, neighbouring villages)
   and add ONE solid ~45–55-word proper-noun-rich sentence to its `s1loc` via
   `enrich.py` (write `enrich.json`, run it, rebuild just that town, re-score).
   One good sentence drops a pair ~2–4pp. Real specifics, NOT generic reword
   (SPEC 8.3). A fast way: spawn one tiny research agent that returns two
   sentences (one per town) and drop them into `enrich.json`.
3. If still over (a "sticky" pair), **enrich BOTH pages.**

`enrich.py` only works on splicer-written **single-line** JSON entries; the
hand-authored seed entries (london/birmingham/leeds-equivalents) are multi-line —
edit those by hand if ever needed.

---

## 6. Biggest uniqueness lever — instruct EVERY agent (from batch 1)

> **VARY the Para-1 opening sentence STRUCTURE town to town** (mix "{Town} is …",
> "Set on the …", "Beyond the chains in …, {Town} …", "A market town …, {Town} …")
> **and VARY the Para-2 closing beat.** Do not reuse one stock opener verbatim.

BH used this from batch 1 and held worst-pair at/under ~51.5% all the way to 505.
(One residual BH tell to tighten next time: many agents copied the gold-standard
Para-2 opener "And the trade is overwhelmingly small and independent…" almost
verbatim — harmless under cap, but vary the Para-2 OPENER too, and consider
widening the link-free scaffold pools (CON/ACC/EMB/ORD) from 4→6 variants up
front for extra headroom. **Keep link-bearing pools — CON_P3 @1 .com, ACC_P4 @2
.com, SELF/SORTED @1 — at their counts, or the 14-link total breaks.**)

For a tight geographic cluster in one batch (Black Country, Tyne & Wear coast,
Cornwall, Welsh Valleys, Isle of Wight), put it in ONE agent's group and tell it
to **differentiate hard using each town's OWN distinct centres/streets**.

---

## 7. Pitfalls carried over (don't relearn these)

- **CRC32 → md5** (§0). The big one — grep first.
- **Clone-rename trio** (diag import, outdir, display-casing) + stale verifier
  header (§0b) — assume all four are latent after the rename.
- **Port the four helpers** from the BH kit (§0c) — don't rebuild them.
- **ORG_BLOCK must be wrapped in its `<script type="application/ld+json">` tag** —
  check-16 enforces exactly 4 JSON-LD blocks.
- **Don't BLEED your own core vocab** — keep VT's lead/spine words OUT of BLEED;
  re-check `tunic`/`scrubs` aren't inherited from a cleaning/other bleed line.
- **verify catches BLEED, the splicer doesn't** — always `verify_vt.py outputs`
  after every batch (BH's "garden centre"/Stamford slip was caught only here).
- **Nearby = CSV towns, not shopping areas**; exact CSV spelling for key + nearby;
  disambiguate same-named towns (§4).
- **Editing `vt_build.py` after a Bash grep** needs a real **Read** of the exact
  line first; `enrich.py` sidesteps this by rewriting the entry's JSON line.
- **`.gitignore` early** (`__pycache__/`, `*.pyc`, `enrich.json`, deliverable
  zips). The built HTML regenerates from `vt_build.py`, so committing the kit +
  research files is enough.
- **Overall-unique ~66–68% is the structural ceiling**; the **52% pair cap** is
  the binding guard. Present the score honestly; don't chase 77%, and don't chase
  the under-cap ~51.5% plateau either.
- **London is the flagship AND the London page** — never rebuild it; copy into
  `outputs/` at the very end so the deliverable is 505/505.

---

## 8. Standing instruction

Hard checks (`verify_vt`) are the binding gate. The 52% pair cap is the binding
uniqueness guard; present overall-unique honestly as a diagnostic, don't chase the
77% floor or the under-cap plateau. Never rebuild the flagship; only ADD pages.
Build in ~56-town batches, research-first, web-verified, nearby chosen from the CSV
and splicer-validated, vary Para-1/Para-2 from batch 1, commit each batch.
Recreate the kit from the shipped files each session — the filesystem resets.

— Handover written at the close of the **BH build (505/505 green: verify 505/505,
worst pair 51.5%, 0 over-cap, overall-unique 68.4%)**. The BH kit zip is the
fastest start: rename, swap vocabulary, set the VT lead/BLEED words, run
§0/§0b/§0c, sample-batch once, then scale.
