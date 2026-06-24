#!/usr/bin/env python3
# DC (Delivery & Courier Services) series builder v1.0
# Read SPEC.md / CLAUDE.md first. HYBRID A/B: equal billing of the owner-driver /
# small courier firm ordering DIRECT ONLINE and the fleet/depot operator on a
# TRADE ACCOUNT. Branded-uniform led (the driver is the brand on the doorstep).
# Lead = POLO + HI-VIS + SOFTSHELL. Medium workwear depth. Exactly 14 .com + 1
# community link per page. No JS, no HTML entities, no delivery-timescale claims.
# Nearby MUST be geographically close, hand-authored, on DC_towns.csv (no rank
# fallback).
import re, os, json, hashlib, sys, csv

def pick(key, salt, n):
    # md5 digest gives well-distributed bits; crc32 % n leaks correlated low
    # bits (e.g. all 7-letter town names collided on the same pool variant).
    h = hashlib.md5((salt + '|' + str(key).lower()).encode()).digest()
    return int.from_bytes(h[:4], 'big') % n

def _find_base():
    here = os.path.dirname(os.path.abspath(__file__))
    for p in (os.path.join(here,'dc-london.html'),'dc-london.html',
              '/mnt/user-data/outputs/dc-london.html','/home/claude/dckit/dc-london.html'):
        if os.path.exists(p): return p
    sys.exit("ERROR: dc-london.html (base template) not found beside dc_build.py")

BASE = open(_find_base(), encoding='utf-8').read()
DOMAIN = 'https://www.ineedworkwear.uk'

def between(start, end, src=BASE):
    i = src.index(start); j = src.index(end, i+len(start)); return src[i:j]
def aria_block(aria):
    k = BASE.index(aria)
    i = BASE.rfind('<div class="dc-wrap"><div class="dc-illust">', 0, k)
    j = BASE.index('</div></div></div>', k) + len('</div></div></div>')
    return BASE[i:j]

CSS      = between('<style>', '</style>') + '</style>'
HEADER   = between('<div class="dc-header">', '\n<div class="dc-hero">')
STATS    = between('<div class="dc-stats">', '\n<div class="dc-cta-bar">')
GARMENT  = between('<div class="dc-wrap"><div class="dc-illust"><div class="dc-garment-row">', '\n<div class="dc-section">')
EMB      = aria_block('Embroidery machine stitching')
SIGNPOST = aria_block('courier signpost')
PREMISES = aria_block('serving couriers and delivery firms across')
ORDER    = aria_block('Order delivery and courier workwear online')
CONTACT  = BASE[BASE.index('<div class="dc-contact-block">'):
                BASE.index('</div></div></div>', BASE.index('<div class="dc-contact-block">'))+len('</div></div></div>')]
FOOTER   = BASE[BASE.index('<footer class="dc-footer">'):BASE.index('</footer>')+len('</footer>')]

def signpost_town(town):
    n = len(town)
    size = 22 if n <= 8 else 19 if n <= 11 else 16 if n <= 15 else 13 if n <= 20 else 11
    tl = ' textLength="200" lengthAdjust="spacingAndGlyphs"' if n > 11 else ''
    return (f'<text x="230" y="62" text-anchor="middle" font-family="Arial,sans-serif" '
            f'font-weight="800" font-size="{size}" fill="#fff"{tl}>{town.upper()}</text>')

# === PRODUCTS ==============================================================
DC_PRODUCTS = ["Embroidered Polo Shirts and T-Shirts","Softshell and Branded Jackets",
 "Fleeces and Mid-Layers","Waterproof Jackets and Coats","Hi-Vis Vests and Tops",
 "Safety Boots and Footwear","Caps, Beanies and Accessories","Embroidery, Names and ID Branding"]

def _card(n,d): return f'<div class="dc-product-card"><div class="dc-product-name">{n}</div><div class="dc-product-detail">{d}</div></div>'
_GA=_card("Embroidered Polo Shirts and T-Shirts","Embroidered polos and t-shirts in breathable, hard-wearing fabrics, the everyday branded layer for the warmer months and the foundation of the delivery uniform.")
_GB=_card("Softshell and Branded Jackets","Softshell and branded jackets, smart and weather-resistant, the layer most couriers live in through spring and autumn, embroidered with the company name and logo.")
_GC=_card("Fleeces and Mid-Layers","Warm, branded fleeces and mid-layers for cold mornings and depot work, worn alone or under a softshell or waterproof as the temperature drops.")
_GD=_card("Waterproof Jackets and Coats","Waterproof jackets and coats that keep a driver dry and presentable on the doorstep in all weather, sized to layer over a fleece or softshell through winter.")
_GE=_card("Hi-Vis Vests and Tops","Hi-vis vests and tops to EN ISO 20471 for roadside and kerbside multidrop work and for visibility in depots, yards and loading bays, branded with the company name.")
_GF=_card("Safety Boots and Footwear","Safety boots and comfortable, supportive footwear for loading, depot and yard work and long days in and out of a van, with grip and protection for heavy parcels.")
_GG=_card("Caps, Beanies and Accessories","Branded caps, beanies and accessories that finish the uniform and keep drivers comfortable in sun and cold, embroidered to match the rest of the kit.")
_GH=_card("Embroidery, Names and ID Branding","In-house embroidery of your company name, logo and driver names onto every layer, so a fleet or an owner-driver looks consistent and professional on every round.")
GRID_POOL=[
 '<div class="dc-product-grid">'+_GA+_GB+_GC+_GD+_GE+_GF+_GG+_GH+'</div>',
 '<div class="dc-product-grid">'+_GA+_GB+_GE+_GC+_GD+_GF+_GG+_GH+'</div>',
 '<div class="dc-product-grid">'+_GA+_GC+_GB+_GD+_GE+_GF+_GG+_GH+'</div>',
]

