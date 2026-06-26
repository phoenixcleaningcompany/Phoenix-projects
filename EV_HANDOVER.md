# EV (Entertainment, Events & Festivals) — build handover

You're building **EV**, a 505-page town series (504 UK towns + a hand-authored London
flagship), the **same scaffold** as CP (Corporate & Professional Services), which was just
delivered: **505/505 verify, worst pair 52.0%, 0 dead links, ~1.71M words, fully
deterministic.** This doc is the distilled playbook from the CP build — what to reuse
verbatim, the fixes already baked into the kit, the duplicate-content levers to keep from
page 1, the bugs that cost time, and the EV-specific layer you must re-derive.

Read CP's `SPEC.md`, `CLAUDE.md`, `BUILD_REPORT.md` and `AGENT_BRIEF.md` next to this.

---

## 0. TL;DR
- **Clone the CP kit, not an older one.** CP already has every hardening fix below baked in.
  Rename `cp`/`cp-`/`CP_` -> `ev`/`ev-`/`EV_`, then rewrite ONLY the series-specific content
  layer (§5) and **invert the BLEED list** (§5 — the single biggest EV-specific trap).
- Keep the **2-local-paragraph baseline + the 3rd-paragraph enrichment remedy** (§3). That is
  the anti-duplicate lever and the single most important thing to carry over.
- Reuse the **locked nearby triples** straight from CP's `towns/*.json` (geography is
  identical and series-independent — §8). Hand-author/validate them yourself; do NOT let
  agents pick nearby.
- Build rhythm: **seed (2) + a 15-town test batch for sign-off + 9 batches of ~56**
  (8 agents x 7 towns; last batch 39). Per batch: locked triples -> research agents write
  `towns/bNN_gX.json` -> `preflight` -> build -> `verify` N/N -> `score` <= 52% -> commit+push.
- Gates that matter: **`verify` 100%** and **worst pair <= 52% (0 strictly over cap)**.
  Overall-unique "BELOW FLOOR" (~60-66%) is expected and fine.

---

## 1. Clone the kit (files to copy from the CP build)
| File | Reuse | Action for EV |
|---|---|---|
| `cp_build.py` | Structure 100% | rename -> `ev_build.py`; rewrite prose pools + leads + schema strings + SVG swaps + seed `TOWNS`; **invert BLEED-driven copy** |
| `verify_cp.py` | Logic 100% | rename -> `verify_ev.py`; swap `LEAD/CO_LEAD/TRI_LEAD`, the `BLEED` list, link counts, slug prefix, the CSV name |
| `preflight_cp.py` | **Keep; depth gate already 2-3 paras** | rename; swap the `verify` import name + the CSV name |
| `score_cp.py` / `diag_cp.py` | **Keep** | rename; swap the `CHROME` CSS-class list to your `ev-` prefix, and the `score_*` import in diag |
| `AGENT_BRIEF.md` | Pattern 100% | rewrite the field spec + the BLEED list + the worked angles for the EV posture |
| `cp-london.html` | Template | **hand-author `ev-london.html`** (the ONE general-knowledge flagship); chrome is extracted from it |
| `CP_towns.csv` | **Identical** | reuse verbatim as `EV_towns.csv` (same 505 rows) |
| `towns/*.json` | **nearby field only** | lift the locked triple per town; rewrite all prose (§8) |

Slug prefix is referenced in: `verify_*` (the `cp-` regexes for links/dead-links/find_town),
`score_*`/`diag_*` (`cp-*.html` globs + CHROME classes), and `*_build.py` (`ev-<slug>.html`,
the `cp-` nearby links, canonical paths). Grep the whole kit for `cp-` and `CP_` before you
build.

---

