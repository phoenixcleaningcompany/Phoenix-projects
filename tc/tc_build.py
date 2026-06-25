#!/usr/bin/env python3
# TC (Telecoms & Network Installation) series builder v1.0 - read SPEC.md/CLAUDE.md
# HYBRID / Template A+B (audience BOTH): large installation contractors with
# fleets of engineers (procurement / trade account) AND small subcontractors and
# sole-trader installers (direct online, no account) - given EQUAL weight (DC-style).
# DIFFERENTIATOR = THREE JOBS AT ONCE: branded/identifiable (engineer legitimate
# on the doorstep and at the cabinet) + visible (hi-vis EN ISO 20471 for roadside
# and street works) + weatherproof/practical (softshells, fleeces, waterproofs,
# cargo trousers, safety boots for all-weather field work). Lead = POLO + HI-VIS +
# SOFTSHELL. MEDIUM depth, LOW local variation (generic shared paras in OWNER/
# PRESENT/NARROW pools, not per-town s1loc - see s1_paras). Headroom from the
# start: cards pooled 3 ways (build_grid), FAQ/WHY/PRESENT/NARROW at 6 variants.
# softshell is TC CORE (TRI_LEAD), NOT bleed. Exactly 14 .com + 1 community per
# page. No JS, no entities, no delivery claims, no Chapter 8 (generic hi-vis only).
# Nearby = geographic, hand-authored, on TC_towns.csv (no rank fallback).
import re, os, json, sys, csv
import hashlib
def pick(key, salt, n):
    h = hashlib.md5((salt + '|' + str(key).lower()).encode()).digest()
    return int.from_bytes(h[:4], 'big') % n

def _find_base():
    here = os.path.dirname(os.path.abspath(__file__))
    for p in (os.path.join(here,'tc-london.html'),'tc-london.html',
              '/mnt/user-data/outputs/tc-london.html','/home/claude/tckit/tc-london.html'):
        if os.path.exists(p): return p
    sys.exit("ERROR: tc-london.html (base template) not found beside tc_build.py")

BASE = open(_find_base(), encoding='utf-8').read()
DOMAIN = 'https://www.ineedworkwear.uk'

def between(start, end, src=BASE):
    i = src.index(start); j = src.index(end, i+len(start)); return src[i:j]
def aria_block(aria):
    k = BASE.index(aria)
    i = BASE.rfind('<div class="tc-wrap"><div class="tc-illust">', 0, k)
    j = BASE.index('</div></div></div>', k) + len('</div></div></div>')
    return BASE[i:j]

CSS      = between('<style>', '</style>') + '</style>'
HEADER   = between('<div class="tc-header">', '\n<div class="tc-hero">')
STATS    = between('<div class="tc-stats">', '\n<div class="tc-cta-bar">')
GARMENT  = between('<div class="tc-wrap"><div class="tc-illust"><div class="tc-garment-row">', '\n<div class="tc-section">')
EMB      = aria_block('Embroidery machine stitching')
SIGNPOST = aria_block('telecoms and network signpost')
PREMISES = aria_block('serving network installers across')
ORDER    = aria_block('Order telecoms and network workwear online')
CONTACT  = BASE[BASE.index('<div class="tc-contact-block">'):
                BASE.index('</div></div></div>', BASE.index('<div class="tc-contact-block">'))+len('</div></div></div>')]
FOOTER   = BASE[BASE.index('<footer class="tc-footer">'):BASE.index('</footer>')+len('</footer>')]

def signpost_town(town):
    n = len(town)
    size = 22 if n <= 8 else 19 if n <= 11 else 16 if n <= 15 else 13 if n <= 20 else 11
    tl = ' textLength="200" lengthAdjust="spacingAndGlyphs"' if n > 11 else ''
    return (f'<text x="230" y="62" text-anchor="middle" font-family="Arial,sans-serif" '
            f'font-weight="800" font-size="{size}" fill="#fff"{tl}>{town.upper()}</text>')

TC_PRODUCTS = ["Polo Shirts and T-Shirts","Cargo Trousers and Work Trousers","Hi-Vis Vests and Jackets",
 "Softshell Jackets","Fleeces and Mid-Layers","Waterproofs and Outdoor Jackets",
 "Safety Boots and Footwear","Embroidery, Names and ID Branding"]

def _card(n,d): return f'<div class="tc-product-card"><div class="tc-product-name">{n}</div><div class="tc-product-detail">{d}</div></div>'
CARD_DETAILS=[
 ("Polo Shirts and T-Shirts",[
   "Branded polos and t-shirts for everyday field work, breathable and hard-wearing, the core layer that identifies an engineer on the doorstep and at the cabinet.",
   "Breathable, durable branded polos and t-shirts for the everyday, the layer that marks an engineer out as a legitimate contractor on the doorstep and at the cabinet.",
   "Hard-wearing branded polos and t-shirts for day-to-day field work, the dependable everyday layer that identifies an engineer to the customer and the public."]),
 ("Cargo Trousers and Work Trousers",[
   "Tough cargo and work trousers with the pockets engineers need for tools and test kit, built to take kneeling at joint boxes and long days on site.",
   "Hard-wearing cargo and work trousers with pockets for tools and test kit, made to take kneeling at joint boxes and chambers and long days in the field.",
   "Durable cargo and work trousers with tool and test-kit pockets, built for kneeling at cabinets and joint boxes and standing up to long days on site."]),
 ("Hi-Vis Vests and Jackets",[
   "Hi-vis vests and jackets to EN ISO 20471 for visibility on the roadside and at street cabinets, poles and joint boxes where engineers work near traffic.",
   "EN ISO 20471 hi-vis vests and jackets for roadside and street-works visibility at cabinets, poles and joint boxes where engineers work close to traffic.",
   "Hi-vis vests and jackets to EN ISO 20471, keeping engineers visible on the roadside and at street cabinets, poles and chambers near passing traffic."]),
 ("Softshell Jackets",[
   "Branded softshell jackets that block wind and light rain while staying easy to work in, the everyday outer layer for field engineers through most of the year.",
   "Branded softshells that cut wind and light rain yet stay easy to work in, the go-to outer layer for field engineers across most of the year.",
   "Wind-and-shower-resistant branded softshell jackets that stay easy to move in, the everyday field-engineer outer layer for most of the year."]),
 ("Fleeces and Mid-Layers",[
   "Warm branded fleeces and mid-layers for cold cabinets, early starts and winter field work, worn under a softshell or hi-vis when the temperature drops.",
   "Branded fleeces and mid-layers for cold mornings and winter field work, an easy warm layer under a softshell or hi-vis when the temperature drops.",
   "Cosy branded fleeces and mid-layers for cold cabinets and early starts, layered under a softshell or hi-vis through the colder months."]),
 ("Waterproofs and Outdoor Jackets",[
   "Waterproof jackets and trousers for the wet days, keeping engineers dry and presentable at the cabinet, up the pole or on customer premises in all weather.",
   "Waterproof jackets and trousers for the wet, keeping engineers dry and presentable at the cabinet, up the pole and on customer premises whatever the weather.",
   "Weatherproof jackets and trousers for the rain, keeping field engineers dry and smart at cabinets, on poles and on customer premises in all conditions."]),
 ("Safety Boots and Footwear",[
   "Supportive, protective safety boots with grip for street works, cabinets, ladders and customer premises, built for long days on your feet in all conditions.",
   "Protective safety boots with grip for street works, ladders, cabinets and customer premises, built for long field days on your feet in all conditions.",
   "Grippy, supportive safety boots for street works, ladders, cabinets and customer premises, made for long days on your feet whatever the ground and weather."]),
 ("Embroidery, Names and ID Branding",[
   "In-house embroidery of your company name, logo and engineer names onto polos, softshells, fleeces and hi-vis, so a contractor fleet or a sole trader looks consistent and professional.",
   "In-house embroidery of your company name, logo and engineer names across polos, softshells, fleeces and hi-vis, so a fleet or a sole-trader installer always looks consistent.",
   "Company name, logo and engineer names embroidered in-house onto polos, softshells, fleeces and hi-vis, so a contractor crew or a single van looks coordinated and professional."]),
]
GRID_ORDER=[(0,1,2,3,4,5,6,7),(1,0,2,3,4,5,6,7),(0,1,3,2,4,5,6,7),(0,2,1,3,4,5,6,7)]
def build_grid(town):
    order = GRID_ORDER[pick(town,'gord',len(GRID_ORDER))]
    cards=[]
    for i in order:
        name,variants = CARD_DETAILS[i]
        cards.append(_card(name, variants[pick(town,f'g{i}',len(variants))]))
    return '<div class="tc-product-grid">'+''.join(cards)+'</div>'

