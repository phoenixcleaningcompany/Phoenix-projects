# iNeedWorkwear — Shopify quantity breaks

A Shopify Function that applies the volume ladder from the pricing calculator to
the storefront cart.

## What it does

| Garments in cart | Discount |
|---|---|
| 1–19 | — |
| 20–49 | 5% |
| 50–99 | 10% |
| 100–499 | 15% |
| 500–999 | 20% |
| 1,000+ | 25% |

Three rules that are easy to get wrong, so they are tested:

**The ladder is driven by total garments, not per line.** Sixty polos split
across three colours is a 60-garment order and earns the 50+ tier. Splitting an
order by colour or size must never cost the customer their break.

**Decoration gets the break too.** Competitor baskets cut decoration 33.9%
between qty 10 and 1,000 while the garment moves only 13.9% — setup and handling
amortise, a bought-in blank doesn't. Holding logo prices flat at volume would
wipe out the price advantage on exactly the orders worth winning. Logo lines are
excluded from the *count* (they'd double it) but still receive the discount.

**Premium garments are capped at 10%.** A ~£9 tee gets discounted 20% at qty 100
by competitors, but a £55 jacket stops at 12% for 30+ and never moves again. An
uncapped ladder would put us 29% under them at qty 1,000 on a jacket they
stopped discounting at 30.

## The cap metafield

A Shopify Function **cannot read a variant's cost**, so the cap has to travel
with the variant. `feed_to_shopify.py` writes it:

```
Variant Metafield: custom.break_cap [number_decimal] = 0.1
```

on every variant costing £20 or more — currently 15.5% of the core range. A
variant with no metafield is uncapped. Malformed values are ignored rather than
zeroing the break, so a bad import degrades to "full discount", never to
"customer silently overcharged".

Logo products must carry the tag `logo`. Garments are tagged `garment` by the
exporter.

## Layout

```
extensions/quantity-breaks/
  shopify.extension.toml   target, API version, input query
  src/tiers.js             the pricing rules — no Shopify API
  src/tiers.test.js        8 tests, run with `npm test`
  src/run.js               translates Shopify input to those rules
  src/run.graphql          what the Function asks Shopify for
```

`tiers.js` is deliberately free of Shopify types so the rules can be tested on a
laptop in milliseconds, and so an API change can never silently alter what a
customer is charged.

```bash
cd extensions/quantity-breaks && npm test
```

## Deploying

This repo has no app scaffold and the Shopify CLI is not installed here, so the
function has not been deployed or run against a live cart.

```bash
npm install -g @shopify/cli
shopify app init                      # once, if there is no app yet
# copy extensions/quantity-breaks into the app's extensions/ directory
shopify app dev                       # test against a development store
shopify app deploy
```

Then in Shopify admin: **Discounts → Create discount → Quantity breaks**, set it
to apply automatically to all products.

## Verify before trusting it

`tiers.js` is tested and correct. `run.js` and the TOML target the Discount
Function API (`cart.lines.discounts.generate.run`, API version 2025-04+), which
replaced the separate Product, Order and Shipping discount APIs — those are
deprecated and cannot be mixed with this one.

**Check two things against whatever `shopify app init` scaffolds**, because they
move between versions and were written here without a live CLI to check against:

1. `api_version` in `shopify.extension.toml` — set to `2025-10`.
2. The exact shape of the returned operation (`productDiscountsAdd`,
   `selectionStrategy`, `value.percentage.value`).

If either is wrong the CLI will say so at build time. The tiers will not change.

## Worth knowing: you may not need this

Since April 2026 Shopify offers **native quantity price breaks on all plans**
through B2B catalogs — no code, set per-product tiers in admin. The catch is
that they only apply to B2B company accounts, not ordinary storefront visitors.

That maps onto the two-tier model well:

- **Concierge / trade customers** — give them a company account and use native
  B2B price breaks. No code to maintain, and it gets you account-specific
  pricing, payment terms and a proper buyer login for free.
- **Self-serve storefront** — needs this Function, because B2B catalogs don't
  reach anonymous shoppers.

Running B2B for trade and this Function for self-serve is more moving parts than
starting with one. If most volume orders will come through the concierge route
anyway, do B2B first and leave this function on the shelf until self-serve
volume orders actually appear.
