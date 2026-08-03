#!/usr/bin/env python3
"""
Ralawise ShopifyExtendedDataFull_v2 -> iNeedWorkwear Shopify import CSV.

Ralawise refresh this feed daily at 1pm, so this is the file to rebuild from —
not the static price list. It carries the account price per colour AND size,
plus images, copy, live stock and spec metafields.

  Variant Price in the feed  = WHAT YOU PAY. Verified against the website's red
                               "Your Price": matches the published carton price
                               on 84% of rows and undercuts it on the rest.
  Variant Price we write out = what the customer pays, garment only at qty 1.
  Variant Cost we write out  = the feed price, so Shopify reports real profit.

Quantity breaks and the logo are NOT in here — breaks belong in a Shopify
Function, the logo is a priced line-item option. Neither can live in a variant.

Usage:
    python3 feed_to_shopify.py FEED.csv OUT.csv [--filter core] [--max-cost 45]
                               [--brands "Premier,Regatta Professional"]
                               [--in-stock-only]
"""
import csv, re, sys, argparse, collections

csv.field_size_limit(10 ** 9)

# ── pricing model — identical to the calculator's bands (rev 3, carton cost) ──
# Bands are keyed on what you PAY. Lifted 9% from the old pack-price bands and
# the edges shifted down 9%, so the shelf price is unchanged.
# Top two bands added from a 2,964-product scrape of Workwear Express, ex VAT
# on both sides. Their multiplier tapers steeply with cost and ours was almost
# flat, so we crossed above them at £12 and were dearer on 96% of products over
# £40 — jackets and softshells, where the 50-unit procurement orders live.
# Below £25 nothing changes: we are already cheaper there at qty 1.
MULT_BANDS = [(0, 1.91), (4.50, 2.02), (9, 1.96), (18.50, 1.85),
              (25, 1.70), (40, 1.60)]

def multiplier(cost):
    m = MULT_BANDS[0][1]
    for lo, v in MULT_BANDS:
        if cost >= lo:
            m = v
    return m

def sell_price(cost):
    raw = cost * multiplier(cost)
    if raw < 20:
        return round(raw, 2)
    return round(raw * 2) / 2          # snap larger items to the nearest 50p

# ── sizes ────────────────────────────────────────────────────────────────────
ORDER = ['3XS','2XS','XS','S','M','L','XL','2XL','3XL','4XL','5XL','6XL','7XL','8XL']
ALIAS = {'XXS':'2XS','XXXS':'3XS','XXL':'2XL','XXXL':'3XL','XXXXL':'4XL'}

def size_rank(s):
    s = ALIAS.get((s or '').strip().upper(), (s or '').strip().upper())
    return ORDER.index(s) if s in ORDER else 99

# ── what counts as decoratable workwear ──────────────────────────────────────
# An allowlist of Types beats keyword-matching titles: the feed's taxonomy is
# clean, and this way a new "Ladies' ¼-zip midlayer" lands in the right bucket
# without anyone editing a keyword list.
CORE_TYPES = {
    'T-Shirts','Hoodies','Polos','Sweatshirts','Jackets','Shirts',
    'Gilets & Body Warmers','Fleece','Trousers','Softshells','Shorts','Caps',
    'Sweatpants','Vests (t-shirt)','Blouses','Safety Vests','Beanies',
    'Knitted Jumpers','Trackwear','Chinos','Sports Overtops','Aprons',
    'Baselayers','Tunics','Cardigans','Hats','Chef Jackets','Tabards',
    'Coveralls','Rugby Shirts','Rain Suits','Dungarees','Waistcoats','Jeans',
    'Leggings','Ponchos','Snoods','Dresses','Skirts','Bodysuits',
}

# ── colour names ─────────────────────────────────────────────────────────────
# 13,421 rows carry footnote markers from Ralawise's own catalogue ("Bark*†").
# They mean something to a trade buyer reading the printed book and nothing at
# all to a customer on a size dropdown.
MARKERS = re.compile(r'[*†‡¹²³^~]+')

