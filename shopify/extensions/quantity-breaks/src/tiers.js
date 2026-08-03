/**
 * iNeedWorkwear quantity breaks — the pricing rules, with no Shopify API in sight.
 *
 * Kept deliberately separate from run.js so the rules can be unit-tested on a
 * laptop, and so a Shopify API change never silently alters what a customer is
 * charged. These numbers mirror the pricing calculator exactly; if one moves,
 * move the other.
 */

/**
 * Discount by total garment quantity in the cart.
 *
 * The ladder used to start at 20. A scrape of 2,964 Workwear Express products
 * plus three verified break tables showed they start at 5-10 and give 10-12%
 * by qty 10 — so across 5-19 units, the commonest workwear order there is, they
 * discounted and we did not. At qty 1 we were 6.7% cheaper than them; at qty 10
 * we were 4.5% DEARER.
 */
export const TIERS = [
  { min: 1,    discount: 0    },
  { min: 5,    discount: 0.05 },
  { min: 10,   discount: 0.10 },
  { min: 25,   discount: 0.13 },
  { min: 50,   discount: 0.15 },
  { min: 100,  discount: 0.18 },
  { min: 250,  discount: 0.20 },
  { min: 1000, discount: 0.25 },
];

/**
 * Premium garments get the break capped, because competitors cut cheap garments
 * harder than expensive ones. The cap is 15%: a verified WWE ladder on a £40.30
 * jacket gives 5% at 5, 12% at 10 and 15% at 25, and stops there while a cheap
 * tee runs on to 20% at 250.
 *
 * A Shopify Function cannot read a variant's cost, so the exporter stamps this
 * onto expensive variants as the metafield custom.break_cap.
 */
export const CAP_METAFIELD = { namespace: "custom", key: "break_cap" };

/** Products carrying this tag are the logo line, not a garment. */
export const LOGO_TAG = "logo";

/** Highest tier whose threshold the quantity has reached. */
export function tierFor(quantity) {
  let discount = 0;
  for (const t of TIERS) {
    if (quantity >= t.min) discount = t.discount;
  }
  return discount;
}

/**
 * The break is driven by how many GARMENTS are being bought, not how many cart
 * lines there are. Someone ordering 60 polos across three colours has bought
 * 60 garments and gets the 50+ tier — splitting the order by colour must not
 * cost them the break.
 *
 * Logo lines are excluded from the count (they would double it) but still get
 * discounted, because decoration is where competitors cut hardest at volume.
 */
export function quantityBasis(lines) {
  return lines
    .filter((l) => !isLogoLine(l))
    .reduce((sum, l) => sum + (Number(l.quantity) || 0), 0);
}

export function isLogoLine(line) {
  const tags = line?.merchandise?.product?.hasTags ?? [];
  return tags.some((t) => t.tag?.toLowerCase() === LOGO_TAG && t.hasTag);
}

/** Per-variant cap, or null when the variant carries none. */
export function capFor(line) {
  const raw = line?.merchandise?.breakCap?.value;
  if (raw === undefined || raw === null || raw === "") return null;
  const n = Number(raw);
  return Number.isFinite(n) && n > 0 ? n : null;
}

/**
 * Discount for one cart line, as a percentage 0-100.
 * Returns null when the line earns nothing, so the caller can skip it entirely
 * rather than posting a 0% discount the customer would see as "-£0.00".
 */
export function discountForLine(line, basis) {
  let d = tierFor(basis);
  const cap = capFor(line);
  if (cap !== null) d = Math.min(d, cap);
  if (d <= 0) return null;
  return Math.round(d * 1000) / 10; // 0.15 -> 15.0, at Shopify's precision
}

/** Human-readable label shown against the discount at checkout. */
export function labelFor(basis) {
  return `Quantity break — ${basis} garments`;
}
