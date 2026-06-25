#!/usr/bin/env python3
# VT (Veterinary & Animal Care) series builder v1.0  - read SPEC.md / CLAUDE.md
# SELF-CHECKOUT / Template B (small-biz: vet practices, kennels, catteries,
# groomers, equine - mostly small businesses/sole traders). Order direct online,
# no account; trade account secondary for larger practice/group. DIFFERENTIATOR =
# TWO ENVIRONMENTS: clinical (scrubs/tunics/polos) + hands-on/outdoor (fleeces/
# waterproofs/safety shoes/wellingtons). Lead = SCRUBS + POLO + FLEECE. LOW depth,
# LOW local variation (generic shared paras in OWNER/PRESENT/NARROW pools, not in
# per-town s1loc). Headroom from the start: cards pooled 3 ways (build_grid),
# FAQ/WHY/PRESENT/NARROW at 6 variants. Exactly 14 .com + 1 community per page.
# No JS, no HTML entities, no delivery claims. Nearby = geographic, on VT_towns.csv.
import re, os, json, sys, csv
import hashlib
def pick(key, salt, n):
    h = hashlib.md5((salt + '|' + str(key).lower()).encode()).digest()
    return int.from_bytes(h[:4], 'big') % n

def _find_base():
    here = os.path.dirname(os.path.abspath(__file__))
    for p in (os.path.join(here,'vt-london.html'),'vt-london.html',
              '/mnt/user-data/outputs/vt-london.html','/home/claude/vtkit/vt-london.html'):
        if os.path.exists(p): return p
    sys.exit("ERROR: vt-london.html (base template) not found beside vt_build.py")

BASE = open(_find_base(), encoding='utf-8').read()
DOMAIN = 'https://www.ineedworkwear.uk'

def between(start, end, src=BASE):
    i = src.index(start); j = src.index(end, i+len(start)); return src[i:j]
def aria_block(aria):
    k = BASE.index(aria)
    i = BASE.rfind('<div class="vt-wrap"><div class="vt-illust">', 0, k)
    j = BASE.index('</div></div></div>', k) + len('</div></div></div>')
    return BASE[i:j]

CSS      = between('<style>', '</style>') + '</style>'
HEADER   = between('<div class="vt-header">', '\n<div class="vt-hero">')
STATS    = between('<div class="vt-stats">', '\n<div class="vt-cta-bar">')
GARMENT  = between('<div class="vt-wrap"><div class="vt-illust"><div class="vt-garment-row">', '\n<div class="vt-section">')
EMB      = aria_block('Embroidery machine stitching')
SIGNPOST = aria_block('veterinary and animal care signpost')
PREMISES = aria_block('serving vets and animal care across')
ORDER    = aria_block('Order veterinary and animal care workwear online')
CONTACT  = BASE[BASE.index('<div class="vt-contact-block">'):
                BASE.index('</div></div></div>', BASE.index('<div class="vt-contact-block">'))+len('</div></div></div>')]
FOOTER   = BASE[BASE.index('<footer class="vt-footer">'):BASE.index('</footer>')+len('</footer>')]

def signpost_town(town):
    n = len(town)
    size = 22 if n <= 8 else 19 if n <= 11 else 16 if n <= 15 else 13 if n <= 20 else 11
    tl = ' textLength="200" lengthAdjust="spacingAndGlyphs"' if n > 11 else ''
    return (f'<text x="230" y="62" text-anchor="middle" font-family="Arial,sans-serif" '
            f'font-weight="800" font-size="{size}" fill="#fff"{tl}>{town.upper()}</text>')

VT_PRODUCTS = ["Veterinary Scrubs","Tunics and Vet Nurse Tops","Polo Shirts and T-Shirts",
 "Fleeces and Mid-Layers","Waterproofs and Outdoor Jackets","Safety Shoes and Wellingtons",
 "Aprons, Caps and Accessories","Embroidery, Names and ID Branding"]

def _card(n,d): return f'<div class="vt-product-card"><div class="vt-product-name">{n}</div><div class="vt-product-detail">{d}</div></div>'
CARD_DETAILS=[
 ("Veterinary Scrubs",[
   "Comfortable, hard-wearing scrubs for vets and nurses, washable at the higher temperatures clinical work needs, the everyday branded layer of the consulting and operating room.",
   "Durable scrubs for vets and nurses, made to wash hot and hold up to clinical days, the core branded layer of the consulting room and theatre.",
   "Hygienic, hard-wearing scrubs for the clinical team, washable at high temperatures and comfortable across a long shift, branded with the practice name."]),
 ("Tunics and Vet Nurse Tops",[
   "Smart, practical tunics and nurse tops for clinical and reception work, easy to wash and wear, presenting the practice as professional and hygienic to every owner.",
   "Easy-care tunics and vet nurse tops for clinical and front-desk work, smart and washable, keeping the practice looking professional and hygienic.",
   "Practical tunics and nurse tops for nursing and reception, comfortable for a full shift and quick to wash, branded to keep the team consistent."]),
 ("Polo Shirts and T-Shirts",[
   "Branded polos and t-shirts for reception, animal care and grooming staff, breathable and durable, the everyday uniform across the practice, kennels and salon.",
   "Breathable, durable branded polos and t-shirts for reception, animal care and grooming teams, the go-to everyday layer across practice, kennels and salon.",
   "Hard-wearing branded polos and t-shirts for front-of-house, animal care and grooming staff, the dependable daily uniform from the desk to the kennels."]),
 ("Fleeces and Mid-Layers",[
   "Warm, branded fleeces and mid-layers for cold kennels, early starts and outdoor work, worn over scrubs or a polo through the colder months.",
   "Branded fleeces and mid-layers for cold kennels and early mornings, an easy warm layer over scrubs or a polo when the work moves outdoors.",
   "Cosy, branded fleeces and mid-layers for chilly kennels, yards and early starts, layered over scrubs or a polo through the colder months."]),
 ("Waterproofs and Outdoor Jackets",[
   "Waterproof jackets and trousers for kennels, yards, stables and large-animal and equine work, keeping staff dry and presentable in all weather and out in the field.",
   "Waterproof jackets and trousers for the wet side of the job - kennels, yards, stables, equine and large-animal work - keeping staff dry and presentable outdoors.",
   "Weatherproof jackets and trousers for kennels, stables, equine and large-animal work, built to keep staff dry and smart through wash-downs and out in the field."]),
 ("Safety Shoes and Wellingtons",[
   "Supportive safety shoes for clinical floors and wellingtons for kennels, yards and stables, with grip and protection for muck, paws, hooves and long days on your feet.",
   "Safety shoes for clinical floors and wellingtons for the yard and kennels, with grip and protection for muck, paws and hooves through long days on your feet.",
   "Grippy safety shoes for the practice floor and wellingtons for kennels, stables and yards, protecting feet from muck, paws and hooves across a long shift."]),
 ("Aprons, Caps and Accessories",[
   "Grooming and handling aprons, caps and accessories to finish the kit, embroidered to match the scrubs, polos and fleeces across the team.",
   "Grooming and handling aprons, caps and accessories to round out the kit, embroidered to tie in with the scrubs, polos and fleeces.",
   "Aprons for grooming and handling, plus caps and accessories, embroidered to match the rest of the uniform across the team."]),
 ("Embroidery, Names and ID Branding",[
   "In-house embroidery of your practice name, logo and staff names onto scrubs, tunics, polos and fleeces, so a small practice or a mobile groomer looks consistent and professional.",
   "In-house embroidery of your practice name, logo and staff names across scrubs, tunics, polos and fleeces, so a small practice or mobile groomer always looks consistent.",
   "Practice name, logo and staff names embroidered in-house onto scrubs, tunics, polos and fleeces, so a single van or a small team looks coordinated and professional."]),
]
GRID_ORDER=[(0,1,2,3,4,5,6,7),(1,0,2,3,4,5,6,7),(0,1,2,4,3,5,6,7),(0,2,1,3,4,5,6,7)]
def build_grid(town):
    order = GRID_ORDER[pick(town,'gord',len(GRID_ORDER))]
    cards=[]
    for i in order:
        name,variants = CARD_DETAILS[i]
        cards.append(_card(name, variants[pick(town,f'g{i}',len(variants))]))
    return '<div class="vt-product-grid">'+''.join(cards)+'</div>'

