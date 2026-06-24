# Learnings from the HM build (505 pages) — playbook for the next series (FS)

Handover for the next session. You already have the FS build files
(`fs_build.py`, `FS_towns.csv`, verify/score, flagship). This doc is **what I
learned shipping 505 HM pages** — uniqueness, validation, research, and the
traps — so you don't re-learn them. Series-agnostic unless marked **[FS]**.

Final HM result for calibration: **505/505 pass the hard gate; overall
uniqueness 80.8%; worst pair 43.9%** (cap 52%).

---

## 1. Uniqueness — what actually moves it

- **Two gates:** overall floor 77%, **worst-pair cap 52%**. The **pair cap is
  the binding one.** Overall sits ~80%+ at full scale and is never the problem;
  a single near-duplicate pair is what bites.
- **Only authored fields count.** The scorer strips shared chrome AND the
  generated boilerplate sections, then **masks the town name**, then compares
  5-gram shingles. So uniqueness lives ENTIRELY in the hand-authored fields:
  `snapshot`, the **four `s1loc` paragraphs**, `kit_loc`, `s2_intro`.
  Boilerplate neither helps nor hurts — pour all variation into those fields.
- **Worst pairs are always structural twins** — same authority + same
  contractor + same geography. HM's recurring offenders: Esher vs Reigate
  (Surrey/Ringway), Aldershot vs Havant (Hampshire/M Group), Cowes vs Shanklin
  (Isle of Wight). When two towns share authority/contractor/road, their pair
  score spikes. **Mitigation that worked:**
  - Lead each town on a *different concrete hook* — a specific junction, named
    employer, industrial estate, current scheme — not the generic authority line.
  - Vary the `snapshot` opening verb and structure (supplies / kits / equips /
    fits out …) and the sentence shapes.
  - Give the 4 `s1loc` paras distinct roles and vary all four:
    (1) geography + authority, (2) delivery model + a *local* trade/employer
    anchor, (3) strategic roads + operator + named junctions, (4) short closing.
    Para 2's local anchor is where twins diverge most — make it specific.
- **Don't chase the overall floor at small N.** Early batches read ~67%
  overall because the scaffold dominates; it climbs with town count. The pair
  cap is what you watch every batch.
- **Run the scorer every batch** and read the *worst pair* it names — if a new
  pair approaches the cap, de-template those two before moving on.

## 2. Validation — the binding hard gate, and how to not trip it

- **verify is the gate, not the scorer.** It must read
  `==== N/N pages passed all hard checks ====`. The score is diagnostic.
