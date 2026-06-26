# CH2 (Charities & Volunteer Orgs) — build handover

You're building **CH2**, a 505-page town series (504 UK towns + a London flagship),
the **same scaffold** as TC (Telecoms). This doc is the distilled playbook from the
TC build: what to reuse, the bug fixes to apply **from the start**, what is
**series-specific and must be re-derived**, the batch rhythm that worked, and the
traps that cost time. Read TC's `tc/SPEC.md`, `tc/CLAUDE.md` and `tc/BUILD_REPORT.md`
alongside this.

---

## 0. TL;DR
- Clone the TC kit, rename `tc`/`tc-`/`TC_` → `ch2`/`ch2-`/`CH2_`, rewrite the
  **series-specific** layer (copy, leads, bleed list, schema strings, SVGs, palette).
- Apply the **4 kit fixes** below before building a single batch (they are
  environment/architecture fixes, series-agnostic).
- Build in **10 batches** (seed 2 + 9×~56), population-rank order, London last.
- Per batch: 8 parallel research agents each **write a validated JSON file** →
  pre-flight scan → build → `verify` (binding gate, must be N/N) → `score` (pair
  cap is the real guard) → commit + push.
- Gate that matters: **`verify` 100%** and **worst pair ≤ cap**. The overall-unique
  "floor" (77%) is a diagnostic and is **not reachable** at 505 pages — don't chase it.

---

## 1. Kit anatomy (what each file is)
| File | Role |
|---|---|
| `ch2-london.html` | Hand-authored flagship. Chrome (header/footer/CSS/SVGs/contact) is **extracted from it** by the generator. Never rebuild it after authoring. |
| `ch2_build.py` | Generator. md5-hashed prose pools + per-town `TOWNS` dict → one `ch2-<slug>.html` per town. |
| `verify_ch2.py` | **The binding gate** — 16 hard checks. Run before every delivery; never ship a FAIL. |
| `score_ch2.py` / `diag_ch2.py` | Uniqueness diagnostics (NOT a gate). diag isolates what an over-cap pair shares. |
| `CH2_towns.csv` | 505 rows (Rank, Town, Population, Nation). **Identical list to TC** — reuse it. |
| `next_towns.py` | Batch planner/validator (resume-safe; `--check` validates nearby, `--done`, `--slugs`). |
| `PROMPT_TEMPLATE.md` | The research-agent spec (allowed-town list + schema + hard rules + style gold). |
| `towns/*.json` | Per-batch town data, merged into `TOWNS` at import. |

---

## 2. THE 4 KIT FIXES — apply before building (series-agnostic)
These were missing/needed in the handover copy and cost time. Bake them in first.

**(a) Output-dir fallback.** The original `main()` hardcoded `/mnt/user-data/outputs`,
which does not exist on a fresh checkout and crashes the build. Replace with:
```python
outdir = (os.environ.get('CH_OUTDIR')
          or ('/mnt/user-data/outputs' if os.path.isdir('/mnt/user-data/outputs')
              else 'outputs'))
os.makedirs(outdir, exist_ok=True)
```

**(b) CSV display-casing + slug-robust TOWNS lookup.** Naive `title()` mangles
`Newcastle upon Tyne` → "Upon", and breaks `Stoke-on-Trent`, `Houghton le Spring`,
`Bishop's Stortford`. Derive the display name from the CSV row, and look TOWNS up by
slug (tolerant of space/hyphen/case):
```python
_DISPLAY=None
def _display_map():
    global _DISPLAY
    if _DISPLAY is None:
        _DISPLAY={slugify(t): t for (_r,t,_n) in _load_csv()}
    return _DISPLAY
def town_display(key):
    return _display_map().get(slugify(key)) or ' '.join(w.capitalize() for w in key.split())
def _entry(town):
    s=slugify(town)
    for k,v in TOWNS.items():
        if slugify(k)==s: return v
    raise KeyError(town)
```
Use `T=_entry(town)` in `assemble()`, and in `main()` resolve `town=town_display(arg)`,
`slug=f"ch2-{slugify(arg)}"`, gate on `slugify(arg) in {slugify(k) for k in TOWNS}`.
**Without this you must defer all mixed-case towns; with it they just work.**

