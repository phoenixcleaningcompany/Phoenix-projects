# TL (Travel, Tourism & Leisure) — build handover

You're building **TL**, a 505-page town series (504 UK towns + a London flagship),
the **same scaffold** as CH2 (Charity & Volunteer) and TC (Telecoms). This doc is the
distilled playbook from the **CH2 build**: what to reuse, the fixes to apply **from
the start** (including ones the CH2 handover did NOT mention but which the CH2 build
proved necessary), what is **series-specific and must be re-derived**, the batch rhythm
that worked, and the traps that cost time. Read CH2's `SPEC.md`, `CLAUDE.md` and
`BUILD_REPORT.md` alongside this.

---

## 0. TL;DR
- Clone the CH2 kit, rename `ch2`/`ch2-`/`CH2_` -> `tl`/`tl-`/`TL_`, rewrite the
  **series-specific** layer (copy, leads, bleed list, schema strings, SVGs, palette, posture).
- Apply the **7 kit fixes** in section 2 before building a single batch. The first 4 are
  the CH2-handover fixes; **fixes 5-7 are new lessons from the CH2 build** and matter a lot.
- Build in a **seed (~2 towns) + 9 batches of ~56** (8 groups of 7), population-rank order,
  London last/never a target.
- Per batch: 8 parallel `general-purpose` agents each **web-research 7 towns and write
  their own `towns/bNN_gX.json`** -> pre-flight scan -> build -> `verify` (binding gate,
  must be N/N) -> `score` (pair cap is the real guard) -> commit + push.
- Gate that matters: **`verify` 100%** and **worst pair <= 52%**. The overall-unique
  "floor" (77%) is a diagnostic and is **not reachable** at 505 pages — don't chase it.
- CH2 final shape to aim at: **505/505 verify, worst pair 50.9%, 0 dead links, 0 over-cap.**

---

## 1. Kit anatomy
| File | Role |
|---|---|
| `tl-london.html` | Hand-authored flagship. Chrome (header/footer/CSS/SVGs/contact) is **extracted from it** by the generator. Never rebuild it after authoring. |
| `tl_build.py` | Generator. md5-hashed prose pools + per-town `TOWNS` dict + `towns/*.json` loader -> one `tl-<slug>.html` per town. |
| `verify_tl.py` | **The binding gate** — 16 hard checks. Run before every delivery; never ship a FAIL. |
| `score_tl.py` / `diag_tl.py` | Uniqueness diagnostics (NOT a gate). diag isolates what an over-cap pair shares. |
| `next_towns.py` | Resume-safe batch planner (`--done` / `N` / `--slugs N` / `--check`). **Build it early** (see fix 5). |
| `TL_towns.csv` | 505 rows (Rank, Town, Population, Nation). **Identical list to CH2/TC** — reuse it verbatim. |
| `towns/bNN_gX.json` | Per-batch town data (research agents write these), merged into `TOWNS` at import. |

---

## 2. THE 7 KIT FIXES — apply before building

### Fixes 1-4 (from the CH2 handover; still required)
**(1) Output-dir fallback.** The seed `main()` hardcoded `/mnt/user-data/outputs`, which
does not exist on a fresh checkout. Replace with:
```python
outdir = (os.environ.get('TL_OUTDIR')
          or ('/mnt/user-data/outputs' if os.path.isdir('/mnt/user-data/outputs') else 'outputs'))
os.makedirs(outdir, exist_ok=True)
```

**(2) JSON batch loader.** Don't hand-grow a 4,000-line Python literal. Keep the seed
(~2 towns) in the literal; load the rest from `towns/*.json`:
```python
def _load_extra_towns():
    here = os.path.dirname(os.path.abspath(__file__)); d = os.path.join(here, 'towns')
    if not os.path.isdir(d): return
    for fn in sorted(os.listdir(d)):
        if fn.endswith('.json'):
            for k, v in json.load(open(os.path.join(d, fn), encoding='utf-8')).items():
                TOWNS[k.lower()] = v
_load_extra_towns()   # call right after the TOWNS literal
```
Same data in -> identical pages out (`pick()` is md5-keyed on town name; dict order is
irrelevant). This let research agents write their own files — the single biggest
efficiency win.

