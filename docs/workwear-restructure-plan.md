# Workwear Site — Complete Restructure & Rebuild Plan

**Status:** Draft plan for review
**Author:** Prepared for Damien, Phoenix Cleaning Company
**Date:** 2026-07-07
**Goal:** Rebuild a large (thousands → tens of thousands of pages) non‑ecommerce workwear
content site that safely funnels visitors to the ecommerce store, **without** duplicate/thin/
unhelpful‑content risk to either domain.

> **Note on scope:** This repo currently contains only a README — the existing workwear build
> is not in it. This document is therefore a strategy + architecture plan written from your
> description. Where it assumes a tech stack or data source, that's flagged as an
> **[ASSUMPTION]** so we can correct it once the current build is available.

---

## 0. TL;DR — the one idea that fixes all three problems

The current site failed because pages were generated as **prose from a template**: same skeleton,
lightly reworded body copy, keyword swapped per batch. Google's systems now explicitly target
exactly this pattern ("scaled content abuse", March 2024 spam policy) regardless of whether a
human or AI wrote it.

The fix is to **stop generating prose and start rendering data.** Every page must be built from a
**structured dataset** (real standards, real product specs, real role/hazard requirements), so that:

- **Uniqueness is a by‑product of the data**, not something we try to "spin" into copy.
- **Structure varies because the data varies** — a page about a flame‑resistance standard genuinely
  looks different from a garment‑care page, because it *contains different things.*
- **Every page earns its existence** by adding information a searcher can't easily get elsewhere
  ("information gain").

You *can* build tens of thousands of pages safely. It is not about the number — it's about the
**value density** (average usefulness per page) and never publishing a page that has no reason to exist.

---

## 1. Diagnosis — name the actual risk, so we fix the right thing

There is no generic "duplicate content penalty." The real exposure is four specific mechanisms:

| # | Mechanism | What it is | How the current build trips it |
|---|-----------|-----------|-------------------------------|
| 1 | **Scaled content abuse** (spam policy, Mar 2024) | Producing many pages *primarily to rank*, with little value per page — AI or human, doesn't matter. | Batches of 300/500/1000 templated pages with reworded copy. This is the textbook definition. |
| 2 | **Site‑level quality classifier** (helpful‑content signals, now part of core ranking) | Google scores the *whole site's* average quality. A large body of thin pages drags down even the good pages. | Thousands of near‑duplicate pages set a low site‑wide baseline. |
| 3 | **Doorway pages** policy | Pages that exist mainly to funnel users onward to another destination, without standalone value. | A non‑ecommerce site whose purpose is to push visitors to an ecommerce store is *structurally* at risk here — this is the single biggest cross‑site danger. |
| 4 | **Duplicate clustering / crawl‑budget waste** | Google canonicalises near‑duplicates together; only one ranks, the rest waste crawl budget and dilute signals. | Batch pages that differ only by keyword collapse into one cluster. |

**Cross‑site (the "penalise both sites" fear):** the risk is *not* that linking transmits a virus.
It's that (a) a site judged as a **doorway/low‑value funnel** has its outbound links devalued and
its referrals discounted, and (b) if the workwear site is publicly associated with the brand, its
low quality is a **reputational/E‑E‑A‑T** drag. The cleaning‑services site "exposed" this because
it cleared the bar the workwear site doesn't.

**Design/branding is also a ranking‑adjacent signal.** Inconsistent, un‑branded pages that "don't
look like real website pages" hurt **Trust** (the T in E‑E‑A‑T), increase pogo‑sticking/bounce, and
read to a quality rater as low‑effort. Branding is not cosmetic here — it's part of the quality story.

---

## 2. Governing principle — the "unit of unique value" test

**No page ships unless it passes at least one of these three tests.** This single gate prevents
the combinatorial explosion of near‑duplicates.

1. **Unique information** — contains facts, data, specs, or synthesis a searcher can't trivially
   get from the top results already (real standard clauses, real GSM/fabric specs, real role hazards).
2. **Unique utility** — *does something*: a selector, calculator, checklist generator, comparison
   engine, size tool. Interactivity is inherently non‑duplicable.
