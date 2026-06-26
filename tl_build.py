#!/usr/bin/env python3
# TL (Travel, Tourism & Leisure) series builder v1.0 - read SPEC.md/CLAUDE.md
# HYBRID / audience BOTH, EQUAL weight: large attractions, theme parks and holiday
# parks with big SEASONAL teams (procurement / TRADE ACCOUNT, managed reordering,
# season onboarding) AND small independent activity centres, attractions and tour
# operators (DIRECT ONLINE, no account). SEASONAL is a driving flag.
# DIFFERENTIATOR = TWO JOBS: IDENTIFIABLE (staff are the face of the visitor
# experience - a branded polo makes them findable/approachable to guests) +
# ALL-WEATHER / SEASONAL (outdoor work across a long season: polo->fleece->softshell
# ->waterproof + outdoor hi-vis, plus a big seasonal intake to onboard fast).
# Lead = POLO + FLEECE + SOFTSHELL (softshell is TL core - NOT bleed here).
# MEDIUM depth, MEDIUM local variation (2 genuinely-local s1loc paras carry weight;
# generic shared paras live in OWNER/PRESENT/NARROW pools - see s1_paras). Headroom:
# cards pooled 3 ways (build_grid), FAQ/WHY/PRESENT/NARROW at 6 variants. No JS, no
# entities, no delivery claims. Exactly 14 .com + 1 community per page. Nearby =
# geographic, hand-authored, on TL_towns.csv. Prefix tl-.
import re, os, json, sys, csv
import hashlib
def pick(key, salt, n):
    h = hashlib.md5((salt + '|' + str(key).lower()).encode()).digest()
    return int.from_bytes(h[:4], 'big') % n

def _find_base():
    here = os.path.dirname(os.path.abspath(__file__))
    for p in (os.path.join(here,'tl-london.html'),'tl-london.html',
              '/mnt/user-data/outputs/tl-london.html','/home/claude/tlkit/tl-london.html'):
        if os.path.exists(p): return p
    sys.exit("ERROR: tl-london.html (base template) not found beside tl_build.py")

BASE = open(_find_base(), encoding='utf-8').read()
DOMAIN = 'https://www.ineedworkwear.uk'

def between(start, end, src=BASE):
    i = src.index(start); j = src.index(end, i+len(start)); return src[i:j]
def aria_block(aria):
    k = BASE.index(aria)
    i = BASE.rfind('<div class="tl-wrap"><div class="tl-illust">', 0, k)
    j = BASE.index('</div></div></div>', k) + len('</div></div></div>')
    return BASE[i:j]

CSS      = between('<style>', '</style>') + '</style>'
HEADER   = between('<div class="tl-header">', '\n<div class="tl-hero">')
STATS    = between('<div class="tl-stats">', '\n<div class="tl-cta-bar">')
GARMENT  = between('<div class="tl-wrap"><div class="tl-illust"><div class="tl-garment-row">', '\n<div class="tl-section">')
EMB      = aria_block('Embroidery machine stitching')
SIGNPOST = aria_block('tourism and attractions welcome sign')
PREMISES = aria_block('serving operators across')
ORDER    = aria_block('Order travel, tourism and leisure workwear online')
CONTACT  = BASE[BASE.index('<div class="tl-contact-block">'):
                BASE.index('</div></div></div>', BASE.index('<div class="tl-contact-block">'))+len('</div></div></div>')]
FOOTER   = BASE[BASE.index('<footer class="tl-footer">'):BASE.index('</footer>')+len('</footer>')]

def sign_town(town):
    n = len(town)
    size = 30 if n <= 9 else 26 if n <= 12 else 22 if n <= 16 else 18 if n <= 20 else 15
    tl = ' textLength="330" lengthAdjust="spacingAndGlyphs"' if n > 14 else ''
    return (f'<text x="230" y="120" text-anchor="middle" font-family="Arial,sans-serif" '
            f'font-weight="800" font-size="{size}" fill="#fff" letter-spacing="1"{tl}>{town.upper()}</text>')

TL_PRODUCTS = ["Polo Shirts and T-Shirts","Fleeces and Mid-Layers","Softshell Jackets",
 "Waterproofs and Outdoor Jackets","Hi-Vis for Outdoor and Events","Gilets and Bodywarmers",
 "Caps, Hats and Accessories","Embroidery, Names and ID Branding"]

def _card(n,d): return f'<div class="tl-product-card"><div class="tl-product-name">{n}</div><div class="tl-product-detail">{d}</div></div>'
CARD_DETAILS=[
 ("Polo Shirts and T-Shirts",[
   "Branded polos and t-shirts for everyday visitor-facing work, breathable and hard-wearing, the core layer that makes staff identifiable to guests across the season.",
   "Breathable, hard-wearing branded polos and t-shirts for the everyday, the core visitor-facing layer that makes staff identifiable and approachable to guests all season.",
   "Hard-wearing branded polos and t-shirts for day-to-day visitor-facing work, the dependable layer that marks staff out as identifiable and approachable to guests."]),
 ("Fleeces and Mid-Layers",[
   "Warm branded fleeces and mid-layers for cooler days and outdoor work, an easy layer over a polo when the weather turns on a park, attraction or activity site.",
   "Branded fleeces and mid-layers for cooler days and outdoor work, an easy warm layer over a polo when the weather turns on a park, attraction or activity site.",
   "Cosy branded fleeces and mid-layers for cool mornings and outdoor work, layered over a polo when it turns chilly at a park, attraction or activity centre."]),
 ("Softshell Jackets",[
   "Branded softshell jackets that block wind and light rain while staying easy to work in, the everyday outer layer for outdoor tourism and leisure staff most of the year.",
   "Branded softshells that cut wind and light rain yet stay easy to work in, the go-to outer layer for outdoor tourism and leisure staff across most of the year.",
   "Wind-and-shower-resistant branded softshell jackets that stay easy to move in, the everyday outdoor outer layer for tourism and leisure staff most of the year."]),
 ("Waterproofs and Outdoor Jackets",[
   "Waterproof jackets and trousers for the wet days, keeping staff dry and presentable at outdoor attractions, holiday parks and activity centres whatever the weather.",
   "Waterproof jackets and trousers for the wet, keeping staff dry and presentable at outdoor attractions, holiday parks and activity centres whatever the weather.",
   "Weatherproof jackets and trousers for the rain, keeping outdoor tourism and leisure staff dry and presentable at parks, attractions and activity sites all season."]),
 ("Hi-Vis for Outdoor and Events",[
   "Hi-vis vests and jackets for car parks, events, marshalling and outdoor activities, keeping staff visible and easy to find around a busy site or attraction.",
   "Hi-vis vests and jackets for car parks, events, stewarding and outdoor activities, keeping staff visible and easy to find around a busy attraction or park.",
   "Hi-vis vests and jackets for car parks, events, marshalling and outdoor activities, keeping staff visible and easy to spot around a busy site or attraction."]),
 ("Gilets and Bodywarmers",[
   "Branded gilets and bodywarmers for core warmth without bulk, a popular layer for outdoor attraction, park and activity staff through the shoulder seasons.",
   "Branded gilets and bodywarmers for warmth without bulk, a popular layer for outdoor attraction, park and activity staff through the cooler shoulder seasons.",
   "Branded gilets and bodywarmers that add core warmth without bulk, a favourite layer for outdoor attraction, park and activity staff in the shoulder seasons."]),
 ("Caps, Hats and Accessories",[
   "Branded caps, hats and accessories to finish the kit and handle the sun, embroidered to match the polos, fleeces and softshells across the team.",
   "Branded caps, hats and accessories that finish the kit and handle the sun, embroidered to match the polos, fleeces and softshells the team already wears.",
   "Branded caps, hats and accessories to complete the kit and cope with the sun, embroidered to match the rest of the team's polos, fleeces and softshells."]),
 ("Embroidery, Names and ID Branding",[
   "In-house embroidery of your operator name, logo and staff names onto polos, fleeces, softshells and hi-vis, so a theme park or a small attraction looks consistent and professional.",
   "In-house embroidery of your operator name, logo and staff names across polos, fleeces, softshells and hi-vis, so a theme park or a small independent attraction always looks consistent.",
   "Your operator name, logo and staff names embroidered in-house onto polos, fleeces, softshells and hi-vis, so a big park or a small attraction looks consistent and professional."]),
]
GRID_ORDER=[(0,1,2,3,4,5,6,7),(1,0,2,3,4,5,6,7),(0,1,3,2,4,5,6,7),(0,2,1,3,4,5,6,7)]
def build_grid(town):
    order = GRID_ORDER[pick(town,'gord',len(GRID_ORDER))]
    cards=[]
    for i in order:
        name,variants = CARD_DETAILS[i]
        cards.append(_card(name, variants[pick(town,f'g{i}',len(variants))]))
    return '<div class="tl-product-grid">'+''.join(cards)+'</div>'