TRUST_POOL=[
 "Branded polos, cargo trousers, hi-vis, softshells and safety boots for telecoms and network engineers - trade accounts or order direct online",
 "Branded polos, cargo trousers, hi-vis, softshells and safety boots for telecoms and network engineers - trade accounts for fleets, direct online for subbies",
 "Trusted by telecoms contractors, network installers and field engineers across the UK for branded polos, hi-vis and softshells - trade or direct",
 "Branded workwear - polos, cargo trousers, hi-vis, softshells and safety boots - for telecoms and network engineers across the UK, trade or direct online",
]
S2INTRO_POOL=[
 "Whether you are a large installation contractor with a fleet of engineers or a one-person subcontractor in {t}, the range is built to kit you from one place: branded polos and cargo trousers, hi-vis for the roadside, and softshells, fleeces, waterproofs and safety boots for all-weather field work.",
 "A large {t} installation contractor with a fleet of engineers, or a one-person subcontractor, is kitted from one place: branded polos and cargo trousers, hi-vis for the roadside, and softshells, fleeces, waterproofs and safety boots for all-weather field work.",
 "For a {t} contractor fleet or a sole-trader installer, the range covers you from one place: branded polos and cargo trousers, hi-vis for the roadside, and softshells, fleeces, waterproofs and safety boots for all-weather field work.",
 "Whether it is a fleet of engineers or a single subcontractor in {t}, you are kitted from one place: branded polos and cargo trousers, hi-vis for the roadside, plus softshells, fleeces, waterproofs and safety boots for all-weather field work.",
]
EMB_P1_POOL=[
 "In telecoms and network installation, the engineer is the face of the contract. They are on a customer doorstep, in a comms room or working at a cabinet in full public view, and how they look decides whether a {t} customer and the public see a legitimate, professional operation. A clean, branded polo, softshell or hi-vis turns an engineer into an identifiable representative of a real contractor, not a stranger poking around the network.",
 "In telecoms and network installation, the engineer is the face of the contract. On a {t} doorstep, in a comms room or at a cabinet in full public view, how the engineer looks decides whether the customer and the public see a legitimate, professional operation. A clean, branded polo, softshell or hi-vis makes an engineer an identifiable representative of a real contractor rather than a stranger.",
 "The engineer is the face of the contract in this trade. Standing on a {t} doorstep, in a comms room or at a street cabinet in full public view, how they look decides whether the customer and the public read a legitimate, professional operation. A clean, branded polo, softshell or hi-vis turns an engineer into a recognisable representative of a real contractor, not a stranger at the network.",
 "In network installation, the engineer is the contract made visible. On a {t} doorstep, in a comms room or at a cabinet where everyone can see, how the engineer presents decides whether a customer trusts a legitimate operation. A clean, branded polo, softshell or hi-vis makes them an identifiable part of a real contractor rather than a stranger poking at the network.",
]
EMB_P2_POOL=[
 "We brand in-house, which means your company name and logo are embroidered onto polos, softshells, fleeces and hi-vis, finished to survive heavy site use and frequent washing. Send your artwork once, we hold it on file, and every reorder, new engineer and new crew matches the last, so whether it is a single subcontractor or a fleet of field teams, the {t} operation looks consistent on every doorstep.",
 "Branding is done in-house onto polos, softshells, fleeces and hi-vis - your company name and logo embroidered and finished to survive heavy site use and frequent washing. We hold your artwork on file, so every reorder, new engineer and crew matches, and whether it is one subcontractor or a fleet, the {t} operation looks consistent on every doorstep.",
 "Your company name and logo are embroidered in-house onto polos, softshells, fleeces and hi-vis, finished to take heavy site use and frequent washing. Held on file, your artwork reproduces on every reorder, new engineer and crew, so a {t} operation looks consistent whether it is a single van or a fleet of field teams.",
 "We badge in-house, embroidering your company name and logo onto polos, softshells, fleeces and hi-vis and finishing them to survive heavy site use and washing. Held on file, your branding matches on every reorder and new starter, so a {t} operation looks consistent whether it is a sole trader or a fleet.",
]
EMB_P3_POOL=[
 "For a growing contractor, that consistency is the point. We hold your branding and sizes on file, so onboarding a new engineer, expanding a crew or kitting a second region reproduces exactly the same branded uniform every time, without anyone having to re-supply artwork or guess at a match.",
 "For a contractor that is growing, consistency is the value. We hold your branding and sizes on file, so a new engineer, an expanded crew or a second region comes back exactly the same branded uniform every time, with no artwork to re-supply.",
 "As a contractor grows and crews change, consistency matters. We keep your branding and sizes on file, so onboarding a new engineer, expanding a crew or kitting a second region reproduces the same branded uniform each time.",
 "For a growing contractor, that consistency is the whole point as crews change. We hold branding and sizes on file, so a new engineer, an expanded crew or a second region reproduces exactly the same branded uniform every time, with nothing to re-supply.",
]
CON_HEAD="Branded, Hi-Vis and All-Weather: Kit for the Field Engineer"
CON_P1_POOL=[
 "Telecoms and network installation workwear has to earn its place three ways at once, and the right kit covers all three. The first is branding. The engineer is the visible face of the contract on the doorstep and at the cabinet, so a branded polo, softshell or hi-vis with the company name tells a {t} customer and the public this is a legitimate, professional operation, and turns a subcontractor into a recognisable part of a real contractor.",
 "Telecoms and network installation workwear earns its place three ways at once, and the right kit does all three. First, branding: the engineer is the visible face of the contract on the doorstep and at the cabinet, so a branded polo, softshell or hi-vis with the company name tells a {t} customer and the public this is a legitimate, professional operation, and makes a subcontractor a recognisable part of a real contractor.",
 "This workwear has to do three jobs at once, and the right kit covers them all. The first is branding. The engineer is the visible face of the contract on a {t} doorstep and at the cabinet, so a branded polo, softshell or hi-vis with the company name signals a legitimate, professional operation to the customer and the public, and turns a subcontractor into a recognisable part of a real contractor.",
 "Telecoms workwear has to earn its place three ways at once. The first is branding: the engineer is the visible face of the contract on the {t} doorstep and at the cabinet, so a branded polo, softshell or hi-vis with the company name tells the customer and the public this is a legitimate, professional operation, and makes a subcontractor a recognisable part of a real contractor.",
]
CON_P2_POOL=[
 "The second is visibility, and the third is weather. Much of the work is outdoors and roadside: at street cabinets, up poles, in joint boxes and footway chambers, often near moving traffic, which is why hi-vis to EN ISO 20471 is core kit. And it runs all year in all conditions, so softshells, fleeces and waterproofs keep an engineer warm and dry, cargo trousers carry the tools, and safety boots handle the ground, the ladder and the kerb.",
 "The second is visibility and the third is weather. A lot of the work is outdoors and roadside - at street cabinets, up poles, in joint boxes and chambers, often near moving traffic - so hi-vis to EN ISO 20471 is core kit. And it runs all year in all conditions, so softshells, fleeces and waterproofs keep an engineer warm and dry, cargo trousers carry the tools, and safety boots handle the ground, the ladder and the kerb.",
 "The second job is visibility and the third is weather. Much of the work happens outdoors and roadside, at cabinets, up poles and in joint boxes and chambers near moving traffic, which makes hi-vis to EN ISO 20471 core kit. It runs all year in all conditions too, so softshells, fleeces and waterproofs keep an engineer warm and dry, cargo trousers carry the tools, and safety boots handle the ground, ladder and kerb.",
 "The second is visibility, the third is weather. So much of the work is outdoors and roadside - cabinets, poles, joint boxes and footway chambers near traffic - that hi-vis to EN ISO 20471 is core kit. And because it runs all year in all conditions, softshells, fleeces and waterproofs keep an engineer warm and dry, cargo trousers carry the tools, and safety boots handle the ground, the ladder and the kerb.",
]
CON_P3_POOL=[
 'The value is one supplier covering the whole field uniform for both the fleet and the subbie, all branded the same. We hold your {t} company name, logo and sizes on file and supply polos, hi-vis, softshells and the rest together, so onboarding a new engineer or kitting a crew reproduces the same branded uniform every time. Browse the range at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
 'The value is one supplier for the whole field uniform, the fleet and the subbie alike, all branded the same. We hold your {t} company name, logo and sizes on file and supply polos, hi-vis, softshells and the rest together, so onboarding a new engineer or kitting a crew reproduces the same branded uniform every time. Browse the range at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
 'The value is having one supplier cover the whole field uniform for both the fleet and the sole trader, branded the same. We keep your {t} company name, logo and sizes on file and supply polos, hi-vis, softshells and the rest together, so a new engineer or a fresh crew comes back the same branded uniform every time. Browse the range at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
 'The value is one supplier for the entire field uniform, fleet and subbie together, all branded the same. We hold your {t} company name, logo and sizes on file and supply polos, hi-vis, softshells and the rest as one, so onboarding a new engineer or kitting a crew reproduces the same uniform every time. Browse the range at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
]
ACC_HEAD="Trade Accounts for Fleets, Direct Online for Subcontractors"
ACC_P1_POOL=[
 "Telecoms and network installation splits into two kinds of buyer, and we have built ordering for both. For a large installation contractor with a fleet of engineers, a trade account is the practical route. It adds managed reordering, agreed pricing and a held kit list with your branding and sizes on file, so onboarding a new engineer, expanding a crew or kitting a second region is fast and consistent for a {t} operation. Send your headcount, your logo and your sizes and we will build the branded uniform list and hold it.",
 "Telecoms and network installation has two kinds of buyer, and ordering is built for both. For a large {t} contractor with a fleet of engineers, a trade account is the practical route: managed reordering, agreed pricing and a held kit list with your branding and sizes on file, so onboarding a new engineer, expanding a crew or kitting a second region is fast and consistent. Send your headcount, logo and sizes and we will build the branded uniform list and hold it.",
 "This trade splits into two kinds of buyer, and we have built ordering for both. For a large installation contractor with a fleet of engineers in {t}, a trade account is the practical route, adding managed reordering, agreed pricing and a held kit list with your branding and sizes on file, so onboarding an engineer, expanding a crew or kitting a second region stays fast and consistent. Send your headcount, logo and sizes and we will build and hold the list.",
 "Network installation splits into two kinds of buyer, and ordering suits both. For a large {t} contractor running a fleet of engineers, a trade account is the practical route: managed reordering, agreed pricing and a held kit list with your branding and sizes on file, so onboarding a new engineer, growing a crew or kitting a second region is fast and consistent. Send your headcount, logo and sizes and we build the branded uniform list and hold it.",
]
ACC_P2_POOL=[
 "For a sole-trader installer or a small subcontractor, ordering direct online is quickest and needs no account at all. Browse the range, pick your polos, cargo trousers, hi-vis, softshell and boots, choose your sizes, send your logo once and check out. There is no minimum and nothing to set up, your kit is dispatched on standard lead times with embroidery added in-house, and your logo is held on file so the next order matches.",
 "For a sole-trader installer or small subcontractor, direct online is quickest and needs no account: browse the range, pick your polos, cargo trousers, hi-vis, softshell and boots, choose sizes, send your logo once and check out. No minimum and nothing to set up, dispatched on standard lead times with embroidery in-house, and your logo held on file so the next order matches.",
 "A sole-trader installer or small subcontractor orders quickest direct online, no account needed: browse the range, pick your polos, cargo trousers, hi-vis, softshell and boots, add sizes, send the logo once and check out. There is no minimum and no setup, kit is dispatched on standard lead times with in-house embroidery, and your logo is held on file for the next order.",
 "For a sole trader or small subcontractor, the quickest route is direct online with no account: browse, pick your polos, cargo trousers, hi-vis, softshell and boots, choose sizes, send your logo once and check out, with no minimum and nothing to set up, dispatched on standard lead times with embroidery in-house and your logo held on file.",
]
ACC_P3_POOL=[
 "Both routes are branded in-house from the same supplier, so whether you are kitting forty engineers in {t} or just yourself, the workwear is consistent, professional and ready for the field. Most contractors run the trade account for the fleet and point their subbies at the direct online route, and everyone ends up matching.",
 "Both routes are branded in-house by the same supplier, so whether you are kitting forty {t} engineers or just yourself, the kit is consistent, professional and field-ready. Most contractors use the trade account for the fleet and send their subbies to the direct online route, and everyone matches.",
 "Both routes come branded in-house from one supplier, so whether it is forty engineers across {t} or just you, the workwear is consistent, professional and ready for the field. Most contractors run a trade account for the fleet and point subbies at direct online, and the whole job matches.",
 "Both routes are branded in-house by one supplier, so whether you kit forty engineers in {t} or only yourself, the kit stays consistent, professional and field-ready. Most contractors keep the fleet on a trade account and send their subbies direct online, and everyone ends up matching.",
]
ACC_P4_POOL=[
 'Set up a trade account for a fleet at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>, or order direct online with no account at <a href="https://www.ineedworkwear.com">iNeedWorkwear</a>.',
 'Set up a trade account for a fleet at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>. For a subcontractor, order direct online with no account at <a href="https://www.ineedworkwear.com">iNeedWorkwear</a>.',
 'Open a trade account for a fleet at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>, or order direct online with no account as a subcontractor at <a href="https://www.ineedworkwear.com">iNeedWorkwear</a>.',
 'Set up a fleet trade account at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>, or as a subcontractor order direct online with no account at <a href="https://www.ineedworkwear.com">iNeedWorkwear</a>.',
]
WHY_P1_POOL=[
 "A telecoms contractor or network installer in {t} whose engineers turn out in clean, branded polos, hi-vis and softshells looks professional and legitimate to every customer and to the public at the roadside, and iNeedWorkwear supplies that whole look from a single place, branded in-house, on a trade account for the fleet or direct online for the subbie, so the operation is consistent from the first doorstep.",
 "A {t} telecoms contractor or network installer whose engineers wear clean, branded polos, hi-vis and softshells looks professional and legitimate to every customer and to the public at the roadside, and iNeedWorkwear supplies that whole look from one place, branded in-house, on a trade account for the fleet or direct online for the subbie, so the operation is consistent from the first doorstep.",
 "When a {t} telecoms contractor or network installer turns its engineers out in clean, branded polos, hi-vis and softshells, it looks professional and legitimate to every customer and to the public at the roadside, and we supply that whole look from a single place, branded in-house, on a trade account or direct online, so the operation is consistent from the first doorstep.",
 "A telecoms contractor or installer in {t} whose engineers wear clean, branded polos, hi-vis and softshells reads as professional and legitimate to every customer and to the public at the kerbside, and we supply that whole look from one place, branded in-house, on a trade account for the fleet or direct online for the subbie, so it stays consistent from the first doorstep.",
 "A {t} telecoms or network contractor whose engineers turn out in clean, branded polos, hi-vis and softshells looks legitimate and professional to every customer and to the public at the roadside, and we supply the whole look from one place, branded in-house, trade or direct, so even a sole trader carries chain-grade polish.",
 "In {t}, a telecoms contractor or network installer whose engineers wear clean, branded polos, hi-vis and softshells looks professional from the first glance on the doorstep, and iNeedWorkwear supplies that whole look from one place, branded in-house, on a trade account for the fleet or direct online for the subbie, so the operation stays consistent.",
]
WHY_P2_POOL=[
 "It is built for both ends of the trade. A large contractor onboarding engineers gets managed reordering and a held kit list, while a sole-trader installer gets a quick, no-account direct route online, and both come back the same branded kit, so a growing operation never ends up with a patchwork of mismatched workwear as it scales.",
 "It is built for both ends of the trade. A large contractor onboarding engineers gets managed reordering and a held kit list, and a sole-trader installer gets a quick, no-account direct route online, with both coming back the same branded kit, so a growing operation avoids a patchwork of mismatched workwear as it scales.",
 "It works for both ends of the trade. A large contractor onboarding engineers gets managed reordering and a held kit list, while a one-van installer gets a quick, no-account online route, and both return the same branded kit, so a scaling operation never drifts into mismatched workwear.",
 "It suits both ends of the trade. A large contractor onboarding engineers gets managed reordering and a held kit list, a sole-trader installer gets a fast no-account online route, and both come back the same branded kit, so a growing operation never ends up with mismatched workwear as it scales.",
 "It is made for both ends of the trade. The large contractor gets managed reordering and a held kit list for onboarding engineers, the sole trader gets a quick no-account online route, and both return the same branded kit, so scaling up never means a patchwork of mismatched workwear.",
 "It covers both ends of the trade. A large contractor onboarding engineers leans on managed reordering and a held kit list, a sole-trader installer uses the quick no-account online route, and both come back the same branded kit, so a growing operation stays matched rather than mismatched.",
]
WHY_P3_POOL=[
 "The range covers what field work actually demands: polos and cargo trousers for the everyday, hi-vis for the roadside, and softshells, fleeces, waterproofs and safety boots for all-weather outdoor work at cabinets, poles and on customer premises. It is a focused, practical range, so choosing, ordering and reordering stay quick for a busy contractor or a busy subbie.",
 "The range covers what field work really demands: polos and cargo trousers for the everyday, hi-vis for the roadside, and softshells, fleeces, waterproofs and safety boots for all-weather outdoor work at cabinets, poles and on customer premises. It is focused and practical, so choosing, ordering and reordering stay quick for a busy contractor or subbie.",
 "Everything in the range reflects what field work demands: polos and cargo trousers for the everyday, hi-vis for the roadside, and softshells, fleeces, waterproofs and safety boots for all-weather work at cabinets, poles and on customer premises. The range is focused and practical, so ordering and reordering stay quick for a busy contractor or subbie.",
 "The range is built around what field work actually demands: polos and cargo trousers for the everyday, hi-vis for the roadside, and softshells, fleeces, waterproofs and safety boots for all-weather outdoor work at cabinets, poles and on premises, so choosing and reordering stay quick for a busy contractor or subbie.",
 "It is a focused, practical range mapped to field work: polos and cargo trousers for the everyday, hi-vis for the roadside, and softshells, fleeces, waterproofs and safety boots for all-weather work at cabinets, poles and on customer premises, which keeps choosing, ordering and reordering fast for a busy contractor or subbie.",
 "The range stays focused on what field work needs: polos and cargo trousers for the everyday, hi-vis for the roadside, and softshells, fleeces, waterproofs and safety boots for all-weather outdoor work at cabinets, poles and on premises, so a busy contractor or subbie can choose and reorder in minutes.",
]
WHY_P4_POOL=[
 "And everything is branded in-house, with your company name and logo embroidered under our control and held on file, ready for the next order, the next engineer or the next crew, so every piece matches what the team already wears and a new starter looks the part from their first shift.",
 "And everything is branded in-house, your company name and logo embroidered under our control and held on file, ready for the next order, engineer or crew, so every piece matches what the team already wears and a new starter looks the part from day one.",
 "And it is all branded in-house, with your company name and logo embroidered under our control and kept on file, ready for the next order, the next engineer or the next crew, so every piece matches the team and a new starter looks right from their first shift.",
 "And everything is branded in-house, your company name and logo embroidered under our control and held on file for the next order, engineer or crew, so each piece matches what the team wears and a new starter looks the part from their first shift.",
 "And the whole lot is branded in-house, with your name and logo embroidered under our control and held on file, ready for the next order, engineer or crew, so every piece matches the team and a new starter looks established from day one.",
 "And it is all branded in-house, your company name and logo embroidered under our control and on file, ready for the next order, the next engineer or the next crew, so every piece lines up with what the team already wears and a new starter looks the part immediately.",
]
ORD_P1_POOL=[
 "iNeedWorkwear supplies branded polos, cargo trousers, hi-vis, softshells, fleeces, waterproofs and safety boots to telecoms contractors, network installers and field engineers across {region}, all embroidered in-house with the company name.",
 "We supply branded polos, cargo trousers, hi-vis, softshells, fleeces, waterproofs and safety boots to telecoms contractors, network installers and field engineers across {region}, all embroidered in-house with the company name.",
 "Across {region}, iNeedWorkwear kits telecoms contractors, network installers and field engineers in branded polos, cargo trousers, hi-vis, softshells, fleeces, waterproofs and safety boots, all embroidered in-house with the company name.",
 "From a single van to a fleet across {region}, iNeedWorkwear supplies branded polos, cargo trousers, hi-vis, softshells, fleeces, waterproofs and safety boots to telecoms and network engineers, all embroidered in-house.",
]
ORD_P2_POOL=[
 "For a sole-trader installer or small subcontractor, ordering direct online is quickest and needs no account: browse the range, pick your polos, cargo trousers, hi-vis, softshell and boots, add your sizes, send your logo once and check out. Your kit is dispatched on standard lead times with embroidery added in-house, and your logo is held on file so the next order matches.",
 "For a sole-trader installer or small subcontractor, direct online is quickest and needs no account: browse, pick your polos, cargo trousers, hi-vis, softshell and boots, add sizes, send your logo once and check out. Your kit ships on standard lead times with embroidery in-house, and your logo is held on file so the next order matches.",
 "A sole-trader installer or small subcontractor orders quickest direct online, no account needed: browse the range, pick your polos, cargo trousers, hi-vis, softshell and boots, add sizes, send the logo once and check out. Kit is dispatched on standard lead times with in-house embroidery, and your logo is held on file for the next order.",
 "For a sole trader or small subcontractor, the quickest route is direct online with no account: browse the range, pick your polos, cargo trousers, hi-vis, softshell and boots, add your sizes, send your logo once and check out, dispatched on standard lead times with embroidery in-house and your logo held on file.",
]
ORD_P3_POOL=[
 "For a larger installation contractor with a fleet of engineers, a trade account adds managed reordering and agreed pricing: send your headcount, your logo and your sizes and we will build a branded uniform list and hold it on file, so new engineers and new crews are onboarded in matching kit.",
 "For a larger installation contractor with a fleet of engineers, a trade account brings managed reordering and agreed pricing: send your headcount, logo and sizes and we will build a branded uniform list and hold it on file, so new engineers and crews are onboarded in matching kit.",
 "A larger installation contractor with a fleet of engineers can use a trade account for managed reordering and agreed pricing: send your headcount, logo and sizes and we will build a branded uniform list and hold it on file, so new engineers and crews onboard in matching kit.",
 "For a larger contractor with a fleet of engineers, a trade account adds managed reordering and agreed pricing: send your headcount, logo and sizes and we will build a branded uniform list and keep it on file, so new engineers and new crews are onboarded in matching kit.",
]
SELF_POOL=[
 'Starting up as a telecoms subcontractor and need kit now? Browse the full range, add your sizes and order direct on self-service checkout at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
 'Just gone out on your own as an installer? Browse the range, add sizes and order direct on self-service checkout at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
 'Setting up as a telecoms or network subcontractor and need kit today? Browse the full range, add your sizes and order direct on self-service checkout at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
 'Need a field-engineer uniform sorted now? Browse the range, add sizes and order direct on self-service checkout at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
]
SORTED_POOL=[
 '<h3>Telecoms and Network Workwear, Sorted</h3><p>From branded polos and cargo trousers to hi-vis, softshells, waterproofs and safety boots, get field-ready workwear built for telecoms and network engineers at fair prices - embroidered in-house with your company name, on a trade account for the fleet or ordered direct online with no account.</p><p><a href="https://www.ineedworkwear.com">Browse telecoms and network workwear at iNeedWorkwear</a></p>',
 '<h3>Telecoms and Network Workwear, Sorted</h3><p>Branded polos and cargo trousers, plus hi-vis, softshells, waterproofs and safety boots - field-ready workwear for telecoms and network engineers at fair prices, embroidered in-house with your company name, on a trade account or ordered direct online with no account.</p><p><a href="https://www.ineedworkwear.com">Browse telecoms and network workwear at iNeedWorkwear</a></p>',
 '<h3>Telecoms and Network Workwear, Sorted</h3><p>From polos and cargo trousers to hi-vis, softshells, waterproofs and safety boots, kit a fleet or a single van at fair prices, embroidered in-house and ordered on a trade account or direct online with no account.</p><p><a href="https://www.ineedworkwear.com">Browse telecoms and network workwear at iNeedWorkwear</a></p>',
 '<h3>Telecoms and Network Workwear, Sorted</h3><p>Polos, cargo trousers, hi-vis, softshells, waterproofs and safety boots, the field-ready kit for telecoms and network engineers at fair prices, embroidered in-house and ready on a trade account for the fleet or direct online for the subbie.</p><p><a href="https://www.ineedworkwear.com">Browse telecoms and network workwear at iNeedWorkwear</a></p>',
]
OWNER_POOL=[
 "And it runs on every size of business, which shapes what a workwear supplier has to do. The national build contractors field whole crews of engineers and buy through procurement, while a large layer of small subcontractors, ex-BT sole traders and independent installers take on work and need just a few branded pieces. A supplier has to serve the fleet and the one-van installer alike, with both a managed account and a quick direct route.",
 "And it runs on every size of business, which shapes the supplier's job. The big build contractors field whole crews and buy through procurement, while a large layer of small subcontractors, ex-BT sole traders and independent installers take on work and want just a few branded pieces. A supplier has to serve the fleet and the one-van installer alike, with a managed account and a quick direct route side by side.",
 "And it runs on businesses of every size, which shapes what a supplier needs to do. National build contractors field whole crews of engineers and buy through procurement, while a big layer of small subcontractors, ex-BT sole traders and independent installers take on work and need only a few branded pieces. A supplier has to handle the fleet and the single van alike, offering both a managed account and a fast direct route.",
 "And every size of business is in the mix, which shapes the supplier's job. The national contractors run crews of engineers through procurement, while a wide layer of small subcontractors, ex-BT sole traders and independent installers pick up work and want a handful of branded pieces. A supplier has to serve the fleet and the one-van installer alike, with a managed account and a quick direct route both on offer.",
 "And the trade spans every size of business, which shapes what a supplier must do. Big build contractors field whole crews and buy centrally, while a large layer of small subcontractors, ex-BT sole traders and independent installers take on work and need just a few branded pieces. A supplier has to look after the fleet and the single installer alike, with both a managed account and a quick direct route.",
 "And it runs on every size of operator, which shapes the supplier's job. The national contractors field crews of engineers and buy through procurement, while a deep layer of small subcontractors, ex-BT sole traders and independent installers take on the work and want only a few branded pieces. A supplier has to cover the fleet and the one-van installer alike, with a managed account and a quick direct route both available.",
]
PRESENT_POOL=[
 "And the kit does three jobs at once, which is what makes telecoms and network workwear its own thing. It is branded and identifiable, so a {t} engineer on a doorstep or at a street cabinet looks like a legitimate contractor rather than a stranger. It is visible, with hi-vis for the roadside and street works near traffic. And it is weatherproof and practical: softshells, fleeces and waterproofs for all-weather outdoor work, cargo trousers for tools, and safety boots underfoot.",
 "And the kit does three jobs at once, which is what sets telecoms and network workwear apart. It is branded and identifiable, so a {t} engineer on a doorstep or at a cabinet reads as a legitimate contractor, not a stranger. It is visible, with hi-vis for the roadside and street works near traffic. And it is weatherproof and practical: softshells, fleeces and waterproofs for all-weather work, cargo trousers for tools, and safety boots underfoot.",
 "And the kit has to do three jobs at once, which is the heart of telecoms and network workwear. It is branded and identifiable, so a {t} engineer on a doorstep or at a street cabinet looks like a legitimate contractor rather than a stranger. It is visible, with hi-vis for the roadside and street works near traffic. And it is weatherproof and practical: softshells, fleeces and waterproofs for all-weather work, cargo trousers for tools, and safety boots underfoot.",
 "And the kit works three ways at once, which is what makes this workwear distinct. It is branded and identifiable, so a {t} engineer on a doorstep or at a cabinet looks like a legitimate contractor, not a stranger. It is visible, with hi-vis for the roadside and street works near traffic. And it is weatherproof and practical: softshells, fleeces and waterproofs for all-weather outdoor work, cargo trousers for tools, and safety boots underfoot.",
 "And the kit pulls three jobs at once, which is what makes telecoms and network workwear its own thing. It is branded and identifiable, so a {t} engineer on a doorstep or at a cabinet looks legitimate rather than like a stranger. It is visible, with hi-vis for the roadside and street works near traffic. And it is weatherproof and practical: softshells, fleeces and waterproofs for all-weather work, cargo trousers for tools, and safety boots underfoot.",
 "And the kit covers three jobs at once, which is what distinguishes telecoms and network workwear. It is branded and identifiable, so a {t} engineer on a doorstep or at a street cabinet looks like a legitimate contractor and not a stranger. It is visible, with hi-vis for the roadside and street works near traffic. And it is weatherproof and practical: softshells, fleeces and waterproofs for all-weather outdoor work, cargo trousers for tools, and safety boots underfoot.",
]
NARROW_POOL=[
 "Because engineers come and go and crews grow, it is a repeat-purchase trade, and the range is built to reorder easily. Polos, cargo trousers, hi-vis, softshells, fleeces, waterproofs and safety boots, branded in-house with the company name, are the whole kit, and we hold your logo and sizes on file so the next order or the next new engineer in {t} matches what the team already wears.",
 "Because engineers come and go and crews grow, this is a repeat-purchase trade, and the range is built to reorder easily. Polos, cargo trousers, hi-vis, softshells, fleeces, waterproofs and safety boots, branded in-house with the company name, are the whole kit, and your logo and sizes are held on file so the next order or new engineer in {t} matches what the team already wears.",
 "Since engineers come and go and crews grow, it is a repeat-purchase trade, and the range is built to reorder easily. Polos, cargo trousers, hi-vis, softshells, fleeces, waterproofs and safety boots, branded in-house with the company name, are the whole kit, and we keep your logo and sizes on file so the next order or new engineer in {t} matches what the team already wears.",
 "Because crews grow and engineers move on, it is a repeat-purchase trade, and the range reorders easily. Polos, cargo trousers, hi-vis, softshells, fleeces, waterproofs and safety boots, branded in-house with the company name, are the whole kit, and your logo and sizes sit on file so the next order or new engineer in {t} matches what the team already wears.",
 "As engineers come and go and crews grow, it is a repeat-purchase trade, and the range is built to reorder fast. Polos, cargo trousers, hi-vis, softshells, fleeces, waterproofs and safety boots, branded in-house with the company name, are the whole kit, and we hold your logo and sizes on file so the next order or new engineer in {t} matches what the team already runs.",
 "Because the workforce churns and crews grow, it is a repeat-purchase trade, and the range is built for easy reordering. Polos, cargo trousers, hi-vis, softshells, fleeces, waterproofs and safety boots, branded in-house with the company name, are the whole kit, and your logo and sizes are on file so the next order or new engineer in {t} lines up with what the team already wears.",
]
KIT_POOL=[
 "Polos, cargo trousers, hi-vis, softshells, fleeces, waterproofs and safety boots, branded with the company name, are the whole kit {loc}.",
 "The whole kit is polos, cargo trousers, hi-vis, softshells, fleeces, waterproofs and safety boots, branded with the company name {loc}.",
 "Polos, cargo trousers, hi-vis, softshells, fleeces, waterproofs and safety boots do the job, branded with the company name {loc}.",
 "It comes down to polos, cargo trousers, hi-vis, softshells, fleeces, waterproofs and safety boots, branded with the company name {loc}.",
 "Polos, cargo trousers, hi-vis, softshells, fleeces, waterproofs and safety boots, all branded with the company name, are the kit {loc}.",
 "Branded polos, cargo trousers, hi-vis, softshells, fleeces, waterproofs and safety boots make up the whole kit {loc}.",
]
S2TAIL_POOL=[
 ", polos, hi-vis and softshells lead, with cargo trousers, waterproofs and boots alongside.",
 ", the core is polos, hi-vis and softshells, with cargo trousers, waterproofs and boots to finish.",
 ", expect polos, hi-vis and softshells first, then cargo trousers, waterproofs and boots.",
 ", polos, hi-vis and softshells do the work, with cargo trousers, waterproofs and boots alongside.",
 ", polos, hi-vis and softshells anchor the kit, with cargo trousers, waterproofs and boots completing it.",
 ", it is polos, hi-vis and softshells, plus cargo trousers, waterproofs and boots.",
]