3. **Unique intent** — serves a genuinely distinct search need, not a synonym of an existing page.
   ("Class 2 vs Class 3 hi‑vis" ≠ "high‑visibility clothing classes" — decide which one page owns
   that intent and consolidate the rest.)

If a proposed page passes *none* of these, **it must not be built** — this is how we get to tens of
thousands of *safe* pages instead of thousands of risky ones.

---

## 3. Content architecture — where genuine uniqueness comes from at scale

The engine of the rebuild is a **structured dataset**, not a copy template. Model workwear as
entities and attributes, then *render* pages from them.

### 3.1 The data model (entities)

- **Garments:** hi‑vis vest, coverall, work trouser, FR jacket, safety boot, chef whites, scrub,
  lab coat, tabard, softshell, waterproof, etc.
- **Sectors:** construction, healthcare/NHS, catering/hospitality, warehousing/logistics,
  manufacturing, automotive, electrical, rail, highways, agriculture, cleaning, security.
- **Roles:** electrician, welder, chef, warehouse operative, mechanic, scaffolder, groundworker, nurse…
- **Standards/certifications (the richest unique‑data seam):** EN ISO 20471 (hi‑vis),
  EN ISO 11612 (heat/flame), EN 343 (rain), EN ISO 20345 (safety footwear), IEC 61482 (arc flash),
  EN 1149 (antistatic), EN 13034 (chemical), rail GO/RT, etc.
- **Attributes:** fabric, GSM/weight, colour, reflective‑tape class, features (knee‑pad pockets),
  care/wash temperature, sizing.
- **Intents:** buying guide, "what to wear for X", compliance explainer, care/maintenance, sizing,
  comparison, cost, branding/embroidery.

### 3.2 The unique‑data backbone: your ecommerce catalogue **[ASSUMPTION: catalogue data is accessible]**

Your ecommerce product catalogue is the asset the competition can't copy: **real** fabric,
GSM, certifications, colours, price bands, sizing. Spec‑driven pages built from it are:

- Genuinely unique (real numbers in real tables, not prose).
- Naturally, *relevantly* linked to the store — which is the **antidote to the doorway problem**
  (the link is a citation of real data, not a funnel CTA).
- Cheap to keep fresh (regenerate when the catalogue changes).

### 3.3 Discipline against combinatorial near‑duplicates

`sector × garment × role × region` is millions of combinations — and 95% of them would be
near‑duplicates. Rules:

- **Only materialise a combination when the data differs meaningfully.** "FR workwear for welders"
  is real (arc flash + heat + spatter). "Hi‑vis vests in Swindon" is a doorway — **do not build
  pure geo‑programmatic pages** unless backed by real local data (stockists, local regs, delivery).
- **Variable depth:** high‑value nodes become full pages; thin nodes become a *section within* a
  parent page or a filtered view, never a standalone URL.
- **Cap each series by value, not by a target count.** Kill the "build 1000" mindset — build "build
  every node that passes §2, and no more."

---

## 4. Page taxonomy & template families (fixing the "not enough structural variation" problem)

The old build used ~1 template per series. The rebuild uses **many distinct template families**,
each with genuinely different DOM/structure because each renders different data:

| Page type | Purpose | Why it's structurally distinct | Rough scale |
|-----------|---------|-------------------------------|-------------|
| **Standard/regulation explainer** | Explain EN ISO 20471 etc. | Clause tables, class diagrams, "does this apply to me" logic | 1 per standard (dozens) |
| **Sector guide** (hub) | Workwear for construction, NHS… | Hazard matrix, role list, required standards, seasonal | 1 per sector (~15–25) |
| **Role guide** | What a welder/electrician wears | Hazard→garment→standard mapping, layering | 1 per meaningful role (100s) |
| **Garment spec/comparison** | Polycotton vs cotton; Class 2 vs 3 | Spec tables, decision tables, pros/cons from real data | 100s |
| **Care & maintenance** | Wash FR coveralls without losing FR | Step lists, temp/care tables, do/don't — high utility | 100s |
| **Sizing & fit** | Size guides per garment/brand | Measurement tables, fit diagrams | 100s |
| **Interactive tools** | Hi‑vis class selector, "which coverall", PPE checklist, embroidery cost, size calculator | Pure JS utility — inherently unique | 5–15 flagship tools |
| **Glossary/definitions** | Define terms/standards/fabrics | Short, interlinked, schema‑marked | 100s |
| **Editorial/blog** | News, seasonal, deep how‑tos, case studies | Human‑led, opinion/experience (E‑E‑A‑T) | ongoing |