**(3) Slug-robust display + lookup.** Naive `title()` mangles `Newcastle upon Tyne` ->
"Upon" and breaks `Stoke-on-Trent`, `Houghton le Spring`, `Bishop's Stortford`. Derive
the display name from the CSV and look TOWNS up by slug:
```python
_DISPLAY=None
def _display_map():
    global _DISPLAY
    if _DISPLAY is None: _DISPLAY={slugify(t): t for (_r,t,_n) in _load_csv()}
    return _DISPLAY
def town_display(key): return _display_map().get(slugify(key)) or ' '.join(w.capitalize() for w in key.split())
def _entry(town):
    s=slugify(town)
    for k,v in TOWNS.items():
        if slugify(k)==s: return v
    raise KeyError(town)
```
Use `T=_entry(town)` in `assemble()`; in `main()` use `town=town_display(arg)`,
`slug=f"tl-{slugify(arg)}"`, gate on `slugify(arg) in {slugify(k) for k in TOWNS}`.
Keep `verify`'s `find_town` matching **longest CSV slug first** so `Newport (Isle of
Wight)` wins over `Newport`.

**(4) Own-town bleed exemption in `verify`.** A town can legitimately be named like a
bleed term. Exempt the page's **own** town from the bleed scan; the term still fails on
every other page:
```python
town_l = (town or "").lower()
hit = [t for t in BLEED if t.lower()!=town_l and re.search(r"\b"+re.escape(t)+r"\b", txt, re.I)]
```
For TL, grep the CSV for town names that collide with your TL bleed list and confirm the
exemption covers them. (CH2's collision was **Wellington**, a CH2 bleed word.)

### Fixes 5-7 (NEW — learned during the CH2 build; bake them in)
**(5) Build `next_towns.py` immediately.** A tiny planner that imports the generator and
reports progress = membership of `TOWNS`. It makes the multi-batch run resumable across
context summarization (which WILL happen ~once per batch). Commands used every batch:
`next_towns.py` (done/left), `next_towns.py 56` (next N names), `next_towns.py --check`
(validate every nearby is on CSV). Copy CH2's verbatim, swap the prefix.

**(6) Widen the section pools 4 -> 6 from the start, and add `snapshot`/`kit_loc`
template fallbacks.** The CH2 seed shipped its EMB/CON/ACC paragraph pools at only **4
variants**, which set a near-dup ceiling that two unlucky towns kept hitting at ~52%.
Widening those pools to 6 (matching FAQ 7x6 / WHY 4x6) buys headroom. **Preserve exact
link counts** when you add variants (CH2: CON_P3 carried 1 `.com` link, ACC_P4 carried 2
— any new variant must match, or the exact link-count check fails). Also make `snapshot`
and `kit_loc` optional in `assemble()` with a town-swapped template fallback, so batch
JSON only needs the genuinely-local fields:
```python
snap = T.get("snapshot") or SNAP_TMPL.format(t=town)
kit  = KIT_POOL[...].format(loc=T.get('kit_loc', KIT_LOC_DEFAULT))
```

**(7) Use THREE local paragraphs per town, not two — this is the durable uniqueness
lever.** CH2's SPEC specified 2 local `s1loc` paragraphs; at 505 pages that left the
unique-to-pooled ratio too low and pairs crept over the 52% cap. Switching every town to
**3 proper-noun-rich local paragraphs** (para 3 = additional named hospices/charity
shops/mutual-aid/neighbourhoods, distinct from 1-2) held the worst pair at **50.9%**
across the whole series with almost no firefighting. Do this from batch 1. `s1_paras`
already appends pooled paragraphs after the local ones, so a 3-element `s1loc` just works.

---

## 3. SERIES-SPECIFIC — re-derive ALL of this for TL (do NOT copy from CH2)
The scaffold is shared; the **content layer is not**.

- **Lead products.** Set `LEAD/CO_LEAD/TRI_LEAD` and the 8 product cards for travel/
  tourism/leisure (likely polos, softshell/fleece, branded shirts/blouses, chinos,
  hi-vis for grounds/marshalling, aprons for cafe/catering, etc. — derive from the TL
  SPEC/matrix row). CH2 led polo + hi-vis + fleece; TL will differ.
- **The BLEED list — THE BIGGEST TRAP. It is per-series and INVERTED vs your own core.**
  - **Remove** TL's own core terms from the inherited list. CH2 BLOCKS several words that
    are almost certainly **TL CORE** and would fail every TL page: `softshell`, `gym`,
    `spa day`, `athleisure`, `tracksuit`, and possibly `garden centre`/`forecourt`. Audit
    every BLEED entry against TL vocabulary before building.
  - **Add CH2's core terms as TL bleed** so TL can't drift into the charity voice:
    `charity`, `volunteer`, `foodbank`, `food bank`, `pantry`, `Trussell`, `FareShare`,
    `safeguarding`, `community group`, `donation`, plus the other series' signatures CH2
    kept (security/cleaning/waste/highways/forestry/care/courier/salon/veterinary, and
    TC's `telecoms/fibre/broadband/Openreach`).
  - Rule of thumb: **if a new town trips bleed, first check it isn't your own core word.**
- **Identity / schema strings:** hero subtitle, h1/title template, CTA, section H2s,
  `serviceType`, `areaServed`, breadcrumb URL slug, Organization `knowsAbout`, FAQ set,
  the stat chips, the `#contract` differentiator block. Re-derive the canonical domain
  path (CH2 = `ineedworkwear.uk/ch2-{slug}.html`).
