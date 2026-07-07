# iNeedWorkwear — Complete Restructure & Rebuild Plan (v2)

**Status:** Plan for review — now grounded in the actual build
**Prepared for:** Damien, Phoenix Cleaning Company
**Date:** 2026-07-07
**Goal:** Rebuild the iNeedWorkwear content site so it can safely reach thousands →
tens of thousands of genuinely useful pages that funnel to the (not‑yet‑built) ecommerce
store, without duplicate/thin/doorway‑content risk to *either* domain.

> **v2 note:** This version replaces the earlier assumptions‑based draft. I've now reviewed a
> 400‑file sample of the real workwear build, the `CW Hybrid Series Planning Matrix`, and four
> pages from the cleaning site (Phoenix Duct Clean) that you hold up as the better build. The
> findings below are measured from those files, not assumed.

---

## 0. Headline recommendation: start fresh — but harvest three assets

You asked whether to rebuild, edit, or scrap. **Scrap the current workwear pages as a live site.**
They are a net liability, not a foundation — and editing 10,000 pages to fix problems baked into
the template and the topic list costs more than rebuilding and leaves the risk signals in place.

But "start fresh" does **not** mean start from nothing. Harvest three things from what exists:

1. **The design‑system discipline of the cleaning site.** Phoenix Duct Clean already proves your
   team can build one coherent, well‑branded system (one palette, one type system, schema markup,
   consistent chrome). That *is* the model. The workwear site's core failure is that it never had one.
2. **The industry taxonomy** in the planning matrix (construction, healthcare, automotive, plumbing…
   with product mappings). The *entity model* is sound; the *town‑multiplication* on top of it is not.
3. **A handful of genuine editorial guides** (e.g. "best safety boots for concrete floors"). These
   can be rebuilt as real, deep buying guides — the seed of the useful‑content layer.

Everything else — the town‑swapped industry pages and, urgently, the off‑topic traffic‑net pages —
should not be migrated. Redirect or `410` them (see §7).

---

## 1. What the actual build shows (evidence)

### 1.1 Branding — no system at all (your problem #1, confirmed)

The cleaning site uses **one** design‑token block on every page:
`--steel:#0E1620; --amber:#D4762A; --teal:#3FA89B`, fonts `Saira Condensed / Inter / Space Mono`.
Every page is unmistakably the same site.

The workwear site has **a different palette and often different fonts per series**:

| Series | Sample colour | Fonts |
|--------|--------------|-------|
| `am-` (automotive) | `#1c2024` dark + amber | Lora / Source Sans |
| `bh-` (hair & beauty) | `#271f33` purple | Lora / Source Sans |
| `festival-` | `#7c3aed` violet | Lora / Source Sans |
| `restaurant-` | `#2c2a27` | **Playfair Display / DM Sans** |
| `blog-` | `#063a09` green | (varies) |
| `eat-` | `#13251a` green | Lora / Source Sans |

There is no shared header/nav, no shared footer identity, no tokens. Each batch looks like a
different website. This is exactly the "doesn't look like real website pages" problem — and it's
the single clearest difference from the cleaning site.

### 1.2 Uniqueness — spun content around a fixed skeleton (your problem #2, confirmed)