**Structural‑variation rules baked into the generator:**
- Each family has **3–5 layout variants**, and block order/inclusion is **driven by which data
  fields are present**, so no two pages in a series share an identical skeleton.
- A **component library** (spec table, hazard matrix, comparison grid, callout, FAQ, tool embed,
  related‑links) assembled by rules — not a fixed sequence.
- **Machine‑similarity ceiling:** the QA gate (§6) rejects any page whose structure/copy exceeds a
  similarity threshold vs its siblings.

---

## 5. Branding & design system (fixing "doesn't look like a real website")

Build **one** design system before any page is generated. Every page renders through it, so
consistency is automatic, not manual.

- **Design tokens:** a defined colour palette (primary/secondary/neutral/semantic), type scale,
  spacing scale, radii, shadows — in one tokens file.
- **Global chrome:** one header, nav, footer, breadcrumb pattern on every page.
- **Component library:** buttons, cards, tables, callouts, tool shells — all themed from tokens.
- **Imagery/iconography system:** consistent treatment; real photography where possible over
  generic stock (helps E‑E‑A‑T and originality).
- **Accessibility baked in** (contrast, focus states, semantic HTML) — also a quality signal.
- **Deliverable:** a short brand/design spec + a live component/style guide page.

> If you have brand assets from the ecommerce store, we mirror its palette/type so the two sites
> feel like one family — reinforcing trust across the funnel.

---

## 6. Build system & quality gates (the part that makes scale safe)

### 6.1 Recommended stack **[ASSUMPTION — confirm/replace]**
- **Static‑site generator** (Astro or Next.js) — fast, indexable, component‑driven.
- **Content as data:** the entity dataset in structured files/DB; pages rendered from it via the
  component library and template families. Editorial in MDX/CMS.
- **Clean separation:** `data/` (facts) — `templates/` (families) — `components/` (blocks) —
  `content/` (editorial). Copy is never hand‑duplicated across pages.

### 6.2 Pre‑publish QA gates (automated — nothing ships that fails)
1. **Uniqueness / similarity check** — embeddings or shingling (e.g. SimHash/MinHash) to compare
   each page against its siblings; **reject** above a similarity threshold.
2. **Thin‑content check** — minimum genuine information density (not just word count): must contain
   real data blocks (spec table, hazard matrix, tool, etc.), not just prose.
3. **§2 value‑test gate** — each page tagged with which of the three tests it passes; untagged = blocked.
4. **Doorway check** — CTA‑to‑content ratio ceiling; a page can't be mostly "buy now" links.
5. **Technical SEO** — unique title/meta/H1, correct canonical, schema.org markup (Product, FAQ,
   HowTo, Definition as appropriate), internal links present, no orphan pages.
6. **Design/lint** — passes design‑system + accessibility + Core Web Vitals budget.

### 6.3 Index management
- **Phased publishing** — release in tranches; watch indexation and rankings before the next tranche.
- **noindex until proven** for experimental series; promote to index only once quality is confirmed.
- **XML sitemaps segmented by page type** so we can monitor how Google treats each family.

---

## 7. Dealing with the existing pages (don't just leave them)

The old pages are actively dragging the site‑wide score. Audit and triage **every** URL:

1. **Crawl + score** existing pages: traffic, impressions, similarity cluster, thinness.
2. **Triage into four buckets:**
   - **Keep & upgrade** — has intent value; rebuild on the new data model.
   - **Consolidate** — merge near‑duplicate clusters into one strong canonical page; 301 the rest.
   - **Prune** — no value, no traffic, no unique intent → **410/redirect**. Removing thin pages
     *raises* the site‑wide average; this is a known recovery lever.
   - **Rewrite as editorial** — salvage genuinely useful topics as human‑led content.