- **SVG scenes (5; town-swapped in `assemble`).** Re-skin palette and redraw the scenes
  for a travel/leisure context, and re-word every `aria-label` and caption the generator
  town-swaps. CH2 town-swaps: the embroidery aria (`a London charity logo`), the signpost
  (plank text via `signpost_town()` + aria + caption), and the premises aria
  (`serving ... across London`). Keep the same swap points.
- **Palette + fonts.** The verifier only checks the **two font families** — pick TL fonts
  and wire the `@import` + the font check. Hex colours are not checked.
- **Posture.** CH2 was Hybrid (national charity trade-account vs small group direct-online,
  equal weight, "every page names both routes"). Decide TL's two buyers (e.g. national
  hotel/leisure chains on managed accounts vs independent B&Bs/attractions direct online)
  and mirror the balance rule.

---

## 4. The batch rhythm that worked (CH2, 0 rejected pages)
1. `python3 next_towns.py 56` -> next 56 by rank.
2. Split into 8 groups of 7. **Pre-assign each town a LOCKED nearby triple** picked from
   the CSV yourself (geographic, hand-verified, on-list). This was the single biggest
   reliability win: **0 off-list / dead links across 504 towns.** Do NOT let agents pick
   nearby freely — they drift off-CSV or pick bad geography.
3. Dispatch **one `general-purpose` agent per group**, each told to: do real web research,
   write THREE local paragraphs per town, use the locked triple verbatim, name a given
   nearby town in `s2_intro`, and **write its own `towns/bNN_gX.json`** then reply only
   with a one-line confirmation + the triples. **Tell agents: "do ALL research yourself;
   do NOT spawn sub-agents."** Agents run async/background.
4. **Wait via the completion notifications + a file-count check** (`ls towns/bNN_*.json |
   wc -l`). Do NOT poll with `sleep`; do NOT read the agent transcript files (they overflow
   context).
5. **Pre-flight scan** (section 5) over the batch JSON.
6. `next_towns.py --check` (validates every nearby is on CSV).
7. `TL_OUTDIR=outputs python3 tl_build.py` (no-arg builds all TOWNS) -> `cp tl-london.html outputs/`.
8. `verify_tl.py outputs` -> **must be N/N PASS**. `score_tl.py outputs` -> confirm worst
   pair <= 52%; if over, `diag_tl.py` + enrich (section 7).
9. `git add towns/bNN_*.json tl_build.py && git commit && git push`. Next batch.

Cost: CH2 ran ~8 agents x ~40k tokens per batch x 10 batches (~3M+ agent tokens total).
Budget for it.

---

