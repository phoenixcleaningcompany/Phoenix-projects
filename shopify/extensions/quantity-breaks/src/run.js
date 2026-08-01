/**
 * Shopify entry point. Thin on purpose — every pricing decision lives in
 * tiers.js, which is unit-tested. This file only translates between Shopify's
 * input shape and that logic.
 *
 * Target: cart.lines.discounts.generate.run (Discount Function API, 2025-04+).
 * The older Product/Order/Shipping Discount APIs are deprecated and cannot be
 * mixed with this one.
 */
import { discountForLine, quantityBasis, labelFor } from "./tiers.js";

const EMPTY = { operations: [] };

export function run(input) {
  const lines = input?.cart?.lines ?? [];
  if (lines.length === 0) return EMPTY;

  // A discount can be configured to apply to products, shipping or order
  // total. Ours is a product discount; bail out if it has been set up as
  // anything else rather than silently doing nothing surprising.
  const classes = input?.discount?.discountClasses ?? [];
  if (classes.length > 0 && !classes.includes("PRODUCT")) return EMPTY;

  const basis = quantityBasis(lines);

  const candidates = [];
  for (const line of lines) {
    const percentage = discountForLine(line, basis);
    if (percentage === null) continue;
    candidates.push({
      message: labelFor(basis),
      targets: [{ cartLine: { id: line.id } }],
      value: { percentage: { value: percentage } },
    });
  }
  if (candidates.length === 0) return EMPTY;

  return {
    operations: [
      {
        productDiscountsAdd: {
          candidates,
          // Every qualifying line is discounted, not just the best one.
          selectionStrategy: "ALL",
        },
      },
    ],
  };
}
