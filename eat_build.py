#!/usr/bin/env python3
# EAT series builder v1.0  -  "Best Places to Eat in <Town>" doorway pages for
# Phoenix Cleaning Company.  Read SPEC.md / CLAUDE.md first.
#
# Standalone cPanel pages (NOT blog posts): no author byline, WebPage schema.
# Editorial spine = 4 researched independents (Takeaway/Casual, Cafe, Restaurant,
# Pub). Soft pivot to TR19 kitchen extraction cleaning ~70% down the page.
# The 4 venues + food_scene + faq are the uniqueness engine (researched, never
# pooled). Only the cleaning pivot scaffold is pooled (and scorer-stripped).
#
# Build:  python3 eat_build.py <slug> [<slug> ...]      (no args = all TOWNS)
# Output: /mnt/user-data/outputs/eat-<slug>.html
import os, re, sys, csv, json, zlib, datetime

# --- evidence gate (set by --require-evidence on the CLI) ------------------
REQUIRE_EVIDENCE   = False   # when True, every non-exempt town must carry per-venue source_url + verified
EVIDENCE_STALE_DAYS = 180    # verified older than this -> warn (re-verify), not a hard fail

HERE   = os.path.dirname(os.path.abspath(__file__))
DOMAIN = "https://www.phoenixcleaningcompany.com"
SITE   = "https://www.phoenixcleaningcompany.com"
PHONE_DISPLAY = "07961 915018"
PHONE_TEL     = "07961915018"
PHONE_E164    = "+447961915018"
EMAIL  = "officepcc1@gmail.com"
BUILD_DATE = "2026-06-22"

# ---- kit assets -----------------------------------------------------------
def _read(name):
    for p in (os.path.join(HERE, name), name, os.path.join("/home/claude/eatkit", name)):
        if os.path.exists(p):
            return open(p, encoding="utf-8").read()
    sys.exit(f"ERROR: required kit file '{name}' not found beside eat_build.py")

CSS = _read("eat_chrome.css")          # the locked <style>...</style> block

