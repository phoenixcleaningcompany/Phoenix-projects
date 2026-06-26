#!/usr/bin/env python3
# CH2 (Charities, Non-Profits & Volunteers) series builder v1.0 - read SPEC.md/CLAUDE.md
# HYBRID / audience BOTH, EQUAL weight: national charities with shops and branches
# (procurement / TRADE ACCOUNT, managed reordering, held kit list) AND small local
# volunteer groups / foodbanks (DIRECT ONLINE, no account, NO MINIMUM). Budget-
# conscious buyer is the driving flag - every pound on kit is a pound off the cause.
# DIFFERENTIATOR = RECOGNISABLE, TRUSTED and AFFORDABLE: kit that makes a volunteer
# instantly official to the public, donors and the people they help, on a tight
# budget, with the charity name embroidered. Lead = POLO + HI-VIS + FLEECE. LOW
# depth, LOW local variation (generic shared paras in OWNER/PRESENT/NARROW pools,
# not per-town s1loc - see s1_paras). Headroom from the start: cards pooled 3 ways
# (build_grid), FAQ/WHY/PRESENT/NARROW at 6 variants. softshell is NOT a CH2 product
# (it is blocked in bleed). No JS, no entities, no delivery claims. Exactly 14 .com
# + 1 community per page. Nearby = geographic, hand-authored, on CH2_towns.csv.
# Prefix ch2- (distinct from the care-home CH series at ineedworkwear.co.uk).
import re, os, json, sys, csv
import hashlib
def pick(key, salt, n):
    h = hashlib.md5((salt + '|' + str(key).lower()).encode()).digest()
    return int.from_bytes(h[:4], 'big') % n

def _find_base():
    here = os.path.dirname(os.path.abspath(__file__))
    for p in (os.path.join(here,'ch2-london.html'),'ch2-london.html',
              '/mnt/user-data/outputs/ch2-london.html','/home/claude/ch2kit/ch2-london.html'):
        if os.path.exists(p): return p
    sys.exit("ERROR: ch2-london.html (base template) not found beside ch2_build.py")

BASE = open(_find_base(), encoding='utf-8').read()
DOMAIN = 'https://www.ineedworkwear.uk'

def between(start, end, src=BASE):
    i = src.index(start); j = src.index(end, i+len(start)); return src[i:j]
def aria_block(aria):
    k = BASE.index(aria)
    i = BASE.rfind('<div class="ch2-wrap"><div class="ch2-illust">', 0, k)
    j = BASE.index('</div></div></div>', k) + len('</div></div></div>')
    return BASE[i:j]

CSS      = between('<style>', '</style>') + '</style>'
HEADER   = between('<div class="ch2-header">', '\n<div class="ch2-hero">')
STATS    = between('<div class="ch2-stats">', '\n<div class="ch2-cta-bar">')
GARMENT  = between('<div class="ch2-wrap"><div class="ch2-illust"><div class="ch2-garment-row">', '\n<div class="ch2-section">')
EMB      = aria_block('Embroidery machine stitching')
SIGNPOST = aria_block('charity and volunteer signpost')
PREMISES = aria_block('serving volunteers across')
ORDER    = aria_block('Order charity and volunteer workwear online')
CONTACT  = BASE[BASE.index('<div class="ch2-contact-block">'):
                BASE.index('</div></div></div>', BASE.index('<div class="ch2-contact-block">'))+len('</div></div></div>')]
FOOTER   = BASE[BASE.index('<footer class="ch2-footer">'):BASE.index('</footer>')+len('</footer>')]

def signpost_town(town):
    n = len(town)
    size = 22 if n <= 8 else 19 if n <= 11 else 16 if n <= 15 else 13 if n <= 20 else 11
    tl = ' textLength="200" lengthAdjust="spacingAndGlyphs"' if n > 11 else ''
    return (f'<text x="230" y="62" text-anchor="middle" font-family="Arial,sans-serif" '
            f'font-weight="800" font-size="{size}" fill="#fff"{tl}>{town.upper()}</text>')

CH2_PRODUCTS = ["Polo Shirts and T-Shirts","Hi-Vis Vests and Waistcoats","Fleeces and Mid-Layers",
 "Waterproofs and Outdoor Jackets","Sweatshirts and Zip Tops","Aprons for Shops and Kitchens",
 "Caps, Beanies and Accessories","Embroidery, Names and ID Branding"]

def _card(n,d): return f'<div class="ch2-product-card"><div class="ch2-product-name">{n}</div><div class="ch2-product-detail">{d}</div></div>'
CARD_DETAILS=[
 ("Polo Shirts and T-Shirts",[
   "Affordable branded polos and t-shirts for shops, events and day-to-day volunteering, the everyday layer that makes a volunteer recognisable and official.",
   "Affordable branded polos and t-shirts for charity shops, events and everyday volunteering, the core layer that marks a volunteer out as official and approachable.",
   "Hard-wearing, affordable branded polos and t-shirts for shops, collections and day-to-day volunteering, the everyday layer that makes a volunteer recognisable."]),
 ("Hi-Vis Vests and Waistcoats",[
   "Hi-vis vests and waistcoats for street collections, event marshalling, litter picks and outdoor volunteering, keeping volunteers visible and easy to find.",
   "Hi-vis vests and waistcoats for collections, marshalling, litter picks and outdoor work, keeping volunteers visible, safe and easy to spot in a crowd.",
   "Hi-vis vests and waistcoats for street collections, event stewarding, conservation and outdoor volunteering, keeping volunteers visible and easy to find."]),
 ("Fleeces and Mid-Layers",[
   "Warm branded fleeces and mid-layers for cold shops, winter collections and outdoor work, an affordable extra layer over a polo when it turns cold.",
   "Branded fleeces and mid-layers for cold charity shops, winter collections and outdoor volunteering, an affordable warm layer over a polo when it turns cold.",
   "Cosy branded fleeces and mid-layers for chilly shops, winter collections and outdoor work, an affordable extra layer over a polo on a cold day."]),
 ("Waterproofs and Outdoor Jackets",[
   "Waterproof jackets for outdoor collections, events, conservation and outreach, keeping volunteers dry and presentable whatever the weather.",
   "Waterproof jackets for outdoor collections, fundraising events, conservation and outreach work, keeping volunteers dry and presentable in any weather.",
   "Waterproof jackets for outdoor collections, events, litter picks and outreach, keeping volunteers dry, warm and presentable whatever the weather."]),
 ("Sweatshirts and Zip Tops",[
   "Comfortable branded sweatshirts and zip tops for cooler days in the shop or at events, a cosy, affordable layer that still carries the charity name.",
   "Branded sweatshirts and zip tops for cooler days in the charity shop or at events, a comfortable, affordable layer that still carries the charity name.",
   "Comfortable branded sweatshirts and zip tops for cool days in the shop or at outdoor events, an affordable cosy layer that still shows the charity name."]),
 ("Aprons for Shops and Kitchens",[
   "Practical branded aprons for charity shops, foodbank sorting and community kitchens, hard-wearing, easy to wash and clearly marked with the charity name.",
   "Hard-wearing branded aprons for charity shops, foodbank sorting and community kitchens, easy to wash and clearly marked with the charity name.",
   "Practical branded aprons for shops, foodbank sorting and community kitchens, tough, easy to wash and clearly marked with the charity name."]),
 ("Caps, Beanies and Accessories",[
   "Branded caps, beanies and accessories to finish the kit, affordable extras embroidered to match the polos, hi-vis and fleeces across the team.",
   "Branded caps, beanies and accessories that finish the look, affordable extras embroidered to match the polos, hi-vis and fleeces the team already wears.",
   "Branded caps, beanies and accessories to complete the kit, affordable extras embroidered to match the rest of the team's polos, hi-vis and fleeces."]),
 ("Embroidery, Names and ID Branding",[
   "In-house embroidery of your charity name, logo and role names onto polos, hi-vis, fleeces and aprons, so a national charity or a small group looks organised and official.",
   "In-house embroidery of your charity name, logo and role names across polos, hi-vis, fleeces and aprons, so a national charity or a small local group looks organised and official.",
   "Your charity name, logo and role names embroidered in-house onto polos, hi-vis, fleeces and aprons, so a big charity or a small group looks organised and official."]),
]
GRID_ORDER=[(0,1,2,3,4,5,6,7),(1,0,2,3,4,5,6,7),(0,1,3,2,4,5,6,7),(0,2,1,3,4,5,6,7)]
def build_grid(town):
    order = GRID_ORDER[pick(town,'gord',len(GRID_ORDER))]
    cards=[]
    for i in order:
        name,variants = CARD_DETAILS[i]
        cards.append(_card(name, variants[pick(town,f'g{i}',len(variants))]))
    return '<div class="ch2-product-grid">'+''.join(cards)+'</div>'

