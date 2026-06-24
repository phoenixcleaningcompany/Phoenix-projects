#!/usr/bin/env python3
# HM (Highway Maintenance & Roadworks) series builder v1.0
# Read SPEC.md / CLAUDE.md first. Concierge / Template A (procurement + depot
# manager buyer at councils and roadworks contractors). Lead = CLASS 3 HI-VIS +
# SAFETY BOOTS + WATERPROOFS. Chapter 8 / EN ISO 20471 conspicuity is the
# differentiator; branding goes OFF the certified reflective area. Exactly 14
# .com + 1 community link per page. No JS, no HTML entities, no delivery-
# timescale claims. Nearby MUST be geographically close, hand-authored, on
# HM_towns.csv (no rank fallback).
import re, os, json, zlib, sys, csv

def pick(key, salt, n):
    return zlib.crc32((salt + '|' + str(key).lower()).encode()) % n

def _find_base():
    here = os.path.dirname(os.path.abspath(__file__))
    for p in (os.path.join(here,'hm-london.html'),'hm-london.html',
              '/mnt/user-data/outputs/hm-london.html','/home/claude/hmkit/hm-london.html'):
        if os.path.exists(p): return p
    sys.exit("ERROR: hm-london.html (base template) not found beside hm_build.py")

BASE = open(_find_base(), encoding='utf-8').read()
DOMAIN = 'https://www.ineedworkwear.uk'

def between(start, end, src=BASE):
    i = src.index(start); j = src.index(end, i+len(start)); return src[i:j]
def aria_block(aria):
    k = BASE.index(aria)
    i = BASE.rfind('<div class="hm-wrap"><div class="hm-illust">', 0, k)
    j = BASE.index('</div></div></div>', k) + len('</div></div></div>')
    return BASE[i:j]

CSS      = between('<style>', '</style>') + '</style>'
HEADER   = between('<div class="hm-header">', '\n<div class="hm-hero">')
STATS    = between('<div class="hm-stats">', '\n<div class="hm-cta-bar">')
GARMENT  = between('<div class="hm-wrap"><div class="hm-illust"><div class="hm-garment-row">', '\n<div class="hm-section">')
EMB      = aria_block('Embroidery machine stitching')
SIGNPOST = aria_block('roadworks signpost')
PREMISES = aria_block('serving councils and contractors across')
ORDER    = aria_block('Order highway maintenance workwear online')
CONTACT  = BASE[BASE.index('<div class="hm-contact-block">'):
                BASE.index('</div></div></div>', BASE.index('<div class="hm-contact-block">'))+len('</div></div></div>')]
FOOTER   = BASE[BASE.index('<footer class="hm-footer">'):BASE.index('</footer>')+len('</footer>')]

def signpost_town(town):
    n = len(town)
    size = 22 if n <= 8 else 19 if n <= 11 else 16 if n <= 15 else 13 if n <= 20 else 11
    tl = ' textLength="200" lengthAdjust="spacingAndGlyphs"' if n > 11 else ''
    return (f'<text x="230" y="62" text-anchor="middle" font-family="Arial,sans-serif" '
            f'font-weight="800" font-size="{size}" fill="#fff"{tl}>{town.upper()}</text>')

# === PRODUCTS ==============================================================
HM_PRODUCTS = ["Class 3 Hi-Vis Jackets and Vests","Hi-Vis Trousers and Coveralls",
 "Safety Boots and Footwear","Waterproofs and Winter Layers","Cargo and Work Trousers",
 "Hard Hats, Gloves and Site PPE","Embroidered Polo Shirts","Embroidery, Names and ID Branding"]

def _card(n,d): return f'<div class="hm-product-card"><div class="hm-product-name">{n}</div><div class="hm-product-detail">{d}</div></div>'
_GA=_card("Class 3 Hi-Vis Jackets and Vests","Class 3 hi-vis jackets, bodywarmers and vests to EN ISO 20471, built for Chapter 8 roadworks alongside live and high-speed traffic, day and night, branded off the certified reflective area.")
_GB=_card("Hi-Vis Trousers and Coveralls","Hi-vis trousers and coveralls to complete a Class 3 ensemble for high-speed and night work, the upper-and-lower conspicuity Chapter 8 expects on the carriageway.")
_GC=_card("Safety Boots and Footwear","Safety boots and wellingtons with grip and protection for broken ground, hot surfacing, gully and verge work, built for crews on their feet across changing road conditions.")
_GD=_card("Waterproofs and Winter Layers","Hi-vis waterproofs, insulated jackets and thermal base layers for all-weather and winter-gritting work, sized to keep crews seen, warm and dry through night shifts and cold snaps.")
_GE=_card("Cargo and Work Trousers","Holster-pocket and cargo work trousers for depot, fitting and groundwork tasks off the live carriageway, durable and pocketed for tools, in colours to match the team kit.")
_GF=_card("Hard Hats, Gloves and Site PPE","Hard hats, gloves, safety glasses and ear protection for surfacing, breaking and roadworks, the everyday head-to-hand PPE every highways gang gets through.")
_GG=_card("Embroidered Polo Shirts","Embroidered polos for depot, supervisory and office staff off the carriageway, branded with the authority or contractor identity for a smart, consistent look.")
_GH=_card("Embroidery, Names and ID Branding","In-house embroidery and heat-sealed branding of the authority or company name and ID, placed off the certified reflective area so Class 3 conspicuity is never compromised.")
GRID_POOL=[
 '<div class="hm-product-grid">'+_GA+_GB+_GC+_GD+_GE+_GF+_GG+_GH+'</div>',
 '<div class="hm-product-grid">'+_GA+_GB+_GD+_GC+_GE+_GF+_GG+_GH+'</div>',
 '<div class="hm-product-grid">'+_GA+_GC+_GB+_GD+_GE+_GF+_GG+_GH+'</div>',
]

