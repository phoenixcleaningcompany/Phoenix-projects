#!/usr/bin/env python3
# EV (Entertainment, Events & Festivals) series builder v1.0 - read SPEC.md/CLAUDE.md
# HYBRID / audience BOTH, EQUAL weight: big venues, festival operators and event
# production companies with large SEASONAL crews (procurement / TRADE ACCOUNT,
# managed reordering, festival-season onboarding) AND small independent event crews,
# promoters and entertainers (DIRECT ONLINE, no account). VERY SEASONAL.
# DIFFERENTIATOR = TWO ENVIRONMENTS (VT-style): FRONT-OF-HOUSE (branded polos make
# stewards, bar, box-office and hospitality identifiable to the crowd - trust, crowd
# management, safety) + CREW/PRODUCTION/RIGGING (hi-vis, fleeces, waterproofs, cargo
# trousers and safety boots for the physical, outdoor, often-overnight get-in and
# breakdown). Lead = POLO + HI-VIS + FLEECE. NO softshell (kept in bleed to separate
# from TL). MEDIUM depth, LOW local variation (2 genuinely-local s1loc paras; generic
# shared paras in OWNER/PRESENT/NARROW pools). No JS, no entities, no delivery claims.
# Exactly 14 .com + 1 community per page. Nearby = geographic, on EV_towns.csv. Prefix ev-.
import re, os, json, sys, csv, glob
import hashlib
def pick(key, salt, n):
    h = hashlib.md5((salt + '|' + str(key).lower()).encode()).digest()
    return int.from_bytes(h[:4], 'big') % n

def _find_base():
    here = os.path.dirname(os.path.abspath(__file__))
    for p in (os.path.join(here,'ev-london.html'),'ev-london.html',
              '/mnt/user-data/outputs/ev-london.html','/home/claude/evkit/ev-london.html'):
        if os.path.exists(p): return p
    sys.exit("ERROR: ev-london.html (base template) not found beside ev_build.py")

BASE = open(_find_base(), encoding='utf-8').read()
DOMAIN = 'https://www.ineedworkwear.uk'

def between(start, end, src=BASE):
    i = src.index(start); j = src.index(end, i+len(start)); return src[i:j]
def aria_block(aria):
    k = BASE.index(aria)
    i = BASE.rfind('<div class="ev-wrap"><div class="ev-illust">', 0, k)
    j = BASE.index('</div></div></div>', k) + len('</div></div></div>')
    return BASE[i:j]

CSS      = between('<style>', '</style>') + '</style>'
HEADER   = between('<div class="ev-header">', '\n<div class="ev-hero">')
STATS    = between('<div class="ev-stats">', '\n<div class="ev-cta-bar">')
GARMENT  = between('<div class="ev-wrap"><div class="ev-illust"><div class="ev-garment-row">', '\n<div class="ev-section">')
EMB      = aria_block('Embroidery machine stitching')
SIGNPOST = aria_block('music festival welcome sign')
PREMISES = aria_block('serving event and festival crews across')
ORDER    = aria_block('Order entertainment, events and festivals workwear online')
CONTACT  = BASE[BASE.index('<div class="ev-contact-block">'):
                BASE.index('</div></div></div>', BASE.index('<div class="ev-contact-block">'))+len('</div></div></div>')]
FOOTER   = BASE[BASE.index('<footer class="ev-footer">'):BASE.index('</footer>')+len('</footer>')]

def sign_town(town):
    n = len(town)
    size = 34 if n <= 8 else 28 if n <= 11 else 23 if n <= 15 else 18 if n <= 20 else 15
    tl = ' textLength="300" lengthAdjust="spacingAndGlyphs"' if n > 13 else ''
    return (f'<text x="230" y="104" text-anchor="middle" font-family="Arial,sans-serif" '
            f'font-weight="800" font-size="{size}" fill="#5a3a1a"{tl}>{town.upper()}</text>')

EV_PRODUCTS = ["Polo Shirts and T-Shirts","Hi-Vis Vests and Jackets","Fleeces and Mid-Layers",
 "Waterproofs and Outdoor Jackets","Crew and Cargo Trousers","Safety Boots and Footwear",
 "Caps, Beanies and Accessories","Embroidery, Names and ID Branding"]

def _card(n,d): return f'<div class="ev-product-card"><div class="ev-product-name">{n}</div><div class="ev-product-detail">{d}</div></div>'
CARD_DETAILS=[
 ("Polo Shirts and T-Shirts",[
   "Branded polos and t-shirts for front-of-house, breathable and hard-wearing, the layer that makes stewards, bar and box-office staff instantly identifiable to the crowd.",
   "Breathable, hard-wearing branded polos and t-shirts for the front-of-house team, the layer that makes stewards, bar and box-office staff instantly identifiable to the crowd.",
   "Hard-wearing branded polos and t-shirts for front-of-house, the everyday layer that marks out stewards, bar and box-office staff as identifiable and approachable to the crowd."]),
 ("Hi-Vis Vests and Jackets",[
   "Hi-vis vests and jackets for stage crew, load-in and marshalling, keeping the team visible on a busy, dark site near vehicles, forklifts and moving kit.",
   "Hi-vis vests and jackets for stage crew, load-in and marshalling, keeping the team seen on a busy, dark site around vehicles, forklifts and moving kit.",
   "Hi-vis vests and jackets for crew, load-in and marshalling, keeping the team visible on a dark, busy site near vehicles, forklifts and moving stage kit."]),
 ("Fleeces and Mid-Layers",[
   "Warm branded fleeces and mid-layers for cold nights and long shifts, an easy layer for crew working outdoors through a get-in, a show and a breakdown.",
   "Branded fleeces and mid-layers for cold nights and long shifts, an easy warm layer for crew working outdoors through a get-in, a show and a breakdown.",
   "Cosy branded fleeces and mid-layers for cold nights and long shifts, layered up by crew working outdoors through the get-in, the show and the breakdown."]),
 ("Waterproofs and Outdoor Jackets",[
   "Waterproof jackets and trousers for wet fields and open sites, keeping crew dry and working through whatever the weather throws at an outdoor event or festival.",
   "Waterproof jackets and trousers for wet fields and open sites, keeping crew dry and working through whatever the weather brings at an outdoor event or festival.",
   "Weatherproof jackets and trousers for wet fields and open sites, keeping crew dry and on the job through whatever an outdoor event or festival throws at them."]),
 ("Crew and Cargo Trousers",[
   "Hard-wearing crew and cargo trousers with tool pockets for riggers, stage and production staff, built for the heavy, hands-on work of building and striking a show.",
   "Hard-wearing crew and cargo trousers with tool pockets for riggers, stage and production crew, made for the heavy, hands-on work of building and striking a show.",
   "Tough crew and cargo trousers with tool pockets for riggers, stage and production staff, built for the heavy, hands-on work of putting up and taking down a show."]),
 ("Safety Boots and Footwear",[
   "Safety boots and footwear for rigging, staging and load-in, protecting crew handling heavy kit and working on uneven outdoor ground across a long event day.",
   "Safety boots and footwear for rigging, staging and load-in, protecting crew who handle heavy kit and work on uneven outdoor ground across a long event day.",
   "Safety boots and footwear for rigging, staging and load-in, protecting crew handling heavy gear and working on rough outdoor ground through a long event day."]),
 ("Caps, Beanies and Accessories",[
   "Branded caps, beanies and accessories to finish the kit and handle the cold or the sun, embroidered to match the polos, hi-vis and fleeces across the team.",
   "Branded caps, beanies and accessories that finish the kit and handle the cold or the sun, embroidered to match the polos, hi-vis and fleeces the team already wears.",
   "Branded caps, beanies and accessories to complete the kit and cope with cold nights or sun, embroidered to match the rest of the team's polos, hi-vis and fleeces."]),
 ("Embroidery, Names and ID Branding",[
   "In-house embroidery of your operator name, logo and crew names onto polos, hi-vis, fleeces and caps, so a venue, a festival or a small crew looks consistent and professional.",
   "In-house embroidery of your operator name, logo and crew names across polos, hi-vis, fleeces and caps, so a venue, a festival or a small independent crew always looks consistent.",
   "Your operator name, logo and crew names embroidered in-house onto polos, hi-vis, fleeces and caps, so a venue, a festival or a small crew looks consistent and professional."]),
]
GRID_ORDER=[(0,1,2,3,4,5,6,7),(1,0,2,3,4,5,6,7),(0,1,3,2,4,5,6,7),(0,2,1,3,4,5,6,7)]
def build_grid(town):
    order = GRID_ORDER[pick(town,'gord',len(GRID_ORDER))]
    cards=[]
    for i in order:
        name,variants = CARD_DETAILS[i]
        cards.append(_card(name, variants[pick(town,f'g{i}',len(variants))]))
    return '<div class="ev-product-grid">'+''.join(cards)+'</div>'

