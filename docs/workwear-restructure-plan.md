# iNeedWorkwear — Complete Restructure & Rebuild Plan (v3)

**Status:** Strategy + prototyping phase complete — foundations proven, awaiting the canary gate
**Prepared for:** Damien, Phoenix Cleaning Company
**Date:** 2026-07-07
**Goal:** Rebuild the iNeedWorkwear content site so it can safely reach thousands →
tens of thousands of genuinely useful pages that funnel to the (not‑yet‑built) ecommerce
store, without duplicate/thin/doorway‑content risk to *either* domain.

> **v3 note:** v2 was grounded in the real build (a 400‑file sample, the `CW Hybrid Series Planning
> Matrix`, and cleaning‑site pages). v3 folds in the **prototyping phase**: a working prototype now
> exists for every distinct page type, the design system is established, the industry‑driven local
> model is validated across three towns, the hub‑and‑spoke content method is proven, and the
> pre‑scale **canary gate** is defined. See §0.5 for what's built, and Appendix B for the asset index.

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

## 0.5 Where we are now (v3) — foundations proven

Since v2 we've moved from strategy to **working prototypes**. The design system and the full
page‑type library now exist as real, rendered pages — so the remaining work is *content volume on
proven templates*, not new design. What's been built and validated:

| Layer | Status | Proof |
|-------|--------|-------|
| **Design system** (iNeedWorkwear brand) | ✅ Established | Navy/orange/hi‑vis‑lime palette, Barlow Condensed/Inter/IBM Plex Mono, one chrome — used on every prototype |
| **Role guide + interactive tool** | ✅ Prototyped | `fr-coveralls-for-welders` (standard‑finder tool, real EN ISO 11611/11612/IEC 61482 data) |
| **Local / area (industry‑driven)** | ✅ Prototyped ×3 | Aberdeen (offshore) · Corby (logistics) · Harrogate (hospitality) — 35% shared vocab vs the old site's 77% |
| **Content hub (pillar)** | ✅ Prototyped | `hi-vis-workwear-guide` |
| **Standard explainer + comparison (spokes)** | ✅ Prototyped | `en-iso-20471…` + `class-2-vs-class-3…`, interlinked hub‑and‑spoke |
| **Care / maintenance (HowTo)** | ✅ Prototyped | `how-to-wash-fr-coveralls` (numbered steps, HowTo schema) |
| **Page architecture & counts** | ✅ Mapped | ~1,350 safe core pages across 14 families (`page-architecture.csv`) |
| **Local data engine** | ✅ Built | 15 economic archetypes + 495‑town list + local‑page data template |
| **Staging & safe launch** | ✅ Defined | §6.4 |
| **Pre‑scale decision gate** | ✅ Defined | §6.5 + `canary-watch-framework.md` |

**The one thing still gating a live build is the canary (§6.5)** — reading how Google treats the
freshly‑launched cleaning 3,000 before we replicate the model on workwear. Everything above is ready
and unpublished until that reads green.

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

### 3.4 Local / geo — the industry‑driven model (validated)

Competitors carpet "workwear in [town]" pages, and you asked whether to match them. The answer isn't
"no local pages" — it's **no thin ones.** A nationwide shipper's town page can't differ on *service*
(same parcel everywhere), so it must differ on **real local‑industry data.** The validated model:

