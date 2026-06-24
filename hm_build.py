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
 "glasgow": {
  "region":"Glasgow and the west of Scotland",
  "nearby":["Paisley","Motherwell","Clydebank"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Glasgow's highway maintenance teams and roadworks contractors, from the city council's in-house roads service and its carriageway and lighting renewal programme to Amey's Transport Scotland trunk-road work on the M8 and the Clyde crossings, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the west of Scotland's roads running",
  "s1loc":[
   "Glasgow carries Scotland's densest urban traffic, with the M8 cutting through the city centre over the Kingston Bridge and the Clyde Tunnel running beneath the river. The city council is the roads authority for the local carriageways, footways and many thousands of lighting columns, and its crews work in Class 3 hi-vis within feet of moving traffic on almost every job.",
   "The council has been delivering a multi-year roads renewal programme worth well over one hundred million pounds, resurfacing hundreds of streets, replacing around nine thousand lighting columns with LED and tackling drainage, with its own neighbourhoods and roads teams doing the work and contractors called off for the larger schemes. It also maintains the Clyde Tunnel directly, an unusual structural responsibility for a city council.",
   "Beyond the local network, Transport Scotland is the roads authority for the motorways, with Amey running the south-west trunk-road unit covering the M8, M74, M77, M73 and the Erskine Bridge in recent years. The Kingston Bridge carries one of the heaviest flows in the country and is closed overnight for joint and bearing inspection, the kind of high-speed, after-dark work where being seen is everything.",
   "Resurfacing, lining, gully work, lighting, structures and winter gritting on the city's steep streets all put Glasgow gangs out on live carriageways in full Class 3 hi-vis, jacket and trousers together.",
  ],
  "kit_loc":"across the city's carriageway, lighting and winter-maintenance work",
  "s2_intro":"Across Glasgow's council carriageway, lighting and drainage work and the Transport Scotland trunk-road network",
 },
 "sheffield": {
  "region":"Sheffield and South Yorkshire",
  "nearby":["Rotherham","Barnsley","Doncaster"],
  "snapshot":"iNeedWorkwear kits Sheffield's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from Amey's long-running Streets Ahead PFI across the city to National Highways work on the M1 and M18, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep South Yorkshire's roads running",
  "s1loc":[
   "Sheffield spreads across seven hills and several river valleys, which makes its road network one of the most awkward in the country to surface and grit. The city's carriageways, footways, bridges, drainage, signals and tens of thousands of lighting columns are run under one of England's longest highway PFIs, and the gangs that look after them work in Class 3 hi-vis beside live traffic.",
   "That work runs through Streets Ahead, the twenty-five-year PFI with Amey that reaches into the 2030s, which resurfaced more than half the city's roads and switched the whole lighting stock to LED in its core investment period before moving to a mix of preventative and reactive upkeep. It is a large, heavily audited programme that puts crews on the carriageway day and night.",
   "The motorways belong to National Highways, with the M1 along the eastern edge through junctions 31 to 35a, the M18 peeling off at 32a and the trans-Pennine A57 and A628 Woodhead route heading west toward Manchester. The Supertram shares carriageway across much of the city, so works near the tram reservation add a layer of coordination to already fast, exposed roads.",
   "Surfacing, lining, gully and drainage, lighting, structures and winter gritting on the steep valley roads put Sheffield crews out in Class 3 hi-vis beside running traffic through the year.",
  ],
  "kit_loc":"across the city's carriageway, lighting and winter-maintenance work",
  "s2_intro":"Across Sheffield's Streets Ahead carriageway, lighting and drainage work and the National Highways motorway network",
 },
 "manchester": {
  "region":"Manchester and Greater Manchester",
  "nearby":["Salford","Stockport","Bolton"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Manchester's highway maintenance teams and roadworks contractors, from the city council's repair framework and the Transport for Greater Manchester Key Route Network to National Highways work on the M60 ring, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep Greater Manchester's roads running",
  "s1loc":[
   "Manchester sits inside one of the busiest motorway boxes in Britain, ringed by the M60 and threaded by the Metrolink tram. The city council looks after the local carriageways, footways and cycleways, while Transport for Greater Manchester coordinates a Key Route Network of around six hundred kilometres of the busiest roads across the ten boroughs that carries most of the peak traffic.",
   "Rather than a PFI, the city runs planned and reactive repairs through a maintenance framework, with firms such as Thermal Road Repairs among those appointed and a planned programme worth tens of millions of pounds a year. Across the conurbation the combined authority and TfGM fund a multi-year renewals programme under the Bee Network banner, keeping repair gangs out across the city day and night.",
   "National Highways runs the motorways: the M60 orbital, the M62 east to west, the M56 to the south, the M61 toward Bolton and the M6 to the west, with schemes such as Simister Island and the A57 link in the pipeline. Metrolink shares city-centre carriageway and junctions, so works near the tramway need careful staging alongside fast motorway traffic.",
   "Resurfacing, lining, drainage, lighting, structures, tram-corridor works and winter gritting all mean Manchester gangs work in hi-vis next to live traffic.",
  ],
  "kit_loc":"across the city's carriageway, tram-corridor and winter-maintenance work",
  "s2_intro":"Across Manchester's council carriageway and tram-corridor work and the National Highways motorway box",
 },
 "edinburgh": {
  "region":"Edinburgh and the Lothians",
  "nearby":["Glasgow","Dundee","Livingston"],
  "snapshot":"iNeedWorkwear kits Edinburgh's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from the council's in-house roads operations and construction framework to BEAR Scotland's Transport Scotland work on the A720 City Bypass, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Lothians' roads running",
  "s1loc":[
   "Edinburgh's roads run through a tight, hilly historic core, with a tram line down Princes Street and Leith Walk that complicates any city-centre dig. The council maintains the carriageways, footways, bridges, retaining walls and lighting, and its crews turn out in Class 3 hi-vis to work safely beside the capital's busy traffic.",
   "The council delivers roads work through its own roads operations team backed by a multi-year construction framework worth around one hundred million pounds, with surfacing and civils lots held by contractors including Aggregate Industries and Holcim. In a recent year it logged its largest single jump in road condition on record, improving hundreds of thousands of square metres of carriageway and footway.",
   "Transport Scotland is the roads authority for the trunk network, with BEAR Scotland running the south-east unit and maintaining the A720 Edinburgh City Bypass, the A1 and the routes out across the Lothians and Borders, while the Queensferry Crossing carries the M90 over the Forth nearby. Bypass work means fast roads, lane closures and traffic management at all hours.",
   "Resurfacing, lining, drainage, lighting, retaining walls and winter gritting on the bypass and the city's hills are all handled by Edinburgh crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the city's carriageway, tram-corridor and winter-maintenance work",
  "s2_intro":"Across Edinburgh's council carriageway and tram-corridor work and the Transport Scotland trunk-road network",
 },
 "liverpool": {
  "region":"Liverpool and Merseyside",
  "nearby":["Birkenhead","St Helens","Warrington"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Liverpool's highway maintenance teams and roadworks contractors, from the council's term contractors and the Liverpool City Region works framework to National Highways work on the M62 and M57, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep Merseyside's roads running",
  "s1loc":[
   "Liverpool's network packs a dense city and dockland into the east bank of the Mersey, with the Queensway and Kingsway road tunnels running under the river to Birkenhead and Wallasey. The council maintains the carriageways, footways and lighting, while Merseytravel operates and maintains the two tunnels, and repair gangs work the whole lot in Class 3 hi-vis beside live traffic.",
   "Day-to-day maintenance runs through term contracts with local firms such as Dowhigh and Huyton Asphalt Civils, north and south of the city, sitting beneath a large Liverpool City Region planned-works framework shared with the neighbouring boroughs and the combined authority for resurfacing, signals and bridges. Eight contractors hold places on that wider framework for the bigger capital schemes.",
   "National Highways carries the motorways, with the M62 east to Manchester, the M57 outer ring, the M58 toward the M6 and the M53 over on the Wirral, plus the historic A580 East Lancashire Road as a major arterial. Tunnel approaches and motorway lane closures alike mean fast traffic and tight management on the busiest crossings in the region.",
   "Resurfacing, lining, drainage, lighting, structures, tunnel-approach works and winter gritting keep Liverpool crews in hi-vis within feet of moving traffic.",
  ],
  "kit_loc":"across the city's carriageway, tunnel-approach and winter-maintenance work",
  "s2_intro":"Across Liverpool's council carriageway and tunnel-approach work and the National Highways motorway network",
 },
 "bristol": {
  "region":"Bristol and the West of England",
  "nearby":["Bath","Weston-super-Mare","Gloucester"],
  "snapshot":"iNeedWorkwear kits Bristol's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from the council's term and asset frameworks to National Highways work on the M5, M4 and M32, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the West of England's roads running",
  "s1loc":[
   "Bristol holds more than twelve hundred kilometres of carriageway across a hilly, historic street pattern, with the M32 urban motorway driving straight into the centre. The council maintains the roads, footways, cycleways, bridges, subways and drainage, and its repair gangs work in Class 3 hi-vis beside the city's heavy traffic.",
   "Maintenance runs through term contracts and frameworks rather than a PFI, including a highways asset management and civils framework worth hundreds of millions of pounds spread over surfacing, bridges and traffic-management lots, with Eurovia, Tarmac, Breedon and Colas among those appointed. Much of the funding flows from the West of England Combined Authority transport settlement.",
   "National Highways runs the motorways, with the M5 north to south past Avonmouth, the M4 east toward the Severn crossings and the M32 spur into the centre. The M5 Avonmouth Bridge alone carries well over one hundred thousand vehicles a day, so structural and resurfacing work there means high-speed traffic and overnight closures.",
   "Resurfacing, lining, drainage, lighting, bridges and winter gritting put Bristol gangs out on live carriageways in full Class 3 hi-vis, jacket and trousers together.",
  ],
  "kit_loc":"across the city's carriageway, lighting and winter-maintenance work",
  "s2_intro":"Across Bristol's council carriageway, lighting and drainage work and the National Highways motorway network",
 },
 "cardiff": {
  "region":"Cardiff and South Wales",
  "nearby":["Newport","Pontypridd","Bridgend"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Cardiff's highway maintenance teams and roadworks contractors, from the council's in-house operation at Brindley Road to the Welsh Government trunk-road network on the M4 and A470, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep South Wales's roads running",
  "s1loc":[
   "Cardiff maintains around five thousand roads and over one hundred thousand highway assets across the Welsh capital. It runs a largely direct-labour operation from its Brindley Road depot in Tremorfa, handling carriageway and footway repairs, lighting, drainage, gully cleansing and barriers, with gangs working in Class 3 hi-vis beside the city's traffic.",
   "The council fields a frontline team of around two hundred staff for planned and reactive work, letting specialist contracts for the larger schemes and managing its stock through a highway asset management plan. It is an unusually in-house model for a city of this size, keeping most everyday maintenance under direct control.",
   "The Welsh Government is the roads authority for the motorways and trunk roads, managed through the South Wales Trunk Road Agent with Traffic Wales running the control centre in Cardiff. The M4 passes north of the city, the A4232 Cardiff Bay link and the A470 into the valleys are trunk routes, and the Brynglas Tunnels just west at Newport are a notorious pinch point for works.",
   "Resurfacing, lining, drainage, lighting, structures and winter gritting put Cardiff crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the city's carriageway, lighting and winter-maintenance work",
  "s2_intro":"Across Cardiff's council carriageway, lighting and drainage work and the Welsh Government trunk-road network",
 },
 "leicester": {
  "region":"Leicester and the East Midlands",
  "nearby":["Nottingham","Coventry","Northampton"],
  "snapshot":"iNeedWorkwear kits Leicester's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from the council's Aggregate Industries surfacing contract to National Highways work on the M1 and M69, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the East Midlands' roads running",
  "s1loc":[
   "Leicester is a compact, busy city wrapped by inner and outer ring roads, with roughly thirty-seven thousand street lights and more than two hundred bridges and structures on the council's books. Its maintenance gangs work in Class 3 hi-vis beside heavy city traffic, day and night.",
   "Carriageway patching and resurfacing run through Aggregate Industries, holding both a multi-year city contract and a larger joint patching deal with the surrounding county that spans thousands of kilometres, fed by asphalt from the Bardon Hill and Croft quarries in Leicestershire. The council also runs separate contracts for structures and street lighting.",
   "National Highways carries the motorways, with the M1 to the west through junctions 21 and 21A, the M69 linking south to Coventry and the M6, and the A46 Leicester Western Bypass tying the motorway to the city's outer ring. The city's role as a logistics hub keeps freight heavy on those approaches at all hours.",
   "Resurfacing, patching, lining, drainage, ring-road work and winter gritting mean Leicester gangs work in hi-vis next to live traffic.",
  ],
  "kit_loc":"across the city's carriageway, ring-road and winter-maintenance work",
  "s2_intro":"Across Leicester's council carriageway and ring-road work and the National Highways motorway network",
 },
 "bradford": {
  "region":"Bradford and West Yorkshire",
  "nearby":["Leeds","Halifax","Huddersfield"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Bradford's highway maintenance teams and roadworks contractors, from the council's in-house operation and the Yorkshire Highways Alliance framework to National Highways work on the M62 and M606, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Bradford district's roads running",
  "s1loc":[
   "The Bradford district climbs steeply into the Pennines, with large estates and roads sitting above the normal snow line, which makes winter and surfacing work unusually demanding. The council runs its highways operation from Britannia House and depots including Stockbridge in Keighley, and its gangs work in Class 3 hi-vis on fast, often exposed roads.",
   "Surfacing and planing run through the Yorkshire Highways Alliance, a collaborative framework led by Kirklees for Bradford, Leeds, Wakefield, York and Calderdale, with Colas among the appointed contractors, while the council's own drivers grit more than seven hundred miles of priority routes from four depots. The wider programme is funded through the West Yorkshire Combined Authority.",
   "National Highways carries the motorways, with the M62 along the south of the district and the M606 spur running north into Bradford as its main motorway link, while the A650, A647 and A641 carry the heaviest urban traffic. Much of this runs on night and lane closures where speed and poor light are the real hazard.",
   "Resurfacing, lining, drainage, lighting, structures and heavy winter gritting on the high Pennine roads are all handled by Bradford crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the district's carriageway, lighting and winter-maintenance work",
  "s2_intro":"Across Bradford's council carriageway, lighting and drainage work and the National Highways motorway network",
 },
 "coventry": {
  "region":"Coventry and Warwickshire",
  "nearby":["Birmingham","Leamington Spa","Rugby"],
  "snapshot":"iNeedWorkwear kits Coventry's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from the council's Balfour Beatty term contract and street-lighting PFI to National Highways work on the M6, M69 and A46, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep Coventry and Warwickshire's roads running",
  "s1loc":[
   "Coventry's network of around nine hundred kilometres is built around a grade-separated inner ring road, one of the more complex urban structures in England. The council maintains the carriageways, footways, drainage, structures and tens of thousands of lights, with highway structures alone valued near half a billion pounds, and its gangs work the lot in Class 3 hi-vis.",
   "Highway maintenance runs through a long-standing term contract with Balfour Beatty Living Places alongside a street-lighting PFI, and from 2026 a new joint Warwickshire contract run with Solihull and the county, again with Balfour Beatty, covering more than five thousand kilometres of road across the three authorities. Temporary traffic management is let separately.",
   "National Highways carries the motorways, with the M6 to the north and west, the M69 east to Leicester and the A46 forming part of the city's orbital, where a major grade-separated upgrade is planned at the Walsgrave junction. The ring road and these trunk routes mean fast traffic and constant lane closures.",
   "Resurfacing, lining, drainage, lighting, structures and ring-road work keep Coventry crews in hi-vis within feet of moving traffic.",
  ],
  "kit_loc":"across the city's carriageway, ring-road and winter-maintenance work",
  "s2_intro":"Across Coventry's council carriageway and ring-road work and the National Highways motorway network",
 },
 "nottingham": {
  "region":"Nottingham and the East Midlands",
  "nearby":["West Bridgford","Beeston","Arnold"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Nottingham's highway maintenance teams and roadworks contractors, from the council's Thomas Bow surfacing framework and street-lighting PFI to National Highways work on the M1, A52 and A453, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep Nottingham's roads running",
  "s1loc":[
   "Nottingham runs around eight hundred and twenty-five kilometres of adopted road alongside one of the largest tram systems in the country, the NET network sharing carriageway right through the centre. The council looks after the roads, footways, drainage and lighting, and its gangs work in Class 3 hi-vis beside both traffic and live tram track.",
   "Surfacing and civils run through a joint Nottingham and Derby framework with Thomas Bow City Asphalt among the appointed contractors, while around thirty-six thousand lighting columns sit under a long PFI now maintained and converted to LED by Enerveo. The East Midlands Combined County Authority has lifted road-maintenance funding sharply across the city and county.",
   "National Highways carries the strategic roads, with the M1 to the west, the A52 east to west through the city and the dualled A453 linking junction 24 into Clifton. The A52 is set for a major junction improvement, and any work near the NET track has to be booked weeks ahead with the tram depot at Wilkinson Street.",
   "Resurfacing, lining, drainage, lighting, tram-corridor work and winter gritting put Nottingham gangs out on live carriageways in full Class 3 hi-vis, jacket and trousers together.",
  ],
  "kit_loc":"across the city's carriageway, tram-corridor and winter-maintenance work",
  "s2_intro":"Across Nottingham's council carriageway and tram-corridor work and the National Highways motorway network",
 },
 "newcastle upon tyne": {
  "region":"Newcastle upon Tyne and Tyneside",
  "nearby":["Gateshead","Tynemouth","Whitley Bay"],
  "snapshot":"iNeedWorkwear kits Newcastle upon Tyne's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from the council's in-house teams and the Tyne crossings to National Highways work on the A1 Western Bypass and A19, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep Tyneside's roads running",
  "s1loc":[
   "Newcastle's network centres on a knot of river crossings, with the council-maintained A167(M) Central Motorway lifting traffic over the city and the Tyne and Wear Metro running through and beneath it. The council inspects, repairs and maintains every public road in the city around the clock, and its gangs work in Class 3 hi-vis on fast, structurally complex roads.",
   "Maintenance runs largely through in-house teams backed by the North East procurement frameworks, with a major refurbishment of the A167(M) Central Motorway viaduct underway by VolkerStevin and VolkerLaser, and the landmark Tyne Bridge in a multi-year restoration by Esh Construction shared with Gateshead. Street lighting sits under a PFI run with North Tyneside.",
   "National Highways carries the strategic roads, with the heavily loaded A1 Western Bypass along the western edge of the city and the A19 and Tyne Tunnel to the east, the tunnel operated as a tolled crossing by TT2 for the region. Bypass, viaduct and tunnel work all mean fast traffic and tight overnight management.",
   "Resurfacing, lining, drainage, lighting, bridges and winter gritting put Newcastle crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the city's carriageway, bridge and winter-maintenance work",
  "s2_intro":"Across Newcastle upon Tyne's council carriageway and bridge work and the National Highways trunk-road network",
 },
 "sunderland": {
  "region":"Sunderland and Wearside",
  "nearby":["Washington","Houghton le Spring","Seaham"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Sunderland's highway maintenance teams and roadworks contractors, from the council's surfacing contractors and the Strategic Transport Corridor to National Highways work on the A19, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep Wearside's roads running",
  "s1loc":[
   "Sunderland's roads straddle the River Wear, so crossings shape every maintenance round, from the cable-stayed Northern Spire down to the Wearmouth and Queen Alexandra bridges. The council maintains the carriageways, footways, lighting and structures, and the Tyne and Wear Metro runs through the city too, with gangs working in Class 3 hi-vis beside live traffic.",
   "Resurfacing runs mainly through the regional NEPO surfacing framework, with Sunderland-based Northumbrian Roads among the contractors, and the council has carried recent highways programmes worth eight to eleven million pounds across well over a hundred schemes. Street lighting and signs sit under a long PFI delivered by Aurora, a Balfour Beatty business, which fitted tens of thousands of LED lanterns.",
   "National Highways carries the A19, the main north-south route west of the city crossing the Wear at Hylton, with recent junction upgrades at Downhill Lane, while the council-maintained A1231 runs over the Northern Spire toward Washington and the A1. The Nissan plant nearby keeps freight heavy on those corridors.",
   "Resurfacing, lining, drainage, lighting, bridges and winter gritting mean Sunderland gangs work in hi-vis next to live traffic.",
  ],
  "kit_loc":"across the city's carriageway, lighting and winter-maintenance work",
  "s2_intro":"Across Sunderland's council carriageway, lighting and drainage work and the National Highways trunk-road network",
 },
 "brighton": {
  "region":"Brighton and the South Coast",
  "nearby":["Hove","Worthing","Eastbourne"],
  "snapshot":"iNeedWorkwear kits Brighton's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from the council's FM Conway highways framework and seafront structures to National Highways work on the A27 and A23, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the South Coast's roads running",
  "s1loc":[
   "Brighton and Hove runs a dense seafront and downland network as a single unitary authority, with around six hundred and twenty kilometres of carriageway and a hundred and fifty kilometres of ageing concrete roads. It also carries an unusual stock of coastal structures, including the seafront arches under King's Road, and its gangs work in Class 3 hi-vis beside busy traffic.",
   "The council runs a multi-supplier highways framework with FM Conway holding the main civils and resurfacing lot alongside Edburton and RJ Dance, and the road-lining lot too, a deal worth around one hundred and sixty-six million pounds. Major seafront and Valley Gardens schemes run on top of routine work, all in a salt-laden setting that is hard on surfacing.",
   "National Highways carries the trunk roads, with the A27 Brighton bypass running east to west across the top of the city, the A23 north toward the M23 and the complex Patcham Interchange where the two networks meet. The council picks up the local network beneath, including the steep Downs climbs of Ditchling Road and Bear Road.",
   "Resurfacing, lining, drainage, lighting, seafront structures and winter gritting on the Downs are all handled by Brighton crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the city's carriageway, seafront and winter-maintenance work",
  "s2_intro":"Across Brighton's council carriageway and seafront work and the National Highways trunk-road network",
 },
 "plymouth": {
  "region":"Plymouth and South West Devon",
  "nearby":["Saltash","Newton Abbot","Torquay"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Plymouth's highway maintenance teams and roadworks contractors, from the council's South West Highways term contract to National Highways work on the A38 Devon Expressway, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep South West Devon's roads running",
  "s1loc":[
   "Plymouth is hemmed in by water, the Plym to the east, the tidal Tamar to the west and the Sound to the south, so its road network leans heavily on a handful of crossings. The council maintains the carriageways, footways, lighting and structures, including dozens of bridges and four tunnels, and its gangs work in Class 3 hi-vis beside live traffic.",
   "Highway maintenance runs under the Plymouth Highways term contract with South West Highways, a Ringway and Eurovia business, covering carriageways, drainage, structures, lighting and winter service from the Prince Rock depot. The Tamar Bridge, carrying the A38 into Cornwall, is run jointly with Cornwall Council as a tolled crossing by the bridge and ferry joint committee.",
   "National Highways carries the A38 Devon Expressway straight through the city from Marsh Mills toward the Tamar, including the tidal-flow lanes through the Saltash Tunnel, and the A380 toward Torbay. With the naval dockyard at Devonport and the ferry port loading the approaches, this is fast, freight-heavy work.",
   "Resurfacing, lining, drainage, lighting, structures and winter gritting on the city's hills put Plymouth crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the city's carriageway, expressway and winter-maintenance work",
  "s2_intro":"Across Plymouth's council carriageway work and the National Highways A38 Devon Expressway",
 },
 "hull": {
  "region":"Hull and the East Riding",
  "nearby":["Grimsby","Beverley","Goole"],
  "snapshot":"iNeedWorkwear kits Hull's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from the council's in-house Streetscene service to National Highways work on the A63 Castle Street and A1033, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep Hull and the East Riding's roads running",
  "s1loc":[
   "Hull is a working port on the Humber, and its road network is shaped by dock and freight traffic moving to and from Associated British Ports. Kingston upon Hull City Council handles most routine and reactive maintenance in-house through its Streetscene service, covering carriageways, footways and drainage, with gangs working in Class 3 hi-vis beside heavy goods traffic.",
   "Street lighting is maintained by the council-linked Kingstown Works on a large LED programme, and the council's gritters run from the Stockholm Road depot to treat a long priority network across an exposed, low-lying district. Most carriageway work is delivered directly by the council's own teams.",
   "National Highways carries the strategic roads, with the A63 Castle Street the main artery linking the M62 to the Port of Hull, now part-way through a major grade-separated rebuild at Mytongate, and the A1033 running east to the Saltend chemical complex. Port-access work means fast roads, heavy freight and tight diversions.",
   "Resurfacing, lining, drainage, lighting, port-access work and winter gritting on the exposed estuary roads mean Hull gangs work in hi-vis next to live traffic.",
  ],
  "kit_loc":"across the city's carriageway, port-access and winter-maintenance work",
  "s2_intro":"Across Hull's council carriageway and port-access work and the National Highways trunk-road network",
 },
 "derby": {
  "region":"Derby and the East Midlands",
  "nearby":["Nottingham","Burton-on-Trent","Long Eaton"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Derby's highway maintenance teams and roadworks contractors, from the council's in-house Commercial Services to National Highways work on the A38 and A52, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep Derby's roads running",
  "s1loc":[
   "Derby runs around eight hundred kilometres of carriageway serving one of the country's densest advanced-manufacturing clusters, from Rolls-Royce at Sinfin to the rail works at Litchurch Lane. The council delivers highways through its in-house Commercial Services arm, based centrally for fast response, maintaining footways, drainage and structures as well as the carriageway, all in Class 3 hi-vis.",
   "The direct-labour team is backed by a multi-lot framework worth tens of millions of pounds covering markings, signals, surfacing and traffic management, and the Commercial Services arm also takes on civils and footway work for outside clients across the area. It is a notably self-sufficient highways operation.",
   "National Highways carries the trunk roads, with the A38 west and north of the city, the A52 east toward Nottingham meeting it at Markeaton and the M1 a short way east. A major A38 junctions upgrade at Kingsway, Markeaton and Little Eaton is in the pipeline, with freight from the city's factories keeping the routes busy.",
   "Resurfacing, lining, drainage, lighting, structures and winter gritting are all handled by Derby crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the city's carriageway, lighting and winter-maintenance work",
  "s2_intro":"Across Derby's council carriageway, lighting and drainage work and the National Highways trunk-road network",
 },
 "southampton": {
  "region":"Southampton and the South",
  "nearby":["Portsmouth","Eastleigh","Fareham"],
  "snapshot":"iNeedWorkwear kits Southampton's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from the council's Balfour Beatty highways partnership to National Highways work on the M27 and M271, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep Southampton's roads running",
  "s1loc":[
   "Southampton sits between the Test and the Itchen, and its roads carry very heavy dock traffic from one of the country's biggest cruise, container and vehicle ports. The council maintains the carriageways, footways, lighting and structures including the Itchen Bridge, and its gangs work in Class 3 hi-vis beside constant freight.",
   "Maintenance runs through a long-standing partnership with Balfour Beatty Living Places, the Highways Service Partnership, recently renewed for a further multi-year term and run from an operational control hub at the Millbrook depot, covering reactive and planned work, winter service and major structures like the Itchen Bridge refurbishment.",
   "National Highways carries the motorways, with the M27 along the top of the city, the M271 spur down to the Western Docks and the A33, and the M3 and A34 heading north toward Winchester. Dock-access and motorway work mean fast roads and heavy goods movements through the day and night.",
   "Resurfacing, lining, drainage, lighting, structures and port-access work mean Southampton gangs work in hi-vis next to live traffic.",
  ],
  "kit_loc":"across the city's carriageway, port-access and winter-maintenance work",
  "s2_intro":"Across Southampton's council carriageway and port-access work and the National Highways motorway network",
 },
 "stoke-on-trent": {
  "region":"Stoke-on-Trent and Staffordshire",
  "nearby":["Newcastle-under-Lyme","Crewe","Stafford"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Stoke-on-Trent's highway maintenance teams and roadworks contractors, from the council's in-house operations and street-lighting PFI to National Highways work on the A500 and A50, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Potteries' roads running",
  "s1loc":[
   "Stoke-on-Trent is a polycentric Potteries city of six towns set across several steep hills, which gives its road network an unusual spread and plenty of gradient. The council runs a mainly in-house highways operations division covering carriageways, footways, drainage and patching, with gangs working in Class 3 hi-vis beside live traffic.",
   "The in-house team is backed by a multi-lot highway works framework for extra capacity, with contractors such as Kilkern appointed, while over forty thousand street lights sit under a long PFI with the operator Enerveo, all upgraded to LED. Specialist traffic-technology work is contracted separately.",
   "National Highways carries the strategic roads, with the A500 D-road arcing around the city to join the M6 at junctions 15 and 16 and the near-motorway A50 heading east toward Derby. Both carry intense freight from the city's ceramics and distribution parks, so junction work means fast roads and constant lane management.",
   "Resurfacing, lining, drainage, lighting, structures and winter gritting on the Potteries hills keep Stoke crews in hi-vis within feet of moving traffic.",
  ],
  "kit_loc":"across the city's carriageway, lighting and winter-maintenance work",
  "s2_intro":"Across Stoke-on-Trent's council carriageway, lighting and drainage work and the National Highways A500 and A50 network",
 },
 "wolverhampton": {
  "region":"Wolverhampton and the Black Country",
  "nearby":["Dudley","Walsall","West Bromwich"],
  "snapshot":"iNeedWorkwear kits Wolverhampton's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from the council's in-house teams and the Black Country works framework to National Highways work on the M54 and M6, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Black Country's roads running",
  "s1loc":[
   "Wolverhampton sits at the western edge of the Black Country, with the A449 Stafford Road and the A4123 to Birmingham carrying heavy industrial freight straight through the city. The council maintains the great majority of the local carriageways, footways, drainage and lighting, and its gangs work in Class 3 hi-vis beside that traffic.",
   "Highway work runs mainly through the council's in-house teams, which have completed tens of thousands of pothole repairs and grit roughly three hundred and eighty kilometres of priority carriageway, and the council leads procurement of the Black Country highways works framework for the neighbouring authorities and the combined authority. Sixteen contractors are appointed to that framework.",
   "National Highways carries the motorways, with the M54 running west to Telford from its junction with the M6 and the M6 itself passing to the east, and a long-planned M54 to M6 link road set to pull freight off the A449. Black Country routes and motorway work alike mean fast traffic and overnight closures.",
   "Resurfacing, lining, drainage, lighting, structures and winter gritting put Wolverhampton crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the city's carriageway, lighting and winter-maintenance work",
  "s2_intro":"Across Wolverhampton's council carriageway, lighting and drainage work and the National Highways motorway network",
 },
 "swansea": {
  "region":"Swansea and South West Wales",
  "nearby":["Llanelli","Neath","Port Talbot"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Swansea's highway maintenance teams and roadworks contractors, from the council's Swansea Highways Partnership to the Welsh Government trunk-road network on the M4 and A483, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep South West Wales's roads running",
  "s1loc":[
   "Swansea runs a coastal city and county network that stretches from the docks out to the Gower, with seafront and port roads that need surfacing tough enough for a salt-laden setting. The council is the roads authority for all the local routes, covering carriageways, footways, lighting and drainage, and its gangs work in Class 3 hi-vis beside live traffic.",
   "Work runs through the Swansea Highways Partnership, a collaboration between the council's own direct services team and a consortium of Alun Griffiths and Hanson, with the council targeting record highway investment of around twenty million pounds. The model keeps real in-house capacity rather than handing everything to a single outsourced contractor.",
   "The Welsh Government is the roads authority for the motorways and trunk roads, run through the South Wales Trunk Road Agent with Traffic Wales managing the network. The M4 threads the Swansea corridor at junctions 42 to 47, the A483 runs from the motorway into the city and the A484 serves the Llanelli side, all fast routes where works need tight management.",
   "Resurfacing, lining, drainage, lighting, coastal routes and winter gritting put Swansea gangs out on live carriageways in full Class 3 hi-vis, jacket and trousers together.",
  ],
  "kit_loc":"across the city's carriageway, coastal and winter-maintenance work",
  "s2_intro":"Across Swansea's council carriageway and coastal-route work and the Welsh Government trunk-road network",
 },
 "milton keynes": {
  "region":"Milton Keynes and Buckinghamshire",
  "nearby":["Bedford","Northampton","Aylesbury"],
  "snapshot":"iNeedWorkwear kits Milton Keynes's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from the council's Ringway grid-road partnership to National Highways work on the M1 and A5, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep Milton Keynes's roads running",
  "s1loc":[
   "Milton Keynes is built on a planned grid of more than fifteen hundred kilometres of road, with around a hundred and thirty grid-road roundabouts and a separate redway cycle network running through underpasses. The council is the unitary roads authority for the grid roads, footways, bridges, lighting and drainage, and its gangs work in Class 3 hi-vis beside fast grid traffic.",
   "Maintenance runs through a term partnership with Ringway, branded MK Highways, on an annual contract worth around twenty million pounds that covers the carriageways, the redways, hundreds of bridges, tens of thousands of lights and the drainage stock, with a separate developer-funded programme rebuilding the busiest roundabouts. The grid's lane markings need near-constant renewal.",
   "National Highways carries the motorways and trunk roads, with the M1 along the eastern edge at junctions 13 and 14, the A5 running through the western side of the city and the A509 heading north. The grid roads themselves run fast and free-flowing, so resurfacing and roundabout work means live, high-speed traffic.",
   "Resurfacing, lining, roundabout work, lighting, structures and winter gritting across the grid mean Milton Keynes gangs work in hi-vis next to live traffic.",
  ],
  "kit_loc":"across the grid roads, roundabout and winter-maintenance work",
  "s2_intro":"Across Milton Keynes's grid-road, roundabout and lighting work and the National Highways motorway network",
 },
 "aberdeen": {
  "region":"Aberdeen and the North East of Scotland",
  "nearby":["Elgin","Arbroath","Dundee"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Aberdeen's highway maintenance teams and roadworks contractors, from the city council's roads service to the Transport Scotland network and the AWPR bypass, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the North East of Scotland's roads running",
  "s1loc":[
   "Aberdeen is a granite city with a busy, expanding harbour, and its approach roads carry heavy traffic to the port and the energy supply base. The city council runs its own roads service covering carriageways, footways, lighting and drainage, and its gangs work in Class 3 hi-vis through a hard northern climate.",
   "Routine maintenance runs through an annual maintenance contract and roads service framework, on a roads and infrastructure budget of around ten million pounds a year, with the surrounding north-east network maintained separately by the neighbouring council. Larger schemes are competitively tendered through Scottish public-sector frameworks.",
   "Transport Scotland is the roads authority for the trunk network, with Amey running the north-east unit on the A90, A96 and A92 in recent years, while the fifty-eight kilometre Aberdeen Western Peripheral Route bypass, opened in 2018 and 2019, is maintained under a long concession by Aberdeen Roads Limited with Balfour Beatty. The bypass and trunk roads mean fast, exposed driving.",
   "Resurfacing, lining, drainage, lighting, harbour-access work and heavy winter gritting are all handled by Aberdeen crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the city's carriageway, harbour-access and winter-maintenance work",
  "s2_intro":"Across Aberdeen's council carriageway and harbour-access work and the Transport Scotland trunk-road network",
 },
 "reading": {
  "region":"Reading and the Thames Valley",
  "nearby":["Slough","Maidenhead","Wokingham"],
  "snapshot":"iNeedWorkwear kits Reading's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from the borough's in-house highways team to National Highways work on the M4 and A33, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Thames Valley's roads running",
  "s1loc":[
   "Reading sits where major road and rail corridors meet in the Thames Valley, carrying high commuter and freight volumes across a network squeezed by the river and the Kennet. The borough is a unitary roads authority covering carriageways, footways, lighting and drainage, and its gangs work in Class 3 hi-vis beside heavy through-traffic.",
   "Maintenance runs through the council's own in-house highways team supported by specialist frameworks, with several million pounds of road investment over recent years and twice-yearly maintenance on major routes including the A329M, A3290 and A33 corridors. Concrete-road preservation has been a particular focus on the older dual carriageways.",
   "National Highways carries the strategic roads, with the M4 across the southern edge at junctions 10 to 12, the A33 relief road heading south toward Basingstoke and the A329M spur into the town. Commuter peaks and motorway closures alike mean fast traffic and tight working windows.",
   "Resurfacing, lining, drainage, lighting, concrete-road work and winter gritting keep Reading crews in hi-vis within feet of moving traffic.",
  ],
  "kit_loc":"across the town's carriageway, lighting and winter-maintenance work",
  "s2_intro":"Across Reading's council carriageway, lighting and drainage work and the National Highways M4 corridor",
 },
 "northampton": {
  "region":"Northampton and West Northamptonshire",
  "nearby":["Wellingborough","Kettering","Daventry"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Northampton's highway maintenance teams and roadworks contractors, from West Northamptonshire's Kier term contract to National Highways work on the M1 and A45, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep West Northamptonshire's roads running",
  "s1loc":[
   "Northampton is a major logistics town built around M1 junction 15, with the Brackmills and Swan Valley distribution estates pumping heavy goods traffic onto the A45 and the motorway approaches. The unitary council is the roads authority for the local carriageways, footways, lighting, drainage and structures, and its gangs work in Class 3 hi-vis beside that freight.",
   "Highway maintenance runs through a term contract with Kier Transportation worth around thirty million pounds a year, covering routine and planned work, resurfacing, structures and winter service, and the council is delivering a programme of A45 junction improvements jointly with National Highways. North Northamptonshire next door runs a parallel Kier contract.",
   "National Highways carries the strategic roads, with the M1 through junctions 15 and 15a, the A45 linking the motorway east through the town toward Wellingborough and the A43 and A508 feeding the wider county. The logistics traffic keeps those routes busy day and night.",
   "Resurfacing, lining, drainage, lighting, structures and winter gritting put Northampton crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the town's carriageway, lighting and winter-maintenance work",
  "s2_intro":"Across Northampton's council carriageway, lighting and drainage work and the National Highways M1 and A45 network",
 },
 "luton": {
  "region":"Luton and Bedfordshire",
  "nearby":["Bedford","Dunstable","Stevenage"],
  "snapshot":"iNeedWorkwear kits Luton's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from the borough's VolkerHighways term contract to National Highways work on the M1, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep Luton's roads running",
  "s1loc":[
   "Luton's road network is shaped by its airport and the M1, with the A505 and the airport spur carrying heavy passenger and commercial traffic at all hours. The borough is a unitary roads authority for around four hundred and eighty kilometres of adopted road, covering carriageways, footways, bridges, drainage and lighting, with gangs working in Class 3 hi-vis beside live traffic.",
   "Maintenance runs through a long-term contract with VolkerHighways, worth up to two hundred million pounds over its life and run from a central depot on Kingsway, covering planned resurfacing, reactive patching, footways, winter gritting and bridge inspection. The council has lifted annual road-repair spending to resurface hundreds of thousands of square metres.",
   "National Highways carries the strategic roads, with the M1 east of the town at junctions 10, 10a and 11 including the airport spur, and the A505 and A6 carrying traffic through the borough. Work near the airport often runs around the clock, so being seen on those approaches is critical.",
   "Resurfacing, lining, drainage, lighting, airport-access work and winter gritting mean Luton gangs work in hi-vis next to live traffic.",
  ],
  "kit_loc":"across the town's carriageway, airport-access and winter-maintenance work",
  "s2_intro":"Across Luton's council carriageway and airport-access work and the National Highways M1 corridor",
 },
 "portsmouth": {
  "region":"Portsmouth and South Hampshire",
  "nearby":["Southampton","Gosport","Fareham"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Portsmouth's highway maintenance teams and roadworks contractors, from the council's Colas highways PFI to National Highways work on the M27 and M275, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep South Hampshire's roads running",
  "s1loc":[
   "Portsmouth is a densely built island city with heavy port and ferry traffic and few parallel routes, so closing one corridor for works ripples across the whole network. The council is the unitary roads authority for the carriageways, footways, lighting and structures, and its gangs work in Class 3 hi-vis in tight, busy streets.",
   "Maintenance runs under a long PFI, with Colas operating the network around the clock through the Ensign Highways arrangement and carrying out heavy structural work on the M275 bridges into the city, from the Tipner Interchange to the Rudmore flyover. The island setting makes structures and bridge upkeep an unusually large part of the job.",
   "National Highways carries the motorways, with the M27 along the top of South Hampshire, the A3(M) spur to the north and the M275 carrying the main route onto the island from the Hilsea Interchange. Island-access work means fast roads and very tight diversions when a lane goes.",
   "Resurfacing, lining, drainage, lighting, bridge work and winter gritting put Portsmouth crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the island city's carriageway, structures and winter-maintenance work",
  "s2_intro":"Across Portsmouth's council carriageway and structures work and the National Highways motorway network",
 },
 "peterborough": {
  "region":"Peterborough and Cambridgeshire",
  "nearby":["Cambridge","Spalding","Stamford"],
  "snapshot":"iNeedWorkwear kits Peterborough's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from the council's Milestone parkway contract to National Highways work on the A1 and A47, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep Peterborough's roads running",
  "s1loc":[
   "Peterborough is a New Town built around high-capacity parkways, the Nene, Fletton and Paston among them, ageing dual carriageways without hard shoulders that need careful cyclical upkeep. The unitary council maintains the local carriageways, footways, lighting and drainage, and its gangs work in Class 3 hi-vis beside fast parkway traffic.",
   "Highway maintenance and street lighting run through a contract now delivered by Milestone Infrastructure, part of M Group, covering design, planned and reactive work, drainage and winter service, with the combined authority funding strategic parkway improvements. The flat fenland to the east makes the parkways especially frost-prone.",
   "National Highways carries the strategic roads, with the A1 and A1(M) west of the city, the A47 Soke Parkway east of Wansford and the A15 to the north, and a programme of A47 dualling and junction work underway. Parkway and trunk work alike mean high-speed traffic and exposed winter conditions.",
   "Resurfacing, lining, drainage, lighting, parkway work and winter gritting on the exposed dual carriageways keep Peterborough crews in hi-vis within feet of moving traffic.",
  ],
  "kit_loc":"across the city's parkway, lighting and winter-maintenance work",
  "s2_intro":"Across Peterborough's council parkway, lighting and drainage work and the National Highways A1 and A47 corridors",
 },
 "bolton": {
  "region":"Bolton and Greater Manchester",
  "nearby":["Wigan","Bury","Salford"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Bolton's highway maintenance teams and roadworks contractors, from the council's highways works framework to National Highways work on the M61 and the TfGM Key Route Network, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep Bolton's roads running",
  "s1loc":[
   "Bolton sits at the Pennine edge of Greater Manchester, with routes climbing toward the West Pennine Moors that bring a long, hard winter season. The borough is the local roads authority for the carriageways, footways, lighting and structures, and its gangs work in Class 3 hi-vis on fast, often high and exposed roads.",
   "Maintenance runs through a multi-lot highways works framework worth around forty million pounds, with established local contractors such as George Cox and Sons appointed across civils, surfacing and structures, and gritters running from the Mayor Street depot through a season that can stretch to twenty-eight weeks. Combined-authority funding tops up skid-resistance work on higher-risk roads.",
   "National Highways carries the motorways, with the M61 linking the M60 to the M6 near Preston through the Horwich and Bolton West junctions and the A666 heading toward Darwen and the moors, while Transport for Greater Manchester coordinates the Key Route Network. The complex Worsley Braided Interchange nearby is among the densest junctions in the North West.",
   "Resurfacing, lining, drainage, lighting, structures and heavy winter gritting on the high moor roads are all handled by Bolton crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the town's carriageway, moor-road and winter-maintenance work",
  "s2_intro":"Across Bolton's council carriageway and moor-road work and the National Highways motorway network",
 },
 "dudley": {
  "region":"Dudley and the Black Country",
  "nearby":["Stourbridge","Halesowen","West Bromwich"],
  "snapshot":"iNeedWorkwear kits Dudley's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from the council's Black Country framework and Lister Road depot to National Highways work on the M5, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Black Country's roads running",
  "s1loc":[
   "Dudley's network runs through the historic industrial heart of the Black Country, with the A4123 Birmingham New Road forming the borough's strategic spine from Wolverhampton toward Birmingham. The borough is the local roads authority for the carriageways, footways, lighting and structures, working from its Lister Road depot, with gangs in Class 3 hi-vis beside heavy freight.",
   "Surfacing and minor works run through a collaborative Black Country procurement model led by Wolverhampton for the four authorities, with Colas appointed to the surfacing framework and a new multi-supplier works framework coming in. The shared model spreads contractors across thousands of kilometres of Black Country road.",
   "National Highways carries the M5 along the eastern edge of the Black Country, with Birchley Island near junction 2 the main interchange for freight using the A4123, while the A461 runs north to south through the borough toward Walsall and Stourbridge. Metro extension works on the A4123 corridor add coordination to the carriageway upkeep.",
   "Resurfacing, lining, drainage, lighting, structures and winter gritting put Dudley crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the borough's carriageway, lighting and winter-maintenance work",
  "s2_intro":"Across Dudley's council carriageway, lighting and drainage work and the National Highways M5 corridor",
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

def _display_name(arg):
    """Resolve a CLI arg (slug or name) to the exact CSV display name and casing."""
    s = slugify(arg)
    for r in _load_csv():
        if slugify(r[1]) == s:
            return r[1]
    return ' '.join(w.capitalize() for w in arg.lower().split())

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
        town=_display_name(town_key)
        tk=town.lower()
        if tk=='london': continue
        if tk not in TOWNS:
            print(f"SKIP {town_key}: not in TOWNS (must be web-researched first)"); continue
        slug=f"hm-{slugify(town)}"
        html=assemble(slug, town)
        path=os.path.join(outdir, f"{slug}.html")
        open(path,'w',encoding='utf-8').write(html)
        print(f"WROTE {path}  ({len(html.split())} words approx)")

if __name__=='__main__':
    main()