TRUST_POOL=[
 "Branded polos, fleeces, softshells, waterproofs and hi-vis for theme parks, holiday parks, attractions and activity centres - trade or direct online",
 "Branded polos, fleeces, softshells, waterproofs and hi-vis for tourism and leisure operators - trade accounts for parks, direct online for independents",
 "Trusted by theme parks, holiday parks, attractions and activity centres across the UK for branded polos, fleeces and softshells - trade or direct",
 "Branded workwear - polos, fleeces, softshells, waterproofs and hi-vis - for tourism and leisure operators across the UK, trade or direct online",
]
S2INTRO_POOL=[
 "Whether you are a major theme park or holiday park or a small independent activity centre or attraction in {t}, the range is built to kit you from one place: branded polos for the everyday, fleeces, softshells and waterproofs for all-weather outdoor work, and hi-vis for car parks, events and activities.",
 "A major {t} theme park or holiday park, or a small independent activity centre or attraction, is kitted from one place: branded polos for the everyday, fleeces, softshells and waterproofs for all-weather outdoor work, and hi-vis for car parks, events and activities.",
 "For a {t} theme park or holiday park or a small independent attraction, the range covers you from one place: branded polos for the everyday, fleeces, softshells and waterproofs for all-weather outdoor work, and hi-vis for car parks, events and activities.",
 "Whether it is a major park or a single independent attraction in {t}, you are kitted from one place: branded polos for the everyday, fleeces, softshells and waterproofs for all-weather outdoor work, plus hi-vis for car parks, events and activities.",
]
EMB_P1_POOL=[
 "In tourism and leisure, staff are the face of the visitor experience. A guest arriving at a busy {t} theme park, holiday park, attraction or activity centre needs to be able to spot at a glance who works there and who to ask, and a clean, branded polo or fleece with the operator name does exactly that, turning a member of staff, even a seasonal one, into a recognisable, approachable part of the team rather than just another person in the crowd.",
 "In tourism and leisure, staff are the face of the visitor experience. At a busy {t} theme park, holiday park, attraction or activity centre, a guest needs to spot at a glance who works there and who to ask, and a clean, branded polo or fleece with the operator name does exactly that, making a member of staff, even a seasonal one, a recognisable, approachable part of the team rather than just another face in the crowd.",
 "Staff are the face of the visitor experience in this trade. A guest at a busy {t} theme park, holiday park, attraction or activity centre needs to see at a glance who works there and who to ask, and a clean, branded polo or fleece with the operator name does just that, turning a member of staff, even a seasonal one, into a recognisable, approachable part of the team.",
 "In tourism and leisure, the staff are the visitor experience made visible. At a busy {t} park, attraction or activity centre, a guest needs to spot at a glance who works there and who to approach, and a clean, branded polo or fleece with the operator name does exactly that, making even a seasonal hire a recognisable, approachable part of the team.",
 "Across tourism and leisure, the staff are what a visitor sees first. At a busy {t} theme park, holiday park, attraction or activity centre, a guest needs to tell at a glance who works there and who to ask, and a clean, branded polo or fleece carrying the operator name does exactly that, making even a seasonal hire a recognisable, approachable part of the team rather than another face in the crowd.",
 "Staff are the visitor experience in this trade, and they have to look it. At a busy {t} park, attraction or activity centre a guest should be able to spot who works there and who to approach in a moment, and a clean, branded polo or fleece with the operator name does just that, turning a member of staff, even a seasonal one, into a recognisable and approachable part of the team.",
]
EMB_P2_POOL=[
 "We brand in-house, which means your operator name and logo are embroidered onto polos, fleeces, softshells, waterproofs and hi-vis, finished to survive heavy seasonal use and frequent washing. Send your artwork once, we hold it on file, and every reorder, new starter and new season matches the last, so whether it is a single independent attraction or a major {t} park with hundreds of staff, the operation looks consistent across the whole site.",
 "Branding is done in-house onto polos, fleeces, softshells, waterproofs and hi-vis - your operator name and logo embroidered and finished to survive heavy seasonal use and frequent washing. We hold your artwork on file, so every reorder, new starter and new season matches, and whether it is one independent attraction or a major {t} park with hundreds of staff, the operation looks consistent across the site.",
 "Your operator name and logo are embroidered in-house onto polos, fleeces, softshells, waterproofs and hi-vis, finished to take heavy seasonal use and frequent washing. Held on file, your artwork reproduces on every reorder, new starter and new season, so a single independent attraction or a major {t} park with hundreds of staff looks consistent across the whole site.",
 "We badge in-house, embroidering your operator name and logo onto polos, fleeces, softshells, waterproofs and hi-vis and finishing them to survive heavy seasonal use and washing. Held on file, your branding matches on every reorder and new starter, so a single {t} attraction or a major park with hundreds of staff looks consistent across the site.",
 "All branding is done in-house, your operator name and logo embroidered onto polos, fleeces, softshells, waterproofs and hi-vis and finished to take heavy seasonal use and frequent washing. Send the artwork once and we hold it on file, so every reorder, new starter and new season matches, and whether it is a single independent attraction or a major {t} park with hundreds of staff the operation looks consistent across the whole site.",
 "We embroider in-house, putting your operator name and logo onto polos, fleeces, softshells, waterproofs and hi-vis, each finished to survive heavy seasonal use and repeated washing. Your artwork stays on file, reproducing on every reorder, new starter and new season, so a single {t} attraction or a major park with hundreds of staff stays consistent right across the site.",
]
EMB_P3_POOL=[
 "And because tourism and leisure runs on a big seasonal intake, that consistency is the point. We hold your branding and sizes on file, so onboarding a whole season's staff, taking on extra hands for a busy event or kitting a second site reproduces exactly the same branded uniform every time, without anyone having to re-supply artwork or guess at a match.",
 "And because tourism and leisure runs on a big seasonal intake, consistency is the value. We hold your branding and sizes on file, so onboarding a season's staff, taking on extra hands for an event or kitting a second site comes back exactly the same branded uniform every time, with no artwork to re-supply.",
 "Because the trade runs on a big seasonal intake, that consistency matters. We keep your branding and sizes on file, so onboarding a whole season's staff, taking on extra hands for a busy event or kitting a second site reproduces the same branded uniform each time.",
 "And because tourism and leisure turns on a big seasonal intake, that consistency is the whole point. We hold branding and sizes on file, so a season's staff, extra event hands or a second site reproduce exactly the same branded uniform every time, with nothing to re-supply.",
 "And since tourism and leisure lives on a big seasonal intake, that consistency is exactly the value. We keep your branding and sizes on file, so onboarding a whole season of staff, taking on extra hands for a busy event or kitting a second site comes back the same branded uniform every time, with no artwork to re-supply and nothing to guess at.",
 "Because the trade turns on a large seasonal intake, consistency is the whole point. With your branding and sizes held on file, onboarding a season of staff, adding extra hands for an event or kitting a second site reproduces the same branded uniform each time, every piece matching what the team already wears.",
]
CON_HEAD="Identifiable, All-Weather and Ready for the Season"
CON_P1_POOL=[
 "Travel, tourism and leisure workwear has to earn its place two ways at once, and the right kit covers both. The first is recognition. Staff are the face of the visitor experience, so a branded polo, fleece or softshell with the operator name makes them instantly identifiable to guests at a busy {t} theme park, holiday park, attraction or activity centre, the person a visitor can find and ask, and turns even a seasonal hire into a recognisable part of the team.",
 "Travel, tourism and leisure workwear earns its place two ways at once, and the right kit does both. First, recognition: staff are the face of the visitor experience, so a branded polo, fleece or softshell with the operator name makes them instantly identifiable to guests at a busy {t} park, attraction or activity centre, the person a visitor can find and ask, and turns even a seasonal hire into a recognisable part of the team.",
 "This workwear has to do two jobs at once, and the right kit covers both. The first is recognition. Staff are the face of the visitor experience, so a branded polo, fleece or softshell with the operator name makes them instantly identifiable to guests at a busy {t} theme park, holiday park or attraction, the person a visitor can find and ask, and turns even a seasonal hire into a recognisable part of the team.",
 "Tourism and leisure workwear has to earn its place two ways at once. The first is recognition: staff are the face of the visitor experience, so a branded polo, fleece or softshell with the operator name makes them instantly identifiable to guests at a busy {t} park, attraction or activity centre, the person to find and ask, and turns even a seasonal hire into a recognisable part of the team.",
]
CON_P2_POOL=[
 "The second is the weather and the season. Much of the work is outdoors and runs across a long operating season in all conditions, so the kit has to layer: polos for the warm days, fleeces and softshells as it cools, waterproofs for the wet, and hi-vis for car parks, events and outdoor activities. It also has to cope with a big seasonal intake, kitting a wave of new staff quickly and consistently when the season starts.",
 "The second is the weather and the season. A lot of the work is outdoors and runs across a long season in all conditions, so the kit has to layer: polos for the warm days, fleeces and softshells as it cools, waterproofs for the wet, and hi-vis for car parks, events and outdoor activities. It also has to handle a big seasonal intake, kitting a wave of new staff quickly and consistently when the season starts.",
 "The second job is the weather and the season. Much of the work happens outdoors across a long operating season in all conditions, so the kit layers: polos for the warm days, fleeces and softshells as it cools, waterproofs for the wet, and hi-vis for car parks, events and outdoor activities. And it has to cope with a big seasonal intake, kitting a wave of new staff fast when the season starts.",
 "The second is weather and season. So much of the work is outdoors across a long season in all conditions that the kit has to layer: polos for the warm days, fleeces and softshells as it cools, waterproofs for the wet, and hi-vis for car parks, events and outdoor activities. And because the season brings a big intake, it has to kit a wave of new staff quickly and consistently.",
]
CON_P3_POOL=[
 'The value is one supplier covering the whole uniform for the big park and the small independent alike, all branded the same. We hold your {t} operator name, logo and sizes on file and supply polos, fleeces, softshells, waterproofs and hi-vis together, so onboarding a fresh season of staff reproduces the same branded uniform every time. Browse the range at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
 'The value is one supplier for the whole uniform, the big park and the small independent alike, all branded the same. We hold your {t} operator name, logo and sizes on file and supply polos, fleeces, softshells, waterproofs and hi-vis together, so onboarding a new season reproduces the same branded uniform every time. Browse the range at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
 'The value is having one supplier cover the whole uniform for both the big park and the small independent, branded the same. We keep your {t} operator name, logo and sizes on file and supply polos, fleeces, softshells, waterproofs and hi-vis together, so each new season comes back the same branded uniform. Browse the range at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
 'The value is one supplier for the entire uniform, the big park and the small independent together, all branded the same. We hold your {t} operator name, logo and sizes on file and supply polos, fleeces, softshells, waterproofs and hi-vis as one, so onboarding a fresh season of staff reproduces the same uniform every time. Browse the range at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
]
ACC_HEAD="Trade Accounts for Large Attractions, Direct Online for Independents"
ACC_P1_POOL=[
 "Tourism and leisure splits into two kinds of buyer, and we have built ordering for both. For a large attraction, theme park or holiday park with a big seasonal team, a trade account is the practical route. It adds managed reordering, agreed pricing and a held kit list with your branding and sizes on file, so onboarding a whole season's staff, taking on extra hands for a busy event or kitting a second site is fast and consistent for a {t} operator. Send your headcount, your logo and your sizes and we will build the branded kit list and hold it.",
 "Tourism and leisure has two kinds of buyer, and ordering is built for both. For a large {t} attraction, theme park or holiday park with a big seasonal team, a trade account is the practical route: managed reordering, agreed pricing and a held kit list with your branding and sizes on file, so onboarding a season's staff, taking on event hands or kitting a second site is fast and consistent. Send your headcount, logo and sizes and we will build the branded kit list and hold it.",
 "This trade splits into two kinds of buyer, and we have built ordering for both. For a large attraction, theme park or holiday park with a big seasonal team in {t}, a trade account is the practical route, adding managed reordering, agreed pricing and a held kit list with your branding and sizes on file, so onboarding a season's staff or kitting a second site stays fast and consistent. Send your headcount, logo and sizes and we will build and hold the list.",
 "Tourism and leisure splits into two kinds of buyer, and ordering suits both. For a large {t} attraction or park running a big seasonal team, a trade account is the practical route: managed reordering, agreed pricing and a held kit list with your branding and sizes on file, so onboarding a season's staff, taking on event hands or kitting a second site is fast and consistent. Send your headcount, logo and sizes and we build the branded kit list and hold it.",
 "Tourism and leisure has two kinds of buyer, and we have built ordering to suit each. For a large {t} attraction, theme park or holiday park running a big seasonal team, the practical route is a trade account: managed reordering, agreed pricing and a held kit list with your branding and sizes on file, so onboarding a whole season of staff, taking on event hands or kitting a second site stays fast and consistent. Send your headcount, your logo and your sizes and we will build the branded kit list and hold it.",
 "There are two kinds of buyer in this trade, and ordering works for both. A large attraction, theme park or holiday park in {t} with a big seasonal team is best served by a trade account, which adds managed reordering, agreed pricing and a held kit list with your branding and sizes on file, so onboarding a season of staff or kitting a second site is fast and consistent. Send your headcount, logo and sizes and we will build and hold the branded kit list.",
]
ACC_P2_POOL=[
 "For an independent activity centre, attraction, museum or tour operator, ordering direct online is quickest and needs no account at all. Browse the range, pick your polos, fleeces, softshells, waterproofs and hi-vis, choose your sizes, send your logo once and check out. There is nothing to set up, your kit is dispatched on standard lead times with embroidery added in-house, and your logo is held on file so the next order matches.",
 "For an independent activity centre, attraction, museum or tour operator, direct online is quickest and needs no account: browse the range, pick your polos, fleeces, softshells, waterproofs and hi-vis, choose sizes, send your logo once and check out. Nothing to set up, dispatched on standard lead times with embroidery in-house, and your logo held on file so the next order matches.",
 "An independent activity centre, attraction, museum or tour operator orders quickest direct online, no account needed: browse the range, pick your polos, fleeces, softshells, waterproofs and hi-vis, add sizes, send the logo once and check out. Nothing to set up, dispatched on standard lead times with in-house embroidery, and your logo held on file for the next order.",
 "For an independent attraction, activity centre or tour operator, the quickest route is direct online with no account: browse, pick your polos, fleeces, softshells, waterproofs and hi-vis, choose sizes, send your logo once and check out, with nothing to set up, dispatched on standard lead times with embroidery in-house and your logo held on file.",
 "For an independent activity centre, attraction, museum or tour operator, the quickest route is direct online and needs no account at all: browse the range, pick your polos, fleeces, softshells, waterproofs and hi-vis, choose your sizes, send your logo once and check out. Nothing to set up, dispatched on standard lead times with embroidery added in-house, and your logo held on file so the next order matches.",
 "An independent activity centre, attraction, museum or tour operator gets going quickest direct online, with no account needed: browse, pick your polos, fleeces, softshells, waterproofs and hi-vis, add your sizes, send the logo once and check out. There is nothing to set up, kit ships on standard lead times with in-house embroidery, and your logo stays on file for the next order.",
]
ACC_P3_POOL=[
 "Both routes are branded in-house from the same supplier, so whether you are kitting two hundred seasonal staff in {t} or just a handful of guides, the workwear is consistent, professional and ready for the season. Most large operators run the trade account centrally and point smaller sites and concessions at the direct online route, and everyone ends up matching.",
 "Both routes are branded in-house by the same supplier, so whether you are kitting two hundred {t} seasonal staff or just a handful of guides, the kit is consistent, professional and ready for the season. Most large operators use the trade account centrally and send smaller sites and concessions to the direct online route, and everyone matches.",
 "Both routes come branded in-house from one supplier, so whether it is two hundred seasonal staff across {t} or just a few guides, the workwear is consistent, professional and ready for the season. Most large operators run a trade account centrally and point smaller sites and concessions at direct online, and the whole site matches.",
 "Both routes are branded in-house by one supplier, so whether you kit two hundred seasonal staff in {t} or only a handful of guides, the kit stays consistent, professional and ready for the season. Most large operators keep the trade account central and send smaller sites and concessions direct online, and everyone ends up matching.",
 "Both routes are branded in-house by the same supplier, so whether you are kitting two hundred seasonal staff across {t} or just a handful of guides, the workwear stays consistent, professional and ready for the season. Most large operators run the trade account centrally and send smaller sites and concessions to the direct online route, and everyone ends up matching.",
 "Either route is branded in-house from one supplier, so kitting two hundred seasonal staff in {t} or only a few guides comes back equally consistent, professional and ready for the season. Larger operators tend to keep the trade account central and point smaller sites and concessions at direct online, so the whole operation matches.",
]
ACC_P4_POOL=[
 'Set up a trade account for an attraction at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>, or order direct online with no account at <a href="https://www.ineedworkwear.com">iNeedWorkwear</a>.',
 'Set up a trade account for an attraction at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>. For an independent, order direct online with no account at <a href="https://www.ineedworkwear.com">iNeedWorkwear</a>.',
 'Open a trade account for an attraction at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>, or order direct online with no account as an independent at <a href="https://www.ineedworkwear.com">iNeedWorkwear</a>.',
 'Set up an attraction trade account at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>, or as an independent order direct online with no account at <a href="https://www.ineedworkwear.com">iNeedWorkwear</a>.',
]
WHY_P1_POOL=[
 "A tourism or leisure operator in {t} whose staff turn out in clean, branded polos, fleeces and softshells looks professional and organised to every visitor, and iNeedWorkwear supplies that whole look from a single place, branded in-house, on a trade account for the big park or direct online for the independent, so staff are identifiable and the operation is consistent from the entrance gate onwards.",
 "A {t} tourism or leisure operator whose staff wear clean, branded polos, fleeces and softshells looks professional and organised to every visitor, and iNeedWorkwear supplies that whole look from one place, branded in-house, on a trade account for the big park or direct online for the independent, so staff are identifiable and the operation is consistent from the gate onwards.",
 "When a {t} tourism or leisure operator turns its staff out in clean, branded polos, fleeces and softshells, it looks professional and organised to every visitor, and we supply that whole look from a single place, branded in-house, on a trade account or direct online, so staff are identifiable and the operation is consistent from the entrance gate onwards.",
 "A tourism or leisure operator in {t} whose staff wear clean, branded polos, fleeces and softshells reads as professional and organised to every visitor, and we supply that whole look from one place, branded in-house, on a trade account for the big park or direct online for the independent, so staff are identifiable from the gate onwards.",
 "A {t} tourism or leisure operator whose staff turn out in clean, branded polos, fleeces and softshells looks organised and professional to every visitor, and we supply the whole look from one place, branded in-house, trade or direct, so even a small independent presents like a major attraction.",
 "In {t}, a tourism or leisure operator whose staff wear clean, branded polos, fleeces and softshells looks professional from the first glance at the gate, and iNeedWorkwear supplies that whole look from one place, branded in-house, on a trade account for the big park or direct online for the independent.",
]
WHY_P2_POOL=[
 "It is built for both ends of the trade and for the season. A large attraction onboarding a wave of seasonal staff gets managed reordering and a held kit list, while a small independent gets a quick, no-account direct route online, and both come back the same branded kit, so a growing operation never ends up with a patchwork of mismatched workwear as it scales or restocks each year.",
 "It is built for both ends of the trade and for the season. A large attraction onboarding a wave of seasonal staff gets managed reordering and a held kit list, and a small independent gets a quick, no-account direct route online, with both coming back the same branded kit, so a growing operation avoids a patchwork of mismatched workwear as it scales or restocks each year.",
 "It works for both ends of the trade and for the season. A large attraction onboarding seasonal staff gets managed reordering and a held kit list, while a small independent gets a quick, no-account online route, and both return the same branded kit, so a scaling operation never drifts into mismatched workwear year on year.",
 "It suits both ends of the trade and the season. A large attraction onboarding a wave of seasonal staff gets managed reordering and a held kit list, a small independent gets a fast no-account online route, and both come back the same branded kit, so a growing operation never ends up with mismatched workwear as it restocks each year.",
 "It is made for both ends of the trade and for the season. The large attraction gets managed reordering and a held kit list for onboarding seasonal staff, the small independent gets a quick no-account online route, and both return the same branded kit, so scaling or restocking never means a patchwork of mismatched workwear.",
 "It covers both ends of the trade and the season. A large attraction onboarding seasonal staff leans on managed reordering and a held kit list, a small independent uses the quick no-account online route, and both come back the same branded kit, so a growing operation stays matched year on year.",
]
WHY_P3_POOL=[
 "The range covers what the work demands: polos for everyday visitor-facing work, fleeces, softshells and waterproofs for all-weather outdoor work across the season, hi-vis for car parks, events and activities, and gilets, caps and accessories to finish. It is a focused, practical range, so choosing, ordering and reordering stay quick for a busy operator at the start of a season.",
 "The range covers what the work really demands: polos for everyday visitor-facing work, fleeces, softshells and waterproofs for all-weather outdoor work across the season, hi-vis for car parks, events and activities, and gilets, caps and accessories to finish. It is focused and practical, so choosing, ordering and reordering stay quick for a busy operator at the start of a season.",
 "Everything in the range reflects what the work demands: polos for everyday visitor-facing work, fleeces, softshells and waterproofs for all-weather outdoor work, hi-vis for car parks, events and activities, and gilets, caps and accessories to finish. The range is focused and practical, so ordering and reordering stay quick for a busy operator at the start of a season.",
 "The range is built around what the work demands: polos for everyday visitor-facing work, fleeces, softshells and waterproofs for all-weather outdoor work across the season, hi-vis for car parks, events and activities, plus gilets, caps and accessories, so choosing and reordering stay quick for a busy operator at the start of a season.",
 "It is a focused, practical range mapped to the work: polos for everyday visitor-facing work, fleeces, softshells and waterproofs for all-weather outdoor work, hi-vis for car parks, events and activities, and gilets, caps and accessories to finish, which keeps choosing, ordering and reordering fast for a busy operator each season.",
 "The range stays focused on what the work needs: polos for everyday visitor-facing work, fleeces, softshells and waterproofs for all-weather outdoor work across the season, hi-vis for car parks, events and activities, and gilets, caps and accessories, so a busy operator can choose and reorder in minutes at the start of a season.",
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
 "iNeedWorkwear supplies branded polos, fleeces, softshells, waterproofs and hi-vis to theme parks, holiday parks, activity centres, visitor attractions, museums and tour operators across {region}, all embroidered in-house with the operator name.",
 "We supply branded polos, fleeces, softshells, waterproofs and hi-vis to theme parks, holiday parks, activity centres, visitor attractions, museums and tour operators across {region}, all embroidered in-house with the operator name.",
 "Across {region}, iNeedWorkwear kits theme parks, holiday parks, activity centres, attractions, museums and tour operators in branded polos, fleeces, softshells, waterproofs and hi-vis, all embroidered in-house with the operator name.",
 "From a single guide to a major park across {region}, iNeedWorkwear supplies branded polos, fleeces, softshells, waterproofs and hi-vis to tourism and leisure operators, all embroidered in-house.",
 "Across {region}, iNeedWorkwear supplies branded polos, fleeces, softshells, waterproofs and hi-vis to theme parks, holiday parks, activity centres, visitor attractions, museums and tour operators, every piece embroidered in-house with the operator name.",
 "iNeedWorkwear supplies tourism and leisure operators right across {region}, from a single guide to a major park, with branded polos, fleeces, softshells, waterproofs and hi-vis, every piece embroidered in-house with the operator name.",
]
ORD_P2_POOL=[
 "For an independent activity centre, attraction or tour operator, ordering direct online is quickest and needs no account: browse the range, pick your polos, fleeces, softshells, waterproofs and hi-vis, add your sizes, send your logo once and check out. Your kit is dispatched on standard lead times with embroidery added in-house, and your logo is held on file so the next order matches.",
 "For an independent activity centre, attraction or tour operator, direct online is quickest and needs no account: browse, pick your polos, fleeces, softshells, waterproofs and hi-vis, add sizes, send your logo once and check out. Your kit ships on standard lead times with embroidery in-house, and your logo is held on file so the next order matches.",
 "An independent activity centre, attraction or tour operator orders quickest direct online, no account needed: browse the range, pick your polos, fleeces, softshells, waterproofs and hi-vis, add sizes, send the logo once and check out. Kit is dispatched on standard lead times with in-house embroidery, and your logo is held on file for the next order.",
 "For an independent attraction or activity centre, the quickest route is direct online with no account: browse the range, pick your polos, fleeces, softshells, waterproofs and hi-vis, add your sizes, send your logo once and check out, dispatched on standard lead times with embroidery in-house and your logo held on file.",
 "Independent activity centres, attractions and tour operators order quickest direct online with no account: browse the range, pick your polos, fleeces, softshells, waterproofs and hi-vis, add your sizes, send your logo once and check out, dispatched on standard lead times with in-house embroidery and your logo held on file so the next order matches.",
 "For an independent attraction, activity centre or tour operator the fastest route is direct online, no account needed: browse, choose your polos, fleeces, softshells, waterproofs and hi-vis, add sizes, send the logo once and check out, dispatched on standard lead times with in-house embroidery and your logo kept on file for next time.",
]
ORD_P3_POOL=[
 "For a larger attraction or park with a big seasonal team, a trade account adds managed reordering and agreed pricing: send your headcount, your logo and your sizes and we will build a branded kit list and hold it on file, so each season's staff and each new starter are onboarded in matching kit.",
 "For a larger attraction or park with a big seasonal team, a trade account brings managed reordering and agreed pricing: send your headcount, logo and sizes and we will build a branded kit list and hold it on file, so each season's staff and each new starter are onboarded in matching kit.",
 "A larger attraction or park with a big seasonal team can use a trade account for managed reordering and agreed pricing: send your headcount, logo and sizes and we will build a branded kit list and hold it on file, so each season's staff onboard in matching kit.",
 "For a larger attraction or park with a big seasonal team, a trade account adds managed reordering and agreed pricing: send your headcount, logo and sizes and we will build a branded kit list and keep it on file, so each season's staff and new starters are onboarded in matching kit.",
 "For a larger attraction or holiday park taking on a big seasonal team, a trade account brings managed reordering and agreed pricing: send your headcount, your logo and your sizes and we will build a branded kit list and hold it on file, so each season's staff and every new starter are onboarded in matching kit.",
 "A larger attraction or holiday park with a big seasonal team can run a trade account for managed reordering and agreed pricing: send through your headcount, logo and sizes and we will build a branded kit list and keep it on file, so every season's staff and each new starter onboard in matching kit.",
]
SELF_POOL=[
 'Opening a new attraction or activity centre and need kit now? Browse the full range, add your sizes and order direct on self-service checkout at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
 'Gearing up for a new season and need kit fast? Browse the range, add sizes and order direct on self-service checkout at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
 'Setting up a new tour, attraction or activity centre and need kit today? Browse the full range, add your sizes and order direct on self-service checkout at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
 'Need seasonal staff kit sorted now? Browse the range, add sizes and order direct on self-service checkout at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
]
SORTED_POOL=[
 '<h3>Travel, Tourism and Leisure Workwear, Sorted</h3><p>From branded polos and fleeces to softshells, waterproofs and hi-vis, get workwear built for theme parks, holiday parks, attractions and activity centres - embroidered in-house with your operator name, on a trade account or ordered direct online with no account.</p><p><a href="https://www.ineedworkwear.com">Browse travel, tourism and leisure workwear at iNeedWorkwear</a></p>',
 '<h3>Travel, Tourism and Leisure Workwear, Sorted</h3><p>Branded polos and fleeces, plus softshells, waterproofs and hi-vis - workwear for theme parks, holiday parks, attractions and activity centres, embroidered in-house with your operator name, on a trade account or ordered direct online.</p><p><a href="https://www.ineedworkwear.com">Browse travel, tourism and leisure workwear at iNeedWorkwear</a></p>',
 '<h3>Travel, Tourism and Leisure Workwear, Sorted</h3><p>From polos and fleeces to softshells, waterproofs and hi-vis, kit a major park or a single independent attraction, embroidered in-house and ordered on a trade account or direct online with no account.</p><p><a href="https://www.ineedworkwear.com">Browse travel, tourism and leisure workwear at iNeedWorkwear</a></p>',
 '<h3>Travel, Tourism and Leisure Workwear, Sorted</h3><p>Polos, fleeces, softshells, waterproofs and hi-vis, the season-ready kit for theme parks, holiday parks, attractions and activity centres, embroidered in-house and ready on a trade account for the park or direct online for the independent.</p><p><a href="https://www.ineedworkwear.com">Browse travel, tourism and leisure workwear at iNeedWorkwear</a></p>',
]
OWNER_POOL=[
 "And the trade runs at every size, which shapes what a workwear supplier has to do. Major attractions, theme parks and hotel groups run big, seasonal teams and buy through procurement, while independent activity centres, heritage sites, tour operators and guides need just a few branded pieces. A supplier here has to serve the big visitor attraction and the one-person guide alike, with both a managed account and a quick direct route.",
 "And the trade runs at every size, which shapes the supplier's job. Major attractions, theme parks and hotel groups run big, seasonal teams and buy through procurement, while independent activity centres, heritage sites, tour operators and guides want just a few branded pieces. A supplier here has to serve the big attraction and the one-person guide alike, with a managed account and a quick direct route side by side.",
 "And the trade runs at every size, which shapes what a supplier needs to do. Major attractions, theme parks and hotel groups run big, seasonal teams and buy through procurement, while a wide layer of independent activity centres, heritage sites and tour operators need only a few branded pieces. A supplier has to handle the big attraction and the single guide alike, offering both a managed account and a fast direct route.",
 "And every size of operator is in the mix, which shapes the supplier's job. Major attractions, parks and hotel groups run big seasonal teams through procurement, while independent activity centres, heritage sites, tour operators and guides pick up work and want a handful of branded pieces. A supplier has to serve the big attraction and the one-person guide alike, with a managed account and a quick direct route both on offer.",
 "And the trade spans every size, which shapes what a supplier must do. Big attractions, theme parks and hotel groups run large seasonal teams and buy centrally, while independent activity centres, heritage sites, tour operators and guides need just a few branded pieces. A supplier has to look after the big attraction and the single guide alike, with both a managed account and a quick direct route.",
 "And it runs on operators of every size, which shapes the supplier's job. Major attractions, parks and hotel groups field big seasonal teams and buy through procurement, while a deep layer of independent activity centres, heritage sites and tour operators want only a few branded pieces. A supplier has to cover the big attraction and the one-person guide alike, with a managed account and a quick direct route both available.",
]
PRESENT_POOL=[
 "And the kit does two jobs at once, which is what makes tourism and leisure workwear its own thing. It makes staff instantly identifiable to visitors, so a guest at a busy {t} attraction or park can spot who works there and who to ask, which turns even a seasonal hire into a recognisable part of the team. And it is layered for all-weather outdoor work across a long season: polos for the warm days, fleeces and softshells as it cools, waterproofs for the wet, and hi-vis for car parks, events and activities.",
 "And the kit does two jobs at once, which is what sets tourism and leisure workwear apart. It makes staff instantly identifiable to visitors, so a guest at a busy {t} attraction or park can spot who works there and who to ask, turning even a seasonal hire into a recognisable part of the team. And it is layered for all-weather outdoor work across a long season: polos for the warm days, fleeces and softshells as it cools, waterproofs for the wet, and hi-vis for car parks, events and activities.",
 "And the kit has to do two jobs at once, which is the heart of tourism and leisure workwear. It makes staff instantly identifiable to visitors, so a guest at a busy {t} attraction or park can spot who works there and who to ask, turning even a seasonal hire into a recognisable part of the team. And it is layered for all-weather outdoor work across a long season: polos, fleeces, softshells and waterproofs, plus hi-vis for car parks, events and activities.",
 "And the kit works two ways at once, which is what makes this workwear distinct. It makes staff instantly identifiable to visitors, so a guest at a busy {t} attraction or park can spot who works there and who to ask, turning even a seasonal hire into a recognisable part of the team. And it is layered for all-weather outdoor work across a long season: polos, fleeces, softshells and waterproofs, plus hi-vis for car parks, events and activities.",
 "And the kit pulls two jobs at once, which is what makes tourism and leisure workwear its own thing. It makes staff instantly identifiable to visitors, so a guest at a busy {t} attraction or park can spot who works there and who to ask, turning a seasonal hire into a recognisable part of the team. And it is layered for all-weather outdoor work across a long season: polos, fleeces, softshells and waterproofs, plus hi-vis for car parks, events and activities.",
 "And the kit covers two jobs at once, which is what distinguishes tourism and leisure workwear. It makes staff instantly identifiable to visitors, so a guest at a busy {t} attraction or park can spot who works there and who to ask, turning even a seasonal hire into a recognisable part of the team. And it is layered for all-weather outdoor work across a long season: polos, fleeces, softshells and waterproofs, plus hi-vis for car parks, events and activities.",
]
NARROW_POOL=[
 "Because tourism and leisure is seasonal, it is a repeat-purchase trade with a big intake each year, and the range is built to reorder easily. Polos, fleeces, softshells, waterproofs and hi-vis, branded in-house with the operator name, are the whole kit, and we hold your logo on file so the next season's staff and the next new starter in {t} match what the team already wears.",
 "Because tourism and leisure is seasonal, this is a repeat-purchase trade with a big intake each year, and the range is built to reorder easily. Polos, fleeces, softshells, waterproofs and hi-vis, branded in-house with the operator name, are the whole kit, and your logo is held on file so the next season's staff and the next new starter in {t} match what the team already wears.",
 "Since tourism and leisure is seasonal, it is a repeat-purchase trade with a big yearly intake, and the range is built to reorder easily. Polos, fleeces, softshells, waterproofs and hi-vis, branded in-house with the operator name, are the whole kit, and we keep your logo on file so the next season's staff and the next new starter in {t} match what the team already wears.",
 "Because the trade is seasonal, it is a repeat-purchase one with a big intake each year, and the range reorders easily. Polos, fleeces, softshells, waterproofs and hi-vis, branded in-house with the operator name, are the whole kit, and your logo sits on file so the next season's staff and the next new starter in {t} match what the team already wears.",
 "As tourism and leisure is seasonal, it is a repeat-purchase trade with a big intake each year, and the range is built to reorder fast. Polos, fleeces, softshells, waterproofs and hi-vis, branded in-house with the operator name, are the whole kit, and we hold your logo on file so the next season's staff and the next new starter in {t} match what the team already runs.",
 "Because tourism and leisure runs on a seasonal intake, it is a repeat-purchase trade, and the range is built for easy reordering. Polos, fleeces, softshells, waterproofs and hi-vis, branded in-house with the operator name, are the whole kit, and your logo is on file so the next season's staff and the next new starter in {t} line up with what the team already wears.",
]
KIT_POOL=[
 "Polos, fleeces, softshells, waterproofs and hi-vis, branded with the operator name, are the whole kit {loc}.",
 "The whole kit is polos, fleeces, softshells, waterproofs and hi-vis, branded with the operator name {loc}.",
 "Polos, fleeces, softshells, waterproofs and hi-vis do the job, branded with the operator name {loc}.",
 "It comes down to polos, fleeces, softshells, waterproofs and hi-vis, branded with the operator name {loc}.",
 "Polos, fleeces, softshells, waterproofs and hi-vis, all branded with the operator name, are the kit {loc}.",
 "Branded polos, fleeces, softshells, waterproofs and hi-vis make up the whole kit {loc}.",
]
S2TAIL_POOL=[
 ", polos, fleeces and softshells lead, with waterproofs and hi-vis alongside.",
 ", the core is polos, fleeces and softshells, with waterproofs and hi-vis to finish.",
 ", expect polos, fleeces and softshells first, then waterproofs and hi-vis.",
 ", polos, fleeces and softshells do the work, with waterproofs and hi-vis alongside.",
 ", polos, fleeces and softshells anchor the kit, with waterproofs and hi-vis completing it.",
 ", it is polos, fleeces and softshells, plus waterproofs and hi-vis.",
]

