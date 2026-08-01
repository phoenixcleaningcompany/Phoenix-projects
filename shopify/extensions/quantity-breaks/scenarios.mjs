// Prints the discount for a set of realistic carts — run with `npm run scenarios`.
import { run } from "./src/run.js";
const line = (id, qty, { logo = false, cap = null } = {}) => ({
  id: `gid://shopify/CartLine/${id}`, quantity: qty,
  merchandise: { breakCap: cap === null ? null : { value: String(cap) },
    product: { hasTags: [{ tag: "logo", hasTag: logo }] } },
});
const show = (name, cart, discount = { discountClasses: ["PRODUCT"] }) => {
  const out = run({ cart: { lines: cart }, discount });
  const c = out.operations[0]?.productDiscountsAdd?.candidates ?? [];
  console.log(`\n${name}`);
  if (!c.length) return console.log("   no discount");
  console.log(`   "${c[0].message}"`);
  for (const x of c) console.log(`   ${x.targets[0].cartLine.id.split("/").pop()}  ${x.value.percentage.value}%`);
};
show("3 polos + logo (below first tier)", [line(0,3), line(1,3,{logo:true})]);
show("60 polos across 3 colours + logo", [line(0,20), line(1,20), line(2,20), line(3,60,{logo:true})]);
show("100 tees + 100 logos", [line(0,100), line(1,100,{logo:true})]);
show("100 premium jackets (capped) + logos", [line(0,100,{cap:0.10}), line(1,100,{logo:true})]);
show("mixed: 60 cheap tees + 40 capped jackets", [line(0,60), line(1,40,{cap:0.10})]);
show("1000 tees", [line(0,1000)]);
show("shipping-only discount config", [line(0,100)], { discountClasses: ["SHIPPING"] });
show("empty cart", []);