def s1_paras(town, T):
    if 's1loc' in T:
        present = PRESENT_POOL[pick(town,'pre',len(PRESENT_POOL))].format(t=town)
        narrow = NARROW_POOL[pick(town,'nar',len(NARROW_POOL))].format(t=town)
        own = OWNER_POOL[pick(town,'own',len(OWNER_POOL))]
        kit = KIT_POOL[pick(town,'kit',len(KIT_POOL))].format(loc=T['kit_loc'])
        return list(T['s1loc']) + [own, present, narrow.rstrip()+' '+kit]
    return T['s1']

def s2_local_text(town, T):
    if 's2_intro' in T:
        return T['s2_intro'].rstrip() + S2TAIL_POOL[pick(town,'s2t',len(S2TAIL_POOL))]
    return T['s2_local']

def faq_for(t, region):
    P = lambda salt, opts: opts[pick(t, salt, len(opts))]
    return [
     (f"Do you supply branded workwear to telecoms and network installers in {t}?", P('fq1',[
      f"Yes. Telecoms contractors, network installers, fibre and broadband engineers and field teams across {region} get branded polos, cargo trousers, hi-vis, softshells, fleeces, waterproofs and safety boots from us, embroidered in-house with the company name. A larger contractor can run a trade account for managed reordering, and a sole-trader subcontractor can order direct online with no account.",
      f"Yes. Branded polos, cargo trousers, hi-vis, softshells, fleeces, waterproofs and safety boots go to telecoms contractors, network installers and field engineers across {region}, embroidered in-house with the company name. A larger contractor runs a trade account for managed reordering, and a sole-trader subcontractor orders direct online with no account.",
      f"Yes. From a one-van installer to a full crew across {region}, we supply branded polos, cargo trousers, hi-vis, softshells, fleeces, waterproofs and safety boots, embroidered in-house with the company name, on a trade account for the fleet or direct online with no account.",
      f"Yes. Telecoms contractors, network installers and field engineers across {region} get branded polos, cargo trousers, hi-vis, softshells, fleeces, waterproofs and safety boots from us, embroidered in-house with the company name, on a trade account or ordered direct online.",
      f"Yes. Across {region} we kit telecoms contractors, network installers and field engineers in branded polos, cargo trousers, hi-vis, softshells, fleeces, waterproofs and safety boots, embroidered in-house with the company name, on a trade account or direct online for a subcontractor.",
      f"Yes. Telecoms and network installers across {region}, from a single van to a fleet, get branded polos, cargo trousers, hi-vis, softshells, fleeces, waterproofs and safety boots from us, embroidered in-house with the company name, on a trade account or direct online with no account."])),
     ("Can you supply a whole fleet of engineers as well as a single subcontractor?", P('fq2',[
      "Yes. A large installation contractor with a fleet of engineers can set up a trade account with managed reordering, agreed pricing and a held kit list, so new engineers are onboarded in matching branded kit fast. A one-person subcontractor can order direct online with no account, picking the few branded pieces they need. Both are branded in-house from one supplier.",
      "Yes. A large contractor with a fleet of engineers can run a trade account with managed reordering, agreed pricing and a held kit list, so new engineers onboard in matching branded kit quickly. A one-person subcontractor orders direct online with no account, picking the few pieces they need. Both are branded in-house from one supplier.",
      "Yes. A fleet of engineers can be kitted on a trade account with managed reordering, agreed pricing and a held kit list for fast onboarding, while a single subcontractor orders direct online with no account. Both routes are branded in-house from the same supplier, so everyone matches.",
      "Yes. A large installation contractor uses a trade account with managed reordering, agreed pricing and a held kit list to onboard new engineers in matching kit, and a sole-trader subcontractor orders direct online with no account. Both are branded in-house from one supplier.",
      "Yes. The fleet goes on a trade account with managed reordering, agreed pricing and a held kit list for quick onboarding, and the single subcontractor orders direct online with no account, both branded in-house from one supplier so the kit matches across the job.",
      "Yes. A contractor fleet runs on a trade account with managed reordering, agreed pricing and a held kit list, so new engineers onboard in matching kit, while a one-person subcontractor orders direct online with no account. Both are branded in-house by the same supplier."])),
     ("What workwear does a telecoms field engineer need?", P('fq3',[
      "The core kit is branded polos for everyday wear, cargo trousers for tools, hi-vis vests and jackets for roadside and street-cabinet visibility, softshells, fleeces and waterproofs for all-weather outdoor work, and safety boots, all branded with the company name. It is built for work at cabinets, poles, joint boxes and on customer premises in all conditions.",
      "The core is branded polos for the everyday, cargo trousers for tools, hi-vis for roadside and cabinet visibility, softshells, fleeces and waterproofs for all-weather work, and safety boots, all branded with the company name, built for cabinets, poles, joint boxes and customer premises in all conditions.",
      "At its core: branded polos for the everyday, cargo trousers for tools, hi-vis for roadside and street-cabinet visibility, softshells, fleeces and waterproofs for all-weather work, and safety boots, all branded with the company name and built for cabinets, poles, joint boxes and customer premises.",
      "The core uniform is branded polos for the everyday, cargo trousers for tools, hi-vis for roadside and cabinet visibility, softshells, fleeces and waterproofs for all-weather work, and safety boots, all branded with the company name across cabinets, poles, joint boxes and customer premises.",
      "It comes down to branded polos for the everyday, cargo trousers for tools, hi-vis for roadside and cabinet visibility, softshells, fleeces and waterproofs for all-weather work, and safety boots, all branded with the company name and made for cabinets, poles and customer premises.",
      "Branded polos for the everyday, cargo trousers for tools, hi-vis for roadside and street-cabinet visibility, softshells, fleeces and waterproofs for all-weather work, and safety boots make up the core, all branded with the company name for cabinets, poles, joint boxes and customer premises."])),
     ("Is the hi-vis suitable for roadside and street works?", P('fq4',[
      "Yes. We supply hi-vis vests and jackets to EN ISO 20471 for visibility on the roadside and at street cabinets, poles and joint boxes where engineers work near traffic, alongside the softshells, fleeces and waterproofs for all-weather outdoor work. It can all be branded with the company name.",
      "Yes. Hi-vis vests and jackets to EN ISO 20471 give visibility on the roadside and at street cabinets, poles and joint boxes near traffic, supplied alongside the softshells, fleeces and waterproofs for all-weather work, all able to be branded with the company name.",
      "Yes, the hi-vis vests and jackets meet EN ISO 20471 for roadside and street-works visibility at cabinets, poles and joint boxes near traffic, supplied with the softshells, fleeces and waterproofs for all-weather work and branded with the company name.",
      "Yes. We supply EN ISO 20471 hi-vis for visibility on the roadside and at cabinets, poles and joint boxes where engineers work near traffic, along with softshells, fleeces and waterproofs for all-weather outdoor work, all branded with the company name.",
      "Yes. The hi-vis vests and jackets are to EN ISO 20471 for roadside and street-cabinet visibility near traffic, supplied alongside softshells, fleeces and waterproofs for all-weather work, and all of it can carry the company branding.",
      "Yes, hi-vis to EN ISO 20471 keeps engineers visible on the roadside and at street cabinets, poles and chambers near traffic, supplied with the softshells, fleeces and waterproofs for all-weather work and branded with the company name."])),
     ("Can you embroider our company name and logo?", P('fq5',[
      "Yes. We embroider your company name and logo in-house onto polos, softshells, fleeces and hi-vis, finished to survive heavy site use and frequent washing. Send your artwork once, we hold it on file, and every reorder and new engineer matches, so a contractor fleet or a sole-trader installer looks consistent and professional on the doorstep and at the cabinet.",
      "Yes. Your company name and logo are embroidered in-house onto polos, softshells, fleeces and hi-vis, finished for heavy site use and frequent washing. Send artwork once and we hold it on file, so every reorder and new engineer matches, and a fleet or a sole trader looks consistent on the doorstep.",
      "Yes, all branding is done in-house onto polos, softshells, fleeces and hi-vis, finished to survive heavy site use and washing. We hold your artwork on file, so every reorder and new engineer matches and a contractor fleet or sole-trader installer looks consistent and professional.",
      "Yes. Send your artwork once and we embroider your company name and logo in-house onto polos, softshells, fleeces and hi-vis, holding it on file so every reorder and new engineer matches, and a fleet or sole-trader installer looks consistent on the doorstep and at the cabinet.",
      "Yes. Company name and logo are embroidered in-house onto polos, softshells, fleeces and hi-vis, finished for heavy site use and washing and held on file, so every reorder and new engineer matches and a fleet or sole trader stays consistent.",
      "Yes, embroidery is done in-house onto polos, softshells, fleeces and hi-vis, finished to take heavy site use and washing. Send your logo once and we keep it on file, so reorders and new engineers line up and a fleet or sole-trader installer looks professional."])),
     ("Do you supply softshells and waterproofs for all-weather field work?", P('fq6',[
      "Yes. Alongside the polos and hi-vis we supply branded softshell jackets, fleeces, waterproof jackets and trousers for the outdoor, all-weather work telecoms and network installation involves, keeping engineers warm, dry and presentable at the cabinet, up the pole or on site.",
      "Yes. As well as polos and hi-vis, we supply branded softshells, fleeces, waterproof jackets and trousers for the outdoor, all-weather work this trade involves, keeping engineers warm, dry and presentable at the cabinet, up the pole or on site.",
      "Yes, we supply branded softshell jackets, fleeces, waterproof jackets and trousers alongside the polos and hi-vis, for the outdoor all-weather work network installation involves, keeping engineers warm, dry and presentable at the cabinet and on site.",
      "Yes. Beyond the polos and hi-vis, we supply branded softshells, fleeces and waterproof jackets and trousers for the all-weather outdoor work telecoms involves, keeping engineers warm, dry and presentable at cabinets, on poles and on site.",
      "Yes. The all-weather layers are covered too: branded softshells, fleeces and waterproof jackets and trousers alongside the polos and hi-vis, keeping engineers warm, dry and presentable at the cabinet, up the pole or on customer premises.",
      "Yes. We supply branded softshells, fleeces and waterproof jackets and trousers with the polos and hi-vis, for the outdoor all-weather work network installation involves, keeping engineers warm, dry and presentable at the cabinet and on site."])),
     ("How quickly can you supply telecoms workwear?", P('fq7',[
      "Order direct online and your kit is dispatched on standard lead times, with embroidery added in-house before it ships. For a contractor fleet on a trade account, send your headcount, your logo and your sizes and we will build a branded uniform list and hold it on file, so new engineers are onboarded in matching kit on standard lead times.",
      "Order direct online and your kit ships on standard lead times, with embroidery added in-house first. For a contractor fleet on a trade account, send your headcount, logo and sizes and we will build a branded uniform list and hold it on file, so new engineers onboard in matching kit on standard lead times.",
      "Order direct online and we dispatch on standard lead times, embroidery added in-house before shipping. For a fleet on a trade account, send your headcount, logo and sizes and we will build a branded uniform list and hold it on file for fast onboarding and reordering.",
      "Order direct online and your kit is dispatched on standard lead times with embroidery done in-house first. For a contractor fleet on a trade account, send your headcount, logo and sizes and we will build a branded uniform list and hold it on file, so new engineers onboard in matching kit.",
      "Order online and we dispatch on standard lead times with embroidery added in-house beforehand. A contractor fleet on a trade account can send headcount, logo and sizes for a branded uniform list held on file, so new engineers onboard in matching kit fast.",
      "Order direct online and your kit ships on standard lead times, embroidered in-house first. For a contractor fleet on a trade account, send your headcount, logo and sizes and we will build a branded uniform list and keep it on file for quick onboarding on standard lead times."])),
    ]