TRUST_POOL=[
 "Branded scrubs, tunics, polos, fleeces and waterproofs for vets, kennels, catteries and equine - order direct online across the UK",
 "Branded scrubs, tunics, polos, fleeces and waterproofs for vets, kennels, catteries and equine - order direct online, no account needed, UK-wide",
 "Trusted by vet practices, kennels, catteries and equine yards across the UK for branded scrubs, polos and fleeces, ordered direct online",
 "Branded workwear - scrubs, tunics, polos, fleeces and waterproofs - for vets, kennels, catteries and equine across the UK, ordered direct online",
]
S2INTRO_POOL=[
 "Whether you are an independent vet practice, a boarding kennels or cattery, a dog groomer or an equine yard in {t}, the range is built to kit you from one place: scrubs, tunics and polos for the clinical side, then fleeces, waterproofs and footwear for the kennels, yard and field.",
 "An independent {t} practice, a boarding kennels or cattery, a dog groomer or an equine yard is kitted from one place: scrubs, tunics and polos for the clinical side, then fleeces, waterproofs and footwear for the kennels, yard and field.",
 "For a {t} vet practice, kennels, cattery, groomer or equine yard, the range covers you from one place: scrubs, tunics and polos for the consulting room, then fleeces, waterproofs and footwear for the kennels, yard and field.",
 "Whether it is an independent practice, a kennels or cattery, a groomer or an equine yard in {t}, you are kitted from one place: scrubs, tunics and polos for the clinical side, plus fleeces, waterproofs and footwear for the kennels, yard and field.",
]
EMB_P1_POOL=[
 "In animal care, an owner is trusting you with a member of the family, and how the team looks is part of how that trust is earned. A clean, branded scrub top or polo tells a {t} owner the practice is organised, professional and serious about the care it gives, and it turns a sole trader or a small business into a recognisable, established name rather than someone improvising.",
 "In animal care, an owner is handing over a member of the family, and how the team looks is part of earning that trust. A clean, branded scrub top or polo tells a {t} owner the practice is organised, professional and serious about its care, turning a sole trader or small business into a recognisable name rather than someone improvising.",
 "An owner trusting you with their animal is trusting you with family, and how the team looks is part of how that trust is built. A clean, branded scrub top or polo signals to a {t} owner that the practice is organised and serious, and makes a sole trader or small business look established rather than improvised.",
 "In animal care the bond is personal, and how the team presents is part of how an owner decides to trust you. A clean, branded scrub top or polo tells a {t} owner the practice is professional and serious about its care, and turns a sole trader or small business into a recognisable, established name.",
]
EMB_P2_POOL=[
 "We brand in-house, which means your practice or business name and logo are embroidered onto scrubs, tunics, polos and fleeces, finished to survive the frequent, hot washing clinical and animal work demands. Send your artwork once, we hold it on file, and every reorder, new nurse and new kennel hand matches the last, so whether it is one van or a small team, the {t} business looks consistent.",
 "Branding is done in-house onto scrubs, tunics, polos and fleeces - your practice name and logo embroidered and finished to survive the frequent, hot washing clinical and animal work demands. We hold your artwork on file, so every reorder, new nurse and kennel hand matches, and whether it is one van or a small team, the {t} business looks consistent.",
 "Your practice or business name and logo are embroidered in-house onto scrubs, tunics, polos and fleeces, finished to take the frequent, hot washing this work demands. Held on file, your artwork reproduces on every reorder, new nurse and kennel hand, so a {t} business looks consistent whether it is one van or a small team.",
 "We badge in-house, embroidering your practice name and logo onto scrubs, tunics, polos and fleeces and finishing them to survive frequent, hot washing. Held on file, your branding matches on every reorder and new starter, so a {t} business looks consistent whether it is a single van or a small team.",
]
EMB_P3_POOL=[
 "For a growing practice, that consistency matters as the team changes. We hold your branding and sizes on file, so kitting a new starter, taking on a nurse or opening a second site reproduces the same branded uniform every time, without anyone having to re-supply artwork or guess at a match.",
 "For a practice that is growing, consistency matters as the team changes. We hold your branding and sizes on file, so a new starter, a nurse or a second site comes back the same branded uniform every time, with no artwork to re-supply.",
 "As a practice grows and the team changes, consistency matters. We keep your branding and sizes on file, so kitting a new starter, taking on a nurse or opening a second site reproduces the same branded uniform each time.",
 "For a growing practice, that consistency is the value as the team changes. We hold branding and sizes on file, so a new starter, a nurse or a second site reproduces exactly the same branded uniform every time, with nothing to re-supply.",
]
CON_HEAD="From the Consulting Room to the Kennels and Yard"
CON_P1_POOL=[
 "Veterinary and animal care workwear has to cover two very different jobs, and a good supplier handles both from one place. The first is clinical. In the consulting and operating room, the uniform is about hygiene and professionalism: scrubs and tunics that wash at high temperatures, keep their shape and present a {t} vet or nurse as clean, capable and reassuring to a worried owner. This is the side an owner sees, and it carries the trust the practice runs on.",
 "Veterinary and animal care workwear does two very different jobs, and a good supplier covers both from one place. First, the clinical side: in the consulting and operating room the uniform is about hygiene and professionalism, with scrubs and tunics that wash hot, keep their shape and present a {t} vet or nurse as clean, capable and reassuring. This is what an owner sees, and it carries the practice's trust.",
 "Animal care workwear has to do two very different jobs, and the right supplier handles both together. The first is clinical: in the consulting and operating room the uniform is about hygiene and professionalism, with scrubs and tunics that wash at high temperatures, hold their shape and present a {t} vet or nurse as clean and reassuring to a worried owner, carrying the trust the practice runs on.",
 "Veterinary and animal care workwear covers two very different jobs, and a good supplier does both from one place. The first is clinical. In the consulting and operating room, the uniform is hygiene and professionalism: scrubs and tunics that wash hot, hold their shape and present a {t} vet or nurse as clean, capable and reassuring to an anxious owner, the side an owner sees and the one that carries trust.",
]
CON_P2_POOL=[
 "The second is hands-on and outdoor. The same business, or the one next door, spends its day in kennels, catteries, grooming rooms, stables and fields. That calls for warmth and weatherproofing: fleeces for cold early starts, waterproof jackets and trousers for the wet and the wash-down, and safety shoes or wellingtons for muck, claws and hooves. It is physical, messy work, and the kit has to take it.",
 "The second is hands-on and outdoor. The same business, or the one next door, works in kennels, catteries, grooming rooms, stables and fields. That needs warmth and weatherproofing: fleeces for cold early starts, waterproof jackets and trousers for the wet and the wash-down, and safety shoes or wellingtons for muck, claws and hooves. It is physical, messy work, and the kit is built for it.",
 "The second job is hands-on and outdoor. The same business, or its neighbour, spends the day in kennels, catteries, grooming rooms, stables and fields, which calls for warmth and weatherproofing: fleeces for cold starts, waterproof jackets and trousers for the wet and the wash-down, and safety shoes or wellingtons for muck, claws and hooves. It is messy, physical work, and the kit has to cope.",
 "The second is the hands-on, outdoor side. The same business, or the one next door, is in kennels, catteries, grooming rooms, stables and fields all day. That means warmth and weatherproofing: fleeces for cold early starts, waterproofs for the wet and the wash-down, and safety shoes or wellingtons for muck, claws and hooves - physical, messy work the kit has to take.",
]
CON_P3_POOL=[
 'Most animal care businesses live somewhere between the two, and the value is having one supplier for both sides, all branded the same. We hold your {t} practice name, logo and sizes on file and supply the clinical and the outdoor kit together, so kitting a new nurse, a kennel hand or a groomer reproduces the same branded uniform every time. Browse the range at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
 'Most animal care businesses sit somewhere between the two, and the value is one supplier for both sides, all branded the same. We hold your {t} practice name, logo and sizes on file and supply the clinical and outdoor kit together, so kitting a new nurse, kennel hand or groomer reproduces the same branded uniform every time. Browse the range at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
 'Most animal care businesses live between the two, and the value is having one supplier for both sides, branded the same. We keep your {t} practice name, logo and sizes on file and supply the clinical and the outdoor kit together, so a new nurse, kennel hand or groomer comes back the same branded uniform every time. Browse the range at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
 'Most animal care businesses straddle the two, and the value is one supplier for both, all branded the same. We hold your {t} practice name, logo and sizes on file and supply the clinical and outdoor kit together, so kitting a new nurse, a kennel hand or a groomer reproduces the same uniform every time. Browse the range at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
]
ACC_HEAD="How to Order: Direct, Online, No Account Needed"
ACC_P1_POOL=[
 "Veterinary and animal care is mostly small practices, kennels and sole traders, so we have built ordering to suit exactly that. The quickest route, and the one most {t} businesses use, is to order direct online with no account at all. Browse the range, pick your scrubs, tunics, polos, fleeces or waterproofs, choose your sizes, send your logo once and check out. There is no minimum, no setup and nothing to manage, and your kit is dispatched on standard lead times with embroidery added in-house first.",
 "Veterinary and animal care is mostly small practices, kennels and sole traders, and ordering is built for exactly that. The quickest route, and the one most {t} businesses use, is direct online with no account: browse the range, pick your scrubs, tunics, polos, fleeces or waterproofs, choose sizes, send your logo once and check out. No minimum, no setup, nothing to manage, dispatched on standard lead times with embroidery in-house first.",
 "Because the trade is mostly small practices, kennels and sole traders, ordering is built to match. The quickest route, used by most {t} businesses, is to order direct online with no account: browse, pick your scrubs, tunics, polos, fleeces or waterproofs, choose sizes, send your logo once and check out. There is no minimum and no setup, and kit is dispatched on standard lead times with embroidery in-house first.",
 "Veterinary and animal care is mostly small practices, kennels and sole traders, and ordering is built for that. The quickest route, and the one most {t} businesses use, is direct online with no account at all: browse the range, pick your scrubs, tunics, polos, fleeces or waterproofs, choose sizes, send your logo once and check out, with no minimum and nothing to manage, dispatched on standard lead times.",
]
ACC_P2_POOL=[
 "It suits the way an animal care business actually buys. A new practice kitting its first nurses, a mobile groomer wanting a few branded polos and a fleece, or an established kennels topping up waterproofs and replacing worn wellingtons can all order in a few minutes and get exactly what they need. We hold your logo on file once you have ordered, so the next order matches the last without you re-sending artwork.",
 "It fits the way an animal care business really buys. A new practice kitting its first nurses, a mobile groomer after a few branded polos and a fleece, or a kennels topping up waterproofs and replacing wellingtons can all order in a few minutes and get exactly what they need. We hold your logo on file once you order, so the next order matches without re-sending artwork.",
 "It matches how an animal care business actually buys. A new practice kitting its nurses, a mobile groomer wanting a couple of polos and a fleece, or a kennels topping up waterproofs and wellingtons can each order in minutes and get just what they need. We keep your logo on file after the first order, so the next one matches without re-sending artwork.",
 "It suits how an animal care business buys in practice. A new practice kitting its first nurses, a mobile groomer wanting a few polos and a fleece, or a kennels replacing worn waterproofs and wellingtons can all order in a few minutes and get exactly what they need. Your logo is held on file once you order, so the next order matches without re-sending artwork.",
]
ACC_P3_POOL=[
 "For a larger practice, a veterinary group or a multi-site operator, a trade account is there if you want it. It adds managed reordering, agreed pricing and a held kit list so new starters and second sites are kitted consistently, but it is an option rather than a requirement, and most small practices in {t} never need one.",
 "For a larger practice, a veterinary group or a multi-site operator, a trade account is available if you want it: managed reordering, agreed pricing and a held kit list so new starters and second sites stay consistent. It is an option, not a requirement, and most small {t} practices never need one.",
 "A larger practice, a veterinary group or a multi-site operator can set up a trade account if they want one, adding managed reordering, agreed pricing and a held kit list for new starters and second sites. It is optional rather than required, and most small {t} practices never need it.",
 "For a larger practice, a group or a multi-site operator, a trade account is there if it helps: managed reordering, agreed pricing and a held kit list so new starters and second sites are kitted consistently. It is an option, not a requirement, and most small {t} practices never use one.",
]
ACC_P4_POOL=[
 'Order direct online with no account at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>, or set up a trade account for a larger practice or group at <a href="https://www.ineedworkwear.com">iNeedWorkwear</a>.',
 'Order direct online with no account at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>. For a larger practice or group, set up a trade account at <a href="https://www.ineedworkwear.com">iNeedWorkwear</a>.',
 'Browse and order direct online with no account at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>, or open a trade account for a larger practice or group at <a href="https://www.ineedworkwear.com">iNeedWorkwear</a>.',
 'Order direct with no account at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>, or for a larger practice or group set up a trade account at <a href="https://www.ineedworkwear.com">iNeedWorkwear</a>.',
]
WHY_P1_POOL=[
 "A vet practice, kennels, cattery or grooming business in {t} whose team turns out in clean, branded scrubs, polos and fleeces looks professional and trustworthy to every owner who walks in, and iNeedWorkwear supplies that whole look from a single place, branded in-house and ordered direct online, so even a sole trader gets a polished, established identity without any fuss.",
 "A {t} vet practice, kennels, cattery or grooming business whose team wears clean, branded scrubs, polos and fleeces looks professional and trustworthy to every owner, and iNeedWorkwear supplies that whole look from one place, branded in-house and ordered direct online, so even a sole trader gets a polished, established identity without fuss.",
 "When a {t} practice, kennels, cattery or grooming business turns its team out in clean, branded scrubs, polos and fleeces, it looks professional and trustworthy to every owner who walks in, and we supply that whole look from a single place, branded in-house and ordered direct online, so even a sole trader gets a polished identity without fuss.",
 "A practice, kennels, cattery or grooming business in {t} whose team wears clean, branded scrubs, polos and fleeces reads as professional and trustworthy to every owner through the door, and we supply that whole look from one place, branded in-house and ordered direct online, so even a sole trader gets a polished, established identity.",
 "A {t} vet practice, kennels or grooming business whose staff turn out in clean, branded scrubs, polos and fleeces looks established and trustworthy to every owner, and we supply the whole look from one place, branded in-house and ordered direct online, so a sole trader gets chain-grade polish without the overhead.",
 "In {t}, a practice, kennels, cattery or grooming business whose team wears clean, branded scrubs, polos and fleeces looks professional from the first glance, and iNeedWorkwear supplies that whole look from one place, branded in-house and ordered direct online, so even a single van carries a polished, established identity.",
]
WHY_P2_POOL=[
 "Everything comes from the same place, which matters when a business spans two environments. The supplier that embroiders your clinical scrubs and tunics also supplies your fleeces, waterproofs and wellingtons for the kennels and yard, so the consulting room and the outdoor side are kitted from one order and the whole team matches, with nothing falling through the gap.",
 "It all comes from one place, which matters when a business spans two environments. The supplier embroidering your clinical scrubs and tunics also supplies the fleeces, waterproofs and wellingtons for the kennels and yard, so the consulting room and the outdoor side are kitted in one order and the team matches, with nothing falling through the gap.",
 "Everything is from the same supplier, which counts when a business works in two environments. The same place that embroiders your scrubs and tunics supplies your fleeces, waterproofs and wellingtons for the kennels and yard, so clinical and outdoor are kitted together and the whole team matches.",
 "It comes from one supplier, which matters across two environments. Whoever embroiders your clinical scrubs and tunics also supplies the fleeces, waterproofs and wellingtons for the kennels and yard, so the consulting room and the outdoor side are kitted from a single order and the team stays matched.",
 "One supplier covers both sides, which matters when the work spans two environments. The team that embroiders your scrubs and tunics also supplies the fleeces, waterproofs and wellingtons for kennels and yard, so clinical and outdoor kit arrive together and the whole practice matches.",
 "Because it all comes from one place, the two environments stay joined up. The supplier embroidering your clinical scrubs and tunics supplies the fleeces, waterproofs and wellingtons for the kennels and yard too, so the consulting room and the outdoor side match and nothing falls through the gap.",
]
WHY_P3_POOL=[
 "The range is deliberately narrow and built around what animal care actually wears: scrubs, tunics, polos, fleeces, waterproofs and footwear, the everyday kit of the practice and the yard. That practical focus keeps choosing, ordering and reordering quick and simple for a busy small business.",
 "The range is deliberately narrow, built around what animal care really wears: scrubs, tunics, polos, fleeces, waterproofs and footwear, the everyday kit of the practice and the yard. That focus keeps choosing, ordering and reordering quick and simple for a busy small business.",
 "Everything in the range reflects what animal care genuinely wears: scrubs, tunics, polos, fleeces, waterproofs and footwear, the daily kit of the practice and the yard. The range is deliberately narrow, so ordering and reordering stay quick for a busy small business.",
 "The range is kept deliberately narrow around what animal care actually wears: scrubs, tunics, polos, fleeces, waterproofs and footwear, the everyday kit of the practice and the yard, so choosing and reordering stay quick and simple for a busy small business.",
 "It is a deliberately narrow range built on what animal care really wears: scrubs, tunics, polos, fleeces, waterproofs and footwear, the everyday kit of practice and yard, which keeps choosing, ordering and reordering fast for a busy small business.",
 "The range stays narrow on purpose, mapped to what animal care wears day to day: scrubs, tunics, polos, fleeces, waterproofs and footwear, the kit of the practice and the yard, so a busy small business can choose and reorder in minutes.",
]
WHY_P4_POOL=[
 "And the ordering fits the trade: direct online with no account for the small practice, kennels or mobile groomer, and a trade account there for the larger practice or group that wants managed reordering, so every reorder, new nurse and kennel hand matches and looks professional from their first shift.",
 "And how you order fits the trade: direct online with no account for the small practice, kennels or mobile groomer, with a trade account there for a larger practice or group wanting managed reordering, so every reorder, new nurse and kennel hand matches from their first shift.",
 "And the ordering suits the trade: direct online with no account for the small practice, kennels or mobile groomer, and a trade account for the larger practice or group that wants managed reordering, so every reorder and new starter matches from day one.",
 "And ordering fits the trade: a no-account direct route online for the small practice, kennels or mobile groomer, and a trade account for a larger practice or group wanting managed reordering, so every reorder, new nurse and kennel hand matches from their first shift.",
 "And the way you order matches the trade: direct online with no account for the small practice, kennels or groomer, with a trade account for the larger practice or group after managed reordering, so each reorder and new starter matches and looks professional from day one.",
 "And ordering is shaped to the trade: order direct online with no account if you are a small practice, kennels or mobile groomer, or run a trade account if you are a larger practice or group, so every reorder and new nurse matches from their first shift.",
]
ORD_P1_POOL=[
 "iNeedWorkwear supplies branded scrubs, tunics, polos, fleeces, waterproofs and safety footwear to vet practices, kennels, catteries, groomers and equine yards across {region}, all embroidered in-house with the practice name.",
 "We supply branded scrubs, tunics, polos, fleeces, waterproofs and safety footwear to vet practices, kennels, catteries, groomers and equine yards across {region}, all embroidered in-house with the practice name.",
 "Across {region}, iNeedWorkwear kits vet practices, kennels, catteries, groomers and equine yards in branded scrubs, tunics, polos, fleeces, waterproofs and safety footwear, all embroidered in-house with the practice name.",
 "From a single van to a small practice across {region}, iNeedWorkwear supplies branded scrubs, tunics, polos, fleeces, waterproofs and safety footwear to vets, kennels, catteries and equine yards, all embroidered in-house.",
]
ORD_P2_POOL=[
 "For a small practice, kennels or mobile groomer, ordering direct online is quickest and needs no account: browse the range, pick your scrubs, polos, fleeces or waterproofs, add your sizes, send your logo once and check out. Your kit is dispatched on standard lead times with embroidery added in-house, and your logo is held on file so the next order matches.",
 "For a small practice, kennels or mobile groomer, direct online is quickest and needs no account: browse, pick your scrubs, polos, fleeces or waterproofs, add sizes, send your logo once and check out. Your kit ships on standard lead times with embroidery in-house, and your logo is held on file so the next order matches.",
 "A small practice, kennels or mobile groomer orders quickest direct online, no account needed: browse the range, pick your scrubs, polos, fleeces or waterproofs, add sizes, send the logo once and check out. Kit is dispatched on standard lead times with in-house embroidery, and your logo is held on file for the next order.",
 "For a small practice, kennels or mobile groomer, the quickest route is direct online with no account: browse the range, pick your scrubs, polos, fleeces or waterproofs, add your sizes, send your logo once and check out, dispatched on standard lead times with embroidery in-house and your logo held on file.",
]
ORD_P3_POOL=[
 "For a larger practice, a veterinary group or a multi-site operator, a trade account adds managed reordering and agreed pricing: send your headcount, your logo and your sizes and we will build a branded uniform list and hold it on file, so new starters and second sites are kitted consistently.",
 "For a larger practice, a veterinary group or a multi-site operator, a trade account brings managed reordering and agreed pricing: send your headcount, logo and sizes and we will build a branded uniform list and hold it on file, so new starters and second sites stay consistent.",
 "A larger practice, a veterinary group or a multi-site operator can use a trade account for managed reordering and agreed pricing: send your headcount, logo and sizes and we will build a branded uniform list and hold it on file for consistent new starters and second sites.",
 "For a larger practice, a group or a multi-site operator, a trade account adds managed reordering and agreed pricing: send your headcount, logo and sizes and we will build a branded uniform list and keep it on file, so new starters and second sites are kitted consistently.",
]
SELF_POOL=[
 'Opening a practice or kennels and need kit now? Browse the full range, add your sizes and order direct on self-service checkout at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
 'Just opened a practice, kennels or grooming room? Browse the range, add sizes and order direct on self-service checkout at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
 'Setting up a practice, kennels or a grooming van and need kit today? Browse the full range, add your sizes and order direct on self-service checkout at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
 'Need a practice or kennels uniform sorted now? Browse the range, add sizes and order direct on self-service checkout at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
]
SORTED_POOL=[
 '<h3>Veterinary and Animal Care Workwear, Sorted</h3><p>From clinical scrubs and tunics to fleeces, waterproofs and wellingtons, get branded workwear built for vets, kennels, catteries and equine at fair prices - embroidered in-house with your practice name, ordered direct online with no account, or on a trade account for a larger practice.</p><p><a href="https://www.ineedworkwear.com">Browse veterinary and animal care workwear at iNeedWorkwear</a></p>',
 '<h3>Veterinary and Animal Care Workwear, Sorted</h3><p>Clinical scrubs and tunics, plus fleeces, waterproofs and wellingtons - branded workwear for vets, kennels, catteries and equine at fair prices, embroidered in-house with your practice name, ordered direct online with no account or on a trade account.</p><p><a href="https://www.ineedworkwear.com">Browse veterinary and animal care workwear at iNeedWorkwear</a></p>',
 '<h3>Veterinary and Animal Care Workwear, Sorted</h3><p>From scrubs and tunics to fleeces, waterproofs and wellingtons, kit a practice, kennels or grooming van at fair prices, embroidered in-house and ordered direct online with no account or on a trade account.</p><p><a href="https://www.ineedworkwear.com">Browse veterinary and animal care workwear at iNeedWorkwear</a></p>',
 '<h3>Veterinary and Animal Care Workwear, Sorted</h3><p>Scrubs, tunics, fleeces, waterproofs and wellingtons, the branded kit for vets, kennels, catteries and equine at fair prices, embroidered in-house and ready to order direct online with no account or on a trade account for a larger practice.</p><p><a href="https://www.ineedworkwear.com">Browse veterinary and animal care workwear at iNeedWorkwear</a></p>',
]
OWNER_POOL=[
 "That shapes what a workwear supplier needs to do. A two-vet practice, a small kennels, a mobile groomer or a one-person equine service does not have a procurement department or a buying account. They want to choose the few branded pieces they need, some scrubs, a few polos, a fleece and a waterproof, and order them quickly and simply, without setting anything up.",
 "This shapes what a workwear supplier has to do. A two-vet practice, a small kennels, a mobile groomer or a one-person equine service has no procurement department and no buying account. They want to pick the few branded pieces they need, some scrubs, a few polos, a fleece and a waterproof, and order them quickly and simply, with nothing to set up.",
 "That shapes the job for a workwear supplier. A two-vet practice, a small kennels, a mobile groomer or a one-person equine service does not have a buying department or a trade account. They want to choose the few branded pieces they need, some scrubs, a few polos, a fleece and a waterproof, and order them quickly, without setting anything up.",
 "It shapes what a supplier needs to do. A two-vet practice, a small kennels, a mobile groomer or a one-person equine service has no procurement department and no buying account, so they want to pick a few branded pieces, some scrubs, a few polos, a fleece and a waterproof, and order them quickly and simply, with nothing to set up.",
 "That shapes how a supplier should work. A small practice, a kennels, a mobile groomer or a one-person equine service has no buying department or trade account, and just wants to choose a few branded pieces, some scrubs, a few polos, a fleece and a waterproof, and order them quickly and simply, without setting anything up.",
 "This shapes what the supplier has to get right. A two-vet practice, a small kennels, a mobile groomer or a one-person equine service does not have a procurement department or a buying account, so they want to pick a few branded pieces, some scrubs, a few polos, a fleece and a waterproof, and order them quickly, with nothing to set up.",
]
PRESENT_POOL=[
 "And the work happens in two very different environments, which is what makes veterinary and animal care workwear its own thing. In the consulting room it is clinical: scrubs and tunics that wash hot, look professional and reassure a {t} owner that their animal is in clean, capable hands. Out in the kennels, the grooming room, the yard or the field it is hands-on and outdoor: fleeces for warmth, waterproofs for the wet, and safety shoes or wellingtons for muck, paws and hooves. The same business often needs both.",
 "And the work spans two very different environments, which is what makes veterinary and animal care workwear its own thing. In the consulting room it is clinical: scrubs and tunics that wash hot, look professional and reassure a {t} owner their animal is in clean, capable hands. Out in the kennels, grooming room, yard or field it is hands-on and outdoor: fleeces for warmth, waterproofs for the wet, and safety shoes or wellingtons for muck, paws and hooves. The same business often needs both.",
 "And it plays out across two very different environments, which is what sets veterinary and animal care workwear apart. In the consulting room it is clinical: scrubs and tunics that wash hot, look professional and reassure a {t} owner their animal is in clean, capable hands. Out in the kennels, grooming room, yard or field it turns hands-on and outdoor: fleeces for warmth, waterproofs for the wet, and safety shoes or wellingtons for muck, paws and hooves. One business usually needs both.",
 "And the day moves between two very different environments, which is what makes this workwear its own thing. In the consulting room it is clinical: scrubs and tunics that wash hot, look professional and reassure a {t} owner their animal is in clean, capable hands. In the kennels, grooming room, yard or field it is hands-on and outdoor: fleeces for warmth, waterproofs for the wet, and safety shoes or wellingtons for muck, paws and hooves. The same business often needs both sides.",
 "And the work runs across two very different environments, which is what makes veterinary and animal care workwear distinct. Inside, it is clinical: scrubs and tunics that wash hot, look professional and reassure a {t} owner their animal is in clean, capable hands. Outside, in the kennels, grooming room, yard or field, it is hands-on: fleeces for warmth, waterproofs for the wet, and safety shoes or wellingtons for muck, paws and hooves. The same business often needs both.",
 "And it happens in two very different environments, which is the heart of veterinary and animal care workwear. In the consulting room it is clinical: scrubs and tunics that wash hot, look professional and reassure a {t} owner their animal is in capable, hygienic hands. In the kennels, grooming room, yard or field it is hands-on and outdoor: fleeces for warmth, waterproofs for the wet, and safety shoes or wellingtons for muck, paws and hooves. Most businesses need both.",
]
NARROW_POOL=[
 "Because it is a narrow, repeat-purchase trade, the range is deliberately focused and easy to reorder. Scrubs, tunics, polos, fleeces, waterproofs and footwear, branded in-house with the practice name, are the whole kit, and we hold your logo on file so the next order, a new nurse or a new kennel hand matches what you already have without anyone in {t} starting again.",
 "Because this is a narrow, repeat-purchase trade, the range is deliberately focused and easy to reorder. Scrubs, tunics, polos, fleeces, waterproofs and footwear, branded in-house with the practice name, are the whole kit, and your logo is held on file so the next order, a new nurse or a new kennel hand matches what you already have without a {t} business starting again.",
 "Since it is a narrow, repeat-purchase trade, the range is kept deliberately focused and easy to reorder. Scrubs, tunics, polos, fleeces, waterproofs and footwear, branded in-house with the practice name, are the whole kit, and we keep your logo on file so the next order, a new nurse or kennel hand matches what you already have without a {t} business starting from scratch.",
 "Because it is a narrow, repeat-purchase trade, the range stays deliberately focused and easy to reorder. Scrubs, tunics, polos, fleeces, waterproofs and footwear, branded in-house with the practice name, are the whole kit, and your logo is held on file so the next order, a new nurse or kennel hand matches what you have without anyone in {t} starting again.",
 "As a narrow, repeat-purchase trade, the range is deliberately focused and quick to reorder. Scrubs, tunics, polos, fleeces, waterproofs and footwear, branded in-house with the practice name, are the whole kit, and we hold your logo on file so the next order, a new nurse or kennel hand matches what a {t} business already runs without starting over.",
 "Being a narrow, repeat-purchase trade, the range is kept focused and simple to reorder. Scrubs, tunics, polos, fleeces, waterproofs and footwear, branded in-house with the practice name, are the whole kit, and your logo sits on file so the next order, a new nurse or kennel hand lines up with what a {t} business already has, without starting again.",
]
KIT_POOL=[
 "Scrubs, tunics, polos, fleeces, waterproofs and footwear, branded with the practice name, are the whole kit {loc}.",
 "The whole kit is scrubs, tunics, polos, fleeces, waterproofs and footwear, branded with the practice name {loc}.",
 "Scrubs, tunics, polos, fleeces, waterproofs and footwear do the job, branded with the practice name {loc}.",
 "It comes down to scrubs, tunics, polos, fleeces, waterproofs and footwear, branded with the practice name {loc}.",
 "Scrubs, tunics, polos, fleeces, waterproofs and footwear, all branded with the practice name, are the kit {loc}.",
 "Branded scrubs, tunics, polos, fleeces, waterproofs and footwear make up the whole kit {loc}.",
]
S2TAIL_POOL=[
 ", scrubs, polos and fleeces lead, with waterproofs and footwear alongside.",
 ", the core is scrubs, polos and fleeces, with waterproofs and footwear to finish.",
 ", expect scrubs, polos and fleeces first, then waterproofs and footwear.",
 ", scrubs, polos and fleeces do the work, with waterproofs and footwear alongside.",
 ", scrubs, polos and fleeces anchor the kit, with waterproofs and footwear completing it.",
 ", it is scrubs, polos and fleeces, plus waterproofs and footwear.",
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
     (f"Do you supply branded workwear to vet practices and kennels in {t}?", P('fq1',[
      f"Yes. Vet practices, veterinary nurses, kennels, catteries, dog groomers and equine yards across {region} get branded scrubs, tunics, polos, fleeces, waterproofs and safety footwear from us, embroidered in-house with the practice name. A sole trader or small practice can order direct online with no account, and a larger practice or group can set up a trade account.",
      f"Yes. Branded scrubs, tunics, polos, fleeces, waterproofs and safety footwear go to vet practices, nurses, kennels, catteries, groomers and equine yards across {region}, embroidered in-house with the practice name. A sole trader or small practice orders direct online with no account, and a larger group can set up a trade account.",
      f"Yes. From a one-van mobile groomer to a small practice across {region}, we supply branded scrubs, tunics, polos, fleeces, waterproofs and safety footwear, embroidered in-house with the practice name, ordered direct online with no account or on a trade account for a larger practice.",
      f"Yes. Vet practices, nurses, kennels, catteries, groomers and equine yards across {region} get branded scrubs, tunics, polos, fleeces, waterproofs and safety footwear from us, embroidered in-house with the practice name, ordered direct online with no account or on a trade account.",
      f"Yes. Across {region} we kit vet practices, nurses, kennels, catteries, groomers and equine yards in branded scrubs, tunics, polos, fleeces, waterproofs and safety footwear, embroidered in-house with the practice name, ordered direct online with no account or on a trade account for a larger practice.",
      f"Yes. Animal care businesses across {region}, from a single van to a small practice, get branded scrubs, tunics, polos, fleeces, waterproofs and safety footwear from us, embroidered in-house with the practice name, with no account needed to order."])),
     ("Can I order without setting up a trade account?", P('fq2',[
      "Yes. Veterinary and animal care is mostly small practices, kennels and sole traders, so the quickest route is to order direct online with no account: browse the range, pick your scrubs, tunics, polos, fleeces or waterproofs, add your sizes, send your logo once and check out. A trade account is there for a larger practice or group that wants managed reordering.",
      "Yes. The trade is mostly small practices, kennels and sole traders, so the quickest route is direct online with no account: browse, pick your scrubs, tunics, polos, fleeces or waterproofs, add sizes, send your logo once and check out. A trade account is there for a larger practice or group that wants managed reordering.",
      "Yes, no account needed. Most of the trade orders direct online: pick your scrubs, tunics, polos, fleeces or waterproofs, add sizes, send the logo once and check out, with a trade account available for a larger practice or group that wants managed reordering.",
      "Yes. Most businesses order direct online with no account: browse the range, pick your scrubs, tunics, polos, fleeces or waterproofs, add sizes and send your logo once. A trade account is there for a larger practice or group that wants managed reordering.",
      "Yes. The trade is mostly small practices, kennels and sole traders, so direct online with no account is the quickest route: browse, pick your scrubs, polos, fleeces or waterproofs, add sizes, send the logo once and check out. A trade account suits a larger practice or group wanting managed reordering.",
      "Yes, ordering needs no account. Browse the range, pick your scrubs, tunics, polos, fleeces or waterproofs, add sizes and send your logo once, which is how most practices order. A trade account stays available for a larger practice or group wanting managed reordering."])),
     ("What workwear does a vet practice or animal care business need?", P('fq3',[
      "The core kit is scrubs and tunics for clinical and nursing work, polos for reception and animal care staff, fleeces for warmth in kennels and yards, waterproofs for outdoor and large-animal work, and safety shoes or wellingtons, all branded with the practice name. The range covers both the consulting room and the kennels, yard or field.",
      "The core is scrubs and tunics for clinical and nursing work, polos for reception and animal care staff, fleeces for warmth in kennels and yards, waterproofs for outdoor and large-animal work, and safety shoes or wellingtons, all branded with the practice name, covering both the consulting room and the yard.",
      "At its core: scrubs and tunics for clinical work, polos for reception and animal care staff, fleeces for cold kennels and yards, waterproofs for outdoor and large-animal work, and safety shoes or wellingtons, all branded with the practice name and spanning the consulting room and the field.",
      "The core uniform is scrubs and tunics for clinical and nursing work, polos for reception and animal care, fleeces for kennels and yards, waterproofs for outdoor and large-animal work, and safety shoes or wellingtons, all branded with the practice name across both the consulting room and the yard.",
      "It comes down to scrubs and tunics for the clinical side, polos for reception and animal care, fleeces for cold kennels and yards, waterproofs for outdoor and large-animal work, and safety shoes or wellingtons, all branded with the practice name and covering the consulting room and the field.",
      "Scrubs and tunics for clinical and nursing work, polos for reception and animal care staff, fleeces for kennels and yards, waterproofs for outdoor and large-animal work, and safety shoes or wellingtons make up the core, all branded with the practice name across both environments."])),
     ("Do you supply waterproofs and footwear for kennels and equine work?", P('fq4',[
      "Yes. Alongside the clinical scrubs and tunics we supply fleeces, waterproof jackets and trousers, and safety shoes and wellingtons for kennels, catteries, grooming, stables, equine and large-animal work, so the same supplier kits the consulting room and the yard from one place.",
      "Yes. As well as clinical scrubs and tunics, we supply fleeces, waterproof jackets and trousers, and safety shoes and wellingtons for kennels, catteries, grooming, stables, equine and large-animal work, so one supplier kits the consulting room and the yard.",
      "Yes, we supply fleeces, waterproof jackets and trousers, and safety shoes and wellingtons for kennels, catteries, grooming, stables, equine and large-animal work, alongside the clinical scrubs and tunics, so the consulting room and the yard come from one place.",
      "Yes. Beyond the clinical scrubs and tunics, we supply fleeces, waterproofs and safety shoes and wellingtons for kennels, catteries, grooming, stables, equine and large-animal work, so the same supplier covers the consulting room and the outdoor side.",
      "Yes. The outdoor side is covered too: fleeces, waterproof jackets and trousers, and safety shoes and wellingtons for kennels, catteries, grooming, stables, equine and large-animal work, supplied alongside the clinical scrubs and tunics from one place.",
      "Yes. We supply fleeces, waterproofs and safety shoes and wellingtons for kennels, catteries, grooming, stables, equine and large-animal work, together with the clinical scrubs and tunics, so the consulting room and the yard are kitted by the same supplier."])),
     ("Can you embroider our practice name and logo?", P('fq5',[
      "Yes. We embroider your practice or business name and logo in-house onto scrubs, tunics, polos and fleeces, finished to survive frequent, hot washing. Send your artwork once, we hold it on file, and every reorder and new starter matches, so a small practice, kennels or mobile groomer looks consistent and professional.",
      "Yes. Your practice or business name and logo are embroidered in-house onto scrubs, tunics, polos and fleeces, finished for frequent, hot washing. Send artwork once and we hold it on file, so every reorder and new starter matches, and a small practice, kennels or mobile groomer looks consistent.",
      "Yes, all branding is done in-house onto scrubs, tunics, polos and fleeces, finished to survive frequent, hot washing. We hold your artwork on file, so every reorder and new starter matches and a small practice or mobile groomer looks consistent and professional.",
      "Yes. Send your artwork once and we embroider your practice name and logo in-house onto scrubs, tunics, polos and fleeces, holding it on file so every reorder and new starter matches, and a small practice, kennels or mobile groomer looks consistent.",
      "Yes. Practice or business name and logo are embroidered in-house onto scrubs, tunics, polos and fleeces, finished for frequent hot washing and held on file, so every reorder and new starter matches and a small practice or mobile groomer stays consistent.",
      "Yes, embroidery is done in-house onto scrubs, tunics, polos and fleeces, finished to take frequent hot washing. Send your logo once and we keep it on file, so reorders and new starters line up and a small practice, kennels or groomer looks professional."])),
     ("Are the scrubs and tunics suitable for clinical hygiene?", P('fq6',[
      "Yes. The scrubs and tunics are hard-wearing and washable at the higher temperatures clinical work needs, comfortable for long shifts and easy to keep clean, presenting vets and nurses as professional and hygienic to every owner who brings an animal in.",
      "Yes. The scrubs and tunics are durable and washable at the higher temperatures clinical work needs, comfortable over a long shift and easy to keep clean, so vets and nurses present as professional and hygienic to every owner.",
      "Yes, the scrubs and tunics are hard-wearing and wash at the higher temperatures clinical hygiene needs, comfortable for long shifts and easy to clean, keeping vets and nurses looking professional and hygienic to every owner.",
      "Yes. Built to wash hot and wear hard, the scrubs and tunics handle the temperatures clinical work needs, stay comfortable through a long shift and keep clean easily, presenting vets and nurses as hygienic and professional.",
      "Yes. The scrubs and tunics wash at the higher temperatures clinical work requires, wear hard, stay comfortable across a long shift and clean up easily, so the clinical team looks professional and hygienic to every owner.",
      "Yes, the scrubs and tunics are made to wash hot and last, comfortable for long shifts and simple to keep clean, presenting vets and nurses as clean, hygienic and professional to every owner who comes in."])),
     ("How quickly can you supply veterinary workwear?", P('fq7',[
      "Order direct online and your kit is dispatched on standard lead times, with embroidery added in-house before it ships. For a larger practice or group on a trade account, send your headcount, your logo and your sizes and we will build a branded uniform list and hold it on file for fast reordering on standard lead times.",
      "Order direct online and your kit ships on standard lead times, with embroidery added in-house first. For a larger practice or group on a trade account, send your headcount, logo and sizes and we will build a branded uniform list and hold it on file for fast reordering on standard lead times.",
      "Order direct online and we dispatch on standard lead times, embroidery added in-house before shipping. For a larger practice or group on a trade account, send your headcount, logo and sizes and we will build a branded uniform list and hold it on file for fast reordering.",
      "Order direct online and your kit is dispatched on standard lead times with embroidery done in-house first. For a larger practice or group on a trade account, send your headcount, logo and sizes and we will build a branded uniform list and hold it on file for fast reordering on standard lead times.",
      "Order online and we dispatch on standard lead times with embroidery added in-house beforehand. A larger practice or group on a trade account can send headcount, logo and sizes for a branded uniform list held on file for fast reordering.",
      "Order direct online and your kit ships on standard lead times, embroidered in-house first. For a larger practice or group on a trade account, send your headcount, logo and sizes and we will build a branded uniform list and keep it on file for quick reordering on standard lead times."])),
    ]