def clean_colour(c):
    return MARKERS.sub('', c or '').replace('  ', ' ').strip(' -')

def clean_title(t):
    """Ralawise titles carry stray inch-marks — 'seamless 3D fit" multi-sport'.
    They read as broken punctuation on a listing page and in a search result."""
    t = (t or '').replace('"', '').replace('“', '').replace('”', '')
    return ' '.join(t.split()).strip(' -,')

# The colours a workwear buyer actually orders. Kept first when a product has
# more colours than Shopify will take in one listing.
STAPLES = {'black','navy','white','french navy','charcoal','grey','graphite',
           'royal','royal blue','bottle green','red','burgundy','sky','sky blue',
           'heather grey','oxford navy','dark grey','light grey','yellow','orange'}

VENDOR_MAP = {'2786': 'Tee Jays'}       # the one supplier the feed leaves as a code

# ── SEO ──────────────────────────────────────────────────────────────────────
# Ralawise's own copy goes out to every workwear site in the country, so the
# body text can't win search. These tags are built from facts THIS listing has
# and the competition doesn't — colour count, size range, and the offer — so
# they read as a real page rather than spun filler. Deliberately mechanical:
# it's the body copy that a human should rewrite, on the 30-50 lines that matter.
TYPE_SINGULAR = {
    'T-Shirts':'T-Shirt', 'Hoodies':'Hoodie', 'Polos':'Polo Shirt',
    'Sweatshirts':'Sweatshirt', 'Jackets':'Jacket', 'Shirts':'Shirt',
    'Gilets & Body Warmers':'Bodywarmer', 'Fleece':'Fleece',
    'Trousers':'Trousers', 'Softshells':'Softshell Jacket', 'Shorts':'Shorts',
    'Caps':'Cap', 'Sweatpants':'Joggers', 'Vests (t-shirt)':'Vest',
    'Blouses':'Blouse', 'Safety Vests':'Hi-Vis Vest', 'Beanies':'Beanie',
    'Knitted Jumpers':'Jumper', 'Trackwear':'Tracksuit', 'Chinos':'Chinos',
    'Sports Overtops':'Overtop', 'Aprons':'Apron', 'Baselayers':'Baselayer',
    'Tunics':'Tunic', 'Cardigans':'Cardigan', 'Hats':'Hat',
    'Chef Jackets':'Chef Jacket', 'Tabards':'Tabard', 'Coveralls':'Coverall',
    'Rugby Shirts':'Rugby Shirt', 'Rain Suits':'Rain Suit',
    'Dungarees':'Dungarees', 'Waistcoats':'Waistcoat', 'Jeans':'Jeans',
    'Leggings':'Leggings', 'Ponchos':'Poncho', 'Snoods':'Snood',
    'Dresses':'Dress', 'Skirts':'Skirt', 'Bodysuits':'Bodysuit',
}
SEO_TITLE_MAX, SEO_DESC_MAX = 60, 155

# ── quantity-break cap ───────────────────────────────────────────────────────
# A Shopify Function cannot read a variant's cost, so the cap has to travel with
# the variant. Premium garments stop at 15%. The cap was 10%, set when TS007
# appeared to stop at 12% for 30+; a verified WWE ladder on TJ133 — a £40.30
# jacket — shows 5% at 5, 12% at 10 and 15% at 25, so 10% was too tight and was
# costing us the premium end of the range.
BREAK_CAP_COST, BREAK_CAP_PCT = 20.0, 0.15
CAP_COL = 'Variant Metafield: custom.break_cap [number_decimal]'

def singular(t):
    t = (t or '').strip()
    return TYPE_SINGULAR.get(t) or (t[:-1] if t.endswith('s') else t) or 'Workwear'

