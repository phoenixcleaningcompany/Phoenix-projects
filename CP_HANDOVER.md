# CP (Corporate & Professional Services) — build handover

You're building **CP**, a 505-page town series (504 UK towns + a London flagship), the
**same scaffold** as TL (Travel/Tourism/Leisure), CH2 (Charity) and TC (Telecoms). This
doc is the distilled playbook from the **TL build**: what to reuse verbatim, the fixes
that are already baked into the kit, the **duplicate-content changes to keep from the
start**, the bugs that cost time and how they were fixed, and the series-specific layer
you must re-derive for CP. Read TL's `SPEC.md`, `CLAUDE.md` and `BUILD_REPORT.md` next to this.

---

## 0. TL;DR
- **Clone the TL kit, not CH2.** TL already has all 7 historic kit-fixes PLUS the
  duplicate-content upgrades baked in. Rename `tl`/`tl-`/`TL_` -> `cp`/`cp-`/`CP_`, then
  rewrite only the **series-specific content layer** (§5).
- Keep the **4-local-paragraph depth** and the **machine-enforced depth gate** from page 1
  (§3) — that is the anti-thin-content + anti-duplicate lever, and it is the single most
  important thing to carry over.
- Reuse the **`AGENT_BRIEF.md` single-source-of-truth** pattern and the **locked-nearby-triples**
  (the geography is identical — you can lift every triple straight from TL's `towns/*.json`, §8).
- Build rhythm: **seed (~2) + a 15-town test batch for sign-off + 9 batches of ~56**
  (8 agents x 7 towns). Per batch: research -> pre-flight -> build -> `verify` N/N -> `score` -> commit+push.
- Gate that matters: **`verify` 100%** and **worst pair <= 52%**. Overall-unique "BELOW
  FLOOR" is expected and fine. TL final shape: **505/505 verify, worst pair 51.7%, 0 dead links.**

---

## 1. Clone the kit (files to copy from the TL build)
| File | Reuse | Action for CP |
|---|---|---|
| `tl_build.py` | Structure 100% | rename -> `cp_build.py`; rewrite prose pools + leads + schema strings + SVG swaps + seed `TOWNS` |
| `verify_tl.py` | Logic 100% | rename -> `verify_cp.py`; swap `LEAD/CO_LEAD/TRI_LEAD`, the `BLEED` list, link counts, slug prefix |
| `preflight_tl.py` | **Keep verbatim** | rename; swap the `BLEED` list + glob; **keep the DEPTH gate (§3)** |
| `next_towns.py` | **Keep verbatim** | rename; swap prefix |
| `score_tl.py` / `diag_tl.py` | **Keep verbatim** | rename; swap the `CHROME` class list to your CSS prefix |
| `AGENT_BRIEF.md` | Pattern 100% | rewrite the field spec + example for the CP angle (§3, §5) |
| `tl-london.html` | Template | **hand-author `cp-london.html`** (the ONE general-knowledge flagship); chrome is extracted from it |
| `TL_towns.csv` | **Identical** | reuse verbatim as `CP_towns.csv` (same 505 rows) |

---

## 2. Already baked into the TL kit (do NOT re-discover — just keep)
These were the 7 historic fixes; in TL they are already implemented, so cloning TL gets them free:
1. **Output-dir fallback** (`CP_OUTDIR` / `outputs`) in `main()`.
2. **`towns/*.json` batch loader** (`_load_extra_towns`) merged into `TOWNS`.
3. **Slug-robust display + lookup** (`town_display` / `_entry`) — needed for `Newcastle upon Tyne`,
   `Stoke-on-Trent`, `Houghton le Spring`, `Bishop's Stortford`, `Newport (Isle of Wight)`.
4. **Own-town bleed exemption** in `verify` (a page may legitimately contain its own town name
   even if it collides with a bleed word). NOTE: this exempts the **page's own town only** — not
   nearby towns or other real place-names (see the bug log, §4).
5. **`next_towns.py`** resume-safe planner (`N` / `--slugs N` / `--done` / `--check`).
6. **Widened section pools 4->6** (zero-link pools only, link counts preserved) + `snapshot`/`kit_loc`
   template fallbacks so batch JSON only needs genuinely-local fields.
7. **Pre-flight scanner** (`preflight_*.py`) catching non-ASCII, bare `&`, missing fields, shape,
   bleed, off-CSV nearby.

---

## 3. THE duplicate-content + thin-content changes — KEEP FROM PAGE 1
This is what the TL build added on top of the historic kit, and the part you specifically want to carry over.

**(a) FOUR local paragraphs per town, not 2-3.** At 505 pages the pooled scaffold means
~85-90% of each page's body is shared boilerplate; the genuinely-unique part is the local
`s1loc` block + town-name swaps + title/meta/H1/4x JSON-LD/nearby. Going from 3 -> **4
proper-noun-rich local paragraphs (~260 unique words/page)** lifted per-page unique body
shingles from ~11% to ~14% and held the worst pair under the 52% near-dup cap. `s1_paras`
appends the pooled paragraphs after the local ones, so a 4-element `s1loc` just works.
Use **4 distinct angles** so the paragraphs don't overlap each other:
  1. the town's marquee draw / scale of the relevant economy,
  2. the second layer of named venues/sites,
  3. heritage/culture/named quarters,
  4. the trade itself (employers, transport, the surrounding catchment).
(Re-cast these four angles for CP — see §5.)

**(b) Machine-enforce the depth in pre-flight** so a thin town is rejected *before build*,
not hoped-for. The TL gate (calibrate to your own batch-1 floor, set thresholds safely below it):
```python
S1LOC_PARAS = 4
PARA_MIN_WORDS = 50          # each paragraph
TOTAL_MIN_WORDS = 235        # all four combined (TL towns landed ~250-320)
PROPER_NOUN_MIN = 35         # heuristic; SEE the undercount note below
```
Proper-noun heuristic = capitalised words (len>1) not at sentence start. It **undercounts
multi-word names** ("Yorkshire Waterways Museum" counts as 3, a human reads 1 name), so set
the threshold with margin and don't chase it — 35 worked; small towns occasionally need a
one-clause enrichment to clear it.

**(c) `AGENT_BRIEF.md` as the single source of truth.** Write the full research spec ONCE
(fields, the 4-angle rule, the hard rules, the depth target, one worked example), commit it,
then give each batch-agent a SHORT prompt: "read AGENT_BRIEF.md, batch=bNN group=gX, write
`towns/bNN_gX.json`, here are your 7 towns + locked triples." This cut per-agent prompt size
massively and kept 80 agents consistent across 10 batches.

**(d) Keep the widened 6-variant pools** and don't shrink any pool. The pair cap is the guard;
more variants = lower collision.

**Reality check (set expectations):** even with all this, overall-unique reads ~66-69% ("BELOW
FLOOR") — that is the pooled-scaffold ceiling at 505 pages and is fine. The deliverable guards
are `verify` 100% and worst pair <= 52%. If the client needs *higher* genuine uniqueness, the
only real lever is **more unique local content** (5 paragraphs, or vary more shared sections per
town) — flag that as a cost/► time trade before scaling, don't silently accept dup risk.

---

## 4. Bug / trap log from the TL build (each cost time — pre-empt them)
- [ ] **Real place-names that collide with bleed words — THE #1 time-sink.** The own-town
      exemption (fix 4) only covers the page's OWN town. Real local names in `s1loc` still trip
      the bleed scan. TL hits and their fixes (rephrase to an equally-accurate alternative, never
      a generic):
      - "**Wellington**" everywhere — Wellington College (Crowthorne/Sandhurst), the Wellington
        Statue (Aldershot), Wellington Country Park (near Sandhurst/Reading), a Wellington district
        (Telford). Fixes: "Iron Duke statue", "California Country Park", name a different nearby draw.
      - "**matchday**" (a sports-bleed word) — agents reach for it on stadium paras; ban it explicitly,
        tell them to write "home games"/"fixtures".
      - "**Stockroom**" (a Stockport cultural venue) tripped the retail "stockroom" bleed -> "cultural venue".
      - "**St Mary of Charity**" (Faversham's church) tripped "charity" -> "St Mary".
      - "**volunteer** crews" (RNLI) tripped "volunteer" -> "crews".
      **Mitigation:** in every agent prompt, explicitly list the handful of bleed words most likely to
      surface as real names for that batch's region (sports/charity/retail/care terms), and tell agents
      to avoid them. Then the pre-flight `BLEED` scan + a quick `python3` rephrase catches the stragglers.
- [ ] **Re-read agent files AFTER the completion notification, not mid-run.** Agents self-correct on
      their final write; an early read can show content they later fixed (caused a phantom "bleed" chase in TL).
- [ ] **One pair can drift over 52%** as N grows (TL: Derby vs Gateshead hit 52.2% on pooled-boilerplate
      alignment). Fix = `diag` the pair, add ONE researched proper-noun-rich paragraph to the **weaker**
      page's `s1loc`. Do not reword distinctive local prose to generic. With 4 paras from batch 1 this is rare.
- [ ] **Small towns** (new towns, commuter suburbs, Black Country towns) run short on named places —
      enrich with real adjacent parks/halls/heritage to clear the proper-noun floor.
- [ ] **Non-ASCII + bare `&`**: pound sign (write "pound"), curly quotes, em-dashes (use " - "), and
      `&` ("B and B", "Marks and Spencer"). Pre-flight catches them; tell agents up front.
- [ ] **Link-bearing pools carry a FIXED link count** — when you add a prose variant to a pool that
      contains an `iNeedWorkwear` link, it must carry the same count or the exact-link-count check fails.
      In TL only the zero-link pools (EMB/ACC/ORD) were widened for this reason.
- [ ] **md5 selector only** in `pick()` — never crc32. Verify the seed rebuilds byte-identical before scaling.
- [ ] **`outputs/`, `dist/`, `__pycache__/` gitignored**; commit `towns/*.json` + generator per batch.
- [ ] **Commits show "Unverified" on GitHub** — the env's commit-signing key is an empty placeholder.
      Author/committer are correct (`Claude <noreply@anthropic.com>`); it's only the missing signature
      and is not fixable without a real key registered to the account. Cosmetic; don't loop on it.

---

## 5. SERIES-SPECIFIC — re-derive ALL of this for CP (do NOT copy TL's content)
The scaffold is shared; the content layer is not. Derive from the **CP SPEC / matrix row**.
- **Lead products.** Corporate/professional dress is more formal than TL. Likely leads:
  branded **business shirts/blouses + knitwear/pullovers + softshell**, plus polos, tailored
  fleeces, blazers/jackets, ties/scarves, lanyards and embroidered logos. Set `LEAD/CO_LEAD/TRI_LEAD`
  and the 8 product cards from the CP matrix row (TL led polo+fleece+softshell — CP will differ).
- **The BLEED list — INVERTED vs your own core (the biggest trap).**
  - **Remove** CP core terms from the inherited list so they don't fail every CP page: likely
    `shirt`, `blouse`, `knitwear`, `tie`, `blazer`, `corporate`, `office`, `professional`, `lanyard`,
    `suit`/`suiting` (whichever CP uses).
  - **Add the other series' signatures as CP bleed** so CP can't drift: TL's `tourism`, `attraction`,
    `theme park`, `holiday park`, `activity centre`, `visitor`, `seaside`, `pier`; CH2's `charity`,
    `volunteer`, `foodbank`; TC's `telecoms/fibre/broadband/Openreach`; plus the inherited
    security/cleaning/waste/highways/forestry/care/courier/salon/veterinary/sports bleed.
  - Rule of thumb: **if a new town trips bleed, first check it isn't your own CP core word.**
  - Re-audit town/term collisions against the CSV (TL's was `Wellington`; CP's own-town exemption
    must cover any town whose name equals a CP bleed term).
- **Identity / schema strings:** hero subtitle, h1/title template, CTA, section H2s, `serviceType`,
  `areaServed`, breadcrumb slug, Organization `knowsAbout`, FAQ set, stat chips, the `#contract`
  differentiator block, canonical domain path.
- **Posture.** Decide CP's two buyers and mirror the balance rule. Likely **Hybrid**: large
  corporates / professional-services groups on **managed trade accounts** (rollout across offices,
  new-starter onboarding, brand-guideline consistency) AND small independent firms ordering **direct
  online**. (TL framed this as park-vs-independent + seasonal; CP's equivalent is multi-office-rollout
  vs single-office, and "brand-consistent, client-facing" rather than "seasonal".)
- **The 4 local-paragraph angles, recast for CP** (the local content is the town's *business*
  economy, not its tourism): (1) the town's office/business core + scale (CBD, financial/legal
  quarter, key employers and sectors), (2) the business parks / enterprise zones / science & tech
  parks by name, (3) the professional-services and institutional layer (chambers of commerce, law/
  accountancy/consulting cluster, universities/research, civic and HQ buildings), (4) the wider
  catchment + transport (stations, motorways, airport, commuter belt). Keep them proper-noun-rich;
  use named districts/parks/institutions (avoid leaning on specific private firm names).
- **SVG scenes (5; town-swapped in assemble).** Re-skin palette and redraw for a corporate context
  (e.g. an office/city-skyline scene, a reception/lanyard scene, a "welcome to {TOWN}" business-park
  sign, a premises scene), and re-word every `aria-label`/caption the generator town-swaps. Keep the
  same swap points (`a {town} ... logo`, the sign text via `sign_town()`, the premises `across {town}`).
- **Palette + fonts.** The verifier only checks the **two font families** — pick CP fonts and wire the
  `@import` + the font check. Hex colours are not checked. (Corporate = restrained navy/grey/accent.)

---

## 6. Batch rhythm that worked (TL, 505/505, 0 rejected pages)
1. `python3 next_towns.py 56` -> next 56 by rank. Split into 8 groups of 7.
2. **Pre-assign each town a LOCKED nearby triple** (geographic, hand-verified, on-CSV) yourself.
   This was the single biggest reliability win: **0 off-list / dead links across 504 towns.** Do NOT
   let agents pick nearby. (For CP you can lift the triples straight from TL — §8.)
3. Dispatch **one `general-purpose` agent per group** (run async/background), each told to read
   `AGENT_BRIEF.md`, do real web research, write 4 local paragraphs, use the locked triple verbatim,
   name a nearby town in `s2_intro`, write its own `towns/bNN_gX.json`, **no sub-agents**, reply one line.
4. **Wait on the completion notifications + a file-count check** (`ls towns/bNN_*.json | wc -l`). Do NOT
   poll with `sleep`; do NOT read the agent transcript files (they overflow context).
5. **Pre-flight** the batch JSON (`preflight_cp.py 'towns/bNN_*.json'`) -> fix any bleed/depth flags.
6. `next_towns.py --check` (every nearby on CSV).
7. `CP_OUTDIR=outputs python3 cp_build.py` (no-arg builds all) -> `cp cp-london.html outputs/`.
8. `verify_cp.py outputs` -> **must be N/N PASS**; `score_cp.py outputs` -> worst pair <= 52%.
9. `git add towns/bNN_*.json cp_build.py && git commit && git push`. Next batch.
Cost: TL ran ~8 agents x ~45k tokens per batch x 10 batches. Budget for it.
**Always run a 15-town test batch first and get sign-off before the automated 9x56 run.**

---

## 7. Gates & scoring reality
- **`verify` is the contract** (16 hard checks): exact link counts (re-derive CP's `.com` + community
  count and keep link-bearing pools at a fixed count), no JS, no HTML entities, meta <=160 (no
  apostrophe), title <=60, town in title+h1, no delivery-timescale claims, lead trio present, 4 JSON-LD
  blocks, dead-link guard, bleed. Every page must pass.
- **`score` floors are diagnostics.** Overall-unique "BELOW FLOOR" (~66-69%) is expected at 505 pages.
  The **pair cap (52%) is the real near-dup guard.** A pair over 52% is the only score result you act on.

---

## 8. Reusable assets from TL (same CSV -> big time-savers)
- **Nearby triples are geographic and series-independent.** Lift every locked triple from the TL build's
  `towns/*.json` instead of re-deriving 504 of them:
  ```python
  import json, glob
  triples = {}
  for f in glob.glob('towns/*.json'):              # point at the TL build's towns/
      for town, v in json.load(open(f)).items():
          triples[town] = v['nearby']
  # -> hand to CP agents as the locked triple per town
  ```
- **Disambiguation list (same CSV, reuse):**
  - `Newport` (Gwent, Wales, rank 44) vs `Newport (Isle of Wight)` (rank 501) — distinct slugs; use the
    full parenthetical key for the IoW one verbatim.
  - **Isle of Wight cluster** (Newport (IoW), Ryde, Cowes, Shanklin, Sandown) cross-links ONLY within the island.
  - `Carlton` = the Nottingham/Gedling one; `Sutton` (London Borough) vs `Sutton Coldfield` vs
    `Sutton-in-Ashfield`; `Stanley` = County Durham; `Gosforth` = Newcastle suburb (not Cumbria);
    `Shipley` = West Yorks (Saltaire); `Newcastle upon Tyne` vs `Newcastle-under-Lyme`.
  - **Isolated towns** (few on-list neighbours — accept distance): Aberdeen, Norwich, Cambridge, Plymouth,
    Inverness, Carlisle, Elgin.
- **Mixed-case / punctuated towns** that need fix 3: `Newcastle upon Tyne`, `Stoke-on-Trent`,
  `Southend-on-Sea`, `Houghton le Spring`, `Bishop's Stortford`, `Barrow-in-Furness`, `Newport (Isle of Wight)`.

---

## 9. Definition of done
505/505 `verify` PASS · worst pair <= 52% (0 over-cap) · 0 dead links · ~1.8M words · seed + 10 batches.
Deliverables: `dist/cp-pages-505.zip` (built HTML) + `dist/cp-kit.zip` (generator + gates + helpers +
flagship + CSV + docs + all town JSON) + `BUILD_REPORT.md`. Build is deterministic — it reproduces byte-identical.
