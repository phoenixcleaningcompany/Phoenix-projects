/**
 * iNeedWorkwear quantity breaks — the pricing rules, with no Shopify API in sight.
 *
 * Kept deliberately separate from run.js so the rules can be unit-tested on a
 * laptop, and so a Shopify API change never silently alters what a customer is
 * charged. These numbers mirror the pricing calculator exactly; if one moves,
 * move the other.
 */

/** Discount by total garment quantity in the cart. */
export const TIERS = [
  { min: 1,    discount: 0    },
  { min: 20,   discount: 0.05 },
  { min: 50,   discount: 0.10 },
  { min: 100,  discount: 0.15 },
  { min: 500,  discount: 0.20 },
  { min: 1000, discount: 0.25 },
];

/**
 * Premium garments get the break capped. Real competitor tables show a ~£9 tee
 * discounted 20% at qty 100 while a £55 jacket stops at 12% for 30+ and never
 * moves again. Without this cap we would be 29% under them at qty 1,000 on a
 * jacket they stopped discounting at 30 — giving away margin to win a race
 * nobody else is running.
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
