#!/usr/bin/env python3
# CP (Corporate & Professional Services) series builder v1.0 - read SPEC.md/CLAUDE.md
# Audience PROCUREMENT, tone CONCIERGE (NOT hybrid). The buyer is a procurement,
# office, HR or brand manager at a bank, law firm, accountancy, consultancy, insurer
# or technology company. Corporate workwear here is a BRAND EXERCISE, not a daily
# uniform: branded polos, shirts, softshells and fleeces for away days, conferences,
# exhibitions, site visits, sponsored/fundraising events and new-starter welcome packs.
# DIFFERENTIATOR = ON-BRAND (exact logo/colours, embroidered to brand guidelines, brand
# pack held on file) + ACCOUNT-MANAGED (single point of contact, held kit list, managed
# reorders and multi-office rollouts, agreed pricing). Lead = POLO + SOFTSHELL + FLEECE.
# softshell is CORE (removed from bleed). LOW depth, LOW variation (2 local s1loc paras;
# generic shared paras in OWNER/PRESENT/NARROW pools). No JS, no entities, no delivery
# claims. Exactly 14 .com + 1 community per page. Nearby = geographic, on CP_towns.csv.
# AVOID in copy: charity (use fundraising/sponsored), festival/stage/crew/front-of-house/
# concert (EV signatures). Prefix cp-.
import re, os, json, sys, csv
import hashlib
def pick(key, salt, n):
    h = hashlib.md5((salt + '|' + str(key).lower()).encode()).digest()
    return int.from_bytes(h[:4], 'big') % n

def _find_base():
    here = os.path.dirname(os.path.abspath(__file__))
    for p in (os.path.join(here,'cp-london.html'),'cp-london.html',
              '/mnt/user-data/outputs/cp-london.html','/home/claude/cpkit/cp-london.html'):
        if os.path.exists(p): return p
    sys.exit("ERROR: cp-london.html (base template) not found beside cp_build.py")

BASE = open(_find_base(), encoding='utf-8').read()
DOMAIN = 'https://www.ineedworkwear.uk'

def between(start, end, src=BASE):
    i = src.index(start); j = src.index(end, i+len(start)); return src[i:j]
def aria_block(aria):
    k = BASE.index(aria)
    i = BASE.rfind('<div class="cp-wrap"><div class="cp-illust">', 0, k)
    j = BASE.index('</div></div></div>', k) + len('</div></div></div>')
    return BASE[i:j]

CSS      = between('<style>', '</style>') + '</style>'
HEADER   = between('<div class="cp-header">', '\n<div class="cp-hero">')
STATS    = between('<div class="cp-stats">', '\n<div class="cp-cta-bar">')
GARMENT  = between('<div class="cp-wrap"><div class="cp-illust"><div class="cp-garment-row">', '\n<div class="cp-section">')
EMB      = aria_block('Embroidery machine stitching')
SIGNPOST = aria_block('corporate and professional services sign')
PREMISES = aria_block('serving professional services firms across')
ORDER    = aria_block('Order corporate and professional services workwear online')
CONTACT  = BASE[BASE.index('<div class="cp-contact-block">'):
                BASE.index('</div></div></div>', BASE.index('<div class="cp-contact-block">'))+len('</div></div></div>')]
FOOTER   = BASE[BASE.index('<footer class="cp-footer">'):BASE.index('</footer>')+len('</footer>')]

def sign_town(town):
    # centred monument-sign town text (x230 y138); logo mark sits above, strapline below
    n = len(town)
    size = 26 if n <= 8 else 22 if n <= 11 else 18 if n <= 15 else 15 if n <= 20 else 13
    tl = ' textLength="240" lengthAdjust="spacingAndGlyphs"' if n > 14 else ''
    return (f'<text x="230" y="138" text-anchor="middle" font-family="Arial,sans-serif" '
            f'font-weight="700" font-size="{size}" fill="#ffffff" letter-spacing="2"{tl}>{town.upper()}</text>')

CP_PRODUCTS = ["Polo Shirts and T-Shirts","Branded Corporate Shirts","Softshell Jackets",
 "Fleeces and Mid-Layers","Quarter-Zips and Sweatshirts","Gilets and Bodywarmers",
 "Caps and Accessories","Logo and Brand-Mark Embroidery"]

def _card(n,d): return f'<div class="cp-product-card"><div class="cp-product-name">{n}</div><div class="cp-product-detail">{d}</div></div>'
CARD_DETAILS=[
 ("Polo Shirts and T-Shirts",[
   "Branded polos and t-shirts for away days, team days and events, the core corporate-casual layer, embroidered to brand so staff look smart and consistent out of the office.",
   "Branded polos and t-shirts for away days, team days and events, the everyday corporate-casual layer, embroidered to brand so a team looks smart and consistent away from the office.",
   "The core corporate-casual layer: branded polos and t-shirts for away days, team days and events, embroidered to brand so staff look smart and consistent whenever they step out of the suit."]),
 ("Branded Corporate Shirts",[
   "Collared shirts and blouses for client-facing days, reception, conferences and exhibitions, finished with a subtle embroidered logo so the brand reads clean and professional.",
   "Collared shirts and blouses for client-facing days, reception, conferences and exhibitions, carrying a subtle embroidered logo so the brand stays clean and professional.",
   "Smart collared shirts and blouses for reception, client days, conferences and exhibitions, finished with a discreet embroidered logo so the brand reads clean and professional."]),
 ("Softshell Jackets",[
   "Smart branded softshell jackets for site visits, outdoor events and away days, a premium outer layer that carries the logo cleanly and keeps a team looking on-brand.",
   "Smart branded softshell jackets for site visits, outdoor events and away days, a premium outer that carries the logo cleanly and keeps the team on-brand away from the office.",
   "Premium branded softshell jackets for site visits, outdoor events and away days, a smart outer layer that carries the logo cleanly and keeps a team looking on-brand."]),
 ("Fleeces and Mid-Layers",[
   "Branded fleeces and mid-layers for offsites, site visits and cold venues, a comfortable, on-brand layer for teams working or representing the firm away from the office.",
   "Branded fleeces and mid-layers for offsites, site visits and cold venues, a comfortable on-brand layer for teams out representing the firm away from the office.",
   "Comfortable branded fleeces and mid-layers for offsites, site visits and cold venues, an easy on-brand layer for teams working or representing the firm out of the office."]),
 ("Quarter-Zips and Sweatshirts",[
   "Corporate-casual quarter-zips and sweatshirts for team days, dress-down and staff merch, embroidered to brand for a smart, modern look the team will actually wear.",
   "Corporate-casual quarter-zips and sweatshirts for team days, dress-down and staff merch, embroidered to brand for a smart, modern look people actually want to wear.",
   "Smart quarter-zips and sweatshirts for team days, dress-down and staff merch, embroidered to brand for a modern, corporate-casual look the team will actually wear."]),
 ("Gilets and Bodywarmers",[
   "Smart branded gilets and bodywarmers for outdoor events, exhibitions and site visits, adding warmth without bulk while keeping the logo and brand front and centre.",
   "Smart branded gilets and bodywarmers for outdoor events, exhibitions and site visits, adding warmth without bulk while keeping the logo and brand on show.",
   "Branded gilets and bodywarmers for outdoor events, exhibitions and site visits, a smart layer that adds warmth without bulk and keeps the logo and brand front and centre."]),
 ("Caps and Accessories",[
   "Branded caps and accessories for sponsored events, exhibitions and staff merch, finishing the set to brand and giving teams a tidy, recognisable look at any event.",
   "Branded caps and accessories for sponsored events, exhibitions and staff merch, completing the set to brand and giving a team a tidy, recognisable look at any event.",
   "Branded caps and accessories for sponsored events, exhibitions and staff merch, finishing the set to brand so a team has a tidy, recognisable look wherever it appears."]),
 ("Logo and Brand-Mark Embroidery",[
   "In-house embroidery of your logo, brand colours and staff names to your guidelines, held on file so every order, new starter and event matches the brand exactly.",
   "In-house embroidery of your logo, brand colours and staff names to your guidelines, kept on file so every order, new starter and event matches the brand exactly.",
   "Your logo, brand colours and staff names embroidered in-house to your guidelines and held on file, so every order, new starter and event matches the brand exactly."]),
]
GRID_ORDER=[(0,1,2,3,4,5,6,7),(1,0,2,3,4,5,6,7),(0,1,3,2,4,5,6,7),(0,2,1,3,4,5,6,7)]
def build_grid(town):
    order = GRID_ORDER[pick(town,'gord',len(GRID_ORDER))]
    cards=[]
    for i in order:
        name,variants = CARD_DETAILS[i]
        cards.append(_card(name, variants[pick(town,f'g{i}',len(variants))]))
    return '<div class="cp-product-grid">'+''.join(cards)+'</div>'

