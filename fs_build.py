#!/usr/bin/env python3
# FS (Forestry, Arboriculture & Tree Surgery) series builder v1.0
# Read SPEC.md / CLAUDE.md first. TEMPLATE B (self-checkout / small-business):
# the buyer is the sole-trader arborist / small crew ordering DIRECT ONLINE, no
# account. Lead = CHAINSAW (trousers/PPE) + SAFETY BOOTS + HELMET. Chainsaw
# protection to EN ISO 11393 (Type A ground / Type C climbing) is the
# differentiator. Exactly 14 .com + 1 community link per page. No JS, no HTML
# entities, no delivery-timescale claims. Nearby MUST be geographically close,
# hand-authored, on FS_towns.csv (no rank fallback).
import re, os, json, zlib, hashlib, sys, csv

def pick(key, salt, n):
    # md5 digest gives well-distributed bits; crc32 % n leaks correlated low
    # bits (e.g. all 7-letter town names collided on the same pool variant).
    h = hashlib.md5((salt + '|' + str(key).lower()).encode()).digest()
    return int.from_bytes(h[:4], 'big') % n

def _find_base():
    here = os.path.dirname(os.path.abspath(__file__))
    for p in (os.path.join(here,'fs-london.html'),'fs-london.html',
              '/mnt/user-data/outputs/fs-london.html','/home/claude/fskit/fs-london.html'):
        if os.path.exists(p): return p
    sys.exit("ERROR: fs-london.html (base template) not found beside fs_build.py")

BASE = open(_find_base(), encoding='utf-8').read()
DOMAIN = 'https://www.ineedworkwear.uk'

def between(start, end, src=BASE):
    i = src.index(start); j = src.index(end, i+len(start)); return src[i:j]
def aria_block(aria):
    k = BASE.index(aria)
    i = BASE.rfind('<div class="fs-wrap"><div class="fs-illust">', 0, k)
    j = BASE.index('</div></div></div>', k) + len('</div></div></div>')
    return BASE[i:j]

CSS      = between('<style>', '</style>') + '</style>'
HEADER   = between('<div class="fs-header">', '\n<div class="fs-hero">')
STATS    = between('<div class="fs-stats">', '\n<div class="fs-cta-bar">')
GARMENT  = between('<div class="fs-wrap"><div class="fs-illust"><div class="fs-garment-row">', '\n<div class="fs-section">')
EMB      = aria_block('Embroidery machine stitching')
SIGNPOST = aria_block('tree surgery signpost')
PREMISES = aria_block('serving arborists and tree surgeons across')
ORDER    = aria_block('Order forestry and tree surgery workwear online')
CONTACT  = BASE[BASE.index('<div class="fs-contact-block">'):
                BASE.index('</div></div></div>', BASE.index('<div class="fs-contact-block">'))+len('</div></div></div>')]
FOOTER   = BASE[BASE.index('<footer class="fs-footer">'):BASE.index('</footer>')+len('</footer>')]

def signpost_town(town):
    n = len(town)
    size = 22 if n <= 8 else 19 if n <= 11 else 16 if n <= 15 else 13 if n <= 20 else 11
    tl = ' textLength="200" lengthAdjust="spacingAndGlyphs"' if n > 11 else ''
    return (f'<text x="230" y="62" text-anchor="middle" font-family="Arial,sans-serif" '
            f'font-weight="800" font-size="{size}" fill="#fff"{tl}>{town.upper()}</text>')

# === PRODUCTS ==============================================================
FS_PRODUCTS = ["Chainsaw Trousers and Protective Clothing","Chainsaw Boots and Safety Footwear",
 "Forestry Helmets, Visors and Ear Defenders","Chainsaw Gloves and Hand Protection",
 "Hi-Vis Jackets and Tops","Waterproofs and Base Layers","Embroidered Polo Shirts and Tops",
 "Embroidery, Names and ID Branding"]

def _card(n,d): return f'<div class="fs-product-card"><div class="fs-product-name">{n}</div><div class="fs-product-detail">{d}</div></div>'
_GA=_card("Chainsaw Trousers and Protective Clothing","Cut-protective chainsaw trousers and clothing to EN ISO 11393, in Type A for ground work and Type C all-round for climbing, usually Class 1 for a 20 metre-per-second chain speed.")
_GB=_card("Chainsaw Boots and Safety Footwear","Chainsaw-protective and safety boots with cut protection, grip and ankle support for felling, clearing and climbing on uneven, wet and timber-strewn ground.")
_GC=_card("Forestry Helmets, Visors and Ear Defenders","Forestry helmet units combining a hard hat, mesh or visor face protection and ear defenders, the head-to-ear protection every chainsaw operator needs on the ground and aloft.")
_GD=_card("Chainsaw Gloves and Hand Protection","Chainsaw-protective and general handling gloves for saw work, brash and timber handling and rope work, with grip and dexterity for ground and climbing crews.")
_GE=_card("Hi-Vis Jackets and Tops","Hi-vis jackets, vests and tops for roadside tree work, highway and rail vegetation and visibility in woodland, keeping a crew seen on the verge and on site.")
_GF=_card("Waterproofs and Base Layers","Waterproof jackets and trousers and warm base layers for outdoor work in all weather, breathable enough for the heat of climbing and clearing through a long day.")
_GG=_card("Embroidered Polo Shirts and Tops","Embroidered polos, t-shirts and softshells branded with your company name, so a sole trader or small crew turns out looking professional on every job and quote.")
_GH=_card("Embroidery, Names and ID Branding","In-house embroidery and badging of your name and ID onto polos, hi-vis and softshells, the cheapest marketing a tree surgeon has, matched on every reorder.")
GRID_POOL=[
 '<div class="fs-product-grid">'+_GA+_GB+_GC+_GD+_GE+_GF+_GG+_GH+'</div>',
 '<div class="fs-product-grid">'+_GA+_GC+_GB+_GD+_GE+_GF+_GG+_GH+'</div>',
 '<div class="fs-product-grid">'+_GA+_GB+_GD+_GC+_GE+_GF+_GG+_GH+'</div>',
]

# === PROSE POOLS ===========================================================
TRUST_POOL=[
 "Chainsaw trousers, boots, helmets and hi-vis for arborists and tree surgeons - order direct online across the UK",
 "Chainsaw-rated trousers, boots, helmets and branded workwear for tree surgeons - ordered direct online, UK-wide",
 "Trusted by sole-trader arborists and small tree-surgery crews across the UK for chainsaw PPE, ordered direct",
 "EN ISO 11393 chainsaw PPE, boots, helmets and branded workwear for arborists and tree surgeons across the UK",
]
S2INTRO_POOL=[
 "Whether you are a climbing arborist, a groundsman or a small tree-surgery crew working {t}'s gardens, parks and roadsides, the range is built to kit you head to toe from one place: chainsaw trousers and boots and a forestry helmet first, then gloves, hi-vis, waterproofs and branded polos.",
 "Climbing arborist, groundsman or small {t} crew, the range kits you head to toe from one place: chainsaw trousers, boots and a forestry helmet first, then gloves, hi-vis, waterproofs and branded polos, ordered direct.",
 "For a {t} arborist or small tree-surgery crew, the range covers the lot from one place: chainsaw trousers and boots and a forestry helmet, plus gloves, hi-vis, waterproofs and branded polos, in the sizes and protection classes you need.",
 "A {t} tree surgeon, climber or groundsman gets kitted head to toe from one place: chainsaw trousers, boots and a forestry helmet first, with gloves, hi-vis, waterproofs and branded polos alongside.",
]
EMB_P1_POOL=[
 "For a tree surgeon, branded kit is the cheapest and most effective marketing there is. A climber and a groundsman turning out in matching, embroidered polos and hi-vis on a customer's drive in {t} look like an established, professional firm, not a couple of people with a saw, and that impression wins the next job on the street as much as the work itself does.",
 "Branded kit is the cheapest marketing a {t} tree surgeon has. A climber and groundsman in matching, embroidered polos and hi-vis on a customer's drive look like an established firm rather than a couple of people with a saw, and that impression wins the next job on the street.",
 "For a {t} tree surgeon, branded kit is marketing that pays for itself. A crew in matching embroidered polos and hi-vis on a customer's drive reads as a professional, established firm, not two people and a saw, and that look wins the next job as much as the work does.",
 "Branded kit is the best-value marketing a {t} tree surgeon can buy. A climber and groundsman in matching embroidered polos and hi-vis look like an established firm on a customer's drive rather than a couple with a saw, and that impression earns the next job on the street.",
]
EMB_P2_POOL=[
 "We brand in-house, which means your company name and any ID are embroidered or badged onto polos, hi-vis and softshells, finished to wear hard outdoors. Send your artwork once, we hold it on file, and every reorder and new team member matches the last, so your {t} outfit looks consistent whether it is one van or three working across the area.",
 "Branding is applied in-house onto polos, hi-vis and softshells - your name and ID embroidered or badged and finished to wear hard outdoors. We hold your artwork on file, so reorders and new team members match, and your {t} outfit looks consistent whether it is one van or three.",
 "Your name and ID are embroidered or badged in-house onto polos, hi-vis and softshells, finished for hard outdoor wear. Held on file, your artwork reproduces on every reorder and new team member, so a {t} outfit stays consistent from one van to a small fleet.",
 "We badge in-house, embroidering your name and ID onto polos, hi-vis and softshells and finishing them to wear hard outdoors. Held on file, your branding matches on every reorder, so your {t} crew looks like one firm whether it is a single van or three.",
]
EMB_P3_POOL=[
 "And because it is all set up for direct ordering, branding a small team is quick and cheap: add your logo to the order, choose the items and sizes you want and check out. There is no minimum order to negotiate and no account to open, just professional, branded kit dispatched to get you out on the job looking the part.",
 "Because it is built for direct ordering, branding a small team is fast and cheap: add your logo, choose the items and sizes and check out, with no minimum order and no account to open, just branded kit dispatched to get you out looking the part.",
 "Set up for direct ordering, branding a small crew is quick and inexpensive: add your logo to the order, pick the items and sizes and check out, no minimum and no account, just professional, branded kit on its way.",
 "And since it is all direct ordering, branding a small team costs little and takes minutes: add the logo, choose items and sizes and check out, no minimum order and no account, just branded kit dispatched to get you on the job looking the part.",
]
# === CHAINSAW PPE BLOCK ====================================================
CON_HEAD="Chainsaw-Rated, Climb-Ready PPE: EN ISO 11393 for Arborists"
CON_P1_POOL=[
 "Tree work is one of the highest-risk trades in the country, and the chainsaw is the reason. That is why chainsaw protection is not optional kit but the core of the range: trousers, boots, gloves and helmet protection rated to EN ISO 11393, the standard that replaced EN 381, designed so the protective layers clog the saw and stop the chain if it touches. For a {t} arborist, getting the type and class right is the whole point.",
 "Tree work is among the highest-risk trades there is, and the chainsaw is why. So chainsaw protection is not optional but the core of the range: trousers, boots, gloves and helmet protection to EN ISO 11393, the standard that replaced EN 381, built so the protective fibres clog the saw and stop the chain on contact. For a {t} arborist, getting the type and class right is the whole point.",
 "Few trades carry the risk tree work does, and the chainsaw is the reason, which is why chainsaw protection is the core of the range rather than an add-on: trousers, boots, gloves and helmet protection to EN ISO 11393, the standard that succeeded EN 381, designed to clog the saw and stop the chain if it touches. For a {t} arborist, the type and class are what matter.",
 "Tree work is one of the most dangerous trades going, and the chainsaw is why, so chainsaw protection is the heart of the range, not an optional extra: trousers, boots, gloves and helmet protection to EN ISO 11393, the standard that replaced EN 381, made to jam the saw and stop the chain on contact. For a {t} arborist, getting the type and class right is everything.",
]
CON_P2_POOL=[
 "The protection has to match the work. Type A trousers protect the front of the legs and suit most ground-based felling and processing; Type C give all-round leg protection for climbing and aerial work, where a running saw can approach from any direction. Most arborist kit is Class 1, rated for a chain speed of 20 metres per second, and it is worn with a forestry helmet carrying a mesh visor and ear defenders, chainsaw boots and chainsaw gloves to complete the head-to-toe protection a chainsaw operator needs.",
 "Protection matches the work: Type A trousers protect the front of the legs for most ground-based felling and processing, while Type C give all-round protection for climbing and aerial work where the saw can come from any angle. Most arborist kit is Class 1 for a 20 metre-per-second chain speed, worn with a forestry helmet, mesh visor and ear defenders, chainsaw boots and gloves for head-to-toe protection.",
 "The protection has to suit the job. Type A trousers cover the front of the legs for ground-based felling and processing; Type C give all-round protection for climbing, where a running saw can approach from any direction. Most kit is Class 1, rated for 20 metres per second, and pairs with a forestry helmet carrying a visor and ear defenders, plus chainsaw boots and gloves.",
 "Protection has to fit the work: Type A trousers protect the leg fronts for most ground felling and processing, and Type C give all-round protection for climbing and aerial work where the saw can come from any side. Most arborist kit is Class 1 for 20 metres per second, worn with a forestry helmet, mesh visor and ear defenders, chainsaw boots and gloves.",
]
CON_P3_POOL=[  # 1 .com link each
 'For a sole trader or small team in {t}, the trick is getting all of that right in one order, in the right sizes and classes, without a procurement department to lean on. We stock the full chainsaw-rated range for ground and climbing crews and set it up for direct online ordering, so you can kit a climber and a groundsman properly and get back out on the job. Browse the chainsaw PPE range at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
 'For a {t} sole trader or small crew, the trick is getting it all right in one order, in the right sizes and classes, with no procurement department to lean on. We stock the full chainsaw-rated range for ground and climbing crews and set it up for direct online ordering, so you can kit a climber and a groundsman properly and get back out. Browse the chainsaw PPE range at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
 'The trick for a {t} sole trader or small team is getting all of it right in one order, the right sizes and protection classes, without a buyer to lean on. We stock the full chainsaw-rated range for ground and climbing crews, set up for direct online ordering, so you can kit the climber and the groundsman properly. Browse the chainsaw PPE range at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
 'For a {t} sole trader or small team, the job is getting it all right in one order, in the right sizes and classes, with no procurement department behind you. We stock the full chainsaw-rated range for ground and climbing crews and set it up for direct online ordering, so a climber and a groundsman get kitted properly. Browse the chainsaw PPE range at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
]
ACC_HEAD="How to Order: Direct, Online, No Account Needed"
ACC_P1_POOL=[
 "This range is built for how a tree surgeon actually buys. There is no trade account to set up, no minimum order to negotiate and no quote to wait on: browse the range, choose your chainsaw trousers, boots, helmet, gloves, hi-vis and a branded polo, pick your sizes and protection classes, add your logo once if you want branding and check out. It is the fastest way for a {t} sole trader or small crew to get properly kitted.",
 "The range is built for how a tree surgeon really buys: no trade account to set up, no minimum order and no quote to wait on. Browse, choose your chainsaw trousers, boots, helmet, gloves, hi-vis and a branded polo, pick sizes and protection classes, add your logo if you want it and check out, the fastest way for a {t} sole trader or small crew to get kitted.",
 "This is built for how a tree surgeon buys: no account, no minimum order, no quote to wait on. Browse the range, choose your chainsaw trousers, boots, helmet, gloves, hi-vis and a branded polo, pick your sizes and classes, add your logo and check out, the quickest route for a {t} sole trader or small crew.",
 "The whole range suits how a tree surgeon actually buys, with no account, no minimum and no quote: browse, choose your chainsaw trousers, boots, helmet, gloves, hi-vis and a branded polo, pick sizes and protection classes, add your logo and check out, the fastest way for a {t} sole trader or small crew to get kitted.",
]
ACC_P2_POOL=[
 "Getting the kit right matters more here than in most trades, so the range is set out to make it simple: Type A or Type C chainsaw trousers depending on whether you are ground-based or climbing, the right protection class, the helmet, gloves and boots to match, and the hi-vis and waterproofs for the conditions. Order it all together and it arrives as a complete, chainsaw-rated kit.",
 "Getting the kit right matters more here than most trades, so the range is laid out simply: Type A or Type C chainsaw trousers for ground or climbing, the right protection class, matching helmet, gloves and boots, and hi-vis and waterproofs for the conditions. Order it together and it lands as a complete, chainsaw-rated kit.",
 "Because getting the kit right matters more here than in most trades, the range is set out to make it easy: Type A or Type C trousers for ground or climbing, the right class, helmet, gloves and boots to match, plus hi-vis and waterproofs. Order the lot together and it arrives as a complete, chainsaw-rated kit.",
 "Getting it right matters more in this trade, so the range is organised to make it simple: Type A or Type C chainsaw trousers for ground or climbing work, the right protection class, the matching helmet, gloves and boots, and the hi-vis and waterproofs for the weather, all arriving as one complete chainsaw-rated kit.",
]
ACC_P3_POOL=[
 "Everything is branded in-house, which means your name and ID are applied under our control before the order ships, so a one-van outfit or a small crew turns out looking professional from day one. Your logo and sizes are held on file, so the next reorder or a new team member matches, and delivery reaches {t} and the surrounding area on standard lead times.",
 "All branding is done in-house, so your name and ID are applied under our control before the order ships, and a one-van outfit or small crew looks professional from day one. We hold your logo and sizes on file, so reorders and new team members match, and delivery reaches {t} and the wider area on standard lead times.",
 "Because branding is done in-house, your name and ID are applied under our control before shipping, so a one-van outfit or small crew turns out professional from the start. Your logo and sizes stay on file for reorders and new starters, and orders reach {t} and the surrounding area on standard lead times.",
 "Branding happens in-house, so your name and ID are applied under our control before the order ships, and a one-van outfit or small crew looks the part from day one. We keep your logo and sizes on file, so reorders and new team members match, and delivery reaches {t} and the area around it on standard lead times.",
]
ACC_P4_POOL=[  # 2 .com links each
 'Order direct online with no account at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>, and if your team grows into needing volume pricing and purchase orders, a trade account is there when you want it at <a href="https://www.ineedworkwear.com">iNeedWorkwear</a>.',
 'Order direct online with no account at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>. If your team grows and you want volume pricing and purchase orders, a trade account is there when you need it at <a href="https://www.ineedworkwear.com">iNeedWorkwear</a>.',
 'Browse and order direct online with no account at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>, and when your team grows into volume pricing and purchase orders, a trade account is ready at <a href="https://www.ineedworkwear.com">iNeedWorkwear</a>.',
 'Order direct online, no account needed, at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>. Should your team grow into needing volume pricing and purchase orders, a trade account is there at <a href="https://www.ineedworkwear.com">iNeedWorkwear</a>.',
]
WHY_P1_POOL=[
 "A {t} tree surgeon who turns out in proper chainsaw-rated trousers and boots, a forestry helmet and clean, branded kit looks like a safe, professional operation to every customer, site manager and council officer who sees the job, and iNeedWorkwear supplies that whole kit from a single place, branded in-house and priced and sold for how a sole trader or small crew actually buys.",
 "Turned out in proper chainsaw-rated trousers and boots, a forestry helmet and clean, branded kit, a {t} tree surgeon looks safe and professional to every customer, site manager and council officer at the job, and iNeedWorkwear supplies that whole kit from one place, branded in-house and sold for how a sole trader or small crew really buys.",
 "A {t} tree surgeon in proper chainsaw-rated trousers and boots, a forestry helmet and clean, branded kit reads as a safe, professional operation to every customer and officer who sees the job, and we supply that complete kit from a single place, branded in-house and priced for how a sole trader or small crew actually buys.",
 "Kitted in proper chainsaw-rated trousers and boots, a forestry helmet and clean, branded gear, a {t} tree surgeon looks safe and professional to customers, site managers and council officers alike, and we supply that whole kit from one place, branded in-house and sold for how a sole trader or small crew buys.",
]
WHY_P2_POOL=[
 "Everything comes from the same place. The supplier that brands your polos and hi-vis also supplies your chainsaw trousers, boots, helmet, gloves and waterproofs, so a climber and a groundsman are kitted head to toe from one order and nothing falls through the gap between the branded layer and the chainsaw protection that keeps you safe.",
 "Kit comes in one order. The supplier branding your polos and hi-vis also supplies chainsaw trousers, boots, helmet, gloves and waterproofs, so a climber and groundsman are kitted head to toe and nothing slips between the branded layer and the chainsaw protection that keeps you safe.",
 "All from one supplier. The same company behind your branded polos and hi-vis also provides chainsaw trousers, boots, helmet, gloves and waterproofs, so a climber and a groundsman are kitted head to toe from a single order.",
 "Kit comes from one place. Alongside the branded polos and hi-vis sit chainsaw trousers, boots, helmet, gloves and waterproofs, so a climber and groundsman are kitted head to toe and nothing falls through the gap between branding and chainsaw protection.",
]
WHY_P3_POOL=[
 "The range is built around what tree work actually wears out and replaces: chainsaw trousers and boots, helmet visors, gloves, hi-vis and waterproofs, the everyday kit of the ground and the canopy. That practical focus keeps pricing and reordering realistic whether you are buying for yourself or for a small crew.",
 "Everything in the range reflects what tree work really gets through: chainsaw trousers and boots, helmet visors, gloves, hi-vis and waterproofs, the daily kit of the ground and the canopy, and that focus keeps pricing and reordering realistic whether you buy for yourself or a small crew.",
 "The range centres on what tree work genuinely uses and replaces, chainsaw trousers and boots, helmet visors, gloves, hi-vis and waterproofs, and that practical focus keeps pricing and reordering sensible whether you are kitting yourself or a small crew.",
 "Everything is built around what tree work really gets through, chainsaw trousers and boots, helmet visors, gloves, hi-vis and waterproofs, so pricing and reordering stay realistic whether you buy for yourself or a small crew.",
]
WHY_P4_POOL=[
 "And it is set up for how you buy: direct online, no account, no minimum order and no quote to wait on, with your logo and sizes held on file so every reorder and new team member matches and turns out looking professional from the first job.",
 "And the ordering suits how you buy: direct online, no account, no minimum and no quote, with your logo and sizes on file so every reorder and new team member matches and looks professional from the first job.",
 "And it fits how you actually buy: direct online, no account, no minimum order, no quote to wait on, with logo and sizes held so every reorder and new starter matches and looks the part from day one.",
 "And it is built for how you buy: straight online, no account, no minimum and no waiting on a quote, with your logo and sizes on file so every reorder and new team member matches and turns out professional from the first job.",
]
ORD_P1_POOL=[
 "iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis, waterproofs and embroidered polos to arborists, tree surgeons and forestry contractors across {region}, all rated to EN ISO 11393 and branded in-house with your company name and ID.",
 "We supply chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis, waterproofs and embroidered polos to arborists, tree surgeons and forestry contractors across {region}, all rated to EN ISO 11393 and branded in-house.",
 "Across {region}, iNeedWorkwear kits arborists, tree surgeons and forestry contractors in chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis, waterproofs and embroidered polos, all to EN ISO 11393 and branded in-house.",
 "From a single climber to a small crew across {region}, iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis, waterproofs and embroidered polos, all rated to EN ISO 11393 and branded in-house.",
]
ORD_P2_POOL=[
 "Ordering is direct and online: browse the range, pick your chainsaw trousers in Type A or Type C and the right protection class, choose your boots, helmet, gloves, hi-vis and a branded polo, add your sizes, send your logo once and check out. There is no account to set up and no quote to wait on.",
 "Ordering is direct online: browse, pick your chainsaw trousers in Type A or Type C and the right class, choose boots, helmet, gloves, hi-vis and a branded polo, add sizes, send your logo once and check out, with no account to set up and no quote to wait on.",
 "You order direct online: browse the range, choose Type A or Type C chainsaw trousers and the right protection class, add boots, helmet, gloves, hi-vis and a branded polo, pick sizes, send the logo once and check out, no account and no quote needed.",
 "Ordering is straight online: browse, pick your chainsaw trousers in Type A or Type C and the right class, choose boots, helmet, gloves, hi-vis and a branded polo, add sizes and send your logo once, then check out, with no account and no quote to wait on.",
]
ORD_P3_POOL=[
 "We hold your logo and sizes on file, so reordering or kitting a new team member is quick and everything matches, and embroidery is added in-house before your order ships.",
 "Your logo and sizes are held on file, so reordering or kitting a new team member is fast and everything matches, with embroidery added in-house before the order ships.",
 "We keep your logo and sizes on file, so a reorder or a new team member is quick and matches the rest, and embroidery is done in-house before your order ships.",
 "Your logo and sizes stay on file, so reordering or kitting a new starter is quick and consistent, and embroidery is added in-house before the order goes out.",
]
SELF_POOL=[  # 1 .com link each
 'Sole trader or small crew and need kit now? Browse the full range, add your sizes and order direct on self-service checkout at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
 'Just kitting yourself or a small crew? Browse the range, add sizes and order direct on self-service checkout at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
 'Sole-trader arborist needing kit today? Browse the full range, add your sizes and order direct on self-service checkout at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
 'Need chainsaw PPE for a small crew now? Browse the range, add sizes and order direct on self-service checkout at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
]
SORTED_POOL=[  # 1 .com link each
 '<h3>Forestry and Tree Surgery Workwear, Sorted</h3><p>From chainsaw trousers and boots to forestry helmets, gloves, hi-vis and waterproofs, get chainsaw-rated kit built for arborists and tree surgeons at fair prices - branded in-house with your name, and ordered direct online with no account needed.</p><p><a href="https://www.ineedworkwear.com">Browse forestry and tree surgery workwear at iNeedWorkwear</a></p>',
 '<h3>Forestry and Tree Surgery Workwear, Sorted</h3><p>Chainsaw trousers, boots, forestry helmets, gloves, hi-vis and waterproofs - chainsaw-rated kit for arborists and tree surgeons at fair prices, branded in-house with your name and ordered direct online, no account needed.</p><p><a href="https://www.ineedworkwear.com">Browse forestry and tree surgery workwear at iNeedWorkwear</a></p>',
 '<h3>Forestry and Tree Surgery Workwear, Sorted</h3><p>From chainsaw trousers and boots to helmets, gloves, hi-vis and waterproofs, kit yourself or your crew out at fair prices, branded in-house and ordered direct online with no account to set up.</p><p><a href="https://www.ineedworkwear.com">Browse forestry and tree surgery workwear at iNeedWorkwear</a></p>',
 '<h3>Forestry and Tree Surgery Workwear, Sorted</h3><p>Chainsaw trousers, boots, forestry helmets, gloves, hi-vis and waterproofs, the full chainsaw-rated kit at fair prices, branded in-house and ordered direct online for a sole trader or small crew.</p><p><a href="https://www.ineedworkwear.com">Browse forestry and tree surgery workwear at iNeedWorkwear</a></p>',
]
OWNER_POOL=[
 "And the buyer is the tree surgeon, not a procurement department: a sole trader or small crew who wants to choose the right kit, get the sizes and protection class right, add a logo and order it direct online, without setting up a trade account or waiting on a quote.",
 "The buyer here is the tree surgeon, not a buying department: a sole trader or small crew wanting to pick the right kit, get the sizes and protection class right, add a logo and order direct online, with no account to set up and no quote to wait on.",
 "It is the tree surgeon who buys, not a procurement office: a sole trader or small crew choosing the right kit, the right sizes and protection class, adding a logo and ordering direct online without a trade account or a quote.",
 "The buyer is the tree surgeon themselves, a sole trader or small crew, who wants to choose the right kit, get the sizes and protection class right, add a logo and order it direct online, no trade account, no quote.",
 "And it is the tree surgeon who buys, not a procurement team: a sole trader or small crew picking the right kit, sizes and protection class, adding a logo and ordering direct online, without an account or a quote to wait on.",
 "The person buying is the tree surgeon, not a buyer: a sole trader or small crew who wants the right kit in the right sizes and protection class, a logo added and the lot ordered direct online, no account and no quote.",
]
KIT_POOL=[
 "Chainsaw trousers, boots and a forestry helmet are the non-negotiables, worn with gloves, hi-vis, waterproofs and branded polos {loc}.",
 "The core kit is chainsaw trousers, boots and a forestry helmet, with gloves, hi-vis, waterproofs and branded polos alongside {loc}.",
 "Chainsaw trousers, boots and a forestry helmet do the heavy lifting, backed by gloves, hi-vis, waterproofs and branded polos {loc}.",
 "It starts with chainsaw trousers, boots and a forestry helmet, with gloves, hi-vis, waterproofs and branded polos making up the rest {loc}.",
 "Chainsaw trousers, boots and a forestry helmet anchor the kit, alongside gloves, hi-vis, waterproofs and branded polos {loc}.",
 "Chainsaw trousers, boots and a forestry helmet are the essentials, with gloves, hi-vis, waterproofs and branded polos alongside {loc}.",
]
S2TAIL_POOL=[
 ", chainsaw trousers, boots and a forestry helmet are the core of the kit, with gloves, hi-vis, waterproofs and polos alongside.",
 ", the essentials are chainsaw trousers, boots and a forestry helmet, backed by gloves, hi-vis, waterproofs and branded polos.",
 ", chainsaw trousers, boots and a forestry helmet lead, with gloves, hi-vis, waterproofs and polos making up the rest.",
 ", chainsaw trousers, boots and a forestry helmet do the bulk of the work, with gloves, hi-vis, waterproofs and polos alongside.",
 ", expect chainsaw trousers, boots and a forestry helmet first, then gloves, hi-vis, waterproofs and branded polos.",
 ", chainsaw trousers, boots and a forestry helmet anchor the kit, with gloves, hi-vis, waterproofs and polos completing it.",
]

def s1_paras(town, T):
    if 's1loc' in T:
        own = OWNER_POOL[pick(town,'own',len(OWNER_POOL))]
        kit = KIT_POOL[pick(town,'kit',len(KIT_POOL))].format(loc=T['kit_loc'])
        p = list(T['s1loc']); p[-1] = p[-1].rstrip()+' '+own
        return p + [kit]
    return T['s1']

def s2_local_text(town, T):
    if 's2_intro' in T:
        return T['s2_intro'].rstrip() + S2TAIL_POOL[pick(town,'s2t',len(S2TAIL_POOL))]
    return T['s2_local']

def faq_for(t, region):
    P = lambda salt, opts: opts[pick(t, salt, len(opts))]
    return [
     (f"Do you supply chainsaw PPE and workwear to tree surgeons in {t}?", P('fq1',[
      f"Yes. Arborists, tree surgeons and forestry contractors across {region} get chainsaw trousers and protective clothing, chainsaw boots, forestry helmets with visors and ear defenders, chainsaw gloves, hi-vis, waterproofs and embroidered polos from us, branded in-house and ordered direct online, with no account needed for a sole trader or small team.",
      f"Yes. Chainsaw trousers and protective clothing, chainsaw boots, forestry helmets with visors, chainsaw gloves, hi-vis, waterproofs and embroidered polos go to arborists and tree surgeons across {region}, branded in-house and ordered direct online, no account needed.",
      f"Yes. From sole-trader climbers to small tree-surgery crews across {region}, we supply chainsaw trousers, boots, forestry helmets, gloves, hi-vis, waterproofs and polos, branded in-house and ordered direct online.",
      f"Yes. Arborists, tree surgeons and forestry contractors across {region} get chainsaw trousers, boots, forestry helmets, gloves, hi-vis, waterproofs and embroidered polos from us, branded in-house and ordered direct online with no account needed."])),
     ("Can a sole trader or small tree surgery firm order without an account?", P('fq2',[
      "Yes. The whole range is set up for direct online ordering: browse, choose your chainsaw trousers, boots, helmet, gloves and a branded polo, add sizes, send your logo once and check out, with no account to set up. It is built for sole traders and small teams who want kit fast, and a trade account is there too if your team grows.",
      "Yes. Everything is set up for direct online ordering: browse, pick your chainsaw trousers, boots, helmet, gloves and a branded polo, add sizes, send your logo once and check out, no account needed. It suits sole traders and small teams, with a trade account available if you grow.",
      "Yes, no account needed. The range is built for direct online ordering: choose your chainsaw trousers, boots, helmet, gloves and a branded polo, add sizes, send the logo once and check out, with a trade account there if your team grows.",
      "Yes. The range is set up for direct online ordering with no account: browse, pick your chainsaw trousers, boots, helmet, gloves and a branded polo, add sizes and send the logo once. It is built for sole traders and small teams, and a trade account is there if you grow."])),
     ("What PPE does an arborist or tree surgeon need?", P('fq3',[
      "The core kit is chainsaw trousers or protective clothing to EN ISO 11393, chainsaw boots, a forestry helmet with mesh visor and ear defenders, chainsaw gloves, hi-vis for roadside and visibility, waterproofs and base layers for outdoor work, and embroidered polos, with Type A protection for ground work and Type C all-round protection for climbing.",
      "Most arborists need chainsaw trousers to EN ISO 11393, chainsaw boots, a forestry helmet with visor and ear defenders, chainsaw gloves, hi-vis, waterproofs and base layers, and embroidered polos, in Type A for ground work and Type C for climbing.",
      "At minimum, chainsaw trousers or protective clothing to EN ISO 11393, chainsaw boots, a forestry helmet with mesh visor and ear defenders, chainsaw gloves, hi-vis, waterproofs and base layers, and branded polos, with Type A for ground and Type C for climbing.",
      "The core kit is chainsaw trousers to EN ISO 11393, chainsaw boots, a forestry helmet with visor and ear defenders, chainsaw gloves, hi-vis, waterproofs and base layers, and embroidered polos, with Type A protection for ground work and Type C for climbing."])),
     ("What is the difference between Type A and Type C chainsaw trousers?", P('fq4',[
      "Type A chainsaw trousers protect the front of the legs and suit most ground-based chainsaw work, while Type C give all-round leg protection and are used for climbing and aerial work where the saw can approach from any angle. Both are rated to EN ISO 11393, usually at Class 1 for a 20 metre-per-second chain speed, and we stock both for ground and climbing crews.",
      "Type A trousers protect the front of the legs for most ground-based chainsaw work; Type C give all-round leg protection for climbing and aerial work where the saw can come from any angle. Both are EN ISO 11393, usually Class 1 for 20 metres per second, and we stock both.",
      "Type A protect the front of the legs and suit ground-based work, while Type C give all-round protection for climbing, where a running saw can approach from any direction. Both are rated to EN ISO 11393, usually Class 1 at 20 metres per second, and we stock both for ground and climbing crews.",
      "Type A chainsaw trousers cover the leg fronts for ground work; Type C give all-round protection for climbing and aerial work. Both meet EN ISO 11393, usually Class 1 for a 20 metre-per-second chain speed, and we stock both for ground and climbing crews."])),
     ("Can you brand kit for a small tree surgery team?", P('fq5',[
      "Yes. We embroider or badge your company name and ID onto polos, hi-vis and softshells in-house, so a one-van outfit or a small crew turns out looking professional on every job and quote. Send your artwork once, we hold it on file, and every reorder and new starter matches, which is the cheapest marketing a tree surgeon has.",
      "Yes. Your company name and ID are embroidered or badged in-house onto polos, hi-vis and softshells, so a one-van outfit or small crew looks professional on every job. Send artwork once and we hold it on file, so reorders and new starters match.",
      "Yes, all branding is done in-house onto polos, hi-vis and softshells, so a one-van outfit or small crew turns out professional on every job and quote. We hold your artwork on file, so every reorder matches, the cheapest marketing a tree surgeon has.",
      "Yes. Send your artwork once and we embroider or badge your name and ID in-house onto polos, hi-vis and softshells, holding it on file so a one-van outfit or small crew matches on every reorder and looks professional on every job."])),
     ("Do you stock both ground and climbing kit?", P('fq6',[
      "Yes. We stock Type A chainsaw trousers and ground PPE for groundsmen and felling work, and Type C all-round chainsaw trousers, lighter climbing layers and the helmets, gloves and boots a climber needs for aerial work, so a tree surgery firm can kit both the climber and the groundie from one place.",
      "Yes. Type A chainsaw trousers and ground PPE for groundsmen and felling, plus Type C all-round trousers, lighter climbing layers and the helmets, gloves and boots a climber needs, so you can kit both the climber and the groundie from one place.",
      "Yes, both. We stock Type A trousers and ground PPE for felling and processing, and Type C all-round trousers, climbing layers and the helmets, gloves and boots a climber needs, so a firm kits the climber and the groundsman together.",
      "Yes. We carry Type A chainsaw trousers and ground PPE for groundsmen, and Type C all-round trousers, lighter climbing layers and the helmets, gloves and boots a climber needs, so a tree surgery firm can kit both from one place."])),
     ("How fast can I get chainsaw PPE and workwear?", P('fq7',[
      "Order direct online and your kit is dispatched on standard lead times, with embroidery added in-house before it ships. Browse the range, add your sizes, send your logo once if you want branding and check out, and we will get a sole trader or a small crew kitted and out on the job without the wait of a trade-account setup.",
      "Order direct online and your kit is dispatched on standard lead times, with embroidery added in-house first. Browse, add your sizes, send your logo if you want branding and check out, and a sole trader or small crew is kitted and out on the job without a trade-account setup.",
      "Order direct online and we dispatch on standard lead times, embroidery added in-house before shipping. Browse the range, add sizes, send the logo once if you want branding and check out, getting a sole trader or small crew kitted without the wait of a trade account.",
      "Order direct online and your kit ships on standard lead times with embroidery done in-house first. Browse, add your sizes, send the logo if you want it and check out, and a sole trader or small crew is kitted and back out without a trade-account setup."])),
    ]

# === PER-TOWN AUTHORED DATA (web-researched; geographic nearby) ============
TOWNS = {
 "birmingham": {
  "region":"Birmingham and the West Midlands",
  "nearby":["Solihull","West Bromwich","Walsall"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Birmingham, from sole-trader climbers and groundsmen to small firms working the city's leafy suburbs, parks and Sutton Park woodland, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear the West Midlands' trees",
  "s1loc":[
   "Birmingham is one of the greenest cities in the UK, with over a million trees and the status of a UN Tree City of the World, and all of that canopy needs managing, which keeps a large community of arborists and tree surgeons busy across the city. Most of them are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work spans the city's contrasts. Leafy suburbs like Edgbaston, Sutton Coldfield, Moseley and Solihull carry mature garden trees and high canopy cover, while parks and the ancient woodland of Sutton Park, a 2,400-acre national nature reserve and a surviving trace of the old Forest of Arden, hold thousands of trees, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Birmingham tree surgeons are typically NPTC and City and Guilds qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, often Arboricultural Association members, and the rise of ash dieback and oak pests across the West Midlands has only added to the felling and sanitation work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "And the firms doing it are mostly small: a climber and a groundsman, a family business, a one or two-van outfit working across the city and into the leafy borders of Solihull and Sutton Coldfield. They buy their own kit, get the sizes and protection class right and want it ordered direct without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the city's gardens, parks and woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Birmingham's gardens, parks and Sutton Park woodland",
 },
 "leeds": {
  "region":"Leeds and West Yorkshire",
  "nearby":["Bradford","Pudsey","Dewsbury"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Leeds, from sole-trader climbers and groundsmen to small firms working the city's leafy suburbs, parks and West Yorkshire woodland, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Yorkshire's trees",
  "s1loc":[
   "Leeds is a green city with a large estate of mature street, park and garden trees, and managing it keeps a big community of arborists and tree surgeons busy across the city and West Yorkshire. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the city's leafy geography. Suburbs like Roundhay, Chapel Allerton, Headingley, Alwoodley and Bramhope carry mature oak, beech and estate trees, while Roundhay Park, Temple Newsam, the Meanwood Valley and the wider White Rose Forest hold parkland and woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Leeds tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and TPO and conservation-area rules shape much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "And the firms are mostly small: a climber and a groundsman, a family business, a one or two-van outfit working across Leeds, Wetherby and the wider West Yorkshire patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the city's gardens, parks and woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Leeds's gardens, parks and West Yorkshire woodland",
 },
 "glasgow": {
  "region":"Glasgow and the West of Scotland",
  "nearby":["Paisley", "Rutherglen", "Clydebank"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Glasgow, from sole-trader climbers and groundsmen to small firms working Pollok Country Park, Cathkin Braes and the wider Clyde Climate Forest, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Glasgow's trees",
  "s1loc":[
   "Glasgow is a green city with a large estate of mature street, park and garden trees, and managing it keeps a big community of arborists and tree surgeons busy across the city and the West of Scotland. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the city's leafy geography. Suburbs like Bearsden, Milngavie, Newlands and the West End carry mature oak, beech and estate trees, while Pollok Country Park, Cathkin Braes, Dawsholm Park, Kelvingrove and the wider Clyde Climate Forest hold parkland and woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Glasgow tree surgeons are typically NPTC, City and Guilds and Lantra qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and conservation-area and TPO rules shape much of the work. Ash dieback is confirmed and spreading across the city's parks, schools and roads, and Storm Eowyn toppled trees the length of Glasgow in early 2025, so felling and clearance stays steady. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "And the firms are mostly small: a climber and a groundsman, a family business, a one or two-van outfit working across Glasgow, Bearsden and the wider West of Scotland patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the city's gardens, parks and woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Glasgow's gardens, parks and Clyde Valley woodland",
 },
 "sheffield": {
  "region":"Sheffield and South Yorkshire",
  "nearby":["Rotherham", "Barnsley", "Chesterfield"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Sheffield, from sole-trader climbers and groundsmen to small firms working Ecclesall Woods, the Rivelin Valley and the city's ancient woodland, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Sheffield's trees",
  "s1loc":[
   "Sheffield is one of the most wooded cities in Britain, with a vast estate of mature street, park and woodland trees, and managing it keeps a big community of arborists and tree surgeons busy across the city and South Yorkshire. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the city's leafy geography. Suburbs like Dore, Totley, Fulwood and Ranmoor carry mature oak, beech and estate trees, while Ecclesall Woods, Graves Park, Endcliffe Park, the Rivelin Valley and the Loxley Valley hold parkland and ancient woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Sheffield tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and the city's street-tree partnership and conservation-area rules shape much of the work. Ash dieback runs through the woodland estate and storm events keep clearance steady, so felling and deadwooding stays in demand. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "And the firms are mostly small: a climber and a groundsman, a family business, a one or two-van outfit working across Sheffield, Dronfield and the wider South Yorkshire patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the city's gardens, parks and ancient woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Sheffield's gardens, parks and South Yorkshire woodland",
 },
 "manchester": {
  "region":"Manchester and Greater Manchester",
  "nearby":["Salford", "Stockport", "Oldham"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Manchester, from sole-trader climbers and groundsmen to small firms working Heaton Park, Fletcher Moss and the City of Trees community forest, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Greater Manchester's trees",
  "s1loc":[
   "Manchester is a green city with a large estate of mature street, park and garden trees, and managing it keeps a big community of arborists and tree surgeons busy across the city and Greater Manchester. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the city's leafy geography. Suburbs like Didsbury, Chorlton, Withington and Whalley Range carry mature oak, beech and estate trees, while Heaton Park, Fletcher Moss, Chorlton Ees and the wider City of Trees community forest hold parkland and woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Manchester tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and the conservation areas at Didsbury St James and Chorlton Green, where trees over 75mm are protected, shape much of the work. Ash dieback runs through the urban forest and storm clearance keeps crews busy. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "And the firms are mostly small: a climber and a groundsman, a family business, a one or two-van outfit working across Manchester, Sale and the wider Greater Manchester patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the city's gardens, parks and woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Manchester's gardens, parks and Greater Manchester woodland",
 },
 "edinburgh": {
  "region":"Edinburgh and the Lothians",
  "nearby":["Musselburgh", "Livingston", "Bathgate"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Edinburgh, from sole-trader climbers and groundsmen to small firms working Corstorphine Hill, the Hermitage of Braid and the Pentland Hills, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Edinburgh's trees",
  "s1loc":[
   "Edinburgh is a particularly leafy city, with a large estate of mature street, park and garden trees, and managing it keeps a big community of arborists and tree surgeons busy across the city and the Lothians. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the city's leafy geography. Suburbs like Corstorphine, Blackford, Morningside and Colinton carry mature oak, beech and estate trees, while Corstorphine Hill, the Hermitage of Braid and Blackford Hill, Holyrood Park and the Pentland Hills hold parkland and broad-leaved woodland of oak, birch, elm, sycamore, beech and ash, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Edinburgh tree surgeons are typically NPTC and Lantra qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and conservation-area and TPO rules shape much of the work. Chalara ash dieback is now firmly established across the city and the council fells infected trees on its land where they pose a risk, so felling and clearance stays steady. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "And the firms are mostly small: a climber and a groundsman, a family business, a one or two-van outfit working across Edinburgh, Musselburgh and the wider Lothians patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the city's gardens, parks and woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Edinburgh's gardens, parks and Lothians woodland",
 },
 "liverpool": {
  "region":"Liverpool and Merseyside",
  "nearby":["Bootle", "Birkenhead", "Crosby"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Liverpool, from sole-trader climbers and groundsmen to small firms working Sefton Park, Calderstones and the wider Mersey Forest, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Merseyside's trees",
  "s1loc":[
   "Liverpool is a green city with a large estate of mature street, park and garden trees, and managing it keeps a big community of arborists and tree surgeons busy across the city and Merseyside. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the city's leafy geography. Suburbs like Allerton, Mossley Hill, Woolton and Aigburth carry mature oak, beech and estate trees, while Sefton Park, Calderstones Park with its thousand-year-old Allerton Oak, Croxteth Hall Park, the National Trust's Speke Hall woodland and the wider Mersey Forest hold parkland and woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Liverpool tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and the Woolton, Allerton and Mossley Hill conservation areas and TPO rules shape much of the work. Ash dieback runs heavy across the Merseyside rural fringe, keeping felling and clearance steady. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "And the firms are mostly small: a climber and a groundsman, a family business, a one or two-van outfit working across Liverpool, Crosby and the wider Merseyside patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the city's gardens, parks and woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Liverpool's gardens, parks and Merseyside woodland",
 },
 "bristol": {
  "region":"Bristol and the West of England",
  "nearby":["Bath", "Weston-super-Mare", "Portishead"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Bristol, from sole-trader climbers and groundsmen to small firms working Leigh Woods, Ashton Court and the wider Forest of Avon, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Bristol's trees",
  "s1loc":[
   "Bristol is a notably green city with a huge estate of mature street, park and garden trees, and looking after it keeps a busy community of arborists and tree surgeons working across the city and the West of England. Most are sole traders and small teams covering domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the city's leafy geography. Suburbs like Clifton, Stoke Bishop, Sneyd Park, Westbury-on-Trym and Henleaze carry mature oak, beech, lime and plane, while Leigh Woods, Ashton Court Estate, Blaise Castle, the Avon Gorge and the wider Forest of Avon hold ancient woodland and veteran oak pollards, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Bristol tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with TPOs, the city's conservation areas and ongoing ash dieback shaping much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "And the firms are mostly small: a climber and a groundsman, a family business, a one or two-van outfit working across Bristol, Bath and the North Somerset patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the city's gardens, parks and gorge-side woodland work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Bristol's gardens, parks and Avon Gorge woodland",
 },
 "cardiff": {
  "region":"Cardiff and South Wales",
  "nearby":["Barry", "Penarth", "Caerphilly"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Cardiff, from sole-trader climbers and groundsmen to small firms working Bute Park, Forest Farm and the Wenallt, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Cardiff's trees",
  "s1loc":[
   "Cardiff is a green capital with a large estate of mature street, park and garden trees, and managing it keeps a steady community of arborists and tree surgeons busy across the city and South Wales. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the city's leafy geography. Suburbs like Cyncoed, Lisvane, Rhiwbina, Llandaff and Penylan carry mature oak, beech and lime, while Bute Park, Roath Park, Forest Farm, the Wenallt and Fforest Fawr hold parkland and semi-natural ancient woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Cardiff tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with Natural Resources Wales, Coed Cymru, TPOs and ongoing ash dieback work in Bute Park and beyond shaping much of the job. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "And the firms are mostly small: a climber and a groundsman, a family business, a one or two-van outfit working across Cardiff, the Vale of Glamorgan and the South Wales valleys. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the city's gardens, parks and valley-edge woodland work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Cardiff's parks, the Wenallt and the South Wales valleys",
 },
 "leicester": {
  "region":"Leicester and Leicestershire",
  "nearby":["Loughborough", "Oadby", "Hinckley"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Leicester, from sole-trader climbers and groundsmen to small firms working Bradgate Park, Watermead and the Charnwood Forest, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Leicestershire's trees",
  "s1loc":[
   "Leicester is a green city with a large estate of mature street, park and garden trees, and managing it keeps a busy community of arborists and tree surgeons working across the city and Leicestershire. Most are sole traders and small teams covering domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the city's leafy geography. Suburbs like Stoneygate, Clarendon Park, Knighton and Western Park carry mature oak, lime, sweet chestnut, plane and beech, while Bradgate Park, Swithland Wood, Watermead Country Park and the wider Charnwood Forest and National Forest hold parkland and ancient woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Leicester tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with the Stoneygate and Clarendon Park conservation areas, TPOs and severe ash dieback across the Charnwood outcrop shaping much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "And the firms are mostly small: a climber and a groundsman, a family business, a one or two-van outfit working across Leicester, Loughborough and the Charnwood patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the city's gardens, parks and Charnwood woodland work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Leicester's gardens, parks and Charnwood Forest woodland",
 },
 "bradford": {
  "region":"Bradford and West Yorkshire",
  "nearby":["Keighley", "Shipley", "Bingley"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Bradford, from sole-trader climbers and groundsmen to small firms working Heaton Woods, the St Ives Estate and Shipley Glen, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Bradford's trees",
  "s1loc":[
   "Bradford is a green district with a large estate of mature street, park and garden trees set against the moorland edge, and managing it keeps a busy community of arborists and tree surgeons working across the city and West Yorkshire. Most are sole traders and small teams covering domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the district's leafy geography. Suburbs like Heaton, Baildon, Cottingley and Saltaire carry mature oak, beech and lime, while Heaton Woods, Northcliffe Wood, Hirst Wood, the St Ives Estate at Bingley and Shipley Glen up onto Baildon Moor hold ancient woodland and parkland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Bradford tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with TPOs, conservation areas and widespread ash dieback across the district's ash population shaping much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "And the firms are mostly small: a climber and a groundsman, a family business, a one or two-van outfit working across Bradford, Keighley and the Aire Valley patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the district's gardens, parks and Aire Valley woodland work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Bradford's woods, the St Ives Estate and the Aire Valley",
 },
 "coventry": {
  "region":"Coventry and Warwickshire",
  "nearby":["Nuneaton", "Bedworth", "Kenilworth"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Coventry, from sole-trader climbers and groundsmen to small firms working Coombe Abbey, the War Memorial Park and the Coundon Wedge, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Coventry's trees",
  "s1loc":[
   "Coventry is a green city with a large estate of mature street, park and garden trees, and managing it keeps a busy community of arborists and tree surgeons working across the city and Warwickshire. Most are sole traders and small teams covering domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the city's leafy geography. Suburbs like Allesley, Earlsdon, Stivichall and Coundon carry mature oak, lime and beech, while Coombe Abbey Country Park, the War Memorial Park, Allesley Park, the Coundon Wedge and the Kenilworth Road woodlands of Wainbody Wood and Stivichall Common hold parkland and mixed woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Coventry tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with the Allesley Village conservation area, TPOs, the council's urban forestry strategy and ongoing ash dieback shaping much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "And the firms are mostly small: a climber and a groundsman, a family business, a one or two-van outfit working across Coventry, Kenilworth and the wider Warwickshire patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the city's gardens, parks and Warwickshire woodland work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Coventry's parks, the Coundon Wedge and Warwickshire woodland",
 },
 "nottingham": {
  "region":"Nottingham and the East Midlands",
  "nearby":["Beeston", "Arnold", "West Bridgford"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Nottingham, from sole-trader climbers and groundsmen to small firms working the city's leafy suburbs, parks and the Greenwood Community Forest, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Nottingham's trees",
  "s1loc":[
   "Nottingham is a green city with a large estate of mature street, park and garden trees, and managing it keeps a busy community of arborists and tree surgeons working across the city and the wider East Midlands. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the city's leafy geography. Suburbs like Mapperley Park, The Park Estate, Sherwood and Wollaton carry mature lime, oak and beech and Victorian garden trees, while Wollaton Park, the Arboretum, Colwick Country Park and the wider Greenwood Community Forest hold parkland and woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Nottingham tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and TPO and conservation-area rules across the city and Rushcliffe, Gedling and Broxtowe shape much of the work. Ash dieback is a live issue here, with diseased ash managed and felled across Sherwood and the suburbs, and every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "And the firms are mostly small: a climber and a groundsman, a family business, a one or two-van outfit working across Nottingham, Beeston and the wider Nottinghamshire patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the city's gardens, parks and woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Nottingham's gardens, parks and Greenwood Community Forest woodland",
 },
 "newcastle upon tyne": {
  "region":"Newcastle upon Tyne and the North East",
  "nearby":["Gateshead", "Gosforth", "Tynemouth"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Newcastle upon Tyne, from sole-trader climbers and groundsmen to small firms working the city's leafy suburbs, parks and Tyneside woodland, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Tyneside's trees",
  "s1loc":[
   "Newcastle upon Tyne is a green city with a large estate of mature street, park and garden trees, and managing it keeps a busy community of arborists and tree surgeons working across the city and the wider North East. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the city's leafy geography. Suburbs like Jesmond, Gosforth, Heaton and Kenton carry mature oak, beech and estate trees, while Jesmond Dene, the Town Moor and Cow Hill, Leazes Park, Heaton Park and Gosforth Central Park hold ancient woodland and parkland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Newcastle tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and TPO and conservation-area rules shape much of the work. Storm Arwen in November 2021 hit the North East hard, with gusts above 90mph coming unusually from the north-east and felling thousands of trees across Tyne and Wear and County Durham, leaving years of clearance and replanting, and every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "And the firms are mostly small: a climber and a groundsman, a family business, a one or two-van outfit working across Newcastle, Gateshead and the wider Tyneside patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the city's gardens, parks and woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Newcastle's gardens, parks and Tyneside woodland",
 },
 "sunderland": {
  "region":"Sunderland and the North East",
  "nearby":["Washington", "Houghton le Spring", "Seaham"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Sunderland, from sole-trader climbers and groundsmen to small firms working the city's parks, country parks and Wearside woodland, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Wearside's trees",
  "s1loc":[
   "Sunderland is a green city with a large estate of mature street, park and garden trees, and managing it keeps a busy community of arborists and tree surgeons working across the city and the wider North East. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the city's leafy geography. Mature trees line the older suburbs and the riverside, while Herrington Country Park below Penshaw Monument, Hetton Lyons Country Park and the woodland and former colliery sites around Washington and Houghton le Spring hold parkland and reclaimed woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Sunderland tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and TPO and conservation-area rules shape much of the work. Storm Arwen in November 2021 battered the North East with gusts above 90mph from an unusual north-east direction, felling thousands of trees across Tyne and Wear and County Durham and leaving years of clearance and replanting, and every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "And the firms are mostly small: a climber and a groundsman, a family business, a one or two-van outfit working across Sunderland, Washington and the wider Wearside patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the city's parks, country parks and woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Sunderland's parks, country parks and Wearside woodland",
 },
 "brighton": {
  "region":"Brighton and East Sussex",
  "nearby":["Hove", "Worthing", "Shoreham-by-Sea"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Brighton, from sole-trader climbers and groundsmen to small firms working the city's leafy suburbs, parks and South Downs woodland, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Brighton's trees",
  "s1loc":[
   "Brighton is a green city with a large estate of mature street, park and garden trees, and managing it keeps a busy community of arborists and tree surgeons working across the city and the wider Sussex coast. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the city's leafy geography. Suburbs like Withdean, Patcham, Preston Park and Hove carry mature elm, beech and estate trees, while Stanmer Park and its Great Wood, Preston Park, Hove Park and Withdean Park run up into the South Downs National Park, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Brighton tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and TPO and conservation-area rules shape much of the work. The city holds the National Elm Collection, with over 17,000 elms protected by Dutch elm disease sanitation felling, so diseased elm work and careful removals are a constant, and every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "And the firms are mostly small: a climber and a groundsman, a family business, a one or two-van outfit working across Brighton, Hove and the wider Sussex patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the city's gardens, parks and Downs woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Brighton's gardens, parks and South Downs woodland",
 },
 "plymouth": {
  "region":"Plymouth and Devon",
  "nearby":["Saltash", "Bodmin", "St Austell"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Plymouth, from sole-trader climbers and groundsmen to small firms working the city's parks, estate woodland and the Plym Valley, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Plymouth's trees",
  "s1loc":[
   "Plymouth is a green city with a large estate of mature street, park and garden trees, and managing it keeps a busy community of arborists and tree surgeons working across the city and the wider Devon and Cornwall border. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the city's leafy geography. Mature trees line the older suburbs and Central Park, while Plymbridge Woods and the Plym Valley, the Saltram estate above the River Plym and the western oak woodland running up to the Dartmoor fringe hold parkland and ancient woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Plymouth tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and TPO and conservation-area rules shape much of the work. The National Trust holds Plymbridge Woods and Saltram with their oak woodland and parkland, ash dieback is being managed across the valley sides, and every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "And the firms are mostly small: a climber and a groundsman, a family business, a one or two-van outfit working across Plymouth, Saltash and the wider Devon and Cornwall patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the city's parks, estate woodland and valley tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Plymouth's parks, estate woodland and the Plym Valley",
 },
 "hull": {
  "region":"Hull and East Yorkshire",
  "nearby":["Beverley", "Hessle", "Cottingham"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Hull, from sole-trader climbers and groundsmen to small firms working the city's leafy avenues, parks and East Yorkshire woodland from Pearson Park to the Humber Bridge Country Park, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear East Yorkshire's trees",
  "s1loc":[
   "Hull is a green port city with a large estate of mature street, avenue and park trees, and managing it keeps a steady community of arborists and tree surgeons busy across the city and out into East Yorkshire. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the city's leafy geography. The Avenues and Pearson Park carry mature oak, ash, sycamore and beech on tree-lined streets, while East Park, Pickering Park and Kingswood hold parkland, and out at the edges Beverley Westwood, Beverley Parks Nature Reserve and the Woodland Trust's Humber Bridge Country Park at Hessle bring proper woodland into reach, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Hull tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and TPO and conservation-area rules in the Avenues and Pearson Park shape much of the work. Ash dieback has put a lot of roadside and woodland ash on the felling list across the East Riding, and every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "And the firms are mostly small: a climber and a groundsman, a family business, a one or two-van outfit working across Hull, Beverley, Hessle and Cottingham and the wider East Yorkshire patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the city's avenues, parks and East Yorkshire woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Hull's avenues, parks and East Yorkshire woodland",
 },
 "derby": {
  "region":"Derby and Derbyshire",
  "nearby":["Belper", "Ripley", "Long Eaton"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Derby, from sole-trader climbers and groundsmen to small firms working the city's leafy suburbs, parks and Derbyshire woodland from Allestree Park to the edge of the Peak District and the National Forest, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Derbyshire's trees",
  "s1loc":[
   "Derby is a green city sitting between the Derwent valley, the Peak District and the National Forest, with a large estate of mature street, park and garden trees, and managing it keeps a busy community of arborists and tree surgeons working across the city and the wider county. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the city's leafy geography. Suburbs like Allestree, Darley Abbey, Mickleover and Littleover carry mature oak, beech and estate trees, while Allestree Park and its Big Wood, Markeaton Park and Darley Park hold parkland and woodland above the Derwent, and Shipley Country Park near Ripley, Belper Parks and the Calke Abbey estate add country-park and veteran-tree work, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Derby tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and TPO and conservation-area rules shape much of the work. With the city bordering the Peak District and the National Forest planting reaching up from the south, there is steady woodland-management, ash dieback felling and replanting work, and every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "And the firms are mostly small: a climber and a groundsman, a family business, a one or two-van outfit working across Derby, Belper, Ripley and Long Eaton and the wider Derbyshire patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the city's gardens, parks and Derbyshire woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Derby's gardens, parks and Derbyshire woodland",
 },
 "southampton": {
  "region":"Southampton and Hampshire",
  "nearby":["Eastleigh", "Totton", "Fareham"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Southampton, from sole-trader climbers and groundsmen to small firms working the city's leafy suburbs, parks and Hampshire woodland from Southampton Common to the edge of the New Forest, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Hampshire's trees",
  "s1loc":[
   "Southampton is a green waterside city with a large estate of mature street, park and garden trees and the New Forest on its doorstep, and managing it keeps a big community of arborists and tree surgeons busy across the city and the wider county. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the city's leafy geography. Suburbs like Bassett, Highfield and Bitterne Park carry mature oak, beech and estate trees on tree-lined roads, while Southampton Common, Mayfield Park and the Chessel Bay reserve hold parkland and woodland inside the city, and Itchen Valley Country Park near Eastleigh, Lakeside at Eastleigh and Holly Hill Woodland Park at Fareham add ancient woodland and country-park work, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Southampton tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and TPO and conservation-area rules shape much of the work. With the New Forest and its Forestry England veteran oaks and beeches close to the south and west around Totton, there is steady woodland and veteran-tree work alongside the urban canopy, and every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "And the firms are mostly small: a climber and a groundsman, a family business, a one or two-van outfit working across Southampton, Eastleigh, Totton and Fareham and the wider Hampshire patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the city's gardens, parks and Hampshire woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Southampton's gardens, parks and Hampshire woodland",
 },
 "stoke-on-trent": {
  "region":"Stoke-on-Trent and Staffordshire",
  "nearby":["Newcastle-under-Lyme", "Kidsgrove", "Biddulph"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Stoke-on-Trent, from sole-trader climbers and groundsmen to small firms working the city's leafy suburbs, parks and Staffordshire woodland from the Trentham Estate to Hem Heath Woods and Cannock Chase, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Staffordshire's trees",
  "s1loc":[
   "Stoke-on-Trent is a green city of six towns with a large estate of mature street, park and garden trees and proper woodland on its fringes, and managing it keeps a busy community of arborists and tree surgeons working across the Potteries and North Staffordshire. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the city's leafy geography. Suburbs like Trentham, Hartshill and Westlands carry mature oak, beech and estate trees, while the Trentham Estate with its ancient woodland, Hem Heath Woods, Park Hall Country Park and Westport Lake hold parkland and woodland, and Apedale Country Park at Newcastle-under-Lyme, Bathpool Park at Kidsgrove and Biddulph Grange Country Park add country-park work, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Stoke tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and TPO and conservation-area rules shape much of the work. Ash dieback has put a lot of woodland and roadside ash on the felling list across Staffordshire, and with Cannock Chase and its Forestry England plantations to the south there is steady woodland-management work too, every chainsaw job, on the ground or roped into a canopy, depending on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "And the firms are mostly small: a climber and a groundsman, a family business, a one or two-van outfit working across Stoke-on-Trent, Newcastle-under-Lyme, Kidsgrove and Biddulph and the wider Staffordshire patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the city's gardens, parks and Staffordshire woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Stoke-on-Trent's gardens, parks and Staffordshire woodland",
 },
 "wolverhampton": {
  "region":"Wolverhampton and the Black Country",
  "nearby":["Bilston", "Willenhall", "Sedgley"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Wolverhampton, from sole-trader climbers and groundsmen to small firms working the city's leafy suburbs, parks and Black Country woodland from West Park and the Smestow Valley to Baggeridge Country Park, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear the Black Country's trees",
  "s1loc":[
   "Wolverhampton is a greener city than its Black Country roots suggest, with a large estate of mature street, park and garden trees, and managing it keeps a steady community of arborists and tree surgeons busy across the city and the wider Black Country. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the city's leafy geography. Suburbs like Tettenhall, Penn and Compton carry mature oak, beech and estate trees, while the Victorian West Park, Bantock Park and the Smestow Valley Local Nature Reserve hold parkland and woodland inside the city, and Northycote Farm, the National Trust's Wightwick Manor and Baggeridge Country Park near Sedgley add estate and country-park work, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Wolverhampton tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and TPO and conservation-area rules around Tettenhall and Sedgley Beacon shape much of the work. Ash dieback has put a lot of roadside and woodland ash on the felling list across the region, and with Cannock Chase and its Forestry England plantations close to the north there is steady woodland work too, every chainsaw job, on the ground or roped into a canopy, depending on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "And the firms are mostly small: a climber and a groundsman, a family business, a one or two-van outfit working across Wolverhampton, Bilston, Willenhall and Sedgley and the wider Black Country patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the city's gardens, parks and Black Country woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Wolverhampton's gardens, parks and Black Country woodland",
 },
 "swansea": {
  "region":"Swansea and West Glamorgan",
  "nearby":["Neath", "Llanelli", "Port Talbot"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Swansea, from sole-trader climbers and groundsmen to small firms working the city's leafy suburbs, Gower woodland and Clyne Valley, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the climbers and groundsmen working Swansea's trees",
  "s1loc":[
   "Swansea is a green coastal city wrapped around Gower, with a big estate of mature street, park, garden and valley trees, and managing it keeps a busy community of arborists and tree surgeons working across the city and the wider Swansea Bay. Most are sole traders and small teams on domestic gardens, council and park contracts and storm clearance, every one of them reliant on proper chainsaw PPE.",
   "The work follows the city's leafy geography. Suburbs like Sketty, Mumbles, Bishopston and Langland carry mature oak, beech and estate trees, while Singleton Park, Clyne Valley Country Park, Bishop's Wood, Penllergare Valley Woods and the Natural Resources Wales forestry on Gower and in the Afan Valley hold parkland and woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Swansea tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with ash dieback across Gower and the valleys driving a steady run of felling and removals. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "And the firms are mostly small: a climber and a groundsman, a family business, a one or two-van outfit working across Swansea, Gower and the wider West Glamorgan patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the city's gardens, parks and Gower woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Swansea's gardens, Gower woodland and Clyne Valley",
 },
 "milton keynes": {
  "region":"Milton Keynes and Buckinghamshire",
  "nearby":["Bedford", "Dunstable", "Bicester"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Milton Keynes, from sole-trader climbers and groundsmen to small firms working the city's millions of trees, linear parks and ancient woodland, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear the forest city's trees",
  "s1loc":[
   "Milton Keynes was built as a forest city, with millions of trees planted across its grid roads, parks and estates, and managing that enormous canopy keeps a busy community of arborists and tree surgeons working right across the city. Most are sole traders and small teams on domestic gardens, grid-road and park contracts and storm clearance, every one of them reliant on proper chainsaw PPE.",
   "The work follows the city's planted geography. The Parks Trust looks after the canopy along the grid roads and the Ouse and Ouzel linear parks, while Linford Wood, Howe Park Wood and Shenley Wood hold ancient woodland and parkland trees, all of it generating thinning, crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Milton Keynes tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with ash dieback across the city's woods driving felling and a major oak-replanting effort. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "And the firms are mostly small: a climber and a groundsman, a family business, a one or two-van outfit working across Milton Keynes, Newport Pagnell and the wider Buckinghamshire patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the city's grid-road trees, linear parks and woodland",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Milton Keynes's grid-road trees, linear parks and ancient woodland",
 },
 "aberdeen": {
  "region":"Aberdeen and the North East",
  "nearby":["Arbroath", "Elgin", "Perth"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Aberdeen, from sole-trader climbers and groundsmen to small firms working the city's leafy West End, parks and Deeside woodland, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the climbers and groundsmen working the Granite City's trees",
  "s1loc":[
   "Aberdeen is a granite city set on the edge of Royal Deeside, with a large estate of mature street, park, garden and estate trees, and managing it keeps a busy community of arborists and tree surgeons working across the city and out along the Dee. Most are sole traders and small teams on domestic gardens, council and park contracts and storm clearance, every one of them reliant on proper chainsaw PPE.",
   "The work follows the city's leafy geography. West End suburbs like Cults, Bieldside, Milltimber and Countesswells carry mature beech, pine and estate trees, while Hazlehead Park, Duthie Park, Countesswells Wood, Foggieton Woods and the Forestry and Land Scotland pinewoods up Deeside hold parkland and woodland, all of it generating crown reductions, dismantles, felling, windblow clearance and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Aberdeen tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with Storm Arwen windblow across the North East having left a long run of clearance and felling work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "And the firms are mostly small: a climber and a groundsman, a family business, a one or two-van outfit working across Aberdeen, Banchory and the wider Deeside patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the city's gardens, parks and Deeside woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Aberdeen's leafy West End, parks and Deeside woodland",
 },
 "reading": {
  "region":"Reading and Berkshire",
  "nearby":["Wokingham", "Bracknell", "Woodley"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Reading, from sole-trader climbers and groundsmen to small firms working the town's leafy suburbs, parks and Thames Valley woodland, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear the Thames Valley's trees",
  "s1loc":[
   "Reading is a green Thames Valley town with a large estate of mature street, park, garden and riverside trees, and managing it keeps a busy community of arborists and tree surgeons working across the town and the wider Berkshire patch. Most are sole traders and small teams on domestic gardens, council and park contracts and storm clearance, every one of them reliant on proper chainsaw PPE.",
   "The work follows the town's leafy geography. Suburbs like Caversham, Caversham Heights, Emmer Green, Tilehurst and Earley carry mature oak, beech and estate trees, while Prospect Park, Caversham Court, the McIlroy Park and Blundells Copse ancient woodland and the Chilterns and Thames-side woods just north hold parkland and woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Reading tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with TPO and conservation-area rules across Caversham and the older suburbs shaping much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "And the firms are mostly small: a climber and a groundsman, a family business, a one or two-van outfit working across Reading, Pangbourne and the wider Berkshire patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's gardens, parks and Thames Valley woodland",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Reading's leafy suburbs, parks and Thames Valley woodland",
 },
 "northampton": {
  "region":"Northampton and Northamptonshire",
  "nearby":["Wellingborough", "Kettering", "Rushden"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Northampton, from sole-trader climbers and groundsmen to small firms working the town's leafy suburbs, parks and Salcey Forest woodland, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the climbers and groundsmen working Northamptonshire's trees",
  "s1loc":[
   "Northampton is a green Nene Valley town with a large estate of mature street, park, garden and parkland trees, and managing it keeps a busy community of arborists and tree surgeons working across the town and the wider Northamptonshire patch. Most are sole traders and small teams on domestic gardens, council and park contracts and storm clearance, every one of them reliant on proper chainsaw PPE.",
   "The work follows the town's leafy geography. Suburbs like Abington, Kingsthorpe, Duston and Wootton carry mature oak, beech and estate trees, while Abington Park, Delapre Woods with its fine oak and sweet chestnut, Hunsbury Hill Country Park and the Forestry England oaks of Salcey Forest hold parkland and woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Northampton tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with ash dieback across the county's parks and woodland driving a steady run of felling and removals. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "And the firms are mostly small: a climber and a groundsman, a family business, a one or two-van outfit working across Northampton, Towcester and the wider Northamptonshire patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's gardens, parks and Northamptonshire woodland",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Northampton's leafy suburbs, parks and Salcey Forest woodland",
 },
 "luton": {
  "region":"Luton and Bedfordshire",
  "nearby":["Dunstable", "Hitchin", "Harpenden"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Luton, from sole-trader climbers and groundsmen to small firms working Stockwood Park, Wardown Park and the Chiltern woodland on the town's edge, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear the Chilterns' trees",
  "s1loc":[
   "Luton sits at the foot of the Chiltern Hills on the River Lea, a busy Bedfordshire town wrapped in mature street, park and estate trees, and managing that green estate keeps a steady community of arborists and tree surgeons working across the town and the surrounding countryside. Most are sole traders and small teams on domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the town's leafy geography. Suburbs like Wigmore, Stopsley and Round Green carry mature garden and street trees, while Stockwood Park and the old Crawley estate, Wardown Park on the Lea, Wigmore Valley Park and Kidney Wood hold parkland and woodland, and the Chiltern beechwoods rise just beyond the edge, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Luton tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and ash dieback across the Chilterns has driven thousands of felled ash trees and a heavy run of safety work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "And the firms are mostly small: a climber and a groundsman, a family business, a one or two-van outfit working across Luton, Dunstable and the wider Bedfordshire and Chilterns patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's gardens, parks and Chiltern woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Luton's parks, gardens and Chiltern woodland",
 },
 "portsmouth": {
  "region":"Portsmouth and Hampshire",
  "nearby":["Gosport", "Fareham", "Havant"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Portsmouth, from sole-trader climbers and groundsmen to small firms working Portsdown Hill, the South Downs and the Hampshire woodland inland, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Hampshire's coastal trees",
  "s1loc":[
   "Portsmouth is a dense island city backed by green Hampshire countryside, with a large estate of street, park and garden trees and the wooded chalk of Portsdown Hill on its northern edge, and managing it keeps a steady community of arborists and tree surgeons busy across the city and South Hampshire. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the city's geography. Suburbs like Cosham, Drayton and Farlington carry mature garden and street trees, while Victoria Park, Portsdown Hill with its chalk grassland and scrub, Staunton Country Park and Stansted Park run along the edge, and Queen Elizabeth Country Park and the South Downs beechwoods rise inland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Portsmouth tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and ash dieback across the South Downs woodlands keeps a heavy run of felling and safety work coming. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "And the firms are mostly small: a climber and a groundsman, a family business, a one or two-van outfit working across Portsmouth, Havant and the wider South Hampshire patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the city's gardens, parks and South Downs woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Portsmouth's parks, Portsdown Hill and South Downs woodland",
 },
 "peterborough": {
  "region":"Peterborough and Cambridgeshire",
  "nearby":["Stamford", "Spalding", "Corby"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Peterborough, from sole-trader climbers and groundsmen to small firms working Nene Park, Thorpe Wood and the Nene Valley woodland, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear the Nene Valley's trees",
  "s1loc":[
   "Peterborough is a fast-growing Cambridgeshire city set in the Nene Valley, with a large estate of street, park and parkway trees and ancient woodland on its doorstep, and managing it keeps a steady community of arborists and tree surgeons busy across the city and the surrounding fen and valley country. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the city's green geography. Suburbs like Longthorpe, Orton and Bretton carry mature garden and parkway trees, while Ferry Meadows and the wider Nene Park, Thorpe Wood on its heavy clay and the Bretton Woodlands hold parkland and woodland, with the Forest of Marston Vale and Nene Valley planting beyond, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Peterborough tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and ash dieback in the Bretton Woodlands has driven a council felling programme along paths and boundaries. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "And the firms are mostly small: a climber and a groundsman, a family business, a one or two-van outfit working across Peterborough, Stamford and the wider Nene Valley and fen patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the city's gardens, parks and Nene Valley woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Peterborough's parks, gardens and Nene Valley woodland",
 },
 "bolton": {
  "region":"Bolton and Greater Manchester",
  "nearby":["Bury", "Wigan", "Horwich"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Bolton, from sole-trader climbers and groundsmen to small firms working Smithills, Moss Bank Park and the West Pennine Moors woodland, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear the West Pennine trees",
  "s1loc":[
   "Bolton is a green Greater Manchester town that climbs from the valley up to the edge of the West Pennine Moors, with a large estate of mature street, park and estate trees, and managing it keeps a steady community of arborists and tree surgeons busy across the town and the moorland fringe. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the town's leafy geography. Suburbs like Heaton, Lostock and Smithills carry mature oak and beech and estate trees, while Moss Bank Park, the Smithills Estate, England's largest Woodland Trust site, running from Barrow Bridge up toward Winter Hill, and the wooded cloughs of the West Pennine Moors hold parkland and woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Bolton tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and exposure to West Pennine wind and a heavy stock of TPO trees around Heaton, Lostock and Smithills Hall shape much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "And the firms are mostly small: a climber and a groundsman, a family business, a one or two-van outfit working across Bolton, Bury and the wider Greater Manchester and West Pennine patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's gardens, parks and West Pennine woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Bolton's parks, estates and West Pennine woodland",
 },
 "dudley": {
  "region":"Dudley and the West Midlands",
  "nearby":["Stourbridge", "Halesowen", "Brierley Hill"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Dudley, from sole-trader climbers and groundsmen to small firms working Saltwells, Wren's Nest and the Black Country urban woodland, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear the Black Country's trees",
  "s1loc":[
   "Dudley sits at the heart of the Black Country, a busy West Midlands borough threaded with street, park and garden trees and pockets of ancient woodland, and managing that urban forest keeps a steady community of arborists and tree surgeons busy across the town and the wider conurbation. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the borough's green geography. Suburbs like Woodside, Sedgley and Gornal carry mature garden and street trees, while Saltwells National Nature Reserve with its ancient Saltwells Wood, the limestone slopes and woodland of Wren's Nest and the Capability Brown parkland at Himley Hall hold woodland and estate trees, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Dudley tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and ash dieback in the borough's mixed oak and ash woodland alongside the council's urban forest and woodland grant work keeps the felling and safety jobs coming. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "And the firms are mostly small: a climber and a groundsman, a family business, a one or two-van outfit working across Dudley, Stourbridge and the wider Black Country patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the borough's gardens, parks and Black Country woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Dudley's parks, nature reserves and Black Country woodland",
 },
 "norwich": {
  "region":"Norwich and Norfolk",
  "nearby":["Ipswich", "Cambridge", "Colchester"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Norwich, from sole-trader climbers and groundsmen to small firms working Mousehold Heath, Whitlingham Country Park and the wider Norfolk woodland, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Norfolk's trees",
  "s1loc":[
   "A fine city wrapped in mature street, park and garden trees, Norwich keeps a busy community of arborists and tree surgeons working across the city and the surrounding Norfolk countryside. Most are sole traders and small teams handling domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the city's leafy geography. Sought-after suburbs like Eaton, Cringleford and the Golden Triangle around Unthank Road and Newmarket Road carry mature oak, beech and the trees of grand Victorian and Edwardian gardens, while Mousehold Heath, Whitlingham Country Park, Lion Wood and the broadleaf woodland on the city's fringe hold parkland and ancient cover, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Norwich tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and ash dieback across Norfolk's heavy ash population keeps felling and roadside clearance work steady. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "These are small outfits for the most part: a climber and a groundsman, a family business, a one or two-van team working across Norwich, Wymondham and the wider Norfolk patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the city's gardens, parks and Norfolk woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Norwich's gardens, heaths and Norfolk woodland",
 },
 "swindon": {
  "region":"Swindon and Wiltshire",
  "nearby":["Chippenham", "Newbury", "Oxford"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Swindon, from sole-trader climbers and groundsmen to small firms working Coate Water, Stanton Country Park and the Great Western Community Forest, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Wiltshire's trees",
  "s1loc":[
   "Ringed by the chalk of the Wiltshire Downs and a growing belt of new and ancient woodland, Swindon keeps a steady community of arborists and tree surgeons working across the town and the surrounding country. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the town's leafy geography. Areas like Old Town around the Town Gardens, Wroughton and Highworth carry mature garden and street trees, while Coate Water Country Park, Stanton Country Park, Stratton Wood and the wider Great Western Community Forest, now part of the new Western Forest, hold parkland and broadleaf woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Swindon tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and ash dieback across Wiltshire's ash keeps roadside and woodland felling steady. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "And the firms tend to be small: a climber and a groundsman, a family business, a one or two-van outfit working across Swindon, Marlborough and the wider Wiltshire patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's gardens, parks and Wiltshire woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Swindon's gardens, country parks and Great Western Community Forest woodland",
 },
 "croydon": {
  "region":"Croydon and South London",
  "nearby":["Sutton", "Bromley", "Epsom"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Croydon, from sole-trader climbers and groundsmen to small firms working Selsdon Wood, Lloyd Park and the Addington Hills, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear South London's trees",
  "s1loc":[
   "Greener than its town centre suggests, Croydon holds over a hundred parks and open spaces and a large estate of mature street, park and garden trees, and managing it keeps a big community of arborists and tree surgeons busy across the borough and the North Downs fringe. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the borough's leafy geography. Suburbs like Sanderstead, Selsdon, Purley and the Webb Estate and Upper Woodcote Village carry mature oak, beech and estate trees, while Selsdon Wood, Lloyd Park, Coombe Wood and the heathland and woodland of the Addington Hills and Shirley Hills hold parkland and ancient cover, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Croydon tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and the borough's dense web of Tree Preservation Orders and conservation areas shapes much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "These are small outfits in the main: a climber and a groundsman, a family business, a one or two-van team working across Croydon, Purley and the wider South London patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the borough's gardens, parks and South London woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Croydon's gardens, parks and Addington Hills woodland",
 },
 "bournemouth": {
  "region":"Bournemouth and Dorset",
  "nearby":["Poole", "Christchurch", "Ferndown"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Bournemouth, from sole-trader climbers and groundsmen to small firms working the pine-clad chines, Meyrick Park and the wider Dorset woodland, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Dorset's trees",
  "s1loc":[
   "Defined by tall maritime pines, wooded chines and a large estate of mature street, park and garden trees, Bournemouth keeps a busy community of arborists and tree surgeons working across the town and the surrounding Dorset coast. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the town's leafy geography. Suburbs like Talbot Woods, Branksome Park and Canford Cliffs carry mature pine, oak and beech, while Alum Chine, Branksome Chine, Meyrick Park, the Central and Coy Pond Gardens with their Pine Walk and the heathland of Hengistbury Head hold parkland and wooded valleys, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Bournemouth tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and ash dieback across Dorset alongside the care of the town's protected pines keeps felling and reduction work steady. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "And the firms are mostly small: a climber and a groundsman, a family business, a one or two-van outfit working across Bournemouth, Poole and the wider Dorset patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's gardens, chines and Dorset woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Bournemouth's gardens, pine-clad chines and Dorset woodland",
 },
 "southend-on-sea": {
  "region":"Southend-on-Sea and Essex",
  "nearby":["Basildon", "Rayleigh", "Canvey Island"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Southend-on-Sea, from sole-trader climbers and groundsmen to small firms working Belfairs Wood, Hadleigh Great Wood and the wider Essex woodland, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear south Essex's trees",
  "s1loc":[
   "Set above the Thames Estuary with a surprising stock of ancient woodland on its doorstep, Southend-on-Sea keeps a steady community of arborists and tree surgeons working across the city and the surrounding south Essex country. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the area's leafy geography. Suburbs like Leigh-on-Sea, Thorpe Bay and Chalkwell carry mature garden and street trees, while Belfairs Wood, Hadleigh Great Wood and Dodd's Grove SSSI, Belfairs Park and the slopes of Belton Hills hold parkland and ancient coppiced oak woodland, some of it among the oldest recorded in Essex, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Southend tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and ash dieback across the Essex woods keeps felling and roadside clearance steady. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "These are small outfits for the most part: a climber and a groundsman, a family business, a one or two-van team working across Southend, Rayleigh and the wider south Essex patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the area's gardens, parks and Essex woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Southend's gardens, parks and Belfairs woodland",
 },
 "walsall": {
  "region":"Walsall and the Black Country",
  "nearby":["Bloxwich", "Wednesbury", "West Bromwich"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Walsall, from sole-trader climbers and groundsmen to small firms working the borough's leafy suburbs, parks and Black Country woodland, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear the Black Country's trees",
  "s1loc":[
   "Walsall sits at the green edge of the Black Country, carrying a big estate of mature street, park and garden trees, and managing it keeps a steady community of arborists and tree surgeons busy across the borough and into the wider West Midlands. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the borough's leafy geography. Suburbs like Aldridge, Streetly and Pelsall carry mature oak, beech and estate trees, while Walsall Arboretum, now the West Midlands' first designated Ancient Tree Site with around 130 veteran trees, along with Barr Beacon and the woodland fringing nearby Sutton Park, hold parkland and ancient timber, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Walsall tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and the borough's veteran trees plus the ongoing ash dieback clearance across the Black Country shape much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Most of these outfits stay small: a climber and a groundsman, a family business, a one or two-van crew working across Walsall, Aldridge and the surrounding West Midlands patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the borough's gardens, parks and Black Country woodland",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Walsall's leafy suburbs, the Arboretum and Black Country woodland",
 },
 "warrington": {
  "region":"Warrington and the Cheshire-Merseyside border",
  "nearby":["Widnes", "Runcorn", "St Helens"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Warrington, from sole-trader climbers and groundsmen to small firms working the town's leafy villages, parks and Mersey Forest woodland, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Cheshire's trees",
  "s1loc":[
   "Straddling the Cheshire and Merseyside border, Warrington carries a large estate of mature street, park and garden trees, and managing it keeps a busy community of arborists and tree surgeons working across the town and out into the wider North West. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the town's leafy geography. Villages like Stockton Heath, Appleton, Grappenhall and Lymm carry mature oak, beech and estate trees, while Walton Hall Gardens, Birchwood Forest Park, Gorse Covert Mounds and the wider Mersey Forest hold parkland and community woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Warrington tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and the young Mersey Forest plantations plus ongoing ash dieback clearance shape much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "The firms themselves are mostly small: a climber and a groundsman, a family business, a one or two-van outfit working across Warrington, Lymm and the surrounding Cheshire and Merseyside patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's gardens, parks and Mersey Forest woodland",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Warrington's leafy villages, parks and Mersey Forest woodland",
 },
 "slough": {
  "region":"Slough and Berkshire",
  "nearby":["Maidenhead", "Windsor", "Uxbridge"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Slough, from sole-trader climbers and groundsmen to small firms working the town's leafy suburbs, parks and Berkshire woodland, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Berkshire's trees",
  "s1loc":[
   "West of London on the Berkshire and Buckinghamshire edge, Slough carries a large estate of mature street, park and garden trees, and managing it keeps a steady community of arborists and tree surgeons busy across the town and the surrounding Thames Valley. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the town's leafy geography. Suburbs and villages like Upton, Langley, Stoke Poges and Datchet carry mature oak, beech and estate trees, while Upton Court Park, Salt Hill Park, Langley Park and the ancient pollarded beeches of Burnham Beeches and Black Park nearby hold parkland and old woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Slough tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and the veteran pollards around Burnham Beeches plus tight conservation-area and TPO rules shape much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Out here the firms tend to stay small: a climber and a groundsman, a family business, a one or two-van outfit working across Slough, Windsor and the wider Berkshire patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's gardens, parks and Berkshire woodland",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Slough's leafy suburbs, parks and Berkshire woodland",
 },
 "huddersfield": {
  "region":"Huddersfield and West Yorkshire",
  "nearby":["Dewsbury", "Halifax", "Brighouse"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Huddersfield, from sole-trader climbers and groundsmen to small firms working the town's leafy suburbs, parks and West Yorkshire woodland, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear the Pennine valleys' trees",
  "s1loc":[
   "Set in the Pennine foothills of West Yorkshire, Huddersfield carries a large estate of mature street, park, valley and garden trees, and managing it keeps a busy community of arborists and tree surgeons working across the town and the surrounding Kirklees countryside. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the town's leafy geography. Suburbs like Edgerton, Lindley and Almondbury carry mature oak, beech and former mill-owners' estate trees, while Beaumont Park, Greenhead Park, Gledholt Woods and the wooded slopes of the Holme and Colne Valleys around Castle Hill hold parkland and steep valley woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Huddersfield tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and the steep valley-side work plus ongoing ash dieback clearance across the Pennine slopes shape much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "By and large the firms stay small: a climber and a groundsman, a family business, a one or two-van outfit working across Huddersfield, Holmfirth and the wider West Yorkshire patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's gardens, parks and Pennine valley woodland",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Huddersfield's leafy suburbs, parks and Holme Valley woodland",
 },
 "telford": {
  "region":"Telford and Shropshire",
  "nearby":["Shrewsbury", "Wolverhampton", "Cannock"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Telford, from sole-trader climbers and groundsmen to small firms working the new town's leafy estates, parks and Shropshire woodland, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Shropshire's trees",
  "s1loc":[
   "Built as a Shropshire New Town and laced with green wedges and woodland from the start, Telford carries an unusually large estate of mature street, park and garden trees, and managing it keeps a steady community of arborists and tree surgeons busy across the town and the surrounding county. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the town's planted geography. Districts like Wellington, Madeley, Coalbrookdale and Oakengates carry mature oak, beech and estate trees, while the 170-hectare Telford Town Park, Apley Woods, Granville Country Park and the steep wooded slopes of the Ironbridge Gorge and the Wrekin hold parkland and ancient woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Telford tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and the new-town tree stock now maturing together plus ash dieback clearance across Shropshire shape much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "For the most part the firms are small: a climber and a groundsman, a family business, a one or two-van outfit working across Telford, Wellington and the wider Shropshire patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the new town's estates, parks and Shropshire woodland",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Telford's leafy estates, Town Park and Ironbridge Gorge woodland",
 },
 "newport": {
  "region":"Newport and South Wales",
  "nearby":["Cwmbran", "Pontypool", "Caerphilly"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Newport, from sole-trader climbers and groundsmen to small firms working the city's leafy suburbs, parks and the ancient woodland of Wentwood, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Gwent's trees",
  "s1loc":[
   "Newport sits in a green corner of South Wales, with a large estate of mature street, park and estate trees, and keeping it managed supports a busy community of arborists and tree surgeons across the city and the wider Gwent patch. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the city's leafy geography. Suburbs like Allt-yr-yn, whose name comes from the Welsh for a wooded slope of ash trees, along with Caerleon and Beechwood carry mature broadleaf and estate trees, while Tredegar Park, Belle Vue Park and Beechwood Park hold parkland and the ancient woodland of Wentwood rolls out to the north, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Newport tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with Natural Resources Wales and Coed Cymru shaping woodland management and ash dieback driving a steady run of ash felling across Allt-yr-yn and the valleys. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "The firms here are mostly small: a climber and a groundsman, a family business, a one or two-van outfit working across Newport, Cwmbran and the wider Gwent patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the city's gardens, parks and South Wales woodland work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Newport's gardens, parks and the ancient woodland of Wentwood",
 },
 "oxford": {
  "region":"Oxford and Oxfordshire",
  "nearby":["Abingdon", "Bicester", "Witney"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Oxford, from sole-trader climbers and groundsmen to small firms working the city's college grounds, parks and Oxfordshire woodland, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Oxfordshire's trees",
  "s1loc":[
   "Oxford is a city of dreaming spires and grand old trees, from college grounds and meadows to street and garden specimens, and managing that estate keeps a large community of arborists and tree surgeons busy across the city and Oxfordshire. Most are sole traders and small teams working domestic gardens, college and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the city's leafy geography. Suburbs like North Oxford, Summertown, Headington and Boars Hill carry mature street and garden trees, while Christ Church Meadow's cedars of Lebanon, the University Parks, the ancient woods of Shotover Country Park and Wytham Woods on the western edge hold parkland and woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Oxford tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and with so many veteran college and conservation-area trees under TPO the rules shape much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Behind the colleges, the firms are mostly small: a climber and a groundsman, a family business, a one or two-van outfit working across Oxford, Abingdon and the wider Oxfordshire patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the city's college grounds, parks and Oxfordshire woodland",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Oxford's college grounds, parks and Oxfordshire woodland",
 },
 "poole": {
  "region":"Poole and Dorset",
  "nearby":["Bournemouth", "Ferndown", "Christchurch"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Poole, from sole-trader climbers and groundsmen to small firms working the town's leafy suburbs, parks and Dorset woodland, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Dorset's trees",
  "s1loc":[
   "Poole spreads around its great natural harbour with a large estate of mature pine, street and garden trees, and keeping it managed supports a busy community of arborists and tree surgeons across the town and across Dorset. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the town's leafy geography. Affluent suburbs like Canford Cliffs, Branksome Park and Parkstone carry mature pine and broadleaf garden trees, while Upton Country Park, the chines running down to the shore and the National Trust woodland on Brownsea Island in the harbour hold parkland and woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Poole tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and with ash dieback across Dorset and BCP Council TPO and conservation-area consent shaping much of the work, where diseased ash often needs sectional dismantling rather than straight felling. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Around the harbour, the firms are mostly small: a climber and a groundsman, a family business, a one or two-van outfit working across Poole, Bournemouth and the wider Dorset patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's gardens, parks and Dorset woodland work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Poole's leafy suburbs, parks and Dorset woodland",
 },
 "dundee": {
  "region":"Dundee and Tayside",
  "nearby":["Perth", "Arbroath", "Glenrothes"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Dundee, from sole-trader climbers and groundsmen to small firms working the city's leafy suburbs, parks and the woodland of Camperdown and Templeton, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Tayside's trees",
  "s1loc":[
   "Dundee rises from the Firth of Tay across a line of wooded hills, with a large estate of mature park, street and garden trees, and managing it keeps a busy community of arborists and tree surgeons working across the city and Tayside. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the city's leafy geography. Suburbs like Broughty Ferry and West Ferry, set among stone walls and mature trees, carry grand Victorian garden specimens, while Camperdown Country Park, home of the original weeping Camperdown elm, along with Templeton Woods, Clatto and Balgay Hill with its wellingtonia and Irish yew hold parkland and woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Dundee tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with Forestry and Land Scotland and NatureScot shaping woodland management and storms like Arwen leaving a heavy run of windblow and dangerous-tree clearance. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Up on the wooded braes, the firms are mostly small: a climber and a groundsman, a family business, a one or two-van outfit working across Dundee, Perth and the wider Tayside patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the city's gardens, parks and Tayside woodland work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Dundee's leafy suburbs, parks and the woodland of Camperdown and Templeton",
 },
 "cambridge": {
  "region":"Cambridge and Cambridgeshire",
  "nearby":["Bedford", "Peterborough", "Bishop's Stortford"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Cambridge, from sole-trader climbers and groundsmen to small firms working the city's college grounds, parks and Cambridgeshire woodland, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Cambridgeshire's trees",
  "s1loc":[
   "Cambridge is a green and historic city, with college courts, the tree-lined Backs and a large estate of mature street and garden trees, and managing it keeps a busy community of arborists and tree surgeons working across the city and Cambridgeshire. Most are sole traders and small teams working domestic gardens, college and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the city's leafy geography. Leafy wards like Newnham carry the highest canopy cover in the city, the Backs run their avenues of limes and hornbeams, and Cherry Hinton Hall, Wandlebury Country Park up on the Gog Magog Hills and Coton Countryside Reserve hold parkland and woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Cambridge tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and with the City Council's Tree Team enforcing TPO and conservation-area consent across the city's many veteran college and street trees. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Beyond the colleges, the firms are mostly small: a climber and a groundsman, a family business, a one or two-van outfit working across Cambridge, Bedford and the wider Cambridgeshire patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the city's college grounds, parks and Cambridgeshire woodland",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Cambridge's college grounds, parks and Cambridgeshire woodland",
 },
 "york": {
  "region":"York and North Yorkshire",
  "nearby":["Harrogate", "Selby", "Knaresborough"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across York, from sole-trader climbers and groundsmen to small firms working the city's ancient Strays, riverside parks and North Yorkshire woodland near the old Forest of Galtres, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear York's trees",
  "s1loc":[
   "A walled city ringed by commons, parkland and river meadow, York carries a large estate of mature street, park and garden trees, and keeping it managed keeps a steady community of arborists and tree surgeons busy across the city and North Yorkshire. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the city's green geography. Conservation-area suburbs like Fulford, Heslington, Bishopthorpe and Dringhouses carry mature oak, beech and estate trees, while the ancient Strays of Knavesmire, Hob Moor and Walmgate Stray, plus Rowntree Park, the Museum Gardens and Strensall Common out toward the old Forest of Galtres, hold parkland and woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. York tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and TPO and conservation-area rules across the city shape much of the work, alongside ongoing ash dieback felling across the county. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "These are small outfits for the most part: a climber and a groundsman, a family business, a one or two-van team working across York, Tadcaster and the wider North Yorkshire patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the city's Strays, parks and woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across York's Strays, riverside parks and North Yorkshire woodland",
 },
 "blackpool": {
  "region":"Blackpool and the Fylde coast",
  "nearby":["Poulton-le-Fylde", "Thornton Cleveleys", "Lytham St Annes"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Blackpool, from sole-trader climbers and groundsmen to small firms working the Fylde coast's parks, leafy resort suburbs and Lancashire woodland from Stanley Park to Witch Wood, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear the Fylde coast's trees",
  "s1loc":[
   "Set on an exposed peninsula between the Wyre and the Ribble, Blackpool and the wider Fylde coast carry a salt-tested estate of street, park and garden trees, and managing them keeps a community of arborists and tree surgeons busy across the resort and Lancashire. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the coast's geography. Leafy suburbs like Bispham, Norbreck, Marton and Stanley Park's surrounds carry mature trees, while Stanley Park itself, Marton Mere, Witch Wood at Lytham St Annes and the old Great Wood of Lytham Hall hold parkland and woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for firms across Poulton-le-Fylde, Thornton Cleveleys and the Fylde.",
   "It is a safety-critical trade run to recognised standards. Fylde tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and exposed-coast wind loading and storm-damaged limbs drive a lot of urgent work, after a fatal falling-branch incident in high winds put tree safety in the local spotlight. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Outfits here run small: a climber and a groundsman, a family business, a one or two-van team working across Blackpool, Fleetwood and the wider Fylde coast. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the coast's parks, suburbs and woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Blackpool's parks, resort suburbs and Fylde coast woodland",
 },
 "ipswich": {
  "region":"Ipswich and Suffolk",
  "nearby":["Colchester", "Chelmsford", "Norwich"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Ipswich, from sole-trader climbers and groundsmen to small firms working the town's leafy suburbs, Victorian parks and Suffolk woodland around Christchurch and Holywells, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Suffolk's trees",
  "s1loc":[
   "A county town wrapped around the Orwell estuary, Ipswich holds a large estate of mature street, park and garden trees, and managing it keeps a community of arborists and tree surgeons busy across the town and Suffolk. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the town's leafy geography. Conservation-area suburbs carry mature oak, beech and estate trees, while Christchurch Park, with its veteran yew, pollarded sweet chestnuts and oaks among more than four thousand trees, plus Holywells Park and the Orwell-side woodlands, hold parkland and woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Ipswich tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members or ARB Approved Contractors, and with so much of the town a conservation area or under TPO, six-week notice and consent shape much of the work, alongside steady ash dieback felling across Suffolk. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "The firms are mostly small here too: a climber and a groundsman, a family business, a one or two-van team working across Ipswich, Woodbridge and the wider Suffolk patch toward Colchester. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's parks, suburbs and Suffolk woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Ipswich's leafy suburbs, Victorian parks and Suffolk woodland",
 },
 "middlesbrough": {
  "region":"Middlesbrough and Teesside",
  "nearby":["Stockton-on-Tees", "Redcar", "Guisborough"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Middlesbrough, from sole-trader climbers and groundsmen to small firms working the town's parks, leafy southern suburbs and Teesside woodland from Stewart Park to the Eston Hills, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Teesside's trees",
  "s1loc":[
   "Sitting between the Tees and the North York Moors, Middlesbrough carries a varied estate of street, park and garden trees, and managing it keeps a steady community of arborists and tree surgeons busy across Teesside. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the town's green southern edge. Leafy suburbs like Marton, Nunthorpe, Acklam and Linthorpe carry mature trees, while Stewart Park with its mature woodland and arboretum, Albert Park, Flatts Lane Country Park and the wooded slopes of the Eston Hills hold parkland and woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for firms across Stockton-on-Tees, Redcar and Guisborough.",
   "It is a safety-critical trade run to recognised standards. Teesside tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, with established Arboricultural Association Approved Contractors on the patch, and ash dieback clearance across the county woodlands drives a steady run of felling. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Most are small outfits: a climber and a groundsman, a family business, a one or two-van team working across Middlesbrough, Ingleby Barwick and the wider Teesside patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's parks, suburbs and Teesside woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Middlesbrough's parks, leafy suburbs and Eston Hills woodland",
 },
 "gloucester": {
  "region":"Gloucester and Gloucestershire",
  "nearby":["Cheltenham", "Worcester", "Bristol"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Gloucester, from sole-trader climbers and groundsmen to small firms working the city's leafy suburbs, country parks and Gloucestershire woodland from Robinswood Hill to the Forest of Dean, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Gloucestershire's trees",
  "s1loc":[
   "A cathedral city on the Severn at the edge of the Forest of Dean, Gloucester holds a large estate of mature street, park and garden trees, and managing it keeps a community of arborists and tree surgeons busy across the city and Gloucestershire. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the city's leafy geography. Suburbs like Tuffley, Hucclecote, Barnwood and Abbeydale carry mature oak, beech and estate trees, while Robinswood Hill Country Park with its meadows, orchards and woodland, the Barnwood Arboretum, Highnam Woods and the wider Forest of Dean hold parkland and woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Gloucester tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and large-scale ash dieback felling across Gloucestershire, with the disease fatal to most native ash, drives a heavy run of work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "The firms here run small: a climber and a groundsman, a family business, a one or two-van team working across Gloucester, Quedgeley and the wider Gloucestershire patch toward Cheltenham. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the city's suburbs, country parks and Gloucestershire woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Gloucester's leafy suburbs, country parks and Forest of Dean woodland",
 },
 "exeter": {
  "region":"Exeter and Devon",
  "nearby":["Exmouth", "Tiverton", "Newton Abbot"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Exeter, from sole-trader climbers and groundsmen to small firms working the city's valley parks, leafy suburbs and the wooded Exe valley, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Devon's trees",
  "s1loc":[
   "Exeter is a green city ringed by river valleys and woodland, and keeping that estate of street, park and estuary trees in order keeps a steady community of arborists and tree surgeons busy across the city and the wider Devon patch. Most are sole traders and small teams working domestic gardens, council and valley-park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the city's leafy geography. Suburbs like St Leonard's, Pennsylvania, Heavitree and Topsham carry mature oak, beech and garden trees, while Riverside Valley Park, Ludwell Valley Park, the Exe estuary and Stoke Woods to the north hold parkland and woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Exeter tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and ash dieback across the valley parks and Devon's wider treescape is driving a steady programme of fells and safety work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "The firms here tend to be small: a climber and a groundsman, a family business, a one or two-van outfit working across Exeter, Exmouth and the wider Devon patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the city's gardens, valley parks and woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Exeter's gardens, valley parks and the wooded Exe valley",
 },
 "solihull": {
  "region":"Solihull and the West Midlands",
  "nearby":["Redditch", "Sutton Coldfield", "Coventry"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Solihull, from sole-trader climbers and groundsmen to small firms working the borough's leafy suburbs, parks and the wooded Arden countryside, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Arden's trees",
  "s1loc":[
   "Set in the old Forest of Arden, Solihull is one of the leafiest boroughs in the West Midlands, and its large estate of mature street, park and garden trees keeps a busy community of arborists and tree surgeons working across the borough and beyond. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the borough's leafy geography. Suburbs and villages like Knowle, Dorridge, Solihull Lodge and Balsall Common carry mature oak, ash and estate trees, while Brueton Park, Elmdon Park, Dorridge Wood and the River Blythe and Grand Union Canal corridors hold parkland and woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Solihull tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and with ash among the borough's most dominant species, ash dieback is driving a steady run of fells and safety work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "The firms here tend to be small: a climber and a groundsman, a family business, a one or two-van outfit working across Solihull, Knowle and the wider West Midlands patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the borough's gardens, parks and Arden woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Solihull's gardens, parks and the wooded Arden countryside",
 },
 "colchester": {
  "region":"Colchester and Essex",
  "nearby":["Ipswich", "Chelmsford", "Brentwood"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Colchester, from sole-trader climbers and groundsmen to small firms working the city's leafy suburbs, parks and Essex woodland, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Essex's trees",
  "s1loc":[
   "Colchester carries a big estate of mature street, park and garden trees across Britain's oldest recorded town, and managing it keeps a steady community of arborists and tree surgeons busy across the city and the wider Essex patch. Most are sole traders and small teams working domestic gardens, council and country-park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the city's leafy geography. Areas like Lexden, Mile End, Greenstead and Stanway carry mature oak, ash and garden trees, while Castle Park, High Woods Country Park, Hilly Fields and the river corridors towards Dedham Vale hold parkland and woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Colchester tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and the council runs a programme of arboricultural works off its tree hazard risk assessments while ash dieback drives steady fells across the area. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Most of the firms here are small: a climber and a groundsman, a family business, a one or two-van outfit working across Colchester, Ipswich and the wider Essex patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the city's gardens, parks and country-park tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Colchester's gardens, parks and Essex woodland",
 },
 "cheltenham": {
  "region":"Cheltenham and Gloucestershire",
  "nearby":["Gloucester", "Worcester", "Evesham"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Cheltenham, from sole-trader climbers and groundsmen to small firms working the town's leafy parks, Regency suburbs and the Cotswold escarpment woodland, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear the Cotswold edge",
  "s1loc":[
   "A leafy Regency spa town sitting under the Cotswold escarpment, Cheltenham carries a large estate of mature street, park and garden trees, and looking after it keeps a steady community of arborists and tree surgeons busy across the town and the surrounding Gloucestershire hills. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the town's leafy geography. Districts like Pittville, Montpellier, Charlton Kings and Leckhampton carry mature beech, oak and garden trees, while Pittville Park, Leckhampton Hill, Crickley Hill and Cleeve Common on the Cotswolds AONB escarpment hold parkland and beech woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Cheltenham tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and with ash dieback reaching Leckhampton Hill and Benhall Woods the borough is running steady inspection and felling work on its escarpment ash. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Most of the firms here are small: a climber and a groundsman, a family business, a one or two-van outfit working across Cheltenham, Gloucester and the wider Cotswolds patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's gardens, parks and Cotswold escarpment tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Cheltenham's gardens, parks and the Cotswold escarpment",
 },
 "gateshead": {
  "region":"Gateshead and Tyne and Wear",
  "nearby":["Newcastle upon Tyne", "Washington", "Chester-le-Street"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Gateshead, from sole-trader climbers and groundsmen to small firms working the borough's parks, leafy suburbs and the wooded Derwent valley, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear the North East's trees",
  "s1loc":[
   "Gateshead runs from Victorian parkland down into the steep, wooded Derwent valley, and keeping that estate of street, park and woodland trees in order keeps a busy community of arborists and tree surgeons working across the borough and the wider Tyne and Wear patch. Most are sole traders and small teams working domestic gardens, council and country-park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the borough's leafy geography. Areas like Low Fell, Whickham, Rowlands Gill and Sunniside carry mature oak, beech and garden trees, while Saltwell Park, the Derwent Walk Country Park, Derwenthaugh Park and the Land of Oak and Iron ancient woodland hold parkland and woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Gateshead tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and Storm Arwen, which drove unusual north-easterly gusts near 100mph and flattened trees across the North East in 2021, left a long tail of windblow and dangerous-tree clearance on top of ongoing ash dieback work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Most of the firms here are small: a climber and a groundsman, a family business, a one or two-van outfit working across Gateshead, Newcastle and the wider Tyne and Wear patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the borough's gardens, parks and Derwent valley woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Gateshead's parks, suburbs and the wooded Derwent valley",
 },
 "high wycombe": {
  "region":"High Wycombe and the Buckinghamshire Chilterns",
  "nearby":["Aylesbury", "Maidenhead", "Slough"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across High Wycombe, from sole-trader climbers and groundsmen to small firms working the town's Chiltern beechwoods, parks and Hughenden valley woodland, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear the Chilterns' trees",
  "s1loc":[
   "Set in the Wye valley and ringed by the Chiltern Hills, High Wycombe sits in one of the most heavily wooded landscapes in England, and managing that tree cover keeps a steady community of arborists and tree surgeons busy across the town and the wider Buckinghamshire Chilterns. Most are sole traders and small teams working domestic gardens, council and estate contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the town's leafy geography. Suburbs and villages like Hazlemere, Tylers Green, Downley, Terriers and Flackwell Heath carry mature beech, oak and estate trees, while Hughenden Park and the National Trust valley at Hughenden Manor, Naphill Common and the Chilterns beechwoods hold parkland and ancient woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. High Wycombe tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with ageing Chiltern beech and ash dieback shaping a lot of the felling and deadwooding. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Most of these outfits are small by design: a climber and a groundsman, a family business, a one or two-van crew working across High Wycombe, Marlow and the wider Chilterns patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's Chiltern beechwoods, parks and valley tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across High Wycombe's Chiltern beechwoods, parks and Hughenden valley woodland",
 },
 "blackburn": {
  "region":"Blackburn and Lancashire",
  "nearby":["Darwen", "Accrington", "Burnley"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Blackburn, from sole-trader climbers and groundsmen to small firms working the town's parks, country park woodland and the edge of the West Pennine Moors, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Lancashire's trees",
  "s1loc":[
   "Sitting on the edge of the West Pennine Moors, Blackburn carries a large estate of mature park, street and estate trees, and keeping it managed gives a steady community of arborists and tree surgeons plenty to do across the town and the wider Lancashire patch. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the town's green geography. Witton Country Park carries close to 480 acres of mixed woodland, parkland and rough grassland on the moorland fringe, while Corporation Park, Sunnyhurst Wood over towards Darwen and the wider West Pennine Moors hold parkland and woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Blackburn tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and with ash dieback present across almost all of Lancashire it drives a heavy load of roadside felling and clearance. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "These are mostly small outfits: a climber and a groundsman, a family business, a one or two-van crew working across Blackburn, Darwen and the wider West Pennine patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's parks, country park and moorland-edge tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Blackburn's parks, country park woodland and the edge of the West Pennine Moors",
 },
 "maidstone": {
  "region":"Maidstone and Kent",
  "nearby":["Chatham", "Rochester", "Tonbridge"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Maidstone, from sole-trader climbers and groundsmen to small firms working the town's parks, nature reserves and the wooded Kent Downs of the Garden of England, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear the Garden of England's trees",
  "s1loc":[
   "As the county town of Kent and the heart of the Garden of England, Maidstone sits among some of the most wooded countryside in Britain, and managing that tree cover keeps a busy community of arborists and tree surgeons working across the town and the wider Kent patch. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the town's leafy geography. Suburbs like Bearsted, Penenden Heath and Weavering carry mature oak, ash and estate trees, while Mote Park's 450 acres of parkland, Vinters Valley Nature Reserve and the ancient woodland of the Kent Downs around Hucking hold parkland and woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "The work also tracks the area's watered, wooded grain. The River Len threads down toward the Medway while the Loose Stream runs through the Loose Valley Conservation Area to meet it at Tovil, both lined with oak, ash and sweet chestnut. North of the town, Cobtree Manor Park preserves the old Tyrwhitt-Drake estate parkland, where Hilliers laid out an arboretum of some six hundred species in the 1970s. Westward, the hop-pole sweet chestnut coppice of Mereworth Woods carries the distinctive west Kent pattern, while the deer park at Boughton Monchelsea Place, set on the ragstone Quarry Hills, frames its drive with chestnut coppice and mature beech. East of the town, Leeds Castle sits within some 345 acres of parkland and woodland whose veteran cedars, beeches and oaks have suffered notable storm losses. Such estate, valley and coppice trees keep generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Maidstone tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with ash dieback across the Kent Downs hornbeam and ash woodland driving a lot of the felling and clearance. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "The firms behind this work are mostly small: a climber and a groundsman, a family business, a one or two-van crew working across Maidstone, the Medway towns and the wider Kent Downs patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's parks, nature reserves and Kent Downs tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Maidstone's parks, nature reserves and the wooded Kent Downs",
 },
 "basingstoke": {
  "region":"Basingstoke and Hampshire",
  "nearby":["Andover", "Newbury", "Fleet"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Basingstoke, from sole-trader climbers and groundsmen to small firms working the town's parks, country woodland and the ancient forests of north Hampshire, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Hampshire's trees",
  "s1loc":[
   "Ringed by the chalk downs and ancient woodland of north Hampshire, Basingstoke carries a large estate of mature park, street and estate trees, and managing it keeps a steady community of arborists and tree surgeons busy across the town and the wider county. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the town's green geography. Suburbs and districts like Chineham, Hatch Warren, Kempshott, Old Basing and Brighton Hill carry mature oak, beech and estate trees, while Eastrop Park along the River Loddon, the War Memorial Park, Basing Wood and the ancient oak woodland of Pamber Forest hold parkland and woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Basingstoke tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with ash dieback and ageing estate oaks shaping a lot of the felling and deadwooding. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Behind all this are mostly small outfits: a climber and a groundsman, a family business, a one or two-van crew working across Basingstoke, Old Basing and the wider north Hampshire patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's parks, country woodland and Hampshire forest tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Basingstoke's parks, country woodland and the ancient forests of north Hampshire",
 },
 "crawley": {
  "region":"Crawley and West Sussex",
  "nearby":["Horsham", "East Grinstead", "Haywards Heath"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Crawley, from sole-trader climbers and groundsmen to small firms working the town's parks, country park woodland and the High Weald forests of St Leonard's and Tilgate, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear the High Weald's trees",
  "s1loc":[
   "On the doorstep of the High Weald National Landscape and ringed by old forest, Crawley carries a large estate of mature park, street and estate trees, and managing it keeps a steady community of arborists and tree surgeons busy across the town and the wider West Sussex patch. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the town's wooded geography. Neighbourhoods like Pound Hill, Tilgate, Three Bridges and Maidenbower carry mature oak, beech and estate trees, while Tilgate Park and its country park, the Forestry-managed Tilgate Forest, St Leonard's Forest and Buchan Country Park hold parkland and ancient Wealden woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Crawley tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with storm damage and ash dieback across the High Weald oak and conifer woodland driving a lot of the clearance. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "The firms that do this are mostly small: a climber and a groundsman, a family business, a one or two-van crew working across Crawley, Horsham and the wider High Weald patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's parks, country park and High Weald forest tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Crawley's parks, country park woodland and the High Weald forests of St Leonard's and Tilgate",
 },
 "walthamstow": {
  "region":"Walthamstow and Waltham Forest",
  "nearby":["Ilford", "Enfield", "Loughton"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Walthamstow, from sole-trader climbers and groundsmen to small firms working Epping Forest, Walthamstow Forest and the borough's leafy hornbeam and oak suburbs, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews who climb and clear north-east London's trees",
  "s1loc":[
   "Tucked against Epping Forest, Walthamstow is a green corner of north-east London with a heavy load of mature street, park and ancient woodland trees, and looking after it keeps a busy community of arborists and tree surgeons working across Waltham Forest. The bulk are sole traders and small teams on domestic gardens, council and park contracts and storm clearance, and not one of them works a saw without proper chainsaw PPE.",
   "The work tracks the borough's leafy geography. Suburbs like Highams Park, Hale End and Chingford carry mature hornbeam, oak and estate trees, while Walthamstow Forest, Lloyd Park, Larks Wood and the City of London's wider Epping Forest hold ancient pollards and parkland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Walthamstow tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with TPO and conservation-area rules and ash dieback both shaping the workload. Every chainsaw job, on the ground or roped into an old hornbeam canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Most of these outfits are small by nature: a climber and a groundsman, a family business, a one or two-van team covering Walthamstow, Leyton, Chingford and out to the Epping Forest edge. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the borough's gardens, parks and ancient forest tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Walthamstow's gardens, Epping Forest edge and hornbeam woodland",
 },
 "basildon": {
  "region":"Basildon and Essex",
  "nearby":["Wickford", "Billericay", "Rayleigh"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Basildon, from sole-trader climbers and groundsmen to small firms working Langdon Hills, Norsey Wood and the borough's wooded ridges, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear the Essex tree line",
  "s1loc":[
   "For a post-war new town, Basildon sits in a surprisingly wooded patch of south Essex, ringed by ancient woodland and country park ridges, and managing that tree estate keeps a steady community of arborists and tree surgeons in work across the borough. Most are sole traders and small teams on domestic gardens, council and park contracts and storm clearance, and every one of them leans on proper chainsaw PPE.",
   "The work follows the borough's green geography. Langdon Hills Country Park, with the ancient woods of Marks Hill, Lincewood and Longwood, runs along the southern ridge, while Norsey Wood at Billericay carries SSSI sweet chestnut coppice and old oak, and leafier Billericay and Rayleigh streets hold mature garden trees, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Basildon tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with Billericay's conservation-area trees, borough TPOs and ash dieback all driving work. Every chainsaw job, on the ground or roped into a chestnut coppice canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "These are mostly small outfits: a climber and a groundsman, a family business, a one or two-van team working Basildon, Wickford, Billericay and the Rayleigh patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the borough's gardens, country parks and woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Basildon's gardens, Langdon Hills ridge and ancient Essex woodland",
 },
 "dartford": {
  "region":"Dartford and Kent",
  "nearby":["Gravesend", "Erith", "Sidcup"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Dartford, from sole-trader climbers and groundsmen to small firms working Joyden's Wood, the Darent valley and the North Downs woodland edge, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews who climb and clear the Darent valley's trees",
  "s1loc":[
   "Strung between the North Downs and the Thames on the Kent and south-east London edge, Dartford carries a mix of ancient woodland, river-valley and suburban trees, and keeping that estate safe keeps a busy community of arborists and tree surgeons working across the borough. Most are sole traders and small teams on domestic gardens, council and park contracts and storm clearance, all of them dependent on proper chainsaw PPE.",
   "The work follows the borough's geography. Joyden's Wood at Wilmington holds ancient woodland with pine and broadleaves, Darenth Country Park sits above the Darent valley on the North Downs edge, and Central Park runs along the river, while leafier Wilmington and Hawley streets carry mature garden trees, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Dartford tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with borough TPOs, conservation-area rules and ash dieback across Kent all shaping the work. Every chainsaw job, on the ground or roped into a North Downs canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "The firms are mostly small: a climber and a groundsman, a family business, a one or two-van outfit working Dartford, Wilmington, Stone and the Gravesend and Sidcup edge. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the borough's gardens, river valley and woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Dartford's gardens, Darent valley and North Downs woodland",
 },
 "bedford": {
  "region":"Bedford and Bedfordshire",
  "nearby":["Kempston", "Rushden", "Luton"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Bedford, from sole-trader climbers and groundsmen to small firms working the Forest of Marston Vale, Putnoe Wood and the town's parks and estates, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Bedfordshire's trees",
  "s1loc":[
   "Set on the Great Ouse at the heart of the Forest of Marston Vale, Bedford has a growing estate of street, park and young community-forest trees alongside older ancient woodland, and managing it keeps a steady community of arborists and tree surgeons busy across the town and Bedfordshire. Most are sole traders and small teams on domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the town's geography. Suburbs like Putnoe, Brickhill and Goldington carry mature oak and estate trees, Putnoe Wood and Mowsbury Park hold ancient woodland and hillfort planting, and the wider Forest of Marston Vale, running south-west towards Kempston and the M1, brings millions of new trees into management, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Bedford tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with borough TPOs, conservation-area rules and ash dieback in the local oak and ash woods all shaping the work. Every chainsaw job, on the ground or roped into a Putnoe Wood canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Mostly these are small outfits: a climber and a groundsman, a family business, a one or two-van team working Bedford, Kempston and out across the Marston Vale and Bedfordshire patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's gardens, community forest and woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Bedford's gardens, Marston Vale forest and ancient woodland",
 },
 "doncaster": {
  "region":"Doncaster and South Yorkshire",
  "nearby":["Mexborough", "Pontefract", "Maltby"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Doncaster, from sole-trader climbers and groundsmen to small firms working Sandall Beat Wood, Brodsworth's estate woods and the borough's parks, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews who climb and clear South Yorkshire's trees",
  "s1loc":[
   "Spread across a big slice of South Yorkshire, Doncaster holds a large estate of street, park, estate and council-managed woodland trees, and looking after it keeps a busy community of arborists and tree surgeons working across the borough. Most are sole traders and small teams on domestic gardens, council and park contracts and storm clearance, and not one of them works a saw without proper chainsaw PPE.",
   "The work follows the borough's geography. Sandall Beat Wood, an SSSI and Local Nature Reserve, and Sandall Park sit on the town's edge, the Brodsworth Hall estate and the Don Gorge at Sprotbrough carry mature woodland, and leafier Bessacarr, Sprotbrough and Tickhill hold estate and garden trees, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Doncaster tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with the council managing dozens of woodlands and Chalara ash dieback driving plenty of felling work. Every chainsaw job, on the ground or roped into a Sandall Beat canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "The firms are mostly small: a climber and a groundsman, a family business, a one or two-van outfit working Doncaster, Mexborough, Conisbrough and the wider South Yorkshire patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the borough's gardens, parks and woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Doncaster's gardens, parks and South Yorkshire woodland",
 },
 "worthing": {
  "region":"Worthing and West Sussex",
  "nearby":["Littlehampton", "Lancing", "Shoreham-by-Sea"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Worthing, from sole-trader climbers and groundsmen to small firms working Highdown, Titnore Wood and the South Downs above the town, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews who climb and clear the Sussex coast's trees",
  "s1loc":[
   "Tucked between the sea and the South Downs, Worthing is a green seaside town with a large estate of mature street, garden and downland trees, and keeping it managed supports a busy community of arborists and tree surgeons along the West Sussex coast. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the town's leafy geography. Suburbs like Tarring, Broadwater, High Salvington and Goring carry mature oak, beech and estate trees, while Highdown Gardens, Beach House Park, Titnore Wood, Cissbury Ring and the Worthing Downland Estate hold parkland and ancient woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Worthing tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and ash dieback felling at sites like The Sanctuary in High Salvington and The Gallops in Findon Valley keeps the saws busy, alongside TPO and South Downs conservation-area rules. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Mostly these are small outfits: a climber and a groundsman, a family business, a one or two-van team working across Worthing, Littlehampton and the wider West Sussex coastal plain. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's gardens, parks and downland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Worthing's gardens, parks and South Downs woodland",
 },
 "rotherham": {
  "region":"Rotherham and South Yorkshire",
  "nearby":["Maltby", "Mexborough", "Barnsley"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Rotherham, from sole-trader climbers and groundsmen to small firms working the Wentworth estate, Clifton Park and the wooded Dearne and Don valleys, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear South Yorkshire's trees",
  "s1loc":[
   "Set in the wooded valleys of the Don and the Dearne, Rotherham carries a large estate of mature park, street and country-estate trees, and managing it keeps a steady community of arborists and tree surgeons busy across South Yorkshire. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the town's leafy geography. Suburbs like Wickersley, Greasbrough, Brecks and Whiston carry mature oak, beech and estate trees, while the Wentworth Woodhouse estate with its plantations, Clifton Park, Boston Park, Ulley and Thrybergh Country Parks hold parkland and woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Rotherham tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and ash dieback across the borough's woodlands keeps the saws busy alongside TPO and conservation-area rules. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Mostly these are small outfits: a climber and a groundsman, a family business, a one or two-van team working across Rotherham, Maltby and the wider South Yorkshire patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the borough's gardens, parks and estate woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Rotherham's parks, estates and Dearne valley woodland",
 },
 "mansfield": {
  "region":"Mansfield and Nottinghamshire",
  "nearby":["Sutton-in-Ashfield", "Hucknall", "Worksop"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Mansfield, from sole-trader climbers and groundsmen to small firms working Berry Hill Park, Sherwood Forest and the wooded Dukeries to the north, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews who climb and clear Sherwood's trees",
  "s1loc":[
   "On the edge of Sherwood Forest, Mansfield sits in classic Nottinghamshire tree country, with a large estate of mature park, street and woodland trees, and managing it keeps a busy community of arborists and tree surgeons working across the county. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the area's leafy geography. Berry Hill Park and its woodlands sit on the town's doorstep, while Sherwood Forest with its veteran oaks and the Major Oak, Sherwood Pines, Vicar Water Country Park and Clumber Park in the Dukeries near Worksop hold ancient parkland and woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Mansfield tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and ash dieback and veteran-oak management across the Sherwood landscape shape the work alongside TPO and conservation-area rules. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Family firms and small crews run most of it: a climber and a groundsman, a one or two-van outfit working across Mansfield, Sutton-in-Ashfield and the wider Nottinghamshire patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the area's gardens, parks and Sherwood woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Mansfield's parks and Sherwood Forest woodland",
 },
 "eastbourne": {
  "region":"Eastbourne and East Sussex",
  "nearby":["Hailsham", "Bexhill-on-Sea", "Seaford"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Eastbourne, from sole-trader climbers and groundsmen to small firms working Hampden Park, Friston Forest and the South Downs above Beachy Head, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear the South Downs' trees",
  "s1loc":[
   "Spread beneath the chalk of the South Downs, Eastbourne is a green seaside town with a large estate of mature park, garden and downland trees, and keeping it managed supports a busy community of arborists and tree surgeons along the East Sussex coast. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the town's leafy geography. Suburbs like Old Town, Meads, Willingdon and Ratton carry mature oak, beech and estate trees, while Hampden Park, Gildredge Park, Friston Forest, the Eastbourne Downland Estate and Beachy Head hold parkland, beech woodland and downland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Eastbourne tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and a major ash dieback programme felling diseased trees in the woodland between Willingdon and Meads keeps the saws busy alongside TPO and South Downs conservation-area rules. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Small outfits do most of the work: a climber and a groundsman, a family business, a one or two-van team working across Eastbourne, Hailsham and the wider East Sussex patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's gardens, parks and downland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Eastbourne's parks, Friston Forest and South Downs woodland",
 },
 "oldham": {
  "region":"Oldham and Greater Manchester",
  "nearby":["Rochdale", "Ashton-under-Lyne", "Royton"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Oldham, from sole-trader climbers and groundsmen to small firms working Tandle Hill, Daisy Nook and the wooded cloughs of the Saddleworth Pennine edge, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews who climb and clear the Pennine edge's trees",
  "s1loc":[
   "Climbing the western slopes of the Pennines, Oldham carries a large estate of mature park, street and valley-clough trees, and managing it keeps a busy community of arborists and tree surgeons working across Greater Manchester. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the borough's leafy geography. Suburbs like Royton, Crompton, Chadderton and Lees carry mature oak, beech and estate trees, while Tandle Hill Country Park with its beech woodland, Alexandra Park, Daisy Nook in the Medlock Valley, Crompton Moor and the Saddleworth fringe hold parkland and woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Oldham tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and ash dieback and exposed Pennine-fringe storm work shape much of the job alongside TPO and conservation-area rules. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Small crews run most of it: a climber and a groundsman, a family business, a one or two-van team working across Oldham, Royton and the wider Saddleworth and Pennine patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the borough's gardens, parks and Pennine woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Oldham's parks, country parks and Saddleworth Pennine woodland",
 },
 "wigan": {
  "region":"Wigan and Greater Manchester",
  "nearby":["Leigh", "Hindley", "Ashton-in-Makerfield"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Wigan, from sole-trader climbers and groundsmen to small firms working Haigh Woodland Park, Borsdane Wood and the borough's Greenheart, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews who climb and clear Wigan's trees",
  "s1loc":[
   "Wigan keeps a steady community of arborists and tree surgeons at work, a green borough on the edge of Greater Manchester with a big estate of mature street, park and woodland trees to manage. Most are sole traders and small teams running domestic gardens, council and country-park contracts and storm clearance, and every one of them depends on proper chainsaw PPE.",
   "The work follows the borough's wooded geography. Suburbs and villages like Standish, Aspull, Orrell and Shevington carry mature oak, beech and estate trees, while Haigh Woodland Park, the ancient woodland at Bottling Wood, Borsdane Wood Local Nature Reserve and the Three Sisters hold parkland and plantation, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Wigan tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with ash dieback and the borough's City of Trees community-forest planting shaping much of the work alongside TPO and conservation-area rules. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Most of the firms here are small: a climber and a groundsman, a family business, a one or two-van outfit working across Wigan, Leigh and the Douglas Valley. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the borough's gardens, parks and woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Wigan's gardens, Haigh Woodland Park and Douglas Valley woodland",
 },
 "sutton coldfield": {
  "region":"Sutton Coldfield and the West Midlands",
  "nearby":["Tamworth", "Lichfield", "Walsall"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Sutton Coldfield, from sole-trader climbers and groundsmen to small firms working Sutton Park national nature reserve, Four Oaks and the town's leafy estates, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear the Royal Town's trees",
  "s1loc":[
   "Few places in the West Midlands are as green as Sutton Coldfield, and managing its huge estate of mature street, park and garden trees keeps a busy community of arborists and tree surgeons going. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the town's leafy geography. Suburbs like Four Oaks, Mere Green, Little Aston and Wylde Green carry mature oak, beech and estate trees, while Sutton Park national nature reserve, with its ancient oak woodlands across more than 2,000 acres, Gum Slade and the wider heathland and lakes hold parkland and woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Sutton Coldfield tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and TPO and conservation-area rules across the leafy wards shape much of the work alongside ash dieback in the ancient woodland. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Up here the firms stay small: a climber and a groundsman, a family business, a one or two-van outfit working across Sutton Coldfield, Four Oaks and the Little Aston patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's gardens, parkland and ancient woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Sutton Coldfield's gardens, Sutton Park and Four Oaks estates",
 },
 "lincoln": {
  "region":"Lincoln and Lincolnshire",
  "nearby":["Gainsborough", "Newark", "Grantham"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Lincoln, from sole-trader climbers and groundsmen to small firms working Hartsholme Country Park, the Cliff and the city's parks and woodland, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews who climb and clear Lincoln's trees",
  "s1loc":[
   "A cathedral city set on the Cliff above the Lincolnshire flatland, Lincoln carries a large estate of mature street, park and garden trees, and keeping it in shape supports a steady community of arborists and tree surgeons. Most are sole traders and small teams working domestic gardens, council and country-park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the city's geography. Areas like Boultham, Swallowbeck and the Uphill streets below the cathedral carry mature limes, oaks and estate trees, while Hartsholme Country Park, Boultham Park, the adjoining Swanholme Lakes and Whisby Nature Park to the west hold Victorian parkland, willow, birch and oak woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Lincoln tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and TPO and conservation-area rules shape much of the work alongside ash dieback across the county's woodland. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Out here the firms are mostly small: a climber and a groundsman, a family business, a one or two-van outfit working across Lincoln, Skellingthorpe and the wider Lincolnshire patch toward Doddington and the Limewoods. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the city's gardens, parks and woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Lincoln's gardens, Hartsholme Country Park and the Cliff woodland",
 },
 "worcester": {
  "region":"Worcester and Worcestershire",
  "nearby":["Malvern", "Droitwich", "Kidderminster"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Worcester, from sole-trader climbers and groundsmen to small firms working Worcester Woods Country Park, the Severn riverside and the Malvern Hills, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Worcestershire's trees",
  "s1loc":[
   "Hugging the River Severn in the heart of Worcestershire, Worcester is a green riverside city with a large estate of mature street, park and garden trees, and managing it keeps a busy community of arborists and tree surgeons going. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the city's leafy geography. Suburbs like Barbourne, St Johns and Battenhall carry mature oak, beech and tree-lined Victorian streets, while Worcester Woods Country Park with its medieval Nunnery Wood, Gheluvelt Park, the Severn riverside and the Malvern Hills beyond hold parkland and ancient woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Worcester tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with the city council's ongoing ash dieback assessments and TPO and conservation-area rules shaping much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Around here the firms stay small: a climber and a groundsman, a family business, a one or two-van outfit working across Worcester, Malvern and out toward the Wyre Forest and Kidderminster. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the city's gardens, riverside parks and woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Worcester's gardens, Worcester Woods and the Severn and Malvern Hills",
 },
 "salford": {
  "region":"Salford and Greater Manchester",
  "nearby":["Manchester", "Stretford", "Urmston"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Salford, from sole-trader climbers and groundsmen to small firms working Clifton Country Park, the RHS Bridgewater estate at Worsley and the peatlands of Chat Moss, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews who climb and clear Salford's trees",
  "s1loc":[
   "Right alongside Manchester yet greener than its city image suggests, Salford carries a large estate of mature street, park and woodland trees, and keeping it managed supports a steady community of arborists and tree surgeons. Most are sole traders and small teams working domestic gardens, council and country-park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the city's geography. Areas like Worsley, Monton, Kersal and Swinton carry mature oak, beech and estate trees, while Clifton Country Park, Buile Hill Park, Kersal Moor, the RHS Bridgewater grounds on the former Worsley New Hall estate and the peatlands of Chat Moss hold parkland and woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Salford tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with the City of Trees community forest and the council's tree-planting pledge driving new woodland work alongside ash dieback and TPO and conservation-area rules. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "In Salford the firms are mostly small: a climber and a groundsman, a family business, a one or two-van outfit working across Salford, Worsley, the Quays and the Irwell valley. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the city's gardens, parks and woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Salford's gardens, Clifton Country Park and the Worsley and Chat Moss woodland",
 },
 "st helens": {
  "region":"St Helens and Merseyside",
  "nearby":["Widnes", "Prescot", "Warrington"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across St Helens, from sole-trader climbers and groundsmen to small firms working Sankey Valley, Sherdley Park and the wider Mersey Forest, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Merseyside's trees",
  "s1loc":[
   "A former coal and glass town turned green, St Helens sits inside the Mersey Forest and carries a large estate of mature street, park and reclaimed-colliery trees, and looking after it keeps a steady community of arborists and tree surgeons busy across the borough and wider Merseyside. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the borough's leafy geography. Suburbs and villages like Eccleston, Windle, Rainford and Sutton carry mature oak, beech and estate trees, while Sankey Valley Country Park, Sherdley Park, Bold Forest Park and the Woodland Trust holdings along the old Sankey Canal hold parkland and woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. St Helens tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with ash dieback driving a steady run of felling licences and removals across the borough and TPO and conservation-area rules shaping much of the rest. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Firms here stay small by nature: a climber and a groundsman, a family business, a one or two-van outfit working St Helens, Haydock, Rainford and the wider Merseyside patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the borough's gardens, parks and Mersey Forest woodland",
  "s2_intro":"Whether you climb, work the ground or run a small crew across St Helens's gardens, parks, Sankey Valley and Mersey Forest woodland",
 },
 "wembley": {
  "region":"Wembley and the London Borough of Brent",
  "nearby":["Harrow", "Edgware", "Ruislip"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Wembley, from sole-trader climbers and groundsmen to small firms working Fryent Country Park, Barn Hill and Brent's leafy suburbs, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear north-west London's trees",
  "s1loc":[
   "For all the stadium and high-rise, Wembley sits in a surprisingly green corner of north-west London, with a large estate of mature street, garden and park trees across Brent, and managing it keeps a busy community of arborists and tree surgeons working the borough. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the borough's leafy geography. Areas like Sudbury Court, Barn Hill, Preston and Kingsbury carry mature oak, hornbeam and estate trees, while Fryent Country Park, Barham Park and the ancient hedgerows and small woods around Roe Green hold parkland and woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Wembley tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and with Brent's 22 conservation areas and a heavy TPO load, six-week notices and consents shape much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Outfits here are mostly small: a climber and a groundsman, a family business, a one or two-van crew working Wembley, Sudbury, Kingsbury and the wider Brent patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the borough's gardens, parks and country-park tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Wembley's gardens, parks and Fryent Country Park woodland",
 },
 "hemel hempstead": {
  "region":"Hemel Hempstead and Hertfordshire",
  "nearby":["Watford", "St Albans", "Berkhamsted"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Hemel Hempstead, from sole-trader climbers and groundsmen to small firms working Box Moor, Roughdown Common and the Ashridge beech woods, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear the Chilterns' trees",
  "s1loc":[
   "Set on the edge of the Chiltern Hills, Hemel Hempstead is a green town wrapped in commons, chalk valleys and beech woodland, and keeping that tree estate in order supports a busy community of arborists and tree surgeons across the town and wider Dacorum. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the town's leafy geography. Areas like Boxmoor, Felden, Bovingdon and Boxmoor's valley sides carry mature oak, beech and estate trees, while the Box Moor Trust commons, Roughdown Common and the National Trust's Ashridge Estate beech and oak woods in the Chilterns AONB hold parkland and woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Hemel tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with ash dieback thinning the woods and hedgerows and TPO and conservation-area rules shaping much of the rest. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Most firms here are small concerns: a climber and a groundsman, a family business, a one or two-van outfit working Hemel, Bovingdon, Berkhamsted and the wider Dacorum patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's gardens, commons and Chilterns woodland",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Hemel Hempstead's gardens, Box Moor commons and Ashridge Chilterns woodland",
 },
 "watford": {
  "region":"Watford and Hertfordshire",
  "nearby":["Bushey", "St Albans", "Borehamwood"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Watford, from sole-trader climbers and groundsmen to small firms working Cassiobury Park, Whippendell Wood and Oxhey Woods, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Hertfordshire's trees",
  "s1loc":[
   "Hemmed by ancient woodland and the Gade and Colne valleys, Watford is a green Hertfordshire town with a large estate of mature street, park and garden trees, and looking after it keeps a busy community of arborists and tree surgeons working across the town and its borders. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the town's leafy geography. Suburbs like Nascot Wood, Cassiobury, Oxhey and neighbouring Bushey carry mature oak, lime and estate trees, while Cassiobury Park, the ancient Whippendell Wood SSSI with its 1672 lime avenue and Oxhey Woods Local Nature Reserve hold parkland and woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Watford tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with conservation areas like Nascot and Oxhey and a steady TPO load meaning six-week notices and consents shape much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Crews here tend to be small: a climber and a groundsman, a family business, a one or two-van outfit working Watford, Bushey, Rickmansworth and the wider Hertfordshire patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's gardens, parks and ancient woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Watford's gardens, Cassiobury Park and Whippendell Wood",
 },
 "stockport": {
  "region":"Stockport and Greater Manchester",
  "nearby":["Bramhall", "Altrincham", "Denton"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Stockport, from sole-trader climbers and groundsmen to small firms working Etherow Country Park, Reddish Vale and the Peak District fringe, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Greater Manchester's trees",
  "s1loc":[
   "Sitting where the Goyt and Tame meet to form the Mersey, Stockport runs from dense Victorian streets out to wooded river valleys and the Peak District fringe, and that mix of mature street, park and valley trees keeps a busy community of arborists and tree surgeons working across the borough. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the borough's leafy geography. Suburbs like Bramhall, Cheadle Hulme, Heaton Moor, Marple and Woodford carry mature oak, beech and estate trees, while Etherow Country Park, Reddish Vale Country Park, Bramall Hall parkland and the woods running up toward Werneth Low hold parkland and woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Stockport tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with a dense TPO load across the Cheshire-border suburbs and conservation areas like Bramhall, Marple and Romiley meaning notices and consents shape much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "By and large the firms are small: a climber and a groundsman, a family business, a one or two-van outfit working Stockport, Bramhall, Marple and the wider Greater Manchester patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the borough's gardens, parks and Peak-fringe woodland",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Stockport's gardens, Etherow and Reddish Vale country parks and Peak District fringe",
 },
 "rochdale": {
  "region":"Rochdale and Greater Manchester",
  "nearby":["Heywood", "Middleton", "Bury"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Rochdale, from sole-trader climbers and groundsmen to small firms working Hollingworth Lake, Healey Dell and the Roch and Spodden valley woodlands, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews who climb and clear the Pennine fringe",
  "s1loc":[
   "On the western edge of the Pennines, Rochdale runs from mill-town streets up into wooded cloughs and valley sides, and looking after all those trees keeps a steady community of arborists and tree surgeons at work across the borough. The trade here is mostly sole traders and small teams on domestic gardens, council and park contracts and storm clearance, and every one of them leans on proper chainsaw PPE to get through the day.",
   "The work tracks the local geography. Leafy suburbs like Bamford, Norden and Littleborough carry mature oak, beech and sycamore, while Hollingworth Lake Country Park, Healey Dell nature reserve in the Spodden Valley, Alkrington Wood, Hopwood Wood and the Roch and Irk valley woodlands hold parkland and steep clough woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Rochdale tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with ash dieback steadily thinning the valley ash and TPO and conservation-area rules shaping much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Most of the outfits stay small. A climber and a groundsman, a family business, a one or two-van firm covering Rochdale, Littleborough and out across the Heywood, Middleton and Bury patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the borough's valley woodland, parks and garden tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Rochdale's Pennine cloughs, valley woods and country parks",
 },
 "hove": {
  "region":"Hove and Sussex",
  "nearby":["Brighton", "Shoreham-by-Sea", "Worthing"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Hove, from sole-trader climbers and groundsmen to small firms working St Ann's Well Gardens, the leafy Tongdean and Withdean avenues and the South Downs above the city, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Sussex's coastal trees",
  "s1loc":[
   "Sitting on the chalk between the sea and the South Downs, Hove carries a rich stock of mature street, park and garden trees, and keeping it healthy supports a busy community of arborists and tree surgeons across the city and wider Sussex. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the city's leafy geography. Suburbs like Tongdean, Withdean and Hangleton carry mature elm, sycamore and beech along grass-verged avenues such as Tongdean Avenue and Shirley Drive, while St Ann's Well Gardens, Hove Recreation Ground and the South Downs National Park scarp hold parkland and downland trees, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Hove tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and the city's nationally important elm collection brings strict Dutch elm disease sanitation and TPO and conservation-area rules into much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Out on the vans the firms stay small. A climber and a groundsman, a family business, a one or two-van outfit working across Hove, Brighton and along the coast to Shoreham-by-Sea and Worthing. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the city's gardens, parks and downland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Hove's elm avenues, seafront gardens and South Downs scarp",
 },
 "ilford": {
  "region":"Ilford and North East London",
  "nearby":["Romford", "Hornchurch", "Walthamstow"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Ilford, from sole-trader climbers and groundsmen to small firms working Valentines Park, Hainault Forest and the leafy Redbridge suburbs, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews who climb and clear Redbridge's trees",
  "s1loc":[
   "Out on the green edge of North East London, Ilford and the wider Redbridge borough hold tens of thousands of street, park and garden trees, and managing them keeps a busy community of arborists and tree surgeons at work across the area. The trade is mostly sole traders and small teams on domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the borough's leafy geography. Suburbs like Cranbrook, Gants Hill, Newbury Park and Aldborough Hatch carry mature oak, lime and plane, while Valentines Park with its 300-year-old field maple, Hainault Forest Country Park and the ancient woodland on the Epping Forest fringe hold parkland and veteran trees, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Ilford tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and with over 21,000 street trees inspected each year and trees over 75mm automatically protected in conservation areas, Redbridge TPO and conservation-area rules shape much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "The outfits themselves stay small. A climber and a groundsman, a family business, a one or two-van firm covering Ilford, Seven Kings and out across the Romford, Hornchurch and Walthamstow patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the borough's parks, forest fringe and garden tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Ilford's parks, Hainault Forest and leafy Redbridge suburbs",
 },
 "barnsley": {
  "region":"Barnsley and South Yorkshire",
  "nearby":["Rotherham", "Mexborough", "Doncaster"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Barnsley, from sole-trader climbers and groundsmen to small firms working Cannon Hall, Wentworth Castle Gardens and the Dearne Valley woodlands, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear South Yorkshire's trees",
  "s1loc":[
   "Set between the Pennine moors and the Dearne Valley, Barnsley carries a wealth of estate, park and garden trees alongside reclaimed colliery woodland, and looking after it keeps a steady community of arborists and tree surgeons busy across the borough and South Yorkshire. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the local geography. Districts like Worsbrough, Stainborough and Birdwell carry mature oak, beech and sycamore, while Cannon Hall Country Park with its veteran specimen trees, the National Trust parkland and woodland at Wentworth Castle Gardens, Locke Park and the Dearne Valley Country Park hold historic estate and valley woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Barnsley tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with ash dieback hitting the borough's ash year on year and TPO and conservation-area rules shaping much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "And the firms keep it small. A climber and a groundsman, a family business, a one or two-van outfit working across Barnsley, the Dearne towns and out toward Rotherham, Mexborough and Doncaster. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the borough's estate parkland, valley woods and garden tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Barnsley's estate parkland, Dearne Valley woods and country parks",
 },
 "darlington": {
  "region":"Darlington and County Durham",
  "nearby":["Stockton-on-Tees", "Newton Aycliffe", "Bishop Auckland"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Darlington, from sole-trader climbers and groundsmen to small firms working South Park, the Denes and the Tees valley woodlands, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews who climb and clear the Tees valley's trees",
  "s1loc":[
   "Down on the Tees in the south of County Durham, Darlington holds a generous stock of Victorian park, street and garden trees together with the wooded becks that thread through the town, and managing it all keeps a steady community of arborists and tree surgeons at work across the area. The trade is mostly sole traders and small teams on domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the town's green geography. Leafy areas around Hummersknott and the Denes carry mature oak, beech and lime, while South Park with its historic specimen trees, the wooded Denes alongside Cocker Beck and the Tees valley woodland hold parkland and riverside trees, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Darlington tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and Storm Arwen, which left a major incident declared across Durham and Darlington with thousands of trees down, still shapes the clearance and replanting work alongside ash dieback and TPO and conservation-area rules. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Out on the vans the firms stay small. A climber and a groundsman, a family business, a one or two-van outfit working across Darlington and out to Stockton-on-Tees, Newton Aycliffe and Bishop Auckland. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's parks, wooded becks and Tees valley tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Darlington's parks, wooded denes and Tees valley woodland",
 },
 "hastings": {
  "region":"Hastings and East Sussex",
  "nearby":["Bexhill-on-Sea", "Eastbourne", "Hailsham"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Hastings, from sole-trader climbers and groundsmen to small firms working Hastings Country Park's ancient gill woodland, the High Weald and the town's wooded suburbs, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews who climb and clear the High Weald's trees",
  "s1loc":[
   "Wooded and steeply folded, Hastings sits in the High Weald with a deep estate of mature street, garden and woodland trees, and looking after it keeps a busy community of arborists and tree surgeons working across the town and East Sussex. Most are sole traders and small teams on domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the town's leafy geography. Suburbs like Ore, Silverhill, Hollington and St Leonards carry mature oak, beech and garden trees, while Hastings Country Park's ancient gill woodlands at Ecclesbourne Glen, Fairlight Glen and Warren Glen, Alexandra Park and the wider High Weald hold parkland and woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Hastings tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with ash dieback in the gill woodlands and TPO and conservation-area rules shaping much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Small outfits run most of this work: a climber and a groundsman, a family business, a one or two-van team working across Hastings, Battle and the wider East Sussex patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's gardens, parks and High Weald woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Hastings's gardens, Country Park gill woods and High Weald",
 },
 "hartlepool": {
  "region":"Hartlepool and County Durham",
  "nearby":["Billingham", "Stockton-on-Tees", "Peterlee"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Hartlepool, from sole-trader climbers and groundsmen to small firms working Summerhill Country Park, Ward Jackson Park and the Durham coast denes, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Teesside's trees",
  "s1loc":[
   "For a coastal town, Hartlepool carries a real green estate of street, park and maturing woodland trees, and managing it keeps a steady community of arborists and tree surgeons working across the town, the Tees Valley and the County Durham coast. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the town's greener edges. Areas like Hart village, Elwick, Rossmere and the western suburbs carry mature garden and estate trees, while Summerhill Country Park's young maturing woodland, Ward Jackson Park, Rossmere Park and the coastal denes at Crimdon and Castle Eden hold parkland and woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Hartlepool tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with Storm Arwen windblow along the Durham coast, ash dieback and TPO and conservation-area rules shaping much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Mostly these are small firms: a climber and a groundsman, a family business, a one or two-van outfit working across Hartlepool, Wynyard and the wider Teesside and County Durham patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's gardens, parks and coastal dene woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Hartlepool's gardens, country parks and Durham coast denes",
 },
 "birkenhead": {
  "region":"Birkenhead and the Wirral",
  "nearby":["Wallasey", "Bebington", "Heswall"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Birkenhead, from sole-trader climbers and groundsmen to small firms working Birkenhead Park, Arrowe Country Park and Bidston Hill, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews who climb and clear the Wirral's trees",
  "s1loc":[
   "Greener than its docks suggest, Birkenhead holds a substantial estate of mature street, park and garden trees, and managing it keeps a busy community of arborists and tree surgeons working across the town and the wider Wirral. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the town's leafy geography. Suburbs like Oxton, Prenton and Noctorum carry mature oak, beech and garden trees, while Birkenhead Park, Arrowe Country Park's deciduous woodland, Bidston Hill and the wider Mersey Forest hold parkland and woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Birkenhead tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with the Wirral's ash dieback assessments and TPO and conservation-area rules shaping much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Small outfits do most of this work: a climber and a groundsman, a family business, a one or two-van team working across Birkenhead, Wallasey and the wider Wirral peninsula. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's parks, gardens and Wirral woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Birkenhead's parks, gardens and Wirral woodland",
 },
 "bath": {
  "region":"Bath and Somerset",
  "nearby":["Bristol", "Trowbridge", "Frome"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Bath, from sole-trader climbers and groundsmen to small firms working the National Trust's Bath Skyline, Smallcombe Wood and Prior Park, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Somerset's trees",
  "s1loc":[
   "Wrapped in wooded hillsides, Bath carries a dense estate of mature street, park and garden trees, and looking after it keeps a busy community of arborists and tree surgeons working across the city and the wider Somerset and Cotswold edge. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the city's leafy geography. Suburbs like Bathwick, Combe Down, Lansdown and Widcombe carry mature oak, beech, lime and ash trees, while the National Trust's Bath Skyline, Smallcombe Wood, Bathwick Wood and Prior Park Landscape Garden hold parkland and woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Bath tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with the city's extensive conservation areas, TPOs and ash dieback shaping much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Family-sized firms run most of this work: a climber and a groundsman, a one or two-van outfit working across Bath, Bradford on Avon and the wider Somerset patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the city's gardens, parks and Skyline woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Bath's gardens, the National Trust Skyline and Somerset woodland",
 },
 "stevenage": {
  "region":"Stevenage and Hertfordshire",
  "nearby":["Hitchin", "Letchworth", "Welwyn Garden City"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Stevenage, from sole-trader climbers and groundsmen to small firms working Fairlands Valley Park, Whomerley Wood and the Knebworth estate, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews who climb and clear Hertfordshire's trees",
  "s1loc":[
   "Laced with green corridors and ancient woods, Stevenage holds a large estate of mature street, park and woodland trees, and managing it keeps a steady community of arborists and tree surgeons working across the town and the wider Hertfordshire patch. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the town's leafy geography. Areas like the Old Town, Shephall, Chells and Great Ashby carry mature oak, beech and garden trees, while Fairlands Valley Park, Monks Wood, Whomerley Wood and the ancient parkland oaks of the Knebworth estate hold parkland and woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Stevenage tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with ash dieback in the local woods and TPO and conservation-area rules shaping much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Small teams handle most of this work: a climber and a groundsman, a family business, a one or two-van outfit working across Stevenage, Knebworth and the wider Hertfordshire patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's parks, gardens and Hertfordshire woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Stevenage's parks, ancient woods and the Knebworth estate",
 },
 "grimsby": {
  "region":"Grimsby and North East Lincolnshire",
  "nearby":["Cleethorpes", "Scunthorpe", "Hull"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Grimsby, from sole-trader climbers and groundsmen to small firms working Weelsby Woods, People's Park and the ancient oak of Bradley Woods, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews who climb and clear the Humber's trees",
  "s1loc":[
   "Greener than its industrial reputation suggests, Grimsby carries a real estate of mature street, park and woodland trees, and looking after it keeps a steady community of arborists and tree surgeons busy across North East Lincolnshire. The bulk are sole traders and small teams on domestic gardens, council park contracts and storm clearance, and every one of them leans on proper chainsaw PPE.",
   "The work tracks the local geography. Leafy suburbs like Scartho and Waltham hold mature garden and street trees, while Weelsby Woods, the Victorian People's Park and the thousand-year-old oak of Bradley and Dixon Woods carry parkland and ancient woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms working towards the Lincolnshire Wolds.",
   "It is a safety-critical trade run to recognised standards. Grimsby tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with ash dieback in the wider Lincolnshire woods and TPO and conservation-area rules shaping much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Most of these outfits stay small: a climber and a groundsman, a family business, a one or two-van team covering Grimsby, Cleethorpes and the wider North East Lincolnshire patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's gardens, parks and woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Grimsby's gardens, Weelsby Woods and the wider North East Lincolnshire patch",
 },
 "southport": {
  "region":"Southport and Merseyside",
  "nearby":["Formby", "Ormskirk", "Crosby"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Southport, from sole-trader climbers and groundsmen to small firms working Hesketh Park, the Botanic Gardens and the Formby pinewoods, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Sefton's trees",
  "s1loc":[
   "A genteel coastal town with wide tree-lined boulevards and big Victorian and Edwardian gardens, Southport holds a substantial estate of mature park, street and estate trees, and managing it keeps a busy community of arborists and tree surgeons working across the Sefton coast. Most are sole traders and small teams on domestic gardens, council park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the town's leafy geography. Premium suburbs like Birkdale and Ainsdale carry wide tree-lined roads and large mature gardens, while Hesketh Park with its champion Dawn Redwood and Japanese pagoda trees, the heavily wooded Botanic Gardens at Churchtown and the National Trust pinewoods and red-squirrel reserve at Formby generate crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Southport tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with ash dieback across the Sefton coast and TPO and conservation-area rules shaping much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "The firms are mostly small: a climber and a groundsman, a family business, a one or two-van outfit working across Southport, Formby and the wider Sefton and West Lancashire patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the coast's gardens, parks and pinewood tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Southport's gardens, parks and the Formby pinewoods",
 },
 "halifax": {
  "region":"Halifax and Calderdale",
  "nearby":["Brighouse", "Huddersfield", "Bradford"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Halifax, from sole-trader climbers and groundsmen to small firms working Shibden Park, Ogden Water and the wooded Pennine valleys, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews who climb and clear Calderdale's trees",
  "s1loc":[
   "Set among the steep, wooded valleys of the Pennines, Halifax holds a heavy estate of mature park, hillside and clough woodland trees, and managing it keeps a busy community of arborists and tree surgeons working across Calderdale. Most are sole traders and small teams on domestic gardens, council park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the town's valley geography. Leafy areas like Savile Park and Skircoat hold mature garden and street trees, while Shibden Park with its Cunnery Wood, Ogden Water Country Park and the National Trust valley woodland at Hardcastle Crags near Hebden Bridge carry parkland and steep Pennine woods, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Halifax tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with ash dieback that forced felling at Hardcastle Crags and the storm work after Storm Lilian brought trees down across Calderdale shaping much of the trade. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Mostly these are small outfits: a climber and a groundsman, a family business, a one or two-van team working across Halifax, Hebden Bridge and the wider Calderdale and Ryburn valley patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the valley's gardens, parks and Pennine woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Halifax's gardens, parks and the wooded Pennine valleys",
 },
 "eltham": {
  "region":"Eltham and South East London",
  "nearby":["Woolwich", "Sidcup", "Bromley"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Eltham, from sole-trader climbers and groundsmen to small firms working the ancient woodland of Oxleas Wood, Avery Hill Park and Eltham Palace gardens, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Greenwich's trees",
  "s1loc":[
   "One of the greener corners of south east London, Eltham carries a substantial estate of mature street, park and ancient woodland trees, and looking after it keeps a steady community of arborists and tree surgeons busy across the Royal Borough of Greenwich. The bulk are sole traders and small teams on domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the area's leafy geography. The rural, tree-rich Eltham Palace conservation area and suburbs like Mottingham and Falconwood hold mature oak and estate trees, while Oxleas Wood, Jack Wood, Castle Wood and Shepherdleas Wood on Shooter's Hill, the Avery Hill Park grounds and the Eltham Palace gardens carry ancient woodland and parkland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Eltham tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with the Oxleas Woodlands SSSI, ash dieback and the dense web of Greenwich TPOs and conservation areas shaping much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Most of these outfits stay small: a climber and a groundsman, a family business, a one or two-van team working across Eltham, Woolwich and the wider south east London patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the borough's gardens, parks and ancient woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Eltham's gardens, parks and the ancient woodland of Oxleas",
 },
 "hounslow": {
  "region":"Hounslow and West London",
  "nearby":["Twickenham", "Feltham", "Staines"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Hounslow, from sole-trader climbers and groundsmen to small firms working Osterley Park, Bedfont Lakes and Hounslow Heath, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews who climb and clear West London's trees",
  "s1loc":[
   "Surprisingly green for an outer-London borough, Hounslow holds a large estate of mature street, park and estate trees, and managing it keeps a busy community of arborists and tree surgeons working across West London. Most are sole traders and small teams on domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the borough's leafy geography. Suburbs like Chiswick, Osterley and Isleworth carry mature garden and street trees, while the National Trust parkland and woodland at Osterley Park, Bedfont Lakes Country Park near Heathrow, Cranford Park and the heathland and birch of Hounslow Heath generate crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Hounslow tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with ash dieback, the Hounslow Highways street-tree programme and a dense web of TPOs and conservation areas shaping much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "The firms are mostly small: a climber and a groundsman, a family business, a one or two-van outfit working across Hounslow, Feltham and the wider West London patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the borough's gardens, parks and woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Hounslow's gardens, parks and Osterley woodland",
 },
 "bromley": {
  "region":"Bromley and South East London",
  "nearby":["Beckenham", "Orpington", "Sidcup"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Bromley, from sole-trader climbers and groundsmen to small firms working High Elms, Jubilee Country Park and the borough's commons and ancient woodland, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews who climb and clear London's greenest borough",
  "s1loc":[
   "Known as one of the greenest boroughs in London, Bromley holds around a third of the capital's ancient woodland and a large estate of mature street, park and garden trees, and looking after it keeps a busy community of arborists and tree surgeons working across the borough and into Kent. Most are sole traders and small teams on domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the borough's leafy geography. Suburbs like Chislehurst, Bickley, Hayes, Keston and Petts Wood carry mature oak, beech and estate trees, while High Elms Country Park, Kelsey Park, Jubilee Country Park and the commons at Hayes and Keston hold parkland and ancient semi-natural woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Bromley tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and with the borough's many conservation areas and Tree Preservation Orders plus ongoing ash dieback felling on the commons shaping much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Firms here run small and local: a climber and a groundsman, a family business, a one or two-van outfit working across Bromley, Orpington and the wider South East London and Kent border patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the borough's gardens, commons and ancient woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Bromley's gardens, commons and ancient woodland",
 },
 "nuneaton": {
  "region":"Nuneaton and Warwickshire",
  "nearby":["Bedworth", "Hinckley", "Tamworth"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Nuneaton, from sole-trader climbers and groundsmen to small firms working Hartshill Hayes Country Park and the old Arden woodland of north Warwickshire, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear north Warwickshire's trees",
  "s1loc":[
   "A market town set in the wooded north of Warwickshire, Nuneaton carries a large estate of mature street, park and garden trees together with the remnant ancient woodland of the old Forest of Arden, and managing it keeps a steady community of arborists and tree surgeons busy across the town and district. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the local geography. Suburbs and villages like Hartshill, Bulkington, Stockingford and Weddington carry mature oak, ash and estate trees, while Hartshill Hayes Country Park, the Nuneaton and Bedworth woodlands and the Pool Bank and Bedworth Sloughs nature sites hold hilly broadleaf and conifer woodland once part of the Arden, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Nuneaton tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with ash dieback felling across the district's ash-rich woods and TPO and conservation-area rules shaping much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Most outfits are small: a climber and a groundsman, a family business, a one or two-van team working across Nuneaton, Bedworth and the wider north Warwickshire and Leicestershire border patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's gardens, country parks and Arden woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Nuneaton's gardens, country parks and Arden woodland",
 },
 "redditch": {
  "region":"Redditch and Worcestershire",
  "nearby":["Bromsgrove", "Worcester", "Solihull"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Redditch, from sole-trader climbers and groundsmen to small firms working Arrow Valley Country Park and the ancient woods at Pitcheroak and Foxlydiate, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews who climb and clear Worcestershire's trees",
  "s1loc":[
   "Built as a new town in a green Worcestershire setting, Redditch wraps a large estate of mature street, park and garden trees around blocks of designated ancient woodland, and looking after it keeps a busy community of arborists and tree surgeons working across the town and district. Most are sole traders and small teams on domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the town's wooded layout. Neighbourhoods like Headless Cross, Webheath, Crabbs Cross and Batchley sit among mature oak, ash and estate trees, while Arrow Valley Country Park and the ancient and semi-natural woods at Pitcheroak, Foxlydiate, Wirehill, Southcrest and Oakenshaw hold parkland and woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Redditch tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with the council felling ash-dieback-affected trees across Pitcheroak and Foxlydiate and TPO and conservation-area rules shaping much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Firms here run small and local: a climber and a groundsman, a family business, a one or two-van outfit working across Redditch, Bromsgrove and the wider Worcestershire and Warwickshire border patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's gardens, country parks and ancient woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Redditch's gardens, country parks and ancient woodland",
 },
 "harlow": {
  "region":"Harlow and Essex",
  "nearby":["Bishop's Stortford", "Hoddesdon", "Hertford"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Harlow, from sole-trader climbers and groundsmen to small firms working Harlow Town Park, Parndon Wood and the town's green wedges, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Essex's greenest new town",
  "s1loc":[
   "Planned as a new town with over a third of its area as parkland and open space, Harlow threads green wedges and ancient woodland right through its neighbourhoods, and managing all those trees keeps a steady community of arborists and tree surgeons busy across the town and the Stort Valley. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the town's green-wedge geography. Areas like Old Harlow, Church Langley, Newhall and Mark Hall carry mature oak, hornbeam and estate trees, while Harlow Town Park, the Grade II listed Sylvia Crowe landscape, and Parndon Wood nature reserve with its 900-year-old oak and coppiced hornbeam hold parkland and ancient woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Harlow tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with ash dieback across the district's woods and TPO and conservation-area rules shaping much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Most outfits are small: a climber and a groundsman, a family business, a one or two-van team working across Harlow, Bishop's Stortford and the wider Essex and Hertfordshire border patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's parks, green wedges and woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Harlow's parks, green wedges and ancient woodland",
 },
 "harrow": {
  "region":"Harrow and North West London",
  "nearby":["Edgware", "Ruislip", "Wembley"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Harrow, from sole-trader climbers and groundsmen to small firms working Harrow Weald Common, Bentley Priory and the Stanmore and Pinner woods, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews who climb and clear North West London's trees",
  "s1loc":[
   "A leafy outer London borough rising to the wooded ridge of Harrow Weald, Harrow carries a large estate of mature street, park and garden trees alongside blocks of ancient woodland, and looking after it keeps a busy community of arborists and tree surgeons working across the borough and into Middlesex. Most are sole traders and small teams on domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the borough's leafy geography. Suburbs like Harrow Weald, Stanmore, Pinner and Hatch End carry mature oak, hornbeam and estate trees, while Harrow Weald Common, Bentley Priory Nature Reserve, Stanmore Country Park and the Pinner woods hold ancient woodland, hornbeam coppice and grassland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Harrow tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with ash dieback across the borough's woods and TPO and conservation-area rules shaping much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Firms here run small and local: a climber and a groundsman, a family business, a one or two-van outfit working across Harrow, Stanmore, Pinner and the wider North West London and Middlesex patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the borough's gardens, commons and ancient woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Harrow's gardens, commons and ancient woodland",
 },
 "st albans": {
  "region":"St Albans and Hertfordshire",
  "nearby":["Hatfield", "Harpenden", "Welwyn Garden City"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across St Albans, from sole-trader climbers and groundsmen to small firms working Verulamium Park, the Woodland Trust's Heartwood Forest and the city's green-belt woods, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews who climb and clear Hertfordshire's trees",
  "s1loc":[
   "A leafy cathedral city ringed by green belt, St Albans carries a large estate of mature street, park and garden trees, and looking after it keeps a busy community of arborists and tree surgeons working across the district. Most are sole traders and small teams on domestic gardens, council and park contracts and storm clearance, and every one of them depends on proper chainsaw PPE.",
   "The work follows the city's green geography. Suburbs like Marshalswick, Fleetville and Bricket Wood carry mature oak, beech and estate trees, while Verulamium Park, Clarence Park, the Gorhambury estate and the Woodland Trust's Heartwood Forest near Sandridge hold parkland and native woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. St Albans tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and with 19 conservation areas plus a long list of Tree Preservation Orders across the district, TPO and conservation-area rules shape much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Most of these outfits are small. A climber and a groundsman, a family business, a one or two-van crew covering St Albans, Harpenden and the wider Hertfordshire patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the city's gardens, parks and green-belt woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across St Albans's gardens, Verulamium Park and Hertfordshire green-belt woodland",
 },
 "stockton-on-tees": {
  "region":"Stockton-on-Tees and the Tees Valley",
  "nearby":["Thornaby-on-Tees", "Billingham", "Middlesbrough"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Stockton-on-Tees, from sole-trader climbers and groundsmen to small firms working Preston Park, the Tees riverside and the borough's parks and highway trees, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Gearing up the people who climb and clear the Tees Valley's trees",
  "s1loc":[
   "Spread along the River Tees, Stockton-on-Tees holds a big stock of mature park, riverside and highway trees, and managing it keeps a community of arborists and tree surgeons busy across the borough and the wider Tees Valley. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the borough's geography. Preston Park on the Tees, the riverside green corridor and parks at Oxbridge, Norton and Roseworth carry mature ash, oak and beech, while Billingham and the surrounding patch hold parkland and roadside trees, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Stockton tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members. Storm Arwen brought down around 250 mature trees across the borough in a single weekend, and with ash a main canopy tree in the parks and along the highways, ash dieback is steadily driving felling and removal work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "These firms tend to be small outfits. A climber and a groundsman, a family business, a one or two-van crew working across Stockton, Thornaby-on-Tees and the wider Tees Valley patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the borough's parks, riverside and highway tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Stockton-on-Tees's parks, Tees riverside and Tees Valley woodland",
 },
 "gosport": {
  "region":"Gosport and Hampshire",
  "nearby":["Fareham", "Portsmouth", "Havant"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Gosport, from sole-trader climbers and groundsmen to small firms working Alver Valley Country Park, the Wildgrounds ancient oak woodland and the Solent peninsula's parks, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews who climb and clear Hampshire's Solent trees",
  "s1loc":[
   "On a green peninsula running down to the Solent, Gosport holds a real spread of mature park, garden and woodland trees, and looking after it keeps a community of arborists and tree surgeons working across the town and South Hampshire. Most are sole traders and small teams on domestic gardens, council and park contracts and storm clearance, and every one of them depends on proper chainsaw PPE.",
   "The work follows the peninsula's geography. The Alver Valley Country Park, with its 580 acres of woodland, meadow and wetland between Gosport and Lee-on-the-Solent, the Wildgrounds nature reserve and the green spaces around Stokes Bay carry mature oak, including veteran ancient pollards, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Gosport tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with TPO and conservation-area rules shaping much of the work and ash dieback steadily altering the countryside around the Solent. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "These outfits stay small for the most part. A climber and a groundsman, a family business, a one or two-van crew covering Gosport, Fareham and the wider Hampshire patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the peninsula's gardens, parks and Solent woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Gosport's gardens, Alver Valley Country Park and Solent woodland",
 },
 "scunthorpe": {
  "region":"Scunthorpe and North Lincolnshire",
  "nearby":["Grimsby", "Gainsborough", "Goole"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Scunthorpe, from sole-trader climbers and groundsmen to small firms working Normanby Hall Country Park, Twigmoor Woods and the broadleaf woodland around the town, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Gearing up the people who climb and clear North Lincolnshire's trees",
  "s1loc":[
   "Set in North Lincolnshire countryside, Scunthorpe carries a good stock of mature park, estate and garden trees, and managing it keeps a community of arborists and tree surgeons busy across the town and the wider district. Most are sole traders and small teams working domestic gardens, council and estate contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the local geography. Normanby Hall Country Park, just north of the town, holds 300 acres of mature broadleaf woodland, walled gardens and a deer park, while Twigmoor Woods and the green spaces around Ashby, Brumby and Flixborough carry oak, beech and ash, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Scunthorpe tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with TPO and conservation-area rules and ash dieback across the Lincolnshire countryside shaping much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Most of these firms are small. A climber and a groundsman, a family business, a one or two-van crew working Scunthorpe, Brigg and the wider North Lincolnshire patch out towards Grimsby. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's gardens, parks and broadleaf woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Scunthorpe's gardens, Normanby Hall Country Park and North Lincolnshire woodland",
 },
 "chesterfield": {
  "region":"Chesterfield and Derbyshire",
  "nearby":["Dronfield", "Belper", "Sheffield"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Chesterfield, from sole-trader climbers and groundsmen to small firms working Linacre Woods, Holmebrook Valley Park and Poolsbrook Country Park on the Peak District's edge, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews who climb and clear Derbyshire's trees",
  "s1loc":[
   "A Peak District gateway town, Chesterfield holds a large estate of mature street, park and woodland trees, and looking after it keeps a busy community of arborists and tree surgeons working across the town and north-east Derbyshire. Most are sole traders and small teams on domestic gardens, council and park contracts and storm clearance, and every one of them depends on proper chainsaw PPE.",
   "The work follows the town's geography. Suburbs like Walton and Brampton carry mature oak, beech and garden trees, while Linacre Woods and its reservoirs, Holmebrook Valley Park and the former-colliery woodland at Poolsbrook Country Park hold oak, ash, sycamore, beech, larch and pine, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Chesterfield tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with TPO and conservation-area rules and ash dieback across the Derbyshire countryside shaping much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "These outfits are mostly small. A climber and a groundsman, a family business, a one or two-van crew working Chesterfield, Dronfield and the wider Peak District fringe towards Sheffield. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's gardens, parks and Peak-fringe woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Chesterfield's gardens, Linacre Woods and Peak District-fringe woodland",
 },
 "ashford": {
  "region":"Ashford and Kent",
  "nearby":["Folkestone", "Canterbury", "Maidstone"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Ashford, from sole-trader climbers and groundsmen to small firms working Kings Wood at Challock, Victoria Park, Conningbrook and the wider Kent Downs woodland, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear the Kent Downs' trees",
  "s1loc":[
   "Sitting under the Kent Downs National Landscape, Ashford is a green town ringed by ancient woodland and chalk-down trees, and looking after that estate keeps a steady community of arborists and tree surgeons busy across the borough and east Kent. Most are sole traders and small teams working domestic gardens, council and country-park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the local geography. The town has Victoria Park and Conningbrook Lakes country park on its doorstep, while Kings Wood at Challock, Hoad's Wood, Ashford Warren and the coppiced sweet-chestnut woods of the Kent Downs hold parkland and ancient woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Ashford tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and ash dieback runs hard through Kent, the county's commonest tree, driving years of removals and replanting. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Firms here stay small by nature: a climber and a groundsman, a family business, a one or two-van outfit working Ashford, Tenterden and the wider Kent Downs patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the borough's parks, country parks and Kent Downs woodland",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Ashford's parks, country parks and Kent Downs woodland",
 },
 "guildford": {
  "region":"Guildford and Surrey",
  "nearby":["Godalming", "Farnham", "Aldershot"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Guildford, from sole-trader climbers and groundsmen to small firms working the Surrey Hills, Pewley Down, the Chantries, Stoke Park and the Hog's Back, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear the Surrey Hills' trees",
  "s1loc":[
   "Set in the Surrey Hills National Landscape with the North Downs and greensand ridges around it, Guildford is a wooded town carrying a large estate of mature oak, beech and yew, and managing it keeps a busy community of arborists and tree surgeons working across the town and Surrey. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the town's leafy geography. Suburbs like Merrow, Onslow Village and Pewley Hill carry mature estate trees, while Pewley Down, the Chantries and Chantry Wood, Stoke Park, Merrow Downs and the Hog's Back ridge hold parkland and ancient woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Guildford tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and AONB planning, TPOs and conservation-area rules shape much of the work across the Surrey Hills. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "And the firms are mostly small: a climber and a groundsman, a family business, a one or two-van outfit working across Guildford, Godalming and the wider Surrey Hills patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's gardens, downs and Surrey Hills woodland",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Guildford's downs, parks and Surrey Hills woodland",
 },
 "lewisham": {
  "region":"Lewisham and south-east London",
  "nearby":["Woolwich", "Eltham", "Beckenham"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Lewisham, from sole-trader climbers and groundsmen to small firms working Beckenham Place Park, Ladywell Fields, Blythe Hill and the borough's Great North Wood remnants, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear south-east London's trees",
  "s1loc":[
   "For an inner London borough Lewisham is strikingly green, carrying mature street, park and garden trees alongside surviving ancient woodland, and looking after that estate keeps a busy community of arborists and tree surgeons working across the borough and south-east London. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the borough's leafy geography. Suburbs like Blackheath, Forest Hill and Sydenham carry mature estate trees, while Beckenham Place Park with its ancient Summerhouse Hill woodland, Sydenham Hill Wood, Ladywell Fields and Blythe Hill Fields hold parkland and Great North Wood remnants, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Lewisham tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and dense streets, TPOs and conservation-area rules shape much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Most outfits here run lean: a climber and a groundsman, a family business, a one or two-van crew working across Lewisham, Catford and the wider south-east London patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the borough's streets, parks and ancient woodland",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Lewisham's parks, streets and ancient woodland",
 },
 "woolwich": {
  "region":"Woolwich and the Royal Borough of Greenwich",
  "nearby":["Eltham", "Erith", "Sidcup"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Woolwich, from sole-trader climbers and groundsmen to small firms working Oxleas Wood, Shooters Hill, Plumstead Common and the Green Chain woodland, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Shooters Hill's trees",
  "s1loc":[
   "Climbing from the Thames up to the wooded ridge of Shooters Hill, Woolwich sits beside some of London's largest surviving ancient woodland, and looking after that estate keeps a steady community of arborists and tree surgeons working across the Royal Borough of Greenwich and south-east London. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the local geography. Areas like Plumstead, Shooters Hill and Eltham carry mature street and estate trees, while Oxleas Wood, Jack Wood and Shepherdleas Wood, Plumstead Common, Eltham Common and the South East London Green Chain hold parkland and SSSI ancient woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Woolwich tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and the Oxleas Woodlands SSSI, coppicing programmes, TPOs and conservation-area rules shape much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Crews here tend to stay small: a climber and a groundsman, a family business, a one or two-van outfit working across Woolwich, Plumstead and the wider Greenwich borough patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the borough's commons, parks and Green Chain woodland",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Woolwich's commons, parks and Shooters Hill woodland",
 },
 "weston-super-mare": {
  "region":"Weston-super-Mare and Somerset",
  "nearby":["Clevedon", "Portishead", "Bridgwater"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Weston-super-Mare, from sole-trader climbers and groundsmen to small firms working Worlebury Hill woods, Ashcombe Park and the Mendip fringe, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Somerset's coastal trees",
  "s1loc":[
   "Backed by the wooded ridge of Worlebury Hill at the western tip of the Mendips, Weston-super-Mare is a green seaside town with a large estate of mature street, park and woodland trees, and managing it keeps a steady community of arborists and tree surgeons busy across North Somerset. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the local geography. Suburbs like Worlebury, Uphill and Milton carry mature garden and estate trees, while Weston Woods on Worlebury Hill, Ashcombe Park, Ashcombe Wood and the beech plantations toward Sand Bay and the Mendip Hills National Landscape hold parkland and woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Weston tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and ash dieback has driven heavy felling and management work through Weston Woods and the wider Mendip fringe. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Firms here stay small by nature: a climber and a groundsman, a family business, a one or two-van outfit working across Weston-super-Mare, Clevedon and the wider North Somerset patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's gardens, parks and Worlebury Hill woodland",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Weston-super-Mare's parks, seafront and Worlebury Hill woodland",
 },
 "west bromwich": {
  "region":"West Bromwich and the Black Country",
  "nearby":["Wednesbury", "Smethwick", "Oldbury"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across West Bromwich, from sole-trader climbers and groundsmen to small firms working Sandwell Valley Country Park, Dartmouth Park and the wider Black Country tree estate, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews who climb and clear the Black Country's trees",
  "s1loc":[
   "For an industrial town, West Bromwich carries a surprising amount of green, and the mature street, park and valley trees that thread through Sandwell keep a steady community of arborists and tree surgeons busy. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, and every one of them leans on proper chainsaw PPE to get through the day.",
   "The work follows the local geography. Suburbs like Charlemont, Hateley Heath and Great Barr carry mature garden and street trees, while Sandwell Valley Country Park holds mixed deciduous and coniferous woodland with sweet chestnuts over 200 years old, Priory Woods and Sot's Hole carry some of the oldest woodland in Sandwell, and Dartmouth Park's restored collection runs to 710 trees across 58 species, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. West Bromwich tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and ash dieback removal, TPO and conservation-area rules shape much of the work across Sandwell. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Across the Sandwell patch the firms are mostly small: a climber and a groundsman, a family business, a one or two-van outfit working West Bromwich, Wednesbury and out toward Walsall. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the borough's gardens, parks and valley woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across West Bromwich's gardens, Sandwell Valley Country Park and Dartmouth Park",
 },
 "edgware": {
  "region":"Edgware and the Barnet and Harrow border",
  "nearby":["Harrow", "Borehamwood", "Barnet"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Edgware, from sole-trader climbers and groundsmen to small firms working Edgwarebury Park, Stanmore Common and Scratchwood, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear north-west London's trees",
  "s1loc":[
   "Straddling the Barnet and Harrow border, Edgware is a leafy stretch of north-west London with a large estate of mature street, garden and parkland trees, and keeping it managed supports a busy community of arborists and tree surgeons. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, each of them dependent on proper chainsaw PPE.",
   "The work follows the suburb's green geography. Areas like Stanmore, Mill Hill and Canons Park carry mature oak, beech and estate trees, while Edgwarebury Park holds old hedgerows and ancient oak and ash plus a block planted by the Watling Chase Community Forest, and Stanmore Common, Harrow Weald Common and Scratchwood carry ancient woodland rich in hornbeam and wild service, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Edgware tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and TPO and conservation-area rules along with ash dieback shape much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Out across the Barnet and Harrow border the firms are mostly small: a climber and a groundsman, a family business, a one or two-van outfit working Edgware, Stanmore and out toward Borehamwood. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the suburb's gardens, parks and ancient woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Edgware's gardens, Edgwarebury Park and Stanmore Common",
 },
 "bury": {
  "region":"Bury and Greater Manchester",
  "nearby":["Radcliffe", "Heywood", "Whitefield"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Bury, from sole-trader climbers and groundsmen to small firms working Burrs Country Park, the Irwell valley and Redisher Wood below Holcombe Hill, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews who climb and clear Bury's trees",
  "s1loc":[
   "Set where Greater Manchester meets the West Pennine Moors, Bury is a green town with a large estate of mature street, park and valley trees, and managing it keeps a steady community of arborists and tree surgeons busy. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the town's river-valley geography. Areas like Whitefield, Radcliffe and Heywood carry mature street and garden trees, while Burrs Country Park holds 36 hectares of woodland and waterside along the River Irwell, the Irwell valley runs north as an urban country park, and Redisher Wood below Holcombe Hill is one of the best ancient woodland sites in the borough, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Bury tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and the council's own tree team, ash dieback and TPO and conservation-area rules shape much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Through the Irwell valley the firms are mostly small: a climber and a groundsman, a family business, a one or two-van outfit working Bury, Radcliffe and out toward Ramsbottom. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's gardens, parks and Irwell valley woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Bury's gardens, Burrs Country Park and the Irwell valley",
 },
 "tamworth": {
  "region":"Tamworth and Staffordshire",
  "nearby":["Lichfield", "Sutton Coldfield", "Cannock"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Tamworth, from sole-trader climbers and groundsmen to small firms working Hopwas Wood, the Castle Grounds and the Anker valley with Cannock Chase nearby, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Staffordshire's trees",
  "s1loc":[
   "Sitting where the Tame and Anker meet in south-east Staffordshire, Tamworth is a green town with a large estate of mature street, park and riverside trees, and managing it keeps a busy community of arborists and tree surgeons going. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, each of them dependent on proper chainsaw PPE.",
   "The work follows the town's wooded geography. The Castle Grounds carry mature parkland and avenue trees, Hopwas Wood and Hopwas Hays Wood hold around 385 acres of ancient woodland, and the Anker valley carries old oak and elm along the river and canal, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms, with the heaths and conifers of Cannock Chase a short run to the north.",
   "It is a safety-critical trade run to recognised standards. Tamworth tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and ash dieback along with TPO and conservation-area rules shape much of the work across Staffordshire. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Across the Tame and Anker valleys the firms are mostly small: a climber and a groundsman, a family business, a one or two-van outfit working Tamworth, Lichfield and out toward Sutton Coldfield. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's gardens, parks and valley woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Tamworth's gardens, Hopwas Wood and the Castle Grounds",
 },
 "chatham": {
  "region":"Chatham and Medway",
  "nearby":["Rochester", "Strood", "Sittingbourne"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Chatham, from sole-trader climbers and groundsmen to small firms working Capstone Farm Country Park, the Great Lines and the North Downs, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews who climb and clear Medway's trees",
  "s1loc":[
   "Rising from the Medway towns onto the chalk of the North Downs, Chatham carries a large estate of mature street, park and downland trees, and managing it keeps a steady community of arborists and tree surgeons busy. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the local geography. Capstone Farm Country Park holds woodland, meadow and waterside, the Great Lines Heritage Park carries open grassland and tree belts above the town, and the chalk slopes of the North Downs run south with beech, ash and yew, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for firms across Chatham, Rochester and Gillingham.",
   "It is a safety-critical trade run to recognised standards. Chatham tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and ash dieback along with TPO and conservation-area rules shape much of the work across Medway. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Out across the Medway towns the firms are mostly small: a climber and a groundsman, a family business, a one or two-van outfit working Chatham, Strood and out toward Sittingbourne. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the towns' gardens, parks and North Downs tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Chatham's gardens, Capstone Farm Country Park and the North Downs",
 },
 "paisley": {
  "region":"Paisley and Renfrewshire",
  "nearby":["Renfrew", "Glasgow", "Clydebank"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Paisley, from sole-trader climbers and groundsmen to small firms working Gleniffer Braes Country Park, Robertson Park and the wooded Renfrewshire braes, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews who climb and clear Renfrewshire's trees",
  "s1loc":[
   "A green town set against the Gleniffer Braes, Paisley carries a deep stock of mature street, park and estate trees, and looking after it keeps a steady community of arborists and tree surgeons busy across Renfrewshire. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, and every one of them leans on proper chainsaw PPE.",
   "The work follows the town's wooded geography. Gleniffer Braes Country Park spreads beech, sycamore, birch and oak over the braes south of town, while Robertson Park, Barshaw Park and woodland like Teucheen Wood at Inchinnan hold parkland and amenity trees, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Paisley tree surgeons are typically NPTC, City and Guilds and Lantra qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with NatureScot and Forestry and Land Scotland shaping the wider picture. Ash dieback has already pushed Renfrewshire Council into felling work, and phytophthora ramorum saw thousands of larch cleared at Gleniffer Braes, while Storm Eowyn left a heavy tail of windblown timber. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Most of these outfits are small: a climber and a groundsman, a family business, a one or two-van crew covering Paisley, Renfrew and the wider Renfrewshire patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the braes, parks and Renfrewshire woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Paisley's braes, parks and Renfrewshire woodland",
 },
 "carlisle": {
  "region":"Carlisle and Cumbria",
  "nearby":["Penrith", "Workington", "Whitehaven"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Carlisle, from sole-trader climbers and groundsmen to small firms working Rickerby Park, Kingmoor and the Eden valley on the edge of the Lake District, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Cumbria's trees",
  "s1loc":[
   "Set where the Eden meets the edge of the Lake District, Carlisle holds a broad estate of mature riverside, park and estate trees, and managing it keeps a busy community of arborists and tree surgeons working across north Cumbria. Most are sole traders and small teams handling domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the city's river and forest geography. Rickerby Park spreads mature trees along the meandering Eden, Kingmoor's old woodland nature reserve sits to the north, and the patch runs out through Stanwix and Wetheral to Armathwaite and the edge of Kershope Forest, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Carlisle tree surgeons are typically NPTC, City and Guilds and Lantra qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with Forestry England and the Woodland Trust active across the county. Ash dieback is set to take a large share of Cumbria's ash, and Storm Arwen left vast windblown timber across the north, keeping clearance work coming. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "The firms here run small: a climber and a groundsman, a family business, a one or two-van outfit covering Carlisle, Penrith and the Eden and Border patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the city's riverside, park and Eden valley tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Carlisle's riverside parks, the Eden valley and the edge of the Lake District",
 },
 "crewe": {
  "region":"Crewe and Cheshire",
  "nearby":["Sandbach", "Congleton", "Newcastle-under-Lyme"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Crewe, from sole-trader climbers and groundsmen to small firms working Queens Park, Wybunbury and the wooded Cheshire plain, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews who climb and clear Cheshire's trees",
  "s1loc":[
   "A railway town set in the green Cheshire plain, Crewe carries a solid estate of mature street, park and farmland trees, and keeping it in order supports a steady community of arborists and tree surgeons across south Cheshire. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the town's parkland and plain. Queens Park brings Victorian parkland and a woodland walk into the heart of Crewe, while Wybunbury, the lanes out to Sandbach and Holmes Chapel and the wooded hills around Congleton hold estate and farmland trees, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Crewe tree surgeons are typically NPTC, City and Guilds and Lantra qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with the Woodland Trust and Trees for Congleton active nearby. Ash dieback is a major driver, with millions of ash at risk across the region prompting inspections and safe removals, and rail and roadside vegetation around the junction adds steady work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "These outfits stay small: a climber and a groundsman, a family business, a one or two-van crew covering Crewe, Sandbach and the south Cheshire patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's parks, gardens and Cheshire plain tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Crewe's parks, gardens and the wooded Cheshire plain",
 },
 "bootle": {
  "region":"Bootle and Merseyside",
  "nearby":["Crosby", "Liverpool", "Wallasey"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Bootle, from sole-trader climbers and groundsmen to small firms working Derby Park, Rimrose Valley Country Park and the Mersey Forest, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Sefton's trees",
  "s1loc":[
   "A working town on the Mersey in the Metropolitan Borough of Sefton, Bootle mixes busy industrial and residential corridors with park and parkland trees, and looking after them keeps a community of arborists and tree surgeons busy across Merseyside. Most are sole traders and small teams handling domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the local green spaces. Derby Park brings Victorian parkland into the centre of Bootle, Rimrose Valley Country Park runs its green corridor between the canal and the railway, and the leafy suburbs of Crosby, Blundellsands and Waterloo and the woods around Little Crosby and Ince Blundell carry mature estate trees, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Bootle tree surgeons are typically NPTC, City and Guilds and Lantra qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with the Mersey Forest and the Woodland Trust shaping the wider canopy. Ash dieback and conservation-area and TPO rules across Sefton shape much of the work, and coastal storm clearance keeps emergency call-outs coming. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "The firms here run small: a climber and a groundsman, a family business, a one or two-van outfit covering Bootle, Crosby and the wider Sefton patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the borough's parks, valley and Mersey Forest tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Bootle's parks, Rimrose Valley and the Mersey Forest",
 },
 "harrogate": {
  "region":"Harrogate and North Yorkshire",
  "nearby":["Knaresborough", "Ripon", "York"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Harrogate, from sole-trader climbers and groundsmen to small firms working the Stray, Valley Gardens, the Pinewoods and the Crimple valley, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews who climb and clear North Yorkshire's trees",
  "s1loc":[
   "A leafy spa town on the edge of Nidderdale, Harrogate holds a rich estate of mature street, park and garden trees, and managing it keeps a busy community of arborists and tree surgeons working across North Yorkshire. Most are sole traders and small teams handling domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the town's green grain. The Stray spreads its protected parkland through the centre, the Valley Gardens and the 96-acre Pinewoods run out towards Harlow Carr and Birk Crag, and the Duchy Estate, the rural fringe above the Crimple valley and the patch out to Knaresborough and Ripon carry mature estate trees, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Harrogate tree surgeons are typically NPTC, City and Guilds and Lantra qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with the Woodland Trust and Forestry England active across the county. Ash dieback and fungal blight monitored in the Valley Gardens shape much of the work, along with conservation-area and TPO rules and the windblown timber left by Storm Arwen. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Most of these outfits are small: a climber and a groundsman, a family business, a one or two-van crew covering Harrogate, Knaresborough and the wider North Yorkshire patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's parks, gardens and Nidderdale tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Harrogate's Stray, gardens and the Crimple valley",
 },
 "maidenhead": {
  "region":"Maidenhead and Berkshire",
  "nearby":["Windsor", "Bracknell", "Slough"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Maidenhead, from sole-trader climbers and groundsmen to small firms working Maidenhead Thicket, Ockwells Park and the National Trust woodland at Cliveden and Pinkneys Green, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews who climb and clear Berkshire's trees",
  "s1loc":[
   "Set in well-wooded Thames-side Berkshire, Maidenhead carries a deep stock of mature street, park and estate trees, and keeping that estate safe supports a busy community of arborists and tree surgeons across the town and beyond. The trade here is overwhelmingly sole traders and small teams working domestic gardens, council and parkland contracts and storm clearance, and every one of them depends on proper chainsaw PPE.",
   "The work follows the local geography. Leafy suburbs like Pinkneys Green, Boyn Hill and the Cookhams carry mature oak, beech and garden trees, while Maidenhead Thicket holds broadleaf wooded common, Ockwells Park is managed woodland and meadow, and the National Trust ground at Cliveden and the Maidenhead and Cookham Commons runs to oak, larch and coppice, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Maidenhead tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and with TPOs and conservation-area controls across Cookham and the older suburbs shaping much of the work alongside ongoing ash dieback removals. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Most outfits stay small: a climber and a groundsman, a family business, a one or two-van firm working across Maidenhead, Windsor and the wider Berkshire patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's gardens, commons and woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Maidenhead's gardens, commons and Berkshire woodland",
 },
 "newcastle-under-lyme": {
  "region":"Newcastle-under-Lyme and Staffordshire",
  "nearby":["Kidsgrove", "Biddulph", "Stoke-on-Trent"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Newcastle-under-Lyme, from sole-trader climbers and groundsmen to small firms working Apedale Country Park, Bradwell Wood and the regenerating woodland of the north Staffordshire coalfield, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear north Staffordshire's trees",
  "s1loc":[
   "On the edge of the Staffordshire Potteries, Newcastle-under-Lyme mixes mature town and suburban trees with the recovering woodland of an old coalfield, and looking after it keeps a steady community of arborists and tree surgeons busy across the borough and into Stoke-on-Trent. Most are sole traders and small teams working domestic gardens, council and country-park contracts and storm clearance, every one of them reliant on proper chainsaw PPE.",
   "The work follows the local ground. Suburbs like Westlands, Clayton and Wolstanton carry mature garden and street trees, while Apedale Community Country Park holds 184 hectares of reclaimed woodland, meadow and pools, Bradwell Wood runs to broadleaf cover, and Silverdale Country Park is young woodland regrown over a former colliery, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Newcastle tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with TPOs, conservation areas and ongoing ash dieback removals across the borough shaping much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "And the firms mostly stay small: a climber and a groundsman, a family business, a one or two-van outfit working across Newcastle, Kidsgrove and the wider north Staffordshire patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the borough's gardens, parks and reclaimed woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Newcastle-under-Lyme's gardens, country parks and north Staffordshire woodland",
 },
 "burnley": {
  "region":"Burnley and Lancashire",
  "nearby":["Nelson", "Accrington", "Colne"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Burnley, from sole-trader climbers and groundsmen to small firms working Towneley Park, the Forest of Burnley and the South Pennine moors, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews who climb and clear Lancashire's trees",
  "s1loc":[
   "Wrapped by the South Pennine moors, Burnley holds a substantial estate of park, valley and street trees alongside large areas of created and restored woodland, and managing it keeps a busy community of arborists and tree surgeons working across the town and the wider Pennine Lancashire patch. Most are sole traders and small teams handling domestic gardens, council and parkland contracts and storm clearance, all of them dependent on proper chainsaw PPE.",
   "The work follows the local geography. Villages and suburbs like Worsthorne, Cliviger and Reedley carry mature garden and field trees, while Towneley Park runs to 180 hectares of parkland and woodland walks, and the Forest of Burnley covers some 430 hectares of native woodland with over a million trees planted since 1997, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Burnley tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with exposed Pennine sites, storm damage from events like Arwen and ongoing ash dieback shaping much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Outfits here mostly stay small: a climber and a groundsman, a family business, a one or two-van firm working across Burnley, Nelson, Colne and the wider East Lancashire patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's parks, woodland and Pennine tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Burnley's parks, created woodland and Pennine moors",
 },
 "enfield": {
  "region":"Enfield and North London",
  "nearby":["Barnet", "Cheshunt", "Potters Bar"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Enfield, from sole-trader climbers and groundsmen to small firms working Trent Park, Forty Hall and the ancient woodland of Whitewebbs, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear North London's trees",
  "s1loc":[
   "Greenest of the North London boroughs by ambition, Enfield carries a large estate of street, park and ancient woodland trees on the old ground of Enfield Chase, and keeping it safe supports a busy community of arborists and tree surgeons across the borough and into Hertfordshire. Most are sole traders and small teams working domestic gardens, council and country-park contracts and storm clearance, every one of them reliant on proper chainsaw PPE.",
   "The work follows the local geography. Suburbs like Winchmore Hill, Hadley Wood and Cockfosters carry mature oak, hornbeam and garden trees, while Trent Park runs to some 400 acres of meadow, lake and ancient woodland, Forty Hall stands in its own parkland estate, and Whitewebbs Wood holds oak, hornbeam and holly on remnant Enfield Chase ground, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Enfield tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with conservation areas at Hadley Wood and Winchmore Hill, widespread TPOs and the high-profile felling of an ancient oak at Whitewebbs all underlining how tightly tree work is scrutinised here. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Most firms here stay small: a climber and a groundsman, a family business, a one or two-van outfit working across Enfield, Barnet and the wider North London and Hertfordshire fringe. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the borough's gardens, parks and ancient woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Enfield's gardens, country parks and ancient Chase woodland",
 },
 "gravesend": {
  "region":"Gravesend and Kent",
  "nearby":["Dartford", "Strood", "Rochester"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Gravesend, from sole-trader climbers and groundsmen to small firms working Shorne Woods Country Park, Cobham Wood and the Thames marshes, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews who climb and clear north Kent's trees",
  "s1loc":[
   "Strung along the Thames in north Kent, Gravesend backs onto a belt of ancient woodland, estate parkland and estuarine marsh, and managing those trees keeps a steady community of arborists and tree surgeons busy across the town and the wider Gravesham patch. Most are sole traders and small teams working domestic gardens, council and country-park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the local geography. Suburbs like Riverview Park and Northfleet carry mature garden and street trees, while Shorne Woods Country Park runs to some 300 acres of woodland, wetland and meadow on the old Cobham Hall Estate, the National Trust's Cobham Wood and the Woodland Trust's Ashenbank Wood hold ancient and veteran oak, sweet chestnut and wood pasture, and Jeskyns Community Woodland adds new planting, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Gravesend tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with veteran-tree management around Cobham, ongoing ash dieback removals and TPO and conservation-area rules shaping much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Outfits here mostly stay small: a climber and a groundsman, a family business, a one or two-van firm working across Gravesend, Rochester and the wider north Kent patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's gardens, country parks and marshland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Gravesend's gardens, ancient woodland and Thames marshes",
 },
 "east kilbride": {
  "region":"East Kilbride and South Lanarkshire",
  "nearby":["Hamilton", "Rutherglen", "Motherwell"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across East Kilbride, from sole-trader climbers and groundsmen to small firms working the wooded gorge of Calderglen Country Park, James Hamilton Heritage Park and the wider South Lanarkshire treescape, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews who climb and clear Lanarkshire's trees",
  "s1loc":[
   "As Scotland's first new town, East Kilbride was planted green from the start, and the oak, beech, sycamore and ash set out in its 1950s and 1960s estates have now reached maturity, keeping a steady community of arborists and tree surgeons busy across the town and the wider South Lanarkshire patch. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the town's green geography. Residential precincts like Calderwood, The Murray, St Leonards, Westwood and newer suburbs such as Stewartfield and Lindsayfield carry mature estate and street trees, while Calderglen Country Park holds 33 hectares of designated woodland along the wooded gorge of the Rotten Calder Water, and James Hamilton Heritage Park adds open parkland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. East Kilbride tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with Forestry and Land Scotland and NatureScot shaping the wider woodland picture and ash dieback driving survey and removal work across South Lanarkshire's ash stock. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Most of these outfits stay small: a climber and a groundsman, a family business, a one or two-van team working across East Kilbride, Hamilton and the wider Lanarkshire ground. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's gardens, parks and wooded gorge tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across East Kilbride's gardens, parks and the wooded Calderglen gorge",
 },
 "south shields": {
  "region":"South Shields and South Tyneside",
  "nearby":["Jarrow", "North Shields", "Tynemouth"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across South Shields, from sole-trader climbers and groundsmen to small firms working the Leas, Cleadon Hills and the leafy Westoe and Whitburn streets, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear South Tyneside's trees",
  "s1loc":[
   "Coastal and green at once, South Shields carries a large estate of mature street, park and garden trees, and looking after it keeps a busy community of arborists and tree surgeons working across the town and the wider South Tyneside borough. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the town's leafy geography. Westoe carries Georgian and Victorian estate trees, Cleadon and Whitburn add tree-lined village streets and mature canopy on the green belt, and Readhead Park, the Cleadon Hills and the National Trust's the Leas above Marsden generate crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. South Shields tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members. Storm Arwen hit South Tyneside as its worst storm since 1954, bringing down an unprecedented number of trees at 163 reported locations and prompting the council to rebuild its tree risk management, so windblow and deadwood work still runs alongside ash dieback and TPO and conservation-area rules. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Outfits here are mostly small: a climber and a groundsman, a family business, a one or two-van team working across South Shields, Jarrow and the wider South Tyneside coast. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's gardens, parks and coastal woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across South Shields's gardens, the Cleadon Hills and the Leas",
 },
 "burton-on-trent": {
  "region":"Burton-on-Trent and Staffordshire",
  "nearby":["Lichfield", "Tamworth", "Derby"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Burton-on-Trent, from sole-trader climbers and groundsmen to small firms working the National Forest, Branston Water Park and Sinai Park woods, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews who climb and clear the National Forest's trees",
  "s1loc":[
   "Sitting inside the maturing National Forest, Burton-on-Trent has a growing estate of street, park, riverside and young plantation trees, and managing it keeps a busy community of arborists and tree surgeons working across the town and the wider east Staffordshire patch. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the town's green geography. Middle-class suburbs like Stapenhill and Winshill carry mature estate and street trees, Stapenhill Gardens, Tower Woods and the riverside Washlands add parkland, and Branston Water Park, the hilltop Sinai Park woods of Shobnall Wood and The Rough, and the wider National Forest planting all generate crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Burton tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with the National Forest and Woodland Trust shaping the wider woodland picture and ash dieback driving survey and removal work across Staffordshire's ash. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "The firms tend to stay small: a climber and a groundsman, a family business, a one or two-van outfit working across Burton, Branston and the wider National Forest ground. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's gardens, parks and National Forest tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Burton's gardens, the Washlands and the National Forest",
 },
 "shrewsbury": {
  "region":"Shrewsbury and Shropshire",
  "nearby":["Telford", "Oswestry", "Stafford"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Shrewsbury, from sole-trader climbers and groundsmen to small firms working the Quarry park, the Severn loop and wooded Haughmond Hill, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Shropshire's trees",
  "s1loc":[
   "Wrapped in a loop of the River Severn, Shrewsbury is a green county town with a large estate of mature street, park and riverside trees, and looking after it keeps a busy community of arborists and tree surgeons working across the town and the wider Shropshire patch. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the town's riverside geography. The Quarry park and its sunken Dingle gardens carry historic lime trees inside the Severn loop, suburbs like Sundorne and the streets along the river hold mature estate and garden trees, and wooded Haughmond Hill to the north east and the National Trust's Attingham Park estate add woodland and parkland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Shrewsbury tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members. Shrewsbury Town Council and Shropshire Council survey ash annually and fell where needed, so ash dieback drives a steady stream of removals alongside TPO and conservation-area rules. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Most outfits here are small: a climber and a groundsman, a family business, a one or two-van team working across Shrewsbury, Atcham and the wider Shropshire ground. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's gardens, riverside parks and woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Shrewsbury's Quarry park, the Severn loop and Haughmond Hill",
 },
 "rugby": {
  "region":"Rugby and Warwickshire",
  "nearby":["Nuneaton", "Leamington Spa", "Daventry"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Rugby, from sole-trader climbers and groundsmen to small firms working Draycote Water, Newbold Quarry and the Great Central Way, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews who climb and clear Warwickshire's trees",
  "s1loc":[
   "Set in green Warwickshire countryside, Rugby carries a large estate of mature street, park and garden trees, and managing it keeps a busy community of arborists and tree surgeons working across the town and the wider county patch. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the town's leafy geography. Suburbs like Bilton, Hillmorton and Newbold-on-Avon carry mature estate and street trees, Caldecott Park holds town-centre canopy rebuilt after Dutch elm disease, and the ash and sycamore woodland around Newbold Quarry, the reservoir margins at Draycote Water and the tree-lined former railway of the Great Central Way all generate crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Rugby tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with the Warwickshire Wildlife Trust and Woodland Trust shaping the wider woodland picture and ash dieback driving survey and removal work across the county's ash. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "The firms here tend to stay small: a climber and a groundsman, a family business, a one or two-van outfit working across Rugby, Bilton and the wider Warwickshire ground. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's gardens, parks and quarry woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Rugby's parks, Newbold Quarry and the Great Central Way",
 },
 "stafford": {
  "region":"Stafford and Staffordshire",
  "nearby":["Cannock", "Rugeley", "Stoke-on-Trent"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Stafford, from sole-trader climbers and groundsmen to small firms working the Cannock Chase fringe, the Shugborough estate parkland and Doxey Marshes willows, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews who climb and clear Staffordshire's trees",
  "s1loc":[
   "A historic county town with the River Sow running through it, Stafford carries a heavy estate of mature street, park and estate trees, and keeping it managed supports a steady community of arborists and tree surgeons across the borough and wider Staffordshire. The bulk are sole traders and small teams on domestic gardens, council and estate contracts and storm clearance, and not one of them works a chainsaw without proper PPE.",
   "The work tracks the town's leafy geography. Suburbs like Baswich, Milford, Brocton, Weeping Cross and Castlechurch carry mature oak, beech and tree-lined streets, while the Shugborough estate's ancient woodland and parkland, the pollarded willows of Doxey Marshes and the Scots pine and silver birch edge of Cannock Chase AONB all generate crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Stafford tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with ash dieback and TPO and conservation-area rules shaping a lot of the workload. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Most outfits here stay small: a climber and a groundsman, a family firm, a one or two-van team working across Stafford, Penkridge, Eccleshall and the Chase-fringe villages. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's gardens, estate parkland and Chase-edge tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Stafford's gardens, the Shugborough estate and the Cannock Chase fringe",
 },
 "taunton": {
  "region":"Taunton and Somerset",
  "nearby":["Bridgwater", "Wellington", "Yeovil"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Taunton, from sole-trader climbers and groundsmen to small firms working Vivary Park, the Quantock Hills and the Neroche woodlands of the Blackdown Hills, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Gearing up the people who climb and clear Somerset's trees",
  "s1loc":[
   "Sitting in its vale between the Quantocks and the Blackdowns, Taunton is a green county town with a deep stock of mature street, park and estate trees, and looking after it keeps a busy community of arborists and tree surgeons working across the town and the wider Somerset patch. Most are sole traders and small teams on domestic gardens, council and parkland contracts and storm clearance, every one of them reliant on proper chainsaw PPE.",
   "The work follows the local landscape. Vivary Park's mature avenues and the leafy roads around Comeytrowe, Trull and Bishops Hull carry oak, lime and beech, while the Quantock Hills, the Blackdown Hills AONB and the Neroche woodlands managed by Forestry England above Taunton Vale hold parkland and woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Taunton tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with widespread ash dieback across the Blackdowns and TPO and conservation-area rules driving much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "The firms here are mostly small outfits: a climber and a groundsman, a family business, a one or two-van team working across Taunton, Wellington, Bridgwater and the Quantock and Blackdown fringe. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's parks, the Quantocks and the Blackdown woodlands",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Taunton's parks, the Quantock Hills and the Neroche woodlands",
 },
 "tynemouth": {
  "region":"Tynemouth and North Tyneside",
  "nearby":["North Shields", "Whitley Bay", "South Shields"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Tynemouth, from sole-trader climbers and groundsmen to small firms working Northumberland Park, the coastal denes and the wider North Tyneside tree stock, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Backing the crews who climb and clear North Tyneside's trees",
  "s1loc":[
   "Perched on the North Sea coast where the Tyne meets the sea, Tynemouth pairs salt-blown seafront with sheltered, leafy denes, and managing that tree stock keeps a tight community of arborists and tree surgeons busy across North Tyneside. Most are sole traders and small teams on domestic gardens, council and park contracts and storm clearance, and every one of them depends on proper chainsaw PPE.",
   "The work follows the coast's wooded pockets. Northumberland Park, the sheltered dene cut by the Pow Burn between Tynemouth and North Shields, carries mature woodland including the Duke's old Turkey Oak, while the leafy streets of Tynemouth, Cullercoats and Whitley Bay and the denes running down to the coast hold the rest, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Tynemouth tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with Storm Arwen having flattened thousands of trees across the North East in 2021 and ash dieback now thinning the denes. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Outfits here run small: a climber and a groundsman, a family business, a one or two-van team working across Tynemouth, North Shields, Whitley Bay and the wider North Tyneside coast. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the borough's parks, coastal denes and storm-damaged tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Tynemouth's parks, coastal denes and the North Tyneside seafront",
 },
 "cannock": {
  "region":"Cannock and Staffordshire",
  "nearby":["Rugeley", "Burntwood", "Lichfield"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Cannock, from sole-trader climbers and groundsmen to small firms working the Cannock Chase AONB heath, the Birches Valley conifer plantations and the oak and birch of the Chase edge, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Equipping the people who climb and clear the Cannock Chase fringe",
  "s1loc":[
   "Set hard against Cannock Chase AONB, Cannock is a town defined by trees, with mature street, garden and Chase-edge stock that keeps a steady community of arborists and tree surgeons working across the district and wider Staffordshire. Most are sole traders and small teams on domestic gardens, council contracts and storm clearance, and not one of them runs a chainsaw without proper PPE.",
   "The work follows the Chase. Suburbs like Hednesford, Heath Hayes, Huntington and Brocton carry mature oak, conifers and oversized garden trees, while Cannock Chase AONB itself, with its open heathland, Scots pine and silver birch, the Birches Valley conifer plantations managed by Forestry England and a herd of around 800 fallow deer, frames the wider landscape, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Cannock tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with structurally compromised Chase-edge oaks, short-lived birch and TPO and conservation-area rules shaping the work, and the Chase land itself only touched on written instruction from Forestry England. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Trade here is mostly small outfits: a climber and a groundsman, a family business, a one or two-van team working across Cannock, Hednesford, Rugeley, Burntwood and the Chase fringe. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the district's gardens, heath and Chase-edge tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Cannock's gardens, the Chase heath and the Birches Valley plantations",
 },
 "farnborough": {
  "region":"Farnborough and Hampshire",
  "nearby":["Aldershot", "Camberley", "Fleet"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Farnborough, from sole-trader climbers and groundsmen to small firms working Caesar's Camp, the Blackwater valley woodland and the pine and heath around Fleet Pond, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews who climb and clear north Hampshire's trees",
  "s1loc":[
   "Wrapped around heath, pine ridge and the Blackwater valley, Farnborough carries a substantial stock of mature street, garden and estate trees, and keeping it managed supports a busy community of arborists and tree surgeons across the town and the wider north Hampshire patch. The majority are sole traders and small teams on domestic gardens, council contracts and storm clearance, every one of them reliant on proper chainsaw PPE.",
   "The work follows the local geography. Leafy roads around the town, Caesar's Camp and the wooded Aldershot training-area ridge, the Swan Inn woods and the Blackwater valley running down to Fleet Pond, the largest freshwater lake in Hampshire, carry oak, beech, Scots pine and birch, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Farnborough tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with ash dieback, the Thames Basin Heaths protections and TPO and conservation-area rules shaping much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Firms here stay small: a climber and a groundsman, a family business, a one or two-van team working across Farnborough, Aldershot, Fleet, Camberley and the Blackwater valley. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's gardens, heath ridge and Blackwater valley tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Farnborough's gardens, Caesar's Camp and the Blackwater valley woodland",
 },
 "torquay": {
  "region":"Torquay and Devon",
  "nearby":["Paignton", "Newton Abbot", "Exmouth"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Torquay, from sole-trader climbers and groundsmen to small firms working Cockington Country Park, Manscombe Woods and the leafy Lincombes, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews who climb and clear the English Riviera's trees",
  "s1loc":[
   "On the English Riviera, Torquay is a green, sheltered town where palms and Mediterranean planting sit alongside mature broadleaf, and looking after that canopy keeps a steady community of arborists and tree surgeons busy across Torbay. Most are sole traders and small teams on domestic gardens, council park work and storm clearance, and every one of them depends on proper chainsaw PPE.",
   "The work follows the town's leafy geography. Conservation-area suburbs like Wellswood, the Lincombes and Maidencombe carry mature oak, beech and estate trees, while Cockington Country Park, Manscombe Woods, Tessier Gardens and Babbacombe Downs hold parkland and woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Torquay tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with Torbay's sixteen conservation areas, area TPOs and ongoing ash dieback shaping much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "And the firms here stay small: a climber and a groundsman, a family business, a one or two-van outfit working across Torquay, Paignton and the wider Torbay patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's gardens, parks and coastal woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Torquay's gardens, country parks and Torbay woodland",
 },
 "inverness": {
  "region":"Inverness and the Highlands",
  "nearby":["Elgin", "Aberdeen", "Perth"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Inverness, from sole-trader climbers and groundsmen to small firms working the Ness Islands, Craig Phadrig and the Caledonian pinewoods along Loch Ness, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear the Highlands' trees",
  "s1loc":[
   "Set where the River Ness meets the firth, Inverness is a green Highland capital ringed by native pine, birch and broadleaf, and managing that estate keeps a hardy community of arborists and tree surgeons busy across a remote, scattered patch. Most are sole traders and small teams on domestic gardens, estate work and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the town's wooded geography. Suburbs like the Crown, Drummond and Culloden carry mature street and garden trees, while the Ness Islands, Craig Phadrig forest and the Caledonian pinewoods along Loch Ness hold parkland and woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Inverness tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, often alongside Forestry and Land Scotland and NatureScot, with windblow from storms like Arwen, Dutch elm disease on Culloden Drive and ash dieback all shaping the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "And the firms stay small here: a climber and a groundsman, a family business, a one or two-van outfit working across Inverness, the Black Isle and out towards Nairn and Loch Ness. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's gardens, riverside parks and Highland woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Inverness's gardens, the Ness Islands and Highland pinewoods",
 },
 "wrexham": {
  "region":"Wrexham and north Wales",
  "nearby":["Oswestry", "Buckley", "Ellesmere Port"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Wrexham, from sole-trader climbers and groundsmen to small firms working Erddig parkland, Alyn Waters Country Park and the Clywedog valley, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews who climb and clear north Wales' trees",
  "s1loc":[
   "Sitting between the Dee valley and the Welsh hills, Wrexham is a green town with a deep stock of mature park, estate and street trees, and looking after it keeps a busy community of arborists and tree surgeons working across the county borough. Most are sole traders and small teams on domestic gardens, council and estate contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the town's leafy geography. Suburbs and villages like Marford, Gresford and Rhostyllen carry mature oak, beech and estate trees, while Erddig's National Trust parkland above the Clywedog, Alyn Waters Country Park and the wooded Clywedog Valley Trail hold parkland and woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Wrexham tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, often alongside Natural Resources Wales and Coed Cymru, with ash dieback and acute oak decline running through the region and TPO and conservation-area rules shaping much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "And the firms stay small in this patch: a climber and a groundsman, a family business, a one or two-van outfit working across Wrexham, the Alyn valley and out towards Oswestry and the border. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's gardens, country parks and valley woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Wrexham's gardens, Erddig parkland and the Clywedog valley",
 },
 "loughborough": {
  "region":"Loughborough and Leicestershire",
  "nearby":["Coalville", "Melton Mowbray", "Leicester"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Loughborough, from sole-trader climbers and groundsmen to small firms working the Outwoods, Beacon Hill and the wider Charnwood Forest, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Charnwood's trees",
  "s1loc":[
   "On the edge of Charnwood Forest, Loughborough is a green Leicestershire town with mature beech, sycamore and oak across its streets, parks and surrounding woodland, and managing it keeps a steady community of arborists and tree surgeons busy. Most are sole traders and small teams on domestic gardens, council contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the town's wooded geography. Suburbs like Shelthorpe and Nanpantan run up to the ancient ground of the Outwoods, Beacon Hill Country Park, Buddon Wood and the wider Charnwood Forest and National Forest, with the Soar Valley running through, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Loughborough tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with National Forest planting, ash dieback and TPO and conservation-area rules shaping much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "And the firms here are mostly small: a climber and a groundsman, a family business, a one or two-van outfit working across Loughborough, Shepshed and the wider Charnwood patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's gardens, parks and Charnwood woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Loughborough's gardens, the Outwoods and Charnwood Forest",
 },
 "stourbridge": {
  "region":"Stourbridge and the West Midlands",
  "nearby":["Halesowen", "Brierley Hill", "Kingswinford"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Stourbridge, from sole-trader climbers and groundsmen to small firms working Mary Stevens Park, Wollescote and the nearby Clent Hills, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews who climb and clear the Black Country's trees",
  "s1loc":[
   "On the leafy western edge of the Black Country, Stourbridge is a greener corner of the West Midlands with mature park, garden and estate trees, and looking after them keeps a busy community of arborists and tree surgeons working across the town and into Worcestershire. Most are sole traders and small teams on domestic gardens, council contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the town's leafy geography. Suburbs like Pedmore, Norton and Wollaston carry mature oak, beech and estate trees, while Mary Stevens Park, Stevens Park at Wollescote and the wooded slopes of the National Trust's Clent Hills, with their beech, oak and Scots pine, hold parkland and woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Stourbridge tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with ash dieback and TPO and conservation-area rules shaping much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "And the firms stay small here: a climber and a groundsman, a family business, a one or two-van outfit working across Stourbridge, Wordsley and the wider Halesowen and Kingswinford patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's gardens, parks and Clent Hills woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Stourbridge's gardens, Mary Stevens Park and the Clent Hills",
 },
 "ellesmere port": {
  "region":"Ellesmere Port and Cheshire West",
  "nearby":["Bebington", "Neston", "Runcorn"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Ellesmere Port, from sole-trader climbers and groundsmen to small firms working Rivacre Valley, Stanney Woods and the wider Mersey Forest, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews who climb and clear Cheshire's trees",
  "s1loc":[
   "Sitting on the Mersey and Dee edge of the Wirral, Ellesmere Port carries a green mix of mature street, park and estate trees, and looking after it keeps a steady community of arborists and tree surgeons busy across the town and west Cheshire. Most are sole traders and small teams on domestic gardens, council and country park contracts and storm clearance, and every one of them leans on proper chainsaw PPE.",
   "The work tracks the local geography. Suburbs like Whitby, Wolverham, Overpool, Great Sutton and Little Sutton carry mature oak, beech and garden trees, while Rivacre Valley Country Park, Stanney Woods ancient woodland of oak and silver birch, Whitby Park and the Wirral Way hold parkland and woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Ellesmere Port tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with ash dieback across the Mersey Forest and TPO and conservation-area rules shaping much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Most of these outfits are small by nature: a climber and a groundsman, a family business, a one or two-van team working across Ellesmere Port, Neston and the wider Cheshire West patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's gardens, parks and Mersey Forest woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Ellesmere Port's gardens, Rivacre Valley and Stanney Woods",
 },
 "dewsbury": {
  "region":"Dewsbury and West Yorkshire",
  "nearby":["Batley", "Mirfield", "Ossett"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Dewsbury, from sole-trader climbers and groundsmen to small firms working Crow Nest Park, Dewsbury Country Park and the Calder valley woodland, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Kirklees trees",
  "s1loc":[
   "Set on the hills above the Calder valley, Dewsbury holds a large estate of mature park, street and garden trees, and managing it keeps a busy community of arborists and tree surgeons working across the town and the wider Kirklees patch. Most are sole traders and small teams on domestic gardens, council and park contracts and storm clearance, each of them dependent on proper chainsaw PPE.",
   "The work follows the valley geography. Crow Nest Park sits above the Calder with its retained tree belts and copses, while Dewsbury Country Park is being planted as the largest new woodland in West Yorkshire with the Woodland Trust, and Wilton Park in Batley, Hagg Wood and Ings Grove Park around Mirfield and Green Park in Ossett carry parkland and woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Dewsbury tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with ash dieback common across the Calder valley and TPO and conservation-area rules shaping much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "These firms tend to stay small: a climber and a groundsman, a family business, a one or two-van outfit working across Dewsbury, Batley, Mirfield and Ossett. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's parks, country park and Calder valley woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Dewsbury's Crow Nest Park, country park and Calder valley woodland",
 },
 "widnes": {
  "region":"Widnes and Halton",
  "nearby":["Runcorn", "St Helens", "Warrington"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Widnes, from sole-trader climbers and groundsmen to small firms working Victoria Park, Pickerings Pasture and the Mersey gateway woodland, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews who climb and clear Halton's trees",
  "s1loc":[
   "On the north bank of the Mersey gateway, Widnes blends an industrial backdrop with valued green space and a large estate of mature park and street trees, and looking after it keeps a steady community of arborists and tree surgeons busy across the town and the Halton borough. Most are sole traders and small teams on domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the riverside geography. Victoria Park with its lake and formal gardens, Pickerings Pasture local nature reserve, Spike Island, Pex Hill Nature Reserve, Sunnybank Woodland Park and the Hale Road woodlands carry parkland and woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms as the Big Halton Forest and the Mersey Forest add to the canopy.",
   "It is a safety-critical trade run to recognised standards. Widnes tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with riverside wind exposure, ash dieback and TPO and conservation-area rules shaping much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Most of these outfits are small: a climber and a groundsman, a family business, a one or two-van team working across Widnes, Runcorn and the wider Halton patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's parks, riverside reserves and Mersey gateway woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Widnes's Victoria Park, Pickerings Pasture and Mersey gateway woodland",
 },
 "runcorn": {
  "region":"Runcorn and Halton",
  "nearby":["Widnes", "Warrington", "Ellesmere Port"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Runcorn, from sole-trader climbers and groundsmen to small firms working Town Park, Wigg Island and the Bridgewater Canal woodland, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Halton's trees",
  "s1loc":[
   "Wrapped around the Mersey and the Manchester Ship Canal, Runcorn carries a green mix of mature park, street and estate trees, and managing it keeps a busy community of arborists and tree surgeons working across the town and the Halton borough. Most are sole traders and small teams on domestic gardens, council and park contracts and storm clearance, each of them dependent on proper chainsaw PPE.",
   "The work tracks the local geography. Town Park forms a wooded core in the New Town, while Wigg Island Community Park between the Mersey and the Ship Canal, the woodland below Halton Castle, Runcorn Hill Park, Murdishaw Valley and the green corridor of the Bridgewater Canal hold parkland and woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms as the Big Halton Forest and the Mersey Forest add new planting.",
   "It is a safety-critical trade run to recognised standards. Runcorn tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with ash dieback and TPO and conservation-area rules shaping much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "These firms are mostly small: a climber and a groundsman, a family business, a one or two-van outfit working across Runcorn, Widnes, Warrington and the wider Halton patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's parks, canal corridor and Mersey woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Runcorn's Town Park, Wigg Island and the Bridgewater Canal woodland",
 },
 "rochester": {
  "region":"Rochester and Medway",
  "nearby":["Chatham", "Strood", "Gravesend"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Rochester, from sole-trader climbers and groundsmen to small firms working Capstone Farm Country Park, the Esplanade and the North Downs woodland, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews who climb and clear Medway's trees",
  "s1loc":[
   "Strung along the Medway beneath the North Downs, Rochester holds a large estate of mature street, park and garden trees, and looking after it keeps a steady community of arborists and tree surgeons busy across the town and the wider Medway towns. Most are sole traders and small teams on domestic gardens, council and country park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the Downs geography. Suburbs like Borstal, The Delce and Frindsbury carry mature oak, beech and garden trees, while Capstone Farm Country Park with its ancient woodland, the riverside Esplanade, Broom Wood, Ranscombe Farm and the wider North Kent Woods and Downs hold parkland and ancient woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Rochester tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with ash dieback heavy across the Kent Downs and TPO and conservation-area rules shaping much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Most of these outfits stay small: a climber and a groundsman, a family business, a one or two-van team working across Rochester, Chatham, Strood and the wider Medway patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's gardens, country park and North Downs woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Rochester's Capstone Farm Country Park, the Esplanade and the North Downs woodland",
 },
 "twickenham": {
  "region":"Twickenham and south-west London",
  "nearby":["Kingston upon Thames", "Feltham", "Hounslow"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Twickenham, from sole-trader climbers and groundsmen to small firms working Bushy Park, Marble Hill, Crane Park and the leafy Thames-side suburbs, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews who climb and clear south-west London's riverside trees",
  "s1loc":[
   "Few corners of London are as green as Twickenham, where a mature estate of street, park and riverside trees keeps a busy community of arborists and tree surgeons at work across the borough of Richmond upon Thames. Most are sole traders and small teams on domestic gardens, council and park contracts and storm clearance, and every one of them depends on proper chainsaw PPE.",
   "The work follows the Thames-side geography. Suburbs like Strawberry Hill, St Margarets, Whitton and Twickenham Green carry mature oak, beech and garden trees, while Bushy Park with its veteran oaks, Marble Hill, Crane Park along the River Crane, Twickenham Rough and the National Nature Reserve woods at Petersham hold parkland and ancient trees, all generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Twickenham tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and with more than 16,000 council street trees plus dense TPO and conservation-area cover at Strawberry Hill and St Margarets, the rules shape much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Most of these outfits stay small: a climber and a groundsman, a family business, a one or two-van team working across Twickenham, Teddington, Hampton and the wider Richmond patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the borough's gardens, royal parks and riverside tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Twickenham's gardens, riverside parks and Bushy Park woodland",
 },
 "scarborough": {
  "region":"Scarborough and the North Yorkshire coast",
  "nearby":["Bridlington", "York", "Beverley"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Scarborough, from sole-trader climbers and groundsmen to small firms working Raincliffe Woods, Peasholm Park and the North York Moors and Dalby Forest fringe, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear the Yorkshire coast's trees",
  "s1loc":[
   "On the North Yorkshire coast, Scarborough carries a surprising amount of tree cover for a seaside town, and managing its street, park and valley trees keeps a steady community of arborists and tree surgeons busy across the town and its rural hinterland. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the local geography. Suburbs and districts like South Cliff, Falsgrave and Oliver's Mount carry mature garden and parkland trees, while Raincliffe and Forge Valley Woods, a 222-hectare community woodland and National Nature Reserve on the town's edge, Peasholm Park and the Dalby Forest and North York Moors fringe hold woodland and parkland, all generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Scarborough tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and ash dieback runs heavily through Yorkshire's woods and roadside trees, driving felling and survey work for North Yorkshire Council. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "These firms tend to be small: a climber and a groundsman, a family business, a one or two-van outfit working across Scarborough, Filey, Whitby and the wider North Yorkshire coast. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the coast's gardens, parks and valley woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Scarborough's gardens, parks and Raincliffe Woods",
 },
 "orpington": {
  "region":"Orpington and the London Borough of Bromley",
  "nearby":["Bromley", "Sidcup", "Sevenoaks"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Orpington, from sole-trader climbers and groundsmen to small firms working High Elms, Scadbury Park, the Cudham valley and the borough's ancient woodland, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews who climb and clear Bromley's wooded edge",
  "s1loc":[
   "Out on the leafy south-east edge of London, Orpington sits where the Bromley borough meets the North Downs, and its large estate of mature street, garden and woodland trees keeps a busy community of arborists and tree surgeons at work. Most are sole traders and small teams on domestic gardens, council and park contracts and storm clearance, and every one of them depends on proper chainsaw PPE.",
   "The work follows the wooded geography. Petts Wood, Chelsfield and Green Street Green carry mature oak and estate trees, while High Elms Country Park with its 250 acres of broadleaved woodland on the North Downs, Scadbury Park ancient woodland and the deep Cudham valley hold parkland and ancient trees, all generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Orpington tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and with the SSSI woodland at High Elms, widespread ash dieback and dense TPO and conservation-area cover, the rules shape much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Most of these outfits are small: a climber and a groundsman, a family business, a one or two-van team working across Orpington, Petts Wood, Chislehurst and into the Sevenoaks fringe. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the borough's gardens, country parks and ancient woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Orpington's gardens, country parks and High Elms woodland",
 },
 "wallasey": {
  "region":"Wallasey and the Wirral",
  "nearby":["Birkenhead", "Bebington", "Heswall"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Wallasey, from sole-trader climbers and groundsmen to small firms working Central Park, Bidston Hill and the North Wirral coast, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear the Wirral's trees",
  "s1loc":[
   "Up on the Wirral peninsula, Wallasey holds a good spread of park, street and woodland trees within the wider Mersey Forest, and managing them keeps a steady community of arborists and tree surgeons busy across the borough. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the peninsula's geography. Wallasey Village and Liscard carry mature garden and street trees, while Central Park with its Green Flag woodland walks, the heath and woodland of Bidston Hill, Bidston Moss community woodland and the North Wirral coast hold parkland and trees, all generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Wallasey tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and ash dieback and Meripilus run through Wirral's woods under the council's own ash dieback policy, driving felling and survey work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "These firms tend to be small: a climber and a groundsman, a family business, a one or two-van outfit working across Wallasey, Birkenhead, Bebington and the wider Wirral. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the peninsula's gardens, parks and coastal woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Wallasey's gardens, parks and Bidston Hill woodland",
 },
 "hayes": {
  "region":"Hayes and the London Borough of Hillingdon",
  "nearby":["Uxbridge", "Ruislip", "Feltham"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Hayes, from sole-trader climbers and groundsmen to small firms working Minet Country Park, the Grand Union Canal, Stockley Park and the Ruislip Woods fringe, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews who climb and clear west London's trees",
  "s1loc":[
   "In west London's borough of Hillingdon, Hayes carries a solid estate of street, park and canal-side trees, and managing it keeps a busy community of arborists and tree surgeons at work across the area. Most are sole traders and small teams on domestic gardens, council and park contracts and storm clearance, and every one of them depends on proper chainsaw PPE.",
   "The work follows the local geography. The old villages of Botwell, Yeading and Hayes End carry mature street and garden trees, while Minet Country Park, Lake Farm Country Park, the Grand Union Canal corridor, the wooded business estate at Stockley Park and Gutteridge Wood hold parkland and trees, all generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Hayes tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and with ash dieback, honey fungus and TPO and conservation-area rules across Hillingdon, plus the ancient woodland of nearby Ruislip Woods, the rules shape much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Most of these outfits stay small: a climber and a groundsman, a family business, a one or two-van team working across Hayes, Uxbridge, Ruislip and the wider Hillingdon patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the borough's gardens, parks and canal-side tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Hayes's gardens, country parks and Grand Union Canal greenery",
 },
 "aylesbury": {
  "region":"Aylesbury and Buckinghamshire",
  "nearby":["Bicester", "High Wycombe", "Hemel Hempstead"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Aylesbury, from sole-trader climbers and groundsmen to small firms working the Vale of Aylesbury, Wendover Woods and the Chiltern escarpment beechwoods, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews who climb and clear the Vale and the Chilterns",
  "s1loc":[
   "Set between the open Vale of Aylesbury and the wooded Chiltern escarpment, Aylesbury is a green town with a big stock of mature street, park, estate and farmland trees, and looking after it keeps a busy community of arborists and tree surgeons at work across the area. Most are sole traders and small teams on domestic gardens, council and estate contracts and storm clearance, and every one of them leans on proper chainsaw PPE.",
   "The work follows the local geography. Villages and leafy edges like Wendover, Weston Turville, Stoke Mandeville and Bierton carry mature oak, beech and estate trees, while Coombe Hill, Wendover Woods, the Low Scrubs beech woods and the wider Chiltern escarpment hold parkland and ancient woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Aylesbury tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with ash dieback across the Chiltern beech-and-ash woods and TPO and conservation-area rules shaping much of the work, and the HS2 corridor through the Vale adding clearance and replanting. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Firms here run small. A climber and a groundsman, a family business, a one or two-van outfit covering Aylesbury, Wendover and the wider Buckinghamshire patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the Vale's gardens, parks and Chiltern woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Aylesbury's Vale gardens, parks and Chiltern escarpment woodland",
 },
 "hereford": {
  "region":"Hereford and Herefordshire",
  "nearby":["Malvern", "Worcester", "Gloucester"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Hereford, from sole-trader climbers and groundsmen to small firms working the Wye Valley, Queenswood Country Park and Haugh Wood, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Herefordshire's trees",
  "s1loc":[
   "Sitting on the River Wye amid orchards and wooded countryside, Hereford is a green city with a large estate of mature street, park, garden and farmland trees, and managing it keeps a community of arborists and tree surgeons busy across the city and the wider county. Most are sole traders and small teams working domestic gardens, estate and orchard contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the city's leafy geography. Suburbs like Tupsley, Hampton Park, Aylestone Hill and Bartonsham carry mature oak, beech and estate trees, while Aylestone Park, Queenswood Country Park, Haugh Wood and the wooded slopes of the Wye Valley hold parkland and woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Hereford tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with ash dieback heavy across the county's hedgerows and woods and TPO and conservation-area rules shaping much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Most outfits here are small. A climber and a groundsman, a family business, a one or two-van firm working across Hereford, Leominster and the wider Herefordshire patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the city's gardens, orchards and Wye Valley woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Hereford's gardens, orchards and Wye Valley woodland",
 },
 "merthyr tydfil": {
  "region":"Merthyr Tydfil and the south Wales valleys",
  "nearby":["Aberdare", "Pontypridd", "Caerphilly"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Merthyr Tydfil, from sole-trader climbers and groundsmen to small firms working Cyfarthfa Park, the Taf Fechan woods and the Brecon Beacons fringe, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews who climb and clear the south Wales valleys",
  "s1loc":[
   "Wrapped around the head of the Taff valley below the Brecon Beacons, Merthyr Tydfil is a green and wooded town with a big stock of mature park, street, hillside and valley-slope trees, and looking after it keeps a community of arborists and tree surgeons busy across the town and the valleys. Most are sole traders and small teams working domestic gardens, council and forestry contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the local geography. Areas like Gurnos, Pant, Cefn Coed and Troed-y-rhiw carry mature estate and street trees, while Cyfarthfa Park, the Taf Fechan gorge and nature reserve, the Gethin and Merthyr Vale forests and the Brecon Beacons fringe hold parkland and conifer and broadleaf woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Merthyr tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with large-scale larch felling for Phytophthora ramorum across the Natural Resources Wales valleys forests and ash dieback shaping much of the work, and Coed Cymru replanting following on. Every chainsaw job, on the ground or roped into a slope or canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Outfits here tend to be small. A climber and a groundsman, a family business, a one or two-van firm working across Merthyr, Aberfan and the wider Taff and Cynon valleys patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's parks, hillsides and valley woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Merthyr Tydfil's parks, hillsides and Taf Fechan valley woodland",
 },
 "halesowen": {
  "region":"Halesowen and the Black Country",
  "nearby":["Stourbridge", "Brierley Hill", "Oldbury"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Halesowen, from sole-trader climbers and groundsmen to small firms working Leasowes Park, the Clent Hills and the Lutley and Illey woods, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear the Black Country's trees",
  "s1loc":[
   "On the green western edge of the Black Country below the Clent Hills, Halesowen carries a large estate of mature street, park, garden and woodland trees, and managing it keeps a community of arborists and tree surgeons busy across the town and the wider West Midlands. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the town's leafy geography. Areas like Hayley Green, Hasbury, Lapal and Cradley carry mature oak and estate trees, while Leasowes Park, the National Trust Clent Hills, the Woodland Trust's Uffmoor Wood and the Lutley and Illey woods hold parkland and woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Halesowen tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with ash dieback across the local woods and hedgerows and TPO and conservation-area rules shaping much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Firms here run small. A climber and a groundsman, a family business, a one or two-van outfit working across Halesowen, Stourbridge and the wider Black Country patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's gardens, parks and Clent Hills woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Halesowen's gardens, Leasowes parkland and Clent Hills woodland",
 },
 "tunbridge wells": {
  "region":"Tunbridge Wells and the High Weald",
  "nearby":["Tonbridge", "Sevenoaks", "Crowborough"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Tunbridge Wells, from sole-trader climbers and groundsmen to small firms working the Common, Dunorlan Park and the Bedgebury and Eridge woodland, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews who climb and clear the High Weald's trees",
  "s1loc":[
   "Ringed by the wooded ridges of the High Weald, Royal Tunbridge Wells is a green town with a large estate of mature street, park, garden and estate trees, and looking after it keeps a busy community of arborists and tree surgeons at work across the town and the Kent and Sussex border. Most are sole traders and small teams working domestic gardens, council and estate contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the town's leafy geography. Suburbs and edges like Rusthall, Southborough, Langton Green and Frant carry mature oak, beech and estate trees, while Tunbridge Wells Common, Dunorlan Park, Calverley Grounds, Eridge Park and Forestry England's Bedgebury National Pinetum and Forest hold parkland and woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Tunbridge Wells tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with ash dieback heavy across the High Weald woods and TPO and conservation-area rules shaping much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Outfits here are mostly small. A climber and a groundsman, a family business, a one or two-van firm working across Tunbridge Wells, Tonbridge and the wider High Weald patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's gardens, parks and High Weald woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Tunbridge Wells's Common, parks and High Weald woodland",
 },
 "dunfermline": {
  "region":"Dunfermline and Fife",
  "nearby":["Kirkcaldy", "Glenrothes", "Alloa"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Dunfermline, from sole-trader climbers and groundsmen to small firms working Pittencrieff Park, Townhill Country Park and the Scots pine of Devilla Forest, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews who climb and clear Fife's trees",
  "s1loc":[
   "A green royal burgh above the Firth of Forth, Dunfermline carries a deep estate of mature park, street and estate trees, and looking after it keeps a steady community of arborists and tree surgeons working across the town and wider Fife. The bulk of them are sole traders and small teams on domestic gardens, council and park contracts and storm clearance, and every one of them leans on proper chainsaw PPE.",
   "The work follows the local geography. Pittencrieff Park holds thousands of trees including semi-natural ancient woodland, giant sequoia and a monkey puzzle, while Townhill Country Park north of town and the Scots pine of Devilla Forest near Crossgates and the Forth-side villages of Limekilns and Crossford carry parkland and woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Dunfermline tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, often alongside Forestry and Land Scotland and NatureScot, with Storm Arwen and ash dieback both adding clearance and felling work across Fife. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Most of the outfits here stay small: a climber and a groundsman, a family business, a one or two-van team covering Dunfermline, Kirkcaldy, Glenrothes and the wider Fife patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's parks, country parks and Fife woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Dunfermline's parks, Townhill Country Park and Devilla Forest woodland",
 },
 "livingston": {
  "region":"Livingston and West Lothian",
  "nearby":["Bathgate", "Falkirk", "Dunfermline"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Livingston, from sole-trader climbers and groundsmen to small firms working Almondell and Calderwood Country Park, the Beecraigs woodland and West Lothian's tree-belts, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Gear for the people who work West Lothian's canopy",
  "s1loc":[
   "Built as a new town and laced with planted tree-belts, Livingston sits in a green corner of West Lothian where the council alone looks after hundreds of hectares of woodland and tens of thousands of trees. Managing all of it keeps a busy community of arborists and tree surgeons going across the town and the county, most of them sole traders and small teams on gardens, council and park work and storm clearance, every one reliant on proper chainsaw PPE.",
   "The work follows the local geography. Almondell and Calderwood Country Park carries natural oak and hazel woodland along the River Almond, Beecraigs Country Park near Linlithgow and Polkemmet over towards Bathgate hold conifer and amenity planting, and the town's own poplar and conifer tree-belts run between the housing, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Livingston tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, often alongside Forestry and Land Scotland and NatureScot. Ash dieback is felling roadside ash across West Lothian and Storm Eowyn brought down thousands of trees and over 800 council enquiries in a single day, and every chainsaw job depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Out here the outfits are mostly small: a climber and a groundsman, a family business, a one or two-van team covering Livingston, Bathgate, Falkirk and the wider West Lothian patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the new town's tree-belts, country parks and West Lothian woodland",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Livingston's tree-belts, Almondell and Calderwood Country Park and the Beecraigs woodland",
 },
 "barrow-in-furness": {
  "region":"Barrow-in-Furness and Cumbria",
  "nearby":["Ulverston", "Kendal", "Lancaster"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Barrow-in-Furness, from sole-trader climbers and groundsmen to small firms working Barrow Park, the Sandscale dunes and the Furness peninsula's woodland, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews who climb and clear Furness's trees",
  "s1loc":[
   "Out on the Furness peninsula at the edge of the Lake District, Barrow-in-Furness mixes a mature estate of park and street trees with the wooded country running north towards the fells. Caring for it keeps a steady community of arborists and tree surgeons busy across the town and south Cumbria, most of them sole traders and small teams on gardens, council and estate contracts and storm clearance, all of them dependent on proper chainsaw PPE.",
   "The work follows the local geography. Barrow Park's 45 acres and the shelter woodland near the Sandscale Haws dunes and Roanhead carry mature amenity trees, while the wooded valleys around Furness Abbey and the Lake District fringe towards Ulverston and Kendal hold parkland and broadleaf woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Barrow tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members. Storm Eowyn matched Storm Arwen for devastation across Cumbria, with Westmorland and Furness highways answering around 70 fallen-tree reports in a day, and ash dieback adds steady felling, so every chainsaw job depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "The firms here are mostly small: a climber and a groundsman, a family business, a one or two-van outfit covering Barrow, Ulverston, Kendal and Lancaster and the wider Furness patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the peninsula's parks, dunes and Furness woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Barrow's parks, the Sandscale dunes and the Furness peninsula woodland",
 },
 "bebington": {
  "region":"Bebington and the Wirral",
  "nearby":["Birkenhead", "Heswall", "Bromborough"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Bebington, from sole-trader climbers and groundsmen to small firms working Port Sunlight, Brotherton Park and Dibbinsdale and the Mersey woods, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Gear for the people who climb the Wirral's trees",
  "s1loc":[
   "A leafy corner of the Wirral peninsula between the Mersey and the Dee, Bebington carries a mature estate of park, garden and estate trees, with the planned greenery of Port Sunlight on its doorstep. Looking after it keeps a busy community of arborists and tree surgeons going across the town and the Wirral, most of them sole traders and small teams on gardens, council and estate contracts and storm clearance, every one reliant on proper chainsaw PPE.",
   "The work follows the local geography. Port Sunlight's tree-lined model village and the SSSI ancient woodland of Brotherton Park and Dibbinsdale along the River Dibbin near Bromborough carry mature and exotic trees, while the wooded fringes towards Birkenhead and the higher ground of Higher Bebington and Heswall hold parkland and garden timber, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Bebington tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members and working alongside the Mersey Forest. Storm Arwen blew down over 600 trees across Wirral, including at Kings Lane in Higher Bebington, and ash dieback and Meripilus keep the council and contractors busy, so every chainsaw job depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "The outfits round here stay small: a climber and a groundsman, a family business, a one or two-van team covering Bebington, Birkenhead, Heswall and Bromborough and the wider Wirral patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the Wirral's villages, parks and Mersey woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Bebington's Port Sunlight greenery, Brotherton Park and Dibbinsdale and the Mersey woods",
 },
 "smethwick": {
  "region":"Smethwick and the Black Country",
  "nearby":["Oldbury", "West Bromwich", "Halesowen"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Smethwick, from sole-trader climbers and groundsmen to small firms working Warley Woods, Victoria Park and the Galton Valley canals, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews who climb the Black Country's trees",
  "s1loc":[
   "A built-up Black Country town in Sandwell, Smethwick still carries a real stock of park, street and canalside trees among the housing and industry. Managing it keeps a steady community of arborists and tree surgeons busy across the town and the wider Black Country, most of them sole traders and small teams on gardens, council and park contracts and storm clearance, all of them dependent on proper chainsaw PPE.",
   "The work follows the local geography. Warley Woods, a 100-acre Repton-designed park with a third of it mature woodland, and the greenery of Victoria Park off the High Street carry amenity trees, while the Galton Valley canal towpaths, Sandwell Valley Country Park towards West Bromwich and the Leasowes over at Halesowen hold parkland and waterside timber, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Smethwick tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with conservation-area and TPO rules around Galton Valley shaping much of the work and ash dieback adding steady felling. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "The firms here are mostly small: a climber and a groundsman, a family business, a one or two-van outfit covering Smethwick, Oldbury, West Bromwich and Halesowen and the wider Sandwell patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's parks, canalsides and Black Country woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Smethwick's Warley Woods, Victoria Park and the Galton Valley canals",
 },
 "horsham": {
  "region":"Horsham and West Sussex",
  "nearby":["Crawley", "Haywards Heath", "Burgess Hill"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Horsham, from sole-trader climbers and groundsmen to small firms working St Leonard's Forest, Warnham nature reserve and the High Weald, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Gearing up the crews who work the Weald's trees",
  "s1loc":[
   "Surrounded by the wooded ridges of the High Weald, Horsham is a town with mature trees in every direction, and looking after that estate keeps a steady community of arborists and tree surgeons busy across the district. They are mostly sole traders and small teams on domestic gardens, council and woodland contracts and storm clearance, and every one of them depends on proper chainsaw PPE.",
   "The work tracks the local geography. Leafy villages such as Mannings Heath, Rusper and Slinfold carry mature oak, hornbeam and estate trees, while St Leonard's Forest, Leechpool Woods and Warnham Local Nature Reserve hold ancient woodland and parkland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Horsham tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with ash dieback and High Weald AONB and conservation-area rules shaping much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Firms here run small and local: a climber and a groundsman, a family business, a one or two-van outfit working Horsham, Southwater and the wider West Sussex Weald. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the district's gardens, forests and Wealden woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Horsham's villages, St Leonard's Forest and the High Weald",
 },
 "washington": {
  "region":"Washington and Tyne and Wear",
  "nearby":["Chester-le-Street", "Houghton le Spring", "Sunderland"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Washington, from sole-trader climbers and groundsmen to small firms working Washington Wildfowl, James Steel Park and the Wear valley, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews who clear the Wear valley's trees",
  "s1loc":[
   "Set in green spaces between the Wear and the Sunderland districts, Washington keeps a working community of arborists and tree surgeons busy across the New Town and the wider patch. Most are sole traders and small teams on domestic gardens, council and park contracts and storm clearance, and every one of them leans on proper chainsaw PPE.",
   "The work follows the local geography. The WWT Washington wetland centre, James Steel Park and the woodland along the River Wear carry mature trees, while Herrington Country Park and the wooded slopes below Penshaw Monument hold parkland and tree cover, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Washington tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and Storm Arwen, which tore through the North East in November 2021, left clearance and replanting work that still shapes the patch. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Small and local is the rule here: a climber and a groundsman, a family business, a one or two-van outfit working Washington, Houghton le Spring and the wider Tyne and Wear patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the New Town's parks, wetlands and Wear valley tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Washington's parks, wetlands and the Wear valley",
 },
 "hornchurch": {
  "region":"Hornchurch and Havering",
  "nearby":["Romford", "Upminster", "Brentwood"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Hornchurch, from sole-trader climbers and groundsmen to small firms working Hornchurch Country Park, the Thames Chase community forest and Havering's ancient woods, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Havering's trees",
  "s1loc":[
   "Out on London's leafy north-east edge, Hornchurch sits among the parks and country woods of Havering, and managing that estate keeps a busy community of arborists and tree surgeons working across the borough. Most are sole traders and small teams on domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the local geography. Suburbs like Emerson Park carry mature garden and estate trees, while Hornchurch Country Park along the Ingrebourne, Bedfords Park with its meadow and mature woodland, and the wider Thames Chase Community Forest hold parkland and tree cover, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Hornchurch tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with ash dieback and TPO and conservation-area rules shaping much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "And the firms stay small: a climber and a groundsman, a family business, a one or two-van outfit working Hornchurch, Upminster and the wider Havering patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the borough's parks, country woods and community-forest tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Hornchurch's parks, country woods and the Thames Chase forest",
 },
 "kettering": {
  "region":"Kettering and Northamptonshire",
  "nearby":["Corby", "Wellingborough", "Rushden"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Kettering, from sole-trader climbers and groundsmen to small firms working Wicksteed Park, the Boughton House estate and Rockingham Forest, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Gearing up the crews who work Northamptonshire's trees",
  "s1loc":[
   "Ringed by the wooded estates and forest country of Northamptonshire, Kettering keeps a steady community of arborists and tree surgeons busy across the town and the surrounding villages. Most are sole traders and small teams on domestic gardens, council and estate contracts and storm clearance, and every one of them depends on proper chainsaw PPE.",
   "The work follows the local geography. Wicksteed Park's rolling parkland and the mature trees of the Boughton House estate carry oak, lime and beech, while the Nene and Ise valleys and the ancient woodland of Rockingham Forest hold tree cover across the patch, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Kettering tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and ash dieback has hit hard across Rockingham Forest, where Forestry England has felled large numbers of ash at Fineshade Wood to keep trails safe. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Firms here run small and local: a climber and a groundsman, a family business, a one or two-van outfit working Kettering, Corby and the wider Northamptonshire patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's parks, estates and Rockingham Forest tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Kettering's parks, estates and Rockingham Forest",
 },
 "brierley hill": {
  "region":"Brierley Hill and the Black Country",
  "nearby":["Stourbridge", "Kingswinford", "Halesowen"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Brierley Hill, from sole-trader climbers and groundsmen to small firms working Saltwells nature reserve, the Fens Pools and Pensnett, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews who clear the Black Country's trees",
  "s1loc":[
   "Greener than its industrial name suggests, Brierley Hill sits among the urban woods and nature reserves of Dudley, and managing that tree estate keeps a working community of arborists and tree surgeons busy across the Black Country. Most are sole traders and small teams on domestic gardens, council and reserve contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the local geography. Saltwells National Nature Reserve, with Saltwells Wood and its ancient woodland, sits alongside the Fens Pools and Buckpool reserves around Pensnett and the wooded land at Barrow Hill, carrying mature oak and birch, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Brierley Hill tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and TPO and conservation-area rules shape much of the work, with Dudley's twenty conservation areas and group tree preservation orders bearing on local sites. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Small and local is the rule here: a climber and a groundsman, a family business, a one or two-van outfit working Brierley Hill, Kingswinford and the wider Dudley patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the borough's reserves, urban woods and Black Country tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Brierley Hill's reserves, urban woods and the Fens Pools",
 },
 "corby": {
  "region":"Corby and Northamptonshire",
  "nearby":["Kettering", "Market Harborough", "Wellingborough"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Corby, from sole-trader climbers and groundsmen to small firms working Rockingham Forest, Fineshade Wood, East Carlton Country Park and the surviving Northamptonshire woodland, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Northamptonshire's trees",
  "s1loc":[
   "A former steel town set in old forest country, Corby keeps a steady community of arborists and tree surgeons busy across the town and the wider Rockingham Forest landscape. Most are sole traders and small teams working domestic gardens, council and country-park contracts and storm clearance, and every one of them depends on proper chainsaw PPE.",
   "The work follows the local geography. Streets and estates around Weldon, Cottingham and Rockingham carry mature oak, ash and parkland trees, while Thoroughsale and Hazel Woods, King's Wood Nature Reserve, Weldon Woodland Park, East Carlton Country Park and Fineshade Wood hold the fragments of the old forest, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Corby tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and ash dieback drives much of the work, with clear-felling of diseased ash and native replanting under way at Fineshade and across the Corby Woodland Project. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Firms here stay small. A climber and a groundsman, a family business, a one or two-van outfit working across Corby, Weldon and the Rockingham Forest villages will buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's gardens, country parks and Rockingham Forest tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Corby's gardens, country parks and Rockingham Forest woodland",
 },
 "bracknell": {
  "region":"Bracknell and Berkshire",
  "nearby":["Wokingham", "Camberley", "Sandhurst"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Bracknell, from sole-trader climbers and groundsmen to small firms working Swinley Forest, Lily Hill Park, the Look Out and the Crowthorne pinewoods, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Berkshire's pinewoods",
  "s1loc":[
   "Wrapped in Crown Estate pine and heath, Bracknell keeps a busy community of arborists and tree surgeons working across the town and the surrounding Berkshire woodland. Most are sole traders and small teams handling domestic gardens, council and forest contracts and storm clearance, and every one of them leans on proper chainsaw PPE.",
   "The work follows the town's wooded geography. Suburbs like Crowthorne, Warfield, Winkfield and Easthampstead carry mature pine, oak and estate trees, while Swinley Forest, Lily Hill Park, the Look Out and the Crowthorne and Bagshot pinewoods hold plantation and parkland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Bracknell tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and the legacy of the 2011 Swinley Forest wildfire and the Thames Basin Heaths protected ground-nesting habitat shape much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Outfits here run lean. A climber and a groundsman, a family business, a one or two-van firm working across Bracknell, Wokingham, Crowthorne and the Crown Estate forest will buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's gardens, parks and Crown Estate forest tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Bracknell's gardens, parks and Swinley Forest pinewoods",
 },
 "leamington spa": {
  "region":"Leamington Spa and Warwickshire",
  "nearby":["Warwick", "Kenilworth", "Stratford-upon-Avon"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Leamington Spa, from sole-trader climbers and groundsmen to small firms working Jephson Gardens, Newbold Comyn, the Avon and the Forest of Arden, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Warwickshire's trees",
  "s1loc":[
   "A leafy spa town in old Arden country, Leamington Spa keeps a steady community of arborists and tree surgeons busy across the town and the wider Warwickshire landscape. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, and every one of them depends on proper chainsaw PPE.",
   "The work follows the town's green geography. Suburbs like Lillington, Milverton, Sydenham and Campion Hills carry mature oak, ash and avenue trees, while Jephson Gardens, the Pump Room Gardens, Newbold Comyn and the River Avon corridor, with the ancient oaks and pockets of the Forest of Arden beyond towards Kenilworth and Stratford, hold parkland and woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Leamington tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and ash dieback shapes much of the work, with Warwick District Council replanting mixed native species at Lillington and Milverton to hold cover as the ash is lost. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Most firms here are small. A climber and a groundsman, a family business, a one or two-van outfit working across Leamington, Warwick, Kenilworth and the Avon valley will buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's gardens, parks and Forest of Arden tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Leamington Spa's gardens, parks and Forest of Arden woodland",
 },
 "kidderminster": {
  "region":"Kidderminster and Worcestershire",
  "nearby":["Stourport-on-Severn", "Bromsgrove", "Droitwich"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Kidderminster, from sole-trader climbers and groundsmen to small firms working the Wyre Forest, Habberley Valley, Hartlebury Common and the Severn and Stour valleys, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Worcestershire's woods",
  "s1loc":[
   "On the edge of one of England's great oakwoods, Kidderminster keeps a busy community of arborists and tree surgeons working across the town and the wider Wyre Forest district. Most are sole traders and small teams handling domestic gardens, council and woodland contracts and storm clearance, and every one of them leans on proper chainsaw PPE.",
   "The work follows the local geography. Areas like Franche, Blakebrook, Habberley and Wribbenhall carry mature oak, ash and garden trees, while the Wyre Forest, Habberley Valley, Hartlebury Common and the wooded banks of the Severn and Stour hold ancient and plantation woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Kidderminster tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and with the Wyre Forest now the largest woodland National Nature Reserve in England, managed by Forestry England and Natural England, ancient sessile oakwood and ash dieback shape much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Firms here run lean. A climber and a groundsman, a family business, a one or two-van outfit working across Kidderminster, Stourport, Bewdley and the Wyre Forest will buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's gardens, commons and Wyre Forest tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Kidderminster's gardens, commons and Wyre Forest woodland",
 },
 "weymouth": {
  "region":"Weymouth and Dorset",
  "nearby":["Dorchester", "Poole", "Bournemouth"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Weymouth, from sole-trader climbers and groundsmen to small firms working Lodmoor, Nothe Gardens, Came Wood and the South Dorset Ridgeway, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Dorset's coastal trees",
  "s1loc":[
   "A Jurassic Coast town set under the chalk Ridgeway, Weymouth keeps a steady community of arborists and tree surgeons busy across the town and the wider Dorset landscape. Most are sole traders and small teams working domestic gardens, council and estate contracts and storm clearance, and every one of them depends on proper chainsaw PPE.",
   "The work follows the town's coastal geography. Areas like Rodwell, Wyke Regis, Preston and Bincombe carry mature pine, oak and garden trees, while Nothe Gardens, Lodmoor, Came Wood and the wooded slopes of the South Dorset Ridgeway towards Dorchester hold parkland and woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Weymouth tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and exposed coastal wind damage, estate woodland on the Ridgeway and ash dieback shape much of the work, with contractors handling everything from selective felling to scrub and rhododendron clearance for estates and wildlife trusts. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Most outfits here are small. A climber and a groundsman, a family business, a one or two-van firm working across Weymouth, Portland, Dorchester and the Ridgeway will buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's gardens, parks and Jurassic Coast tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Weymouth's gardens, parks and South Dorset Ridgeway woodland",
 },
 "canterbury": {
  "region":"Canterbury and Kent",
  "nearby":["Whitstable", "Herne Bay", "Faversham"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Canterbury, from sole-trader climbers and groundsmen to small firms working the city's leafy lanes, the Stour valley and the ancient oak and hornbeam coppice of the Blean, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews who climb and clear Kent's cathedral-city trees",
  "s1loc":[
   "Canterbury sits in a green pocket of east Kent, ringed by ancient woodland and threaded by the River Stour, and looking after that tree stock keeps a steady community of arborists and tree surgeons busy across the city and the surrounding villages. Most are sole traders and small teams on domestic gardens, council and conservation contracts and storm clearance, and every one of them leans on proper chainsaw PPE.",
   "The work follows the city's wooded geography. Leafy streets around the University of Kent, Wincheap, Harbledown and Bridge carry mature oak and beech, while Larkey Valley Wood, Blean Woods national nature reserve, West Blean and Thornden and the Stour corridor hold parkland, ancient coppice and woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms working out to Sturry and Blean.",
   "It is a safety-critical trade run to recognised standards. Canterbury tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and with ash dieback heavy across the Blean and the wider Kent countryside, TPO and conservation-area rules shape much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Most of these outfits are small. A climber and a groundsman, a family firm, a one or two-van team working the CT1, CT2 and CT3 postcodes across Canterbury, Whitstable and Faversham. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the city's gardens, river valley and ancient Blean woodland",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Canterbury's leafy lanes, the Stour valley and the Blean woodland",
 },
 "barry": {
  "region":"Barry and the Vale of Glamorgan",
  "nearby":["Penarth", "Cardiff", "Bridgend"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Barry, from sole-trader climbers and groundsmen to small firms working the town's coastal parks, Porthkerry's woodland and the wider Vale of Glamorgan, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear the Vale's trees",
  "s1loc":[
   "Barry is the largest town in the Vale of Glamorgan, a coastal patch where much of the urban forest sits in private gardens and residential streets, and managing it keeps a busy community of arborists and tree surgeons working across the town and the wider Vale. Most are sole traders and small teams on domestic gardens, council and country-park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the local geography. Streets around Romilly Park and the older parts of Barry carry mature garden trees, while Porthkerry Country Park holds 220 acres of woodland and meadow under its Victorian viaduct, Cosmeston Lakes runs out toward Penarth and Cwm George and Casehill Woods sit inland near Dinas Powys, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Barry tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and with ash dieback a recognised threat across the Vale's tree stock under Natural Resources Wales guidance, TPO and conservation-area rules shape much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "And the firms are mostly small. A climber and a groundsman, a family business, a one or two-van outfit working Barry Island, Penarth and the wider Vale of Glamorgan and Cardiff patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's gardens, coastal parks and Vale woodland",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Barry's coastal parks, Porthkerry woodland and the wider Vale of Glamorgan",
 },
 "hamilton": {
  "region":"Hamilton and South Lanarkshire",
  "nearby":["Motherwell", "Wishaw", "Bellshill"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Hamilton, from sole-trader climbers and groundsmen to small firms working Chatelherault's ancient oaks, Strathclyde Park and the Clyde and Avon valleys, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews who climb and clear Lanarkshire's trees",
  "s1loc":[
   "Set above the Clyde in South Lanarkshire, Hamilton is a green town with a big estate of mature street, park and estate trees, and keeping it in order supports a steady community of arborists and tree surgeons across the town and the surrounding Lanarkshire belt. Most are sole traders and small teams on domestic gardens, council and country-park contracts and storm clearance, and every one of them depends on proper chainsaw PPE.",
   "The work follows the river valleys. Leafy streets around Bothwell and Uddingston carry mature trees, while Chatelherault Country Park holds the centuries-old Cadzow oaks above the Avon gorge, Strathclyde Park spreads along the Clyde and the wider Clyde valley woodland runs out toward Motherwell, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Hamilton tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and with Storm Eowyn windblow clearance across central and south Scotland and a long-running South Lanarkshire ash dieback programme under Forestry and Land Scotland and NatureScot, much of the work is shaped by storms, disease and TPO rules. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "These outfits are mostly small. A climber and a groundsman, a family firm, a one or two-van team working across Hamilton, Bothwell and the wider South Lanarkshire patch toward Wishaw and Bellshill. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's gardens, country parks and Clyde valley woodland",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Hamilton's country parks, Chatelherault oaks and the Clyde and Avon valleys",
 },
 "folkestone": {
  "region":"Folkestone and Kent",
  "nearby":["Hythe", "Dover", "Deal"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Folkestone, from sole-trader climbers and groundsmen to small firms working the Warren, the Lower Leas Coastal Park and the North Downs woodland of the Kent Downs, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear east Kent's trees",
  "s1loc":[
   "Tucked under the North Downs on the east Kent coast, Folkestone has a varied estate of cliff, garden and woodland trees, and managing it keeps a steady community of arborists and tree surgeons busy across the town and the surrounding district. Most are sole traders and small teams on domestic gardens, council contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the local geography. Leafy streets around Sandgate and Cheriton carry mature garden trees, while the Warren holds the deciduous ancient woodland that has grown across the old undercliff landslips, the Lower Leas Coastal Park runs along the seafront and the North Downs scarp and Kent Downs woodland rise behind the town toward Hythe, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Folkestone tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and with severe ash dieback driving felling in nearby woodland such as Hythe's Eaton Lands, TPO and conservation-area rules shape much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Most of these firms are small. A climber and a groundsman, a family business, a one or two-van outfit working across Folkestone, Hythe and the wider east Kent patch toward Dover and Deal. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's gardens, coastal parks and North Downs woodland",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Folkestone's coastal parks, the Warren and the North Downs woodland",
 },
 "crosby": {
  "region":"Crosby and Merseyside",
  "nearby":["Bootle", "Formby", "Liverpool"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Crosby, from sole-trader climbers and groundsmen to small firms working the coastal pinewoods and dunes, Little Crosby and the wider Mersey Forest, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews who climb and clear Sefton's trees",
  "s1loc":[
   "A coastal town in the Metropolitan Borough of Sefton, Crosby has a leafy estate of street, garden and parkland trees backing onto the Merseyside dune coast, and looking after it keeps a steady community of arborists and tree surgeons busy across the town and the wider borough. Most are sole traders and small teams on domestic gardens, council and woodland contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the local geography. The grand villa streets of Blundellsands and Great Crosby carry mature garden trees, while the Formby pinewoods and dunes run up the coast, Little Crosby and Ince Blundell hold estate and farmland trees and the wider Mersey Forest spreads across Sefton, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms working out through Thornton, Waterloo and Hightown.",
   "It is a safety-critical trade run to recognised standards. Crosby tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and with Sefton's coastal pinewoods, conservation areas and ash dieback shaping the work alongside TPO rules. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "These outfits are mostly small. A climber and a groundsman, a family firm, a one or two-van team working across Crosby, Bootle and the wider Sefton and Liverpool patch toward Formby. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's gardens, coastal pinewoods and Mersey Forest woodland",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Crosby's coastal pinewoods, dunes and the wider Mersey Forest",
 },
 "keighley": {
  "region":"Keighley and West Yorkshire",
  "nearby":["Bingley", "Shipley", "Bradford"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Keighley, from sole-trader climbers and groundsmen to small firms working Cliffe Castle Park, the St Ives Estate and the wooded cloughs of the Worth and Aire valleys, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews who climb and clear the Worth valley's trees",
  "s1loc":[
   "A mill town set among Pennine fells and wooded valleys, Keighley carries a heavy stock of mature street, park and estate trees, and looking after it keeps a steady community of arborists and tree surgeons working across the town and the wider Bradford district. Most are sole traders and small teams on domestic gardens, council and park contracts and storm clearance, and every one of them needs proper chainsaw PPE to do it.",
   "The work follows the valley geography. Cliffe Castle Park carries mature lime, chestnut and sycamore, the 550-acre St Ives Estate at Bingley holds woodland, larch and horse chestnut, and Northcliffe Woods at Shipley plus the Worth and Aire valley cloughs run down toward Rombalds Moor, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Keighley tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with ash dieback reported to Bradford Council's trees team and TPO and conservation-area rules shaping much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "These outfits stay small by design: a climber and a groundsman, a family business, a one or two-van team covering Keighley, Bingley, Shipley and the rest of the Bradford patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's parks, estates and Worth valley woodland",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Keighley's parks, the St Ives Estate and the wooded Worth and Aire valleys",
 },
 "eastleigh": {
  "region":"Eastleigh and Hampshire",
  "nearby":["Winchester", "Fareham", "Southampton"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Eastleigh, from sole-trader climbers and groundsmen to small firms working Itchen Valley Country Park, Lakeside, Stoke Park Woods and the ancient woodland of the Itchen, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Hampshire's trees",
  "s1loc":[
   "Sitting in the wooded valley of the Itchen between Winchester and Southampton, Eastleigh has a large estate of mature street, park and garden trees, and managing it keeps a busy community of arborists and tree surgeons working across the borough and wider Hampshire. Most are sole traders and small teams on domestic gardens, council and park contracts and storm clearance, all of them dependent on proper chainsaw PPE.",
   "The work follows the local geography. Itchen Valley Country Park holds 90 acres of ancient woodland and conifer plantation, Lakeside Country Park carries lake-edge and woodland trees, and Stoke Park Woods, Telegraph Woods with its Douglas firs and sweet chestnut, and Hiltingbury Lakes at Chandler's Ford run out toward Bishopstoke and Fair Oak, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Eastleigh tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with ash dieback across Hampshire's ancient woodland and TPO and conservation-area rules shaping much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Most of these firms are small by design: a climber and a groundsman, a family business, a one or two-van team working Eastleigh, Chandler's Ford, Bishopstoke and the wider Hampshire patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the borough's country parks and Itchen valley woodland",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Eastleigh's country parks, Stoke Park Woods and the wooded Itchen valley",
 },
 "lancaster": {
  "region":"Lancaster and Lancashire",
  "nearby":["Morecambe", "Kendal", "Preston"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Lancaster, from sole-trader climbers and groundsmen to small firms working Williamson Park, the wooded Lune valley and the edge of the Forest of Bowland, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews who climb and clear the Lune valley's trees",
  "s1loc":[
   "A historic city set on the River Lune at the edge of the Forest of Bowland, Lancaster carries a deep stock of mature street, park and estate trees, and keeping on top of it supports a steady community of arborists and tree surgeons across the city and wider Lancashire. Most are sole traders and small teams on domestic gardens, council and park contracts and storm clearance, every one of them reliant on proper chainsaw PPE.",
   "The work follows the landscape. Williamson Park holds woodland walks around the Ashton Memorial, the suburbs of Scotforth, Bowerham and Hala carry mature street and garden trees, and the wooded cloughs and river valleys of the Lune climb toward Quernmore and the Forest of Bowland National Landscape, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Lancaster tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with Storm Arwen windblow across Lancashire's woodland and TPO and conservation-area rules shaping much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "By and large these are small outfits: a climber and a groundsman, a family business, a one or two-van team covering Lancaster, Morecambe and the wider Lune valley patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the city's parks and Lune valley woodland",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Lancaster's parks, the wooded Lune valley and the edge of the Forest of Bowland",
 },
 "macclesfield": {
  "region":"Macclesfield and Cheshire",
  "nearby":["Congleton", "Wilmslow", "Buxton"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Macclesfield, from sole-trader climbers and groundsmen to small firms working Macclesfield Forest, Tegg's Nose Country Park and the wooded Bollin valley on the edge of the Peak District, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear the Bollin valley's trees",
  "s1loc":[
   "A former silk town on the western edge of the Peak District, Macclesfield carries a large estate of mature street, park and estate trees, and managing it keeps a busy community of arborists and tree surgeons working across the town and wider Cheshire. Most are sole traders and small teams on domestic gardens, council and park contracts and storm clearance, all of them dependent on proper chainsaw PPE.",
   "The work follows the landscape. Tegg's Nose Country Park holds the broadleaved Teggsnose Wood of oak, beech, hornbeam and holly, Macclesfield Forest runs as conifer plantation around Trentabank and Ridgegate, and the wooded Bollin valley threads down through suburbs like Prestbury, Bollington and Tytherington, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Macclesfield tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with ash dieback and decline-related dismantles handled through Cheshire East TPO and conservation-area rules shaping much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "These firms tend to stay small: a climber and a groundsman, a family business, a one or two-van team covering Macclesfield, Bollington, Prestbury and the wider Cheshire patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's forest, country park and Bollin valley tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Macclesfield's forest, Tegg's Nose and the wooded Bollin valley",
 },
 "cumbernauld": {
  "region":"Cumbernauld and North Lanarkshire",
  "nearby":["Falkirk", "Coatbridge", "Airdrie"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Cumbernauld, from sole-trader climbers and groundsmen to small firms working Palacerigg Country Park, the ancient woodland of Cumbernauld Glen and the Scottish Wildlife Trust reserves, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews who climb and clear North Lanarkshire's trees",
  "s1loc":[
   "Built as a new town and planted through with woodland belts and amenity trees, Cumbernauld carries a heavy stock of mature street, park and estate trees, and keeping on top of it supports a steady community of arborists and tree surgeons across the town and wider North Lanarkshire. Most are sole traders and small teams on domestic gardens, council and park contracts and storm clearance, every one of them reliant on proper chainsaw PPE.",
   "The work follows the landscape. Palacerigg Country Park holds 40-plus hectares of planted native trees and shrubs in the hills to the south-east, the ancient woodland of Cumbernauld Glen and the Scottish Wildlife Trust's Forest Wood reserve carry oak, bluebell ground and invasive Sitka spruce, and the town's wooded belts thread out toward Falkirk and the Kelvin valley, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Cumbernauld tree surgeons are typically NPTC and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, alongside Forestry and Land Scotland and NatureScot guidance and storm windblow clearance shaping much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "By and large these are small outfits: a climber and a groundsman, a family business, a one or two-van team covering Cumbernauld, Falkirk, Coatbridge and the wider North Lanarkshire patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's country park and Glen woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Cumbernauld's country park, Cumbernauld Glen and the Scottish Wildlife Trust woods",
 },
 "perth": {
  "region":"Perth and Perthshire",
  "nearby":["Dundee", "Kirkcaldy", "Glenrothes"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Perth, from sole-trader climbers and groundsmen to small firms working Kinnoull Hill, the Scone Palace policies and the wider Big Tree Country woodland, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Big Tree Country",
  "s1loc":[
   "Sitting at the heart of Perthshire's Big Tree Country, Perth is wrapped in mature woodland and parkland, and keeping that estate in order supports a steady community of arborists and tree surgeons across the city and beyond. Most are sole traders and small teams working domestic gardens, estate and policy woodland and storm clearance, every one of them reliant on proper chainsaw PPE.",
   "The work follows the geography of the Tay. Wooded ground at Kinnoull Hill, Quarrymill Den, the Scone Palace policies and pinetum and the riverside parks carries mature beech, pine, oak and champion conifers, while the surrounding glens and the Tay Forest Park hold commercial and amenity timber, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Perth tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with Forestry and Land Scotland and NatureScot shaping the wider woodland picture and Storm Arwen and Storm Eowyn windblow leaving years of clear-up. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "These are small outfits for the most part: a climber and a groundsman, a family business, a one or two-van firm working across Perth, Scone and the wider Perthshire and Tayside patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the city's parks, policies and Perthshire woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Perth's parks, river policies and Big Tree Country woodland",
 },
 "cheshunt": {
  "region":"Cheshunt and Hertfordshire",
  "nearby":["Hoddesdon", "Hertford", "Enfield"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Cheshunt, from sole-trader climbers and groundsmen to small firms working Cedars Park, Broxbourne Woods and the Lea Valley, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear the Lea Valley's trees",
  "s1loc":[
   "Set in the green Lea Valley on the Hertfordshire edge of London, Cheshunt has a large estate of mature street, park and garden trees, and looking after it keeps a busy community of arborists and tree surgeons at work across the town and the wider valley. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the valley's leafy geography. Cedars Park and Cheshunt Park carry mature cedar, oak and parkland trees, the New River corridor and the Lee Valley Regional Park thread woodland and riverside through the town, and Broxbourne Woods, Wormley Wood and Bencroft Wood hold ancient oak and hornbeam, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Cheshunt tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with the Woodland Trust managing Wormley and Hoddesdonpark Woods and ash dieback and TPO and conservation-area rules shaping much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Local firms tend to be small ones: a climber and a groundsman, a family business, a one or two-van outfit working across Cheshunt, Waltham Cross, Goffs Oak and the wider Broxbourne and Lea Valley patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's parks, riverside and Lea Valley woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Cheshunt's parks, New River corridor and Lea Valley woodland",
 },
 "wellingborough": {
  "region":"Wellingborough and Northamptonshire",
  "nearby":["Rushden", "Kettering", "Northampton"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Wellingborough, from sole-trader climbers and groundsmen to small firms working Irchester Country Park, the Nene valley and the Rockingham Forest woodland, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear the Nene valley's trees",
  "s1loc":[
   "Strung along the Nene valley in Northamptonshire, Wellingborough holds a large estate of mature street, park and garden trees, and managing it keeps a steady community of arborists and tree surgeons busy across the town and the surrounding countryside. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the river and the old forest country. Irchester Country Park carries mixed broadleaf and conifer woodland on its reclaimed ironstone ground, the Nene valley and Summer Leys hold riverside and wetland trees, and the wider Rockingham Forest and Salcey Forest woodland frame the patch, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Wellingborough tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with Forestry England managing Salcey Forest nearby and ash dieback and TPO and conservation-area rules shaping much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Most of the firms are small: a climber and a groundsman, a family business, a one or two-van outfit working across Wellingborough, Rushden, Irchester and the wider Nene valley patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's parks, river and Nene valley woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Wellingborough's country parks, Nene valley and Rockingham Forest woodland",
 },
 "kingston upon thames": {
  "region":"Kingston upon Thames and south west London",
  "nearby":["Sutton", "Esher", "Twickenham"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Kingston upon Thames, from sole-trader climbers and groundsmen to small firms working Richmond Park, Bushy Park, Home Park and the Thames-side suburbs, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear south west London's trees",
  "s1loc":[
   "Green and well-treed on the banks of the Thames, Kingston upon Thames has a large estate of mature street, park and garden trees, and keeping it in order supports a big community of arborists and tree surgeons across the borough and south west London. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the borough's leafy geography. Suburbs like Coombe, Surbiton, Kingston Hill and Norbiton carry mature oak, beech and garden trees, while Richmond Park, Bushy Park, Home Park and the Hogsmill and Thames corridors hold royal parkland, veteran oaks and wood pasture, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Kingston tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with oak processionary moth and ash dieback management and TPO and conservation-area rules shaping much of the work across the Royal Borough. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Behind the work sit mostly small firms: a climber and a groundsman, a family business, a one or two-van outfit working across Kingston, New Malden, Surbiton and the wider south west London patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the borough's gardens, royal parks and Thames-side tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Kingston's gardens, royal parks and Thames-side woodland",
 },
 "andover": {
  "region":"Andover and Hampshire",
  "nearby":["Winchester", "Salisbury", "Basingstoke"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Andover, from sole-trader climbers and groundsmen to small firms working Harewood Forest, the Test valley and Anton Lakes, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Hampshire's chalk-country trees",
  "s1loc":[
   "Set among the Hampshire chalk downs in the Test valley, Andover has a large estate of mature street, park and garden trees, and looking after it keeps a steady community of arborists and tree surgeons busy across the town and the surrounding villages. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the downland and the river. Harewood Forest, Hampshire's largest ancient woodland outside the New Forest, carries English oak, hazel and silver birch, while Anton Lakes, Harewood Common and the Test valley hold riverside, wetland and hedgerow trees and the chalk downs frame the patch, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "The Bourne valley runs northeast of Andover, where the Bourne Rivulet, a winterbourne also called the Swift above Hurstbourne Tarrant, rises and flows past St Mary Bourne and on through the watercress beds at Hurstbourne Priors. At Doles Wood near Smannell and Finkley, a spring beech woodland once part of Finkley Forest, the ground climbs steadily off the North Wessex Downs. The Hurstbourne Park estate, a Grade II historic landscape with a wooded deer park of fourteenth-century origin near the Portway Roman line, holds mature parkland timber, the work running to crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "To the southwest, Danebury Iron Age hillfort rises above downland and West Wood, its ramparts crowned with large beech that Hampshire County Council inherited when it bought the site in 1958. Down on the Test, Chilbolton Cow Common and the timber-framed thatched village of Wherwell sit among riverside floodplain and ancient sessile oak, while the East Hampshire hangers further out carry their famous beech-clad slopes. From the chalk-stream margins to the scrub and standing oaks of the commons, this is a landscape of estate parkland, hangers and wet valley woodland that keeps local firms busy with sectional takedowns, pruning and emergency storm clearance.",
   "It is a safety-critical trade run to recognised standards. Andover tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with Test Valley Borough Council tree planting and ash dieback and TPO and conservation-area rules shaping much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "The firms here are mostly small ones: a climber and a groundsman, a family business, a one or two-van outfit working across Andover, East Anton, Barton Stacey and the wider Test valley patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's gardens, downland and Test valley woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Andover's gardens, chalk downs and Test valley woodland",
 },
 "llanelli": {
  "region":"Llanelli and Carmarthenshire",
  "nearby":["Swansea", "Neath", "Port Talbot"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Llanelli, from sole-trader climbers and groundsmen to small firms working the Millennium Coastal Park, the wooded Swiss Valley and Mynydd Mawr, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews who climb and clear Carmarthenshire's trees",
  "s1loc":[
   "A coastal Carmarthenshire town with a green hinterland of reservoir woodland, regenerated coastal park and valley trees, Llanelli keeps a steady community of arborists and tree surgeons at work across the town and the wider county. The bulk are sole traders and small teams on domestic gardens, council and park contracts and storm clearance, and every one of them depends on proper chainsaw PPE.",
   "The work tracks the local geography. Suburbs like Felinfoel, Llwynhendy and Bynea carry mature garden and estate trees, while the Millennium Coastal Park, the mature woodland around the Lliedi reservoirs in the Swiss Valley, Stradey and the regenerated Mynydd Mawr Woodland Park hold parkland and broadleaf cover, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Llanelli tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with ash dieback across Carmarthenshire and Natural Resources Wales guidance, plus TPO and conservation-area rules, shaping much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "These are mostly small outfits: a climber and a groundsman, a family business, a one or two-van crew working across Llanelli, Burry Port and the wider Carmarthenshire patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's coastal park, valley woodland and garden tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Llanelli's coastal park, Swiss Valley woodland and Carmarthenshire estates",
 },
 "neath": {
  "region":"Neath and Neath Port Talbot",
  "nearby":["Swansea", "Port Talbot", "Llanelli"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Neath, from sole-trader climbers and groundsmen to small firms working Gnoll Country Park, the wooded Vale of Neath and Afan Forest Park, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear the Vale of Neath's trees",
  "s1loc":[
   "Set among the steep wooded valleys of Neath Port Talbot, Neath keeps a busy community of arborists and tree surgeons at work across the town and the surrounding hills. Most are sole traders and small teams on domestic gardens, council and park contracts and storm clearance, and every one of them depends on proper chainsaw PPE.",
   "The work follows the valley geography. Suburbs like Cadoxton, Cimla and Tonna carry mature garden and roadside trees, while Gnoll Country Park, the sessile oak and ash woodland on the steep sides of the Vale of Neath and the conifer stands of Afan Forest Park hold parkland and forest, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Neath tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with ash dieback in the valley woodland and Natural Resources Wales guidance, plus larch clearance at Gnoll and TPO and conservation-area rules, shaping much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Run as small outfits for the most part: a climber and a groundsman, a family business, a one or two-van crew working across Neath, the Vale and the wider Neath Port Talbot patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the valley's parks, oak woodland and garden tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Neath's country park, Vale of Neath woodland and Afan forest",
 },
 "bridgend": {
  "region":"Bridgend and south Wales",
  "nearby":["Port Talbot", "Maesteg", "Barry"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Bridgend, from sole-trader climbers and groundsmen to small firms working Bryngarw Country Park, the wooded Ogmore valley and Parc Slip, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews who climb and clear Bridgend's trees",
  "s1loc":[
   "Sitting where the south Wales valleys meet the coast, Bridgend carries a large estate of mature park, garden and valley-side trees, and managing it keeps a steady community of arborists and tree surgeons busy across the county borough. Most are sole traders and small teams on domestic gardens, council and park contracts and storm clearance, and every one of them depends on proper chainsaw PPE.",
   "The work follows the local geography. Areas like Coity, Tondu and the Garw and Ogmore valleys carry mature oak, ash and estate trees, while the broadleaf and conifer woodland of Bryngarw Country Park, the oak and ash of Craig-y-Parcau on the Ogmore River and the restored woodland at Parc Slip nature reserve hold parkland and forest, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Bridgend tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with ash dieback in the valley woodland and Natural Resources Wales guidance, plus woodland thinning at Bryngarw and TPO and conservation-area rules, shaping much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Trading mostly as small outfits: a climber and a groundsman, a family business, a one or two-van crew working across Bridgend, Maesteg and the wider Ogmore and Garw patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the borough's country parks, valley woodland and garden tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Bridgend's country parks, Ogmore valley woodland and Parc Slip",
 },
 "cwmbran": {
  "region":"Cwmbran and Torfaen",
  "nearby":["Newport", "Pontypool", "Caerphilly"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Cwmbran, from sole-trader climbers and groundsmen to small firms working the Boating Lake, Henllys and the wooded valley sides, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Torfaen's trees",
  "s1loc":[
   "A Torfaen new town wrapped in wooded valley sides, Cwmbran carries a large estate of amenity, street and woodland trees, and managing it keeps a steady community of arborists and tree surgeons busy across the town. Most are sole traders and small teams on domestic gardens, council and park contracts and storm clearance, and every one of them depends on proper chainsaw PPE.",
   "The work follows the new town's geography. Districts like Henllys, Croesyceiliog and Llanyrafon carry mature garden and amenity trees, while Cwmbran Boating Lake, the upland woodland and common around Mynydd Henllys and the wooded slopes that frame the valley hold parkland and broadleaf cover, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Cwmbran tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with ash dieback across Torfaen and Natural Resources Wales guidance, the emergency conifer felling alongside the railway at the Boating Lake and TPO and conservation-area rules shaping much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Working mostly as small outfits: a climber and a groundsman, a family business, a one or two-van crew working across Cwmbran, Pontypool and the wider Torfaen patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the new town's lake, commons and valley-side woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Cwmbran's boating lake, Henllys commons and wooded valley sides",
 },
 "christchurch": {
  "region":"Christchurch and Dorset",
  "nearby":["Bournemouth", "New Milton", "Ferndown"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Christchurch, from sole-trader climbers and groundsmen to small firms working Stanpit Marsh, Steamer Point and the New Forest fringe, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews who climb and clear Dorset's coastal trees",
  "s1loc":[
   "Set where the Avon and the Stour meet the sea on the Dorset coast, Christchurch carries an estate of mature garden, riverside and woodland trees, and managing it keeps a steady community of arborists and tree surgeons busy across the BH23 patch. Most are sole traders and small teams on domestic gardens, council and park contracts and storm clearance, and every one of them depends on proper chainsaw PPE.",
   "The work follows the coastal geography. Areas like Highcliffe, Mudeford, Somerford and Stanpit carry mature garden and clifftop trees, while Stanpit Marsh, the cliff-top woodland at Steamer Point near Highcliffe, the floodplain trees along the Avon and Stour and the New Forest fringe to the east hold marsh, parkland and woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Christchurch tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with ash dieback, waterlogged floodplain trees prone to failure and TPO and conservation-area rules shaping much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Mostly small outfits: a climber and a groundsman, a family business, a one or two-van crew working across Christchurch, Highcliffe and the wider BH23 and New Forest fringe. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's marsh, riverside and clifftop woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Christchurch's marsh, Avon and Stour riverbanks and New Forest fringe",
 },
 "romford": {
  "region":"Romford and Havering",
  "nearby":["Hornchurch", "Upminster", "Brentwood"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Romford, from sole-trader climbers and groundsmen to small firms working Raphael Park, Bedfords Park and the Wellingtonia redwood avenue of Havering Country Park, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews who climb and clear Havering's trees",
  "s1loc":[
   "On the green edge of north-east London, Romford keeps a steady community of arborists and tree surgeons busy across Havering's parks, gardens and country-park woodland. The bulk of them are sole traders and small teams running domestic gardens, council and park contracts and storm clearance, and every one of them depends on proper chainsaw PPE.",
   "The work follows the borough's leafy geography. Mature street and garden trees run through Gidea Park, Emerson Park and Harold Wood, while Raphael Park, Bedfords Park and Havering Country Park, with its famous Wellingtonia avenue of giant redwoods, hold parkland and woodland alongside Hainault Forest to the north, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Romford tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with ash dieback and TPO and conservation-area rules shaping much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Most outfits here are small by design: a climber and a groundsman, a family business, a one or two-van team working across Romford, Hornchurch and the wider Havering patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the borough's gardens, parks and country-park woodland",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Romford's gardens, parks and Havering country-park woodland",
 },
 "barnet": {
  "region":"Barnet and North London",
  "nearby":["Edgware", "Borehamwood", "Potters Bar"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Barnet, from sole-trader climbers and groundsmen to small firms working Hadley Wood, Monken Hadley Common, Oak Hill Park and the ancient woodland of Coldfall, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear North London's trees",
  "s1loc":[
   "One of London's greenest boroughs, Barnet carries a large estate of mature street, park and garden trees, and managing it keeps a busy community of arborists and tree surgeons working across the borough and into Hertfordshire. Most are sole traders and small teams running domestic gardens, council and park contracts and storm clearance, all of them dependent on proper chainsaw PPE.",
   "The work follows the borough's leafy geography. Suburbs like Totteridge, Hadley Wood, Mill Hill and Whetstone carry mature oak, beech and estate trees, while Monken Hadley Common, Oak Hill Park, the ancient hornbeam and oak of Coldfall and Big Wood and the Dollis Valley Greenwalk hold parkland and woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Barnet tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with ash dieback and the borough's many TPOs and conservation areas, such as Totteridge, shaping much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "And the firms stay small: a climber and a groundsman, a family business, a one or two-van outfit working across High Barnet, East Barnet and the wider North London patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the borough's gardens, commons and ancient woodland",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Barnet's gardens, commons and ancient woodland",
 },
 "paignton": {
  "region":"Paignton and Torbay",
  "nearby":["Torquay", "Newton Abbot", "Exmouth"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Paignton, from sole-trader climbers and groundsmen to small firms working Clennon Valley, the ancient woodland of Occombe and the Paignton Zoo grounds, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews who climb and clear the English Riviera's trees",
  "s1loc":[
   "Set on the English Riviera, Paignton is a green resort town with a large estate of mature street, park and garden trees, and managing it keeps a steady community of arborists and tree surgeons busy across Torbay and South Devon. Most are sole traders and small teams running domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the bay's leafy geography. Suburbs like Preston, Goodrington, Higher Blagdon and nearby Marldon carry mature trees, while Clennon Valley, the ancient semi-natural woodland of Occombe, Scadson and Cockington Valley Woods, and the wooded grounds around Paignton Zoo hold parkland and woodland, much of it managed by the Torbay Coast and Countryside Trust, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Paignton tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with ash dieback hitting Devon hard and TPO and conservation-area rules shaping much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "The firms here are mostly small: a climber and a groundsman, a family business, a one or two-van outfit working across Paignton, Torquay and the wider Torbay patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the bay's gardens, valleys and ancient woodland",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Paignton's gardens, valley woods and English Riviera parkland",
 },
 "kirkcaldy": {
  "region":"Kirkcaldy and Fife",
  "nearby":["Glenrothes", "Dunfermline", "Perth"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Kirkcaldy, from sole-trader climbers and groundsmen to small firms working Beveridge Park, Ravenscraig and the long-established woodland of Dunnikier Park, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews who climb and clear Fife's trees",
  "s1loc":[
   "On the Fife coast, Kirkcaldy carries a large estate of mature street, park and estate trees, and managing it keeps a steady community of arborists and tree surgeons busy across the town and the wider county. Most are sole traders and small teams running domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the town's leafy geography. Mature trees line the streets and estates, while Beveridge Park, Ravenscraig Park above Dysart and the long-established woodland of Dunnikier Park hold parkland and woodland, with the South East Fife Woods managed by Forestry and Land Scotland just inland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Kirkcaldy tree surgeons are typically NPTC and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with NatureScot guidance, ash dieback and the heavy storm clearance left by Arwen and Eowyn shaping much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Outfits here run small: a climber and a groundsman, a family business, a one or two-van team working across Kirkcaldy, Glenrothes and the wider Fife patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's parks, estates and Fife woodland",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Kirkcaldy's parks, estate woodland and Fife coast",
 },
 "batley": {
  "region":"Batley and West Yorkshire",
  "nearby":["Dewsbury", "Mirfield", "Ossett"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Batley, from sole-trader climbers and groundsmen to small firms working Wilton Park, the Howley Hall estate and the wooded Spen and Calder valleys, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Kirklees trees",
  "s1loc":[
   "In the mill country of north Kirklees, Batley keeps a steady community of arborists and tree surgeons busy across its parks, gardens and the wooded valleys of West Yorkshire. Most are sole traders and small teams running domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the town's valley geography. Districts like Soothill, Healey and nearby Birstall carry mature trees, while Wilton Park between the town and Birstall, the old Howley Hall estate and the wooded slopes of the Spen and Calder valleys, threaded by the Spen Valley Greenway, hold parkland and woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Batley tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with ash dieback and TPO and conservation-area rules shaping much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Most firms here are a small affair: a climber and a groundsman, a family business, a one or two-van outfit working across Batley, Dewsbury and the wider Kirklees patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's parks, estates and valley woodland",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Batley's parks, estate grounds and Spen and Calder valley woodland",
 },
 "yeovil": {
  "region":"Yeovil and Somerset",
  "nearby":["Taunton", "Bridgwater", "Dorchester"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Yeovil, from sole-trader climbers and groundsmen to small firms working Ninesprings and Yeovil Country Park, Ham Hill and the wooded Yeo valley, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Somerset's trees",
  "s1loc":[
   "A market town set in the wooded Yeovil Scarplands close to the Dorset border, Yeovil carries a big estate of mature street, park and valley trees, and looking after it keeps a steady community of arborists and tree surgeons busy across south Somerset. Most are sole traders and small teams working domestic gardens, council contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the town's leafy geography. Suburbs like Penn Hill, Preston Plucknett, Abbey Manor and Forest Hill carry mature oak, beech and estate trees, while Ninesprings, the 40-hectare Yeovil Country Park, Wyndham Hill, Summerhouse Hill and Ham Hill hold parkland and woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Yeovil tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and ash dieback across Somerset, alongside TPO and conservation-area rules, shapes much of the work, with diseased ash already replaced by native planting at Ninesprings and Pit Wood at Ham Hill. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Small outfits do most of it: a climber and a groundsman, a family business, a one or two-van team working across Yeovil, Sherborne and the wider south Somerset patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's gardens, parks and Yeo valley tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Yeovil's gardens, Yeovil Country Park and Ham Hill woodland",
 },
 "welwyn garden city": {
  "region":"Welwyn Garden City and Hertfordshire",
  "nearby":["Hatfield", "Hertford", "Hitchin"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Welwyn Garden City, from sole-trader climbers and groundsmen to small firms working Sherrardspark Wood, Stanborough and the surrounding green belt, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear the garden city's trees",
  "s1loc":[
   "Built as a tree-lined garden city, Welwyn Garden City sits inside a generous Hertfordshire green belt and carries a huge estate of mature avenue, park and woodland trees, and managing it keeps a community of arborists and tree surgeons busy across the town. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the town's wooded edges. Streets and suburbs around Reddings, Pentley Park and Woodland Rise carry mature oak and estate trees, while Sherrardspark Wood, a 75-hectare ancient oak and hornbeam SSSI on the town's north-west edge, along with Stanborough Park and lakes and nearby Panshanger Park, hold woodland and parkland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Welwyn Garden City tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and with Sherrardspark Wood SSSI carrying oaks up to 250 years old, ash dieback, TPO and conservation-area rules shape much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Small firms handle most of it: a climber and a groundsman, a family business, a one or two-van team working across Welwyn Garden City, Hatfield and the wider Welwyn Hatfield patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's avenues, parks and ancient woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Welwyn Garden City's avenues, Sherrardspark Wood and the green belt",
 },
 "carlton": {
  "region":"Carlton and Nottinghamshire",
  "nearby":["Arnold", "West Bridgford", "Beeston"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Carlton, from sole-trader climbers and groundsmen to small firms working Gedling Country Park, Colwick and the Trent valley, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Gedling's trees",
  "s1loc":[
   "Sitting on the eastern edge of Nottingham in the Borough of Gedling, beside the River Trent, Carlton carries a mix of mature suburban, park and young colliery-restoration trees, and looking after them keeps a steady community of arborists and tree surgeons busy across the borough. Most are sole traders and small teams working domestic gardens, council contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the local geography. Carlton and neighbouring Mapperley, Gedling and Burton Joyce carry mature garden and street trees, while Gedling Country Park, 580 acres of restored colliery land planted with birch, oak, alder and hawthorn, along with Colwick Country Park and the Trent corridor, hold woodland and parkland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Carlton tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and with thousands of new trees going in between Gedling Country Park and Digby Park in Arnold, thinning, ash dieback, TPO and conservation-area rules shape much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Small outfits run most of it: a climber and a groundsman, a family business, a one or two-van team working across Carlton, Arnold and the wider Gedling patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the borough's gardens, parks and Trent valley tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Carlton's gardens, Gedling Country Park and the Trent corridor",
 },
 "west bridgford": {
  "region":"West Bridgford and Nottinghamshire",
  "nearby":["Beeston", "Arnold", "Long Eaton"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across West Bridgford, from sole-trader climbers and groundsmen to small firms working Sharphill Wood, Bridgford Park and the Trent at Holme Pierrepont, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Rushcliffe's trees",
  "s1loc":[
   "The administrative centre of Rushcliffe, sitting on the south bank of the River Trent opposite Nottingham, West Bridgford carries a leafy estate of mature street, park and riverside trees, and managing it keeps a community of arborists and tree surgeons busy across the borough. Most are sole traders and small teams working domestic gardens, council contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the town's geography. West Bridgford and neighbouring Edwalton, Gamston, Wilford and Lady Bay carry mature garden and avenue trees, while Sharphill Wood, a 24-acre mixed broadleaf Local Nature Reserve of ash, beech, English oak and lime overlooking Trent Bridge, along with Bridgford Park, the Hook nature reserve and Holme Pierrepont, hold woodland and riverside parkland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. West Bridgford tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and with Sharphill Wood losing trees to fungal dieback and trees felled along its paths for safety, plus TPO and conservation-area rules, much of the work is shaped by tree health. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Small firms do most of it: a climber and a groundsman, a family business, a one or two-van team working across West Bridgford, Ruddington and the wider Rushcliffe patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's gardens, parks and Trent riverside tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across West Bridgford's gardens, Sharphill Wood and the Trent at Holme Pierrepont",
 },
 "beckenham": {
  "region":"Beckenham and the London Borough of Bromley",
  "nearby":["Bromley", "Lewisham", "Orpington"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Beckenham, from sole-trader climbers and groundsmen to small firms working Beckenham Place Park's ancient woodland, Kelsey Park and Cator Park, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear south London's trees",
  "s1loc":[
   "A leafy suburb on the Bromley and Lewisham border in south-east London, Beckenham carries a dense estate of mature street, garden and ancient woodland trees, and looking after it keeps a busy community of arborists and tree surgeons working across the borough. Most are sole traders and small teams working domestic gardens, council contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the suburb's wooded character. Beckenham and neighbouring Shortlands, Park Langley and New Beckenham carry mature oak, horse chestnut and estate trees, while Beckenham Place Park, with around 20 hectares of ancient woodland of English oak, sessile oak, sweet chestnut and an ancient Turkey oak, along with Kelsey Park and Cator Park, hold woodland and parkland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Beckenham tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and with ash dieback felling across Bromley's commons and strict TPO and conservation-area protection around Shortlands, much of the work is shaped by tree health and amenity rules. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Small outfits handle most of it: a climber and a groundsman, a family business, a one or two-van team working across Beckenham, Bromley and the wider south-east London patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the borough's gardens, parks and ancient woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Beckenham's gardens, Beckenham Place Park and Kelsey Park",
 },
 "sutton": {
  "region":"Sutton and South West London",
  "nearby":["Epsom", "Croydon", "Kingston upon Thames"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Sutton, from sole-trader climbers and groundsmen to small firms working Nonsuch Park, Oaks Park, Beddington Park and the chalk Downs, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Sutton's trees",
  "s1loc":[
   "One of London's leafiest boroughs, Sutton carries a heritage of Victorian and Edwardian avenues, veteran trees and a string of historic parks, and keeping that estate safe supports a busy community of arborists and tree surgeons. Most are sole traders and small teams on domestic gardens, council and park contracts and storm clearance, every one of them reliant on proper chainsaw PPE.",
   "The work follows the borough's old-village geography. Suburbs like Cheam, Carshalton, Wallington, Belmont and Worcester Park carry mature plane, lime, beech and ancient sweet chestnut, while Nonsuch Park, Oaks Park, Beddington Park and the chalk Downs hold parkland, ancient woodland and estate trees, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Sutton tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with TPOs, the Carshalton and Cheam conservation areas and ash dieback shaping much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Small outfits do most of it: a climber and a groundsman, a family business, a one or two-van team working across Sutton, Carshalton, Cheam and out toward Epsom and the Surrey edge. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the borough's gardens, parks and chalk-Downs tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Sutton's gardens, parks and the chalk Downs",
 },
 "banbury": {
  "region":"Banbury and Oxfordshire",
  "nearby":["Bicester", "Daventry", "Leamington Spa"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Banbury, from sole-trader climbers and groundsmen to small firms working Spiceball Country Park, the Cherwell, Broughton parkland and the Bicester woods, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Cherwell's trees",
  "s1loc":[
   "Set where the Cherwell valley meets rolling Oxfordshire ironstone country, Banbury has a steady supply of mature parkland, hedgerow and garden trees, and looking after them keeps a community of arborists and tree surgeons busy. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the local geography. Spiceball Country Park and its community woodland sit along the River Cherwell and the Oxford Canal, while Broughton Castle parkland, Stoke Wood near Bicester and the new Banbury and Burnehyll community woodlands hold parkland and broadleaf trees, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Banbury tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with TPOs, Cherwell conservation areas and widespread ash dieback shaping much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "And the firms tend to be small: a climber and a groundsman, a family business, a one or two-van outfit working across Banbury, Bloxham, Deddington and out toward Bicester and the Daventry edge. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the area's gardens, riverside parks and Oxfordshire woodland",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Banbury's gardens, riverside parks and Cherwell woodland",
 },
 "winchester": {
  "region":"Winchester and Hampshire",
  "nearby":["Eastleigh", "Andover", "Southampton"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Winchester, from sole-trader climbers and groundsmen to small firms working St Catherine's Hill, the Itchen, Farley Mount and Crab Wood, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Hampshire's trees",
  "s1loc":[
   "A green cathedral city set in the chalk valley of the Itchen, Winchester is ringed by water meadows, tree-lined ridges and ancient woodland, and managing that estate keeps a community of arborists and tree surgeons busy. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them reliant on proper chainsaw PPE.",
   "The work follows the city's chalk-and-river geography. Suburbs like St Cross, Hyde, Teg Down and Oliver's Battery carry mature oak and beech, while St Catherine's Hill, Farley Mount Country Park, Crab Wood, West Wood and the Hursley estate hold downland, ancient broadleaf woodland and hazel coppice, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Winchester tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with TPOs, the Winchester conservation area and ash dieback in the ancient woods shaping much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Small outfits handle most of it: a climber and a groundsman, a family business, a one or two-van team working across Winchester, the Itchen Valley villages and out toward Eastleigh and Southampton. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the city's gardens, downland and ancient woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Winchester's gardens, downland and Itchen Valley woodland",
 },
 "beeston": {
  "region":"Beeston and Nottinghamshire",
  "nearby":["West Bridgford", "Long Eaton", "Arnold"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Beeston, from sole-trader climbers and groundsmen to small firms working Attenborough Nature Reserve, the Trent, Beeston Sidings and Bramcote Hills, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Broxtowe's trees",
  "s1loc":[
   "Sitting in the Broxtowe borough just south-west of Nottingham, Beeston pairs leafy Victorian streets with the wide green floodplain of the Trent, and looking after that tree stock keeps a community of arborists and tree surgeons busy. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the local geography. Suburbs like Bramcote, Chilwell and Toton carry the big mature trees of Victorian gardens, while Attenborough Nature Reserve at the meeting of the Erewash and the Trent, Beeston Sidings, Bramcote Hills park and the Wollaton ridge woodland hold wetland scrub, plantation and parkland trees, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Beeston tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with Broxtowe TPOs, conservation areas and ash dieback shaping much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Small outfits do most of it: a climber and a groundsman, a family business, a one or two-van team working the NG9 patch across Beeston, Chilwell, Stapleford and out toward West Bridgford and Long Eaton. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the area's gardens, riverside reserves and Trent-valley woodland",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Beeston's gardens, riverside reserves and Trent-valley woodland",
 },
 "ayr": {
  "region":"Ayr and South Ayrshire",
  "nearby":["Kilmarnock", "Irvine", "Paisley"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Ayr, from sole-trader climbers and groundsmen to small firms working Rozelle Park, Belleisle and the Ayr Gorge woodlands, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Ayrshire's trees",
  "s1loc":[
   "Strung along the Firth of Clyde coast at the mouth of the River Ayr, this South Ayrshire town carries mature estate parkland, riverside woodland and tree-lined streets, and looking after them keeps a community of arborists and tree surgeons busy. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the local geography. Rozelle Park and the Belleisle estate carry mature parkland and specimen trees, while the Ayr Gorge woodlands at Failford hold one of Ayrshire's most important ancient woods of oak, ash and old beech, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Ayr tree surgeons are typically NPTC and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and Storm Eowyn windblow, which Forestry and Land Scotland and NatureScot tracked across the region, plus ash dieback drive a lot of clearance and felling. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Small outfits handle most of it: a climber and a groundsman, a family business, a one or two-van team working across Ayr, Prestwick, Troon and out toward Kilmarnock and Irvine. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's gardens, estate parks and Ayrshire woodland",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Ayr's gardens, estate parks and Ayr Gorge woodland",
 },
 "kilmarnock": {
  "region":"Kilmarnock and East Ayrshire",
  "nearby":["Ayr", "Irvine", "Paisley"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Kilmarnock, from sole-trader climbers and groundsmen to small firms working Dean Castle Country Park, the Kay Park and the wooded Irvine valley, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews who climb and clear East Ayrshire's trees",
  "s1loc":[
   "A green town set in the wooded valleys of East Ayrshire, Kilmarnock carries a large estate of mature street, park and estate trees, and looking after it keeps a steady community of arborists and tree surgeons busy across the town and wider Ayrshire. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the local geography. The name Dean itself is an old Scots word for a wooded valley, and Dean Castle Country Park runs to parkland limes, ornamental pines and native woodland under great oaks, while the Kay Park, Kilmarnock's burns and the Irvine valley around Galston, Newmilns and Darvel hold further parkland and riverside trees, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Kilmarnock tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with widespread ash dieback across Scotland and TPO and conservation-area rules shaping much of the work, alongside Forestry and Land Scotland and NatureScot woodland nearby. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Mostly these are small outfits: a climber and a groundsman, a family business, a one or two-van firm covering Kilmarnock, Kilmaurs, Hurlford and the wider East Ayrshire patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's gardens, parks and Ayrshire valley woodland",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Kilmarnock's Dean Castle parkland, the Kay Park and the wooded Irvine valley",
 },
 "bridgwater": {
  "region":"Bridgwater and Somerset",
  "nearby":["Taunton", "Burnham-on-Sea", "Weston-super-Mare"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Bridgwater, from sole-trader climbers and groundsmen to small firms working the Quantock Hills oak woods, Cannington and the Sedgemoor levels, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Somerset's trees",
  "s1loc":[
   "Sitting between the Quantock Hills and the levels of King's Sedgemoor, Bridgwater carries a mix of mature street, park, orchard and estate trees, and managing it keeps a busy community of arborists and tree surgeons working across the town and wider Somerset. Most are sole traders and small teams working domestic gardens, council and estate contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the local landscape. The Quantock Hills west of the town hold sessile oak woodlands, ancient parkland and Forestry England's Great Wood, while Cannington, Hestercombe's wooded estate near Cheddon Fitzpaine and the willow and poplar lines of the Sedgemoor levels run down to Burnham-on-Sea, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Bridgwater tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members and several trained through Bridgwater College's land-based arboriculture courses at Cannington, with ash dieback and TPO and conservation-area rules shaping much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Family firms and small crews carry most of the load: a climber and a groundsman, a one or two-van outfit working across Bridgwater, Taunton, Cannington and the wider Sedgemoor patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's gardens, parks and Quantock woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Bridgwater's Quantock oak woods, the Sedgemoor levels and the Cannington estates",
 },
 "salisbury": {
  "region":"Salisbury and Wiltshire",
  "nearby":["Amesbury", "Andover", "Trowbridge"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Salisbury, from sole-trader climbers and groundsmen to small firms working Grovely Wood, the Harnham water meadows and Cranborne Chase, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews who climb and clear Wiltshire's trees",
  "s1loc":[
   "Set where the Avon, Nadder and Wylye meet, Salisbury is a green cathedral city with a large estate of mature street, park, riverside and estate trees, and looking after it keeps a busy community of arborists and tree surgeons working across the city and wider Wiltshire. Most are sole traders and small teams working domestic gardens, council and estate contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the local geography. Grovely Wood on its chalk ridge above the Wylye is one of southern Wiltshire's largest woodlands, while the Harnham and Bodenham water meadows, the Avon valley and the wooded combes of Cranborne Chase carry willow, alder, beech and oak, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Salisbury tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with ash dieback widespread across the Plain and Wiltshire Council woodlands and TPO and conservation-area rules shaping much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Small outfits carry most of the work: a climber and a groundsman, a family business, a one or two-van firm covering Salisbury, Wilton, Amesbury and the wider south Wiltshire patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the city's gardens, water meadows and chalk woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Salisbury's Grovely Wood, the Harnham water meadows and the Cranborne Chase valleys",
 },
 "havant": {
  "region":"Havant and Hampshire",
  "nearby":["Portsmouth", "Fareham", "Chichester"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Havant, from sole-trader climbers and groundsmen to small firms working Staunton Country Park, Havant Thicket and Stansted Forest, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Hampshire's trees",
  "s1loc":[
   "Tucked between Portsmouth and the South Downs, Havant carries a large estate of mature street, park, ancient woodland and estate trees, and managing it keeps a steady community of arborists and tree surgeons working across the borough and wider Hampshire. Most are sole traders and small teams working domestic gardens, council and estate contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the local geography. Staunton Country Park at Leigh Park runs to Regency parkland and ancient woodland through The Avenue and Havant Thicket, while Stansted Forest, the South Downs above Rowlands Castle and the wooded edges of Emsworth and Hayling Island carry oak, beech and pine, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Havant tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with ash dieback across Hampshire woodland and TPO and conservation-area rules shaping much of the work, alongside Forestry England and Woodland Trust ground nearby. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Family firms and small crews do most of it: a climber and a groundsman, a one or two-van outfit working across Havant, Emsworth, Bedhampton and the wider south Hampshire patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the borough's gardens, parks and South Downs woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Havant's Staunton parkland, Havant Thicket and Stansted Forest",
 },
 "hinckley": {
  "region":"Hinckley and Leicestershire",
  "nearby":["Nuneaton", "Leicester", "Coalville"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Hinckley, from sole-trader climbers and groundsmen to small firms working Burbage Common and Woods, the Ashby Canal and Market Bosworth woods, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews who climb and clear Leicestershire's trees",
  "s1loc":[
   "On the Leicestershire and Warwickshire border, Hinckley carries a mix of mature street, park, common and estate trees, and looking after it keeps a busy community of arborists and tree surgeons working across the town and wider county. Most are sole traders and small teams working domestic gardens, council and estate contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the local landscape. Burbage Common and Woods on the edge of town is the borough's largest countryside site, a surviving fragment of the medieval Hinckley forest still managed by coppicing, while the Ashby Canal towpath, the woods around Market Bosworth and the wooded Bosworth battlefield carry oak, ash and hedgerow timber, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Hinckley tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with ash dieback heavy across the Midlands and TPO and conservation-area rules shaping much of the work, alongside National Forest planting nearby. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Small outfits carry most of the load: a climber and a groundsman, a family business, a one or two-van firm working across Hinckley, Burbage, Earl Shilton, Market Bosworth and the wider Hinckley and Bosworth patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's gardens, commons and canal-side woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Hinckley's Burbage Common, the Ashby Canal and the Market Bosworth woods",
 },
 "middleton": {
  "region":"Middleton and Greater Manchester",
  "nearby":["Heywood", "Rochdale", "Bury"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Middleton, from sole-trader climbers and groundsmen to small firms working Alkrington Woods, Boggart Hole Clough and the Irk valley, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews who climb and clear Greater Manchester's trees",
  "s1loc":[
   "Sitting in the Rochdale borough where the Irk valley threads down toward Manchester, Middleton holds a big stock of mature street, park and woodland trees, and keeping that estate safe keeps a steady community of arborists and tree surgeons busy across the town and north Greater Manchester. Most are sole traders and small teams on domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the local geography. Suburbs like Alkrington and Rhodes carry mature oak, beech and estate trees, while Alkrington Woods on the River Irk, Boggart Hole Clough and the wider Irk valley green corridor hold parkland and broadleaf woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms working Middleton, Heywood, Rochdale and Bury.",
   "It is a safety-critical trade run to recognised standards. Middleton tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with ash dieback confirmed across the Bury and Rochdale districts driving felling and replanting alongside City of Trees and the Pennine Edge Forest. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "These are small outfits for the most part: a climber and a groundsman, a family business, a one or two-van crew covering Middleton, Heywood and the wider Rochdale and Bury patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's gardens, parks and Irk valley woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Middleton's gardens, Alkrington Woods and the Irk valley",
 },
 "ashton-under-lyne": {
  "region":"Ashton-under-Lyne and Tameside",
  "nearby":["Stalybridge", "Hyde", "Denton"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Ashton-under-Lyne, from sole-trader climbers and groundsmen to small firms working Daisy Nook, Stamford Park and the Medlock valley, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Tameside's trees",
  "s1loc":[
   "Set in Tameside on the edge of the Greater Manchester conurbation, Ashton-under-Lyne carries a deep estate of mature street, park and valley trees, and managing it keeps a busy community of arborists and tree surgeons working across the town and the wider borough. Most are sole traders and small teams on domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work tracks the local landscape. The leafy ground around Stamford Park and the Dingle, Daisy Nook Country Park in the Medlock valley and the woodland cloughs of Haughton Dale and Hurst Clough carry mature oak, beech and estate trees, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms working Ashton-under-Lyne, Stalybridge, Hyde and Denton.",
   "It is a safety-critical trade run to recognised standards. Ashton tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with ash dieback now endemic across Tameside driving the council and contractors to fell and replant on council land, schools and housing sites. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Mostly these are small outfits: a climber and a groundsman, a family business, a one or two-van crew covering Ashton, Stalybridge, Hyde and Denton and the Tame and Medlock valleys. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's parks, country parks and Medlock valley tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Ashton-under-Lyne's parks, Daisy Nook and the Medlock valley",
 },
 "sutton-in-ashfield": {
  "region":"Sutton-in-Ashfield and Nottinghamshire",
  "nearby":["Mansfield", "Hucknall", "Alfreton"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Sutton-in-Ashfield, from sole-trader climbers and groundsmen to small firms working Brierley Forest Park, Silverhill Wood and the Maun valley, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews who climb and clear Ashfield's trees",
  "s1loc":[
   "A former mining town at the heart of Nottinghamshire's Ashfield district, Sutton-in-Ashfield has greened a lot of its old colliery ground into woodland and park, and managing that growing tree estate keeps a community of arborists and tree surgeons busy across the town and north Notts. Most are sole traders and small teams on domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the reclaimed landscape. Brierley Forest Park on the old Sutton Colliery site, with its arboretum and broadleaf and conifer plantings, Silverhill Wood near Teversal, and the Maun corridor at King's Mill Reservoir and Sutton Lawn carry maturing oak, birch and mixed woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms working Sutton-in-Ashfield, Mansfield, Hucknall and Alfreton.",
   "It is a safety-critical trade run to recognised standards. Ashfield tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with ash dieback now endemic across Nottinghamshire and TPO and conservation-area rules shaping much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "For the most part these are small outfits: a climber and a groundsman, a family business, a one or two-van crew covering Sutton, Mansfield, Hucknall and Alfreton and the reclaimed colliery woodland between them. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's parks, reclaimed colliery woodland and Maun valley tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Sutton-in-Ashfield's Brierley Forest Park, Silverhill Wood and the Maun valley",
 },
 "chippenham": {
  "region":"Chippenham and Wiltshire",
  "nearby":["Trowbridge", "Melksham", "Swindon"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Chippenham, from sole-trader climbers and groundsmen to small firms working the Bowood estate, Monkton Park and the Avon, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Wiltshire's trees",
  "s1loc":[
   "Standing at a historic crossing of the River Avon in north Wiltshire, Chippenham is a market town wrapped in estate parkland and broadleaf woodland, and looking after that tree estate keeps a steady community of arborists and tree surgeons busy across the town and the county. Most are sole traders and small teams on domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the Wiltshire landscape. Suburbs like Pewsham and Monkton carry mature garden and street trees, while Monkton Park and the Avon, Maud Heath's Causeway country, Vincients Wood on the western edge and the great labelled tree collection of the Bowood estate toward Calne hold parkland and woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms working Chippenham, Trowbridge, Melksham and Swindon.",
   "It is a safety-critical trade run to recognised standards. Chippenham tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with ash dieback driving felling and native replanting at sites like Vincients Wood and TPO and conservation-area rules shaping much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "These tend to be small outfits: a climber and a groundsman, a family business, a one or two-van crew covering Chippenham, Trowbridge, Melksham and Swindon and the Avon valley estates between them. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's gardens, estate parkland and Avon valley woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Chippenham's Bowood estate, Monkton Park and the Avon",
 },
 "caerphilly": {
  "region":"Caerphilly and south Wales",
  "nearby":["Pontypridd", "Cardiff", "Newport"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Caerphilly, from sole-trader climbers and groundsmen to small firms working Caerphilly Castle parkland, the Aber Valley and Cwmcarn Forest, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews who climb and clear the south Wales valleys' trees",
  "s1loc":[
   "Wrapped around its great castle on the southern edge of the valleys, Caerphilly sits among regreened hillsides and forestry that keep a busy community of arborists and tree surgeons working across the town and the wider county borough. Most are sole traders and small teams on domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work climbs the valley landscape. The parkland around Caerphilly Castle, the wooded Aber Valley up toward Senghenydd, the ridge of Mynydd y Grug above Bedwas and the Natural Resources Wales forestry at Cwmcarn carry oak, beech, larch and mixed conifer, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms working Caerphilly, Pontypridd, Cardiff and Newport.",
   "It is a safety-critical trade run to recognised standards. Caerphilly tree surgeons are typically NPTC and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with ash dieback confirmed in the castle grounds and Natural Resources Wales and Coed Cymru driving big larch-disease felling at Cwmcarn and Storm Darragh clearance across the Welsh woodland estate. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Across the borough the outfits are mostly small: a climber and a groundsman, a family business, a one or two-van crew covering Caerphilly, Pontypridd, Cardiff and Newport and the wooded valleys between them. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the borough's castle parkland, valley woodland and forestry tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Caerphilly's castle parkland, the Aber Valley and Cwmcarn Forest",
 },
 "coatbridge": {
  "region":"Coatbridge and North Lanarkshire",
  "nearby":["Airdrie", "Motherwell", "Bellshill"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Coatbridge, from sole-trader climbers and groundsmen to small firms working Drumpellier Country Park, the Monkland Canal corridor and North Lanarkshire woodland, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews who climb and clear Lanarkshire's trees",
  "s1loc":[
   "A former ironworks and canal town, Coatbridge has grown a green edge of mature park, street and estate trees, and keeping that estate safe supports a steady community of arborists and tree surgeons across the town and the wider North Lanarkshire patch. Most are sole traders and small teams on domestic gardens, council and park contracts and storm clearance, and every one of them depends on proper chainsaw PPE.",
   "The work follows the local ground. Drumpellier Country Park carries 500 acres of mixed woodland, lochs and SSSI ground, while the Monkland Canal corridor, Summerlee and the leafier streets toward Townhead and Blairhill hold mature oak, beech and lime, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Coatbridge tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with TPO and conservation-area rules and clear-up after Storm Eowyn shaping much of the recent work alongside Forestry and Land Scotland and NatureScot guidance. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "These are small outfits for the most part: a climber and a groundsman, a family business, a one or two-van crew working across Coatbridge, Airdrie and the wider North Lanarkshire ground. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's parks, canal corridor and Lanarkshire woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Coatbridge's parks, the Monkland Canal corridor and North Lanarkshire woodland",
 },
 "lytham st annes": {
  "region":"Lytham St Annes and the Fylde coast",
  "nearby":["Blackpool", "Poulton-le-Fylde", "Preston"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Lytham St Annes, from sole-trader climbers and groundsmen to small firms working Lytham Hall's Great Wood, Ashton Gardens and the Fylde coast dunes, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear the Fylde coast's trees",
  "s1loc":[
   "Known locally as Leafy Lytham for its mature tree-lined streets, Lytham St Annes carries a large estate of park, garden and avenue trees, and looking after it keeps a busy community of arborists and tree surgeons working across the town and the wider Fylde coast. Most are sole traders and small teams on domestic gardens, council and park contracts and storm clearance, each one dependent on proper chainsaw PPE.",
   "The work follows the coastal geography. Lytham Hall sits in 78 acres of historic woodland with its Great Wood and Witch Wood, while Ashton Gardens, Lowther Gardens, Fairhaven Lake and the leafier streets of Ansdell and Fairhaven hold mature oak, beech and lime, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Lytham tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with ash dieback removals, TPO and conservation-area rules and storm clear-up shaping much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Mostly these are small outfits: a climber and a groundsman, a family business, a one or two-van crew working across Lytham, St Annes and the wider Fylde and Preston ground. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's parks, hall woodland and Fylde coast tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Lytham St Annes's parks, Lytham Hall woodland and Fylde coast dunes",
 },
 "worksop": {
  "region":"Worksop and Nottinghamshire",
  "nearby":["Retford", "Mansfield", "Chesterfield"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Worksop, from sole-trader climbers and groundsmen to small firms working Clumber Park, Sherwood Forest and the Dukeries estates, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews who climb and clear the Dukeries' trees",
  "s1loc":[
   "Gateway to the Dukeries and the northern edge of Sherwood Forest, Worksop sits among some of the most heavily wooded country in the Midlands, and managing that estate keeps a strong community of arborists and tree surgeons busy across the town and the wider Nottinghamshire patch. Most are sole traders and small teams on domestic gardens, estate and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the Dukeries geography. Clumber Park spreads over 3,800 acres of parkland, heath and woods with its two-mile Lime Tree Avenue, while Sherwood Forest, the Welbeck and Thoresby estates and Hannah Park Wood on the sandstone escarpment hold ancient oak, beech and lime, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Worksop tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with ash dieback, veteran-tree work around Sherwood's ancient oaks and TPO and conservation-area rules shaping much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "For the most part these are small outfits: a climber and a groundsman, a family business, a one or two-van crew working across Worksop, Retford and the wider Bassetlaw and Mansfield ground. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the Dukeries estates, parks and Sherwood woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Worksop's Dukeries estates, Clumber Park and Sherwood Forest woodland",
 },
 "leigh": {
  "region":"Leigh and Greater Manchester",
  "nearby":["Wigan", "Hindley", "Atherton"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Leigh, from sole-trader climbers and groundsmen to small firms working Pennington Flash, Lilford Park and the Bridgewater Canal corridor, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Wigan borough's trees",
  "s1loc":[
   "A former mining and mill town reclaimed as green space, Leigh carries a growing estate of park, canal and street trees, and keeping it safe supports a steady community of arborists and tree surgeons across the town and the wider Wigan borough. Most are sole traders and small teams on domestic gardens, council and park contracts and storm clearance, each one dependent on proper chainsaw PPE.",
   "The work follows the local ground. Pennington Flash Country Park holds reclaimed parkland and woodland off the Bridgewater Canal, while Lilford Park in the grounds of the old Atherton Hall estate, Pennington Hall Park and the leafier streets toward Atherton and Hindley carry mature oak, beech and lime, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Leigh tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with ash dieback removals, TPO and conservation-area rules and storm clear-up shaping much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "These are small outfits for the most part: a climber and a groundsman, a family business, a one or two-van crew working across Leigh, Atherton and the wider Wigan and Greater Manchester ground. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's parks, canal corridor and Wigan borough woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Leigh's parks, Pennington Flash and the Bridgewater Canal corridor",
 },
 "bexhill-on-sea": {
  "region":"Bexhill-on-Sea and East Sussex",
  "nearby":["Hastings", "Eastbourne", "Hailsham"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Bexhill-on-Sea, from sole-trader climbers and groundsmen to small firms working Highwoods, Combe Valley and the High Weald woodland, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews who climb and clear East Sussex's trees",
  "s1loc":[
   "Set on the edge of the most wooded country in England, Bexhill-on-Sea carries a large estate of park, garden and street trees backed by the ancient woods of the High Weald, and managing it keeps a busy community of arborists and tree surgeons working across the town and the wider East Sussex coast. Most are sole traders and small teams on domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the local geography. Highwoods holds 83 acres of traditional coppiced sessile oak and birch on the town's northern edge, while Combe Valley Countryside Park, Egerton Park and the leafier streets toward Cooden and Sidley carry mature oak, ash and elm, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Bexhill tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with widespread ash dieback removals across the High Weald and TPO and conservation-area rules shaping much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Mostly these are small outfits: a climber and a groundsman, a family business, a one or two-van crew working across Bexhill, Hastings and the wider Rother and East Sussex ground. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's parks, coppiced woods and High Weald tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Bexhill-on-Sea's parks, Highwoods and the High Weald woodland",
 },
 "altrincham": {
  "region":"Altrincham and Trafford, Greater Manchester",
  "nearby":["Stretford", "Urmston", "Wilmslow"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Altrincham, from sole-trader climbers and groundsmen to small firms working Dunham Massey's ancient deer park, the Bollin valley and Bowdon's leafy avenues, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews who climb and clear Trafford's trees",
  "s1loc":[
   "Few Greater Manchester towns are as wooded as Altrincham, a green corner of Trafford with mature street, garden and parkland trees that keep a steady community of arborists and tree surgeons in work across the town and out into north Cheshire. The trade here is built on sole traders and small teams, every one of them dependent on proper chainsaw PPE.",
   "The work follows the town's leafy geography. Affluent suburbs like Bowdon, Hale and Hale Barns carry heavy mature oak, beech and estate trees, while Dunham Massey's ancient 300-acre National Trust deer park, the Bollin valley and the streets around the Old Market Place conservation area hold parkland and woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Altrincham tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and Trafford's many conservation areas and TPOs shape much of the work, alongside ongoing ash dieback removal. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Outfits here stay small by nature: a climber and a groundsman, a family business, a one or two-van firm working Altrincham, Bowdon, Timperley and the wider Trafford and north Cheshire patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's gardens, parks and parkland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Altrincham's gardens, Dunham Massey parkland and the Bollin valley",
 },
 "urmston": {
  "region":"Urmston and Trafford, Greater Manchester",
  "nearby":["Stretford", "Altrincham", "Manchester"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Urmston, from sole-trader climbers and groundsmen to small firms working Davyhulme Park, the Mersey valley and Urmston Meadows, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear the Mersey valley's trees",
  "s1loc":[
   "Urmston is a green, tree-lined corner of Trafford, its verdant suburban streets and Mersey-side open spaces holding a large estate of mature trees that keeps a community of arborists and tree surgeons busy across the town and into Greater Manchester. Most are sole traders and small teams, every one of them dependent on proper chainsaw PPE.",
   "The work follows the town's geography. Established suburbs across Urmston, Flixton and Davyhulme carry mature garden and street trees, while Davyhulme Park, the Davyhulme Millennium Nature Reserve along the Ship Canal, Urmston Meadows and the wider Mersey valley and Stretford Ees hold parkland and riverside woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Urmston tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with Trafford TPOs, conservation areas and ash dieback all shaping the workload. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "These are mostly small outfits: a climber and a groundsman, a family business, a one or two-van firm working Urmston, Flixton, Stretford and the wider Mersey valley patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's gardens, parks and Mersey valley tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Urmston's gardens, Davyhulme parks and the Mersey valley",
 },
 "grantham": {
  "region":"Grantham and Lincolnshire",
  "nearby":["Newark", "Stamford", "Melton Mowbray"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Grantham, from sole-trader climbers and groundsmen to small firms working the Belton estate, Londonthorpe Woods and Wyndham Park, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews who climb and clear Lincolnshire's trees",
  "s1loc":[
   "Set among the wooded edges of the Lincolnshire uplands, Grantham carries a large estate of mature street, park and estate trees, and managing it keeps a steady community of arborists and tree surgeons busy across the town and the surrounding countryside. Most are sole traders and small teams, every one of them dependent on proper chainsaw PPE.",
   "The work follows the town's geography. Villages and suburbs like Manthorpe, Londonthorpe, Belton and Harlaxton carry mature oak, beech and estate trees, while the National Trust's Belton estate with its ancient wooded parkland, the Woodland Trust's Londonthorpe Woods, Wyndham Park and the river Witham hold parkland and woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Grantham tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with ash dieback across the county's woods and hedgerows and TPO and conservation-area rules shaping much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Firms here run lean: a climber and a groundsman, a family business, a one or two-van outfit working Grantham, Belton, Ancaster and the wider south Lincolnshire patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's gardens, parks and estate woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Grantham's gardens, the Belton estate and Londonthorpe Woods",
 },
 "boston": {
  "region":"Boston and the Lincolnshire fens",
  "nearby":["Skegness", "Spalding", "Lincoln"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Boston, from sole-trader climbers and groundsmen to small firms working Central Park, the Witham and the fenland around Frampton Marsh, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear the fenland's trees",
  "s1loc":[
   "Out on the flat Lincolnshire fens, Boston holds its trees in town parks, churchyards, garden plots and the shelterbelts and windbreaks that punctuate an otherwise open, near-treeless landscape, and managing them keeps a community of arborists and tree surgeons busy across the town and the surrounding fen. Most are sole traders and small teams, every one of them dependent on proper chainsaw PPE.",
   "The work follows the town's geography. Boston Central Park, the streets around the Stump and St Botolph's, the river Witham and The Haven and the fen-edge land out towards Frampton Marsh hold the bulk of the mature trees, alongside roadside and field-boundary planting, all of it generating crown reductions, dismantles, felling, deadwooding, shelterbelt work and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Boston tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with ash dieback thinning the county's hedgerow and shelterbelt trees and TPO and conservation-area rules shaping much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Outfits stay small out here: a climber and a groundsman, a family business, a one or two-van firm working Boston, Frampton, Kirton and the wider fenland patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's parks, churchyards and fenland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Boston's Central Park, the Witham and the fenland around Frampton Marsh",
 },
 "newbury": {
  "region":"Newbury and Berkshire",
  "nearby":["Thatcham", "Reading", "Basingstoke"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Newbury, from sole-trader climbers and groundsmen to small firms working Snelsmore Common, Greenham Common and the Kennet valley, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews who climb and clear Berkshire's trees",
  "s1loc":[
   "Wrapped in heath, common and river-valley woodland, Newbury carries a large estate of mature street, park and estate trees, and managing it keeps a steady community of arborists and tree surgeons busy across the town and West Berkshire. Most are sole traders and small teams, every one of them dependent on proper chainsaw PPE.",
   "The work follows the town's geography. Areas like Donnington, Speen, Wash Common and Shaw carry mature oak, beech and estate trees, while Snelsmore Common Country Park with its ancient broadleaved woodland, Greenham and Crookham Commons, Bowdown Woods and the Kennet valley hold heathland, woodland and riverside trees, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Newbury tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with active ash dieback work in West Berkshire woods like Bowdown alongside TPO and conservation-area rules shaping much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Most firms here are small: a climber and a groundsman, a family business, a one or two-van outfit working Newbury, Donnington, Thatcham and the wider West Berkshire patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's gardens, commons and valley woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Newbury's gardens, Snelsmore and Greenham commons and the Kennet valley",
 },
 "cleethorpes": {
  "region":"Cleethorpes and North East Lincolnshire",
  "nearby":["Grimsby", "Scunthorpe", "Hull"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Cleethorpes, from sole-trader climbers and groundsmen to small firms working Cleethorpes Country Park, Sidney Park and the wind-exposed trees of the Humber coast, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews that keep the Humber coast's trees in check",
  "s1loc":[
   "For a breezy coastal town, Cleethorpes carries a real spread of street, park and garden trees, and looking after them on this exposed Humber edge keeps a steady community of arborists and tree surgeons working across North East Lincolnshire. Most are sole traders and small teams on domestic gardens, council and park contracts and storm clearance, and every one of them leans on proper chainsaw PPE.",
   "The work tracks the local geography. Cleethorpes Country Park with its lake and planted woodland, Sidney Park near the seafront and the maturing street trees inland all carry tree work, while the wind-pruned, salt-stressed canopy along the coast and out toward Grimsby keeps crews busy with crown reductions, dismantles, felling, deadwooding and stump grinding.",
   "It is a safety-critical trade run to recognised standards. Cleethorpes tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and TPO and conservation-area rules shape much of the job. Dutch elm disease confirmed by North East Lincolnshire Council's trees and woodland officers around the Kings Road and Lakeside area means removals and replanting, and every chainsaw cut, on the ground or up a rope, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "These are small outfits for the most part: a climber and a groundsman, a family firm, a one or two-van team working across Cleethorpes, Grimsby and the wider North East Lincolnshire patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, with no procurement department or trade account in the way.",
  ],
  "kit_loc":"across the town's parks, seafront and Humber-coast tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Cleethorpes's Country Park, Sidney Park and wind-exposed coastal trees",
 },
 "bicester": {
  "region":"Bicester and Oxfordshire",
  "nearby":["Oxford", "Banbury", "Aylesbury"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Bicester, from sole-trader climbers and groundsmen to small firms working Bure Park, Burnehyll Community Woodland and the garden town's new tree planting, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Oxfordshire's trees",
  "s1loc":[
   "As a designated garden town, Bicester is being planted up fast, and that growing estate of street, park and woodland trees keeps a busy community of arborists and tree surgeons working across this corner of Oxfordshire. Most are sole traders and small teams on domestic gardens, estate and park contracts and storm clearance, all of them dependent on proper chainsaw PPE.",
   "The work follows the local geography. Bure Park Local Nature Reserve on the River Bure, Garth Park in the town centre and the new Burnehyll Community Woodland on the outskirts carry tree work, as do the maturing trees through Langford Village, Kingsmere and Graven Hill and the stone-built villages of Wendlebury, Chesterton, Bucknell and Launton, generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Bicester tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and TPO and conservation-area rules shape much of the work. Ash dieback remains a significant concern for tree management across Oxfordshire, and every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Mostly these are small outfits: a climber and a groundsman, a family business, a one or two-van team working across Bicester, Bicester Village and the wider Cherwell patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the garden town's parks, woodland and new tree planting",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Bicester's parks, community woodland and garden-town planting",
 },
 "ramsgate": {
  "region":"Ramsgate and Thanet, Kent",
  "nearby":["Margate", "Broadstairs", "Deal"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Ramsgate, from sole-trader climbers and groundsmen to small firms working Ellington Park, King George VI Memorial Park and the chalk coast above Pegwell Bay, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews that climb and clear Thanet's trees",
  "s1loc":[
   "Set on the chalk of the Isle of Thanet, Ramsgate carries a good estate of park, street and garden trees, and managing them keeps a steady community of arborists and tree surgeons working across this corner of east Kent. Most are sole traders and small teams on domestic gardens, council and park contracts and storm clearance, every one of them reliant on proper chainsaw PPE.",
   "The work follows the town's geography. Ellington Park in the heart of Ramsgate and the woodland of King George VI Memorial Park high on the cliffs toward Broadstairs carry tree work, as do the maturing trees through Nethercourt, Eastcliff and the inland parish of St Lawrence, while the exposed chalk coast and the scrub around Pegwell Bay add to the crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Ramsgate tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with Thanet District Council managing TPOs and conservation areas. Ash dieback is well established across east Kent, where ash is the most common tree, and every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "For the most part these are small outfits: a climber and a groundsman, a family business, a one or two-van team working across Ramsgate, Broadstairs and the wider Thanet patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's parks, clifftop and chalk-coast tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Ramsgate's parks, clifftop woodland and chalk coast",
 },
 "margate": {
  "region":"Margate and Thanet, Kent",
  "nearby":["Ramsgate", "Broadstairs", "Herne Bay"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Margate, from sole-trader climbers and groundsmen to small firms working Dane Park, Tivoli Park and the exposed chalk coast of Thanet, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear the Thanet coast's trees",
  "s1loc":[
   "Out on the exposed chalk of Thanet, Margate still holds a real spread of park, street and garden trees, and keeping them safe keeps a busy community of arborists and tree surgeons working across this stretch of north Kent. Most are sole traders and small teams on domestic gardens, council and park contracts and storm clearance, all of them dependent on proper chainsaw PPE.",
   "The work tracks the local geography. Dane Park in the heart of town, the Tivoli Park and Hartsdown Park woodlands to the west and Northdown Park out at Palm Bay carry tree work, as do the maturing trees through Cliftonville, Westbrook and Westgate-on-Sea and the recent planting at Westover Gardens, all generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Margate tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with Thanet District Council managing TPOs and conservation areas. Ash dieback is well established across east Kent, where ash is the most common tree, and every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Mostly these are small outfits: a climber and a groundsman, a family business, a one or two-van team working across Margate, Cliftonville and the wider Thanet patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's parks, gardens and exposed chalk-coast tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Margate's parks, woodland and exposed chalk coast",
 },
 "sittingbourne": {
  "region":"Sittingbourne and Swale, Kent",
  "nearby":["Faversham", "Chatham", "Maidstone"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Sittingbourne, from sole-trader climbers and groundsmen to small firms working Milton Creek Country Park, the surrounding orchards and the ancient woodland of the Kent Downs, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews that climb and clear Swale's trees",
  "s1loc":[
   "Set between the Saxon Shore and the Kent Downs, Sittingbourne carries a real mix of orchard, park, street and garden trees, and managing them keeps a steady community of arborists and tree surgeons working across Swale. Most are sole traders and small teams on domestic gardens, orchard and park contracts and storm clearance, every one of them reliant on proper chainsaw PPE.",
   "The work follows the local geography. Milton Creek Country Park on its tidal inlet, with restored orchard and Forestry Commission-funded woodland planting, carries tree work, as do the maturing trees through Borden, Bobbing, Tunstall and Milton Regis and the orchards and ancient woodland rising south toward Bredgar, Stockbury and the Kent Downs, all generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Sittingbourne tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and TPO and conservation-area rules shape much of the work. Ash dieback is well established in this part of Kent, where ash makes up almost a fifth of all trees, and every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "For the most part these are small outfits: a climber and a groundsman, a family business, a one or two-van team working across Sittingbourne, Faversham and the wider Swale patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's country park, orchards and Kent Downs tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Sittingbourne's country park, orchards and Kent Downs woodland",
 },
 "hatfield": {
  "region":"Hatfield and Hertfordshire",
  "nearby":["Welwyn Garden City", "St Albans", "Hertford"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Hatfield, from sole-trader climbers and groundsmen to small firms working Hatfield Park's veteran oaks, Mill Green and the surrounding green belt woodland, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews who climb and clear Hertfordshire's trees",
  "s1loc":[
   "Set in the green belt between the old town and the new, Hatfield carries a heavy estate of mature park, street and garden trees, and looking after them keeps a steady community of arborists and tree surgeons busy across the town and wider Hertfordshire. Most are sole traders and small teams on domestic gardens, council and park contracts and storm clearance, and every one of them leans on proper chainsaw PPE.",
   "The work tracks the local geography. Areas like Old Hatfield, Roe Green and the wood-pasture of Hatfield Park carry ancient oak, hornbeam and beech pollards, while Mill Green, the Ellenbrook Fields and the green belt woodland fringing the Lea and Mimram valleys hold parkland and copses, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Hatfield tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with TPOs, the Welwyn Garden City estate management scheme, conservation-area rules and ash dieback all shaping the workload. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "These are mostly small outfits: a climber and a groundsman, a family business, a one or two-van team working across Hatfield, Welwyn Garden City and the surrounding Hertfordshire patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's parks, estate woodland and green belt tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Hatfield's parks, estate woodland and green belt",
 },
 "bishop's stortford": {
  "region":"Bishop's Stortford and Hertfordshire",
  "nearby":["Harlow", "Hertford", "Hoddesdon"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Bishop's Stortford, from sole-trader climbers and groundsmen to small firms working Hatfield Forest, the Stort valley and Southern Country Park, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear the Stort valley's trees",
  "s1loc":[
   "Strung along the Stort valley on the Hertfordshire and Essex border, Bishop's Stortford is a leafy market town with a deep stock of mature park, riverside and garden trees, and managing them keeps a busy community of arborists and tree surgeons working across the town and surrounding countryside. Most are sole traders and small teams on domestic gardens, council and park contracts and storm clearance, all of them dependent on proper chainsaw PPE.",
   "The work follows the town's wooded geography. Thorley, Thorley Park and St Michael's Mead sit close to the mature woodland of Thorley Lane East Woods and the Southern Country Park, while Castle Park, Grange Paddocks and the Red, White and Blue open space carry oak, hornbeam, rowan and hazel along the River Stort, and the National Trust's Hatfield Forest lies just to the east, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Stortford tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with tree preservation orders at Thorley Lane East Woods, conservation areas and ash dieback all shaping the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "And the firms tend to be small: a climber and a groundsman, a family business, a one or two-van outfit working across Bishop's Stortford, Sawbridgeworth and the wider Stort valley patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's parks, riverside and forest tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Bishop's Stortford's parks, the Stort valley and Hatfield Forest",
 },
 "wokingham": {
  "region":"Wokingham and Berkshire",
  "nearby":["Reading", "Bracknell", "Camberley"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Wokingham, from sole-trader climbers and groundsmen to small firms working Elms Field, the Emm Brook, Dinton Pastures and the Bramshill Forest fringe, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews who climb and clear Berkshire's trees",
  "s1loc":[
   "A recognised Tree City with a strong stock of mature park, street and garden trees, Wokingham keeps a steady community of arborists and tree surgeons busy across the town and the wider Berkshire patch. Most are sole traders and small teams on domestic gardens, council and park contracts and storm clearance, every one of them reliant on proper chainsaw PPE.",
   "The work follows the town's leafy geography. Emmbrook, Woosehill and Wescott carry mature oak, lime, birch and maple, while Elms Field in the centre, the Emm Brook and Woosehill Riverside Walk, Dinton Pastures Country Park along the Loddon and the Forestry England pines of the Bramshill Forest fringe hold parkland and woodland, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Wokingham tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with tree preservation orders, conservation areas and ash dieback all shaping the work and protected-tree felling a live local concern. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Most of these outfits are small: a climber and a groundsman, a family business, a one or two-van team working across Wokingham, Winnersh and the wider Berkshire patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's parks, brook valleys and woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Wokingham's parks, the Emm Brook and Dinton Pastures",
 },
 "feltham": {
  "region":"Feltham and West London",
  "nearby":["Hounslow", "Twickenham", "Staines"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Feltham, from sole-trader climbers and groundsmen to small firms working Feltham Park, the river Crane, Hanworth Park and Bedfont, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear West London's trees",
  "s1loc":[
   "Greener than most of West London, Feltham carries a broad stock of mature park, street and garden trees, and looking after them keeps a busy community of arborists and tree surgeons working across the town and the London Borough of Hounslow. Most are sole traders and small teams on domestic gardens, council and park contracts and storm clearance, all of them dependent on proper chainsaw PPE.",
   "The work tracks the local geography. Feltham, Hanworth and Bedfont carry mature street and garden trees, while Feltham Park, the river Crane and Crane Park, Hanworth Park on the old air park and the lakes and woodland of Bedfont Lakes Country Park hold parkland and damp riverside woods, with Hounslow Heath nearby, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Feltham tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with tree preservation orders, conservation areas and ash dieback all shaping the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Running it are mostly small outfits: a climber and a groundsman, a family business, a one or two-van team working across Feltham, Hanworth and the wider Hounslow patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's parks, riverside and country park tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Feltham's parks, the river Crane and Bedfont Lakes",
 },
 "farnham": {
  "region":"Farnham and Surrey",
  "nearby":["Aldershot", "Godalming", "Guildford"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Farnham, from sole-trader climbers and groundsmen to small firms working Farnham Park, Alice Holt Forest, the Bourne woods and the North Downs, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the crews who climb and clear Surrey's trees",
  "s1loc":[
   "Wrapped in deer park, forest and downland woodland, Farnham carries a deep stock of mature park, street and garden trees, and managing them keeps a busy community of arborists and tree surgeons working across the town and west Surrey. Most are sole traders and small teams on domestic gardens, council and park contracts and storm clearance, every one of them reliant on proper chainsaw PPE.",
   "The work follows the town's wooded geography. The medieval deer park of Farnham Park carries ancient oak, lime and beech, while the Forestry England woodlands of Alice Holt Forest and the Bourne woods south of the town, plus the wooded slopes of the North Downs and the Bourne, hold parkland and forest, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Farnham tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with tree preservation orders, conservation areas and ash dieback all shaping the work, and a long memory of Dutch elm disease in Farnham Park. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Behind it all are mostly small outfits: a climber and a groundsman, a family business, a one or two-van team working across Farnham, Godalming and the wider Waverley patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's deer park, forest and downland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Farnham's deer park, Alice Holt Forest and the Bourne woods",
 },
 "fareham": {
  "region":"Fareham and Hampshire",
  "nearby":["Gosport", "Portsmouth", "Eastleigh"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Fareham, from sole-trader climbers and groundsmen to small firms working Holly Hill Woodland Park, the Cams Hall estate and the Meon valley, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear south Hampshire's trees",
  "s1loc":[
   "Set between Portsmouth Harbour and the Meon valley, Fareham is a green borough with a deep estate of mature street, park and estate trees, and looking after it keeps a busy community of arborists and tree surgeons working across the town and south Hampshire. Most are sole traders and small teams on domestic gardens, council and park contracts and storm clearance, and every one of them depends on proper chainsaw PPE.",
   "The work follows the borough's leafy geography. Holly Hill Woodland Park carries ancient oak, beech and yew alongside swamp cypress and coastal redwood down to the River Hamble, while the Cams Hall estate, the Cams Plantation tree belt, Funtley, Titchfield and Wallington hold mature parkland and garden trees, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Fareham tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and with more than 5,000 properties under Tree Preservation Orders and conservation-area cover at Cams Hall, TPO and conservation rules shape much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Small outfits carry this work: a climber and a groundsman, a family business, a one or two-van team covering Fareham, Stubbington and the wider south Hampshire patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the borough's gardens, parks and woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Fareham's gardens, Holly Hill woodland and the Meon valley",
 },
 "chorley": {
  "region":"Chorley and Lancashire",
  "nearby":["Leyland", "Preston", "Horwich"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Chorley, from sole-trader climbers and groundsmen to small firms working Astley Park, Healey Nab and the Yarrow valley, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Lancashire's trees",
  "s1loc":[
   "Sitting at the foot of the West Pennine Moors, Chorley is a green town with a large estate of mature street, park and woodland trees, and managing it keeps a strong community of arborists and tree surgeons busy across the borough and Lancashire. Most are sole traders and small teams working domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the town's leafy geography. Astley Park and Hall hold mature parkland trees in the centre, while Healey Nab, Duxbury Woods, the Yarrow Valley Country Park, Cuerden Valley and the wooded edges of Euxton, Adlington and Coppull carry oak, beech and the moorland-fringe plantations, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Chorley tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with ash dieback now widespread across Lancashire driving felling of brittle, unstable trees alongside TPO and conservation-area rules. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Small outfits run this work: a climber and a groundsman, a family business, a one or two-van team covering Chorley, Leyland and the wider West Pennine patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's parks, valleys and moorland-fringe tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Chorley's parks, Healey Nab and the Yarrow valley",
 },
 "castleford": {
  "region":"Castleford and West Yorkshire",
  "nearby":["Pontefract", "Normanton", "Featherstone"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Castleford, from sole-trader climbers and groundsmen to small firms working Fairburn Ings, Pontefract Park and the Aire and Calder, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear the Aire valley's trees",
  "s1loc":[
   "Where the Aire and the Calder meet, Castleford is a town of reclaimed coalfield greenery with a growing estate of maturing street, park and woodland trees, and looking after it keeps a busy community of arborists and tree surgeons working across the town and the Wakefield district. Most are sole traders and small teams on domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the lower Aire valley's geography. RSPB Fairburn Ings carries wet and deciduous woodland reclaimed from old coal spoil, while Pontefract Park's woodland and lake, the Aire and Calder Navigation corridor and the wooded edges of Normanton and Featherstone hold birch, willow and maturing oak, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Castleford tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, with Wakefield Council's urban tree and woodland strategy, TPO and conservation-area rules at Newmillerdam shaping much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Small outfits carry this work: a climber and a groundsman, a family business, a one or two-van team covering Castleford, Pontefract and the wider Five Towns patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's parks, reserves and riverside tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Castleford's parks, Fairburn Ings and the Aire and Calder",
 },
 "ilkeston": {
  "region":"Ilkeston and Derbyshire",
  "nearby":["Long Eaton", "Ripley", "Derby"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Ilkeston, from sole-trader climbers and groundsmen to small firms working Shipley Country Park, the Erewash valley and Straws Bridge, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear the Erewash valley's trees",
  "s1loc":[
   "Strung along the Erewash valley on the Derbyshire and Nottinghamshire border, Ilkeston is a green Erewash town with a deep estate of mature street, park and woodland trees, and managing it keeps a busy community of arborists and tree surgeons working across the town and the wider county. Most are sole traders and small teams on domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the valley's geography. Shipley Country Park holds over 600 acres of lakes and woodland to the north, while Straws Bridge, Pewit Carr, Pioneer Meadows and the wooded edges of Cotmanhay, Kirk Hallam and West Hallam carry oak, ash and the old colliery plantations, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Ilkeston tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and with around 9 million ash trees in Derbyshire and a multi-million-pound county ash dieback programme felling brittle, unstable trees, that work and TPO and conservation rules shape much of the trade. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Small outfits run this work: a climber and a groundsman, a family business, a one or two-van team covering Ilkeston, Long Eaton and the wider Erewash patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's parks, valley and woodland tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Ilkeston's parks, Shipley Country Park and the Erewash valley",
 },
 "cramlington": {
  "region":"Cramlington and Northumberland",
  "nearby":["Blyth", "Bedlington", "Morpeth"],
  "snapshot":"iNeedWorkwear supplies chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs to arborists, tree surgeons and forestry contractors across Cramlington, from sole-trader climbers and groundsmen to small firms working Plessey Woods Country Park, Northumberlandia and the Blyth valley, all rated to EN ISO 11393, branded in-house and ordered direct online with no account needed.",
  "s1_head":"Kitting the people who climb and clear Northumberland's trees",
  "s1loc":[
   "Set on the coastal plain north of Newcastle, Cramlington is a green Northumberland town with a maturing estate of street, park and woodland trees, and looking after it keeps a busy community of arborists and tree surgeons working across the town and south-east Northumberland. Most are sole traders and small teams on domestic gardens, council and park contracts and storm clearance, every one of them dependent on proper chainsaw PPE.",
   "The work follows the Blyth valley's geography. Plessey Woods Country Park carries a hundred acres of riverside oak woodland along the River Blyth, while Northumberlandia's landscaped slopes, the Arcot Hall grasslands and the green edges of Beaconhill, Eastfield and Collingwood hold maturing parkland and garden trees, all of it generating crown reductions, dismantles, felling, deadwooding and stump grinding for local firms.",
   "It is a safety-critical trade run to recognised standards. Cramlington tree surgeons are typically NPTC, City and Guilds and LANTRA qualified, working to BS 3998 for tree work and BS 5837 where trees meet construction, many of them Arboricultural Association members, and with Storm Arwen having torn down 16 million trees across Northumberland and south-east Scotland in 2021, windblow clearance, replanting and TPO rules still shape much of the work. Every chainsaw job, on the ground or roped into a canopy, depends on cut-protective trousers, boots, a forestry helmet and gloves rated to EN ISO 11393.",
   "Small outfits carry this work: a climber and a groundsman, a family business, a one or two-van team covering Cramlington, Bedlington and the wider Blyth valley patch. They buy their own kit, get the sizes and protection class right and want it ordered direct, without a procurement department or a trade account in the way.",
  ],
  "kit_loc":"across the town's parks, woodland and Blyth valley tree work",
  "s2_intro":"Whether you climb, work the ground or run a small crew across Cramlington's parks, Plessey Woods and the Blyth valley",
 },
}

# === CSV / nearby ==========================================================
_CSV=None
def _load_csv():
    global _CSV
    if _CSV is not None: return _CSV
    here=os.path.dirname(os.path.abspath(__file__))
    for p in (os.path.join(here,'FS_towns.csv'),'FS_towns.csv','/mnt/user-data/outputs/FS_towns.csv'):
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
                         f"(web-verified, all on FS_towns.csv). No rank/auto fallback.")
    bad = [n for n in nb if not any(r[1].lower()==n.lower() for r in _load_csv())]
    if bad:
        raise ValueError(f"{town}: nearby town(s) not on FS_towns.csv: {bad}")
    return nb[:3]

# === title / meta ==========================================================
def build_title(town):
    for t in (f"{town} Forestry and Tree Surgery Workwear",
              f"{town} Tree Surgery Workwear",
              f"{town} Forestry Workwear", f"{town} Arborist Workwear"):
        if len(t) <= 60: return t
    return f"{town} Tree Surgery Workwear"

def build_meta(town):
    for m in (f"Chainsaw trousers, boots, helmets and hi-vis for {town} arborists and tree surgeons - EN ISO 11393 PPE, order online direct, with in-house embroidery.",
              f"Chainsaw trousers, boots and helmets for {town} arborists and tree surgeons - EN ISO 11393 PPE, order online direct, in-house embroidery.",
              f"Chainsaw PPE, boots and helmets for {town} arborists and tree surgeons - EN ISO 11393 rated, order online direct, in-house embroidery.",
              f"Chainsaw PPE and workwear for {town} arborists and tree surgeons - EN ISO 11393 rated, order online direct."):
        if len(m) <= 160: return m
    return f"Chainsaw PPE and workwear for {town} tree surgeons - order online direct."

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
        "name":f"Forestry and Tree Surgery Workwear Supply and Embroidery in {town}",
        "serviceType":"Forestry and tree surgery workwear and PPE supply and embroidery",
        "provider":{"@id":"https://www.ineedworkwear.com/#organization"},
        "areaServed":[{"@type":"City","name":town}]+[{"@type":"City","name":n} for n in nearby],
        "audience":{"@type":"BusinessAudience","name":"Arborists, tree surgeons and forestry contractors"},
        "description":f"Chainsaw trousers, chainsaw boots, forestry helmets, gloves, hi-vis and waterproofs supplied to arborists and tree surgeons in {town}, EN ISO 11393 rated, ordered direct online, with in-house embroidery.",
        "hasOfferCatalog":{"@type":"OfferCatalog","name":"Forestry and Tree Surgery Workwear",
            "itemListElement":[{"@type":"Offer","itemOffered":{"@type":"Product","name":p}} for p in FS_PRODUCTS]}}
    crumb = {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Home","item":DOMAIN},
        {"@type":"ListItem","position":2,"name":"Forestry and Tree Surgery Workwear","item":f"{DOMAIN}/forestry-tree-surgery-workwear"},
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

    emb_svg   = EMB.replace('a London tree surgery company logo', f'a {town} tree surgery company logo')
    sign_svg  = SIGNPOST.replace('London forestry and tree surgery signpost', f'{town} forestry and tree surgery signpost')
    sign_svg  = re.sub(r'<text x="230" y="62".*?</text>', signpost_town(town), sign_svg, flags=re.S)
    sign_svg  = sign_svg.replace('every kind of London tree work', f'every kind of {town} tree work')
    prem_svg  = PREMISES.replace('serving arborists and tree surgeons across London', f'serving arborists and tree surgeons across {town}')

    H=[build_head(town, slug, faqs, nearby), HEADER]
    H.append(f'<div class="fs-hero"><div class="fs-wrap"><div class="fs-subtitle">Chainsaw PPE and Workwear for Arborists and Tree Surgeons</div><h1>{town} Forestry and Tree Surgery Workwear</h1></div></div>')
    H.append('<div class="fs-pulse"></div>')
    H.append(f'<div class="fs-trust-strip"><p>{trust}</p></div>')
    H.append(f'<div class="fs-wrap"><div class="fs-snapshot"><div class="fs-snapshot-label">Supplier Snapshot</div><p>{snap}</p></div></div>')
    H.append(STATS)
    H.append('<div class="fs-cta-bar"><a href="https://www.ineedworkwear.com" class="fs-cta-btn">Browse Forestry and Arborist PPE</a></div>')
    H.append('<div class="fs-jump-links"><a href="#range">Workwear Range</a><a href="#contract">Chainsaw PPE</a><a href="#accounts">How to Order</a><a href="#order">Order Online</a></div>')
    H.append(GARMENT)
    H.append(f'<div class="fs-section"><div class="fs-wrap"><h2>{s1head}</h2>'+''.join(f'<p>{p}</p>' for p in s1ps)+'</div></div>')
    H.append(f'<div class="fs-section" id="range"><div class="fs-wrap"><h2>Forestry and Tree Surgery Workwear Range</h2><p>{s2intro} <a href="https://www.ineedworkwear.com">Browse the full range at iNeedWorkwear.com</a>.</p><p class="fs-btn-center"><a href="https://www.ineedworkwear.com" class="fs-section-btn">Browse The Range</a></p>{grid}</div></div>')
    H.append(f'<div class="fs-section"><div class="fs-wrap"><h2>Branding for a One-Van Outfit or a Small Crew</h2>'+''.join(f'<p>{p}</p>' for p in emb)+'</div></div>')
    H.append(emb_svg)
    H.append(f'<div class="fs-wrap"><div class="fs-contract" id="contract"><h3>{CON_HEAD}</h3>'+''.join(f'<p>{p}</p>' for p in con)+'</div></div>')
    H.append(sign_svg)
    H.append(f'<div class="fs-section" id="accounts"><div class="fs-wrap"><h2>{ACC_HEAD}</h2>'+''.join(f'<p>{p}</p>' for p in acc)+'</div></div>')
    H.append(prem_svg)
    H.append(f'<div class="fs-section"><div class="fs-wrap"><h2>Why Arborists and Tree Surgeons Choose iNeedWorkwear</h2>'+''.join(f'<p>{p}</p>' for p in why)+'</div></div>')
    H.append(ORDER)
    H.append(f'<div class="fs-section" id="order"><div class="fs-wrap"><h2>Order Forestry and Tree Surgery Workwear Online</h2><p>{ordr[0]}</p><p>{ordr[1]}</p><p>{ordr[2]}</p><p class="fs-btn-center"><a href="https://www.ineedworkwear.com" class="fs-section-btn">Order Online Now</a></p><p>{selfp}</p>'+CONTACT+'</div></div>')
    faq_html=''.join(f'<div class="fs-faq-item"><div class="fs-faq-q">{q}</div><div class="fs-faq-a">{a}</div></div>' for q,a in faqs)
    H.append(f'<div class="fs-faq"><div class="fs-wrap"><h2>Forestry and Tree Surgery Workwear FAQ</h2>{faq_html}</div></div>')
    H.append(f'<div class="fs-wrap"><div class="fs-workwear">{sorted_}</div></div>')
    nb_links=''.join(f'<a href="fs-{slugify(n)}.html">Tree surgery workwear in {n}</a>\n' for n in nearby)
    H.append(f'<div class="fs-nearby"><div class="fs-wrap"><h3>Forestry and Tree Surgery Workwear in Nearby Towns</h3><div class="fs-nearby-links">{nb_links}</div></div></div>')
    H.append(FOOTER+'\n</body></html>')
    return '\n'.join(H)

def main():
    args=[a for a in sys.argv[1:]]
    outdir=os.environ.get('FS_OUTDIR','outputs')
    os.makedirs(outdir, exist_ok=True)
    disp={r[1].lower():r[1] for r in _load_csv()}  # exact CSV display names
    if not args:
        args=[t for t in TOWNS if t!='london']
    for town_key in args:
        tk=town_key.lower()
        if tk=='london': continue
        if tk not in TOWNS:
            print(f"SKIP {town_key}: not in TOWNS (must be web-researched first)"); continue
        town=disp.get(tk) or ' '.join(w.capitalize() for w in tk.split())
        slug=f"fs-{slugify(town)}"
        html=assemble(slug, town)
        path=os.path.join(outdir, f"{slug}.html")
        open(path,'w',encoding='utf-8').write(html)
        print(f"WROTE {path}  ({len(html.split())} words approx)")

if __name__=='__main__':
    main()
