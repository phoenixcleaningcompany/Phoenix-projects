#!/usr/bin/env python3
# RT (Supermarkets & Retail) series builder v1.0
# Read SPEC.md / CLAUDE.md first. CONCIERGE / Template A (procurement buyer), but
# TARGETS INDEPENDENTS (independent retailers, convenience stores, forecourts,
# garden centres, farm shops, small multi-store groups) - NOT the big chains,
# which procure centrally via national tender. Staff-uniform led: the staff are
# the shopfront. Lead = TABARD + POLO + FLEECE. Medium depth, LOW local variation
# (the two generic shared paras live in SHOPFRONT_POOL / CONSIST_POOL, not in the
# per-town s1loc - see s1_paras). Exactly 14 .com + 1 community link per page. No
# JS, no HTML entities, no delivery-timescale claims. Nearby MUST be
# geographically close, hand-authored, on RT_towns.csv (no rank fallback).
import re, os, json, zlib, sys, csv

import hashlib
def pick(key, salt, n):
    # md5 gives well-distributed bits; crc32 % n leaks correlated low bits,
    # so all same-length town names collided on the same pool variant at once.
    h = hashlib.md5((salt + '|' + str(key).lower()).encode()).digest()
    return int.from_bytes(h[:4], 'big') % n

def _find_base():
    here = os.path.dirname(os.path.abspath(__file__))
    for p in (os.path.join(here,'rt-london.html'),'rt-london.html',
              '/mnt/user-data/outputs/rt-london.html','/home/claude/rtkit/rt-london.html'):
        if os.path.exists(p): return p
    sys.exit("ERROR: rt-london.html (base template) not found beside rt_build.py")

BASE = open(_find_base(), encoding='utf-8').read()
DOMAIN = 'https://www.ineedworkwear.uk'

def between(start, end, src=BASE):
    i = src.index(start); j = src.index(end, i+len(start)); return src[i:j]
def aria_block(aria):
    k = BASE.index(aria)
    i = BASE.rfind('<div class="rt-wrap"><div class="rt-illust">', 0, k)
    j = BASE.index('</div></div></div>', k) + len('</div></div></div>')
    return BASE[i:j]

CSS      = between('<style>', '</style>') + '</style>'
HEADER   = between('<div class="rt-header">', '\n<div class="rt-hero">')
STATS    = between('<div class="rt-stats">', '\n<div class="rt-cta-bar">')
GARMENT  = between('<div class="rt-wrap"><div class="rt-illust"><div class="rt-garment-row">', '\n<div class="rt-section">')
EMB      = aria_block('Embroidery machine stitching')
SIGNPOST = aria_block('retail signpost')
PREMISES = aria_block('serving independent retailers across')
ORDER    = aria_block('Order supermarket and retail workwear online')
CONTACT  = BASE[BASE.index('<div class="rt-contact-block">'):
                BASE.index('</div></div></div>', BASE.index('<div class="rt-contact-block">'))+len('</div></div></div>')]
FOOTER   = BASE[BASE.index('<footer class="rt-footer">'):BASE.index('</footer>')+len('</footer>')]

def signpost_town(town):
    n = len(town)
    size = 22 if n <= 8 else 19 if n <= 11 else 16 if n <= 15 else 13 if n <= 20 else 11
    tl = ' textLength="200" lengthAdjust="spacingAndGlyphs"' if n > 11 else ''
    return (f'<text x="230" y="62" text-anchor="middle" font-family="Arial,sans-serif" '
            f'font-weight="800" font-size="{size}" fill="#fff"{tl}>{town.upper()}</text>')

# === PRODUCTS ==============================================================
RT_PRODUCTS = ["Embroidered Polo Shirts","Tabards and Aprons","Fleeces and Sweatshirts",
 "Safety Shoes and Footwear","Hi-Vis for Warehouse and Yard","Cargo and Stockroom Trousers",
 "Caps, Beanies and Accessories","Embroidery, Names and ID Branding"]

def _card(n,d): return f'<div class="rt-product-card"><div class="rt-product-name">{n}</div><div class="rt-product-detail">{d}</div></div>'
_GA=_card("Embroidered Polo Shirts","Embroidered polos in breathable, hard-wearing fabrics, the everyday branded layer for shop-floor and counter staff, finished with the shop name and logo.")
_GB=_card("Tabards and Aprons","Branded tabards and aprons for tills, counters, delis and the shop floor, easy to wear over staff clothing and the classic, recognisable retail layer.")
_GC=_card("Fleeces and Sweatshirts","Warm, branded fleeces and sweatshirts for colder days, chillers and forecourts, worn over the polo to keep staff comfortable and on-brand year-round.")
_GD=_card("Safety Shoes and Footwear","Comfortable, supportive safety shoes and footwear for staff on their feet all day and handling stock, with grip and protection for the shop floor and stockroom.")
_GE=_card("Hi-Vis for Warehouse and Yard","Hi-vis vests and tops for warehouse, stockroom, delivery and garden-centre yard work, keeping staff seen during deliveries and out in the open.")
_GF=_card("Cargo and Stockroom Trousers","Hard-wearing cargo and work trousers for stockroom, warehouse and garden-centre staff, pocketed and durable for handling and replenishing stock.")
_GG=_card("Caps, Beanies and Accessories","Branded caps, beanies and accessories for forecourt, yard and outdoor staff, embroidered to match the rest of the uniform across the team.")
_GH=_card("Embroidery, Names and ID Branding","In-house embroidery of your shop name, logo and staff names onto every layer, so the whole team looks consistent across the shop floor, tills and stockroom.")
GRID_POOL=[
 '<div class="rt-product-grid">'+_GA+_GB+_GC+_GD+_GE+_GF+_GG+_GH+'</div>',
 '<div class="rt-product-grid">'+_GB+_GA+_GC+_GD+_GE+_GF+_GG+_GH+'</div>',
 '<div class="rt-product-grid">'+_GA+_GB+_GC+_GE+_GD+_GF+_GG+_GH+'</div>',
]