# === PROSE POOLS ===========================================================
TRUST_POOL=[
 "Supplying Class 3 hi-vis, safety boots, waterproofs and branded workwear to highways teams and roadworks contractors across the UK",
 "Class 3 hi-vis, safety boots, waterproofs and branded workwear for highway maintenance teams and roadworks contractors nationwide",
 "Trusted by councils and roadworks contractors across the UK for Chapter 8 Class 3 hi-vis, PPE and multi-depot supply",
 "Chapter 8-ready Class 3 hi-vis, safety boots, waterproofs and branded workwear for highways teams across the UK",
]
S2INTRO_POOL=[
 "Across {t}'s resurfacing, lining, drainage, lighting and winter-maintenance work, a highways operation kits several groups at once: the carriageway gang working alongside live traffic, the drainage and lighting crews, the winter-gritting teams, the supervisors and the depot and office staff, each to the conspicuity standard the job needs.",
 "A {t} highways operation kits several groups in one go, from the carriageway gang alongside live traffic to the drainage and lighting crews, the winter teams, the supervisors and the depot and office staff, each to the conspicuity standard the job demands.",
 "Highway maintenance kit for a {t} authority or contractor has to do several jobs: keep gangs seen alongside live, high-speed traffic to Chapter 8, survive surfacing and winter work, and carry the authority or company identity off the certified reflective area.",
 "A {t} highways operation dresses a carriageway gang, drainage and lighting crews, winter-gritting teams, supervisors and depot staff at once, each to the conspicuity standard Chapter 8 and the job demand.",
]
EMB_P1_POOL=[
 "On a highways job, what people wear is a safety control before it is presentation: the Class 3 hi-vis is what keeps a worker seen by a driver at speed, day or night, on a {t} carriageway. Branding has to sit alongside that, never on top of it, which is why we place the authority or company name and ID off the certified retroreflective and background material, so the conspicuity the garment is rated for stays intact.",
 "What a {t} highways gang wears is a safety control first and presentation second: the Class 3 hi-vis keeps a worker seen by a driver at speed, day or night. Branding sits alongside that, never over it, so we place the authority or company name and ID off the certified retroreflective and background material to keep the rated conspicuity intact.",
 "On a {t} road job, the kit is a safety control before it is presentation, because the Class 3 hi-vis is what keeps a worker seen by a passing driver day and night. Branding must work around that, so we place the name and ID off the certified retroreflective and background material and the garment keeps the conspicuity it is rated for.",
 "Workwear on a {t} highways job is a safety control first: the Class 3 hi-vis keeps a worker seen by a driver at speed in any light. Branding has to sit alongside it, not on top, so the authority or company name and ID go off the certified retroreflective and background material, keeping the rated conspicuity intact.",
]
EMB_P2_POOL=[
 "We brand in-house, which means the authority or company name and any ID are embroidered or heat-sealed onto hi-vis and polos, finished to survive surfacing, winter work and industrial laundering. Send your artwork once, we hold it on file, and every reorder, new starter and subcontractor matches the last, so a gang on a {t} carriageway reads as one authority or one contractor rather than a mix of kit.",
 "Branding is applied in-house onto hi-vis and polos - the authority or company name and ID embroidered or heat-sealed and finished to survive surfacing, winter work and industrial laundering. We hold your artwork on file, so reorders, new starters and subcontractors all match, and a {t} gang reads as one authority or contractor rather than a mix of kit.",
 "Names and ID are embroidered or heat-sealed in-house onto hi-vis and polos, finished to take surfacing, winter work and industrial laundering. Your artwork is held on file, so every reorder and subcontractor matches, and a gang on a {t} carriageway reads as one outfit.",
 "We badge in-house, embroidering or heat-sealing the authority or company name and ID onto hi-vis and polos and finishing them to survive surfacing, winter and industrial laundering. Held on file, your branding reproduces on every reorder, new starter and subcontractor, so a {t} gang turns out as one authority or contractor.",
]
EMB_P3_POOL=[
 "For an operation running several depots, gangs or a subcontractor chain, we manage the branding and sizes across the whole network, so kitting a new starter, equipping a subcontractor crew or replacing worn hi-vis reproduces the same compliant, branded, correctly conspicuous kit every time, across every depot and crew.",
 "Where an operation runs several depots, gangs or a subcontractor chain, we manage branding and sizes across the network, so a new starter, a subcontractor crew or a replacement for worn hi-vis comes back the same compliant, branded, conspicuous kit every time.",
 "An operation with several depots, gangs or a subcontractor chain can run its branding and sizes across the whole network on one account, so kitting a new starter or a subcontractor crew reproduces the same compliant, correctly conspicuous, branded kit each time.",
 "For multi-depot and subcontractor operations, branding and sizes are managed across the whole network, so kitting a new starter, equipping a subcontractor crew or replacing worn hi-vis reproduces the same compliant, branded, conspicuous kit every time.",
]
# === CHAPTER 8 / SECTOR SCHEME BLOCK ======================================
CON_HEAD="Chapter 8 and Sector Scheme Compliant Teams: Class 3 Hi-Vis for the Highway"
CON_P1_POOL=[
 "Highway maintenance in {t} is governed by Chapter 8 of the Traffic Signs Manual and the conspicuity standards that go with working alongside live, often high-speed traffic. That makes Class 3 high-visibility clothing to EN ISO 20471, a jacket and trousers worn together as a full ensemble, the baseline rather than an option, so a worker is seen by a driver at distance, in poor light and at night, which is where most of the risk on a road job sits.",
 "Road maintenance in {t} works to Chapter 8 of the Traffic Signs Manual and the conspicuity standards for working alongside live, often high-speed traffic. So Class 3 high-visibility clothing to EN ISO 20471, jacket and trousers as a full ensemble, is the baseline not an option, keeping a worker seen at distance, in poor light and at night, where most of the risk sits.",
 "Because {t} highway maintenance is governed by Chapter 8 of the Traffic Signs Manual and the conspicuity demands of working next to live, often high-speed traffic, Class 3 high-visibility clothing to EN ISO 20471, jacket and trousers as a full ensemble, is the baseline rather than an option, so a worker is seen by a driver at distance, in poor light and at night.",
 "Highway maintenance in {t} runs to Chapter 8 of the Traffic Signs Manual and the conspicuity standards of working alongside live, high-speed traffic, which makes a full Class 3 ensemble to EN ISO 20471, jacket and trousers together, the baseline not an option, keeping a worker seen at distance, in poor light and at night where the risk is greatest.",
]
CON_P2_POOL=[
 "The detail is what keeps it compliant. Branding is placed off the certified retroreflective and background material so the garment keeps its Class 3 rating, hi-vis is replaced rather than patched once it is worn, soiled or faded below standard, and the kit is built to survive surfacing, gritting and industrial laundering. Around it sit the safety boots, hard hats, gloves and waterproofs a roadworks gang needs, with the cold-weather layers that winter and night work demand.",
 "Detail is what keeps it compliant: branding goes off the certified retroreflective and background material so the garment keeps its Class 3 rating, hi-vis is replaced not patched once worn, soiled or faded below standard, and the kit survives surfacing, gritting and industrial laundering. Around it sit the safety boots, hard hats, gloves and waterproofs a gang needs, with the cold-weather layers winter and night work demand.",
 "The detail decides compliance: branding sits off the certified retroreflective and background material to keep the Class 3 rating, hi-vis is replaced rather than patched once below standard, and the kit takes surfacing, gritting and industrial laundering. Around it are the safety boots, hard hats, gloves and waterproofs a roadworks gang needs, plus the cold-weather layers for winter and night work.",
 "What keeps it compliant is the detail: branding off the certified retroreflective and background material so the Class 3 rating holds, hi-vis replaced not patched once worn or faded below standard, and kit built to survive surfacing, gritting and industrial laundering, alongside the safety boots, hard hats, gloves, waterproofs and cold-weather layers a gang needs.",
]
CON_P3_POOL=[  # 1 .com link each
 'Most of all, a highways authority or contractor needs kit it can reproduce consistently across depots, gangs and a subcontractor chain, and stand behind at audit and on sector-scheme work. We keep your identity, artwork and sizes on file, so kitting a new starter, equipping a subcontractor crew or replacing worn hi-vis on an existing {t} contract reproduces the same compliant, conspicuous, branded kit every time. Talk to us about contract and multi-depot supply at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
 'Above all, a {t} highways authority or contractor needs kit it can reproduce across depots, gangs and a subcontractor chain and stand behind at audit and on sector-scheme work. With your identity, artwork and sizes on file, kitting a new starter, equipping a subcontractor crew or replacing worn hi-vis reproduces the same compliant, conspicuous, branded kit every time. Talk to us about contract and multi-depot supply at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
 'Most importantly, a highways operation needs consistency across depots, gangs and subcontractors that it can stand behind at audit and on sector-scheme work. We hold your identity, artwork and sizes on file, so a new starter, a subcontractor crew or a replacement for worn hi-vis on a {t} contract comes back the same compliant, conspicuous, branded kit every time. Talk to us about contract and multi-depot supply at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
 'Above everything, a highways authority or contractor needs kit it can reproduce across depots, gangs and subcontractors and stand behind at audit. Your identity, artwork and sizes stay on file, so kitting a new starter, equipping a subcontractor crew or replacing worn hi-vis on a {t} contract reproduces the same compliant, conspicuous, branded kit every time. Talk to us about contract and multi-depot supply at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
]
ACC_HEAD="Ordering, Trade Accounts and Multi-Depot Supply"
ACC_P1_POOL=[
 "For most highways authorities and contractors in {t} the right route is a trade account. It gives procurement and depot managers purchase-order ordering, volume pricing and a single point of contact for every depot, so Class 3 hi-vis and PPE can be reordered against a framework, new starters and subcontractors kitted quickly and every gang and depot kept consistent. Tell us your headcount, your depot list, your identity and your logo and we will build a branded, Chapter 8-ready kit list and pricing for the whole operation.",
 "Most {t} highways authorities and contractors run a trade account: procurement and depot managers get purchase-order ordering, volume pricing and one point of contact for every depot, so Class 3 hi-vis and PPE reorders against a framework, new starters and subcontractors are kitted fast and every gang stays consistent. Send your headcount, depot list, identity and logo and we will build a branded, Chapter 8-ready kit list and pricing.",
 "A trade account is the natural route for most {t} highways operations. Procurement and depot managers get PO ordering, volume pricing and a single contact for every depot, so reordering against a framework, kitting new starters and keeping gangs consistent all stay simple. Give us your headcount, depot list, identity and logo and we will build a branded, Chapter 8-ready kit list and pricing.",
 "For the typical {t} highways authority or contractor, a trade account is the way to buy: purchase-order ordering, volume pricing and one contact across every depot, so Class 3 hi-vis and PPE reorders against the framework, new starters are kitted quickly and gangs stay consistent. Tell us your headcount, depot list, identity and logo and we will build the branded, Chapter 8-ready kit list and pricing.",
]
ACC_P2_POOL=[
 "Smaller operations are covered too. A small works contractor or a single depot can order direct online without setting up an account: browse the range, choose Class 3 hi-vis, boots, waterproofs and a branded polo, add sizes, send the logo once and check out. It is the fastest route to compliant, branded kit for a small crew.",
 "Smaller operations have a route too. A small works contractor or single depot can order direct online with no account: browse the range, pick Class 3 hi-vis, boots, waterproofs and a branded polo, add sizes, send the logo once and check out, the quickest way to get a small crew compliant and branded.",
 "Small operations are catered for as well. A small works contractor or a single depot can order direct online without an account, choosing Class 3 hi-vis, boots, waterproofs and a branded polo, adding sizes and sending the logo once, the fastest route to compliant, branded kit for a crew.",
 "There is a quick route for small operations as well. A small works contractor or single depot can buy direct online with no account: browse, pick Class 3 hi-vis, boots, waterproofs and a branded polo, add sizes and send the logo once, getting a small crew compliant and branded without delay.",
]
ACC_P3_POOL=[
 "Every order is branded in-house, which means your identity and ID are applied under our control rather than outsourced, so we manage the quality, the placement off the reflective area and the lead time. Your artwork and sizes are held on file for reordering, new starters and subcontractors, and delivery reaches {t} and the surrounding area on standard lead times.",
 "All branding is done in-house, so your identity and ID are applied under our control rather than sent out, keeping quality, placement off the reflective area and timing consistent. We hold your artwork and sizes on file for reorders, new starters and subcontractors, and deliver to {t} and the wider area on standard lead times.",
 "Because branding is done in-house, your identity and ID are applied under our control rather than outsourced, keeping the quality and the placement off the reflective area right. Your artwork and sizes stay on file for reordering, new starters and subcontractors, and orders reach {t} and the surrounding area on standard lead times.",
 "Branding happens in-house, so your identity and ID are applied under our control rather than farmed out, with placement kept off the reflective area. We keep your artwork and sizes on file for reorders, new starters and subcontractors, and delivery reaches {t} and the area around it on standard lead times.",
]
ACC_P4_POOL=[  # 2 .com links each
 'Set up a trade account for purchase-order ordering and volume pricing at <a href="https://www.ineedworkwear.com">iNeedWorkwear</a>, or for a single depot or small contractor you can browse and order direct at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
 'Open a trade account for purchase-order ordering and volume pricing at <a href="https://www.ineedworkwear.com">iNeedWorkwear</a>. For a single depot or small contractor, browse and order direct at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
 'Run procurement through a trade account for purchase-order ordering and volume pricing at <a href="https://www.ineedworkwear.com">iNeedWorkwear</a>, or order direct for a single depot or small contractor at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
 'Set up purchase-order ordering and volume pricing on a trade account at <a href="https://www.ineedworkwear.com">iNeedWorkwear</a>. A single depot or small contractor can browse and order direct at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
]
WHY_P1_POOL=[
 "A {t} highways authority or contractor whose gangs turn out in clean, correctly branded Class 3 hi-vis, sound boots and the right cold-weather kit looks like a compliant, controlled operation to every safety auditor, client officer and member of the public who passes the works, and iNeedWorkwear builds that whole kit from a single supplier, branded in-house off the reflective area and priced for the volumes a highways operation actually buys.",
 "Turned out in clean, correctly branded Class 3 hi-vis, sound boots and the right cold-weather kit, a {t} highways authority or contractor reads as a compliant, controlled operation to safety auditors, client officers and the public passing the works, and iNeedWorkwear builds that whole kit from one supplier, branded in-house off the reflective area and priced for the volumes a highways operation really buys.",
 "A {t} highways authority or contractor whose gangs wear clean, correctly branded Class 3 hi-vis, sound boots and the right cold-weather kit looks compliant and controlled to every auditor, client officer and passer-by at the works, and we build that complete kit from a single supplier, branded in-house off the reflective area and priced for genuine highways volumes.",
 "Turned out in clean, correctly branded Class 3 hi-vis, sound boots and the right cold-weather kit, a {t} highways authority or contractor looks like a compliant, controlled operation to auditors, client officers and the public, and we supply that whole kit from one place, branded in-house off the reflective area and priced for real volumes.",
]
WHY_P2_POOL=[
 "Everything comes from the same place. The supplier that brands your hi-vis also supplies your safety boots, waterproofs, thermal layers, cargo trousers, hard hats, gloves and polos, so every depot and gang matches and nothing falls through the gap between the Class 3 layer and the rest of the kit a roadworks operation needs.",
 "Kit comes in one order. The supplier branding your hi-vis also supplies safety boots, waterproofs, thermal layers, cargo trousers, hard hats, gloves and polos, so every depot and gang matches and nothing slips between the Class 3 layer and the rest of the kit a roadworks operation needs.",
 "All from one supplier. The same company behind your branded Class 3 hi-vis also provides safety boots, waterproofs, thermal layers, cargo trousers, hard hats, gloves and polos, so every depot and gang matches from a single source.",
 "Kit comes from one place. Alongside the branded Class 3 hi-vis sit safety boots, waterproofs, thermal layers, cargo trousers, hard hats, gloves and polos, so every depot and gang matches and nothing falls through the gap between hi-vis and the rest.",
]
WHY_P3_POOL=[
 "The range is built around what highway maintenance actually wears out and replaces: Class 3 hi-vis, boots, waterproofs and gloves, the everyday kit of the carriageway, the gully and the winter shift. That practical focus keeps pricing, stock and reordering realistic for an operation kitting dozens or hundreds of people across depots, gangs and subcontractors.",
 "Everything in the range reflects what highway maintenance really gets through: Class 3 hi-vis, boots, waterproofs and gloves, the daily kit of the carriageway, the gully and the winter shift, and that focus keeps pricing, stock and reordering realistic for an operation kitting dozens or hundreds across depots, gangs and subcontractors.",
 "The range centres on what highway maintenance genuinely uses and replaces, Class 3 hi-vis, boots, waterproofs and gloves, and that practical focus keeps pricing, stock and reordering sensible for an operation equipping people across depots, gangs and subcontractors.",
 "Everything is built around what a working highways operation really gets through, Class 3 hi-vis, boots, waterproofs and gloves, so pricing, stock and reordering stay sensible for an operation kitting dozens or hundreds across depots, gangs and subcontractors.",
]
WHY_P4_POOL=[
 "Ordering is built for how authorities and contractors actually buy: a trade account with purchase-order ordering and volume pricing for the multi-depot operation, and a quick direct route for the small contractor or single depot, with your identity, logo and sizes held on file so every reorder, new starter and subcontractor matches and stays compliant.",
 "How you order suits how the trade really buys, a trade account with purchase-order ordering and volume pricing for the multi-depot operation, and a quick direct route for the small contractor or single depot, with identity, branding and sizes on file so reorders always match and stay compliant.",
 "The ordering fits the trade: a trade account with PO ordering and volume pricing for the multi-depot operation, and a fast direct route for the small contractor or single depot, with identity, branding and sizes held so every reorder, new starter and subcontractor is the same and compliant.",
 "The way you order suits the trade, a trade account with PO ordering and volume pricing for the multi-depot operation and a fast direct route for the small contractor, with identity, branding and sizes on file so each reorder comes back identical and compliant.",
]
ORD_P1_POOL=[
 "iNeedWorkwear supplies Class 3 hi-vis, hi-vis trousers, safety boots, waterproofs, thermal layers, cargo trousers, hard hats, gloves and embroidered polos to highway maintenance teams and roadworks contractors across {region}, all branded in-house with the authority or company identity and placed off the certified reflective area.",
 "We supply Class 3 hi-vis, hi-vis trousers, safety boots, waterproofs, thermal layers, cargo trousers, hard hats, gloves and embroidered polos to highway maintenance teams and roadworks contractors across {region}, all branded in-house and placed off the certified reflective area.",
 "Across {region}, iNeedWorkwear kits highway maintenance teams and roadworks contractors in Class 3 hi-vis, hi-vis trousers, safety boots, waterproofs, thermal layers, cargo trousers, hard hats, gloves and embroidered polos, branded in-house off the certified reflective area.",
 "From a single depot to multi-site frameworks across {region}, iNeedWorkwear kits highway maintenance teams and roadworks contractors with Class 3 hi-vis, hi-vis trousers, safety boots, waterproofs, thermal layers, cargo trousers, hard hats, gloves and embroidered polos, branded in-house off the reflective area.",
]
ORD_P2_POOL=[
 "For most operations the route is a trade account: tell us your headcount, your depot list and your logo, and we will build a branded, Chapter 8-ready Class 3 hi-vis and PPE kit list with volume pricing and purchase-order ordering. We hold your artwork and sizes on file, so reordering is fast and every new starter, replacement and subcontractor is kitted, branded and compliant across every depot and gang.",
 "Most operations run a trade account: send your headcount, depot list and logo, and we will put together a branded, Chapter 8-ready Class 3 hi-vis and PPE kit list with volume pricing and purchase-order ordering. With your artwork and sizes on file, reordering is quick and every new starter, replacement and subcontractor is branded and compliant across every depot and gang.",
 "For the majority of operations it is a trade account: give us your headcount, depot list and logo, and we build a branded, Chapter 8-ready Class 3 hi-vis and PPE kit list with volume pricing and purchase-order ordering. Your artwork and sizes stay on file, so reorders are fast and every new starter and subcontractor matches and stays compliant.",
 "For most operations the route is a trade account: send your headcount, depot list and logo and we will build a branded, Chapter 8-ready Class 3 hi-vis and PPE kit list with volume pricing and purchase-order ordering, holding your artwork and sizes on file so reorders are fast and every new starter and subcontractor is compliant across every depot and gang.",
]
ORD_P3_POOL=[
 "For a single depot or a small works contractor, ordering direct online is quickest: browse the range, add your sizes, send your logo once and check out, with no account to set up.",
 "For a single depot or small works contractor, the quickest route is direct online: browse the range, add sizes, send the logo once and check out, with no account needed.",
 "A single depot or a small works contractor can order direct online fastest: pick the range, add sizes, send the logo once and check out, no account required.",
 "A single depot or small works contractor orders quickest direct online: browse the range, add sizes, send the logo a single time and check out, with no account to set up.",
]
SELF_POOL=[  # 1 .com link each
 'Running one small roadworks crew and need kit now? Browse the full range, add your sizes and order direct on self-service checkout at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
 'Just kitting a single depot or small crew? Browse the range, add sizes and order direct on self-service checkout at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
 'Need kit for one small roadworks crew right now? Browse the full range, add your sizes and order direct on self-service checkout at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
 'Sorting a single depot or small contractor today? Browse the range, add sizes and order direct on self-service checkout at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
]
SORTED_POOL=[  # 1 .com link each
 '<h3>Highway Maintenance Workwear, Sorted</h3><p>From Class 3 hi-vis and safety boots to waterproofs, thermal layers, hard hats and gloves, get Chapter 8-ready kit built for highways teams and roadworks contractors at fair prices - branded in-house off the reflective area, and supplied across every depot.</p><p><a href="https://www.ineedworkwear.com">Browse highway maintenance workwear at iNeedWorkwear</a></p>',
 '<h3>Highway Maintenance Workwear, Sorted</h3><p>Class 3 hi-vis, safety boots, waterproofs, thermal layers, hard hats and gloves - Chapter 8-ready kit for highways teams and roadworks contractors at fair prices, branded in-house off the reflective area across every depot.</p><p><a href="https://www.ineedworkwear.com">Browse highway maintenance workwear at iNeedWorkwear</a></p>',
 '<h3>Highway Maintenance Workwear, Sorted</h3><p>From Class 3 hi-vis and boots to waterproofs, thermal layers, hard hats and gloves, kit your highways operation out at fair prices, branded in-house off the reflective area and delivered across every depot.</p><p><a href="https://www.ineedworkwear.com">Browse highway maintenance workwear at iNeedWorkwear</a></p>',
 '<h3>Highway Maintenance Workwear, Sorted</h3><p>Class 3 hi-vis, safety boots, waterproofs, thermal layers, hard hats and gloves, the full Chapter 8-ready kit at fair prices, branded in-house and ready to reorder across every depot and gang.</p><p><a href="https://www.ineedworkwear.com">Browse highway maintenance workwear at iNeedWorkwear</a></p>',
]
OWNER_POOL=[
 "The buyer is a procurement or fleet and depot manager at a council or a contractor, specifying against Chapter 8, EN ISO 20471 and sector-scheme requirements rather than buying on impulse, so the kit has to meet the conspicuity standard, survive surfacing and winter work, stay consistent across depots and crews, and reorder quickly for new starters and subcontractors.",
 "It is normally a procurement or depot manager at a council or contractor who signs for the kit, specifying against Chapter 8, EN ISO 20471 and sector schemes, so the hi-vis and PPE has to meet the conspicuity standard, survive surfacing and winter work, stay consistent across depots and reorder fast for new starters and subcontractors.",
 "Procurement or a depot manager at a council or contractor does the buying here, against Chapter 8 and sector-scheme requirements, so the kit has to meet the conspicuity standard, survive surfacing and winter work, stay consistent across every depot and gang, and reorder fast for new starters and subcontractors.",
 "The person buying is a procurement or depot manager at a council or contractor rather than the operative, specifying against Chapter 8 and EN ISO 20471, so the kit must meet the conspicuity standard, survive surfacing and winter work, stay consistent across depots and reorder quickly for new starters and subcontractors.",
 "Buying sits with procurement or a depot manager at a council or contractor, against Chapter 8 and sector schemes, so the hi-vis and PPE has to meet the conspicuity standard, survive surfacing and winter work, hold consistency across depots and reorder fast for new starters and subcontractors.",
 "It is a procurement or depot manager at a council or contractor who buys, against Chapter 8, EN ISO 20471 and sector-scheme requirements, so the kit must meet the conspicuity standard, survive surfacing and winter work, stay consistent across every depot and reorder quickly for new starters and subcontractors.",
]
KIT_POOL=[
 "Class 3 hi-vis carries the everyday load, with safety boots, waterproofs, thermal layers, cargo trousers, hard hats, gloves and polos completing the kit {loc}.",
 "The everyday kit is Class 3 hi-vis first, then safety boots and waterproofs, with thermal layers, cargo trousers, hard hats, gloves and polos {loc}.",
 "Class 3 hi-vis does the daily work, backed by safety boots, waterproofs, thermal layers, cargo trousers, hard hats, gloves and polos {loc}.",
 "It starts with Class 3 hi-vis, with safety boots, waterproofs, thermal layers, cargo trousers, hard hats, gloves and polos making up the rest {loc}.",
 "Class 3 hi-vis anchors the kit, alongside safety boots, waterproofs, thermal layers, cargo trousers, hard hats, gloves and polos {loc}.",
 "Class 3 hi-vis takes the everyday load, with safety boots, waterproofs, thermal layers, cargo trousers, hard hats, gloves and polos alongside {loc}.",
]
S2TAIL_POOL=[
 ", Class 3 hi-vis is the core of the kit, with safety boots, waterproofs, thermal layers, hard hats, gloves and polos alongside.",
 ", the staples are Class 3 hi-vis and safety boots, backed by waterproofs, thermal layers, cargo trousers, hard hats, gloves and polos.",
 ", Class 3 hi-vis leads, with safety boots, waterproofs, thermal layers, cargo trousers, hard hats, gloves and polos making up the rest.",
 ", Class 3 hi-vis and safety boots do the bulk of the work, with waterproofs, thermal layers, hard hats, gloves and polos alongside.",
 ", expect Class 3 hi-vis first, then safety boots, waterproofs, thermal layers, cargo trousers, hard hats, gloves and polos.",
 ", Class 3 hi-vis and safety boots anchor the kit, with waterproofs, thermal layers, cargo trousers, hard hats, gloves and polos completing it.",
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
     (f"Do you supply Chapter 8 hi-vis and workwear to highways teams in {t}?", P('fq1',[
      f"Yes. Local authority highways teams and roadworks contractors across {region} get Class 3 hi-vis jackets and trousers, safety boots, waterproofs, thermal layers, cargo trousers, hard hats, gloves and embroidered polos from us, with in-house embroidery, name and ID branding placed off the certified reflective area, multi-depot supply and trade accounts.",
      f"Yes. Class 3 hi-vis jackets and trousers, safety boots, waterproofs, thermal layers, cargo trousers, hard hats, gloves and embroidered polos go to highways teams and roadworks contractors across {region}, branded off the certified reflective area, with multi-depot supply and trade accounts.",
      f"Yes. Councils and roadworks contractors across {region} get Class 3 hi-vis, safety boots, waterproofs, thermal layers, hard hats, gloves and polos from us, with branding placed off the reflective area, multi-depot supply and trade accounts.",
      f"Yes. From a single depot to multi-site frameworks across {region}, we supply Class 3 hi-vis, safety boots, waterproofs, thermal layers, hard hats, gloves and polos, on a trade account or ordered direct online."])),
     ("Why does Class 3 hi-vis lead the range for highway maintenance?", P('fq2',[
      "Because roadworks happen alongside live, often high-speed traffic, where Chapter 8 of the Traffic Signs Manual and Class 3 conspicuity to EN ISO 20471 set the standard. A full Class 3 ensemble of hi-vis jacket and trousers is what keeps a road worker seen day and night, which is why Class 3 hi-vis leads the range, with safety boots and waterproofs close behind.",
      "Because roadworks sit alongside live, often high-speed traffic, where Chapter 8 and Class 3 conspicuity to EN ISO 20471 are the standard. A full Class 3 ensemble of jacket and trousers keeps a worker seen day and night, so Class 3 hi-vis leads, with safety boots and waterproofs behind.",
      "Roadworks happen next to live, high-speed traffic, where Chapter 8 and Class 3 conspicuity to EN ISO 20471 set the bar. A full Class 3 ensemble of hi-vis jacket and trousers keeps a worker seen day and night, so it leads the range, backed by safety boots and waterproofs.",
      "Because road work happens alongside live, high-speed traffic to Chapter 8 and Class 3 conspicuity under EN ISO 20471, a full ensemble of hi-vis jacket and trousers keeps a worker seen day and night, which is why Class 3 hi-vis leads, with safety boots and waterproofs close behind."])),
     ("What workwear and PPE does a highway maintenance team need?", P('fq3',[
      "The core list is Class 3 hi-vis jackets and vests, hi-vis trousers and coveralls, safety boots, waterproofs and winter layers for all-weather and gritting work, cargo work trousers, hard hats, gloves and site PPE, and embroidered polos for depot, supervisory and office staff, all branded with the authority or contractor identity.",
      "Most teams order Class 3 hi-vis jackets and vests, hi-vis trousers, safety boots, waterproofs and winter layers, cargo trousers, hard hats, gloves and site PPE, and embroidered polos for depot and office staff, all branded with the authority or contractor identity.",
      "At minimum, Class 3 hi-vis jackets and vests, hi-vis trousers and coveralls, safety boots, waterproofs and winter layers, cargo work trousers, hard hats, gloves and site PPE, plus polos for depot, supervisory and office staff.",
      "The core list is Class 3 hi-vis, hi-vis trousers, safety boots, waterproofs and winter layers, cargo trousers, hard hats, gloves and site PPE, and embroidered polos for depot and office staff, all branded with the authority or contractor identity."])),
     ("Can you brand hi-vis without compromising Chapter 8 conspicuity?", P('fq4',[
      "Yes. We embroider or heat-seal the authority or company name and ID in-house, placed off the certified retroreflective and background material so the Class 3 conspicuity of the garment is not compromised. Send your artwork once, we hold it on file, and every reorder and new starter matches across depots and crews.",
      "Yes. The name and ID are embroidered or heat-sealed in-house, placed off the certified retroreflective and background material so the garment keeps its Class 3 conspicuity. Send artwork once and we keep it on file, so every reorder and new starter matches.",
      "Yes, all branding is done in-house and placed off the certified retroreflective and background material, so the Class 3 conspicuity is never compromised. We hold your artwork on file, so every reorder comes back the same across depots and crews.",
      "Yes. Send your artwork once and we embroider or heat-seal the name and ID in-house, off the certified retroreflective and background material so the Class 3 rating holds, keeping it on file so reorders and new starters match across depots."])),
     ("Do you supply both councils and roadworks contractors?", P('fq5',[
      "Yes. We supply local authority highways departments and the term-maintenance and roadworks contractors working on council and National Highways networks alike, with Class 3 hi-vis and PPE branded to each identity, held on file for fast reordering across depots, crews and subcontractors.",
      "Yes. Local authority highways departments and the term-maintenance and roadworks contractors on council and National Highways networks are both supplied, with Class 3 hi-vis and PPE branded to each identity and held on file for fast reordering across depots and subcontractors.",
      "Yes, both councils and contractors. We supply highways departments and the term-maintenance and roadworks contractors on council and National Highways networks, with Class 3 hi-vis and PPE branded to each identity and held on file for reordering across depots and crews.",
      "Yes. We supply council highways departments and the roadworks and term-maintenance contractors on council and National Highways networks alike, branding Class 3 hi-vis and PPE to each identity and holding it on file for fast reordering across depots, crews and subcontractors."])),
     ("How do trade accounts and ordering work for a highways operation?", P('fq6',[
      "Most highways authorities and contractors run a trade account with purchase-order ordering, volume pricing and a single point of contact, so kit can be reordered against a framework, new starters and subcontractors kitted quickly and every depot and crew kept consistent. Smaller operations can also order direct online without an account.",
      "Most authorities and contractors use a trade account: PO ordering, volume pricing and one contact, so kit reorders against a framework, new starters and subcontractors are kitted fast and depots stay consistent. Smaller operations can also order direct online without an account.",
      "Highways authorities and contractors generally run a trade account with PO ordering, volume pricing and one point of contact, so kit reorders against a framework and every depot stays consistent. Smaller operations can order direct online instead.",
      "Most run a trade account: purchase-order ordering, volume pricing and a single contact, so kit reorders against a framework and depots and gangs stay consistent. Smaller operations can also order direct online without an account."])),
     ("How quickly can you quote for a highways contract?", P('fq7',[
      "We quote within twenty-four hours. Send your headcount, your depot list and your logo and we will build a branded, Chapter 8-ready Class 3 hi-vis and PPE kit list with volume pricing for a single depot or a full multi-site highways framework.",
      "We quote within twenty-four hours. Send your headcount, depot list and logo and we will put together a branded, Chapter 8-ready Class 3 hi-vis and PPE kit list with volume pricing for one depot or a multi-site framework.",
      "Within twenty-four hours. Give us your headcount, depot list and logo and we will assemble a branded, Chapter 8-ready Class 3 hi-vis and PPE kit list with volume pricing for a single depot or a multi-site highways framework.",
      "We turn quotes around within twenty-four hours. Send your headcount, depot list and logo and we will build a branded, Chapter 8-ready Class 3 hi-vis and PPE kit list with volume pricing for a single depot or a full multi-site highways framework."])),
    ]