def _load_towns_csv():
    raw = None
    for p in (os.path.join(HERE, "eat_towns.csv"), "eat_towns.csv",
              os.path.join(HERE, "FS_towns.csv"), "FS_towns.csv"):
        if os.path.exists(p):
            raw = p; break
    if not raw:
        sys.exit("ERROR: eat_towns.csv not found beside eat_build.py")
    names = []
    with open(raw, newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            r = {k.lower().strip(): (v or "").strip() for k, v in row.items()}
            n = r.get("town") or r.get("name")
            if n:
                names.append(n)
    return names

CSV_TOWNS = _load_towns_csv()

def slugify(name):
    s = name.lower().replace("&", " and ")
    s = re.sub(r"['()]", "", s)
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", s)).strip("-")

CSV_SLUGS = {slugify(t) for t in CSV_TOWNS}

def pick(key, salt, n):
    return zlib.crc32((salt + "|" + str(key).lower()).encode()) % n

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

# ===========================================================================
# POOLS — only the cleaning pivot scaffold is pooled (and scorer-stripped).
# Pivot prose is keyed by pivot_variant; the per-town pivot_local_hook is
# spliced in so two same-variant towns never read identically.
# ===========================================================================
INTRO_POOL = [
    "{T} does not have one food scene so much as several, layered street by "
    "street. This guide does something simple: it picks one genuine standout in "
    "each of four everyday categories and uses them as doorways into the wider "
    "town.",
    "There is far more to eat in {T} than any one page could hold, so this guide "
    "keeps it honest: one real, independent standout per category - somewhere to "
    "grab a quick bite, a proper coffee, a meal out and a pint - chosen on merit.",
    "Rather than list everywhere in {T}, this guide names four places worth "
    "going out of your way for, one in each everyday category, and lets them "
    "point you towards the rest of the town.",
]

# Pivot intro lead (per variant). The town hook is appended after this.
PIVOT_INTRO = {
    "high-volume": "Every venue in this guide runs on a commercial kitchen, and "
        "behind each cookline sits an extraction system - canopy, baffle filters, "
        "plenum, ductwork and roof fan - pulling heat, smoke and grease-laden "
        "vapour out of the building.",
    "pub-town": "Behind every bar in this guide is a kitchen, and behind every "
        "kitchen an extraction system - canopy, baffle filters, plenum, ductwork "
        "and fan - drawing grease-laden air off the cookline and out through the "
        "roof.",
    "coastal": "Fryers, grills and pass after pass through a busy season put a "
        "commercial kitchen's extraction system - canopy, baffle filters, plenum, "
        "ductwork and fan - under real strain, drawing grease-laden vapour out of "
        "the building.",
    "market-town": "Every kitchen in this guide, however small, runs an "
        "extraction system - canopy, baffle filters, plenum, ductwork and fan - "
        "that pulls heat, smoke and grease-laden air off the cookline.",
}
PIVOT_LAW = ("Under the Regulatory Reform (Fire Safety) Order 2005, the "
    "\"responsible person\" for a premises must assess and manage fire risk, and "
    "a grease-laden duct is one of the most serious risks in any catering "
    "building. The Health and Safety at Work etc. Act 1974 and the Health and "
    "Safety Executive (HSE) reinforce the same duty of care, while an "
    "Environmental Health Officer (EHO) or a buildings insurer can ask to see "
    "documented proof the extraction system has been professionally cleaned.")
TR19_DEF = ("TR19 Grease is the UK industry standard for cleaning ductwork and "
    "extraction systems in commercial kitchens, published by the Building "
    "Engineering Services Association (BESA). It defines how grease deposits are "
    "measured, the maximum thickness allowed before cleaning is due, and the "
    "post-clean certification a kitchen should hold - the benchmark insurers, "
    "fire assessors and EHOs look for.")
PIVOT_PULL = {
    "high-volume": "The food gets the headlines. The extraction system is what "
        "keeps the kitchen open, insured and safe - quietly, behind the pass.",
    "pub-town": "A great pub kitchen lives or dies on its food. The extraction "
        "system is what keeps it open, insured and safe behind the scenes.",
    "coastal": "A seaside kitchen earns its year in a few hot months. A clean "
        "extraction system is what keeps it trading through every one of them.",
    "market-town": "A small kitchen is no less of a fire risk than a big one. "
        "A clean, certified extraction system is what keeps it safe and insured.",
}
INSIGHT_H3 = "The Cleaning Frequency Most Operators Get Wrong"
INSIGHT_BODY = [
    "Here is something many venue owners do not realise: under TR19 Grease, "
    "cleaning frequency is set by how many hours the kitchen actually cooks, not "
    "by how the canopy looks. A heavy-use kitchen running 12 to 16 hours a day "
    "should be cleaned roughly every three months. Moderate use of 6 to 12 hours "
    "points to every six months, and light use of 2 to 6 hours to every twelve.",
    "The catch is that baffle filters can look clean while the plenum, the "
    "horizontal duct runs and the fan housing carry a heavy grease load that "
    "throttles airflow and lowers extract efficiency. A fire in that concealed "
    "ductwork spreads fast. That is why a dated TR19 certificate, kept in the "
    "fire logbook, is the document an insurer expects to see - and its absence at "
    "the point of a claim is a common reason cover is refused.",
    "Phoenix Cleaning Company provides professional "
    "<a href=\"{SITE}/extractioncleaning.html\">kitchen extraction cleaning</a> "
    "across {T} and the UK, cleaning the full system from canopy to roof fan and "
    "issuing a dated TR19 certificate with before-and-after photographs and an "
    "access report. Teams work overnight or around your covers, so the kitchen is "
    "ready for the next service.",
]
PIVOT_CLOSE = ("Whatever the kitchen - a busy takeaway, a high-volume coffee "
    "operation, a destination dining room or a pub kitchen - the principle is the "
    "same: a clean extraction system is what stands between a thriving venue and a "
    "preventable disaster. <a href=\"{SITE}\">Phoenix Cleaning Company</a> handles "
    "that work so {T}'s kitchens can get on with feeding the town.")

# ===========================================================================
# SHARED CHROME FRAGMENTS
# ===========================================================================
TOPBAR = (
 '<header class="topbar">'
 f'<a href="{SITE}" class="topbar-brand">Phoenix <span>Cleaning</span> Company</a>'
 '<nav class="topbar-nav">'
 f'<a href="{SITE}/extractioncleaning.html" class="nav-link">Extraction Cleaning</a>'
 f'<a href="{SITE}/ductcleaning.html" class="nav-link">Duct Cleaning</a>'
 f'<a href="{SITE}/kitchencleaning.html" class="nav-link">Kitchen Cleaning</a>'
 f'<a href="{SITE}/levtesting.html" class="nav-link">LEV Testing</a>'
 f'<a href="{SITE}/contactus.html" class="nav-link">Contact</a>'
 '</nav>'
 f'<div class="topbar-cta"><a href="mailto:{EMAIL}" class="btn btn-copper">Get a Quote</a></div>'
 '</header>')

EXTRACTION_SVG = (
 '<div class="insight-svg-wrap"><svg viewBox="0 0 680 200" xmlns="http://www.w3.org/2000/svg" '
 'aria-label="Cross-section of a commercial kitchen extraction system showing grease accumulation points">'
 '<rect width="680" height="200" rx="4" fill="#1D2433"/>'
 '<text x="340" y="20" text-anchor="middle" font-family="Inter, sans-serif" font-size="9" font-weight="600" letter-spacing="2" fill="#C4793A">HOW GREASE BUILDS UP IN YOUR EXTRACTION SYSTEM</text>'
 '<rect x="40" y="135" width="200" height="14" rx="2" fill="#6B7280"/><text x="140" y="145" text-anchor="middle" font-family="Inter, sans-serif" font-size="7" font-weight="600" fill="#D1D5DB">CANOPY</text>'
 '<rect x="90" y="122" width="50" height="13" rx="1" fill="#9CA3AF"/><text x="115" y="132" text-anchor="middle" font-family="Inter, sans-serif" font-size="6.5" font-weight="600" fill="#374151">FILTER</text>'
 '<rect x="180" y="98" width="45" height="37" rx="2" fill="#4B5563"/><text x="202" y="120" text-anchor="middle" font-family="Inter, sans-serif" font-size="6.5" font-weight="600" fill="#9CA3AF">PLENUM</text>'
 '<rect x="180" y="126" width="45" height="9" rx="1" fill="#C4793A" opacity="0.3"/>'
 '<rect x="225" y="90" width="200" height="18" rx="1" fill="#4B5563"/><rect x="225" y="90" width="200" height="3.5" fill="#C4793A" opacity="0.22"/><rect x="225" y="104.5" width="200" height="3.5" fill="#C4793A" opacity="0.22"/>'
 '<text x="325" y="103" text-anchor="middle" font-family="Inter, sans-serif" font-size="6.5" font-weight="600" fill="#9CA3AF">DUCTWORK</text>'
 '<circle cx="455" cy="99" r="20" fill="#374151" stroke="#6B7280" stroke-width="1.5"/><circle cx="455" cy="99" r="3.5" fill="#6B7280"/>'
 '<line x1="455" y1="82" x2="455" y2="116" stroke="#9CA3AF" stroke-width="1.5"/><line x1="438" y1="99" x2="472" y2="99" stroke="#9CA3AF" stroke-width="1.5"/>'
 '<line x1="443" y1="87" x2="467" y2="111" stroke="#9CA3AF" stroke-width="1.5"/><line x1="443" y1="111" x2="467" y2="87" stroke="#9CA3AF" stroke-width="1.5"/>'
 '<text x="455" y="128" text-anchor="middle" font-family="Inter, sans-serif" font-size="6.5" font-weight="600" fill="#9CA3AF">FAN</text>'
 '<rect x="483" y="76" width="55" height="18" rx="1" fill="#4B5563"/><polygon points="538,72 565,85 538,98" fill="#4B5563"/><text x="510" y="89" text-anchor="middle" font-family="Inter, sans-serif" font-size="6.5" font-weight="600" fill="#9CA3AF">EXIT</text>'
 '<rect x="55" y="155" width="170" height="7" rx="1" fill="#374151"/><text x="140" y="188" text-anchor="middle" font-family="Inter, sans-serif" font-size="7" fill="#5A5E6B">COOKLINE</text>'
 '<rect x="40" y="178" width="10" height="7" rx="1" fill="#C4793A" opacity="0.3"/><text x="55" y="184" font-family="Inter, sans-serif" font-size="7" fill="#9CA3AF">Grease accumulation</text>'
 '<rect x="220" y="178" width="10" height="7" rx="1" fill="#6B7280"/><text x="235" y="184" font-family="Inter, sans-serif" font-size="7" fill="#9CA3AF">Steel components</text>'
 '</svg></div>')

CERT_STRIP = (
 '<div class="cert-strip"><div class="cert-grid">'
 '<div class="cert-item"><svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><polyline points="9 12 11 14 15 10"/></svg><h4>TR19 Certificate</h4><p>Issued on completion of every job. Accepted by insurers, fire assessors and EHO.</p></div>'
 '<div class="cert-item"><svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg><h4>Before &amp; After Photos</h4><p>Full photographic evidence of all work, provided with your report.</p></div>'
 '<div class="cert-item"><svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg><h4>24/7 Availability</h4><p>Any time of day or night, including weekends and bank holidays at no extra cost.</p></div>'
 '<div class="cert-item"><svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg><h4>Insurance Compliant</h4><p>Our certificate satisfies the requirements of all major commercial insurers.</p></div>'
 '</div></div>')

def cta_section(town):
    return (
     '<section class="cta-section"><div class="container">'
     f'<h2>Keep Your {esc(town)} Kitchen Compliant</h2>'
     f'<p>Phoenix Cleaning Company provides professional kitchen extraction system cleaning for commercial kitchens across {esc(town)} and the UK. Certified to TR19, fully insured, available 24/7 with no disruption to your service.</p>'
     '<div class="cta-actions">'
     f'<a href="tel:{PHONE_TEL}" class="btn btn-white btn-lg">Call {PHONE_DISPLAY}</a>'
     f'<a href="mailto:{EMAIL}" class="btn btn-dark btn-lg">Email for a Quote</a>'
     '</div></div></section>')

FOOTER = (
 '<footer class="footer"><div class="footer-inner">'
 '<div><div class="footer-brand">Phoenix <span>Cleaning</span> Company</div>'
 '<p>Professional kitchen extraction system, duct and laundry duct cleaning across the UK. Fully certified to TR19, 24/7 service, no disruption to your business.</p>'
 f'<p style="margin-top:0.75rem;"><a href="tel:{PHONE_TEL}" style="color:#C4793A; font-weight:600; text-decoration:none;">{PHONE_DISPLAY}</a><br>'
 f'<a href="mailto:{EMAIL}" style="color:rgba(255,255,255,0.5); text-decoration:none;">{EMAIL}</a></p></div>'
 '<div><h4>Services</h4><ul>'
 f'<li><a href="{SITE}/extractioncleaning.html">Kitchen Extraction Cleaning</a></li>'
 f'<li><a href="{SITE}/ductcleaning.html">Kitchen Duct Cleaning</a></li>'
 f'<li><a href="{SITE}/kitchencleaning.html">Kitchen Cleaning</a></li>'
 f'<li><a href="{SITE}/laundryclean.html">Laundry Duct Cleaning</a></li>'
 f'<li><a href="{SITE}/levtesting.html">LEV Testing</a></li></ul></div>'
 '<div><h4>Company</h4><ul>'
 f'<li><a href="{SITE}">About Us</a></li>'
 f'<li><a href="{SITE}/contactus.html">Contact Us</a></li>'
 f'<li><a href="mailto:{EMAIL}">Get a Quote</a></li>'
 f'<li><a href="tel:{PHONE_TEL}">Call Us</a></li></ul></div>'
 '</div>'
 '<div class="footer-bottom"><p>&copy; 2026 Phoenix Cleaning Company. Independent local food guide published by Phoenix Cleaning Company.</p>'
 f'<a href="{SITE}">phoenixcleaningcompany.com</a></div></footer>')

# ---- hero SVG -------------------------------------------------------------
def hero_svg(town, T):
    if T.get("hero_svg"):
        return T["hero_svg"]
    if T.get("hero_svg_file"):
        try:
            return _read(T["hero_svg_file"])
        except SystemExit:
            pass
    # generic palette-correct fallback (town name varies it)
    up = esc(town.upper())
    return (
     f'<svg viewBox="0 0 520 400" xmlns="http://www.w3.org/2000/svg" aria-label="Where to eat in {esc(town)} - plate and cutlery">'
     '<rect width="520" height="400" rx="6" fill="#1D2433"/>'
     '<rect x="60" y="40" width="400" height="34" rx="3" fill="#2C3040"/>'
     f'<text x="260" y="63" text-anchor="middle" font-family="Barlow Condensed, sans-serif" font-size="17" font-weight="800" letter-spacing="2" fill="#C4793A" textLength="360" lengthAdjust="spacingAndGlyphs">WHERE TO EAT IN {up}</text>'
     '<circle cx="260" cy="225" r="120" fill="#2C3040"/><circle cx="260" cy="225" r="120" fill="none" stroke="#C4793A" stroke-width="2" opacity="0.5"/>'
     '<circle cx="260" cy="225" r="86" fill="#26303F"/><circle cx="260" cy="225" r="86" fill="none" stroke="#C4793A" stroke-width="1.5" opacity="0.8"/>'
     '<g stroke="#C4793A" stroke-width="5" stroke-linecap="round" fill="none" opacity="0.92">'
     '<line x1="120" y1="170" x2="120" y2="285"/><line x1="110" y1="170" x2="110" y2="200"/><line x1="130" y1="170" x2="130" y2="200"/><line x1="110" y1="200" x2="130" y2="200"/>'
     '<line x1="400" y1="170" x2="400" y2="285"/><path d="M400 170 q16 14 0 34" /></g>'
     '<text x="260" y="360" text-anchor="middle" font-family="Inter, sans-serif" font-size="12" fill="#5A5E6B">Four independents, one local food guide</text>'
     '</svg>')

# ---- schema ---------------------------------------------------------------
def venue_schema_type(vtype):
    t = vtype.lower()
    if "cafe" in t or "coffee" in t: return "CafeOrCoffeeShop"
    if "pub" in t or "bar" in t:     return "BarOrPub"
    if "restaurant" in t:            return "Restaurant"
    return "FoodEstablishment"

def build_head(town, slug, T):
    canon = f"{DOMAIN}/eat-{slug}.html"
    title = T["meta_title"]; meta = T["meta_description"]
    webpage = {"@context":"https://schema.org","@type":"WebPage","name":title,
        "description":meta,"url":canon,"inLanguage":"en-GB",
        "datePublished":BUILD_DATE,"dateModified":BUILD_DATE,
        "publisher":{"@type":"Organization","name":"Phoenix Cleaning Company","url":SITE,
            "telephone":PHONE_E164,"email":EMAIL},
        "about":{"@type":"Thing","name":f"Restaurants and places to eat in {town}"}}
    items = []
    for i, v in enumerate(T["venues"], 1):
        items.append({"@type":"ListItem","position":i,"item":{
            "@type":venue_schema_type(v["type"]),"name":v["name"],
            "servesCuisine":v.get("cuisine","Food"),
            "address":{"@type":"PostalAddress","addressLocality":town,
                       "addressRegion":T.get("region",""),"addressCountry":"GB"}}})
    itemlist = {"@context":"https://schema.org","@type":"ItemList",
        "name":f"Best Places to Eat in {town}",
        "itemListOrder":"https://schema.org/ItemListUnordered",
        "numberOfItems":len(items),"itemListElement":items}
    faqpage = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
        {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}}
        for q,a in T["faq"]]}
    org = {"@context":"https://schema.org","@type":"Organization",
        "@id":f"{SITE}/#organization","name":"Phoenix Cleaning Company","url":SITE,
        "description":"UK commercial kitchen extraction system, duct and laundry duct cleaning to the TR19 Grease standard. Certified, insured, available 24/7.",
        "telephone":PHONE_E164,"email":EMAIL,"areaServed":"GB",
        "knowsAbout":["Kitchen extraction system cleaning","Kitchen duct cleaning",
            "TR19 Grease compliance","LEV testing","Commercial kitchen deep cleaning"]}
    crumb = {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Home","item":DOMAIN},
        {"@type":"ListItem","position":2,"name":"Places to Eat","item":f"{DOMAIN}/places-to-eat"},
        {"@type":"ListItem","position":3,"name":town,"item":canon}]}
    def ld(o): return '<script type="application/ld+json">\n'+json.dumps(o, ensure_ascii=False)+'\n</script>'
    return (
     '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">'
     '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
     f'<title>{esc(title)}</title>\n'
     f'<meta name="description" content="{esc(meta)}">\n'
     f'<link rel="canonical" href="{canon}">\n'
     f'<meta property="og:title" content="{esc(title)}">\n'
     f'<meta property="og:description" content="{esc(meta)}">\n'
     '<meta property="og:type" content="website">\n'
     f'<meta property="og:url" content="{canon}">\n'
     '<link rel="preconnect" href="https://fonts.googleapis.com">'
     '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
     '<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">\n'
     + ld(webpage)+"\n"+ld(itemlist)+"\n"+ld(faqpage)+"\n"+ld(org)+"\n"+ld(crumb)+"\n"
     + CSS + '</head><body id="top">\n')