# === PROSE POOLS ===========================================================
TRUST_POOL=[
 "Embroidered polos, tabards, fleeces and safety shoes for independent shops, convenience stores and garden centres across the UK",
 "Branded polos, tabards, fleeces and safety shoes for independent retailers, convenience stores and garden centres - UK-wide, on account or direct",
 "Trusted by independent retailers, convenience stores and garden centres across the UK for branded staff uniforms and in-house embroidery",
 "Branded retail uniforms - polos, tabards, fleeces and safety shoes - for independent shops and stores across the UK, managed on one account",
]
S2INTRO_POOL=[
 "Whether you run a single convenience store, a high-street shop, a garden centre or a small group of sites across {t}, the range is built to kit the whole team from one place: branded polos, tabards and fleeces for the shop floor, then safety shoes, hi-vis and stockroom trousers for the back of house.",
 "Single convenience store, high-street shop, garden centre or a small {t} group, the range kits the whole team from one place: branded polos, tabards and fleeces for the shop floor, then safety shoes, hi-vis and stockroom trousers for the back of house.",
 "For a {t} shop, convenience store or garden centre, the range covers the whole team from one place: branded polos, tabards and fleeces for the front, safety shoes, hi-vis and stockroom trousers for the back, in the sizes you need.",
 "A {t} convenience store, high-street shop or garden centre gets the whole team kitted from one place: branded polos, tabards and fleeces up front, with safety shoes, hi-vis and stockroom trousers behind.",
]
EMB_P1_POOL=[
 "In retail, the staff are the brand. A customer judges a {t} shop in seconds, and a team in clean, matching, branded uniform signals that the place is well run and worth trusting, long before anyone says a word. A branded polo or tabard turns staff into a recognisable team rather than a group of individuals, and makes a small independent look as organised and professional as any chain.",
 "In retail the staff are the brand. A customer judges a {t} shop in seconds, and a team in clean, matching, branded uniform signals a well-run, trustworthy place before a word is said. A branded polo or tabard makes staff a recognisable team rather than individuals, and a small independent look as professional as any chain.",
 "The staff are the brand in retail. A {t} customer forms a view of a shop in seconds, and a team in clean, branded uniform reads as well run and trustworthy from the door. A branded polo or tabard turns staff into a recognisable team and makes an independent look as organised as any chain.",
 "In a shop, the staff are the brand. A customer sizes up a {t} store in seconds, and a team in matching, branded uniform signals it is well run and worth trusting before anyone speaks. A branded polo or tabard makes the team recognisable and an independent look as professional as a chain.",
]
EMB_P2_POOL=[
 "We brand in-house, which means your shop name and logo are embroidered onto polos, tabards, fleeces and hi-vis, finished to survive daily wear and frequent washing. Send your artwork once, we hold it on file, and every reorder, new starter and seasonal hire matches the last, so the {t} team looks consistent through every shift and across the shop floor, the tills and the stockroom.",
 "Branding is applied in-house onto polos, tabards, fleeces and hi-vis - your shop name and logo embroidered and finished to survive daily wear and washing. We hold your artwork on file, so every reorder, new starter and seasonal hire matches, and the {t} team looks consistent through every shift and across the shop floor, tills and stockroom.",
 "Your shop name and logo are embroidered in-house onto polos, tabards, fleeces and hi-vis, finished for daily wear and frequent washing. Held on file, your artwork reproduces on every reorder, new starter and seasonal hire, so a {t} team stays consistent across shifts, the shop floor, the tills and the stockroom.",
 "We badge in-house, embroidering your shop name and logo onto polos, tabards, fleeces and hi-vis and finishing them for daily wear and washing. Held on file, your branding matches on every reorder and new starter, so the {t} team looks consistent through every shift and across the shop floor, tills and stockroom.",
]
EMB_P3_POOL=[
 "For an operator running more than one site, that consistency is the whole point. We manage your branding and sizes across every store, so kitting a new starter, opening a second shop or replacing worn kit reproduces exactly the same branded uniform every time, and every site looks like the same business without anyone having to re-supply artwork or chase a match.",
 "For a multi-site operator, that consistency is the point. We manage your branding and sizes across every store, so a new starter, a second shop or a replacement for worn kit comes back exactly the same branded uniform, and every site looks like one business with no artwork to re-supply.",
 "Where an operator runs more than one site, consistency is everything. We run your branding and sizes across every store, so kitting a new starter, opening a second shop or replacing worn kit reproduces the same branded uniform each time, and every site looks like the same business.",
 "For an operator with several sites, that consistency is the whole value. We manage branding and sizes across every store, so a new starter, a second shop or a replacement for worn kit reproduces exactly the same branded uniform every time, and every site looks like one business.",
]
# === IDENTITY / SHOPFRONT BLOCK ============================================
CON_HEAD="Your Staff Are Your Shopfront: A Consistent Retail Uniform"
CON_P1_POOL=[
 "A retail uniform has two jobs, front of house and back of house, and a good supplier covers both from one place. Front of house, the uniform is about brand and trust: embroidered polos, tabards and fleeces that carry the {t} shop name, present the team as organised and professional, and stay smart through long shifts on the shop floor and behind the till. It is the single biggest impression a customer takes from the staff.",
 "A retail uniform does two jobs, front of house and back of house, and a good supplier handles both. Front of house it is about brand and trust: embroidered polos, tabards and fleeces carrying the {t} shop name, presenting the team as organised and professional and staying smart through long shifts on the floor and behind the till, the biggest impression a customer takes from the staff.",
 "A retail uniform works front of house and back of house, and the right supplier covers both. Front of house, it is brand and trust: embroidered polos, tabards and fleeces with the {t} shop name, presenting the team as organised and professional and staying smart through long shifts on the shop floor and the till, the single biggest impression customers take.",
 "A retail uniform has a front-of-house and a back-of-house job, and a good supplier does both from one place. Front of house, it is about brand and trust: embroidered polos, tabards and fleeces carrying the {t} shop name, keeping the team looking organised and professional through long shifts on the floor and behind the till.",
]
CON_P2_POOL=[
 "Back of house, the same staff are stacking shelves, taking deliveries, working the chiller, the stockroom and, in a garden centre or forecourt, the yard outdoors. That calls for the practical layer: safety shoes for people on their feet all day, hi-vis for warehouse, delivery and yard work, and hard-wearing cargo or stockroom trousers for handling and replenishing stock. The best uniform moves a staff member from till to stockroom without a change of supplier or a clash of kit.",
 "Back of house, those same staff stack shelves, take deliveries and work the chiller, the stockroom and, in a garden centre or forecourt, the yard. That needs the practical layer: safety shoes for staff on their feet all day, hi-vis for warehouse, delivery and yard work, and hard-wearing cargo or stockroom trousers, so a uniform moves from till to stockroom without a change of supplier or a clash of kit.",
 "Behind the scenes, the same staff are stacking shelves, taking deliveries and working the chiller, stockroom and, in a garden centre or forecourt, the yard. That calls for safety shoes for people on their feet all day, hi-vis for warehouse, delivery and yard work, and durable cargo or stockroom trousers, so the uniform carries a staff member from till to stockroom from one supplier.",
 "Back of house, those staff stack shelves, take deliveries and work the chiller, the stockroom and the garden-centre or forecourt yard. That needs the practical layer: safety shoes for long days on their feet, hi-vis for warehouse, delivery and yard work, and hard-wearing cargo or stockroom trousers, so a uniform moves from till to stockroom without a clash of kit.",
]
CON_P3_POOL=[  # 1 .com link each
 'For an independent retailer in {t}, the value is having one supplier kit the whole team and keep it consistent as staff come and go. We hold your shop name, logo and sizes on file and supply the front and back of house from a single managed account, so kitting a new starter, opening a second store or replacing worn kit reproduces the same uniform every time. Browse the retail range at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
 'For a {t} independent retailer, the value is one supplier kitting the whole team and keeping it consistent as staff come and go. With your shop name, logo and sizes on file, we supply front and back of house from a single managed account, so kitting a new starter, opening a second store or replacing worn kit reproduces the same uniform every time. Browse the retail range at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
 'The value for a {t} independent retailer is having one supplier kit the whole team and keep it consistent through staff turnover. We hold your shop name, logo and sizes on file and supply front and back of house from one managed account, so a new starter, a second store or a replacement for worn kit comes back the same uniform every time. Browse the retail range at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
 'For an independent retailer in {t}, the point is one supplier kitting the whole team and holding it consistent as staff come and go. Your shop name, logo and sizes stay on file and we supply front and back of house from a single managed account, so kitting a new starter, opening a second store or replacing worn kit reproduces the same uniform every time. Browse the retail range at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
]
ACC_HEAD="Trade Accounts, Multi-Store Supply and Reordering"
ACC_P1_POOL=[
 "For most independent retailers in {t} the right route is a managed trade account. It gives the shop owner or area manager one point of contact, agreed pricing and a uniform list held on file, so kitting the team, reordering for new starters and seasonal staff, and keeping every shift and every store consistent all run from one place. Tell us your headcount, your shop name and logo and your sizes, and we will build a branded uniform list and pricing for the whole operation.",
 "Most {t} independent retailers use a managed trade account: the shop owner or area manager gets one point of contact, agreed pricing and a uniform list on file, so kitting the team, reordering for new starters and seasonal staff and keeping every shift and store consistent all run from one place. Send your headcount, shop name and logo and your sizes and we will build a branded uniform list and pricing.",
 "A managed trade account is the natural route for most {t} independents. The shop owner or area manager gets one contact, agreed pricing and a uniform list held on file, so kitting the team, reordering for new starters and keeping every store consistent stay simple. Give us your headcount, shop name and logo and your sizes and we will build a branded uniform list and pricing.",
 "For the typical {t} independent retailer, a managed trade account is the way to buy: one point of contact, agreed pricing and a uniform list on file, so kitting the team, reordering for new and seasonal staff and keeping every shift and store consistent all run from one place. Tell us your headcount, shop name and logo and your sizes and we will build the branded uniform list and pricing.",
]
ACC_P2_POOL=[
 "Multi-store and small-group operators get the most from it. With your branding and sizes held across the account, opening a second or third store, replacing worn kit or onboarding a new manager all reproduce the same uniform, so every site looks like one business and nobody is chasing artwork or guessing sizes between shops.",
 "Multi-store and small-group operators gain the most. With branding and sizes held across the account, opening a second or third store, replacing worn kit or onboarding a manager all reproduce the same uniform, so every site looks like one business with no chasing artwork or guessing sizes.",
 "Small-group and multi-store operators benefit most. With your branding and sizes held on the account, a second or third store, a kit replacement or a new manager all reproduce the same uniform, so every site looks like one business and nobody hunts for artwork or sizes between shops.",
 "Multi-store operators get the most value. With branding and sizes held across the account, opening another store, replacing worn kit or onboarding a new manager all reproduce the same uniform, so every site looks like one business without anyone chasing artwork or sizes.",
]
ACC_P3_POOL=[
 "A single small shop is covered too. If you just need to kit a handful of staff, you can order direct online without setting up an account: browse the range, pick your polos, tabards, fleeces and safety shoes, add sizes, send your logo once and check out. It is the quickest way to get one store smartly branded, and delivery reaches {t} and the surrounding area on standard lead times.",
 "A single small shop is covered as well. To kit a handful of staff you can order direct online with no account: browse, pick your polos, tabards, fleeces and safety shoes, add sizes, send your logo once and check out, the quickest way to get one {t} store smartly branded, with delivery on standard lead times.",
 "There is a route for a single small shop too. If you only need a handful of staff kitted, order direct online without an account: pick your polos, tabards, fleeces and safety shoes, add sizes, send the logo once and check out, the fastest way to brand one store, with delivery to {t} and the area on standard lead times.",
 "A single small shop is catered for as well. To kit just a few staff you can order direct online with no account: browse, choose your polos, tabards, fleeces and safety shoes, add sizes and send your logo once, the quickest way to get one {t} store smartly branded, on standard lead times.",
]
ACC_P4_POOL=[  # 2 .com links each
 'Set up a managed trade account for multi-store pricing and reordering at <a href="https://www.ineedworkwear.com">iNeedWorkwear</a>, or for a single shop browse and order direct at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
 'Open a managed trade account for multi-store pricing and reordering at <a href="https://www.ineedworkwear.com">iNeedWorkwear</a>. For a single shop, browse and order direct at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
 'Run a group through a managed trade account for multi-store pricing and reordering at <a href="https://www.ineedworkwear.com">iNeedWorkwear</a>, or order direct for a single shop at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
 'Set up multi-store pricing and reordering on a managed trade account at <a href="https://www.ineedworkwear.com">iNeedWorkwear</a>. A single shop can browse and order direct at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
]
WHY_P1_POOL=[
 "An independent shop, convenience store or garden centre in {t} whose staff turn out in clean, branded polos, tabards and fleeces looks organised and professional to every customer who walks in, and iNeedWorkwear supplies that whole uniform from a single place, branded in-house and managed on one account so a small retailer gets chain-quality consistency without a corporate buying team.",
 "A {t} independent shop, convenience store or garden centre whose staff wear clean, branded polos, tabards and fleeces looks organised and professional to every customer, and iNeedWorkwear supplies that whole uniform from one place, branded in-house and managed on one account, giving a small retailer chain-quality consistency without a corporate buying team.",
 "When a {t} independent shop, convenience store or garden centre turns its staff out in clean, branded polos, tabards and fleeces, it looks organised and professional to every customer who walks in, and we supply that whole uniform from a single place, branded in-house and managed on one account, so a small retailer gets chain-quality consistency without a buying team.",
 "An independent shop, convenience store or garden centre in {t} whose team wears clean, branded polos, tabards and fleeces reads as organised and professional to every customer, and we supply that complete uniform from one place, branded in-house and managed on one account, giving a small retailer chain-quality consistency without a corporate buying department.",
]
WHY_P2_POOL=[
 "Everything comes from the same place. The supplier that embroiders your polos and tabards also supplies your fleeces, safety shoes, hi-vis and stockroom trousers, so the shop floor and the back of house are kitted from one account and the whole team matches, with nothing falling through the gap between front-of-house uniform and back-of-house workwear.",
 "Kit comes from one account. The supplier embroidering your polos and tabards also supplies fleeces, safety shoes, hi-vis and stockroom trousers, so shop floor and back of house are kitted together and the whole team matches, with nothing slipping between front-of-house uniform and back-of-house workwear.",
 "All from one supplier. The same company embroidering your polos and tabards provides your fleeces, safety shoes, hi-vis and stockroom trousers, so the shop floor and the back of house are kitted from one account and the whole team matches.",
 "Kit comes from one place. Alongside the embroidered polos and tabards sit fleeces, safety shoes, hi-vis and stockroom trousers, so shop floor and back of house are kitted together, the team matches, and nothing falls through the gap between uniform and workwear.",
]
WHY_P3_POOL=[
 "The range is built around what retail actually wears out and replaces: polos, tabards, fleeces and safety shoes, the everyday kit of the shop floor and the stockroom. That practical focus keeps pricing and reordering realistic whether you are kitting one store or a small group of sites.",
 "Everything in the range reflects what retail really gets through: polos, tabards, fleeces and safety shoes, the daily kit of the shop floor and stockroom, and that focus keeps pricing and reordering realistic whether you kit one store or a small group of sites.",
 "The range centres on what retail genuinely uses and replaces, polos, tabards, fleeces and safety shoes, and that practical focus keeps pricing and reordering sensible whether you are kitting a single store or a small group of sites.",
 "Everything is built around what a shop really gets through, polos, tabards, fleeces and safety shoes, so pricing and reordering stay realistic whether you kit one store or a small group of sites.",
]
WHY_P4_POOL=[
 "And the ordering suits how independents actually buy: a managed account with held artwork and sizes for the multi-store operator, and a quick direct route for the single shop, so every reorder, new starter and seasonal hire matches and looks professional from their first shift.",
 "And the ordering fits how independents really buy: a managed account with held artwork and sizes for the multi-store operator, and a fast direct route for the single shop, so every reorder, new starter and seasonal hire matches and looks professional from the first shift.",
 "And how you order suits independents: a managed account with artwork and sizes on file for the multi-store operator, and a quick direct route for the single shop, so every reorder, new starter and seasonal hire is the same and looks professional from day one.",
 "And the ordering suits how independents buy: a managed account with held artwork and sizes for the multi-store operator and a fast direct route for the single shop, so every reorder, new starter and seasonal hire matches and looks professional from their first shift.",
]
ORD_P1_POOL=[
 "iNeedWorkwear supplies embroidered polos, tabards, fleeces, safety shoes, hi-vis and stockroom trousers to independent retailers, convenience stores, garden centres and farm shops across {region}, all branded in-house with the shop name and logo.",
 "We supply embroidered polos, tabards, fleeces, safety shoes, hi-vis and stockroom trousers to independent retailers, convenience stores, garden centres and farm shops across {region}, all branded in-house with the shop name and logo.",
 "Across {region}, iNeedWorkwear kits independent retailers, convenience stores, garden centres and farm shops in embroidered polos, tabards, fleeces, safety shoes, hi-vis and stockroom trousers, all branded in-house with the shop name and logo.",
 "From a single shop to a small group across {region}, iNeedWorkwear supplies embroidered polos, tabards, fleeces, safety shoes, hi-vis and stockroom trousers to independent retailers, convenience stores, garden centres and farm shops, all branded in-house.",
]
ORD_P2_POOL=[
 "For a shop or a small group, the route is a managed trade account: send your headcount, your shop name and logo and your sizes and we will build a branded uniform list with agreed pricing. We hold your artwork and sizes on file, so reordering is fast and every new starter, seasonal hire and second store is kitted, branded and consistent across the shop floor and stockroom.",
 "For a shop or small group, it is a managed trade account: send your headcount, shop name and logo and your sizes and we will build a branded uniform list with agreed pricing. With your artwork and sizes on file, reordering is quick and every new starter, seasonal hire and second store is branded and consistent across the shop floor and stockroom.",
 "Shops and small groups use a managed trade account: give us your headcount, shop name and logo and your sizes and we build a branded uniform list with agreed pricing. Your artwork and sizes stay on file, so reorders are fast and every new starter and second store matches across the shop floor and stockroom.",
 "For a shop or a small group the route is a managed trade account: send your headcount, shop name and logo and your sizes and we will build a branded uniform list with agreed pricing, holding your artwork and sizes on file so reorders are fast and every new starter, seasonal hire and second store stays consistent.",
]
ORD_P3_POOL=[
 "For a single small shop, ordering direct online is quickest: browse the range, add your sizes, send your logo once and check out, with no account to set up.",
 "For a single small shop, the quickest route is direct online: browse the range, add sizes, send the logo once and check out, with no account needed.",
 "A single small shop can order direct online fastest: pick the range, add sizes, send the logo once and check out, no account required.",
 "A single small shop orders quickest direct online: browse, add sizes, send the logo a single time and check out, with no account to set up.",
]
SELF_POOL=[  # 1 .com link each
 'Single shop and need a uniform sorted now? Browse the full range, add your sizes and order direct on self-service checkout at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
 'Just kitting one shop? Browse the range, add sizes and order direct on self-service checkout at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
 'Independent shop needing a branded uniform today? Browse the full range, add your sizes and order direct on self-service checkout at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
 'Need a staff uniform for one store now? Browse the range, add sizes and order direct on self-service checkout at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
]
SORTED_POOL=[  # 1 .com link each
 '<h3>Supermarket and Retail Workwear, Sorted</h3><p>From embroidered polos and tabards to fleeces, safety shoes, hi-vis and stockroom trousers, get branded uniforms built for independent retailers and stores at fair prices - branded in-house with your shop name, on a managed account or ordered direct online.</p><p><a href="https://www.ineedworkwear.com">Browse supermarket and retail workwear at iNeedWorkwear</a></p>',
 '<h3>Supermarket and Retail Workwear, Sorted</h3><p>Embroidered polos, tabards, fleeces, safety shoes, hi-vis and stockroom trousers - branded retail uniforms at fair prices, branded in-house with your shop name, on a managed account or ordered direct online.</p><p><a href="https://www.ineedworkwear.com">Browse supermarket and retail workwear at iNeedWorkwear</a></p>',
 '<h3>Supermarket and Retail Workwear, Sorted</h3><p>From embroidered polos and tabards to fleeces, safety shoes, hi-vis and stockroom trousers, kit one shop or a small group out at fair prices, branded in-house and ordered on a managed account or direct online.</p><p><a href="https://www.ineedworkwear.com">Browse supermarket and retail workwear at iNeedWorkwear</a></p>',
 '<h3>Supermarket and Retail Workwear, Sorted</h3><p>Embroidered polos, tabards, fleeces, safety shoes, hi-vis and stockroom trousers, the full branded retail uniform at fair prices, branded in-house and ready to order on a managed account or direct online.</p><p><a href="https://www.ineedworkwear.com">Browse supermarket and retail workwear at iNeedWorkwear</a></p>',
]
# === LOW-VARIATION SHARED PARAS (pooled, not in per-town s1loc) =============
SHOPFRONT_POOL=[  # "uniform is the shopfront" para, varied per town ({t})
 "For them the uniform is the shopfront. Staff are the most visible thing a customer meets in a {t} shop, and a clean, branded polo or tabard says organised, professional and trustworthy in a way plain clothes never can. Front of house it is polos, tabards and fleeces carrying the shop name; behind it, in the stockroom, the chiller and the yard, it is safety shoes, hi-vis and hard-wearing trousers for staff handling stock all day.",
 "The uniform is the shopfront here. Staff are the most visible thing a customer meets in a {t} shop, so a clean, branded polo or tabard says organised, professional and trustworthy where plain clothes cannot. Front of house it is polos, tabards and fleeces with the shop name; back of house, in the stockroom, chiller and yard, it is safety shoes, hi-vis and hard-wearing trousers for staff handling stock all day.",
 "To them, the uniform is the shopfront. In a {t} shop the staff are the most visible thing a customer meets, and a clean, branded polo or tabard reads as organised, professional and trustworthy in a way plain clothes never do. Up front it is polos, tabards and fleeces carrying the shop name; in the stockroom, chiller and yard it is safety shoes, hi-vis and durable trousers for handling stock.",
 "For these businesses the uniform is the shopfront. Staff are the most visible thing a {t} customer meets, so a clean, branded polo or tabard signals organised, professional and trustworthy where plain clothes never could. Front of house it is polos, tabards and fleeces with the shop name; behind it, safety shoes, hi-vis and hard-wearing trousers for the stockroom, chiller and yard.",
]
CONSIST_POOL=[  # "consistent as the team turns over / managed account" para, varied per town ({t})
 "And it has to stay consistent as the team turns over. Retail runs on shifts, seasonal staff and a steady churn of new starters, so the uniform has to reorder easily and match every time. iNeedWorkwear is built for exactly that: a managed account that holds your shop name, logo and sizes on file, branded in-house, so kitting a new starter or a second {t} store reproduces the same uniform without anyone having to start again.",
 "And it has to hold consistent as staff turn over. Retail runs on shifts, seasonal hires and a steady churn of new starters, so the uniform must reorder easily and match every time. iNeedWorkwear is built for that: a managed account holding your shop name, logo and sizes on file, branded in-house, so kitting a new starter or a second {t} store reproduces the same uniform without starting again.",
 "And the uniform has to stay consistent through staff turnover. Retail runs on shifts, seasonal staff and a constant flow of new starters, so it has to reorder easily and match each time. iNeedWorkwear is built for exactly that, a managed account that keeps your shop name, logo and sizes on file, branded in-house, so a new starter or a second {t} store comes back the same uniform without starting from scratch.",
 "And it must stay consistent as the team changes. Retail runs on shifts, seasonal hires and a steady churn of new starters, so the uniform has to reorder easily and match every time, which is exactly what iNeedWorkwear is built for: a managed account holding your shop name, logo and sizes on file, branded in-house, so kitting a new starter or a second {t} store reproduces the same uniform every time.",
]
OWNER_POOL=[  # carries the "independents not chains" targeting note
 "The big chains are not really the market here. The major supermarkets and retailers procure their uniforms centrally, through national tenders run by corporate buying teams, so the businesses that need a supplier are the independents: the shop owner, the convenience-store operator, the garden-centre manager or the area manager of a small group, who wants a smart, consistent, branded uniform without a procurement department to run it.",
 "The big chains are not the market here. Major supermarkets and retailers buy their uniforms centrally through national tenders run by corporate teams, so the businesses needing a supplier are the independents: the shop owner, the convenience-store operator, the garden-centre manager or the area manager of a small group, after a smart, consistent, branded uniform without a procurement department.",
 "The chains are not really the market. Major retailers procure uniforms centrally via national tenders run by corporate buyers, so the businesses that need a supplier are the independents, the shop owner, the convenience-store operator, the garden-centre manager or the area manager of a small group, who want a smart, consistent, branded uniform without a buying department to run it.",
 "The big chains are not the market for this. Major supermarkets and retailers tender their uniforms centrally through corporate buying teams, so it is the independents who need a supplier: the shop owner, the convenience-store operator, the garden-centre manager or the area manager of a small group, wanting a smart, consistent, branded uniform without a procurement department.",
 "The major chains are not the market here, since they procure uniforms centrally through national tenders run by corporate teams. The businesses that need a supplier are the independents: the shop owner, the convenience-store operator, the garden-centre manager or the area manager of a small group, who wants a smart, consistent, branded uniform without a procurement department to run it.",
 "Big chains are not really the market, procuring their uniforms centrally via national tenders through corporate buying teams. The businesses that need a supplier are the independents, the shop owner, the convenience-store operator, the garden-centre manager or the area manager of a small group, after a smart, consistent, branded uniform without a procurement department.",
]
KIT_POOL=[
 "Front of house it is polos, tabards and fleeces; back of house, safety shoes, hi-vis and stockroom trousers {loc}.",
 "Up front it is polos, tabards and fleeces, and behind it safety shoes, hi-vis and stockroom trousers {loc}.",
 "The front-of-house layer is polos, tabards and fleeces, the back-of-house layer safety shoes, hi-vis and stockroom trousers {loc}.",
 "Polos, tabards and fleeces carry the front of house, with safety shoes, hi-vis and stockroom trousers behind {loc}.",
 "Front of house runs on polos, tabards and fleeces, back of house on safety shoes, hi-vis and stockroom trousers {loc}.",
 "It is polos, tabards and fleeces up front and safety shoes, hi-vis and stockroom trousers in the back {loc}.",
]
S2TAIL_POOL=[
 ", polos, tabards and fleeces lead the shop floor, with safety shoes, hi-vis and stockroom trousers behind.",
 ", the front-of-house staples are polos, tabards and fleeces, backed by safety shoes, hi-vis and stockroom trousers.",
 ", polos, tabards and fleeces are the shop-floor core, with safety shoes, hi-vis and stockroom trousers making up the rest.",
 ", polos, tabards and fleeces do the front of house, with safety shoes, hi-vis and stockroom trousers behind.",
 ", expect polos, tabards and fleeces up front, then safety shoes, hi-vis and stockroom trousers.",
 ", polos, tabards and fleeces anchor the shop floor, with safety shoes, hi-vis and stockroom trousers completing it.",
]