TRUST_POOL=[
 "Branded polos, hi-vis, fleeces, waterproofs and safety boots for venues, festivals and event crews - front-of-house and crew, trade or direct online",
 "Branded polos, hi-vis, fleeces, waterproofs and safety boots for events and festivals - trade accounts for venues, direct online for crews",
 "Trusted by venues, festivals, production companies and event crews across the UK for branded front-of-house and crew workwear - trade or direct",
 "Branded workwear - polos, hi-vis, fleeces, waterproofs and safety boots - for venues, festivals and event crews across the UK, trade or direct online",
]
S2INTRO_POOL=[
 "Whether you are a major venue or festival or a small independent event crew in {t}, the range is built to kit you from one place: branded polos for the front-of-house team, and hi-vis, fleeces, waterproofs, cargo trousers and safety boots for the crew.",
 "A major {t} venue or festival, or a small independent event crew, is kitted from one place: branded polos for the front-of-house team, and hi-vis, fleeces, waterproofs, cargo trousers and safety boots for the crew.",
 "For a {t} venue or festival or a small independent crew, the range covers you from one place: branded polos for the front-of-house team, and hi-vis, fleeces, waterproofs, cargo trousers and safety boots for the crew.",
 "Whether it is a major {t} festival or a single independent crew, you are kitted from one place: branded polos for the front-of-house team, plus hi-vis, fleeces, waterproofs, cargo trousers and safety boots for the crew.",
]
EMB_P1_POOL=[
 "In entertainment and events, the team is the most visible part of the operation. At a busy {t} concert, festival or theatre, the audience needs to see at a glance who is staff and who to ask, and a clean, branded polo with the operator name does exactly that, turning a front-of-house steward, bar or box-office worker, even a casual or seasonal one, into a recognisable, approachable part of the team rather than just another person in the crowd.",
 "In entertainment and events, the team is the most visible part of the operation. At a busy {t} concert, festival or theatre, the audience needs to spot at a glance who is staff and who to ask, and a clean, branded polo with the operator name does just that, making a front-of-house steward, bar or box-office worker, even a casual or seasonal one, a recognisable, approachable part of the team rather than another face in the crowd.",
 "The team is the most visible part of any event. At a busy {t} concert, festival or theatre, the audience needs to see at a glance who is staff and who to approach, and a clean, branded polo with the operator name does exactly that, turning a front-of-house steward, bar or box-office worker, even a seasonal one, into a recognisable, approachable part of the team.",
 "In events and entertainment, the team is the operation made visible. At a busy {t} concert, festival or theatre, the audience needs to spot at a glance who is staff and who to ask, and a clean, branded polo with the operator name does exactly that, making even a casual or seasonal front-of-house hire a recognisable, approachable part of the team.",
]
EMB_P2_POOL=[
 "We brand in-house, which means your operator name and logo are embroidered onto polos, hi-vis, fleeces, waterproofs and caps, finished to survive heavy seasonal use and frequent washing. Send your artwork once, we hold it on file, and every reorder, new starter and new season matches the last, so whether it is a single independent crew or a major {t} venue with hundreds of staff and crew, the operation looks consistent from the front gate to the stage.",
 "Branding is done in-house onto polos, hi-vis, fleeces, waterproofs and caps - your operator name and logo embroidered and finished to survive heavy seasonal use and frequent washing. We hold your artwork on file, so every reorder, new starter and new season matches, and whether it is one independent crew or a major {t} venue with hundreds of staff, the operation looks consistent from the front gate to the stage.",
 "Your operator name and logo are embroidered in-house onto polos, hi-vis, fleeces, waterproofs and caps, finished to take heavy seasonal use and frequent washing. Held on file, your artwork reproduces on every reorder, new starter and new season, so a single independent crew or a major {t} venue with hundreds of staff looks consistent from the front gate to the stage.",
 "We badge in-house, embroidering your operator name and logo onto polos, hi-vis, fleeces, waterproofs and caps and finishing them to survive heavy seasonal use and washing. Held on file, your branding matches on every reorder and new starter, so a single {t} crew or a major venue with hundreds of staff looks consistent from the front gate to the stage.",
]
EMB_P3_POOL=[
 "And because events and festivals run on a big seasonal intake, that consistency is the point. We hold your branding and sizes on file, so onboarding a whole season's crew and front-of-house team, taking on extra hands for a busy festival weekend or kitting a second site reproduces exactly the same branded uniform every time, without anyone having to re-supply artwork or guess at a match.",
 "And because events and festivals run on a big seasonal intake, consistency is the value. We hold your branding and sizes on file, so onboarding a season's crew and front-of-house team, taking on extra hands for a festival weekend or kitting a second site comes back exactly the same branded uniform every time, with no artwork to re-supply.",
 "Because the trade runs on a big seasonal intake, that consistency matters. We keep your branding and sizes on file, so onboarding a whole season's crew and front-of-house team, taking on extra hands for a busy festival weekend or kitting a second site reproduces the same branded uniform each time.",
 "And because events and festivals turn on a big seasonal intake, that consistency is the whole point. We hold branding and sizes on file, so a season's crew, extra festival-weekend hands or a second site reproduce exactly the same branded uniform every time, with nothing to re-supply.",
]
CON_HEAD="Branded for Front-of-House, Built for the Crew"
CON_P1_POOL=[
 "Entertainment, events and festivals workwear has to do two very different jobs at once, and the right kit covers both. The first is front-of-house. The team is the most visible part of any event, so a branded polo with the operator name makes stewards, bar, box-office and hospitality staff instantly identifiable to the audience at a busy {t} venue, festival or theatre, the people a guest can find and ask, which matters for trust, crowd management and safety, and turns even a casual or seasonal hire into a recognisable part of the team.",
 "Entertainment, events and festivals workwear does two very different jobs at once, and the right kit does both. First, front-of-house: the team is the most visible part of any event, so a branded polo with the operator name makes stewards, bar, box-office and hospitality staff instantly identifiable to the audience at a busy {t} venue, festival or theatre, the people a guest can find and ask, which matters for trust, crowd management and safety, and turns even a seasonal hire into a recognisable part of the team.",
 "This workwear has to do two very different jobs at once, and the right kit covers both. The first is front-of-house. The team is the most visible part of any event, so a branded polo with the operator name makes stewards, bar, box-office and hospitality staff instantly identifiable to the audience at a busy {t} venue or festival, the people a guest can find and ask, which matters for trust, crowd management and safety, and turns even a casual or seasonal hire into a recognisable part of the team.",
 "Events and festivals workwear has to earn its place two ways at once. The first is front-of-house: the team is the most visible part of any event, so a branded polo with the operator name makes stewards, bar, box-office and hospitality staff instantly identifiable to the audience at a busy {t} venue or festival, the people to find and ask, which matters for trust, crowd management and safety, and turns even a seasonal hire into a recognisable part of the team.",
]
CON_P2_POOL=[
 "The second is the crew. Stage, rigging and production work is physical, outdoor and often overnight, so the crew needs hi-vis to stay visible on a busy, dark site near vehicles and moving kit, fleeces and waterproofs for cold nights and wet fields, cargo trousers for tools and safety boots for the heavy work of rigging and staging. It also has to cope with a very seasonal calendar and a big festival-season intake, kitting a wave of crew and front-of-house staff quickly when the season starts.",
 "The second is the crew. Stage, rigging and production work is physical, outdoor and often overnight, so the crew needs hi-vis to stay visible on a busy, dark site around vehicles and moving kit, fleeces and waterproofs for cold nights and wet fields, cargo trousers for tools and safety boots for the heavy work of rigging and staging. And it has to handle a very seasonal calendar and a big festival-season intake, kitting a wave of crew and front-of-house staff quickly when the season starts.",
 "The second job is the crew. Stage, rigging and production work is physical, outdoor and often overnight, so the crew needs hi-vis for visibility on a busy, dark site near vehicles and moving kit, fleeces and waterproofs for cold nights and wet fields, cargo trousers for tools and safety boots for the heavy work of rigging and staging. And because the season brings a big intake, it has to kit a wave of crew and front-of-house staff quickly.",
 "The second is the crew. Stage, rigging and production work is physical, outdoor and often overnight, so the crew needs hi-vis to stay seen on a busy, dark site near vehicles and moving kit, fleeces and waterproofs for cold nights and wet fields, cargo trousers for tools and safety boots for the heavy work of rigging and staging. It also has to cope with a very seasonal calendar and a big festival-season intake of crew and front-of-house staff.",
]
CON_P3_POOL=[
 'The value is one supplier covering both halves of the operation, the front-of-house team and the crew, all branded the same. We hold your {t} operator name, logo and sizes on file and supply polos, hi-vis, fleeces, waterproofs and safety boots together, so onboarding a new season reproduces the same branded look every time. Browse the range at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
 'The value is one supplier for both halves of the operation, the front-of-house team and the crew, all branded the same. We hold your {t} operator name, logo and sizes on file and supply polos, hi-vis, fleeces, waterproofs and safety boots together, so onboarding a new season reproduces the same branded look every time. Browse the range at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
 'The value is having one supplier cover both halves of the operation, the front-of-house team and the crew, branded the same. We keep your {t} operator name, logo and sizes on file and supply polos, hi-vis, fleeces, waterproofs and safety boots together, so each new season comes back the same branded look. Browse the range at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
 'The value is one supplier for the whole operation, front-of-house and crew together, all branded the same. We hold your {t} operator name, logo and sizes on file and supply polos, hi-vis, fleeces, waterproofs and safety boots as one, so onboarding a new season reproduces the same branded look every time. Browse the range at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
]
ACC_HEAD="Trade Accounts for Venues and Festivals, Direct Online for Crews"
ACC_P1_POOL=[
 "Entertainment and events splits into two kinds of buyer, and we have built ordering for both. For a large venue, festival or production company with a big seasonal crew, a trade account is the practical route. It adds managed reordering, agreed pricing and a held kit list with your branding and sizes on file, so onboarding a whole season's crew and front-of-house staff, taking on extra hands for a busy festival weekend or kitting a second site is fast and consistent for a {t} operator. Send your headcount, your logo and your sizes and we will build the branded kit list and hold it.",
 "Entertainment and events has two kinds of buyer, and ordering is built for both. For a large {t} venue, festival or production company with a big seasonal crew, a trade account is the practical route: managed reordering, agreed pricing and a held kit list with your branding and sizes on file, so onboarding a season's crew and front-of-house staff, taking on festival-weekend hands or kitting a second site is fast and consistent. Send your headcount, logo and sizes and we will build the branded kit list and hold it.",
 "This trade splits into two kinds of buyer, and we have built ordering for both. For a large venue, festival or production company with a big seasonal crew in {t}, a trade account is the practical route, adding managed reordering, agreed pricing and a held kit list with your branding and sizes on file, so onboarding a season's crew or kitting a second site stays fast and consistent. Send your headcount, logo and sizes and we will build and hold the list.",
 "Entertainment and events splits into two kinds of buyer, and ordering suits both. For a large {t} venue or festival running a big seasonal crew, a trade account is the practical route: managed reordering, agreed pricing and a held kit list with your branding and sizes on file, so onboarding a season's crew and front-of-house staff, taking on festival-weekend hands or kitting a second site is fast and consistent. Send your headcount, logo and sizes and we build the branded kit list and hold it.",
]
ACC_P2_POOL=[
 "For an independent event crew, promoter or entertainer, ordering direct online is quickest and needs no account at all. Browse the range, pick your polos, hi-vis, fleeces, waterproofs and safety boots, choose your sizes, send your logo once and check out. There is nothing to set up, your kit is dispatched on standard lead times with embroidery added in-house, and your logo is held on file so the next order matches.",
 "For an independent event crew, promoter or entertainer, direct online is quickest and needs no account: browse the range, pick your polos, hi-vis, fleeces, waterproofs and safety boots, choose sizes, send your logo once and check out. Nothing to set up, dispatched on standard lead times with embroidery in-house, and your logo held on file so the next order matches.",
 "An independent event crew, promoter or entertainer orders quickest direct online, no account needed: browse the range, pick your polos, hi-vis, fleeces, waterproofs and safety boots, add sizes, send the logo once and check out. Nothing to set up, dispatched on standard lead times with in-house embroidery, and your logo held on file for the next order.",
 "For an independent crew, promoter or entertainer, the quickest route is direct online with no account: browse, pick your polos, hi-vis, fleeces, waterproofs and safety boots, choose sizes, send your logo once and check out, with nothing to set up, dispatched on standard lead times with embroidery in-house and your logo held on file.",
]
ACC_P3_POOL=[
 "Both routes are branded in-house from the same supplier, so whether you are kitting two hundred seasonal crew and front-of-house staff in {t} or just a handful of crew, the workwear is consistent, professional and ready for the season. Most large operators run the trade account centrally and point smaller crews and contractors at the direct online route, and everyone ends up matching.",
 "Both routes are branded in-house by the same supplier, so whether you are kitting two hundred {t} seasonal crew and front-of-house staff or just a handful of crew, the kit is consistent, professional and ready for the season. Most large operators use the trade account centrally and send smaller crews and contractors to the direct online route, and everyone matches.",
 "Both routes come branded in-house from one supplier, so whether it is two hundred seasonal crew across {t} or just a few crew, the workwear is consistent, professional and ready for the season. Most large operators run a trade account centrally and point smaller crews and contractors at direct online, and the whole operation matches.",
 "Both routes are branded in-house by one supplier, so whether you kit two hundred seasonal crew and front-of-house staff in {t} or only a handful of crew, the kit stays consistent, professional and ready for the season. Most large operators keep the trade account central and send smaller crews and contractors direct online, and everyone ends up matching.",
]
ACC_P4_POOL=[
 'Set up a trade account for a venue or festival at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>, or order direct online with no account at <a href="https://www.ineedworkwear.com">iNeedWorkwear</a>.',
 'Set up a trade account for a venue or festival at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>. For an independent crew, order direct online with no account at <a href="https://www.ineedworkwear.com">iNeedWorkwear</a>.',
 'Open a trade account for a venue or festival at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>, or order direct online with no account as an independent crew at <a href="https://www.ineedworkwear.com">iNeedWorkwear</a>.',
 'Set up a venue or festival trade account at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>, or as an independent crew order direct online with no account at <a href="https://www.ineedworkwear.com">iNeedWorkwear</a>.',
]
WHY_P1_POOL=[
 "An event or festival operator in {t} whose front-of-house team turns out in clean, branded polos and whose crew is in matching hi-vis and fleeces looks professional and organised to every guest, and iNeedWorkwear supplies that whole look from a single place, branded in-house, on a trade account for the big venue or direct online for the independent crew, so staff are identifiable and the operation is consistent from the front gate to the stage.",
 "A {t} event or festival operator whose front-of-house team wears clean, branded polos and whose crew is in matching hi-vis and fleeces looks professional and organised to every guest, and iNeedWorkwear supplies that whole look from one place, branded in-house, on a trade account for the big venue or direct online for the independent crew, so staff are identifiable from the front gate to the stage.",
 "When a {t} event or festival operator turns its front-of-house team out in clean, branded polos and its crew in matching hi-vis and fleeces, it looks professional and organised to every guest, and we supply that whole look from a single place, branded in-house, on a trade account or direct online, so staff are identifiable and the operation is consistent from the front gate to the stage.",
 "An event or festival operator in {t} whose front-of-house wears clean, branded polos and whose crew is in matching hi-vis reads as professional and organised to every guest, and we supply that whole look from one place, branded in-house, on a trade account for the big venue or direct online for the independent crew, so staff are identifiable from the gate to the stage.",
 "A {t} event or festival operator whose front-of-house turns out in clean, branded polos and whose crew is in matching hi-vis and fleeces looks organised and professional to every guest, and we supply the whole look from one place, branded in-house, trade or direct, so even a small independent crew presents like a major venue.",
 "In {t}, an event or festival operator whose front-of-house wears clean, branded polos and whose crew is in matching hi-vis looks professional from the first glance at the gate, and iNeedWorkwear supplies that whole look from one place, branded in-house, on a trade account for the big venue or direct online for the independent crew.",
]
WHY_P2_POOL=[
 "It is built for both halves of the operation and for the season. A large venue or festival onboarding a wave of seasonal crew and front-of-house staff gets managed reordering and a held kit list, while a small independent crew gets a quick, no-account direct route online, and both come back the same branded kit, so a growing operation never ends up with a patchwork of mismatched workwear as it scales or restocks each year.",
 "It is built for both halves of the operation and for the season. A large venue or festival onboarding seasonal crew and front-of-house staff gets managed reordering and a held kit list, and a small independent crew gets a quick, no-account direct route online, with both coming back the same branded kit, so a growing operation avoids a patchwork of mismatched workwear as it scales or restocks each year.",
 "It works for both halves of the operation and for the season. A large venue or festival onboarding seasonal crew gets managed reordering and a held kit list, while a small independent crew gets a quick, no-account online route, and both return the same branded kit, so a scaling operation never drifts into mismatched workwear year on year.",
 "It suits both halves of the operation and the season. A large venue or festival onboarding a wave of seasonal crew and front-of-house staff gets managed reordering and a held kit list, a small independent crew gets a fast no-account online route, and both come back the same branded kit, so a growing operation never ends up with mismatched workwear as it restocks each year.",
 "It is made for both halves of the operation and for the season. The large venue or festival gets managed reordering and a held kit list for onboarding seasonal crew, the small independent crew gets a quick no-account online route, and both return the same branded kit, so scaling or restocking never means a patchwork of mismatched workwear.",
 "It covers both halves of the operation and the season. A large venue or festival onboarding seasonal crew leans on managed reordering and a held kit list, a small independent crew uses the quick no-account online route, and both come back the same branded kit, so a growing operation stays matched year on year.",
]
WHY_P3_POOL=[
 "The range covers what the work demands on both sides: polos for the front-of-house team, and hi-vis, fleeces, waterproofs, cargo trousers and safety boots for the crew. It is a focused, practical range, so choosing, ordering and reordering stay quick for a busy operator in the run-up to a season or a single big event.",
 "The range covers what the work really demands on both sides: polos for the front-of-house team, and hi-vis, fleeces, waterproofs, cargo trousers and safety boots for the crew. It is focused and practical, so choosing, ordering and reordering stay quick for a busy operator in the run-up to a season or a single big event.",
 "Everything in the range reflects what the work demands on both sides: polos for the front-of-house team, and hi-vis, fleeces, waterproofs, cargo trousers and safety boots for the crew. The range is focused and practical, so ordering and reordering stay quick for a busy operator before a season or a big event.",
 "The range is built around what the work demands on both sides: polos for the front-of-house team, and hi-vis, fleeces, waterproofs, cargo trousers and safety boots for the crew, so choosing and reordering stay quick for a busy operator in the run-up to a season or a single big event.",
 "It is a focused, practical range mapped to the work on both sides: polos for the front-of-house team, and hi-vis, fleeces, waterproofs, cargo trousers and safety boots for the crew, which keeps choosing, ordering and reordering fast for a busy operator each season.",
 "The range stays focused on what the work needs on both sides: polos for the front-of-house team, and hi-vis, fleeces, waterproofs, cargo trousers and safety boots for the crew, so a busy operator can choose and reorder in minutes before a season or a big event.",
]
WHY_P4_POOL=[
 "And everything is branded in-house, with your operator name and logo embroidered under our control and held on file, ready for the next order, the next starter or the next season, so every piece matches what the team already wears and a new seasonal hire looks the part from their first shift.",
 "And everything is branded in-house, your operator name and logo embroidered under our control and held on file, ready for the next order, starter or season, so every piece matches what the team already wears and a new seasonal hire looks the part from day one.",
 "And it is all branded in-house, with your operator name and logo embroidered under our control and kept on file, ready for the next order, the next starter or the next season, so every piece matches the team and a new seasonal hire looks right from their first shift.",
 "And everything is branded in-house, your operator name and logo embroidered under our control and held on file for the next order, starter or season, so each piece matches what the team wears and a new seasonal hire looks the part from their first shift.",
 "And the whole lot is branded in-house, with your name and logo embroidered under our control and held on file, ready for the next order, starter or season, so every piece matches the team and a new seasonal hire looks established from day one.",
 "And it is all branded in-house, your operator name and logo embroidered under our control and on file, ready for the next order, the next starter or the next season, so every piece lines up with what the team already wears and a new seasonal hire looks the part immediately.",
]
ORD_P1_POOL=[
 "iNeedWorkwear supplies branded polos, hi-vis, fleeces, waterproofs and safety boots to concert venues, festival operators, event production companies, theatres and independent event crews across {region}, all embroidered in-house with the operator name.",
 "We supply branded polos, hi-vis, fleeces, waterproofs and safety boots to concert venues, festival operators, production companies, theatres and independent event crews across {region}, all embroidered in-house with the operator name.",
 "Across {region}, iNeedWorkwear kits concert venues, festival operators, production companies, theatres and event crews in branded polos, hi-vis, fleeces, waterproofs and safety boots, all embroidered in-house with the operator name.",
 "From a single crew to a major festival across {region}, iNeedWorkwear supplies branded polos, hi-vis, fleeces, waterproofs and safety boots to venues, festivals and event crews, all embroidered in-house.",
]
ORD_P2_POOL=[
 "For an independent event crew, promoter or entertainer, ordering direct online is quickest and needs no account: browse the range, pick your polos, hi-vis, fleeces, waterproofs and safety boots, add your sizes, send your logo once and check out. Your kit is dispatched on standard lead times with embroidery added in-house, and your logo is held on file so the next order matches.",
 "For an independent event crew, promoter or entertainer, direct online is quickest and needs no account: browse, pick your polos, hi-vis, fleeces, waterproofs and safety boots, add sizes, send your logo once and check out. Your kit ships on standard lead times with embroidery in-house, and your logo is held on file so the next order matches.",
 "An independent event crew, promoter or entertainer orders quickest direct online, no account needed: browse the range, pick your polos, hi-vis, fleeces, waterproofs and safety boots, add sizes, send the logo once and check out. Kit is dispatched on standard lead times with in-house embroidery, and your logo is held on file for the next order.",
 "For an independent crew or promoter, the quickest route is direct online with no account: browse the range, pick your polos, hi-vis, fleeces, waterproofs and safety boots, add your sizes, send your logo once and check out, dispatched on standard lead times with embroidery in-house and your logo held on file.",
]
ORD_P3_POOL=[
 "For a larger venue, festival or production company with a big seasonal crew, a trade account adds managed reordering and agreed pricing: send your headcount, your logo and your sizes and we will build a branded kit list and hold it on file, so each season's crew and front-of-house staff are onboarded in matching kit.",
 "For a larger venue, festival or production company with a big seasonal crew, a trade account brings managed reordering and agreed pricing: send your headcount, logo and sizes and we will build a branded kit list and hold it on file, so each season's crew and front-of-house staff are onboarded in matching kit.",
 "A larger venue, festival or production company with a big seasonal crew can use a trade account for managed reordering and agreed pricing: send your headcount, logo and sizes and we will build a branded kit list and hold it on file, so each season's crew onboard in matching kit.",
 "For a larger venue, festival or production company with a big seasonal crew, a trade account adds managed reordering and agreed pricing: send your headcount, logo and sizes and we will build a branded kit list and keep it on file, so each season's crew and front-of-house staff are onboarded in matching kit.",
]
SELF_POOL=[
 'Running a new event or festival and need kit now? Browse the full range, add your sizes and order direct on self-service checkout at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
 'Gearing up for a new season and need kit fast? Browse the range, add sizes and order direct on self-service checkout at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
 'Setting up a new crew, venue or festival and need kit today? Browse the full range, add your sizes and order direct on self-service checkout at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
 'Need crew and front-of-house kit sorted now? Browse the range, add sizes and order direct on self-service checkout at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
]
SORTED_POOL=[
 '<h3>Entertainment, Events and Festivals Workwear, Sorted</h3><p>From branded front-of-house polos to crew hi-vis, fleeces, waterproofs and safety boots, get workwear built for venues, festivals and event crews - embroidered in-house with your operator name, on a trade account or ordered direct online with no account.</p><p><a href="https://www.ineedworkwear.com">Browse entertainment, events and festivals workwear at iNeedWorkwear</a></p>',
 '<h3>Entertainment, Events and Festivals Workwear, Sorted</h3><p>Branded front-of-house polos, plus crew hi-vis, fleeces, waterproofs and safety boots - workwear for venues, festivals and event crews, embroidered in-house with your operator name, on a trade account or ordered direct online.</p><p><a href="https://www.ineedworkwear.com">Browse entertainment, events and festivals workwear at iNeedWorkwear</a></p>',
 '<h3>Entertainment, Events and Festivals Workwear, Sorted</h3><p>From front-of-house polos to crew hi-vis, fleeces, waterproofs and safety boots, kit a major venue or a single independent crew, embroidered in-house and ordered on a trade account or direct online with no account.</p><p><a href="https://www.ineedworkwear.com">Browse entertainment, events and festivals workwear at iNeedWorkwear</a></p>',
 '<h3>Entertainment, Events and Festivals Workwear, Sorted</h3><p>Polos, hi-vis, fleeces, waterproofs and safety boots, the season-ready kit for venues, festivals and event crews, embroidered in-house and ready on a trade account for the venue or direct online for the crew.</p><p><a href="https://www.ineedworkwear.com">Browse entertainment, events and festivals workwear at iNeedWorkwear</a></p>',
]
OWNER_POOL=[
 "And that trade runs at every size, which shapes what a workwear supplier has to do. Major venues, festival operators and production companies run big crews and large seasonal teams and buy through procurement, while independent event crews, promoters, mobile entertainers and one-van operators need just a few branded pieces. A supplier here has to serve the big festival and the single crew alike, with both a managed account and a quick direct route.",
 "And that trade runs at every size, which shapes the supplier's job. Major venues, festival operators and production companies run big crews and large seasonal teams and buy through procurement, while independent event crews, promoters and entertainers want just a few branded pieces. A supplier here has to serve the big festival and the single crew alike, with a managed account and a quick direct route side by side.",
 "And that trade runs at every size, which shapes what a supplier needs to do. Major venues, festival operators and production companies run big crews and large seasonal teams and buy through procurement, while a wide layer of independent event crews, promoters and entertainers need only a few branded pieces. A supplier has to handle the big festival and the single crew alike, offering both a managed account and a fast direct route.",
 "And every size of operator is in the mix, which shapes the supplier's job. Major venues, festivals and production companies run big crews and seasonal teams through procurement, while independent event crews, promoters and entertainers pick up work and want a handful of branded pieces. A supplier has to serve the big festival and the single crew alike, with a managed account and a quick direct route both on offer.",
 "And the trade spans every size, which shapes what a supplier must do. Big venues, festival operators and production companies run large crews and seasonal teams and buy centrally, while independent event crews, promoters and entertainers need just a few branded pieces. A supplier has to look after the big festival and the single crew alike, with both a managed account and a quick direct route.",
 "And it runs on operators of every size, which shapes the supplier's job. Major venues, festivals and production companies field big crews and seasonal teams and buy through procurement, while a deep layer of independent event crews, promoters and entertainers want only a few branded pieces. A supplier has to cover the big festival and the single crew alike, with a managed account and a quick direct route both available.",
]
PRESENT_POOL=[
 "And the kit splits two ways, which is what makes event workwear its own thing. Front-of-house staff, the stewards, bar, box office and hospitality teams, need branded polos so the audience at a busy {t} event can see at a glance who is official and who to ask. The crew, riggers and production teams need hi-vis, fleeces, waterproofs, cargo trousers and safety boots for the physical, outdoor, often overnight work of the get-in, the show and the breakdown.",
 "And the kit splits two ways, which is what sets event workwear apart. Front-of-house staff, the stewards, bar, box office and hospitality teams, need branded polos so the audience at a busy {t} event can see at a glance who is official and who to ask. The crew, riggers and production teams need hi-vis, fleeces, waterproofs, cargo trousers and safety boots for the physical, outdoor, often overnight work of the get-in, the show and the breakdown.",
 "And the kit has to split two ways, which is the heart of event workwear. Front-of-house staff, the stewards, bar, box office and hospitality teams, need branded polos so the audience at a busy {t} event can see at a glance who is official and who to ask. The crew, riggers and production teams need hi-vis, fleeces, waterproofs, cargo trousers and safety boots for the physical, outdoor, often overnight work of the get-in and breakdown.",
 "And the kit works two ways at once, which is what makes this workwear distinct. Front-of-house staff, the stewards, bar, box office and hospitality teams, need branded polos so the audience at a busy {t} event can see who is official and who to ask. The crew, riggers and production teams need hi-vis, fleeces, waterproofs, cargo trousers and safety boots for the physical, outdoor, often overnight work of the get-in and breakdown.",
 "And the kit pulls two ways at once, which is what makes event workwear its own thing. Front-of-house staff, the stewards, bar, box office and hospitality teams, need branded polos so the audience at a busy {t} event can spot who is official and who to ask. The crew, riggers and production teams need hi-vis, fleeces, waterproofs, cargo trousers and safety boots for the physical, outdoor, often overnight work of the get-in and breakdown.",
 "And the kit covers two jobs at once, which is what distinguishes event workwear. Front-of-house staff, the stewards, bar, box office and hospitality teams, need branded polos so the audience at a busy {t} event can see at a glance who is official and who to ask. The crew, riggers and production teams need hi-vis, fleeces, waterproofs, cargo trousers and safety boots for the physical, outdoor, often overnight get-in and breakdown.",
]
NARROW_POOL=[
 "Because events and festivals are very seasonal, it is a repeat-purchase trade with a big intake each year, and the range is built to reorder easily. Polos, hi-vis, fleeces, waterproofs and safety boots, branded in-house with the operator name, are the whole kit, and we hold your logo on file so the next season's crew and the next new starter in {t} match what the team already wears.",
 "Because events and festivals are very seasonal, this is a repeat-purchase trade with a big intake each year, and the range is built to reorder easily. Polos, hi-vis, fleeces, waterproofs and safety boots, branded in-house with the operator name, are the whole kit, and your logo is held on file so the next season's crew and the next new starter in {t} match what the team already wears.",
 "Since events and festivals are very seasonal, it is a repeat-purchase trade with a big yearly intake, and the range is built to reorder easily. Polos, hi-vis, fleeces, waterproofs and safety boots, branded in-house with the operator name, are the whole kit, and we keep your logo on file so the next season's crew and the next new starter in {t} match what the team already wears.",
 "Because the trade is very seasonal, it is a repeat-purchase one with a big intake each year, and the range reorders easily. Polos, hi-vis, fleeces, waterproofs and safety boots, branded in-house with the operator name, are the whole kit, and your logo sits on file so the next season's crew and the next new starter in {t} match what the team already wears.",
 "As events and festivals are very seasonal, it is a repeat-purchase trade with a big intake each year, and the range is built to reorder fast. Polos, hi-vis, fleeces, waterproofs and safety boots, branded in-house with the operator name, are the whole kit, and we hold your logo on file so the next season's crew and the next new starter in {t} match what the team already runs.",
 "Because events and festivals run on a seasonal intake, it is a repeat-purchase trade, and the range is built for easy reordering. Polos, hi-vis, fleeces, waterproofs and safety boots, branded in-house with the operator name, are the whole kit, and your logo is on file so the next season's crew and the next new starter in {t} line up with what the team already wears.",
]
KIT_POOL=[
 "Polos, hi-vis, fleeces, waterproofs and safety boots, branded with the operator name, are the whole kit {loc}.",
 "The whole kit is polos, hi-vis, fleeces, waterproofs and safety boots, branded with the operator name {loc}.",
 "Polos, hi-vis, fleeces, waterproofs and safety boots do the job, branded with the operator name {loc}.",
 "It comes down to polos, hi-vis, fleeces, waterproofs and safety boots, branded with the operator name {loc}.",
 "Polos, hi-vis, fleeces, waterproofs and safety boots, all branded with the operator name, are the kit {loc}.",
 "Branded polos, hi-vis, fleeces, waterproofs and safety boots make up the whole kit {loc}.",
]
S2TAIL_POOL=[
 ", polos lead front-of-house, with hi-vis, fleeces and safety boots for the crew.",
 ", the core is polos for front-of-house, with hi-vis, fleeces and safety boots for the crew.",
 ", expect polos for front-of-house, then hi-vis, fleeces and safety boots for the crew.",
 ", polos cover front-of-house, with hi-vis, fleeces and safety boots for the crew.",
 ", polos anchor front-of-house, with hi-vis, fleeces and safety boots completing the crew kit.",
 ", it is polos for front-of-house, plus hi-vis, fleeces and safety boots for the crew.",
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
     (f"Do you supply branded workwear to venues, festivals and event crews in {t}?", P('fq1',[
      f"Yes. Concert venues, festival operators, event production companies, theatres and independent event crews across {region} get branded polos, hi-vis, fleeces, waterproofs and safety boots from us, embroidered in-house with the operator name. A large venue or festival can run a trade account for managed reordering and seasonal intake, and a small crew or promoter can order direct online with no account.",
      f"Yes. Branded polos, hi-vis, fleeces, waterproofs and safety boots go to concert venues, festival operators, production companies, theatres and independent event crews across {region}, embroidered in-house with the operator name. A large venue or festival runs a trade account for managed reordering and seasonal intake, and a small crew orders direct online with no account.",
      f"Yes. From a single crew to a major festival across {region}, we supply branded polos, hi-vis, fleeces, waterproofs and safety boots, embroidered in-house with the operator name, on a trade account for the venue or direct online with no account.",
      f"Yes. Concert venues, festival operators, production companies and event crews across {region} get branded polos, hi-vis, fleeces, waterproofs and safety boots from us, embroidered in-house with the operator name, on a trade account or ordered direct online.",
      f"Yes. Across {region} we kit concert venues, festival operators, production companies and event crews in branded polos, hi-vis, fleeces, waterproofs and safety boots, embroidered in-house with the operator name, on a trade account or direct online for an independent crew.",
      f"Yes. Event and festival operators across {region}, from a single crew to a major venue, get branded polos, hi-vis, fleeces, waterproofs and safety boots from us, embroidered in-house with the operator name, on a trade account or direct online with no account."])),
     ("Can you kit both front-of-house staff and the production crew?", P('fq2',[
      "Yes. Front-of-house staff such as stewards, bar, box office and hospitality get branded polos so the public can identify who is official, while the stage crew, riggers and production team get hi-vis, fleeces, waterproofs, cargo trousers and safety boots for the physical, outdoor, often overnight work of the get-in and breakdown. Both are branded the same with the operator name, from one supplier.",
      "Yes. Front-of-house staff like stewards, bar, box office and hospitality get branded polos so the public can see who is official, while the crew, riggers and production team get hi-vis, fleeces, waterproofs, cargo trousers and safety boots for the physical, outdoor, often overnight work of the get-in and breakdown. Both are branded the same, from one supplier.",
      "Yes. The front-of-house team gets branded polos so the public can identify who is official, and the crew, riggers and production team get hi-vis, fleeces, waterproofs, cargo trousers and safety boots for the physical, outdoor, often overnight get-in and breakdown. Both halves are branded the same with the operator name, from one supplier.",
      "Yes. Stewards, bar, box office and hospitality get branded polos so the public can identify who is official, while stage crew, riggers and production get hi-vis, fleeces, waterproofs, cargo trousers and safety boots for the physical, outdoor, often overnight work of the get-in and breakdown, all from one supplier and branded the same.",
      "Yes. We kit the front-of-house team in branded polos so the public can see who is official, and the crew, riggers and production team in hi-vis, fleeces, waterproofs, cargo trousers and safety boots for the heavy, outdoor, often overnight get-in and breakdown, both branded the same with the operator name.",
      "Yes. Front-of-house staff get branded polos so the audience can identify who is official, while the crew, riggers and production team get hi-vis, fleeces, waterproofs, cargo trousers and safety boots for the physical, outdoor, often overnight get-in and breakdown, all from one supplier."])),
     ("Can you handle a large seasonal festival crew intake?", P('fq3',[
      "Yes. Events and festivals are very seasonal, so a large venue, festival or production company can run a trade account with managed reordering, agreed pricing and a held kit list, and we onboard a whole season's crew and front-of-house staff in matching branded kit on standard lead times. We hold your logo and sizes on file, so each season and each new starter comes back the same.",
      "Yes. As events and festivals are very seasonal, a large venue, festival or production company can run a trade account with managed reordering, agreed pricing and a held kit list, and we onboard a season's crew and front-of-house staff in matching branded kit on standard lead times. Your logo and sizes are held on file, so each season and each new starter comes back the same.",
      "Yes. A large venue, festival or production company can run a trade account with managed reordering, agreed pricing and a held kit list, so a whole season's crew and front-of-house staff are onboarded in matching branded kit on standard lead times. We hold your logo and sizes on file, so each new season and each new starter matches.",
      "Yes. The trade is very seasonal, so a large venue, festival or production company runs a trade account with managed reordering, agreed pricing and a held kit list, and we onboard a season's crew and front-of-house staff in matching branded kit on standard lead times, with your logo and sizes held on file so each season matches.",
      "Yes. A large venue, festival or production company can run a trade account with managed reordering and a held kit list to onboard a whole season's crew and front-of-house staff in matching kit on standard lead times, with your logo and sizes on file so each new season and each new starter comes back the same.",
      "Yes. Events and festivals run on a seasonal intake, so a large venue or festival uses a trade account with managed reordering, agreed pricing and a held kit list, and we onboard a season's crew and front-of-house staff in matching branded kit on standard lead times, with logo and sizes held on file."])),
     ("Why does branding matter for front-of-house event staff?", P('fq4',[
      "At a busy event the audience needs to see at a glance who is staff, so a branded polo makes stewards, bar, box office and hospitality instantly identifiable, which matters for trust, crowd management and safety. We embroider the operator name and logo in-house, turning everyday kit into a recognisable, professional uniform that even a casual or seasonal hire wears from their first shift.",
      "At a busy event the audience needs to spot at a glance who is staff, so a branded polo makes stewards, bar, box office and hospitality instantly identifiable, which matters for trust, crowd management and safety. We embroider the operator name and logo in-house, turning everyday kit into a recognisable uniform that even a casual or seasonal hire wears from day one.",
      "Because the audience needs to see at a glance who is staff at a busy event, a branded polo makes stewards, bar, box office and hospitality instantly identifiable, which matters for trust, crowd management and safety. The operator name and logo are embroidered in-house, turning everyday kit into a recognisable, professional uniform.",
      "At a busy event the audience needs to find someone official quickly, so a branded polo makes stewards, bar, box office and hospitality instantly identifiable, which matters for trust, crowd management and safety. We embroider the operator name and logo in-house, turning everyday kit into a professional, recognisable uniform from a hire's first shift.",
      "Front-of-house staff are the event made visible, so a branded polo makes stewards, bar, box office and hospitality instantly identifiable to the audience, which matters for trust, crowd management and safety. We embroider the operator name and logo in-house, turning everyday kit into a recognisable, professional uniform.",
      "Since the audience needs to see who is staff at a busy event, a branded polo makes stewards, bar, box office and hospitality instantly identifiable, which matters for trust, crowd management and safety. The operator name and logo are embroidered in-house, turning everyday kit into a recognisable uniform a seasonal hire wears from day one."])),
     ("Do you supply hi-vis and safety boots for stage crew and rigging?", P('fq5',[
      "Yes. Stage crew, riggers and production teams get hi-vis vests and jackets for visibility on a busy site near vehicles and forklifts, fleeces and waterproofs for cold nights and wet fields, cargo trousers for tools and safety boots for the heavy, physical work of rigging and staging, all branded with the operator name.",
      "Yes. Stage crew, riggers and production teams get hi-vis vests and jackets for visibility on a busy site around vehicles and forklifts, fleeces and waterproofs for cold nights and wet fields, cargo trousers for tools and safety boots for the heavy work of rigging and staging, all branded with the operator name.",
      "Yes, the crew side is fully covered: hi-vis for visibility on a busy site near vehicles and forklifts, fleeces and waterproofs for cold nights and wet fields, cargo trousers for tools and safety boots for the heavy, physical work of rigging and staging, all branded with the operator name.",
      "Yes. Riggers, stage crew and production teams get hi-vis for visibility near vehicles and forklifts, fleeces and waterproofs for cold nights and wet fields, cargo trousers for tools and safety boots for the heavy work of rigging and staging, all branded with the operator name.",
      "Yes. The crew gets hi-vis vests and jackets for visibility on a busy, dark site near vehicles and forklifts, fleeces and waterproofs for cold nights and wet fields, cargo trousers for tools and safety boots for rigging and staging, all branded with the operator name.",
      "Yes. Stage crew, riggers and production get hi-vis for visibility near vehicles and forklifts, fleeces and waterproofs for cold nights and wet fields, cargo trousers for tools and safety boots for the heavy work of rigging and staging, all branded with the operator name."])),
     ("Can you embroider our venue, festival or crew name and logo?", P('fq6',[
      "Yes. We embroider your operator name and logo in-house onto polos, hi-vis, fleeces, waterproofs and caps, finished to survive heavy seasonal use and frequent washing. Send your artwork once, we hold it on file, and every reorder, new starter and new season matches, so a venue, a festival or a small independent crew looks consistent and professional.",
      "Yes. Your operator name and logo are embroidered in-house onto polos, hi-vis, fleeces, waterproofs and caps, finished for heavy seasonal use and frequent washing. Send artwork once and we hold it on file, so every reorder, new starter and new season matches, and a venue, festival or small crew looks consistent.",
      "Yes, all branding is done in-house onto polos, hi-vis, fleeces, waterproofs and caps, finished to survive heavy seasonal use and washing. We hold your artwork on file, so every reorder, new starter and new season matches and a venue, festival or small independent crew looks consistent and professional.",
      "Yes. Send your artwork once and we embroider your operator name and logo in-house onto polos, hi-vis, fleeces, waterproofs and caps, holding it on file so every reorder, new starter and new season matches, and a venue, festival or small crew looks consistent and professional.",
      "Yes. Operator name and logo are embroidered in-house onto polos, hi-vis, fleeces, waterproofs and caps, finished for heavy seasonal use and washing and held on file, so every reorder, new starter and new season matches and a venue, festival or small crew stays consistent.",
      "Yes, embroidery is done in-house onto polos, hi-vis, fleeces, waterproofs and caps, finished to take heavy seasonal use and washing. Send your logo once and we keep it on file, so reorders, new starters and new seasons line up and a venue, festival or small crew looks professional."])),
     ("How quickly can you supply event and festival workwear?", P('fq7',[
      "Order direct online and your kit is dispatched on standard lead times, with embroidery added in-house before it ships. For a large venue, festival or production company on a trade account, send your headcount, your logo and your sizes and we will build a branded kit list and hold it on file, so each season's crew and front-of-house staff are onboarded in matching kit on standard lead times.",
      "Order direct online and your kit ships on standard lead times, with embroidery added in-house first. For a large venue, festival or production company on a trade account, send your headcount, logo and sizes and we will build a branded kit list and hold it on file, so each season's crew onboard in matching kit on standard lead times.",
      "Order direct online and we dispatch on standard lead times, embroidery added in-house before shipping. For a venue or festival on a trade account, send your headcount, logo and sizes and we will build a branded kit list and hold it on file for fast seasonal onboarding and reordering.",
      "Order direct online and your kit is dispatched on standard lead times with embroidery done in-house first. For a large venue, festival or production company on a trade account, send your headcount, logo and sizes and we will build a branded kit list and hold it on file, so each season's crew onboard in matching kit.",
      "Order online and we dispatch on standard lead times with embroidery added in-house beforehand. A large venue, festival or production company on a trade account can send headcount, logo and sizes for a branded kit list held on file, so each season's crew and front-of-house staff onboard in matching kit fast.",
      "Order direct online and your kit ships on standard lead times, embroidered in-house first. For a large venue, festival or production company on a trade account, send your headcount, logo and sizes and we will build a branded kit list and keep it on file for quick seasonal onboarding on standard lead times."])),
    ]

