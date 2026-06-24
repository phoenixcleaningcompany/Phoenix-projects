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