# Fix 6: town-swapped fallbacks so batch JSON only needs genuinely-local fields.
SNAP_TMPL=("iNeedWorkwear supplies branded polos, fleeces, softshells, waterproofs and hi-vis to "
 "theme parks, holiday parks, activity centres, visitor attractions, museums and tour operators "
 "across {t}, embroidered in-house with the operator name. The trade runs from large attractions "
 "with big seasonal teams to small independent activity centres and guides, so a larger operator "
 "can run a trade account for managed reordering and seasonal intake, while an independent can "
 "order direct online with no account.")
KIT_LOC_DEFAULT="across the area's attractions, parks and visitor sites"

def s1_paras(town, T):
    if 's1loc' in T:
        present = PRESENT_POOL[pick(town,'pre',len(PRESENT_POOL))].format(t=town)
        narrow = NARROW_POOL[pick(town,'nar',len(NARROW_POOL))].format(t=town)
        own = OWNER_POOL[pick(town,'own',len(OWNER_POOL))]
        kit = KIT_POOL[pick(town,'kit',len(KIT_POOL))].format(loc=T.get('kit_loc', KIT_LOC_DEFAULT))
        return list(T['s1loc']) + [own, present, narrow.rstrip()+' '+kit]
    return T['s1']

def s2_local_text(town, T):
    if 's2_intro' in T:
        return T['s2_intro'].rstrip() + S2TAIL_POOL[pick(town,'s2t',len(S2TAIL_POOL))]
    return T['s2_local']

