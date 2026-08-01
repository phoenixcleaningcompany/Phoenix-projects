import test from "node:test";
import assert from "node:assert/strict";
import {
  tierFor, quantityBasis, isLogoLine, capFor, discountForLine,
} from "./tiers.js";

const garment = (quantity, cap = null) => ({
  quantity,
  merchandise: {
    breakCap: cap === null ? null : { value: String(cap) },
    product: { hasTags: [{ tag: "logo", hasTag: false }] },
  },
});
const logo = (quantity) => ({
  quantity,
  merchandise: {
    breakCap: null,
    product: { hasTags: [{ tag: "logo", hasTag: true }] },
  },
});

test("tier thresholds match the pricing calculator", () => {
  assert.equal(tierFor(1), 0);
  assert.equal(tierFor(19), 0);
  assert.equal(tierFor(20), 0.05);
  assert.equal(tierFor(49), 0.05);
  assert.equal(tierFor(50), 0.10);
  assert.equal(tierFor(100), 0.15);
  assert.equal(tierFor(499), 0.15);
  assert.equal(tierFor(500), 0.20);
  assert.equal(tierFor(1000), 0.25);
  assert.equal(tierFor(5000), 0.25);
});

test("quantity is counted across lines, not per line", () => {
  // 60 polos split across three colours is still a 60-garment order.
  assert.equal(quantityBasis([garment(20), garment(20), garment(20)]), 60);
  assert.equal(discountForLine(garment(20), 60), 10);
});

test("logo lines are excluded from the count but still discounted", () => {
  const cart = [garment(50), logo(50)];
  assert.equal(quantityBasis(cart), 50, "logo units must not inflate the basis");
  assert.equal(discountForLine(cart[1], 50), 10, "decoration gets the break too");
});

test("premium garments have the break capped", () => {
  assert.equal(discountForLine(garment(1000, 0.10), 1000), 10);
  assert.equal(discountForLine(garment(1000), 1000), 25, "uncapped is unaffected");
  // cap only bites once the tier passes it
  assert.equal(discountForLine(garment(50, 0.10), 50), 10);
  assert.equal(discountForLine(garment(20, 0.10), 20), 5);
});

test("no discount below the first threshold", () => {
  assert.equal(discountForLine(garment(1), 1), null);
  assert.equal(discountForLine(garment(19), 19), null);
});

test("malformed cap metafields are ignored rather than zeroing the break", () => {
  for (const bad of ["", "abc", "0", "-1", null]) {
    const line = garment(100);
    line.merchandise.breakCap = bad === null ? null : { value: bad };
    assert.equal(capFor(line), null, `cap ${JSON.stringify(bad)} should be ignored`);
    assert.equal(discountForLine(line, 100), 15);
  }
});

test("missing tag data does not crash the function", () => {
  assert.equal(isLogoLine({}), false);
  assert.equal(isLogoLine({ merchandise: {} }), false);
  assert.equal(quantityBasis([{ quantity: 5, merchandise: {} }]), 5);
});

test("percentages are emitted at Shopify's precision", () => {
  assert.equal(discountForLine(garment(20), 20), 5);
  assert.equal(discountForLine(garment(100), 100), 15);
  assert.equal(typeof discountForLine(garment(100), 100), "number");
});