3. **Migration map** with 301s so equity is preserved and no soft‑404s remain.

> Expect to *delete a large share* of the current pages. That is a feature, not a loss.

---

## 8. Cross‑site linking strategy (protect both domains)

- **Every outbound link to the store is a relevant citation** ("this coverall meets EN ISO 11612 —
  view specs/buy"), not a blanket funnel CTA. Relevance is what separates a resource from a doorway.
- **The workwear site must stand alone** — genuinely useful with zero purchases made. If it passes
  §2 on its own merits, it is not a doorway by definition.
- **Reasonable link density** — content first, commercial links secondary and contextual.
- **Consistent brand association** so trust flows both ways once quality is established.
- Follow links to your own store are fine; the protection is the *quality of the linking page*,
  not link attributes.

---

## 9. Metrics & governance

- **Value density** — % of indexed pages passing §2 (target: 100%; this is the north star).
- **Indexation ratio** — indexed / submitted per page‑type sitemap (near‑duplicate families show low ratios).
- **Similarity distribution** — internal duplicate‑cluster report, tracked over time.
- **Organic performance** — impressions/clicks per page family; funnel referrals to the store.
- **Core Web Vitals + design conformance** — automated budgets.
- **Editorial calendar** for the human‑led layer (ongoing freshness + E‑E‑A‑T).

---

## 10. Phased roadmap

| Phase | Outcome | Key deliverables |
|-------|---------|------------------|
| **0. Audit & decisions** | Know the current state; lock the stack & data sources | URL inventory + triage buckets; confirm catalogue data access; confirm SSG stack |
| **1. Foundations** | The "one site" exists | Design system + tokens + component library; brand spec; base SSG scaffold |
| **2. Data model** | Facts, not prose | Entity dataset; standards/spec data ingested from catalogue; §2 tagging schema |
| **3. Template families** | Structural variety | 3–5 layout variants per page type; component‑assembly rules |
| **4. QA harness** | Scale becomes safe | Similarity, thin‑content, doorway, technical‑SEO, design gates in CI |
| **5. Pilot tranche** | Prove the model | Build 1–2 high‑value families (e.g. standards explainers + sector guides), index, monitor |
| **6. Old‑page cleanup** | Raise site‑wide average | Execute consolidate/prune/redirect migration map |
| **7. Scale out** | Thousands → tens of thousands, safely | Roll out remaining families in monitored tranches |
| **8. Editorial + tools** | E‑E‑A‑T + utility moat | Flagship interactive tools; ongoing editorial calendar |

---

## 11. Open questions to confirm before Phase 1

1. **Where is the current build**, and what stack was it generated in? (Determines migration effort.)
2. **Can we access the ecommerce product catalogue as structured data?** (This is the uniqueness engine.)
3. **Preferred stack** — is Astro/Next acceptable, or is there an existing platform to stay on?
4. **Brand assets** — do we have the ecommerce store's palette/type/logo to mirror?
5. **URL/domain** — same domain rebuild, or new structure with redirects?
6. **Scale ambition & timeline** — realistic first‑tranche size and go‑live target?

---

### Appendix A — Worked example: one node, done right

**Topic:** "Flame‑resistant coveralls for welders"

- **Passes §2:** unique information (welding hazards: arc, spatter, radiant heat → EN ISO 11612 +
  IEC 61482 requirements) **and** unique utility (embedded "FR standard finder" tool).
- **Data rendered:** required standards table, fabric/GSM options from catalogue, care rules that
  preserve FR properties, layering guidance, sizing.
- **Structure:** hazard matrix → standards table → real product specs → care do/don't → tool → FAQ.
  *Different DOM from a sizing page because it contains different data.*
- **Outbound link:** contextual — "coveralls certified to EN ISO 11612 in the catalogue" (citation,
  not funnel).
- **Result:** genuinely useful with zero purchase; not thin; not duplicate; not a doorway.

Contrast the old build: a template that said "Looking for FR coveralls for [ROLE]? We have a great
range…" with the role swapped — thin, duplicative, doorway. **That page type is retired.**