def s1_paras(town, T):
    if 's1loc' in T:
        shopfront = SHOPFRONT_POOL[pick(town,'shp',len(SHOPFRONT_POOL))].format(t=town)
        consist = CONSIST_POOL[pick(town,'con',len(CONSIST_POOL))].format(t=town)
        own = OWNER_POOL[pick(town,'own',len(OWNER_POOL))]
        kit = KIT_POOL[pick(town,'kit',len(KIT_POOL))].format(loc=T['kit_loc'])
        p = list(T['s1loc']) + [own, shopfront, consist.rstrip()+' '+kit]
        return p
    return T['s1']

def s2_local_text(town, T):
    if 's2_intro' in T:
        return T['s2_intro'].rstrip() + S2TAIL_POOL[pick(town,'s2t',len(S2TAIL_POOL))]
    return T['s2_local']

def faq_for(t, region):
    P = lambda salt, opts: opts[pick(t, salt, len(opts))]
    return [
     (f"Do you supply branded uniforms to independent retailers in {t}?", P('fq1',[
      f"Yes. Independent retailers, convenience stores, forecourts, garden centres and farm shops across {region} get embroidered polos, tabards, fleeces, safety shoes, warehouse hi-vis and stockroom trousers from us, branded in-house with the shop name, on a managed trade account with artwork and sizes held on file for reorders and new starters.",
      f"Yes. Embroidered polos, tabards, fleeces, safety shoes, hi-vis and stockroom trousers go to independent retailers, convenience stores, garden centres and farm shops across {region}, branded in-house with the shop name, on a managed trade account or ordered direct online.",
      f"Yes. From a single shop to a small group across {region}, we supply embroidered polos, tabards, fleeces, safety shoes, hi-vis and stockroom trousers to independent retailers, convenience stores and garden centres, branded in-house, on account or direct.",
      f"Yes. Independent retailers, convenience stores, garden centres and farm shops across {region} get embroidered polos, tabards, fleeces, safety shoes, hi-vis and stockroom trousers from us, branded in-house with the shop name, on a managed account with artwork and sizes held on file."])),
     ("Can you kit a whole shop team and keep it consistent?", P('fq2',[
      "Yes. A trade account lets you kit the whole team in the same branded polos, tabards and fleeces, with safety shoes, hi-vis and cargo trousers for the stockroom and yard. We hold your logo and sizes on file, so a new starter or a second store is kitted in exactly the same uniform, and reorders match every time across shifts and sites.",
      "Yes. A trade account kits the whole team in the same branded polos, tabards and fleeces, plus safety shoes, hi-vis and cargo trousers for the stockroom and yard, with logo and sizes on file so a new starter or second store matches exactly and reorders are consistent across shifts and sites.",
      "Yes, that is the point of a managed account. Kit the whole team in the same branded polos, tabards and fleeces, with safety shoes, hi-vis and cargo trousers behind, and we hold your logo and sizes on file so new starters and second stores match every time.",
      "Yes. With a trade account the whole team wears the same branded polos, tabards and fleeces, with safety shoes, hi-vis and cargo trousers for the stockroom and yard, and your logo and sizes stay on file so a new starter or a second store is kitted identically every time."])),
     ("What uniform does a shop or convenience store need?", P('fq3',[
      "The core uniform is embroidered polos and tabards for the shop floor and tills, fleeces and sweatshirts for colder days and chillers, safety shoes for staff on their feet all day, hi-vis for warehouse, yard and delivery work, and cargo or stockroom trousers, all branded with the shop name and logo.",
      "Most shops need embroidered polos and tabards for the floor and tills, fleeces and sweatshirts for colder days and chillers, safety shoes for staff on their feet all day, hi-vis for warehouse and yard work, and cargo or stockroom trousers, all branded with the shop name.",
      "At minimum, embroidered polos and tabards for the shop floor and tills, fleeces and sweatshirts for colder days and chillers, safety shoes, hi-vis for warehouse, yard and delivery work, and cargo or stockroom trousers, all branded with the shop name and logo.",
      "The core uniform is embroidered polos and tabards for the shop floor and tills, fleeces and sweatshirts for the cold and chillers, safety shoes for long days on their feet, hi-vis for warehouse and yard, and cargo or stockroom trousers, all branded with the shop name."])),
     ("Do you only supply the big supermarket chains?", P('fq4',[
      "No, the opposite. Major chains procure their uniforms centrally through national tenders, so we focus on independent retailers, convenience stores, forecourts, garden centres, farm shops and small multi-store retail groups, the businesses that want a smart, branded uniform without a corporate procurement department to run it.",
      "No, the reverse. The big chains tender their uniforms centrally through corporate buyers, so we focus on independent retailers, convenience stores, forecourts, garden centres, farm shops and small multi-store groups that want a smart, branded uniform without a procurement department.",
      "No. The major chains procure centrally via national tender, so our focus is independent retailers, convenience stores, forecourts, garden centres, farm shops and small multi-store groups, the businesses that want a smart, branded uniform without a corporate buying team.",
      "No, quite the opposite. Big chains buy uniforms centrally through national tenders, so we serve independent retailers, convenience stores, forecourts, garden centres, farm shops and small multi-store groups wanting a smart, branded uniform without a procurement department."])),
     ("Can you brand uniforms with our shop name and logo?", P('fq5',[
      "Yes. We embroider your shop name and logo in-house onto polos, tabards, fleeces and hi-vis, finished to survive daily wear and frequent washing. Send your artwork once, we hold it on file, and every reorder and new starter matches, so your team looks consistent across the shop floor, the tills and the stockroom.",
      "Yes. Your shop name and logo are embroidered in-house onto polos, tabards, fleeces and hi-vis, finished for daily wear and washing. Send artwork once and we hold it on file, so every reorder and new starter matches across the shop floor, tills and stockroom.",
      "Yes, all branding is done in-house onto polos, tabards, fleeces and hi-vis, finished to survive daily wear and washing. We hold your artwork on file, so every reorder and new starter matches across the shop floor, tills and stockroom.",
      "Yes. Send your artwork once and we embroider your shop name and logo in-house onto polos, tabards, fleeces and hi-vis, holding it on file so every reorder and new starter matches across the shop floor, the tills and the stockroom."])),
     ("Do you supply hi-vis and footwear for the stockroom and yard?", P('fq6',[
      "Yes. Alongside the front-of-house polos, tabards and fleeces we supply safety shoes for staff on their feet all day, hi-vis for warehouse, yard, garden-centre and delivery work, and cargo or stockroom trousers, so the same supplier kits the shop floor and the back of house from one account.",
      "Yes. With the front-of-house polos, tabards and fleeces we supply safety shoes for long days on their feet, hi-vis for warehouse, yard and delivery work, and cargo or stockroom trousers, so one supplier kits the shop floor and the back of house from a single account.",
      "Yes, the back of house is covered too: safety shoes for staff on their feet all day, hi-vis for warehouse, yard, garden-centre and delivery work, and cargo or stockroom trousers, alongside the front-of-house polos, tabards and fleeces, all from one account.",
      "Yes. Beyond the front-of-house polos, tabards and fleeces we supply safety shoes, hi-vis for warehouse, yard and delivery work, and cargo or stockroom trousers, so the same supplier kits the shop floor and the back of house from one account."])),
     ("How quickly can you supply retail uniforms?", P('fq7',[
      "Order direct online and your kit is dispatched on standard lead times, with embroidery added in-house before it ships. For a managed account, send your headcount, your logo and your sizes and we will build a branded uniform list and quote, hold it on file and turn reorders and new-starter kit around on standard lead times.",
      "Order direct online and your kit ships on standard lead times, with embroidery added in-house first. For a managed account, send your headcount, logo and sizes and we will build a branded uniform list and quote, hold it on file and turn reorders and new-starter kit around on standard lead times.",
      "Order direct online and we dispatch on standard lead times, embroidery added in-house before shipping. For a managed account, send your headcount, logo and sizes and we will build a branded uniform list and quote and hold it on file, turning reorders around on standard lead times.",
      "Order direct online and your kit is dispatched on standard lead times with embroidery done in-house first. For a managed account, send your headcount, logo and sizes and we will build a branded uniform list and quote, hold it on file and turn reorders and new-starter kit around on standard lead times."])),
    ]

