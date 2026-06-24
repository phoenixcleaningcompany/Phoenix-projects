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
 "norwich": {
  "region":"Norwich and Norfolk",
  "nearby":["Ipswich","Cambridge","Peterborough"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Norwich's highway maintenance teams and roadworks contractors, from Norfolk County Council's highways operation to National Highways work on the A47 and A11, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep Norfolk's roads running",
  "s1loc":[
   "Norwich is the hub of a large, mostly rural county network, ringed by the A1270 Broadland Northway, the council-built northern distributor that opened in 2018. Norfolk County Council is the highway authority for the city and the wider county, and its gangs work in Class 3 hi-vis beside live traffic on everything from the ring road to the city's medieval core.",
   "Maintenance has in recent years run through Norse Highways, the council's own company, while Norfolk has let a new fourteen-year highways and infrastructure works term contract worth around seven hundred million pounds to Kier, mobilising from 2026 and covering carriageways, drainage, structures, lighting and winter service across the county. It is one of the largest single highways procurements in the East of England.",
   "National Highways carries the strategic roads, with the A47 running east to west across Norfolk and being dualled in sections, and the A11 the dualled trunk route south-west toward Thetford and Cambridge, the two meeting at the Thickthorn junction now itself due for a major upgrade. Trunk and ring-road work alike mean fast traffic and tight management on roads that funnel into a compact city.",
   "Resurfacing, lining, drainage, lighting, ring-road work and winter gritting across an exposed, low-lying county put Norwich crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the city's carriageway, ring-road and winter-maintenance work",
  "s2_intro":"Across Norwich's council carriageway and ring-road work and the National Highways A47 and A11 network",
 },
 "swindon": {
  "region":"Swindon and Wiltshire",
  "nearby":["Chippenham","Oxford","Newbury"],
  "snapshot":"iNeedWorkwear kits Swindon's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from the borough council's Connor Construction term contract to National Highways work on the M4 and the A419 corridor, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep Wiltshire's roads running",
  "s1loc":[
   "Swindon is a fast-growing unitary on the M4 corridor, famous for the Magic Roundabout, the ring of five mini-roundabouts at the town centre. The borough council is the highway authority for its carriageways, footways, lighting and drainage, and its gangs work in Class 3 hi-vis beside heavy commuter and freight traffic.",
   "The council delivers maintenance through a highway maintenance term service contract awarded in 2024 to Connor Construction, covering drainage works, resurfacing, structural patching and footway treatments, with firms such as Wills Bros and Octavius carrying out recent junction rebuilds at Coate and the White Hart across the New Eastern Villages growth area.",
   "National Highways carries the M4 along the southern edge through junctions 15 and 16, while the A419 dual carriageway north toward Cirencester has run under a long shadow-toll concession managed by Road Management Services. The A420 toward Oxford and the local primary network carry the rest, all fast roads where works need tight management.",
   "Resurfacing, lining, drainage, lighting, roundabout work and winter gritting mean Swindon gangs work in hi-vis next to live traffic.",
  ],
  "kit_loc":"across the town's carriageway, roundabout and winter-maintenance work",
  "s2_intro":"Across Swindon's council carriageway and roundabout work and the National Highways M4 corridor",
 },
 "croydon": {
  "region":"Croydon and South London",
  "nearby":["Sutton","Bromley","Beckenham"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Croydon's highway maintenance teams and roadworks contractors, from the borough's FM Conway highways contract to the Transport for London red routes through the area, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep South London's roads running",
  "s1loc":[
   "Croydon is the largest of the London boroughs by population and a major commercial centre, with a dense road network feeding the A23 Purley Way retail corridor and the town-centre flyover. The council maintains the borough roads while Transport for London runs the red routes, and gangs work in Class 3 hi-vis beside heavy, slow-moving urban traffic.",
   "The council delivers highway maintenance through a contract with FM Conway worth up to one hundred and thirty million pounds over an initial seven years, covering carriageways, footways, drainage, lighting and structures across more than seven hundred kilometres of road. The red routes such as the A23 and A232 are maintained for Transport for London through its own Works for London arrangement, also held by FM Conway in the south.",
   "There is no motorway in the borough, but the A23 Brighton Road and Purley Way, the A232 and the A212 carry intense traffic toward central London and the M25 at junction 7 to the south. Red-route and borough work alike mean constant lane management on some of the busiest urban roads in the country.",
   "Resurfacing, lining, drainage, lighting and footway work are all handled by Croydon crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the borough's carriageway, lighting and footway work",
  "s2_intro":"Across Croydon's borough carriageway and footway work and the Transport for London red-route network",
 },
 "bournemouth": {
  "region":"Bournemouth and East Dorset",
  "nearby":["Poole","Christchurch","Ferndown"],
  "snapshot":"iNeedWorkwear kits Bournemouth's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from the BCP Council highways programme to National Highways work on the A31, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Bournemouth coast's roads running",
  "s1loc":[
   "Bournemouth sits at the heart of the Bournemouth, Christchurch and Poole conurbation on the Dorset coast, with the A338 Wessex Way spur road running straight into the town from the A31. BCP Council is the highway authority for around twelve hundred and fifty kilometres of road across the three towns, and its gangs work in Class 3 hi-vis beside busy seaside and commuter traffic.",
   "BCP Council runs highway maintenance and civil engineering through a term service contract let after the 2019 merger and its own highway delivery team, with major recent works including movement-joint replacement on the Wessex Way overbridges and a fleet of fourteen gritters holding nearly three thousand tonnes of salt for winter. Coastal exposure drives faster wear on the seafront roads.",
   "National Highways carries the A31 to the north of the town, the dualled trunk route toward Ringwood and the M27, while the A338 Wessex Way and the A35 are the main council-managed strategic corridors into and across the conurbation. Spur-road and seafront work alike mean fast traffic and tight working windows.",
   "Resurfacing, lining, drainage, lighting, seafront work and winter gritting put Bournemouth crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the town's carriageway, seafront and winter-maintenance work",
  "s2_intro":"Across Bournemouth's council carriageway and seafront work and the National Highways A31 corridor",
 },
 "southend-on-sea": {
  "region":"Southend-on-Sea and south Essex",
  "nearby":["Basildon","Rayleigh","Canvey Island"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Southend-on-Sea's highway maintenance teams and roadworks contractors, from the city council's Marlborough highways partnership to the A127 and A13 arterial network, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep south Essex's roads running",
  "s1loc":[
   "Southend-on-Sea is a coastal city at the end of the Thames Estuary, with sixteen square miles of network and seven miles of seafront to look after, including the approaches to the longest pleasure pier in the world. The city council is the unitary highway authority, and its gangs work in Class 3 hi-vis beside heavy resort and commuter traffic.",
   "Highway maintenance runs in partnership with Marlborough Highways, covering the carriageways, footways, drainage, lighting, traffic signals, car parks and the foreshore across the city, with the partnership renewed on a new seven-year term from 2026. Recent work has included retiming the A13 and A127 signals to keep the arterial routes flowing.",
   "The A127 Southend Arterial Road and the A13 are the two strategic corridors linking the city to the M25 and London, shared with Essex along their length, with the A130 connecting north toward Chelmsford at the Fairglen interchange. Arterial and seafront work alike mean fast traffic and tight management on routes with few alternatives.",
   "Resurfacing, lining, drainage, lighting, seafront work and winter gritting keep Southend crews in hi-vis within feet of moving traffic.",
  ],
  "kit_loc":"across the city's carriageway, seafront and winter-maintenance work",
  "s2_intro":"Across Southend-on-Sea's council carriageway and seafront work and the A127 and A13 arterial network",
 },
 "walsall": {
  "region":"Walsall and the Black Country",
  "nearby":["Wolverhampton","West Bromwich","Cannock"],
  "snapshot":"iNeedWorkwear kits Walsall's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from the council's Black Country highways framework to National Highways work on the M6 and the A5, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the northern Black Country's roads running",
  "s1loc":[
   "Walsall sits at the northern edge of the Black Country, where historic routes like the A461 Lichfield Road, the A34 and the A454 Black Country Route meet the M6. The metropolitan borough council is the highway authority for the local carriageways, footways, lighting and drainage, and its gangs work in Class 3 hi-vis beside heavy industrial traffic.",
   "Surfacing and minor works run through the collaborative Black Country framework led by Wolverhampton for the four boroughs, with contractors such as Thomas Bow appointed, while the council runs its own resurfacing programme of several miles of carriageway a year and uses rapid patching contractors through the worst of winter. The M6 Junction 10 rebuild was delivered jointly with National Highways.",
   "National Highways carries the M6 along the southern and western edge through junctions 7 to 11 and the A5 to the north around Brownhills, and the long-planned M54 to M6 link will divert thousands of vehicles a day off local A-roads when it is built. The Black Country Route and motorway junction work alike mean fast roads and constant lane management.",
   "Resurfacing, lining, drainage, lighting, structures and winter gritting put Walsall crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the borough's carriageway, lighting and winter-maintenance work",
  "s2_intro":"Across Walsall's council carriageway, lighting and drainage work and the National Highways M6 and A5 network",
 },
 "warrington": {
  "region":"Warrington and Cheshire",
  "nearby":["St Helens","Runcorn","Widnes"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Warrington's highway maintenance teams and roadworks contractors, from the council's Tarmac term contract to National Highways work on the M6, M62 and M56, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep Warrington's roads running",
  "s1loc":[
   "Warrington sits between Manchester and Liverpool at the crossing of the Mersey and the Manchester Ship Canal, where the M6, M62 and M56 all converge. The borough is a unitary highway authority for the local carriageways, footways, lighting and structures, and its gangs work in Class 3 hi-vis beside some of the heaviest motorway-fed traffic in the North West.",
   "Maintenance runs through a term contract with Tarmac, jointly procured with neighbouring Halton, covering carriageways, footways, drainage, bridges, lighting and winter service, with the two boroughs sharing operational resource across Runcorn and Widnes. The council is also promoting a new Western Link bridge over the Ship Canal.",
   "National Highways carries the motorways, with the M6 over the Thelwall Viaduct across the Ship Canal and Mersey, the M62 east to west and the M56 to the south, plus the A49 and A57 as the main local trunk routes. Viaduct and motorway work alike mean fast traffic and major structural maintenance over water.",
   "Resurfacing, lining, drainage, lighting, structures and winter gritting mean Warrington gangs work in hi-vis next to live traffic.",
  ],
  "kit_loc":"across the borough's carriageway, lighting and winter-maintenance work",
  "s2_intro":"Across Warrington's council carriageway, lighting and drainage work and the National Highways motorway network",
 },
 "slough": {
  "region":"Slough and the Thames Valley",
  "nearby":["Maidenhead","Windsor","Uxbridge"],
  "snapshot":"iNeedWorkwear kits Slough's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from the borough council's highways team to National Highways work on the M4 near Heathrow, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Thames Valley's roads running",
  "s1loc":[
   "Slough sits immediately west of London and just north of Heathrow, with the vast Slough Trading Estate, the largest privately owned industrial estate in Europe, generating intense freight on the A4 and the M4. The borough is a unitary highway authority for the local carriageways, footways, lighting and drainage, and its gangs work in Class 3 hi-vis beside that traffic.",
   "The council delivers planned and reactive maintenance through its highways team and works frameworks, having tightened spending after recent financial pressures and aiming to shift the balance toward planned preventative work, and it shares procurement such as traffic-signal maintenance with the other Berkshire authorities. Heavy goods loading off the trading estate drives fast wear on the A4.",
   "National Highways carries the M4 along the southern boundary through junctions 5 and 6, one of the busiest stretches in the country given the Heathrow traffic just to the east, with the A4 Bath Road and the A355 carrying the rest of the strategic load. Motorway and trading-estate work alike mean fast roads and very heavy freight.",
   "Resurfacing, lining, drainage, lighting and winter gritting are all handled by Slough crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the town's carriageway, trading-estate and winter-maintenance work",
  "s2_intro":"Across Slough's council carriageway and trading-estate work and the National Highways M4 corridor",
 },
 "huddersfield": {
  "region":"Huddersfield and Kirklees",
  "nearby":["Halifax","Dewsbury","Brighouse"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Huddersfield's highway maintenance teams and roadworks contractors, from Kirklees Council and the Yorkshire Alliance framework to National Highways work on the trans-Pennine M62, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep Kirklees's roads running",
  "s1loc":[
   "Huddersfield is the main town of Kirklees, set in the southern Pennine valleys where roads climb quickly onto exposed moorland. Kirklees Council is the metropolitan highway authority for the carriageways, footways, lighting and structures, and its gangs work in Class 3 hi-vis on fast, high and weather-beaten roads.",
   "Kirklees leads the Yorkshire Alliance surfacing and planing framework on behalf of Bradford, Leeds, Wakefield, York and Calderdale, an eighty-eight million pound arrangement with Colas across all its lots, and runs a major A629 corridor improvement between Ainley Top and the ring road. It can also call off the North Yorkshire-led carriageways framework for larger schemes.",
   "National Highways carries the trans-Pennine M62 across the north of the district, climbing to the highest point of any motorway in England near Scammonden, where a dedicated fleet handles snow and fog while the lowlands stay clear. The A62 and A616 trans-Pennine routes and the A629 carry the rest, all demanding in winter.",
   "Resurfacing, lining, drainage, lighting and heavy winter gritting on the Pennine passes keep Huddersfield crews in hi-vis within feet of moving traffic.",
  ],
  "kit_loc":"across the district's carriageway, moor-road and winter-maintenance work",
  "s2_intro":"Across Huddersfield's council carriageway and moor-road work and the National Highways trans-Pennine network",
 },
 "telford": {
  "region":"Telford and Shropshire",
  "nearby":["Shrewsbury","Wolverhampton","Cannock"],
  "snapshot":"iNeedWorkwear kits Telford's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from the council's Balfour Beatty highways contract to National Highways work on the M54, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep Shropshire's roads running",
  "s1loc":[
   "Telford is a 1968 new town built around a grid of dual-carriageway distributor roads, with the A442 Queensway as its spine and the M54 as its only motorway. Telford and Wrekin Council is the unitary highway authority for some six hundred miles of road, and its gangs work in Class 3 hi-vis beside fast distributor-road traffic.",
   "Highway maintenance runs through a long-running contract with Balfour Beatty Living Places, worth over one hundred million pounds and covering the carriageways, footpaths, drainage, winter gritting and a capital schemes programme, with AtkinsRealis providing professional and design services alongside. The new-town pavements, much of them concrete and early asphalt, are now reaching the end of their design life.",
   "National Highways carries the M54, the twenty-three-mile Telford motorway running from the M6 to the A5 at Wellington, and a new northbound M54 to M6 link has been approved that will take thousands of vehicles a day off local A-roads. The A5 and the A442 Queensway carry the rest, all fast roads where works need tight management.",
   "Resurfacing, lining, drainage, lighting, distributor-road work and winter gritting put Telford crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the town's carriageway, distributor-road and winter-maintenance work",
  "s2_intro":"Across Telford's council carriageway and distributor-road work and the National Highways M54 network",
 },
 "newport": {
  "region":"Newport and South East Wales",
  "nearby":["Cardiff","Cwmbran","Caerphilly"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Newport's highway maintenance teams and roadworks contractors, from the city council's roads service to the Welsh Government trunk-road network on the M4 and the Brynglas Tunnels, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep South East Wales's roads running",
  "s1loc":[
   "Newport sits at the gateway between England and South Wales, where the M4 narrows through the twin Brynglas Tunnels, the only bored tunnels on the UK motorway network and the worst pinch point on the Welsh motorway. Newport City Council is the unitary highway authority for around seven hundred kilometres of local road, and its gangs work in Class 3 hi-vis beside that traffic.",
   "The council maintains its network with its own teams backed by the South East and Mid Wales highways framework led by Cardiff, and its Fixing Our Roads programme has resurfaced more than thirty major routes including Chepstow Road, Malpas Road and the A467. The cancelled M4 relief road has left the tunnels as the long-term bottleneck.",
   "The Welsh Government is the roads authority for the motorways and trunk roads, run through the South Wales Trunk Road Agent with Alun Griffiths delivering the Newport corridor in recent years. The M4 and Brynglas Tunnels, the A48 Southern Distributor Road over the Usk and the A449 north all carry heavy traffic where works need very tight management.",
   "Resurfacing, lining, drainage, lighting, structures and winter gritting mean Newport gangs work in hi-vis next to live traffic.",
  ],
  "kit_loc":"across the city's carriageway, lighting and winter-maintenance work",
  "s2_intro":"Across Newport's council carriageway, lighting and drainage work and the Welsh Government trunk-road network",
 },
 "oxford": {
  "region":"Oxford and Oxfordshire",
  "nearby":["Banbury","Abingdon","Witney"],
  "snapshot":"iNeedWorkwear kits Oxford's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from Oxfordshire County Council's Milestone term contract to National Highways work on the A34 and A40, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep Oxfordshire's roads running",
  "s1loc":[
   "Oxford's medieval street pattern and dense colleges squeeze carriageways and restrict when works can run, while five park-and-ride sites feed the city from the ring road. Oxfordshire County Council is the highway authority for more than four thousand eight hundred kilometres of road, and its gangs work in Class 3 hi-vis in tight, busy streets and on fast county roads.",
   "The county runs its highways through a term contract with Milestone, now M Group Highways, worth around eight hundred and forty million pounds to 2033, covering carriageways, footways, cycleways, drainage, structures, winter service and smaller upgrade schemes, delivered by asset-response teams based around Bicester, Banbury, Witney, Abingdon and Didcot.",
   "National Highways carries the A34, the busy trunk route past the city's western edge that jams at the Peartree interchange, and the A40 east to the M40 at Wheatley, with the A44 heading north toward Woodstock. Trunk and park-and-ride corridor work alike mean fast traffic and tight overnight windows.",
   "Resurfacing, lining, drainage, lighting and winter gritting are all handled by Oxford crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the city's carriageway, lighting and winter-maintenance work",
  "s2_intro":"Across Oxford's county carriageway, lighting and drainage work and the National Highways A34 and A40 network",
 },
 "poole": {
  "region":"Poole and East Dorset",
  "nearby":["Bournemouth","Christchurch","Ferndown"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Poole's highway maintenance teams and roadworks contractors, from the BCP Council highways programme to National Highways work on the A35 and A350, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep Poole's roads running",
  "s1loc":[
   "Poole wraps around one of the largest natural harbours in the world, with a working port at Hamworthy and the Twin Sails and Sandbanks crossings shaping how traffic moves. Poole forms part of the BCP Council unitary, the highway authority for around twelve hundred and fifty kilometres of road across the conurbation, and its gangs work in Class 3 hi-vis beside busy harbourside and commuter traffic.",
   "BCP Council runs highway maintenance and civil engineering through a term service contract covering the three towns, with around fifteen million pounds of transport improvements delivered along Ringwood Road in Poole in recent years. Salt spray and tidal flooding on the harbourside roads drive faster carriageway wear than inland.",
   "National Highways carries the A35 west toward Dorchester and the A350 north toward Blandford and the A303, the main freight and commuter routes inland, while the harbour geography forces through-traffic onto a handful of crossings via Holes Bay Road and the Twin Sails lifting bridge. Port-access and trunk work alike mean fast roads and heavy freight.",
   "Resurfacing, lining, drainage, lighting, harbourside work and winter gritting put Poole crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the town's carriageway, harbourside and winter-maintenance work",
  "s2_intro":"Across Poole's council carriageway and harbourside work and the National Highways A35 and A350 network",
 },
 "dundee": {
  "region":"Dundee and Tayside",
  "nearby":["Perth","Arbroath","Glenrothes"],
  "snapshot":"iNeedWorkwear kits Dundee's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from the council's Tayside Contracts partnership to the Transport Scotland network and the Tay Road Bridge, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep Tayside's roads running",
  "s1loc":[
   "Dundee sits on the north bank of the Firth of Tay, linked to Fife by the two-and-a-quarter-kilometre Tay Road Bridge, with the A90 running through the city toward Aberdeen and Perth. Dundee City Council is the Scottish unitary highway authority for around five hundred and fifty kilometres of carriageway, and its gangs work in Class 3 hi-vis beside live traffic.",
   "Road maintenance runs through the Roads Maintenance Partnership with Tayside Contracts, the shared trading arm of the three Tayside councils and the largest civil engineering operation in the area, handling inspections, defect repairs, gully cleaning, lighting and winter service from depots at Claverhouse off the A90. The Tay Road Bridge has just had its full deck replaced.",
   "Transport Scotland is the roads authority for the trunk network, with BEAR Scotland and Amey working the A90 Aberdeen and Perth corridor and the A92 toward Arbroath, while the Tay Road Bridge, carrying the A92, is run by its own joint board. Bridge and trunk work alike mean fast, exposed roads where conspicuity is critical.",
   "Resurfacing, lining, drainage, lighting, bridge work and heavy winter gritting are all handled by Dundee crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the city's carriageway, bridge and winter-maintenance work",
  "s2_intro":"Across Dundee's council carriageway and bridge work and the Transport Scotland trunk-road network",
 },
 "cambridge": {
  "region":"Cambridge and Cambridgeshire",
  "nearby":["Peterborough","Bedford","St Albans"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Cambridge's highway maintenance teams and roadworks contractors, from Cambridgeshire County Council's Milestone partnership to National Highways work on the M11 and A14, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep Cambridgeshire's roads running",
  "s1loc":[
   "Cambridge is one of the fastest-growing cities in England, its historic core and heavy cycle use forcing highway works into tight lane and footway closures. Cambridgeshire County Council is the highway authority for around two thousand seven hundred kilometres of carriageway and over twelve hundred structures, and its gangs work in Class 3 hi-vis beside busy radial traffic.",
   "Maintenance runs through Cambridgeshire Highways, the partnership with Milestone, now M Group Highways, that came across when the business was bought from Skanska, with county highways spending around fifty-eight million pounds a year and a new term contract being procured. Constant development growth adds a steady stream of developer-funded works.",
   "National Highways carries the M11 south to the M25 and the A14 across the top of the city, recently upgraded with a new bypass south of Huntingdon and a viaduct over the Great Ouse, while the billion-pound A428 Black Cat scheme to the west is under construction toward a 2027 opening. Trunk and growth-corridor work alike mean fast traffic and major plant movements.",
   "Resurfacing, lining, drainage, lighting and winter gritting mean Cambridge gangs work in hi-vis next to live traffic.",
  ],
  "kit_loc":"across the city's carriageway, lighting and winter-maintenance work",
  "s2_intro":"Across Cambridge's county carriageway, lighting and drainage work and the National Highways M11 and A14 network",
 },
 "york": {
  "region":"York and North Yorkshire",
  "nearby":["Harrogate","Knaresborough","Selby"],
  "snapshot":"iNeedWorkwear kits York's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from the city council's frameworks to National Highways work on the A64, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep York's roads running",
  "s1loc":[
   "York's Roman walls, cobbled streets and dense scheduled monuments make any excavation in the centre a careful, closely watched job, with heritage setts needing specialist reinstatement. City of York Council is the unitary highway authority for almost eight hundred kilometres of carriageway, and its gangs work in Class 3 hi-vis from the historic core out to the ring road.",
   "The council delivers works through commissioned frameworks, including the Yorkshire Alliance surfacing framework with Colas and a North Yorkshire-led carriageways framework, and has lifted its annual maintenance budget to around sixteen and a half million pounds against a large structural backlog. It is also promoting dualling of the A1237 outer ring road.",
   "National Highways carries the A64, which forms the south-eastern arc of York's outer ring and the main route to the Yorkshire coast, with a dualling of the section east of the city in its longer-term pipeline. The council-maintained A1237 completes the ring, and outer-ring and trunk work alike mean fast traffic and tight management.",
   "Resurfacing, lining, drainage, lighting, heritage paving and winter gritting put York crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the city's carriageway, ring-road and winter-maintenance work",
  "s2_intro":"Across York's council carriageway and ring-road work and the National Highways A64",
 },
 "blackpool": {
  "region":"Blackpool and the Fylde Coast",
  "nearby":["Preston","Lytham St Annes","Poulton-le-Fylde"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Blackpool's highway maintenance teams and roadworks contractors, from the council's Layton depot and works frameworks to National Highways work on the M55, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Fylde Coast's roads running",
  "s1loc":[
   "Blackpool runs the famous Promenade and the only surviving first-generation tramway in Britain, eleven miles of line sharing road space along the seafront from Starr Gate to Fleetwood. Blackpool Council is the unitary highway authority for over three hundred miles of road, and its gangs work in Class 3 hi-vis beside heavy resort traffic and live tram track.",
   "The council mixes in-house teams based at the Layton depot with contracted services, with Enveco running winter gritting as Operation Snowdrop, and it has launched a North West highways framework worth up to two hundred million pounds for surfacing and civils across the region. Seasonal visitor peaks drive heavy wear on the approach roads.",
   "National Highways carries the M55, the twelve-mile motorway linking Blackpool to the M6 at Preston, terminating at junction 4 where it meets the A583 and A5230 into town, while the A585 trunk road runs north to Fleetwood. Promenade and motorway work alike mean fast traffic, tram coordination and exposed coastal conditions.",
   "Resurfacing, lining, drainage, lighting, tramway-corridor work and winter gritting keep Blackpool crews in hi-vis within feet of moving traffic.",
  ],
  "kit_loc":"across the resort's carriageway, promenade and winter-maintenance work",
  "s2_intro":"Across Blackpool's council carriageway and promenade work and the National Highways M55",
 },
 "ipswich": {
  "region":"Ipswich and Suffolk",
  "nearby":["Colchester","Chelmsford","Cambridge"],
  "snapshot":"iNeedWorkwear kits Ipswich's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from Suffolk County Council's Milestone partnership to National Highways work on the A14, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep Suffolk's roads running",
  "s1loc":[
   "Ipswich is the county town of Suffolk and a working port on the Orwell, with the A14 running across it toward Felixstowe, the largest container port in the country. Suffolk County Council is the highway authority through its Suffolk Highways service, and its gangs work in Class 3 hi-vis beside heavy port-bound freight.",
   "Suffolk switched its highways and professional-services contract from Kier to Milestone, now M Group Highways, in 2023 on a partnership worth up to a billion pounds over as long as twenty years, covering roads, pavements, rights of way, drainage, new schemes and winter gritting across the county from depots around the area.",
   "National Highways carries the A14, one of the most freight-intensive corridors in England, and the A12, the two converging at the Seven Hills interchange east of the town, with the Copdock interchange at junction 55 the main gateway between the strategic and local networks. Port-freight and trunk work alike mean fast roads and abnormal loads.",
   "Resurfacing, lining, drainage, lighting and winter gritting are all handled by Ipswich crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the town's carriageway, port-access and winter-maintenance work",
  "s2_intro":"Across Ipswich's county carriageway and port-access work and the National Highways A14",
 },
 "middlesbrough": {
  "region":"Middlesbrough and Teesside",
  "nearby":["Stockton-on-Tees","Hartlepool","Redcar"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Middlesbrough's highway maintenance teams and roadworks contractors, from the council's term contractors to National Highways work on the A19 and A66, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep Teesside's roads running",
  "s1loc":[
   "Middlesbrough sits on the south bank of the Tees in the heart of Teesside, with the A19 crossing the river just to the west on the heavily loaded Tees Viaduct. Middlesbrough Council is the unitary highway authority, running a shared technical and laboratory service for the neighbouring Tees Valley councils, and its gangs work in Class 3 hi-vis beside live traffic.",
   "The council delivers term maintenance through contracted major and minor works lots worth several million pounds a year, supported by Tees Valley Combined Authority resurfacing funding, with its own inspection and materials-testing laboratory serving Stockton, Hartlepool and Redcar and Cleveland as well. It re-procured the term contract in recent years.",
   "National Highways carries the A19 over the Tees Viaduct, which takes over a hundred thousand vehicles a day and is at capacity, prompting work on a new Tees crossing, and the A66 east to Redcar and the Teesworks freeport. Viaduct, freeport and trunk work alike mean fast roads and heavy industrial freight.",
   "Resurfacing, lining, drainage, lighting, structures and winter gritting mean Middlesbrough gangs work in hi-vis next to live traffic.",
  ],
  "kit_loc":"across the town's carriageway, lighting and winter-maintenance work",
  "s2_intro":"Across Middlesbrough's council carriageway, lighting and drainage work and the National Highways A19 and A66 network",
 },
 "gloucester": {
  "region":"Gloucester and Gloucestershire",
  "nearby":["Cheltenham","Bristol","Worcester"],
  "snapshot":"iNeedWorkwear kits Gloucester's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from Gloucestershire County Council's Ringway term contract to National Highways work on the M5 and the A417, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep Gloucestershire's roads running",
  "s1loc":[
   "Gloucester sits on the Severn at the meeting of strategic flows between the Midlands, the South West and Wales, with the M5 running along its western edge. Gloucestershire County Council is the highway authority for the city and county, and its gangs work in Class 3 hi-vis beside motorway-fed traffic and across a Severn floodplain that brings recurring drainage and flood-risk work.",
   "The county runs maintenance through a term contract with Ringway worth around thirty-five million pounds a year, covering defect repairs, drainage, structures and major projects, and is delivering an M5 Junction 10 all-movements upgrade alongside National Highways, with the contract under review for renewal or retender.",
   "National Highways carries the M5 past the city at junctions 11 and 11A, the A40 east to Cheltenham and the A417, where the long-awaited Missing Link dualling between Brockworth and Cowley is under construction by Kier toward a 2027 opening. Motorway and trunk work alike mean fast traffic and major earthworks.",
   "Resurfacing, lining, drainage, lighting, flood work and winter gritting put Gloucester crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the city's carriageway, lighting and winter-maintenance work",
  "s2_intro":"Across Gloucester's county carriageway, lighting and drainage work and the National Highways M5 and A417 network",
 },
 "exeter": {
  "region":"Exeter and Devon",
  "nearby":["Exmouth","Tiverton","Newton Abbot"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Exeter's highway maintenance teams and roadworks contractors, from Devon County Council's Milestone term contract to National Highways work at the M5 terminus, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep Devon's roads running",
  "s1loc":[
   "Exeter is the gateway to the far South West, sitting where the M5 ends and the A30 and A38 carry on into Cornwall and toward Plymouth. Devon County Council, which runs the largest local road network in England at around thirteen thousand kilometres, is the highway authority, and its gangs work in Class 3 hi-vis beside heavy holiday and freight traffic.",
   "The county delivers routine and reactive maintenance through a term contract with Milestone, covering inspections, drainage, resurfacing and emergency call-outs from depots across Devon, and lets separate framework contractors for capital schemes such as the A379 corridor and the South West Exeter growth area.",
   "National Highways carries the M5 to its terminus at junction 31 south of the city, where the A38 Devon Expressway heads for Plymouth and the A30 strikes west into Cornwall, making the junctions 29 to 31 corridor the funnel for all South West Peninsula traffic. Holiday peaks and Atlantic weather make it relentless, fast work.",
   "Resurfacing, lining, drainage, lighting and winter gritting are all handled by Exeter crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the city's carriageway, lighting and winter-maintenance work",
  "s2_intro":"Across Exeter's county carriageway, lighting and drainage work and the National Highways M5 and A30 network",
 },
 "solihull": {
  "region":"Solihull and the West Midlands",
  "nearby":["Birmingham","Coventry","Sutton Coldfield"],
  "snapshot":"iNeedWorkwear kits Solihull's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from the council's joint Balfour Beatty contract to National Highways work on the M42, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep Solihull's roads running",
  "s1loc":[
   "Solihull packs a remarkable density of national infrastructure into one borough, with Birmingham Airport, the NEC, Birmingham Business Park and the planned HS2 interchange all clustered in the M42 box. The metropolitan borough council is the highway authority for the local network, and its gangs work in Class 3 hi-vis beside intense airport, exhibition and construction traffic.",
   "Maintenance runs through the joint contract shared with Coventry and Warwickshire, delivered by Balfour Beatty Living Places across more than five thousand kilometres of road, with a new seven-year deal worth up to nine hundred million pounds from 2026. The council also runs streetlighting and drainage functions through its own operational division.",
   "National Highways carries the M42 through junctions 4 to 7 and the A45, forming the box around the airport and the NEC, with HS2 civil works bringing major overnight and weekend closures of the M42 around junctions 6 and 7 in recent years. Airport-access and HS2 work alike mean fast roads and complex multi-agency staging.",
   "Resurfacing, lining, drainage, lighting, structures and winter gritting mean Solihull gangs work in hi-vis next to live traffic.",
  ],
  "kit_loc":"across the borough's carriageway, lighting and winter-maintenance work",
  "s2_intro":"Across Solihull's council carriageway, lighting and drainage work and the National Highways M42 network",
 },
 "colchester": {
  "region":"Colchester and Essex",
  "nearby":["Chelmsford","Ipswich","Harlow"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Colchester's highway maintenance teams and roadworks contractors, from Essex Highways and its Ringway Jacobs partnership to National Highways work on the A12, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep north Essex's roads running",
  "s1loc":[
   "Colchester, Britain's oldest recorded town and now a city, depends on the A12 and A120 corridor that carries heavy freight for the ports of Harwich and Felixstowe. Essex County Council is the highway authority, and its gangs work in Class 3 hi-vis beside some of the busiest trunk-road freight in the East of England.",
   "Highways are delivered through Essex Highways, the managing-contractor partnership with Ringway Jacobs, covering inspections, repairs, drainage, resurfacing and lighting across the county, with the county procuring a new contract worth around three billion pounds over seven years from 2027. Garrison activity in the town adds abnormal-load movements.",
   "National Highways carries the A12 past the western edge of the town, where the A120 joins at the Marks Tey interchange, a route carrying up to ninety thousand vehicles a day with a high share of port freight, and a widening scheme between junctions 19 and 25 has consent but faces challenge. Trunk and port-freight work alike mean fast roads and tight management.",
   "Resurfacing, lining, drainage, lighting and winter gritting keep Colchester crews in hi-vis within feet of moving traffic.",
  ],
  "kit_loc":"across the city's carriageway, lighting and winter-maintenance work",
  "s2_intro":"Across Colchester's county carriageway, lighting and drainage work and the National Highways A12 corridor",
 },
 "cheltenham": {
  "region":"Cheltenham and Gloucestershire",
  "nearby":["Gloucester","Worcester","Bristol"],
  "snapshot":"iNeedWorkwear kits Cheltenham's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from Gloucestershire County Council's Ringway term contract to National Highways work on the M5 and A40, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep Cheltenham's roads running",
  "s1loc":[
   "Cheltenham is a Regency spa town that hosts GCHQ on its western approach and draws a quarter of a million visitors to its racecourse each March, both shaping how its roads are managed. Gloucestershire County Council is the highway authority, and its gangs work in Class 3 hi-vis beside heavy festival, commuter and government-site traffic.",
   "Maintenance runs through the county's term contract with Ringway, with major junction schemes let separately, Knights Brown rebuilding the Arle Court roundabout and M5 Junction 11 slip and Galliford Try on early works for the big M5 Junction 10 upgrade. The A435 north to Bishop's Cleeve has had a two-phase improvement programme.",
   "National Highways carries the M5 to the west at junctions 10 and 11, with a two-hundred-and-forty-nine-million-pound all-movements upgrade of Junction 10 due to start in 2026, while the A40 runs east to west past GCHQ and the A435 heads north. Racecourse-week and motorway work alike mean fast traffic and large temporary management.",
   "Resurfacing, lining, drainage, lighting and winter gritting are all handled by Cheltenham crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the town's carriageway, lighting and winter-maintenance work",
  "s2_intro":"Across Cheltenham's county carriageway, lighting and drainage work and the National Highways M5 and A40 network",
 },
 "gateshead": {
  "region":"Gateshead and Tyneside",
  "nearby":["Newcastle upon Tyne","Sunderland","South Shields"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Gateshead's highway maintenance teams and roadworks contractors, from the council's in-house teams and the Tyne bridges to National Highways work on the A1 Western Bypass, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep Gateshead's roads running",
  "s1loc":[
   "Gateshead faces Newcastle across one of the densest clusters of river crossings in England, from the Tyne Bridge it co-owns to the High Level, Redheugh and Swing bridges. The metropolitan borough council is the highway authority, and its gangs work in Class 3 hi-vis beside heavy cross-river and MetroCentre traffic, with the A167 Gateshead Highway flyover being demolished after a safety closure.",
   "The council runs highways through in-house inspection teams commissioning works scheme by scheme, with Esh Construction delivering the major Tyne Bridge restoration, the biggest since it was built, jointly with Newcastle and funded through the North East Combined Authority. The A184 Felling Bypass carries the borough's heavy vehicle movements.",
   "National Highways carries the A1 Western Bypass along the western side of the conurbation, one of the busiest roads in the North East, and the A194(M) spur linking the A1 to the A19 and the Tyne Tunnel. Bypass, bridge and flyover work alike mean fast traffic and complex structural staging over the river.",
   "Resurfacing, lining, drainage, lighting, bridges and winter gritting put Gateshead crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the borough's carriageway, bridge and winter-maintenance work",
  "s2_intro":"Across Gateshead's council carriageway and bridge work and the National Highways A1 Western Bypass",
 },
 "high wycombe": {
  "region":"High Wycombe and Buckinghamshire",
  "nearby":["Aylesbury","Slough","Maidenhead"],
  "snapshot":"iNeedWorkwear kits High Wycombe's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from Buckinghamshire Council's Balfour Beatty contract to National Highways work on the M40, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep Buckinghamshire's roads running",
  "s1loc":[
   "High Wycombe sits in a steep Chilterns valley on the M40, with the Handy Cross junction one of the busiest interchanges on the route south of Birmingham. Buckinghamshire Council, the unitary covering the whole county, is the highway authority for over five thousand kilometres of road, and its gangs work in Class 3 hi-vis beside fast motorway-fed traffic.",
   "Maintenance runs through an eight-year term contract worth one hundred and seventy-six million pounds with Balfour Beatty Living Places, with Atkins on the consultancy side and a panel of framework contractors for schemes, run from a county depot at Aylesbury and a base at Cressex near M40 junction 4. The council has trialled in-situ recycling of road material to cut lorry movements.",
   "National Highways oversees the M40 through the Chilterns, managed and maintained under a long concession by Egis, descending through the Stokenchurch cutting and crossing the Wycombe valley on a major structure at junction 3, all in a sensitive protected landscape. The A404 to Maidenhead and the A40 carry the rest of the strategic load.",
   "Resurfacing, lining, drainage, lighting, structures and winter gritting mean High Wycombe gangs work in hi-vis next to live traffic.",
  ],
  "kit_loc":"across the town's carriageway, lighting and winter-maintenance work",
  "s2_intro":"Across High Wycombe's county carriageway, lighting and drainage work and the National Highways M40",
 },
 "blackburn": {
  "region":"Blackburn and East Lancashire",
  "nearby":["Darwen","Burnley","Accrington"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Blackburn's highway maintenance teams and roadworks contractors, from the council's in-house highways operation to National Highways work on the M65, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep East Lancashire's roads running",
  "s1loc":[
   "Blackburn sits at the western end of the M65 where the Pennine moors rise quickly to the east, bringing a long, severe winter season. Blackburn with Darwen is its own unitary highway authority, running its highways largely in-house with a small fleet of gritters, and its gangs work in Class 3 hi-vis on fast, exposed roads.",
   "The council keeps everyday maintenance under direct control, deliberately opening a minor-works framework to local firms working alongside its own teams, with Aggregate Industries appointed for surfacing schemes and a wider infrastructure framework worth up to two hundred and fifty million pounds tendered recently. It runs six gritters on round-the-clock winter standby.",
   "National Highways carries the M65 along the southern and eastern edge of the borough, the main east-west link across East Lancashire toward Preston and the M6 one way and Burnley and Colne the other, with the A666 running south to Bolton and the A677 west. Moorland and motorway work alike mean fast roads and harsh winter conditions.",
   "Resurfacing, lining, drainage, lighting and heavy winter gritting on the Pennine edge are all handled by Blackburn crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the borough's carriageway, moor-road and winter-maintenance work",
  "s2_intro":"Across Blackburn's council carriageway and moor-road work and the National Highways M65",
 },
 "maidstone": {
  "region":"Maidstone and Kent",
  "nearby":["Tonbridge","Tunbridge Wells","Chatham"],
  "snapshot":"iNeedWorkwear kits Maidstone's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from Kent County Council's term contract to National Highways work on the M20 and M2, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep Kent's roads running",
  "s1loc":[
   "Maidstone is the county town of Kent, sitting in the centre of the motorway box formed by the M20 and M2 that carries the nation's cross-Channel freight. Kent County Council, one of the largest highway authorities in England, is responsible for the roads, and its gangs work in Class 3 hi-vis beside heavy international lorry traffic on the A229 and the trunk approaches.",
   "Kent ran its highways with Amey for around a dozen years before signing a new term contract with Ringway from 2026, worth around fifty million pounds a year on an initial fourteen-year term, covering everything from potholes and gritting to bridges and emergency response, from the Aylesford depot just north-west of the town.",
   "National Highways carries the M20 south of Maidstone and the M2 to the north, with the moveable-barrier Operation Brock contraflow held ready on the M20 between junctions 8 and 9 to keep traffic moving when cross-Channel travel is disrupted. The A229 links the two motorways through the town, all routes where works need very tight management.",
   "Resurfacing, lining, drainage, lighting, structures and winter gritting put Maidstone crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the town's carriageway, lighting and winter-maintenance work",
  "s2_intro":"Across Maidstone's county carriageway, lighting and drainage work and the National Highways M20 and M2 network",
 },
 "basingstoke": {
  "region":"Basingstoke and Hampshire",
  "nearby":["Andover","Newbury","Winchester"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Basingstoke's highway maintenance teams and roadworks contractors, from Hampshire County Council's Milestone term contract to National Highways work on the M3, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep north Hampshire's roads running",
  "s1loc":[
   "Basingstoke is built around a 1960s ring road and one of the densest roundabout networks in the country, earning it the nickname Doughnut City, with big distribution parks feeding the A33 and the M3. Hampshire County Council, responsible for over eight thousand five hundred kilometres of carriageway, is the highway authority, and its gangs work in Class 3 hi-vis beside heavy logistics traffic.",
   "Hampshire runs its highways through Milestone under the Hampshire Highways brand, the contract first let to Skanska in 2017 and extended to 2029 after delivering more than three hundred and fifty million pounds of work, with Milestone also on the county's five-hundred-million-pound civils and highways framework. Roundabout surfacing and line marking are a constant workstream.",
   "National Highways carries the M3 along the southern edge through junctions 6 and 7, with the Black Dam roundabout at junction 6 a busy interface between the motorway and the county network, while the A33 runs north-east to Reading and the M4 and the A339 toward Newbury and Alton. Motorway and ring-road work alike mean fast traffic and tight staging.",
   "Resurfacing, lining, drainage, lighting, roundabout work and winter gritting mean Basingstoke gangs work in hi-vis next to live traffic.",
  ],
  "kit_loc":"across the town's carriageway, roundabout and winter-maintenance work",
  "s2_intro":"Across Basingstoke's county carriageway and roundabout work and the National Highways M3",
 },
 "crawley": {
  "region":"Crawley and West Sussex",
  "nearby":["Horsham","Haywards Heath","Redhill"],
  "snapshot":"iNeedWorkwear kits Crawley's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from West Sussex County Council's VolkerHighways contract to National Highways work on the M23 and Gatwick, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep West Sussex's roads running",
  "s1loc":[
   "Crawley is shaped by Gatwick Airport on its northern edge and the Manor Royal business district, one of the largest in the South East, which together drive intense, time-sensitive traffic on the M23 and A23. West Sussex County Council, with around two thousand five hundred miles of road, is the highway authority, and its gangs work in Class 3 hi-vis beside airport-related freight and passenger flows.",
   "West Sussex split its highways work from 2025, with VolkerHighways taking core carriageway maintenance, gritting, structures and markings on a seven-year deal worth around sixteen and a half million pounds a year and FM Conway taking drainage, while Manor Royal improvement schemes run alongside. The county repaired tens of thousands of potholes and resurfaced over a hundred miles in a recent year.",
   "National Highways carries the M23 from the M25 down to Gatwick and Crawley through junctions 9 and 10, a smart-motorway section needing constant monitoring, with the A23 the main parallel route into the town and to Brighton. Gatwick access work runs on overnight closures to protect airport operations, fast work in tight windows.",
   "Resurfacing, lining, drainage, lighting and winter gritting keep Crawley crews in hi-vis within feet of moving traffic.",
  ],
  "kit_loc":"across the town's carriageway, lighting and winter-maintenance work",
  "s2_intro":"Across Crawley's county carriageway, lighting and drainage work and the National Highways M23",
 },
 "chelmsford": {
  "region":"Chelmsford and Essex",
  "nearby":["Basildon","Brentwood","Colchester"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Chelmsford's highway maintenance teams and roadworks contractors, from Essex Highways and its Ringway Jacobs partnership to National Highways work on the A12, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep Essex's roads running",
  "s1loc":[
   "Chelmsford, Essex's only city, sits on the A12 between London and the Haven ports, a corridor where heavy goods vehicles run at roughly double the national share. Essex County Council is the highway authority through its Essex Highways service, and its gangs work in Class 3 hi-vis beside that freight and the busy city distributor roads.",
   "Highways are delivered through Essex Highways, the term partnership with Ringway Jacobs run from a Chelmsford base, covering inspections, repairs, drainage, resurfacing, lighting and a winter fleet of around fifty gritters, with the county now procuring a successor contract worth around two and a half billion pounds from 2027.",
   "National Highways carries the A12 east to west past the city, the dominant trunk route toward Colchester and Felixstowe, now subject to a major widening between junctions 19 and 25, while the A130 runs south to the A127 and A13 and the A138 threads the centre. Trunk and city work alike mean fast traffic and tight management.",
   "Resurfacing, lining, drainage, lighting and winter gritting put Chelmsford crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the city's carriageway, lighting and winter-maintenance work",
  "s2_intro":"Across Chelmsford's county carriageway, lighting and drainage work and the National Highways A12 corridor",
 },
 "preston": {
  "region":"Preston and Lancashire",
  "nearby":["Blackpool","Leyland","Chorley"],
  "snapshot":"iNeedWorkwear kits Preston's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from Lancashire County Council's highways service to National Highways work on the M6, M55 and M65, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep Lancashire's roads running",
  "s1loc":[
   "Preston is Lancashire's county town and the hub of its highways network, sitting where the M6, M55 and M65 meet. Lancashire County Council is the highway authority, running its highways service directly from a depot at Bamber Bridge, and its gangs work in Class 3 hi-vis beside heavy motorway-fed and city traffic.",
   "Lancashire moved to a streamlined single-provider maintenance arrangement across the county in recent years, reporting a sharp fall in road defects and twelve-month guarantees on repairs, while the council itself led the Preston Western Distributor with Costain. The county hub role keeps a heavy maintenance programme running year-round.",
   "National Highways carries the M6 along the eastern edge, the M55 west to Blackpool with a new junction 2 added for the Western Distributor, and the M65 east toward Blackburn and Burnley, with the A59 and the historic A6 as the main radials. Motorway and distributor work alike mean fast roads and tight management.",
   "Resurfacing, lining, drainage, lighting and winter gritting mean Preston gangs work in hi-vis next to live traffic.",
  ],
  "kit_loc":"across the city's carriageway, lighting and winter-maintenance work",
  "s2_intro":"Across Preston's county carriageway, lighting and drainage work and the National Highways motorway network",
 },
 "walthamstow": {
  "region":"Walthamstow and East London",
  "nearby":["Ilford","Enfield","Loughton"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Walthamstow's highway maintenance teams and roadworks contractors, from the London Borough of Waltham Forest to the Transport for London red routes through the area, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep east London's roads running",
  "s1loc":[
   "Walthamstow is the main town of the London Borough of Waltham Forest, with the A406 North Circular skirting its northern fringe and the A12 along the southern edge. The borough council is the highway authority for around four hundred kilometres of local road, and its gangs work in Class 3 hi-vis beside dense, slow-moving urban traffic.",
   "The council runs planned and emergency maintenance and street-works coordination across its non-TfL network, inspecting utility works to the national reinstatement standard, while the A406 and A12 red routes are maintained by Transport for London through its Works for London programme. Borough and red-route teams coordinate closely where local roads feed the North Circular.",
   "The strategic roads here are TfL-operated rather than National Highways, with the A406 North Circular the main orbital corridor between the M11 at Woodford and the A12 at Waterworks Corner, and the M11 itself starting just beyond the borough at junction 4. Red-route and borough work alike mean constant lane management in a tight urban grid.",
   "Resurfacing, lining, drainage, lighting and footway work are all handled by Walthamstow crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the borough's carriageway, lighting and footway work",
  "s2_intro":"Across Walthamstow's borough carriageway and footway work and the Transport for London red-route network",
 },
 "basildon": {
  "region":"Basildon and Essex",
  "nearby":["Chelmsford","Brentwood","Grays Thurrock"],
  "snapshot":"iNeedWorkwear kits Basildon's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from Essex Highways and its Ringway Jacobs partnership to National Highways work on the A127 and A13, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep south Essex's roads running",
  "s1loc":[
   "Basildon is a 1949 new town built on a planned grid between the A127 and the A13, with one of the largest concentrations of advanced manufacturing in the South of England along its enterprise corridor. Essex County Council is the highway authority, and its gangs work in Class 3 hi-vis beside heavy industrial and arterial traffic.",
   "Highways are delivered through Essex Highways, the term partnership with Ringway Jacobs run from Chelmsford, with the county procuring a successor contract worth around two and a half billion pounds from 2027 and Major Road Network funding sought for A127 improvements. The new-town grid roads, built in the 1950s to 1970s, need steady resurfacing.",
   "National Highways and the county share the A127 Southend Arterial Road, one of Britain's first purpose-built arterials and now the backbone of the Basildon enterprise corridor, with the A13 to the south and the A176 linking the town centre to both. Arterial and junction work alike mean fast traffic and heavy freight.",
   "Resurfacing, lining, drainage, lighting and winter gritting keep Basildon crews in hi-vis within feet of moving traffic.",
  ],
  "kit_loc":"across the town's carriageway, grid-road and winter-maintenance work",
  "s2_intro":"Across Basildon's county carriageway and grid-road work and the National Highways A127 and A13 network",
 },
 "dartford": {
  "region":"Dartford and Kent",
  "nearby":["Gravesend","Sidcup","Bromley"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Dartford's highway maintenance teams and roadworks contractors, from Kent County Council's term contract to National Highways and the Dartford Crossing, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep north Kent's roads running",
  "s1loc":[
   "Dartford sits at the Kent end of the Dartford Crossing, the busiest river crossing in the country, where the M25 meets the QEII Bridge and the two Thames tunnels. Kent County Council is the highway authority for the local roads, and its gangs work in Class 3 hi-vis beside relentless crossing-bound freight and commuter traffic.",
   "Kent ran its highways with Amey for around a dozen years before moving to a new term contract with Ringway from 2026, worth around fifty million pounds a year on a long term, covering potholes, gritting, bridges, drainage and emergency response across the county including Dartford. The riverside business parks add heavy goods movements.",
   "National Highways runs the strategic network, with the M25 and the A282 Dartford Crossing the dominant corridor, the QEII Bridge cable stays and the tunnels needing constant overnight maintenance, plus the A2 west to London and the A206 riverside bypass. The crossing is run for National Highways by the Connect Plus consortium, and the planned Lower Thames Crossing will eventually relieve it.",
   "Resurfacing, lining, drainage, lighting and winter gritting are all handled by Dartford crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the town's carriageway, crossing-approach and winter-maintenance work",
  "s2_intro":"Across Dartford's county carriageway and crossing-approach work and the National Highways M25 and Dartford Crossing",
 },
 "bedford": {
  "region":"Bedford and Bedfordshire",
  "nearby":["Milton Keynes","Northampton","Luton"],
  "snapshot":"iNeedWorkwear kits Bedford's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from the borough council's Heidelberg Materials term contract to National Highways work on the A421 and A428, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep Bedfordshire's roads running",
  "s1loc":[
   "Bedford sits on the River Great Ouse and the A421 corridor that carries heavy freight between the Midlands, the Bedford logistics cluster and the East Anglia ports. Bedford Borough Council is the unitary highway authority, and its gangs work in Class 3 hi-vis beside that traffic, with the river floodplain making drainage and culvert work a priority on low-lying roads.",
   "The council re-awarded its term highways maintenance contract to Heidelberg Materials in 2025, a five-year deal worth around thirty million pounds covering resurfacing, drainage, kerb and ironwork and minor bridge repairs, building on a relationship that dates back over a decade. Annual highways investment has run above twenty million pounds across recent years.",
   "National Highways carries the A421 east to west, linking Bedford to the M1 at junction 13 and the A1 at the Black Cat, where the billion-pound A428 Black Cat to Caxton Gibbet scheme is building a three-level junction and ten miles of new dual carriageway toward a 2027 opening. The A6 runs north to south through the town as the main local spine.",
   "Resurfacing, lining, drainage, lighting and winter gritting put Bedford crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the borough's carriageway, lighting and winter-maintenance work",
  "s2_intro":"Across Bedford's council carriageway, lighting and drainage work and the National Highways A421 and A428 network",
 },
 "doncaster": {
  "region":"Doncaster and South Yorkshire",
  "nearby":["Sheffield","Rotherham","Barnsley"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Doncaster's highway maintenance teams and roadworks contractors, from the city council's highways framework to National Highways work on the A1(M), M18 and M180, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Doncaster area's roads running",
  "s1loc":[
   "Doncaster is a major freight and logistics hub in South Yorkshire, sitting where the A1(M), M18 and M180 meet around the iPort rail terminal at Rossington. The City of Doncaster Council is the metropolitan highway authority, and its gangs work in Class 3 hi-vis beside intense heavy goods traffic.",
   "The council delivers capital works through a multi-lot highways construction framework worth up to one hundred and fifty-five million pounds across resurfacing, civils, public realm and lighting, running its reactive maintenance through its own operation. The iPort, which handles the country's longest freight trains, drives sustained surfacing demand on the eastern network.",
   "National Highways carries the A1(M) along the western edge through junctions 36 to 38, the M18 to the east toward the iPort and the closed Doncaster Sheffield Airport, and the M180 to the Humber ports, with the A630 through the town centre. Motorway-interchange work alike means fast roads and heavy freight.",
   "Resurfacing, lining, drainage, lighting and winter gritting mean Doncaster gangs work in hi-vis next to live traffic.",
  ],
  "kit_loc":"across the borough's carriageway, lighting and winter-maintenance work",
  "s2_intro":"Across Doncaster's council carriageway, lighting and drainage work and the National Highways A1(M), M18 and M180 network",
 },
 "worthing": {
  "region":"Worthing and West Sussex",
  "nearby":["Brighton","Littlehampton","Shoreham-by-Sea"],
  "snapshot":"iNeedWorkwear kits Worthing's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from West Sussex County Council's VolkerHighways contract to National Highways work on the A27, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the West Sussex coast's roads running",
  "s1loc":[
   "Worthing runs along the West Sussex coast beneath the South Downs, with the A27 trunk road squeezed across its northern edge as a well-known congestion pinch point. West Sussex County Council is the highway authority, and its gangs work in Class 3 hi-vis beside busy coastal and through traffic.",
   "West Sussex split its highways work from 2025, with VolkerHighways taking core carriageway maintenance, gritting, structures and markings on a seven-year deal and FM Conway taking drainage. The planned A27 Worthing and Lancing improvement was cancelled in 2024, so the existing dual carriageway carries trunk traffic with no capacity uplift in prospect.",
   "National Highways carries the A27 along the top of the town toward Brighton and Chichester, while the A24 runs north from the Grove Lodge roundabout toward Horsham and the A259 is the coastal seafront route. Seafront salt spray and the A27 pinch point alike keep maintenance demanding.",
   "Resurfacing, lining, drainage, lighting, seafront work and winter gritting put Worthing crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the town's carriageway, seafront and winter-maintenance work",
  "s2_intro":"Across Worthing's county carriageway and seafront work and the National Highways A27 corridor",
 },
 "rotherham": {
  "region":"Rotherham and South Yorkshire",
  "nearby":["Sheffield","Doncaster","Mexborough"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Rotherham's highway maintenance teams and roadworks contractors, from the council's in-house highways team to National Highways work on the M1 and M18, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Rotherham area's roads running",
  "s1loc":[
   "Rotherham sits between Sheffield and the M1, home to the Advanced Manufacturing Park at Waverley where Boeing, the AMRC and Nuclear AMRC cluster on former colliery land. Rotherham Metropolitan Borough Council is the highway authority, and its gangs work in Class 3 hi-vis beside heavy manufacturing and motorway-fed traffic.",
   "The council delivers day-to-day maintenance through its in-house highways team, commissioning the external market for capital resurfacing, with a twelve-million-pound annual capital programme and a total of fifty-five million pounds across the decade to 2028. The A630 Parkway was upgraded to a dual three-lane road serving the manufacturing park and M1 junction 33.",
   "National Highways carries the M1 through the western borough at junctions 33 to 35 and the M18 beginning to the east toward Doncaster, with the A630 Sheffield Parkway, the A633 and A6178 as the main local corridors toward Mexborough and Barnsley. Motorway and parkway work alike mean fast roads and heavy freight.",
   "Resurfacing, lining, drainage, lighting and winter gritting are all handled by Rotherham crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the borough's carriageway, lighting and winter-maintenance work",
  "s2_intro":"Across Rotherham's council carriageway, lighting and drainage work and the National Highways M1 and M18 network",
 },
 "mansfield": {
  "region":"Mansfield and Nottinghamshire",
  "nearby":["Sutton-in-Ashfield","Nottingham","Chesterfield"],
  "snapshot":"iNeedWorkwear kits Mansfield's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from Nottinghamshire's Via East Midlands to National Highways work on the M1 corridor, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Mansfield area's roads running",
  "s1loc":[
   "Mansfield sits at the centre of the former Nottinghamshire coalfield, on a network of purpose-built colliery access and connector roads now carrying logistics and commuter traffic. Nottinghamshire County Council is the highway authority, and its gangs work in Class 3 hi-vis beside that traffic across the Mansfield and Ashfield towns.",
   "Highways are delivered by Via East Midlands, the company wholly owned by the county council, handling resurfacing, drainage, signs, lighting, signals, salting and bridges from the Bilsthorpe depot on a county programme that has run to around sixty-six million pounds a year. The coalfield-era roads, built for coal lorries, now take changed traffic loads.",
   "National Highways runs the M1 around seven miles west through junctions 27 and 28, with the A38 and the Mansfield and Ashfield Regeneration Route linking the towns to the motorway, the A60 the main north-south spine and the A617 east to Newark. Regeneration-route and trunk-access work alike keep crews on fast roads.",
   "Resurfacing, lining, drainage, lighting and winter gritting mean Mansfield gangs work in hi-vis next to live traffic.",
  ],
  "kit_loc":"across the area's carriageway, lighting and winter-maintenance work",
  "s2_intro":"Across Mansfield's county carriageway, lighting and drainage work and the National Highways M1 corridor",
 },
 "eastbourne": {
  "region":"Eastbourne and East Sussex",
  "nearby":["Brighton","Hastings","Hailsham"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Eastbourne's highway maintenance teams and roadworks contractors, from East Sussex County Council's Balfour Beatty contract to National Highways work on the A27 and A22, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the East Sussex coast's roads running",
  "s1loc":[
   "Eastbourne sits between the South Downs and the Channel, a major south-coast resort with a seafront network exposed to coastal weather and the chalk-downland approaches to Beachy Head. East Sussex County Council is the highway authority, and its gangs work in Class 3 hi-vis beside busy resort and through traffic.",
   "East Sussex moved from Costain to Balfour Beatty Living Places in 2023 on a seven-year contract worth two hundred and ninety-seven million pounds, run from a county control hub and covering roads, drainage, lighting, signals, bridges and winter service, with a recent programme funding resurfacing of Terminus Road in the town centre. Coastal exposure drives faster wear on the seafront.",
   "National Highways carries the A27 along the northern fringe toward Brighton and Lewes, the only such trunk route south of the M25, and the A22 north through Polegate toward the M25, with the council-maintained A259 seafront and coast road. Bypass and seafront work alike mean live traffic and tight management.",
   "Resurfacing, lining, drainage, lighting, seafront work and winter gritting keep Eastbourne crews in hi-vis within feet of moving traffic.",
  ],
  "kit_loc":"across the town's carriageway, seafront and winter-maintenance work",
  "s2_intro":"Across Eastbourne's county carriageway and seafront work and the National Highways A27 and A22 network",
 },
 "oldham": {
  "region":"Oldham and Greater Manchester",
  "nearby":["Manchester","Rochdale","Ashton-under-Lyne"],
  "snapshot":"iNeedWorkwear kits Oldham's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from the council's in-house highways service to National Highways work on the M60 and A627(M), with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Oldham area's roads running",
  "s1loc":[
   "Oldham climbs from the Greater Manchester conurbation onto the Pennine fringe toward Saddleworth, with the Metrolink tram running through the town centre. Oldham Council is the highway authority, and its gangs work in Class 3 hi-vis on roads with the gradient, drainage and frost demands of upland Greater Manchester.",
   "The council brought its highways management back in-house from the former Unity Partnership with Kier, now running the network directly and engaging specialist contractors through frameworks, including a planned strategic partnership for highway improvements, and refurbishing the Manchester Street viaduct with combined-authority transport funding.",
   "National Highways carries the M60 orbital to the south and west through junctions 21 to 24 and the A627(M) spur linking Chadderton and the M62 toward Rochdale, with the A663 and A62 as the main local corridors. The M60 and M62 interchange congestion and the Pennine winter alike keep crews busy on fast roads.",
   "Resurfacing, lining, drainage, lighting, tram-corridor work and winter gritting are all handled by Oldham crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the borough's carriageway, tram-corridor and winter-maintenance work",
  "s2_intro":"Across Oldham's council carriageway and tram-corridor work and the National Highways M60 and A627(M) network",
 },
 "wigan": {
  "region":"Wigan and Greater Manchester",
  "nearby":["Bolton","Leigh","St Helens"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Wigan's highway maintenance teams and roadworks contractors, from the council's in-house highways team to National Highways work on the M6 and M58, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Wigan area's roads running",
  "s1loc":[
   "Wigan sits at a strategic point on the national motorway network in the south-west of Greater Manchester, where the M6 runs north to south through the borough. Wigan Council is the highway authority, running an award-winning in-house highways model, and its gangs work in Class 3 hi-vis beside heavy motorway-fed freight.",
   "Rather than a single term contractor, the council delivers through its in-house team and specialist frameworks, with Colas on footway sealing, Tarmac and J Hopkins on resurfacing and Casey and Bethell on major schemes, and is developing an M58 Link Road to connect the motorway interchange to the A49 into town.",
   "National Highways carries the M6 through junctions 25 to 27, recently upgraded to all-lane running between junctions 21a and 26, and the M58 connecting to Merseyside at junction 26, with the A49 the main local spine. Smart-motorway and link-road work alike mean fast roads and heavy freight.",
   "Resurfacing, lining, drainage, lighting and winter gritting put Wigan crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the borough's carriageway, lighting and winter-maintenance work",
  "s2_intro":"Across Wigan's council carriageway, lighting and drainage work and the National Highways M6 and M58 network",
 },
 "sutton coldfield": {
  "region":"Sutton Coldfield and the West Midlands",
  "nearby":["Birmingham","Lichfield","Tamworth"],
  "snapshot":"iNeedWorkwear kits Sutton Coldfield's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from the Birmingham highways PFI with Kier to National Highways work on the M6 Toll and A38, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep Sutton Coldfield's roads running",
  "s1loc":[
   "Sutton Coldfield is a large town at the northern edge of Birmingham, wrapped around the ancient parkland of Sutton Park and carrying through traffic between the city and Lichfield. Birmingham City Council is the highway authority, and its gangs work in Class 3 hi-vis beside the A38 bypass and the busy town-centre corridors.",
   "Maintenance here is part of Birmingham's citywide highways PFI covering some 2,500 kilometres of carriageway, delivered by Kier since 2020 after the original contractor exited, with the long-term contract still being resolved between the council and government. Sutton Coldfield's roads are maintained as part of that one large city operation.",
   "National Highways carries the M6 Toll around the north and east, with junctions onto the A38 Sutton Coldfield bypass and the M42 at Minworth, while the former trunk route through the town is now the A5127 Lichfield Road. Toll-motorway and bypass work alike mean fast roads and heavy freight from the Minworth logistics area.",
   "Resurfacing, lining, drainage, lighting and winter gritting mean Sutton Coldfield gangs work in hi-vis next to live traffic.",
  ],
  "kit_loc":"across the town's carriageway, lighting and winter-maintenance work",
  "s2_intro":"Across Sutton Coldfield's council carriageway, lighting and drainage work and the National Highways M6 Toll and A38 network",
 },
 "lincoln": {
  "region":"Lincoln and Lincolnshire",
  "nearby":["Newark","Gainsborough","Grantham"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Lincoln's highway maintenance teams and roadworks contractors, from Lincolnshire County Council's Balfour Beatty contract to National Highways work on the A46, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep Lincolnshire's roads running",
  "s1loc":[
   "Lincoln is the county city of a large rural shire, its cathedral set atop a steep limestone hill above a historic core where any dig is closely watched. Lincolnshire County Council is the highway authority for around nine thousand kilometres of road, and its gangs work in Class 3 hi-vis from the steep Cathedral Quarter out to the bypass.",
   "Balfour Beatty Living Places holds the county term contract, awarded in 2020 and extended in 2023 to around 2032 for a combined commitment near five hundred and forty-seven million pounds, run from depots across Lincolnshire with an operational control hub, and it is also building the North Hykeham Relief Road from 2026.",
   "National Highways carries the A46 around the south and west of the city as a bypass linking toward Newark and the A1, with the A15 running through Lincoln north to south, and the council-built Lincoln Eastern Bypass having relieved the city centre when it opened in 2020. Bypass and city work alike mean fast traffic and tight historic-core management.",
   "Resurfacing, lining, drainage, lighting and winter gritting put Lincoln crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the city's carriageway, lighting and winter-maintenance work",
  "s2_intro":"Across Lincoln's county carriageway, lighting and drainage work and the National Highways A46",
 },
 "worcester": {
  "region":"Worcester and Worcestershire",
  "nearby":["Bromsgrove","Droitwich","Malvern"],
  "snapshot":"iNeedWorkwear kits Worcester's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from Worcestershire County Council's Ringway contract to National Highways work on the M5, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep Worcestershire's roads running",
  "s1loc":[
   "Worcester sits on the River Severn beside the M5, its city-centre crossings long carrying through traffic until the new southern link relieved them. Worcestershire County Council is the highway authority for around four thousand kilometres of road, and its gangs work in Class 3 hi-vis beside motorway-fed and city traffic.",
   "Ringway has run the county term maintenance contract since 2005, extended to 2025 at around twenty to thirty million pounds a year, with the major infrastructure-engineering contract transitioning to Alun Griffiths from mid-2025, the latter having built the A4440 Southern Link Road and its new Carrington Bridge over the Severn.",
   "National Highways carries the M5 to the west through junctions 6 and 7, with the A44 east to Evesham, the A38 north to Droitwich and the A4440 Worcester Southern Link Road, now dualled, carrying over thirty thousand vehicles a day around the south of the city. Motorway and link-road work alike mean fast roads and tight management.",
   "Resurfacing, lining, drainage, lighting and winter gritting are all handled by Worcester crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the city's carriageway, lighting and winter-maintenance work",
  "s2_intro":"Across Worcester's county carriageway, lighting and drainage work and the National Highways M5 corridor",
 },
 "salford": {
  "region":"Salford and Greater Manchester",
  "nearby":["Manchester","Bolton","Stretford"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Salford's highway maintenance teams and roadworks contractors, from the council's highways works framework to National Highways work on the M60 and M602, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Salford area's roads running",
  "s1loc":[
   "Salford runs from MediaCityUK at the Quays out along the A580 East Lancashire Road, with the M60 and M602 carrying enormous daily flows on its margins. Salford City Council is the metropolitan highway authority, and its gangs work in Class 3 hi-vis beside some of the busiest motorway sections in the North West.",
   "The council delivers works through a technical and highways works framework of around nineteen contractors across civils, structures and drainage, refreshed for 2026, alongside the Greater Manchester authorities' shared maintenance framework, and resurfaces the heavily used A580 in successive programmes.",
   "National Highways carries the M60 orbital through the Eccles Interchange at junctions 12 and 13, among the highest-volume on the whole ring, and the M602 spur into Salford and the Quays, with the A580 East Lancashire Road and the A57 as the main arterials. Interchange and arterial work alike mean fast roads and heavy lorry flows.",
   "Resurfacing, lining, drainage, lighting and winter gritting mean Salford gangs work in hi-vis next to live traffic.",
  ],
  "kit_loc":"across the city's carriageway, lighting and winter-maintenance work",
  "s2_intro":"Across Salford's council carriageway, lighting and drainage work and the National Highways M60 and M602 network",
 },
 "st helens": {
  "region":"St Helens and Merseyside",
  "nearby":["Liverpool","Warrington","Wigan"],
  "snapshot":"iNeedWorkwear kits St Helens's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from the council's in-house team and the Liverpool City Region framework to National Highways work on the M6 and M62, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the St Helens area's roads running",
  "s1loc":[
   "St Helens, the home of Pilkington glass since 1826, sits between the M6 and M62 in the Liverpool City Region, its Cowley Hill works and logistics estates driving heavy goods traffic. St Helens Borough Council is the highway authority, and its gangs work in Class 3 hi-vis beside that freight.",
   "Most routine repairs are done by the council's in-house team from the Hardshaw Brook depot, including a Multihog first-fix vehicle to cut reliance on patching contractors, while planned capital works run through the eight-hundred-and-fifty-million-pound Liverpool City Region planned-works framework with Merseyside firms such as Huyton Asphalt Civils and Dowhigh.",
   "National Highways carries the M6 through the east of the borough at junctions 23 and 24, recently upgraded to all-lane running, and the M62 along the north at junction 7, where the A570 St Helens Linkway runs into town, with the A58 the main local spine. Smart-motorway and linkway work alike mean fast roads and heavy freight.",
   "Resurfacing, lining, drainage, lighting and winter gritting put St Helens crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the borough's carriageway, lighting and winter-maintenance work",
  "s2_intro":"Across St Helens's council carriageway, lighting and drainage work and the National Highways M6 and M62 network",
 },
 "wembley": {
  "region":"Wembley and North West London",
  "nearby":["Harrow","Edgware","Barnet"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Wembley's highway maintenance teams and roadworks contractors, from the London Borough of Brent to the Transport for London red routes and stadium event traffic, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Wembley area's roads running",
  "s1loc":[
   "Wembley, in the London Borough of Brent, is built around one of the busiest event venues in Europe, where ninety-thousand-capacity crowds turn the road network into a managed event space on match and concert days. Brent Council is the highway authority for the borough roads, and its gangs work in Class 3 hi-vis beside dense urban and event traffic.",
   "Brent runs its local network through term contractors O'Hara Bros and GW Highways on seven-year deals from 2023, with Marlborough Highways on footway and public-realm schemes, while Transport for London maintains the A406 North Circular and A404 red routes through Works for London. Event days bring planned closures of Engineers Way, South Way and Empire Way.",
   "The A406 North Circular along the eastern side is TfL-operated and jams from mid-afternoon on event days, with the A404 Harrow Road another red route and the M1 starting at Staples Corner in Brent as a relief valve. Event-day and red-route work alike mean constant temporary management and signing.",
   "Resurfacing, lining, drainage, lighting and event-day management are all handled by Wembley crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the area's carriageway, event-route and lighting work",
  "s2_intro":"Across Wembley's borough carriageway and event-route work and the Transport for London red-route network",
 },
 "hemel hempstead": {
  "region":"Hemel Hempstead and Hertfordshire",
  "nearby":["Watford","St Albans","Berkhamsted"],
  "snapshot":"iNeedWorkwear kits Hemel Hempstead's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from Hertfordshire's Ringway contract to National Highways work on the M1 and M25, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep west Hertfordshire's roads running",
  "s1loc":[
   "Hemel Hempstead is a postwar new town where M1 junction 8 and M25 junction 20 sit within a few kilometres, feeding the huge Maylands logistics cluster and its twenty thousand workers. Hertfordshire County Council is the highway authority, and its gangs work in Class 3 hi-vis beside heavy distribution traffic, with the Plough Magic Roundabout of six mini-roundabouts at the centre.",
   "Hertfordshire renewed its term contract with Ringway from 2025 at a minimum of fifty-five million pounds a year on a long term, covering over five thousand kilometres of road, pothole repair, lighting, signals, gritting and improvement schemes county-wide, with a Hertfordshire-based supply chain built into the deal.",
   "National Highways carries the M1 at junction 8 and the M25 at junction 20 within a short distance of the town, with the A41 dual carriageway toward Watford and Aylesbury and the A414 to St Albans. Motorway-junction and A41 work alike mean fast roads and heavy logistics freight.",
   "Resurfacing, lining, drainage, lighting, roundabout work and winter gritting mean Hemel Hempstead gangs work in hi-vis next to live traffic.",
  ],
  "kit_loc":"across the town's carriageway, roundabout and winter-maintenance work",
  "s2_intro":"Across Hemel Hempstead's county carriageway and roundabout work and the National Highways M1 and M25 network",
 },
 "watford": {
  "region":"Watford and Hertfordshire",
  "nearby":["St Albans","Hemel Hempstead","Bushey"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Watford's highway maintenance teams and roadworks contractors, from Hertfordshire's Ringway contract to National Highways work on the M1 and M25, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Watford area's roads running",
  "s1loc":[
   "Watford sits where the M1 and M25 converge within a few miles, making it one of the highest-traffic maintenance zones in Hertfordshire, with the Berrygrove interchange merging fourteen lanes onto shared transitions. Hertfordshire County Council is the highway authority, and its gangs work in Class 3 hi-vis beside that motorway-fed traffic.",
   "Hertfordshire runs its highways through Ringway, retained from 2025 on a long term worth at least fifty-five million pounds a year, with a joint county and Watford member panel setting local scheme priorities and the A41 corridor carrying heavy aggregate and construction supply traffic to and from the M25.",
   "National Highways carries the M1 at junction 5 Berrygrove and the M25 at junctions 19 and 20 around the borough, with the A41 dual carriageway northwest toward Hemel Hempstead and the A405 North Orbital linking the two motorways. Interchange and A41 work alike mean fast roads and heavy freight.",
   "Resurfacing, lining, drainage, lighting and winter gritting are all handled by Watford crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the borough's carriageway, lighting and winter-maintenance work",
  "s2_intro":"Across Watford's county carriageway, lighting and drainage work and the National Highways M1 and M25 network",
 },
 "stockport": {
  "region":"Stockport and Greater Manchester",
  "nearby":["Manchester","Altrincham","Wilmslow"],
  "snapshot":"iNeedWorkwear kits Stockport's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from the STaR framework with George Cox and Tarmac to National Highways work on the M60, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Stockport area's roads running",
  "s1loc":[
   "Stockport sits where the M60 orbital meets the A6 corridor to the Peak District, beneath the Grade II-star railway viaduct that strides over the motorway and the Mersey valley. Stockport Metropolitan Borough Council is the highway authority, and its gangs work in Class 3 hi-vis beside heavy orbital and radial traffic.",
   "Maintenance is delivered through the STaR Procurement framework shared with neighbouring boroughs, with George Cox and Sons as principal civils contractor and Tarmac on surfacing, running fifty to seventy schemes a year, and the council has invested in drainage and maintenance on the A555 Manchester Airport relief road.",
   "National Highways carries the M60 through the east of the borough at junctions 25 to 27, with the A6 the main radial to Hazel Grove and the Pennines, the A34 south to Cheadle and Wilmslow and the A555 relief road to the airport. Viaduct and motorway work alike mean fast roads and complex multi-agency staging, as when the M60 closed for the viaduct restoration.",
   "Resurfacing, lining, drainage, lighting and winter gritting put Stockport crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the borough's carriageway, lighting and winter-maintenance work",
  "s2_intro":"Across Stockport's council carriageway, lighting and drainage work and the National Highways M60",
 },
 "rochdale": {
  "region":"Rochdale and Greater Manchester",
  "nearby":["Oldham","Bury","Heywood"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Rochdale's highway maintenance teams and roadworks contractors, from the council's in-house operation to National Highways work on the M62 and A627(M), with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Rochdale area's roads running",
  "s1loc":[
   "Rochdale sits on the western Pennine edge of Greater Manchester, where the M62 climbs toward its high point near the Yorkshire boundary and the Metrolink tram runs on-street through the town centre. Rochdale Borough Council is the highway authority, and its gangs work in Class 3 hi-vis on roads that face the most severe winters in the conurbation.",
   "The council brought highway maintenance back in-house in 2022 when Balfour Beatty's contract ended, one of few metropolitan boroughs to run direct delivery for potholes, gritting, drainage and resurfacing, with a revenue support framework worth up to around twenty-eight million pounds backing the in-house team from 2026.",
   "National Highways carries the M62 through the south of the borough at junctions 20 and 21 and the A627(M) spur linking Chadderton to the M62 at junction 20, with the A58 and A664 the main local routes to Halifax, Bury and Oldham. Trans-Pennine and spur work alike mean fast roads and demanding winter gritting from the Princess Street depot.",
   "Resurfacing, lining, drainage, lighting, tram-corridor work and heavy winter gritting mean Rochdale gangs work in hi-vis next to live traffic.",
  ],
  "kit_loc":"across the borough's carriageway, tram-corridor and winter-maintenance work",
  "s2_intro":"Across Rochdale's council carriageway and tram-corridor work and the National Highways M62 and A627(M) network",
 },
 "hove": {
  "region":"Hove and the Sussex coast",
  "nearby":["Brighton","Worthing","Shoreham-by-Sea"],
  "snapshot":"iNeedWorkwear kits Hove's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from Brighton and Hove City Council's FM Conway framework to National Highways work on the A27, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Hove seafront's roads running",
  "s1loc":[
   "Hove forms the western half of the Brighton and Hove unitary, a seafront city carrying an unusual stock of coastal structures including the highway arches beneath King's Road and Grand Junction Road. Brighton and Hove City Council is the sole highway authority, and its gangs work in Class 3 hi-vis beside busy seafront and city traffic.",
   "The council runs a multi-supplier highways framework with FM Conway, now part of VINCI, holding the main civils and resurfacing lot alongside Edburton and RJ Dance, maintaining the carriageways, footways and a heavy set of seafront structures, with a major arches renewal programme bid to government in a salt-laden coastal setting.",
   "National Highways carries the A27 Brighton and Shoreham bypass along the northern edge of the city and the A23 north toward the M23, while the A259 coast road and the A2023 are the main council corridors through Hove. Bypass and seafront work alike mean live traffic and demanding coastal maintenance.",
   "Resurfacing, lining, drainage, lighting, seafront structures and winter gritting are all handled by Hove crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the city's carriageway, seafront and winter-maintenance work",
  "s2_intro":"Across Hove's council carriageway and seafront work and the National Highways A27 corridor",
 },
 "ilford": {
  "region":"Ilford and East London",
  "nearby":["Romford","Walthamstow","Barnet"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Ilford's highway maintenance teams and roadworks contractors, from the London Borough of Redbridge and its Kenson partnership to the Transport for London red routes, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Ilford area's roads running",
  "s1loc":[
   "Ilford is the principal town of the London Borough of Redbridge, on the Elizabeth line corridor where the A406 North Circular meets the A12 at the Redbridge Roundabout. The borough council is the highway authority for the local roads, and its gangs work in Class 3 hi-vis beside dense east-London traffic.",
   "Redbridge works with Kenson Highways as its principal maintenance and resurfacing contractor, recently resurfacing over seventy-five roads in a six-million-pound programme using low-carbon asphalt, while Transport for London maintains the A406 and A12 red routes and funds junction schemes such as Ilford Green through the Works for London framework.",
   "The A406 North Circular and A12 Eastern Avenue through the area are TfL-operated red routes, the North Circular crossing the River Roding on a viaduct to meet the A12 at the grade-separated Redbridge Roundabout, with the A118 the main borough high-road corridor. Red-route and town-centre work alike mean constant lane management.",
   "Resurfacing, lining, drainage, lighting and footway work keep Ilford crews in hi-vis within feet of moving traffic.",
  ],
  "kit_loc":"across the borough's carriageway, lighting and footway work",
  "s2_intro":"Across Ilford's borough carriageway and footway work and the Transport for London red-route network",
 },
 "barnsley": {
  "region":"Barnsley and South Yorkshire",
  "nearby":["Sheffield","Rotherham","Doncaster"],
  "snapshot":"iNeedWorkwear kits Barnsley's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from the council's in-house direct labour to National Highways work on the M1 and A628, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Barnsley area's roads running",
  "s1loc":[
   "Barnsley sits at the northern edge of the former South Yorkshire coalfield between Sheffield and the Pennines, with the Dearne Valley Parkway built to regenerate former colliery land. Barnsley Metropolitan Borough Council is the highway authority, and its gangs work in Class 3 hi-vis beside heavy logistics traffic from the M1-side distribution parks.",
   "The council runs a predominantly in-house direct labour model for day-to-day maintenance, lighting and traffic engineering, bringing in specialist contractors for surface dressing and barriers, with an eighteen-million-pound capital programme covering over a hundred sites a year.",
   "National Highways carries the M1 along the eastern edge at junctions 36 to 38 and the A628 trans-Pennine route west over the Woodhead Pass, one of the most demanding high roads in England, with the A61 the main spine and the A6195 Dearne Valley Parkway serving the logistics parks. Woodhead and motorway work alike mean fast roads and severe winters.",
   "Resurfacing, lining, drainage, lighting and winter gritting put Barnsley crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the borough's carriageway, lighting and winter-maintenance work",
  "s2_intro":"Across Barnsley's council carriageway, lighting and drainage work and the National Highways M1 and A628 network",
 },
 "darlington": {
  "region":"Darlington and the Tees Valley",
  "nearby":["Hartlepool","Middlesbrough","Newton Aycliffe"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Darlington's highway maintenance teams and roadworks contractors, from the borough council's highways teams to National Highways work on the A1(M) and A66, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Darlington area's roads running",
  "s1loc":[
   "Darlington, the birthplace of the mainline railway, sits where the A1(M) and the A66 trans-Pennine route converge in the Tees Valley. Darlington Borough Council is the unitary highway authority for the roads, bridges and retaining walls of the town, and its gangs work in Class 3 hi-vis beside strategic freight and commuter traffic.",
   "The council manages highways through in-house design and network teams with externally tendered works for resurfacing and reconstruction, on a maintenance budget around three million pounds a year topped up by Tees Valley and government grants, using the shared Tees Valley Highways Design Guide and maintaining over a hundred road bridges.",
   "National Highways carries the A1(M) along the eastern bypass through junctions 56 to 59 and the A66 west toward Scotch Corner and the M6, where the billion-pound A66 Northern Trans-Pennine dualling is consented, while the planned Darlington Northern Link Road will tie the A66 to the A1(M). Bypass and trans-Pennine work alike mean fast roads and major schemes.",
   "Resurfacing, lining, drainage, lighting and winter gritting are all handled by Darlington crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the town's carriageway, lighting and winter-maintenance work",
  "s2_intro":"Across Darlington's council carriageway, lighting and drainage work and the National Highways A1(M) and A66 network",
 },
 "hartlepool": {
  "region":"Hartlepool and the Tees Valley",
  "nearby":["Darlington","Middlesbrough","Stockton-on-Tees"],
  "snapshot":"iNeedWorkwear kits Hartlepool's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from the borough council's highways teams to National Highways work on the A19 and A689, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Hartlepool area's roads running",
  "s1loc":[
   "Hartlepool is a North Sea port on a peninsula north of the Tees, where all major access runs through the A179 and A689 junctions with the A19. Hartlepool Borough Council is the unitary highway authority for over four hundred kilometres of road, and its gangs work in Class 3 hi-vis beside port and industrial traffic.",
   "The council manages a Transport Asset Management Plan across the network with a five-year maintenance programme of dozens of schemes a year, delivered through tendered packages and regional frameworks, while PD Ports and the Teesside Freeport designation drive growing logistics traffic on the approach roads.",
   "National Highways carries the A19 to the west, the main connector between Tyneside and Teesside, with the A179 the northern approach and the A689 the port and industrial route to Stockton, now backed by fifty million pounds of Tees Valley funding for widening and signals. A19-diversion and port work alike mean fast roads and heavy freight on a network with few alternatives.",
   "Resurfacing, lining, drainage, lighting and winter gritting put Hartlepool crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the town's carriageway, port-access and winter-maintenance work",
  "s2_intro":"Across Hartlepool's council carriageway and port-access work and the National Highways A19 and A689 network",
 },
 "hastings": {
  "region":"Hastings and East Sussex",
  "nearby":["Bexhill-on-Sea","Eastbourne","Hailsham"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Hastings's highway maintenance teams and roadworks contractors, from East Sussex County Council's Balfour Beatty contract to National Highways work on the A21, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Hastings coast's roads running",
  "s1loc":[
   "Hastings has a steep coastal topography, the Old Town and Stade fishing quarter wedged between sandstone cliffs served by funicular railways. East Sussex County Council is the highway authority, and its gangs work in Class 3 hi-vis beside seafront, hill and through traffic in a constrained network of narrow streets and gradients.",
   "East Sussex runs its highways through Balfour Beatty Living Places on a seven-year contract from 2023 worth two hundred and ninety-seven million pounds, covering roads, drainage, lighting, signals and bridges from a county control hub, with the A259 seafront and the Combe Valley Way relief road among the recurring priorities.",
   "National Highways carries the A21, the main trunk route north to the M25 at Sevenoaks, while the A259 coast road and the A2100 to Battle are county roads, and the new Queensway Gateway Road has improved links from St Leonards to the A21. Seafront-exposed and steep-hill work alike mean demanding, weather-beaten maintenance.",
   "Resurfacing, lining, drainage, lighting, seafront work and winter gritting mean Hastings gangs work in hi-vis next to live traffic.",
  ],
  "kit_loc":"across the town's carriageway, seafront and winter-maintenance work",
  "s2_intro":"Across Hastings's county carriageway and seafront work and the National Highways A21",
 },
 "birkenhead": {
  "region":"Birkenhead and the Wirral",
  "nearby":["Liverpool","Wallasey","Bebington"],
  "snapshot":"iNeedWorkwear kits Birkenhead's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from Wirral Council and the Liverpool City Region framework to the Mersey tunnels and the M53, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Wirral's roads running",
  "s1loc":[
   "Birkenhead is the principal town of the Wirral, facing Liverpool across the Mersey and linked to it by the Queensway and Kingsway road tunnels. Wirral Council is the highway authority for the borough, and its gangs work in Class 3 hi-vis beside dock, tunnel-approach and town-centre traffic, with Cammell Laird's shipyard and the Wirral Waters regeneration adding heavy movements.",
   "Wirral mixes in-house delivery with tendered works, resurfacing hundreds of roads in recent years and using the Procure Partnerships framework with John Graham Construction for Birkenhead town-centre schemes, while sitting as a client on the eight-hundred-and-fifty-million-pound Liverpool City Region planned-works framework with Merseyside contractors.",
   "National Highways carries the M53 down the peninsula from junction 1 at Wallasey, while the Queensway and Kingsway tunnels under the Mersey are operated and maintained by Merseytravel with overnight closures, and the A41 New Chester Road runs south to Bebington and Ellesmere Port. Tunnel-approach and motorway work alike mean fast roads and tight diversions.",
   "Resurfacing, lining, drainage, lighting and winter gritting are all handled by Birkenhead crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the borough's carriageway, tunnel-approach and winter-maintenance work",
  "s2_intro":"Across Birkenhead's council carriageway and tunnel-approach work and the National Highways M53 and Mersey tunnels",
 },
 "bath": {
  "region":"Bath and North East Somerset",
  "nearby":["Bristol","Chippenham","Weston-super-Mare"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Bath's highway maintenance teams and roadworks contractors, from Bath and North East Somerset Council's VolkerHighways contract to National Highways work on the M4 and A36, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep Bath's roads running",
  "s1loc":[
   "Bath is a UNESCO World Heritage city where weight and access limits ring the historic core and the listed Cleveland Bridge carries a long-standing tonnage restriction. Bath and North East Somerset Council is the unitary highway authority for around eleven hundred kilometres of road, and its gangs work in Class 3 hi-vis in tightly constrained, heritage-sensitive streets.",
   "Maintenance runs through a term contract with VolkerHighways, which succeeded Skanska and was extended to 2029 at around nine million pounds a year, covering carriageways, drainage and street lighting from a near carbon-neutral depot, with a recent resurfacing programme of ninety-two thousand square metres. Works in the centre need Historic England consent and careful traffic orders.",
   "National Highways carries the M4 to the north at junctions 17 and 18 and the A4 in from the east and west, while the A36 and A46 form the main through-routes, with heavy goods vehicles over eighteen tonnes diverted around the city via the ring road and the A46. Trunk and heritage-core work alike mean tight, closely managed sites.",
   "Resurfacing, lining, drainage, lighting and winter gritting are all handled by Bath crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the city's carriageway, lighting and winter-maintenance work",
  "s2_intro":"Across Bath's council carriageway, lighting and drainage work and the National Highways M4 and A36 network",
 },
 "stevenage": {
  "region":"Stevenage and Hertfordshire",
  "nearby":["Hitchin","Letchworth","Welwyn Garden City"],
  "snapshot":"iNeedWorkwear kits Stevenage's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from Hertfordshire's Ringway contract to National Highways work on the A1(M), with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Stevenage area's roads running",
  "s1loc":[
   "Stevenage was designated Britain's first post-war new town in 1946 and built with a fully segregated cycleway network running as a parallel layer to its roads, with underpasses and bridges keeping cyclists clear of traffic. Hertfordshire County Council is the highway authority, and its gangs work in Class 3 hi-vis across both the road grid and that cycleway network.",
   "Hertfordshire runs its highways through Ringway, retained from 2025 on a long term worth at least fifty-five million pounds a year, delivered for the north of the county from the Coreys Mill depot near A1(M) junction 8, with the cycle tracks, underpass structures and parapets adding maintenance distinct from the carriageway programme.",
   "National Highways carries the A1(M) along the western edge through junctions 7 and 8, the main north-south freight artery, with the A602 the principal connector into the town and the Gunnels Wood Road industrial corridor driving heavy traffic. Motorway and distributor work alike mean fast roads and tight management.",
   "Resurfacing, lining, drainage, lighting, cycleway work and winter gritting mean Stevenage gangs work in hi-vis next to live traffic.",
  ],
  "kit_loc":"across the town's carriageway, cycleway and winter-maintenance work",
  "s2_intro":"Across Stevenage's county carriageway and cycleway work and the National Highways A1(M)",
 },
 "grimsby": {
  "region":"Grimsby and North East Lincolnshire",
  "nearby":["Cleethorpes","Scunthorpe","Lincoln"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Grimsby's highway maintenance teams and roadworks contractors, from North East Lincolnshire Council to National Highways work on the A180 and M180, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Grimsby area's roads running",
  "s1loc":[
   "Grimsby and neighbouring Immingham form the UK's largest port complex by tonnage, handling around forty-six million tonnes a year and pushing an exceptional share of heavy goods traffic onto the A180. North East Lincolnshire Council is the unitary highway authority, and its gangs work in Class 3 hi-vis beside that port freight.",
   "Highways and transport ran for fifteen years under a strategic partnership with Equans until 2025, when the council brought the majority of services back in-house, keeping work with local subcontractors and a separate highways framework for specialist packages. The port-driven traffic accelerates carriageway wear well beyond a typical local network.",
   "National Highways carries the M180 west to the M18 and the A180 east to Grimsby and the docks, with the A160 link to Immingham dualled to ease port congestion and a full concrete-carriageway reconstruction programmed, plus the A16 south toward Boston. Port-access and trunk work alike mean fast roads and very heavy freight.",
   "Resurfacing, lining, drainage, lighting, port-access work and winter gritting put Grimsby crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the area's carriageway, port-access and winter-maintenance work",
  "s2_intro":"Across Grimsby's council carriageway and port-access work and the National Highways A180 and M180 network",
 },
 "southport": {
  "region":"Southport and Sefton",
  "nearby":["Formby","Crosby","Ormskirk"],
  "snapshot":"iNeedWorkwear kits Southport's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from Sefton Council and the Liverpool City Region framework to the A565 coastal corridor, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Southport area's roads running",
  "s1loc":[
   "Southport is a Victorian seaside resort, the largest town in Sefton, with a long seafront and the A565 coastal corridor carrying heavy visitor traffic to the promenade and the Royal Birkdale golf links. Sefton Council is the metropolitan highway authority, and its gangs work in Class 3 hi-vis beside salt-laden seafront roads that wear faster than inland.",
   "The council delivers footway and carriageway maintenance through annual service contracts with Dowhigh as prime contractor, moving to a longer eight-year deal, and draws on the Liverpool City Region planned-works framework for capital schemes such as the multi-year Southport Eastern Access corridor of junction upgrades.",
   "There is no motorway into Southport itself, but the A565 runs the coast toward Liverpool and Preston, the A570 heads inland to Ormskirk and the M58, and Sefton is improving M58 junction 1 at Switch Island. Coastal-corridor and junction work alike mean exposed conditions and tight management.",
   "Resurfacing, lining, drainage, lighting, seafront work and winter gritting are all handled by Southport crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the resort's carriageway, seafront and winter-maintenance work",
  "s2_intro":"Across Southport's council carriageway and seafront work and the A565 coastal corridor",
 },
 "halifax": {
  "region":"Halifax and Calderdale",
  "nearby":["Huddersfield","Bradford","Brighouse"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Halifax's highway maintenance teams and roadworks contractors, from Calderdale Council and the Yorkshire Alliance framework to National Highways work on the M62, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep Calderdale's roads running",
  "s1loc":[
   "Halifax is the main town of Calderdale, set in steep Pennine valleys where bridges and retaining walls are integral to the road network and the M62 crosses the tops at over three hundred and seventy metres. Calderdale Council is the highway authority, and its gangs work in Class 3 hi-vis on demanding valley and moorland roads.",
   "Surfacing runs through the Yorkshire Alliance framework with Colas, alongside the council's in-house team and a fifteen-million-pound highways investment programme, much of it shaped by flood resilience after the 2015 Boxing Day floods damaged hundreds of structures and bridges across the Calder Valley at a cost of around twenty-five million pounds.",
   "National Highways carries the trans-Pennine M62 through the district at junctions 24 and 25, climbing to the highest motorway point in England near Scammonden, with the A629 the main spine to Huddersfield and Keighley and the A646 and A58 the valley routes. Trans-Pennine and valley work alike mean severe winters and heavy structures maintenance.",
   "Resurfacing, lining, drainage, lighting, bridge work and heavy winter gritting mean Halifax gangs work in hi-vis next to live traffic.",
  ],
  "kit_loc":"across the district's carriageway, valley-road and winter-maintenance work",
  "s2_intro":"Across Halifax's council carriageway and valley-road work and the National Highways M62",
 },
 "eltham": {
  "region":"Eltham and South East London",
  "nearby":["Woolwich","Lewisham","Sidcup"],
  "snapshot":"iNeedWorkwear kits Eltham's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from the Royal Borough of Greenwich's Marlborough contract to the Transport for London red routes, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Eltham area's roads running",
  "s1loc":[
   "Eltham sits on the A205 South Circular in the Royal Borough of Greenwich, one of south-east London's most congested orbital corridors. The borough council is the highway authority for the local roads, and its gangs work in Class 3 hi-vis beside heavy, slow-moving urban traffic.",
   "Greenwich runs its local network through a term contract with Marlborough Highways from 2024, worth up to fifty-six million pounds over its full term and covering carriageways, footways, drainage and winter service from a borough depot, while Transport for London maintains the red routes through FM Conway's South area framework.",
   "There is no motorway in the borough, but the A205 South Circular threads through Eltham along Westhorne Avenue and Eltham Road and the A20 runs south toward Sidcup and the M25. Red-route and borough work sit side by side, so crews from both the TfL framework and the borough contract often work in close proximity.",
   "Resurfacing, lining, drainage, lighting and footway work keep Eltham crews in hi-vis within feet of moving traffic.",
  ],
  "kit_loc":"across the borough's carriageway, lighting and footway work",
  "s2_intro":"Across Eltham's borough carriageway and footway work and the Transport for London red-route network",
 },
 "hounslow": {
  "region":"Hounslow and West London",
  "nearby":["Feltham","Hayes","Twickenham"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Hounslow's highway maintenance teams and roadworks contractors, from the borough's Hounslow Highways PFI with Ringway to National Highways work on the M4, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep west London's roads running",
  "s1loc":[
   "Hounslow sits on Heathrow's doorstep, with the M4 and A4 corridor carrying enormous airport passenger and freight flows across the borough. The London Borough of Hounslow is the highway authority, and its gangs work in Class 3 hi-vis beside some of the busiest surface roads in the country.",
   "The borough runs a twenty-five-year highways PFI, Hounslow Highways, owned by VINCI and Barclays with delivery by Ringway, running to 2037 and maintaining four hundred and thirty kilometres of carriageway and seven hundred kilometres of footway from a dedicated depot, one of the larger highways PFIs in London.",
   "National Highways carries the M4 through the north of the borough to Heathrow, while Transport for London runs the A4 Great West Road, the A30, the A312 Hayes Bypass and the A316 as red routes, all carrying heavy airport and logistics traffic. Motorway, red-route and airport work alike mean fast roads and tight, around-the-clock management.",
   "Resurfacing, lining, drainage, lighting and winter gritting are all handled by Hounslow crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the borough's carriageway, lighting and winter-maintenance work",
  "s2_intro":"Across Hounslow's borough carriageway, lighting and drainage work and the National Highways M4 corridor",
 },
 "bromley": {
  "region":"Bromley and South East London",
  "nearby":["Orpington","Croydon","Sidcup"],
  "snapshot":"iNeedWorkwear kits Bromley's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from the borough's highways framework and FM Conway to the Transport for London red routes, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Bromley area's roads running",
  "s1loc":[
   "Bromley is the largest London borough by area, with over eight hundred kilometres of carriageway running from dense suburb to the rural fringe at Biggin Hill and Downe. The London Borough of Bromley is the highway authority, and its gangs work in Class 3 hi-vis across a network closer in scale to a county than an inner-London borough.",
   "The borough delivers maintenance through a contractor panel including FM Conway, and is re-tendering a six-year framework worth around seventy-one million pounds split into major and minor works, while FM Conway also holds the Transport for London South area framework covering Bromley's red routes.",
   "There is no motorway in the borough, but the A21 runs from Catford through Bromley and Orpington toward the M25 at junction 4, the A20 follows the Sidcup and Farnborough corridor and the A232 crosses east to west. Red-route and suburban-fringe work alike mean fast radial traffic and a wide range of road types.",
   "Resurfacing, lining, drainage, lighting and winter gritting put Bromley crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the borough's carriageway, lighting and winter-maintenance work",
  "s2_intro":"Across Bromley's borough carriageway, lighting and drainage work and the Transport for London red-route network",
 },
 "nuneaton": {
  "region":"Nuneaton and Warwickshire",
  "nearby":["Coventry","Bedworth","Hinckley"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Nuneaton's highway maintenance teams and roadworks contractors, from Warwickshire's joint Balfour Beatty contract to National Highways work on the M6, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep Nuneaton and north Warwickshire's roads running",
  "s1loc":[
   "Nuneaton is the largest town in Warwickshire, sitting just east of the M6 with the A444 as its main artery to junction 3 and the town centre. Warwickshire County Council is the highway authority, and its gangs work in Class 3 hi-vis beside heavy motorway-fed and arterial traffic.",
   "Maintenance runs through the joint contract shared with Coventry and Solihull, delivered by Balfour Beatty Living Places across more than five thousand kilometres of road, now in its third term on a deal worth up to nine hundred million pounds, with recent full-depth resurfacing of the A444 Griff Island and Griff Way.",
   "National Highways carries the M6 immediately west at junction 3, the main north-south freight spine, with the A444 running north to south through the town toward Atherstone, the A5 Watling Street to the north and the A47 east to Leicester. Motorway-junction and A444 work alike mean fast roads and heavy freight.",
   "Resurfacing, lining, drainage, lighting and winter gritting mean Nuneaton gangs work in hi-vis next to live traffic.",
  ],
  "kit_loc":"across the town's carriageway, lighting and winter-maintenance work",
  "s2_intro":"Across Nuneaton's county carriageway, lighting and drainage work and the National Highways M6",
 },
 "redditch": {
  "region":"Redditch and Worcestershire",
  "nearby":["Bromsgrove","Birmingham","Solihull"],
  "snapshot":"iNeedWorkwear kits Redditch's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from Worcestershire's Ringway contract to National Highways work on the M42, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Redditch area's roads running",
  "s1loc":[
   "Redditch is a 1964 new town built to new-town highway standards, encircled by the Redditch Ringway and linked to Birmingham by the A441 Alvechurch Highway dual carriageway. Worcestershire County Council is the highway authority, and its gangs work in Class 3 hi-vis on a purpose-built network of distributor roads now reaching the end of its design life.",
   "Ringway runs the county term maintenance contract covering carriageways, footways, drainage and over a thousand structures, operating in the north of the county from the Lye Bridge depot near Alvechurch, with resurfacing of the A441 corridor a recurring feature of the annual programme.",
   "National Highways carries the M42 to the east at junction 2 for the A441 and junction 3 for the A435, with the A441 running north into Birmingham and the A448 west to Bromsgrove and the M5. New-town distributor and motorway-junction work alike mean fast roads and tight management.",
   "Resurfacing, lining, drainage, lighting, distributor-road work and winter gritting put Redditch crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the town's carriageway, distributor-road and winter-maintenance work",
  "s2_intro":"Across Redditch's county carriageway and distributor-road work and the National Highways M42",
 },
 "harlow": {
  "region":"Harlow and West Essex",
  "nearby":["Chelmsford","Bishop's Stortford","Hoddesdon"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Harlow's highway maintenance teams and roadworks contractors, from Essex Highways and its Ringway Jacobs partnership to National Highways work on the M11, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep West Essex's roads running",
  "s1loc":[
   "Harlow is a post-war new town master-planned by Frederick Gibberd, with one of the most extensive dedicated cycleway and footpath networks in England keeping cyclists clear of the roads. Essex County Council is the highway authority, and its gangs work in Class 3 hi-vis across both the carriageway network and that legacy cycle infrastructure.",
   "Highways are delivered through Essex Highways, the partnership with Ringway Jacobs run from Chelmsford, with the county procuring a successor contract worth up to three billion pounds from 2027, and Octavius delivering recent schemes such as the Templefields access road in the town's enterprise zone.",
   "National Highways carries the M11 along the eastern edge, where the new junction 7a opened in 2022 to serve the Harlow and Gilston Garden Town, with the A414 the main east-west route and the A1025 linking it to the motorway. Motorway and garden-town growth work alike mean fast roads and heavy construction traffic.",
   "Resurfacing, lining, drainage, lighting, cycleway work and winter gritting keep Harlow crews in hi-vis within feet of moving traffic.",
  ],
  "kit_loc":"across the town's carriageway, cycleway and winter-maintenance work",
  "s2_intro":"Across Harlow's county carriageway and cycleway work and the National Highways M11",
 },
 "harrow": {
  "region":"Harrow and North West London",
  "nearby":["Edgware","Wembley","Ruislip"],
  "snapshot":"iNeedWorkwear kits Harrow's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from the borough's JB Riney and Tarmac contract to the Transport for London red routes, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Harrow area's roads running",
  "s1loc":[
   "Harrow is a dense inner-suburban borough in north-west London, its landmark hill rising above the surrounding streets and creating gradient and drainage challenges. The London Borough of Harrow is the highway authority for the local roads, and its gangs work in Class 3 hi-vis beside heavy suburban through-traffic.",
   "The borough runs a highways term contract worth around one hundred and ten million pounds with JB Riney, now part of Tarmac, from a borough depot covering routine and emergency maintenance, resurfacing, lighting and gritting, while Transport for London maintains the A404 and A409 red routes that cross the borough.",
   "There is no motorway in the borough, but the A404 Pinner Road, the A409 and the A4006 Kenton Road carry heavy through-traffic toward the M1, M25 and M40 just beyond, with the A406 North Circular along the eastern edge run by TfL. Red-route and suburban work alike mean constant lane management on busy corridors.",
   "Resurfacing, lining, drainage, lighting and footway work are all handled by Harrow crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the borough's carriageway, lighting and footway work",
  "s2_intro":"Across Harrow's borough carriageway and footway work and the Transport for London red-route network",
 },
 "st albans": {
  "region":"St Albans and Hertfordshire",
  "nearby":["Hatfield","Welwyn Garden City","Hemel Hempstead"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to St Albans's highway maintenance teams and roadworks contractors, from Hertfordshire's Ringway contract to National Highways work on the M1, M25 and A1(M), with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the St Albans area's roads running",
  "s1loc":[
   "St Albans is a cathedral city ringed by strategic motorways, sitting inside the triangle of the M1, M25 and A1(M) with a compressed historic centre. Hertfordshire County Council is the highway authority, and its gangs work in Class 3 hi-vis from the tight Roman-era core out to the motorway-fed orbital roads.",
   "Hertfordshire runs its highways through Ringway, retained from 2025 on a seven-year term worth around three hundred and eighty-five million pounds, covering road maintenance, lighting, signals, gritting and emergency response across the county, with a Hertfordshire supply chain drawn from the Hemel Hempstead and Hatfield industrial areas.",
   "National Highways carries the M1 at junctions 6 and 7, the M25 at junction 21a and the A1(M) at junction 3, with the A414 North Orbital the main local strategic corridor between them carrying heavy commercial traffic. Motorway-triangle and orbital work alike mean fast roads and major junction maintenance.",
   "Resurfacing, lining, drainage, lighting and winter gritting mean St Albans gangs work in hi-vis next to live traffic.",
  ],
  "kit_loc":"across the city's carriageway, lighting and winter-maintenance work",
  "s2_intro":"Across St Albans's county carriageway, lighting and drainage work and the National Highways M1, M25 and A1(M) network",
 },
 "stockton-on-tees": {
  "region":"Stockton-on-Tees and the Tees Valley",
  "nearby":["Middlesbrough","Hartlepool","Billingham"],
  "snapshot":"iNeedWorkwear kits Stockton-on-Tees's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from the borough council's highways teams to National Highways work on the A19 and A66, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Stockton area's roads running",
  "s1loc":[
   "Stockton-on-Tees has one of the widest high streets in England and sits on the Tees just west of the A19 Tees Viaduct, the high-level crossing into Middlesbrough. Stockton-on-Tees Borough Council is the unitary highway authority, and its gangs work in Class 3 hi-vis beside strategic and industrial traffic.",
   "The council manages highways through its own network team with term specialist contractors for surfacing and structures, Tarmac among those supplying low-carbon resurfacing, topped up by Tees Valley Combined Authority maintenance grants shared across the five Tees Valley authorities.",
   "National Highways carries the A19 over the Tees Viaduct, which takes over a hundred thousand vehicles a day and is at capacity, and the A66 east to Middlesbrough and west to Darlington, with the A689 Wolviston interchange improved and the A1027 and A1046 the main local routes. Viaduct and trunk work alike mean fast roads and heavy industrial freight.",
   "Resurfacing, lining, drainage, lighting and winter gritting are all handled by Stockton crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the borough's carriageway, lighting and winter-maintenance work",
  "s2_intro":"Across Stockton-on-Tees's council carriageway, lighting and drainage work and the National Highways A19 and A66 network",
 },
 "gosport": {
  "region":"Gosport and South East Hampshire",
  "nearby":["Fareham","Portsmouth","Havant"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Gosport's highway maintenance teams and roadworks contractors, from Hampshire County Council's Milestone contract to the A32 peninsula corridor, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Gosport peninsula's roads running",
  "s1loc":[
   "Gosport is a peninsula town with no railway, where the single A32 carries every motor vehicle entering or leaving by land and a passenger ferry crosses the harbour to Portsmouth. Hampshire County Council is the highway authority, and its gangs work in Class 3 hi-vis on a network where the one road corridor is critical to the whole town.",
   "Hampshire runs its highways through Milestone, now M Group Highways, under the Hampshire Highways brand, the contract first let to Skanska in 2017 and extended to 2029 after over three hundred and fifty million pounds of work, with the Fareham area as the logistics base for the peninsula.",
   "There is no National Highways road into Gosport itself, with the A32 to Fareham managed by the county as the sole land corridor and a bus rapid transit route added to ease its capacity, while the M27 is the nearest motorway just to the north. Single-corridor and tidal-estuary work alike mean critical, carefully managed sites.",
   "Resurfacing, lining, drainage, lighting and winter gritting put Gosport crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the peninsula's carriageway, lighting and winter-maintenance work",
  "s2_intro":"Across Gosport's county carriageway and lighting work and the A32 peninsula corridor",
 },
 "scunthorpe": {
  "region":"Scunthorpe and North Lincolnshire",
  "nearby":["Grimsby","Cleethorpes","Goole"],
  "snapshot":"iNeedWorkwear kits Scunthorpe's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from North Lincolnshire Council's in-house team to National Highways work on the M180, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Scunthorpe area's roads running",
  "s1loc":[
   "Scunthorpe is a steel town, the British Steel works driving wide loads and coil traffic onto the Phoenix Parkway and the A1077 corridor. North Lincolnshire Council is the unitary highway authority, running highways from its Normanby Enterprise Park depot, and its gangs work in Class 3 hi-vis beside that heavy industrial traffic.",
   "The council carries out much of its routine maintenance with its own operatives, investing in extra plant for pothole repair and using framework subcontractors for planned resurfacing, with the Lincolnshire Lakes scheme reshaping the western edge of the town and truncating the old M181 spur.",
   "National Highways carries the M180 east to west with junctions 3 and 4 serving the town, while the short M181 spur was largely taken over by the council and the A18 and A1077 carry the rest of the strategic load toward the Humber bank. Steelworks and trunk work alike mean fast roads and heavy freight.",
   "Resurfacing, lining, drainage, lighting and winter gritting mean Scunthorpe gangs work in hi-vis next to live traffic.",
  ],
  "kit_loc":"across the town's carriageway, lighting and winter-maintenance work",
  "s2_intro":"Across Scunthorpe's council carriageway, lighting and drainage work and the National Highways M180",
 },
 "chesterfield": {
  "region":"Chesterfield and Derbyshire",
  "nearby":["Sheffield","Dronfield","Alfreton"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Chesterfield's highway maintenance teams and roadworks contractors, from Derbyshire County Council's ALLRoads team to National Highways work on the M1, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Chesterfield area's roads running",
  "s1loc":[
   "Chesterfield, famous for its twisted church spire, sits just east of the M1 between Sheffield and the Peak District. Derbyshire County Council is the highway authority, and its gangs work in Class 3 hi-vis beside motorway-fed traffic and on the A61 spine through the town centre.",
   "Derbyshire delivers highways through its own direct labour organisation, ALLRoads, with a turnover above twenty million pounds handling construction, drainage, lighting and reinstatements across more than three thousand five hundred miles of network, bringing in specialist contractors for larger schemes.",
   "National Highways carries the M1 to the south-west, with junction 29 linking via the A617 to Chesterfield and Mansfield and junction 29a serving the Markham Vale enterprise zone on the former colliery site, while the A61 runs north to south through the town. Motorway-junction and A61 work alike mean fast roads and heavy logistics freight.",
   "Resurfacing, lining, drainage, lighting and winter gritting are all handled by Chesterfield crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the town's carriageway, lighting and winter-maintenance work",
  "s2_intro":"Across Chesterfield's county carriageway, lighting and drainage work and the National Highways M1",
 },
 "ashford": {
  "region":"Ashford and Kent",
  "nearby":["Maidstone","Folkestone","Canterbury"],
  "snapshot":"iNeedWorkwear kits Ashford's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from Kent County Council's term contract to National Highways work on the M20, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Ashford area's roads running",
  "s1loc":[
   "Ashford is an international rail gateway on the M20, its road network carrying cross-Channel freight bound for Dover and the Eurotunnel terminal. Kent County Council is the highway authority, and its gangs work in Class 3 hi-vis beside heavy international lorry traffic on the A2070 and the trunk approaches.",
   "Kent ran its highways with Amey for around a dozen years before moving to a new term contract with Ringway from 2026, worth around fifty million pounds a year, with a separate specialist surfacing framework covering the Ashford and Folkestone district awarded to CW Surfacing.",
   "National Highways carries the M20 north of the town through junctions 8 to 10, with the deployable Operation Brock contraflow held ready between junctions 8 and 9 for cross-Channel disruption, the A2070 trunk link to the international station and the junction 10a lorry area. Brock and trunk work alike mean fast roads and very tight management.",
   "Resurfacing, lining, drainage, lighting and winter gritting put Ashford crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the town's carriageway, lighting and winter-maintenance work",
  "s2_intro":"Across Ashford's county carriageway, lighting and drainage work and the National Highways M20",
 },
 "guildford": {
  "region":"Guildford and Surrey",
  "nearby":["Godalming","Aldershot","Redhill"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Guildford's highway maintenance teams and roadworks contractors, from Surrey County Council's Ringway contract to National Highways work on the A3, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Guildford area's roads running",
  "s1loc":[
   "Guildford has the A3 trunk road running straight through it as a high-speed dual carriageway, with a one-way gyratory wrapping the town centre and National Highways itself headquartered in the town. Surrey County Council is the highway authority for the local roads, and its gangs work in Class 3 hi-vis where strategic and local networks meet.",
   "Surrey moved its term maintenance contract from Kier to Ringway in 2022, a deal worth up to two and a half billion pounds over as long as twenty-one years, covering road repairs, resurfacing, structures, drainage and winter service across the county from Surrey depots.",
   "National Highways carries the A3 through the town, with concrete repairs and resurfacing recurring at the Dennis Roundabout where it meets the A322, the A31 branching south-west to Farnham and the M25 junction 10 upgrade to the north-east. Trunk and gyratory work alike mean fast traffic and tight overnight windows.",
   "Resurfacing, lining, drainage, lighting and winter gritting mean Guildford gangs work in hi-vis next to live traffic.",
  ],
  "kit_loc":"across the town's carriageway, lighting and winter-maintenance work",
  "s2_intro":"Across Guildford's county carriageway, lighting and drainage work and the National Highways A3",
 },
 "lewisham": {
  "region":"Lewisham and South East London",
  "nearby":["Bromley","Eltham","Croydon"],
  "snapshot":"iNeedWorkwear kits Lewisham's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from the borough's FM Conway contract to the Transport for London red routes, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Lewisham area's roads running",
  "s1loc":[
   "Lewisham sits where several major radials converge in inner south-east London, with the A205 South Circular among the most congested roads in the country running across the borough. The London Borough of Lewisham is the highway authority for the local roads, and its gangs work in Class 3 hi-vis in a dense, busy urban network.",
   "The borough runs a ten-year highways contract with FM Conway from 2022 covering inspections, reactive and planned works and minor schemes, while FM Conway also holds the Transport for London South area framework that maintains the borough's red routes alongside the other south London boroughs.",
   "There is no motorway in the borough, but the A20 and A21 radials run from central London toward the M25 and the A205 South Circular crosses east to west as a red route with no stopping along most of its length. Red-route and inner-London work alike mean narrow carriageways, closely spaced junctions and heavy pedestrian footfall.",
   "Resurfacing, lining, drainage, lighting and footway work are all handled by Lewisham crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the borough's carriageway, lighting and footway work",
  "s2_intro":"Across Lewisham's borough carriageway and footway work and the Transport for London red-route network",
 },
 "woolwich": {
  "region":"Woolwich and South East London",
  "nearby":["Eltham","Erith","Lewisham"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Woolwich's highway maintenance teams and roadworks contractors, from the Royal Borough of Greenwich's Marlborough contract to the Transport for London red routes and the Woolwich Ferry, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Woolwich area's roads running",
  "s1loc":[
   "Woolwich sits on the south bank of the Thames in the Royal Borough of Greenwich, linked across the river by the free Woolwich Ferry and now by the Silvertown Tunnel. The borough council is the highway authority for the local roads, and its gangs work in Class 3 hi-vis beside heavy riverside and ferry-approach traffic.",
   "Greenwich runs its local network through a term contract with Marlborough Highways from 2024, worth up to fifty-six million pounds over its full term, covering carriageways, footways, drainage and winter service from a borough depot, with the Royal Arsenal regeneration and the Elizabeth line at Woolwich driving sustained works.",
   "Transport for London runs the A206 Woolwich Church Street and the A205 South Circular as red routes, and operates the Woolwich Ferry, which saw traffic rise after the tolled Silvertown and Blackwall tunnels opened, while National Highways runs the A102 and Silvertown Tunnel on the north bank. Ferry-approach and red-route work alike mean tight, busy sites.",
   "Resurfacing, lining, drainage, lighting and footway work keep Woolwich crews in hi-vis within feet of moving traffic.",
  ],
  "kit_loc":"across the borough's carriageway, ferry-approach and footway work",
  "s2_intro":"Across Woolwich's borough carriageway and ferry-approach work and the Transport for London red-route network",
 },
 "weston-super-mare": {
  "region":"Weston-super-Mare and North Somerset",
  "nearby":["Bristol","Bridgwater","Clevedon"],
  "snapshot":"iNeedWorkwear kits Weston-super-Mare's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from North Somerset Council's NSEC contract to National Highways work on the M5, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Weston area's roads running",
  "s1loc":[
   "Weston-super-Mare is a coastal resort on the Severn Estuary, its seafront promenade and the A370 corridor carrying heavy visitor traffic. North Somerset Council is the unitary highway authority, and its gangs work in Class 3 hi-vis beside salt-exposed seafront roads and the busy approaches from the M5.",
   "The council delivers cyclical and reactive maintenance through North Somerset Environment Company, its own trading company, from depots at Westlands and Aisecome Way, covering around eleven hundred kilometres of road including surfacing, drainage, gritting and traffic management.",
   "National Highways carries the M5 through the hinterland, with junction 21 the main access via the A370 and recent structural work on St Georges Bridge, junction 22 onto the A38, and the A371 running east toward the Mendips. Motorway-junction and seafront work alike mean fast roads and exposed coastal conditions.",
   "Resurfacing, lining, drainage, lighting, seafront work and winter gritting are all handled by Weston-super-Mare crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the town's carriageway, seafront and winter-maintenance work",
  "s2_intro":"Across Weston-super-Mare's council carriageway and seafront work and the National Highways M5",
 },
 "edgware": {
  "region":"Edgware and North West London",
  "nearby":["Barnet","Harrow","Watford"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Edgware's highway maintenance teams and roadworks contractors, from the Barnet and Harrow boroughs to the Transport for London red routes on the A5, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Edgware area's roads running",
  "s1loc":[
   "Edgware sits at the northern end of the A5 Edgware Road, the dead-straight Roman Watling Street that forms the boundary between the London Boroughs of Barnet and Harrow. Both boroughs are highway authorities for their sides of the corridor, and their gangs work in Class 3 hi-vis beside heavy north-west London traffic.",
   "Barnet runs a highways maintenance framework of nine contractors including Marlborough Highways and VolkerHighways, with the Tarmac Kier joint venture as its principal term contractor on a deal worth around twenty-five million pounds, while Harrow has been procuring a framework worth around three hundred million pounds, and Transport for London maintains the A5 as a red route.",
   "The A5 Edgware Road is a TfL red route running unbroken toward central London, with the A41 to the east connecting to the M1 at Apex Corner and the A410 Whitchurch Lane crossing to Harrow and Watford. Dual-borough and red-route work alike mean careful coordination between two authorities and TfL.",
   "Resurfacing, lining, drainage, lighting and footway work mean Edgware gangs work in hi-vis next to live traffic.",
  ],
  "kit_loc":"across the area's carriageway, lighting and footway work",
  "s2_intro":"Across Edgware's borough carriageway and footway work and the Transport for London red-route network",
 },
 "bury": {
  "region":"Bury and Greater Manchester",
  "nearby":["Rochdale","Radcliffe","Whitefield"],
  "snapshot":"iNeedWorkwear kits Bury's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from the council's J Hopkins term contract to National Highways work on the M66, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Bury area's roads running",
  "s1loc":[
   "Bury is the northern terminus of the Metrolink Bury Line and a logistics node where the M66 forms the town's eastern bypass toward the M62 and the M65. Bury Metropolitan Borough Council is the highway authority, partnering with Transport for Greater Manchester on the Key Route Network, and its gangs work in Class 3 hi-vis beside motorway-fed and tram-corridor traffic.",
   "The council delivers maintenance through its highway service with J Hopkins Contractors as term contractor, spending around three and a half million pounds a year on resurfacing, and is procuring a new highways and civils framework worth around seventy-two million pounds to launch in 2026.",
   "National Highways carries the M66 north to south through the borough from the M62 at junction 3 toward Ramsbottom and the M65, passing the East Lancashire Railway viaduct, with the A56 Bury New Road the main radial to Manchester. Motorway and tram-corridor work alike mean fast roads and close coordination with Metrolink.",
   "Resurfacing, lining, drainage, lighting, tram-corridor work and winter gritting put Bury crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the borough's carriageway, tram-corridor and winter-maintenance work",
  "s2_intro":"Across Bury's council carriageway and tram-corridor work and the National Highways M66",
 },
 "tamworth": {
  "region":"Tamworth and Staffordshire",
  "nearby":["Lichfield","Sutton Coldfield","Cannock"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Tamworth's highway maintenance teams and roadworks contractors, from Staffordshire's Amey Infrastructure+ contract to National Highways work on the M42, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Tamworth area's roads running",
  "s1loc":[
   "Tamworth sits at M42 junction 10 on the A5 Watling Street, one of the most logistics-dense locations in the West Midlands with Birch Coppice, Ventura Park and other distribution parks clustered around it. Staffordshire County Council is the highway authority, and its gangs work in Class 3 hi-vis beside intense HGV traffic.",
   "Staffordshire runs its highways through Amey under the long-running Infrastructure Plus partnership covering the county's six-thousand-kilometre network, extended for a further five years from 2024 with an extra thirty million pounds, spanning maintenance, structures, drainage and environmental services.",
   "National Highways carries the M42 along the eastern and northern edge, with junction 10 the main access to the A5 and the logistics cluster, the A5 Watling Street running east to west to the south of the town and the A51 north to Lichfield. Motorway-junction and distribution-park work alike mean fast roads and very heavy freight.",
   "Resurfacing, lining, drainage, lighting and winter gritting mean Tamworth gangs work in hi-vis next to live traffic.",
  ],
  "kit_loc":"across the town's carriageway, lighting and winter-maintenance work",
  "s2_intro":"Across Tamworth's county carriageway, lighting and drainage work and the National Highways M42",
 },
 "chatham": {
  "region":"Chatham and the Medway towns",
  "nearby":["Rochester","Maidstone","Gravesend"],
  "snapshot":"iNeedWorkwear kits Chatham's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from Medway Council's VolkerHighways contract to National Highways work on the M2 and the Medway Tunnel, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Medway towns' roads running",
  "s1loc":[
   "Chatham is the commercial heart of the Medway towns, a continuous conurbation of around two hundred and eighty thousand people from Strood through Rochester to Gillingham. Medway Council is the unitary highway authority, and its gangs work in Class 3 hi-vis beside heavy conurbation traffic, including the council-run Medway Tunnel under the river.",
   "Medway runs its highways through VolkerHighways on a contract covering eight hundred and twenty-seven kilometres of road from 2017, with a successor procurement underway, and the Medway Tunnel is an unusual council responsibility needing confined-space and electrical competencies and out-of-hours emergency cover.",
   "National Highways carries the M2 to the north-east toward the M25 and the Channel ports and the A2 trunk route through the towns, while the A289 Medway Towns Northern Relief Road runs through the Medway Tunnel linking Strood to Chatham. Motorway, A2 and tunnel work alike mean fast roads and specialist structures maintenance.",
   "Resurfacing, lining, drainage, lighting and winter gritting are all handled by Chatham crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the towns' carriageway, tunnel and winter-maintenance work",
  "s2_intro":"Across Chatham's council carriageway and tunnel work and the National Highways M2 and A2 network",
 },
 "paisley": {
  "region":"Paisley and Renfrewshire",
  "nearby":["Glasgow","Renfrew","Clydebank"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Paisley's highway maintenance teams and roadworks contractors, from Renfrewshire Council to the Transport Scotland network and Glasgow Airport, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep Renfrewshire's roads running",
  "s1loc":[
   "Paisley sits on the M8 next to Glasgow Airport, at the junction of the motorway, the A737 and the airport approaches, one of the most traffic-sensitive spots in Scotland. Renfrewshire Council is the roads authority, running an in-house roads operations team from its Paisley depot, and its gangs work in Class 3 hi-vis beside heavy motorway and airport traffic.",
   "The council expands its in-house team for local schemes and brings in contractors such as Paisley-based Clark Contracts on frameworks, with Farrans delivering the fifty-nine-million-pound AMIDS South project of new road and bridge links between the town, the manufacturing district and the airport.",
   "Transport Scotland is the roads authority for the trunk network, with Amey running the south-west unit covering the M8, the busiest motorway in Scotland, the A8 alongside it and the A737 bypass past Paisley and Johnstone toward Ayrshire. Motorway and airport-corridor work alike mean fast roads and overnight possessions.",
   "Resurfacing, lining, drainage, lighting and winter gritting put Paisley crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the town's carriageway, lighting and winter-maintenance work",
  "s2_intro":"Across Paisley's council carriageway, lighting and drainage work and the Transport Scotland trunk-road network",
 },
 "carlisle": {
  "region":"Carlisle and north Cumbria",
  "nearby":["Penrith","Workington","Kendal"],
  "snapshot":"iNeedWorkwear kits Carlisle's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from Cumberland Council to National Highways work on the M6 and the Carlisle Southern Link Road, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep north Cumbria's roads running",
  "s1loc":[
   "Carlisle is the most northerly city in England, the point where the M6 ends and traffic crosses into Scotland, and a place twice hit by major flooding that damaged its roads and bridges. Cumberland Council, the unitary that replaced Cumbria County Council in 2023, is the highway authority, and its gangs work in Class 3 hi-vis across a large, partly upland network.",
   "Cumberland runs a mixed model of in-house resource and specialist term contracts inherited and split from the old county arrangements, with a road-marking contract held by Tim Doody and Co, while Galliford Try built the two-hundred-and-sixty-million-pound Carlisle Southern Link Road that opened in 2026. The flood history shapes bridge inspection and drainage priorities.",
   "National Highways carries the M6 to its northern terminus at junction 44, the main England to Scotland freight corridor, with the A69 trans-Pennine route east to Newcastle, the A7 north to the border and the A595 along the Cumbrian coast. Border-freight and flood-resilience work alike mean fast roads and demanding structures maintenance.",
   "Resurfacing, lining, drainage, lighting and winter gritting mean Carlisle gangs work in hi-vis next to live traffic.",
  ],
  "kit_loc":"across the city's carriageway, lighting and winter-maintenance work",
  "s2_intro":"Across Carlisle's council carriageway, lighting and drainage work and the National Highways M6",
 },
 "crewe": {
  "region":"Crewe and Cheshire East",
  "nearby":["Sandbach","Northwich","Stoke-on-Trent"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Crewe's highway maintenance teams and roadworks contractors, from Cheshire East's Ringway Jacobs contract to National Highways work on the M6 and A500, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Crewe area's roads running",
  "s1loc":[
   "Crewe is a historic railway town in south Cheshire, ringed by the A500 D-road linking the M6 to Stoke-on-Trent and threaded by level crossings and railway bridges. Cheshire East Council is the unitary highway authority, and its gangs work in Class 3 hi-vis beside heavy road and rail-interface traffic.",
   "Cheshire East runs its highways through Ringway Jacobs on a fifteen-year contract worth around six hundred million pounds from 2018, covering some sixteen hundred miles of road from depots at Crewe and Congleton, with Balfour Beatty delivering the Crewe Green link road improvements that opened in 2024.",
   "National Highways carries the M6 to the east at junctions 16 and 17, with the A500 D-road bypassing the town toward the A50 and Stoke, its long-planned dualling delayed after the cancellation of the HS2 Crewe hub, and the A50 and A532 the main connectors. Motorway and D-road work alike mean fast roads and rail-corridor coordination.",
   "Resurfacing, lining, drainage, lighting and winter gritting are all handled by Crewe crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the town's carriageway, lighting and winter-maintenance work",
  "s2_intro":"Across Crewe's council carriageway, lighting and drainage work and the National Highways M6 and A500 network",
 },
 "bootle": {
  "region":"Bootle and Merseyside",
  "nearby":["Liverpool","Crosby","Southport"],
  "snapshot":"iNeedWorkwear kits Bootle's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from Sefton Council and the Liverpool City Region framework to National Highways work on the A5036 dock road, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Bootle area's roads running",
  "s1loc":[
   "Bootle sits immediately north of Liverpool on the Mersey waterfront, defined by the Port of Liverpool and the A5036 dock road that carries its container freight. Sefton Council is the metropolitan highway authority, and its gangs work in Class 3 hi-vis beside intense port and dock traffic.",
   "Sefton procures highway maintenance through a series of annual service contracts by discipline and is a named client on the eight-hundred-and-fifty-million-pound Liverpool City Region planned-works framework, administering its highways from Merton House in Bootle, with the dock corridor carrying a disproportionate maintenance burden from heavy loading.",
   "National Highways carries the A5036 from Switch Island and the M57 and M58 to the Seaforth container terminal, the designated dock-road freight route, with the A565 the coastal road north toward Crosby and Southport, while the planned A5036 Princess Way improvement was cancelled in 2024. Dock-road and port work alike mean fast roads and very heavy freight.",
   "Resurfacing, lining, drainage, lighting and winter gritting put Bootle crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the borough's carriageway, dock-road and winter-maintenance work",
  "s2_intro":"Across Bootle's council carriageway and dock-road work and the National Highways A5036",
 },
 "harrogate": {
  "region":"Harrogate and North Yorkshire",
  "nearby":["Knaresborough","Ripon","York"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Harrogate's highway maintenance teams and roadworks contractors, from North Yorkshire Council and its NY Highways arm to the A59 and A61 corridors, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Harrogate area's roads running",
  "s1loc":[
   "Harrogate is a spa town and conference destination whose tree-lined approaches and town-centre streets carry heavy year-round visitor volumes, and where the Great Yorkshire Showground on the southern edge concentrates a summer traffic surge each show week. North Yorkshire Council is the unitary highway authority, and its gangs work in Class 3 hi-vis on commercially sensitive resort roads.",
   "Maintenance is delivered through NY Highways, the council-owned company launched in 2021 that runs an in-house direct-labour model across almost five thousand eight hundred miles of road from its Northallerton base, backed by a three-hundred-million-pound carriageways framework with Aggregate Industries, Tarmac, Hanson and Galliford Try. During the Great Yorkshire Show, non-emergency works on key approaches are suspended by agreement.",
   "There is no motorway through the town, so the A61 north-south through the centre and the A59 east-west to the Empress Roundabout are the spine, with the National Highways A1(M) bypassing to the east and the eighty-two-million-pound A59 Kex Gill realignment near Blubberhouses in its final phase. Resort-corridor and trunk diversion work alike demand careful management.",
   "Surfacing, lining, drainage, lighting and winter gritting all fall to Harrogate crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the spa town's carriageway, town-centre and winter-maintenance work",
  "s2_intro":"Across Harrogate's NY Highways carriageway work and the A59 and A61 corridors",
 },
 "maidenhead": {
  "region":"Maidenhead and Berkshire",
  "nearby":["Slough","Windsor","Bracknell"],
  "snapshot":"iNeedWorkwear kits Maidenhead's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from the Royal Borough of Windsor and Maidenhead's Marlborough contract to National Highways work on the M4 and A404(M), with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Maidenhead area's roads running",
  "s1loc":[
   "Maidenhead sits on the Great Western Main Line and the Elizabeth line, with Brunel's Grade I listed railway bridge of 1838 carrying the tracks across the Thames just south of the town and its two flat brick arches forcing close coordination with Network Rail around the station. The Royal Borough of Windsor and Maidenhead is the unitary highway authority, and its gangs work in Class 3 hi-vis through that rail-constrained network.",
   "After VolkerHighways held the term contract from 2017, Marlborough Highways won a new one-hundred-and-fifteen-million-pound deal from April 2026 covering six hundred and thirty-two kilometres of road, eight hundred kilometres of footway, over three hundred bridges and forty thousand highway trees. The handover spans a large structures and drainage portfolio alongside routine carriageway work.",
   "National Highways carries the M4 through the south of the borough at the dual-numbered junction 8/9 and the short A404(M) Maidenhead bypass spur, both upgraded during the all-lane-running smart-motorway scheme completed in 2022, while the A308 Windsor Road is the local spine. Motorway-junction and urban work alike mean fast roads and tight management.",
   "Resurfacing, lining, drainage, lighting and winter gritting put Maidenhead crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the borough's carriageway, structures and winter-maintenance work",
  "s2_intro":"Across Maidenhead's Marlborough carriageway work and the National Highways M4 and A404(M)",
 },
 "newcastle-under-lyme": {
  "region":"Newcastle-under-Lyme and Staffordshire",
  "nearby":["Stoke-on-Trent","Kidsgrove","Stafford"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Newcastle-under-Lyme's highway maintenance teams and roadworks contractors, from Staffordshire County Council's Amey Infrastructure Plus partnership to National Highways work on the M6, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Newcastle-under-Lyme area's roads running",
  "s1loc":[
   "Newcastle-under-Lyme is merged in urban terms with neighbouring Stoke-on-Trent, and the A500 dual carriageway, the local D-road, forms both the boundary and the connective spine between them. Staffordshire County Council is the highway authority, and its gangs work in Class 3 hi-vis across a network where cross-boundary street-works coordination with the city is a routine feature.",
   "The county delivers highways through the Infrastructure Plus partnership with Amey, running since 2014 and extended from October 2024 on a deal worth around seventy million pounds a year, with recent structural maintenance in the town on Dimsdale Parade West, Lower Milehouse Lane and the A519 Brook Lane. Heavy goods traffic off the M6 stresses the D-road pavement well beyond average.",
   "National Highways carries the M6 to the south and west at junctions 15 and 16, while the A500 links junction 16 into the Potteries and the A34 runs north-south through the historic town centre. Motorway-corridor and medieval-core work alike mean fast roads alongside restricted-width sites.",
   "Resurfacing, lining, drainage, lighting and winter gritting are all handled by Newcastle crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the area's carriageway, distributor-road and winter-maintenance work",
  "s2_intro":"Across Newcastle-under-Lyme's Amey carriageway work and the National Highways M6 and A500",
 },
 "burnley": {
  "region":"Burnley and Lancashire",
  "nearby":["Accrington","Nelson","Blackburn"],
  "snapshot":"iNeedWorkwear kits Burnley's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from Lancashire County Council's surfacing framework to National Highways work on the M65 and A56, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Burnley area's roads running",
  "s1loc":[
   "Burnley sits at the effective eastern end of the National Highways-managed M65, where Lancashire County Council takes over the motorway at junction 10 and grits it through to the Colne terminus at junction 14. The county is the highway authority for around four thousand six hundred miles of road, and its gangs work in Class 3 hi-vis across that unusual split-responsibility corridor.",
   "Lancashire runs a framework model rather than a single named term contractor, drawing on Colas, Tarmac and others for surfacing, vehicle restraint systems and specialist works, with a twenty-one-million-pound programme resurfacing more than a hundred roads in recent years. The Calder Valley Motorway brought a heavy portfolio of bridges and viaducts, including the Montford Viaduct, into routine inspection.",
   "National Highways carries the M65 to junction 10 and the A56 link from the M66, while the A682 threads through central Burnley and Nelson and the recent junction 9 Heasandford widening eased a busy interchange. Pennine A-roads toward the Yorkshire border at the A646 add demanding winter exposure.",
   "Surfacing, lining, drainage, lighting, structures and heavy winter gritting mean Burnley gangs work in hi-vis next to live traffic.",
  ],
  "kit_loc":"across the area's carriageway, Pennine-road and winter-maintenance work",
  "s2_intro":"Across Burnley's Lancashire framework carriageway work and the National Highways M65 and A56",
 },
 "enfield": {
  "region":"Enfield and North London",
  "nearby":["Barnet","Cheshunt","Potters Bar"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Enfield's highway maintenance teams and roadworks contractors, from the borough's Marlborough contract to the Transport for London red routes and the M25, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep Enfield's roads running",
  "s1loc":[
   "Enfield's network sits at the meeting point of two Transport for London red routes, the A10 Great Cambridge Road and the A406 North Circular, the M25 at junction 25, and the borough's own classified roads, so works coordination here spans three separate highway authorities. The London Borough of Enfield is the local authority, and its gangs work in Class 3 hi-vis across that layered network.",
   "Enfield delivers borough roads through a forty-five-million-pound highway maintenance and civil engineering contract running to 2027 with Marlborough Highways, covering carriageway recycling, resurfacing, lighting and reactive repair, and the borough was approved to extend lane rental from red routes to its own roads to curb utility disruption. The A10 corridor is a long-standing congestion pressure point.",
   "National Highways operates the M25 at junction 25 above Waltham Cross, recently upgraded with a new clockwise slip and an extra anti-clockwise lane, while TfL maintains the A10 and the ageing, heavily trafficked A406 North Circular structures. Orbital-motorway and red-route work alike mean fast roads and tight management.",
   "Resurfacing, lining, drainage, lighting and winter gritting put Enfield crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the borough's carriageway, red-route and winter-maintenance work",
  "s2_intro":"Across Enfield's Marlborough carriageway work, the TfL red routes and the M25",
 },
 "gravesend": {
  "region":"Gravesend and Kent",
  "nearby":["Dartford","Rochester","Chatham"],
  "snapshot":"iNeedWorkwear kits Gravesend's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from Kent County Council's Ringway term contract to National Highways work on the A2 and M2, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Gravesend area's roads running",
  "s1loc":[
   "Gravesend sits on the south bank of the Thames in the Ebbsfleet and A2 corridor, on the doorstep of the planned Lower Thames Crossing that would carry a new tunnelled route under the river to the east. Kent County Council is the highway authority, and its gangs work in Class 3 hi-vis across a network bracing for that nationally significant scheme.",
   "Kent moved its highways term maintenance to Ringway from May 2026 under a twenty-one-year contract worth about fifty million pounds a year, taking over from Amey after twelve years and covering pothole repair, gritting, drainage and bridge inspection with sharper performance targets. The Ebbsfleet growth area adds development-driven works to the routine programme.",
   "National Highways carries the A2 and M2 to the south as the strategic London-to-Channel route, while the A226 runs the riverside through Gravesend toward Dartford. Trunk-corridor and town work alike mean heavy freight and tightly managed sites.",
   "Surfacing, lining, drainage, lighting and winter gritting are all handled by Gravesend crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the area's carriageway, riverside-corridor and winter-maintenance work",
  "s2_intro":"Across Gravesend's Ringway carriageway work and the National Highways A2 and M2",
 },
 "east kilbride": {
  "region":"East Kilbride and Lanarkshire",
  "nearby":["Glasgow","Hamilton","Motherwell"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to East Kilbride's highway maintenance teams and roadworks contractors, from South Lanarkshire Council to Transport Scotland trunk roads on the A726 and M77 corridor, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the East Kilbride area's roads running",
  "s1loc":[
   "East Kilbride was Scotland's first post-war new town, planned around a distinctive network of large roundabouts and dual carriageways that still defines how traffic moves through it. South Lanarkshire Council is the unitary roads authority, running its East Kilbride and Cambuslang area office, and its gangs work in Class 3 hi-vis across that roundabout-led layout south of Glasgow.",
   "The council maintains local roads in-house, while the trunk network around the town is Transport Scotland's responsibility through its south-west operating arrangements, with Connect Roads maintaining the A726 Queensway and Glasgow Southern Orbital under the M77 DBFO contract. The mix of council estate roads and tolled-era DBFO trunk routes splits maintenance across two regimes.",
   "Transport Scotland carries the M77 and A77 toward Glasgow and the A726 across the southern orbital, while the A725 links north to Hamilton and the M74. New-town distributor and trunk work alike mean fast roads and careful management.",
   "Resurfacing, lining, drainage, lighting and winter gritting put East Kilbride crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the new town's carriageway, distributor-road and winter-maintenance work",
  "s2_intro":"Across East Kilbride's council carriageway work and the Transport Scotland A726 and M77 corridor",
 },
 "south shields": {
  "region":"South Shields and South Tyneside",
  "nearby":["Jarrow","Gateshead","Sunderland"],
  "snapshot":"iNeedWorkwear kits South Shields' highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from South Tyneside Council to National Highways work on the A19 and the Tyne Tunnel approaches, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the South Shields area's roads running",
  "s1loc":[
   "South Shields stands at the mouth of the Tyne, with the A19 and the Tyne Tunnel approaches at Jarrow shaping how freight and commuter traffic move through the borough. South Tyneside Council is the metropolitan highway authority, one of seven councils in the North East Mayoral Combined Authority, and its gangs work in Class 3 hi-vis beside that estuary freight.",
   "The council runs an annual resurfacing programme using specialist subcontractors selected for environmental and sustainability performance, with Network North funding lifting recent highway maintenance budgets across the town. Proximity to the tunnel approaches and the A19 keeps a steady stream of trunk-adjacent works on the books.",
   "National Highways carries the A19 north-south through the borough toward the Tyne Tunnel, with the A194 the link to the tunnel mouth and the A183 the coast road toward Sunderland. Trunk-corridor and coastal work alike mean fast roads and exposed conditions.",
   "Surfacing, lining, drainage, lighting and winter gritting are all handled by South Shields crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the borough's carriageway, coast-road and winter-maintenance work",
  "s2_intro":"Across South Shields' council carriageway work and the National Highways A19 and A194",
 },
 "burton-on-trent": {
  "region":"Burton-on-Trent and Staffordshire",
  "nearby":["Derby","Tamworth","Lichfield"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Burton-on-Trent's highway maintenance teams and roadworks contractors, from Staffordshire County Council's Amey Infrastructure Plus partnership to National Highways work on the A38 and A50, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Burton-on-Trent area's roads running",
  "s1loc":[
   "Burton-on-Trent is the home of British brewing and a major logistics centre, with Toyota's Burnaston plant just up the A38 and a dense pattern of distribution traffic feeding the trunk road. Staffordshire County Council is the highway authority, and its gangs work in Class 3 hi-vis beside that brewing and automotive freight in East Staffordshire.",
   "The county delivers highways through the Infrastructure Plus partnership with Amey, in place since 2014 and extended from October 2024, with recent town schemes including the B5008 Newton Road carriageway reconstruction and Swan junction signal upgrade and the Borough Road walking and cycling improvements. Amey draws on county depots and recycled aggregate for surface dressing.",
   "National Highways carries the A38 past the town as the strategic Birmingham-to-Derby route, with the A50 linking east toward the M1 and the A511 the local spine. Trunk-corridor and town-centre work alike mean heavy freight and tight management.",
   "Resurfacing, lining, drainage, lighting and winter gritting put Burton crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the area's carriageway, freight-corridor and winter-maintenance work",
  "s2_intro":"Across Burton-on-Trent's Amey carriageway work and the National Highways A38 and A50",
 },
 "shrewsbury": {
  "region":"Shrewsbury and Shropshire",
  "nearby":["Telford","Oswestry","Wolverhampton"],
  "snapshot":"iNeedWorkwear kits Shrewsbury's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from Shropshire Council's Kier-led mixed-economy model to National Highways work on the A5 and A49, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Shrewsbury area's roads running",
  "s1loc":[
   "Shrewsbury is the county town of Shropshire, wrapped in a tight loop of the River Severn that the planned North West Relief Road would bridge to complete an outer ring. Shropshire Council is the unitary highway authority for a large rural network, and its gangs work in Class 3 hi-vis across town-centre and far-flung county roads alike.",
   "The council runs an award-winning mixed-economy model that keeps some work in-house while Kier delivers planned and responsive works, street lighting, drainage and winter maintenance under a contract extended to April 2026 with options to 2028. In one recent year the partnership repaired nearly thirty-six thousand potholes across the county.",
   "National Highways carries the A5 around the town as the strategic route toward Telford and the M54 and on to North Wales, with the A49 running north-south toward Hereford and Whitchurch and the A458 heading west into mid Wales. Trunk-bypass and rural work alike mean fast roads and long, dispersed sites.",
   "Surfacing, lining, drainage, lighting and winter gritting are all handled by Shrewsbury crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the county town's carriageway, rural-road and winter-maintenance work",
  "s2_intro":"Across Shrewsbury's Kier-delivered carriageway work and the National Highways A5 and A49",
 },
 "rugby": {
  "region":"Rugby and Warwickshire",
  "nearby":["Coventry","Nuneaton","Leamington Spa"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Rugby's highway maintenance teams and roadworks contractors, from Warwickshire County Council's Balfour Beatty contract to National Highways work at the M6 and M1 split, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Rugby area's roads running",
  "s1loc":[
   "Rugby sits at one of the most strategically critical points on the English motorway network, the Catthorpe Interchange, where the M1 meets the M6 and the A14 on the eastern fringe of the borough. Warwickshire County Council is the highway authority, and its gangs work in Class 3 hi-vis beside one of the busiest freight interchanges in the country.",
   "The county runs its term maintenance through Balfour Beatty Living Places in a joint contract with Coventry and Solihull, the latest a three-hundred-and-fifteen-million-pound seven-year deal from May 2026 covering over five thousand kilometres of road. Adjacent freight activity at DIRFT, the Daventry International Rail Freight Terminal, drives heavy traffic-management and reinstatement demand.",
   "National Highways operates the M1, M6 and A14 around Catthorpe and has carried out bridge-deck and resurfacing work at junction 18 near Crick, while the A5 Watling Street crosses the borough and the A426 feeds the town centre, where an improvement scheme has been in preparation. Interchange and A-road work alike mean fast roads and tight management.",
   "Resurfacing, lining, drainage, lighting and winter gritting put Rugby crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the borough's carriageway, interchange-corridor and winter-maintenance work",
  "s2_intro":"Across Rugby's Balfour Beatty carriageway work and the National Highways M1, M6 and A14",
 },
 "stafford": {
  "region":"Stafford and Staffordshire",
  "nearby":["Cannock","Rugeley","Stoke-on-Trent"],
  "snapshot":"iNeedWorkwear kits Stafford's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from Staffordshire County Council's Amey Infrastructure Plus partnership to National Highways work on the M6, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Stafford area's roads running",
  "s1loc":[
   "Stafford is the county town and the seat of Staffordshire County Council at Staffordshire Place, making it the administrative hub for the county highways function as well as a busy market town. The council is the highway authority, and its gangs work in Class 3 hi-vis across roads radiating from the M6 corridor.",
   "Highways run through the Infrastructure Plus partnership with Amey, in place since 2014 and extended from October 2024, operating from depots including Gailey on the A5 Watling Street to the south. The signature Stafford Western Access Route, delivered through the partnership, unlocked housing and employment land west of the town and shows the breadth of work beyond routine repair.",
   "National Highways carries the M6 past the western edge at junctions 13 and 14, where overnight closures push diversion pressure onto the A34 toward Stone and the A518 toward Uttoxeter. Motorway and connector work alike mean fast roads and carefully signed diversions.",
   "Surfacing, lining, drainage, lighting and winter gritting are all handled by Stafford crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the county town's carriageway, connector-road and winter-maintenance work",
  "s2_intro":"Across Stafford's Amey carriageway work and the National Highways M6, A34 and A518",
 },
 "taunton": {
  "region":"Taunton and Somerset",
  "nearby":["Bridgwater","Wellington","Yeovil"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Taunton's highway maintenance teams and roadworks contractors, from Somerset Council's Kier term contract to National Highways work on the M5, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Taunton area's roads running",
  "s1loc":[
   "Taunton is the county town of Somerset and the base of Somerset Council, the unitary authority created in April 2023 by merging the county with its four districts. That reorganisation reshaped how highway contracts are procured, and the council's gangs work in Class 3 hi-vis across the whole reformed network.",
   "From April 2024 Kier Transportation holds the principal term maintenance contract, a two-hundred-and-twenty-five-million-pound deal under a new four-way split that also draws in Kiely Group, Octavius and Heidelberg Materials, with many Milestone staff transferring under TUPE and the area served from the Priorswood depot. The unitary transition was a significant change to contract management.",
   "National Highways carries the M5 to the east at junctions 25 and 26, while the A38 links to Wellington and the A358 heads north toward the A303, though the planned A358 dualling was cancelled in the October 2024 budget. The Toneway corridor on the A38 at Creech Castle has seen capacity work at a key pinch point.",
   "Resurfacing, lining, drainage, lighting and winter gritting put Taunton crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the county town's carriageway, corridor and winter-maintenance work",
  "s2_intro":"Across Taunton's Kier carriageway work and the National Highways M5 and A38",
 },
 "tynemouth": {
  "region":"Tynemouth and North Tyneside",
  "nearby":["North Shields","Whitley Bay","South Shields"],
  "snapshot":"iNeedWorkwear kits Tynemouth's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from North Tyneside Council's Capita partnership to National Highways work on the A19 and the Tyne Tunnel, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Tynemouth area's roads running",
  "s1loc":[
   "Tynemouth sits on the coast where the A1058 Coast Road meets the A19 and the Tyne Tunnel, a fixed crossing carrying around sixty-five thousand vehicles a day under the river. North Tyneside Council is the metropolitan highway authority, part of the North East Mayoral Combined Authority, and its gangs work in Class 3 hi-vis beside that tunnel-fed traffic.",
   "The council delivers highway asset maintenance and construction through a technical-services partnership with Capita, based at Cobalt Business Park, which manages the resurfacing and maintenance programme, while TT2 operates the Tyne Tunnel under a public-private partnership on behalf of the combined authority. Periodic tunnel closures drive significant cross-council network management.",
   "National Highways carries the A19 north-south through the borough with the Tyne Tunnel as its river crossing, while the A1058 Coast Road runs east-west to the coast through the triple-deck stack interchange completed in 2019 to clear the old roundabout queues. Trunk and interchange work alike mean fast roads and tight management.",
   "Surfacing, lining, drainage, lighting and winter gritting are all handled by Tynemouth crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the area's carriageway, coast-road and winter-maintenance work",
  "s2_intro":"Across Tynemouth's Capita carriageway work and the National Highways A19 and A1058",
 },
 "cannock": {
  "region":"Cannock and Staffordshire",
  "nearby":["Lichfield","Rugeley","Walsall"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Cannock's highway maintenance teams and roadworks contractors, from Staffordshire County Council's Amey Infrastructure Plus partnership to National Highways work on the M6 Toll and A5, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Cannock area's roads running",
  "s1loc":[
   "Cannock sits in the heart of the West Midlands motorway corridor, bounded to the east by the M6 Toll and to the south by the A5 Watling Street, with the Cannock Chase Area of Outstanding Natural Beauty constraining expansion to the north. Staffordshire County Council is the highway authority, and its gangs work in Class 3 hi-vis across that motorway-ringed network.",
   "The county delivers highways through the Infrastructure Plus partnership with Amey, drawing on the Gailey depot on the A5, and the A5 corridor through the district is one of the busiest mixed-use roads in the Midlands, carrying logistics traffic from the Kingswood Lakeside distribution park off the M6 Toll. The A460 toward Rugeley carries around twenty-six thousand vehicles a day.",
   "National Highways operates the tolled M6 Toll to the east at junctions T5 and T7 and the A5 to the south, where a major resurfacing scheme ran through spring 2024 with full closures at the Churchbridge and Great Wyrley roundabouts, while the consented M54-to-M6 link would later relieve the A460. Tolled-motorway and trunk work alike mean fast roads and tight management.",
   "Resurfacing, lining, drainage, lighting and winter gritting put Cannock crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the area's carriageway, logistics-corridor and winter-maintenance work",
  "s2_intro":"Across Cannock's Amey carriageway work and the National Highways M6 Toll and A5",
 },
 "farnborough": {
  "region":"Farnborough and Hampshire",
  "nearby":["Aldershot","Camberley","Fleet"],
  "snapshot":"iNeedWorkwear kits Farnborough's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from Hampshire County Council's M Group Highways contract to National Highways work on the M3 and the A331, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Farnborough area's roads running",
  "s1loc":[
   "Farnborough is the home of British aviation, and the biennial Farnborough International Airshow at its aerodrome generates an exceptional temporary traffic-management burden on the A325 and surrounding roads. Hampshire County Council is the highway authority for around five thousand four hundred miles of road, and its gangs work in Class 3 hi-vis across that event-prone network in Rushmoor.",
   "Hampshire Highways runs through a long-term term contract held by the former Milestone Infrastructure, now trading as M Group Highways after the 2025 rebrand and extended to 2029, with Pavenet among the named surfacing subcontractors. During show weeks the county imposes temporary speed limits and suspends turns on the A325 with marshals and signed diversions.",
   "National Highways carries the M3 to the east at junction 4 and the fast A331 Blackwater Valley Route down the eastern edge of the town, the primary relief route for airshow flows, while the A325 Farnborough Road is the local spine. Motorway, dual-carriageway and event work alike mean fast roads and intensive coordination.",
   "Surfacing, lining, drainage, lighting and winter gritting are all handled by Farnborough crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the area's carriageway, event-route and winter-maintenance work",
  "s2_intro":"Across Farnborough's M Group Highways carriageway work and the National Highways M3 and A331",
 },
 "torquay": {
  "region":"Torquay and Torbay",
  "nearby":["Paignton","Newton Abbot","Exeter"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Torquay's highway maintenance teams and roadworks contractors, from Torbay Council's SWISCo delivery company to National Highways work on the A380 South Devon Highway, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Torquay area's roads running",
  "s1loc":[
   "Torquay is the largest town in Torbay and the heart of the English Riviera, a coastal resort whose seafront roads and promenades carry a heavy seasonal tourism surge each summer. Torbay Council is the unitary highway authority, and its gangs work in Class 3 hi-vis on salt-exposed seafront roads where surface quality is a commercial sensitivity.",
   "Rather than outsourcing to a national term contractor, the council delivers highways and street-scene work through SWISCo, the council-owned company set up in 2020 when the previous TOR2 arrangement ended and services were brought back in house, covering pothole repair, drainage and street lighting. Maintenance scheduling has to work around the summer peak.",
   "National Highways carries the A380 as the strategic link to the wider Devon network, including the South Devon Highway dual carriageway opened in 2015 that bypassed Kingskerswell, while the A3022 connects the town centre to the A380. Resort-corridor and trunk work alike mean exposed conditions and seasonal pressure.",
   "Resurfacing, lining, drainage, lighting, seafront work and winter gritting put Torquay crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the resort's carriageway, seafront and winter-maintenance work",
  "s2_intro":"Across Torquay's SWISCo carriageway work and the National Highways A380",
 },
 "inverness": {
  "region":"Inverness and the Highlands",
  "nearby":["Elgin","Perth","Aberdeen"],
  "snapshot":"iNeedWorkwear kits Inverness highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from Highland Council to Transport Scotland trunk roads run by BEAR Scotland on the A9, A82 and A96, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Inverness area's roads running",
  "s1loc":[
   "Inverness is the Highland capital and the service hub for a vast, sparsely populated hinterland, which makes road connectivity disproportionately important to its economy. Highland Council is the unitary roads authority for the largest council area in the UK, over four thousand miles of local road, and its gangs work in Class 3 hi-vis across that immense network.",
   "The council runs local roads largely through in-house labour with specialist term contracts, awarding Thermal Road Repairs a two-year patching deal in 2025 after a successful trial, while Tarmac appears on its supplier register. The sheer scale of the network, reaching out to Sutherland, Caithness and Wester Ross, demands depots spread across the region.",
   "In Scotland trunk roads are Transport Scotland's responsibility, maintained in the north by BEAR Scotland, covering the A9 to Perth, the A82 along the Great Glen and the A96 to Aberdeen, with the multi-billion-pound A9 dualling programme and a four-million-pound strengthening of the Kessock Bridge under way. Trunk and local work alike mean long distances and harsh winters.",
   "Surfacing, lining, drainage, lighting and heavy winter gritting are all handled by Inverness crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the Highland capital's carriageway, rural-trunk and winter-maintenance work",
  "s2_intro":"Across Inverness council carriageway work and the Transport Scotland A9, A82 and A96",
 },
 "wrexham": {
  "region":"Wrexham and North Wales",
  "nearby":["Oswestry","Shrewsbury","Buckley"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Wrexham's highway maintenance teams and roadworks contractors, from Wrexham County Borough Council to Welsh Government trunk roads managed by the North and Mid Wales Trunk Road Agent on the A483 and A55, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Wrexham area's roads running",
  "s1loc":[
   "Wrexham is the largest town in North Wales and a designated growth town, anchored by Wrexham Industrial Estate, one of the largest in Wales, which pushes heavy haulage onto the surrounding network. Wrexham County Borough Council is the Welsh unitary highway authority, and its gangs work in Class 3 hi-vis across town and cross-border routes.",
   "The council maintains local roads through in-house resource and term contracts and works a sub-depot at Miners Park, Llay, while the trunk network is the Welsh Government's responsibility through the North and Mid Wales Trunk Road Agent, which procures surfacing, drainage and civil works on the A483 and A5 via 2025 frameworks. Cross-boundary flows with England add coordination.",
   "Welsh Government trunk roads carry the A483 north-south through the area toward the A55 North Wales Expressway near Chester, with the A534 a key cross-border link and recent restrictions at the Ruabon interchange and Newbridge bypass for maintenance. Trunk and county work alike mean fast roads and bilingual signing.",
   "Resurfacing, lining, drainage, lighting and winter gritting put Wrexham crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the area's carriageway, cross-border-route and winter-maintenance work",
  "s2_intro":"Across Wrexham's council carriageway work and the Welsh Government A483 and A55",
 },
 "loughborough": {
  "region":"Loughborough and Leicestershire",
  "nearby":["Leicester","Nottingham","Coalville"],
  "snapshot":"iNeedWorkwear kits Loughborough's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from Leicestershire County Council's Aggregate Industries patching contract to National Highways work on the M1, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Loughborough area's roads running",
  "s1loc":[
   "Loughborough sits close to the M1 at junction 23 and is home to one of the country's leading technical universities, whose large student and research population shapes travel on the A6 and surrounding roads. Leicestershire County Council is the highway authority, and its gangs work in Class 3 hi-vis across the Charnwood network.",
   "The county delivers carriageway patching and repair through a joint contract with Leicester City awarded to Aggregate Industries in 2023, worth up to around forty-seven million pounds over five years across three thousand miles of road, and uses the Midlands Highway Alliance Plus framework for larger schemes. The Loughborough and Shepshed growth corridor adds development-driven works.",
   "National Highways carries the M1 to the west at junction 23, where the A512 approach has been upgraded to dual carriageway, and retrofitted emergency areas between junctions 23a and 25 in a programme completed in early 2025, while the A6 runs through the town toward Derby and Leicester. Motorway and A-road work alike mean fast roads and overnight closures.",
   "Surfacing, lining, drainage, lighting and winter gritting are all handled by Loughborough crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the area's carriageway, growth-corridor and winter-maintenance work",
  "s2_intro":"Across Loughborough's Aggregate Industries carriageway work and the National Highways M1 and A512",
 },
 "stourbridge": {
  "region":"Stourbridge and the Black Country",
  "nearby":["Dudley","Halesowen","Brierley Hill"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Stourbridge's highway maintenance teams and roadworks contractors, from Dudley Council and the Black Country highways framework to National Highways work on the M5, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Stourbridge area's roads running",
  "s1loc":[
   "Stourbridge is the home of the internationally recognised Glass Quarter, centred on Amblecote and Wordsley along the A491, where over four hundred years of glassmaking sit directly beside an active town-centre corridor. Dudley Metropolitan Borough Council is the highway authority, and its gangs work in Class 3 hi-vis at the south-western tip of the Black Country.",
   "Dudley maintains roads through the Black Country collaborative highways framework led by Wolverhampton on behalf of the four boroughs, with Colas among the appointed surfacing contractors and a successor framework worth around one hundred and fifty million pounds running from April 2026. The town sits where the dense conurbation grid gives way to the rural Worcestershire fringe.",
   "National Highways carries the M5 to the south-east at junctions 3 and 4, while the A491 forms the spine of the Stourbridge ring road and runs north toward Wolverhampton, the A458 links east to Birmingham and the A449 heads south to Kidderminster. Motorway and ring-road work alike mean varied carriageway types and tight management.",
   "Resurfacing, lining, drainage, lighting and winter gritting put Stourbridge crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the area's carriageway, ring-road and winter-maintenance work",
  "s2_intro":"Across Stourbridge's Black Country framework carriageway work and the National Highways M5",
 },
 "ellesmere port": {
  "region":"Ellesmere Port and Cheshire",
  "nearby":["Birkenhead","Bebington","Bromborough"],
  "snapshot":"iNeedWorkwear kits Ellesmere Port's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from Cheshire West and Chester Council's Colas delivery partnership to National Highways work on the M53 and M56, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Ellesmere Port area's roads running",
  "s1loc":[
   "Ellesmere Port is shaped industrially by the Stanlow oil refinery, one of the UK's largest processing around twelve million tonnes of crude a year, and the Stellantis vehicle plant, both of which drive abnormal loads and heavy freight onto the M53 and A5117. Cheshire West and Chester Council is the unitary highway authority, and its gangs work in Class 3 hi-vis beside that industrial traffic.",
   "The council appointed Colas as its Highways Delivery Partner from April 2023, taking over from Ringway, supported by Waterman and by Bouygues on lighting and signals, on a contract running to 2030 with an annual value of around nineteen million pounds. The refinery and assembly plant generate access-road and reinstatement work well beyond the routine.",
   "National Highways carries the M53 down the western edge at junctions 9 to 11 where it merges into the M56, with the A5117 carrying traffic east toward the A41, and recent barrier-replacement work between junctions 9 and 11. Motorway and industrial-access work alike mean fast roads and abnormal-load planning.",
   "Surfacing, lining, drainage, lighting and winter gritting are all handled by Ellesmere Port crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the area's carriageway, industrial-access and winter-maintenance work",
  "s2_intro":"Across Ellesmere Port's Colas carriageway work and the National Highways M53 and M56",
 },
 "dewsbury": {
  "region":"Dewsbury and West Yorkshire",
  "nearby":["Batley","Huddersfield","Mirfield"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Dewsbury's highway maintenance teams and roadworks contractors, from Kirklees Council and the Yorkshire Alliance framework to National Highways work on the M1 and M62, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Dewsbury area's roads running",
  "s1loc":[
   "Dewsbury is a heavy-woollen-district market town in Kirklees, set between the Spen and Calder valleys with a ring road threading its town centre past the railway station. Kirklees Council is the metropolitan highway authority for around two thousand six hundred kilometres of road, and its gangs work in Class 3 hi-vis across those valley distributor routes.",
   "Kirklees leads the Yorkshire Alliance surfacing and planing framework shared with Bradford, Leeds, Wakefield, York and Calderdale, on which Colas holds places across all twelve lots of the eighty-eight-million-pound deal, with A E Yates also active regionally. The Connecting Kirklees capital plan keeps a steady flow of carriageway, footway and structures work in the town.",
   "National Highways carries the M1 to the east at junction 40 near Ossett and the M62 to the north at junction 28, while the A638 forms the Dewsbury ring road and the A653 links north to Leeds, with the A638 Dewsbury-Cleckheaton sustainable travel corridor a recent scheme. Motorway and distributor work alike mean fast roads and mixed freight.",
   "Resurfacing, lining, drainage, lighting and winter gritting put Dewsbury crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the area's carriageway, ring-road and winter-maintenance work",
  "s2_intro":"Across Dewsbury's Yorkshire Alliance carriageway work and the National Highways M1 and M62",
 },
 "widnes": {
  "region":"Widnes and Halton",
  "nearby":["Runcorn","Warrington","St Helens"],
  "snapshot":"iNeedWorkwear kits Widnes' highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from Halton Borough Council's Tarmac term contract to the Mersey Gateway and Silver Jubilee bridges, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Widnes area's roads running",
  "s1loc":[
   "Widnes stands on the north bank of the Mersey opposite Runcorn, defined by its two river crossings and a chemicals-manufacturing heritage that still feeds heavy goods traffic through its industrial estates. Halton Borough Council is the unitary highway authority, and its gangs work in Class 3 hi-vis beside that estuary and industrial traffic.",
   "Halton and neighbouring Warrington jointly procured a highways term maintenance contract awarded to Tarmac Trading, worth around one hundred and seventeen million pounds from 2023 to 2029, while the crossings are overseen by the Mersey Gateway Crossings Board with Merseylink as operator. The Everite Road and waterfront estates keep up a steady carriageway-reinstatement demand.",
   "National Highways carries the M62 to the north, while the A562 links west to Liverpool, the A557 Widnes Eastern Bypass runs north-south to the motorway, and the A533 crosses the Silver Jubilee Bridge to Runcorn alongside the tolled Mersey Gateway opened in 2017. Motorway, bypass and bridge work alike mean fast roads and major structures.",
   "Surfacing, lining, drainage, lighting and winter gritting are all handled by Widnes crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the area's carriageway, bridge-approach and winter-maintenance work",
  "s2_intro":"Across Widnes' Tarmac carriageway work and the Mersey Gateway and Silver Jubilee bridges",
 },
 "runcorn": {
  "region":"Runcorn and Halton",
  "nearby":["Widnes","Warrington","Prescot"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Runcorn's highway maintenance teams and roadworks contractors, from Halton Borough Council's Tarmac term contract to National Highways work on the M56 and the Mersey crossings, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Runcorn area's roads running",
  "s1loc":[
   "Runcorn sits on the south bank of the Mersey opposite Widnes, a 1960s new town whose planned grid of busways and distributor roads gives it a maintenance pattern unlike a traditional town centre. Halton Borough Council is the unitary highway authority, and its gangs work in Class 3 hi-vis across that new-town network and its two river crossings.",
   "As across the rest of the borough, highways run under the joint Halton and Warrington term contract awarded to Tarmac Trading from 2023 to 2029, with the Mersey Gateway Crossings Board and Merseylink responsible for the bridge structures themselves. The new-town distributor roads and industrial estates carry a sustained, distinctive workload.",
   "National Highways carries the M56 to the south toward Manchester and Chester, while the A557 runs through the town to the Mersey Gateway approaches and the A533 crosses the Silver Jubilee Bridge to Widnes, the older 1961 crossing reopened in 2021 after refurbishment. Motorway and bridge-approach work alike mean fast roads and major structures.",
   "Resurfacing, lining, drainage, lighting and winter gritting put Runcorn crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the new town's carriageway, bridge-approach and winter-maintenance work",
  "s2_intro":"Across Runcorn's Tarmac carriageway work and the National Highways M56 and the Mersey crossings",
 },
 "rochester": {
  "region":"Rochester and the Medway towns",
  "nearby":["Chatham","Strood","Gravesend"],
  "snapshot":"iNeedWorkwear kits Rochester's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from Medway Council's VolkerHighways term contract to National Highways work on the M2 and A2, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Rochester area's roads running",
  "s1loc":[
   "Rochester is the historic core of the Medway towns, its Norman castle and cathedral standing on the west bank of the river where three crossings carry traffic between Strood and Chatham. Medway Council is the unitary highway authority for Rochester, Chatham, Strood, Gillingham and Rainham, and its gangs work in Class 3 hi-vis across that river-divided network.",
   "Medway has run its highways and street lighting through a term contract with VolkerHighways, in place since 2017 on an arrangement worth around nine million pounds a year over eight hundred and twenty-seven kilometres of road, with the council preparing a successor as the deal nears renewal. VolkerHighways is also responsible for inspecting and maintaining the Medway Tunnel.",
   "National Highways carries the M2 north of the town across the Medway Bridge and the A2 through the Medway towns as the strategic London-to-Channel route, while the A289 Northern Relief Road runs the third crossing through the immersed-tube Medway Tunnel opened in 1996. Trunk and tunnel work alike mean heavy freight and major structures.",
   "Surfacing, lining, drainage, lighting and winter gritting are all handled by Rochester crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the area's carriageway, tunnel-approach and winter-maintenance work",
  "s2_intro":"Across Rochester's VolkerHighways carriageway work and the National Highways M2 and A2",
 },
 "twickenham": {
  "region":"Twickenham and South West London",
  "nearby":["Hounslow","Feltham","Kingston upon Thames"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Twickenham's highway maintenance teams and roadworks contractors, from Richmond upon Thames and FM Conway to the Transport for London red routes, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Twickenham area's roads running",
  "s1loc":[
   "Twickenham is home to Allianz Stadium, the national rugby union ground holding over eighty-two thousand, whose international and Six Nations match days drive intensive event traffic management across the surrounding streets. The London Borough of Richmond upon Thames is the local highway authority, and its gangs work in Class 3 hi-vis around those fixture-day closures.",
   "Richmond runs a shared public-realm and highways contract with neighbouring Wandsworth held by FM Conway, covering some three thousand six hundred streets and worth up to ninety-eight million pounds, and FM Conway also sits on the Transport for London South Area framework that covers the red routes and structures in the borough. Match-day closures on Whitton Road, Rugby Road and London Road are a fixed feature.",
   "The A316 Great Chertsey Road is a TfL-managed red route through Twickenham linking central London to the M3 at junction 1, with TfL running planned block closures for drainage, structures and markings, while the A305 Richmond Road is the local spine. Red-route and event work alike mean fast roads and tight coordination.",
   "Resurfacing, lining, drainage, lighting and winter gritting put Twickenham crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the area's carriageway, event-route and winter-maintenance work",
  "s2_intro":"Across Twickenham's FM Conway carriageway work and the TfL A316 red route",
 },
 "scarborough": {
  "region":"Scarborough and the North Yorkshire coast",
  "nearby":["Bridlington","Beverley","York"],
  "snapshot":"iNeedWorkwear kits Scarborough's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from North Yorkshire Council and its NY Highways arm to National Highways work on the A64, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Scarborough area's roads running",
  "s1loc":[
   "Scarborough is the largest settlement on the Yorkshire coast, a North Sea resort whose road links west and along the cliffs carry its visitor economy. North Yorkshire Council, the unitary authority that absorbed the old borough in 2023, is the highway authority, and its gangs work in Class 3 hi-vis from the Seamer Carr depot on the southern edge of town.",
   "Maintenance runs through NY Highways, the council-owned company launched in 2021 to bring work in house after the previous Ringway contract, operating a direct-labour model across some five thousand eight hundred miles of road alongside commercial clients. Coastal erosion along the cliff roads has brought specialist protective schemes into the programme.",
   "National Highways carries the A64 as the primary, and effectively sole, strategic link west to York and the motorway network, terminating near the railway station, while the A165 runs south toward Hull, the A170 connects to Thirsk and the A171 hugs the eroding clifftop coast toward Whitby. Trunk and coastal work alike mean long diversions and exposed sites.",
   "Surfacing, lining, drainage, lighting and winter gritting are all handled by Scarborough crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the resort's carriageway, coastal-road and winter-maintenance work",
  "s2_intro":"Across Scarborough's NY Highways carriageway work and the National Highways A64",
 },
 "orpington": {
  "region":"Orpington and South East London",
  "nearby":["Bromley","Sidcup","Sevenoaks"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Orpington's highway maintenance teams and roadworks contractors, from the London Borough of Bromley and FM Conway to National Highways work on the M25 and A21, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Orpington area's roads running",
  "s1loc":[
   "Orpington sits at the southern end of the London Borough of Bromley on the M25 and A21 commuter corridor, at the edge of the green belt where outer London meets Kent. Bromley is the local highway authority, and its gangs work in Class 3 hi-vis across a mix of residential, retail and light-industrial streets feeding that motorway junction.",
   "Bromley has used FM Conway as its term highway maintenance contractor for carriageway and footway works, reactive repair, drainage and lighting, and put a successor framework worth around seventy-one million pounds out to tender from July 2026 split into major and minor works lots. FM Conway also holds the Transport for London South Area framework covering red routes and structures in the borough.",
   "National Highways operates the M25 along the southern edge at junction 4, where it meets the A21 trunk road toward Hastings and the A224, with borough roads feeding that interchange under Bromley's own authority. Orbital-motorway and trunk-feeder work alike mean fast roads and tight management.",
   "Resurfacing, lining, drainage, lighting and winter gritting put Orpington crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the area's carriageway, commuter-corridor and winter-maintenance work",
  "s2_intro":"Across Orpington's FM Conway carriageway work and the National Highways M25 and A21",
 },
 "wallasey": {
  "region":"Wallasey and the Wirral",
  "nearby":["Birkenhead","Bebington","Liverpool"],
  "snapshot":"iNeedWorkwear kits Wallasey's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from Wirral Council's in-house highways team and Heidelberg Materials surfacing to National Highways work on the M53, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Wallasey area's roads running",
  "s1loc":[
   "Wallasey occupies the north-eastern tip of the Wirral Peninsula at the mouth of the Mersey, where the Kingsway Tunnel carries around forty-five thousand vehicles a day under the river to Liverpool. Wirral Council is the metropolitan highway authority, and its gangs work in Class 3 hi-vis on coastal approaches exposed to Liverpool Bay and the estuary.",
   "Wirral brought highway maintenance back in house in 2018 after contracts with Colas and then BAM Nuttall ended, running reactive and planned work with its own team, while Heidelberg Materials resecured the surfacing contract worth around nine million pounds over three years. The Kingsway Tunnel is operated separately by Merseytravel rather than the council.",
   "National Highways carries the M53 down the spine of the peninsula from junction 1 at Wallasey, where it meets the A554 Wallasey North Approach Road at Bidston, toward Ellesmere Port and the Chester bypass. Motorway and coastal-approach work alike mean fast roads and salt-laden, weather-exposed surfaces.",
   "Surfacing, lining, drainage, lighting and winter gritting are all handled by Wallasey crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the area's carriageway, coastal-approach and winter-maintenance work",
  "s2_intro":"Across Wallasey's council carriageway work and the National Highways M53",
 },
 "halesowen": {
  "region":"Halesowen and the Black Country",
  "nearby":["Dudley","Stourbridge","Oldbury"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Halesowen's highway maintenance teams and roadworks contractors, from Dudley Council and the Black Country highways framework to National Highways work on the M5, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Halesowen area's roads running",
  "s1loc":[
   "Halesowen sits at the southern end of the Dudley borough where the Black Country meets the Worcestershire fringe, its road network built around the A456 Manor Way bypass feeding straight into the M5. Dudley Metropolitan Borough Council is the highway authority, and its gangs work in Class 3 hi-vis on that fast dual carriageway and the streets around it.",
   "Dudley procures maintenance through the collaborative Black Country highways framework led by Wolverhampton on behalf of the four boroughs, with Colas among the appointed surfacing contractors across some three thousand six hundred kilometres of road. The Manor Way corridor sees recurring overnight resurfacing between the Grange Road and M5-link roundabouts.",
   "National Highways carries the M5 along the eastern edge at junction 3, where the A456 heads west toward Kidderminster, while the A459 runs north to Dudley town centre. Motorway-link and dual-carriageway work alike mean fast roads and motorway-adjacent traffic management.",
   "Resurfacing, lining, drainage, lighting and winter gritting put Halesowen crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the area's carriageway, bypass-corridor and winter-maintenance work",
  "s2_intro":"Across Halesowen's Black Country framework carriageway work and the National Highways M5 and A456",
 },
 "smethwick": {
  "region":"Smethwick and the Black Country",
  "nearby":["Oldbury","West Bromwich","Birmingham"],
  "snapshot":"iNeedWorkwear kits Smethwick's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from Sandwell Council and the Black Country highways framework to National Highways work on the M5 viaduct, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Smethwick area's roads running",
  "s1loc":[
   "Smethwick lies beneath the elevated M5 Oldbury viaduct, where the motorway runs on stilts over canals and dense urban fabric carrying around a hundred and twenty thousand vehicles a day between junctions 1 and 2. Sandwell Metropolitan Borough Council is the highway authority, and its gangs work in Class 3 hi-vis on the canal-side streets below.",
   "Sandwell maintains roads through the same Black Country collaborative framework led by Wolverhampton, with Colas among the appointed contractors and surface-dressing across the local network. The National Highways viaduct concrete-repair programme, one of the largest of its kind, has pushed heavy diversion pressure onto Sandwell's A-roads.",
   "National Highways operates the M5 viaduct, while the A4123 Wolverhampton Road and the A457 Oldbury Road form the Key Route Network spine through the borough toward Birmingham. Elevated-motorway and arterial work alike mean fast roads and constant diversion coordination.",
   "Surfacing, lining, drainage, lighting and winter gritting are all handled by Smethwick crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the area's carriageway, arterial-road and winter-maintenance work",
  "s2_intro":"Across Smethwick's Black Country framework carriageway work and the National Highways M5 viaduct",
 },
 "brierley hill": {
  "region":"Brierley Hill and the Black Country",
  "nearby":["Dudley","Stourbridge","Kingswinford"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Brierley Hill's highway maintenance teams and roadworks contractors, from Dudley Council and the Black Country highways framework alongside the Wednesbury to Brierley Hill Metro works, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Brierley Hill area's roads running",
  "s1loc":[
   "Brierley Hill is dominated by the Merry Hill shopping centre, one of the region's biggest retail destinations, with the A461 and A4036 carrying its constant flows. Dudley Metropolitan Borough Council is the highway authority, and its gangs work in Class 3 hi-vis around the Waterfront and the busy roundabouts that serve Merry Hill.",
   "Dudley maintains roads through the Black Country collaborative framework led by Wolverhampton, with Colas among the appointed surfacing contractors, while the Wednesbury to Brierley Hill West Midlands Metro extension threads tram construction through the town toward a new Merry Hill stop. Temporary roundabouts and lane closures along The Embankment run alongside that work.",
   "National Highways operates the wider strategic network with the M5 to the east, while the council-managed A461 forms the Dudley-to-Walsall axis and the A4036 serves Merry Hill. Retail-corridor and tram-construction work alike mean heavy traffic and live-site management.",
   "Resurfacing, lining, drainage, lighting and winter gritting put Brierley Hill crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the area's carriageway, retail-corridor and winter-maintenance work",
  "s2_intro":"Across Brierley Hill's Black Country framework carriageway work and the A461 and A4036 corridors",
 },
 "kidderminster": {
  "region":"Kidderminster and Worcestershire",
  "nearby":["Stourport-on-Severn","Bromsgrove","Worcester"],
  "snapshot":"iNeedWorkwear kits Kidderminster's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from Worcestershire County Council's Ringway term contract to National Highways work on the M5, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Kidderminster area's roads running",
  "s1loc":[
   "Kidderminster is the home of the British carpet industry, its weaving heritage preserved at the Museum of Carpet in Stour Vale Mill and its manufacturing estates strung along the Stour and Worcester road corridors. Worcestershire County Council is the highway authority, and its gangs work in Class 3 hi-vis across the Wyre Forest network.",
   "The county runs its highways through Ringway, the long-standing Worcestershire term contractor, on a combined maintenance contract covering around four thousand kilometres of road and over thirteen hundred structures, with winter service and cyclical works. The A449 spine ties the town to the M5 catchment and the Black Country.",
   "National Highways operates the M5 nearby, reached via junction 3 and the A456 or junction 6 and the A449, while through the town the A449 Wolverhampton road and the A456 form the principal corridors. Trunk-access and town-spine work alike mean busy roads and steady congestion management.",
   "Surfacing, lining, drainage, lighting and winter gritting are all handled by Kidderminster crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the area's carriageway, town-spine and winter-maintenance work",
  "s2_intro":"Across Kidderminster's Ringway carriageway work and the National Highways M5 and A449",
 },
 "hereford": {
  "region":"Hereford and Herefordshire",
  "nearby":["Worcester","Malvern","Gloucester"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Hereford's highway maintenance teams and roadworks contractors, from Herefordshire Council's move to an in-house model with M Group to National Highways work on the A49, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Hereford area's roads running",
  "s1loc":[
   "Hereford is a rural cathedral city where the A49 funnels all through-traffic across the River Wye in the city centre, the long-debated western bypass over the river still the defining infrastructure question. Herefordshire Council is the unitary highway authority for a large rural network, and its gangs work in Class 3 hi-vis on city-crossing and far-flung county roads alike.",
   "After the long-running Balfour Beatty Living Places public-realm contract ended in 2026, the council moved oversight back in house with M Group as delivery partner plus a framework of approved local contractors at agreed rates. Phase 1 of the Hereford bypass, linking the A49 to the A465 with Graham appointed to build it, has kept major roadworks on the agenda.",
   "National Highways carries the A49 north-south through the city and across the Wye as the strategic route between Ross-on-Wye and Shrewsbury, with the A465 the Abergavenny road and the A438 heading toward Ledbury. Trunk and rural work alike mean long, dispersed sites and a single critical river crossing.",
   "Resurfacing, lining, drainage, lighting and winter gritting put Hereford crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the city's carriageway, rural-road and winter-maintenance work",
  "s2_intro":"Across Hereford's in-house and M Group carriageway work and the National Highways A49",
 },
 "tunbridge wells": {
  "region":"Tunbridge Wells and Kent",
  "nearby":["Tonbridge","Sevenoaks","Crowborough"],
  "snapshot":"iNeedWorkwear kits Tunbridge Wells' highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from Kent County Council's Ringway term contract to National Highways work on the A21, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Tunbridge Wells area's roads running",
  "s1loc":[
   "Royal Tunbridge Wells is a Wealden spa town where the A21 carries traffic from the M25 down toward Hastings and the dualled section at Pembury serves the hospital corridor. Kent County Council is the highway authority, and its gangs work in Class 3 hi-vis on the A-roads radiating through the wooded Weald.",
   "Kent moved its highways term maintenance to Ringway, a Vinci subsidiary, from May 2026 under a twenty-one-year contract worth around fifty million pounds a year, taking over from Amey after twelve years. The North Farm industrial estate on the town's edge is the local hub for plant hire and trade supply to highways crews.",
   "National Highways operates the A21 to the east as the strategic spine, while the council-managed A26 runs to Tonbridge and the A267 heads south toward Mayfield. Trunk-corridor and Wealden A-road work alike mean fast roads and tight management. The A21 Tonbridge to Pembury dualling, opened in 2017, remains the area's reference scheme.",
   "Surfacing, lining, drainage, lighting and winter gritting are all handled by Tunbridge Wells crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the area's carriageway, Wealden-road and winter-maintenance work",
  "s2_intro":"Across Tunbridge Wells' Ringway carriageway work and the National Highways A21",
 },
 "canterbury": {
  "region":"Canterbury and Kent",
  "nearby":["Whitstable","Herne Bay","Faversham"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Canterbury's highway maintenance teams and roadworks contractors, from Kent County Council's Ringway term contract to National Highways work on the A2 and M2, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Canterbury area's roads running",
  "s1loc":[
   "Canterbury is a cathedral city whose tight inner ring road shapes almost all of its traffic management, with the A2 outside following the line of the Roman Watling Street toward Dover. Kent County Council is the highway authority, and its gangs work in Class 3 hi-vis on the ring road and the radial routes into the historic core.",
   "As across Kent, the county term maintenance contract passed to Ringway from May 2026 after twelve years with Amey, covering pothole repair, gritting, drainage and structures on the twenty-one-year deal. The council has run overnight resurfacing on the A299 Thanet Way with phased night-time closures toward the coast.",
   "National Highways carries the A2 past the city and the M2 to the west, while the council-managed A28 runs toward Ashford and Thanet and the A299 Thanet Way heads to Whitstable and Herne Bay. Trunk-corridor and ring-road work alike mean heavy through-traffic and constrained city sites.",
   "Resurfacing, lining, drainage, lighting and winter gritting put Canterbury crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the city's carriageway, ring-road and winter-maintenance work",
  "s2_intro":"Across Canterbury's Ringway carriageway work and the National Highways A2 and M2",
 },
 "folkestone": {
  "region":"Folkestone and Kent",
  "nearby":["Hythe","Dover","Ashford"],
  "snapshot":"iNeedWorkwear kits Folkestone's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from Kent County Council's Ringway term contract to National Highways work on the M20 and the Eurotunnel approaches, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Folkestone area's roads running",
  "s1loc":[
   "Folkestone is the British end of the Channel Tunnel, where the M20 runs down to the Eurotunnel terminal at Cheriton and cross-Channel freight dominates the strategic network. Kent County Council is the highway authority, and its gangs work in Class 3 hi-vis on the local roads beneath that motorway and terminal traffic.",
   "Kent's county term maintenance contract moved to Ringway from May 2026 after Amey's twelve years, on the twenty-one-year, roughly fifty-million-pounds-a-year deal covering repairs, gritting, drainage and emergency response. The Eurotunnel terminal is a major operational site that interacts constantly with highway works in the area.",
   "National Highways operates the M20 as the dominant route from the M25 to the coast, runs Operation Brock between junctions 8 and 9 to queue Europe-bound lorries during cross-Channel disruption, and manages the A20 toward Dover, while the council holds the A259 coast road. Motorway, terminal and coast-road work alike mean fast roads and freight resilience.",
   "Surfacing, lining, drainage, lighting and winter gritting are all handled by Folkestone crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the area's carriageway, terminal-approach and winter-maintenance work",
  "s2_intro":"Across Folkestone's Ringway carriageway work and the National Highways M20 and A20",
 },
 "horsham": {
  "region":"Horsham and West Sussex",
  "nearby":["Crawley","Haywards Heath","Burgess Hill"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Horsham's highway maintenance teams and roadworks contractors, from West Sussex County Council's VolkerHighways contract to the A24 corridor and Gatwick approaches, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Horsham area's roads running",
  "s1loc":[
   "Horsham is a West Sussex market town on the A24, the main corridor carrying commuter and freight flows north toward Dorking and the M25 and south toward Worthing. West Sussex County Council is the highway authority, and its gangs work in Class 3 hi-vis along that busy spine and the routes toward Gatwick.",
   "West Sussex re-procured its highways work in recent years, with VolkerHighways awarded the seven-year Highway Maintenance Core Services contract from April 2025 at around sixteen and a half million pounds a year, taking over from long-standing partner Balfour Beatty. Industrial estates such as Foundry Lane and Hop Oast on the town edge support the highways supply chain.",
   "The principal routes here are all county-managed A-roads feeding the National Highways M23 and M25, with the A24 the main artery, the A264 linking east toward Crawley and Gatwick and the A281 running southwest toward Guildford. Corridor and airport-related work alike mean heavy flows and resilience planning.",
   "Resurfacing, lining, drainage, lighting and winter gritting put Horsham crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the area's carriageway, A24-corridor and winter-maintenance work",
  "s2_intro":"Across Horsham's VolkerHighways carriageway work and the A24 and A264 corridors",
 },
 "eastleigh": {
  "region":"Eastleigh and Hampshire",
  "nearby":["Southampton","Winchester","Fareham"],
  "snapshot":"iNeedWorkwear kits Eastleigh's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from Hampshire County Council's M Group Highways contract to National Highways work on the M3 and M27, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Eastleigh area's roads running",
  "s1loc":[
   "Eastleigh sits in the angle of the M3 and M27, a railway-engineering town whose Eastleigh Works built locomotives and carriages and still anchors its industrial estates off the A335. Hampshire County Council is the highway authority for one of the largest networks in England, and its gangs work in Class 3 hi-vis between those two motorways.",
   "Hampshire Highways runs through the long-term term contract held by the former Milestone Infrastructure, now trading as M Group Highways after the 2025 rebrand and extended to 2029, covering on the order of eight thousand five hundred kilometres of carriageway. National Highways concrete-overlay resurfacing on the M27 has driven overnight closures nearby.",
   "National Highways carries the M3 toward London and Southampton and the M27 along the south coast, meeting near junction 14 and M27 junction 4, while the council-managed A335 links the town to the motorways and Southampton Airport. Motorway and airport-access work alike mean fast roads and tight management.",
   "Surfacing, lining, drainage, lighting and winter gritting are all handled by Eastleigh crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the area's carriageway, motorway-access and winter-maintenance work",
  "s2_intro":"Across Eastleigh's M Group Highways carriageway work and the National Highways M3 and M27",
 },
 "dunfermline": {
  "region":"Dunfermline and Fife",
  "nearby":["Kirkcaldy","Glenrothes","Edinburgh"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Dunfermline's highway maintenance teams and roadworks contractors, from Fife Council to Transport Scotland trunk roads on the M90 and the Queensferry Crossing, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Dunfermline area's roads running",
  "s1loc":[
   "Dunfermline is Scotland's newest city, granted city status in 2022, sitting at the northern end of the Queensferry Crossing where the M90 forms the main gateway between Fife and Edinburgh. Fife Council is the unitary roads authority, and its gangs work in Class 3 hi-vis across west Fife local roads beside that motorway corridor.",
   "The council runs an annual Area Roads Programme for the Dunfermline area through its own roads service and appointed contractors, handling structural repair, resurfacing and surface dressing, with larger schemes such as the A994 and Glen Bridge works let to outside firms. Industrial estates at Pitreavie and Halbeath sit close to the M90.",
   "In Scotland trunk roads are Transport Scotland's responsibility, with the M90 and the Queensferry Crossing maintained by BEAR Scotland from its unit office at the Forth crossings, carrying out cable, expansion-joint and barrier work on the bridge. Local and trunk work alike mean fast roads and major-structure proximity.",
   "Surfacing, lining, drainage, lighting and winter gritting are all handled by Dunfermline crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the area's carriageway, bridge-corridor and winter-maintenance work",
  "s2_intro":"Across Dunfermline's Fife Council carriageway work and the Transport Scotland M90 and Queensferry Crossing",
 },
 "livingston": {
  "region":"Livingston and West Lothian",
  "nearby":["Bathgate","Edinburgh","Falkirk"],
  "snapshot":"iNeedWorkwear kits Livingston's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from West Lothian Council to Transport Scotland trunk roads on the M8 corridor, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Livingston area's roads running",
  "s1loc":[
   "Livingston is a Scottish new town designated in 1962 and built around a purpose-made network of dual-carriageway distributor roads, roundabouts and grade-separated junctions feeding the M8. West Lothian Council is the unitary roads authority, and its gangs work in Class 3 hi-vis across that engineered distributor layout.",
   "The council maintains local roads and the extensive distributor network, including the A899 spine, largely through its in-house roads service with contractor support. Major industrial and distribution estates at Houstoun, Deans, Brucefield and Kirkton reflect the new town's economic base and add heavy traffic to the network.",
   "In Scotland trunk roads are Transport Scotland's responsibility, with the M8 just north of the town and the M8 and M9 slip roads and bridges maintained by BEAR Scotland, while the A899 and A779 form the town's primary spine. New-town distributor and motorway work alike mean fast roads and careful management.",
   "Resurfacing, lining, drainage, lighting and winter gritting put Livingston crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the new town's carriageway, distributor-road and winter-maintenance work",
  "s2_intro":"Across Livingston's West Lothian carriageway work and the Transport Scotland M8 corridor",
 },
 "hamilton": {
  "region":"Hamilton and Lanarkshire",
  "nearby":["Motherwell","East Kilbride","Wishaw"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Hamilton's highway maintenance teams and roadworks contractors, from South Lanarkshire Council to Transport Scotland trunk roads on the M74, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Hamilton area's roads running",
  "s1loc":[
   "Hamilton is the administrative base of South Lanarkshire Council, whose headquarters on Almada Street sit directly beside the M74, the principal motorway artery between Glasgow and the south. The council is the unitary roads authority, and its gangs work in Class 3 hi-vis on local roads through its Hamilton area office.",
   "Maintenance is delivered in-house with contractor support across local roads, footways, bridges and signals, with the Hamilton roads area office coordinating the network. Industrial sites around Blantyre and the Hamilton International Technology Park add commercial traffic to the local road system.",
   "In Scotland trunk roads are Transport Scotland's responsibility, with the M74 and the surrounding Lanarkshire motorways maintained in the south-west unit by Amey, which also holds the DBFO-style contract for the upgraded M8, M73 and M74 around Glasgow, and the Hamilton motorway services on the route. Local and trunk work alike mean fast roads and tight management.",
   "Surfacing, lining, drainage, lighting and winter gritting are all handled by Hamilton crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the area's carriageway, motorway-corridor and winter-maintenance work",
  "s2_intro":"Across Hamilton's South Lanarkshire carriageway work and the Transport Scotland M74",
 },
 "barrow-in-furness": {
  "region":"Barrow-in-Furness and Cumbria",
  "nearby":["Ulverston","Kendal","Lancaster"],
  "snapshot":"iNeedWorkwear kits Barrow-in-Furness highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from Westmorland and Furness Council to National Highways work on the A590, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Barrow-in-Furness area's roads running",
  "s1loc":[
   "Barrow-in-Furness is home to the BAE Systems submarine shipyard, the UK's largest by workforce and still growing, served by the long, mostly single-carriageway A590 as its lifeline to the M6. Westmorland and Furness Council, the unitary created in 2023 from the former Cumbria County Council, is the highway authority, and its gangs work in Class 3 hi-vis across the Furness peninsula.",
   "The new unitary inherited Cumbria's highways responsibilities and maintains roads, bridges and drainage through its highways service and term contractors, running resurfacing, surface dressing and a major pothole-prevention programme. The shipyard and port concentrate heavy-vehicle traffic on the approaches into the town.",
   "National Highways carries the A590 from M6 junction 36 through Ulverston to Barrow and Walney, with the A595 the other principal route, the constrained single-carriageway nature of the A590 making its resilience a recurring strategic issue. Trunk and peninsula work alike mean long routes and exposed conditions.",
   "Resurfacing, lining, drainage, lighting and winter gritting put Barrow crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the area's carriageway, peninsula-route and winter-maintenance work",
  "s2_intro":"Across Barrow-in-Furness council carriageway work and the National Highways A590",
 },
 "lancaster": {
  "region":"Lancaster and Lancashire",
  "nearby":["Morecambe","Preston","Kendal"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Lancaster's highway maintenance teams and roadworks contractors, from Lancashire County Council to National Highways work on the M6 and the Bay Gateway, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Lancaster area's roads running",
  "s1loc":[
   "Lancaster combines the M6 corridor, a major university driving growth at junction 33, and the Bay Gateway link road that reshaped traffic by connecting Morecambe and Heysham directly to the motorway. Lancashire County Council is the highway authority for around four thousand six hundred miles of road, and its gangs work in Class 3 hi-vis across that mix of motorway, link-road and city routes.",
   "The county maintains local roads, bridges and drainage through its highways service and term contractors, running resurfacing and a Lancaster district highways masterplan. The A6070, the former M6 Lancaster bypass spur, had its motorway status removed in 2023 to enable major bridge-bearing and drainage works funded by a nine-point-two-million-pound grant.",
   "National Highways carries the M6 at junctions 33 and 34, with the A6 the main north-south local artery and the A683 Bay Gateway, a dual carriageway opened in 2016 carrying over eighteen thousand vehicles a day, linking Heysham to junction 34. Motorway, link-road and city work alike mean fast roads and varied sites.",
   "Surfacing, lining, drainage, lighting and winter gritting are all handled by Lancaster crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the area's carriageway, link-road and winter-maintenance work",
  "s2_intro":"Across Lancaster's Lancashire carriageway work and the National Highways M6 and A683",
 },
 "bebington": {
  "region":"Bebington and the Wirral",
  "nearby":["Birkenhead","Bromborough","Heswall"],
  "snapshot":"iNeedWorkwear kits Bebington's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from Wirral Council's in-house highways team and Heidelberg Materials surfacing to National Highways work on the M53, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Bebington area's roads running",
  "s1loc":[
   "Bebington sits on the eastern Wirral beside Port Sunlight, the Lever Brothers Victorian model village, on the industrial-and-residential belt between Birkenhead and Bromborough. Wirral Council is the metropolitan highway authority, and its gangs work in Class 3 hi-vis along the A41 New Chester Road and the streets around it.",
   "Wirral runs its highways function in house, having taken management directly to its own team after working through BAM Nuttall, while Heidelberg Materials is the main surfacing contractor and resecured a roughly nine-million-pound carriageway resurfacing deal in recent years with an interest in lower-carbon asphalt. The eastern Wirral corridor carries steady commercial traffic.",
   "National Highways operates the M53 to the west, the nineteen-mile Wirral motorway running from the Kingsway tunnel south to the A55 near Chester with access around junction 4, while the council-managed A41 New Chester Road is the historic Birkenhead-to-Chester artery through Rock Ferry and New Ferry. Motorway and arterial work alike mean fast roads and tight management.",
   "Resurfacing, lining, drainage, lighting and winter gritting put Bebington crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the area's carriageway, arterial-road and winter-maintenance work",
  "s2_intro":"Across Bebington's council carriageway work and the National Highways M53 and A41",
 },
 "crosby": {
  "region":"Crosby and Sefton",
  "nearby":["Bootle","Formby","Liverpool"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Crosby's highway maintenance teams and roadworks contractors, from Sefton Council and its Dowhigh term contract to National Highways and the A5036 dock-road corridor, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Crosby area's roads running",
  "s1loc":[
   "Crosby sits on the Sefton coast north of Liverpool, where Antony Gormley's Another Place spreads a hundred cast-iron figures along the foreshore and the A565 carries both seaside and dock traffic. Sefton Council is the metropolitan highway authority, and its gangs work in Class 3 hi-vis along that coastal arterial.",
   "Sefton delivers highway and drainage maintenance through annual and term service contracts, with Dowhigh of Netherton acting as prime contractor in recent years and supporting works under the Liverpool City Region framework. Junction upgrades and town-centre regeneration on the A565 have featured in the recent programme.",
   "National Highways operates the wider strategic network, while locally the A565 is the coastal corridor linking Liverpool to Formby and Southport and the A5036 is the principal docks access route toward the Port of Liverpool. Coastal-corridor and dock-road work alike mean salt-exposed surfaces and heavy port traffic.",
   "Surfacing, lining, drainage, lighting and winter gritting are all handled by Crosby crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the area's carriageway, coastal-corridor and winter-maintenance work",
  "s2_intro":"Across Crosby's Dowhigh carriageway work and the A565 and A5036 corridors",
 },
 "macclesfield": {
  "region":"Macclesfield and Cheshire",
  "nearby":["Congleton","Wilmslow","Buxton"],
  "snapshot":"iNeedWorkwear kits Macclesfield's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from Cheshire East Council's Ringway Jacobs term contract to National Highways and the A523 Silk Road corridor, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Macclesfield area's roads running",
  "s1loc":[
   "Macclesfield is a historic silk-manufacturing town on the edge of the Peak District, its weaving heritage commemorated in the A523 Silk Road bypass and its economy anchored by AstraZeneca's large pharmaceutical campus at Hurdsfield. Cheshire East Council is the unitary highway authority for around sixteen hundred miles of road, and its gangs work in Class 3 hi-vis across that hill-edge network.",
   "The council delivers highways through a long-term term-maintenance contract with Ringway Jacobs, which has held Cheshire East work since 2011 and won a renewed deal from October 2018 running up to fifteen years across carriageways, footways and cycleways. The Silk Road, A537 and A536 convergence is a known congestion point.",
   "National Highways operates the wider strategic network, while the council-managed A523 Silk Road carries the north-south route from Manchester and Poynton, the A537 links Knutsford to Buxton and the A536 runs to Congleton, with recent bridge-joint and footway work on the Gas Road Bridge. Bypass and A-road work alike mean busy roads and structures maintenance.",
   "Resurfacing, lining, drainage, lighting and winter gritting put Macclesfield crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the area's carriageway, bypass-corridor and winter-maintenance work",
  "s2_intro":"Across Macclesfield's Ringway Jacobs carriageway work and the A523 Silk Road corridor",
 },
 "keighley": {
  "region":"Keighley and West Yorkshire",
  "nearby":["Bingley","Shipley","Bradford"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Keighley's highway maintenance teams and roadworks contractors, from Bradford Council and the Yorkshire Highways Alliance framework to the A629 and A650 Aire Valley corridors, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Keighley area's roads running",
  "s1loc":[
   "Keighley sits at the confluence of the Aire and the Worth, a former mill town that is the gateway to the Worth Valley and its heritage steam railway to Haworth. The City of Bradford Metropolitan District Council is the highway authority, and its gangs work in Class 3 hi-vis along the valley-floor routes and the steep streets above them.",
   "Bradford procures major and framework highway works through the Yorkshire Highways Alliance shared with Leeds, Wakefield, Kirklees, Calderdale and York, with regional contractors including Colas securing Alliance work in recent years, and runs winter service from the Stockbridge depot in Keighley. Mill sites along the Aire and Worth add reinstatement work.",
   "National Highways operates the wider strategic network, while the council-managed A629 diverts the Skipton-to-Halifax route through the town and the A650 carries Airedale through-traffic, the two forming a long-running valley improvement corridor. Crossroads and valley work alike mean busy roads and constrained sites.",
   "Surfacing, lining, drainage, lighting and winter gritting are all handled by Keighley crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the area's carriageway, valley-corridor and winter-maintenance work",
  "s2_intro":"Across Keighley's Yorkshire Alliance carriageway work and the A629 and A650 corridors",
 },
 "washington": {
  "region":"Washington and Wearside",
  "nearby":["Sunderland","Chester-le-Street","Houghton le Spring"],
  "snapshot":"iNeedWorkwear kits Washington's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from Sunderland City Council and its surfacing contractor to National Highways work on the A1(M) and A19, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Washington area's roads running",
  "s1loc":[
   "Washington was designated a new town in 1964, planned as eighteen residential villages and built beside the A1(M), and is dominated by the Nissan Sunderland car plant, the UK's largest car factory. Sunderland City Council is the metropolitan highway authority, and its gangs work in Class 3 hi-vis on the automotive-logistics corridors that ring the town.",
   "The council delivers its highway maintenance programme through its in-house Highway Operations Section with its surfacing contractor Northumbrian Roads, a partner of over twenty-five years, while Esh has delivered major schemes such as the Strategic Transport Corridor. The town's roughly ten industrial estates, several named after northern engineers, add heavy traffic.",
   "National Highways carries the A1(M) along the western edge with Washington Services between junctions 64 and 65, fed by the A194(M), while the A19 dual carriageway runs east toward the Tyne tunnels and Nissan and the A1231 Sunderland Highway links the villages to the motorway. Trunk and distributor work alike mean fast roads and heavy freight.",
   "Resurfacing, lining, drainage, lighting and winter gritting put Washington crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the new town's carriageway, logistics-corridor and winter-maintenance work",
  "s2_intro":"Across Washington's Sunderland carriageway work and the National Highways A1(M) and A19",
 },
 "merthyr tydfil": {
  "region":"Merthyr Tydfil and the South Wales Valleys",
  "nearby":["Aberdare","Pontypridd","Caerphilly"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Merthyr Tydfil's highway maintenance teams and roadworks contractors, from Merthyr Tydfil County Borough Council to Welsh Government trunk roads on the A470 and the A465 Heads of the Valleys, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Merthyr Tydfil area's roads running",
  "s1loc":[
   "Merthyr Tydfil is the smallest county borough in Wales, set at the head of the valleys where the A470 spine runs south to Cardiff and the M4 and the A465 Heads of the Valleys road crosses the upland terrain. Merthyr Tydfil County Borough Council is the Welsh unitary highway authority, and its gangs work in Class 3 hi-vis on those steep valley roads.",
   "The council maintains adopted highways through its own highways operations team and external term and call-off contractors for resurfacing, surveys and structures. The defining local scheme is the A465 dualling of Sections 5 and 6 from Dowlais Top to Hirwaun, the first road delivered through the Welsh Government's Mutual Investment Model with the Future Valleys consortium.",
   "Trunk roads in Wales are the Welsh Government's responsibility via Traffic Wales, with the South Wales Trunk Road Agent as delivery agent managing the A470 and A465 through the borough alongside framework contractors including Alun Griffiths. Trunk and valley work alike mean upland conditions and major civils nearby.",
   "Surfacing, lining, drainage, lighting and winter gritting are all handled by Merthyr crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the area's carriageway, valley-road and winter-maintenance work",
  "s2_intro":"Across Merthyr Tydfil's council carriageway work and the Welsh Government A470 and A465",
 },
 "barry": {
  "region":"Barry and the Vale of Glamorgan",
  "nearby":["Cardiff","Penarth","Bridgend"],
  "snapshot":"iNeedWorkwear kits Barry's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from the Vale of Glamorgan Council to Welsh Government trunk roads near the A48, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Barry area's roads running",
  "s1loc":[
   "Barry is a port and seaside town on the South Wales coast, its dock estate opened in 1889 as a coal-export rival to Cardiff and Barry Island still drawing seasonal crowds. The Vale of Glamorgan Council, headquartered in the town, is the Welsh unitary highway authority, and its gangs work in Class 3 hi-vis on the dock and coastal roads.",
   "The council's Highway Maintenance Division maintains all adopted roads and footways through in-house teams and external term and call-off contractors, including a traffic-management supply and installation contract in recent years. The dock estate still shapes the town's heavy-vehicle network, with operational land concentrated around Barry Docks.",
   "Trunk roads in Wales are the Welsh Government's responsibility via Traffic Wales and the South Wales Trunk Road Agent, with the nearest trunk spine the A48 north of Barry linking to the M4, while the council-managed A4050 runs from Cardiff at Culverhouse Cross and the A4055 is the coastal arterial via Dinas Powys. Dock, coastal and tourist traffic alike mean mixed flows and careful management.",
   "Resurfacing, lining, drainage, lighting and winter gritting put Barry crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the area's carriageway, dock-road and winter-maintenance work",
  "s2_intro":"Across Barry's council carriageway work and the Welsh Government A48 and the A4050 corridor",
 },
 "weymouth": {
  "region":"Weymouth and Dorset",
  "nearby":["Dorchester","Poole","Bournemouth"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Weymouth's highway maintenance teams and roadworks contractors, from Dorset Council's Hanson term service contract to the A354 Weymouth Relief Road, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Weymouth area's roads running",
  "s1loc":[
   "Weymouth is a Dorset harbour town whose quayside and seafront draw heavy tourist traffic and whose A354 Weymouth Relief Road was built specifically ahead of the 2012 Olympic and Paralympic sailing on Portland. Dorset Council, the unitary created in 2019, is the highway authority, and its gangs work in Class 3 hi-vis on those coastal and harbour routes.",
   "Dorset Highways maintains the county roads, cycleways and bridges, delivering in recent years through the Highways Term Service Contract with Hanson and procuring a replacement reported at around two hundred million pounds over a proposed ten-year term. Surface treatment on the relief road has been carried out to prevent water ingress and deterioration.",
   "There is no National Highways trunk route directly at Weymouth, so the council-managed A354 from Dorchester to Weymouth and Portland, including the relief road, is the strategic spine, with the A353 running east. Relief-road and harbour-route work alike mean mixed tourist and port traffic and seasonal scheduling.",
   "Surfacing, lining, drainage, lighting and winter gritting are all handled by Weymouth crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the area's carriageway, relief-road and winter-maintenance work",
  "s2_intro":"Across Weymouth's Hanson carriageway work and the A354 Weymouth Relief Road",
 },
 "hayes": {
  "region":"Hayes and West London",
  "nearby":["Uxbridge","Ruislip","Hounslow"],
  "snapshot":"iNeedWorkwear kits Hayes' highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from the London Borough of Hillingdon to National Highways work on the M4 and the Transport for London A312, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Hayes area's roads running",
  "s1loc":[
   "Hayes grew along the Grand Union Canal industrial corridor in West London and now sits close to Heathrow, with the A312 Parkway the main route through and freight from the canal-side and Stockley Park estates feeding the airport. The London Borough of Hillingdon is the local highway authority, and its gangs work in Class 3 hi-vis across that industrial network.",
   "Hillingdon's street teams handle road and pavement repairs, highway drainage, inspections and vehicle crossings on the borough's local roads, with redevelopment of sites such as the former Nestle factory adding construction traffic. The Adler and Abenglen industrial estates off Betam Road sit close to the A312.",
   "National Highways operates the M4 just south of Hayes and the M25 further west, while within London the A312 Parkway and Hayes bypass is a Transport for London red route and the A437 Dawley Road serves the industrial corridor. Motorway, red-route and airport-freight work alike mean fast roads and three layers of highway authority.",
   "Resurfacing, lining, drainage, lighting and winter gritting put Hayes crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the area's carriageway, industrial-corridor and winter-maintenance work",
  "s2_intro":"Across Hayes' Hillingdon carriageway work, the National Highways M4 and the TfL A312",
 },
 "hornchurch": {
  "region":"Hornchurch and East London",
  "nearby":["Romford","Upminster","Ilford"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Hornchurch's highway maintenance teams and roadworks contractors, from the London Borough of Havering's Marlborough partnership to National Highways work on the M25 and the Transport for London A127, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Hornchurch area's roads running",
  "s1loc":[
   "Hornchurch sits at the eastern edge of London between the major arterials, with the A12 to the north, the A13 and A1306 to the south and the M25 forming the borough's boundary. The London Borough of Havering is the local highway authority, and its gangs work in Class 3 hi-vis on the borough streets feeding those routes.",
   "Havering delivers highway maintenance, including resurfacing of roads and pavements, in partnership with Marlborough Highways in recent years, alongside the council's own teams. Industrial and depot land around Romford and the Rainham and A1306 corridor adds commercial traffic to the network.",
   "National Highways operates the M25 at the borough boundary, while within London the A127 Southend Arterial Road begins at Gallows Corner where it turns off the A12, with the A12, A13 and A127 all Transport for London red routes. Orbital-motorway and red-route work alike mean fast roads and tight coordination across authorities.",
   "Surfacing, lining, drainage, lighting and winter gritting are all handled by Hornchurch crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the area's carriageway, arterial-edge and winter-maintenance work",
  "s2_intro":"Across Hornchurch's Marlborough carriageway work, the M25 and the TfL A127",
 },
 "kettering": {
  "region":"Kettering and Northamptonshire",
  "nearby":["Corby","Wellingborough","Market Harborough"],
  "snapshot":"iNeedWorkwear kits Kettering's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from North Northamptonshire Council's Kier term contract to National Highways work on the A14, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Kettering area's roads running",
  "s1loc":[
   "Kettering sits squarely in the A14 corridor and the Northamptonshire logistics golden triangle, a national distribution hub where warehousing clusters along the trunk road and the A43. North Northamptonshire Council, the unitary created in 2021, is the highway authority, and its gangs work in Class 3 hi-vis beside that heavy goods traffic.",
   "The council runs its highways term maintenance through Kier on a contract in the order of thirty million pounds a year, covering routine, reactive and cyclical maintenance, winter service, surface dressing and safety inspections on an initial seven-year term with extensions. Kettering Business Park and Telford Way industrial estate anchor the local supply chain.",
   "National Highways carries the A14 just south of the town as the main route linking the M1 and M6 with the East Coast ports, while the A43 heads toward Corby and Northampton and the A509 to Wellingborough. Trunk-corridor and junction work around junctions 7 to 10 alike mean fast roads and heavy freight.",
   "Resurfacing, lining, drainage, lighting and winter gritting put Kettering crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the area's carriageway, logistics-corridor and winter-maintenance work",
  "s2_intro":"Across Kettering's Kier carriageway work and the National Highways A14",
 },
 "corby": {
  "region":"Corby and Northamptonshire",
  "nearby":["Kettering","Wellingborough","Market Harborough"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Corby's highway maintenance teams and roadworks contractors, from North Northamptonshire Council's Kier term contract to National Highways work on the A14 and the A43, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Corby area's roads running",
  "s1loc":[
   "Corby is a former steel town and 1950s new town whose atypical road layout reflects its industrial past, with the A43 the spine carrying traffic toward Kettering, Northampton and Stamford. North Northamptonshire Council, the unitary created in 2021, is the highway authority, and its gangs work in Class 3 hi-vis across the town's distribution-heavy network.",
   "Highways run under the same Kier term maintenance contract as the rest of North Northamptonshire, roughly thirty million pounds a year over a seven-year initial term, covering reactive and cyclical maintenance, winter service and inspections. The Earlstrees and Willowbrook estates and the Phoenix Parkway distribution operations drive heavy traffic.",
   "National Highways carries the A14 around six miles south at Kettering, while the council-managed A43, including the A43 Corby Link Road dual carriageway to the Stanion roundabout, and the A6116 serve the town and its estates. Link-road and distribution work alike mean fast roads and heavy goods vehicles.",
   "Surfacing, lining, drainage, lighting and winter gritting are all handled by Corby crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the area's carriageway, link-road and winter-maintenance work",
  "s2_intro":"Across Corby's Kier carriageway work and the National Highways A14 and the A43",
 },
 "leamington spa": {
  "region":"Leamington Spa and Warwickshire",
  "nearby":["Warwick","Kenilworth","Coventry"],
  "snapshot":"iNeedWorkwear kits Leamington Spa's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from Warwickshire County Council's Balfour Beatty contract to National Highways work on the M40, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Leamington Spa area's roads running",
  "s1loc":[
   "Royal Leamington Spa is a Regency spa town within Warwick District that has become Silicon Spa, one of the UK's largest clusters of video-games and digital studios, sitting close to the M40. Warwickshire County Council is the highway authority, and its gangs work in Class 3 hi-vis across a network mixing heritage townscape with a growing tech-employment base.",
   "The county delivers its highways through Balfour Beatty Living Places in a joint contract with Coventry and Solihull, the latest a roughly three-hundred-and-fifteen-million-pound seven-year deal covering over five thousand kilometres of road, Balfour Beatty's third consecutive term. The Tachbrook Park and Sydenham areas anchor the local business and supply base.",
   "National Highways operates the M40 at junctions 13 and 14, with the council-managed A46 dual carriageway the Warwick and Stratford corridor toward Coventry and the A452 the Kenilworth link. Motorway and dual-carriageway work alike mean fast roads and grade-separated junction maintenance.",
   "Resurfacing, lining, drainage, lighting and winter gritting put Leamington crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the area's carriageway, public-realm and winter-maintenance work",
  "s2_intro":"Across Leamington Spa's Balfour Beatty carriageway work and the National Highways M40 and A46",
 },
 "aylesbury": {
  "region":"Aylesbury and Buckinghamshire",
  "nearby":["High Wycombe","Bicester","Milton Keynes"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Aylesbury's highway maintenance teams and roadworks contractors, from Buckinghamshire Council's Balfour Beatty Living Places contract to National Highways work on the A41, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Aylesbury area's roads running",
  "s1loc":[
   "Aylesbury is a designated Garden Town with large-scale planned housing growth driving a ring of new link roads, the A41 the historic London-to-Birmingham corridor running through it. Buckinghamshire Council, the unitary created in 2020, is the highway authority, and its gangs work in Class 3 hi-vis across that expanding network.",
   "After Ringway Jacobs delivered the council's highways for around thirteen years, the Term Maintenance Contract passed to Balfour Beatty Living Places from April 2023 with Atkins as consultancy partner, covering routine and reactive maintenance, minor improvements and winter service. The South East Aylesbury Link Road and the HS2-funded Stoke Mandeville Relief Road have added major schemes.",
   "National Highways operates the A41 corridor, while the council-managed A413 is the Wendover and Amersham route and the A418 the Oxford Road, with the new link roads and nearby HS2 works adding realignment. Trunk, link-road and HS2-adjacent work alike mean fast roads and active construction.",
   "Surfacing, lining, drainage, lighting and winter gritting are all handled by Aylesbury crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the area's carriageway, link-road and winter-maintenance work",
  "s2_intro":"Across Aylesbury's Balfour Beatty Living Places carriageway work and the National Highways A41",
 },
 "bracknell": {
  "region":"Bracknell and Berkshire",
  "nearby":["Wokingham","Camberley","Sandhurst"],
  "snapshot":"iNeedWorkwear kits Bracknell's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from Bracknell Forest Council's Ringway term contract to National Highways work on the M4 and the A329(M), with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Bracknell area's roads running",
  "s1loc":[
   "Bracknell is a post-war new town whose centre has been rebuilt around the Lexicon scheme, generating extensive public-realm and footway works alongside its road network. Bracknell Forest Council is the Berkshire unitary highway authority, and its gangs work in Class 3 hi-vis across the new-town distributor roads and the regenerated centre.",
   "The council delivers its highways term maintenance, including winter service, through Ringway, with annual spend in the order of ten million pounds and a relationship dating back to around 2004 that has been extended to around 2028. The Western and Southern Industrial Areas and a large office base add commercial traffic.",
   "National Highways operates the M4 just to the north, while the A329(M), one of the few motorway-standard spur roads of its kind, links the town toward the M4 and Reading and the A322 is the Bagshot and Guildford corridor. Motorway-spur and distributor work alike mean fast roads and viaduct and junction maintenance.",
   "Resurfacing, lining, drainage, lighting and winter gritting put Bracknell crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the new town's carriageway, public-realm and winter-maintenance work",
  "s2_intro":"Across Bracknell's Ringway carriageway work and the National Highways M4 and A329(M)",
 },
 "cumbernauld": {
  "region":"Cumbernauld and North Lanarkshire",
  "nearby":["Falkirk","Coatbridge","Airdrie"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Cumbernauld's highway maintenance teams and roadworks contractors, from North Lanarkshire Council to Transport Scotland trunk roads on the M80, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Cumbernauld area's roads running",
  "s1loc":[
   "Cumbernauld is a post-war Scottish new town, designated in 1955 and built around a multi-level road layout and a landmark town-centre megastructure, on the corridor between Glasgow, Stirling and Falkirk. North Lanarkshire Council is the unitary roads authority, and its gangs work in Class 3 hi-vis across that engineered new-town network.",
   "The council delivers local roads maintenance, winter service and street works largely in house, while the A8011 town-centre road system is its responsibility. The Wardpark industrial estate, split by the M80 and accessed at Castlecary, hosts the logistics and manufacturing base that drives heavy traffic and roadworks demand.",
   "In Scotland trunk roads are Transport Scotland's responsibility, with the M80 through the town run under the Stepps to Haggs design-build-finance-operate concession and routine maintenance carried out by BEAR Scotland, the upgraded route having absorbed the old A80 and opened fully in 2011. New-town distributor and DBFO motorway work alike mean fast roads and tight management.",
   "Surfacing, lining, drainage, lighting and winter gritting are all handled by Cumbernauld crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the new town's carriageway, distributor-road and winter-maintenance work",
  "s2_intro":"Across Cumbernauld's North Lanarkshire carriageway work and the Transport Scotland M80",
 },
 "perth": {
  "region":"Perth and Perthshire",
  "nearby":["Dundee","Kirkcaldy","Glenrothes"],
  "snapshot":"iNeedWorkwear kits Perth's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from Perth and Kinross Council to Transport Scotland trunk roads on the A9, M90 and A90, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Perth area's roads running",
  "s1loc":[
   "Perth is the gateway to the Highlands, sitting where the A9, M90 and A90 converge with the Broxden Roundabout and the Friarton Bridge as its key structures. Perth and Kinross Council is the unitary roads authority for the city and a large rural Perthshire network, and its gangs work in Class 3 hi-vis across that convergence of strategic routes.",
   "The council maintains local roads, winter gritting and street works through its Roads Infrastructure team, with the Inveralmond industrial estate by the A9 roundabout the main distribution base. The Cross Tay Link Road, a six-kilometre route with the new Destiny Bridge over the Tay, opened in 2025 at around a hundred and fifty million pounds, the largest local road project since the Friarton Bridge.",
   "In Scotland trunk roads are Transport Scotland's responsibility, split around Perth between BEAR Scotland on the A9 and A85 and Amey on the M90 and A90. Trunk-convergence and city work alike mean fast roads and careful coordination across two operating units.",
   "Resurfacing, lining, drainage, lighting and winter gritting put Perth crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the area's carriageway, trunk-convergence and winter-maintenance work",
  "s2_intro":"Across Perth's council carriageway work and the Transport Scotland A9, M90 and A90",
 },
 "kirkcaldy": {
  "region":"Kirkcaldy and Fife",
  "nearby":["Glenrothes","Dunfermline","Perth"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Kirkcaldy's highway maintenance teams and roadworks contractors, from Fife Council to Transport Scotland trunk roads on the A92, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Kirkcaldy area's roads running",
  "s1loc":[
   "Kirkcaldy is the largest town in Fife, the Lang Toun strung along the Firth of Forth coast where a fast inland dual carriageway runs in contrast to the slower coastal esplanade route. Fife Council is the unitary roads authority, and its gangs work in Class 3 hi-vis across that mid-Fife network.",
   "The council delivers local roads maintenance, resurfacing, winter gritting and street works through its in-house Roads Services, with recent programmes targeting the A921 coastal route through the town. The contrast between the regional road and the seafront esplanade shapes the maintenance calendar.",
   "In Scotland trunk roads are Transport Scotland's responsibility, with BEAR Scotland the operating company for Fife, maintaining the A92 East Fife Regional Road that serves Kirkcaldy and runs from the M90 through Glenrothes toward Dundee. Regional-dual and coastal-route work alike mean fast roads and exposed estuary conditions.",
   "Surfacing, lining, drainage, lighting and winter gritting are all handled by Kirkcaldy crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the area's carriageway, coastal-route and winter-maintenance work",
  "s2_intro":"Across Kirkcaldy's Fife Council carriageway work and the Transport Scotland A92",
 },
 "ayr": {
  "region":"Ayr and South Ayrshire",
  "nearby":["Kilmarnock","Irvine","Paisley"],
  "snapshot":"iNeedWorkwear kits Ayr's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from the Ayrshire Roads Alliance to Transport Scotland trunk roads on the A77, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Ayr area's roads running",
  "s1loc":[
   "Ayr sits on the A77 corridor that runs south toward Stranraer and the Cairnryan ferry terminals, the main freight and passenger gateway to Northern Ireland, and serves Glasgow Prestwick Airport just to the north. South Ayrshire Council is the roads authority, and its gangs work in Class 3 hi-vis on that strategic coastal route.",
   "Local roads and transportation are delivered through the Ayrshire Roads Alliance, the shared service run jointly with East Ayrshire Council and based at London Road in Kilmarnock, handling maintenance, gritting and street works. The Heathfield industrial area on the northern edge anchors the local works and logistics base.",
   "In Scotland trunk roads are Transport Scotland's responsibility, maintained in the south-west unit by Amey since 2020, with the A77 forming the Ayr bypass and recent junction-safety work at Doonholm Road and Corton Road, while the A70 heads east to Cumnock and the A719 runs the coast. Trunk-bypass and ferry-route work alike mean fast roads and heavy freight.",
   "Resurfacing, lining, drainage, lighting and winter gritting put Ayr crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the area's carriageway, ferry-corridor and winter-maintenance work",
  "s2_intro":"Across Ayr's Ayrshire Roads Alliance carriageway work and the Transport Scotland A77",
 },
 "kilmarnock": {
  "region":"Kilmarnock and East Ayrshire",
  "nearby":["Ayr","Irvine","Paisley"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Kilmarnock's highway maintenance teams and roadworks contractors, from the Ayrshire Roads Alliance to Transport Scotland trunk roads on the A77 and A76, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Kilmarnock area's roads running",
  "s1loc":[
   "Kilmarnock is the largest town in East Ayrshire and a road hub for the region, sitting where the A77 Glasgow-to-Ayr corridor meets the A71 cross-country route and the A76 toward Dumfries. East Ayrshire Council is the roads authority, and its gangs work in Class 3 hi-vis across that Ayrshire junction of trunk and local routes.",
   "Local roads and transportation run through the Ayrshire Roads Alliance, the shared service with South Ayrshire Council headquartered on London Road in Kilmarnock, making the town the administrative centre for highway maintenance across much of Ayrshire. The Bonnyton and Moorfield industrial areas support the manufacturing and distribution base.",
   "In Scotland trunk roads are Transport Scotland's responsibility, maintained in the south-west unit by Amey, with the A77 running past the town as a dual carriageway bypass and recent resurfacing between Meiklewood and Grassyards, while the A71 is dualled toward Irvine and the A76 heads down the Nith valley. Trunk and cross-country work alike mean fast roads and tight management.",
   "Surfacing, lining, drainage, lighting and winter gritting are all handled by Kilmarnock crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the area's carriageway, trunk-junction and winter-maintenance work",
  "s2_intro":"Across Kilmarnock's Ayrshire Roads Alliance carriageway work and the Transport Scotland A77 and A76",
 },
 "llanelli": {
  "region":"Llanelli and Carmarthenshire",
  "nearby":["Swansea","Port Talbot","Neath"],
  "snapshot":"iNeedWorkwear kits Llanelli's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from Carmarthenshire County Council to Welsh Government trunk roads on the M4 and A484, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Llanelli area's roads running",
  "s1loc":[
   "Llanelli sits on the Loughor estuary at the western edge of the South Wales M4 corridor, where coastal traffic, the estuary crossing and the motorway terminus near Pont Abraham all shape its roads. Carmarthenshire County Council is the Welsh unitary highway authority, and its gangs work in Class 3 hi-vis on tidal, exposed coastal stretches.",
   "The council maintains adopted roads, footways and structures through in-house highways teams supplemented by local supply-chain contractors. The A484 Loughor Bridge, a steel-span crossing of the river completed in 1988, and the automotive-supply estates along the Llethri Road corridor feeding the M4 add distinct maintenance demand.",
   "Trunk roads in Wales are the Welsh Government's responsibility via Traffic Wales and the South Wales Trunk Road Agent, with the M4 to the east connected at junction 48 Pont Abraham by the A4138, while the A484 is the main coastal corridor toward Swansea and the A476 heads north to Cross Hands. Motorway-terminus and estuary work alike mean fast roads and tidal conditions.",
   "Resurfacing, lining, drainage, lighting and winter gritting put Llanelli crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the area's carriageway, estuary-corridor and winter-maintenance work",
  "s2_intro":"Across Llanelli's council carriageway work and the Welsh Government M4 and A484",
 },
 "neath": {
  "region":"Neath and Neath Port Talbot",
  "nearby":["Port Talbot","Swansea","Bridgend"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Neath's highway maintenance teams and roadworks contractors, from Neath Port Talbot Council to Welsh Government trunk roads on the M4 and the A465 Heads of the Valleys, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Neath area's roads running",
  "s1loc":[
   "Neath links the M4 corridor to the Vale of Neath and the A465 Heads of the Valleys route, and the town is the operational home of the South Wales Trunk Road Agent, putting it at the centre of both local and trunk-road delivery. Neath Port Talbot County Borough Council is the Welsh unitary highway authority, and its gangs work in Class 3 hi-vis across that dual role.",
   "Local maintenance runs through council highways teams and supply-chain contractors, while the council hosts SWTRA, which manages around a hundred and seventy-eight kilometres of motorway and four hundred and thirty-six of trunk road for the Welsh Government. The Port Talbot steelworks to the south-west and the Vale of Neath industry add heavy traffic.",
   "Trunk roads in Wales are the Welsh Government's responsibility via Traffic Wales and SWTRA, with the M4 passing south of Neath, the A465 running north-east up the Vale of Neath and the A474 linking toward Pontardawe, the A465 dualling programme reaching its final sections in 2025. Motorway and Heads of the Valleys work alike mean fast roads and major civils.",
   "Surfacing, lining, drainage, lighting and winter gritting are all handled by Neath crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the area's carriageway, valley-corridor and winter-maintenance work",
  "s2_intro":"Across Neath's council carriageway work and the Welsh Government M4 and A465",
 },
 "bridgend": {
  "region":"Bridgend and South Wales",
  "nearby":["Port Talbot","Maesteg","Pontypridd"],
  "snapshot":"iNeedWorkwear kits Bridgend's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from Bridgend County Borough Council to Welsh Government trunk roads on the M4, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Bridgend area's roads running",
  "s1loc":[
   "Bridgend is a classic M4-corridor manufacturing town, where around eighteen kilometres of motorway run through the county borough served by three junctions and the legacy of the major Ford engine plant near junction 36 still shapes traffic. Bridgend County Borough Council is the Welsh unitary highway authority for roughly seven hundred and ninety kilometres of road, and its gangs work in Class 3 hi-vis across it.",
   "The council maintains the adopted network and around twenty-five thousand road gullies in house with supply-chain support, handling potholes, collisions, spillages and winter service. The industrial estates at Brackla, Waterton and Pencoed feed heavy goods traffic onto the motorway junctions.",
   "Trunk roads in Wales are the Welsh Government's responsibility via Traffic Wales and the South Wales Trunk Road Agent, with the M4 served by junction 35 at Pencoed, junction 36 for the town and junction 37 at Pyle, while the A48 runs parallel as the local distributor and the A473 links toward Pontyclun. Motorway-junction and A48 diversion work alike mean fast roads and tight management.",
   "Resurfacing, lining, drainage, lighting and winter gritting put Bridgend crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the area's carriageway, motorway-junction and winter-maintenance work",
  "s2_intro":"Across Bridgend's council carriageway work and the Welsh Government M4 and A48",
 },
 "cwmbran": {
  "region":"Cwmbran and Torfaen",
  "nearby":["Pontypool","Newport","Caerphilly"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Cwmbran's highway maintenance teams and roadworks contractors, from Torfaen County Borough Council to Welsh Government trunk roads on the A4042, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Cwmbran area's roads running",
  "s1loc":[
   "Cwmbran is a post-war Welsh new town built around a planned distributor-road layout, with Cwmbran Drive feeding the A4042 trunk road and the M4 to the south. Torfaen County Borough Council is the Welsh unitary highway authority for Cwmbran, Pontypool and the wider borough, and its gangs work in Class 3 hi-vis across that new-town network.",
   "The council has committed additional capital to local road improvement in recent years and delivers maintenance through its highways teams and local contractors, with essential works including canal-bridge maintenance at Pontypool. Industrial and business estates at Llantarnam and Springvale feed the A4051 and A4042 toward the M4.",
   "Trunk roads in Wales are the Welsh Government's responsibility via Traffic Wales and the South Wales Trunk Road Agent, with the A4042 the main strategic spine running south past Cwmbran toward Newport and the M4 and north toward Pontypool and Abergavenny, the A472 crossing at Pontypool and the A4051 Cwmbran Drive the principal local distributor. Trunk and distributor work alike mean fast roads and careful management.",
   "Surfacing, lining, drainage, lighting and winter gritting are all handled by Cwmbran crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the new town's carriageway, distributor-road and winter-maintenance work",
  "s2_intro":"Across Cwmbran's council carriageway work and the Welsh Government A4042",
 },
 "bridgwater": {
  "region":"Bridgwater and Somerset",
  "nearby":["Taunton","Weston-super-Mare","Wellington"],
  "snapshot":"iNeedWorkwear kits Bridgwater's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from Somerset Council's Kier term contract to National Highways work on the M5 and the Hinkley Point C corridor, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Bridgwater area's roads running",
  "s1loc":[
   "Bridgwater is dominated by Hinkley Point C nuclear construction traffic, with EDF running park-and-ride and freight-management sites at the M5 junctions and construction lorries routed west along the A39 to the site. Somerset Council, the unitary created in 2023, is the highway authority for around four thousand miles of road, and its gangs work in Class 3 hi-vis beside that sustained nuclear-build traffic.",
   "From April 2024 the council awarded Kier its roughly two-hundred-and-twenty-five-million-pound core maintenance contract over eight years, with Kiely Bros on surface treatments and Heidelberg Materials on resurfacing, the Kier partnership inducted at the town's Canalside centre. The Express Park, Huntworth and Dunball estates generate substantial heavy goods traffic.",
   "National Highways carries the M5 through the area at junctions 23 and 24, while the A38 parallels it as the main local corridor and the A39 runs west toward Hinkley Point and the coast. Motorway-junction and nuclear-corridor work alike mean fast roads and intensive freight management.",
   "Resurfacing, lining, drainage, lighting and winter gritting put Bridgwater crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the area's carriageway, nuclear-corridor and winter-maintenance work",
  "s2_intro":"Across Bridgwater's Kier carriageway work and the National Highways M5 and A39",
 },
 "christchurch": {
  "region":"Christchurch and Dorset",
  "nearby":["Bournemouth","Poole","New Milton"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Christchurch's highway maintenance teams and roadworks contractors, from Bournemouth, Christchurch and Poole Council to National Highways work on the A35 and the A338 spur road, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Christchurch area's roads running",
  "s1loc":[
   "Christchurch sits at the eastern edge of the Bournemouth conurbation where the A35 bypass meets the A338 Bournemouth Spur Road, the area's principal arterial dual carriageway, beside the harbour fed by the Stour and Avon. Bournemouth, Christchurch and Poole Council, the unitary created in 2019, is the highway authority, and its gangs work in Class 3 hi-vis along those corridors.",
   "The council delivers highways through a Highways Term Service Contract reported at around a hundred million pounds, covering transportation and civil-engineering works alongside in-house teams. The A338 spur road reconstruction, funded through the Dorset Growth Deal at around twenty-two million pounds, involved bespoke asphalt and heathland SSSI ecological constraints on the verges.",
   "National Highways operates the wider strategic network, while the A35 trunk corridor runs east-west through the New Forest toward Southampton, the A337 heads to Lymington and the A338 spur links to the A31 and the M27. Spur-road and bypass work alike mean fast roads and protected-heathland constraints.",
   "Surfacing, lining, drainage, lighting and winter gritting are all handled by Christchurch crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the area's carriageway, spur-road and winter-maintenance work",
  "s2_intro":"Across Christchurch's BCP carriageway work and the A35 and A338 corridors",
 },
 "paignton": {
  "region":"Paignton and Torbay",
  "nearby":["Torquay","Newton Abbot","Exeter"],
  "snapshot":"iNeedWorkwear kits Paignton's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from Torbay Council's SWISCo delivery company to National Highways work on the A380 South Devon Highway, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Paignton area's roads running",
  "s1loc":[
   "Paignton is a core English Riviera resort within Torbay, its tourist traffic running the A3022 seafront corridor and access fed inland by the A380 South Devon Highway. Torbay Council is the unitary highway authority covering Torquay, Paignton and Brixham, and its gangs work in Class 3 hi-vis on the geographically constrained bay roads.",
   "Highways are delivered through SWISCo, the council-owned company that leads the network, maintaining around eighteen thousand street-lighting units, fifty-six signalised junctions and dozens of crossings across the bay. Recent works in Paignton have included Colley End Road, Underidge Drive and major town-centre gas-main and public-realm schemes, with the Yalberton industrial estate the local base.",
   "National Highways connects Torbay via the A380 South Devon Highway, a five-and-a-half-kilometre dual carriageway opened in 2015 that bypassed Kingskerswell, ending at Collaton St Mary where it meets the A3022 into Paignton and the A385 toward Totnes, with the Penn Inn flyover a key structure. Resort and link-road work alike mean seasonal flows and tight management.",
   "Resurfacing, lining, drainage, lighting, seafront work and winter gritting put Paignton crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the resort's carriageway, seafront and winter-maintenance work",
  "s2_intro":"Across Paignton's SWISCo carriageway work and the National Highways A380",
 },
 "yeovil": {
  "region":"Yeovil and Somerset",
  "nearby":["Taunton","Bridgwater","Dorchester"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Yeovil's highway maintenance teams and roadworks contractors, from Somerset Council's Kier term contract to National Highways work on the A303 and A30, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Yeovil area's roads running",
  "s1loc":[
   "Yeovil is the home of British helicopters, with the Leonardo works producing rotary-wing aircraft on a site dating to 1915 and generating heavy industrial and freight movements. Somerset Council, the unitary created in 2023, is the highway authority, and its gangs work in Class 3 hi-vis on the A30 and A303 corridor between the South West and the M3.",
   "From April 2024 Kier leads the council's core maintenance under the roughly two-hundred-and-twenty-five-million-pound contract, with improvement-scheme firms and utilities alongside, having taken over from Milestone Infrastructure with staff transferring across. The Lufton and Houndstone estates and Bunford anchor the town's industrial base.",
   "National Highways carries the A303 north of Yeovil as the strategic corridor toward the M3 and London, with the A37 running to Shepton Mallet and Dorchester and the A30 the historic east-west route, the Sparkford to Ilchester dualling a scheme on the corridor. Trunk-corridor and industrial work alike mean fast roads and heavy freight.",
   "Surfacing, lining, drainage, lighting and winter gritting are all handled by Yeovil crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the area's carriageway, trunk-corridor and winter-maintenance work",
  "s2_intro":"Across Yeovil's Kier carriageway work and the National Highways A303 and A30",
 },
 "salisbury": {
  "region":"Salisbury and Wiltshire",
  "nearby":["Amesbury","Andover","Trowbridge"],
  "snapshot":"iNeedWorkwear kits Salisbury's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from Wiltshire Council's M Group Highways contract to National Highways work on the A303 and A36, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Salisbury area's roads running",
  "s1loc":[
   "Salisbury is a cathedral city with a constrained historic core ringed by relief roads, where the A303 past Stonehenge to the north remains a single-carriageway congestion point after the tunnel scheme was cancelled. Wiltshire Council is the unitary highway authority, and its gangs work in Class 3 hi-vis around the city ring and the trunk approaches.",
   "From April 2023 the council awarded Milestone Infrastructure, now trading as M Group Highways, its roughly eighty-million-pound five-year highways contract, taking over from Ringway and covering lighting, drainage, potholes, gritting, bridges and verges with around twenty Parish Stewards working alongside town and parish councils. The Churchfields and Old Sarum estates anchor the local base.",
   "National Highways carries the A303 north via Amesbury and Stonehenge, the A36 linking Southampton to Bath through the city and the A338 toward Bournemouth, with the A303 Amesbury to Berwick Down tunnel scheme cancelled in 2024 and its consent revoked in 2026. Trunk and ring-road work alike mean fast roads and a heritage-constrained core.",
   "Resurfacing, lining, drainage, lighting and winter gritting put Salisbury crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the city's carriageway, ring-road and winter-maintenance work",
  "s2_intro":"Across Salisbury's M Group Highways carriageway work and the National Highways A303 and A36",
 },
 "havant": {
  "region":"Havant and Hampshire",
  "nearby":["Portsmouth","Fareham","Chichester"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Havant's highway maintenance teams and roadworks contractors, from Hampshire County Council's M Group Highways contract to National Highways work on the A3(M) and A27, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Havant area's roads running",
  "s1loc":[
   "Havant sits at the strategic A3(M) and A27 junction immediately north-east of Portsmouth, a key gateway for the city and Hayling Island traffic on one of the busiest stretches of the south coast. Hampshire County Council is the highway authority for one of the largest networks in England, and its gangs work in Class 3 hi-vis on that high-volume corridor.",
   "Hampshire Highways runs through the partnership with Milestone Infrastructure, now trading as M Group Highways, in place since 2017 and extended to 2029, covering over eight thousand five hundred kilometres of carriageway with tens of thousands of task orders a year and a recent road-material recycling hub. The New Lane and Brockhampton estates anchor the local base.",
   "National Highways carries the A3(M), the six-mile motorway from Horndean to Bedhampton, and the A27 east-west trunk route through the area, meeting at the A3(M) and A27 interchange with the M275 the Portsmouth spur. Motorway and busy-trunk work alike mean fast roads and frequent emergency repairs.",
   "Surfacing, lining, drainage, lighting and winter gritting are all handled by Havant crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the area's carriageway, trunk-junction and winter-maintenance work",
  "s2_intro":"Across Havant's M Group Highways carriageway work and the National Highways A3(M) and A27",
 },
 "wellingborough": {
  "region":"Wellingborough and Northamptonshire",
  "nearby":["Kettering","Rushden","Northampton"],
  "snapshot":"iNeedWorkwear kits Wellingborough's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from North Northamptonshire Council's Kier term contract to National Highways work on the A45, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Wellingborough area's roads running",
  "s1loc":[
   "Wellingborough sits on the A45 dual-carriageway corridor that feeds the A14, M1 and A1, with the Stanton Cross growth area east of the railway station adding thousands of homes and new link roads. North Northamptonshire Council, the unitary created in 2021, is the highway authority, and its gangs work in Class 3 hi-vis along that growth corridor.",
   "The council delivers highway maintenance through a term contract with Kier, commenced in September 2022 at roughly thirty million pounds a year over an initial seven-year term with extension options. The Park Farm, Denington and Finedon Road industrial estates, plus newer logistics units along the A45, drive heavy goods traffic and section-278 access works.",
   "National Highways operates the wider trunk network, while the dual-carriageway A45 is the key strategic route through the town, the A509 links north toward Kettering and the A510 crosses east-west. Trunk-corridor and growth-area work alike mean fast roads and new junction construction.",
   "Resurfacing, lining, drainage, lighting and winter gritting put Wellingborough crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the area's carriageway, growth-corridor and winter-maintenance work",
  "s2_intro":"Across Wellingborough's Kier carriageway work and the A45 corridor",
 },
 "banbury": {
  "region":"Banbury and Oxfordshire",
  "nearby":["Bicester","Leamington Spa","Daventry"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Banbury's highway maintenance teams and roadworks contractors, from Oxfordshire County Council's M Group Highways contract to National Highways work on the M40, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Banbury area's roads running",
  "s1loc":[
   "Banbury sits on the M40 at the heart of the Bicester and Banbury logistics corridor, its historic Banbury Cross the town landmark and distribution development spreading east of the motorway. Oxfordshire County Council is the highway authority, and its gangs work in Class 3 hi-vis along that freight-heavy corridor.",
   "The county runs its term maintenance through Milestone Infrastructure, now trading as M Group Highways and the long-standing incumbent since 2010, reappointed on a new contract from April 2025 covering more than four thousand eight hundred kilometres of highway, with Banbury used as a live test site for pothole-repair methods. The Wildmere Road estates and Frontier Park anchor local logistics.",
   "National Highways operates the M40 skirting the town to the east, with junction 11 the main access connecting the A422 toward Brackley and the single-carriageway A361 toward Daventry. Motorway-junction and A-road work alike mean fast roads and heavy distribution traffic.",
   "Surfacing, lining, drainage, lighting and winter gritting are all handled by Banbury crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the area's carriageway, logistics-corridor and winter-maintenance work",
  "s2_intro":"Across Banbury's M Group Highways carriageway work and the National Highways M40",
 },
 "carlton": {
  "region":"Carlton and Nottinghamshire",
  "nearby":["Nottingham","Arnold","West Bridgford"],
  "snapshot":"iNeedWorkwear kits Carlton's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from Nottinghamshire County Council's Via East Midlands company to the A612 Gedling corridor, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Carlton area's roads running",
  "s1loc":[
   "Carlton is a built-up Nottingham suburb in Gedling borough, strung along the A612 corridor east of the city. Nottinghamshire County Council is the highway authority, and its gangs work in Class 3 hi-vis across that suburban network and the routes opened up by recent infrastructure.",
   "The county delivers highways through Via East Midlands, the Teckal company wholly owned by the council since 2019 and managing the network since 2016, with profits reinvested in the county and a five-year extension expected toward 2031. The Gedling Access Road, a roughly forty-eight-million-pound bypass opened in 2022, terminates at a new signal-controlled junction with the A612.",
   "National Highways operates the wider trunk network, while the council-managed A612 Trent Valley Road is the key route through the Gedling and Carlton area and the A6011 serves the area east of Nottingham. Suburban and bypass-junction work alike mean busy roads and new-junction maintenance.",
   "Resurfacing, lining, drainage, lighting and winter gritting put Carlton crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the area's carriageway, suburban-corridor and winter-maintenance work",
  "s2_intro":"Across Carlton's Via East Midlands carriageway work and the A612 Gedling corridor",
 },
 "west bridgford": {
  "region":"West Bridgford and Nottinghamshire",
  "nearby":["Nottingham","Carlton","Beeston"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to West Bridgford's highway maintenance teams and roadworks contractors, from Nottinghamshire County Council's Via East Midlands company to National Highways work on the A52, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the West Bridgford area's roads running",
  "s1loc":[
   "West Bridgford sits beside Trent Bridge, home to the Test cricket ground and next to Nottingham Forest's City Ground, bordered by the A52 Nottingham ring road to the south and east. Nottinghamshire County Council is the highway authority, and its gangs work in Class 3 hi-vis around those riverside sporting venues and the ring road.",
   "The county delivers highways through Via East Midlands, its wholly-owned Teckal company managing the network since 2016, with an extension expected toward 2031. The A60 Loughborough Road and the A6011 Radcliffe Road over Lady Bay Bridge are the key local routes, with limited heavy industrial land in this largely residential town.",
   "National Highways operates the strategic A52, which forms the southern and eastern Nottingham ring road bordering the town and runs toward the A46 and A1, with junction improvements at Nottingham Knight and Wheatcroft progressing under a compulsory purchase order, while Trent Bridge and Lady Bay Bridge are notable structures. Ring-road and junction work alike mean fast roads and major structures.",
   "Surfacing, lining, drainage, lighting and winter gritting are all handled by West Bridgford crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the area's carriageway, ring-road and winter-maintenance work",
  "s2_intro":"Across West Bridgford's Via East Midlands carriageway work and the National Highways A52",
 },
 "beeston": {
  "region":"Beeston and Nottinghamshire",
  "nearby":["Nottingham","Long Eaton","West Bridgford"],
  "snapshot":"iNeedWorkwear kits Beeston's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from Nottinghamshire County Council's Via East Midlands company to National Highways work on the A52, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Beeston area's roads running",
  "s1loc":[
   "Beeston is home to the global Boots site and sits next to the University of Nottingham, with the NET tram running through the town centre and along the A6005 University Boulevard. Nottinghamshire County Council is the highway authority, and its gangs work in Class 3 hi-vis on that busy multi-modal corridor.",
   "The county delivers highways through Via East Midlands, its wholly-owned Teckal company managing the network since 2016 with an extension expected toward 2031, while the urban tram is run separately by Nottingham Express Transit. The Boots campus and the university are significant trip generators feeding the A6005 and A52.",
   "National Highways operates the A52, the Brian Clough Way running along the northern edge of Beeston past University Park, with footway and cycleway improvements carried out around the campus, while the A6005 Queens Road is the main local route toward Nottingham and Long Eaton. Trunk and tram-corridor work alike mean fast roads and multi-modal coordination.",
   "Resurfacing, lining, drainage, lighting and winter gritting put Beeston crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the area's carriageway, tram-corridor and winter-maintenance work",
  "s2_intro":"Across Beeston's Via East Midlands carriageway work and the National Highways A52",
 },
 "cheshunt": {
  "region":"Cheshunt and Hertfordshire",
  "nearby":["Hoddesdon","Enfield","Hertford"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Cheshunt's highway maintenance teams and roadworks contractors, from Hertfordshire County Council's Ringway contract to National Highways work on the M25, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Cheshunt area's roads running",
  "s1loc":[
   "Cheshunt sits in the Lee Valley on the London and Hertfordshire boundary, where the A10 spine meets the M25 at junction 25, a long-standing congestion point. Hertfordshire County Council is the highway authority, and its gangs work in Class 3 hi-vis along that busy corridor through the Broxbourne borough.",
   "Hertfordshire retained Ringway as its term maintenance contractor on a new deal from October 2025, an initial seven-year core term worth around three hundred and eighty-five million pounds with potential to extend toward twenty-one years, covering potholes, lighting, signals, gritting and emergency response. Growth in the Upper Lea Valley keeps the A10 corridor a maintenance focus.",
   "National Highways operates the M25 and its junction 25 interchange where the A10 meets the motorway, while the A1170 and the A121 toward Waltham Abbey are locally important and the council has run A10 junction improvements. Orbital-motorway and A10 work alike mean fast roads and tight management.",
   "Surfacing, lining, drainage, lighting and winter gritting are all handled by Cheshunt crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the area's carriageway, A10-corridor and winter-maintenance work",
  "s2_intro":"Across Cheshunt's Ringway carriageway work and the National Highways M25 and A10",
 },
 "barnet": {
  "region":"Barnet and North London",
  "nearby":["Edgware","Borehamwood","Potters Bar"],
  "snapshot":"iNeedWorkwear kits Barnet's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from the London Borough of Barnet's contractor partnership to the Transport for London red routes and the M1, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Barnet area's roads running",
  "s1loc":[
   "Barnet straddles the A1 and the A406 North Circular and reaches the M1 at the edge of London, with the Brent Cross and Staples Corner interchanges among the busiest structures in north London. The London Borough of Barnet is the highway authority for borough roads, and its gangs work in Class 3 hi-vis at that red-route and trunk-road interface.",
   "Highways are delivered through a contractor partnership in recent years, with the Tarmac Kier Joint Venture as the primary term maintenance contractor and Marlborough Highways and O'Hara Bros supporting carriageway and footway reconstruction. Works bases concentrate around Staples Corner, Brent Cross and the Edgware and Colindale corridors.",
   "National Highways operates the M1 at junction 1 by Staples Corner and the M25 to the north at South Mimms, while Transport for London runs the A406 North Circular red route and the A41 Watford Way, meeting the A1 at Henlys Corner. Trunk, motorway and red-route work alike mean fast roads and major interchanges.",
   "Resurfacing, lining, drainage, lighting and winter gritting put Barnet crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the borough's carriageway, interchange and winter-maintenance work",
  "s2_intro":"Across Barnet's carriageway work, the TfL North Circular and the M1",
 },
 "welwyn garden city": {
  "region":"Welwyn Garden City and Hertfordshire",
  "nearby":["Hatfield","Hertford","Stevenage"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Welwyn Garden City's highway maintenance teams and roadworks contractors, from Hertfordshire County Council's Ringway contract to National Highways work on the A1(M), with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Welwyn Garden City area's roads running",
  "s1loc":[
   "Welwyn Garden City was founded in 1920 as the second English garden city and later designated a new town, its planned tree-lined boulevards contrasting with the high-speed A1(M) running along its edge. Hertfordshire County Council is the highway authority, and its gangs work in Class 3 hi-vis where the garden city meets the motorway corridor.",
   "Hertfordshire delivers routine and reactive works through Ringway, retained on the new contract from October 2025 covering maintenance, potholes, lighting, signals and gritting across the county. The Mundells and Bessemer Road industrial areas provide works compounds serving the A1(M) corridor.",
   "National Highways operates the A1(M) along the western and southern side of the town at junction 4 and junction 6 on the Welwyn Bypass, while the A1000 links to Hatfield, the A414 provides the east-west connection and the A6129 links the centre to the motorway. Motorway and connector work alike mean fast roads and recurring incident response.",
   "Surfacing, lining, drainage, lighting and winter gritting are all handled by Welwyn Garden City crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the area's carriageway, motorway-corridor and winter-maintenance work",
  "s2_intro":"Across Welwyn Garden City's Ringway carriageway work and the National Highways A1(M)",
 },
 "romford": {
  "region":"Romford and East London",
  "nearby":["Hornchurch","Upminster","Ilford"],
  "snapshot":"iNeedWorkwear kits Romford's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from the London Borough of Havering's Marlborough partnership to the Transport for London A12 and A127, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Romford area's roads running",
  "s1loc":[
   "Romford is a historic market town whose royal charter dates to 1247 and whose town-centre core is wrapped by the A12 and A127 arterials and the Gallows Corner interchange. The London Borough of Havering is the highway authority, and its gangs work in Class 3 hi-vis where that market-town centre meets the high-volume arterial roads.",
   "Havering delivers highways with Marlborough Highways, appointed in recent years to a contract worth around a hundred and seventy million pounds covering maintenance, capital works, street lighting, winter maintenance and gully cleaning after earlier resurfacing partnerships. Industrial estates around the A12 and A127 corridor and Rom Valley Way serve as works bases.",
   "National Highways operates the M25 to the east, while Transport for London runs the A12 Eastern Avenue toward East Anglia, the A127 Southend Arterial Road beginning at Gallows Corner and the A118 through the centre, with TfL refurbishing the Gallows Corner flyover in recent years. Arterial and interchange work alike mean fast roads and a notorious congestion point.",
   "Resurfacing, lining, drainage, lighting and winter gritting put Romford crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the area's carriageway, arterial-corridor and winter-maintenance work",
  "s2_intro":"Across Romford's Marlborough carriageway work, the TfL A12 and A127",
 },
 "batley": {
  "region":"Batley and West Yorkshire",
  "nearby":["Dewsbury","Mirfield","Brighouse"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Batley's highway maintenance teams and roadworks contractors, from Kirklees Council and the Yorkshire Alliance framework to National Highways work on the M62, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Batley area's roads running",
  "s1loc":[
   "Batley sits at the heart of the Heavy Woollen District, its former-mill townscape strung along the A652 Bradford Road between the M62 to the north and the A653 Leeds corridor. Kirklees Council is the West Yorkshire metropolitan highway authority, and its gangs work in Class 3 hi-vis across that legacy-industrial network.",
   "Kirklees leads the Yorkshire Alliance surfacing and planing framework on behalf of Bradford, Leeds, Wakefield, York and Calderdale, an eighty-eight-million-pound framework on which Colas holds places across all twelve lots, while routine maintenance is partly delivered in house. Mill-conversion and logistics estates along Bradford Road provide works bases.",
   "National Highways operates the M62 just north of the town, while the council-managed A652 Bradford Road runs through Batley with planned junction improvements and the A653 Leeds Road corridor toward Shaw Cross and the White Rose area is slated for bus and junction works. Motorway and corridor work alike mean fast roads and constrained mill-town sites.",
   "Surfacing, lining, drainage, lighting and winter gritting are all handled by Batley crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the area's carriageway, mill-town-corridor and winter-maintenance work",
  "s2_intro":"Across Batley's Yorkshire Alliance carriageway work and the National Highways M62",
 },
 "kingston upon thames": {
  "region":"Kingston upon Thames and South West London",
  "nearby":["Twickenham","Esher","Epsom"],
  "snapshot":"iNeedWorkwear kits Kingston upon Thames highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from the Royal Borough's shared service with R J Dance and FM Conway to the A3 and the Transport for London red routes, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Kingston upon Thames area's roads running",
  "s1loc":[
   "Kingston upon Thames is defined by its one-way gyratory system and the A3 Kingston bypass carrying strategic through-traffic around the town. The Royal Borough of Kingston upon Thames is the highway authority for its local roads, and its gangs work in Class 3 hi-vis keeping a busy gyratory and a dense urban network moving.",
   "The borough runs a Highways and Transport Shared Service with the London Borough of Sutton, with R J Dance appointed for reactive maintenance and FM Conway for planned works, while FM Conway also holds the Transport for London South Area framework covering red routes and structures. Works capacity sits around Chessington and the Tolworth corridor.",
   "National Highways operates the wider strategic network, while Transport for London runs the A3 Kingston bypass and the borough holds the A308 riverside corridor and the A240 toward Epsom, with the Thames bridges and retaining structures notable assets. Red-route and gyratory work alike mean fast roads and tight urban management.",
   "Resurfacing, lining, drainage, lighting and winter gritting put Kingston crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the borough's carriageway, gyratory and winter-maintenance work",
  "s2_intro":"Across Kingston upon Thames carriageway work, the A3 and the TfL red routes",
 },
 "beckenham": {
  "region":"Beckenham and South East London",
  "nearby":["Bromley","Lewisham","Croydon"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Beckenham's highway maintenance teams and roadworks contractors, from the London Borough of Bromley's FM Conway partnership to the Transport for London red routes and the A21, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Beckenham area's roads running",
  "s1loc":[
   "Beckenham sits among the leafy south-east London suburbs near the A21 corridor toward Bromley and the M25, its network crossed by the area's many railway lines. The London Borough of Bromley is the highway authority, and its gangs work in Class 3 hi-vis on suburban high streets and corridor routes.",
   "Bromley delivers highways with FM Conway as its infrastructure service partner and term contractor, alongside other firms, having completed the Beckenham High Street public-realm and resurfacing scheme around Beckenham Green, while FM Conway also holds the Transport for London South Area framework. Depot and materials capacity sits across the wider borough.",
   "National Highways operates the wider strategic network, while Transport for London runs the red routes and the A21 strategic route runs east toward Bromley and the M25, with the A222 through Beckenham toward Penge and the A234 Croydon Road corridor the local spines. Suburban high-street and corridor work alike mean rail-bridge structures and busy local roads.",
   "Surfacing, lining, drainage, lighting and winter gritting are all handled by Beckenham crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the area's carriageway, high-street and winter-maintenance work",
  "s2_intro":"Across Beckenham's FM Conway carriageway work and the A21 corridor",
 },
 "sutton": {
  "region":"Sutton and South London",
  "nearby":["Croydon","Epsom","Kingston upon Thames"],
  "snapshot":"iNeedWorkwear kits Sutton's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from the London Borough of Sutton's shared service with R J Dance and FM Conway to the Transport for London red routes, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Sutton area's roads running",
  "s1loc":[
   "Sutton's network pivots on the A217 and A232 junctions, and the borough has long featured in proposals to extend the London tram toward the town, shaping its corridor planning. The London Borough of Sutton is the highway authority, and its gangs work in Class 3 hi-vis on those busy radial routes.",
   "Sutton runs a Highways and Transport Shared Service with the Royal Borough of Kingston, using R J Dance for reactive maintenance and FM Conway for planned works, the model later extended to Kingston, while FM Conway also holds the Transport for London South Area framework. Works capacity sits around Beddington and the Kimpton corridor.",
   "National Highways operates the wider strategic network, while Transport for London runs the red routes and the council holds the A217 north-south route toward Banstead and the M25, the A232 Cheam corridor and the A24 nearby. Radial-route and potential light-rail work alike mean busy roads and corridor coordination.",
   "Resurfacing, lining, drainage, lighting and winter gritting put Sutton crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the borough's carriageway, radial-route and winter-maintenance work",
  "s2_intro":"Across Sutton's shared-service carriageway work and the A217 and A232 corridors",
 },
 "andover": {
  "region":"Andover and Hampshire",
  "nearby":["Basingstoke","Winchester","Salisbury"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Andover's highway maintenance teams and roadworks contractors, from Hampshire County Council's M Group Highways contract to National Highways work on the A303 and A34, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Andover area's roads running",
  "s1loc":[
   "Andover sits on the A303 west-country corridor passing south of the town, linked by the A34 strategic route up to the M4 and down toward the M3 and Winchester. Hampshire County Council is the highway authority for one of the largest networks in England, and its gangs work in Class 3 hi-vis along those strategic approaches.",
   "Hampshire Highways runs through the partnership with Milestone Infrastructure, now trading as M Group Highways, in place since 2017 and extended to 2029, covering on the order of eight thousand five hundred kilometres of carriageway. The Walworth and Andover Business Park areas provide depot capacity serving the wider corridor.",
   "National Highways operates the A303 toward the South West, where it sees regular overnight closures, and the A34 north-south route, while the A3057 links Andover south toward Romsey and the Test Valley, the junctions where these meet being key works locations. Strategic-corridor and local work alike mean fast roads and overnight schemes.",
   "Surfacing, lining, drainage, lighting and winter gritting are all handled by Andover crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the area's carriageway, strategic-corridor and winter-maintenance work",
  "s2_intro":"Across Andover's M Group Highways carriageway work and the National Highways A303 and A34",
 },
 "winchester": {
  "region":"Winchester and Hampshire",
  "nearby":["Eastleigh","Andover","Southampton"],
  "snapshot":"iNeedWorkwear kits Winchester's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from Hampshire County Council's M Group Highways contract to National Highways work on the M3 and A34, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Winchester area's roads running",
  "s1loc":[
   "Winchester is a historic cathedral city defined by the M3 Twyford Down cutting south-east of the centre and by the park-and-ride operations that keep traffic out of its core. Hampshire County Council is the highway authority, and its gangs work in Class 3 hi-vis between the motorway corridor and the heritage city centre.",
   "Hampshire Highways runs through the partnership with Milestone Infrastructure, now trading as M Group Highways, in place since 2017 and extended to 2029, handling tens of thousands of task orders a year. Depot and industrial capacity sits around Winnall and the Bar End and Easton Lane area on the city edge.",
   "National Highways operates the M3 through the deep Twyford Down chalk cutting that completed the motorway in 1995, the A34 north toward the M4 and the A31 toward the New Forest, with major junction 9 improvements progressing as a structures-led scheme. Motorway-cutting and junction work alike mean fast roads and significant structures.",
   "Resurfacing, lining, drainage, lighting and winter gritting put Winchester crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the city's carriageway, motorway-corridor and winter-maintenance work",
  "s2_intro":"Across Winchester's M Group Highways carriageway work and the National Highways M3 and A34",
 },
 "middleton": {
  "region":"Middleton and Greater Manchester",
  "nearby":["Rochdale","Heywood","Oldham"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Middleton's highway maintenance teams and roadworks contractors, from Rochdale Council's in-house highways service to National Highways work on the M60 and M62, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Middleton area's roads running",
  "s1loc":[
   "Middleton sits on the north-east edge of the Manchester orbital, where the M60 meets the trans-Pennine M62 near junction 20 and the A664 feeds the town. Rochdale Metropolitan Borough Council is the highway authority, and its gangs work in Class 3 hi-vis beside that busy interchange under the wider Transport for Greater Manchester Bee Network.",
   "Rochdale brought highway maintenance back in house from 2022, delivering potholes, gritting, drainage and resurfacing with its own teams after the previous Balfour Beatty contract ended, and has sought a framework worth up to around twenty-eight million pounds to add supplementary labour and plant. The Stakehill Industrial Estate off the A664 anchors local logistics traffic.",
   "National Highways operates the M60 and M62 with the interchange and the Castleton bridge works nearby, the A627(M) spur and the A664 Rochdale Road linking the town in. Orbital, trans-Pennine and borough-road work alike mean fast roads and tight junction management.",
   "Surfacing, lining, drainage, lighting and winter gritting are all handled by Middleton crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the area's carriageway, interchange and winter-maintenance work",
  "s2_intro":"Across Middleton's Rochdale carriageway work and the National Highways M60 and M62",
 },
 "ashton-under-lyne": {
  "region":"Ashton-under-Lyne and Greater Manchester",
  "nearby":["Stalybridge","Droylsden","Denton"],
  "snapshot":"iNeedWorkwear kits Ashton-under-Lyne's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from Tameside Council to National Highways work on the M60 and the A627(M), with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Ashton-under-Lyne area's roads running",
  "s1loc":[
   "Ashton-under-Lyne sits on the eastern side of the Manchester orbital where the M60 at junction 23 meets the A635 through the town and the A627(M) spurs toward Oldham. Tameside Metropolitan Borough Council is the highway authority, and its gangs work in Class 3 hi-vis under the Transport for Greater Manchester Bee Network.",
   "The council runs its Highways Service with daily defect-recording inspectors and a multi-lot maintenance framework spanning resurfacing, drainage, structures, lining, lighting and traffic management. Warehousing along the A635 and A627 corridors and light manufacturing near Ashton Moss drive the local workload.",
   "National Highways operates the M60 on the western side at junction 23, while the A627(M) provides the motorway spur and the A635 carries the main town-centre route, the Metrolink East Manchester Line terminus having opened in the centre in 2013 alongside tram infrastructure past Ashton Moss. Orbital and tram-interface work alike mean fast roads and careful coordination.",
   "Resurfacing, lining, drainage, lighting and winter gritting put Ashton crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the area's carriageway, tram-interface and winter-maintenance work",
  "s2_intro":"Across Ashton-under-Lyne's Tameside carriageway work and the National Highways M60 and A627(M)",
 },
 "leigh": {
  "region":"Leigh and Greater Manchester",
  "nearby":["Atherton","Hindley","Wigan"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Leigh's highway maintenance teams and roadworks contractors, from Wigan Council's in-house highways service to the A580 East Lancashire Road, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Leigh area's roads running",
  "s1loc":[
   "Leigh sits west of the conurbation on the A580 East Lancashire Road, the major dual carriageway toward Salford and Manchester, with the guided busway running its rapid-transit route alongside. Wigan Metropolitan Borough Council is the highway authority, and its gangs work in Class 3 hi-vis under the Transport for Greater Manchester Bee Network.",
   "The council manages highways largely in house through its Highways and Network Management Group, maintaining around eleven hundred and sixty kilometres of road, some thirty-six thousand street lights and over four hundred structures, issuing specific works such as road marking to contractors. The A580 corridor carries significant commercial traffic.",
   "National Highways operates the wider motorway network, while the A580 East Lancashire Road is the defining route, combined with the Leigh to Salford and Manchester guided busway opened in 2016 over around seven kilometres of guideway plus bus lanes, and the A579 the local connector. Dual-carriageway and busway-interface work alike mean fast roads and lane-allocation management.",
   "Surfacing, lining, drainage, lighting and winter gritting are all handled by Leigh crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the area's carriageway, busway-corridor and winter-maintenance work",
  "s2_intro":"Across Leigh's Wigan carriageway work and the A580 East Lancashire Road",
 },
 "altrincham": {
  "region":"Altrincham and Greater Manchester",
  "nearby":["Stretford","Urmston","Wilmslow"],
  "snapshot":"iNeedWorkwear kits Altrincham's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from Trafford Council's One Trafford Partnership with Amey to National Highways work on the M56, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Altrincham area's roads running",
  "s1loc":[
   "Altrincham sits in the south-west of the conurbation where the M56 feeds toward the M60 orbital and the A56 Manchester Road is the principal local arterial, with the Metrolink interchange at the southern end of the tram network. Trafford Council is the highway authority, and its gangs work in Class 3 hi-vis under the Transport for Greater Manchester Bee Network.",
   "Trafford delivers highways through the One Trafford Partnership with Amey, the fifteen-year partnership formed in 2015 covering roads, bridges, lighting, drainage and road safety across around eight hundred kilometres of road and some thirty thousand lighting columns. Recent A56 junction upgrades at Barrington Road and Sinderland Road were delivered through the partnership.",
   "National Highways operates the M56 to the south and west feeding the M60, while the council-managed A56 Manchester Road is the main arterial and the Altrincham Interchange combines tram, rail and bus. Motorway and multi-modal work alike mean fast roads and busy interchange management.",
   "Resurfacing, lining, drainage, lighting and winter gritting put Altrincham crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the area's carriageway, arterial-road and winter-maintenance work",
  "s2_intro":"Across Altrincham's One Trafford Partnership carriageway work and the National Highways M56",
 },
 "urmston": {
  "region":"Urmston and Greater Manchester",
  "nearby":["Stretford","Altrincham","Salford"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Urmston's highway maintenance teams and roadworks contractors, from Trafford Council's One Trafford Partnership with Amey to National Highways work on the M60 and Trafford Park, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Urmston area's roads running",
  "s1loc":[
   "Urmston sits beside Trafford Park, the first planned industrial estate in the world at nearly five square miles, served by the M60 orbital at junctions 9 to 11 and the A57 Chester Road. Trafford Council is the highway authority, and its gangs work in Class 3 hi-vis at the heart of that high-volume freight corridor under the Bee Network.",
   "Trafford delivers highways through the One Trafford Partnership with Amey, formed in 2015, covering maintenance, resurfacing, drainage, lighting and structures, and Urmston hosted a 2023 trial of solar hybrid streetlights on Woodbridge Road alongside an Active Neighbourhood walking and cycling programme. Trafford Park generates heavy commercial and logistics traffic on the estate roads.",
   "National Highways operates the M60 orbital at junctions 9 to 11 serving Trafford Park, while the A57 Chester Road is the principal arterial through the area. Orbital and industrial-estate work alike mean fast roads and constant freight movement.",
   "Surfacing, lining, drainage, lighting and winter gritting are all handled by Urmston crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the area's carriageway, industrial-estate and winter-maintenance work",
  "s2_intro":"Across Urmston's One Trafford Partnership carriageway work and the National Highways M60",
 },
 "hinckley": {
  "region":"Hinckley and Leicestershire",
  "nearby":["Nuneaton","Bedworth","Leicester"],
  "snapshot":"iNeedWorkwear kits Hinckley's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from Leicestershire County Council's Aggregate Industries patching contract to National Highways work on the M69, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Hinckley area's roads running",
  "s1loc":[
   "Hinckley sits on the M69 linking the M1 near Leicester to the M6 near Coventry, with major logistics growth at Hinckley Park beside junction 1 anchored by a large DPD parcel hub. Leicestershire County Council is the highway authority, and its gangs work in Class 3 hi-vis along that motorway-and-logistics corridor in west Leicestershire.",
   "The county delivers carriageway patching and repair through a joint contract with Leicester City awarded to Aggregate Industries, worth up to around forty-seven million pounds, with asphalt supplied from the Bardon Hill and Croft plants. The proposed Hinckley National Rail Freight Interchange would add further access works.",
   "National Highways operates the M69 with junction 1 serving the town, while the A5 Roman Watling Street runs along the county boundary and the A47 links toward Leicester and Earl Shilton. Motorway and heritage-corridor work alike mean fast roads and heavy distribution traffic.",
   "Resurfacing, lining, drainage, lighting and winter gritting put Hinckley crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the area's carriageway, logistics-corridor and winter-maintenance work",
  "s2_intro":"Across Hinckley's Aggregate Industries carriageway work and the National Highways M69 and A5",
 },
 "sutton-in-ashfield": {
  "region":"Sutton-in-Ashfield and Nottinghamshire",
  "nearby":["Mansfield","Alfreton","Hucknall"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Sutton-in-Ashfield's highway maintenance teams and roadworks contractors, from Nottinghamshire County Council's Via East Midlands company to National Highways work on the M1, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Sutton-in-Ashfield area's roads running",
  "s1loc":[
   "Sutton-in-Ashfield sits on the west Nottinghamshire coalfield, where the M1 at junction 28 just north of the town is a heavily used freight gateway prone to peak congestion. Nottinghamshire County Council is the highway authority, and its gangs work in Class 3 hi-vis across that former-mining network turned manufacturing and logistics base.",
   "The county delivers highways through Via East Midlands, its wholly-owned Teckal company managing the network since 2016 and brought fully in house in 2019, covering roads, lighting, signals and winter service with an extension running toward the early 2030s. Haulage operators concentrate around junction 28.",
   "National Highways operates the M1 at junction 28, while the A38 with its 2005 bypass runs through toward Derby and Nottingham, meeting the A611 and the A617 at Kings Mill. Motorway and bypass work alike mean fast roads and concentrated freight.",
   "Surfacing, lining, drainage, lighting and winter gritting are all handled by Sutton crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the area's carriageway, coalfield-corridor and winter-maintenance work",
  "s2_intro":"Across Sutton-in-Ashfield's Via East Midlands carriageway work and the National Highways M1 and A38",
 },
 "worksop": {
  "region":"Worksop and Nottinghamshire",
  "nearby":["Retford","Mansfield","Chesterfield"],
  "snapshot":"iNeedWorkwear kits Worksop's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from Nottinghamshire County Council's Via East Midlands company to National Highways work on the A1, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Worksop area's roads running",
  "s1loc":[
   "Worksop sits on the A1 Great North Road corridor in north Nottinghamshire, a strategic distribution location where the Bassetlaw logistics corridor is a leading growth zone. Nottinghamshire County Council is the highway authority, and its gangs work in Class 3 hi-vis along that freight-heavy network.",
   "The county delivers highways through Via East Midlands, its wholly-owned Teckal company managing the network since 2016 with a contract extended toward the early 2030s, covering maintenance, lighting, signals and winter service. The large EM.EX Worksop logistics scheme along the A1 and A57 will generate associated access works.",
   "National Highways operates the A1 running just east of the town at the Apleyhead junction, while the A57 runs east-west toward Sheffield and the A1 and the A60 north-south toward Mansfield and Retford. Trunk and logistics work alike mean fast roads and heavy goods traffic.",
   "Resurfacing, lining, drainage, lighting and winter gritting put Worksop crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the area's carriageway, A1-corridor and winter-maintenance work",
  "s2_intro":"Across Worksop's Via East Midlands carriageway work and the National Highways A1",
 },
 "ilkeston": {
  "region":"Ilkeston and Derbyshire",
  "nearby":["Long Eaton","Beeston","Ripley"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Ilkeston's highway maintenance teams and roadworks contractors, from Derbyshire County Council's ALLRoads service to National Highways work on the M1, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Ilkeston area's roads running",
  "s1loc":[
   "Ilkeston sits in the Erewash Valley on the River Erewash, the Derbyshire and Nottinghamshire boundary, with the M1 at junction 25 the principal motorway gateway. Derbyshire County Council is the highway authority for over three thousand five hundred miles of road, and its gangs work in Class 3 hi-vis across that valley network.",
   "The county delivers much of its work through ALLRoads, its in-house direct labour organisation handling major construction, reinstatements, drainage and lighting with a turnover above twenty million pounds, supplemented by external contractors. The A609 through the town is a key resurfacing route and Erewash Valley industrial sites line the A6007.",
   "National Highways operates the M1 at junctions 25 and 26 nearby, while the council-managed A609 Nottingham Road and the A6007 Stapleford Road link toward Stapleford, Heanor and the motorway. Motorway-gateway and valley work alike mean fast roads and busy local corridors.",
   "Surfacing, lining, drainage, lighting and winter gritting are all handled by Ilkeston crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the area's carriageway, valley-corridor and winter-maintenance work",
  "s2_intro":"Across Ilkeston's Derbyshire ALLRoads carriageway work and the National Highways M1",
 },
 "grantham": {
  "region":"Grantham and Lincolnshire",
  "nearby":["Newark","Stamford","Melton Mowbray"],
  "snapshot":"iNeedWorkwear kits Grantham's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from Lincolnshire County Council's Balfour Beatty contract to National Highways work on the A1, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Grantham area's roads running",
  "s1loc":[
   "Grantham sits on the A1 Great North Road in south Lincolnshire, where the Grantham Southern Relief Road is being built in phases to link a new A1 junction to the A52, bridging the Witham valley and the East Coast Main Line. Lincolnshire County Council is the highway authority, and its gangs work in Class 3 hi-vis along that trunk corridor.",
   "The county delivers core highways maintenance through Balfour Beatty Living Places on a term contract worth around two hundred and seventeen million pounds over roughly nine thousand kilometres of road, with a separate one-hundred-and-fifty-million-pound framework for resurfacing and improvement. Recent town schemes covered the A52 and A607 Station Approach junction and Harlaxton Road.",
   "National Highways operates the A1 past the town, while the council-managed A52 runs toward Nottingham and Boston and the A607 toward Lincoln and Melton Mowbray, the relief road's final phase with its long bridge over the railway and the Witham still under construction. Trunk and relief-road work alike mean fast roads and major structures.",
   "Resurfacing, lining, drainage, lighting and winter gritting put Grantham crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the area's carriageway, relief-road and winter-maintenance work",
  "s2_intro":"Across Grantham's Balfour Beatty carriageway work and the National Highways A1",
 },
 "lytham st annes": {
  "region":"Lytham St Annes and the Fylde coast",
  "nearby":["Blackpool","Poulton-le-Fylde","Preston"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Lytham St Annes highway maintenance teams and roadworks contractors, from Lancashire County Council to National Highways work on the M55, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Lytham St Annes area's roads running",
  "s1loc":[
   "Lytham St Annes is a Fylde coast resort where the M55 terminus near Blackpool funnels seasonal tourist traffic and the A584 seafront route is a recurring congestion pinch-point. Lancashire County Council is the highway authority, and its gangs work in Class 3 hi-vis along that coastal corridor.",
   "The county has moved toward a single managed-service term provider for routine repairs and resurfacing, keeping in-house teams for urgent defects and carrying a twelve-month repair warranty under the revised model. The M55 to Heyhouses Link Road, a single carriageway from Whitehills Roundabout opened in 2024, improved motorway access for St Annes, Ansdell and Lytham.",
   "National Highways operates the M55 across the Fylde terminating near Blackpool, while the council-managed A584 Clifton Drive is the principal seafront route linking St Annes, Lytham and Blackpool. Motorway and seafront work alike mean fast roads and seasonal congestion management.",
   "Resurfacing, lining, drainage, lighting and winter gritting put Lytham St Annes crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the resort's carriageway, seafront and winter-maintenance work",
  "s2_intro":"Across Lytham St Annes council carriageway work and the National Highways M55",
 },
 "chorley": {
  "region":"Chorley and Lancashire",
  "nearby":["Leyland","Horwich","Bolton"],
  "snapshot":"iNeedWorkwear kits Chorley's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from Lancashire County Council to National Highways work on the M61 and M6, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Chorley area's roads running",
  "s1loc":[
   "Chorley sits in central Lancashire where the M61 from Manchester merges with the M6 at the junction 9 and junction 29 interchange, one of the busier junctions in the county. Lancashire County Council is the highway authority, and its gangs work in Class 3 hi-vis along that motorway cluster and the parallel A6.",
   "The county runs a single managed-service term contractor for routine repairs and resurfacing with in-house teams for urgent defects and a twelve-month repair warranty. Buckshaw Village, the large development on the former Royal Ordnance site between Chorley and Leyland, and the Euxton industrial parks drive heavy commuter and freight movement, supported by M6 and M61 junction improvements.",
   "National Highways operates the M61 and M6 merging at junction 9 and 29, while the A6 is the principal parallel corridor toward Bamber Bridge and Preston. Motorway-merge and A6 work alike mean fast roads and heavy estate-bound traffic.",
   "Surfacing, lining, drainage, lighting and winter gritting are all handled by Chorley crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the area's carriageway, motorway-corridor and winter-maintenance work",
  "s2_intro":"Across Chorley's Lancashire carriageway work and the National Highways M61 and M6",
 },
 "coatbridge": {
  "region":"Coatbridge and the Lanarkshire corridor",
  "nearby":["Airdrie","Bellshill","Motherwell"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Coatbridge's highway maintenance teams and roadworks contractors, from North Lanarkshire Council to Transport Scotland trunk roads on the M8 and A8, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Coatbridge area's roads running",
  "s1loc":[
   "Coatbridge sits in the historic Lanarkshire iron-and-steel corridor, where the M8 and the A8 spine link a dense cluster of industrial estates at Eurocentral and Bargeddie. North Lanarkshire Council is the unitary roads authority, and its gangs work in Class 3 hi-vis on local streets beside that heavy-freight corridor.",
   "The council maintains all roads on its list of public roads and runs winter gritting and roadworks notices in house for the local network, while the trunk roads and motorways around the town are not its responsibility. Two highway tiers run side by side here, council local roads and the Transport Scotland trunk network.",
   "In Scotland trunk roads are Transport Scotland's responsibility, maintained in the relevant unit by Amey, with the M8 to the south linking Glasgow and Edinburgh, the A8 running past Bargeddie Roundabout toward Eurocentral and the A89 a key primary route. Motorway and industrial-corridor work alike mean fast roads and recurrent trunk maintenance.",
   "Resurfacing, lining, drainage, lighting and winter gritting put Coatbridge crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the area's carriageway, industrial-corridor and winter-maintenance work",
  "s2_intro":"Across Coatbridge's North Lanarkshire carriageway work and the Transport Scotland M8 and A8",
 },
 "caerphilly": {
  "region":"Caerphilly and the South Wales Valleys",
  "nearby":["Cardiff","Pontypridd","Blackwood"],
  "snapshot":"iNeedWorkwear kits Caerphilly's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from Caerphilly County Borough Council to Welsh Government trunk roads near the A470, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Caerphilly area's roads running",
  "s1loc":[
   "Caerphilly is dominated by its medieval castle, with through-traffic diverted off the historic route past it onto the A469 and A468 bypass system in the Rhymney Valley. Caerphilly County Borough Council is the Welsh unitary highway authority, and its gangs work in Class 3 hi-vis on those valley commuter and freight routes.",
   "The council maintains the local road network and coordinates utility roadworks in house and through local contractors, while the trunk roads in its area are not its responsibility. Industrial estates are reached off the A469 Rhymney bypass with links toward the A465.",
   "Trunk roads in Wales are the Welsh Government's responsibility via Traffic Wales and the South Wales Trunk Road Agent, administered by Neath Port Talbot Council, with the A468 Ring Road linking to the A470 toward the M4 at junction 32 and Cardiff and the A469 the eastern valley relief route. Trunk and valley work alike mean fast roads and a classic two-tier Welsh setup.",
   "Surfacing, lining, drainage, lighting and winter gritting are all handled by Caerphilly crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the area's carriageway, valley-route and winter-maintenance work",
  "s2_intro":"Across Caerphilly's council carriageway work and the Welsh Government A468 and A470",
 },
 "castleford": {
  "region":"Castleford and the Five Towns of West Yorkshire",
  "nearby":["Pontefract","Normanton","Featherstone"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Castleford's highway maintenance teams and roadworks contractors, from Wakefield Council to National Highways work on the M62, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Castleford area's roads running",
  "s1loc":[
   "Castleford is the largest of the Five Towns, a rugby-league heartland where the M62 runs behind the town and junction 32 at Glasshoughton anchors the Xscape leisure centre and Junction 32 retail outlet. Wakefield Council is the West Yorkshire metropolitan highway authority, and its gangs work in Class 3 hi-vis along that retail-and-motorway corridor.",
   "The council runs a permit scheme controlling street works alongside asset maintenance and resurfacing, with the West Yorkshire Combined Authority funding major corridor schemes including around twenty-two and a half million pounds on the A61 and A639 toward Leeds. The Glasshoughton estates on the former colliery site generate heavy retail traffic.",
   "National Highways operates the M62 along the south of the town with junction 32 the key interchange, while the council-managed A639 serves Normanton, Glasshoughton and Pontefract and the A656 is another key link, with the M1 and A1(M) nearby. Motorway and retail-corridor work alike mean fast roads and congested junctions.",
   "Resurfacing, lining, drainage, lighting and winter gritting put Castleford crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the area's carriageway, retail-corridor and winter-maintenance work",
  "s2_intro":"Across Castleford's Wakefield carriageway work and the National Highways M62",
 },
 "ramsgate": {
  "region":"Ramsgate and Kent",
  "nearby":["Margate","Broadstairs","Deal"],
  "snapshot":"iNeedWorkwear kits Ramsgate's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from Kent County Council's Ringway term contract to the A299 Thanet Way and A256, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Ramsgate area's roads running",
  "s1loc":[
   "Ramsgate's Royal Harbour and port sit at the foot of the A299 and A256 freight corridor on the Isle of Thanet, where coastal exposure and clay subsoil drive a recurring resurfacing programme. Kent County Council is the highway authority, and its gangs work in Class 3 hi-vis on those exposed coastal approaches.",
   "Kent moved its highways term maintenance to Ringway, a Vinci subsidiary, from May 2026 under a twenty-one-year contract worth around fifty million pounds a year, taking over from Amey after twelve years. The Pysons Road and Manston Road industrial estates and the wider Manston employment land support local highways and trades work.",
   "There is no motorway in Thanet, so the council-managed A299 Thanet Way running from Brenley Corner near Faversham to Ramsgate is the principal artery, with the A256 heading south toward Sandwich, Dover and the A2, and an extensive A299 resurfacing programme phased through summer 2026. Coastal-corridor and port-access work alike mean exposed conditions and heavy freight.",
   "Surfacing, lining, drainage, lighting and winter gritting are all handled by Ramsgate crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the area's carriageway, port-corridor and winter-maintenance work",
  "s2_intro":"Across Ramsgate's Ringway carriageway work and the A299 Thanet Way and A256",
 },
 "margate": {
  "region":"Margate and Kent",
  "nearby":["Ramsgate","Broadstairs","Herne Bay"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Margate's highway maintenance teams and roadworks contractors, from Kent County Council's Ringway term contract to the A28 and A299 Thanet Way, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Margate area's roads running",
  "s1loc":[
   "Margate's seafront and the Turner Contemporary gallery have anchored a tourism-led regeneration, so the condition and appearance of its coastal carriageways and the A28 and A299 approaches carry both visitor-economy and safety weight. Kent County Council is the highway authority, and its gangs work in Class 3 hi-vis on the Thanet coast roads.",
   "As across Kent, the county term maintenance contract passed to Ringway from May 2026 after Amey's twelve years, on the twenty-one-year deal covering carriageways, gritting, drainage and structures. The Westwood and Westwood Cross employment area supports local highways and trades activity.",
   "There is no motorway in Thanet, so the council-managed A28 links Margate inland through Birchington and Canterbury and the A299 Thanet Way is the strategic east-west route, with the 2026 A299 resurfacing programme sending diversions via the A291 and A28. Coastal-resort and inland-corridor work alike mean weather exposure and seasonal flows.",
   "Resurfacing, lining, drainage, lighting and winter gritting put Margate crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the area's carriageway, coastal-corridor and winter-maintenance work",
  "s2_intro":"Across Margate's Ringway carriageway work and the A28 and A299 Thanet Way",
 },
 "sittingbourne": {
  "region":"Sittingbourne and Kent",
  "nearby":["Faversham","Maidstone","Chatham"],
  "snapshot":"iNeedWorkwear kits Sittingbourne's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from Kent County Council's Ringway term contract to National Highways work on the M2 and the A249 Sheppey crossing, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Sittingbourne area's roads running",
  "s1loc":[
   "Sittingbourne sits where the M2 corridor meets the A249 route to the Isle of Sheppey, a strategic freight and commuter pinch-point with the high-level Sheppey Crossing viaduct over the Swale. Kent County Council is the highway authority, and its gangs work in Class 3 hi-vis along that motorway and crossing corridor.",
   "Kent's county term maintenance contract moved to Ringway from May 2026 after Amey's twelve years, on the twenty-one-year, roughly fifty-million-pound-a-year deal, while National Highways completed the around one-hundred-million-pound M2 junction 5 Stockbury flyover in early 2025. The Eurolink and Kemsley logistics estates line the M2 and A249.",
   "National Highways operates the M2 just south of the town and the new Stockbury flyover, while the council-managed A249 links the M2 and M20 north to Sheerness via the Sheppey Crossing, with Housing Infrastructure Fund junction works at Key Street and Grovehurst. Motorway, flyover and crossing work alike mean fast roads and wind-exposed structures.",
   "Surfacing, lining, drainage, lighting and winter gritting are all handled by Sittingbourne crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the area's carriageway, crossing-corridor and winter-maintenance work",
  "s2_intro":"Across Sittingbourne's Ringway carriageway work and the National Highways M2 and A249",
 },
 "bexhill-on-sea": {
  "region":"Bexhill-on-Sea and East Sussex",
  "nearby":["Hastings","Eastbourne","Hailsham"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Bexhill-on-Sea's highway maintenance teams and roadworks contractors, from East Sussex Highways and Balfour Beatty Living Places to the A259 and the Combe Valley Way link road, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Bexhill-on-Sea area's roads running",
  "s1loc":[
   "Bexhill-on-Sea sits on the East Sussex coast where the A259 frontage and the Bexhill to Hastings Link Road, named Combe Valley Way, shape how traffic and development move. East Sussex County Council is the highway authority, and its gangs work in Class 3 hi-vis along the seafront and the valley link.",
   "The East Sussex Highways partnership transferred in recent years to Balfour Beatty Living Places, which won a seven-year contract worth around two hundred and ninety-seven million pounds from May 2023 covering roads, drainage, lighting, signals, bridges and gritting, still trading publicly as East Sussex Highways. The North Bexhill business park off Combe Valley Way supports local activity.",
   "There is no motorway through Bexhill, so the council-managed A259 is the main coastal route between Hastings and Eastbourne and the A269 runs north, while the Combe Valley Way link road, opened in 2015 at around a hundred and twenty million pounds, connects the A259 to the A21 side of St Leonards. Coastal and link-road work alike mean exposed conditions and growth-driven schemes.",
   "Resurfacing, lining, drainage, lighting and winter gritting put Bexhill crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the area's carriageway, link-road and winter-maintenance work",
  "s2_intro":"Across Bexhill-on-Sea's East Sussex Highways carriageway work and the A259 and Combe Valley Way",
 },
 "fareham": {
  "region":"Fareham and Hampshire",
  "nearby":["Gosport","Portsmouth","Havant"],
  "snapshot":"iNeedWorkwear kits Fareham's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from Hampshire County Council's M Group Highways contract to National Highways work on the M27, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Fareham area's roads running",
  "s1loc":[
   "Fareham sits on the M27 and the A27 Portsmouth-to-Southampton corridor, with the Welborne garden village of around six thousand new homes north of the town driving the M27 junction 10 upgrade. Hampshire County Council is the highway authority for one of the largest networks in England, and its gangs work in Class 3 hi-vis along the Solent corridor.",
   "Hampshire Highways runs through the partnership with Milestone Infrastructure, now trading as M Group Highways, in place since 2017 and extended to 2029, with a joint road-material recycling hub, while the major junction 10 scheme is built by VolkerFitzpatrick with an underpass, new slips and link roads. The Solent Enterprise Zone at Daedalus and Segensworth anchor local industry.",
   "National Highways operates the M27 immediately north of the town as the strategic spine of South Hampshire, while the A27 is the parallel local route and the A32 runs north-south linking Gosport up to the motorway. Motorway-junction and Solent-corridor work alike mean fast roads and major construction.",
   "Surfacing, lining, drainage, lighting and winter gritting are all handled by Fareham crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the area's carriageway, Solent-corridor and winter-maintenance work",
  "s2_intro":"Across Fareham's M Group Highways carriageway work and the National Highways M27 and A27",
 },
 "boston": {
  "region":"Boston and Lincolnshire",
  "nearby":["Spalding","Skegness","Grantham"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Boston's highway maintenance teams and roadworks contractors, from Lincolnshire County Council's Balfour Beatty contract to the A16 and the John Adams Way relief road, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Boston area's roads running",
  "s1loc":[
   "Boston sits on the A16 in the low-lying Lincolnshire Fens, where the A16 and A52 combine along the John Adams Way relief road across the River Witham and the Port of Boston brings freight onto the network. Lincolnshire County Council is the highway authority, and its gangs work in Class 3 hi-vis in a setting where drainage and bridge maintenance are unusually prominent.",
   "The county delivers core highways through Balfour Beatty Living Places, which runs the county depot network for winter and reactive work, with resurfacing through a separate one-hundred-and-fifty-million-pound framework carrying firms such as Tarmac and Thomas Bow. The Boston Riverside and A16 trading estates support local activity.",
   "National Highways operates the wider trunk network, while the council-managed A16 runs the Grimsby-to-Peterborough corridor, the A52 crosses east-west and the John Adams Way relief road carries combined A16 and A52 traffic over the Witham. Relief-road and Fenland work alike mean swing-bridge structures and heavy drainage demand.",
   "Resurfacing, lining, drainage, lighting and winter gritting put Boston crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the area's carriageway, Fenland-corridor and winter-maintenance work",
  "s2_intro":"Across Boston's Balfour Beatty carriageway work and the A16 and John Adams Way",
 },
 "cleethorpes": {
  "region":"Cleethorpes and North East Lincolnshire",
  "nearby":["Grimsby","Scunthorpe","Skegness"],
  "snapshot":"iNeedWorkwear kits Cleethorpes' highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from North East Lincolnshire Council's in-house highways service to National Highways work on the A180, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Cleethorpes area's roads running",
  "s1loc":[
   "Cleethorpes is the coastal resort end of the A180, but its surrounding network is dominated by the Grimsby and Immingham port complex, one of the UK's largest by tonnage, generating constant heavy freight. North East Lincolnshire Council is the unitary highway authority, and its gangs work in Class 3 hi-vis beside that port-driven traffic.",
   "After roughly fifteen years under a private partnership that began with Balfour Beatty Workplace and became Equans, the council brought highways and related services back in house in July 2025, with around two hundred and seventy staff transferring to direct management. The long concrete sections of the A180 are a standing local maintenance talking point.",
   "National Highways operates the A180 dual carriageway from the M180 to Grimsby, then single carriageway toward Cleethorpes seafront, with the A46 running north to Isaac's Hill and the A160 feeding Immingham Dock. Trunk and port-access work alike mean fast roads, concrete-surface repair and very heavy freight.",
   "Surfacing, lining, drainage, lighting and winter gritting are all handled by Cleethorpes crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the area's carriageway, port-access and winter-maintenance work",
  "s2_intro":"Across Cleethorpes' council carriageway work and the National Highways A180",
 },
 "hatfield": {
  "region":"Hatfield and Hertfordshire",
  "nearby":["Welwyn Garden City","St Albans","Potters Bar"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Hatfield's highway maintenance teams and roadworks contractors, from Hertfordshire County Council's Ringway contract to National Highways work on the A1(M) and the Hatfield Tunnel, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Hatfield area's roads running",
  "s1loc":[
   "Hatfield is defined by the A1(M) and its tunnel, by the Galleria shopping centre built over the motorway in an aircraft-hangar form, and by the former de Havilland aerodrome now redeveloped as Hatfield Business Park. Hertfordshire County Council is the highway authority, and its gangs work in Class 3 hi-vis around that motorway-and-aviation-heritage setting.",
   "Hertfordshire retained Ringway as its term maintenance contractor on the new deal from October 2025, covering potholes, lighting, signals, gritting, grass cutting and improvement schemes, with Vinci as Ringway's parent group. The Hatfield Business Park on the old aerodrome generates commercial traffic off the A1001 and A414.",
   "National Highways operates the A1(M) through the town with junction 3 serving the Galleria and the Hatfield Tunnel carrying the motorway beneath the town, while the council holds the A414, the A1001 Comet Way and the A1057. Motorway-tunnel and connector work alike mean fast roads and significant structures.",
   "Resurfacing, lining, drainage, lighting and winter gritting put Hatfield crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the area's carriageway, motorway-corridor and winter-maintenance work",
  "s2_intro":"Across Hatfield's Ringway carriageway work and the National Highways A1(M)",
 },
 "bishop's stortford": {
  "region":"Bishop's Stortford and Hertfordshire",
  "nearby":["Harlow","Hertford","Hoddesdon"],
  "snapshot":"iNeedWorkwear kits Bishop's Stortford's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from Hertfordshire County Council's Ringway contract to National Highways work on the M11 and London Stansted, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Bishop's Stortford area's roads running",
  "s1loc":[
   "Bishop's Stortford sits on the M11 at junction 8 right beside London Stansted Airport, so its network carries heavy airport access, freight and commuter traffic, with the Birchanger Green services on the motorway. Hertfordshire County Council is the highway authority for the local roads, and its gangs work in Class 3 hi-vis along that airport corridor.",
   "Hertfordshire retained Ringway as its county term maintenance contractor on the new deal from October 2025, continuous since 2012, covering routine maintenance, potholes, lighting and gritting. Airport-related logistics and business parks cluster around Stansted and the A120 and M11 corridor.",
   "National Highways operates the M11 with junction 8 and 8A connecting the A120 dual carriageway toward Braintree and Colchester and the airport, while the A1250 Dunmow Road and A1060 are local routes, and the capacity-constrained junction has seen Essex Highways improvement schemes as the county boundary runs close to the town. Motorway and airport-access work alike mean fast roads and split highway authorities.",
   "Resurfacing, lining, drainage, lighting and winter gritting are all handled by Bishop's Stortford crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the area's carriageway, airport-corridor and winter-maintenance work",
  "s2_intro":"Across Bishop's Stortford's Ringway carriageway work and the National Highways M11",
 },
 "bicester": {
  "region":"Bicester and Oxfordshire",
  "nearby":["Banbury","Oxford","Aylesbury"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Bicester's highway maintenance teams and roadworks contractors, from Oxfordshire County Council's M Group Highways contract to National Highways work on the M40, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Bicester area's roads running",
  "s1loc":[
   "Bicester is an M40 town with formal Garden Town status, anchored by Bicester Village designer retail and Bicester Motion at the former RAF site, with large-scale growth including the North West Bicester eco-town. Oxfordshire County Council is the highway authority, and its gangs work in Class 3 hi-vis along the A41 and the town's ring road.",
   "The county runs its highways through Milestone, now trading as M Group Highways, which secured a new contract worth around eight hundred and forty million pounds from April 2025 covering more than four thousand eight hundred kilometres of road, footways, drainage, structures and winter service to 2033. Logistics land along the A41 and the garden-town growth drive sustained works.",
   "National Highways operates the M40 with junction 9 to the south interchanging the A34 toward Oxford and the A41 toward Bicester and Aylesbury, the A41 carrying around thirty-six thousand vehicles a day, while the ring road is formed from the A41, A4095, A4421 and Vendee Drive. Motorway-junction and ring-road work alike mean fast roads and heavy retail traffic.",
   "Resurfacing, lining, drainage, lighting and winter gritting put Bicester crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the area's carriageway, ring-road and winter-maintenance work",
  "s2_intro":"Across Bicester's M Group Highways carriageway work and the National Highways M40",
 },
 "chippenham": {
  "region":"Chippenham and Wiltshire",
  "nearby":["Melksham","Trowbridge","Bath"],
  "snapshot":"iNeedWorkwear kits Chippenham's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from Wiltshire Council's M Group Highways contract to National Highways work on the M4, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Chippenham area's roads running",
  "s1loc":[
   "Chippenham sits where the M4 at junction 17 meets the A350, the principal north-south spine through west Wiltshire toward Melksham and Trowbridge. Wiltshire Council is the unitary highway authority, and its gangs work in Class 3 hi-vis along that motorway-and-A350 corridor that stages maintenance across the northern county.",
   "The council runs its highways through Milestone, now trading as M Group Highways, on a five-year contract from April 2023 with an option to 2032, taking over from Ringway and covering potholes, drainage, lighting, gritting, bridges and verges plus the Parish Stewards who handle small local fixes. The Methuen Park and Bumpers Farm estates anchor local trade supply.",
   "National Highways operates the M4 just north of the town at junction 17, while the council-managed A350 is the key north-south corridor and the A4 runs east-west toward Bath and Calne, with recent bridge works at Jenkins Bridge in the town. Motorway and A350-corridor work alike mean fast roads and structures maintenance.",
   "Resurfacing, lining, drainage, lighting and winter gritting put Chippenham crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the area's carriageway, A350-corridor and winter-maintenance work",
  "s2_intro":"Across Chippenham's M Group Highways carriageway work and the National Highways M4 and A350",
 },
 "newbury": {
  "region":"Newbury and West Berkshire",
  "nearby":["Thatcham","Reading","Basingstoke"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Newbury's highway maintenance teams and roadworks contractors, from West Berkshire Council's term contract to National Highways work on the A34 and the Newbury bypass, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Newbury area's roads running",
  "s1loc":[
   "Newbury is defined by the A34 and the Newbury bypass, one of the most high-profile road schemes in UK history opened in 1998, which removed long-distance trunk traffic from the town centre. West Berkshire Council is the unitary highway authority, and its gangs work in Class 3 hi-vis along that national north-south corridor.",
   "The council has retendered its Highways Term Maintenance Contract in recent years, moving from VolkerHighways to Marlborough Highways on a deal worth around a hundred and fifty million pounds, covering reactive and planned maintenance, winter service and asset management. The Hambridge Lane and Faraday Road estates and the Thatcham industrial areas support local trade.",
   "National Highways operates the A34 trunk route past the town as the strategic Midlands-to-south-coast corridor and the M4 to the north at junction 13, while the A4 runs east-west through the area. Trunk-bypass and motorway work alike mean fast roads and tight management on a key national axis.",
   "Resurfacing, lining, drainage, lighting and winter gritting put Newbury crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the area's carriageway, bypass-corridor and winter-maintenance work",
  "s2_intro":"Across Newbury's council carriageway work and the National Highways A34 and M4",
 },
 "wokingham": {
  "region":"Wokingham and Berkshire",
  "nearby":["Reading","Woodley","Bracknell"],
  "snapshot":"iNeedWorkwear kits Wokingham's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from Wokingham Borough Council's Balfour Beatty Living Places contract to National Highways work on the M4 and the council-run A329(M), with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Wokingham area's roads running",
  "s1loc":[
   "Wokingham is unusual in maintaining its own motorway, the A329(M), a four-mile motorway-standard route from west of Bracknell to north-west of Winnersh that is the council's responsibility rather than National Highways. Wokingham Borough Council is the Berkshire unitary highway authority, and its gangs work in Class 3 hi-vis on that rare council motorway and the surrounding network.",
   "Balfour Beatty Living Places holds the highway network term maintenance contract at around four million pounds a year plus a street-lighting deal, and delivered the council's largest-ever roads programme of eight schemes worth about a hundred and twenty-four million pounds under the Scape framework. The Molly Millars Lane estate and Winnersh Triangle business park anchor local activity.",
   "National Highways operates the M4 along the south of the borough at junction 10, while the council holds the A329(M) and the A329 distributor, and an extensive programme of distributor and relief roads supports housing growth, including the North and South Wokingham Distributor Roads and the Winnersh Relief Road. Motorway and distributor work alike mean fast roads and developer-funded schemes.",
   "Resurfacing, lining, drainage, lighting and winter gritting put Wokingham crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the area's carriageway, distributor-road and winter-maintenance work",
  "s2_intro":"Across Wokingham's Balfour Beatty Living Places carriageway work and the M4 and A329(M)",
 },
 "farnham": {
  "region":"Farnham and Surrey",
  "nearby":["Aldershot","Farnborough","Guildford"],
  "snapshot":"iNeedWorkwear supplies Class 3 hi-vis, safety boots, waterproofs and branded workwear to Farnham's highway maintenance teams and roadworks contractors, from Surrey County Council's Ringway contract to National Highways work on the A31 Hog's Back, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Farnham area's roads running",
  "s1loc":[
   "Farnham is defined by the A31 Hog's Back, the distinctive ridge route along the North Downs between Guildford and Farnham, and by its position just south-west of the A331 Blackwater Valley corridor toward the M3. Surrey County Council is the highway authority, and its gangs work in Class 3 hi-vis where those regional routes converge.",
   "Surrey's core maintenance contract has been held by Ringway since 2022 on a roughly ten-year deal with options that could extend up to twenty-one years, taking over from Kier and continuing the training academy. Recent works on the A331 Blackwater Valley Route and the A31 Hog's Back, including a new slip lane removing the Runfold roundabout movement, have been delivered in the area.",
   "National Highways operates trunk sections of the A31 including the Hog's Back, while the modern Farnham bypass joins the A331 at Tongham, the A325 heads toward Aldershot and Farnborough and the A287 is a key local route, the trunk-versus-local split varying by section. Ridge-route and Blackwater Valley work alike mean fast roads and section-specific responsibilities.",
   "Resurfacing, lining, drainage, lighting and winter gritting put Farnham crews out in Class 3 hi-vis beside running traffic.",
  ],
  "kit_loc":"across the area's carriageway, ridge-route and winter-maintenance work",
  "s2_intro":"Across Farnham's Ringway carriageway work and the National Highways A31 Hog's Back",
 },
 "feltham": {
  "region":"Feltham and West London",
  "nearby":["Hounslow","Staines","Hayes"],
  "snapshot":"iNeedWorkwear kits Feltham's highway maintenance teams and roadworks contractors with Class 3 hi-vis, safety boots, waterproofs and branded workwear, from the London Borough of Hounslow's Hounslow Highways PFI to the Transport for London A30 and A312, with name and ID branding placed off the certified reflective area and multi-depot supply.",
  "s1_head":"Kitting the people who keep the Feltham area's roads running",
  "s1loc":[
   "Feltham sits immediately next to Heathrow Airport in west London, where the A312 Causeway and the A30 Great South West Road funnel airport, freight and commuter traffic and the M3 joins the network to the south-west. The London Borough of Hounslow is the highway authority, and its gangs work in Class 3 hi-vis along that dense airport corridor.",
   "Hounslow maintains its adopted network through Hounslow Highways, a roughly twenty-five-year PFI partnership with VINCI Concessions and Ringway covering carriageways, footways, lighting, drainage and structures, distinct from the term-contract model used elsewhere. The council operates a depot on Pears Road in Feltham, with Heathrow-related logistics estates around the A30 and A312.",
   "National Highways operates the wider strategic network, while Transport for London runs the red routes around Feltham, with the A312, the A30 Great South West Road and the A314 the key corridors and the M3 to the south-west. Red-route and airport-access work alike mean fast roads and a distinctive PFI delivery model.",
   "Resurfacing, lining, drainage, lighting and winter gritting are all handled by Feltham crews in Class 3 hi-vis on the carriageway.",
  ],
  "kit_loc":"across the area's carriageway, airport-corridor and winter-maintenance work",
  "s2_intro":"Across Feltham's Hounslow Highways carriageway work and the TfL A30 and A312",
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
