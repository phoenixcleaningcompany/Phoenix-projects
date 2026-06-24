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
