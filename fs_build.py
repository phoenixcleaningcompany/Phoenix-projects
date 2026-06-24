#!/usr/bin/env python3
# FS (Forestry, Arboriculture & Tree Surgery) series builder v1.0
# Read SPEC.md / CLAUDE.md first. TEMPLATE B (self-checkout / small-business):
# the buyer is the sole-trader arborist / small crew ordering DIRECT ONLINE, no
# account. Lead = CHAINSAW (trousers/PPE) + SAFETY BOOTS + HELMET. Chainsaw
# protection to EN ISO 11393 (Type A ground / Type C climbing) is the
# differentiator. Exactly 14 .com + 1 community link per page. No JS, no HTML
# entities, no delivery-timescale claims. Nearby MUST be geographically close,
# hand-authored, on FS_towns.csv (no rank fallback).
import re, os, json, zlib, sys, csv

def pick(key, salt, n):
    return zlib.crc32((salt + '|' + str(key).lower()).encode()) % n

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
    if not args:
        args=[t for t in TOWNS if t!='london']
    for town_key in args:
        tk=town_key.lower()
        if tk=='london': continue
        if tk not in TOWNS:
            print(f"SKIP {town_key}: not in TOWNS (must be web-researched first)"); continue
        town=' '.join(w.capitalize() for w in tk.split())
        slug=f"fs-{slugify(town)}"
        html=assemble(slug, town)
        path=os.path.join(outdir, f"{slug}.html")
        open(path,'w',encoding='utf-8').write(html)
        print(f"WROTE {path}  ({len(html.split())} words approx)")

if __name__=='__main__':
    main()