Measured on two pages from the same series (`am-aberdeen` vs `am-abingdon`, both "Garage and
Mechanic Workwear Supplier"):

- **77% shared vocabulary** (2,216 of ~2,880 word tokens common to both).
- **7 of 8 `<h2>` headings identical, word‑for‑word.** Only the opening "local flavour" heading
  differs ("The energy city's fleet and 4x4 trade" vs "The MG factory and the Radley Road trade").
- Body sentences reworded around the same fixed structure.

That is the classic **spun‑content signature**: same skeleton, same topic, lightly reworded prose,
one town swapped in. Google's systems detect this as near‑duplication even when exact phrase overlap
is low, and cluster the pages together.

### 1.3 Templating — duplication by design (your problem #3, confirmed)

The `CW Hybrid Series Planning Matrix` sets out the intended system:

- **~37 industry series**, most at **500 towns** each (some 200), tiered for build order.
- Rendered through **two templates** — "A (Concierge)" and "B (Self‑checkout)" — plus a hybrid.
- The declared uniqueness lever is a "Local Variation: High/Medium/Low" column — i.e. **town‑name
  substitution.** "Towns: 500" against each industry.

That's **~10,000+ near‑identical pages across 2–3 templates.** The matrix is, in effect, a
blueprint for the exact pattern ("scaled content abuse") that Google's March 2024 spam policy targets.

### 1.4 The fourth problem — topical sprawl / doorway pages (not on your list; the biggest risk)

The sample contains large programmatic series with **nothing to do with workwear**, each keyword‑
stuffed and linking to the shop:

| Page | Words | "workwear" mentions | Shop links |
|------|------:|--------------------:|-----------:|
| `world-cup-bulgaria` (Bulgaria's WC history) | 2,882 | 31 | 11 |
| `festival-2000-trees` (music festival guide) | 2,794 | 43 | 17 |
| `eat-barnet` ("best places to eat") | 2,516 | 45 | 12 |
| `best-youth-clubs-harrow` | 2,625 | 12 | 5 |
| `restaurant-carlton` ("launch a restaurant") | 3,058 | 21 | 6 |

Others in the set: town criers, nurseries, festivals A–Z, "eat" guides by town, world‑cup by nation.
A World Cup history page on a workwear domain that mentions "workwear" 31 times and pushes 11 shop
links is a textbook **doorway page**. This is the content most likely to get the domain classified as
a low‑value funnel — and because these pages link to the ecommerce store, that judgement is what
puts **both** sites at risk. **This series must be deleted, not fixed.**

### 1.5 A caution about the cleaning site (the "good" build)

The cleaning site is genuinely better — one design system, real local specifics (street names,
councils, local history), useful editorial. **But do not simply clone its location‑page pattern at
10,000× scale**, because it carries two latent risks that only bite at scale:

- **Repeated fixed "stats"** ("4,287 canopies degreased", "54,754 hours on site") appear identical
  on every page. If those numbers aren't literally true, that's an E‑E‑A‑T/trust problem; at scale
  it's a duplication signal too.
- **"On the ground" job anecdotes and testimonials** (e.g. the "bacon rolls" story) read as
  per‑town template slots. If they're not real, that's a trust risk on a page type Google scrutinises.

The cleaning site works because it is **small and tightly on‑topic** (a few hundred pages in one
niche). The workwear ambition is 20–50× larger and was topically sprawling — the same location‑page
recipe that passes at cleaning‑site scale would trip the **site‑level quality classifier** at
workwear scale. That gap is the heart of your question, and §2 is the answer to it.

---

## 2. Can you build tens of thousands of pages safely? Yes — but not this way

The honest answer: **there is no safe page count — there is only safe value density.** 50,000
genuinely useful pages is fine; 5,000 town‑swapped ones is not. Google scores the *average* quality
of the site, so the constraint is: *every page must add something a searcher can't easily get elsewhere.*

The current build fails because its only uniqueness lever is the town name. To scale safely,
uniqueness has to come from **real, structured data and real utility** — things that genuinely differ
page to page. The rest of this plan is how to get there.

### The governing rule — the "unit of unique value" test

**No page ships unless it passes at least one of these three tests:**

1. **Unique information** — real facts a searcher can't trivially get from the current top results
   (a specific safety standard's clauses, real garment specs, a real role's hazard profile).
2. **Unique utility** — it *does something*: a selector, calculator, checklist generator, comparison
   engine. Interactivity is inherently non‑duplicable.
3. **Unique intent** — it serves a genuinely distinct search need, not a synonym of another page.

A town‑swapped "Garage Workwear in [Town]" page passes none of these. A "Bulgaria World Cup" page
passes none of these *for a workwear site*. Both are retired. This one gate is what converts a
10,000‑page liability into a 10,000‑page asset.

---

## 3. Where genuine uniqueness comes from (the engine)

Stop generating **prose from a template**. Start rendering **data through a component library.**
Uniqueness then becomes a by‑product of the data, and structure varies because the data varies.

### 3.1 The data model (entities), not the town list

- **Garments:** hi‑vis, coverall, work trouser, FR jacket, safety boot, chef whites, scrub, tabard,
  softshell, waterproof…
- **Sectors:** construction, healthcare, hospitality, warehousing, automotive, plumbing/electrical,
  landscaping, FM/cleaning, manufacturing… *(reuse the matrix's taxonomy)*
- **Roles:** welder, electrician, chef, warehouse operative, groundworker, mechanic, nurse…
- **Standards (the richest unique‑data seam):** EN ISO 20471 (hi‑vis), EN ISO 11612 (heat/flame),
  EN 343 (rain), EN ISO 20345 (safety footwear), IEC 61482 (arc flash), EN 1149 (antistatic),
  EN 13034 (chemical), rail GO/RT…
- **Attributes:** fabric, GSM, colour, tape class, features, wash/care temperature, sizing.
- **Intents:** buying guide, "what to wear for X", compliance explainer, care, sizing, comparison,
  cost, embroidery/branding.

### 3.2 The supplier‑DAM trap (critical — this changes the strategy)

You told me catalogue data and imagery will come from **workwear suppliers' digital asset libraries.**
That means the raw specs and photos are **identical to every other reseller** pulling the same DAM —
the *opposite* of a unique asset. Rules that follow directly:

- **Never publish supplier copy or specs as page text.** Treat the DAM as *raw input to transform* —
  synthesise your own spec tables, comparisons, and standard/hazard mappings on top of it.
- **Differentiate imagery.** Raw DAM photos will be image‑deduped by Google against dozens of rivals.
  Plan for own photography where feasible, or at minimum processed/annotated/composited images.
- **The unique value lives in the layer you add** — standards analysis, role/hazard mapping, care
  guidance, tools, comparisons. No supplier feed contains those. That layer is your moat.

### 3.3 Discipline against combinatorial near‑duplicates

`sector × garment × role × town` is millions of combinations, ~95% near‑duplicate. So:

- **Only build a combination when the data genuinely differs.** "FR coveralls for welders" is real
  (arc + spatter + radiant heat). "Garage workwear in Abingdon" is not — it's a town swap.
- **Kill the town‑multiplication default.** Do **not** build 500 town variants per industry. Build
  *one strong industry/role guide*, and create a local page **only** where real local data exists
  (a physical stockist, local regulation, real delivery/lead‑time info) — otherwise it's a doorway.
- **Variable depth:** thin nodes become a *section within* a parent page or a filtered view, never a
  standalone URL.
- **Cap by value, not by a target count.** Retire "build 500" thinking. Build every node that passes
  §2, and no more.

---

## 4. Page taxonomy & template families (fixes the over‑templating)

The old build: 2–3 templates for everything. The rebuild: **many families, each structurally
distinct because each renders different data**, and each with 3–5 layout variants.

| Page type | Example | Why structurally distinct |
|-----------|---------|---------------------------|
| **Standard/regulation explainer** | "EN ISO 20471 hi‑vis classes explained" | Clause tables, class diagrams, applicability logic |
| **Sector guide (hub)** | "Workwear for construction" | Hazard matrix, role list, required standards |
| **Role guide** | "What a welder should wear" | Hazard → garment → standard mapping |
| **Garment comparison** | "Class 2 vs Class 3 hi‑vis" | Decision tables, spec grids from real data |
| **Care & maintenance** | "Washing FR coveralls without losing FR" | Step lists, temperature/care tables — high utility |
| **Sizing & fit** | Per‑garment size guides | Measurement tables, fit diagrams |
| **Interactive tools** | Hi‑vis class selector; "which coverall?"; PPE checklist; embroidery cost; size calculator | Pure utility — inherently unique |
| **Glossary** | Standards/fabric definitions | Short, interlinked, schema‑marked |
| **Editorial/blog** | Buying guides, deep how‑tos | Human‑led, real experience (E‑E‑A‑T) |

**Structural‑variation rules in the generator:** block order and inclusion driven by *which data
fields are present*, so no two pages in a series share an identical skeleton; a component library
(spec table, hazard matrix, comparison grid, callout, FAQ, tool embed) assembled by rules; and a
QA gate (§6) that rejects any page too similar to its siblings.

---

## 5. Branding & design system (fixes problem #1) — systematise the cleaning site

You already have the exemplar. Do for iNeedWorkwear what Phoenix Duct Clean did — **once, centrally**
— and render every page through it:

- **One token file:** palette (primary/secondary/neutral/semantic), type scale, spacing, radii,
  shadows. One palette for the whole site, chosen to sit alongside the future store.
- **Global chrome:** one header, nav, footer, breadcrumb on every page.
- **Component library** themed from tokens (buttons, cards, tables, callouts, tool shells).
- **Imagery system** (see §3.2 — differentiate from DAM stock).
- **Accessibility + Core Web Vitals** budgets baked in (both are quality signals).
- **Deliverable:** a brand spec + a live style‑guide page, before any content page is generated.

---

## 6. Build system & QA gates (what makes scale safe)

### 6.1 Stack **[to confirm]**
- **Static‑site generator** (Astro or Next.js) — component‑driven, fast, indexable.
- **Content as data:** the entity dataset in structured files/DB, rendered via template families and
  the component library; editorial in MDX/CMS. Copy is never hand‑duplicated across pages.
- **Clean separation:** `data/` (facts) · `templates/` (families) · `components/` (blocks) ·
  `content/` (editorial).

### 6.2 Pre‑publish gates (automated in CI — nothing ships that fails)
1. **Similarity gate** — embeddings or SimHash/MinHash vs siblings; reject above a threshold. *(This
   alone would have blocked the `am-aberdeen`/`am-abingdon` pattern.)*
2. **Thin‑content gate** — must contain real data blocks (spec table, hazard matrix, tool), not just prose.
3. **§2 value‑test gate** — each page tagged with which test it passes; untagged = blocked.
4. **Doorway gate** — CTA/shop‑link‑to‑content ratio ceiling. *(This would have blocked the World Cup pages.)*
5. **Topical‑relevance gate** — page must map to a workwear entity; off‑topic = blocked.
6. **Technical SEO** — unique title/meta/H1, correct canonical, schema.org, internal links, no orphans.
7. **Design/lint** — design‑system + accessibility + CWV budgets.

### 6.3 Index management
- **Phased publishing** in tranches; watch indexation and rankings before the next tranche.
- **`noindex` until proven** for experimental families.
- **Sitemaps segmented by page type** to monitor how Google treats each family.

---

## 7. Dealing with the existing pages

They are actively dragging any shared quality signal. Triage every URL:

1. **Off‑topic traffic‑net series** (world cup, festivals, eat, youth clubs, restaurants, nurseries,
   town criers): **delete → `410`** (or redirect to the closest relevant hub only where one exists).
   Do not migrate. These are pure liability.
2. **Town‑swapped industry pages:** **retire the town variants.** Keep the *industry topic*; rebuild
   as a smaller set of deep sector/role guides on the new system. 301 each dead town URL to its
   sector hub.
3. **Genuine editorial** (real buying guides): **rebuild** as deep, first‑hand editorial. Keep the URL
   where it has any equity.
4. **Migration map** with 301s; no soft‑404s left behind.

> Expect to delete the large majority of current URLs. Removing thin/off‑topic pages *raises* the
> site's average quality — it's a recovery lever, not a loss.

---

## 8. Cross‑site linking (protect both domains)

- **Every link to the store is a relevant citation** ("coveralls certified to EN ISO 11612 →
  view specs"), never a blanket funnel CTA. Relevance is what separates a resource from a doorway.
- **The content site must stand alone** — useful with zero purchases. If a page passes §2 on its own
  merits, it is not a doorway by definition.
- **Content first, commercial links secondary** (the opposite of the current World Cup pages).
- Because the store isn't built yet, **design both around one brand system now** so they read as one
  family when the store launches.

---

## 9. Metrics & governance

- **Value density** — % of indexed pages passing §2 (north star; target 100%).
- **Indexation ratio** per page‑type sitemap (near‑duplicate families show low ratios).
- **Internal similarity distribution** — duplicate‑cluster report over time.
- **Organic performance** per family + funnel referrals to the store.
- **CWV + design conformance** — automated budgets.
- **Editorial calendar** for the human‑led layer (freshness + E‑E‑A‑T).

---

## 10. Phased roadmap

| Phase | Outcome | Key deliverables |
|-------|---------|------------------|
| **0. Decommission risk** | Stop the bleeding | Delete/`410` off‑topic series; 301 town pages to hubs; migration map |
| **1. Foundations** | "One site" exists | Design system + tokens + component library (systematise the cleaning site); brand spec |
| **2. Data model** | Facts, not prose | Entity dataset (reuse matrix taxonomy); standards data; DAM‑transform pipeline; §2 tagging |
| **3. Template families** | Structural variety | 3–5 layout variants per page type; component‑assembly rules |
| **4. QA harness** | Scale becomes safe | Similarity, thin, doorway, relevance, technical‑SEO, design gates in CI |
| **5. Pilot tranche** | Prove the model | Build 1–2 high‑value families (standards explainers + sector guides), index, monitor |
| **6. Scale out** | Thousands, safely | Roll out remaining families in monitored tranches |
| **7. Tools + editorial** | Utility + E‑E‑A‑T moat | Flagship interactive tools; ongoing editorial |

---

## 11. Open questions before Phase 1

1. **Scope of the cull** — are you comfortable deleting the off‑topic series outright (my strong
   recommendation), or do you want a page‑by‑page review first?
2. **Stack** — Astro/Next acceptable, or an existing platform (the current pages look hand‑built/
   cPanel‑hosted) to stay on?
3. **Imagery** — can we commission any own photography, or is it DAM‑only at launch? (Sets how hard
   we must work on image differentiation.)
4. **Are the cleaning site's stats/testimonials real?** (Determines whether that pattern is safe to
   carry into the workwear system.)
5. **URL/domain** — rebuild on the same `iNeedWorkwear` domain with redirects, or fresh structure?
6. **First‑tranche scope & timeline.**

---

### Appendix A — Worked example: one node, done right

**Topic:** "Flame‑resistant coveralls for welders"

- **Passes §2:** unique information (welding hazards → EN ISO 11612 + IEC 61482) **and** unique
  utility (embedded FR‑standard finder).
- **Data rendered:** required‑standards table, fabric/GSM options (transformed from DAM, not pasted),
  care rules that preserve FR properties, layering, sizing.
- **Structure:** hazard matrix → standards table → spec comparison → care do/don't → tool → FAQ.
  A different DOM from a sizing page, because it contains different data.
- **Outbound link:** contextual — "coveralls certified to EN ISO 11612 →" (citation, not funnel).
- **Result:** useful with zero purchase; not thin, not duplicate, not a doorway.

**Contrast with the retired pattern:** `am-abingdon` — "Garage and Mechanic Workwear Supplier"
with the town swapped and 7/8 headings identical to `am-aberdeen`; or `world-cup-bulgaria` — a
football‑history essay stuffed with 31 "workwear" mentions and 11 shop links. Both fail all three
tests. **That is the build we are replacing.**