TOWNS = {
 "birmingham": {
  "region":"Birmingham and the West Midlands",
  "nearby":["Solihull","West Bromwich","Walsall"],
  "snapshot":"iNeedWorkwear supplies branded polos, cargo trousers, hi-vis, softshells, fleeces, waterproofs and safety boots to telecoms contractors, network installers and field engineers across Birmingham, embroidered in-house with the company name. The trade runs from national build contractors with fleets of engineers to one-van subcontractors, so a larger firm can run a trade account for managed reordering, while a sole trader can order direct online with no account.",
  "s1_head":"Kitting the field engineers of the West Midlands",
  "s1loc":[
   "Birmingham and the wider West Midlands are in the middle of a huge network build. Openreach has thousands of engineers across the Midlands pushing full fibre out through the city and into Sandwell, Wolverhampton and Solihull, CityFibre and the alternative networks are building alongside through contractors like Kelly Group and Morrison Telecom, and Virgin Media and the mobile operators keep upgrading on top. Around the big build sit local cabling firms like Midland Telecom Networks and a long tail of broadband, CCTV and structured-cabling installers.",
   "And it runs on every size of business. The national build contractors field whole crews of engineers and buy through procurement, while a large layer of small subcontractors, ex-BT sole traders and independent broadband and CCTV installers take on work across the city and need just a few branded pieces. A workwear supplier here has to serve the fleet and the one-van installer alike, which is why we run trade accounts and direct online ordering side by side.",
  ],
  "kit_loc":"across the city's streets, cabinets and customer premises",
  "s2_intro":"Whether you are a national build contractor with crews across Birmingham, a structured-cabling firm or a one-van broadband installer in Solihull",
 },
 "leeds": {
  "region":"Leeds and West Yorkshire",
  "nearby":["Bradford","Pudsey","Dewsbury"],
  "snapshot":"iNeedWorkwear supplies branded polos, cargo trousers, hi-vis, softshells, fleeces, waterproofs and safety boots to telecoms contractors, network installers and field engineers across Leeds, embroidered in-house with the company name. The trade runs from build contractors with fleets of engineers to one-van subcontractors, so a larger firm can run a trade account for managed reordering, while a sole trader can order direct online with no account.",
  "s1_head":"Kitting the field engineers of Yorkshire",
  "s1loc":[
   "Leeds is a CityFibre Gigabit City, with full fibre going in across the city and the major build contractors, from Openreach delivery partners to civils firms like OCU, working through Chapel Allerton, Holbeck, Pudsey, Morley and Beeston. Alongside the residential rollout sits a strong commercial scene: structured-cabling and fibre-optic firms such as Express Data, Eurocoms and Leeds Communications wiring offices, schools and multi-site businesses in Cat5e, Cat6 and fibre across Yorkshire.",
   "And the trade runs the full range of sizes. The build contractors put crews of engineers on the street and buy centrally, while commercial cabling firms, CCTV installers and ex-BT sole-trader telephone and broadband engineers take on work for homes and businesses around the city. A workwear supplier has to kit the fleet and the one-person installer alike, which is why we run trade accounts for the crews and direct online ordering, with no account, for everyone else.",
  ],
  "kit_loc":"across the city's streets, cabinets and customer premises",
  "s2_intro":"Whether you are a build contractor with crews across Leeds, a structured-cabling firm or a one-van broadband installer toward Pudsey",
 },
 "glasgow": {
  "region":"Glasgow and the west of Scotland",
  "nearby":["Paisley","East Kilbride","Clydebank"],
  "snapshot":"iNeedWorkwear supplies branded polos, cargo trousers, hi-vis, softshells, fleeces, waterproofs and safety boots to telecoms contractors, network installers and field engineers across Glasgow, embroidered in-house with the company name. The trade runs from city-wide fibre build crews to one-van subcontractors, so a larger firm can run a trade account for managed reordering, while a sole trader can order direct online with no account.",
  "s1_head":"Kitting the field engineers of the west of Scotland",
  "s1loc":[
   "Glasgow is a CityFibre full fibre city, with the company's 270m pound city-wide build running through local partners like PMK and Glenevin, and IMS Scotland on the Clydebank section, across Thornliebank, Newton Mearns, Clarkston, Cambuslang, Bishopbriggs, Anniesland and Netherton. Openreach has its own full fibre programme pushing across the Glasgow City Region and out to Paisley and Clydebank, while Virgin Media O2 and nexfibre, Netomnia and YouFibre and Hyperoptic in the apartment blocks all build on top. Around the rollout sits a long tail of broadband, CCTV and structured-cabling installers.",
   "And the commercial side runs just as deep. Structured-cabling and CCTV firms wire offices, schools and multi-site businesses in Cat5e, Cat6 and fibre out at Hillington Park toward Paisley, Scotland's largest business park, and across Strathclyde Business Park, with the University of Strathclyde and the city-centre campuses generating their own network work. The build contractors put crews of engineers on the street and buy centrally, while commercial cabling firms, CCTV installers and ex-BT sole-trader telephone and broadband engineers take on work for homes and businesses from Rutherglen to Johnstone.",
  ],
  "kit_loc":"across the city's streets, cabinets and customer premises",
  "s2_intro":"Whether you are a build contractor with crews across Glasgow, a structured-cabling firm or a one-van broadband installer toward Paisley",
 },
 "sheffield": {
  "region":"Sheffield and South Yorkshire",
  "nearby":["Rotherham","Barnsley","Chapeltown"],
  "snapshot":"Sheffield is a CityFibre Gigabit City in the middle of a full-fibre build, and the workwear has to cover both ends of the trade. We run trade accounts for the build contractors and cabling firms putting crews on the street and buying centrally, and direct online ordering, with no account needed, for the ex-BT sole traders and one-van broadband and CCTV installers working across the city and out toward Rotherham and Barnsley.",
  "s1_head":"Kitting the field engineers of South Yorkshire",
  "s1loc":[
   "Sheffield is a CityFibre Gigabit City, with a 115 million pound full-fibre build going in through Darnall, Wybourn, Attercliffe, Burngreave, Hillsborough, Crookes and Woodseats, delivered on the ground by build partner O'Connor Utilities. Alongside it Openreach has put a 129 million pound network across South Yorkshire, reaching well over 200,000 Sheffield properties, and alt-net Netomnia is building its own full-fibre too. Virgin Media O2 and the mobile operators keep upgrading on top, so on any street you find competing crews pulling fibre through ducts and poles into homes and cabinets.",
   "And the build sits next to a serious commercial scene. The Advanced Manufacturing Park and Sheffield Business Park host the AMRC, Factory 2050 and a cluster of engineering firms, the University of Sheffield and Sheffield Hallam run multi-site campuses, and Kelham Island and Attercliffe are full of offices and workshops. Structured-cabling and CCTV installers wire all of it in Cat5e, Cat6 and fibre, from a one-van firm in Rotherham to crews fitting out a business park. A workwear supplier here has to kit the fleet and the sole trader alike.",
  ],
  "kit_loc":"across the city's streets, cabinets and customer premises",
  "s2_intro":"Whether you are a build contractor with crews across Sheffield, a structured-cabling firm or a one-van broadband installer toward Rotherham",
 },
 "manchester": {
  "region":"Manchester and Greater Manchester",
  "nearby":["Salford","Stockport","Oldham"],
  "snapshot":"Across Manchester and Greater Manchester we kit the network trade, from build contractors running crews of fibre engineers on trade accounts to the ex-BT sole traders and one-van broadband and CCTV installers who order direct online with no account. Whether you field a fleet through procurement or just need a few branded pieces for yourself, we serve the big delivery partners and the single installer side by side across the city.",
  "s1_head":"Kitting the field engineers of Greater Manchester",
  "s1loc":[
   "Manchester and Greater Manchester are in the middle of a major full-fibre build. Openreach has pushed live across all ten boroughs and past the 135,000 mark, with delivery partners like MJ Quinn building out through Tameside and beyond, while CityFibre runs alongside through contractors such as Kelly Group and civils firms like OCU. The alt-nets are busy too: nexfibre and Netomnia and brsk are wiring South Manchester through Didsbury, Withington, Chorlton, Burnage and Levenshulme, Freedom Fibre is investing into Salford around Walkden, and Virgin Media O2 keeps upgrading on top.",
   "Alongside the residential rollout sits a serious commercial scene. Spinningfields, the so-called Canary Wharf of the North, and the NOMA district carry hundreds of offices needing Cat5e, Cat6, fibre and CCTV, while MediaCityUK and Salford Quays form one of Europe's most wired digital neighbourhoods around the BBC, ITV and a cluster of tech firms. Add the universities, the Ancoats and Stockport business space, and a long tail of structured-cabling and security installers working sites across the city, and the demand for trade kit runs deep.",
  ],
  "kit_loc":"across the city's streets, cabinets and customer premises",
  "s2_intro":"Whether you are a build contractor with crews across Manchester, a structured-cabling firm or a one-van broadband installer toward Salford",
 },
 "edinburgh": {
  "region":"Edinburgh and the Lothians",
  "nearby":["Musselburgh","Livingston","Bathgate"],
  "snapshot":"Edinburgh and the Lothians run on a busy fibre build, and the trade comes in every size. CityFibre, Openreach and GoFibre put crews of engineers on the street and buy centrally, while structured-cabling firms, CCTV installers and one-van broadband engineers take on work across the city and out toward Musselburgh and Bathgate. We run trade accounts for the fleets and direct online ordering, with no account, for the sole trader who needs a few branded pieces.",
  "s1_head":"Kitting the field engineers of the Lothians",
  "s1loc":[
   "Edinburgh is a CityFibre full-fibre city, with the network already through Leith, Granton, Corstorphine, Sighthill, Liberton and South Gyle and pushing on into Portobello, Craiglockhart and Drylaw. Openreach has passed more than 80,000 premises here, building through delivery partners like Morrison Telecom Services, Kier and KN Circet, and out into West Lothian around Bathgate and Broxburn. GoFibre is wiring the outer south and East Lothian, while Hyperoptic and YouFibre fill in city-centre and Leith apartment blocks. Around all of that sits a long tail of broadband and CCTV installers.",
   "Alongside the residential rollout sits a strong commercial scene. The financial cluster at Edinburgh Park and South Gyle, and the Exchange district around Scottish Widows, Standard Life and Baillie Gifford, keep structured-cabling and fibre-optic firms wiring offices in Cat5e, Cat6 and fibre. Add the universities, the life-sciences labs at the BioQuarter by Little France, and multi-site retail and public buildings across the city, and there is steady commercial and CCTV work the whole year. From Musselburgh in the east to Livingston and Bathgate in the west, installers cover homes and businesses alike.",
  ],
  "kit_loc":"across the city's streets, cabinets and customer premises",
  "s2_intro":"Whether you are a build contractor with crews across Edinburgh, a structured-cabling firm or a one-van broadband installer toward Musselburgh",
 },
 "liverpool": {
  "region":"Liverpool and Merseyside",
  "nearby":["Bootle","Birkenhead","Crosby"],
  "snapshot":"From central Liverpool out to Bootle, Birkenhead and Crosby, the city runs on full-fibre build and a busy commercial cabling trade. We kit the lot, naming both routes: trade accounts for the build crews and contractor fleets buying branded gear by the box, and direct online ordering, no account needed, for the ex-BT sole trader and one-van broadband or CCTV installer who just wants a few pieces.",
  "s1_head":"Kitting the field engineers of Merseyside",
  "s1loc":[
   "Liverpool and Merseyside are in the thick of a full-fibre build. Openreach has run Fibre First across the city and the Wirral with Merseyside-based contractor MJ Quinn putting hundreds of engineers on the street through Liverpool, the Wirral and Prescot, while Netomnia and its YouFibre brand have poured tens of millions into a 10Gbps network reaching well past 110,000 premises through Sefton Park, Stoneycroft and Aintree. CityFibre and Virgin Media O2 build on top, the latter passing over 118,000 homes across the city and out toward Bootle, Birkenhead and Huyton.",
   "Alongside the residential rollout sits a strong commercial scene. LCR Connect, the joint venture with ITS Technology Group and NGE, has laid a 214km gigabit network linking exchanges, data centres and business parks across all six boroughs from its Daresbury Park base. In the Baltic Triangle, hundreds of digital and creative firms and a local data centre keep structured-cabling and CCTV installers wiring offices, warehouses and studios in Cat5e, Cat6 and fibre, with the same trade running through Liverpool Waters, the docklands and the universities.",
  ],
  "kit_loc":"across the city's streets, cabinets and customer premises",
  "s2_intro":"Whether you are a build contractor with crews across Liverpool, a structured-cabling firm or a one-van broadband installer toward Bootle",
 },
 "bristol": {
  "region":"Bristol and the West of England",
  "nearby":["Bath","Portishead","Clevedon"],
  "snapshot":"Bristol and the West of England run on full-fibre and a busy commercial cabling trade, so we kit both ends of it. We supply branded workwear to the build contractors and structured-cabling firms that put crews on the street and buy on trade accounts, and to the sole-trader broadband, fibre and CCTV installers who order direct online with no account. Fleet or one-van, the gear ships the same way.",
  "s1_head":"Kitting the field engineers of the West Country",
  "s1loc":[
   "Bristol and the West of England are deep into a full-fibre build. Openreach has pushed its network through Bedminster, Easton, Filton, Whitchurch and Westbury-on-Trym, CityFibre has gone in across Redland, Cotham, Bishopston, Southville and Knowle, and the alt-nets build alongside - Netomnia and YouFibre, nexfibre and Virgin Media O2 across the city, with Bath-based Truespeed running out toward Portishead, Portbury, Easton-in-Gordano and Clevedon. Around the big rollout sits a long tail of broadband, fibre and CCTV installers taking on work street by street.",
   "It is not just the residential build, though. The Temple Quarter enterprise zone around Temple Meads, the harbourside digital and tech scene, and the aerospace cluster at Filton with Airbus and Rolls-Royce all pull in structured-cabling and fibre work. Aztec West, Bristol's biggest business park up by Bradley Stoke and Stoke Gifford, plus the universities and multi-site offices across the centre, keep firms wiring Cat5e, Cat6 and fibre alongside CCTV and access control. That commercial layer runs right next to the network crews on every job.",
  ],
  "kit_loc":"across the city's streets, cabinets and customer premises",
  "s2_intro":"Whether you are a build contractor with crews across Bristol, a structured-cabling firm or a one-van broadband installer toward Portishead",
 },
 "cardiff": {
  "region":"Cardiff and South Wales",
  "nearby":["Barry","Penarth","Caerphilly"],
  "snapshot":"Cardiff runs on a mix of national fibre crews and one-van installers, and a workwear supplier here has to serve both. We kit the build contractors and structured-cabling firms that buy on trade accounts for whole teams, and the ex-BT sole traders, broadband engineers and CCTV fitters who order direct online, with no account, for just a few branded pieces across the city and South Wales.",
  "s1_head":"Kitting the field engineers of South Wales",
  "s1loc":[
   "Cardiff is in the middle of a serious full-fibre build, and a lot of it is home-grown. Openreach has taken full fibre past 80 percent of the city and is still working through Llanishen, Llandaff, Pentyrch and Llanrumney, while Welsh altnet Ogi builds its own 10Gbps network out from East Moors through Cardiff Bay, Dumballs Road, Capital Quarter and the Central Square area. Netomnia and YouFibre push fibre across eastern Cardiff around Pontprennau, St Mellons and Llanrumney, and Hyperoptic, Virgin Media O2 and nexfibre keep upgrading apartments through Butetown and the Bay.",
   "Cardiff also carries a heavy commercial cabling load. Central Square sits at the heart of it, with BBC Cymru Wales New Broadcasting House, the Principality Stadium and the financial and professional offices that ring the station all wired in Cat5e, Cat6 and fibre. Out in Cardiff Bay the media, university and public-sector buildings need structured cabling, CCTV and access control, and a long tail of independent installers handles offices, schools and multi-site work across the city and out toward Barry, Penarth and Caerphilly.",
  ],
  "kit_loc":"across the city's streets, cabinets and customer premises",
  "s2_intro":"Whether you are a build contractor with crews across Cardiff, a structured-cabling firm or a one-van broadband installer toward Penarth",
 },
 "leicester": {
  "region":"Leicester and Leicestershire",
  "nearby":["Oadby","Hinckley","Loughborough"],
  "snapshot":"Leicester runs on full-fibre crews and a long tail of independent installers. We kit both, with trade accounts for the build contractors and cabling firms putting whole teams on the street and direct online ordering, no account needed, for the one-van broadband and CCTV installers working homes and small businesses across the city and out toward Oadby, Hinckley and Loughborough.",
  "s1_head":"Kitting the field engineers of the East Midlands",
  "s1loc":[
   "Leicester is a CityFibre city, with an 80 million pound full-fibre build that has taken more than 100,000 homes ready for service and pushed through Wigston, Braunstone, Glen Parva, Beaumont Leys and Belgrave. Openreach has full fibre live across the city centre, Aylestone and out into Oadby, and alt-nets including Netomnia and YouFibre plus Virgin Media O2 and nexfibre are building on top. Beyond the city, CityFibre is delivering Project Gigabit across rural Leicestershire, so engineers and civils crews are working cabinets and chambers right across the county.",
   "Alongside the street build sits a busy commercial scene tied to Leicester's distribution and logistics base. Meridian Business Park at junction 21 of the M1 and the M69, and Magna Park at Lutterworth, one of Europe's largest logistics parks, keep structured-cabling and CCTV firms wiring warehouses, offices and multi-site units in Cat5e, Cat6 and fibre. The University of Leicester and De Montfort University, the city's offices around Belgrave and the trade units toward Hinckley and Loughborough all add steady network, data and security work across the area.",
  ],
  "kit_loc":"across the city's streets, cabinets and customer premises",
  "s2_intro":"Whether you are a build contractor with crews across Leicester, a structured-cabling firm or a one-van broadband installer toward Oadby",
 },
 "bradford": {
  "region":"Bradford and West Yorkshire",
  "nearby":["Keighley","Shipley","Bingley"],
  "snapshot":"Bradford is a busy full-fibre city, and the trade behind it runs every size. We kit the build contractors running crews of engineers across the district on trade accounts, and we serve the structured-cabling firms, CCTV installers and ex-BT sole-trader broadband engineers who take work around the city and order direct online with no account. Fleet and one-van installer, both kitted the same.",
  "s1_head":"Kitting the field engineers of Bradford",
  "s1loc":[
   "Bradford is a CityFibre Gigabit City, with a build worth more than 75 million pounds rolling full fibre out from East Bowling through Bowling and Tyersal, delivered on the ground by contractor Network Plus. Openreach is building hard alongside, with over 160,000 premises already passed across Shipley, Dudley Hill, Laisterdyke, Low Moor and Queensbury, and Yorkshire alt-net Quickline is pushing fibre out through the wider district. Around all of it works a long tail of broadband, CCTV and structured-cabling installers across Bradford.",
   "Alongside the residential rollout sits a real commercial scene. The Victorian warehouses of Little Germany around Peckover Street and Vicar Lane, the offices at Salts Mill and Saltaire, the business parks toward Shipley and the University of Bradford all need wiring and re-wiring in Cat5e, Cat6 and fibre. Structured-cabling and CCTV firms run offices, schools and multi-site jobs from Manningham across to Keighley and Bingley, while smaller installers cover homes and shopfronts right across the district.",
  ],
  "kit_loc":"across the city's streets, cabinets and customer premises",
  "s2_intro":"Whether you are a build contractor with crews across Bradford, a structured-cabling firm or a one-van broadband installer toward Shipley",
 },
 "coventry": {
  "region":"Coventry and Warwickshire",
  "nearby":["Nuneaton","Bedworth","Kenilworth"],
  "snapshot":"We supply telecoms and network-installation workwear across Coventry and Warwickshire, from the build crews running full fibre through the city to the one-van broadband and CCTV installers working out toward Nuneaton. We kit fleets on trade accounts for the contractors and offer direct online ordering, no account needed, for sole traders and small firms, so every installer in the area can pick up branded, hard-wearing kit that suits the job.",
  "s1_head":"Kitting the field engineers of Warwickshire",
  "s1loc":[
   "Coventry is a CityFibre city, with full fibre going in across the city alongside Openreach, which now passes well over 100,000 premises here. CityFibre has worked through Tile Hill, Allesley Village, Binley and Walsgrave, with build moving on into Radford, Holbrooks, Keresley, Longford, Stoke and Wyken. Netomnia and its YouFibre brand are building too, and Virgin Media O2 with nexfibre keeps extending fibre on top. Behind the named networks sit civils crews, jointers and fibre engineers running cable through cabinets and footways street by street.",
   "Alongside the residential rollout sits a strong commercial scene. Structured-cabling and CCTV firms wire offices, schools and the big research and automotive sites at Ansty Park, MIRA Technology Park and the UK Battery Industrialisation Centre, plus the campuses of Coventry and Warwick universities and the business parks around the ring road. Local installers run Cat5e, Cat6 and fibre for multi-site firms across the city and out through Bedworth and Kenilworth, so the trade here spans heavy network build and detailed commercial fit-out side by side.",
  ],
  "kit_loc":"across the city's streets, cabinets and customer premises",
  "s2_intro":"Whether you are a build contractor with crews across Coventry, a structured-cabling firm or a one-van broadband installer toward Nuneaton",
 },
 "nottingham": {
  "region":"Nottingham and Nottinghamshire",
  "nearby":["Beeston","Arnold","West Bridgford"],
  "snapshot":"Nottingham is a full-fibre city, and the trade behind it runs every size. CityFibre and Openreach crews are on the streets alongside alt-net and commercial cabling teams, so a workwear supplier here has to kit both the build fleet and the lone installer. We run trade accounts for the crews who buy branded gear in bulk and direct online ordering, with no account needed, for the one-van engineer ordering a few pieces.",
  "s1_head":"Kitting the field engineers of Nottinghamshire",
  "s1loc":[
   "Nottingham is a CityFibre city, with a full-fibre rollout delivered by build partner McCann pushing the network out through Aspley, Bilborough, Wollaton, Basford, Bulwell, Hyson Green, the Meadows and across the river into West Bridgford and Gamston. Openreach engineers are running fibre across the city and county at the same time, the alt-nets Netomnia and YouFibre are building alongside, and Hyperoptic and Virgin Media O2 keep upgrading on top. Around the residential build sits a long tail of broadband, CCTV and structured-cabling installers working homes and businesses right across the area.",
   "And the commercial side is just as busy. Structured-cabling and fibre teams wire the offices and labs at Nottingham Science Park and BioCity in the Creative Quarter, fit out the University of Nottingham and Nottingham Trent campuses, and run Cat5e, Cat6 and fibre through business space at the Boots Enterprise Zone and out toward Beeston and Arnold. CCTV and access-control installers cover retail, schools and multi-site firms across the city. It is a steady mix of cabling, security and network work that keeps engineers on the road all week.",
  ],
  "kit_loc":"across the city's streets, cabinets and customer premises",
  "s2_intro":"Whether you are a build contractor with crews across Nottingham, a structured-cabling firm or a one-van broadband installer toward Beeston",
 },
 "sunderland": {
  "region":"Sunderland and the North East",
  "nearby":["Washington","Houghton le Spring","South Shields"],
  "snapshot":"Sunderland is a city mid-build on full fibre, with network contractors and a long tail of broadband and CCTV installers working across Wearside. We kit both routes: trade accounts for the build crews and commercial fleets that buy branded workwear in volume, and direct online ordering, no account needed, for the ex-BT sole trader and one-van installer who just want a few pieces.",
  "s1_head":"Kitting the field engineers of Wearside",
  "s1loc":[
   "Sunderland is a full-fibre city under its Smart City programme, and the build is everywhere. CityFibre is pushing its 62 million pound network out through Hendon, Southwick, Ryhope, Millfield and St Michael's, with civils from MAP Group and delivery by United Living, while Openreach has taken full fibre past more than 20,000 premises. The alternative networks are building alongside, with Netomnia and YouFibre, nexfibre and Virgin Media O2 and Hyperoptic all active across Wearside, so crews are in the streets and cabinets right across the city.",
   "Off the residential build sits a strong commercial scene. Doxford International Business Park, the old Enterprise Zone off the A19, and Rainton Bridge toward Houghton le Spring fill up with offices, contact centres and data sites that need structured cabling and CCTV in Cat5e, Cat6 and fibre. Add the Nissan plant and its supply chain at Washington, the university and the Sunderland Software City digital cluster, and you get a steady run of fit-outs and multi-site jobs for cabling and security installers around the city.",
  ],
  "kit_loc":"across the city's streets, cabinets and customer premises",
  "s2_intro":"Whether you are a build contractor with crews across Sunderland, a structured-cabling firm or a one-van broadband installer toward Washington",
 },
}