TRUST_POOL=[
 "Branded polos, shirts, softshells and fleeces for banks, law firms, accountancies and tech companies - on-brand and account-managed",
 "Branded polos, shirts, softshells and fleeces for professional firms - on-brand, embroidered to your guidelines, account-managed",
 "On-brand corporate kit for banks, law firms, accountancies and tech companies - embroidered to your guidelines, on a managed account",
 "Branded corporate kit - polos, shirts, softshells and fleeces - for professional firms, on-brand and account-managed from one supplier",
]
S2INTRO_POOL=[
 "Whether you are a {t} bank, law firm, accountancy or technology company, the range is built to keep you on-brand from one place: branded polos and shirts for events and client days, and softshells, fleeces and quarter-zips for away days, site visits and exhibitions.",
 "A {t} bank, law firm, accountancy or technology company is kept on-brand from one place: branded polos and shirts for events and client days, and softshells, fleeces and quarter-zips for away days, site visits and exhibitions.",
 "For a {t} bank, law firm, accountancy or technology company, the range keeps you on-brand from one place: branded polos and shirts for events and client days, and softshells, fleeces and quarter-zips for away days, site visits and exhibitions.",
 "Whether it is a {t} bank, law firm or technology company, the range keeps the brand consistent from one place: branded polos and shirts for events and client days, plus softshells, fleeces and quarter-zips for away days, site visits and exhibitions.",
]
EMB_P1_POOL=[
 "In corporate and professional services, branded kit represents the firm in public. When a team turns out at a {t} conference, an exhibition, an away day or a sponsored event, the polos, shirts and softshells they wear stand for the brand just as much as the logo on the door, so the kit has to be exactly on-brand: the right logo, the right colours and embroidered to the firm's guidelines, reading as the brand rather than as generic workwear.",
 "In corporate and professional services, branded kit stands in for the firm in public. When a team appears at a {t} conference, an exhibition, an away day or a sponsored event, the polos, shirts and softshells they wear represent the brand as much as the logo on the door, so the kit has to be exactly on-brand: the right logo, the right colours and embroidered to guidelines, reading as the brand rather than generic workwear.",
 "Corporate kit represents the firm in public. When a team turns out at a {t} conference, an exhibition, an away day or a sponsored event, the polos, shirts and softshells they wear stand for the brand just as much as the logo on the door, so the kit has to be exactly on-brand: the right logo, the right colours and embroidered to the firm's guidelines, not generic workwear.",
 "In professional services, branded kit is the firm made visible. When a team appears at a {t} conference, an exhibition, an away day or a sponsored event, the polos, shirts and softshells they wear represent the brand as much as the logo on the door, so the kit has to be exactly on-brand: the right logo, the right colours, embroidered to guidelines, reading as the brand and not as generic workwear.",
]
EMB_P2_POOL=[
 "We brand in-house, which means your logo, brand colours and staff names are embroidered onto polos, shirts, softshells and fleeces and finished cleanly to suit a professional brand. Send your brand pack once, we hold it on file, and every reorder, new starter and event matches the last, so whether it is one {t} team or a firm with offices across the country, the brand looks consistent wherever it appears.",
 "Branding is done in-house onto polos, shirts, softshells and fleeces - your logo, brand colours and staff names embroidered and finished cleanly to suit a professional brand. Send your brand pack once and we hold it on file, so every reorder, new starter and event matches, and whether it is one {t} team or a firm with offices nationwide, the brand looks consistent wherever it appears.",
 "Your logo, brand colours and staff names are embroidered in-house onto polos, shirts, softshells and fleeces, finished cleanly to suit a professional brand. Held on file from your brand pack, they reproduce on every reorder, new starter and event, so one {t} team or a firm with offices across the country looks consistent wherever the brand appears.",
 "We badge in-house, embroidering your logo, brand colours and staff names onto polos, shirts, softshells and fleeces and finishing them cleanly for a professional brand. We hold your brand pack on file, so every reorder, new starter and event matches, and whether it is one {t} team or a national firm, the brand stays consistent wherever it appears.",
]
EMB_P3_POOL=[
 "And because corporate kit is occasional rather than daily, that held brand pack is the point. We keep your logo, colours and sizes on file, so ordering welcome packs for new starters, kitting a team for an away day or a conference stand, or restocking for a sponsored event reproduces exactly the same on-brand look every time, without anyone having to re-supply artwork or check a colour match.",
 "And because corporate kit is occasional rather than daily, the held brand pack is the value. We keep your logo, colours and sizes on file, so welcome packs for new starters, an away-day order, a conference stand or a sponsored-event restock reproduce exactly the same on-brand look every time, with no artwork to re-supply and no colour to second-guess.",
 "Because corporate kit is occasional rather than a daily uniform, that held brand pack matters. We keep your logo, colours and sizes on file, so ordering welcome packs, kitting a team for an away day or conference, or restocking for a sponsored event reproduces the same on-brand look each time, without re-supplying artwork or checking a colour match.",
 "And because corporate kit is bought for occasions rather than worn daily, the held brand pack is the whole point. We keep your logo, colours and sizes on file, so welcome packs, an away-day order, a conference stand or a sponsored-event restock come back exactly the same on-brand look every time, with nothing to re-supply.",
]
CON_HEAD="On-Brand, Account-Managed Corporate Kit"
CON_P1_POOL=[
 "Corporate and professional services workwear has to earn its place two ways, and the right service covers both. The first is the brand. A branded polo, shirt or softshell represents the firm in public, so it has to be exactly on-brand: the right logo, the right colours and embroidered to your guidelines, so it reads as the brand the firm has built, not as generic workwear, whether it appears at a {t} conference, an away day or a sponsored event.",
 "Corporate and professional services workwear earns its place two ways, and the right service does both. The first is the brand. A branded polo, shirt or softshell represents the firm in public, so it has to be exactly on-brand: the right logo, the right colours and embroidered to your guidelines, so it reads as the brand the firm has built, not generic workwear, whether it appears at a {t} conference, an away day or a sponsored event.",
 "This workwear has to work two ways, and the right service covers both. The first is the brand. A branded polo, shirt or softshell represents the firm in public, so it has to be exactly on-brand: the right logo, the right colours and embroidered to your guidelines, reading as the brand the firm has built rather than generic workwear, whether it appears at a {t} conference, an away day or a sponsored event.",
 "Corporate workwear has to earn its place two ways, and the right service handles both. The first is the brand: a branded polo, shirt or softshell represents the firm in public, so it has to be exactly on-brand, with the right logo, the right colours and embroidered to your guidelines, so it reads as the brand the firm has built and not as generic workwear at a {t} conference, away day or sponsored event.",
]
CON_P2_POOL=[
 "The second is the service. Because corporate kit is occasional rather than a daily uniform, the value is in how it is managed: a single point of contact, a held kit list and brand pack, agreed pricing and managed reorders, so procurement can place one order and have every office, team and event come back the same. Roll out welcome packs for new starters, kit a team for a conference or restock for an exhibition, all from the same held pack.",
 "The second is the service. As corporate kit is occasional rather than a daily uniform, the value is in how it is managed: a single point of contact, a held kit list and brand pack, agreed pricing and managed reorders, so procurement places one order and every office, team and event comes back the same. Roll out welcome packs, kit a team for a conference or restock for an exhibition, all from the same held pack.",
 "The second is the service. Because corporate kit is bought for occasions rather than worn daily, the value is the management: a single point of contact, a held kit list and brand pack, agreed pricing and managed reorders, so procurement places one order and every office, team and event matches. Welcome packs, a conference order or an exhibition restock all come from the same held pack.",
 "The second is the service. Since corporate kit is occasional rather than a daily uniform, the value lies in how it is run: a single point of contact, a held kit list and brand pack, agreed pricing and managed reorders, so procurement can place one order and have every office, team and event come back the same, all from one held pack.",
]
CON_P3_POOL=[
 'The result is one supplier keeping the brand consistent wherever it appears in public, across every {t} office and occasion, all embroidered in-house to your guidelines. We hold your brand pack and sizes on file and supply polos, shirts, softshells and fleeces together, so the firm always looks like itself. Browse the range at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
 'The result is one supplier keeping the brand consistent wherever it appears, across every {t} office and occasion, all embroidered in-house to your guidelines. We hold your brand pack and sizes on file and supply polos, shirts, softshells and fleeces as one, so the firm always looks like itself. Browse the range at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
 'The result is one supplier holding the brand consistent wherever it appears in public, across every {t} office and occasion, all embroidered in-house to your guidelines. We keep your brand pack and sizes on file and supply polos, shirts, softshells and fleeces together, so the firm always looks like itself. Browse the range at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
 'The result is a single supplier keeping the brand consistent wherever it appears, across every {t} office and occasion, all embroidered in-house to your guidelines. We hold your brand pack and sizes on file and supply polos, shirts, softshells and fleeces together, so the firm always looks like itself. Browse the range at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
]
ACC_HEAD="A Managed Account for Consistent, On-Brand Corporate Kit"
ACC_P1_POOL=[
 "Corporate workwear is bought differently from a daily uniform, so we run it as a managed account. You get a single point of contact, a held kit list and brand pack, agreed pricing and managed reorders, so procurement, office or brand managers place one order and have every {t} office, team and event come back exactly on-brand. Send your brand pack, your logo and your sizes once and we build the branded kit list and hold it on file.",
 "Corporate workwear is bought differently from a daily uniform, so it is run as a managed account. You get a single point of contact, a held kit list and brand pack, agreed pricing and managed reorders, so procurement, office or brand managers place one order and every {t} office, team and event comes back exactly on-brand. Send your brand pack, logo and sizes once and we build the branded kit list and hold it on file.",
 "Because corporate workwear is bought differently from a daily uniform, we run it as a managed account: a single point of contact, a held kit list and brand pack, agreed pricing and managed reorders, so procurement, office or brand managers place one order and every {t} office, team and event comes back exactly on-brand. Send your brand pack, logo and sizes once and we build and hold the branded kit list.",
 "Corporate workwear is bought differently from a uniform, so we run it as a managed account. You get a single point of contact, a held kit list and brand pack, agreed pricing and managed reorders, so procurement, office or brand managers place one order and have every {t} office, team and event come back on-brand. Send your brand pack, logo and sizes once and we build the kit list and hold it on file.",
]
ACC_P2_POOL=[
 "From there, the occasions look after themselves. Onboarding welcome packs for new starters, an away-day order for a department, a conference or exhibition stand, or a restock for a sponsored event are all reproduced from the same held pack, in the same colours and to the same guidelines, so nobody has to re-supply artwork or check a brand match each time.",
 "From there, the occasions look after themselves. Welcome packs for new starters, an away-day order for a department, a conference or exhibition stand, or a sponsored-event restock are all reproduced from the same held pack, in the same colours and to the same guidelines, so nobody re-supplies artwork or checks a brand match each time.",
 "After that, the occasions look after themselves. Onboarding welcome packs, an away-day order for a department, a conference or exhibition stand, or a restock for a sponsored event all come from the same held pack, in the same colours and to the same guidelines, with no artwork to re-supply and no brand match to check.",
 "From there, the occasions take care of themselves. Welcome packs for new starters, a departmental away-day order, a conference or exhibition stand, or a sponsored-event restock are reproduced from the same held pack, in the same colours and to the same guidelines, so nobody re-supplies artwork or second-guesses a brand match.",
]
ACC_P3_POOL=[
 "And because everything is branded in-house and held on file, the brand stays consistent wherever it appears. A {t} firm with several offices, or several teams, gets the same on-brand kit across all of them, so a head office and a regional team look like the same firm at the same event, which is the whole point of corporate kit.",
 "And because everything is branded in-house and held on file, the brand stays consistent wherever it appears. A {t} firm with several offices or teams gets the same on-brand kit across all of them, so a head office and a regional team look like the same firm at the same event, which is the whole point of corporate kit.",
 "Because everything is branded in-house and held on file, the brand stays consistent wherever it appears. A {t} firm with several offices, or several teams, gets the same on-brand kit across all of them, so the head office and a regional team look like one firm at the same event, which is the point of corporate kit.",
 "And since everything is branded in-house and held on file, the brand stays consistent wherever it appears. A {t} firm with several offices or teams gets the same on-brand kit across all of them, so a head office and a regional team read as the same firm at the same event, which is exactly the point of corporate kit.",
]
ACC_P4_POOL=[
 'Set up a managed account at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>, or browse the range and order online at <a href="https://www.ineedworkwear.com">iNeedWorkwear</a>.',
 'Set up a managed account at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>. You can also browse the range and order online at <a href="https://www.ineedworkwear.com">iNeedWorkwear</a>.',
 'Open a managed account at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>, or browse the range and order online at <a href="https://www.ineedworkwear.com">iNeedWorkwear</a>.',
 'Set up a managed account at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>, or simply browse the range and order online at <a href="https://www.ineedworkwear.com">iNeedWorkwear</a>.',
]
WHY_P1_POOL=[
 "A bank, law firm, accountancy or tech company in {t} whose people turn out in clean, on-brand polos, shirts and softshells at an event looks every bit as professional as its offices and its reputation, and iNeedWorkwear keeps that look consistent from a single managed account, embroidered in-house to your guidelines, so the brand is represented properly wherever your teams appear in public.",
 "A {t} bank, law firm, accountancy or tech company whose people turn out in clean, on-brand polos, shirts and softshells at an event looks as professional as its offices and reputation, and iNeedWorkwear keeps that look consistent from a single managed account, embroidered in-house to your guidelines, so the brand is represented properly wherever your teams appear.",
 "When a {t} bank, law firm or tech company turns its people out in clean, on-brand polos, shirts and softshells at an event, it looks every bit as professional as its offices and its reputation, and we keep that look consistent from one managed account, embroidered in-house to your guidelines, so the brand is represented properly wherever your teams appear in public.",
 "A bank, law firm, accountancy or tech company in {t} whose people wear clean, on-brand polos, shirts and softshells at an event reads as professional as its offices and reputation, and iNeedWorkwear keeps that look consistent from one managed account, embroidered in-house to your guidelines, so the brand shows up properly wherever your teams appear.",
 "A {t} bank, law firm, accountancy or tech company whose teams turn out in clean, on-brand polos, shirts and softshells looks as professional in the field as it does in its offices, and we keep that look consistent from a single managed account, embroidered in-house to your guidelines, so the brand is represented properly at every event.",
 "In {t}, a bank, law firm, accountancy or tech company whose people wear clean, on-brand polos, shirts and softshells at an event looks as professional as its reputation, and iNeedWorkwear keeps that look consistent from a single managed account, embroidered in-house to your guidelines, wherever the teams appear in public.",
]
WHY_P2_POOL=[
 "It is built around how corporate kit is actually bought: occasionally, for specific occasions, and always to brand. A held brand pack, managed reorders and a single point of contact mean procurement can kit a department for an away day, order welcome packs or restock for a conference without re-supplying artwork or risking a colour drift, so a growing firm never ends up with a patchwork of off-brand workwear.",
 "It is built around how corporate kit is really bought: occasionally, for specific occasions, and always to brand. A held brand pack, managed reorders and a single point of contact mean procurement can kit a department for an away day, order welcome packs or restock for a conference without re-supplying artwork or risking colour drift, so a growing firm avoids a patchwork of off-brand workwear.",
 "It works the way corporate kit is actually bought: occasionally, for specific occasions, and always to brand. A held brand pack, managed reorders and a single point of contact let procurement kit a department for an away day, order welcome packs or restock for a conference without re-supplying artwork or risking a colour drift, so a growing firm never collects a patchwork of off-brand workwear.",
 "It suits how corporate kit is actually bought: occasionally, for set occasions, and always to brand. A held brand pack, managed reorders and a single point of contact mean procurement can kit a department for an away day, order welcome packs or restock for a conference with no artwork to re-supply and no colour drift, so a growing firm never ends up with mismatched off-brand workwear.",
 "It is designed around how corporate kit gets bought: occasionally, for specific occasions, and always on-brand. A held brand pack, managed reorders and a single point of contact mean procurement can kit a department for an away day, order welcome packs or restock for a conference without re-supplying artwork or risking colour drift, so a growing firm avoids a patchwork of off-brand kit.",
 "It maps to how corporate kit is actually bought: now and then, for specific occasions, and always to brand. A held brand pack, managed reorders and a single point of contact mean procurement can kit a department for an away day, order welcome packs or restock for a conference without re-supplying artwork or risking a colour drift, so a growing firm never ends up off-brand.",
]
WHY_P3_POOL=[
 "The range is deliberately narrow and focused on what the work needs: polos and shirts for events and client days, and softshells, fleeces, quarter-zips and gilets for away days, site visits and exhibitions. It is a tight, premium range, so choosing, ordering and reordering stay quick and simple for a busy office, brand or procurement manager.",
 "The range is deliberately narrow and focused on what is needed: polos and shirts for events and client days, and softshells, fleeces, quarter-zips and gilets for away days, site visits and exhibitions. It is a tight, premium range, so choosing, ordering and reordering stay quick for a busy office, brand or procurement manager.",
 "Everything in the range is deliberately narrow and focused on what the work needs: polos and shirts for events and client days, and softshells, fleeces, quarter-zips and gilets for away days, site visits and exhibitions. The range is tight and premium, so ordering and reordering stay quick for a busy office or procurement manager.",
 "The range is kept deliberately narrow and focused: polos and shirts for events and client days, and softshells, fleeces, quarter-zips and gilets for away days, site visits and exhibitions. It is a tight, premium range, so choosing and reordering stay quick and simple for a busy office, brand or procurement manager.",
 "It is a deliberately narrow, premium range mapped to what the work needs: polos and shirts for events and client days, and softshells, fleeces, quarter-zips and gilets for away days, site visits and exhibitions, which keeps choosing and reordering quick for a busy office or procurement manager.",
 "The range stays deliberately narrow and focused on the need: polos and shirts for events and client days, and softshells, fleeces, quarter-zips and gilets for away days, site visits and exhibitions, so a busy office, brand or procurement manager can choose and reorder in minutes.",
]
WHY_P4_POOL=[
 "And everything is branded in-house, with your logo and brand colours embroidered under our control and held on file, ready for the next order, the next new starter or the next event, so every piece matches the brand exactly and the firm always looks like itself, from the head office to a regional team at the same event.",
 "And everything is branded in-house, your logo and brand colours embroidered under our control and held on file, ready for the next order, new starter or event, so every piece matches the brand exactly and the firm always looks like itself, from head office to a regional team at the same event.",
 "And it is all branded in-house, with your logo and brand colours embroidered under our control and kept on file, ready for the next order, the next new starter or the next event, so every piece matches the brand and the firm always looks like itself, from the head office to a regional team.",
 "And everything is branded in-house, your logo and brand colours embroidered under our control and held on file for the next order, new starter or event, so every piece matches the brand exactly and the firm always looks like itself, head office and regional team alike.",
 "And the whole range is branded in-house, with your logo and brand colours embroidered under our control and held on file, ready for the next order, new starter or event, so every piece matches the brand exactly and the firm consistently looks like itself wherever it appears.",
 "And it is all branded in-house, your logo and brand colours embroidered under our control and on file, ready for the next order, the next new starter or the next event, so every piece lines up with the brand and the firm always looks like itself, from head office to a regional team.",
]
ORD_P1_POOL=[
 "iNeedWorkwear supplies branded polos, shirts, softshells and fleeces to banks, law firms, accountancies, consultancies, insurers and technology companies across {region}, all embroidered in-house to brand guidelines.",
 "We supply branded polos, shirts, softshells and fleeces to banks, law firms, accountancies, consultancies, insurers and technology companies across {region}, all embroidered in-house to brand guidelines.",
 "Across {region}, iNeedWorkwear supplies branded polos, shirts, softshells and fleeces to banks, law firms, accountancies, consultancies, insurers and technology companies, all embroidered in-house to brand guidelines.",
 "From a single team to a national firm across {region}, iNeedWorkwear supplies branded polos, shirts, softshells and fleeces to professional firms, all embroidered in-house to brand guidelines.",
]
ORD_P2_POOL=[
 "The simplest route for a firm is a managed account: send your brand pack, your logo and your sizes and we build a branded kit list and hold it on file, so each order, new starter and event is reproduced on-brand, in the same colours and to the same guidelines, with a single point of contact for every office and team.",
 "The simplest route is a managed account: send your brand pack, logo and sizes and we build a branded kit list and hold it on file, so each order, new starter and event is reproduced on-brand, in the same colours and to the same guidelines, with a single point of contact for every office and team.",
 "For most firms the simplest route is a managed account: send your brand pack, logo and sizes and we build a branded kit list and hold it on file, so each order, new starter and event comes back on-brand, in the same colours and to the same guidelines, with one point of contact for every office and team.",
 "A managed account is the simplest route for a firm: send your brand pack, your logo and your sizes and we build a branded kit list and hold it on file, so each order, new starter and event is reproduced on-brand and to the same guidelines, with a single point of contact across offices and teams.",
]
ORD_P3_POOL=[
 "You can also browse the range and order online, picking your polos, shirts, softshells and fleeces, adding your sizes and sending your brand pack once. Your kit is dispatched on standard lead times with embroidery added in-house, and your brand pack is held on file so the next order matches.",
 "You can also browse the range and order online, picking your polos, shirts, softshells and fleeces, adding sizes and sending your brand pack once. Your kit ships on standard lead times with embroidery added in-house, and your brand pack is held on file so the next order matches.",
 "Or browse the range and order online, picking your polos, shirts, softshells and fleeces, adding your sizes and sending your brand pack once. Kit is dispatched on standard lead times with embroidery in-house, and your brand pack is held on file so the next order matches.",
 "You can also browse and order online, choosing your polos, shirts, softshells and fleeces, adding your sizes and sending your brand pack once, dispatched on standard lead times with embroidery in-house and your brand pack held on file so the next order matches.",
]
SELF_POOL=[
 'Setting up a brand refresh or kitting a team for an event? Browse the full range, add your sizes and order direct on self-service checkout at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
 'Refreshing the brand or kitting a team for an event? Browse the range, add sizes and order direct on self-service checkout at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
 'Planning a brand refresh or an away-day order? Browse the full range, add your sizes and order direct on self-service checkout at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
 'Need branded kit for a conference or away day? Browse the range, add sizes and order direct on self-service checkout at <a href="https://www.ineedworkwear.com">iNeedWorkwear.com</a>.',
]
SORTED_POOL=[
 '<h3>Corporate and Professional Services Workwear, Sorted</h3><p>From branded polos and shirts to softshells, fleeces and quarter-zips, get on-brand workwear built for banks, law firms, accountancies and tech companies - embroidered in-house to your guidelines, on a managed account or ordered direct online.</p><p><a href="https://www.ineedworkwear.com">Browse corporate and professional services workwear at iNeedWorkwear</a></p>',
 '<h3>Corporate and Professional Services Workwear, Sorted</h3><p>Branded polos and shirts, plus softshells, fleeces and quarter-zips - on-brand workwear for banks, law firms, accountancies and tech companies, embroidered in-house to your guidelines, on a managed account or ordered direct online.</p><p><a href="https://www.ineedworkwear.com">Browse corporate and professional services workwear at iNeedWorkwear</a></p>',
 '<h3>Corporate and Professional Services Workwear, Sorted</h3><p>From branded polos and shirts to softshells, fleeces and quarter-zips, kit a firm on-brand for away days, conferences and events, embroidered in-house to your guidelines and ordered on a managed account or direct online.</p><p><a href="https://www.ineedworkwear.com">Browse corporate and professional services workwear at iNeedWorkwear</a></p>',
 '<h3>Corporate and Professional Services Workwear, Sorted</h3><p>Polos, shirts, softshells, fleeces and quarter-zips, the on-brand kit for banks, law firms, accountancies and tech companies, embroidered in-house to your guidelines and ready on a managed account or direct online.</p><p><a href="https://www.ineedworkwear.com">Browse corporate and professional services workwear at iNeedWorkwear</a></p>',
]
OWNER_POOL=[
 "And because most of these firms wear no uniform day to day, corporate workwear here is a brand exercise rather than a daily one. It is bought by procurement, office and brand managers for specific occasions, and when it does appear it has to match the firm's brand exactly, because a branded polo or softshell represents the firm in public just as much as the letterhead or the website does.",
 "And because most of these firms wear no daily uniform, corporate workwear here is a brand exercise rather than a daily one. It is bought by procurement, office and brand managers for specific occasions, and when it appears it has to match the firm's brand exactly, because a branded polo or softshell represents the firm in public as much as the letterhead or the website does.",
 "And since most of these firms wear no uniform day to day, corporate workwear here is a brand exercise rather than a daily one. Procurement, office and brand managers buy it for specific occasions, and when it appears it has to match the firm's brand exactly, because a branded polo or softshell stands for the firm in public just as much as the letterhead or the website.",
 "And because these firms mostly wear no uniform day to day, corporate workwear here is a brand exercise, not a daily one. It is bought by procurement, office and brand managers for set occasions, and when it appears it has to match the brand exactly, because a branded polo or softshell represents the firm in public as much as the letterhead or website does.",
 "And as most of these firms have no daily uniform, corporate workwear here is a brand exercise rather than a daily one. Procurement, office and brand managers buy it for specific occasions, and when it does appear it has to be exactly on-brand, because a branded polo or softshell represents the firm in public just as much as the letterhead or the website.",
 "And because most of these firms wear suits, not uniforms, day to day, corporate workwear here is a brand exercise rather than a daily one. It is bought by procurement, office and brand managers for specific occasions, and when it appears it has to match the brand exactly, since a branded polo or softshell represents the firm in public as much as the letterhead does.",
]
PRESENT_POOL=[
 "And the kit is for the moments staff step out of the suit, which is what makes corporate workwear its own thing. Away days and team days, conferences and exhibitions, sponsored and fundraising events, site and client visits, and welcome packs for new starters: a {t} firm needs branded polos, shirts and softshells that are exactly on-brand, embroidered to guidelines and held on file so every occasion matches.",
 "And the kit is for the moments staff step out of the suit, which is what sets corporate workwear apart. Away days and team days, conferences and exhibitions, sponsored and fundraising events, site and client visits, and welcome packs for new starters: a {t} firm needs branded polos, shirts and softshells that are exactly on-brand, embroidered to guidelines and held on file so every occasion matches.",
 "And the kit covers the moments staff step out of the suit, which is the heart of corporate workwear. Away days and team days, conferences and exhibitions, sponsored and fundraising events, site and client visits, and new-starter welcome packs: a {t} firm needs branded polos, shirts and softshells that are exactly on-brand, embroidered to guidelines and held on file so every occasion matches.",
 "And the kit is built for the moments staff step out of the suit, which is what makes corporate workwear distinct. Away days and team days, conferences and exhibitions, sponsored and fundraising events, site and client visits, and welcome packs: a {t} firm needs branded polos, shirts and softshells that are exactly on-brand, embroidered to guidelines and held on file so every occasion matches.",
 "And the kit serves the moments staff step out of the suit, which is what makes this workwear its own thing. Away days and team days, conferences and exhibitions, sponsored and fundraising events, site and client visits, and welcome packs for new starters: a {t} firm needs branded polos, shirts and softshells, exactly on-brand, embroidered to guidelines and held on file so every occasion matches.",
 "And the kit is for the occasions when staff step out of the suit, which is what distinguishes corporate workwear. Away days and team days, conferences and exhibitions, sponsored and fundraising events, site and client visits, and new-starter welcome packs: a {t} firm needs branded polos, shirts and softshells, exactly on-brand and embroidered to guidelines, held on file so every occasion matches.",
]
NARROW_POOL=[
 "Because corporate kit is occasional and always on-brand, the range is deliberately narrow and the value is consistency and service. Branded polos, shirts, softshells and fleeces, embroidered in-house to your guidelines, are the whole kit, and a held brand pack, managed reorders and a single point of contact mean each {t} office, team and event matches the brand the firm has built.",
 "Because corporate kit is occasional and always on-brand, the range is deliberately narrow and the value is consistency and service. Branded polos, shirts, softshells and fleeces, embroidered in-house to your guidelines, are the whole kit, and a held brand pack, managed reorders and a single point of contact keep each {t} office, team and event on-brand.",
 "Since corporate kit is occasional and always on-brand, the range is deliberately narrow and the value is consistency and service. Branded polos, shirts, softshells and fleeces, embroidered in-house to your guidelines, are the whole kit, and a held brand pack, managed reorders and a single point of contact mean each {t} office, team and event matches the brand.",
 "Because corporate kit is bought occasionally and must always be on-brand, the range is deliberately narrow and the value is consistency and service. Branded polos, shirts, softshells and fleeces, embroidered in-house to your guidelines, are the whole kit, and a held brand pack, managed reorders and one point of contact keep each {t} office, team and event matching the brand.",
 "As corporate kit is occasional and always on-brand, the range is deliberately narrow and the value is consistency and service. Branded polos, shirts, softshells and fleeces, embroidered in-house to your guidelines, are the whole kit, and a held brand pack, managed reorders and a single point of contact mean each {t} office, team and event matches the brand the firm has built.",
 "Because corporate kit is occasional and has to be on-brand every time, the range is deliberately narrow and the value is consistency and service. Branded polos, shirts, softshells and fleeces, embroidered in-house to your guidelines, are the whole kit, and a held brand pack, managed reorders and a single point of contact keep each {t} office, team and event on-brand.",
]
KIT_POOL=[
 "Branded polos, shirts, softshells and fleeces, embroidered to your guidelines, are the whole kit {loc}.",
 "The whole kit is branded polos, shirts, softshells and fleeces, embroidered to your guidelines {loc}.",
 "Branded polos, shirts, softshells and fleeces, embroidered to brand, do the job {loc}.",
 "It comes down to branded polos, shirts, softshells and fleeces, embroidered to your guidelines {loc}.",
 "Branded polos, shirts, softshells and fleeces, all embroidered to your guidelines, are the kit {loc}.",
 "On-brand polos, shirts, softshells and fleeces make up the whole kit {loc}.",
]
S2TAIL_POOL=[
 ", polos and shirts lead, with softshells and fleeces for events out of the office.",
 ", the core is polos and shirts, with softshells and fleeces for events away from the office.",
 ", expect polos and shirts, then softshells and fleeces for away days and site visits.",
 ", polos and shirts cover client days, with softshells and fleeces for events outdoors.",
 ", polos and shirts anchor it, with softshells and fleeces completing the kit for offsites.",
 ", it is polos and shirts, plus softshells and fleeces for away days and exhibitions.",
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
     (f"Do you supply branded workwear to corporate and professional services firms in {t}?", P('fq1',[
      f"Yes. Banks, law firms, accountancies, consultancies, insurers and technology companies across {region} get branded polos, shirts, softshells and fleeces from us, embroidered in-house to brand guidelines. It is a managed account with a single point of contact, your brand pack held on file, and reorders kept consistent across every office, team and event.",
      f"Yes. Branded polos, shirts, softshells and fleeces go to banks, law firms, accountancies, consultancies, insurers and technology companies across {region}, embroidered in-house to brand guidelines. It is a managed account with a single point of contact, your brand pack on file, and reorders kept consistent across every office, team and event.",
      f"Yes. From a single team to a national firm across {region}, we supply branded polos, shirts, softshells and fleeces, embroidered in-house to brand guidelines, on a managed account with a single point of contact and your brand pack held on file.",
      f"Yes. Banks, law firms, accountancies and technology companies across {region} get branded polos, shirts, softshells and fleeces from us, embroidered in-house to brand guidelines, on a managed account with your brand pack held on file.",
      f"Yes. Across {region} we kit banks, law firms, accountancies, consultancies and technology companies in branded polos, shirts, softshells and fleeces, embroidered in-house to brand guidelines, on a managed account with one point of contact.",
      f"Yes. Professional firms across {region}, from a single team to a national practice, get branded polos, shirts, softshells and fleeces from us, embroidered in-house to brand guidelines, on a managed account with your brand pack held on file."])),
     ("What do professional firms usually use branded workwear for?", P('fq2',[
      "Corporate workwear is mostly for the moments staff step out of the suit: away days and team days, conferences and exhibitions, sponsored and fundraising events, site and client visits, and welcome packs for new starters. The range is deliberately narrow - branded polos, shirts, softshells and fleeces - and the value is that every piece is exactly on-brand.",
      "Mostly for the moments staff step out of the suit: away days and team days, conferences and exhibitions, sponsored and fundraising events, site and client visits, and new-starter welcome packs. The range is deliberately narrow - branded polos, shirts, softshells and fleeces - and the value is that every piece is exactly on-brand.",
      "It is for the moments staff step out of the suit: away days, conferences and exhibitions, sponsored and fundraising events, site and client visits, and welcome packs for new starters. The range stays narrow - branded polos, shirts, softshells and fleeces - and the point is that every piece is exactly on-brand.",
      "Corporate kit is for occasions rather than daily wear: away days and team days, conferences and exhibitions, sponsored and fundraising events, site and client visits, and welcome packs. The range is deliberately narrow - polos, shirts, softshells and fleeces - and every piece is exactly on-brand.",
      "It covers the moments staff step out of the suit: away days, conferences and exhibitions, sponsored and fundraising events, site and client visits, and welcome packs for new starters. A narrow range of branded polos, shirts, softshells and fleeces, all exactly on-brand.",
      "Mainly the moments staff step out of the suit: team and away days, conferences and exhibitions, sponsored and fundraising events, site and client visits, and new-starter welcome packs. The range is deliberately narrow - polos, shirts, softshells and fleeces - and every piece is exactly on-brand."])),
     ("Can you match our brand guidelines exactly?", P('fq3',[
      "Yes. Corporate kit represents the brand in public, so it has to be exactly on-brand: the right logo, the right colours and embroidered to your guidelines, so a polo or softshell reads as the brand rather than generic workwear. We hold your brand pack on file, so every order, new starter and event matches the last.",
      "Yes. Corporate kit represents the brand in public, so it has to be exactly on-brand: the right logo, the right colours and embroidered to your guidelines, so a polo or softshell reads as the brand, not generic workwear. Your brand pack is held on file, so every order, new starter and event matches.",
      "Yes. Because corporate kit represents the brand in public, it has to be exactly on-brand: the right logo, the right colours and embroidered to your guidelines, so a polo or softshell reads as the brand rather than generic workwear. We hold your brand pack on file, so every order matches the last.",
      "Yes. Corporate kit stands for the brand in public, so it has to be exactly on-brand: the right logo, the right colours, embroidered to your guidelines, so a polo or softshell reads as the brand and not as generic workwear. Your brand pack is held on file so every order, new starter and event matches.",
      "Yes. Since corporate kit represents the brand in public, it has to be exactly on-brand: the right logo, the right colours and embroidered to your guidelines, so a polo or softshell reads as the brand. We keep your brand pack on file, so every order, new starter and event matches the last.",
      "Yes. Corporate kit represents the brand in public, so it is made exactly on-brand: the right logo, the right colours and embroidered to your guidelines, reading as the brand rather than generic workwear. We hold your brand pack on file so every order and new starter matches."])),
     ("Do you manage the account across multiple offices and teams?", P('fq4',[
      "Yes. It is a concierge, account-managed service: a single point of contact, a held kit list and brand pack, agreed pricing and managed reorders, so procurement can place one order and every office, team and event matches. Roll out a welcome pack, an away-day order or a conference stand from the same held pack.",
      "Yes. It is a concierge, account-managed service: a single point of contact, a held kit list and brand pack, agreed pricing and managed reorders, so procurement places one order and every office, team and event matches. Roll out a welcome pack, an away-day order or a conference stand from one held pack.",
      "Yes. The account is managed end to end: a single point of contact, a held kit list and brand pack, agreed pricing and managed reorders, so procurement can place one order and every office, team and event matches, all from the same held pack.",
      "Yes. It is a managed, concierge service: one point of contact, a held kit list and brand pack, agreed pricing and managed reorders, so procurement places a single order and every office, team and event comes back the same, from the same held pack.",
      "Yes. The service is account-managed: a single point of contact, a held kit list and brand pack, agreed pricing and managed reorders, so procurement can place one order and have every office, team and event match, all reproduced from one held pack.",
      "Yes. It is a concierge account: one point of contact, a held kit list and brand pack, agreed pricing and managed reorders, so procurement places one order and every office, team and event matches, whether a welcome pack, an away day or a conference stand."])),
     ("Can you embroider our logo, brand colours and staff names?", P('fq5',[
      "Yes. We embroider your logo, brand colours and staff names in-house onto polos, shirts, softshells and fleeces, finished cleanly to suit a professional brand. Send your brand pack once, we hold it on file, and every reorder, new starter and event matches, so a bank, a law firm or a tech company always looks consistent.",
      "Yes. Your logo, brand colours and staff names are embroidered in-house onto polos, shirts, softshells and fleeces, finished cleanly for a professional brand. Send your brand pack once and we hold it on file, so every reorder, new starter and event matches, and a bank, law firm or tech company always looks consistent.",
      "Yes, all branding is done in-house onto polos, shirts, softshells and fleeces, finished cleanly to suit a professional brand. We hold your brand pack on file, so every reorder, new starter and event matches and a bank, a law firm or a tech company always looks consistent.",
      "Yes. Send your brand pack once and we embroider your logo, brand colours and staff names in-house onto polos, shirts, softshells and fleeces, holding it on file so every reorder, new starter and event matches, and a bank, law firm or tech company always looks consistent.",
      "Yes. Logo, brand colours and staff names are embroidered in-house onto polos, shirts, softshells and fleeces, finished cleanly for a professional brand and held on file, so every reorder, new starter and event matches and the firm always looks consistent.",
      "Yes, embroidery is done in-house onto polos, shirts, softshells and fleeces, finished cleanly to suit a professional brand. Send your brand pack once and we keep it on file, so reorders, new starters and events line up and a bank, law firm or tech company looks consistent."])),
     ("Do you supply softshells and fleeces for site visits and outdoor events?", P('fq6',[
      "Yes. Alongside the polos and shirts we supply smart branded softshell jackets, fleeces, quarter-zips and gilets for site visits, exhibitions, outdoor events and away days, premium layers that carry the logo cleanly and keep teams on-brand away from the office.",
      "Yes. Alongside the polos and shirts we supply smart branded softshells, fleeces, quarter-zips and gilets for site visits, exhibitions, outdoor events and away days, premium layers that carry the logo cleanly and keep teams on-brand away from the office.",
      "Yes. As well as polos and shirts we supply branded softshell jackets, fleeces, quarter-zips and gilets for site visits, exhibitions, outdoor events and away days, smart layers that carry the logo cleanly and keep teams on-brand out of the office.",
      "Yes. Beyond the polos and shirts we supply smart branded softshells, fleeces, quarter-zips and gilets for site visits, exhibitions, outdoor events and away days, premium layers that carry the logo cleanly and keep a team on-brand away from the office.",
      "Yes. With the polos and shirts we supply branded softshell jackets, fleeces, quarter-zips and gilets for site visits, exhibitions, outdoor events and away days, premium layers that carry the logo cleanly and keep teams on-brand outside the office.",
      "Yes. Alongside polos and shirts there are smart branded softshells, fleeces, quarter-zips and gilets for site visits, exhibitions, outdoor events and away days, premium layers that carry the logo cleanly and keep teams on-brand away from the office."])),
     ("How do we order corporate workwear?", P('fq7',[
      "Set up a managed account and we build a branded kit list and hold your brand pack on file, so each order, new starter and event is reproduced on-brand on standard lead times. You can also browse the range and order online, with embroidery added in-house, and your brand pack held on file so the next order matches.",
      "Set up a managed account and we build a branded kit list and hold your brand pack on file, so each order, new starter and event comes back on-brand on standard lead times. You can also browse and order online, with embroidery added in-house, and your brand pack held on file so the next order matches.",
      "Set up a managed account and we build a branded kit list and keep your brand pack on file, so each order, new starter and event is reproduced on-brand on standard lead times. Or browse the range and order online, with embroidery in-house and your brand pack held on file for the next order.",
      "The simplest route is a managed account: we build a branded kit list and hold your brand pack on file, so each order, new starter and event is reproduced on-brand on standard lead times. You can also browse and order online, with embroidery in-house and your brand pack held on file.",
      "Set up a managed account and we build and hold a branded kit list and your brand pack, so each order, new starter and event is reproduced on-brand on standard lead times. You can also browse the range and order online, embroidery added in-house, brand pack held on file.",
      "Open a managed account and we build a branded kit list and hold your brand pack on file, so each order, new starter and event comes back on-brand on standard lead times. You can also browse the range and order online, with embroidery in-house and your brand pack on file."])),
    ]