TRUST_POOL=[
 "Branded polos, hi-vis, fleeces, waterproofs and aprons for charities, foodbanks and volunteer groups - affordable, no minimum, order direct online",
 "Branded polos, hi-vis, fleeces and waterproofs for charities, foodbanks and volunteer groups - affordable, no minimum, trade accounts or direct online",
 "Trusted by charities, foodbanks and volunteer groups across the UK for affordable branded polos, hi-vis and fleeces - trade or direct, no minimum",
 "Affordable branded workwear - polos, hi-vis, fleeces, waterproofs and aprons - for charities and volunteer groups across the UK, trade or direct online",
]
S2INTRO_POOL=[
 "Whether you are a national charity with shops and branches or a small local foodbank or community group in {t}, the range is built to kit you affordably from one place: branded polos and hi-vis, fleeces and waterproofs for the cold and wet, and aprons for shops and kitchens.",
 "A national {t} charity with shops and branches, or a small local foodbank or community group, is kitted affordably from one place: branded polos and hi-vis, fleeces and waterproofs for the cold and wet, and aprons for shops and kitchens.",
 "For a {t} charity with shops and branches or a small volunteer group, the range kits you affordably from one place: branded polos and hi-vis, fleeces and waterproofs for the cold and wet, and aprons for shops and kitchens.",
 "Whether it is a national charity or a single foodbank in {t}, you are kitted affordably from one place: branded polos and hi-vis, fleeces and waterproofs for the cold and wet, plus aprons for shops and kitchens.",
]
EMB_P1_POOL=[
 "For a charity, how the volunteers look is part of how the public, donors and the people being helped trust the work. A clean, branded polo or hi-vis with the charity name tells everyone at a {t} foodbank, collection, shop or community event who is official, who to approach and who is there to help. Branding turns a willing volunteer into a recognisable, reassuring presence.",
 "For a charity, how its volunteers look is part of how the public, donors and the people being helped trust the work. A clean, branded polo or hi-vis with the charity name shows everyone at a {t} foodbank, collection, shop or event who is official, who to approach and who is there to help. Branding makes a willing volunteer a recognisable, reassuring presence.",
 "How the volunteers look is part of how a {t} charity earns trust from the public, donors and the people it helps. A clean, branded polo or hi-vis with the charity name tells everyone at a foodbank, collection, shop or community event who is official and who is there to help, turning a willing volunteer into a recognisable, reassuring presence.",
 "For a charity, the way volunteers look is part of how the public, donors and service users trust the work. A clean, branded polo or hi-vis with the charity name marks out, at any {t} foodbank, collection, shop or event, who is official and who to approach, turning a willing volunteer into a recognisable, reassuring presence.",
]
EMB_P2_POOL=[
 "We brand in-house, which means your charity name and logo are embroidered onto polos, hi-vis, fleeces and aprons, finished to survive frequent washing. Send your artwork once, we hold it on file, and every reorder and new volunteer matches the last, so whether it is a single {t} community group or a national charity with shops across the country, the look is consistent everywhere the name appears.",
 "Branding is done in-house onto polos, hi-vis, fleeces and aprons - your charity name and logo embroidered and finished to survive frequent washing. We hold your artwork on file, so every reorder and new volunteer matches, and whether it is one {t} community group or a national charity with shops countrywide, the look stays consistent everywhere the name appears.",
 "Your charity name and logo are embroidered in-house onto polos, hi-vis, fleeces and aprons, finished to take frequent washing. Held on file, your artwork reproduces on every reorder and new volunteer, so a single {t} community group or a national charity with shops across the country looks consistent everywhere the name appears.",
 "We badge in-house, embroidering your charity name and logo onto polos, hi-vis, fleeces and aprons and finishing them to survive frequent washing. Held on file, your branding matches on every reorder and new volunteer, so a {t} community group or a national charity with shops countrywide looks consistent everywhere.",
]
EMB_P3_POOL=[
 "And because volunteer teams change constantly, that consistency is what keeps a charity looking organised. We hold your branding and sizes on file, so kitting a new volunteer, opening a new shop or running a one-off event reproduces the same branded look every time, without anyone having to re-supply artwork or guess at a match, and without paying over the odds.",
 "And because volunteer teams change all the time, that consistency keeps a charity looking organised. We hold your branding and sizes on file, so a new volunteer, a new shop or a one-off event comes back the same branded look every time, with no artwork to re-supply and no paying over the odds.",
 "Because volunteer teams turn over constantly, that consistency is what keeps a charity looking organised. We keep your branding and sizes on file, so kitting a new volunteer, opening a new shop or running an event reproduces the same branded look each time, without re-supplying artwork or overspending.",
 "And as volunteers come and go, that consistency is what keeps a charity looking organised. We hold branding and sizes on file, so a new volunteer, a new shop or a one-off event reproduces the same branded look every time, with nothing to re-supply and no paying over the odds.",
]
CON_HEAD="Recognisable, Trusted and Affordable: Kit for Volunteers"
CON_P1_POOL=[
 "Charity and volunteer workwear really only has to do one thing, but it has to do it on a tight budget. That one thing is recognition. A branded polo, hi-vis or fleece with the charity name makes a {t} volunteer instantly identifiable as official to the public, to donors and to the people they are there to help, which builds trust and supports safeguarding at a foodbank, a collection, a charity shop or a community event. People need to see at a glance who is part of the team.",
 "Charity and volunteer workwear really only has one job, but it has to do it on a tight budget. That job is recognition. A branded polo, hi-vis or fleece with the charity name makes a {t} volunteer instantly identifiable as official to the public, donors and the people they help, which builds trust and supports safeguarding at a foodbank, collection, shop or community event. People need to see at a glance who is part of the team.",
 "Charity and volunteer workwear mainly has to do one thing, on a tight budget: make the volunteer recognisable. A branded polo, hi-vis or fleece with the charity name marks a {t} volunteer out as official to the public, donors and the people they help, building trust and supporting safeguarding at a foodbank, collection, shop or event. People need to see at a glance who is part of the team.",
 "Charity and volunteer workwear has one main job, done on a tight budget: recognition. A branded polo, hi-vis or fleece with the charity name makes a {t} volunteer instantly official to the public, donors and the people they help, which builds trust and supports safeguarding at a foodbank, a collection, a shop or a community event, so people can see at a glance who is part of the team.",
]
CON_P2_POOL=[
 "The budget is the constraint that shapes everything else. Every pound a charity spends on kit is a pound not spent on the cause, so the workwear has to be affordable: a narrow, practical range of branded basics, ordered in whatever quantity is needed with no minimum, rather than an expensive uniform programme. Polos and hi-vis do most of the work, with fleeces, waterproofs and aprons added as the weather and the role demand.",
 "Budget is the constraint that shapes everything else. Every pound a charity spends on kit is a pound not spent on the cause, so the workwear has to be affordable: a narrow, practical range of branded basics, ordered in any quantity with no minimum, not an expensive uniform programme. Polos and hi-vis do most of the work, with fleeces, waterproofs and aprons added as the weather and role demand.",
 "The budget shapes everything else. Because every pound spent on kit is a pound off the cause, the workwear has to be affordable: a narrow, practical range of branded basics, ordered in whatever quantity is needed with no minimum, rather than a costly uniform programme. Polos and hi-vis do most of the work, with fleeces, waterproofs and aprons added as the weather and the role demand.",
 "The budget is the constraint behind everything else. Every pound on kit is a pound not spent on the cause, so the workwear has to be affordable: a narrow, practical range of branded basics ordered in any quantity with no minimum, not an expensive uniform programme. Polos and hi-vis do most of the work, with fleeces, waterproofs and aprons added as the weather and role demand.",
]
CON_P3_POOL=[
 'The value is one affordable supplier covering the whole volunteer look, branded the same, for the {t} national charity and the local group alike. We hold your charity name, logo and sizes on file and supply the kit together, so kitting a new volunteer or opening a new shop reproduces the same branded look every time. Browse the range at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
 'The value is one affordable supplier for the whole volunteer look, the {t} national charity and the local group alike, branded the same. We hold your charity name, logo and sizes on file and supply the kit together, so a new volunteer or a new shop comes back the same branded look every time. Browse the range at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
 'The value is having one affordable supplier cover the whole volunteer look, branded the same, for both the {t} national charity and the local group. We keep your charity name, logo and sizes on file and supply the kit together, so a new volunteer or a new shop comes back the same branded look every time. Browse the range at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
 'The value is one affordable supplier for the entire volunteer look, the {t} national charity and the local group together, branded the same. We hold your charity name, logo and sizes on file and supply the kit as one, so kitting a new volunteer or opening a new shop reproduces the same look every time. Browse the range at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
]
ACC_HEAD="Trade Accounts for Charities, Direct Online for Volunteer Groups"
ACC_P1_POOL=[
 "The charity sector splits into two kinds of buyer, and we have built ordering for both. For a national charity with shops, branches and fundraising teams, a trade account is the practical route. It adds managed reordering, agreed pricing and a held kit list with your branding and sizes on file, so kitting a new volunteer, opening a new shop or rolling out across branches is consistent and easy to manage for a {t} charity. Send your numbers, your logo and your sizes and we will build the branded kit list and hold it.",
 "The charity sector has two kinds of buyer, and ordering is built for both. For a national {t} charity with shops, branches and fundraising teams, a trade account is the practical route: managed reordering, agreed pricing and a held kit list with your branding and sizes on file, so kitting a new volunteer, opening a new shop or rolling out across branches is consistent. Send your numbers, logo and sizes and we will build the branded kit list and hold it.",
 "The sector splits into two kinds of buyer, and we have built ordering for both. For a national charity with shops, branches and fundraising teams in {t}, a trade account is the practical route, adding managed reordering, agreed pricing and a held kit list with your branding and sizes on file, so kitting a volunteer, opening a shop or rolling out across branches stays consistent. Send your numbers, logo and sizes and we will build and hold the list.",
 "The charity sector splits into two kinds of buyer, and ordering suits both. For a national {t} charity running shops, branches and fundraising teams, a trade account is the practical route: managed reordering, agreed pricing and a held kit list with your branding and sizes on file, so kitting a new volunteer, opening a shop or rolling out across branches is consistent. Send your numbers, logo and sizes and we build the branded kit list and hold it.",
]
ACC_P2_POOL=[
 "For a small local foodbank, community group or volunteer-run project, ordering direct online is quickest and needs no account at all, and there is no minimum. Browse the range, pick your polos, hi-vis, fleeces or aprons, choose your sizes, send your logo once and check out. You can order a handful of pieces or a hundred, your kit is dispatched on standard lead times with embroidery added in-house, and your logo is held on file so the next order matches.",
 "For a small local foodbank, community group or volunteer project, direct online is quickest and needs no account, with no minimum: browse the range, pick your polos, hi-vis, fleeces or aprons, choose sizes, send your logo once and check out. Order a handful or a hundred, dispatched on standard lead times with embroidery in-house, and your logo held on file so the next order matches.",
 "A small local foodbank, community group or volunteer project orders quickest direct online, no account and no minimum: browse the range, pick your polos, hi-vis, fleeces or aprons, add sizes, send the logo once and check out. Order a few pieces or a hundred, dispatched on standard lead times with in-house embroidery, and your logo held on file for the next order.",
 "For a small foodbank, community group or volunteer project, the quickest route is direct online, no account and no minimum: browse, pick your polos, hi-vis, fleeces or aprons, choose sizes, send your logo once and check out, ordering a handful or a hundred, dispatched on standard lead times with embroidery in-house and your logo held on file.",
]
ACC_P3_POOL=[
 "Both routes are branded in-house from the same supplier and both are kept affordable, so whether you are kitting a national charity or a single {t} foodbank, the workwear is consistent, recognisable and easy on the budget. Most large charities run the trade account centrally and point their local branches and groups at the direct online route, and everyone ends up matching.",
 "Both routes are branded in-house by the same supplier and both are kept affordable, so whether you are kitting a national charity or a single {t} foodbank, the kit is consistent, recognisable and easy on the budget. Most large charities run the trade account centrally and send their branches and groups to the direct online route, and everyone matches.",
 "Both routes come branded in-house from one supplier and both stay affordable, so whether it is a national charity or a single foodbank in {t}, the workwear is consistent, recognisable and easy on the budget. Most large charities keep the trade account central and point local branches and groups at direct online, and everyone matches.",
 "Both routes are branded in-house by one supplier and kept affordable, so whether you kit a national charity or a single {t} foodbank, the kit stays consistent, recognisable and easy on the budget. Most large charities run the account centrally and send branches and groups to direct online, and everyone ends up matching.",
]
ACC_P4_POOL=[
 'Set up a trade account for a charity at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>, or order direct online with no account at <a href="https://www.ineedworkwear.com">iNeedWorkwear</a>.',
 'Set up a trade account for a charity at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>. For a small group, order direct online with no account at <a href="https://www.ineedworkwear.com">iNeedWorkwear</a>.',
 'Open a trade account for a charity at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>, or as a small group order direct online with no account at <a href="https://www.ineedworkwear.com">iNeedWorkwear</a>.',
 'Set up a charity trade account at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>, or as a volunteer group order direct online with no account at <a href="https://www.ineedworkwear.com">iNeedWorkwear</a>.',
]
# --- pool widening (4 -> 6 variants) for cross-page spread; link counts preserved
EMB_P1_POOL += [
 "For a charity, the look of its volunteers is part of how the public, donors and the people being helped place their trust. A clean, branded polo or hi-vis carrying the charity name signals at any {t} foodbank, collection, shop or community event who is official and who to turn to, so a willing volunteer becomes a recognisable, reassuring presence the moment they arrive.",
 "How volunteers present themselves is part of how a {t} charity is trusted by the public, donors and the people it serves. A tidy branded polo or hi-vis with the charity name shows at a glance, at a foodbank, a collection, a shop or an event, who is part of the team and who to approach, turning a willing volunteer into a recognisable and reassuring face.",
]
EMB_P2_POOL += [
 "Branding happens in-house: your charity name and logo are embroidered onto polos, hi-vis, fleeces and aprons and finished to take constant washing. We keep your artwork on file so every reorder and new volunteer lines up, and whether you are a single {t} community group or a national charity with shops nationwide, the look holds steady everywhere the name shows.",
 "We embroider in-house, putting your charity name and logo onto polos, hi-vis, fleeces and aprons and finishing them for heavy laundering. Your artwork stays on file, so each reorder and every new volunteer matches, and a lone {t} community group or a national charity with branches across the country looks the same wherever its name appears.",
]
EMB_P3_POOL += [
 "And with volunteer teams forever changing, that steadiness is what keeps a charity looking organised. We keep your branding and sizes on file, so kitting a new volunteer, opening another shop or covering a one-off event comes back the same branded look each time, with no artwork to resend and nothing paid over the odds.",
 "And because the volunteer roster never stops turning over, that steadiness is what keeps a charity looking organised. With your branding and sizes held on file, a new volunteer, a new shop or a single event reproduces the same branded look every time, without re-sending artwork and without paying more than you need to.",
]
CON_P1_POOL += [
 "Charity and volunteer workwear really has just one job, and a tight budget to do it on: recognition. A branded polo, hi-vis or fleece carrying the charity name makes a {t} volunteer instantly official to the public, to donors and to the people they are there to help, which builds trust and supports safeguarding at a foodbank, a collection, a shop or a community event. Everyone needs to see at a glance who belongs to the team.",
 "Charity and volunteer workwear comes down to one job done on a tight budget, and that job is recognition. A branded polo, hi-vis or fleece with the charity name makes a {t} volunteer official at a glance to the public, donors and the people they help, building trust and supporting safeguarding at a foodbank, collection, shop or community event, so it is clear straight away who is part of the team.",
]
CON_P2_POOL += [
 "Budget is what shapes the rest. Because every pound spent on kit is a pound taken from the cause, the workwear has to stay affordable: a tight, practical range of branded basics ordered in any quantity with no minimum, not a costly uniform scheme. Polos and hi-vis carry most of the load, with fleeces, waterproofs and aprons added as the weather and the role require.",
 "Everything else is shaped by the budget. Since every pound on kit is a pound away from the cause, the workwear must be affordable: a narrow, practical set of branded basics ordered in whatever number is needed with no minimum, rather than an expensive uniform programme. Polos and hi-vis do the bulk of the work, with fleeces, waterproofs and aprons added as weather and role demand.",
]
CON_P3_POOL += [
 'The value is a single affordable supplier covering the entire volunteer look, branded alike, for the {t} national charity and the local group together. We keep your charity name, logo and sizes on file and supply the kit as one, so kitting a new volunteer or opening a new shop returns the same branded look every time. Browse the range at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
 'The value is one affordable supplier handling the whole volunteer look, branded the same way, for both the {t} national charity and the local group. We hold your charity name, logo and sizes on file and send the kit together, so a new volunteer or a new shop comes back the same branded look each time. Browse the range at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
]
ACC_P1_POOL += [
 "The charity sector divides into two kinds of buyer, and we have built ordering for each. For a national charity with shops, branches and fundraising teams, a trade account is the sensible route: managed reordering, agreed pricing and a held kit list with your branding and sizes on file, so kitting a new volunteer, opening a shop or rolling out across branches stays consistent for a {t} charity. Send your numbers, logo and sizes and we will build the branded kit list and hold it.",
 "Buyers in the charity sector fall into two camps, and ordering is built for both. For a national {t} charity running shops, branches and fundraising teams, a trade account is the practical choice, bringing managed reordering, agreed pricing and a held kit list with your branding and sizes on file, so a new volunteer, a new shop or a branch roll-out stays consistent. Send your numbers, logo and sizes and we build and hold the branded kit list.",
]
ACC_P2_POOL += [
 "For a small local foodbank, community group or volunteer project, direct online ordering is the fastest route and needs no account, with no minimum: browse, choose your polos, hi-vis, fleeces or aprons, set your sizes, upload your logo once and check out. Order a few pieces or a hundred, dispatched on standard lead times with embroidery in-house, and your logo stays on file so the next order matches.",
 "A small local foodbank, community group or volunteer project gets going fastest direct online, with no account and no minimum: browse, pick your polos, hi-vis, fleeces or aprons, choose sizes, send your logo once and check out. Whether it is a handful of pieces or a hundred, the kit ships on standard lead times with in-house embroidery, and your logo is kept on file so the next order lines up.",
]
ACC_P3_POOL += [
 "Both routes are branded in-house by the same supplier and both stay affordable, so whether you are kitting a national charity or a single {t} foodbank, the workwear stays consistent, recognisable and gentle on the budget. Most large charities keep the trade account central and steer their branches and groups to direct online, and everyone ends up matching.",
 "Both routes come branded in-house from one supplier and both are kept affordable, so whether the order is for a national charity or a lone {t} foodbank, the kit stays consistent, recognisable and easy on the budget. Most big charities run the trade account centrally and send local branches and groups to direct online, so everyone matches in the end.",
]
ACC_P4_POOL += [
 'For a charity, open a trade account at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>; for a small volunteer group, order direct online with no account at <a href="https://www.ineedworkwear.com">iNeedWorkwear</a>.',
 'Start a charity trade account at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>, or as a small group order direct online with no account at <a href="https://www.ineedworkwear.com">iNeedWorkwear</a>.',
]
WHY_P1_POOL=[
 "A charity or volunteer group in {t} whose people turn out in clean, branded polos, hi-vis and fleeces looks organised, official and trustworthy to the public, donors and the people it helps, and iNeedWorkwear supplies that whole look from a single place, branded in-house and kept affordable, on a trade account for the national charity or direct online with no minimum for the local group, so the cause is well represented without overspending.",
 "A {t} charity or volunteer group whose people wear clean, branded polos, hi-vis and fleeces looks organised, official and trustworthy to the public, donors and the people it helps, and iNeedWorkwear supplies that whole look from one place, branded in-house and kept affordable, on a trade account for the national charity or direct online with no minimum for the local group, so the cause is well represented without overspending.",
 "When a {t} charity or volunteer group turns its people out in clean, branded polos, hi-vis and fleeces, it looks organised, official and trustworthy to the public, donors and the people it helps, and we supply that whole look from a single place, branded in-house and kept affordable, on a trade account or direct online with no minimum, so the cause is well represented without overspending.",
 "A charity or volunteer group in {t} whose people wear clean, branded polos, hi-vis and fleeces reads as organised, official and trustworthy to the public, donors and the people it helps, and we supply that whole look from one place, branded in-house and kept affordable, on a trade account for the national charity or direct online with no minimum for the local group, so the cause is well represented without overspending.",
 "A {t} charity or volunteer group whose people turn out in clean, branded polos, hi-vis and fleeces looks organised and trustworthy to the public, donors and the people it helps, and we supply the whole look from one place, branded in-house and kept affordable, trade or direct with no minimum, so even a tiny group looks official without overspending.",
 "In {t}, a charity or volunteer group whose people wear clean, branded polos, hi-vis and fleeces looks organised and official from the first glance, and iNeedWorkwear supplies that whole look from one place, branded in-house and kept affordable, on a trade account for the national charity or direct online with no minimum for the local group.",
]
WHY_P2_POOL=[
 "It is built for both ends of the sector. A national charity kitting volunteers across shops and branches gets managed reordering and a held kit list, while a small foodbank or community group gets a quick, no-account, no-minimum direct route online, and both come back the same branded kit, so a charity looks consistent everywhere its name appears.",
 "It is built for both ends of the sector. A national charity kitting volunteers across shops and branches gets managed reordering and a held kit list, and a small foodbank or community group gets a quick, no-account, no-minimum direct route online, with both coming back the same branded kit, so a charity looks consistent everywhere its name appears.",
 "It works for both ends of the sector. A national charity kitting volunteers across shops and branches gets managed reordering and a held kit list, while a small foodbank or group gets a quick, no-account, no-minimum online route, and both return the same branded kit, so a charity looks consistent everywhere its name appears.",
 "It suits both ends of the sector. A national charity kitting volunteers across shops and branches gets managed reordering and a held kit list, a small foodbank or community group gets a fast no-account, no-minimum online route, and both come back the same branded kit, so a charity stays consistent everywhere its name appears.",
 "It is made for both ends of the sector. The national charity gets managed reordering and a held kit list for kitting volunteers across shops and branches, the small group gets a quick no-account, no-minimum online route, and both return the same branded kit, so a charity looks consistent everywhere.",
 "It covers both ends of the sector. A national charity kitting volunteers across shops and branches leans on managed reordering and a held kit list, a small foodbank or group uses the quick no-account, no-minimum online route, and both come back the same branded kit, so a charity stays consistent everywhere its name appears.",
]
WHY_P3_POOL=[
 "The range is deliberately narrow and practical, built around what volunteers actually wear: polos and hi-vis for shops, events and collections, fleeces and waterproofs for the cold and wet, and aprons for shops and kitchens. That focus keeps it affordable and keeps choosing, ordering and reordering quick for a busy, budget-conscious charity.",
 "The range is deliberately narrow and practical, built around what volunteers really wear: polos and hi-vis for shops, events and collections, fleeces and waterproofs for the cold and wet, and aprons for shops and kitchens. That focus keeps it affordable and keeps choosing, ordering and reordering quick for a busy, budget-conscious charity.",
 "Everything in the range reflects what volunteers actually wear: polos and hi-vis for shops, events and collections, fleeces and waterproofs for the cold and wet, and aprons for shops and kitchens. The range is narrow and practical, which keeps it affordable and keeps ordering and reordering quick for a busy, budget-conscious charity.",
 "The range is built around what volunteers actually wear: polos and hi-vis for shops, events and collections, fleeces and waterproofs for the cold and wet, and aprons for shops and kitchens, kept deliberately narrow so it stays affordable and choosing and reordering stay quick for a busy, budget-conscious charity.",
 "It is a narrow, practical range mapped to volunteering: polos and hi-vis for shops, events and collections, fleeces and waterproofs for the cold and wet, and aprons for shops and kitchens, which keeps it affordable and keeps choosing, ordering and reordering fast for a busy, budget-conscious charity.",
 "The range stays narrow and practical, around what volunteers actually wear: polos and hi-vis for shops, events and collections, fleeces and waterproofs for the cold and wet, and aprons for shops and kitchens, so it stays affordable and a busy, budget-conscious charity can choose and reorder in minutes.",
]
WHY_P4_POOL=[
 "And everything is branded in-house, with your charity name and logo embroidered under our control and held on file, ready for the next order, the next volunteer or the next new shop, so every piece matches what the team already wears and a new volunteer looks official from their first shift.",
 "And everything is branded in-house, your charity name and logo embroidered under our control and held on file, ready for the next order, volunteer or new shop, so every piece matches what the team already wears and a new volunteer looks official from day one.",
 "And it is all branded in-house, with your charity name and logo embroidered under our control and kept on file, ready for the next order, the next volunteer or the next new shop, so every piece matches the team and a new volunteer looks official from their first shift.",
 "And everything is branded in-house, your charity name and logo embroidered under our control and held on file for the next order, volunteer or new shop, so each piece matches what the team wears and a new volunteer looks official from their first shift.",
 "And the whole lot is branded in-house, with your charity name and logo embroidered under our control and held on file, ready for the next order, volunteer or new shop, so every piece matches the team and a new volunteer looks official from day one.",
 "And it is all branded in-house, your charity name and logo embroidered under our control and on file, ready for the next order, the next volunteer or the next new shop, so every piece lines up with what the team already wears and a new volunteer looks official immediately.",
]
ORD_P1_POOL=[
 "iNeedWorkwear supplies branded polos, hi-vis, fleeces, waterproofs and aprons to charities, foodbanks, community groups and volunteer-run projects across {region}, all embroidered in-house with the charity name and kept affordable for a volunteer budget.",
 "We supply branded polos, hi-vis, fleeces, waterproofs and aprons to charities, foodbanks, community groups and volunteer-run projects across {region}, all embroidered in-house with the charity name and kept affordable for a volunteer budget.",
 "Across {region}, iNeedWorkwear kits charities, foodbanks, community groups and volunteer-run projects in branded polos, hi-vis, fleeces, waterproofs and aprons, all embroidered in-house with the charity name and kept affordable for a volunteer budget.",
 "From a single foodbank to a national charity across {region}, iNeedWorkwear supplies branded polos, hi-vis, fleeces, waterproofs and aprons to charities and volunteer groups, all embroidered in-house and kept affordable.",
]
ORD_P2_POOL=[
 "For a small foodbank, community group or volunteer project, ordering direct online is quickest and needs no account, with no minimum: browse the range, pick your polos, hi-vis, fleeces or aprons, add your sizes, send your logo once and check out. Your kit is dispatched on standard lead times with embroidery added in-house, and your logo is held on file so the next order matches.",
 "For a small foodbank, community group or volunteer project, direct online is quickest and needs no account, with no minimum: browse, pick your polos, hi-vis, fleeces or aprons, add sizes, send your logo once and check out. Your kit ships on standard lead times with embroidery in-house, and your logo is held on file so the next order matches.",
 "A small foodbank, community group or volunteer project orders quickest direct online, no account and no minimum: browse the range, pick your polos, hi-vis, fleeces or aprons, add sizes, send the logo once and check out. Kit is dispatched on standard lead times with in-house embroidery, and your logo is held on file for the next order.",
 "For a small foodbank or volunteer group, the quickest route is direct online, no account and no minimum: browse the range, pick your polos, hi-vis, fleeces or aprons, add your sizes, send your logo once and check out, dispatched on standard lead times with embroidery in-house and your logo held on file.",
]
ORD_P3_POOL=[
 "For a national charity with shops, branches and fundraising teams, a trade account adds managed reordering and agreed pricing: send your numbers, your logo and your sizes and we will build a branded kit list and hold it on file, so new volunteers and new shops are kitted consistently across the country.",
 "For a national charity with shops, branches and fundraising teams, a trade account brings managed reordering and agreed pricing: send your numbers, logo and sizes and we will build a branded kit list and hold it on file, so new volunteers and new shops are kitted consistently across the country.",
 "A national charity with shops, branches and fundraising teams can use a trade account for managed reordering and agreed pricing: send your numbers, logo and sizes and we will build a branded kit list and hold it on file, so new volunteers and shops are kitted consistently across the country.",
 "For a national charity with shops, branches and fundraising teams, a trade account adds managed reordering and agreed pricing: send your numbers, logo and sizes and we will build a branded kit list and keep it on file, so new volunteers and new shops are kitted consistently across the country.",
]
SELF_POOL=[
 'Setting up a new community group or foodbank and need kit now? Browse the full range, add your sizes and order direct on self-service checkout at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
 'Just started a new volunteer group or foodbank? Browse the range, add sizes and order direct on self-service checkout at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
 'Setting up a community group, pantry or foodbank and need kit today? Browse the full range, add your sizes and order direct on self-service checkout at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
 'Need volunteer kit sorted now? Browse the range, add sizes and order direct on self-service checkout at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
]
SORTED_POOL=[
 '<h3>Charity and Volunteer Workwear, Sorted</h3><p>From branded polos and hi-vis to fleeces, waterproofs and aprons, get affordable workwear built for charities, foodbanks and volunteer groups at fair prices - embroidered in-house with your charity name, on a trade account or ordered direct online with no account and no minimum.</p><p><a href="https://www.ineedworkwear.com">Browse charity and volunteer workwear at iNeedWorkwear</a></p>',
 '<h3>Charity and Volunteer Workwear, Sorted</h3><p>Branded polos and hi-vis, plus fleeces, waterproofs and aprons - affordable workwear for charities, foodbanks and volunteer groups at fair prices, embroidered in-house with your charity name, on a trade account or ordered direct online with no account and no minimum.</p><p><a href="https://www.ineedworkwear.com">Browse charity and volunteer workwear at iNeedWorkwear</a></p>',
 '<h3>Charity and Volunteer Workwear, Sorted</h3><p>From polos and hi-vis to fleeces, waterproofs and aprons, kit a national charity or a single foodbank at fair prices, embroidered in-house and ordered on a trade account or direct online with no account and no minimum.</p><p><a href="https://www.ineedworkwear.com">Browse charity and volunteer workwear at iNeedWorkwear</a></p>',
 '<h3>Charity and Volunteer Workwear, Sorted</h3><p>Polos, hi-vis, fleeces, waterproofs and aprons, the affordable kit for charities, foodbanks and volunteer groups at fair prices, embroidered in-house and ready on a trade account for the charity or direct online with no minimum for the group.</p><p><a href="https://www.ineedworkwear.com">Browse charity and volunteer workwear at iNeedWorkwear</a></p>',
]
OWNER_POOL=[
 "And the sector runs at every size, which shapes what a workwear supplier has to do. National and big regional charities operate shops, fundraising teams and outreach across many branches and buy centrally, while a huge layer of small community groups, foodbanks, pantries and volunteer-run projects work on a shoestring and just need a few branded pieces. A supplier has to serve the national charity and the one-room foodbank alike, with both a managed account and a quick direct route, no minimum.",
 "And the sector runs at every size, which shapes the supplier's job. National and big regional charities run shops, fundraising teams and outreach across many branches and buy centrally, while a huge layer of small community groups, foodbanks, pantries and volunteer-run projects work on a shoestring and want just a few branded pieces. A supplier has to serve the national charity and the one-room foodbank alike, with a managed account and a quick direct route, no minimum.",
 "And the sector runs at every size, which shapes what a supplier needs to do. National and big regional charities operate shops, fundraising teams and outreach across many branches and buy centrally, while a big layer of small community groups, foodbanks and volunteer-run projects work on a shoestring and need only a few branded pieces. A supplier has to handle the national charity and the single foodbank alike, offering both a managed account and a fast direct route with no minimum.",
 "And every size of organisation is in the mix, which shapes the supplier's job. National and big regional charities run shops, fundraising teams and outreach across branches and buy centrally, while a wide layer of small community groups, foodbanks and volunteer-run projects work on a shoestring and want a handful of branded pieces. A supplier has to serve the national charity and the one-room foodbank alike, with a managed account and a quick direct route, no minimum.",
 "And the sector spans every size, which shapes what a supplier must do. Big national and regional charities run shops, fundraising teams and outreach across many branches and buy centrally, while a large layer of small community groups, foodbanks, pantries and volunteer projects work on a shoestring and need just a few branded pieces. A supplier has to look after the national charity and the single foodbank alike, with both a managed account and a quick direct route with no minimum.",
 "And it runs on organisations of every size, which shapes the supplier's job. The national and big regional charities run shops, fundraising teams and outreach across branches and buy centrally, while a deep layer of small community groups, foodbanks and volunteer-run projects work on a shoestring and want only a few branded pieces. A supplier has to cover the national charity and the one-room foodbank alike, with a managed account and a quick direct route, no minimum.",
]
PRESENT_POOL=[
 "And the kit really has one job, done on a budget, which is what makes charity and volunteer workwear its own thing. It has to make a {t} volunteer instantly recognisable and official, so the public, donors and the people being helped can see at a glance who to trust at a foodbank, a collection, a charity shop or a community event. And it has to do that affordably, because every pound on kit is a pound off the cause, so it is a narrow range of branded basics, not an expensive uniform.",
 "And the kit really has one job, done on a budget, which is what sets charity and volunteer workwear apart. It has to make a {t} volunteer instantly recognisable and official, so the public, donors and the people being helped can see at a glance who to trust at a foodbank, a collection, a shop or an event. And it has to do that affordably, because every pound on kit is a pound off the cause, so it is a narrow range of branded basics, not an expensive uniform.",
 "And the kit really has one job, done on a tight budget, which is the heart of charity and volunteer workwear. It must make a {t} volunteer instantly recognisable and official, so the public, donors and the people being helped can see at a glance who to trust at a foodbank, collection, shop or community event. And it has to be affordable, because every pound on kit is a pound off the cause, so it is a narrow range of branded basics, not a costly uniform.",
 "And the kit does one job on a budget, which is what makes this workwear distinct. It has to make a {t} volunteer instantly recognisable and official, so the public, donors and the people being helped can see at a glance who to trust at a foodbank, a collection, a shop or a community event. And it has to do it affordably, because every pound on kit is a pound off the cause, so it is a narrow range of branded basics, not an expensive uniform.",
 "And the kit really has a single job, done cheaply, which is what makes charity and volunteer workwear its own thing. It must make a {t} volunteer instantly recognisable and official, so the public, donors and the people being helped can see who to trust at a foodbank, collection, shop or event. And it has to be affordable, because every pound on kit is a pound off the cause, so it is a narrow range of branded basics, not an expensive uniform.",
 "And the kit comes down to one job on a budget, which is what distinguishes charity and volunteer workwear. It has to make a {t} volunteer instantly recognisable and official, so the public, donors and the people being helped can see at a glance who to trust at a foodbank, a collection, a shop or a community event. And it has to be affordable, because every pound on kit is a pound off the cause, so it is a narrow range of branded basics, not a costly uniform.",
]
NARROW_POOL=[
 "Because volunteers come and go all the time, it is a repeat-purchase trade, and the range is built to reorder easily with no minimum. Polos, hi-vis, fleeces, waterproofs and aprons, branded in-house with the charity name, are the whole kit, and we hold your logo on file so the next order or the next new volunteer in {t} matches what the team already wears.",
 "Because volunteers come and go all the time, this is a repeat-purchase trade, and the range is built to reorder easily with no minimum. Polos, hi-vis, fleeces, waterproofs and aprons, branded in-house with the charity name, are the whole kit, and your logo is held on file so the next order or new volunteer in {t} matches what the team already wears.",
 "Since volunteers come and go constantly, it is a repeat-purchase trade, and the range is built to reorder easily with no minimum. Polos, hi-vis, fleeces, waterproofs and aprons, branded in-house with the charity name, are the whole kit, and we keep your logo on file so the next order or new volunteer in {t} matches what the team already wears.",
 "Because volunteer teams turn over constantly, it is a repeat-purchase trade, and the range reorders easily with no minimum. Polos, hi-vis, fleeces, waterproofs and aprons, branded in-house with the charity name, are the whole kit, and your logo sits on file so the next order or new volunteer in {t} matches what the team already wears.",
 "As volunteers come and go all the time, it is a repeat-purchase trade, and the range is built to reorder fast with no minimum. Polos, hi-vis, fleeces, waterproofs and aprons, branded in-house with the charity name, are the whole kit, and we hold your logo on file so the next order or new volunteer in {t} matches what the team already runs.",
 "Because the volunteer team churns constantly, it is a repeat-purchase trade, and the range is built for easy reordering with no minimum. Polos, hi-vis, fleeces, waterproofs and aprons, branded in-house with the charity name, are the whole kit, and your logo is on file so the next order or new volunteer in {t} lines up with what the team already wears.",
]
KIT_POOL=[
 "Polos, hi-vis, fleeces, waterproofs and aprons, branded with the charity name, are the whole kit {loc}.",
 "The whole kit is polos, hi-vis, fleeces, waterproofs and aprons, branded with the charity name {loc}.",
 "Polos, hi-vis, fleeces, waterproofs and aprons do the job, branded with the charity name {loc}.",
 "It comes down to polos, hi-vis, fleeces, waterproofs and aprons, branded with the charity name {loc}.",
 "Polos, hi-vis, fleeces, waterproofs and aprons, all branded with the charity name, are the kit {loc}.",
 "Branded polos, hi-vis, fleeces, waterproofs and aprons make up the whole kit {loc}.",
]
S2TAIL_POOL=[
 ", polos, hi-vis and fleeces lead, with waterproofs and aprons alongside.",
 ", the core is polos, hi-vis and fleeces, with waterproofs and aprons to finish.",
 ", expect polos, hi-vis and fleeces first, then waterproofs and aprons.",
 ", polos, hi-vis and fleeces do the work, with waterproofs and aprons alongside.",
 ", polos, hi-vis and fleeces anchor the kit, with waterproofs and aprons completing it.",
 ", it is polos, hi-vis and fleeces, plus waterproofs and aprons.",
]

