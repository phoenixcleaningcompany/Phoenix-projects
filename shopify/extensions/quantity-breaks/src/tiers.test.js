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
  assert.equal(tierFor(4), 0);
  assert.equal(tierFor(5), 0.05);
  assert.equal(tierFor(9), 0.05);
  assert.equal(tierFor(10), 0.10);
  assert.equal(tierFor(24), 0.10);
  assert.equal(tierFor(25), 0.13);
  assert.equal(tierFor(50), 0.15);
  assert.equal(tierFor(100), 0.18);
  assert.equal(tierFor(250), 0.20);
  assert.equal(tierFor(1000), 0.25);
  assert.equal(tierFor(5000), 0.25);
});

test("the ladder starts before WWE's, at every tier they publish", () => {
  // Their verified ladders: 5% at 5, 10-12% at 10, 12-15% at 25.
  assert.ok(tierFor(5)  >= 0.05, "must discount from 5 units");
  assert.ok(tierFor(10) >= 0.10, "must match their 10-unit tier");
  assert.ok(tierFor(25) >= 0.13, "must match their 25-unit tier");
});

test("quantity is counted across lines, not per line", () => {
  // 60 polos split across three colours is still a 60-garment order.
  assert.equal(quantityBasis([garment(20), garment(20), garment(20)]), 60);
  assert.equal(discountForLine(garment(20), 60), 15);
});

test("logo lines are excluded from the count but still discounted", () => {
  const cart = [garment(50), logo(50)];
  assert.equal(quantityBasis(cart), 50, "logo units must not inflate the basis");
  assert.equal(discountForLine(cart[1], 50), 15, "decoration gets the break too");
});

test("premium garments have the break capped", () => {
  assert.equal(discountForLine(garment(1000, 0.15), 1000), 15);
  assert.equal(discountForLine(garment(1000), 1000), 25, "uncapped is unaffected");
  // cap only bites once the tier passes it
  assert.equal(discountForLine(garment(100, 0.15), 100), 15);
  assert.equal(discountForLine(garment(10, 0.15), 10), 10, "below the cap, unaffected");
});

test("no discount below the first threshold", () => {
  assert.equal(discountForLine(garment(1), 1), null);
  assert.equal(discountForLine(garment(4), 4), null);
});

test("malformed cap metafields are ignored rather than zeroing the break", () => {
  for (const bad of ["", "abc", "0", "-1", null]) {
    const line = garment(100);
    line.merchandise.breakCap = bad === null ? null : { value: bad };
    assert.equal(capFor(line), null, `cap ${JSON.stringify(bad)} should be ignored`);
    assert.equal(discountForLine(line, 100), 18);
  }
});

test("missing tag data does not crash the function", () => {
  assert.equal(isLogoLine({}), false);
  assert.equal(isLogoLine({ merchandise: {} }), false);
  assert.equal(quantityBasis([{ quantity: 5, merchandise: {} }]), 5);
});

test("percentages are emitted at Shopify's precision", () => {
  assert.equal(discountForLine(garment(5), 5), 5);
  assert.equal(discountForLine(garment(25), 25), 13);
  assert.equal(typeof discountForLine(garment(100), 100), "number");
  assert.equal(discountForLine(garment(100), 100), 18);
});