# === PER-TOWN AUTHORED DATA (web-researched; geographic nearby; 2 local paras) ==
TOWNS = {
 "birmingham": {
  "region":"Birmingham and the West Midlands",
  "nearby":["Solihull","West Bromwich","Walsall"],
  "snapshot":"iNeedWorkwear supplies embroidered polos, tabards, fleeces, safety shoes, hi-vis and stockroom trousers to independent retailers, convenience stores, garden centres and farm shops across Birmingham, from the suburban high streets to the city arcades, branded in-house with the shop name on a managed trade account, with artwork and sizes held on file so new starters and second stores are kitted in exactly the same uniform.",
  "s1_head":"Kitting the shops that line the West Midlands' high streets",
  "s1loc":[
   "Birmingham is built on retail, and beyond the big-name chains in the Bullring sits a vast independent scene. The city centre arcades, Great Western, the Piccadilly and Burlington arcades, hold independent boutiques and delis, while the suburbs carry the real density: thriving independent high streets in Kings Heath, Moseley, Stirchley, Harborne and Bournville, full of family-run shops, bottle shops, bakeries, refill grocers and lifestyle stores.",
   "Around them runs the everyday retail that never closes: convenience stores and independent supermarkets on every residential road from Aston to Kingstanding, forecourts, farmers' markets in Moseley and Kings Heath, the Bullring Rag Market and Digbeth's Redbrick Market, and garden centres on the city fringe. Almost every one of these puts staff in front of customers in something branded, and almost all of them are independents rather than chains.",
  ],
  "kit_loc":"across the city's high streets, convenience stores and garden centres",
  "s2_intro":"Whether you run a Kings Heath high-street shop, a convenience store, a garden centre or a small group of sites across Birmingham",
 },
 "leeds": {
  "region":"Leeds and West Yorkshire",
  "nearby":["Bradford","Pudsey","Dewsbury"],
  "snapshot":"iNeedWorkwear supplies embroidered polos, tabards, fleeces, safety shoes, hi-vis and stockroom trousers to independent retailers, convenience stores, garden centres and farm shops across Leeds, from the Victorian arcades and Kirkgate Market to the suburban high streets, branded in-house with the shop name on a managed trade account, with artwork and sizes held on file so new starters and second stores are kitted in exactly the same uniform.",
  "s1_head":"Kitting the shops that line Yorkshire's high streets",
  "s1loc":[
   "Leeds is one of the top retail cities in the UK, and beyond the chains in Trinity and Victoria Leeds sits a deep independent scene. The Victorian arcades, Grand, Queens, Thornton's and the County Arcade, and the Corn Exchange under its domed roof hold independent boutiques and homeware stores, while Kirkgate Market, one of the largest covered markets in Europe and the birthplace of M&S, runs on independent traders, grocers and delis spanning generations.",
   "Beyond the centre, the suburban high streets carry the everyday independents: Chapel Allerton, Headingley, Meanwood, Cross Gates and out to Farsley and Bramley, full of family-run shops, bookshops, plant and refill stores and convenience stores, with farmers' and makers' markets and garden centres across West Yorkshire. Almost every one of these puts staff in front of customers in something branded, and almost all of them are independents rather than chains.",
  ],
  "kit_loc":"across the city's high streets, convenience stores and garden centres",
  "s2_intro":"Whether you run a Chapel Allerton high-street shop, a convenience store, a garden centre or a small group of sites across Leeds",
 },
}