TOWNS = {
 "birmingham": {
  "region":"Birmingham and the West Midlands",
  "nearby":["Solihull","West Bromwich","Walsall"],
  "snapshot":"iNeedWorkwear supplies branded scrubs, tunics, polos, fleeces, waterproofs and safety footwear to vet practices, veterinary nurses, kennels, catteries, dog groomers and equine yards across Birmingham, from the city practices to the green-belt fringe, embroidered in-house with the practice name. Veterinary and animal care is mostly small practices and sole traders, so the quickest route is to order direct online with no account, while a larger practice or group can set up a trade account.",
  "s1_head":"Kitting the practices, kennels and yards of the West Midlands",
  "s1loc":[
   "Birmingham and the wider West Midlands have a large companion-animal scene. Independent practices and bigger veterinary groups sit on high streets across the city and out through Sutton Coldfield, Solihull and Edgbaston, alongside the wider world of animal work: boarding kennels and catteries on the green-belt fringe, dog groomers in salons and mobile vans, doggy daycare, and well-known rescues like Birmingham Dogs Home. Equine and large-animal work runs out toward the rural edges.",
   "And it is dominated by small businesses. The independent practices, the one-van mobile groomers, the family-run kennels and catteries and the equine yards around the city are mostly small teams and sole traders rather than national chains. Every one of them puts staff in front of worried owners and hands-on with animals, so the uniform has to be both clinically clean and tough enough for the kennels and the yard.",
  ],
  "kit_loc":"across the city's consulting rooms, kennels and yards",
  "s2_intro":"Whether you are an independent practice in Sutton Coldfield, a boarding kennels on the green-belt fringe, a mobile groomer or an equine yard across Birmingham",
 },
 "leeds": {
  "region":"Leeds and West Yorkshire",
  "nearby":["Bradford","Pudsey","Dewsbury"],
  "snapshot":"iNeedWorkwear supplies branded scrubs, tunics, polos, fleeces, waterproofs and safety footwear to vet practices, veterinary nurses, kennels, catteries, dog groomers and equine yards across Leeds, from the suburban practices to the rural fringe, embroidered in-house with the practice name. Veterinary and animal care is mostly small practices and sole traders, so the quickest route is to order direct online with no account, while a larger practice or group can set up a trade account.",
  "s1_head":"Kitting the practices, kennels and yards of Yorkshire",
  "s1loc":[
   "Leeds has more than forty veterinary practices across the city, a mix of independents and bigger groups spread through Kirkstall, Colton, Horsforth, Armley, Morley and Shadwell. Around them sits the wider animal-care trade: boarding kennels, catteries and grooming on the rural fringe toward Wetherby and Wharfedale, mobile and salon dog groomers across the suburbs, doggy daycare and animal rescues, with equine and livery yards out toward Harewood and the Dales edge.",
   "And the trade is overwhelmingly small and independent. The suburban practices, the one-van groomers, the family-run kennels and catteries and the livery yards around the city are mostly small teams and sole traders rather than national chains. Each of them faces owners in the consulting room and works hands-on in the kennels and yard, so the uniform has to be clinically clean and tough enough for the outdoor side.",
  ],
  "kit_loc":"across the city's consulting rooms, kennels and yards",
  "s2_intro":"Whether you are an independent practice in Kirkstall, a boarding kennels toward Wetherby, a mobile groomer or an equine yard across Leeds",
 },
 "glasgow": {"region": "Glasgow and the Greater Glasgow area", "nearby": ["Rutherglen", "Paisley", "Clydebank"], "snapshot": "iNeedWorkwear supplies branded scrubs, tunics, polos, fleeces, waterproofs and safety footwear to vet practices, veterinary nurses, kennels, catteries, dog groomers and equine yards across Glasgow, from the inner-city surgeries to the rural fringe, embroidered in-house with the practice name. Veterinary and animal care is mostly small practices and sole traders, so the quickest route is to order direct online with no account, while a larger practice or group can set up a trade account.", "s1_head": "Kitting the practices, kennels and yards of Greater Glasgow", "s1loc": ["Glasgow runs dozens of veterinary practices across the city, from the Pets'n'Vets Roundhouse hospital at Pollokshaws and Rouken Glen surgery to independents like East End Vets in Parkhead and ScotVet over Sandyhills, Shettleston and Baillieston. Around them sits the wider animal-care trade: boarding kennels and catteries on the green edge such as Valley Kennels near Milngavie and Birdston toward Kirkintilloch, mobile and salon groomers across the suburbs, and rescues serving the conurbation.", "Most of this work is done by small, independent teams. The neighbourhood surgeries, the one-van groomers, the family-run kennels and catteries out toward Larkhall and the livery yards on the moorland fringe are mostly sole traders and tight crews rather than chains. Each faces a worried owner in the consulting room and then works hands-on in the kennels and yard, so the uniform must stay clinically clean indoors and tough enough for the wet outdoor side."], "kit_loc": "across the city's consulting rooms, kennels and yards", "s2_intro": "Whether you are an independent practice in Shettleston, a boarding kennels toward Milngavie, a mobile groomer or an equine yard across Glasgow"},
 "manchester": {"region": "Manchester and Greater Manchester", "nearby": ["Salford", "Stretford", "Stockport"], "snapshot": "iNeedWorkwear supplies branded scrubs, tunics, polos, fleeces, waterproofs and safety footwear to vet practices, veterinary nurses, kennels, catteries, dog groomers and equine yards across Manchester, from the inner suburbs to the rural fringe, embroidered in-house with the practice name. Veterinary and animal care is mostly small practices and sole traders, so the quickest route is to order direct online with no account, while a larger practice or group can set up a trade account.", "s1_head": "Kitting the practices, kennels and yards of Greater Manchester", "s1loc": ["Across the southern suburbs Manchester carries a dense run of practices, from Ashleigh Veterinary Centre in Whalley Range and Yew Tree in Withington to the cat-only Manchester Cat Clinic between Withington and Didsbury and surgeries through Chorlton. Around them sits the wider animal-care trade: the Manchester and Cheshire Dogs Home rehoming strays, boarding kennels and catteries on the moorland edge such as Moss Cottage at Sale, salon and mobile groomers, and equine yards out toward the Cheshire border.", "The operators are nearly all small and independent. The suburban surgeries, the doggy-daycare and grooming rooms, the family kennels and catteries near the M60 and the livery yards on the rural fringe tend to be sole traders and small teams rather than national groups. Each one meets owners in a clinical consulting room and then works hands-on in the kennels, grooming room and yard, so the kit has to read clean indoors and cope outdoors in all weathers."], "kit_loc": "across the city's consulting rooms, kennels and yards", "s2_intro": "Whether you are an independent practice in Chorlton, a boarding kennels toward Sale, a mobile groomer or an equine yard across Manchester"},
 "liverpool": {"region": "Liverpool and Merseyside", "nearby": ["Bootle", "Birkenhead", "Crosby"], "snapshot": "iNeedWorkwear supplies branded scrubs, tunics, polos, fleeces, waterproofs and safety footwear to vet practices, veterinary nurses, kennels, catteries, dog groomers and equine yards across Liverpool, from the city surgeries to the rural fringe, embroidered in-house with the practice name. Veterinary and animal care is mostly small practices and sole traders, so the quickest route is to order direct online with no account, while a larger practice or group can set up a trade account.", "s1_head": "Kitting the practices, kennels and yards of Merseyside", "s1loc": ["Set across south Liverpool, the trade runs from the independent Woolton Veterinary Centre serving Woolton Village, Aigburth, Allerton and Mossley Hill to Medivet on Aigburth Road and Adams Vets reaching Garston and Kirkby. Around them sits the wider animal-care scene: the RSPCA branch and Dogs Trust Merseyside rehoming at Halewood, boarding kennels and catteries such as Carla Lane Animals in Need at Melling, salon and mobile groomers, and yards on the green edge toward the city boundary.", "Behind the bigger names the trade stays small and hands-on. The neighbourhood surgeries, the one-van groomers, the sanctuary kennels and family catteries out at Melling and Knowsley and the livery yards on the rural fringe are mostly sole traders and small crews. Each reassures an owner in a clinical room and then turns to wet, physical work in the kennels and yard, so the workwear has to wash hot and stay smart while standing up to the outdoor graft."], "kit_loc": "across the city's consulting rooms, kennels and yards", "s2_intro": "Whether you are an independent practice in Woolton, a boarding kennels toward Melling, a mobile groomer or an equine yard across Liverpool"},
 "sheffield": {"region": "Sheffield and South Yorkshire", "nearby": ["Rotherham", "Chesterfield", "Barnsley"], "snapshot": "iNeedWorkwear supplies branded scrubs, tunics, polos, fleeces, waterproofs and safety footwear to vet practices, veterinary nurses, kennels, catteries, dog groomers and equine yards across Sheffield, from the inner suburbs to the moorland edge, embroidered in-house with the practice name. Veterinary and animal care is mostly small practices and sole traders, so the quickest route is to order direct online with no account, while a larger practice or group can set up a trade account.", "s1_head": "Kitting the practices, kennels and yards of South Yorkshire", "s1loc": ["Sheffield runs a deep spread of veterinary practices, from Hallam Vets at Crookes and Holme Lane to Broomhill Veterinary Practice on Crookes Road, Hunters Bar and Springfield on Ecclesall Road, and Highfield and Hallamshire clinics further out. Around them the wider animal-care trade fills the suburbs and the moorland fringe: Centre Barks at Moscar boarding and grooming toward the Peak District, Mosborough Kennels and Cattery to the south, plus equine and livery yards out around Stocksbridge and Bradfield.", "What ties them together is scale: nearly all of it is small and independent. The Hillsborough and Ecclesall practices, the one-van groomers, the family kennels at Moscar and Mosborough and the smallholdings climbing toward the Peak are run by tight teams and sole traders, not chains. Each reassures an owner in a clean consulting room one hour and works hands-on in a kennel block or a wet field the next, so the kit has to cover both."], "kit_loc": "across the city's consulting rooms, kennels and yards", "s2_intro": "Whether you are an independent practice in Crookes, a boarding kennels toward Moscar, a mobile groomer or an equine yard around Stocksbridge"},
 "edinburgh": {"region": "Edinburgh and the Lothians", "nearby": ["Musselburgh", "Livingston", "Dunfermline"], "snapshot": "iNeedWorkwear supplies branded scrubs, tunics, polos, fleeces, waterproofs and safety footwear to vet practices, veterinary nurses, kennels, catteries, dog groomers and equine yards across Edinburgh, from the city tenements to the Pentland edge, embroidered in-house with the practice name. Veterinary and animal care is mostly small practices and sole traders, so the quickest route is to order direct online with no account, while a larger practice or group can set up a trade account.", "s1_head": "Kitting the practices, kennels and yards of the Lothians", "s1loc": ["Spread across more than thirty practices, Edinburgh carries a strong independent streak: family-run Leith Vets in the old port, West Edinburgh Vets and Westport in Corstorphine, Thistle Vets at Chesser and Clovenstone, and the Dick Vet teaching practice out at Easter Bush. Beyond the clinics the trade widens through Colinton Cattery beside the Pentlands, Cranstoun and Meadowhill out in Midlothian, Christine's grooming parlour in town, and livery and farm yards on the green belt south and west.", "Look at who actually runs it and the picture is small and owner-led. The Morningside and Corstorphine practices, the Leith family clinic, the lone mobile groomers, the Midlothian kennels and the Pentland-edge livery yards are mostly compact teams and sole traders rather than big groups. Every one of them moves between a hygienic consulting room and the hands-on work of a kennel run or a muddy stable, so the workwear has to hold up on both sides."], "kit_loc": "across the city's consulting rooms, kennels and yards", "s2_intro": "Whether you are an independent practice in Leith, a boarding kennels out in Midlothian, a mobile groomer or an equine yard along the Pentland edge"},
 "bristol": {"region": "Bristol and the West of England", "nearby": ["Bath", "Clevedon", "Portishead"], "snapshot": "iNeedWorkwear supplies branded scrubs, tunics, polos, fleeces, waterproofs and safety footwear to vet practices, veterinary nurses, kennels, catteries, dog groomers and equine yards across Bristol, from the harbourside suburbs to the Mendip fringe, embroidered in-house with the practice name. Veterinary and animal care is mostly small practices and sole traders, so the quickest route is to order direct online with no account, while a larger practice or group can set up a trade account.", "s1_head": "Kitting the practices, kennels and yards of the West Country", "s1loc": ["Beyond the chains, Bristol holds dozens of practices with a strong independent core: The Grove Vets in Henleaze, Downs Veterinary Practice, Fishponds Veterinary Centre to the east, Zetland Vets and clinics through Clifton, Redland and Bedminster. Surrounding them is a busy animal-care trade, with Cottage Kennels and Cattery toward South Gloucestershire, Wynhol and Woodview out in the North Somerset countryside, Emersons Green grooming and boarding, and equine and farm yards reaching down to the Mendip fringe.", "Behind the variety, the operators stay small. The Clifton and Bedminster practices, the Fishponds clinic, the single-van groomers, the family kennels at Wynhol and Woodview and the livery yards toward Mendip are run by modest teams and sole traders, not national brands. Each works clean in a consulting room facing a worried owner and then heads outside to a kennel block, a grooming room or a stable, so the uniform has to do both jobs well."], "kit_loc": "across the city's consulting rooms, kennels and yards", "s2_intro": "Whether you are an independent practice in Henleaze, a boarding kennels out toward North Somerset, a mobile groomer or an equine yard on the Mendip fringe"},
}