TOWNS = {
 "birmingham": {
  "region":"Birmingham and the West Midlands",
  "nearby":["Solihull","West Bromwich","Walsall"],
  "snapshot":"iNeedWorkwear supplies branded polos, hi-vis, fleeces, waterproofs and safety boots to concert venues, festival operators, event production companies, theatres and independent event crews across Birmingham, embroidered in-house with the operator name. The trade runs from big arenas and festivals with large seasonal crews to small independent crews and promoters, so a larger operator can run a trade account for managed reordering and seasonal intake, while a small crew can order direct online with no account.",
  "s1_head":"Kitting the events capital of the Midlands",
  "s1loc":[
   "Birmingham is the Midlands' events capital. The canal-side Utilita Arena and bp pulse LIVE at the NEC handle the big arena tours, Symphony Hall hosts the City of Birmingham Symphony Orchestra, the O2 Academy and O2 Institute anchor the Digbeth music quarter, and the Hippodrome runs as the busiest single theatre in the UK, while open-air festivals like MADE in Birmingham at Luna Springs and the Mostly Jazz, Funk and Soul Festival at Moseley Park fill the summer.",
   "And the trade runs at every size. Major venues, arenas, festival operators and production companies run big crews and large seasonal teams and buy through procurement, while independent event crews, promoters and entertainers around Digbeth and the wider city need just a few branded pieces. A workwear supplier here has to serve the big festival and the single crew alike, which is why we run trade accounts and direct online ordering side by side.",
  ],
  "kit_loc":"across the city's venues, festivals and events",
  "s2_intro":"Whether you are a major Birmingham arena or festival, a production company or a small independent event crew in Digbeth",
 },
 "leeds": {
  "region":"Leeds and West Yorkshire",
  "nearby":["Bradford","Pudsey","Dewsbury"],
  "snapshot":"iNeedWorkwear supplies branded polos, hi-vis, fleeces, waterproofs and safety boots to concert venues, festival operators, event production companies, theatres and independent event crews across Leeds, embroidered in-house with the operator name. The trade runs from big arenas and festivals with large seasonal crews to small independent crews and promoters, so a larger operator can run a trade account for managed reordering and seasonal intake, while a small crew can order direct online with no account.",
  "s1_head":"Kitting the events trade of Yorkshire",
  "s1loc":[
   "Leeds is one of the best cities in the UK for live music and events. The First Direct Arena pulls in the big touring acts, the O2 Academy fills the Grade I listed former Coliseum, and grassroots rooms like the Brudenell Social Club and Belgrave Music Hall keep the scene alive, alongside the theatres and Leeds Town Hall, while the huge Leeds Festival takes over Bramham Park every August bank holiday and Slam Dunk and the city-wide Live at Leeds run through the year.",
   "And the trade runs the full range of sizes. Big arenas, festival operators and production companies run large crews and seasonal teams and buy centrally, while independent event crews, promoters and entertainers across the city need just a few branded pieces. A workwear supplier has to kit the big festival and the single crew alike, which is why we run trade accounts and direct online ordering side by side.",
  ],
  "kit_loc":"across the city's venues, festivals and events",
  "s2_intro":"Whether you are a major Leeds arena or festival, a production company or a small independent event crew toward Pudsey",
 },
}