- **Drive each town page from its real dominant industries**, not a town‑name swap. Aberdeen → offshore
  (FR/antistatic/multi‑norm); Corby → logistics (hi‑vis/cold‑store); Harrogate → hospitality
  (uniforms/hygiene). The *workwear answer genuinely differs per town* — that's information gain, and it
  proved out at **35% shared vocabulary / 4% phrase overlap** across the three prototypes (vs the old
  site's 77%).
- **An archetype engine, not hand‑spinning.** 15 UK economic archetypes each map to an industry mix →
  standards → garments → Shopify collections; 495 towns are assigned archetype(s), which pre‑populate
  the page. Assignments are confidence‑flagged (H/M/L) to **verify against ONS/NOMIS** before build —
  never invented certainty. (`tranche1-archetypes.csv`, `tranche1-town-list.csv`.)
- **A per‑town differentiation stack** (so no single element carries it): real industry mix · sector→
  standard mapping · a real, anonymised‑but‑specific **supplied‑customer story** (the cleaning site's
  mechanism — `local-page-data-template.csv`, adapted from the Job_Notes CSV; **real supplies only,
  never fabricated**) · named local estates/colleges · honest delivery info.
- **Honest schema.** Represent as a delivery/service‑area guide (`Article`/`FAQ`/`Breadcrumb`), **never
  a fake `LocalBusiness`** with a town address you don't have.
- **Depth over breadth + measured.** Build the ~200–500 towns with genuinely rich data (not 5,000);
  smaller places fold into region pages; run a curated batch, watch it in its own sitemap, then scale.

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

**Status:** every family above except sizing/glossary is now **prototyped** (§0.5) — the sizing,
glossary and employer/compliance families reuse the same templates, so the library is effectively
complete and the remaining work is content, not design.

### 4.1 Hub‑and‑spoke — how the content layer is organised

The useful‑content layer (standards explainers, comparisons, care, buying guides ≈ 730 of the ~1,350
core pages) is built as **hub‑and‑spoke clusters**, mirroring the cleaning site's method:

- A **pillar hub** per topic (e.g. "Hi‑vis workwear: classes, standards & how to choose") gives the
  overview and fans out to the detail.
- **Spokes** each answer one specific question (e.g. "EN ISO 20471 explained", "Class 2 vs Class 3")
  and link **back to the hub, to sibling spokes, and to the shop collection** as a citation.
- New spokes grow the cluster around the hub over time — the FR cluster, footwear cluster, glove
  cluster all follow the same recipe. *(Prototyped: the hi‑vis cluster — hub + 2 spokes, fully
  interlinked, 28–41% shared vocab across the three.)*
- Pages are **webpage‑styled, not blog‑styled** — hero with stat tiles, cards, decision tables,
  keyfacts, FAQ; no "journal / X‑min‑read" byline treatment.

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

**Status:** the iNeedWorkwear system is **established and in use across all prototypes** — deep navy
ground, workwear‑orange primary, hi‑vis‑lime interactive accent; Barlow Condensed (display) / Inter
(body) / IBM Plex Mono (labels); one header/footer/nav. Deliberately its own brand, built with the
cleaning site's discipline. Next step is extracting it into a reusable tokens + component starter.

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

### 6.4 Staging & safe launch (build in the open, invisible to Google)

You can build the whole site publicly and preview it as you go — the trick is *how* you hide it.

**Don't rely on `robots.txt` `Disallow` alone.** It blocks crawling, not indexing: a disallowed URL
can still be indexed as a bare link, and — critically — if a page is disallowed, Google can't read a
`noindex` tag on it, so the two cancel out. Use one of the two correct methods instead:

| Method | Publicly reachable? | In Google's index? | Use when |
|--------|---------------------|--------------------|----------|
| **Password (HTTP auth)** — cPanel → *Directory Privacy* | No (login required) | Never | Private team/stakeholder preview — **recommended** |
| **Site‑wide `noindex`** — `X-Robots-Tag: noindex` header or `<meta name="robots" content="noindex">` in every page head, **robots.txt left open** so Google can read it | Yes | No | You want a shareable public URL |

- **cPanel note:** password protection is **Directory Privacy** (a login wall), *not* file‑permission
  codes (`644`/`755`). Leave permissions at the web defaults — `700` on a folder just breaks the site.
- **Build on a staging subdomain/domain** (e.g. `staging.ineedworkwear.co.uk`), not the live path, so
  no half‑built signals ever touch the production domain.
- **Go‑live checklist (per tranche):** the #1 SEO disaster is launching with `noindex`/auth still on.
  Before lifting the block for a tranche: content live **and** matching Shopify collections live · no
  dead links · titles/meta/canonical/schema correct · then remove the block, submit the segmented
  sitemap in Search Console, and confirm indexing.

### 6.5 The canary gate — decide *when* to scale (the current blocker)

The cleaning site launched only days ago, so whether the programmatic model passes *Google's* quality
bar (not just ours) is unknown — and takes weeks to read. Rather than bet the workwear domain and the
future store on a guess, **use the cleaning 3,000 as the canary**: read Search Console before
replicating the model on workwear. Full method in `canary-watch-framework.md`; in brief:

- **Earliest, most honest signal = indexation ratio** (GSC → Pages): of the URLs submitted, how many
  index vs sit in *"Crawled / Discovered – currently not indexed"*? A large, static pile there is
  Google declining pages it has seen.
- **Segment the sitemap by page type** so indexation is read *per pattern* — the key diagnostic.
- **Go/Amber/Red thresholds:** 🟢 ≥70–80% indexed and climbing by wk 6–8 → replicate. 🟠 40–70% or one
  weak family → fix that pattern, re‑test, replicate only proven families. 🔴 <40% flat, duplicate‑
  canonical statuses, or spike‑then‑decay → don't touch workwear; rebuild the model first.
- **Durability is the real test** — hold at wk 12–16 and across the first core update; an early bump
  is a "honeymoon", not proof. Keep the workwear build ready but **unpublished** until green.

*(Assets: `canary-watch-framework.md`, `canary-tracking-sheet.csv`, `canary-watch-dashboard.html`.)*

> **Amendment (2026-07-11, Damien's decision):** The canary gate is **waived for the 25 T2 town
> pages** — each carries genuinely differentiated, industry-specific content (verified by the gate
> suite at ≤11% cross-page similarity), so they don't match the scaled-thin pattern the gate guards
> against. The gate's logic still applies to any *future* mass replication. New hard ceilings replace
> the open-ended T3 ambition: **area pages capped at ~50 total** (31 live after this build) and
> **informational pages capped at ~500 site-wide** — competitor evidence suggests area pages beyond
> that see little traction. The T3 "~200–450 towns" line in the backlog is superseded by these caps.

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

| Phase | Outcome | Status |
|-------|---------|--------|
| **A. Strategy & evidence** | Diagnosis + governing rules | ✅ Done (§0–§3) |
| **B. Design system** | "One site" identity | ✅ Established (§5, §0.5) |
| **C. Template library** | A prototype per page type | ✅ Done — role/local/hub/spoke/care (§0.5) |
| **D. Page architecture & data engine** | Counts + local model + town data | ✅ Done — 14 families, archetype engine, 495 towns (§0.5) |
| **E. Canary gate** | Decide *when* to scale | 🟡 **In progress — the current blocker (§6.5)** |
| **0. Decommission risk** | Stop the bleeding | ⬜ Delete/`410` off‑topic series; 301 town pages to hubs; migration map (§7) |
| **1. Cluster spec + build harness** | Repeatable build | ⬜ "Hub + N spokes" recipe + data schema; QA gates in CI (§6.2); tokens/component starter |
| **2. Data model → catalogue** | Facts, not prose | ⬜ Entity dataset; DAM‑transform pipeline; Shopify collection + tag structure (per tranche) |
| **3. Pilot tranche** | Prove on workwear | ⬜ 1–2 families + matching collections, staged, indexed, monitored |
| **4. Scale out** | Thousands, safely | ⬜ Remaining families/clusters in monitored tranches |
| **5. Tools + editorial** | Utility + E‑E‑A‑T moat | ⬜ Flagship tools; ongoing editorial |

Phases A–D are complete; **E (canary) is the gate.** Phases 0–5 fire once E reads green — 0
(cleanup) and 1 (harness) can run in parallel with the canary watch since neither publishes live
workwear content.

---

## 11. Open questions / decisions

Resolved this session: **local/geo** (industry‑driven model, §3.4) · **content sequencing** (link to
Shopify collections, not products — many‑to‑few, category‑parallel tranches) · **staging** (Directory
Privacy, §6.4). Still open:

1. **Scope of the cull** — delete the off‑topic series outright (my strong recommendation), or a
   page‑by‑page review first?
2. **Stack** — Astro/Next, or stay on the current cPanel/hand‑built hosting? (The prototypes are
   self‑contained HTML that already run on cPanel, so either is viable.)
3. **Imagery** — any own photography, or DAM‑only at launch? (Sets how hard we work on image differentiation.)
4. **Are the cleaning site's stats/testimonials real?** (Determines whether that pattern is safe to reuse.)
5. **URL/domain** — same `iNeedWorkwear` domain with redirects, or fresh structure?
6. **Do you have real workwear supply records** (like the cleaning Job_Notes CSV) to seed the
   supplied‑customer stories, or does that layer build up as you win customers?

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

---

### Appendix B — Asset index (everything built this project)

All committed to branch `claude/workwear-restructure-plan-mq8w1e`.

**Strategy & planning (`docs/`)**
- `workwear-restructure-plan.md` / `.pdf` — this plan
- `page-architecture.csv` — 14 page families, counts, tiers, value tests, collections
- `page-architecture-entities.csv` — the standards/sectors/roles/garments axes behind the counts
- `page-architecture-matrix.html` — visual page‑architecture dashboard
- `local-page-data-template.csv` — the per‑town input schema (Aberdeen + Corby worked examples)
- `tranche1-archetypes.csv` — 15 UK economic archetypes → industry mix/standards/garments/collections
- `tranche1-town-list.csv` — 495 towns, archetype‑assigned, confidence‑flagged
- `tranche1-generator.mjs` — regenerates the town list from the archetypes
- `canary-watch-framework.md` — the pre‑scale go/no‑go gate
- `canary-tracking-sheet.csv` — weekly Search Console log template
- `canary-watch-dashboard.html` — visual canary go/no‑go dashboard

**Prototypes (`prototypes/`) — one per distinct page type**
- `fr-coveralls-for-welders.html` — role guide + interactive standard‑finder tool
- `workwear-aberdeen.html` · `workwear-corby.html` · `workwear-harrogate.html` — industry‑driven local pages
- `hi-vis-workwear-guide.html` — content **hub** (pillar)
- `en-iso-20471-hi-vis-classes-explained.html` — **spoke** (standard explainer)
- `class-2-vs-class-3-hi-vis.html` — **spoke** (comparison / decision)
- `how-to-wash-fr-coveralls.html` — care / maintenance (HowTo)

**Immediate next steps** (order): finish the **canary gate** (§6.5) → in parallel, **decommission
risk** (§7) and author the **cluster spec + build harness** (Phase 1) → on green, **pilot tranche**.