_CSV=None
def _load_csv():
    global _CSV
    if _CSV is not None: return _CSV
    here=os.path.dirname(os.path.abspath(__file__))
    for p in (os.path.join(here,'TC_towns.csv'),'TC_towns.csv','/mnt/user-data/outputs/TC_towns.csv'):
        if os.path.exists(p):
            rows=[]
            with open(p,newline='',encoding='utf-8-sig') as f:
                for r in csv.DictReader(f): rows.append((int(r["Rank"]), r["Town"].strip(), (r.get("Nation") or "").strip()))
            _CSV=rows; return _CSV
    _CSV=[]; return _CSV

def slugify(name):
    return re.sub(r'-+','-', re.sub(r"[^a-z0-9]+","-", name.lower().replace("&"," and "))).strip('-')

_DISPLAY=None
def _display_map():
    """slug -> CSV display name, preserving real casing (Newcastle upon Tyne,
    Stoke-on-Trent, Houghton le Spring) instead of naive word-capitalisation."""
    global _DISPLAY
    if _DISPLAY is None:
        _DISPLAY = {slugify(t): t for (_r, t, _n) in _load_csv()}
    return _DISPLAY

def town_display(key):
    return _display_map().get(slugify(key)) or ' '.join(w.capitalize() for w in key.split())

