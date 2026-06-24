# FS Series — Forestry & Tree Surgery Workwear — HANDOVER

**For the next code session. Read this first, then SPEC.md (HM) as the architectural reference.**

Series **#18** in the CW Hybrid matrix (`CW_Hybrid_Series_Planning_Matrix.xlsx`,
Build Order row 18). Code **`FS`**. One HTML page per UK town for the
forestry / arboriculture / tree-surgery trade. Page prefix `fs-`,
canonical/og to `https://www.ineedworkwear.uk/fs-<slug>.html`.

---

## 1. Status at handover

- **Nothing FS exists yet.** The repo currently holds ONLY the completed HM
  (Highway Maintenance, series #17) kit: `hm-london.html`, `hm_build.py`,
  `verify_hm.py`, `score_hm.py`, `diag_hm.py`, `HM_towns.csv` (505),
  `SPEC.md`, `CLAUDE.md`, and `outputs/` (505 HM pages, all QA-green).
- **HM is finished** — 505/505 pages pass the hard gate; series complete and
  pushed to `claude/repo-access-yga2o1`.
- **FS is a fresh build.** It also requires the **first-ever Template B
  (self-checkout)** layout — the matrix Summary marks Template B "TO BUILD".
  HM was Template A (Concierge). So FS = new series **and** new template.

## 2. What FS is (from the planning matrix)

| Field | Value |
|---|---|
| Series code | **FS** |
| Industry | Forestry, Arboriculture & Tree Surgery (matrix row 37) |
| Audience | **Small Biz** — sole traders & small arb/tree-surgery teams |
| Page tone / template | **Self-checkout / Template B** |
| Workwear depth | High |
| Local variation | Medium (rural variation strong) |
| Town count | **200** |
| Tier | 2 (build second) |
| Key products | Chainsaw trousers, safety boots, hi-vis, hard hats with visors, polo shirts, waterproofs, gloves, embroidery |

## 3. The two big differences from HM

### (a) Template B — Self-checkout posture
HM's Template A is **concierge**: phone + email + .com contact block, trade
accounts, PO/volume pricing, multi-depot frameworks. **FS Template B is
self-checkout**: buyer is a **sole trader or small crew**, so the page leads
**browse-and-buy / order-online**, **.com prominent + email** (de-emphasise
phone/trade-account language), individual & small-team quantities, quick
reorder. Per the matrix Summary: *"Contact block: .com prominent + email.
Quick ordering, individual/small team, browse-and-buy focus."* This changes the
contact block, the CTAs, the identity-block framing and the FAQ — not the
generator architecture.

### (b) Chainsaw-PPE identity, not Chapter 8
HM's differentiator is Chapter 8 / Class 3 / "branding off the reflective area."
**FS's differentiator is chainsaw cut-protection compliance.** Build the
identity block around:
- **EN ISO 11393** chainsaw-protective clothing — leg protection **Type A**
  (front, ground work) vs **Type C** (all-round, for climbers/aerial work);
  **Class 1/2/3** chain speeds (20/24/28 m/s).
- **Forestry helmet** to **EN 397** with mesh visor (EN 1731) + ear defenders
  (EN 352) — the combined head/face/hearing unit.
- **Chainsaw safety boots** (EN ISO 17249), chainsaw gloves (EN 381-7).
- HSE / **AFAG** (Arboriculture & Forestry Advisory Group) guidance context.
- **Signature thread (the FS analogue of HM's "branding off the reflective
  area"):** branding/embroidery is placed **off the chainsaw-protective panels**
  so the cut-protection rating is never compromised; protective layers are
  **replaced, not patched/repaired**, once cut into or below standard. Run this
  thread through range, embroidery, and FAQ — it is the page's distinctive
  compliance point, exactly as the reflective-area thread was for HM.

## 4. Scaffolding to create (mirror the HM kit, renamed `fs_`)

1. **`fs-london.html`** — the FS flagship / base template the generator reads.
   Easiest path: copy `hm-london.html` and convert to **Template B + forestry
   identity + forestry palette** (see §5). This is the single biggest task and
   the thing to get right first; everything else extracts chrome from it.
2. **`fs_build.py`** — clone `hm_build.py`; `s/hm_/fs_/`, `s/hm-/fs-/`,
   point at `fs-london.html` and `FS_towns.csv`. Keep the architecture:
   extracts shared chrome (CSS/header/stats/SVG scenes/contact/footer) from the
   flagship via `between()` / `aria_block()` markers, assembles each town from
   crc32-hashed prose pools + an inline `TOWNS` dict. Keep `require_nearby()`,
   the 4 JSON-LD blocks, `signpost_town()` and the SVG town-swaps in
   `assemble()` (re-point the swap targets at the FS SVG scene aria/plank text).
3. **`FS_towns.csv`** — 200 towns (Rank,Town,Population,Nation). **Open
   decision** — see §7.
4. **`verify_fs.py`** — clone `verify_hm.py`; the binding hard gate. Adjust:
   lead-product trio, JSON-LD count, link counts, and the **BLEED list**
   (§6).
5. **`score_fs.py` + `diag_fs.py`** — clone from HM. **Critical rename gotcha
   (learned on HM):** after `s/re_/fs_/` style renames, ALSO explicitly
   `s/score_hm/score_fs/` and `s/diag_hm/diag_fs/` inside the files, or the
   diagnostics call the wrong module.
6. **`SPEC.md`** — rewrite the HM SPEC for FS (audience, lead trio, identity
   block, palette, hard rules, BLEED, uniqueness, research mandate).
7. **`CLAUDE.md`** — update the runbook header/workflow for FS (or keep HM's and
   add an FS section). Note the project CLAUDE.md currently describes HM.

## 5. TOWNS entry schema (unchanged from HM)
Key = lowercased CSV display name. Fields: `region`, `nearby` (exactly 3
geographically-close towns, **all on FS_towns.csv**), `snapshot`, `s1_head`,
`s1loc` (list of 4 researched paragraphs), `kit_loc`, `s2_intro`. Re-tone all
prose for the arb/tree-surgery trade and self-checkout buyer.

### Lead products (verifier-enforced) — proposed
LEAD = **chainsaw trousers**, CO_LEAD = **safety boots**, TRI_LEAD =
**forestry helmet / hard hat with visor**. 8-card grid suggestion: Chainsaw
Trousers (Type A/C) / Chainsaw Safety Boots / Forestry Helmets, Visors & Ear
Defenders / Hi-Vis Tops & Vests / Waterproofs & Base Layers / Chainsaw Gloves &
Hand Protection / Embroidered Polo Shirts / Embroidery, Names & ID.

### Palette / design — proposed
Swap HM's tarmac-slate for a **forestry identity**: forest/conifer green
(e.g. `#2f5233` / hover `#23391f`) + bark-brown or charcoal + a hi-vis or
amber accent. SVG scenes re-themed: chainsaw-PPE garment row (chainsaw
trousers / forestry helmet+visor / chainsaw boot / glove), embroidery scene,
town signpost (e.g. WOODLAND / TREE WORK), an **arb worksite scene** (chipper,
felled timber, cones/signage, climbing line), order-online. Confirm colours
with the user — this is a brand decision.

## 6. BLEED list (verifier) — the key FS-specific rule
**Do NOT block `chainsaw`, `tree surgery`, `arboriculture`, `forestry`,
`EN ISO 11393`, `Type C`, `AFAG`** — these are FS's core vocabulary, exactly as
HM deliberately allowed `Class 3` / `Chapter 8` / `hi-vis`. (HM's BLEED list
explicitly *bans* `chainsaw`/`tree surgery` to keep HM separated from FS — so
when cloning, REMOVE forestry from the ban list and instead ban the OTHER
industries: highway/Chapter 8 roadworks, food-hygiene (BRCGS/hairnet), security
(SIA/body armour), cleaning (COSHH/tabard), waste (RCV/refuse/bin lorry),
renewables (solar/EV/heat pump/MCS), care/edu (Ofsted/CQC), gas (Gas Safe).)

## 7. Open decisions for the user (resolve before town batches)
1. **Town list.** Reuse the top 200 of `HM_towns.csv` (population-ranked), or a
   **rural-weighted** 200 (forestry/arb skews rural — market towns, county
   towns, National-Park-adjacent towns) rather than pure big-city order?
   Recommend a rural-weighted list since "rural variation strong."
2. **Flagship town.** HM used London as the un-built general-knowledge flagship.
   For FS, is London still the flagship/reference, or a more forestry-relevant
   anchor? (London works fine as the build base even if odd thematically.)
3. **Palette / brand** colours for Template B / forestry (§5).
4. **Self-checkout contact block** specifics — exact .com/email treatment,
   whether any phone appears at all, CTA wording.
5. Confirm the **lead-product trio** in §5 (drives the verifier).

## 8. Proven workflow / cadence (from HM — reuse exactly)
1. Stand up the scaffolding (§4); build & QA the flagship first.
2. Per batch of ~30 towns: **web-research first** — fan out **6 parallel
   `general-purpose` background agents × 5 towns**, each told *"do the web
   searches YOURSELF; do NOT spawn sub-agents,"* each given a tailored on-CSV
   `nearby` allow-list and any disambiguation notes. For FS, research per town:
   local arb/tree-surgery firms or context, woodland/estate/National Trust /
   Forestry England presence, council tree teams, notable
   storm/ash-dieback/utility-vegetation work — **never author from memory**.
3. Author a `splice_batchN.py` in the scratchpad that defines a `NEW` dict and
   appends entries before the `"\n}\n\n# === CSV / nearby"` marker in
   `fs_build.py`. ASCII only, no double-quotes inside strings (esc() asserts).
4. **Immediately after splicing, count:** `python3 -c "import fs_build;
   print(len(fs_build.TOWNS))"` — this caught missing entries twice on HM.
5. Build: `python3 fs_build.py <slugs...>`. Verify: `python3 verify_fs.py
   outputs` (must read `==== N/N pages passed all hard checks ====`). Score:
   `python3 score_fs.py outputs` (pair-cap ≤52% is the binding guard; overall
   floor 77% — don't chase it at small N).
6. Commit + push to the designated branch with the standard trailer; **no PR**.
7. Watch for transient API 529 overloads on research agents — relaunch the
   failed group, don't author from memory.

## 9. Standing constraints (carry over)
- Develop/commit/push **only** to the session's designated feature branch;
  never push elsewhere without explicit permission; **no PRs** unless asked.
- Git identity used on HM: `git -c user.name="Claude"
  -c user.email="damien@phoenixcleaningcompany.com"`.
- Commit trailer:
  `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>` +
  `Claude-Session: <session url>`.
- Do **not** put the model identifier in commits/PRs/code — chat only.
- Use the scratchpad dir for temp/splice scripts.
- **Never rebuild a flagship**; only ADD town pages to `outputs/`.
- Filesystem resets between sessions — recreate the kit from these files.

## 10. First three concrete steps for the next session
1. Read this file + `SPEC.md` + skim `hm_build.py` / `verify_hm.py` /
   `score_hm.py` to internalise the architecture.
2. Get the §7 open decisions answered by the user (town list, palette,
   contact-block, lead trio).
3. Build `fs-london.html` (Template B + forestry identity), then clone the
   four scripts, then build + QA the flagship before any town batches.