# ---- nearby hard guard ----------------------------------------------------
def require_nearby(town, T):
    nb = T.get("nearby") or []
    if len(nb) < 3:
        sys.exit(f"ERROR [{town}]: needs 3 hand-authored nearby towns, found {len(nb)}")
    bad = [n for n in nb if slugify(n) not in CSV_SLUGS]
    if bad:
        sys.exit(f"ERROR [{town}]: nearby not on CSV (would be dead links): {bad}")
    return nb[:3]


def _parse_date(s):
    try:
        return datetime.date.fromisoformat(str(s).strip())
    except Exception:
        return None


def require_evidence(town, T):
    """Hard-gate the research: every venue must carry a source_url and a
    parseable `verified` ISO date (YYYY-MM-DD). London-style general-knowledge
    flagships may set `evidence_exempt: True`. Returns the audit manifest dict.
    Stale verifications warn (re-verify) but do not fail the build."""
    slug = slugify(town)
    if T.get("evidence_exempt"):
        return {"slug": slug, "town": town, "built_at": BUILD_DATE,
                "exempt": True, "reason": T.get("evidence_exempt_reason", "general-knowledge flagship"),
                "venues": [{"name": v.get("name", "")} for v in T.get("venues", [])],
                "nearby": T.get("nearby", [])[:3]}
    problems, vman = [], []
    today = datetime.date.today()
    for i, v in enumerate(T.get("venues", []), 1):
        name = v.get("name", f"venue {i}")
        src = (v.get("source_url") or "").strip()
        ver = _parse_date(v.get("verified"))
        if not src or not re.match(r"^https?://", src):
            problems.append(f"venue '{name}' missing/invalid source_url")
        if not ver:
            problems.append(f"venue '{name}' missing/invalid verified date (need YYYY-MM-DD)")
        elif (today - ver).days > EVIDENCE_STALE_DAYS:
            print(f"   warn [{town}]: '{name}' verified {ver} is >{EVIDENCE_STALE_DAYS}d old - re-confirm it is still trading")
        vman.append({"name": name, "source_url": src, "verified": str(v.get("verified", ""))})
    if problems:
        sys.exit(f"ERROR [{town}]: --require-evidence failed:\n   - " + "\n   - ".join(problems)
                 + "\n   (research the town live and add source_url + verified per venue in towns_data.py)")
    return {"slug": slug, "town": town, "built_at": BUILD_DATE, "exempt": False,
            "venues": vman, "nearby": T.get("nearby", [])[:3]}

