# Canary-Watch Framework — the cleaning site as the go/no-go gate

**Purpose:** Before replicating the programmatic model on iNeedWorkwear (and putting the
workwear domain *and* the future Shopify store's reputation behind it), read how Google actually
treats the freshly-launched Phoenix Duct Clean 3,000. This turns the "should we scale?" decision
from a gut call into a measured one.

**The one question:** *Is Google accepting these pages as valuable, or quietly judging them thin,
duplicate or low-value?* Everything below answers that as early and as objectively as possible.

> **Why this gate exists.** The cleaning site went live only days ago, so its "success" so far is
> that it passed *our* quality gates. Whether it passes *Google's* is unknown and takes weeks to
> read. Watching one domain's data is far cheaper than discovering the answer on two.

---

## 0. Setup — do this on day 0 (once)

1. **Verify the site in Google Search Console (GSC)** — use a **Domain property** if you control DNS
   (covers http/https + www/non-www), otherwise a URL-prefix property for the exact live origin.
2. **Submit an XML sitemap — segmented by page type.** This is the single most valuable setup step.
   Instead of one `sitemap.xml`, submit several:
   - `sitemap-locations.xml` (the town/service-area pages)
   - `sitemap-editorial.xml` (the guides / answer pages)
   - `sitemap-core.xml` (home + the main service/hub pages)
   Segmenting lets GSC show indexation **per page type**, so you can see *which pattern Google likes*
   — the most important diagnostic you can have.
3. **Set a baseline** — record the total URL count per sitemap (week 0).
4. **Do NOT mass-request indexing** via URL Inspection. Let Google crawl naturally — forced indexing
   hides the very signal (does Google *choose* to index this?) you're trying to measure.
5. **Add Bing Webmaster Tools** as a cheap second opinion (Bing often indexes faster).
6. **Connect GA4** (or your analytics) so you can see organic sessions by landing page later.
7. **Bookmark the Google Search Status Dashboard** to align any ranking swings with known core/spam
   updates.

---

## 1. The signal ladder — read from earliest to most durable

Signals arrive in order. **Indexation comes first and is the most honest; rankings and traffic lag.**
Don't wait for traffic to decide — the index report tells you in weeks.

### Phase 1 · Crawl & Index (weeks 1–4) — the earliest, clearest verdict
Where: **GSC → Pages** (Index report) and **GSC → Sitemaps**.

Track the **indexation ratio** — of the URLs submitted, how many are **Indexed** vs **Not indexed** —
and, crucially, the *reasons* under "Not indexed". The tell-tale buckets:

| GSC status | What it means | Read |
|---|---|---|
| **Crawled – currently not indexed** | Google crawled it and chose not to index | ⚠️ The clearest "low-value/thin" verdict when it's a large share |
| **Discovered – currently not indexed** | Known but not even crawled yet | ⚠️ Crawl-budget / perceived-low-priority at scale |
| **Duplicate without user-selected canonical** | Duplication detected | 🚩 Directly the town-swap risk |
| **Duplicate, Google chose different canonical** | Google merged it with another page | 🚩 Near-duplicate cluster |
| **Soft 404** | Perceived thin/empty | ⚠️ Thin content |
| **Alternate page with proper canonical** | Intentional canonical | ✅ Usually fine |

**What "good" looks like:** the Indexed count climbs steadily over days/weeks toward most of the
submitted set, and the "Crawled/Discovered – not indexed" buckets stay small and shrink.
**What "bad" looks like:** indexation plateaus at a low fraction with a big "Crawled – currently not
indexed" pile — Google has seen the pages and declined them.

> **New-domain caveat:** a brand-new site indexes *slowly regardless of quality*, so week-1–2 low
> numbers are not yet a verdict. It's the **trend over weeks 2–8** that matters.

### Phase 2 · Impressions & early ranking (weeks 3–8)
Where: **GSC → Performance** (Search results). Also the crude `site:phoenixductclean.com` count.

- **Impressions rising** across the indexed set = Google is surfacing/testing the pages. Good.
- **Indexed but ~zero impressions** = indexed yet not ranked — weak pages.
- **Query spread widening** (Performance → Queries) = genuine topical relevance building.
- **Per-page-type split** (filter Performance by URL, or use the segmented sitemaps) = which family
  earns impressions. Maybe location pages perform and thin ones don't — that's actionable gold.

### Phase 3 · Durability & quality (weeks 8–16+) — the real test
- **Sustained rankings** — do positions hold and climb, or **spike then decay**? The classic
  thin-content signature is a "new-content honeymoon" bump that fades after a few weeks.
- **Manual Actions** — GSC → **Security & Manual Actions**. A *thin content* or *pure spam* action
  is a hard stop (rare, but decisive).
- **Core-update behaviour** — the definitive test. Across the next core/spam update, did the site
  **gain, hold, or drop**? A drop across an update = the model is on the wrong side of the line.
- **Site-wide health** — do the *good* pages (home, service hubs) still rank, or is the whole domain
  suppressed by the thin layer?
- **Traffic → outcomes** — organic sessions and actual enquiries/referrals (GA4).

---

## 2. What to log each week

Use `canary-tracking-sheet.csv` (in this repo). Weekly, record per segmented sitemap where possible:
Submitted · Indexed · Indexed % · Crawled-not-indexed · Discovered-not-indexed · Duplicate(any) ·
Impressions (28d) · Clicks (28d) · Avg position · `site:` count · Manual action? · Notes.

Ten minutes a week. The **trend** is the product, not any single week.

---

## 3. Go / Amber / Red — the decision thresholds

Read at the **week-8 provisional checkpoint** and confirmed at **week 12–16 + first core update.**

| Signal | 🟢 GREEN — replicate on workwear | 🟠 AMBER — revise the model first | 🔴 RED — do not replicate |
|---|---|---|---|
| **Indexation ratio** (wk 6–8) | **≥ 70–80%** and climbing/stable | 40–70% and plateauing | **< 40%** and flat/falling |
| **"Crawled/Discovered – not indexed"** | Small minority, shrinking | Sizeable, static | **Large share** of the set |
| **Duplicate-canonical statuses** | Negligible | Present on a page-type | 🚩 Big share (town-swap rejected) |
| **Impressions** | Rising, widening queries | Flat on many indexed pages | ~Zero across indexed pages |
| **Ranking durability** | Holds/climbs to wk 16 | Wobbly | **Spike-then-decay**, or drop across an update |
| **Manual action** | None | None | Any thin/spam action |
| **Good/hub pages** | Rank normally | Mixed | Suppressed site-wide |

**Decision rules**
- **GREEN** → the model works. Greenlight the workwear replication (tranche-by-tranche, still
  phased). Keep watching.
- **AMBER** → the *idea* works but a **specific family is weak** (the segmented sitemaps will name
  it). Fix that pattern's uniqueness/value on the cleaning site, re-test, *then* replicate only the
  proven families. Do not scale the weak one.
- **RED** → the thin/duplicate pattern is being rejected. **Do not touch workwear with it.** Rebuild
  the cleaning model first (more per-page uniqueness, prune/consolidate the rejected pages) — you've
  learned it cheaply on one domain instead of two.

---

## 4. Interpretation traps (don't get fooled)

- **The honeymoon.** New content often gets a temporary boost, then Google re-evaluates. An early
  ranking spike is *not* proof — durability at 8–16 weeks and across an update is.
- **Slow initial index ≠ failure.** New domains crawl slowly; judge the trend, not week 1.
- **Correlation with updates.** Before blaming the model for a swing, check the Search Status
  Dashboard — a move may be a dated core update (which is itself the signal you want).
- **Indexed-then-dropped.** Watch for pages that index then fall out weeks later — that's a *late
  negative verdict*, worse than never indexing.
- **Averages hide the story.** A healthy home page can prop up a site-wide average while the
  programmatic layer quietly fails. Always read **per page type**.

---

## 5. Cadence summary

| When | Action |
|---|---|
| **Day 0** | Verify GSC · submit segmented sitemaps · baseline · connect Bing/GA4 |
| **Weekly, wk 1–8** | Log the row in the tracking sheet (10 min) |
| **Week 8** | **Provisional go/amber/red checkpoint** |
| **Week 12–16 + next core update** | **Final confirmation** — durability is the real test |
| **Throughout** | Keep the workwear build ready but **unpublished** until GREEN |

**Bottom line:** don't spend the cleaning site's data by rushing. In a few weeks it will tell you —
from your own 3,000 pages — exactly how Google treats this model, which beats any amount of guessing
about competitors.