def trim_to(s, limit):
    """Cut at a word boundary, never mid-word, never leaving dangling punctuation."""
    s = ' '.join((s or '').split())
    if len(s) <= limit:
        return s
    cut = s[:limit].rsplit(' ', 1)[0]
    return cut.rstrip(' ,;:-–—') or s[:limit]

def seo_title(title, vendor, ptype, taken=None):
    """'<product> | Embroidered & Printed <type>', shortened as the budget runs out.

    Ladder down to ever-shorter tails rather than giving up: a title with no
    intent keyword at all ranks for nothing but the product's own name, which
    every other Ralawise reseller is also using.
    """
    base = singular(ptype)
    tails = [f" | Embroidered & Printed {base}", f" | Custom {base}",
             f" | Custom Branded {base}", f" | Custom Workwear",
             f" | Embroidered", f" | {vendor}", ""]
    for tail in tails:
        cand = title + tail
        if len(cand) <= SEO_TITLE_MAX and not (taken and cand in taken):
            return cand
    for tail in tails:                      # length was the binding constraint
        if len(title) + len(tail) <= SEO_TITLE_MAX:
            return title + tail
    return trim_to(title, SEO_TITLE_MAX)

def seo_desc(title, ptype, n_colours, size_lo, size_hi, free_ship=40):
    bits = [title]
    if n_colours > 1:
        bits.append(f"in {n_colours} colours")
    if size_lo and size_hi and size_lo != size_hi:
        bits.append(f"{size_lo}-{size_hi}")
    lead = ' '.join(bits).rstrip('.') + '.'
    offer = (f" Embroidered or printed with your logo. Free digitising, "
             f"free UK delivery over £{free_ship}.")
    if len(lead) + len(offer) <= SEO_DESC_MAX:
        return lead + offer
    short = " Your logo embroidered or printed. Free digitising."
    if len(lead) + len(short) <= SEO_DESC_MAX:
        return lead + short
    return trim_to(lead, SEO_DESC_MAX)

META = [
    ('Metafield: my_fields.fabric [single_line_text_field]',            'fabric'),
    ('Metafield: my_fields.weight_gsm [single_line_text_field]',        'weight_gsm'),
    ('Metafield: my_fields.washing_instructions [single_line_text_field]', 'washing_instructions'),
    ('Metafield: my_fields.specification [single_line_text_field]',     'specification'),
    ('Metafield: my_fields.gender [single_line_text_field]',            'gender'),
    ('Metafield: my_fields.accreditations [list.single_line_text_field]', 'accreditations'),
    ('Metafield: size_guide [url]',                                     'size_guide'),
]

OUT = ['Handle','Title','Body (HTML)','Vendor','Type','Tags','Published',
       'Option1 Name','Option1 Value','Option2 Name','Option2 Value',
       'Variant SKU','Variant Grams','Variant Weight Unit',
       'Variant Inventory Tracker','Variant Inventory Qty',
       'Variant Inventory Policy','Variant Fulfillment Service',
       'Variant Price','Variant Compare At Price','Variant Requires Shipping',
       'Variant Taxable','Variant Cost','Image Src','Image Position',
       'Image Alt Text','Variant Image','SEO Title','SEO Description',
       CAP_COL,'Status'] + \
      [f'Metafield: custom.{k} [single_line_text_field]' for _, k in META]


