TOWNS = {}

# --------------------------------------------------------------------------
# CARDIFF — web-researched 2026-06-22
# Sources: guide.michelin.com, ffwrnes.co.uk, waterlootea.com,
#          tinyrebel.co.uk, gorserestaurant.co.uk, purplepoppadom.com,
#          tripadvisor.co.uk, yelp.co.uk, visitcardiff.com
# --------------------------------------------------------------------------
TOWNS["cardiff"] = {
    "region": "Wales",
    "population": "390K",
    "nearby": ["Newport", "Penarth", "Barry"],
    "meta_title": "Best Places to Eat in Cardiff: Local Food Guide",
    "meta_description": (
        "Wood-fired pizza in the Victorian Market, an arcade teahouse, "
        "Cardiff first Michelin star and Welsh craft ale. "
        "Four independents. Read the guide."
    ),
    "trust_strip": (
        "From wood-fired pizza in a Victorian market to Cardiff's first "
        "Michelin-starred tasting menu, the Welsh capital punches well above "
        "its weight for independent food"
    ),
    "snapshot": (
        "For a fast answer: Ffwrnes Pizza at Cardiff Central Market for "
        "wood-fired Neapolitan with Welsh toppings, Waterloo Tea in the "
        "Wyndham Arcade for one of the finest teahouses in Britain, Gorse "
        "on Kings Road in Pontcanna for Cardiff's first Michelin-starred "
        "Welsh tasting menu, and Tiny Rebel on Westgate Street for craft "
        "ale from Wales's Supreme Champion Beer of Britain brewery. Four "
        "moods, one walkable Welsh capital."
    ),
    "stats": [
        ("390K", "Cardiff population (approx)"),
        ("2025", "Year Cardiff earned its first Michelin star"),
        ("5", "Cardiff's Victorian and Edwardian shopping arcades"),
        ("4", "Hand-picked independents"),
    ],
    "pivot_variant": "high-volume",
    "pivot_local_hook": (
        "Cardiff's food scene runs from wood-fired pizza ovens in a Victorian "
        "market to the tasting-menu kitchens of Pontcanna, each service "
        "pushing a heavy load of grease-laden vapour into canopies above "
        "the pass."
    ),
    "venues": [
        {
            "type": "Takeaway",
            "name": "Ffwrnes Pizza",
            "area": "Cardiff Central Market, St Mary Street (first floor stalls)",
            "cuisine": "Wood-fired Neapolitan pizza, Welsh ingredients",
            "body": (
                "Ffwrnes (Welsh for 'oven') began as a Piaggio van called Smokey Pete "
                "in 2014, when friends Ieuan Harry and Jeremy Phillips took their "
                "wood-fired rig to events across Wales. With a Development Bank of "
                "Wales micro-loan they graduated to a permanent stall on the first "
                "floor of Cardiff's Victorian Central Market, opening there in 2018. "
                "The set-up is deliberately simple: a short list of twelve Neapolitan-"
                "style pizzas made with Welsh produce — salt-marsh lamb, local chorizo, "
                "Welsh cheese — fired in a proper wood oven, then eaten standing at a "
                "counter or taken away. The 'Pizza Boys', as they are known from a BBC "
                "series and the Welsh-language Bois y Pizza on S4C, have become one of "
                "Cardiff's most-loved food stories. The food hygiene check confirmed "
                "them trading in February 2026."
            ),
            "known_for": "Welsh-ingredient wood-fired Neapolitan pizza in a Victorian market",
            "good_for": "A fast, characterful lunch in a historic setting",
            "source_url": "https://ratings.food.gov.uk/business/1076564/ffwrnes-pizza-cardiff",
            "verified": "2026-06-22",
        },
        {
            "type": "Cafe",
            "name": "Waterloo Tea",
            "area": "Wyndham Arcade, Mill Lane, city centre",
            "cuisine": "Speciality tea and coffee, all-day cafe",
            "body": (
                "Kasim Ali founded Waterloo Tea in Penylan in 2008 and within a year "
                "the tea house had been named Best Cafe in the UK by the Beverage "
                "Standards Association, after three unannounced visits. The Wyndham "
                "Arcade branch, which opened in 2014, sits inside one of the city's "
                "oldest covered arcades — iron-and-glass Victorian vaulting, built in "
                "1887 — and offers a selection of more than 60 loose-leaf teas sourced "
                "from India, China, Sri Lanka, Taiwan and Japan, alongside speciality "
                "coffee roasted locally by Hard Lines. The two-floor space is calm and "
                "unhurried, with an afternoon tea of handmade sandwiches, scones with "
                "clotted cream and seasonal cakes. January 2026 reviews confirm it is "
                "actively trading with consistently high ratings."
            ),
            "known_for": "60-plus loose-leaf teas, UK's Best Cafe award, Victorian arcade setting",
            "good_for": "A long, relaxed tea break or afternoon tea in a remarkable room",
            "source_url": "https://waterlootea.com/pages/city-centre",
            "verified": "2026-06-22",
        },
        {
            "type": "Restaurant",
            "name": "Gorse",
            "area": "186-188 Kings Road, Pontcanna",
            "cuisine": "Modern Welsh fine dining, tasting menu",
            "body": (
                "Tom Waters trained at The Square and at Heston Blumenthal's Fat Duck "
                "before returning to his native Wales to open Gorse in Pontcanna in "
                "May 2024. Less than nine months later, in February 2025, it became "
                "Cardiff's first ever Michelin-starred restaurant. The small dining "
                "room — an open kitchen, a handful of tables, handcrafted Welsh "
                "ceramics on every surface — serves a tasting menu of seven or ten "
                "courses built around micro-seasonal Welsh produce: seaweed from the "
                "Pembrokeshire coast, mountain lamb, foraged herbs. Waters describes "
                "his aim as putting the best of Wales on the plate, and the 2026 "
                "Michelin Guide confirmed the star retained. Book well ahead; the "
                "restaurant opens Wednesday evenings and Thursday to Saturday for "
                "lunch and dinner."
            ),
            "known_for": "Cardiff's first Michelin star, modern Welsh seasonal tasting menu",
            "good_for": "A landmark occasion meal rooted in Welsh landscape and produce",
            "source_url": "https://guide.michelin.com/gb/en/south-glamorgan/cardiff/restaurant/gorse",
            "verified": "2026-06-22",
        },
        {
            "type": "Pub",
            "name": "Tiny Rebel Cardiff",
            "area": "25 Westgate Street, city centre (by Principality Stadium)",
            "cuisine": "Craft beer, pub food",
            "body": (
                "Tiny Rebel was founded in Newport in 2012 by brothers-in-law Bradley "
                "Cummings and Gareth Williams. Their Cwtch red ale won Supreme "
                "Champion Beer of Britain in 2015 — the youngest brewery and the first "
                "from Wales to take the title. The Cardiff bar opened in 2013 in a "
                "Grade II listed building on Westgate Street — a late-Victorian county "
                "club with heavy iron shutters on the original treasury windows — just "
                "yards from the Principality Stadium. Two floors of quirky rooms pour "
                "Tiny Rebel's own beers alongside rotating craft lines and up to four "
                "Welsh ciders. May 2026 reviews confirm it is open and busy, with "
                "quiz nights, vinyl evenings and an accessible food menu running "
                "Monday to Saturday until 9pm."
            ),
            "known_for": "Cwtch, Supreme Champion Beer of Britain 2015, Grade II listed building",
            "good_for": "A pint of award-winning Welsh craft ale in a characterful listed pub",
            "source_url": "https://www.tinyrebel.co.uk/bars/cardiff",
            "verified": "2026-06-22",
        },
    ],
    "food_scene": [
        (
            "Cardiff's food map is shaped by its Victorian heritage and its position as a "
            "young, outward-looking capital. The city centre is threaded by five covered "
            "arcades — more Victorian and Edwardian covered walkways than any other city "
            "in the UK — and these have become home to some of its most creative "
            "independent food businesses, from loose-leaf tea rooms to deli counters. "
            "Cardiff Central Market, built in 1891 inside an ornate iron-and-glass "
            "structure, hosts wood-fired pizza, pierogi and souvlaki stalls alongside "
            "the oldest fishmongers and butchers in the city."
        ),
        (
            "A short walk west, the neighbourhoods of Pontcanna and Canton have become "
            "Cardiff's most settled food quarter. Kings Road and Pontcanna Street hold "
            "independent brunch cafes, neighbourhood bistros and, since 2024, the city's "
            "first Michelin-starred restaurant. City Road in Roath plays a different role: "
            "an international food mile where Syrian, Korean, Lebanese and Chinese "
            "kitchens stand shoulder to shoulder, reflecting Cardiff's historic port "
            "diversity. Cardiff Bay adds waterfront dining to the mix."
        ),
        (
            "Welsh produce runs through the best kitchens: laverbread — an edible seaweed "
            "harvested from Welsh shores and pan-fried with bacon — is one of the city's "
            "signature breakfast ingredients, and Cardiff Market sells it fresh. Salt-marsh "
            "lamb from the Gower, Pembrokeshire shellfish and Welsh dairy appear across "
            "menus at every price point, and the craft-beer scene anchored by Newport "
            "brewery Tiny Rebel gives the city a distinctly Welsh drinking character."
        ),
    ],
    "visit": [
        (
            "The city centre is compact and walkable. The arcades, Cardiff Central Market "
            "and Westgate Street are within ten minutes of each other on foot, making it "
            "easy to take in the Victorian covered walkways before settling in for lunch. "
            "Pontcanna is a twenty-minute walk west of the centre along Cathedral Road, "
            "or a short taxi ride from Cardiff Central station."
        ),
        (
            "Time a visit well and the day shapes itself: a tea at Waterloo in the Wyndham "
            "Arcade, pizza at Ffwrnes in the Central Market, an evening tasting menu at "
            "Gorse, and a nightcap of Welsh craft ale at Tiny Rebel before the walk back "
            "to the station. Book Gorse weeks ahead; Tiny Rebel and Ffwrnes take walk-ins."
        ),
    ],
    "checklist": [
        "Walk the Victorian arcades from the Royal Arcade (1858) through to Wyndham, then take tea at Waterloo",
        "Head to Cardiff Central Market for Ffwrnes pizza at the first-floor stall",
        "Book Gorse in Pontcanna well in advance — it opens four services a week and fills quickly",
        "Tiny Rebel is two minutes from Cardiff Central station, a natural last stop",
        "Cardiff Central station has direct trains to Newport, Barry and Penarth for a day trip extension",
    ],
    "what_to_order": (
        "Order with intent. At Ffwrnes, the salt-marsh lamb or Welsh cheese pizza fresh from "
        "the wood oven. At Waterloo Tea, ask which single-origin is on filter that day, then "
        "settle in for a full afternoon tea if time allows. At Gorse, trust the ten-course menu "
        "and whatever micro-seasonal Welsh produce Waters is working with that week. At Tiny "
        "Rebel, a pint of Cwtch red ale — the beer that put Welsh craft brewing on the national "
        "map — and the pub food menu if you need something to eat."
    ),
    "glance": [
        ("Best for a quick bite", "Ffwrnes Pizza, for a wood-fired Welsh pizza at Cardiff Central Market"),
        ("Best for an occasion", "Gorse, for Cardiff's first Michelin-starred Welsh tasting menu in Pontcanna"),
        ("Best for atmosphere", "Waterloo Tea in the Wyndham Arcade, under Victorian iron-and-glass vaulting"),
    ],
    "faq": [
        (
            "Where can I get the best independent pizza in Cardiff?",
            "Ffwrnes Pizza at Cardiff Central Market has been serving wood-fired Neapolitan "
            "pizza with Welsh ingredients — salt-marsh lamb, local cheese — from the "
            "Victorian market's first floor since 2018, and its food hygiene rating was "
            "renewed in February 2026 confirming it is trading.",
        ),
        (
            "Which is the best cafe or tea room in Cardiff city centre?",
            "Waterloo Tea at the Wyndham Arcade is widely regarded as one of the finest "
            "in Wales. Founded in Penylan in 2008 by Kasim Ali, it was named Best Cafe "
            "in the UK by the Beverage Standards Association and the Wyndham Arcade "
            "branch offers over 60 loose-leaf teas in a beautifully preserved Victorian "
            "arcade setting.",
        ),
        (
            "Does Cardiff have any Michelin-starred restaurants?",
            "Yes. Gorse on Kings Road in Pontcanna, opened by chef Tom Waters in May 2024, "
            "became Cardiff's first Michelin-starred restaurant in February 2025 and "
            "retained its star in the 2026 guide. Waters previously trained at The Square "
            "and Heston Blumenthal's Fat Duck, and the menu is built entirely around "
            "seasonal Welsh produce.",
        ),
        (
            "What is the best pub for real ale and craft beer in Cardiff?",
            "Tiny Rebel on Westgate Street is the flagship bar of the Newport brewery "
            "whose Cwtch red ale won Supreme Champion Beer of Britain in 2015 — the "
            "first Welsh brewery to take the title. The Cardiff bar opened in 2013 in a "
            "Grade II listed Victorian building a short walk from the Principality Stadium "
            "and confirmed open as of May 2026.",
        ),
        (
            "What traditional Welsh food can I try in Cardiff?",
            "Laverbread — seaweed harvested from Welsh shores, pan-fried and traditionally "
            "served with smoked bacon — is a Cardiff breakfast staple available at Cardiff "
            "Market stalls. Welsh salt-marsh lamb, Pembrokeshire shellfish and Welsh rarebit "
            "appear across city-centre menus. Ffwrnes Pizza uses Welsh produce, and Gorse "
            "sources almost entirely from small Welsh farms and fishermen.",
        ),
        (
            "Are Cardiff's best food spots easy to reach without a car?",
            "Very. Cardiff Central Market, Waterloo Tea and Tiny Rebel are all within "
            "ten minutes on foot from Cardiff Central station. Pontcanna (for Gorse) is "
            "a twenty-minute walk or a short taxi ride. Newport, Penarth and Barry are "
            "all reachable by direct train in under thirty minutes.",
        ),
    ],
}