**(c) JSON batch loader.** Don't grow a 4,000-line Python literal by hand-splicing 56
entries per batch (error-prone). Keep the seed (~2 towns) in the literal; load the rest
from `towns/*.json`:
```python
def _load_extra_towns():
    here=os.path.dirname(os.path.abspath(__file__))
    d=os.path.join(here,'towns')
    if not os.path.isdir(d): return
    for fn in sorted(os.listdir(d)):
        if fn.endswith('.json'):
            for k,v in json.load(open(os.path.join(d,fn),encoding='utf-8')).items():
                TOWNS[k.lower()]=v
_load_extra_towns()  # call right after the TOWNS literal
```
Same data in → same pages out (pick() is md5-keyed on town name; dict order is
irrelevant). This let **research agents write their own JSON files** — the single
biggest efficiency win of the TC build.

**(d) Own-town bleed exemption in `verify`.** A town can be legitimately named like a
bleed term (TC: **Wellington**, Somerset — `wellington` is a TC bleed word). Exempt the
page's **own** town from the bleed scan; the term still fails on every other page:
```python
town_l = (town or "").lower()
hit = [term for term in BLEED
       if term.lower() != town_l
       and re.search(r"\b" + re.escape(term) + r"\b", txt, re.I)]
```
For CH2, check the CSV for towns whose names collide with your CH2 bleed list and confirm
this exemption covers them (it matches on the full town name; multi-word collisions like
"X Centre" would need the term phrased to not be a bare town-name substring).

---

## 3. SERIES-SPECIFIC — re-derive ALL of this for CH2 (do NOT copy from TC)
The scaffold is shared; the **content layer is not**. Re-derive:

- **Lead products** (TC = polo + hi-vis + softshell). CH2 is charity/volunteer wear —
  likely **polo + t-shirt + tabard** (charity-shop tabards) and/or hi-vis for
  fundraisers/marshals, fleeces, hoodies, aprons. Set `LEAD/CO_LEAD/TRI_LEAD` and the
  8 product cards accordingly.