## 2. Already baked into the CP kit (do NOT re-discover — just keep)
These were added DURING the CP build and are the reason it scaled cleanly:
1. **Canonical display names** (`town_display()` / `_entry()` in `*_build.py`). Naive
   `' '.join(w.capitalize() ...)` mangles 23 towns ("Newcastle Upon Tyne",
   "Stoke-on-trent", "Weston-super-mare", "Newport (isle Of Wight)"). `town_display(key)`
   looks the canonical spelling up from the CSV by slug; `_entry(town)` does a slug-robust
   `TOWNS` lookup so any key spelling resolves. **Keep both** — they cost a day in CP.
2. **Own-town BLEED exemption** in `verify` check 10 and in `preflight`: a page may contain
   its OWN town name even if it equals a bleed term (CP: Wellington town vs `wellington`
   bleed). EV will have its own collisions — re-audit town names vs your new bleed list.
3. **`_load_extra_towns()`** merges per-batch `towns/*.json` into `TOWNS` (the seed stays
   inline; batches are JSON files). This is what keeps per-batch commits clean and keeps
   agent output out of your context.
4. **`preflight_*.py`** batch validator: ASCII-only, bare `&`, HTML entities, BLEED (own-town
   exempt), nearby-on-CSV + not-self, key-on-CSV, and a depth band (`PARA_MIN/PARA_MAX`,
   **s1loc 2-3 paragraphs**). Run it on every batch BEFORE building.
5. **`CP_OUTDIR` / `outputs` fallback** in `main()` (defaults to `/mnt/user-data/outputs`,
   honours an env override, falls back to `./outputs`). Output dir doesn't affect bytes.
6. **md5 selector only** in `pick()` (never crc32). Verify the seed rebuilds byte-identical
   before scaling — CP reproduced both golden seed pages exactly.

---

## 3. THE duplicate-content lever — KEEP FROM PAGE 1
The genuinely-unique part of each page is the local `s1loc` block + town-name swaps +
title/meta/H1/4x JSON-LD/nearby. Everything else is pooled boilerplate (~85% of the body).

**(a) 2 local proper-noun-rich paragraphs per town as the baseline.** `s1_paras()` appends
the pooled paragraphs after the local ones, so a 2-element `s1loc` "just works". Each para
55-90 words, factually researched, named places/orgs. (CP's SPEC set 2; if EV's matrix row
says more, follow it — but the remedy below matters more than the baseline.)

**(b) The 3rd-paragraph enrichment remedy — this is how you clear the pair cap.** As N grows,
specific pairs drift over 52% on pooled-boilerplate alignment. The fix that worked 25 times in
CP: `diag` the pair, then add **ONE researched, proper-noun-rich 3rd paragraph (~65-120 words)
to the weaker (smaller-rank) page's `s1loc`** — real local business/venue detail, NEVER
reword distinctive prose to generic. The kit's `preflight` already accepts **2-3 paragraphs**
so enriched entries still pass. One enrichment typically moves a pair 2-4 points and can
surface a new ~52.0 pair (whack-a-mole near the ceiling) — that's normal; stop once **0 pairs
are strictly over 52.0**.

**(c) `AGENT_BRIEF.md` as the single source of truth.** Write the full spec ONCE (fields,
the s1loc shape, the hard rules + BLEED list, one worked example), commit it, then give each
batch-agent a SHORT prompt: "read AGENT_BRIEF.md, write `towns/bNN_gX.json`, here are your 7
towns + locked triples". This kept ~70 agents consistent across 9 batches.

**(d) Keep the widened pools** (CP: TRUST 4, S2INTRO 4, EMB/CON/ACC/WHY/ORD 4-6, OWNER/
PRESENT/NARROW/KIT 5-6, FAQ 7x6, product cards 3-way via `build_grid`). More variants = lower
collision. Link-bearing pools carry a FIXED link count (see §7).

**Reality check:** overall-unique reads ~60-66% ("BELOW FLOOR") at 505 pages. That is the
pooled-scaffold ceiling and is FINE. The pair cap (<=52%, 0 over) is the real guard. If the
client wants higher genuine uniqueness, the only lever is more unique local content (3-4 paras
everywhere) — flag it as a cost/time trade before scaling.