- **ASCII-only authoring.** No curly quotes, no char >126. The splice `esc()`
  asserts this and will abort the batch. Write `pounds` not `£`, hyphen or
  `to` not en-dash, and **never a double-quote inside a string value** (it
  breaks the dict). Apostrophes are fine (they're ASCII).
- **`require_nearby()` hard-fails** on missing / fewer-than-3 / off-list
  nearby. Every `nearby` entry must match a CSV **display name exactly**
  (e.g. `Newport (Isle of Wight)`, `Thornton Cleveleys` with no hyphen). Verify
  nearby against the CSV *before* building, not after.
- Other checks that bit on HM: exact link counts, **exactly 4 JSON-LD blocks**
  (FAQ+Org+Service+Breadcrumb), meta length + no apostrophes in meta, the
  lead-product trio present, word-count floor, and the **dead-link guard**
  (every `fs-<slug>.html` link must resolve to a CSV town).
- The verifier does **not** mandate any specific road-operator phrase, so
  edge/devolved wording passes fine (see §6) — don't add words just to satisfy
  a check that isn't there.

## 3. The two cheap checks that caught real bugs

1. **Count immediately after every splice:**
   `python3 -c "import fs_build; print(len(fs_build.TOWNS))"`.
   This caught two silent omissions on HM (a batch added 27 of 30; another
   dropped one town mid-dict). Costs nothing; do it every time.
2. **Set-difference at milestones** — CSV towns minus `TOWNS` keys (minus the
   flagship). This caught **West Bromwich**, which had been silently skipped in
   an early batch and would otherwise have shipped as a hole in the series.
   Per-batch counts alone won't catch an early gap; run the diff periodically.

## 4. Splice mechanics that proved robust

- A `splice_batchN.py` in the scratchpad defines a `NEW` dict + `esc()`/`emit()`
  helpers and inserts the block before the single end marker
  `"\n}\n\n# === CSV / nearby"`.
- **Guard every splice:** `assert src.count(end_marker) == 1` AND
  `assert '\n "<first-key>": {' not in src` (idempotency — stops a double-run
  from duplicating a batch).
- Keep batches ~30 towns. Author in the scratchpad, never hand-edit the giant
  generator dict directly.

## 5. Research cadence (where correctness comes from)

- **Web-research every town; never author from memory.** (Flagship is the only
  general-knowledge exception.)
- Fan out **6 parallel `general-purpose` background agents × 5 towns**. Tell
  each: *"Do the web searches YOURSELF; do NOT spawn or delegate to
  sub-agents."* Give each a **tailored on-CSV `nearby` allow-list** and
  **disambiguation notes**.
- **Disambiguation is essential** — same-name towns wrecked early drafts until
  pinned: Hythe (Kent vs Hampshire), Bangor (Wales vs NI), Ripley (Derbyshire
  vs Surrey vs N. Yorks), Newport (Wales vs Isle of Wight), Wellington
  (Somerset vs Telford). Tell the agent the county/nation and a population hint.
- Frame time-sensitive facts as **"in recent years"** — contracts change.

## 6. Data accuracy / staleness — trust live research over assumptions

The brief's assumed contractor was wrong often enough that the rule is **let
research override the prompt and apply current corrections.** Real HM examples:
Bellshill → HOCHTIEF (not Amey, from Oct 2024); Chesham → Balfour Beatty Living
Places (not Ringway Jacobs); Woodley → VolkerHighways (not BBLP); Faversham →
Ringway (from May 2026, ex-Amey). Also note council-owned-company and edge
models so prose stays distinctive: NY Highways, CORMAC/Corserv, Island Roads
PFI, Humber Bridge Board, joint-owned Tamar Bridge. Devolved handling (Scotland:
Transport Scotland / BEAR / Amey; Wales: Welsh Gov / Traffic Wales / NMWTRA /
SWTRA) simply omits "National Highways" and still passes verify.

## 7. Transient failures

Research agents intermittently returned **`API Error: 529 Overloaded`** with no
data (a cluster of them in one batch). **Relaunch the failed group** (stagger if
the overload persists); do **not** backfill from memory to keep moving.

## 8. [FS] The one rule that's series-specific: BLEED inversion

Each series' verifier must **ALLOW its own core vocabulary and BAN the other
industries'.** HM deliberately *allowed* `Class 3` / `Chapter 8` / `hi-vis`
(its core) while *banning* `chainsaw` / `tree surgery` to keep HM separate from
FS. **For FS, invert it:** allow `chainsaw` / `tree surgery` / `arboriculture` /
`forestry` / `EN ISO 11393` / `Type C` / `AFAG`, and ban the others'
(roadworks/Chapter 8, food-hygiene, security, cleaning, waste, renewables,
care/edu, gas). This BLEED list is the mechanism that keeps sibling series from
reading like each other — get it right per series.

## 9. [FS] Two quick notes for the self-checkout template

- FS is **Template B (self-checkout)** — the authored prose should lead
  browse-and-buy / order-online for sole traders & small crews, not concierge
  trade-account language. Keep the same uniqueness discipline (§1) regardless.
- **Town list:** you're providing the FS list. Whatever it is, the §1–§3
  discipline (nearby-on-CSV, exact display names, count + set-diff checks)
  applies unchanged.

## 10. Standing constraints (carried over)
- Develop/commit/push **only** to the session's designated feature branch; no
  pushes elsewhere without explicit permission; **no PRs** unless asked.
- Git identity used: `git -c user.name="Claude"
  -c user.email="damien@phoenixcleaningcompany.com"`.
- Commit trailer: `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>` +
  `Claude-Session: <url>`. Never put the model id in committed artifacts.
- Scratchpad dir for temp/splice scripts. Never rebuild a flagship; only ADD
  pages. Filesystem resets between sessions.