TOWNS = {
 "birmingham": {
  "region":"Birmingham and the West Midlands",
  "nearby":["Solihull","West Bromwich","Walsall"],
  "snapshot":"iNeedWorkwear supplies branded polos, shirts, softshells and fleeces to banks, law firms, accountancies, consultancies, insurers and technology companies across Birmingham, embroidered in-house to brand guidelines. As the UK's largest professional-services hub outside London, the city is full of firms that need on-brand kit for away days, conferences and events, and we run it as a managed account: a single point of contact, your brand pack held on file, and reorders kept consistent across every office, team and event.",
  "s1_head":"Kitting the largest professional-services hub outside London",
  "s1loc":[
   "Birmingham is the UK's largest professional-services hub outside London. HSBC UK has its headquarters at Centenary Square, the only clearing-bank HQ outside the capital, Deutsche Bank and Goldman Sachs run major operations in the city, and all of the Big Four, PwC, EY, Deloitte and KPMG, keep their largest regional offices in the Colmore Business District, alongside many of the UK's top-50 law firms and a fast-growing fintech and insurance scene around Colmore Row, Brindleyplace, Paradise and Snowhill.",
   "It is a city of professionals in suits, but ones who regularly step into branded kit. With tens of thousands of people across banking, legal, accountancy, consultancy and tech, Birmingham firms need on-brand polos, shirts and softshells for the conferences, away days, exhibitions and sponsored events that fill the calendar, and they buy it through procurement, office and brand managers who care that it matches the brand exactly.",
  ],
  "kit_loc":"across the firm's offices and teams",
  "s2_intro":"Whether you are a Birmingham bank, a Colmore Business District law firm, an accountancy or a technology company",
 },
 "leeds": {
  "region":"Leeds and West Yorkshire",
  "nearby":["Bradford","Pudsey","Dewsbury"],
  "snapshot":"iNeedWorkwear supplies branded polos, shirts, softshells and fleeces to banks, law firms, accountancies, consultancies, insurers and technology companies across Leeds, embroidered in-house to brand guidelines. As the UK's largest financial centre outside London, the city is full of firms that need on-brand kit for away days, conferences and events, and we run it as a managed account: a single point of contact, your brand pack held on file, and reorders kept consistent across every office, team and event.",
  "s1_head":"Kitting the largest financial centre outside London",
  "s1loc":[
   "Leeds is the UK's largest financial centre outside London, often called the Northern Square Mile. More than 30 national and international banks operate here, including first direct, with the Bank of England's only note-issuing centre outside London and the FCA in the city, alongside all of the Big Four and over 150 accountancy firms, and a legal sector of more than 1,100 firms including DLA Piper, Squire Patton Boggs, Addleshaw Goddard, Eversheds, Pinsent Masons and Walker Morris around the city centre and King Street.",
   "It is a city of professionals in suits, but ones who regularly step into branded kit. With over 40,000 people across financial and professional services, Leeds firms need on-brand polos, shirts and softshells for the conferences, away days, exhibitions and sponsored events that fill the calendar, and they buy it through procurement, office and brand managers who care that it matches the brand exactly.",
  ],
  "kit_loc":"across the firm's offices and teams",
  "s2_intro":"Whether you are a Leeds bank, a city-centre law firm, an accountancy or a technology company",
 },
}