# ===========================================================================
# ASSEMBLE
# ===========================================================================
def venue_card(v):
    return (
     '<div class="venue">'
     f'<span class="venue-tag">{esc(v["type"])}</span>'
     f'<h3 class="venue-name">{esc(v["name"])}</h3>'
     f'<div class="venue-area">{esc(v["area"])}</div>'
     f'<p>{v["body"]}</p>'
     '<div class="venue-meta">'
     f'<div><div class="meta-label">Known for</div><div class="meta-text">{esc(v["known_for"])}</div></div>'
     f'<div><div class="meta-label">Good for</div><div class="meta-text">{esc(v["good_for"])}</div></div>'
     '</div></div>')

def assemble(slug, town):
    T = TOWNS[town.lower()]
    nearby = require_nearby(town, T)
    var = T.get("pivot_variant", "high-volume")
    if var not in PIVOT_INTRO: var = "high-volume"
    P = lambda pool, salt: pool[pick(town, salt, len(pool))]

    H = [build_head(town, slug, T), TOPBAR]

    # hero
    H.append(
     '<section class="hero"><div class="hero-inner"><div>'
     f'<p class="hero-eyebrow">{esc(town)} Food &amp; Drink Guide</p>'
     f'<h1>Best Places to <span>Eat</span> in {esc(town)}</h1>'
     f'<p class="hero-sub">{esc(T["snapshot"][:155].rsplit(" ",1)[0])}...</p>'
     '<div class="hero-actions">'
     '<a href="#picks" class="btn btn-copper btn-lg">See the Four Picks</a>'
     '<a href="#scene" class="btn btn-outline-copper btn-lg">The Food Scene</a>'
     f'</div></div><div class="hero-image-wrap">{hero_svg(town, T)}</div></div></section>')

    H.append(f'<div class="alert-band"><p>{esc(T["trust_strip"])}</p></div>')
    H.append('<nav class="jump-links" aria-label="On this page">'
     '<a href="#picks">The Four Picks</a><a href="#scene">The Food Scene</a>'
     '<a href="#kitchens">Behind the Pass</a><a href="#visit">Planning Your Visit</a>'
     '<a href="#faq">FAQ</a></nav>')

    H.append('<main><article>')

    # 1 — Where to eat
    intro = P(INTRO_POOL, "intro").format(T=esc(town))
    stat_cards = "".join(
        f'<div class="stat-card"><div class="stat-num">{esc(str(val))}</div>'
        f'<div class="stat-label">{esc(lbl)}</div></div>' for val, lbl in T["stats"])
    H.append(
     '<section class="section section-light"><div class="article-content">'
     f'<h2>Where to Eat in {esc(town)}</h2>'
     '<div class="snapshot"><span class="lbl">'
     '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>'
     f'Quick Answer</span><p>{esc(T["snapshot"])}</p></div>'
     f'<p>{intro}</p>'
     f'<div class="stat-row">{stat_cards}</div>'
     '</div></section>')

    # 2 — The Four Picks
    cards = "".join(venue_card(v) for v in T["venues"])
    glance = "".join(
        f'<div class="glance-col"><h4>{esc(h)}</h4><p>{esc(b)}</p></div>'
        for h, b in T["glance"])
    H.append(
     '<section class="section section-alt" id="picks"><div class="article-content">'
     '<p class="section-label">The Shortlist</p><h2 class="section-title">The Four Picks</h2>'
     f'{cards}<div class="glance">{glance}</div></div></section>')

    # 3 — Food scene + mid CTA
    fs = "".join(f"<p>{p}</p>" for p in T["food_scene"])
    H.append(
     '<section class="section section-light" id="scene"><div class="article-content">'
     f'<h2>{esc(town)}\'s Food Scene</h2>{fs}'
     '<div class="mid-cta">'
     f'<p>Run a kitchen in {esc(town)}? Phoenix keeps extraction systems clean, certified and compliant - overnight, with no disruption to service.</p>'
     f'<a href="tel:{PHONE_TEL}" class="btn btn-white">Call {PHONE_DISPLAY}</a>'
     '</div></div></section>')

    # 4 — The pivot
    hook = T.get("pivot_local_hook", "")
    p1 = PIVOT_INTRO[var] + (" " + hook if hook else "")
    insight_body = "".join(
        f"<p>{p.format(SITE=SITE, T=esc(town))}</p>" for p in INSIGHT_BODY)
    H.append(
     '<section class="section section-alt" id="kitchens"><div class="article-content">'
     f'<h2>Behind the Pass: The Kitchens That Keep {esc(town)} Fed</h2>'
     f'<p>{p1}</p><p>{PIVOT_LAW}</p>'
     '<div class="snapshot"><span class="lbl">'
     '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>'
     f'What is TR19 Grease?</span><p>{TR19_DEF}</p></div>'
     f'<div class="pull-quote"><p>{esc(P([PIVOT_PULL[var]], "pull"))}</p></div>'
     '<div class="insight-box"><div class="insight-label">'
     '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>'
     f'Industry Insight</div><h3>{INSIGHT_H3}</h3>{insight_body}{EXTRACTION_SVG}</div>'
     f'<p>{PIVOT_CLOSE.format(SITE=SITE, T=esc(town))}</p>'
     '</div></section>')

    # 5 — Planning + what to order
    visit = "".join(f"<p>{p}</p>" for p in T["visit"])
    checks = "".join(f"<li>{esc(c)}</li>" for c in T["checklist"])
    H.append(
     '<section class="section section-light" id="visit"><div class="article-content">'
     f'<h2>Planning Your Visit</h2>{visit}'
     f'<ul class="eat-check">{checks}</ul>'
     f'<h2>What to Order and How to Do the Day</h2><p>{T["what_to_order"]}</p>'
     '</div></section>')

    # 6 — FAQ
    faq = "".join(
        f'<div style="border-bottom:1px solid var(--border); padding:1.25rem 0;">'
        f'<h3 style="font-family:\'Barlow Condensed\',sans-serif; font-size:1.15rem; color:var(--charcoal); margin-bottom:0.6rem;">{esc(q)}</h3>'
        f'<p style="margin:0; color:var(--text); font-size:0.95rem; line-height:1.65;">{esc(a)}</p></div>'
        for q, a in T["faq"])
    H.append(
     '<section class="section section-alt" id="faq"><div class="article-content">'
     '<p class="section-label">Frequently Asked Questions</p>'
     f'<h2 class="section-title">{esc(town)} Food and Drink FAQ</h2>'
     f'<div style="margin-top:1.5rem;">{faq}</div></div></section>')

    H.append('</article></main>')

    # tail chrome
    H.append(CERT_STRIP)
    H.append(cta_section(town))
    nb = "".join(
        f'<a href="eat-{slugify(n)}.html" class="related-card"><p class="rc-cat">Food Guide</p>'
        f'<h3>Best Places to Eat in {esc(n)}</h3></a>' for n in nearby)
    nb += (f'<a href="{SITE}/extractioncleaning.html" class="related-card">'
           '<p class="rc-cat">Our Services</p>'
           '<h3>Kitchen Extraction Cleaning &mdash; UK Wide</h3></a>')
    H.append('<section class="related-section"><div class="related-inner">'
     '<p class="section-label">Best Places to Eat in Nearby Towns</p>'
     f'<div class="related-grid">{nb}</div></div></section>')
    H.append(FOOTER + "\n</body></html>")
    return "\n".join(H)