def faq_for(t, region):
    P = lambda salt, opts: opts[pick(t, salt, len(opts))]
    return [
     (f"Do you supply branded workwear to tourism and leisure operators in {t}?", P('fq1',[
      f"Yes. Theme parks, holiday parks, activity centres, visitor attractions, museums, tour operators and leisure businesses across {region} get branded polos, fleeces, softshells, waterproofs and hi-vis from us, embroidered in-house with the operator name. A large attraction can run a trade account for managed reordering and seasonal intake, and a small independent can order direct online with no account.",
      f"Yes. Branded polos, fleeces, softshells, waterproofs and hi-vis go to theme parks, holiday parks, activity centres, attractions, museums and tour operators across {region}, embroidered in-house with the operator name. A large attraction runs a trade account for managed reordering and seasonal intake, and a small independent orders direct online with no account.",
      f"Yes. From a one-person guide to a major park across {region}, we supply branded polos, fleeces, softshells, waterproofs and hi-vis, embroidered in-house with the operator name, on a trade account for the park or direct online with no account.",
      f"Yes. Theme parks, holiday parks, activity centres, attractions and tour operators across {region} get branded polos, fleeces, softshells, waterproofs and hi-vis from us, embroidered in-house with the operator name, on a trade account or ordered direct online.",
      f"Yes. Across {region} we kit theme parks, holiday parks, activity centres, attractions and tour operators in branded polos, fleeces, softshells, waterproofs and hi-vis, embroidered in-house with the operator name, on a trade account or direct online for an independent.",
      f"Yes. Tourism and leisure operators across {region}, from a single guide to a major park, get branded polos, fleeces, softshells, waterproofs and hi-vis from us, embroidered in-house with the operator name, on a trade account or direct online with no account."])),
     ("Can you handle a large seasonal staff intake?", P('fq2',[
      "Yes. Tourism and leisure is seasonal, so a large attraction or holiday park can run a trade account with managed reordering, agreed pricing and a held kit list, and we onboard a whole season's staff in matching branded kit on standard lead times. We hold your logo and sizes on file, so each new season and each new starter comes back the same.",
      "Yes. As tourism and leisure is seasonal, a large attraction or holiday park can run a trade account with managed reordering, agreed pricing and a held kit list, and we onboard a whole season's staff in matching branded kit on standard lead times. Your logo and sizes are held on file, so each season and each new starter comes back the same.",
      "Yes. A large attraction or park can run a trade account with managed reordering, agreed pricing and a held kit list, so a whole season's staff are onboarded in matching branded kit on standard lead times. We hold your logo and sizes on file, so each new season and each new starter matches.",
      "Yes. The trade is seasonal, so a large attraction or holiday park runs a trade account with managed reordering, agreed pricing and a held kit list, and we onboard a season's staff in matching branded kit on standard lead times, with your logo and sizes held on file so each season matches.",
      "Yes. A large attraction or holiday park can run a trade account with managed reordering and a held kit list to onboard a whole season's staff in matching kit on standard lead times, with your logo and sizes on file so each new season and each new starter comes back the same.",
      "Yes. Tourism and leisure runs on a seasonal intake, so a large attraction or park uses a trade account with managed reordering, agreed pricing and a held kit list, and we onboard a season's staff in matching branded kit on standard lead times, with logo and sizes held on file."])),
     ("What workwear do tourism and leisure teams usually need?", P('fq3',[
      "The core kit is branded polos and t-shirts for everyday visitor-facing work, fleeces, softshells and waterproofs for outdoor and all-weather work across the season, hi-vis for car parks, events and outdoor activities, and gilets, caps and accessories, all branded with the operator name so staff are identifiable to visitors.",
      "The core is branded polos and t-shirts for everyday visitor-facing work, fleeces, softshells and waterproofs for outdoor and all-weather work, hi-vis for car parks, events and activities, and gilets, caps and accessories, all branded with the operator name so staff are identifiable.",
      "At its core: branded polos and t-shirts for visitor-facing work, fleeces, softshells and waterproofs for outdoor and all-weather work across the season, hi-vis for car parks, events and activities, and gilets, caps and accessories, all branded with the operator name.",
      "The core uniform is branded polos for visitor-facing work, fleeces, softshells and waterproofs for outdoor and all-weather work, hi-vis for car parks, events and activities, and gilets, caps and accessories, all branded with the operator name so staff are identifiable to visitors.",
      "It comes down to branded polos for visitor-facing work, fleeces, softshells and waterproofs for outdoor and all-weather work, hi-vis for car parks, events and activities, and gilets, caps and accessories, all branded with the operator name.",
      "Branded polos for visitor-facing work, fleeces, softshells and waterproofs for outdoor and all-weather work across the season, hi-vis for car parks, events and activities, and gilets, caps and accessories make up the core, all branded with the operator name."])),
     ("Why does branding matter for tourism and leisure staff?", P('fq4',[
      "Staff are the face of the visitor experience, so a branded polo or fleece makes them instantly identifiable and approachable to visitors who need to find someone to ask, which matters at a busy theme park, holiday park, attraction or activity centre. We embroider the operator name and logo in-house, turning everyday kit into a recognisable, professional uniform.",
      "Staff are the face of the visitor experience, so a branded polo or fleece makes them instantly identifiable and approachable to guests who need someone to ask, which matters at a busy theme park, holiday park, attraction or activity centre. We embroider the operator name and logo in-house, turning everyday kit into a recognisable, professional uniform.",
      "Because staff are the face of the visitor experience, a branded polo or fleece makes them instantly identifiable and approachable to visitors looking for someone to ask, which matters at a busy park, attraction or activity centre. The operator name and logo are embroidered in-house, turning everyday kit into a recognisable uniform.",
      "Staff are the face of the visitor experience, so a branded polo or fleece makes them instantly identifiable to guests who need to find someone to ask at a busy theme park, holiday park, attraction or activity centre. We embroider the operator name and logo in-house, turning everyday kit into a professional, recognisable uniform.",
      "Staff are the visitor experience made visible, so a branded polo or fleece makes them instantly identifiable and approachable to guests at a busy park, attraction or activity centre. We embroider the operator name and logo in-house, turning everyday kit into a recognisable, professional uniform.",
      "Since staff are the face of the visitor experience, a branded polo or fleece makes them instantly identifiable and approachable to visitors at a busy theme park, holiday park or attraction. The operator name and logo are embroidered in-house, turning everyday kit into a recognisable, professional uniform."])),
     ("Can you embroider our operator name and logo?", P('fq5',[
      "Yes. We embroider your operator name and logo in-house onto polos, fleeces, softshells, waterproofs and hi-vis, finished to survive heavy seasonal use and frequent washing. Send your artwork once, we hold it on file, and every reorder, new starter and new season matches, so a theme park or a small independent attraction looks consistent and professional.",
      "Yes. Your operator name and logo are embroidered in-house onto polos, fleeces, softshells, waterproofs and hi-vis, finished for heavy seasonal use and frequent washing. Send artwork once and we hold it on file, so every reorder, new starter and new season matches, and a theme park or small attraction looks consistent.",
      "Yes, all branding is done in-house onto polos, fleeces, softshells, waterproofs and hi-vis, finished to survive heavy seasonal use and washing. We hold your artwork on file, so every reorder, new starter and new season matches and a theme park or small independent attraction looks consistent and professional.",
      "Yes. Send your artwork once and we embroider your operator name and logo in-house onto polos, fleeces, softshells, waterproofs and hi-vis, holding it on file so every reorder, new starter and new season matches, and a theme park or small attraction looks consistent and professional.",
      "Yes. Operator name and logo are embroidered in-house onto polos, fleeces, softshells, waterproofs and hi-vis, finished for heavy seasonal use and washing and held on file, so every reorder, new starter and new season matches and a park or small attraction stays consistent.",
      "Yes, embroidery is done in-house onto polos, fleeces, softshells, waterproofs and hi-vis, finished to take heavy seasonal use and washing. Send your logo once and we keep it on file, so reorders, new starters and new seasons line up and a theme park or small attraction looks professional."])),
     ("Do you supply softshells and waterproofs for outdoor attraction work?", P('fq6',[
      "Yes. Alongside the polos and fleeces we supply branded softshell jackets, waterproof jackets and trousers and outdoor hi-vis for the outdoor, all-weather work that theme parks, holiday parks, activity centres and attractions involve, keeping staff warm, dry and presentable across the whole season.",
      "Yes. As well as polos and fleeces, we supply branded softshells, waterproof jackets and trousers and outdoor hi-vis for the outdoor, all-weather work theme parks, holiday parks, activity centres and attractions involve, keeping staff warm, dry and presentable across the season.",
      "Yes, we supply branded softshell jackets, waterproof jackets and trousers and outdoor hi-vis alongside the polos and fleeces, for the outdoor all-weather work parks, attractions and activity centres involve, keeping staff warm, dry and presentable all season.",
      "Yes. Beyond the polos and fleeces, we supply branded softshells, waterproofs and outdoor hi-vis for the all-weather outdoor work theme parks, holiday parks, activity centres and attractions involve, keeping staff warm, dry and presentable across the whole season.",
      "Yes. The all-weather layers are covered too: branded softshells, waterproof jackets and trousers and outdoor hi-vis alongside the polos and fleeces, keeping staff warm, dry and presentable at outdoor parks, attractions and activity centres all season.",
      "Yes. We supply branded softshells, waterproofs and outdoor hi-vis with the polos and fleeces, for the outdoor all-weather work theme parks, holiday parks and activity centres involve, keeping staff warm, dry and presentable across the season."])),
     ("How quickly can you supply tourism and leisure workwear?", P('fq7',[
      "Order direct online and your kit is dispatched on standard lead times, with embroidery added in-house before it ships. For a large attraction or park on a trade account, send your headcount, your logo and your sizes and we will build a branded kit list and hold it on file, so each season's staff are onboarded in matching kit on standard lead times.",
      "Order direct online and your kit ships on standard lead times, with embroidery added in-house first. For a large attraction or park on a trade account, send your headcount, logo and sizes and we will build a branded kit list and hold it on file, so each season's staff onboard in matching kit on standard lead times.",
      "Order direct online and we dispatch on standard lead times, embroidery added in-house before shipping. For an attraction or park on a trade account, send your headcount, logo and sizes and we will build a branded kit list and hold it on file for fast seasonal onboarding and reordering.",
      "Order direct online and your kit is dispatched on standard lead times with embroidery done in-house first. For a large attraction or park on a trade account, send your headcount, logo and sizes and we will build a branded kit list and hold it on file, so each season's staff onboard in matching kit.",
      "Order online and we dispatch on standard lead times with embroidery added in-house beforehand. A large attraction or park on a trade account can send headcount, logo and sizes for a branded kit list held on file, so each season's staff onboard in matching kit fast.",
      "Order direct online and your kit ships on standard lead times, embroidered in-house first. For a large attraction or park on a trade account, send your headcount, logo and sizes and we will build a branded kit list and keep it on file for quick seasonal onboarding on standard lead times."])),
    ]