SNAP_TMPL=("iNeedWorkwear supplies branded polos, hi-vis, fleeces, waterproofs and aprons to "
 "charities, charity shops, foodbanks and volunteer groups across {t}, embroidered in-house with "
 "the charity name. The sector runs from national charities with shops and branches to tiny local "
 "groups on a shoestring, so a larger charity can run a trade account for managed reordering, while "
 "a small group can order direct online with no account and no minimum.")
KIT_LOC_DEFAULT="across the area's shops, foodbanks and community events"

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
     (f"Do you supply branded workwear to charities and volunteer groups in {t}?", P('fq1',[
      f"Yes. Charities, charity shops, foodbanks, community groups and volunteer-run projects across {region} get branded polos, hi-vis, fleeces, waterproofs and aprons from us, embroidered in-house with the charity name. A national charity can run a trade account for managed reordering across branches, and a small local group can order direct online with no account and no minimum.",
      f"Yes. Branded polos, hi-vis, fleeces, waterproofs and aprons go to charities, charity shops, foodbanks, community groups and volunteer-run projects across {region}, embroidered in-house with the charity name. A national charity runs a trade account for managed reordering, and a small local group orders direct online with no account and no minimum.",
      f"Yes. From a one-room foodbank to a national charity across {region}, we supply branded polos, hi-vis, fleeces, waterproofs and aprons, embroidered in-house with the charity name, on a trade account or direct online with no account and no minimum.",
      f"Yes. Charities, foodbanks, community groups and volunteer-run projects across {region} get branded polos, hi-vis, fleeces, waterproofs and aprons from us, embroidered in-house with the charity name, on a trade account or ordered direct online with no minimum.",
      f"Yes. Across {region} we kit charities, charity shops, foodbanks and volunteer groups in branded polos, hi-vis, fleeces, waterproofs and aprons, embroidered in-house with the charity name, on a trade account or direct online with no minimum for a small group.",
      f"Yes. Charities and volunteer groups across {region}, from a single foodbank to a national charity, get branded polos, hi-vis, fleeces, waterproofs and aprons from us, embroidered in-house with the charity name, on a trade account or direct online with no account and no minimum."])),
     ("Is there a minimum order for a small volunteer group?", P('fq2',[
      "No. A small foodbank or community group can order direct online with no account and no minimum, picking just the few branded polos, hi-vis or fleeces they need. The kit is kept affordable on purpose, because money spent on workwear is money not spent on the cause, and your logo is held on file so the next order matches.",
      "No. A small foodbank or community group orders direct online with no account and no minimum, picking just the few branded polos, hi-vis or fleeces they need. The kit is kept affordable on purpose, because money on workwear is money off the cause, and your logo is held on file so the next order matches.",
      "No, there is no minimum. A small foodbank or community group can order direct online with no account, picking just the branded polos, hi-vis or fleeces they need. The kit is kept affordable on purpose, and your logo is held on file so the next order matches.",
      "No minimum at all. A small foodbank or community group orders direct online with no account, picking only the few branded polos, hi-vis or fleeces they need, kept affordable because money on kit is money off the cause, with your logo held on file so the next order matches.",
      "No. There is no minimum, so a small foodbank or community group can order direct online with no account, picking just the branded polos, hi-vis or fleeces they need, kept affordable on purpose, with your logo on file so the next order matches.",
      "No, no minimum. A small foodbank or community group orders direct online with no account, taking just the few branded polos, hi-vis or fleeces they need, kept affordable because every pound on kit is a pound off the cause, with your logo held on file for next time."])),
     ("What workwear do charity and volunteer teams usually need?", P('fq3',[
      "The core kit is branded polos and t-shirts for shops, events and day-to-day volunteering, hi-vis vests for collections, marshalling and outdoor work, fleeces and waterproofs for cold and wet conditions, and aprons for charity shops and foodbank kitchens, all branded with the charity name so volunteers are recognisable and official.",
      "The core is branded polos and t-shirts for shops, events and everyday volunteering, hi-vis for collections, marshalling and outdoor work, fleeces and waterproofs for cold and wet conditions, and aprons for shops and foodbank kitchens, all branded with the charity name so volunteers are recognisable.",
      "At its core: branded polos and t-shirts for shops, events and day-to-day volunteering, hi-vis for collections, marshalling and outdoor work, fleeces and waterproofs for the cold and wet, and aprons for charity shops and foodbank kitchens, all branded with the charity name.",
      "The core uniform is branded polos for shops, events and everyday volunteering, hi-vis for collections and outdoor work, fleeces and waterproofs for cold and wet conditions, and aprons for shops and foodbank kitchens, all branded with the charity name so volunteers are recognisable and official.",
      "It comes down to branded polos for shops, events and day-to-day volunteering, hi-vis for collections and outdoor work, fleeces and waterproofs for the cold and wet, and aprons for shops and kitchens, all branded with the charity name and kept affordable.",
      "Branded polos and t-shirts for shops, events and everyday volunteering, hi-vis for collections and outdoor work, fleeces and waterproofs for the cold and wet, and aprons for shops and kitchens make up the core, all branded with the charity name so volunteers are recognisable."])),
     ("Why does branding matter so much for volunteers?", P('fq4',[
      "A branded polo or hi-vis instantly marks a volunteer out as official to the public, donors and the people they help, which builds trust and supports safeguarding at a foodbank, a collection, a charity shop or a community event. We embroider the charity name and logo in-house, turning an affordable polo into recognisable, trusted kit.",
      "A branded polo or hi-vis instantly marks a volunteer out as official to the public, donors and the people they help, building trust and supporting safeguarding at a foodbank, collection, shop or community event. We embroider the charity name and logo in-house, turning an affordable polo into recognisable, trusted kit.",
      "A branded polo or hi-vis makes a volunteer instantly official to the public, donors and the people they help, which builds trust and supports safeguarding at a foodbank, a collection, a shop or a community event. We embroider the charity name and logo in-house, turning an affordable polo into recognisable kit.",
      "A branded polo or hi-vis instantly identifies a volunteer as official to the public, donors and the people they help, building trust and supporting safeguarding at a foodbank, collection, shop or event. We embroider the charity name and logo in-house, turning an affordable polo into recognisable, trusted kit.",
      "Branding makes a volunteer instantly recognisable as official to the public, donors and the people they help, which builds trust and supports safeguarding at a foodbank, a collection, a shop or a community event. We embroider the charity name and logo in-house, turning an affordable polo into trusted kit.",
      "A branded polo or hi-vis marks a volunteer out as official at a glance to the public, donors and the people they help, building trust and supporting safeguarding at a foodbank, collection, shop or event. The charity name and logo are embroidered in-house, turning an affordable polo into recognisable, trusted kit."])),
     ("Can you embroider our charity name and logo?", P('fq5',[
      "Yes. We embroider your charity name and logo in-house onto polos, hi-vis, fleeces and aprons, finished to survive frequent washing. Send your artwork once, we hold it on file, and every reorder and new volunteer matches, so a national charity or a small local group looks organised and official across every shop, branch and event.",
      "Yes. Your charity name and logo are embroidered in-house onto polos, hi-vis, fleeces and aprons, finished for frequent washing. Send artwork once and we hold it on file, so every reorder and new volunteer matches, and a national charity or a small group looks organised across every shop, branch and event.",
      "Yes, all branding is done in-house onto polos, hi-vis, fleeces and aprons, finished to survive frequent washing. We hold your artwork on file, so every reorder and new volunteer matches and a national charity or a small local group looks organised and official.",
      "Yes. Send your artwork once and we embroider your charity name and logo in-house onto polos, hi-vis, fleeces and aprons, holding it on file so every reorder and new volunteer matches, and a national charity or a small group looks organised across every shop, branch and event.",
      "Yes. Charity name and logo are embroidered in-house onto polos, hi-vis, fleeces and aprons, finished for frequent washing and held on file, so every reorder and new volunteer matches and a national charity or a small group stays organised and official.",
      "Yes, embroidery is done in-house onto polos, hi-vis, fleeces and aprons, finished to take frequent washing. Send your logo once and we keep it on file, so reorders and new volunteers line up and a national charity or a small local group looks organised and official."])),
     ("Do you supply hi-vis for collections and outdoor volunteering?", P('fq6',[
      "Yes. Alongside the polos and fleeces we supply hi-vis vests and waistcoats for street collections, event marshalling, litter picks, conservation work and other outdoor volunteering, plus waterproofs for the wet, all able to be branded with the charity name and kept affordable for a volunteer budget.",
      "Yes. As well as polos and fleeces, we supply hi-vis vests and waistcoats for collections, marshalling, litter picks, conservation and other outdoor volunteering, plus waterproofs for the wet, all able to be branded with the charity name and kept affordable for a volunteer budget.",
      "Yes, we supply hi-vis vests and waistcoats alongside the polos and fleeces, for street collections, marshalling, litter picks, conservation and outdoor volunteering, plus waterproofs for the wet, all branded with the charity name and kept affordable.",
      "Yes. Beyond the polos and fleeces, we supply hi-vis vests and waistcoats for collections, marshalling, litter picks, conservation and outdoor volunteering, plus waterproofs for the wet, all branded with the charity name and kept affordable for a volunteer budget.",
      "Yes. The outdoor layers are covered too: hi-vis vests and waistcoats for collections, marshalling, litter picks and conservation alongside the polos and fleeces, plus waterproofs for the wet, all branded with the charity name and kept affordable.",
      "Yes. We supply hi-vis vests and waistcoats with the polos and fleeces, for street collections, marshalling, litter picks, conservation and outdoor volunteering, plus waterproofs for the wet, all branded with the charity name and kept affordable for a volunteer budget."])),
     ("How affordable is charity and volunteer workwear?", P('fq7',[
      "The range is deliberately narrow and kept at fair prices, because every pound spent on kit is a pound not spent on the cause. Order direct online with no account and no minimum, or set up a trade account for a national charity for managed reordering and agreed pricing, with embroidery added in-house either way on standard lead times.",
      "The range is deliberately narrow and kept at fair prices, because every pound on kit is a pound not spent on the cause. Order direct online with no account and no minimum, or set up a trade account for a national charity for managed reordering and agreed pricing, with embroidery added in-house on standard lead times.",
      "It is kept affordable on purpose: a narrow range at fair prices, because every pound spent on kit is a pound off the cause. Order direct online with no account and no minimum, or set up a trade account for a national charity for managed reordering and agreed pricing, with embroidery in-house on standard lead times.",
      "The range is narrow and kept at fair prices, because every pound on kit is a pound not spent on the cause. Order direct online with no account and no minimum, or set up a trade account for a national charity for managed reordering and agreed pricing, embroidery added in-house either way on standard lead times.",
      "Affordability is the point: a deliberately narrow range at fair prices, because money on kit is money off the cause. Order direct online with no account and no minimum, or run a trade account for a national charity with managed reordering and agreed pricing, with embroidery in-house on standard lead times.",
      "The range is narrow and priced fairly on purpose, because every pound spent on kit is a pound off the cause. Order direct online with no account and no minimum, or set up a trade account for a national charity for managed reordering and agreed pricing, with embroidery added in-house on standard lead times."])),
    ]