_CSV=None
def _load_csv():
    global _CSV
    if _CSV is not None: return _CSV
    here=os.path.dirname(os.path.abspath(__file__))
    for p in (os.path.join(here,'EV_towns.csv'),'EV_towns.csv','/mnt/user-data/outputs/EV_towns.csv'):
        if os.path.exists(p):
            rows=[]
            with open(p,newline='',encoding='utf-8-sig') as f:
                for r in csv.DictReader(f): rows.append((int(r["Rank"]), r["Town"].strip(), (r.get("Nation") or "").strip()))
            _CSV=rows; return _CSV
    _CSV=[]; return _CSV

def slugify(name):
    return re.sub(r'-+','-', re.sub(r"[^a-z0-9]+","-", name.lower().replace("&"," and "))).strip('-')

# --- canonical display names (CSV is the source of truth) -------------------
_DISPLAY=None
def town_display(key):
    """Canonical CSV spelling for a town key/slug. Naive capitalize() mangles
    particle/hyphen towns (Newcastle upon Tyne, Weston-super-Mare); the CSV holds
    the correct casing, so resolve by slug and fall back to capitalize()."""
    global _DISPLAY
    if _DISPLAY is None:
        _DISPLAY={slugify(name): name for _r,name,_n in _load_csv()}
    return _DISPLAY.get(slugify(key), ' '.join(w.capitalize() for w in str(key).split()))