def _entry(town):
    """Look up a TOWNS entry by slug, tolerant of space/hyphen/case differences."""
    s = slugify(town)
    for k, v in TOWNS.items():
        if slugify(k) == s:
            return v
    raise KeyError(f"{town} not in TOWNS")

def require_nearby(town, T):
    nb = T.get("nearby")
    if not nb or len(nb) < 3:
        raise ValueError(f"{town}: 'nearby' must list 3 geographically-close towns "
                         f"(web-verified, all on TC_towns.csv). No rank/auto fallback.")
    bad = [n for n in nb if not any(r[1].lower()==n.lower() for r in _load_csv())]
    if bad:
        raise ValueError(f"{town}: nearby town(s) not on TC_towns.csv: {bad}")
    return nb[:3]

def build_title(town):
    for t in (f"{town} Telecoms and Network Workwear",
              f"{town} Telecoms and Network Kit", f"{town} Telecoms Workwear"):
        if len(t) <= 60: return t
    return f"{town} Telecoms Workwear"

def build_meta(town):
    for m in (f"Branded polos, cargo trousers, hi-vis, softshells and safety boots for {town} telecoms and network engineers - trade accounts or order direct online.",
              f"Branded polos, hi-vis, softshells and safety boots for {town} telecoms and network engineers - trade accounts or direct online, in-house embroidery.",
              f"Branded polos, cargo trousers, hi-vis and softshells for {town} telecoms and network engineers - trade or direct online, in-house embroidery.",
              f"Branded telecoms workwear for {town} network engineers - polos, hi-vis, softshells and safety boots, trade accounts or order direct online."):
        if len(m) <= 160: return m
    return f"Branded telecoms workwear for {town} network engineers - polos, hi-vis, softshells, trade or direct online."

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
        "name":f"Telecoms and Network Installation Workwear Supply and Embroidery in {town}",
        "serviceType":"Telecoms and network installation workwear and embroidery supply",
        "provider":{"@id":"https://www.ineedworkwear.com/#organization"},
        "areaServed":[{"@type":"City","name":town}]+[{"@type":"City","name":n} for n in nearby],
        "audience":{"@type":"BusinessAudience","name":"Telecoms contractors, network installers and field engineers"},
        "description":f"Branded polos, cargo trousers, hi-vis, softshells, fleeces, waterproofs and safety boots supplied to telecoms contractors, network installers and field engineers in {town}, on a trade account or direct online, with in-house embroidery.",
        "hasOfferCatalog":{"@type":"OfferCatalog","name":"Telecoms and Network Installation Workwear",
            "itemListElement":[{"@type":"Offer","itemOffered":{"@type":"Product","name":p}} for p in TC_PRODUCTS]}}
    crumb = {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Home","item":DOMAIN},
        {"@type":"ListItem","position":2,"name":"Telecoms and Network Installation Workwear","item":f"{DOMAIN}/telecoms-network-installation-workwear"},
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
    T = _entry(town)
    region = T.get("region", town)
    nearby = require_nearby(town, T)
    faqs = faq_for(town, region)
    P = lambda pool, salt: pool[pick(town, salt, len(pool))]

    trust   = T.get("trust", P(TRUST_POOL,'trust'))
    snap    = T["snapshot"]
    s1head  = T["s1_head"]
    s1ps    = s1_paras(town, T)
    s2intro = s2_local_text(town, T)
    grid    = build_grid(town)
    emb     = [P(EMB_P1_POOL,'e1').format(t=town), P(EMB_P2_POOL,'e2').format(t=town), P(EMB_P3_POOL,'e3')]
    con     = [P(CON_P1_POOL,'c1').format(t=town), P(CON_P2_POOL,'c2'), P(CON_P3_POOL,'c3').format(t=town)]
    acc     = [P(ACC_P1_POOL,'a1').format(t=town), P(ACC_P2_POOL,'a2'),
               P(ACC_P3_POOL,'a3').format(t=town), P(ACC_P4_POOL,'a4')]
    why     = [P(WHY_P1_POOL,'w1').format(t=town), P(WHY_P2_POOL,'w2'), P(WHY_P3_POOL,'w3'), P(WHY_P4_POOL,'w4')]
    ordr    = [P(ORD_P1_POOL,'o1').format(region=region), P(ORD_P2_POOL,'o2'), P(ORD_P3_POOL,'o3')]
    selfp   = P(SELF_POOL,'self'); sorted_ = P(SORTED_POOL,'sorted')

    emb_svg   = EMB.replace('a London telecoms logo', f'a {town} telecoms logo')
    sign_svg  = SIGNPOST.replace('London telecoms and network signpost', f'{town} telecoms and network signpost')
    sign_svg  = re.sub(r'<text x="230" y="62".*?</text>', signpost_town(town), sign_svg, flags=re.S)
    sign_svg  = sign_svg.replace('every kind of London telecoms', f'every kind of {town} telecoms')
    prem_svg  = PREMISES.replace('serving network installers across London', f'serving network installers across {town}')

    H=[build_head(town, slug, faqs, nearby), HEADER]
    H.append(f'<div class="tc-hero"><div class="tc-wrap"><div class="tc-subtitle">Branded Workwear for Telecoms and Network Engineers</div><h1>{town} Telecoms and Network Installation Workwear</h1></div></div>')
    H.append('<div class="tc-pulse"></div>')
    H.append(f'<div class="tc-trust-strip"><p>{trust}</p></div>')
    H.append(f'<div class="tc-wrap"><div class="tc-snapshot"><div class="tc-snapshot-label">Supplier Snapshot</div><p>{snap}</p></div></div>')
    H.append(STATS)
    H.append('<div class="tc-cta-bar"><a href="https://www.ineedworkwear.com" class="tc-cta-btn">Browse Telecoms and Network Workwear</a></div>')
    H.append('<div class="tc-jump-links"><a href="#range">Workwear Range</a><a href="#contract">The Uniform</a><a href="#accounts">Ordering and Accounts</a><a href="#order">How to Order</a></div>')
    H.append(GARMENT)
    H.append(f'<div class="tc-section"><div class="tc-wrap"><h2>{s1head}</h2>'+''.join(f'<p>{p}</p>' for p in s1ps)+'</div></div>')
    H.append(f'<div class="tc-section" id="range"><div class="tc-wrap"><h2>Telecoms and Network Installation Workwear Range</h2><p>{s2intro} <a href="https://www.ineedworkwear.com">Browse the full range at iNeedWorkwear.com</a>.</p><p class="tc-btn-center"><a href="https://www.ineedworkwear.com" class="tc-section-btn">Browse The Range</a></p>{grid}</div></div>')
    H.append(f'<div class="tc-section"><div class="tc-wrap"><h2>Branding for a Contractor Fleet or a Sole-Trader Installer</h2>'+''.join(f'<p>{p}</p>' for p in emb)+'</div></div>')
    H.append(emb_svg)
    H.append(f'<div class="tc-wrap"><div class="tc-contract" id="contract"><h3>{CON_HEAD}</h3>'+''.join(f'<p>{p}</p>' for p in con)+'</div></div>')
    H.append(sign_svg)
    H.append(f'<div class="tc-section" id="accounts"><div class="tc-wrap"><h2>{ACC_HEAD}</h2>'+''.join(f'<p>{p}</p>' for p in acc)+'</div></div>')
    H.append(prem_svg)
    H.append(f'<div class="tc-section"><div class="tc-wrap"><h2>Why Telecoms and Network Installers Choose iNeedWorkwear</h2>'+''.join(f'<p>{p}</p>' for p in why)+'</div></div>')
    H.append(ORDER)
    H.append(f'<div class="tc-section" id="order"><div class="tc-wrap"><h2>How to Order Telecoms and Network Workwear</h2><p>{ordr[0]}</p><p>{ordr[1]}</p><p>{ordr[2]}</p><p class="tc-btn-center"><a href="https://www.ineedworkwear.com" class="tc-section-btn">Browse And Order Online</a></p><p>{selfp}</p>'+CONTACT+'</div></div>')
    faq_html=''.join(f'<div class="tc-faq-item"><div class="tc-faq-q">{q}</div><div class="tc-faq-a">{a}</div></div>' for q,a in faqs)
    H.append(f'<div class="tc-faq"><div class="tc-wrap"><h2>Telecoms and Network Workwear FAQ</h2>{faq_html}</div></div>')
    H.append(f'<div class="tc-wrap"><div class="tc-workwear">{sorted_}</div></div>')
    nb_links=''.join(f'<a href="tc-{slugify(n)}.html">Telecoms and network workwear in {n}</a>\n' for n in nearby)
    H.append(f'<div class="tc-nearby"><div class="tc-wrap"><h3>Telecoms and Network Workwear in Nearby Towns</h3><div class="tc-nearby-links">{nb_links}</div></div></div>')
    H.append(FOOTER+'\n</body></html>')
    return '\n'.join(H)

def main():
    args=[a for a in sys.argv[1:]]
    outdir = (os.environ.get('TC_OUTDIR')
              or ('/mnt/user-data/outputs' if os.path.isdir('/mnt/user-data/outputs')
                  else 'outputs'))
    os.makedirs(outdir, exist_ok=True)
    if not args:
        args=[t for t in TOWNS if t!='london']
    town_slugs={slugify(k) for k in TOWNS}
    for town_key in args:
        s=slugify(town_key)
        if s=='london': continue
        if s not in town_slugs:
            print(f"SKIP {town_key}: not in TOWNS (must be web-researched first)"); continue
        town=town_display(town_key)
        slug=f"tc-{s}"
        html=assemble(slug, town)
        path=os.path.join(outdir, f"{slug}.html")
        open(path,'w',encoding='utf-8').write(html)
        print(f"WROTE {path}  ({len(html.split())} words approx)")

if __name__=='__main__':
    main()