TOWNS = {
 "birmingham": {
  "region":"Birmingham and the West Midlands",
  "nearby":["Solihull","West Bromwich","Walsall"],
  "snapshot":"iNeedWorkwear supplies branded polos, hi-vis, fleeces, waterproofs and aprons to charities, charity shops, foodbanks and volunteer groups across Birmingham, embroidered in-house with the charity name. The sector runs from national charities with shops and branches to tiny local groups on a shoestring, so a larger charity can run a trade account for managed reordering, while a small group can order direct online with no account and no minimum.",
  "s1_head":"Kitting the volunteers of the West Midlands",
  "s1loc":[
   "Birmingham has one of the largest charity sectors outside London, with well over 2,000 registered charities and a deep third-sector tradition. FareShare Midlands redistributes surplus food from its Birmingham warehouse to hundreds of charity and community group members, the Midland Langar Seva Society and foodbanks like Birmingham Central and B30 feed people across the city, and long-standing charities from Birmingham Settlement, founded in 1899, to St Basil's and Midland Mencap work alongside hospices, faith groups and mutual-aid networks.",
   "And the sector runs at every size. National and big regional charities operate shops, fundraising teams and outreach across many branches and buy centrally, while a huge layer of small community groups, foodbanks, pantries and volunteer-run projects work on a shoestring and just need a few branded pieces. A workwear supplier here has to serve the national charity and the one-room foodbank alike, which is why we run trade accounts and direct online ordering, with no minimum, side by side.",
  ],
  "kit_loc":"across the city's shops, foodbanks and community events",
  "s2_intro":"Whether you are a national charity with shops across Birmingham, a FareShare-supplied community group or a small volunteer-run foodbank in Solihull",
 },
 "leeds": {
  "region":"Leeds and West Yorkshire",
  "nearby":["Bradford","Pudsey","Dewsbury"],
  "snapshot":"iNeedWorkwear supplies branded polos, hi-vis, fleeces, waterproofs and aprons to charities, charity shops, foodbanks and volunteer groups across Leeds, embroidered in-house with the charity name. The sector runs from national charities with shops and branches to tiny local groups on a shoestring, so a larger charity can run a trade account for managed reordering, while a small group can order direct online with no account and no minimum.",
  "s1_head":"Kitting the volunteers of Yorkshire",
  "s1loc":[
   "Leeds has a busy, volunteer-driven charity sector. FareShare Yorkshire runs a volunteer-driven centre in the city, supplying hundreds of charities and community groups with surplus food, the Trussell foodbanks Leeds North and West and Leeds South and East hand out tens of thousands of food parcels a year, and independent providers like Right Choices in Headingley, the Holbeck and Bramley foodbanks and FoodCycle community meals in Harehills run almost entirely on volunteers, coordinated through the Leeds Food Aid Network and Leeds Community Foundation.",
   "And the sector runs the full range of sizes. Big charity networks operate shops, distribution centres and fundraising teams and buy centrally, while small foodbanks, pantries, soup kitchens and volunteer-run projects across Harehills, Beeston, Burley and Bramley work on a shoestring and just need a few branded pieces. A workwear supplier has to kit the national charity and the one-room foodbank alike, which is why we run trade accounts for the big charities and direct online ordering, with no minimum, for everyone else.",
  ],
  "kit_loc":"across the city's shops, foodbanks and community events",
  "s2_intro":"Whether you are a charity with shops across Leeds, a FareShare-supplied community group or a small volunteer-run foodbank toward Pudsey",
 },
}