_CSV=None
def _load_csv():
    global _CSV
    if _CSV is not None: return _CSV
    here=os.path.dirname(os.path.abspath(__file__))
    for p in (os.path.join(here,'CP_towns.csv'),'CP_towns.csv','/mnt/user-data/outputs/CP_towns.csv'):
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
                         f"(web-verified, all on CP_towns.csv). No rank/auto fallback.")
    bad = [n for n in nb if not any(r[1].lower()==n.lower() for r in _load_csv())]
    if bad:
        raise ValueError(f"{town}: nearby town(s) not on CP_towns.csv: {bad}")
    return nb[:3]

def build_title(town):
    for t in (f"{town} Corporate and Professional Services Workwear",
              f"{town} Corporate and Professional Workwear", f"{town} Corporate Workwear"):
        if len(t) <= 60: return t
    return f"{town} Corporate Workwear"

def build_meta(town):
    for m in (f"Branded polos, shirts, softshells and fleeces for {town} banks, law firms and tech companies - on-brand, account-managed, in-house embroidery.",
              f"Branded polos, shirts and softshells for {town} banks, law firms and tech companies - on-brand, account-managed, in-house embroidery.",
              f"On-brand corporate workwear for {town} banks, law firms and tech companies - polos, shirts, softshells and fleeces, account-managed.",
              f"Branded corporate workwear for {town} professional firms - polos, shirts, softshells and fleeces, on-brand and account-managed."):
        if len(m) <= 160: return m
    return f"On-brand corporate workwear for {town} professional firms - polos, shirts, softshells, account-managed."

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
        "name":f"Corporate and Professional Services Workwear Supply and Embroidery in {town}",
        "serviceType":"Corporate and professional services workwear and embroidery supply",
        "provider":{"@id":"https://www.ineedworkwear.com/#organization"},
        "areaServed":[{"@type":"City","name":town}]+[{"@type":"City","name":n} for n in nearby],
        "audience":{"@type":"BusinessAudience","name":"Banks, law firms, accountancies, consultancies and technology companies"},
        "description":f"Branded polos, shirts, softshells and fleeces supplied to corporate and professional services firms in {town}, on a managed account, embroidered in-house to brand guidelines.",
        "hasOfferCatalog":{"@type":"OfferCatalog","name":"Corporate and Professional Services Workwear",
            "itemListElement":[{"@type":"Offer","itemOffered":{"@type":"Product","name":p}} for p in CP_PRODUCTS]}}
    crumb = {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Home","item":DOMAIN},
        {"@type":"ListItem","position":2,"name":"Corporate and Professional Services Workwear","item":f"{DOMAIN}/corporate-professional-services-workwear"},
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

    emb_svg   = EMB.replace('a London corporate logo', f'a {town} corporate logo')
    # corporate monument sign (signpost slot): swap aria, the centred {town} text, and caption
    sign_svg  = SIGNPOST.replace('London corporate and professional services sign', f'{town} corporate and professional services sign')
    sign_svg  = re.sub(r'<text x="230" y="138".*?</text>', sign_town(town), sign_svg, flags=re.S)
    sign_svg  = sign_svg.replace('every London office and team', f'every {town} office and team')
    # office building (premises slot): swap aria and caption
    prem_svg  = PREMISES.replace('serving professional services firms across London', f'serving professional services firms across {town}')
    prem_svg  = prem_svg.replace('professional firms across London', f'professional firms across {town}')

    H=[build_head(town, slug, faqs, nearby), HEADER]
    H.append(f'<div class="cp-hero"><div class="cp-wrap"><div class="cp-subtitle">Branded Workwear for Corporate and Professional Services</div><h1>{town} Corporate and Professional Services Workwear</h1></div></div>')
    H.append('<div class="cp-pulse"></div>')
    H.append(f'<div class="cp-trust-strip"><p>{trust}</p></div>')
    H.append(f'<div class="cp-wrap"><div class="cp-snapshot"><div class="cp-snapshot-label">Supplier Snapshot</div><p>{snap}</p></div></div>')
    H.append(STATS)
    H.append('<div class="cp-cta-bar"><a href="https://www.ineedworkwear.com" class="cp-cta-btn">Browse Corporate and Professional Services Workwear</a></div>')
    H.append('<div class="cp-jump-links"><a href="#range">Workwear Range</a><a href="#contract">The Kit</a><a href="#accounts">The Managed Account</a><a href="#order">How to Order</a></div>')
    H.append(GARMENT)
    H.append(f'<div class="cp-section"><div class="cp-wrap"><h2>{s1head}</h2>'+''.join(f'<p>{p}</p>' for p in s1ps)+'</div></div>')
    H.append(f'<div class="cp-section" id="range"><div class="cp-wrap"><h2>Corporate and Professional Services Workwear Range</h2><p>{s2intro} <a href="https://www.ineedworkwear.com">Browse the full range at iNeedWorkwear.com</a>.</p><p class="cp-btn-center"><a href="https://www.ineedworkwear.com" class="cp-section-btn">Browse The Range</a></p>{grid}</div></div>')
    H.append(f'<div class="cp-section"><div class="cp-wrap"><h2>Branding for a Bank, a Law Firm or a Tech Company</h2>'+''.join(f'<p>{p}</p>' for p in emb)+'</div></div>')
    H.append(emb_svg)
    H.append(f'<div class="cp-wrap"><div class="cp-contract" id="contract"><h3>{CON_HEAD}</h3>'+''.join(f'<p>{p}</p>' for p in con)+'</div></div>')
    H.append(sign_svg)
    H.append(f'<div class="cp-section" id="accounts"><div class="cp-wrap"><h2>{ACC_HEAD}</h2>'+''.join(f'<p>{p}</p>' for p in acc)+'</div></div>')
    H.append(prem_svg)
    H.append(f'<div class="cp-section"><div class="cp-wrap"><h2>Why Corporate and Professional Firms Choose iNeedWorkwear</h2>'+''.join(f'<p>{p}</p>' for p in why)+'</div></div>')
    H.append(ORDER)
    H.append(f'<div class="cp-section" id="order"><div class="cp-wrap"><h2>How to Order Corporate and Professional Services Workwear</h2><p>{ordr[0]}</p><p>{ordr[1]}</p><p>{ordr[2]}</p><p class="cp-btn-center"><a href="https://www.ineedworkwear.com" class="cp-section-btn">Browse And Order Online</a></p><p>{selfp}</p>'+CONTACT+'</div></div>')
    faq_html=''.join(f'<div class="cp-faq-item"><div class="cp-faq-q">{q}</div><div class="cp-faq-a">{a}</div></div>' for q,a in faqs)
    H.append(f'<div class="cp-faq"><div class="cp-wrap"><h2>Corporate and Professional Services Workwear FAQ</h2>{faq_html}</div></div>')
    H.append(f'<div class="cp-wrap"><div class="cp-workwear">{sorted_}</div></div>')
    nb_links=''.join(f'<a href="cp-{slugify(n)}.html">Corporate and professional services workwear in {n}</a>\n' for n in nearby)
    H.append(f'<div class="cp-nearby"><div class="cp-wrap"><h3>Corporate and Professional Services Workwear in Nearby Towns</h3><div class="cp-nearby-links">{nb_links}</div></div></div>')
    H.append(FOOTER+'\n</body></html>')
    return '\n'.join(H)

def main():
    args=[a for a in sys.argv[1:]]
    outdir=os.environ.get('CP_OUTDIR') or ('/mnt/user-data/outputs' if os.path.isdir('/mnt/user-data/outputs') else 'outputs')
    os.makedirs(outdir, exist_ok=True)
    if not args:
        args=[t for t in TOWNS if t!='london']
    for town_key in args:
        tk=town_key.lower()
        if tk=='london': continue
        if tk not in TOWNS:
            print(f"SKIP {town_key}: not in TOWNS (must be web-researched first)"); continue
        town=' '.join(w.capitalize() for w in tk.split())
        slug=f"cp-{slugify(town)}"
        html=assemble(slug, town)
        path=os.path.join(outdir, f"{slug}.html")
        open(path,'w',encoding='utf-8').write(html)
        print(f"WROTE {path}  ({len(html.split())} words approx)")

if __name__=='__main__':
    main()