# === CSV / nearby ==========================================================
_CSV=None
def _load_csv():
    global _CSV
    if _CSV is not None: return _CSV
    here=os.path.dirname(os.path.abspath(__file__))
    for p in (os.path.join(here,'RT_towns.csv'),'RT_towns.csv','/mnt/user-data/outputs/RT_towns.csv'):
        if os.path.exists(p):
            rows=[]
            with open(p,newline='',encoding='utf-8-sig') as f:
                for r in csv.DictReader(f): rows.append((int(r["Rank"]), r["Town"].strip(), (r.get("Nation") or "").strip()))
            _CSV=rows; return _CSV
    _CSV=[]; return _CSV

def slugify(name):
    return re.sub(r'-+','-', re.sub(r"[^a-z0-9]+","-", name.lower().replace("&"," and "))).strip('-')

def require_nearby(town, T):
    nb = T.get("nearby")
    if not nb or len(nb) < 3:
        raise ValueError(f"{town}: 'nearby' must list 3 geographically-close towns "
                         f"(web-verified, all on RT_towns.csv). No rank/auto fallback.")
    bad = [n for n in nb if not any(r[1].lower()==n.lower() for r in _load_csv())]
    if bad:
        raise ValueError(f"{town}: nearby town(s) not on RT_towns.csv: {bad}")
    return nb[:3]