TOWNS = {
 "birmingham": {
  "region":"Birmingham and the West Midlands",
  "nearby":["Solihull","West Bromwich","Walsall"],
  "snapshot":"iNeedWorkwear supplies branded polos, fleeces, softshells, waterproofs and hi-vis to theme parks, holiday parks, activity centres, visitor attractions, museums and tour operators across Birmingham, embroidered in-house with the operator name. The trade runs from large attractions with big seasonal teams to small independent activity centres and guides, so a larger operator can run a trade account for managed reordering and seasonal intake, while an independent can order direct online with no account.",
  "s1_head":"Kitting the visitor economy of the West Midlands",
  "s1loc":[
   "Birmingham and the West Midlands run one of the country's biggest visitor economies, drawing over 145 million visits a year. The city's attractions span Cadbury World, the National SEA LIFE Centre, the LEGOLAND Discovery Centre and the Thinktank science museum, the open-air Black Country Living Museum just outside, and green spaces like Cannon Hill Park and the canals at Brindleyplace, alongside theatres, a busy hotel trade, a wide tour-operator scene and Birmingham Airport on the doorstep.",
   "And the trade runs at every size. Major attractions, museums and hotel groups run big, seasonal teams and buy through procurement, while independent activity centres, heritage sites, tour operators and guides across the city need just a few branded pieces. A workwear supplier here has to serve the big visitor attraction and the one-person guide alike, which is why we run trade accounts and direct online ordering side by side.",
  ],
  "kit_loc":"across the city's attractions, parks and visitor sites",
  "s2_intro":"Whether you are a major Birmingham attraction or hotel group, a heritage site or a small independent activity centre in Solihull",
 },
 "leeds": {
  "region":"Leeds and West Yorkshire",
  "nearby":["Bradford","Pudsey","Dewsbury"],
  "snapshot":"iNeedWorkwear supplies branded polos, fleeces, softshells, waterproofs and hi-vis to theme parks, holiday parks, activity centres, visitor attractions, museums and tour operators across Leeds, embroidered in-house with the operator name. The trade runs from large attractions and arenas with big seasonal teams to small independent activity centres and guides, so a larger operator can run a trade account for managed reordering and seasonal intake, while an independent can order direct online with no account.",
  "s1_head":"Kitting the visitor economy of Yorkshire",
  "s1loc":[
   "Leeds has a busy, varied visitor economy. The Royal Armouries, Roundhay Park and its Tropical World, Harewood House, Temple Newsam and Kirkstall Abbey draw visitors across the city, while activity venues from TeamSport karting and the Leeds Urban Bike Park to climbing walls, crazy golf and escape rooms keep the leisure trade busy, alongside the First Direct Arena, the theatres, a strong hotel scene and Leeds Bradford Airport.",
   "And the trade runs the full range of sizes. Big national and regional attractions, arenas and hotel groups run large, seasonal teams and buy centrally, while independent activity centres, heritage sites, tour operators and guides need just a few branded pieces. A workwear supplier has to kit the big attraction and the one-person guide alike, which is why we run trade accounts and direct online ordering side by side.",
  ],
  "kit_loc":"across the city's attractions, parks and visitor sites",
  "s2_intro":"Whether you are a major Leeds attraction or arena, a heritage site or a small independent activity centre toward Pudsey",
 },
}