# === PROSE POOLS ===========================================================
TRUST_POOL=[
 "Embroidered polos, softshells, hi-vis and waterproofs for couriers and delivery drivers - trade accounts or order direct online across the UK",
 "Branded polos, softshells, fleeces and hi-vis for couriers and delivery firms - on a fleet trade account or ordered direct online, UK-wide",
 "Trusted by owner-drivers and delivery fleets across the UK for branded polos, softshells, hi-vis and the all-weather courier uniform",
 "Branded delivery uniforms - polos, softshells, fleeces, hi-vis and waterproofs - for couriers and fleets across the UK, on account or direct",
]
S2INTRO_POOL=[
 "Whether you are an owner-driver, a multidrop courier or a delivery fleet working {t}'s doorsteps and depots, the range is built to kit you from one place: branded polos, softshells and fleeces first, then waterproofs, hi-vis vests, safety boots and caps.",
 "Owner-driver, multidrop courier or delivery fleet, a {t} operation gets kitted from one place: branded polos, softshells and fleeces first, then waterproofs, hi-vis vests, safety boots and caps, on account or direct.",
 "For a {t} courier or delivery firm, the range covers the lot from one place: branded polos, softshells and fleeces, plus waterproofs, hi-vis vests, safety boots and caps, in the sizes and quantities you need.",
 "A {t} owner-driver, multidrop courier or delivery fleet is kitted from one place: branded polos, softshells and fleeces first, with waterproofs, hi-vis vests, safety boots and caps alongside.",
]
EMB_P1_POOL=[
 "For a delivery or courier business, the driver is the brand. They are the one person a customer in {t} actually sees, dozens of times a day, at the door, at the kerb and in the street, and what they are wearing is the single biggest impression the company makes. A clean, embroidered polo, softshell or fleece says professional, expected and trustworthy in a way an unmarked top never can.",
 "The driver is the brand for a {t} delivery or courier firm. They are the one person a customer sees, dozens of times a day, at the door and the kerb, so what they wear is the biggest impression the company makes, and a clean, embroidered polo, softshell or fleece reads as professional and trustworthy where an unmarked top never does.",
 "In delivery and courier work, the driver is the brand. For a {t} firm, the driver is the one person the customer meets, again and again, at the doorstep and kerbside, so a clean, embroidered polo, softshell or fleece is the biggest impression the company makes, and it says professional and expected in a way plain kit cannot.",
 "For a {t} courier or delivery business, the driver is the face of the brand, the one person a customer sees dozens of times a day at the door and the kerb. What they wear makes the biggest impression the firm leaves, and a clean, embroidered polo, softshell or fleece says professional and trustworthy where an unmarked top falls flat.",
]
EMB_P2_POOL=[
 "We brand in-house, which means your company name and logo are embroidered onto polos, softshells, fleeces and hi-vis, finished to survive daily wear and frequent washing. Send your artwork once, we hold it on file, and every reorder, new driver and subcontractor matches the last, so whether it is one van or a fleet, every driver on a {t} round looks like the same company.",
 "Branding is applied in-house onto polos, softshells, fleeces and hi-vis - your name and logo embroidered and finished to survive daily wear and frequent washing. We hold your artwork on file, so every reorder, new driver and subcontractor matches, and whether it is one van or a fleet, every driver on a {t} round looks like one company.",
 "Your name and logo are embroidered in-house onto polos, softshells, fleeces and hi-vis, finished to take daily wear and frequent washing. Held on file, your artwork reproduces on every reorder, new driver and subcontractor, so a {t} round looks like the same company whether it is one van or a fleet.",
 "We badge in-house, embroidering your name and logo onto polos, softshells, fleeces and hi-vis and finishing them to survive daily wear and washing. Held on file, your branding matches on every reorder and new driver, so every driver on a {t} round looks like one company, one van or a whole fleet.",
]
EMB_P3_POOL=[
 "For a fleet, that consistency is the whole point. We manage your branding and sizes across the operation, so kitting a new starter, equipping a subcontractor or replacing a worn softshell reproduces exactly the same branded uniform every time, across every depot and round, without anyone having to re-supply artwork or chase a match.",
 "For a fleet, consistency is the point. We manage your branding and sizes across the operation, so a new starter, a subcontractor or a replacement for a worn softshell comes back exactly the same branded uniform every time, across every depot and round, with no artwork to re-supply.",
 "Across a fleet, consistency is everything. We run your branding and sizes for the whole operation, so kitting a new starter, equipping a subcontractor or replacing a worn softshell reproduces the same branded uniform each time, across every depot and round.",
 "For a fleet operation, that consistency is the whole value. We manage branding and sizes across the operation, so a new starter, a subcontractor crew or a replacement for a worn softshell reproduces exactly the same branded uniform every time, across every depot and round.",
]
# === IDENTITY / UNIFORM BLOCK ==============================================
CON_HEAD="Branded, All-Weather and Road-Ready: The Delivery Driver's Uniform"
CON_P1_POOL=[
 "Delivery and courier kit does three jobs at once, and getting the balance right is what makes a uniform work for a {t} operation. First it carries the brand: the driver is the face of the company on the doorstep, so the polos, softshells and fleeces are embroidered and kept smart. Second it handles the weather: a round runs in all conditions, so waterproofs, fleeces and layers keep a driver dry, warm and presentable from a summer afternoon to a winter night.",
 "A {t} delivery uniform does three jobs at once, and balancing them is what makes it work. First it carries the brand: the driver is the face of the firm on the doorstep, so polos, softshells and fleeces are embroidered and kept smart. Second it handles the weather: a round runs in all conditions, so waterproofs, fleeces and layers keep a driver dry, warm and presentable from summer afternoon to winter night.",
 "Courier and delivery kit in {t} has to do three things at once. First it carries the brand, because the driver is the face of the company at the doorstep, so the polos, softshells and fleeces are embroidered and kept smart. Second it handles the weather, since a round runs in all conditions, so waterproofs, fleeces and layers keep a driver dry, warm and presentable through the year.",
 "For a {t} courier or delivery operation, the kit does three jobs at once. First it carries the brand: the driver is the face of the firm on the doorstep, so polos, softshells and fleeces are embroidered and kept smart. Second it handles the weather, because a round runs in all conditions, so waterproofs, fleeces and layers keep a driver dry, warm and presentable from summer to winter.",
]
CON_P2_POOL=[
 "Third, it keeps drivers safe and seen. Multidrop and parcel work means constant time at the roadside and kerbside and in depots, yards and loading bays, so hi-vis vests and tops to EN ISO 20471 are part of the kit, worn over the branded layer wherever visibility matters, and safety boots give the grip and protection that loading and long days in and out of a van demand. The result is a layering system that takes a driver through the whole year and the whole working day.",
 "Third, it keeps drivers safe and seen: multidrop work means constant time at the roadside and kerbside and in depots, yards and loading bays, so hi-vis vests and tops to EN ISO 20471 are part of the kit, worn over the branded layer where visibility matters, with safety boots for the grip and protection loading and long days in a van demand. The result is a layering system for the whole year and the whole day.",
 "Third, it keeps drivers safe and visible. Parcel and multidrop work means constant roadside and kerbside time and work in depots, yards and loading bays, so hi-vis vests and tops to EN ISO 20471 go over the branded layer wherever needed, and safety boots give the grip and protection loading and long days in and out of a van demand, completing a layering system for the whole working year.",
 "Third, it keeps a driver safe and seen. Multidrop and parcel rounds mean constant time at the roadside and kerbside and in yards and loading bays, so hi-vis vests and tops to EN ISO 20471 are part of the kit, worn over the branded layer where visibility matters, with safety boots for the grip and protection that loading and long van days demand, all building into a year-round layering system.",
]
CON_P3_POOL=[  # 1 .com link each
 'Whether you run a fleet or drive a single van in {t}, the aim is the same: a consistent, branded, all-weather uniform that makes every driver look professional and stay safe. We hold your identity, artwork and sizes on file and supply the whole kit from one place, so kitting a new driver or replacing a worn layer reproduces the same uniform every time. Browse the courier and delivery range at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
 'Whether you run a {t} fleet or drive a single van, the aim is the same: a consistent, branded, all-weather uniform that keeps every driver professional and safe. With your identity, artwork and sizes on file, we supply the whole kit from one place, so kitting a new driver or replacing a worn layer reproduces the same uniform every time. Browse the courier and delivery range at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
 'Fleet or single van, the aim for a {t} operation is the same: a consistent, branded, all-weather uniform that makes every driver look professional and stay safe. We keep your identity, artwork and sizes on file and supply the whole kit from one place, so a new driver or a replacement layer reproduces the same uniform each time. Browse the courier and delivery range at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
 'Whether it is a {t} fleet or a single van, the goal is one consistent, branded, all-weather uniform that keeps every driver professional and safe. We hold your identity, artwork and sizes on file and supply the whole kit from one place, so kitting a new driver or replacing a worn layer comes back the same uniform every time. Browse the courier and delivery range at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
]
ACC_HEAD="Ordering: Trade Accounts and Direct Online"
ACC_P1_POOL=[
 "Delivery and courier businesses buy in two different ways, and we are set up for both, equally. A fleet or depot operator in {t} usually wants a trade account: purchase-order ordering, volume pricing and a single point of contact, so every driver, new starter and subcontractor is kitted in the same branded polos, softshells, fleeces and hi-vis, and reorders against an agreed kit list are quick and consistent across depots. Tell us your headcount, your logo and your sizes and we will build a branded kit list and pricing for the whole operation.",
 "Courier and delivery firms buy two ways, and we are set up for both, equally. A {t} fleet or depot operator usually wants a trade account: purchase-order ordering, volume pricing and one point of contact, so every driver, new starter and subcontractor is kitted in the same branded polos, softshells, fleeces and hi-vis, with reorders against an agreed kit list quick and consistent across depots. Send your headcount, logo and sizes and we will build a branded kit list and pricing.",
 "There are two ways delivery businesses buy, and we handle both equally. A fleet or depot operator in {t} usually runs a trade account: PO ordering, volume pricing and a single contact, so every driver and new starter is kitted in the same branded polos, softshells, fleeces and hi-vis, and reorders stay quick and consistent across depots. Give us your headcount, logo and sizes and we will build a branded kit list and pricing for the operation.",
 "Delivery and courier firms buy in two ways and we are built for both, equally. A {t} fleet or depot operator usually wants a trade account, with purchase-order ordering, volume pricing and one point of contact, so every driver, new starter and subcontractor wears the same branded polos, softshells, fleeces and hi-vis, and reorders are quick and consistent across depots. Tell us your headcount, logo and sizes and we will build the kit list and pricing.",
]
ACC_P2_POOL=[
 "An owner-driver or a small courier firm wants the opposite: speed and simplicity, with no account to set up. You can order direct online, browse the range, pick a few branded polos, a softshell, a hi-vis vest and safety boots, add your sizes, send your logo once and check out. It is the fastest way to get a single driver or a two-or-three-van outfit looking professional and out on the road.",
 "An owner-driver or small courier firm wants the opposite, speed and simplicity with no account to set up: order direct online, browse the range, pick a few branded polos, a softshell, a hi-vis vest and safety boots, add sizes, send the logo once and check out, the fastest way to get a single driver or a small outfit looking professional and on the road.",
 "For an owner-driver or small courier firm it is the reverse, speed and simplicity with no account: order direct online, browse, choose a few branded polos, a softshell, a hi-vis vest and safety boots, add your sizes, send your logo once and check out, the quickest way to get one driver or a two-or-three-van outfit out and looking professional.",
 "An owner-driver or small courier firm wants speed and simplicity instead, with no account to set up: order direct online, browse the range, pick branded polos, a softshell, a hi-vis vest and safety boots, add sizes, send the logo once and check out, the fastest route to getting a single driver or a small outfit professional and on the road.",
]
ACC_P3_POOL=[
 "Either way, every order is branded in-house, so your name and logo are applied under our control rather than outsourced, keeping the quality and the placement consistent. Your artwork and sizes are held on file for reordering, new drivers and subcontractors, and delivery reaches {t} and the surrounding area on standard lead times.",
 "Whichever route you take, all branding is done in-house, so your name and logo are applied under our control rather than sent out, keeping quality and placement consistent. We hold your artwork and sizes on file for reorders, new drivers and subcontractors, and deliver to {t} and the wider area on standard lead times.",
 "Either way, branding is done in-house, so your name and logo are applied under our control rather than outsourced, keeping quality and placement right. Your artwork and sizes stay on file for reordering, new drivers and subcontractors, and orders reach {t} and the surrounding area on standard lead times.",
 "Both routes are branded in-house, so your name and logo are applied under our control rather than farmed out, with consistent quality and placement. We keep your artwork and sizes on file for reorders, new drivers and subcontractors, and delivery reaches {t} and the area around it on standard lead times.",
]
ACC_P4_POOL=[  # 2 .com links each
 'Set up a trade account for fleet pricing and purchase-order ordering at <a href="https://www.ineedworkwear.com">iNeedWorkwear</a>, or for a single van or a small courier firm browse and order direct at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
 'Open a trade account for fleet pricing and purchase-order ordering at <a href="https://www.ineedworkwear.com">iNeedWorkwear</a>. For a single van or small courier firm, browse and order direct at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
 'Run a fleet through a trade account for volume pricing and purchase-order ordering at <a href="https://www.ineedworkwear.com">iNeedWorkwear</a>, or order direct for a single van or small courier firm at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
 'Set up fleet pricing and purchase-order ordering on a trade account at <a href="https://www.ineedworkwear.com">iNeedWorkwear</a>. A single van or small courier firm can browse and order direct at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
]
WHY_P1_POOL=[
 "A {t} delivery or courier operation whose drivers turn out in clean, branded polos, softshells and hi-vis looks like a professional, established company to every customer who opens the door, and iNeedWorkwear supplies that whole uniform from a single place, branded in-house and sold both ways, on a fleet trade account or direct online for an owner-driver.",
 "Drivers turned out in clean, branded polos, softshells and hi-vis make a {t} delivery or courier firm look professional and established to every customer who opens the door, and iNeedWorkwear supplies that whole uniform from one place, branded in-house and sold both ways, on a fleet trade account or direct online for an owner-driver.",
 "A {t} courier or delivery firm whose drivers wear clean, branded polos, softshells and hi-vis reads as professional and established to every customer at the door, and we supply that complete uniform from a single place, branded in-house and sold both ways, on a fleet account or direct online for an owner-driver.",
 "When a {t} delivery or courier operation turns its drivers out in clean, branded polos, softshells and hi-vis, it looks professional and established to every customer who opens the door, and we supply that whole uniform from one place, branded in-house and sold both ways, fleet account or direct online.",
]
WHY_P2_POOL=[
 "Everything comes from the same place. The supplier that embroiders your polos also supplies your softshells, fleeces, waterproofs, hi-vis vests, safety boots and caps, so every driver is kitted head to toe from one order and the whole fleet matches, with nothing falling through the gap between the branded layer and the weather and safety kit.",
 "Kit comes in one order. The supplier embroidering your polos also supplies softshells, fleeces, waterproofs, hi-vis vests, safety boots and caps, so every driver is kitted head to toe and the whole fleet matches, with nothing slipping between the branded layer and the weather and safety kit.",
 "All from one supplier. The same company embroidering your polos also provides softshells, fleeces, waterproofs, hi-vis vests, safety boots and caps, so every driver is kitted head to toe from a single order and the whole fleet matches.",
 "Kit comes from one place. Alongside the embroidered polos sit softshells, fleeces, waterproofs, hi-vis vests, safety boots and caps, so every driver is kitted head to toe, the fleet matches, and nothing falls through the gap between branding and the weather and safety layers.",
]
WHY_P3_POOL=[
 "The range is built around what delivery work actually wears out and replaces: polos, softshells, fleeces, waterproofs and hi-vis, the everyday layers of a year-round, all-weather round. That practical focus keeps pricing, stock and reordering realistic whether you are buying for one van or for a fleet of hundreds.",
 "Everything in the range reflects what delivery work really gets through: polos, softshells, fleeces, waterproofs and hi-vis, the daily layers of a year-round, all-weather round, and that focus keeps pricing, stock and reordering realistic whether you buy for one van or a fleet of hundreds.",
 "The range centres on what delivery work genuinely uses and replaces, polos, softshells, fleeces, waterproofs and hi-vis, and that practical focus keeps pricing, stock and reordering sensible whether you are kitting one van or a fleet of hundreds.",
 "Everything is built around what a delivery round really gets through, polos, softshells, fleeces, waterproofs and hi-vis, so pricing, stock and reordering stay realistic whether you buy for a single van or a fleet of hundreds.",
]
WHY_P4_POOL=[
 "And the ordering suits how delivery firms actually buy: a trade account with volume pricing and purchase orders for the fleet, and a fast direct route for the owner-driver, with your logo and sizes held on file so every reorder, new driver and subcontractor matches and looks professional from day one.",
 "And the ordering fits how delivery firms really buy: a trade account with volume pricing and purchase orders for the fleet, and a quick direct route for the owner-driver, with logo and sizes on file so every reorder, new driver and subcontractor matches and looks professional from day one.",
 "And how you order suits the trade: a trade account with volume pricing and POs for the fleet, and a fast direct route for the owner-driver, with logo and sizes held so every reorder, new driver and subcontractor is the same and looks professional from the start.",
 "And the ordering suits how delivery firms buy: a fleet trade account with volume pricing and purchase orders, and a fast direct route for the owner-driver, with your logo and sizes on file so every reorder and new driver matches and looks professional from day one.",
]
ORD_P1_POOL=[
 "iNeedWorkwear supplies embroidered polos, softshells, fleeces, waterproofs, hi-vis vests, safety boots and caps to couriers and delivery firms across {region}, all branded in-house with the company name and logo.",
 "We supply embroidered polos, softshells, fleeces, waterproofs, hi-vis vests, safety boots and caps to couriers and delivery firms across {region}, all branded in-house with the company name and logo.",
 "Across {region}, iNeedWorkwear kits couriers and delivery firms in embroidered polos, softshells, fleeces, waterproofs, hi-vis vests, safety boots and caps, all branded in-house with the company name and logo.",
 "From a single van to a depot fleet across {region}, iNeedWorkwear supplies embroidered polos, softshells, fleeces, waterproofs, hi-vis vests, safety boots and caps to couriers and delivery firms, all branded in-house.",
]
ORD_P2_POOL=[
 "For a fleet or depot, the route is a trade account: send your headcount, your logo and your sizes and we will build a branded kit list with volume pricing and purchase-order ordering. We hold your artwork and sizes on file, so reordering is fast and every new driver, replacement and subcontractor is kitted, branded and consistent across every depot and round.",
 "For a fleet or depot, it is a trade account: send your headcount, logo and sizes and we will build a branded kit list with volume pricing and purchase-order ordering. With your artwork and sizes on file, reordering is quick and every new driver, replacement and subcontractor is branded and consistent across every depot and round.",
 "Fleets and depots use a trade account: give us your headcount, logo and sizes and we build a branded kit list with volume pricing and purchase-order ordering. Your artwork and sizes stay on file, so reorders are fast and every new driver and subcontractor matches and stays consistent across depots.",
 "For a fleet or depot the route is a trade account: send your headcount, logo and sizes and we will build a branded kit list with volume pricing and purchase-order ordering, holding your artwork and sizes on file so reorders are fast and every new driver and subcontractor is branded and consistent across every round.",
]
ORD_P3_POOL=[
 "For an owner-driver or a small courier firm, ordering direct online is quickest: browse the range, add your sizes, send your logo once and check out, with no account to set up.",
 "For an owner-driver or small courier firm, the quickest route is direct online: browse the range, add sizes, send the logo once and check out, with no account needed.",
 "An owner-driver or small courier firm can order direct online fastest: pick the range, add sizes, send the logo once and check out, no account required.",
 "An owner-driver or small courier firm orders quickest direct online: browse, add sizes, send the logo a single time and check out, with no account to set up.",
]
SELF_POOL=[  # 1 .com link each
 'Single van or small courier firm and need kit now? Browse the full range, add your sizes and order direct on self-service checkout at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
 'Just kitting one van or a small courier firm? Browse the range, add sizes and order direct on self-service checkout at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
 'Owner-driver needing branded kit today? Browse the full range, add your sizes and order direct on self-service checkout at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
 'Need a delivery uniform for one van now? Browse the range, add sizes and order direct on self-service checkout at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
]
SORTED_POOL=[  # 1 .com link each
 '<h3>Delivery and Courier Workwear, Sorted</h3><p>From embroidered polos and softshells to fleeces, waterproofs, hi-vis vests and safety boots, get branded kit built for couriers and delivery drivers at fair prices - branded in-house with your name, on a fleet trade account or ordered direct online.</p><p><a href="https://www.ineedworkwear.com">Browse delivery and courier workwear at iNeedWorkwear</a></p>',
 '<h3>Delivery and Courier Workwear, Sorted</h3><p>Embroidered polos, softshells, fleeces, waterproofs, hi-vis vests and safety boots - branded delivery kit at fair prices, branded in-house with your name, on a fleet trade account or ordered direct online.</p><p><a href="https://www.ineedworkwear.com">Browse delivery and courier workwear at iNeedWorkwear</a></p>',
 '<h3>Delivery and Courier Workwear, Sorted</h3><p>From embroidered polos and softshells to fleeces, waterproofs, hi-vis vests and boots, kit one van or a whole fleet out at fair prices, branded in-house and ordered on account or direct online.</p><p><a href="https://www.ineedworkwear.com">Browse delivery and courier workwear at iNeedWorkwear</a></p>',
 '<h3>Delivery and Courier Workwear, Sorted</h3><p>Embroidered polos, softshells, fleeces, waterproofs, hi-vis vests and safety boots, the full branded delivery uniform at fair prices, branded in-house and ready to order on account or direct online.</p><p><a href="https://www.ineedworkwear.com">Browse delivery and courier workwear at iNeedWorkwear</a></p>',
]
OWNER_POOL=[
 "And the buyers split two ways: a fleet or depot operator kitting dozens or hundreds of drivers wants a trade account, volume pricing and consistency across every depot and new starter, while an owner-driver or small courier firm wants to choose a few branded polos and a softshell and order them direct, online, today.",
 "And the buyers fall into two camps: a fleet or depot operator kitting dozens or hundreds wants a trade account, volume pricing and consistency across depots and new starters, while an owner-driver or small courier firm wants to pick a few branded polos and a softshell and order direct online today.",
 "And there are two kinds of buyer: a fleet or depot operator kitting dozens or hundreds of drivers, who wants a trade account and consistency across depots, and an owner-driver or small courier firm, who wants to choose a few branded items and order them direct online today.",
 "And the buying splits two ways: the fleet or depot operator kitting dozens or hundreds, after a trade account, volume pricing and consistency across depots, and the owner-driver or small courier firm, who just wants a few branded polos and a softshell ordered direct online today.",
 "And buyers come in two types: a fleet or depot operator kitting dozens or hundreds of drivers wants a trade account and consistency across every depot, while an owner-driver or small courier firm wants a few branded polos and a softshell ordered direct online today.",
 "And the buyers divide two ways: a fleet or depot operator kitting dozens or hundreds wants a trade account, volume pricing and consistency, and an owner-driver or small courier firm wants to pick a few branded items and order them direct, online, the same day.",
]
KIT_POOL=[
 "Branded polos, softshells and fleeces are the core of the kit, worn with waterproofs, hi-vis vests, safety boots and caps {loc}.",
 "The core kit is branded polos, softshells and fleeces, with waterproofs, hi-vis vests, safety boots and caps alongside {loc}.",
 "Branded polos, softshells and fleeces do the everyday work, backed by waterproofs, hi-vis vests, safety boots and caps {loc}.",
 "It starts with branded polos, softshells and fleeces, with waterproofs, hi-vis vests, safety boots and caps making up the rest {loc}.",
 "Branded polos, softshells and fleeces anchor the kit, alongside waterproofs, hi-vis vests, safety boots and caps {loc}.",
 "Branded polos, softshells and fleeces are the essentials, with waterproofs, hi-vis vests, safety boots and caps alongside {loc}.",
]
S2TAIL_POOL=[
 ", branded polos, softshells and fleeces are the core of the kit, with waterproofs, hi-vis vests, safety boots and caps alongside.",
 ", the essentials are branded polos, softshells and fleeces, backed by waterproofs, hi-vis vests, safety boots and caps.",
 ", branded polos, softshells and fleeces lead, with waterproofs, hi-vis vests, safety boots and caps making up the rest.",
 ", branded polos, softshells and fleeces do the bulk of the work, with waterproofs, hi-vis vests, safety boots and caps alongside.",
 ", expect branded polos, softshells and fleeces first, then waterproofs, hi-vis vests, safety boots and caps.",
 ", branded polos, softshells and fleeces anchor the kit, with waterproofs, hi-vis vests, safety boots and caps completing it.",
]