# === PER-TOWN AUTHORED DATA (web-researched; geographic nearby) ============
TOWNS = {
 "birmingham": {
  "region":"Birmingham and the West Midlands",
  "nearby":["Solihull","West Bromwich","Walsall"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs, thermal layers and branded workwear to Birmingham's highway maintenance teams and roadworks contractors, from the council highways network and its long-running PFI maintenance contract to the National Highways motorway work around the city, with in-house embroidery placed off the certified reflective area, multi-depot supply and trade accounts.",
  "s1_head":"Kitting the people who keep the West Midlands' roads running",
  "s1loc":[
   "Birmingham runs one of the largest and busiest local road networks in the country, and almost all of its maintenance happens in Class 3 hi-vis alongside live traffic. The city's highways, more than 2,500km of carriageway and 5,000km of footway, plus tens of thousands of street-lighting columns, structures and the city traffic-control system, are managed under a long-running highways PFI, with the actual surfacing, lining, drainage, lighting and repair carried out by a maintenance contractor and its supply chain.",
   "In recent years that work has been delivered through Birmingham Highways Limited, with Kier Highways as the maintenance contractor and Tarmac on surfacing, covering routine and reactive maintenance, winter service, street lighting and structures across the city. It is a large, complex operation that keeps gangs on the carriageway day and night, every one of them dependent on Chapter 8-compliant Class 3 conspicuity.",
   "Around the city the motorway network is run by National Highways, with the M5, M6 and M42 and the famous Gravelly Hill interchange, Spaghetti Junction, carrying huge daily traffic and their own programme of resurfacing, barrier and structures work delivered by national framework contractors. Council and motorway work alike means high-speed roads, night closures and traffic management, where conspicuity is the single most important property of the kit.",
   "Across all of it, surfacing, lining, gully and drainage, street lighting, structures and winter gritting, a Birmingham highways authority or contractor is dressing gangs to Chapter 8 and EN ISO 20471, in Class 3 hi-vis jackets and trousers, with branding kept off the certified reflective area so conspicuity and identity both hold.",
  ],
  "kit_loc":"across the city's carriageway, lighting and winter-maintenance work",
  "s2_intro":"Across Birmingham's council carriageway, lighting and drainage work and the National Highways motorway network",
 },
 "leeds": {
  "region":"Leeds and West Yorkshire",
  "nearby":["Bradford","Pudsey","Dewsbury"],
  "snapshot":"iNeedWorkwear kits Leeds's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs, thermal layers and branded workwear, from the council's in-house Connecting Leeds highways programme and its long-running street-lighting PFI to the National Highways motorway work around the city, with in-house embroidery placed off the certified reflective area, multi-depot supply and trade accounts.",
  "s1_head":"Kitting the people who keep Yorkshire's roads running",
  "s1loc":[
   "Leeds maintains one of the largest local road networks in the North, and almost all of its upkeep happens in Class 3 hi-vis alongside live traffic. The council looks after the city's carriageways and footways through its Connecting Leeds highways programme and asset-management strategy, covering surfacing, patching, lining, drainage, barriers and winter service, with the actual work carried out by in-house teams and roadworks contractors across the city and West Yorkshire.",
   "Street lighting sits under one of the longest-running lighting PFIs in the country, with a dedicated contractor maintaining the city's lighting columns and illuminated signs, while the wider regional programme is funded and coordinated through the West Yorkshire Combined Authority. It all keeps crews out on the carriageway and verge day and night, every one of them dependent on Chapter 8-compliant Class 3 conspicuity.",
   "Around the city the motorway network is run by National Highways, with the M1, M62 and the M621 urban motorway running right through Leeds, carrying heavy daily traffic and a steady programme of resurfacing, bridge waterproofing and barrier work delivered through national framework contractors, much of it on night and lane closures. Council and motorway work alike means high-speed roads and traffic management, where conspicuity is the single most important property of the kit.",
   "Across all of it, surfacing, lining, drainage, lighting, structures and winter gritting, a Leeds highways authority or contractor is dressing gangs to Chapter 8 and EN ISO 20471, in Class 3 hi-vis jackets and trousers, with branding kept off the certified reflective area so conspicuity and identity both hold.",
  ],
  "kit_loc":"across the city's carriageway, lighting and winter-maintenance work",
  "s2_intro":"Across Leeds's council carriageway, lighting and drainage work and the National Highways motorway network",
 },
}

# === CSV / nearby ==========================================================
_CSV=None
def _load_csv():
    global _CSV
    if _CSV is not None: return _CSV
    here=os.path.dirname(os.path.abspath(__file__))
    for p in (os.path.join(here,'HM_towns.csv'),'HM_towns.csv','/mnt/user-data/outputs/HM_towns.csv'):
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
                         f"(web-verified, all on HM_towns.csv). No rank/auto fallback.")
    bad = [n for n in nb if not any(r[1].lower()==n.lower() for r in _load_csv())]
    if bad:
        raise ValueError(f"{town}: nearby town(s) not on HM_towns.csv: {bad}")
    return nb[:3]