def _load_extra_towns():
    """Fix 2: merge per-batch towns/*.json into TOWNS (research agents write these)."""
    here = os.path.dirname(os.path.abspath(__file__)); d = os.path.join(here, 'towns')
    if not os.path.isdir(d): return
    for fn in sorted(os.listdir(d)):
        if fn.endswith('.json'):
            with open(os.path.join(d, fn), encoding='utf-8') as fh:
                for k, v in json.load(fh).items():
                    TOWNS[k.lower()] = v
_load_extra_towns()

_CSV=None
def _load_csv():
    global _CSV
    if _CSV is not None: return _CSV
    here=os.path.dirname(os.path.abspath(__file__))
    for p in (os.path.join(here,'TL_towns.csv'),'TL_towns.csv','/mnt/user-data/outputs/TL_towns.csv'):
        if os.path.exists(p):
            rows=[]
            with open(p,newline='',encoding='utf-8-sig') as f:
                for r in csv.DictReader(f): rows.append((int(r["Rank"]), r["Town"].strip(), (r.get("Nation") or "").strip()))
            _CSV=rows; return _CSV
    _CSV=[]; return _CSV

def slugify(name):
    return re.sub(r'-+','-', re.sub(r"[^a-z0-9]+","-", name.lower().replace("&"," and "))).strip('-')