UNIFORM_POOL=[  # "uniform before PPE" para, varied per town ({t})
 "What they wear is a uniform before it is PPE. A delivery driver is the most visible, most frequent face a courier company has, meeting {t} customers at the door dozens of times a day, so a clean, branded polo, softshell or fleece is what makes a driver and a firm look professional. Around it sit the practical layers: waterproofs for the weather, hi-vis vests for the roadside and the depot, and safety boots for loading and yard work.",
 "The kit is a uniform first and PPE second. A driver is the most visible, most frequent face a {t} courier firm has, at the door dozens of times a day, so a clean, branded polo, softshell or fleece is what makes the driver and the firm look professional, with the practical layers around it: waterproofs for the weather, hi-vis vests for roadside and depot, and safety boots for loading and yard work.",
 "More than PPE, it is a uniform. The driver is the most visible, most frequent face a {t} delivery firm has, meeting customers at the door all day, so a clean, branded polo, softshell or fleece is what reads as professional, with the working layers around it: waterproofs for the weather, hi-vis vests for the roadside and depot, and safety boots for loading and the yard.",
 "It is a uniform before it is protective kit. A {t} delivery driver is the company's most visible, most frequent face, at the door dozens of times a day, so a clean, branded polo, softshell or fleece is what makes a driver and a firm look professional, surrounded by the practical layers: waterproofs for the weather, hi-vis vests for roadside and depot, and safety boots for loading and yard work.",
]
LAYER_POOL=[  # "layering system" para, varied per town ({t})
 "And the work runs year-round and all-weather, which makes the kit a layering system: an embroidered polo in summer, a fleece and softshell through spring and autumn, a waterproof over the top in winter, and a hi-vis vest whenever a driver is at the kerbside or in a yard. Every layer carries the same branding, so a {t} driver looks consistent whatever the round and the weather throw at them.",
 "The round is year-round and all-weather, so the kit works as a layering system: an embroidered polo in summer, a fleece and softshell through spring and autumn, a waterproof over the top in winter, and a hi-vis vest whenever a driver is at the kerbside or in a yard, every layer carrying the same branding so a {t} driver looks consistent in any weather.",
 "Because the work is year-round and all-weather, the kit is really a layering system: a polo in summer, a fleece and softshell in spring and autumn, a waterproof over the top in winter, and a hi-vis vest at the kerbside or in the yard, all carrying the same branding so a {t} driver stays consistent whatever the round and weather bring.",
 "The job runs all year in all weather, so the kit layers up: an embroidered polo in summer, a fleece and softshell through the shoulder seasons, a waterproof over the top in winter, and a hi-vis vest at the kerbside or in a yard, every layer branded the same so a {t} driver looks consistent come rain or shine.",
]