# === title / meta ==========================================================
def build_title(town):
    for t in (f"{town} Highway Maintenance and Roadworks Workwear",
              f"{town} Highway Maintenance Workwear",
              f"{town} Highways Workwear", f"{town} Roadworks Workwear"):
        if len(t) <= 60: return t
    return f"{town} Highways Workwear"

def build_meta(town):
    for m in (f"Class 3 hi-vis, safety boots and waterproofs for {town} highways teams and roadworks contractors - Chapter 8 ready kit, trade accounts and in-house embroidery.",
              f"Class 3 hi-vis, safety boots and waterproofs for {town} highways teams and roadworks contractors - Chapter 8 ready kit and in-house embroidery.",
              f"Class 3 hi-vis, safety boots and waterproofs for {town} highways and roadworks contractors - Chapter 8 ready kit, in-house embroidery.",
              f"Chapter 8 Class 3 hi-vis and workwear for {town} highways teams and roadworks contractors - in-house embroidery."):
        if len(m) <= 160: return m
    return f"Chapter 8 Class 3 hi-vis and workwear for {town} highways teams - in-house embroidery."

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
        "name":f"Highway Maintenance and Roadworks Workwear Supply and Embroidery in {town}",
        "serviceType":"Highway maintenance and roadworks workwear and PPE supply and embroidery",
        "provider":{"@id":"https://www.ineedworkwear.com/#organization"},
        "areaServed":[{"@type":"City","name":town}]+[{"@type":"City","name":n} for n in nearby],
        "audience":{"@type":"BusinessAudience","name":"Local authority highways teams and roadworks contractors"},
        "description":f"Class 3 hi-vis, safety boots, waterproofs, thermal layers, hard hats and gloves supplied to highway maintenance teams and roadworks contractors in {town}, Chapter 8 ready, with in-house embroidery and multi-depot supply.",
        "hasOfferCatalog":{"@type":"OfferCatalog","name":"Highway Maintenance Workwear",
            "itemListElement":[{"@type":"Offer","itemOffered":{"@type":"Product","name":p}} for p in HM_PRODUCTS]}}
    crumb = {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Home","item":DOMAIN},
        {"@type":"ListItem","position":2,"name":"Highway Maintenance Workwear","item":f"{DOMAIN}/highway-maintenance-workwear"},
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

    emb_svg   = EMB.replace('a London highways company logo', f'a {town} highways company logo')
    sign_svg  = SIGNPOST.replace('London highway maintenance and roadworks signpost', f'{town} highway maintenance and roadworks signpost')
    sign_svg  = re.sub(r'<text x="230" y="62".*?</text>', signpost_town(town), sign_svg, flags=re.S)
    sign_svg  = sign_svg.replace('every kind of London highways work', f'every kind of {town} highways work')
    prem_svg  = PREMISES.replace('serving councils and contractors across London', f'serving councils and contractors across {town}')

    H=[build_head(town, slug, faqs, nearby), HEADER]
    H.append(f'<div class="hm-hero"><div class="hm-wrap"><div class="hm-subtitle">Chapter 8 Hi-Vis and Workwear for Highways Teams</div><h1>{town} Highway Maintenance and Roadworks Workwear</h1></div></div>')
    H.append('<div class="hm-pulse"></div>')
    H.append(f'<div class="hm-trust-strip"><p>{trust}</p></div>')
    H.append(f'<div class="hm-wrap"><div class="hm-snapshot"><div class="hm-snapshot-label">Supplier Snapshot</div><p>{snap}</p></div></div>')
    H.append(STATS)
    H.append('<div class="hm-cta-bar"><a href="https://www.ineedworkwear.com" class="hm-cta-btn">Browse Highway Maintenance Workwear</a></div>')
    H.append('<div class="hm-jump-links"><a href="#range">Workwear Range</a><a href="#contract">Chapter 8 Compliance</a><a href="#accounts">Ordering and Accounts</a><a href="#order">How to Order</a></div>')
    H.append(GARMENT)
    H.append(f'<div class="hm-section"><div class="hm-wrap"><h2>{s1head}</h2>'+''.join(f'<p>{p}</p>' for p in s1ps)+'</div></div>')
    H.append(f'<div class="hm-section" id="range"><div class="hm-wrap"><h2>Highway Maintenance Workwear Range</h2><p>{s2intro} <a href="https://www.ineedworkwear.com">Browse the full range at iNeedWorkwear.com</a>.</p><p class="hm-btn-center"><a href="https://www.ineedworkwear.com" class="hm-section-btn">Browse The Range</a></p>{grid}</div></div>')
    H.append(f'<div class="hm-section"><div class="hm-wrap"><h2>Branding, Identity and Conspicuity</h2>'+''.join(f'<p>{p}</p>' for p in emb)+'</div></div>')
    H.append(emb_svg)
    H.append(f'<div class="hm-wrap"><div class="hm-contract" id="contract"><h3>{CON_HEAD}</h3>'+''.join(f'<p>{p}</p>' for p in con)+'</div></div>')
    H.append(sign_svg)
    H.append(f'<div class="hm-section" id="accounts"><div class="hm-wrap"><h2>{ACC_HEAD}</h2>'+''.join(f'<p>{p}</p>' for p in acc)+'</div></div>')
    H.append(prem_svg)
    H.append(f'<div class="hm-section"><div class="hm-wrap"><h2>Why Highways Teams and Contractors Choose iNeedWorkwear</h2>'+''.join(f'<p>{p}</p>' for p in why)+'</div></div>')
    H.append(ORDER)
    H.append(f'<div class="hm-section" id="order"><div class="hm-wrap"><h2>How to Order Highway Maintenance Workwear</h2><p>{ordr[0]}</p><p>{ordr[1]}</p><p>{ordr[2]}</p><p class="hm-btn-center"><a href="https://www.ineedworkwear.com" class="hm-section-btn">Request A Quote</a></p><p>{selfp}</p>'+CONTACT+'</div></div>')
    faq_html=''.join(f'<div class="hm-faq-item"><div class="hm-faq-q">{q}</div><div class="hm-faq-a">{a}</div></div>' for q,a in faqs)
    H.append(f'<div class="hm-faq"><div class="hm-wrap"><h2>Highway Maintenance Workwear FAQ</h2>{faq_html}</div></div>')
    H.append(f'<div class="hm-wrap"><div class="hm-workwear">{sorted_}</div></div>')
    nb_links=''.join(f'<a href="hm-{slugify(n)}.html">Highway maintenance workwear in {n}</a>\n' for n in nearby)
    H.append(f'<div class="hm-nearby"><div class="hm-wrap"><h3>Highway Maintenance Workwear in Nearby Towns</h3><div class="hm-nearby-links">{nb_links}</div></div></div>')
    H.append(FOOTER+'\n</body></html>')
    return '\n'.join(H)

def main():
    args=[a for a in sys.argv[1:]]
    outdir=os.environ.get('HM_OUTDIR','outputs')
    os.makedirs(outdir, exist_ok=True)
    if not args:
        args=[t for t in TOWNS if t!='london']
    for town_key in args:
        tk=town_key.lower()
        if tk=='london': continue
        if tk not in TOWNS:
            print(f"SKIP {town_key}: not in TOWNS (must be web-researched first)"); continue
        town=' '.join(w.capitalize() for w in tk.split())
        slug=f"hm-{slugify(town)}"
        html=assemble(slug, town)
        path=os.path.join(outdir, f"{slug}.html")
        open(path,'w',encoding='utf-8').write(html)
        print(f"WROTE {path}  ({len(html.split())} words approx)")

if __name__=='__main__':
    main()