## 5. Pre-flight scan (reuse verbatim; swap glob + BLEED list; allow 2-3 s1loc paras)
```python
import json, glob, re, csv
BLEED=[...]                  # <-- TL bleed list
REQ=["region","nearby","s1_head","s1loc","kit_loc","s2_intro"]   # snapshot optional via fallback
csv_towns={r["Town"].strip().lower() for r in csv.DictReader(open("TL_towns.csv",encoding="utf-8-sig"))}
issues=0; n=0
for f in sorted(glob.glob("towns/bNN_*.json")):
    for k,v in json.load(open(f,encoding="utf-8")).items():
        n+=1; blob=json.dumps(v,ensure_ascii=False)
        if any(ord(c)>127 for c in blob): print("NONASCII",k); issues+=1   # pound/curly quotes/em-dash
        if "&" in blob: print("AMP",k); issues+=1                          # agents emit "B&B", "V&A"
        if [x for x in REQ if x not in v]: print("FIELD",k); issues+=1
        if len(v.get("nearby",[]))!=3 or not (2<=len(v.get("s1loc",[]))<=3): print("SHAPE",k); issues+=1
        for t in BLEED:
            if t.lower()==k.lower(): continue                              # own-town exemption
            if re.search(r'\b'+re.escape(t)+r'\b',blob,re.I): print("BLEED",k,t); issues+=1
        for nb in v.get("nearby",[]):
            if nb.lower() not in csv_towns: print("NEARBY-OFF-CSV",k,nb); issues+=1
print(f"entries={n} issues={issues}")
```
Note `&` is the one agents reliably slip on for travel/tourism ("B&B", "Bed and
Breakfast", attraction names). The prompt must say: write "and", never the `&` character.

---

## 6. Gates & scoring reality
- **`verify` is the contract.** 16 hard checks: exact link counts (CH2 = 14 `.com` + 1
  community — re-derive TL's and keep link-bearing pools carrying a fixed count), no JS,
  no HTML entities, meta <=160 (no apostrophe in meta), title <=60, town in title+h1, no
  delivery-timescale claims, lead trio present, 4 JSON-LD blocks, dead-link guard, bleed.
  **Every page must pass.**
- **`score` floors are diagnostics.** CH2 final overall-unique **66.0%** (the 77% floor is
  unreachable at 505 pages — pooled-scaffold ceiling). The **pair cap (52%) is the real
  near-duplicate guard.** "BELOW FLOOR" on overall is expected and fine; a pair **over 52%**
  is not — fix it (section 7).

---

## 7. If a pair goes over the 52% cap
Pairs creep up as N grows; watch `score` every batch. When one exceeds the cap:
1. `python3 diag_tl.py outputs tl-a.html tl-b.html` — shows the exact shingles the pair
   shares (a control page subtracts boilerplate). In CH2 the overlap was almost always
   **pooled boilerplate that md5 happened to align**, not local content.
2. Add **one researched, proper-noun-rich local paragraph (~70-90 words)** to the
   **weaker** page's `s1loc`. Do NOT reword distinctive local prose into generic phrasing.
3. If you started every town at 3 paragraphs (fix 7), this is rare. CH2's only repeat
   offenders were the early 2-paragraph towns; once enriched to 3, the series settled at
   50.9%. So: **3 paragraphs from batch 1 ≈ no firefighting.**

---

## 8. Gotchas / traps checklist (each cost time in CH2)
- [ ] **Bleed inversion (section 3)** — your own core word left in the inherited bleed list
      fails every page. For TL specifically audit `softshell/gym/spa day/athleisure/tracksuit`.
- [ ] **Town/term collisions** — apply the own-town exemption (fix 4) and grep the CSV for
      names colliding with the TL bleed list.
- [ ] **Mixed-case towns** (`Newcastle upon Tyne`, `Stoke-on-Trent`, `Southend-on-Sea`,
      `Houghton le Spring`, `Bishop's Stortford`) need fix 3 or they render/match wrong.
- [ ] **Non-ASCII + bare `&` from agents**: pound sign (write "pound"), curly quotes,
      em-dashes (use " - "), and `&` ("B&B" -> "B and B"). Pre-flight catches them.
- [ ] **Nearby must be on the CSV and geographic.** Pre-assign LOCKED triples; validate with
      `next_towns --check`. Isolated towns (Aberdeen, Norwich, Elgin, Plymouth, Inverness,
      Carlisle) have few on-list neighbours — pick the closest available and accept the distance.
- [ ] **Disambiguation:** `Newport` (Gwent, Wales) vs `Newport (Isle of Wight)` — use the
      full parenthetical key/spelling; they must produce distinct slugs. `Chapeltown` = the
      Sheffield one. `Rothwell` = W.Yorks (near Leeds). `Blackwood` = Gwent. `Fulwood` =
      Preston. `Sutton` vs `Sutton Coldfield` vs `Sutton-in-Ashfield`. `Stanley`/`Hythe`/
      `Ripley`/`Bangor` have multiple UK instances — tell the agent which. **The Isle of
      Wight cluster (Newport (IoW), Ryde, Cowes, Shanklin, Sandown) cross-links only within
      the island.** London boroughs need London-area nearby.
- [ ] **Don't spawn sub-agents** from research agents (slow, confusing completion signals).
- [ ] **md5 selector only** in `pick()` — never crc32. Verify the seed rebuilds
      byte-identical before scaling.
- [ ] **Link-bearing pools carry a fixed link count** — any new prose variant added to a
      pool containing an `iNeedWorkwear` link must carry the same count.
- [ ] **`outputs/`, `dist/`, `__pycache__/` gitignored**; commit `towns/*.json` + generator
      per batch; pages regenerate deterministically so built HTML need not live in git.
- [ ] **Don't chase the 77% overall-unique floor** — it's unreachable; the pair cap is the gate-adjacent guard.

---

## 9. Resume / reproduce
- Progress = membership of `TOWNS` (seed literal + `towns/*.json`). After any reset,
  `next_towns.py` reports done/left and `--slugs N` emits the next N. The build is
  deterministic, so a re-run reproduces byte-identical pages.
- Deliverables: `dist/tl-pages-505.zip` (built HTML) + optionally `dist/tl-kit.zip`
  (generator + gates + helpers + flagship + CSV + docs + all town JSON). Final report ->
  `BUILD_REPORT.md`.

### CH2 final scoreboard (your target shape)
505/505 verify PASS · worst pair 50.9% (cap 52%, 0 over-cap) · 0 dead links ·
overall-unique 66.0% (diagnostic) · ~2.4M words · seed + 10 batches of ~56.