def s1_paras(town, T):
    if 's1loc' in T:
        uniform = UNIFORM_POOL[pick(town,'uni',len(UNIFORM_POOL))].format(t=town)
        layer = LAYER_POOL[pick(town,'lay',len(LAYER_POOL))].format(t=town)
        own = OWNER_POOL[pick(town,'own',len(OWNER_POOL))]
        kit = KIT_POOL[pick(town,'kit',len(KIT_POOL))].format(loc=T['kit_loc'])
        p = list(T['s1loc']) + [uniform, layer.rstrip()+' '+own]
        return p + [kit]
    return T['s1']

def s2_local_text(town, T):
    if 's2_intro' in T:
        return T['s2_intro'].rstrip() + S2TAIL_POOL[pick(town,'s2t',len(S2TAIL_POOL))]
    return T['s2_local']

def faq_for(t, region):
    P = lambda salt, opts: opts[pick(t, salt, len(opts))]
    return [
     (f"Do you supply branded workwear to couriers and delivery firms in {t}?", P('fq1',[
      f"Yes. Owner-driver couriers and delivery fleets across {region} get embroidered polos and t-shirts, softshell and branded jackets, fleeces, waterproofs, hi-vis vests, safety boots and caps from us, branded in-house with the company name, on a trade account for a fleet or ordered direct online for an owner-driver.",
      f"Yes. Embroidered polos and t-shirts, softshell jackets, fleeces, waterproofs, hi-vis vests, safety boots and caps go to couriers and delivery firms across {region}, branded in-house with the company name, on a fleet trade account or ordered direct online.",
      f"Yes. From owner-drivers to depot fleets across {region}, we supply embroidered polos, softshells, fleeces, waterproofs, hi-vis vests, safety boots and caps, branded in-house, on account or ordered direct online.",
      f"Yes. Couriers and delivery firms across {region} get embroidered polos, softshells, fleeces, waterproofs, hi-vis vests, safety boots and caps from us, branded in-house with the company name, on a trade account or ordered direct online."])),
     ("Can an owner-driver order without a trade account?", P('fq2',[
      "Yes. An owner-driver or small courier firm can order direct online with no account: browse the range, choose your branded polos, a softshell, a hi-vis vest and safety boots, add sizes, send your logo once and check out. A trade account with volume pricing and purchase orders is there for fleets and depots that want it.",
      "Yes. An owner-driver or small courier firm orders direct online with no account: browse, pick your branded polos, a softshell, a hi-vis vest and safety boots, add sizes, send the logo once and check out. A trade account is there for fleets and depots that want volume pricing and POs.",
      "Yes, no account needed. An owner-driver or small firm orders direct online: choose your branded polos, a softshell, a hi-vis vest and safety boots, add sizes, send the logo once and check out, with a trade account available for fleets and depots.",
      "Yes. An owner-driver or small courier firm can order direct online without an account: browse, pick branded polos, a softshell, a hi-vis vest and safety boots, add sizes and send the logo once. A fleet trade account with volume pricing and POs is there if you want it."])),
     ("What workwear do delivery drivers and couriers need?", P('fq3',[
      "The core kit is embroidered polos and t-shirts for the warmer months, softshell jackets and fleeces for layering, waterproofs for all-weather doorstep work, hi-vis vests to EN ISO 20471 for roadside and depot visibility, safety boots for loading and depot work, and caps or beanies, all branded with the company name.",
      "Most drivers need embroidered polos and t-shirts, softshell jackets and fleeces, waterproofs, hi-vis vests to EN ISO 20471, safety boots and caps or beanies, all branded with the company name, a year-round layering system for an all-weather round.",
      "At minimum, embroidered polos and t-shirts, softshell jackets and fleeces for layering, waterproofs, hi-vis vests to EN ISO 20471, safety boots and caps or beanies, all branded with the company name.",
      "The core kit is embroidered polos and t-shirts, softshells and fleeces for layering, waterproofs for the weather, hi-vis vests to EN ISO 20471 for roadside and depot visibility, safety boots and caps, all branded with the company name."])),
     ("Why does branding matter so much for delivery drivers?", P('fq4',[
      "A delivery driver is the most visible and most frequent face of a courier company, meeting customers at the door dozens of times a day. A clean, embroidered polo, softshell or fleece makes a driver and a firm look professional and trustworthy at the doorstep, which is the cheapest and most effective marketing a delivery business has.",
      "A delivery driver is the most visible face of a courier firm, meeting customers at the door dozens of times a day, so a clean, embroidered polo, softshell or fleece makes the driver and the firm look professional and trustworthy, the cheapest and most effective marketing a delivery business has.",
      "Because the driver is the most visible, most frequent face of the company, meeting customers at the door all day. A clean, embroidered polo, softshell or fleece reads as professional and trustworthy at the doorstep, which is the best-value marketing a delivery firm has.",
      "A delivery driver meets customers at the door dozens of times a day and is the most visible face of the company, so a clean, embroidered polo, softshell or fleece makes the driver and the firm look professional and trusted, the cheapest marketing a delivery business has."])),
     ("Can you kit out a whole delivery fleet consistently?", P('fq5',[
      "Yes. A trade account gives a fleet or depot purchase-order ordering, volume pricing and one point of contact, so every driver, new starter and subcontractor is kitted in the same branded polos, softshells, fleeces and hi-vis. We hold your logo and sizes on file, so reorders and new starters always match across depots.",
      "Yes. A trade account gives a fleet purchase-order ordering, volume pricing and one contact, so every driver, new starter and subcontractor wears the same branded polos, softshells, fleeces and hi-vis, with your logo and sizes on file so reorders and new starters match across depots.",
      "Yes. With a trade account, a fleet or depot gets PO ordering, volume pricing and a single contact, so every driver and new starter is kitted in the same branded polos, softshells, fleeces and hi-vis, and we hold your logo and sizes on file so reorders match across depots.",
      "Yes. A fleet or depot trade account brings purchase-order ordering, volume pricing and one point of contact, so every driver, new starter and subcontractor matches in the same branded polos, softshells, fleeces and hi-vis, with logo and sizes held on file for consistent reorders across depots."])),
     ("Do you supply hi-vis for roadside and depot work?", P('fq6',[
      "Yes. We supply hi-vis vests and tops to EN ISO 20471 for multidrop drivers working at the roadside and kerbside and for staff in depots, yards and loading bays, alongside the branded polos, softshells, fleeces and waterproofs that make up the rest of the delivery uniform.",
      "Yes. Hi-vis vests and tops to EN ISO 20471 cover multidrop drivers at the roadside and kerbside and staff in depots, yards and loading bays, alongside the branded polos, softshells, fleeces and waterproofs of the rest of the uniform.",
      "Yes, hi-vis vests and tops to EN ISO 20471 for roadside and kerbside multidrop work and for depot, yard and loading-bay visibility, worn with the branded polos, softshells, fleeces and waterproofs that make up the delivery uniform.",
      "Yes. We supply hi-vis vests and tops to EN ISO 20471 for multidrop drivers at the roadside and kerbside and for depot, yard and loading-bay staff, alongside the branded polos, softshells, fleeces and waterproofs of the uniform."])),
     ("How quickly can you supply courier and delivery workwear?", P('fq7',[
      "Order direct online and your kit is dispatched on standard lead times, with embroidery added in-house before it ships. For a fleet, send your headcount, your logo and your sizes and we will build a branded kit list and quote, hold it on file and turn reorders and new-starter kit around on standard lead times.",
      "Order direct online and your kit ships on standard lead times, with embroidery added in-house first. For a fleet, send your headcount, logo and sizes and we will build a branded kit list and quote, hold it on file and turn reorders and new-starter kit around on standard lead times.",
      "Order direct online and we dispatch on standard lead times, embroidery added in-house before shipping. For a fleet, send your headcount, logo and sizes and we will build a branded kit list and quote and hold it on file, turning reorders around on standard lead times.",
      "Order direct online and your kit is dispatched on standard lead times with embroidery done in-house first. For a fleet, send your headcount, logo and sizes and we will build a branded kit list and quote, hold it on file and turn reorders and new-starter kit around on standard lead times."])),
    ]