# Fix 3: slug-robust display name + entry lookup (Newcastle upon Tyne, Stoke-on-Trent,
# Houghton le Spring, Bishop's Stortford etc must render and match correctly).
_DISPLAY=None
def _display_map():
    global _DISPLAY
    if _DISPLAY is None: _DISPLAY={slugify(t): t for (_r,t,_n) in _load_csv()}
    return _DISPLAY
def town_display(key):
    return _display_map().get(slugify(key)) or ' '.join(w.capitalize() for w in str(key).split())
def _entry(town):
    s=slugify(town)
    for k,v in TOWNS.items():
        if slugify(k)==s: return v
    raise KeyError(town)

def require_nearby(town, T):
    nb = T.get("nearby")
    if not nb or len(nb) < 3:
        raise ValueError(f"{town}: 'nearby' must list 3 geographically-close towns "
                         f"(web-verified, all on TL_towns.csv). No rank/auto fallback.")
    bad = [n for n in nb if not any(r[1].lower()==n.lower() for r in _load_csv())]
    if bad:
        raise ValueError(f"{town}: nearby town(s) not on TL_towns.csv: {bad}")
    return nb[:3]

def build_title(town):
    for t in (f"{town} Travel, Tourism and Leisure Workwear",
              f"{town} Tourism and Leisure Workwear", f"{town} Tourism Workwear"):
        if len(t) <= 60: return t
    return f"{town} Tourism Workwear"

