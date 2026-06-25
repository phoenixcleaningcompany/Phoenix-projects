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
 "newcastle upon tyne": {
  "region":"Newcastle upon Tyne and the North East",
  "nearby":["Gateshead","Sunderland","South Shields"],
  "snapshot":"Newcastle upon Tyne sits at the centre of a major North East network build, with full fibre going in across the city and over the Tyne into Gateshead. We kit both routes the trade runs on: build contractors and structured-cabling firms that field whole crews of engineers and buy on trade accounts, and the ex-BT sole traders and one-van broadband and CCTV installers who order direct online, with no account, and just need a few branded pieces.",
  "s1_head":"Kitting the field engineers of Tyneside",
  "s1loc":[
   "Newcastle is deep into its full-fibre rollout. CityFibre has built a network past tens of thousands of premises under a multi-million pound plan, running through Gosforth, Kenton, Fenham, Heaton and Byker and south into Gateshead, Teams and Dunston, with toob and other providers selling over it. Openreach is upgrading its own copper to fibre across the North of Tyne exchanges, and Virgin Media O2 and the mobile operators keep upgrading on top. Delivery partners and civils crews are working cabinets, chambers and poles across the city, so there is a steady population of build engineers on the streets of Newcastle every week.",
   "Alongside the residential build sits a strong commercial and structured-cabling scene. Cabling and CCTV firms wire offices, schools and multi-site businesses in Cat5e, Cat6 and fibre across the big employment sites - Quorum Business Park and Cobalt Park out toward North Tyneside, the Newcastle Helix and Stephenson Quarter near the centre, and the quayside office blocks. Newcastle University and Northumbria University add campus and data-cabling work, and a long tail of independent installers takes on broadband, networking and security jobs for homes and businesses around Jesmond, Gosforth and Byker. It is a genuinely mixed trade that needs reliable workwear.",
  ],
  "kit_loc":"across the city's streets, cabinets and customer premises",
  "s2_intro":"Whether you are a build contractor with crews across Newcastle upon Tyne, a structured-cabling firm or a one-van broadband installer toward Gateshead",
 },
 "brighton": {
  "region":"Brighton and Hove",
  "nearby":["Hove","Worthing","Crawley"],
  "snapshot":"Brighton and Hove are in the middle of a multi-year full-fibre build across the city and along the coast toward Hove. We serve both routes the trade runs on: build contractors and structured-cabling firms that put whole crews of engineers on the street and buy on trade accounts, and the sole-trader and one-van broadband and CCTV installers who order direct online, with no account, and just need a few branded pieces to look the part.",
  "s1_head":"Kitting the field engineers of Brighton and Hove",
  "s1loc":[
   "Brighton and Hove are well into a major full-fibre rollout. CityFibre is partway through an 80 million pound build covering almost every home and business in the city, with streets already live in Moulsecoomb and Bevendean, Hanover and Elm Grove, Woodingdean and East Brighton, and providers like Vodafone, Giganet and Octaplus selling over it. Openreach has taken its own full fibre past more than 50,000 premises and is pushing east toward Kemptown, while smaller alt-nets including Brighton Fibre, Hyperoptic at the Marina and Grain add coverage. That keeps build engineers working cabinets and chambers across the city most weeks.",
   "The commercial side is just as busy. Structured-cabling and CCTV firms wire offices, schools and multi-site businesses in Cat5e, Cat6 and fibre across the city - the New England Quarter and Preston Barracks near the station, the Lewes Road campuses, and the seafront and North Laine office blocks. The University of Sussex and University of Brighton add campus cabling and networking work, and a long tail of independent installers handles broadband, networking and security jobs for homes and small firms around Kemptown, Hanover and Portslade. It is a mixed trade, from full crews to one-person installers, and all of it needs hard-wearing kit.",
  ],
  "kit_loc":"across the city's streets, cabinets and customer premises",
  "s2_intro":"Whether you are a build contractor with crews across Brighton, a structured-cabling firm or a one-van broadband installer toward Hove",
 },
 "plymouth": {
  "region":"Plymouth and the South West",
  "nearby":["Exeter","Saltash","Torquay"],
  "snapshot":"Plymouth is aiming to be one of the best-connected cities in the UK, with full fibre going in citywide and out toward Saltash and the Plymstock suburbs. We kit both routes the trade runs on: build contractors and structured-cabling firms that field crews of engineers and buy on trade accounts, and the ex-BT sole traders and one-van broadband and CCTV installers who order direct online, with no account, and just need a few branded pieces.",
  "s1_head":"Kitting the field engineers of the South West",
  "s1loc":[
   "Plymouth is well into a citywide full-fibre build. CityFibre is delivering a multi-million pound network reaching almost every property, with strong coverage through Southway, Derriford, Peverell, Mutley, Stoke and Devonport. Openreach is upgrading all six of the city's exchange areas to full fibre, pushing into St Budeaux, Crownhill, Plympton and Plymstock, and Virgin Media O2 cable covers much of the city on top. The council-backed Local Full Fibre Network has wired public-sector sites too. Between the residential rollout and the public-sector work there are build and civils crews on cabinets and chambers across Plymouth most weeks.",
   "The commercial scene keeps the cabling trade busy alongside the build. Structured-cabling and CCTV firms wire offices, schools and multi-site businesses in Cat5e, Cat6 and fibre across the key sites - the Derriford and Estover business parks, Langage Business Park out toward Plympton, the Royal William Yard and the city-centre and waterfront offices. The University of Plymouth and the defence and marine employers around Devonport add campus and secure-site networking work, and a long tail of independent installers handles broadband, networking and security jobs for homes and small firms across the city. It is a genuinely mixed trade.",
  ],
  "kit_loc":"across the city's streets, cabinets and customer premises",
  "s2_intro":"Whether you are a build contractor with crews across Plymouth, a structured-cabling firm or a one-van broadband installer toward Saltash",
 },
 "hull": {
  "region":"Hull and East Yorkshire",
  "nearby":["Grimsby","Scunthorpe","Doncaster"],
  "snapshot":"Hull is unusual - its incumbent network is KCOM, not Openreach - and the city now has real competition from MS3, Connexin and Grain building full fibre alongside it. We serve both routes the trade runs on: build contractors and structured-cabling firms that field crews of engineers and buy on trade accounts, and the sole-trader broadband and CCTV installers who order direct online, with no account, and just need a few branded pieces.",
  "s1_head":"Kitting the field engineers of East Yorkshire",
  "s1loc":[
   "Hull's network is different to most of the UK. The incumbent is KCOM, whose Lightstream full fibre already covers the whole city, and from August 2025 KCOM opened its ducts and poles to rivals under an infrastructure-sharing offer. That has fuelled a competitive build: MS3 Networks has passed tens of thousands of premises and topped 20,000 customers, Connexin built a large network now folded into CityFibre, and Grain Connect is expanding too. Around 70 to 79 percent of premises now have an alternative to KCOM. With multiple operators digging across districts like Bransholme, Orchard Park, Hessle Road and Holderness Road, there are build crews on the streets most weeks.",
   "The commercial side keeps the cabling trade busy alongside the residential build. Structured-cabling and CCTV firms wire offices, schools and multi-site businesses in Cat5e, Cat6 and fibre across the key sites - the Priory Park and Melton business parks west of the city, the Fruit Market and city-centre offices, and the port and logistics estates along the Humber. The University of Hull adds campus and data-cabling work, and a long tail of independent installers handles broadband, networking and security jobs for homes and small firms across the city. It is a mixed trade that needs reliable kit.",
  ],
  "kit_loc":"across the city's streets, cabinets and customer premises",
  "s2_intro":"Whether you are a build contractor with crews across Hull, a structured-cabling firm or a one-van broadband installer toward Grimsby",
 },
 "derby": {
  "region":"Derby and Derbyshire",
  "nearby":["Nottingham","Burton-on-Trent","Loughborough"],
  "snapshot":"Derby is well into a full-fibre transformation, with CityFibre and Openreach both building across the city and out into Derbyshire. We kit both routes the trade runs on: build contractors and structured-cabling firms that field crews of engineers and buy on trade accounts, and the ex-BT sole traders and one-van broadband and CCTV installers who order direct online, with no account, and just need a few branded pieces.",
  "s1_head":"Kitting the field engineers of Derbyshire",
  "s1loc":[
   "Derby is deep into a citywide full-fibre build. CityFibre is delivering a multi-million pound network with its build partner McCann, with work through Alvaston, Boulton, Chellaston, Littleover and Normanton and completed sections across Allestree, Mackworth, Mickleover, Darley and Abbey, and providers like Vodafone, Zen and Gigabit Networks selling over it. Openreach has taken its own full fibre past more than 85,000 properties across the city, and Virgin Media O2 cable covers much on top. With a citywide council partnership wiring thousands of social homes as well, there are build and civils crews on cabinets and chambers across Derby most weeks.",
   "The commercial scene keeps the cabling trade busy alongside the residential rollout. Structured-cabling and CCTV firms wire offices, schools and multi-site businesses in Cat5e, Cat6 and fibre across the key sites - Pride Park near the station, Infinity Park and the Rolls-Royce campus to the south, and the city-centre and Cathedral Quarter offices. The University of Derby and the big advanced-manufacturing employers add campus and secure-site networking work, and a long tail of independent installers handles broadband, networking and security jobs for homes and small firms across the city. It is a genuinely mixed trade.",
  ],
  "kit_loc":"across the city's streets, cabinets and customer premises",
  "s2_intro":"Whether you are a build contractor with crews across Derby, a structured-cabling firm or a one-van broadband installer toward Nottingham",
 },
 "southampton": {
  "region":"Southampton and Hampshire",
  "nearby":["Portsmouth","Eastleigh","Winchester"],
  "snapshot":"Southampton is in the middle of a full-fibre build, with Openreach upgrading across the city and toob running its own network alongside. We serve both routes the trade runs on: build contractors and structured-cabling firms that field crews of engineers and buy on trade accounts, and the sole-trader and one-van broadband and CCTV installers who order direct online, with no account, and just need a few branded pieces to look the part.",
  "s1_head":"Kitting the field engineers of Hampshire",
  "s1loc":[
   "Southampton is well into its full-fibre rollout. Openreach is upgrading its network across the SO14, SO15, SO16 and SO17 districts, taking full fibre past tens of thousands of premises with thousands more to follow. toob, the Southampton-based alt-net, runs its own ultrafast network across much of the city, and Virgin Media O2 cable covers a large share on top, with around 96 percent of premises now able to get ultrafast broadband. Between the Openreach build and the alt-net digging across districts like Portswood, Shirley, Bitterne and Woolston, there are build and civils crews on cabinets and chambers across Southampton most weeks.",
   "The commercial side keeps the cabling trade busy alongside the residential build. Structured-cabling and CCTV firms wire offices, schools and multi-site businesses in Cat5e, Cat6 and fibre across the key sites - Solent Business Park out toward Whiteley, the Ocean Village and Town Quay waterfront offices, and the city-centre and Cumberland Place blocks. The University of Southampton and Solent University add campus and data-cabling work, and the port and logistics estates need security and networking jobs too, with a long tail of independent installers handling broadband and CCTV for homes and small firms across the city. It is a mixed trade.",
  ],
  "kit_loc":"across the city's streets, cabinets and customer premises",
  "s2_intro":"Whether you are a build contractor with crews across Southampton, a structured-cabling firm or a one-van broadband installer toward Portsmouth",
 },
 "stoke-on-trent": {
  "region":"Stoke-on-Trent and Staffordshire",
  "nearby":["Newcastle-under-Lyme","Crewe","Stafford"],
  "snapshot":"Stoke-on-Trent is building a council-owned full-fibre network across the Potteries while Openreach and the alt-nets upgrade on top. We kit both routes the trade runs on: build contractors and structured-cabling firms that field crews of engineers and buy on trade accounts, and the sole-trader and one-van broadband and CCTV installers who order direct online, with no account, and just need a few branded pieces.",
  "s1_head":"Kitting the field engineers of the Potteries",
  "s1loc":[
   "Stoke-on-Trent has an unusual full-fibre story. The city council owns a citywide open-access network built and operated by VX Fiber, with LilaConnect selling and installing the connections, rolled out through Weston Coyney, Meir, Longton, Shelton and Bentilee. Openreach began expanding its own full fibre across the city from 2025, starting in Burslem and pushing into Trentham and Blythe Bridge, and YouFibre on the Netomnia network has become the standout alt-net offering symmetric multi-gig speeds. Virgin Media O2 cable covers much on top. With several operators digging across the six towns, there are build crews on cabinets and chambers most weeks.",
   "The commercial side keeps the cabling trade busy alongside the residential build. Structured-cabling and CCTV firms wire offices, schools and multi-site businesses in Cat5e, Cat6 and fibre across the key sites - Festival Park near Etruria, Trentham Lakes to the south, and the Etruria Valley business park and city-centre offices. Staffordshire University adds campus and data-cabling work, and the big logistics and distribution estates across the Potteries need security and networking jobs too, with a long tail of independent installers handling broadband and CCTV for homes and small firms across the city. It is a genuinely mixed trade.",
  ],
  "kit_loc":"across the city's streets, cabinets and customer premises",
  "s2_intro":"Whether you are a build contractor with crews across Stoke-on-Trent, a structured-cabling firm or a one-van broadband installer toward Newcastle-under-Lyme",
 },
 "wolverhampton": {
  "region":"Wolverhampton and the Black Country",
  "nearby":["Walsall","Dudley","Telford"],
  "snapshot":"Wolverhampton sits at the heart of a major Black Country network build, with full fibre going in across the city and a steady run of commercial cabling and CCTV work alongside it. We kit the people who do that work two ways: trade accounts for build contractors and cabling firms who order branded workwear for whole crews, and direct online ordering, with no account needed, for the sole-trader broadband and CCTV installer who wants just a few pieces.",
  "s1_head":"Kitting the field engineers of the Black Country",
  "s1loc":[
   "Wolverhampton has been one of the West Midlands' busiest full fibre cities. CityFibre completed a roughly 50 million pound primary build that took its network past more than 100,000 premises, more than 90 percent of the city's homes, while Openreach and Virgin Media O2 keep building and upgrading on top. Engineers and civils crews have worked through Bilston, Wednesfield, Tettenhall, Pendeford and Blakenhall, pulling fibre through streets and cabinets and connecting flats, new builds and business parks. Smaller networks such as Grain and Hyperoptic have reached pockets too, so on any given street you will find more than one network in the ground.",
   "Around the residential build sits a steady commercial scene. The i54 technology park off the M54, home to Jaguar Land Rover, Moog and Eurofins, plus established estates around Pendeford and Wednesfield, give structured-cabling firms a constant flow of Cat5e, Cat6 and fibre work in offices, factories and warehouses. The University of Wolverhampton, the city centre interchange and the canalside regeneration in Bilston and Wednesfield add CCTV, access-control and data-cabling jobs. A long tail of independent broadband, CCTV and structured-cabling installers takes on this work across the city, much of it ex-BT sole traders running a single van.",
  ],
  "kit_loc":"across the city's streets, cabinets and customer premises",
  "s2_intro":"Whether you are a build contractor with crews across Wolverhampton, a structured-cabling firm or a one-van broadband installer toward Walsall",
 },
 "swansea": {
  "region":"Swansea and South West Wales",
  "nearby":["Neath","Port Talbot","Llanelli"],
  "snapshot":"Swansea is in the middle of a big full fibre push, with residential rollout and commercial cabling work running side by side across the city and out along the coast. We supply the people doing that work in two ways: trade accounts for build contractors and cabling firms ordering branded workwear for full crews, and direct online ordering, with no account, for the sole-trader broadband and CCTV installer who only needs a few branded pieces.",
  "s1_head":"Kitting the field engineers of South West Wales",
  "s1loc":[
   "Swansea has had heavy full fibre investment. Openreach put around 28 million pound into its network here, reaching roughly three quarters of properties, with the SA1, SA2 and SA5 areas among the first in line, and Ogi, the Welsh alt-net, has been building its own full fibre across parts of the city and wider South West Wales. Crews have worked through the city centre, Morriston, Townhill and the SA1 Waterfront, pulling fibre through streets and cabinets and connecting homes, flats and businesses. With more than one network in the ground in many areas, there is steady build, connection and repair work across the city.",
   "Alongside the residential rollout sits a real commercial scene. The SA1 Swansea Waterfront and the city centre carry offices and apartment blocks, Swansea University's Bay Campus on Fabian Way and the older Singleton Park campus are large connected sites, and industrial areas around Llansamlet and Morriston keep structured-cabling firms busy with Cat5e, Cat6 and fibre. Hospitals such as Morriston, schools and multi-site businesses add data-cabling, CCTV and access-control work. A layer of independent broadband, CCTV and cabling installers, many of them one-van operators, takes on this work across the city and along the M4 corridor.",
  ],
  "kit_loc":"across the city's streets, cabinets and customer premises",
  "s2_intro":"Whether you are a build contractor with crews across Swansea, a structured-cabling firm or a one-van broadband installer toward Neath",
 },
 "milton keynes": {
  "region":"Milton Keynes and north Buckinghamshire",
  "nearby":["Bedford","Northampton","Luton"],
  "snapshot":"Milton Keynes was one of the UK's first full fibre cities and still has a busy network and commercial cabling scene across its grid. We kit the people who do that work two ways: trade accounts for build contractors and cabling firms who order branded workwear for whole crews, and direct online ordering, with no account needed, for the sole-trader broadband and CCTV installer who only wants a few branded pieces.",
  "s1_head":"Kitting the field engineers of north Buckinghamshire",
  "s1loc":[
   "Milton Keynes was CityFibre's flagship full fibre town. The roughly 43 million pound build laid almost 1,000km of fibre across nearly every street and reached around 90,000 homes, about 90 percent of addressable properties, and Openreach has since layered its own full fibre on top so many MK addresses now have a choice of networks. Engineers and civils crews have worked the grid system across estates from Bletchley and Wolverton to Westcroft and Broughton, pulling fibre through the redways, streets and cabinets and connecting homes, flats and businesses. The dense grid layout keeps build, connection and repair work steady across the town.",
   "The commercial side is just as active. Central Milton Keynes, the CMK business district, is full of office towers and larger premises, and estates around Kiln Farm, Knowlhill, Bleak Hall and Linford Wood give structured-cabling firms a constant run of Cat5e, Cat6 and fibre work. The shopping district, warehouses along the H and V grid roads, schools and multi-site businesses add CCTV, access-control and data-cabling jobs. A long tail of independent broadband, CCTV and structured-cabling installers, much of it ex-BT sole traders in a single van, takes on this work across the grid and the surrounding villages.",
  ],
  "kit_loc":"across the town's streets, cabinets and customer premises",
  "s2_intro":"Whether you are a build contractor with crews across Milton Keynes, a structured-cabling firm or a one-van broadband installer toward Bedford",
 },
 "aberdeen": {
  "region":"Aberdeen and the North East of Scotland",
  "nearby":["Dundee","Edinburgh","Glasgow"],
  "snapshot":"Aberdeen has had a heavy full fibre build and a strong commercial cabling scene tied to its energy sector. We supply the people doing that work in two ways: trade accounts for build contractors and cabling firms who order branded workwear for whole crews, and direct online ordering, with no account, for the sole-trader broadband and CCTV installer who only needs a few branded pieces.",
  "s1_head":"Kitting the field engineers of the North East of Scotland",
  "s1loc":[
   "Aberdeen has seen one of Scotland's larger full fibre builds. CityFibre completed a roughly 59 million pound primary build that ran over 762km of new fibre and reached more than 105,000 homes, around 97 percent of the city's premises, while Openreach keeps building its own full fibre on top. Crews have worked through Dyce, Bridge of Don, Mastrick, Cults and out toward Kingswells and Westhill, pulling fibre through granite streets and cabinets and connecting homes, flats and businesses. With more than one network in the ground across much of the city, build, connection and repair work stays steady.",
   "The commercial scene is shaped by the energy sector. The industrial estates at Altens and East and West Tullos, the Energy Transition Zone, and the office parks at Westhill and Bridge of Don keep structured-cabling firms busy with Cat5e, Cat6 and fibre across offices, warehouses and supply-chain premises. Robert Gordon University's Garthdee campus and the University of Aberdeen, hospitals, schools and multi-site businesses add CCTV, access-control and data-cabling work. A layer of independent broadband, CCTV and cabling installers, many of them one-van operators, takes on this work across the city and out across Aberdeenshire.",
  ],
  "kit_loc":"across the city's streets, cabinets and customer premises",
  "s2_intro":"Whether you are a build contractor with crews across Aberdeen, a structured-cabling firm or a one-van broadband installer toward Dundee",
 },
 "reading": {
  "region":"Reading and the Thames Valley",
  "nearby":["Wokingham","Bracknell","Slough"],
  "snapshot":"Reading sits in the Thames Valley tech corridor with a heavy full fibre build and a strong commercial cabling scene. We kit the people who do that work two ways: trade accounts for build contractors and cabling firms who order branded workwear for whole crews, and direct online ordering, with no account needed, for the sole-trader broadband and CCTV installer who only wants a few branded pieces.",
  "s1_head":"Kitting the field engineers of the Thames Valley",
  "s1loc":[
   "Reading has had one of the Thames Valley's busiest full fibre builds. CityFibre ran a roughly 58 million pound project that laid around 1,230km of fibre and reached more than 97,000 premises, close to 98 percent of the area, with services live across Tilehurst, Norcot and beyond, while Openreach and Virgin Media O2 keep building and upgrading on top. Crews have worked through Caversham, Whitley, Southcote, Earley and Calcot, pulling fibre through streets and cabinets and connecting homes, flats and businesses. With more than one network in the ground across much of the town, build and connection work stays steady.",
   "Reading is sometimes called the UK's Silicon Valley, and its commercial scene reflects it. Thames Valley Park, home to Microsoft's UK headquarters and Oracle, and the Green Park business park give structured-cabling firms a steady run of Cat5e, Cat6 and fibre work in large offices and data-heavy premises. The University of Reading's Whiteknights campus, the town centre, schools and multi-site businesses add CCTV, access-control and data-cabling jobs. A long tail of independent broadband, CCTV and structured-cabling installers, much of it ex-BT sole traders in a single van, takes on this work across the town and the wider Thames Valley.",
  ],
  "kit_loc":"across the town's streets, cabinets and customer premises",
  "s2_intro":"Whether you are a build contractor with crews across Reading, a structured-cabling firm or a one-van broadband installer toward Wokingham",
 },
 "northampton": {
  "region":"Northampton and Northamptonshire",
  "nearby":["Wellingborough","Kettering","Milton Keynes"],
  "snapshot":"Northampton has had a heavy full fibre build with strong alt-net coverage and a busy commercial cabling scene. We supply the people doing that work two ways: trade accounts for build contractors and cabling firms who order branded workwear for whole crews, and direct online ordering, with no account, for the sole-trader broadband and CCTV installer who only needs a few branded pieces.",
  "s1_head":"Kitting the field engineers of Northamptonshire",
  "s1loc":[
   "Northampton has had a deep full fibre build with unusually strong alt-net coverage, well above the UK average. CityFibre's rollout covers Kingsthorpe, Abington, Weston Favell, the Billing areas, Dallington, Duston and Far Cotton, while Openreach has invested more than 87 million pound across Northamptonshire and Virgin Media O2 keeps upgrading on top. Crews have pulled fibre through streets and cabinets across the town and connected homes, flats and businesses, with full fibre at gigabit speeds now the norm across large parts of Northampton. With more than one network in the ground in many areas, build, connection and repair work stays steady.",
   "The commercial side runs alongside it. Brackmills, one of the larger industrial and distribution estates in the county, plus the estates and warehouses around Moulton Park, Round Spinney and Swan Valley, give structured-cabling firms a constant flow of Cat5e, Cat6 and fibre work in offices, factories and logistics premises. The University of Northampton's Waterside campus, the town centre, schools and multi-site businesses add CCTV, access-control and data-cabling jobs. A long tail of independent broadband, CCTV and cabling installers, much of it ex-BT sole traders in a single van, takes on this work across the town and the county.",
  ],
  "kit_loc":"across the town's streets, cabinets and customer premises",
  "s2_intro":"Whether you are a build contractor with crews across Northampton, a structured-cabling firm or a one-van broadband installer toward Wellingborough",
 },
 "luton": {
  "region":"Luton and Bedfordshire",
  "nearby":["Dunstable","Hemel Hempstead","Stevenage"],
  "snapshot":"Luton has a competitive full fibre build and a steady commercial cabling scene across the town and the Dunstable conurbation. We kit the people who do that work two ways: trade accounts for build contractors and cabling firms who order branded workwear for whole crews, and direct online ordering, with no account needed, for the sole-trader broadband and CCTV installer who only wants a few branded pieces.",
  "s1_head":"Kitting the field engineers of Bedfordshire",
  "s1loc":[
   "Luton has a genuinely competitive full fibre market. CityFibre is investing around 45 million pound to wire Luton and Dunstable, with more than 35,000 premises ready for service, Openreach has been adding around 40,000 premises to its Bedfordshire footprint, and the alt-net Grain has enabled properties around Bury Park, with Virgin Media O2 on top. Crews have worked through Stopsley, Bramingham Park, Sundon Park, Limbury and Bury Park, pulling fibre through streets and cabinets and connecting homes, flats and businesses. With more than one network in the ground across much of the town, build and connection work stays steady.",
   "The commercial scene runs alongside it. The Capability Green business park off junction 10 of the M1, the town centre and the estates and warehouses around the airport and Napier Park give structured-cabling firms a steady run of Cat5e, Cat6 and fibre work in offices, logistics premises and larger buildings. The University of Bedfordshire's town centre campus, schools and multi-site businesses across the Luton and Dunstable conurbation add CCTV, access-control and data-cabling jobs. A long tail of independent broadband, CCTV and cabling installers, much of it ex-BT sole traders in a single van, takes on this work across the town and into south Bedfordshire.",
  ],
  "kit_loc":"across the town's streets, cabinets and customer premises",
  "s2_intro":"Whether you are a build contractor with crews across Luton, a structured-cabling firm or a one-van broadband installer toward Dunstable",
 },
 "portsmouth": {
  "region":"Portsmouth and South Hampshire",
  "nearby":["Gosport","Southampton","Havant"],
  "snapshot":"Portsmouth is in the middle of a major full-fibre build, with Openreach engineers and alt-net crews working across the island city and out into South Hampshire. The work runs from new estates to busy commercial districts, and it needs reliable, branded workwear all year. We supply the build contractors and structured-cabling firms on trade accounts, and we sell the same hi-vis, softshell and polo ranges direct online, with no account, to the sole trader and one-van broadband installer.",
  "s1_head":"Kitting the field engineers of South Hampshire",
  "s1loc":[
   "Portsmouth is a busy full-fibre city. Openreach has declared its build underway with delivery partner Morrison Telecom Services pushing FTTP across the island, while CityFibre has laid dense full fibre that regional builder Toob and other providers sell on. Gigabit coverage of the city now runs very high, with work threading through Fratton, Southsea, Cosham, Paulsgrove and North End, then out across South Hampshire toward Havant, Fareham and Gosport. Add the mobile operators and Virgin Media upgrading on top, and there is steady street, cabinet and pole work for civils crews and broadband engineers right across the city.",
   "And alongside the residential rollout sits a strong commercial scene. Structured-cabling and CCTV installers wire offices, schools and multi-site businesses in Cat5e, Cat6 and fibre across the Lakeside North Harbour campus off the M27, the University of Portsmouth buildings, the Historic Dockyard and naval base, and the trading estates around Portsea Island and Hilsea. The big build contractors field whole crews and buy centrally, while ex-BT sole traders and independent broadband and CCTV installers take on work for homes and businesses across the city and need just a few branded pieces.",
  ],
  "kit_loc":"across the city's streets, cabinets and customer premises",
  "s2_intro":"Whether you are a build contractor with crews across Portsmouth, a structured-cabling firm or a one-van broadband installer toward Gosport",
 },
 "peterborough": {
  "region":"Peterborough and Cambridgeshire",
  "nearby":["Cambridge","Northampton","Bedford"],
  "snapshot":"Peterborough is a completed CityFibre full-fibre city with ongoing Project Gigabit work across Cambridgeshire, so there is steady network and cabling work in the city and surrounding villages. The build runs from residential streets to business parks, and it needs reliable, branded workwear in all weathers. We supply the build contractors and structured-cabling firms on trade accounts, and we sell the same hi-vis, softshell and polo ranges direct online, with no account, to the sole trader and one-van broadband installer.",
  "s1_head":"Kitting the field engineers of Cambridgeshire",
  "s1loc":[
   "Peterborough is a CityFibre full-fibre city. CityFibre laid almost 700km of full fibre and completed its primary build, reaching roughly 85 percent of the city's homes, with providers including Vodafone, TalkTalk, Zen and IDNet selling over the network and an extension out to villages like Glinton and Eye. Openreach is building FTTP alongside, and Peterborough-headquartered alt-net LightSpeed Broadband also operates in the region. Under Project Gigabit, CityFibre is reaching rural and hard-to-reach premises across Cambridgeshire, so there is steady street, cabinet and pole work for civils crews and broadband engineers across Werrington, Orton, Bretton, Stanground and Hampton.",
   "And alongside the residential rollout sits a solid commercial scene. Structured-cabling and CCTV installers wire offices, warehouses, schools and multi-site businesses in Cat5e, Cat6 and fibre across Peterborough Business Park, the Lynch Wood and Hampton office parks, the city centre and the distribution sheds along the A1 and Fengate. The big build contractors field whole crews and buy centrally, while ex-BT sole traders and independent broadband and CCTV installers take on work for homes and businesses across the city and need just a few branded pieces.",
  ],
  "kit_loc":"across the city's streets, cabinets and customer premises",
  "s2_intro":"Whether you are a build contractor with crews across Peterborough, a structured-cabling firm or a one-van broadband installer toward Cambridge",
 },
 "bolton": {
  "region":"Bolton and Greater Manchester",
  "nearby":["Bury","Wigan","Salford"],
  "snapshot":"Bolton is in the middle of a major full-fibre build, with Openreach, CityFibre and alt-net crews working across the town and the wider Greater Manchester area. The work runs from terraced streets to business parks, and it needs reliable, branded workwear in all weathers. We supply the build contractors and structured-cabling firms on trade accounts, and we sell the same hi-vis, softshell and polo ranges direct online, with no account, to the sole trader and one-van broadband installer.",
  "s1_head":"Kitting the field engineers of Greater Manchester",
  "s1loc":[
   "Bolton is a busy full-fibre town. Openreach has added a further 10.5 million pound build covering Astley Bridge, Daubhill, Horwich and Westhoughton, while CityFibre is live across the town through build partner MakeHappenGroup, with teams working in Egerton, Smithills, Barrow Bridge and either side of Blackburn Road, plus Farnworth. Netomnia and YouFibre are extending full fibre alongside, and the mobile operators and Virgin Media keep upgrading on top. That leaves steady street, cabinet and pole work for civils crews and broadband engineers right across Bolton and out toward the rest of Greater Manchester.",
   "And alongside the residential rollout sits a strong commercial scene. Structured-cabling and CCTV installers wire offices, warehouses, schools and multi-site businesses in Cat5e, Cat6 and fibre across Logistics North off the M61, the Middlebrook park at Horwich, the University of Bolton buildings and the town-centre offices and trading estates. The national build contractors field whole crews and buy centrally, while ex-BT sole traders and independent broadband and CCTV installers take on work for homes and businesses around the town and need just a few branded pieces.",
  ],
  "kit_loc":"across the town's streets, cabinets and customer premises",
  "s2_intro":"Whether you are a build contractor with crews across Bolton, a structured-cabling firm or a one-van broadband installer toward Bury",
 },
 "dudley": {
  "region":"Dudley and the Black Country",
  "nearby":["Wolverhampton","Walsall","Halesowen"],
  "snapshot":"Dudley is in the middle of a full-fibre build, with alt-net and Openreach crews working across the borough and the wider Black Country. The work runs from residential streets to canalside business parks, and it needs reliable, branded workwear in all weathers. We supply the build contractors and structured-cabling firms on trade accounts, and we sell the same hi-vis, softshell and polo ranges direct online, with no account, to the sole trader and one-van broadband installer.",
  "s1_head":"Kitting the field engineers of the Black Country",
  "s1loc":[
   "Dudley is a busy full-fibre borough. Brierley Hill-based alt-net Brsk, now part of the Netomnia and YouFibre group, has rolled out full fibre across much of the area, while nexfibre and Virgin Media O2 are investing more than 2.7 million pound to upgrade up to 20,000 homes and businesses in Dudley, and Openreach is building FTTP alongside. Work threads through Brierley Hill, Sedgley, Tipton, Halesowen, Pensnett and Stourbridge, with the mobile operators upgrading on top, leaving steady street, cabinet and pole work for civils crews and broadband engineers across the borough.",
   "And alongside the residential rollout sits a solid commercial scene. Structured-cabling and CCTV installers wire offices, warehouses, schools and multi-site businesses in Cat5e, Cat6 and fibre across the Waterfront and Merry Hill at Brierley Hill, the DY5 Enterprise Zone, Blackbrook Valley Industrial Estate and the Lye and Pensnett trading estates. The build contractors field whole crews and buy centrally, while ex-BT sole traders and independent broadband and CCTV installers take on work for homes and businesses around the borough and need just a few branded pieces.",
  ],
  "kit_loc":"across the borough's streets, cabinets and customer premises",
  "s2_intro":"Whether you are a build contractor with crews across Dudley, a structured-cabling firm or a one-van broadband installer toward Wolverhampton",
 },
 "norwich": {
  "region":"Norwich and Norfolk",
  "nearby":["Ipswich","Peterborough","Cambridge"],
  "snapshot":"Norwich is in the middle of a major full-fibre build, with CityFibre and Openreach crews working across the city and out into rural Norfolk. The work runs from city streets to research and business parks, and it needs reliable, branded workwear in all weathers. We supply the build contractors and structured-cabling firms on trade accounts, and we sell the same hi-vis, softshell and polo ranges direct online, with no account, to the sole trader and one-van broadband installer.",
  "s1_head":"Kitting the field engineers of Norfolk",
  "s1loc":[
   "Norwich is a busy full-fibre city. CityFibre has been building across the city since 2021, originally aiming at close to 100,000 premises, and under Project Gigabit is now connecting rural and hard-to-reach Norfolk premises, with first state-aid homes going live in villages like Horsham St Faith and Newton St Faith. Openreach is deploying FTTP alongside, and alt-nets including County Broadband and Swish Fibre are active across parts of the county. Work threads through districts such as Thorpe Hamlet, Mile Cross, Eaton, Hellesdon and the Golden Triangle, leaving steady street, cabinet and pole work for civils crews and broadband engineers.",
   "And alongside the residential rollout sits a strong commercial scene. Structured-cabling and CCTV installers wire offices, labs, schools and multi-site businesses in Cat5e, Cat6 and fibre across the Norwich Research Park and UEA campus to the south-west, the Broadland Business Park off the A47, the city-centre offices and the trading estates around the Northway. The build contractors field whole crews and buy centrally, while ex-BT sole traders and independent broadband and CCTV installers take on work for homes and businesses across the city and need just a few branded pieces.",
  ],
  "kit_loc":"across the city's streets, cabinets and customer premises",
  "s2_intro":"Whether you are a build contractor with crews across Norwich, a structured-cabling firm or a one-van broadband installer toward Ipswich",
 },
 "swindon": {
  "region":"Swindon and Wiltshire",
  "nearby":["Oxford","Cheltenham","Reading"],
  "snapshot":"Swindon is a full-fibre town with CityFibre and Openreach crews working across the town and out into rural Wiltshire. The work runs from residential estates to business parks, and it needs reliable, branded workwear in all weathers. We supply the build contractors and structured-cabling firms on trade accounts, and we sell the same hi-vis, softshell and polo ranges direct online, with no account, to the sole trader and one-van broadband installer.",
  "s1_head":"Kitting the field engineers of Wiltshire",
  "s1loc":[
   "Swindon is a CityFibre Fibre City. CityFibre has laid around 777km of full fibre as part of a 40 million pound investment, connecting premises across Stratton, Pinehurst and Moredon, with Vodafone, TalkTalk and Giganet selling over the network. Openreach already treats Swindon as a Fibre City and, under Project Gigabit, is extending FTTP to rural Wiltshire premises around Wroughton, Royal Wootton Bassett, Lyneham, Highworth and Chippenham. With the mobile operators and Virgin Media upgrading on top, there is steady street, cabinet and pole work for civils crews and broadband engineers across the town and the surrounding villages.",
   "And alongside the residential rollout sits a solid commercial scene. The town's Great Western Railway works heritage and former Honda site have given way to modern business parks, and structured-cabling and CCTV installers wire offices, warehouses, schools and multi-site businesses in Cat5e, Cat6 and fibre across Windmill Hill Business Park, the Dorcan and Cheney Manor estates, the Nationwide and Intel offices and the M4-corridor sheds. The build contractors field whole crews and buy centrally, while ex-BT sole traders and independent broadband and CCTV installers take on work around the town and need just a few branded pieces.",
  ],
  "kit_loc":"across the town's streets, cabinets and customer premises",
  "s2_intro":"Whether you are a build contractor with crews across Swindon, a structured-cabling firm or a one-van broadband installer toward Oxford",
 },
 "croydon": {
  "region":"Croydon and South London",
  "nearby":["Bromley","Sutton","Lewisham"],
  "snapshot":"Croydon is in the middle of a major full-fibre build, with Openreach and London alt-net crews working across the borough and the wider South London area. The work runs from residential streets to office towers, and it needs reliable, branded workwear in all weathers. We supply the build contractors and structured-cabling firms on trade accounts, and we sell the same hi-vis, softshell and polo ranges direct online, with no account, to the sole trader and one-van broadband installer.",
  "s1_head":"Kitting the field engineers of South London",
  "s1loc":[
   "Croydon is a busy full-fibre borough. Openreach has named Croydon among its London full-fibre locations, with ultrafast coverage of the borough now very high, while alt-nets Community Fibre and Hyperoptic run their own full fibre, including a Community Fibre deal to wire around 11,000 council properties. Work threads through Thornton Heath, South Norwood, Addiscombe, Selhurst, Norbury and Purley, with the mobile operators and Virgin Media O2 upgrading on top. That leaves steady street, cabinet and pole work for civils crews and broadband engineers right across the borough and out into the rest of South London.",
   "And alongside the residential rollout sits a strong commercial scene. Structured-cabling and CCTV installers wire offices, schools and multi-site businesses in Cat5e, Cat6 and fibre across the office towers around East Croydon and Wellesley Road, the Croydon town-centre and Whitgift districts, the trading estates at Purley Way and the business space toward Bromley and Sutton. The build contractors field whole crews and buy centrally, while ex-BT sole traders and independent broadband and CCTV installers take on work for homes and businesses across the borough and need just a few branded pieces.",
  ],
  "kit_loc":"across the borough's streets, cabinets and customer premises",
  "s2_intro":"Whether you are a build contractor with crews across Croydon, a structured-cabling firm or a one-van broadband installer toward Bromley",
 },
 "bournemouth": {
  "region":"Bournemouth and Dorset",
  "nearby":["Poole","Christchurch","Southampton"],
  "snapshot":"Bournemouth sits inside a busy Dorset full-fibre build, with CityFibre and Openreach both running engineers across the conurbation and a long tail of broadband, CCTV and structured-cabling installers working behind them. The trade here splits two ways, and we serve both: build contractors and cabling firms that field whole crews and buy on a trade account, and sole-trader and direct installers who order branded workwear online with no account at all.",
  "s1_head":"Kitting the field engineers of Dorset",
  "s1loc":[
   "Bournemouth and the wider BCP conurbation are deep into a full-fibre build. CityFibre has invested tens of millions to pass well over 100,000 premises across Bournemouth, Christchurch and Poole, while Openreach has put its own money into local exchanges to take Full Fibre past tens of thousands more homes and businesses. The work runs through Boscombe, Charminster, Westbourne, Lansdowne and Winton, with Virgin Media and the mobile operators upgrading on top. Behind the named networks sits the usual long tail of broadband, CCTV and structured-cabling installers working across the town's streets, cabinets and customer premises.",
   "Alongside the residential rollout sits a strong commercial scene. JP Morgan runs a major technology and operations campus at Littledown near Boscombe, and the town carries a real financial-services and digital cluster, with agencies and product studios around Lansdowne, Charminster and Westbourne. The Bournemouth International Centre, the university quarter and the Lansdowne business district all need structured cabling, fibre and CCTV, and firms wiring offices, schools and multi-site businesses in Cat5e, Cat6 and fibre take on work right across Dorset. It is varied, proper local work that keeps a steady base of installers and cabling crews busy.",
  ],
  "kit_loc":"across the town's streets, cabinets and customer premises",
  "s2_intro":"Whether you are a build contractor with crews across Bournemouth, a structured-cabling firm or a one-van broadband installer toward Poole",
 },
 "southend-on-sea": {
  "region":"Southend-on-Sea and south Essex",
  "nearby":["Basildon","Rayleigh","Chelmsford"],
  "snapshot":"Southend-on-Sea is one of the best-connected places in the country, with Openreach, CityFibre and a south Essex public-sector fibre network all built out and a busy base of broadband, CCTV and cabling installers working behind them. The trade splits two ways, and we serve both: build contractors and cabling firms that field whole crews and buy on a trade account, and sole-trader and direct installers who order branded workwear online with no account at all.",
  "s1_head":"Kitting the field engineers of south Essex",
  "s1loc":[
   "Southend-on-Sea has had one of the heaviest full-fibre builds in the country. CityFibre completed a multi-million-pound network passing more than 70,000 premises, and Openreach invested around 20 million pound to take Full Fibre past about three quarters of properties, leaving Southend among the best-connected places in the UK. The work runs through Westcliff, Leigh-on-Sea, Chalkwell, Thorpe Bay, Southchurch and Shoeburyness, with Virgin Media and the mobile operators upgrading on top. Behind the named networks sits the usual long tail of broadband, CCTV and structured-cabling installers working across the town's streets, cabinets and customer premises.",
   "Alongside the residential rollout sits a real commercial scene. A 280km full-fibre network built for the south Essex councils connects hundreds of public-sector sites and thousands of businesses across Basildon, Rochford, Castle Point and Southend, and London Southend Airport and its surrounding business and logistics units add further demand. The seafront, the central business district, the colleges and the airport corridor all need structured cabling, fibre and CCTV, and firms wiring offices, schools and multi-site businesses in Cat5e, Cat6 and fibre take on work right across south Essex. It is steady, proper local work.",
  ],
  "kit_loc":"across the town's streets, cabinets and customer premises",
  "s2_intro":"Whether you are a build contractor with crews across Southend-on-Sea, a structured-cabling firm or a one-van broadband installer toward Basildon",
 },
 "walsall": {
  "region":"Walsall and the Black Country",
  "nearby":["Wolverhampton","West Bromwich","Dudley"],
  "snapshot":"Walsall sits in the middle of a heavy Black Country full-fibre build, with Openreach, Netomnia and other networks running engineers across the borough and a long tail of broadband, CCTV and cabling installers working behind them. The trade here splits two ways, and we serve both: build contractors and cabling firms that field whole crews and buy on a trade account, and sole-trader and direct installers who order branded workwear online with no account at all.",
  "s1_head":"Kitting the field engineers of the Black Country",
  "s1loc":[
   "Walsall is in the middle of a heavy Black Country full-fibre build. Openreach has invested around 30 million pound to take Full Fibre past roughly 80 per cent of properties, with more than 110,000 homes and businesses already able to upgrade, while Netomnia and YouFibre have built ultrafast network across Walsall and neighbouring Wednesbury using poles and ducts. The work runs through Bloxwich, Willenhall, Darlaston, Aldridge and Pleck, with Virgin Media and the mobile operators upgrading on top. Behind the named networks sits the usual long tail of broadband, CCTV and structured-cabling installers working across the town's streets, cabinets and customer premises.",
   "Alongside the residential rollout sits a strong industrial and commercial scene. Walsall has long been Black Country manufacturing country, and estates like Leamore Industrial Park, the Bloxwich Lane and Willenhall Lane estates and Impact Park near junction 10 of the M6 carry warehouses, depots and units that all need structured cabling, fibre and CCTV. Firms wiring offices, factories, schools and multi-site businesses in Cat5e, Cat6 and fibre take on work right across Walsall and the wider Black Country, alongside the broadband and CCTV trade serving homes and small premises. It is steady, proper local work.",
  ],
  "kit_loc":"across the town's streets, cabinets and customer premises",
  "s2_intro":"Whether you are a build contractor with crews across Walsall, a structured-cabling firm or a one-van broadband installer toward Wolverhampton",
 },
 "warrington": {
  "region":"Warrington and Cheshire",
  "nearby":["Widnes","Runcorn","St Helens"],
  "snapshot":"Warrington sits between Liverpool and Manchester in the middle of a busy Cheshire full-fibre build, with CityFibre, Openreach and Freedom Fibre all running engineers across the town and a long tail of broadband, CCTV and cabling installers working behind them. The trade here splits two ways, and we serve both: build contractors and cabling firms that field whole crews and buy on a trade account, and sole-trader and direct installers who order branded workwear online with no account.",
  "s1_head":"Kitting the field engineers of Cheshire",
  "s1loc":[
   "Warrington is deep into a full-fibre build, sitting between Liverpool and Manchester. CityFibre has built full fibre across the town centre, Great Sankey, Latchford and Padgate, Openreach has put around 51 million pound into its own ultrafast network, and Freedom Fibre has built for homes around Culcheth, Croft and the south of the town. Coverage now runs high across the WA postcodes, with Virgin Media and the mobile operators upgrading on top. Behind the named networks sits the usual long tail of broadband, CCTV and structured-cabling installers working across the town's streets, cabinets and customer premises.",
   "Alongside the residential rollout sits a strong commercial scene. Warrington is a major business and logistics location, with Birchwood Park, the Gemini and Omega retail and distribution zones and the Lingley Mere and Daresbury sites carrying offices, warehouses and large employers. All of it needs structured cabling, fibre and CCTV, and firms wiring offices, schools, depots and multi-site businesses in Cat5e, Cat6 and fibre take on work right across Cheshire. Combined with the broadband and CCTV trade serving homes and small premises, it keeps a steady base of installers and cabling crews busy across the town.",
  ],
  "kit_loc":"across the town's streets, cabinets and customer premises",
  "s2_intro":"Whether you are a build contractor with crews across Warrington, a structured-cabling firm or a one-van broadband installer toward Widnes",
 },
 "slough": {
  "region":"Slough and the Thames Valley",
  "nearby":["Maidenhead","Windsor","Hayes"],
  "snapshot":"Slough sits in the Thames Valley with a completed full-fibre build, with CityFibre, Openreach and Virgin Media all at similar gigabit coverage and a busy base of broadband, CCTV and cabling installers working behind them. The trade here splits two ways, and we serve both: build contractors and cabling firms that field whole crews and buy on a trade account, and sole-trader and direct installers who order branded workwear online with no account at all.",
  "s1_head":"Kitting the field engineers of the Thames Valley",
  "s1loc":[
   "Slough has had a town-wide full-fibre build. CityFibre invested around 24 million pound and laid almost 500km of fibre, completing a primary build that is ready for service for tens of thousands of homes and most businesses, and starting the work on the Slough Trading Estate itself. Openreach and Virgin Media have built alongside, so CityFibre, Openreach and Virgin Media now sit at a similar level of gigabit coverage. The work runs through Chalvey, Cippenham, Langley and Britwell, with the mobile operators upgrading on top, behind which sits a long tail of broadband, CCTV and structured-cabling installers working across the town's streets, cabinets and customer premises.",
   "Alongside the residential rollout sits one of the biggest commercial scenes in the country. The Slough Trading Estate is one of the largest single-ownership business parks in Europe, the town is a major data-centre cluster for the Thames Valley, and the surrounding office and logistics units carry corporate headquarters and tech firms. All of it needs structured cabling, fibre and CCTV, and firms wiring offices, data halls, schools and multi-site businesses in Cat5e, Cat6 and fibre take on work right across the Thames Valley, alongside the broadband and CCTV trade serving homes and small premises. It is steady, proper local work.",
  ],
  "kit_loc":"across the town's streets, cabinets and customer premises",
  "s2_intro":"Whether you are a build contractor with crews across Slough, a structured-cabling firm or a one-van broadband installer toward Maidenhead",
 },
 "huddersfield": {
  "region":"Huddersfield and West Yorkshire",
  "nearby":["Halifax","Dewsbury","Brighouse"],
  "snapshot":"Huddersfield sits inside a heavy West Yorkshire full-fibre build, with Openreach and CityFibre both built out across the town and a long tail of broadband, CCTV and cabling installers working behind them. The trade here splits two ways, and we serve both: build contractors and cabling firms that field whole crews and buy on a trade account, and sole-trader and direct installers who order branded workwear online with no account at all.",
  "s1_head":"Kitting the field engineers of West Yorkshire",
  "s1loc":[
   "Huddersfield is deep into a full-fibre build, part of a wider West Yorkshire push. Openreach has taken Full Fibre past more than 80 per cent of properties locally, with almost 60,000 homes and businesses able to upgrade, sitting inside a 237 million pound regional investment that has reached more than 790,000 premises across West Yorkshire. CityFibre has built across much of the town too, with Virgin Media and the mobile operators upgrading on top. The work runs through Lindley, Marsh, Paddock, Lockwood and Almondbury, behind which sits the usual long tail of broadband, CCTV and structured-cabling installers working across the town's streets, cabinets and customer premises.",
   "Alongside the residential rollout sits a real commercial scene. Huddersfield carries the University of Huddersfield, a busy town centre and surrounding industrial estates and business units across the Colne and Holme valleys, all of which need structured cabling, fibre and CCTV. Firms wiring offices, mills, schools and multi-site businesses in Cat5e, Cat6 and fibre take on work right across this part of West Yorkshire, stretching out toward Brighouse, Dewsbury and Halifax. Combined with the broadband and CCTV trade serving homes and small premises, it keeps a steady base of installers and cabling crews busy across the area.",
  ],
  "kit_loc":"across the town's streets, cabinets and customer premises",
  "s2_intro":"Whether you are a build contractor with crews across Huddersfield, a structured-cabling firm or a one-van broadband installer toward Halifax",
 },
 "telford": {
  "region":"Telford and Shropshire",
  "nearby":["Shrewsbury","Wolverhampton","Cannock"],
  "snapshot":"Telford sits inside a busy Shropshire full-fibre build, with Openreach, Virgin Media and the alt-net Exascale all running engineers across the borough and a long tail of broadband, CCTV and cabling installers working behind them. The trade here splits two ways, and we serve both: build contractors and cabling firms that field whole crews and buy on a trade account, and sole-trader and direct installers who order branded workwear online with no account at all.",
  "s1_head":"Kitting the field engineers of Shropshire",
  "s1loc":[
   "Telford is deep into a full-fibre build, with the network rapidly expanding across Shropshire. Openreach was first to start rolling out Full Fibre and its build is spreading fast, Virgin Media has a strong presence in Telford and Wrekin offering both hybrid and full-fibre services, and the alt-net Exascale has built a fibre route from the business-dense Hortonwood area through Trench Lock, Donnington, Ketley, Lawley, Horsehay and Madeley down to Halesfield. The work runs through Stirchley, Madeley, Dawley, Hadley and Oakengates, behind which sits the usual long tail of broadband, CCTV and structured-cabling installers working across the town's streets, cabinets and customer premises.",
   "Alongside the residential rollout sits a strong industrial and commercial scene. Telford is a major manufacturing and distribution location, and its big estates - Hortonwood, Stafford Park, Halesfield and Hadley Castle, plus Telford Town Centre off junction 5 of the M54 - carry factories, warehouses and offices that all need structured cabling, fibre and CCTV. Firms wiring offices, factories, schools and multi-site businesses in Cat5e, Cat6 and fibre take on work right across Telford and the wider Shropshire, alongside the broadband and CCTV trade serving homes and small premises. It is steady, proper local work.",
  ],
  "kit_loc":"across the town's streets, cabinets and customer premises",
  "s2_intro":"Whether you are a build contractor with crews across Telford, a structured-cabling firm or a one-van broadband installer toward Shrewsbury",
 },
 "newport": {
  "region":"Newport and South Wales",
  "nearby":["Cardiff","Cwmbran","Pontypool"],
  "snapshot":"Newport sits in the middle of a busy South Wales network build, with Openreach, the Welsh alt-net Ogi and other providers pushing full fibre across the city and the surrounding valleys. Around that rollout sits a steady commercial cabling and CCTV trade. We kit both routes here: trade accounts for build contractors and cabling firms running fleets of engineers, and direct online ordering, with no account, for the sole trader and one-van installer.",
  "s1_head":"Kitting the field engineers of Newport and Gwent",
  "s1loc":[
   "Newport is in the thick of the South Wales full-fibre build. Openreach has engineers across Gwent extending Full Fibre out through Pillgwenlly, Ringland, Bettws and Maesglas, while Ogi, the Wales-focused alternative network with a regional office in Newport, builds its own FTTP through communities like Langstone, Underwood and Llanvaches. Virgin Media and the mobile operators keep upgrading on top, and Project Gigabit work reaches the harder rural premises around the city. Behind the build sit a long tail of broadband, CCTV and structured-cabling installers taking on work street by street.",
   "Alongside the residential rollout runs a strong commercial scene. Newport carries the South Wales semiconductor cluster, with KLA building its European base at Imperial Park, the Nexperia and Vishay wafer fab, and a packaging chain reaching toward Caldicot. Add the Admiral offices by the railway station, the government and civil-service presence, and business parks like Celtic Springs and Imperial Park, and you get a constant demand for structured cabling in Cat5e, Cat6 and fibre plus CCTV across offices, cleanrooms and campuses. Local cabling and security installers wire those sites for businesses right across the city.",
  ],
  "kit_loc":"across the city's streets, cabinets and customer premises",
  "s2_intro":"Whether you are a build contractor with crews across Newport, a structured-cabling firm or a one-van broadband installer toward Cwmbran",
 },
 "oxford": {
  "region":"Oxford and Oxfordshire",
  "nearby":["Abingdon","Didcot","Witney"],
  "snapshot":"Oxford and the wider Oxfordshire are in the middle of a steady full-fibre build, with Openreach, the alt-net Netomnia with YouFibre and Gigaclear out in the county all extending networks across the area. Around the build sits a strong commercial cabling and CCTV trade serving the science parks and colleges. We kit both routes here: trade accounts for contractors and cabling firms running fleets, and direct online ordering, with no account, for the one-van installer.",
  "s1_head":"Kitting the field engineers of Oxfordshire",
  "s1loc":[
   "Oxford is well into its full-fibre upgrade. Openreach is modernising the Oxford exchange areas with FTTP, the alternative network Netomnia is building with YouFibre across southern parts of the city behind a multi-million-pound investment, and Virgin Media with nexfibre covers much of the built-up area. Out beyond the ring road, Gigaclear runs extensive rural full fibre through the Oxfordshire villages, with Project Gigabit work reaching the harder premises. Districts like Cowley, Headington, Botley and Blackbird Leys all see engineers on the street, supported by a long tail of broadband and CCTV installers taking on the connections.",
   "Around the residential build sits a heavyweight commercial scene. Oxford carries the university colleges and research estate, the science and innovation parks at Oxford Science Park and Begbroke, and the national science campus at Harwell with Milton Park nearby toward Didcot. Add the John Radcliffe and Churchill hospital sites and the BMW plant at Cowley, and you get constant demand for structured cabling in Cat5e, Cat6 and fibre plus CCTV across labs, offices and campuses. Local cabling and security firms wire those sites for businesses across the city and county.",
  ],
  "kit_loc":"across the city's streets, cabinets and customer premises",
  "s2_intro":"Whether you are a build contractor with crews across Oxford, a structured-cabling firm or a one-van broadband installer toward Didcot",
 },
 "poole": {
  "region":"Poole and the Dorset coast",
  "nearby":["Bournemouth","Christchurch","Ferndown"],
  "snapshot":"Poole sits inside the Bournemouth, Christchurch and Poole conurbation, where CityFibre, Openreach and Virgin Media are all pushing full fibre across the area. Around the build runs a steady commercial cabling and CCTV trade along the harbourside and business parks. We kit both routes here: trade accounts for build contractors and cabling firms running fleets of engineers, and direct online ordering, with no account, for the sole trader and one-van installer.",
  "s1_head":"Kitting the field engineers of the Dorset coast",
  "s1loc":[
   "Poole is part of one of the south coast's biggest full-fibre builds. CityFibre has invested tens of millions across Bournemouth, Christchurch and Poole, passing well over 100,000 premises and putting areas like Canford Heath and Canford Cliffs live, while Virgin Media covers much of the conurbation and altnets such as toob add further choice. Openreach continues its own FTTP work on top. Across Parkstone, Branksome, Hamworthy and Upton, engineers and a long tail of broadband and CCTV installers are on the street day to day, working the cabinets and customer premises.",
   "Alongside the residential rollout sits a busy commercial scene. Poole carries a working harbour and quayside, the Holes Bay and Nuffield industrial estates, and a marine and manufacturing base running into the wider Bournemouth conurbation. Add the offices, retail parks and holiday accommodation along the coast, and you get steady demand for structured cabling in Cat5e, Cat6 and fibre plus CCTV across units, offices and seafront sites. Local cabling and security installers wire those premises for businesses around the town and across the BCP area.",
  ],
  "kit_loc":"across the town's streets, cabinets and customer premises",
  "s2_intro":"Whether you are a build contractor with crews across Poole, a structured-cabling firm or a one-van broadband installer toward Bournemouth",
 },
 "dundee": {
  "region":"Dundee and Tayside",
  "nearby":["Perth","Arbroath","Kirkcaldy"],
  "snapshot":"Dundee is a CityFibre full-fibre city, with that build now complete and GoFibre and Openreach extending gigabit broadband across Tayside on top. Around the rollout sits a strong commercial cabling and CCTV trade serving the waterfront and campuses. We kit both routes here: trade accounts for build contractors and cabling firms running fleets of engineers, and direct online ordering, with no account, for the sole trader and one-van installer.",
  "s1_head":"Kitting the field engineers of Tayside",
  "s1loc":[
   "Dundee is a CityFibre full-fibre city. CityFibre completed the primary build of its network here, laying hundreds of kilometres of full fibre and passing more than 58,000 homes, and it also wired public-sector sites across the city. Openreach continues its own FTTP upgrades, Virgin Media covers much of the built-up area, and GoFibre is now delivering its Project Gigabit build across the wider Tayside, Angus and Perth and Kinross area. Across Lochee, Broughty Ferry, Menzieshill and the city centre, engineers and a long tail of broadband and CCTV installers work the cabinets and premises.",
   "Alongside the residential rollout runs a strong commercial scene. Dundee's transformed waterfront is anchored by the V and A Dundee, and the city is a long-standing UK hub for video-game development around Abertay University, with studios and a wider creative-tech cluster. Add the life-sciences research at the University of Dundee and Ninewells, the city's two universities, and the harbour and business parks, and you get steady demand for structured cabling in Cat5e, Cat6 and fibre plus CCTV across studios, labs and offices. Local cabling and security firms wire those sites across the city.",
  ],
  "kit_loc":"across the city's streets, cabinets and customer premises",
  "s2_intro":"Whether you are a build contractor with crews across Dundee, a structured-cabling firm or a one-van broadband installer toward Perth",
 },
 "cambridge": {
  "region":"Cambridge and Cambridgeshire",
  "nearby":["Peterborough","Bedford","Stevenage"],
  "snapshot":"Cambridge has several competing full-fibre networks going in at once, with Openreach, CityFibre, Netomnia with YouFibre and Virgin Media with nexfibre all building across the city. Around the build sits a heavyweight commercial cabling and CCTV trade serving Silicon Fen. We kit both routes here: trade accounts for build contractors and cabling firms running fleets of engineers, and direct online ordering, with no account, for the sole trader and one-van installer.",
  "s1_head":"Kitting the field engineers of Cambridgeshire",
  "s1loc":[
   "Cambridge has a busy multi-network full-fibre build. Openreach runs its own FTTP across the city, CityFibre has laid well over a hundred kilometres of full fibre and backs a large Project Gigabit programme across Cambridgeshire, the alternative network Netomnia builds with YouFibre, and Virgin Media with nexfibre covers much of the built-up area. Across Cherry Hinton, Trumpington, Arbury, Chesterton and the Mill Road area, engineers and a long tail of broadband and CCTV installers work the cabinets and customer premises day to day, with rural Project Gigabit work reaching the harder county premises.",
   "Around the residential build sits one of the UK's strongest commercial scenes. This is Silicon Fen: Cambridge Science Park, Cambridge Business Park and St John's Innovation Centre to the north, the Cambridge Biomedical Campus with Addenbrooke's and Royal Papworth to the south, and the university colleges and labs through the centre. Add the deep-tech, AI and biotech firms across the city, and you get constant demand for structured cabling in Cat5e, Cat6 and fibre plus CCTV across labs, offices and campuses. Local cabling and security firms wire those sites for businesses across the city and county.",
  ],
  "kit_loc":"across the city's streets, cabinets and customer premises",
  "s2_intro":"Whether you are a build contractor with crews across Cambridge, a structured-cabling firm or a one-van broadband installer toward Peterborough",
 },
 "york": {
  "region":"York and North Yorkshire",
  "nearby":["Harrogate","Selby","Knaresborough"],
  "snapshot":"York is a CityFibre full-fibre city, with Openreach and Virgin Media building alongside across the city. Around the rollout sits a steady commercial cabling and CCTV trade serving the university and the bio-economy campuses. We kit both routes here: trade accounts for build contractors and cabling firms running fleets of engineers, and direct online ordering, with no account, for the sole trader and one-van installer.",
  "s1_head":"Kitting the field engineers of North Yorkshire",
  "s1loc":[
   "York has a long full-fibre history and a busy current build. CityFibre runs a city-wide full-fibre network here, one of the earliest large residential rollouts in the UK, and it is still extending through Clifton Moor, Fulford, parts of Huntington and the city centre. Openreach is upgrading the York Central, Acomb, Dringhouses and Melrosegate exchange areas with its own FTTP, and Virgin Media covers much of the built-up area. Across Holgate, Tang Hall, Heworth and Clifton, engineers and a long tail of broadband and CCTV installers work the cabinets and customer premises day to day.",
   "Alongside the residential rollout sits a strong commercial scene. York carries the University of York at Heslington and York Science Park, and the bio-economy effort through BioYorkshire and the York Biotech Campus, the former agri-food site north of the city. Add the rail and visitor economy, the city-centre offices and the business parks at Clifton Moor and Monks Cross, and you get steady demand for structured cabling in Cat5e, Cat6 and fibre plus CCTV across labs, offices and heritage sites. Local cabling and security firms wire those premises across the city and North Yorkshire.",
  ],
  "kit_loc":"across the city's streets, cabinets and customer premises",
  "s2_intro":"Whether you are a build contractor with crews across York, a structured-cabling firm or a one-van broadband installer toward Harrogate",
 },
 "blackpool": {
  "region":"Blackpool and the Fylde Coast",
  "nearby":["Lytham St Annes","Poulton-le-Fylde","Preston"],
  "snapshot":"Blackpool is a CityFibre full-fibre town, with Virgin Media and Openreach building alongside across the Fylde coast. Around the rollout sits a steady commercial cabling and CCTV trade serving the seafront and enterprise zones. We kit both routes here: trade accounts for build contractors and cabling firms running fleets of engineers, and direct online ordering, with no account, for the sole trader and one-van installer.",
  "s1_head":"Kitting the field engineers of the Fylde Coast",
  "s1loc":[
   "Blackpool is well into its full-fibre upgrade. CityFibre is investing tens of millions to take gigabit-capable full fibre to nearly every home and business in the town, Virgin Media already covers much of the resort, and Openreach adds its own FTTP on top, so the town is now among the better-connected in the country. There is also shared public fibre laid along the tramline corridor from Squires Gate toward Fleetwood. Across Bispham, Marton, Layton and South Shore, engineers and a long tail of broadband and CCTV installers work the cabinets and customer premises day to day.",
   "Alongside the residential rollout runs a distinctive commercial scene. Blackpool's economy turns on tourism, with the Promenade, the Pleasure Beach and the hotels and attractions all needing connectivity, and the town sits within an advanced-manufacturing and energy cluster. Add the Blackpool Airport Enterprise Zone, the Hillhouse Technology Enterprise Zone toward Fleetwood, the large civil-service presence and the BAE Systems site at Warton nearby, and you get steady demand for structured cabling in Cat5e, Cat6 and fibre plus CCTV across offices, units and seafront sites. Local cabling and security firms wire those premises across the Fylde.",
  ],
  "kit_loc":"across the town's streets, cabinets and customer premises",
  "s2_intro":"Whether you are a build contractor with crews across Blackpool, a structured-cabling firm or a one-van broadband installer toward Lytham St Annes",
 },
 "ipswich": {
  "region":"Ipswich and Suffolk",
  "nearby":["Colchester","Chelmsford","Norwich"],
  "snapshot":"Ipswich is a busy full-fibre town, with CityFibre having finished its primary build past most of the town and Openreach and County Broadband adding more across Suffolk. That mix of work keeps a steady stream of engineers and installers on the road. We kit both sides of the trade in Ipswich: build contractors and structured-cabling firms running fleets on trade accounts, and sole-trader broadband and CCTV installers ordering direct online with no account at all.",
  "s1_head":"Kitting the field engineers of Suffolk",
  "s1loc":[
   "Ipswich has had one of the more intense full-fibre builds in the east of England. CityFibre completed its primary network past around 98 percent of the town, working through areas like Kesgrave, Foxhall and Whitton, while Openreach has pushed its own FTTP across Suffolk and County Broadband has wired the rural villages around Ipswich, Hadleigh and the Shotley peninsula. Behind every one of those networks sit the delivery partners and civils crews who dig the footways, blow fibre through ducts and connect homes, working out of compounds and welfare units right across the IP postcodes.",
   "Alongside the residential rollout, Ipswich has a genuinely deep telecoms and structured-cabling scene anchored by Adastral Park at Martlesham Heath, BT's research campus and the Innovation Martlesham cluster of high-tech firms, plus the University of Suffolk DigiTech Centre. Cabling and CCTV installers wire offices and units around Ransomes Europark, the Ipswich Waterfront, Whitehouse Industrial Estate and the port estate down towards Felixstowe in Cat5e, Cat6 and fibre. It is the kind of work that needs engineers in branded polos and softshells day in, day out across the town.",
  ],
  "kit_loc":"across the town's streets, cabinets and customer premises",
  "s2_intro":"Whether you are a build contractor with crews across Ipswich, a structured-cabling firm or a one-van broadband installer toward Colchester",
 },
 "middlesbrough": {
  "region":"Middlesbrough and Teesside",
  "nearby":["Stockton-on-Tees","Redcar","Hartlepool"],
  "snapshot":"Middlesbrough sits in the middle of a major Teesside full-fibre build, with CityFibre's town-wide network alongside Openreach FTTP and Virgin Media and nexfibre on top. All of it keeps engineers and installers working across Teesside. We supply both routes in Middlesbrough: the build contractors and cabling firms that run fleets and buy on trade accounts, and the sole-trader broadband and CCTV installers who order direct online with no account needed.",
  "s1_head":"Kitting the field engineers of Teesside",
  "s1loc":[
   "Middlesbrough is at the heart of a large Tees Valley network build. CityFibre's town-wide full-fibre rollout has been going in since the work started in the Brambles Farm and Thorntree areas, with Stockton-based MAP Group as a build partner, and the wider Tees Valley investment runs alongside the Hartlepool and Redcar joint build. Openreach FTTP, Virgin Media's cable network and nexfibre are all extending across Teesside too. That stacks delivery partners, civils crews and connection engineers onto the streets of Middlesbrough and out toward Stockton-on-Tees, Redcar and Hartlepool every working day.",
   "On the commercial side, Middlesbrough has a strong and growing digital quarter. Teesside University leads the DigitalCity initiative, the Boho Zone is the town's digital and creative hub, and Teesworks on the river is one of the biggest industrial regeneration sites in the country. Structured-cabling and CCTV installers wire offices, campus buildings and units around the town centre, Riverside Park and the Teesside Industrial Estate in Cat5e, Cat6 and fibre. It is steady engineer-on-site work that needs proper branded hi-vis and softshells across Teesside.",
  ],
  "kit_loc":"across the town's streets, cabinets and customer premises",
  "s2_intro":"Whether you are a build contractor with crews across Middlesbrough, a structured-cabling firm or a one-van broadband installer toward Stockton-on-Tees",
 },
 "gloucester": {
  "region":"Gloucester and Gloucestershire",
  "nearby":["Cheltenham","Worcester","Swindon"],
  "snapshot":"Gloucester is a multi-network full-fibre city, with CityFibre and Openreach both building hard and Gigaclear strong across rural Gloucestershire. That mix keeps engineers and installers busy right across the county. We kit both sides of the trade in Gloucester: the build contractors and structured-cabling firms running fleets on trade accounts, and the sole-trader broadband and CCTV installers who order direct online with no account at all.",
  "s1_head":"Kitting the field engineers of Gloucestershire",
  "s1loc":[
   "Gloucester has seen full fibre go in from several directions. CityFibre has been live across large parts of the city, with areas like Quedgeley among the first to switch on, Openreach has its own FTTP build running through the city and out into Gloucestershire, and Gigaclear, the rural full-fibre specialist for the South West, reaches the villages around the county. Smaller networks like Hyperoptic and OFNL appear in pockets too. Behind all of it, delivery partners and civils crews work the footways through Barnwood, Hempsted, Kingsway and the rest of the GL postcodes.",
   "Gloucester's commercial cabling scene runs around its docks and business parks. The regenerated Gloucester Quays and Gloucester Docks, the King's Quarter scheme in the city centre and Olympus Park out at Quedgeley all draw offices, units and multi-site businesses that need structured cabling and CCTV. Installers wire these in Cat5e, Cat6 and fibre, with more work out toward the Gloucester Business Park at Brockworth and the trading estates near the M5. It is consistent engineer-on-site work that calls for branded polos and softshells across the city.",
  ],
  "kit_loc":"across the city's streets, cabinets and customer premises",
  "s2_intro":"Whether you are a build contractor with crews across Gloucester, a structured-cabling firm or a one-van broadband installer toward Cheltenham",
 },
 "exeter": {
  "region":"Exeter and Devon",
  "nearby":["Exmouth","Newton Abbot","Torquay"],
  "snapshot":"Exeter is one of the best-connected cities in the South West, with Openreach FTTP across most of the city, Virgin Media cable and Jurassic Fibre building locally. All of it keeps engineers and installers on the road across Devon. We supply both routes in Exeter: build contractors and cabling firms that run fleets and buy on trade accounts, and sole-trader broadband and CCTV installers who order direct online with no account needed.",
  "s1_head":"Kitting the field engineers of Devon",
  "s1loc":[
   "Exeter has had a strong full-fibre rollout. Openreach invested heavily in its FTTP network across the city, reaching the large majority of properties, while Virgin Media's cable network covers much of Exeter and Jurassic Fibre, the Devon-based full-fibre altnet, has built around the eastern edge of the city and out to Exmouth. That keeps Openreach delivery partners and civils crews working the streets through Heavitree, Pinhoe, Alphington and St Thomas, and out toward Exmouth, Newton Abbot and Tiverton as the build pushes across Devon.",
   "On the commercial side, Exeter has real anchors for structured-cabling and CCTV work. The Met Office headquarters and Exeter Science Park sit out at Sowton, the University of Exeter's Streatham campus runs across the north of the city, and the Marsh Barton and Sowton industrial estates and Skypark hold a big spread of offices and units. Installers wire all of these in Cat5e, Cat6 and fibre, plus the offices around Southernhay and the city centre. It is steady engineer-on-site work that needs branded hi-vis and softshells across the EX postcodes.",
  ],
  "kit_loc":"across the city's streets, cabinets and customer premises",
  "s2_intro":"Whether you are a build contractor with crews across Exeter, a structured-cabling firm or a one-van broadband installer toward Exmouth",
 },
 "solihull": {
  "region":"Solihull and the West Midlands",
  "nearby":["Birmingham","Coventry","Sutton Coldfield"],
  "snapshot":"Solihull is a full-fibre town in the middle of the West Midlands build, with CityFibre's network finished past much of the borough and Openreach and Netomnia adding more on top. That keeps engineers and installers busy across the area. We kit both sides of the trade in Solihull: build contractors and structured-cabling firms running fleets on trade accounts, and sole-trader broadband and CCTV installers ordering direct online with no account at all.",
  "s1_head":"Kitting the field engineers of the West Midlands",
  "s1loc":[
   "Solihull sits inside the huge West Midlands network build. CityFibre completed its primary full-fibre build across the borough, taking in the town centre, Blythe Valley Park and the NEC corridor, while Openreach FTTP is also available across Solihull and Netomnia has been delivering tens of thousands of premises from its West Midlands exchanges nearby. Virgin Media covers much of the borough on top. That stacks delivery partners and civils crews onto the streets through Shirley, Olton, Knowle, Dorridge and Chelmsley Wood, with more work running out toward Birmingham, Coventry and Sutton Coldfield.",
   "Solihull's commercial cabling scene is genuinely strong because so much business sits in the borough. Birmingham Business Park, Blythe Valley Park off the M42, the National Exhibition Centre and Birmingham Airport, and the Touchwood centre and offices in the town all draw structured-cabling and CCTV work. Installers wire offices, units and campus buildings in Cat5e, Cat6 and fibre across Bickenhill, Elmdon and the town centre. It is consistent engineer-on-site work that needs branded polos and softshells across the borough.",
  ],
  "kit_loc":"across the town's streets, cabinets and customer premises",
  "s2_intro":"Whether you are a build contractor with crews across Solihull, a structured-cabling firm or a one-van broadband installer toward Birmingham",
 },
 "colchester": {
  "region":"Colchester and Essex",
  "nearby":["Chelmsford","Ipswich","Southend-on-Sea"],
  "snapshot":"Colchester is a full-fibre city served by Openreach, County Broadband and nexfibre, with more building across Essex all the time. That keeps engineers and installers on the road around the city and the county. We supply both routes in Colchester: build contractors and cabling firms that run fleets and buy on trade accounts, and sole-trader broadband and CCTV installers who order direct online with no account needed at all.",
  "s1_head":"Kitting the field engineers of Essex",
  "s1loc":[
   "Colchester's full fibre comes from a real mix of networks. Openreach has built FTTP across much of the city under its Essex contracts, County Broadband, the Essex-based altnet, has wired the rural communities around Colchester such as Wormingford and out into Tendring, and nexfibre's rollout has been spotted across the city too. That keeps Openreach delivery partners, County Broadband crews and civils teams working the footways through Greenstead, Highwoods, Stanway and Lexden, with more build pushing out toward Chelmsford and up toward Ipswich as the Essex programme continues.",
   "On the commercial side, Colchester has a solid spread of cabling and CCTV work. Colchester Business Park and the Severalls and Stanway industrial areas hold offices and units, the University of Essex sits at Wivenhoe Park on the edge of the city, and the town centre and the growing Northern Gateway draw more business in. Installers wire all of these in Cat5e, Cat6 and fibre, kitting out offices, schools and multi-site firms. It is steady engineer-on-site work that needs branded hi-vis and softshells across the CO postcodes.",
  ],
  "kit_loc":"across the city's streets, cabinets and customer premises",
  "s2_intro":"Whether you are a build contractor with crews across Colchester, a structured-cabling firm or a one-van broadband installer toward Chelmsford",
 },
 "cheltenham": {
  "region":"Cheltenham and Gloucestershire",
  "nearby":["Gloucester","Worcester","Swindon"],
  "snapshot":"Cheltenham is a national cyber hub in the middle of a full-fibre build, with CityFibre investing across the town and Openreach and Gigaclear adding more across Gloucestershire. That keeps engineers and installers busy across the area. We kit both sides of the trade in Cheltenham: build contractors and structured-cabling firms running fleets on trade accounts, and sole-trader broadband and CCTV installers ordering direct online with no account at all.",
  "s1_head":"Kitting the field engineers of Gloucestershire",
  "s1loc":[
   "Cheltenham has had a substantial full-fibre build. CityFibre is investing across the town to bring gigabit-capable full fibre town-wide, with work running through areas like Alstone, Rowanfield and Lansdown, while Openreach has its own FTTP build and Gigaclear, the rural full-fibre specialist, reaches the villages around Gloucestershire. Glide and OFNL appear in pockets too. Behind all of it, delivery partners and civils crews dig the footways and blow fibre through the GL postcodes, working out of compounds across Cheltenham and toward Gloucester.",
   "Cheltenham's commercial cabling scene is shaped by its standing as a cyber and digital centre. GCHQ sits on the western edge of the town, and the major Golden Valley development beside it is set to deliver Cyber Central, a national cyber innovation district with over a million square feet of commercial space. That, plus the offices around the town centre, Montpellier and the business parks toward the racecourse, gives structured-cabling and CCTV installers plenty to wire in Cat5e, Cat6 and fibre. It is consistent engineer-on-site work that calls for branded polos and softshells across the town.",
  ],
  "kit_loc":"across the town's streets, cabinets and customer premises",
  "s2_intro":"Whether you are a build contractor with crews across Cheltenham, a structured-cabling firm or a one-van broadband installer toward Gloucester",
 },
 "gateshead": {
  "region":"Gateshead and Tyne and Wear",
  "nearby":["Newcastle upon Tyne","Sunderland","Middlesbrough"],
  "snapshot":"Gateshead is in the middle of a major full-fibre build, and the telecoms trade here runs on two tracks. Build contractors and structured-cabling firms field whole crews across the borough and buy through fleet and trade accounts, while ex-engineer sole traders and one-van broadband and CCTV installers take on work for homes and small businesses. We run trade accounts for the crews and direct online ordering, with no account, for everyone else who needs just a few branded pieces.",
  "s1_head":"Kitting the field engineers of Tyne and Wear",
  "s1loc":[
   "Gateshead is a CityFibre town. CityFibre is investing 42 million pound in a town-wide full fibre network reaching more than 109,000 properties, with GCU UK leading the build out of a Team Valley base and work that began around the Bridges and central Gateshead. Openreach is pushing FTTP across the borough alongside it, and Virgin Media O2 keeps upgrading its own footprint. Crews are working through districts such as Felling, Dunston, Teams and Bensham, threading fibre through streets, chambers and cabinets toward Newcastle upon Tyne across the river.",
   "Alongside the residential rollout sits a strong commercial and structured-cabling scene. Team Valley Trading Estate and its Kingsway spine, the MetroCentre retail estate, the Baltic Quarter and PROTO at Gateshead Quays all run on Cat5e, Cat6 and fibre backbones, with CCTV and access-control work across retail parks and offices. Local cabling and CCTV installers wire schools, warehouses and multi-site businesses around the borough, and the wider Tyne and Wear scene pulls in work toward Sunderland and back into Newcastle upon Tyne for offices, depots and the riverside developments.",
  ],
  "kit_loc":"across the borough's streets, cabinets and customer premises",
  "s2_intro":"Whether you are a build contractor with crews across Gateshead, a structured-cabling firm or a one-van broadband installer toward Newcastle upon Tyne",
 },
 "high wycombe": {
  "region":"High Wycombe and Buckinghamshire",
  "nearby":["Slough","Maidenhead","Reading"],
  "snapshot":"High Wycombe is in the middle of a busy full-fibre build, and the telecoms trade here splits two ways. Build contractors and structured-cabling firms put crews across the town and buy through fleet and trade accounts, while ex-engineer sole traders and one-van broadband and CCTV installers handle homes and small businesses. We run trade accounts for the crews and direct online ordering, with no account, for everyone else who only needs a few branded pieces to look the part.",
  "s1_head":"Kitting the field engineers of Buckinghamshire",
  "s1loc":[
   "High Wycombe has unusually heavy alt-net competition. CityFibre is investing 23 million pound in a town-wide full fibre network, with Instalcom as build partner and work that started in West Wycombe, while nexfibre, carrying Virgin Media O2 services, is delivering to more than 15,000 premises across High Wycombe and Marlow. Openreach engineers are building FTTP alongside both. Crews are working through Cressex, Totteridge, Sands, Booker and the HP11 town centre, threading fibre through streets, footways and cabinets toward Marlow and Slough.",
   "Alongside the residential rollout sits a solid commercial and structured-cabling scene. Cressex Business Park, the Globe Park estate at nearby Marlow and the town-centre and Sands industrial units all run on Cat5e, Cat6 and fibre backbones, with CCTV and access-control work across offices, schools and warehouses. Local cabling and CCTV installers wire multi-site businesses around the Wycombe district, and the trade reaches out along the M40 and Thames Valley toward Maidenhead and Slough for office fit-outs, retail parks and distribution units that need structured cabling and camera systems.",
  ],
  "kit_loc":"across the town's streets, cabinets and customer premises",
  "s2_intro":"Whether you are a build contractor with crews across High Wycombe, a structured-cabling firm or a one-van broadband installer toward Marlow",
 },
 "blackburn": {
  "region":"Blackburn and Lancashire",
  "nearby":["Accrington","Darwen","Burnley"],
  "snapshot":"Blackburn is in the middle of a full-fibre build, and the telecoms trade here runs on two tracks. Build contractors and structured-cabling firms field crews across the borough and buy through fleet and trade accounts, while ex-engineer sole traders and one-van broadband and CCTV installers take on work for homes and small businesses. We run trade accounts for the crews and direct online ordering, with no account, for everyone else who needs just a handful of branded pieces.",
  "s1_head":"Kitting the field engineers of Lancashire",
  "s1loc":[
   "Blackburn and Darwen are seeing a busy full fibre build. Openreach is rolling FTTP across the BB postcodes, Faster Britain has built a 10Gbps-capable full fibre network connecting thousands of organisations across Blackburn and Accrington, and Fusion Fibre Group is bringing ultrafast connectivity to homes and businesses across Lancashire. Virgin Media O2 keeps upgrading on top. Crews are working through districts such as Mill Hill, Ewood, Roe Lee, Shadsworth and Darwen, threading fibre through terraced streets, chambers and cabinets toward Accrington.",
   "Alongside the residential rollout sits a strong commercial and structured-cabling scene. The Whitebirk and Shadsworth industrial estates, Blackburn Interchange and the town-centre business units all run on Cat5e, Cat6 and fibre backbones, with CCTV and access-control work across mills, warehouses and offices. Local cabling and CCTV installers wire schools, factories and multi-site businesses around the borough, and the trade reaches across East Lancashire toward Accrington, Darwen and Burnley for distribution units, retail parks and the manufacturing premises that need structured cabling and camera systems.",
  ],
  "kit_loc":"across the borough's streets, cabinets and customer premises",
  "s2_intro":"Whether you are a build contractor with crews across Blackburn, a structured-cabling firm or a one-van broadband installer toward Accrington",
 },
 "maidstone": {
  "region":"Maidstone and Kent",
  "nearby":["Chatham","Rochester","Gravesend"],
  "snapshot":"Maidstone is in the middle of a major full-fibre build, and the telecoms trade here splits two ways. Build contractors and structured-cabling firms put crews across the town and buy through fleet and trade accounts, while ex-engineer sole traders and one-van broadband and CCTV installers handle homes and small businesses. We run trade accounts for the crews and direct online ordering, with no account, for everyone else who only needs a few branded pieces to look the part on site.",
  "s1_head":"Kitting the field engineers of Kent",
  "s1loc":[
   "Maidstone is a CityFibre town. CityFibre is investing 50 million pound in a town-wide full fibre network, delivered by Lanes-i and running toward completion across the borough. Openreach and Netomnia, carrying YouFibre, are both building their own FTTP in the same streets, with smaller builds from Hyperoptic and OFNL and Trooli edging in around Loose. Virgin Media O2 keeps upgrading on top. Crews are working through districts such as Shepway, Park Wood, Penenden Heath, Tovil and Loose, threading fibre through streets, chambers and cabinets toward Chatham.",
   "Alongside the residential rollout sits a busy commercial and structured-cabling scene. The Parkwood Industrial Estate, the 20/20 and Eclipse Park business parks off the M20, and the county-town offices that come with Maidstone being the Kent administrative centre all run on Cat5e, Cat6 and fibre backbones, with CCTV and access-control work across offices, depots and retail. Orbital Net delivers full fibre to business parks across Kent, and local cabling and CCTV installers wire schools and multi-site firms around the borough and out toward Rochester and Gravesend.",
  ],
  "kit_loc":"across the town's streets, cabinets and customer premises",
  "s2_intro":"Whether you are a build contractor with crews across Maidstone, a structured-cabling firm or a one-van broadband installer toward Chatham",
 },
 "basingstoke": {
  "region":"Basingstoke and Hampshire",
  "nearby":["Reading","Winchester","Andover"],
  "snapshot":"Basingstoke has been a full-fibre town since the early Openreach builds, and the telecoms trade here runs on two tracks. Build contractors and structured-cabling firms field crews across the town and buy through fleet and trade accounts, while ex-engineer sole traders and one-van broadband and CCTV installers take on homes and small businesses. We run trade accounts for the crews and direct online ordering, with no account, for everyone else who needs just a few branded pieces.",
  "s1_head":"Kitting the field engineers of Hampshire",
  "s1loc":[
   "Basingstoke was one of Openreach's early Fibre First towns, so FTTP coverage runs deep across the town, with Virgin Media O2 cable filling many of the gaps. Alt-net presence is lighter here, concentrated in Chineham, Lychpit, Popley, Oakridge, Old Basing and parts of Winklebury, with YouFibre running over Netomnia and CityFibre infrastructure and BDUK-funded cabinets being built around Chineham off the Basingstoke exchange. Crews are working through districts such as Brighton Hill, South Ham, Kempshott, Hatch Warren and Viables, threading fibre through streets, chambers and cabinets toward Reading.",
   "Alongside the residential network sits a heavyweight commercial and structured-cabling scene. Chineham Business Park, the adjacent Hampshire International Business Park, Houndmills, Kingsland and the Basing View enterprise zone host UK headquarters for the likes of Sony Professional Solutions, Eli Lilly, De La Rue and major insurance and finance names, all running on Cat5e, Cat6 and fibre backbones with extensive CCTV and access control. Local cabling and CCTV installers wire offices, data rooms and multi-site businesses around the town and out along the M3 toward Winchester and Reading.",
  ],
  "kit_loc":"across the town's streets, cabinets and customer premises",
  "s2_intro":"Whether you are a build contractor with crews across Basingstoke, a structured-cabling firm or a one-van broadband installer toward Reading",
 },
 "crawley": {
  "region":"Crawley and West Sussex",
  "nearby":["Horsham","Redhill","Reigate"],
  "snapshot":"Crawley sits next to Gatwick and is seeing a busy full-fibre build, and the telecoms trade here splits two ways. Build contractors and structured-cabling firms put crews across the town and buy through fleet and trade accounts, while ex-engineer sole traders and one-van broadband and CCTV installers handle homes and small businesses. We run trade accounts for the crews and direct online ordering, with no account, for everyone else who only needs a few branded pieces.",
  "s1_head":"Kitting the field engineers of West Sussex",
  "s1loc":[
   "Crawley has a layered full fibre build. CityFibre has invested 23 million pound in a town-wide network, with the rollout moving through areas such as Ifield West, Bewbush and Broadfield, while ITS Technology Group has completed a 32km XGS-PON full fibre network reaching more than 1,500 businesses, including over 700 in the Manor Royal district, backed by Towns Fund investment. Openreach is building FTTP alongside, with Virgin Media O2 upgrading on top. Crews thread fibre through streets, chambers and cabinets across the neighbourhoods and toward Horsham.",
   "Alongside the residential rollout sits a major commercial and structured-cabling scene. Manor Royal Business District, the biggest business park in the Gatwick Diamond at 540 acres with over 600 businesses, plus the cargo, hangar and office estates of London Gatwick Airport on its doorstep, all run on Cat5e, Cat6 and fibre backbones with heavy CCTV and access-control demand. Local cabling and CCTV installers wire offices, warehouses and aviation-support units around Manor Royal and out across the Surrey and Sussex border toward Redhill and Reigate.",
  ],
  "kit_loc":"across the town's streets, cabinets and customer premises",
  "s2_intro":"Whether you are a build contractor with crews across Crawley, a structured-cabling firm or a one-van broadband installer toward Horsham",
 },
 "chelmsford": {
  "region":"Chelmsford and Essex",
  "nearby":["Brentwood","Basildon","Colchester"],
  "snapshot":"Chelmsford is in the middle of a full-fibre build, and the telecoms trade here runs on two tracks. Build contractors and structured-cabling firms field crews across the city and buy through fleet and trade accounts, while ex-engineer sole traders and one-van broadband and CCTV installers take on homes and small businesses. We run trade accounts for the crews and direct online ordering, with no account, for everyone else who needs just a handful of branded pieces on site.",
  "s1_head":"Kitting the field engineers of Essex",
  "s1loc":[
   "Chelmsford has a busy full fibre build with several operators active. Openreach has rolled FTTP across much of the city and is extending further under Project Gigabit funding, while Netomnia, carrying YouFibre, and CityFibre are both building their own networks in and around the city, and County Broadband works the wider Essex footprint. Virgin Media O2 keeps upgrading on top. Crews are working through districts such as Springfield, Broomfield, Great Baddow, Moulsham, Widford and Chelmer Village, threading fibre through streets, chambers and cabinets toward Brentwood.",
   "Alongside the residential rollout sits a strong commercial and structured-cabling scene. Springfield Business Park off the A12 Boreham interchange, the Widford Industrial Estate, and the Anglia Ruskin University Rivermead campus and its Arise innovation hubs all run on Cat5e, Cat6 and fibre backbones, with CCTV and access-control work across offices, warehouses and the Britvic site at Widford. Local cabling and CCTV installers wire schools, depots and multi-site businesses around the city and out across Essex toward Basildon and Colchester for office fit-outs and distribution units.",
  ],
  "kit_loc":"across the city's streets, cabinets and customer premises",
  "s2_intro":"Whether you are a build contractor with crews across Chelmsford, a structured-cabling firm or a one-van broadband installer toward Brentwood",
 },
 "preston": {
  "region":"Preston and Lancashire",
  "nearby":["Blackburn","Chorley","Leyland"],
  "snapshot":"Preston is a busy full-fibre town, with Openreach, CityFibre and the alternative networks all building across the city and out into Lancashire. That keeps engineers and installers working hard, and they buy kit two ways. The national build contractors run whole crews and order through trade accounts, while ex-BT sole traders and small broadband and CCTV firms order direct online with no account. We serve both routes from the same workwear range.",
  "s1_head":"Kitting the field engineers of Lancashire",
  "s1loc":[
   "Preston is in the middle of a major full-fibre build. CityFibre's city-wide rollout has pushed through Frenchwood, Fishwick, Ribbleton, Holme Slack, Deepdale, Gallows Hill and the city centre, while Openreach keeps expanding its own Full Fibre network across Fulwood and the wider PR postcodes. Alternative networks including YouFibre on Netomnia, brsk and Hyperoptic build alongside them, which has made Preston one of the best-connected towns in Lancashire. All of that puts civils gangs, fibre jointers and provisioning engineers on the streets day in, day out, working cabinets, chambers and poles right across the city.",
   "Around the residential build sits a strong commercial and structured-cabling scene. The University of Central Lancashire (UCLan) in the city centre, the Samlesbury Enterprise Zone with BAE Systems and AMRC North West, and the business parks along the Preston East and Red Scar areas all need Cat5e, Cat6 and fibre wiring, plus CCTV and access control. Local cabling and security installers fit out offices, schools, warehouses and multi-site businesses across Preston, Fulwood and out toward Leyland and Chorley, working homes and commercial premises alike.",
  ],
  "kit_loc":"across the town's streets, cabinets and customer premises",
  "s2_intro":"Whether you are a build contractor with crews across Preston, a structured-cabling firm or a one-van broadband installer toward Leyland",
 },
 "walthamstow": {
  "region":"Walthamstow and north-east London",
  "nearby":["Ilford","Enfield","Loughton"],
  "snapshot":"Walthamstow sits in the middle of London's full-fibre push, with Openreach, Community Fibre and Hyperoptic all building across Waltham Forest. That keeps engineers and installers busy, and they buy kit two ways. The big build contractors field crews and order through trade accounts, while ex-BT sole traders and small broadband and CCTV firms order direct online with no account. We run both routes side by side from one workwear range.",
  "s1_head":"Kitting the field engineers of north-east London",
  "s1loc":[
   "Walthamstow is part of London's busy full-fibre rollout. Openreach is extending its Full Fibre network across Waltham Forest, Community Fibre is building its London-only network through the borough, and Hyperoptic has rolled out to streets and social housing across Walthamstow and the wider E17 area. The work runs through Wood Street, Higham Hill, St James Street and around Blackhorse Road, putting civils teams, fibre jointers and provisioning engineers on the streets working cabinets, chambers and customer premises right across this corner of north-east London.",
   "Around the residential build sits a strong commercial and structured-cabling scene. The Blackhorse Lane industrial estates, Uplands Business Park, SEGRO Park Walthamstow and the Lockwood Way units host warehouses, studios and maker spaces, while the high streets, schools and offices around Walthamstow Central all need Cat5e, Cat6 and fibre, plus CCTV and access control. Local cabling and security installers fit out these premises and take on work for homes and businesses across Walthamstow and out toward Ilford and Enfield, serving both commercial and residential jobs.",
  ],
  "kit_loc":"across the area's streets, cabinets and customer premises",
  "s2_intro":"Whether you are a build contractor with crews across Walthamstow, a structured-cabling firm or a one-van broadband installer toward Ilford",
 },
 "basildon": {
  "region":"Basildon and south Essex",
  "nearby":["Wickford","Rayleigh","Southend-on-Sea"],
  "snapshot":"Basildon is a busy network town, with Openreach and Virgin Media building full fibre across the new town and Project Gigabit reaching the harder neighbourhoods. That keeps engineers and installers working hard, and they buy kit two ways. The build contractors run crews and order through trade accounts, while ex-BT sole traders and small broadband and CCTV firms order direct online with no account. We serve both routes from one workwear range.",
  "s1_head":"Kitting the field engineers of south Essex",
  "s1loc":[
   "Basildon is in the middle of a steady full-fibre build. Openreach is extending its Full Fibre network across the town centre, Laindon, Pitsea, Vange, Fryerns and Langdon Hills, with Virgin Media's cable network already passing much of the new town, and Project Gigabit work reaching the harder-to-serve neighbourhoods that earlier commercial plans missed. The South Essex councils' public-sector fibre network adds to the picture too. All of that puts civils gangs, fibre jointers and provisioning engineers on the streets across the SS postcodes, working cabinets, chambers and customer premises day in, day out.",
   "Around the residential build sits a solid commercial and structured-cabling scene. Basildon Business Park, Cranes Farm Road, the Festival Leisure Park and the industrial estates around Pipps Hill and Burnt Mills host offices, warehouses, retail and leisure units that all need Cat5e, Cat6 and fibre, plus CCTV and access control. Local cabling and security installers fit out these premises and take on work for homes and businesses across Basildon and out toward Wickford and Rayleigh, serving both commercial and residential jobs.",
  ],
  "kit_loc":"across the town's streets, cabinets and customer premises",
  "s2_intro":"Whether you are a build contractor with crews across Basildon, a structured-cabling firm or a one-van broadband installer toward Wickford",
 },
 "dartford": {
  "region":"Dartford and Kent",
  "nearby":["Gravesend","Erith","Sidcup"],
  "snapshot":"Dartford is a busy full-fibre town on the Kent and south-east London edge, with Openreach and the alternative networks building across the DA postcodes. That keeps engineers and installers working hard, and they buy kit two ways. The big build contractors run crews and order through trade accounts, while ex-BT sole traders and small broadband and CCTV firms order direct online with no account. We run both routes from one workwear range.",
  "s1_head":"Kitting the field engineers of Kent",
  "s1loc":[
   "Dartford is part of Openreach's large Kent full-fibre programme, with engineers building and expanding the Full Fibre network across Dartford and nearby Barming, Bearsted and Aylesford as part of a major county-wide upgrade. Alternative networks such as Netomnia build alongside, using existing ducts and poles, and Virgin Media's cable network already passes much of the town. The work runs through the town centre, Temple Hill, Stone and out toward Greenhithe, putting civils gangs, fibre jointers and provisioning engineers on the streets working cabinets, chambers and customer premises right across this corner of Kent.",
   "Around the residential build sits a strong commercial and structured-cabling scene. Crossways Business Park beside the Dartford crossing, the retail and leisure units near Bluewater, and the trade and industrial estates around the town all need Cat5e, Cat6 and fibre, plus CCTV and access control. Local cabling and security firms fit out offices, warehouses and multi-site businesses across Dartford and out toward Gravesend and Erith, taking on work for both commercial premises and homes and keeping installers busy right across the DA postcodes.",
  ],
  "kit_loc":"across the town's streets, cabinets and customer premises",
  "s2_intro":"Whether you are a build contractor with crews across Dartford, a structured-cabling firm or a one-van broadband installer toward Gravesend",
 },
 "bedford": {
  "region":"Bedford and Bedfordshire",
  "nearby":["Kempston","Wellingborough","Milton Keynes"],
  "snapshot":"Bedford is a steady full-fibre town, with Openreach building across the borough and CityFibre's Project Gigabit work reaching the harder-to-serve areas of Bedfordshire. That keeps engineers and installers busy, and they buy kit two ways. The build contractors run crews and order through trade accounts, while ex-BT sole traders and small broadband and CCTV firms order direct online with no account. We serve both routes from one workwear range.",
  "s1_head":"Kitting the field engineers of Bedfordshire",
  "s1loc":[
   "Bedford is in the middle of a steady full-fibre build. Openreach is extending its Full Fibre network across the town and the wider MK postcodes, and CityFibre's Project Gigabit contract for Bedfordshire, Northamptonshire and Milton Keynes is bringing full fibre to harder-to-reach areas such as Bromham, Renhold, Willington, Cardington and Shortstown. Newer developments around New Cardington, Wixams and Fenlake are opening up fuller fibre choices too. All of that puts civils gangs, fibre jointers and provisioning engineers on the streets across Bedford and Kempston, working cabinets, chambers and customer premises day in, day out.",
   "Around the residential build sits a solid commercial and structured-cabling scene. The University of Bedfordshire campus, Bedford College and the iMET advanced-manufacturing centre, plus the business parks and industrial estates around Cardington, Elstow and the Wixams all need Cat5e, Cat6 and fibre, plus CCTV and access control. Local cabling and security installers fit out offices, schools, warehouses and multi-site businesses across Bedford and out toward Kempston and Wellingborough, taking on work for both commercial premises and homes.",
  ],
  "kit_loc":"across the town's streets, cabinets and customer premises",
  "s2_intro":"Whether you are a build contractor with crews across Bedford, a structured-cabling firm or a one-van broadband installer toward Kempston",
 },
 "doncaster": {
  "region":"Doncaster and South Yorkshire",
  "nearby":["Rotherham","Pontefract","Goole"],
  "snapshot":"Doncaster is a CityFibre town, with full fibre going in across the city alongside Openreach and the alternative networks. That keeps engineers and installers working hard, and they buy kit two ways. The build contractors run crews and order through trade accounts, while ex-BT sole traders and small broadband and CCTV firms order direct online with no account. We run trade accounts and direct online ordering side by side from one workwear range.",
  "s1_head":"Kitting the field engineers of South Yorkshire",
  "s1loc":[
   "Doncaster is a CityFibre town in the middle of a major full-fibre build. CityFibre's city-wide rollout has laid well over a hundred kilometres of fibre through Intake, Lakeside, Cantley, Bessacarr, Kirk Sandall, Edenthorpe, Wheatley, Hexthorpe, Balby and Armthorpe, delivered with build partners on its behalf. Openreach keeps expanding its own Full Fibre network across the DN postcodes alongside it. All of that puts civils gangs, fibre jointers and provisioning engineers on the streets across the city day in, day out, working cabinets, chambers and customer premises right across Doncaster.",
   "Around the residential build sits a strong commercial and structured-cabling scene. The iPort rail-freight and logistics park, the Lakeside business and retail area, and the trade and industrial estates around the wider DN region host warehouses, offices and distribution sites that all need Cat5e, Cat6 and fibre, plus CCTV and access control. Local cabling and security installers fit out these premises and take on work for homes and businesses across Doncaster and out toward Rotherham and Mexborough, serving both commercial and residential jobs.",
  ],
  "kit_loc":"across the city's streets, cabinets and customer premises",
  "s2_intro":"Whether you are a build contractor with crews across Doncaster, a structured-cabling firm or a one-van broadband installer toward Rotherham",
 },
 "worthing": {
  "region":"Worthing and the West Sussex coast",
  "nearby":["Lancing","Hove","Brighton"],
  "snapshot":"Worthing is a busy full-fibre town, with Openreach and the alternative networks building across the West Sussex coast. That keeps engineers and installers working hard, and they buy kit two ways. The build contractors run crews and order through trade accounts, while ex-BT sole traders and small broadband and CCTV firms order direct online with no account. We serve both the fleet and the one-van installer from one workwear range.",
  "s1_head":"Kitting the field engineers of the West Sussex coast",
  "s1loc":[
   "Worthing is part of a steady full-fibre build along the West Sussex coast. Openreach's build programme covers Worthing Central, Worthing West, Worthing Swandean, Findon, Shoreham and Lancing among dozens of exchange areas across the county, while alternative networks such as YouFibre on Netomnia have rolled out across parts of Worthing, Lancing and Rustington. The BEACH project has also added small mobile cells along the town centre and seafront. All of that puts civils gangs, fibre jointers and provisioning engineers on the streets across the BN postcodes, working cabinets, chambers and customer premises day in, day out.",
   "Around the residential build sits a solid commercial and structured-cabling scene. The Worthing seafront and town-centre offices, the GB Met college campuses, and the business and industrial estates around Lyons Farm and the wider Adur and Worthing area all need Cat5e, Cat6 and fibre, plus CCTV and access control. Local cabling and security installers fit out offices, schools and multi-site businesses across Worthing and out toward Lancing and Shoreham-by-Sea, taking on work for both commercial premises and homes along the coast.",
  ],
  "kit_loc":"across the town's streets, cabinets and customer premises",
  "s2_intro":"Whether you are a build contractor with crews across Worthing, a structured-cabling firm or a one-van broadband installer toward Lancing",
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