# === title / meta ==========================================================
def build_title(town):
    for t in (f"{town} Supermarket and Retail Workwear",
              f"{town} Retail and Shop Workwear", f"{town} Retail Workwear"):
        if len(t) <= 60: return t
    return f"{town} Retail Workwear"

def build_meta(town):
    for m in (f"Branded polos, tabards, fleeces and safety shoes for {town} shops, convenience stores and garden centres - retail uniforms with in-house embroidery.",
              f"Branded polos, tabards, fleeces and safety shoes for {town} shops and convenience stores - retail uniforms with in-house embroidery.",
              f"Branded polos, tabards and fleeces for {town} shops, convenience stores and garden centres - retail uniforms with in-house embroidery.",
              f"Branded retail uniforms for {town} shops and convenience stores - polos, tabards, fleeces, with in-house embroidery."):
        if len(m) <= 160: return m
    return f"Branded retail uniforms for {town} shops - polos, tabards, fleeces, in-house embroidery."

# === SCHEMA / HEAD =========================================================
def _extract_org():
    blocks = re.findall(r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>', BASE, re.S)
    for b in blocks:
        if '"Organization"' in b: return b.strip()
    raise RuntimeError("Organization block not found in base")
ORG_BLOCK = _extract_org()

def _ld(obj): return '<script type="application/ld+json">\n'+json.dumps(obj,ensure_ascii=False)+'</script>'

def build_head(town, slug, faqs, nearby):
    title = build_title(town); meta = build_meta(town)
    canon = f"{DOMAIN}/{slug}.html"
    faq = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
        {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]}
    svc = {"@context":"https://schema.org","@type":"Service",
        "name":f"Supermarket and Retail Workwear Supply and Embroidery in {town}",
        "serviceType":"Retail and supermarket workwear and uniform supply and embroidery",
        "provider":{"@id":"https://www.ineedworkwear.com/#organization"},
        "areaServed":[{"@type":"City","name":town}]+[{"@type":"City","name":n} for n in nearby],
        "audience":{"@type":"BusinessAudience","name":"Independent retailers, convenience stores and garden centres"},
        "description":f"Embroidered polos, tabards, fleeces, safety shoes, hi-vis and stockroom trousers supplied to independent retailers, convenience stores and garden centres in {town}, on managed trade accounts, with in-house embroidery.",
        "hasOfferCatalog":{"@type":"OfferCatalog","name":"Supermarket and Retail Workwear",
            "itemListElement":[{"@type":"Offer","itemOffered":{"@type":"Product","name":p}} for p in RT_PRODUCTS]}}
    crumb = {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Home","item":DOMAIN},
        {"@type":"ListItem","position":2,"name":"Supermarket and Retail Workwear","item":f"{DOMAIN}/supermarket-retail-workwear"},
        {"@type":"ListItem","position":3,"name":town,"item":canon}]}
    return ('<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        f'<link rel="canonical" href="{canon}">\n<title>{title}</title>\n'
        f'<meta name="description" content="{meta}">\n'
        f'<meta property="og:title" content="{title}">\n'
        f'<meta property="og:description" content="{meta}">\n'
        '<meta property="og:type" content="website">\n'
        f'<meta property="og:url" content="{canon}">\n'
        +_ld(faq)+'\n<script type="application/ld+json">\n'+ORG_BLOCK+'</script>\n'+_ld(svc)+'\n'+_ld(crumb)+'\n'+CSS+'</head><body id="top">\n')