_CSV=None
def _load_csv():
    global _CSV
    if _CSV is not None: return _CSV
    here=os.path.dirname(os.path.abspath(__file__))
    for p in (os.path.join(here,'VT_towns.csv'),'VT_towns.csv','/mnt/user-data/outputs/VT_towns.csv'):
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
                         f"(web-verified, all on VT_towns.csv). No rank/auto fallback.")
    bad = [n for n in nb if not any(r[1].lower()==n.lower() for r in _load_csv())]
    if bad:
        raise ValueError(f"{town}: nearby town(s) not on VT_towns.csv: {bad}")
    return nb[:3]

def build_title(town):
    for t in (f"{town} Veterinary and Animal Care Workwear",
              f"{town} Veterinary and Animal Workwear", f"{town} Veterinary Workwear"):
        if len(t) <= 60: return t
    return f"{town} Veterinary Workwear"

def build_meta(town):
    for m in (f"Branded scrubs, tunics, polos, fleeces and waterproofs for {town} vets, kennels, catteries and equine - order direct online, in-house embroidery.",
              f"Branded scrubs, tunics, polos and fleeces for {town} vets, kennels and equine - order direct online with in-house embroidery, no account needed.",
              f"Branded scrubs, polos, fleeces and waterproofs for {town} vet practices, kennels and equine - order direct online with in-house embroidery.",
              f"Branded veterinary workwear for {town} vets, kennels and equine - scrubs, polos, fleeces, waterproofs, ordered direct online with embroidery."):
        if len(m) <= 160: return m
    return f"Branded veterinary workwear for {town} vets and kennels - scrubs, polos, fleeces, ordered online with embroidery."

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
        "name":f"Veterinary and Animal Care Workwear Supply and Embroidery in {town}",
        "serviceType":"Veterinary and animal care workwear and embroidery supply",
        "provider":{"@id":"https://www.ineedworkwear.com/#organization"},
        "areaServed":[{"@type":"City","name":town}]+[{"@type":"City","name":n} for n in nearby],
        "audience":{"@type":"BusinessAudience","name":"Vet practices, kennels, catteries, groomers and equine yards"},
        "description":f"Branded scrubs, tunics, polos, fleeces, waterproofs and safety footwear supplied to vet practices, kennels, catteries, groomers and equine yards in {town}, ordered direct online or on a trade account, with in-house embroidery.",
        "hasOfferCatalog":{"@type":"OfferCatalog","name":"Veterinary and Animal Care Workwear",
            "itemListElement":[{"@type":"Offer","itemOffered":{"@type":"Product","name":p}} for p in VT_PRODUCTS]}}
    crumb = {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Home","item":DOMAIN},
        {"@type":"ListItem","position":2,"name":"Veterinary and Animal Care Workwear","item":f"{DOMAIN}/veterinary-animal-care-workwear"},
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
    grid    = build_grid(town)
    emb     = [P(EMB_P1_POOL,'e1').format(t=town), P(EMB_P2_POOL,'e2').format(t=town), P(EMB_P3_POOL,'e3')]
    con     = [P(CON_P1_POOL,'c1').format(t=town), P(CON_P2_POOL,'c2'), P(CON_P3_POOL,'c3').format(t=town)]
    acc     = [P(ACC_P1_POOL,'a1').format(t=town), P(ACC_P2_POOL,'a2'),
               P(ACC_P3_POOL,'a3').format(t=town), P(ACC_P4_POOL,'a4')]
    why     = [P(WHY_P1_POOL,'w1').format(t=town), P(WHY_P2_POOL,'w2'), P(WHY_P3_POOL,'w3'), P(WHY_P4_POOL,'w4')]
    ordr    = [P(ORD_P1_POOL,'o1').format(region=region), P(ORD_P2_POOL,'o2'), P(ORD_P3_POOL,'o3')]
    selfp   = P(SELF_POOL,'self'); sorted_ = P(SORTED_POOL,'sorted')

    emb_svg   = EMB.replace('a London vet practice logo', f'a {town} vet practice logo')
    sign_svg  = SIGNPOST.replace('London veterinary and animal care signpost', f'{town} veterinary and animal care signpost')
    sign_svg  = re.sub(r'<text x="230" y="62".*?</text>', signpost_town(town), sign_svg, flags=re.S)
    sign_svg  = sign_svg.replace('every kind of London animal care', f'every kind of {town} animal care')
    prem_svg  = PREMISES.replace('serving vets and animal care across London', f'serving vets and animal care across {town}')

    H=[build_head(town, slug, faqs, nearby), HEADER]
    H.append(f'<div class="vt-hero"><div class="vt-wrap"><div class="vt-subtitle">Branded Workwear for Vets, Kennels, Catteries and Equine</div><h1>{town} Veterinary and Animal Care Workwear</h1></div></div>')
    H.append('<div class="vt-pulse"></div>')
    H.append(f'<div class="vt-trust-strip"><p>{trust}</p></div>')
    H.append(f'<div class="vt-wrap"><div class="vt-snapshot"><div class="vt-snapshot-label">Supplier Snapshot</div><p>{snap}</p></div></div>')
    H.append(STATS)
    H.append('<div class="vt-cta-bar"><a href="https://www.ineedworkwear.com" class="vt-cta-btn">Browse Veterinary and Animal Care Workwear</a></div>')
    H.append('<div class="vt-jump-links"><a href="#range">Workwear Range</a><a href="#contract">The Uniform</a><a href="#accounts">Ordering and Accounts</a><a href="#order">How to Order</a></div>')
    H.append(GARMENT)
    H.append(f'<div class="vt-section"><div class="vt-wrap"><h2>{s1head}</h2>'+''.join(f'<p>{p}</p>' for p in s1ps)+'</div></div>')
    H.append(f'<div class="vt-section" id="range"><div class="vt-wrap"><h2>Veterinary and Animal Care Workwear Range</h2><p>{s2intro} <a href="https://www.ineedworkwear.com">Browse the full range at iNeedWorkwear.com</a>.</p><p class="vt-btn-center"><a href="https://www.ineedworkwear.com" class="vt-section-btn">Browse The Range</a></p>{grid}</div></div>')
    H.append(f'<div class="vt-section"><div class="vt-wrap"><h2>Branding for a Practice, a Kennels or a Mobile Groomer</h2>'+''.join(f'<p>{p}</p>' for p in emb)+'</div></div>')
    H.append(emb_svg)
    H.append(f'<div class="vt-wrap"><div class="vt-contract" id="contract"><h3>{CON_HEAD}</h3>'+''.join(f'<p>{p}</p>' for p in con)+'</div></div>')
    H.append(sign_svg)
    H.append(f'<div class="vt-section" id="accounts"><div class="vt-wrap"><h2>{ACC_HEAD}</h2>'+''.join(f'<p>{p}</p>' for p in acc)+'</div></div>')
    H.append(prem_svg)
    H.append(f'<div class="vt-section"><div class="vt-wrap"><h2>Why Vets, Kennels and Animal Care Choose iNeedWorkwear</h2>'+''.join(f'<p>{p}</p>' for p in why)+'</div></div>')
    H.append(ORDER)
    H.append(f'<div class="vt-section" id="order"><div class="vt-wrap"><h2>How to Order Veterinary and Animal Care Workwear</h2><p>{ordr[0]}</p><p>{ordr[1]}</p><p>{ordr[2]}</p><p class="vt-btn-center"><a href="https://www.ineedworkwear.com" class="vt-section-btn">Browse And Order Online</a></p><p>{selfp}</p>'+CONTACT+'</div></div>')
    faq_html=''.join(f'<div class="vt-faq-item"><div class="vt-faq-q">{q}</div><div class="vt-faq-a">{a}</div></div>' for q,a in faqs)
    H.append(f'<div class="vt-faq"><div class="vt-wrap"><h2>Veterinary and Animal Care Workwear FAQ</h2>{faq_html}</div></div>')
    H.append(f'<div class="vt-wrap"><div class="vt-workwear">{sorted_}</div></div>')
    nb_links=''.join(f'<a href="vt-{slugify(n)}.html">Vet and animal care workwear in {n}</a>\n' for n in nearby)
    H.append(f'<div class="vt-nearby"><div class="vt-wrap"><h3>Veterinary and Animal Care Workwear in Nearby Towns</h3><div class="vt-nearby-links">{nb_links}</div></div></div>')
    H.append(FOOTER+'\n</body></html>')
    return '\n'.join(H)

def main():
    args=[a for a in sys.argv[1:]]
    outdir = os.environ.get('VT_OUTDIR') or ('/mnt/user-data/outputs'
             if os.path.isdir('/mnt/user-data/outputs') else 'outputs')
    os.makedirs(outdir, exist_ok=True)
    disp = {r[1].lower(): r[1] for r in _load_csv()}
    if not args:
        args=[t for t in TOWNS if t!='london']
    for town_key in args:
        tk=town_key.lower()
        if tk=='london': continue
        if tk not in TOWNS:
            print(f"SKIP {town_key}: not in TOWNS (must be web-researched first)"); continue
        town=disp.get(tk, ' '.join(w.capitalize() for w in tk.split()))
        slug=f"vt-{slugify(town)}"
        html=assemble(slug, town)
        path=os.path.join(outdir, f"{slug}.html")
        open(path,'w',encoding='utf-8').write(html)
        print(f"WROTE {path}  ({len(html.split())} words approx)")

if __name__=='__main__':
    main()