def _load_extra_towns():
    here=os.path.dirname(os.path.abspath(__file__))
    d=os.path.join(here,'towns')
    if not os.path.isdir(d): return
    for fn in sorted(os.listdir(d)):
        if fn.endswith('.json'):
            for k,v in json.load(open(os.path.join(d,fn),encoding='utf-8')).items():
                TOWNS[k.lower()]=v
_load_extra_towns()

_CSV=None
def _load_csv():
    global _CSV
    if _CSV is not None: return _CSV
    here=os.path.dirname(os.path.abspath(__file__))
    for p in (os.path.join(here,'CH2_towns.csv'),'CH2_towns.csv','/mnt/user-data/outputs/CH2_towns.csv'):
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
    global _DISPLAY
    if _DISPLAY is None:
        _DISPLAY={slugify(t): t for (_r,t,_n) in _load_csv()}
    return _DISPLAY
def town_display(key):
    return _display_map().get(slugify(key)) or ' '.join(w.capitalize() for w in key.split())
def _entry(town):
    s=slugify(town)
    for k,v in TOWNS.items():
        if slugify(k)==s: return v
    raise KeyError(town)

def require_nearby(town, T):
    nb = T.get("nearby")
    if not nb or len(nb) < 3:
        raise ValueError(f"{town}: 'nearby' must list 3 geographically-close towns "
                         f"(web-verified, all on CH2_towns.csv). No rank/auto fallback.")
    bad = [n for n in nb if not any(r[1].lower()==n.lower() for r in _load_csv())]
    if bad:
        raise ValueError(f"{town}: nearby town(s) not on CH2_towns.csv: {bad}")
    return nb[:3]