# === ASSEMBLE ==============================================================
def assemble(slug, town):
    T = TOWNS[town.lower()]
    region = T.get("region", town)
    nearby = require_nearby(town, T)
    faqs = faq_for(town, region)
    P = lambda pool, salt: pool[pick(town, salt, len(pool))]

    trust   = T.get("trust", P(TRUST_POOL,'trust'))
    snap    = T["snapshot"]
    s1head  = T["s1_head"]
    s1ps    = s1_paras(town, T)
    s2intro = s2_local_text(town, T)
    grid    = P(GRID_POOL,'grid')
    emb     = [P(EMB_P1_POOL,'e1').format(t=town), P(EMB_P2_POOL,'e2').format(t=town), P(EMB_P3_POOL,'e3')]
    con     = [P(CON_P1_POOL,'c1').format(t=town), P(CON_P2_POOL,'c2'), P(CON_P3_POOL,'c3').format(t=town)]
    acc     = [P(ACC_P1_POOL,'a1').format(t=town), P(ACC_P2_POOL,'a2'),
               P(ACC_P3_POOL,'a3').format(t=town), P(ACC_P4_POOL,'a4')]
    why     = [P(WHY_P1_POOL,'w1').format(t=town), P(WHY_P2_POOL,'w2'), P(WHY_P3_POOL,'w3'), P(WHY_P4_POOL,'w4')]
    ordr    = [P(ORD_P1_POOL,'o1').format(region=region), P(ORD_P2_POOL,'o2'), P(ORD_P3_POOL,'o3')]
    selfp   = P(SELF_POOL,'self'); sorted_ = P(SORTED_POOL,'sorted')

    emb_svg   = EMB.replace('a London retail company logo', f'a {town} retail company logo')
    sign_svg  = SIGNPOST.replace('London supermarket and retail signpost', f'{town} supermarket and retail signpost')
    sign_svg  = re.sub(r'<text x="230" y="62".*?</text>', signpost_town(town), sign_svg, flags=re.S)
    sign_svg  = sign_svg.replace('every kind of London retail', f'every kind of {town} retail')
    prem_svg  = PREMISES.replace('serving independent retailers across London', f'serving independent retailers across {town}')

    H=[build_head(town, slug, faqs, nearby), HEADER]
    H.append(f'<div class="rt-hero"><div class="rt-wrap"><div class="rt-subtitle">Branded Uniforms for Independent Retailers and Stores</div><h1>{town} Supermarket and Retail Workwear</h1></div></div>')
    H.append('<div class="rt-pulse"></div>')
    H.append(f'<div class="rt-trust-strip"><p>{trust}</p></div>')
    H.append(f'<div class="rt-wrap"><div class="rt-snapshot"><div class="rt-snapshot-label">Supplier Snapshot</div><p>{snap}</p></div></div>')
    H.append(STATS)
    H.append('<div class="rt-cta-bar"><a href="https://www.ineedworkwear.com" class="rt-cta-btn">Browse Retail Uniforms and Workwear</a></div>')
    H.append('<div class="rt-jump-links"><a href="#range">Workwear Range</a><a href="#contract">Staff Uniform</a><a href="#accounts">Ordering and Accounts</a><a href="#order">How to Order</a></div>')
    H.append(GARMENT)
    H.append(f'<div class="rt-section"><div class="rt-wrap"><h2>{s1head}</h2>'+''.join(f'<p>{p}</p>' for p in s1ps)+'</div></div>')
    H.append(f'<div class="rt-section" id="range"><div class="rt-wrap"><h2>Supermarket and Retail Workwear Range</h2><p>{s2intro} <a href="https://www.ineedworkwear.com">Browse the full range at iNeedWorkwear.com</a>.</p><p class="rt-btn-center"><a href="https://www.ineedworkwear.com" class="rt-section-btn">Browse The Range</a></p>{grid}</div></div>')
    H.append(f'<div class="rt-section"><div class="rt-wrap"><h2>Branding That Builds Trust on the Shop Floor</h2>'+''.join(f'<p>{p}</p>' for p in emb)+'</div></div>')
    H.append(emb_svg)
    H.append(f'<div class="rt-wrap"><div class="rt-contract" id="contract"><h3>{CON_HEAD}</h3>'+''.join(f'<p>{p}</p>' for p in con)+'</div></div>')
    H.append(sign_svg)
    H.append(f'<div class="rt-section" id="accounts"><div class="rt-wrap"><h2>{ACC_HEAD}</h2>'+''.join(f'<p>{p}</p>' for p in acc)+'</div></div>')
    H.append(prem_svg)
    H.append(f'<div class="rt-section"><div class="rt-wrap"><h2>Why Independent Retailers Choose iNeedWorkwear</h2>'+''.join(f'<p>{p}</p>' for p in why)+'</div></div>')
    H.append(ORDER)
    H.append(f'<div class="rt-section" id="order"><div class="rt-wrap"><h2>How to Order Retail and Supermarket Workwear</h2><p>{ordr[0]}</p><p>{ordr[1]}</p><p>{ordr[2]}</p><p class="rt-btn-center"><a href="https://www.ineedworkwear.com" class="rt-section-btn">Request A Quote</a></p><p>{selfp}</p>'+CONTACT+'</div></div>')
    faq_html=''.join(f'<div class="rt-faq-item"><div class="rt-faq-q">{q}</div><div class="rt-faq-a">{a}</div></div>' for q,a in faqs)
    H.append(f'<div class="rt-faq"><div class="rt-wrap"><h2>Supermarket and Retail Workwear FAQ</h2>{faq_html}</div></div>')
    H.append(f'<div class="rt-wrap"><div class="rt-workwear">{sorted_}</div></div>')
    nb_links=''.join(f'<a href="rt-{slugify(n)}.html">Retail workwear in {n}</a>\n' for n in nearby)
    H.append(f'<div class="rt-nearby"><div class="rt-wrap"><h3>Supermarket and Retail Workwear in Nearby Towns</h3><div class="rt-nearby-links">{nb_links}</div></div></div>')
    H.append(FOOTER+'\n</body></html>')
    return '\n'.join(H)

def main():
    args=[a for a in sys.argv[1:]]
    outdir = os.environ.get('RT_OUTDIR') or ('/mnt/user-data/outputs'
             if os.path.isdir('/mnt/user-data/outputs') else 'outputs')
    os.makedirs(outdir, exist_ok=True)
    disp = {r[1].lower(): r[1] for r in _load_csv()}   # r[1] = Town column (exact CSV spelling)
    if not args:
        args=[t for t in TOWNS if t!='london']
    for town_key in args:
        tk=town_key.lower()
        if tk=='london': continue
        if tk not in TOWNS:
            print(f"SKIP {town_key}: not in TOWNS (must be web-researched first)"); continue
        town = disp.get(tk, ' '.join(w.capitalize() for w in tk.split()))
        slug=f"rt-{slugify(town)}"
        html=assemble(slug, town)
        path=os.path.join(outdir, f"{slug}.html")
        open(path,'w',encoding='utf-8').write(html)
        print(f"WROTE {path}  ({len(html.split())} words approx)")

if __name__=='__main__':
    main()