def _entry(town):
    """Slug-robust TOWNS lookup so any key spelling (display or slug) resolves."""
    s=slugify(town)
    if town.lower() in TOWNS: return TOWNS[town.lower()]
    for k,v in TOWNS.items():
        if slugify(k)==s: return v
    raise KeyError(town)

def _load_extra_towns():
    """Merge per-batch towns/*.json into TOWNS. The seed (London/Birmingham/Leeds)
    stays inline; every other batch ships as a committed JSON file so agent output
    never enters the build's context and per-batch commits stay clean."""
    here=os.path.dirname(os.path.abspath(__file__))
    for f in sorted(glob.glob(os.path.join(here,'towns','*.json'))):
        try:
            data=json.load(open(f,encoding='utf-8'))
        except Exception as e:
            sys.exit(f"ERROR: bad town JSON {f}: {e}")
        for k,v in data.items():
            TOWNS[k.lower()]=v
_load_extra_towns()

def require_nearby(town, T):
    nb = T.get("nearby")
    if not nb or len(nb) < 3:
        raise ValueError(f"{town}: 'nearby' must list 3 geographically-close towns "
                         f"(web-verified, all on EV_towns.csv). No rank/auto fallback.")
    bad = [n for n in nb if not any(r[1].lower()==n.lower() for r in _load_csv())]
    if bad:
        raise ValueError(f"{town}: nearby town(s) not on EV_towns.csv: {bad}")
    return nb[:3]