---

## 4. Bug / trap log from the CP build (each cost time — pre-empt them)
- [ ] **Stale read: build AFTER all completion notifications, never mid-run.** CP's final
      full build was kicked off the moment entry-count hit the target, but two agents were
      still doing their final write — one page (`cp-neston`) baked in a pre-final sentence and
      broke byte-identical determinism. Fix: wait for ALL 8 completion notifications + a file
      AND entry-count check, then do a CLEAN full rebuild before packaging. Re-run the
      determinism check (`CP_OUTDIR=/tmp/repro` build + `filecmp` vs outputs) at the very end.
- [ ] **Display-name bug (fixed, fix #1 above)** — naive capitalize() mangles hyphenated /
      particle towns. If you re-derive `main()`, keep `town_display()`/`_entry()`.
- [ ] **Real place-names that collide with bleed words — the #1 recurring snag.** The own-town
      exemption only covers the page's OWN town. Real local names in `s1loc` still trip the
      scan. In CP, agents reached for "Festival Park" (Stoke), "Wellington Street" (Sheffield),
      "St Mary of Charity" (Faversham) — all rephrased to equally-accurate alternatives. For EV
      these flip (festival/stage/crew become legal) but NEW collisions appear from your new
      bleed list (e.g. corporate/finance terms). **In every agent prompt, name the handful of
      bleed words most likely to surface as real names for that batch's region, and tell agents
      to dodge them.** Preflight catches stragglers.
- [ ] **Bleed scan is substring-naive in ad-hoc greps, word-boundary in the gates.** Agents
      kept "flagging" `occu**pier**s`, `**spa**ce`, `aero**space**`, `**Crew**e`,
      `**stage**coach`. The real `verify`/`preflight` use `\b...\b`, so these are NON-issues.
      Don't chase them.
- [ ] **Link-bearing pools carry a FIXED link count.** When you add a prose variant to a pool
      containing an iNeedWorkwear link, it must carry the same count or the exact-link-count
      check fails. CP's link-bearing pools: CON_P3=1, ACC_P4=2, SELF=1, SORTED=1; everything
      else zero-link. Re-derive EV's split and keep it constant.
- [ ] **Disambiguation (same CSV):** two `Newport`s (Gwent rank 44 = key `newport`; Isle of
      Wight rank 501 = key `newport (isle of wight)` verbatim, slug `newport-isle-of-wight`).
      IoW cluster (Newport (IoW), Ryde, Cowes, Shanklin, Sandown) cross-links ONLY within the
      island. Also: `Carlton`=Gedling/Notts; `Sutton` (London) vs `Sutton Coldfield` vs
      `Sutton-in-Ashfield`; `Stanley`=Co Durham; `Gosforth`=Newcastle suburb (not Cumbria);
      `Shipley`=West Yorks; `Rothwell`=Leeds (LS26); `Chapeltown`=Sheffield; `Hythe`=Kent;
      `Newcastle upon Tyne` vs `Newcastle-under-Lyme`; `Wellington`=Somerset.
- [ ] **Isolated towns** (few on-list neighbours — accept distance): Aberdeen, Norwich,
      Cambridge, Plymouth, Inverness, Carlisle, Elgin, Dumfries, Bangor, Skegness, Barnstaple.
- [ ] **`outputs/`, `dist/`, `__pycache__/` gitignored**; commit `towns/*.json` + generator
      + gates per batch. The built HTML is NOT committed (regenerated deterministically).
- [ ] **Commits show "Unverified" on GitHub** — the env's signing key is a placeholder.
      Cosmetic; don't loop on it.

---

## 5. SERIES-SPECIFIC — re-derive ALL of this for EV
The scaffold is shared; the content layer is not. Derive from the EV SPEC / matrix row.

- **The BLEED list — INVERTED vs CP (the biggest trap).**
  - **REMOVE the EV signatures CP blocked** so they don't fail every EV page: `festival`,
    `stage`, `crew`, `rigging`, `front-of-house`, `steward`, `concert`, plus `event`-family
    terms EV needs. These are EV CORE now.
  - **ADD CP's signatures as EV bleed** so EV can't drift into the corporate series:
    `corporate`, `professional services`, `account-managed`, `managed account`, `brand pack`,
    `away day`, `procurement`, `law firm`, `accountancy`, `consultancy` (whichever CP owned).
  - **KEEP the other series' signatures blocked**: TL tourism/theme park/holiday park/activity
    centre/tour operator/visitor/seaside/pier; CH2 charity/foodbank/volunteer; TC telecoms/
    fibre/broadband/Openreach; VT veterinary/scrubs/kennel/cattery/equine; BH barber/spa day/
    clog/hoodie; plus the inherited security/cleaning/waste/highways/forestry/care/courier/
    retail/sports (matchday/gym/tracksuit) bleed. Trim any that are genuinely EV-core.
  - Rule of thumb: **if a new town trips bleed, first check it isn't your own EV core word.**
  - **Re-audit town/term collisions** against the CSV for your NEW bleed list (CP's was
    `wellington`; EV's own-town exemption must cover any town whose name equals an EV bleed
    term).
- **Lead products.** EV (events/festivals/entertainment crews) differs from CP's polo/
  softshell/fleece. Likely leads: **hi-vis / event crew tees / softshell / hoodies /
  bomber jackets / lanyards / wristbands / staff/security ID**, plus stage-crew blacks.
  Set `LEAD/CO_LEAD/TRI_LEAD` and the 8 product cards from the EV matrix row.
- **Posture.** Decide EV's buyer(s) and mirror the balance rule. Likely event production
  companies / festival organisers / venues / AV-staging crews / promoters, ordering crew kit
  for a run of dates — recast CP's "managed account, brand exercise" framing into EV's
  equivalent (per-event / per-season crew kit, fast turnaround for a tour or festival run).
- **The local-paragraph angles, recast for EV:** (1) the town's marquee venues / arenas /
  festival sites and the scale of its events economy; (2) the second layer of named
  venues/theatres/conference centres; (3) the production/AV/staging/promoter cluster and
  civic events; (4) the catchment + transport feeding crews and audiences. Proper-noun rich,
  named venues/sites (avoid leaning on private firm names except in the flagship/local-para
  exception).
- **Identity / schema strings:** hero subtitle, h1/title template, CTA, section H2s,
  `serviceType`, `areaServed`, breadcrumb slug, Organization `knowsAbout`, FAQ set, stat
  chips, the `#contract` differentiator block, canonical domain path.
- **SVG scenes (5; town-swapped in assemble).** Re-skin palette and redraw for an events
  context (e.g. a stage/rig scene, a crew/lanyard scene, a "welcome to {TOWN}" event-site
  sign, a venue scene, an order-online laptop). Re-word every `aria-label`/caption the
  generator town-swaps. Keep the same swap points (`a {town} ... logo`, the sign text via
  `sign_town()`, the premises `across {town}`).
- **Palette + fonts.** The verifier only checks the **two font families** — pick EV fonts and
  wire the `@import` + the font check. Hex colours are not checked.

---

## 6. Batch rhythm that worked (CP, 505/505, 0 rejected pages)
1. Take the next 56 towns by rank. Split into 8 groups of 7 (last batch 39 = 6 groups).
2. **Pre-assign each town a LOCKED nearby triple** (geographic, hand-verified, on-CSV) yourself,
   and validate the whole set against the CSV in one script BEFORE dispatch. This was the
   single biggest reliability win: **0 off-list / dead links across 504 towns.** Do NOT let
   agents pick nearby. (Lift the triples from CP's `towns/*.json` — §8.)
3. Dispatch **one general-purpose agent per group (async/background)**, each told to read
   `AGENT_BRIEF.md`, do real web research, write 2 local paragraphs, use the locked triple
   verbatim, write its own `towns/bNN_gX.json`, **no sub-agents**, reply one line (the count).
4. **Wait on ALL completion notifications + a file-count AND entry-count check.** Do NOT poll
   with `sleep`; do NOT read agent transcript files (they overflow context).
5. **Preflight** the batch JSON (`preflight_ev.py 'towns/bNN_*.json'`) -> fix any flags.
6. Build (no-arg builds all), `cp ev-london.html outputs/`.
7. `verify_ev.py outputs` -> **must be N/N PASS**; `score_ev.py outputs` -> worst pair <= 52%.
8. If a pair is over cap: `diag_ev.py` it, enrich the weaker page's `s1loc` with a 3rd
   researched paragraph (§3b), rebuild those towns, rescore.
9. `git add towns/bNN_*.json *_build.py && commit && push`. Next batch.
Cost: CP ran ~8 agents x ~38-45k tokens per batch x 9 batches. Budget for it.
**Always run a 15-town test batch first and get sign-off before the automated 9x56 run.**

---

## 7. Gates & scoring reality
- **`verify` is the contract** (16 hard checks): exact link counts (re-derive EV's `.com` +
  community count and keep link-bearing pools at a fixed count), no JS, no HTML entities, meta
  <=160 (no apostrophe), title <=60, town in title+h1, no delivery-timescale claims, lead trio
  present, 4 JSON-LD blocks, dead-link guard (`ev-` on CSV), bleed (own-town exempt). Every
  page must pass.
- **`score` floors are diagnostics.** Overall-unique "BELOW FLOOR" (~60-66%) is expected. The
  **pair cap (52%) is the real near-dup guard** — a pair strictly over 52% is the only score
  result you act on. CP converged at worst pair 52.0% with 0 strictly over.

---

## 8. Reusable assets from CP (same CSV -> big time-savers)
- **Nearby triples are geographic and series-independent.** Lift every locked triple from the
  CP build's `towns/*.json` (the `nearby` field) instead of re-deriving 504 of them:
  ```python
  import json, glob
  triples = {}
  for f in glob.glob('towns/*.json'):          # point at the CP build's towns/
      for town, v in json.load(open(f)).items():
          triples[town] = v['nearby']
  # London/Birmingham/Leeds nearby live inline in cp_build.py's TOWNS seed:
  #   London -> Croydon/Bromley/Ilford ; Birmingham -> Solihull/West Bromwich/Walsall ;
  #   Leeds -> Bradford/Pudsey/Dewsbury
  # -> hand each EV agent the locked triple per town
  ```
  Re-validate them on `EV_towns.csv` (identical rows) before dispatch, and re-check the
  own-town/bleed audit against your NEW EV bleed list.
- **Mixed-case / punctuated towns** that rely on the display fix (#1): Newcastle upon Tyne,
  Stoke-on-Trent, Southend-on-Sea, Weston-super-Mare, Houghton le Spring, Bishop's Stortford,
  Barrow-in-Furness, Newport (Isle of Wight), Stratford-upon-Avon, Newcastle-under-Lyme, and
  ~13 more hyphen/particle towns.

---

## 9. Definition of done (what CP hit — match it)
505/505 `verify` PASS · worst pair <= 52% (0 strictly over) · 0 dead links · ~1.7M words ·
deterministic byte-identical rebuild · seed reproduces the golden pages exactly.
Deliverables: `dist/ev-pages-505.zip` (built HTML) + `dist/ev-kit.zip` (generator + gates +
helpers + flagship + CSV + docs + all town JSON) + `BUILD_REPORT.md`.
CP final shape for reference: **505/505 verify, worst pair 52.0%, 0 over-cap, 0 dead links,
1,708,630 words, 25 pages given a 3rd enrichment paragraph, fully deterministic.**