def main():
    global REQUIRE_EVIDENCE, EVIDENCE_STALE_DAYS
    outdir = "/mnt/user-data/outputs"
    os.makedirs(outdir, exist_ok=True)
    raw = sys.argv[1:]
    # flags
    if "--require-evidence" in raw:
        REQUIRE_EVIDENCE = True
        raw = [a for a in raw if a != "--require-evidence"]
    if "--max-age-days" in raw:
        i = raw.index("--max-age-days")
        try:
            EVIDENCE_STALE_DAYS = int(raw[i + 1]); del raw[i:i + 2]
        except (IndexError, ValueError):
            sys.exit("ERROR: --max-age-days needs an integer")
    args = [a.lower() for a in raw] or list(TOWNS)
    for key in args:
        if key not in TOWNS:
            print(f"SKIP {key}: not in TOWNS (web-research it into towns_data.py first)")
            continue
        town = " ".join(w.capitalize() for w in key.split("-")) if "-" in key else \
               " ".join(w.capitalize() for w in key.split())
        # prefer the canonical CSV spelling if present
        for t in CSV_TOWNS:
            if slugify(t) == slugify(key):
                town = t; break
        slug = slugify(town)
        manifest = require_evidence(town, TOWNS[town.lower()]) if REQUIRE_EVIDENCE else None
        html = assemble(slug, town)
        path = os.path.join(outdir, f"eat-{slug}.html")
        open(path, "w", encoding="utf-8").write(html)
        tag = ""
        if manifest is not None:
            open(os.path.join(outdir, f"eat-{slug}.evidence.json"), "w", encoding="utf-8").write(
                json.dumps(manifest, ensure_ascii=False, indent=2))
            tag = "  [evidence: EXEMPT]" if manifest.get("exempt") else "  [evidence: OK]"
        print(f"WROTE {path}  ({len(re.sub(r'<[^>]+>',' ',html).split())} words incl. chrome){tag}")

# import data at module load (after helpers defined)
from towns_data import TOWNS  # noqa: E402

if __name__ == "__main__":
    main()