def build_title(town):
    for t in (f"{town} Entertainment, Events and Festivals Workwear",
              f"{town} Events and Festivals Workwear", f"{town} Events Workwear"):
        if len(t) <= 60: return t
    return f"{town} Events Workwear"

def build_meta(town):
    for m in (f"Branded polos, hi-vis, fleeces, waterproofs and safety boots for {town} venues, festivals and event crews - front-of-house and crew.",
              f"Branded polos, hi-vis, fleeces and waterproofs for {town} venues, festivals and crews - front-of-house and crew, in-house embroidery.",
              f"Branded event and festival workwear for {town} venues and crews - polos, hi-vis, fleeces and safety boots, trade or direct online.",
              f"Branded workwear for {town} venues, festivals and event crews - polos, hi-vis, fleeces and safety boots, trade or direct."):
        if len(m) <= 160: return m
    return f"Branded event workwear for {town} venues and crews - polos, hi-vis, fleeces, safety boots, trade or direct."

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
        "name":f"Entertainment, Events and Festivals Workwear Supply and Embroidery in {town}",
        "serviceType":"Entertainment, events and festivals workwear and embroidery supply",
        "provider":{"@id":"https://www.ineedworkwear.com/#organization"},
        "areaServed":[{"@type":"City","name":town}]+[{"@type":"City","name":n} for n in nearby],
        "audience":{"@type":"BusinessAudience","name":"Event production companies, venues, festivals and event crews"},
        "description":f"Branded polos, hi-vis, fleeces, waterproofs and safety boots supplied to venues, festivals and event crews in {town}, on a trade account or direct online, with in-house embroidery.",
        "hasOfferCatalog":{"@type":"OfferCatalog","name":"Entertainment, Events and Festivals Workwear",
            "itemListElement":[{"@type":"Offer","itemOffered":{"@type":"Product","name":p}} for p in EV_PRODUCTS]}}
    crumb = {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Home","item":DOMAIN},
        {"@type":"ListItem","position":2,"name":"Entertainment, Events and Festivals Workwear","item":f"{DOMAIN}/entertainment-events-festivals-workwear"},
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

    emb_svg   = EMB.replace('a London event logo', f'a {town} event logo')
    # festival sign (signpost slot): swap aria, the big {town} text, and caption
    sign_svg  = SIGNPOST.replace('London music festival welcome sign', f'{town} music festival welcome sign')
    sign_svg  = re.sub(r'<text x="230" y="104".*?</text>', sign_town(town), sign_svg, flags=re.S)
    sign_svg  = sign_svg.replace('every London event', f'every {town} event')
    # premises (DJ stage slot): swap aria and caption
    prem_svg  = PREMISES.replace('serving event and festival crews across London', f'serving event and festival crews across {town}')
    prem_svg  = prem_svg.replace('serving crews across London', f'serving crews across {town}')

    H=[build_head(town, slug, faqs, nearby), HEADER]
    H.append(f'<div class="ev-hero"><div class="ev-wrap"><div class="ev-subtitle">Branded Workwear for Entertainment, Events and Festivals</div><h1>{town} Entertainment, Events and Festivals Workwear</h1></div></div>')
    H.append('<div class="ev-pulse"></div>')
    H.append(f'<div class="ev-trust-strip"><p>{trust}</p></div>')
    H.append(f'<div class="ev-wrap"><div class="ev-snapshot"><div class="ev-snapshot-label">Supplier Snapshot</div><p>{snap}</p></div></div>')
    H.append(STATS)
    H.append('<div class="ev-cta-bar"><a href="https://www.ineedworkwear.com" class="ev-cta-btn">Browse Entertainment, Events and Festivals Workwear</a></div>')
    H.append('<div class="ev-jump-links"><a href="#range">Workwear Range</a><a href="#contract">The Kit</a><a href="#accounts">Ordering and Accounts</a><a href="#order">How to Order</a></div>')
    H.append(GARMENT)
    H.append(f'<div class="ev-section"><div class="ev-wrap"><h2>{s1head}</h2>'+''.join(f'<p>{p}</p>' for p in s1ps)+'</div></div>')
    H.append(f'<div class="ev-section" id="range"><div class="ev-wrap"><h2>Entertainment, Events and Festivals Workwear Range</h2><p>{s2intro} <a href="https://www.ineedworkwear.com">Browse the full range at iNeedWorkwear.com</a>.</p><p class="ev-btn-center"><a href="https://www.ineedworkwear.com" class="ev-section-btn">Browse The Range</a></p>{grid}</div></div>')
    H.append(f'<div class="ev-section"><div class="ev-wrap"><h2>Branding for a Venue, a Festival or an Independent Event Crew</h2>'+''.join(f'<p>{p}</p>' for p in emb)+'</div></div>')
    H.append(emb_svg)
    H.append(f'<div class="ev-wrap"><div class="ev-contract" id="contract"><h3>{CON_HEAD}</h3>'+''.join(f'<p>{p}</p>' for p in con)+'</div></div>')
    H.append(sign_svg)
    H.append(f'<div class="ev-section" id="accounts"><div class="ev-wrap"><h2>{ACC_HEAD}</h2>'+''.join(f'<p>{p}</p>' for p in acc)+'</div></div>')
    H.append(prem_svg)
    H.append(f'<div class="ev-section"><div class="ev-wrap"><h2>Why Event and Festival Operators Choose iNeedWorkwear</h2>'+''.join(f'<p>{p}</p>' for p in why)+'</div></div>')
    H.append(ORDER)
    H.append(f'<div class="ev-section" id="order"><div class="ev-wrap"><h2>How to Order Entertainment, Events and Festivals Workwear</h2><p>{ordr[0]}</p><p>{ordr[1]}</p><p>{ordr[2]}</p><p class="ev-btn-center"><a href="https://www.ineedworkwear.com" class="ev-section-btn">Browse And Order Online</a></p><p>{selfp}</p>'+CONTACT+'</div></div>')
    faq_html=''.join(f'<div class="ev-faq-item"><div class="ev-faq-q">{q}</div><div class="ev-faq-a">{a}</div></div>' for q,a in faqs)
    H.append(f'<div class="ev-faq"><div class="ev-wrap"><h2>Entertainment, Events and Festivals Workwear FAQ</h2>{faq_html}</div></div>')
    H.append(f'<div class="ev-wrap"><div class="ev-workwear">{sorted_}</div></div>')
    nb_links=''.join(f'<a href="ev-{slugify(n)}.html">Entertainment, events and festivals workwear in {n}</a>\n' for n in nearby)
    H.append(f'<div class="ev-nearby"><div class="ev-wrap"><h3>Entertainment, Events and Festivals Workwear in Nearby Towns</h3><div class="ev-nearby-links">{nb_links}</div></div></div>')
    H.append(FOOTER+'\n</body></html>')
    return '\n'.join(H)

def main():
    args=[a for a in sys.argv[1:]]
    outdir=os.environ.get('EV_OUTDIR') or os.path.join(os.path.dirname(os.path.abspath(__file__)),'outputs')
    if not args:
        args=[t for t in TOWNS if t!='london']
    for town_key in args:
        tk=town_key.lower()
        if tk=='london': continue
        try:
            _entry(tk)
        except KeyError:
            print(f"SKIP {town_key}: not in TOWNS (must be web-researched first)"); continue
        town=town_display(tk)
        slug=f"ev-{slugify(town)}"
        html=assemble(slug, town)
        path=os.path.join(outdir, f"{slug}.html")
        open(path,'w',encoding='utf-8').write(html)
        print(f"WROTE {path}  ({len(html.split())} words approx)")

if __name__=='__main__':
    main()