def money(x):
    try:
        return float(str(x).replace('£', '').replace(',', '').strip())
    except (ValueError, AttributeError):
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('infile'); ap.add_argument('outfile')
    ap.add_argument('--filter', choices=['core', 'all'], default='core')
    ap.add_argument('--max-cost', type=float, default=None)
    ap.add_argument('--brands', default=None)
    ap.add_argument('--in-stock-only', action='store_true')
    ap.add_argument('--max-variants', type=int, default=100,
                    help='Shopify caps a product at 100 variants on standard '
                         'plans. Colours are dropped, deepest-stocked kept, '
                         'until the product fits. 0 = no cap.')
    ap.add_argument('--free-ship', type=int, default=40,
                    help='free-delivery threshold quoted in the meta description')
    ap.add_argument('--publish', action='store_true',
                    help='write Status=active. Default is draft — nothing goes '
                         'live until you have looked at it.')
    a = ap.parse_args()

    brands = {b.strip().lower() for b in a.brands.split(',')} if a.brands else None

    prods = collections.OrderedDict()
    n_in = skipped = bad = 0
    for row in csv.DictReader(open(a.infile, encoding='utf-8-sig', errors='replace')):
        n_in += 1
        h    = (row.get('Handle') or '').strip()
        cost = money(row.get('Variant Price'))
        size = (row.get('Option2 Value') or '').strip()
        sku  = (row.get('Variant SKU') or '').strip()
        # One row in the source is mis-quoted and spills a description into the
        # status column; anything without a handle, SKU and price is unusable.
        if not h or not sku or cost is None or cost <= 0:
            bad += 1; continue
        if a.filter == 'core' and row.get('Type') not in CORE_TYPES:
            skipped += 1; continue
        if a.max_cost and cost > a.max_cost:
            skipped += 1; continue
        vendor = VENDOR_MAP.get((row.get('Vendor') or '').strip(),
                                (row.get('Vendor') or '').strip())
        if brands and vendor.lower() not in brands:
            skipped += 1; continue
        try:
            qty = int(float(row.get('Variant Inventory Qty') or 0))
        except ValueError:
            qty = 0
        if a.in_stock_only and qty <= 0:
            skipped += 1; continue

        p = prods.setdefault(h, {'row': row, 'vendor': vendor, 'variants': [],
                                 'images': [], 'seen_img': set()})
        p['variants'].append({
            'colour': clean_colour(row.get('Option1 Value')),
            'size': size, 'sku': sku, 'cost': cost, 'qty': qty,
            'grams': (row.get('Variant Grams') or '').strip(),
            'vimg': (row.get('Variant Image') or '').strip(),
        })
        # Image Src is a semicolon-separated list — a lifestyle shot plus the
        # per-colour shot. Dedupe across the whole product and renumber: the
        # feed stamps every image Position 1, which Shopify will not accept.
        for u in (row.get('Image Src') or '').split(';'):
            u = u.strip()
            if u and u not in p['seen_img']:
                p['seen_img'].add(u); p['images'].append(u)

    n_prod = n_var = n_ratchet = n_trimmed = n_dropped_col = 0
    seen_titles = set()
    with open(a.outfile, 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, fieldnames=OUT, extrasaction='ignore')
        w.writeheader()
        for h, p in prods.items():
            src, alt = p['row'], (p['row'].get('Image Alt Text') or '').strip()
            # group by colour, then price up the size ladder within each colour
            by_col = collections.OrderedDict()
            for v in p['variants']:
                by_col.setdefault(v['colour'], []).append(v)

            # A jacket in 29 colours across 8 sizes is 232 variants and Shopify
            # rejects the product outright. Keep the colours actually worth
            # listing — the workwear staples first, then whatever is stocked
            # deepest — and drop the long tail of one-off shades.
            if a.max_variants and len(p['variants']) > a.max_variants:
                ranked = sorted(
                    by_col.items(),
                    key=lambda kv: (clean_colour(kv[0]).lower() not in STAPLES,
                                    -sum(v['qty'] for v in kv[1])))
                kept, used = collections.OrderedDict(), 0
                for colour, vs in ranked:
                    if used + len(vs) > a.max_variants and kept:
                        n_dropped_col += 1
                        continue
                    kept[colour] = vs; used += len(vs)
                by_col = kept
                n_trimmed += 1

            lines = []
            for colour, vs in by_col.items():
                vs.sort(key=lambda v: size_rank(v['size']))
                floor = 0.0
                for v in vs:
                    raw = sell_price(v['cost'])
                    # A bigger size costs more but can land in a lower band and
                    # come out cheaper. Nobody believes a 3XL under the 2XL.
                    if raw < floor - 0.001:
                        n_ratchet += 1
                    v['price'] = max(raw, floor)
                    floor = v['price']
                    lines.append((colour, v))

            # Size range for the meta description, taken AFTER trimming so it
            # describes what the page actually offers.
            ranked = sorted({v['size'] for _, v in lines if size_rank(v['size']) < 99},
                            key=size_rank)
            title, ptype = clean_title(src.get('Title', '')), src.get('Type', '')
            s_title = seo_title(title, p['vendor'], ptype, seen_titles)
            seen_titles.add(s_title)
            s_desc  = seo_desc(title, ptype, len(by_col),
                               ranked[0] if ranked else '',
                               ranked[-1] if ranked else '',
                               a.free_ship)

            imgs = p['images']
            nrows = max(len(lines), len(imgs))
            for i in range(nrows):
                rec = {'Handle': h}
                if i == 0:
                    rec.update({
                        'Title': title,
                        'Body (HTML)': src.get('Body (HTML)', ''),
                        'Vendor': p['vendor'],
                        'Type': src.get('Type', ''),
                        'Tags': ','.join(x for x in [p['vendor'], h, src.get('Type', ''), 'garment'] if x),
                        'Published': 'TRUE' if a.publish else 'FALSE',
                        'Option1 Name': 'Colour', 'Option2 Name': 'Size',
                        'SEO Title': s_title, 'SEO Description': s_desc,
                        'Status': 'active' if a.publish else 'draft',
                    })
                    for col, key in META:
                        rec[f'Metafield: custom.{key} [single_line_text_field]'] = \
                            (src.get(col) or '').strip()
                if i < len(lines):
                    colour, v = lines[i]
                    rec.update({
                        'Option1 Value': colour, 'Option2 Value': v['size'],
                        'Variant SKU': v['sku'], 'Variant Grams': v['grams'],
                        'Variant Weight Unit': 'g',
                        'Variant Inventory Tracker': '',
                        'Variant Inventory Qty': v['qty'],
                        'Variant Inventory Policy': 'continue',
                        'Variant Fulfillment Service': 'manual',
                        'Variant Price': f"{v['price']:.2f}",
                        'Variant Cost': f"{v['cost']:.2f}",
                        'Variant Requires Shipping': 'TRUE',
                        'Variant Taxable': 'TRUE',
                        'Variant Image': v['vimg'],
                        CAP_COL: (f"{BREAK_CAP_PCT}" if v['cost'] >= BREAK_CAP_COST else ''),
                    })
                    n_var += 1
                if i < len(imgs):
                    rec.update({'Image Src': imgs[i], 'Image Position': i + 1,
                                'Image Alt Text': alt})
                w.writerow(rec)
            n_prod += 1

    # Only variants that actually made it into the file — a trimmed colour has
    # a cost but never got priced, so the two lists must come from one walk.
    sold = [(v['price'], v['cost']) for p in prods.values()
            for v in p['variants'] if 'price' in v and v['price'] > 0]
    gm = sum((pr - c) / pr for pr, c in sold) / max(1, len(sold))

    print(f"read {n_in:,} feed rows  ->  wrote {a.outfile}")
    print(f"  {n_prod:,} products   {n_var:,} variants   "
          f"{sum(len(p['images']) for p in prods.values()):,} images")
    print(f"  filtered out {skipped:,}   unusable {bad:,}")
    print(f"  garment gross margin (before decoration, qty 1): {gm*100:.1f}%")
    if n_trimmed:
        print(f"  {n_trimmed:,} products trimmed to fit {a.max_variants} variants "
              f"({n_dropped_col:,} colours dropped, staples and deepest stock kept)")
    if n_ratchet:
        print(f"  {n_ratchet:,} variants lifted so a bigger size is never cheaper")
    print(f"  status: {'ACTIVE — goes live on import' if a.publish else 'draft'}")


if __name__ == '__main__':
    main()
