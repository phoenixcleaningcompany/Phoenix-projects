# Cluster build harness — the repeatable "hub + N spokes" recipe

This is how the useful‑content layer (~730 of the ~1,350 core pages) gets built at scale **without
duplication risk**. It follows the plan's core principle: **stop generating prose from a template —
author content as *data*, then render it through one component library.** Copy is never hand‑
duplicated across pages, and all the hub↔spoke↔shop wiring, breadcrumbs and schema are generated,
so broken links and near‑duplicates are *structurally* impossible.

**Proven:** the hi‑vis cluster in this folder regenerates the hub + 2 spokes from
`clusters/hi-vis.json` and passes all 27 QA gates (max sibling similarity 9%).

---

## The workflow

```
1. Author the cluster's content as data   →  clusters/<topic>.json
2. Generate the pages                      →  node render.mjs clusters/<topic>.json out
3. QA-gate the output                      →  node gates.mjs out
4. Stage (behind Directory Privacy) → watch canary → publish tranche
```

Steps 2–4 are mechanical and deterministic. **The only creative work is step 1** — researching and
writing the genuinely unique, real content (standards, tables, FAQs) into the data file. That's
where the information gain comes from; everything else is rendering.

### Where Claude Code plugs in
Claude Code (the way you built the cleaning 3,000) does **step 1**: given the cluster spec below and
a topic, it researches and drafts the structured JSON — real standards data, comparison tables, FAQ
answers, per‑page blocks. Then the **deterministic renderer** produces the pages. This split is the
safeguard: the LLM authors *unique substance per page*; it never controls layout, interlinking or
consistency, so it can't reintroduce the spun‑template failure. Gates catch anything thin or
duplicated before it ships.

---

## The cluster data schema

A cluster JSON has two parts: `cluster` (shared settings) and `pages` (the hub + spokes).

```jsonc
{
  "cluster": {
    "id": "hi-vis",                    // used in filenames/labels
    "topic": "Hi-vis",                 // brand copy + footer heading
    "shopLabel": "hi-vis",
    "shopUrl": "https://shop.ineedworkwear.co.uk/c/hi-vis",   // citation target
    "baseUrl": "https://www.ineedworkwear.co.uk",
    "date": "2026-07-08",
    "trust": ["…", "…"],               // trust-bar ticks (optional)
    "cta": { "h2": "…", "p": "…", "actions": [ {"label","href","style":"white|dark"} ] }
  },
  "pages": [
    {
      "slug": "hi-vis-workwear-guide",
      "role": "hub",                   // hub | spoke | care   (exactly one hub)
      "navLabel": "Hi-vis hub",        // used in auto nav/footer/breadcrumb
      "spokeType": "Standard explainer",   // spokes: the label chip
      "cardTitle": "…", "cardBlurb": "…",  // spokes: how the hub's spoke-grid shows it
      "crumbTail": "Standards",        // spokes: breadcrumb tail
      "kicker": "Standards hub · High-visibility workwear",   // hero eyebrow
      "h1": "…", "metaTitle": "…", "metaDesc": "…", "lede": "…",
      "heroCta": [ {"label","href","style":"orange|ghost"} ],   // optional
      "heroMeta": [ {"n":"EN ISO 20471","l":"The standard"} ],  // hero stat tiles
      "schema": { "type": "Article" },        // or {"type":"HowTo","steps":[{name,text}]}
      "blocks": [ … ordered content blocks … ],
      "faq": [ {"q":"…","a":"…"} ]             // powers FAQ block + FAQPage schema
    }
  ]
}
```

### Blocks (the component library)
Each page is an ordered list of typed blocks. Each renders as a design‑system component. `variant`
sets the section background (`""`=paper, `"alt"`=white, `"dark"`=navy); `narrow:true` constrains
width for reading. Content `html` fields accept authored inline markup (`<strong>`, `<a>`, `<em>`,
`<ul>`), so tables/links stay in the author's control.

| Block | Renders | Key fields |
|-------|---------|-----------|
| `prose` | A text section | `klabel, h2, html, narrow?, variant?` |
| `cards` | 3‑up card grid (e.g. classes) | `h2, lead, items:[{s,h3,area?,p,hot?}]` |
| `table` | Data table | `h2, lead, head:[…], rows:[[…]]` |
| `keyfacts` | Stat‑tile row | `h2, items:[{n,l}]` |
| `steps` | Numbered HowTo steps | `h2, items:[{h3,html}]` |
| `warnbar` | Warning callout | `html` |
| `citebox` | Inline citation → shop/spoke | `html` |
| `faq` | Accordion (from `page.faq`) | `klabel, h2` |
| `spokes` | **Auto** — hub's grid of spoke cards | *(derived from the cluster)* |
| `clusternav` | **Auto** — pill nav back to hub + siblings + shop | *(derived)* |

### What is auto‑wired (authors never touch)
- **Interlinking:** hub → every spoke (`spokes` block); every spoke → hub + siblings (`clusternav`);
  every page's footer lists the whole cluster + shop.
- **Breadcrumbs:** Home → Hub → Page, as `BreadcrumbList` JSON‑LD.
- **Schema:** `Article` (or `HowTo`) + `FAQPage` (from `faq`) + `BreadcrumbList`, injected per page.
- **Head:** title, meta description, canonical, Open Graph, fonts.
- **Chrome:** header/nav, hero, trust bar, CTA, footer — one design system, every page.

---

## The QA gates (`gates.mjs`)

Run over the generated output; **exit 1 if any fail.** Tunable thresholds at the top of the file.

| Gate | Rule |
|------|------|
| `unique-title` / `single-h1` | exactly one each |
| `canonical` / `schema` | canonical present; ≥2 JSON‑LD blocks incl. breadcrumb |
| `thin-content:words` | ≥ 350 visible words |
| `thin-content:data-blocks` | ≥ 1 data component (table/cards/steps/keyfacts) |
| `doorway:shop-ratio` | ≤ 12 shop links per 1,000 words |
| `interlinking` | ≥ 2 internal cluster links |
| `titles-distinct` | all page titles unique across the cluster |
| `hub-spoke-wired` | every spoke ↔ hub, both directions |
| `similarity` | max 8‑gram Jaccard between siblings ≤ 50% |

*(Verified: injecting a thin, shop‑stuffed, duplicate‑title page trips `thin-content`,
`doorway:shop-ratio` and `titles-distinct` — the gates are real, not rubber stamps.)*

---

## Add a new cluster (FR, footwear, gloves…)

1. Copy `clusters/hi-vis.json` → `clusters/fr.json`.
2. Change `cluster` settings (id/topic/shopUrl) and author the hub + spokes as data — real standards,
   tables, FAQs for that topic. (This is the Claude Code authoring step.)
3. `node render.mjs clusters/fr.json out-fr && node gates.mjs out-fr`.
4. Fix any gate failures (usually: add a data block, trim shop links, deepen a thin page), re‑run.

**Extending the component library:** a new block type = one new function in the `BLOCKS` map in
`render.mjs`. No template rewrites — every page type is just a different block sequence.

> `out/` is generated build output (git‑ignored). Regenerate it any time with `render.mjs`.