- **The BLEED list — THIS IS THE BIGGEST TRAP.** The bleed list is *per series* and is
  **inverted** relative to your own core vocabulary:
  - **Remove** CH2's own core terms from the inherited list. **`tabard` and `hoodie` are
    BLEED in TC but are almost certainly CORE in CH2** — leaving them in would fail every
    CH2 page. Same for any charity-shop / volunteer vocabulary.
  - **Add** TC's core terms as CH2 bleed: `telecoms, network, fibre, broadband, CCTV,
    cabling, engineer, installer, Openreach, CityFibre, cabinet, EN ISO 20471, softshell`
    (if softshell isn't a CH2 lead), etc. — so CH2 pages can't drift into TC's voice.
  - Keep the other series' signatures blocked (security/cleaning/waste/highways/forestry/
    care/sports/retail/courier/salon/veterinary) **except** any that are genuinely CH2
    core (e.g. charity work may legitimately touch "care" or "community" — adjudicate).
  - Rule of thumb: **if a new town trips bleed, first check it isn't your own core word.**
- **Identity / schema strings**: hero subtitle, h1/title templates, CTA, section H2s,
  `serviceType`, `areaServed`, breadcrumb URL slug, Organization `knowsAbout`, FAQ set.
- **SVG scenes** (TC has 5: garment row, embroidery hoop, signpost, premises, order
  laptop). Re-skin palette + redraw the "premises" scene for a charity context (shop/
  community hall/event) and re-word every `aria-label` and caption that the generator
  town-swaps. Keep the embroidery scene generic (TC kept the realistic machine VT-only).
- **Palette + fonts.** Verifier only checks the **two font families** (TC: Lora + Source
  Sans 3) — pick CH2 fonts and wire the `@import` + the verifier's font check. Hex
  colours are not checked.
- **Posture** (TC = Hybrid, equal weight to fleet vs sole-trader). CH2's two audiences
  are probably large national charities (procurement / managed accounts) vs small local
  volunteer groups / single shops (direct online). Mirror the Hybrid balance rule:
  **every page names both ordering routes.**

---

## 4. The batch rhythm that worked
1. `python3 next_towns.py 56` → the next 56 by rank (London is rank 1, never a target).
2. Split into 8 groups of 7. For each group, dispatch **one `general-purpose` agent** that:
   - reads `PROMPT_TEMPLATE.md`, does **real web research**, and **writes**
     `towns/bNN_gX.json` (a JSON object of 7 entries), then replies only with the
     nearby triples.
   - **Tell agents: "Do ALL research yourself; do NOT spawn sub-agents."** Some agents
     fan out to sub-agents, which is slow and muddies completion signals.
3. Wait for all 8 files with a background watcher (don't poll in-band):
   ```bash
   until [ "$(ls towns/bNN_*.json 2>/dev/null | wc -l)" -ge 8 ]; do sleep 3; done
   ```
   (run_in_background). You'll get a completion notification.
4. **Pre-flight scan** (script in §5) over the batch JSON: ASCII-only, no `&`, all 7
   fields, nearby length 3 / s1loc length 2, no bleed term (own-town-exempt).
5. `next_towns.py --check` (validates every nearby is on CSV — catches off-list typos).
6. `python3 ch2_build.py` (no-arg builds all TOWNS) → `cp ch2-london.html outputs/`.
7. `verify_ch2.py outputs` → **must be N/N PASS**. `score_ch2.py outputs` → confirm worst
   pair ≤ cap; if over, run `diag_ch2.py` and enrich (see §7).
8. `git add towns/bNN_*.json && git commit && git push`. Move to next batch.

Per TC batch this was ~8 agents × ~40k tokens. All 9 batches ran clean (0 rejected).

---

## 5. Pre-flight scan (reuse verbatim, swap the bNN glob + BLEED list)
```python
import json, glob, re
BLEED=[...]                  # <-- CH2 bleed list
REQ=["region","nearby","snapshot","s1_head","s1loc","kit_loc","s2_intro"]
issues=0; n=0
for f in sorted(glob.glob('towns/bNN_*.json')):
    for k,v in json.load(open(f,encoding='utf-8')).items():
        n+=1; blob=json.dumps(v)
        if any(ord(c)>127 for c in blob): print("NONASCII",k); issues+=1
        if '&' in blob: print("AMP",k); issues+=1          # agents emit "V&A" etc.
        if [x for x in REQ if x not in v]: print("FIELD",k); issues+=1
        if len(v.get('nearby',[]))!=3 or len(v.get('s1loc',[]))!=2: print("SHAPE",k); issues+=1
        for t in BLEED:
            if t.lower()==k.lower(): continue            # own-town exemption
            if re.search(r'\b'+re.escape(t)+r'\b',blob,re.I): print("BLEED",k,t); issues+=1