def build_meta(town):
    for m in (f"Branded polos, fleeces, softshells, waterproofs and hi-vis for {town} tourism, theme parks and attractions - trade or direct, in-house embroidery.",
              f"Branded polos, fleeces, softshells and hi-vis for {town} theme parks, attractions and activity centres - trade or direct, in-house embroidery.",
              f"Branded tourism and leisure workwear for {town} attractions - polos, fleeces, softshells and hi-vis, trade accounts or order direct online.",
              f"Branded workwear for {town} theme parks and attractions - polos, fleeces, softshells and hi-vis, trade or direct, in-house embroidery."):
        if len(m) <= 160: return m
    return f"Branded tourism workwear for {town} attractions - polos, fleeces, softshells, hi-vis, trade or direct online."

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
        "name":f"Travel, Tourism and Leisure Workwear Supply and Embroidery in {town}",
        "serviceType":"Travel, tourism and leisure workwear and embroidery supply",
        "provider":{"@id":"https://www.ineedworkwear.com/#organization"},
        "areaServed":[{"@type":"City","name":town}]+[{"@type":"City","name":n} for n in nearby],
        "audience":{"@type":"BusinessAudience","name":"Theme parks, holiday parks, activity centres, tourist attractions and tour operators"},
        "description":f"Branded polos, fleeces, softshells, waterproofs and hi-vis supplied to tourism and leisure operators in {town}, on a trade account or direct online, with in-house embroidery.",
        "hasOfferCatalog":{"@type":"OfferCatalog","name":"Travel, Tourism and Leisure Workwear",
            "itemListElement":[{"@type":"Offer","itemOffered":{"@type":"Product","name":p}} for p in TL_PRODUCTS]}}
    crumb = {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Home","item":DOMAIN},
        {"@type":"ListItem","position":2,"name":"Travel, Tourism and Leisure Workwear","item":f"{DOMAIN}/travel-tourism-leisure-workwear"},
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
    snap    = T.get("snapshot") or SNAP_TMPL.format(t=town)
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

    emb_svg   = EMB.replace('a London tourism logo', f'a {town} tourism logo')
    # attraction sign (signpost slot): swap aria, the big WELCOME TO {town} text, and caption
    sign_svg  = SIGNPOST.replace('London tourism and attractions welcome sign', f'{town} tourism and attractions welcome sign')
    sign_svg  = re.sub(r'<text x="230" y="120".*?</text>', sign_town(town), sign_svg, flags=re.S)
    sign_svg  = sign_svg.replace('every kind of London attraction', f'every kind of {town} attraction')
    # premises (aeroplane slot): swap aria and caption
    prem_svg  = PREMISES.replace('serving operators across London', f'serving operators across {town}')
    prem_svg  = prem_svg.replace('serving visitors across London', f'serving visitors across {town}')

    H=[build_head(town, slug, faqs, nearby), HEADER]
    H.append(f'<div class="tl-hero"><div class="tl-wrap"><div class="tl-subtitle">Branded Workwear for Travel, Tourism and Leisure</div><h1>{town} Travel, Tourism and Leisure Workwear</h1></div></div>')
    H.append('<div class="tl-pulse"></div>')
    H.append(f'<div class="tl-trust-strip"><p>{trust}</p></div>')
    H.append(f'<div class="tl-wrap"><div class="tl-snapshot"><div class="tl-snapshot-label">Supplier Snapshot</div><p>{snap}</p></div></div>')
    H.append(STATS)
    H.append('<div class="tl-cta-bar"><a href="https://www.ineedworkwear.com" class="tl-cta-btn">Browse Travel, Tourism and Leisure Workwear</a></div>')
    H.append('<div class="tl-jump-links"><a href="#range">Workwear Range</a><a href="#contract">The Kit</a><a href="#accounts">Ordering and Accounts</a><a href="#order">How to Order</a></div>')
    H.append(GARMENT)
    H.append(f'<div class="tl-section"><div class="tl-wrap"><h2>{s1head}</h2>'+''.join(f'<p>{p}</p>' for p in s1ps)+'</div></div>')
    H.append(f'<div class="tl-section" id="range"><div class="tl-wrap"><h2>Travel, Tourism and Leisure Workwear Range</h2><p>{s2intro} <a href="https://www.ineedworkwear.com">Browse the full range at iNeedWorkwear.com</a>.</p><p class="tl-btn-center"><a href="https://www.ineedworkwear.com" class="tl-section-btn">Browse The Range</a></p>{grid}</div></div>')
    H.append(f'<div class="tl-section"><div class="tl-wrap"><h2>Branding for a Theme Park, a Holiday Park or an Independent Attraction</h2>'+''.join(f'<p>{p}</p>' for p in emb)+'</div></div>')
    H.append(emb_svg)
    H.append(f'<div class="tl-wrap"><div class="tl-contract" id="contract"><h3>{CON_HEAD}</h3>'+''.join(f'<p>{p}</p>' for p in con)+'</div></div>')
    H.append(sign_svg)
    H.append(f'<div class="tl-section" id="accounts"><div class="tl-wrap"><h2>{ACC_HEAD}</h2>'+''.join(f'<p>{p}</p>' for p in acc)+'</div></div>')
    H.append(prem_svg)
    H.append(f'<div class="tl-section"><div class="tl-wrap"><h2>Why Tourism and Leisure Operators Choose iNeedWorkwear</h2>'+''.join(f'<p>{p}</p>' for p in why)+'</div></div>')
    H.append(ORDER)
    H.append(f'<div class="tl-section" id="order"><div class="tl-wrap"><h2>How to Order Travel, Tourism and Leisure Workwear</h2><p>{ordr[0]}</p><p>{ordr[1]}</p><p>{ordr[2]}</p><p class="tl-btn-center"><a href="https://www.ineedworkwear.com" class="tl-section-btn">Browse And Order Online</a></p><p>{selfp}</p>'+CONTACT+'</div></div>')
    faq_html=''.join(f'<div class="tl-faq-item"><div class="tl-faq-q">{q}</div><div class="tl-faq-a">{a}</div></div>' for q,a in faqs)
    H.append(f'<div class="tl-faq"><div class="tl-wrap"><h2>Travel, Tourism and Leisure Workwear FAQ</h2>{faq_html}</div></div>')
    H.append(f'<div class="tl-wrap"><div class="tl-workwear">{sorted_}</div></div>')
    nb_links=''.join(f'<a href="tl-{slugify(n)}.html">Travel, tourism and leisure workwear in {n}</a>\n' for n in nearby)
    H.append(f'<div class="tl-nearby"><div class="tl-wrap"><h3>Travel, Tourism and Leisure Workwear in Nearby Towns</h3><div class="tl-nearby-links">{nb_links}</div></div></div>')
    H.append(FOOTER+'\n</body></html>')
    return '\n'.join(H)

def main():
    args=[a for a in sys.argv[1:]]
    # Fix 1: output-dir fallback (the hardcoded /mnt/user-data/outputs is absent on a fresh checkout).
    outdir=(os.environ.get('TL_OUTDIR')
            or ('/mnt/user-data/outputs' if os.path.isdir('/mnt/user-data/outputs') else 'outputs'))
    os.makedirs(outdir, exist_ok=True)
    town_slugs={slugify(k) for k in TOWNS}
    if not args:
        args=[t for t in TOWNS if slugify(t)!='london']
    for arg in args:
        s=slugify(arg)
        if s=='london': continue
        if s not in town_slugs:
            print(f"SKIP {arg}: not in TOWNS (must be web-researched first)"); continue
        town=town_display(arg)
        slug=f"tl-{s}"
        html=assemble(slug, town)
        path=os.path.join(outdir, f"{slug}.html")
        open(path,'w',encoding='utf-8').write(html)
        print(f"WROTE {path}  ({len(html.split())} words approx)")

if __name__=='__main__':
    main()