def build_title(town):
    for t in (f"{town} Charity and Volunteer Workwear",
              f"{town} Charity Volunteer Workwear", f"{town} Charity Workwear"):
        if len(t) <= 60: return t
    return f"{town} Charity Workwear"

def build_meta(town):
    for m in (f"Branded polos, hi-vis, fleeces and waterproofs for {town} charities, foodbanks and volunteer groups - affordable, no minimum, in-house embroidery.",
              f"Affordable branded polos, hi-vis and fleeces for {town} charities, foodbanks and volunteer groups - no minimum, trade or direct, in-house embroidery.",
              f"Branded polos, hi-vis and fleeces for {town} charities and volunteer groups - affordable, no minimum, trade accounts or order direct online.",
              f"Affordable charity workwear for {town} volunteer groups - branded polos, hi-vis and fleeces, no minimum, in-house embroidery, trade or direct."):
        if len(m) <= 160: return m
    return f"Affordable charity workwear for {town} volunteer groups - polos, hi-vis, fleeces, no minimum, trade or direct."

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
        "name":f"Charity and Volunteer Workwear Supply and Embroidery in {town}",
        "serviceType":"Charity and volunteer workwear and embroidery supply",
        "provider":{"@id":"https://www.ineedworkwear.com/#organization"},
        "areaServed":[{"@type":"City","name":town}]+[{"@type":"City","name":n} for n in nearby],
        "audience":{"@type":"BusinessAudience","name":"Charities, non-profits, foodbanks and volunteer groups"},
        "description":f"Branded polos, hi-vis, fleeces, waterproofs and aprons supplied to charities, foodbanks and volunteer groups in {town}, on a trade account or direct online with no minimum, with in-house embroidery.",
        "hasOfferCatalog":{"@type":"OfferCatalog","name":"Charity and Volunteer Workwear",
            "itemListElement":[{"@type":"Offer","itemOffered":{"@type":"Product","name":p}} for p in CH2_PRODUCTS]}}
    crumb = {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Home","item":DOMAIN},
        {"@type":"ListItem","position":2,"name":"Charity and Volunteer Workwear","item":f"{DOMAIN}/charity-volunteer-workwear"},
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

    emb_svg   = EMB.replace('a London charity logo', f'a {town} charity logo')
    sign_svg  = SIGNPOST.replace('London charity and volunteer signpost', f'{town} charity and volunteer signpost')
    sign_svg  = re.sub(r'<text x="230" y="62".*?</text>', signpost_town(town), sign_svg, flags=re.S)
    sign_svg  = sign_svg.replace('every kind of London volunteer', f'every kind of {town} volunteer')
    prem_svg  = PREMISES.replace('serving volunteers across London', f'serving volunteers across {town}')

    H=[build_head(town, slug, faqs, nearby), HEADER]
    H.append(f'<div class="ch2-hero"><div class="ch2-wrap"><div class="ch2-subtitle">Branded Workwear for Charities, Non-Profits and Volunteers</div><h1>{town} Charity and Volunteer Workwear</h1></div></div>')
    H.append('<div class="ch2-pulse"></div>')
    H.append(f'<div class="ch2-trust-strip"><p>{trust}</p></div>')
    H.append(f'<div class="ch2-wrap"><div class="ch2-snapshot"><div class="ch2-snapshot-label">Supplier Snapshot</div><p>{snap}</p></div></div>')
    H.append(STATS)
    H.append('<div class="ch2-cta-bar"><a href="https://www.ineedworkwear.com" class="ch2-cta-btn">Browse Charity and Volunteer Workwear</a></div>')
    H.append('<div class="ch2-jump-links"><a href="#range">Workwear Range</a><a href="#contract">The Kit</a><a href="#accounts">Ordering and Accounts</a><a href="#order">How to Order</a></div>')
    H.append(GARMENT)
    H.append(f'<div class="ch2-section"><div class="ch2-wrap"><h2>{s1head}</h2>'+''.join(f'<p>{p}</p>' for p in s1ps)+'</div></div>')
    H.append(f'<div class="ch2-section" id="range"><div class="ch2-wrap"><h2>Charity and Volunteer Workwear Range</h2><p>{s2intro} <a href="https://www.ineedworkwear.com">Browse the full range at iNeedWorkwear.com</a>.</p><p class="ch2-btn-center"><a href="https://www.ineedworkwear.com" class="ch2-section-btn">Browse The Range</a></p>{grid}</div></div>')
    H.append(f'<div class="ch2-section"><div class="ch2-wrap"><h2>Branding for a National Charity or a Local Volunteer Group</h2>'+''.join(f'<p>{p}</p>' for p in emb)+'</div></div>')
    H.append(emb_svg)
    H.append(f'<div class="ch2-wrap"><div class="ch2-contract" id="contract"><h3>{CON_HEAD}</h3>'+''.join(f'<p>{p}</p>' for p in con)+'</div></div>')
    H.append(sign_svg)
    H.append(f'<div class="ch2-section" id="accounts"><div class="ch2-wrap"><h2>{ACC_HEAD}</h2>'+''.join(f'<p>{p}</p>' for p in acc)+'</div></div>')
    H.append(prem_svg)
    H.append(f'<div class="ch2-section"><div class="ch2-wrap"><h2>Why Charities and Volunteer Groups Choose iNeedWorkwear</h2>'+''.join(f'<p>{p}</p>' for p in why)+'</div></div>')
    H.append(ORDER)
    H.append(f'<div class="ch2-section" id="order"><div class="ch2-wrap"><h2>How to Order Charity and Volunteer Workwear</h2><p>{ordr[0]}</p><p>{ordr[1]}</p><p>{ordr[2]}</p><p class="ch2-btn-center"><a href="https://www.ineedworkwear.com" class="ch2-section-btn">Browse And Order Online</a></p><p>{selfp}</p>'+CONTACT+'</div></div>')
    faq_html=''.join(f'<div class="ch2-faq-item"><div class="ch2-faq-q">{q}</div><div class="ch2-faq-a">{a}</div></div>' for q,a in faqs)
    H.append(f'<div class="ch2-faq"><div class="ch2-wrap"><h2>Charity and Volunteer Workwear FAQ</h2>{faq_html}</div></div>')
    H.append(f'<div class="ch2-wrap"><div class="ch2-workwear">{sorted_}</div></div>')
    nb_links=''.join(f'<a href="ch2-{slugify(n)}.html">Charity and volunteer workwear in {n}</a>\n' for n in nearby)
    H.append(f'<div class="ch2-nearby"><div class="ch2-wrap"><h3>Charity and Volunteer Workwear in Nearby Towns</h3><div class="ch2-nearby-links">{nb_links}</div></div></div>')
    H.append(FOOTER+'\n</body></html>')
    return '\n'.join(H)

def main():
    args=[a for a in sys.argv[1:]]
    outdir=(os.environ.get('CH_OUTDIR')
            or ('/mnt/user-data/outputs' if os.path.isdir('/mnt/user-data/outputs')
                else 'outputs'))
    os.makedirs(outdir, exist_ok=True)
    if not args:
        args=[t for t in TOWNS if t!='london']
    known={slugify(k) for k in TOWNS}
    for town_key in args:
        s=slugify(town_key)
        if s=='london': continue
        if s not in known:
            print(f"SKIP {town_key}: not in TOWNS (must be web-researched first)"); continue
        town=town_display(town_key)
        slug=f"ch2-{s}"
        html=assemble(slug, town)
        path=os.path.join(outdir, f"{slug}.html")
        open(path,'w',encoding='utf-8').write(html)
        print(f"WROTE {path}  ({len(html.split())} words approx)")

if __name__=='__main__':
    main()