# === PER-TOWN AUTHORED DATA (web-researched; geographic nearby) ============
TOWNS = {
 "birmingham": {
  "region":"Birmingham and the West Midlands",
  "nearby":["Solihull","West Bromwich","Walsall"],
  "snapshot":"iNeedWorkwear supplies embroidered polos, softshells, fleeces, waterproofs, hi-vis vests and safety boots to couriers and delivery firms across Birmingham, from owner-driver and multidrop couriers to same-day firms and the depot fleets clustered around the city's motorway network, all branded in-house with the company name, on a trade account for a fleet or ordered direct online for an owner-driver.",
  "s1_head":"Kitting the people who deliver the West Midlands, door to door",
  "s1loc":[
   "Birmingham sits at the heart of the UK's logistics network, on the edge of the Midlands distribution belt and wrapped by the M5, M6, M40 and M42, with rail and air freight through New Street and Birmingham Airport. That connectivity makes the city one of the busiest delivery markets in the country, and it keeps a vast community of couriers and delivery drivers moving parcels, pallets and same-day consignments across the West Midlands every day.",
   "The operations span the whole spectrum. National carriers run parcel depots across the city, in trade parks at Aston, Tyburn and Erdington and along the motorway corridors, while a dense layer of independent same-day and multidrop firms and owner-drivers handles urgent, document and last-mile work into every postcode from the city centre to Solihull, Walsall and the Black Country. Almost all of them wear something branded, and almost all of it works hard in all weathers.",
  ],
  "kit_loc":"across the city's doorsteps, depots and motorway-side hubs",
  "s2_intro":"Whether you drive a single van, run a multidrop round or operate a depot fleet across Birmingham and the motorway network around it",
 },
 "leeds": {
  "region":"Leeds and West Yorkshire",
  "nearby":["Bradford","Pudsey","Dewsbury"],
  "snapshot":"iNeedWorkwear supplies embroidered polos, softshells, fleeces, waterproofs, hi-vis vests and safety boots to couriers and delivery firms across Leeds, from owner-driver and multidrop couriers to same-day firms and the depot fleets along the M1 and M62 corridors, all branded in-house with the company name, on a trade account for a fleet or ordered direct online for an owner-driver.",
  "s1_head":"Kitting the people who deliver Yorkshire, door to door",
  "s1loc":[
   "Leeds is the commercial capital of Yorkshire and a major distribution centre, sitting on the M1, M62 and M621 at the crossroads of the North, with logistics hubs at Stourton and along Gelderd Road and the wider distribution belt running out through Wakefield, Normanton and Castleford. That makes it one of the busiest delivery markets in the North, keeping a large community of couriers and delivery drivers moving parcels, documents and same-day consignments across West Yorkshire every day.",
   "The operations span the whole spectrum. National carriers run parcel depots across the city and the M62 corridor, while a dense layer of independent same-day and multidrop firms and owner-drivers handles urgent, last-mile and document work, much of it for the legal, financial and retail businesses that make Leeds one of the biggest commercial centres outside London. Almost all of them wear something branded, and almost all of it works hard in all weathers.",
  ],
  "kit_loc":"across the city's doorsteps, depots and motorway-side hubs",
  "s2_intro":"Whether you drive a single van, run a multidrop round or operate a depot fleet across Leeds and the M1 and M62 corridors",
 },
}