print(f"entries={n} issues={issues}")
```

---

## 6. Gates & scoring reality
- **`verify` is the contract.** 16 hard checks: exact link counts (TC = 14 `.com` + 1
  community — re-derive CH2's), no JS, no HTML entities, meta ≤160 (no apostrophe in
  meta), title ≤60, town in title+h1, no delivery-timescale claims, lead trio present,
  4 JSON-LD blocks, dead-link guard, bleed. **Every page must pass.**
- **`score` floors are diagnostics.** TC final: overall-unique **69.2%** (the 77% floor
  is unreachable at 505 pages — pooled scaffold ceiling; VT hit ~67%), worst pair
  **51.4%** vs a 52% cap. The **pair cap is the real near-duplicate guard**; overall
  "BELOW FLOOR" is expected and fine.

---

## 7. If a pair goes over the cap (didn't happen in TC, but plan for it)
TC's worst pair held at 51.4% the whole way, so **no enrichment was ever needed**. But
pairwise dup between two specific pages is fixed regardless of N, and new pairs appear as
towns are added, so watch `score` each batch. If a pair exceeds the cap:
1. `python3 diag_ch2.py outputs ch2-a.html ch2-b.html` — shows the exact shingles the
   pair shares (boilerplate subtracted via a control page).
2. Add **one researched, proper-noun-rich sentence (~40–70 words)** to the **weaker**
   page's `s1loc` (its local paragraphs). ~40–70 words moves a pair ~2–3 points. Do NOT
   reword distinctive local prose into generic phrasing.

---

## 8. Gotchas / traps checklist (each cost time in TC)
- [ ] **Bleed inversion** (§3) — your own core word in the inherited bleed list fails
      every page. Audit first.
- [ ] **`wellington`-style town/term collisions** — apply the own-town exemption (2d) and
      grep the CSV for names that collide with your CH2 bleed list.
- [ ] **Mixed-case towns** (`Newcastle upon Tyne`, `Stoke-on-Trent`, `Southend-on-Sea`,
      `Houghton le Spring`, `Bishop's Stortford`) — need fix (2b) or they render wrong /
      don't match. Apostrophe towns work via slug match; keep the apostrophe in the JSON key.
- [ ] **Non-ASCII from agents**: `£` (write "80 million pound"), curly quotes, em-dashes
      (use " - "), and **bare `&`** ("V&A" → "V and A"). The pre-flight `ord>127` + `&`
      checks catch them; the prompt forbids them.
- [ ] **Nearby must be on the CSV** and geographic. Pre-assign a hint triple per town in
      the agent prompt, give agents the full ALLOWED LIST, and validate with
      `next_towns --check`. Isolated towns (Elgin, Carlisle, Plymouth) have few on-list
      neighbours — pick the closest available and say so.
- [ ] **Disambiguation**: Newport (Welsh) vs `Newport (Isle of Wight)` (full parenthetical
      key); Chapeltown = Sheffield; Rothwell = W.Yorks; Blackwood = Gwent; Fulwood =
      Preston; Sutton vs Sutton Coldfield vs Sutton-in-Ashfield; London boroughs need
      London-area nearby. The **Isle of Wight cluster cross-links only within the island.**
- [ ] **Don't spawn sub-agents** from research agents (slow, confusing completion signals).
- [ ] **md5 selector only** in `pick()` — never crc32 (low-bit correlation collides
      same-length town names). Verify the seed rebuilds byte-identical before scaling.
- [ ] **Link-bearing pools carry a fixed link count** — any new prose variant added to a
      pool that contains an `iNeedWorkwear` link must carry the same count, or the exact
      link-count check fails.
- [ ] **`outputs/`, `dist/`, `__pycache__/` gitignored**; commit per batch; pages
      regenerate deterministically so the zips need not live in git.

---

## 9. Resume / reproduce
- Progress = membership of `TOWNS` (seed literal + `towns/*.json`). After any reset,
  `next_towns.py --done` tells you what's left and `--slugs N` emits the next N. The build
  is deterministic, so a re-run reproduces byte-identical pages.
- Deliverables: `dist/ch2-pages-505.zip` (built HTML) + `dist/ch2-kit.zip` (generator +
  gates + helpers + flagship + CSV + docs + all town JSON). Final report → `ch2/BUILD_REPORT.md`.

---

### TC final scoreboard (your target shape)
505/505 verify PASS · worst pair 51.4% (cap 52%, 0 over-cap) · 0 dead links ·
overall-unique 69.2% (diagnostic) · ~1.72M words · built in 10 batches.