# === CSV / nearby ==========================================================
_CSV=None
def _load_csv():
    global _CSV
    if _CSV is not None: return _CSV
    here=os.path.dirname(os.path.abspath(__file__))
    for p in (os.path.join(here,'DC_towns.csv'),'DC_towns.csv','/mnt/user-data/outputs/DC_towns.csv'):
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
                         f"(web-verified, all on DC_towns.csv). No rank/auto fallback.")
    bad = [n for n in nb if not any(r[1].lower()==n.lower() for r in _load_csv())]
    if bad:
        raise ValueError(f"{town}: nearby town(s) not on DC_towns.csv: {bad}")
    return nb[:3]

# === title / meta ==========================================================
def build_title(town):
    for t in (f"{town} Delivery and Courier Workwear",
              f"{town} Courier Workwear", f"{town} Delivery Workwear"):
        if len(t) <= 60: return t
    return f"{town} Courier Workwear"

def build_meta(town):
    for m in (f"Embroidered polos, softshells, hi-vis and waterproofs for {town} couriers and delivery drivers - branded workwear, trade accounts or order online direct.",
              f"Embroidered polos, softshells, hi-vis and waterproofs for {town} couriers and delivery drivers - branded workwear, on account or order online.",
              f"Branded polos, softshells, hi-vis and waterproofs for {town} couriers and delivery drivers - trade accounts or order online direct.",
              f"Branded workwear for {town} couriers and delivery drivers - polos, softshells, hi-vis, trade accounts or order online direct."):
        if len(m) <= 160: return m
    return f"Branded workwear for {town} couriers and delivery drivers - order online or on account."

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
        "name":f"Delivery and Courier Workwear Supply and Embroidery in {town}",
        "serviceType":"Delivery and courier workwear and embroidery supply",
        "provider":{"@id":"https://www.ineedworkwear.com/#organization"},
        "areaServed":[{"@type":"City","name":town}]+[{"@type":"City","name":n} for n in nearby],
        "audience":{"@type":"BusinessAudience","name":"Courier and delivery drivers and logistics operators"},
        "description":f"Embroidered polos, softshells, fleeces, waterproofs, hi-vis vests and safety boots supplied to couriers and delivery firms in {town}, on trade accounts or ordered direct online, with in-house embroidery.",
        "hasOfferCatalog":{"@type":"OfferCatalog","name":"Delivery and Courier Workwear",
            "itemListElement":[{"@type":"Offer","itemOffered":{"@type":"Product","name":p}} for p in DC_PRODUCTS]}}
    crumb = {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Home","item":DOMAIN},
        {"@type":"ListItem","position":2,"name":"Delivery and Courier Workwear","item":f"{DOMAIN}/delivery-courier-workwear"},
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

    emb_svg   = EMB.replace('a London courier company logo', f'a {town} courier company logo')
    sign_svg  = SIGNPOST.replace('London delivery and courier signpost', f'{town} delivery and courier signpost')
    sign_svg  = re.sub(r'<text x="230" y="62".*?</text>', signpost_town(town), sign_svg, flags=re.S)
    sign_svg  = sign_svg.replace('every kind of London delivery work', f'every kind of {town} delivery work')
    prem_svg  = PREMISES.replace('serving couriers and delivery firms across London', f'serving couriers and delivery firms across {town}')

    H=[build_head(town, slug, faqs, nearby), HEADER]
    H.append(f'<div class="dc-hero"><div class="dc-wrap"><div class="dc-subtitle">Branded Workwear for Couriers and Delivery Drivers</div><h1>{town} Delivery and Courier Workwear</h1></div></div>')
    H.append('<div class="dc-pulse"></div>')
    H.append(f'<div class="dc-trust-strip"><p>{trust}</p></div>')
    H.append(f'<div class="dc-wrap"><div class="dc-snapshot"><div class="dc-snapshot-label">Supplier Snapshot</div><p>{snap}</p></div></div>')
    H.append(STATS)
    H.append('<div class="dc-cta-bar"><a href="https://www.ineedworkwear.com" class="dc-cta-btn">Browse Courier and Delivery Workwear</a></div>')
    H.append('<div class="dc-jump-links"><a href="#range">Workwear Range</a><a href="#contract">The Driver Uniform</a><a href="#accounts">Ordering and Accounts</a><a href="#order">How to Order</a></div>')
    H.append(GARMENT)
    H.append(f'<div class="dc-section"><div class="dc-wrap"><h2>{s1head}</h2>'+''.join(f'<p>{p}</p>' for p in s1ps)+'</div></div>')
    H.append(f'<div class="dc-section" id="range"><div class="dc-wrap"><h2>Delivery and Courier Workwear Range</h2><p>{s2intro} <a href="https://www.ineedworkwear.com">Browse the full range at iNeedWorkwear.com</a>.</p><p class="dc-btn-center"><a href="https://www.ineedworkwear.com" class="dc-section-btn">Browse The Range</a></p>{grid}</div></div>')
    H.append(f'<div class="dc-section"><div class="dc-wrap"><h2>Your Driver Is Your Brand on the Doorstep</h2>'+''.join(f'<p>{p}</p>' for p in emb)+'</div></div>')
    H.append(emb_svg)
    H.append(f'<div class="dc-wrap"><div class="dc-contract" id="contract"><h3>{CON_HEAD}</h3>'+''.join(f'<p>{p}</p>' for p in con)+'</div></div>')
    H.append(sign_svg)
    H.append(f'<div class="dc-section" id="accounts"><div class="dc-wrap"><h2>{ACC_HEAD}</h2>'+''.join(f'<p>{p}</p>' for p in acc)+'</div></div>')
    H.append(prem_svg)
    H.append(f'<div class="dc-section"><div class="dc-wrap"><h2>Why Couriers and Delivery Firms Choose iNeedWorkwear</h2>'+''.join(f'<p>{p}</p>' for p in why)+'</div></div>')
    H.append(ORDER)
    H.append(f'<div class="dc-section" id="order"><div class="dc-wrap"><h2>How to Order Delivery and Courier Workwear</h2><p>{ordr[0]}</p><p>{ordr[1]}</p><p>{ordr[2]}</p><p class="dc-btn-center"><a href="https://www.ineedworkwear.com" class="dc-section-btn">Request A Quote</a></p><p>{selfp}</p>'+CONTACT+'</div></div>')
    faq_html=''.join(f'<div class="dc-faq-item"><div class="dc-faq-q">{q}</div><div class="dc-faq-a">{a}</div></div>' for q,a in faqs)
    H.append(f'<div class="dc-faq"><div class="dc-wrap"><h2>Delivery and Courier Workwear FAQ</h2>{faq_html}</div></div>')
    H.append(f'<div class="dc-wrap"><div class="dc-workwear">{sorted_}</div></div>')
    nb_links=''.join(f'<a href="dc-{slugify(n)}.html">Courier workwear in {n}</a>\n' for n in nearby)
    H.append(f'<div class="dc-nearby"><div class="dc-wrap"><h3>Delivery and Courier Workwear in Nearby Towns</h3><div class="dc-nearby-links">{nb_links}</div></div></div>')
    H.append(FOOTER+'\n</body></html>')
    return '\n'.join(H)

def main():
    args=[a for a in sys.argv[1:]]
    outdir=os.environ.get('DC_OUTDIR') or ('/mnt/user-data/outputs' if os.path.isdir('/mnt/user-data/outputs') else 'outputs')
    os.makedirs(outdir, exist_ok=True)
    if not args:
        args=[t for t in TOWNS if t!='london']
    for town_key in args:
        tk=town_key.lower()
        if tk=='london': continue
        if tk not in TOWNS:
            print(f"SKIP {town_key}: not in TOWNS (must be web-researched first)"); continue
        town=' '.join(w.capitalize() for w in tk.split())
        slug=f"dc-{slugify(town)}"
        html=assemble(slug, town)
        path=os.path.join(outdir, f"{slug}.html")
        open(path,'w',encoding='utf-8').write(html)
        print(f"WROTE {path}  ({len(html.split())} words approx)")

if __name__=='__main__':
    main()
