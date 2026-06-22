TOWNS = {}

# --------------------------------------------------------------------------
# READING — web-researched 2026-06-22
# --------------------------------------------------------------------------
TOWNS["reading"] = {
    "region": "Berkshire",
    "population": "220K",
    "nearby": ["Wokingham", "Maidenhead", "Bracknell"],
    "meta_title": "Best Places to Eat in Reading: Local Food Guide",
    "meta_description": (
        "Where to eat in Reading: pan-Asian plates, a sourdough forge cafe, "
        "a Kennet riverside brasserie and a CAMRA free house. Read the guide."
    ),
    "trust_strip": (
        "From a riverside brasserie that opened the year the Oracle launched "
        "to a CAMRA-celebrated free house on Russell Street, Reading punches "
        "well above its size for independent eating"
    ),
    "snapshot": (
        "For a fast answer: Coconut Bar and Kitchen on St Mary's Butts for "
        "pan-Asian plates and katsu curry at any hour, Shed at the Old Forge "
        "for proper sourdough and handmade sandwiches, London Street Brasserie "
        "for riverside modern-British dining since 2000, and the Nag's Head on "
        "Russell Street for 12 changing real ales and CAMRA's seal of approval. "
        "Four moods, one compact Berkshire town."
    ),
    "stats": [
        ("220K", "Population (approx)"),
        ("2000", "Year London Street Brasserie opened beside the Kennet"),
        ("12", "Changing real ales on the Nag's Head handpumps"),
        ("4", "Hand-picked independents"),
    ],
    "pivot_variant": "high-volume",
    "pivot_local_hook": (
        "Reading's kitchens run long hours: the Oracle Riverside bars and "
        "restaurants turn over multiple services a day, the Oxford Road "
        "curry houses run late-night fryers every evening, and the town's "
        "pan-Asian and brasserie kitchens throw a sustained grease-laden "
        "vapour load into their canopies from lunchtime through last orders."
    ),
    "venues": [
        {
            "type": "Casual",
            "name": "Coconut Bar and Kitchen",
            "area": "St Mary's Butts, town centre",
            "cuisine": "Pan-Asian — Japanese, Korean, Malaysian, Thai",
            "body": (
                "Opened in 2014 on St Mary's Butts, directly opposite the Broad "
                "Street Mall and a five-minute walk from the station, Coconut Bar "
                "and Kitchen draws on half a dozen Asian food traditions without "
                "muddying any of them. The setting is industrial chic — galvanised "
                "metal, exposed pipework, bare-filament bulbs — and the menu "
                "ranges from Japanese katsu curry and Korean bibimbap to Malaysian "
                "rice noodles and Thai chicken wings, with everything cooked fresh. "
                "The chicken katsu with gyudon sauce and shiitake mushrooms on "
                "Japanese rice is the dish most tables order. Bookings are taken "
                "and it opens seven days; the bottomless brunch runs Sunday to "
                "Friday for those who want prosecco with their prawn katsu."
            ),
            "known_for": "Japanese katsu curry, Korean bibimbap and a long pan-Asian menu",
            "good_for": "Casual weekday lunch or a lively evening with a crowd",
            "source_url": "https://www.coconutbarkitchen.co.uk/",
            "verified": "2026-06-22",
        },
        {
            "type": "Cafe",
            "name": "Shed",
            "area": "Merchants Place (The Old Forge), town centre",
            "cuisine": "Handmade sandwiches, sourdough, soup, coffee",
            "body": (
                "Shed started making sandwiches in the summer of 2012 and has "
                "grown quietly into one of Reading's most-recommended lunch stops. "
                "It occupies an old forge in Merchants Place, and the exposed "
                "brick and low ceilings give it exactly the atmosphere the name "
                "suggests. Everything is made in-house and in small batches: "
                "doorstop sourdough sandwiches, stuffed wraps, hearty salad boxes "
                "and home-baked cakes, alongside Italian coffee and quality "
                "loose-leaf teas. They buy local wherever they can and cook what "
                "they cook well rather than expanding the range endlessly. Open "
                "Monday to Friday from 8am and Saturday from 10am, food until "
                "3pm — ideal for a properly assembled lunch rather than a "
                "counter grab."
            ),
            "known_for": "Sourdough toasties, doorstop sandwiches and home-baked cakes in an old forge",
            "good_for": "A proper sit-down lunch in the town centre",
            "source_url": "https://theshedcafe.co.uk/",
            "verified": "2026-06-22",
        },
        {
            "type": "Restaurant",
            "name": "London Street Brasserie",
            "area": "2-4 London Street, beside the Kennet",
            "cuisine": "Modern British brasserie",
            "body": (
                "London Street Brasserie opened in 2000 in a Grade II-listed toll "
                "house built in 1750 on Duke Street bridge, literally cantilevered "
                "out over the River Kennet. Chef-proprietor Paul Clerehugh has "
                "made it Reading's most celebrated independent restaurant: Michelin "
                "recognition, regular best-of listings, and 918 OpenTable reviews "
                "averaging 4.7 stars underline two decades of consistent cooking. "
                "The menu is modern British with a brasserie tempo — good "
                "ingredients, clean flavours, no fuss — served across two rooms "
                "and a small riverside terrace. The set lunch menu (noon to 6pm) "
                "is well-priced for the quality; Sunday lunch fills early. Book "
                "ahead at weekends, especially for the Kennet-facing terrace seats."
            ),
            "known_for": "Two decades of modern-British brasserie cooking beside the Kennet, Michelin-noted",
            "good_for": "A proper occasion meal or a long riverside Sunday lunch",
            "source_url": "https://www.londonstreetbrasserie.co.uk/",
            "verified": "2026-06-22",
        },
        {
            "type": "Pub",
            "name": "The Nag's Head",
            "area": "5 Russell Street, near the station",
            "cuisine": "Real ale and craft cider free house",
            "body": (
                "The Nag's Head on Russell Street is Reading's most-decorated "
                "ale pub: a multiple winner of Reading and Mid-Berkshire CAMRA "
                "Pub of the Year and a recurrent entry in the Good Beer Guide, "
                "the pub has 12 constantly rotating real ales on handpump, a "
                "14-tap craft keg wall and 13 ciders and perries, with the "
                "blackboard noting vessel type and dispense method beside each. "
                "The selection tilts toward local and independent breweries, and "
                "the stock turns fast enough that every visit brings something "
                "different. There is a covered garden for warmer months, board "
                "games on the shelves, and basic hot food to line the stomach. "
                "It is a genuine free house — no tie, no corporate landlord — "
                "and five minutes from the station, which means it is usually "
                "the first stop recommended to anyone arriving in Reading by train."
            ),
            "known_for": "12 rotating real ales, 13 ciders, multiple CAMRA Pub of the Year wins",
            "good_for": "Serious ale and cider drinking close to the station",
            "source_url": "https://camra.org.uk/pubs/nags-head-reading-155710",
            "verified": "2026-06-22",
        },
    ],
    "food_scene": [
        (
            "Reading's food geography divides into three zones. The town centre "
            "clusters around the Oracle shopping complex and its riverside strip "
            "on the Kennet and Avon Canal — a run of bars and restaurants that "
            "fills at lunchtime and again from early evening. London Street and "
            "the waterfront give it the most characterful setting, with the canal "
            "running underneath the oldest buildings. Friar Street and Gun Street "
            "hold the independent bars and late-night venues."
        ),
        (
            "The Oxford Road corridor, running south-west from the centre, is "
            "where Reading's South Asian and global food traditions are strongest. "
            "Curry houses, Bangladeshi restaurants and international kitchens line "
            "the road, and it is busy most evenings. St Mary's Butts and the "
            "surrounding streets form a compact eating district between the Oracle "
            "and the station, with the pan-Asian and casual options. Caversham, "
            "just north across the Thames, has a quieter village-scale food scene "
            "of its own."
        ),
        (
            "Reading does not have one signature dish in the way that Birmingham "
            "has the balti, but its food market — held on the first and third "
            "Saturday of each month at the old cattle market on Great Knollys "
            "Street — gives a good cross-section of what local producers are "
            "growing and making. The town's independent food scene grew notably "
            "across 2024-2025, with more openings than closures and a spread of "
            "kitchens confident enough to specialise rather than try to be "
            "everything to everyone."
        ),
    ],
    "visit": [
        (
            "Shed and Coconut Bar and Kitchen both sit within five minutes of the "
            "station and of each other, making the town centre zone easy on foot. "
            "London Street Brasserie is a short walk east along the Kennet — "
            "follow the riverside path from the Oracle — and the Nag's Head is "
            "a two-minute walk from the station on Russell Street. All four "
            "venues are reachable without a car from Reading railway station, "
            "which sits on the Great Western Main Line with fast links from "
            "London Paddington (25 minutes), Bristol and Oxford."
        ),
        (
            "The Oracle Riverside is the obvious landmark to navigate from — "
            "the Kennet runs underneath the shopping centre and the riverside "
            "walkway connects the Oracle to London Street. Time a visit around "
            "Shed's Monday-to-Friday hours if a daytime sandwich stop is on the "
            "plan; London Street Brasserie's set lunch menu runs noon to 6pm "
            "and is the best-value entry point to the riverside brasserie. "
            "The Nag's Head is the natural finishing point for the evening."
        ),
    ],
    "checklist": [
        "Chicken katsu with gyudon sauce at Coconut Bar and Kitchen",
        "A sourdough doorstop sandwich at Shed in the old forge on Merchants Place",
        "The set lunch menu at London Street Brasserie on the Kennet terrace",
        "A pint of whatever is freshest on the Nag's Head handpumps",
        "The farmers' market on Great Knollys Street (first and third Saturday, 8:15am-noon)",
    ],
    "what_to_order": (
        "Start with the chicken katsu at Coconut for a feel of the town's "
        "pan-Asian range, work through a sourdough lunch at Shed, take the "
        "set lunch at London Street Brasserie for the riverside setting and "
        "modern-British cooking at a sensible price, and end the day at the "
        "Nag's Head with a half of whatever the chalk board says was just "
        "tapped — the rotating cask list is the whole point."
    ),
    "glance": [
        ("Best for a quick bite", "Shed — sourdough sandwiches made to order in an old forge, weekdays only"),
        ("Best for an occasion", "London Street Brasserie — 25 years beside the Kennet, Michelin-noted"),
        ("Best for atmosphere", "The Nag's Head — a free house, 12 handpumps and the town's best ale selection"),
    ],
    "faq": [
        (
            "What is the best independent restaurant in Reading?",
            "London Street Brasserie on London Street has been Reading's most "
            "consistently celebrated independent since it opened in 2000 in a "
            "Grade II-listed toll house beside the River Kennet. Chef-proprietor "
            "Paul Clerehugh has held Michelin recognition and a loyal local "
            "following for over two decades. Book ahead for weekends."
        ),
        (
            "Where should I eat near Reading station?",
            "The Nag's Head on Russell Street is a two-minute walk from the "
            "main entrance and is Reading's top-rated real-ale pub, with 12 "
            "rotating cask ales and 13 ciders. For food, Coconut Bar and "
            "Kitchen on St Mary's Butts is a five-minute walk and open seven days."
        ),
        (
            "Is there a good food market in Reading?",
            "Yes — the farmers' market at the old cattle market on Great Knollys "
            "Street runs on the first and third Saturday of each month from "
            "8:15am to noon. It focuses on local producers from Berkshire and "
            "the surrounding counties selling direct."
        ),
        (
            "Where is the best place to eat on the Oxford Road in Reading?",
            "The Oxford Road corridor is Reading's South Asian and global food "
            "street, with curry houses and Bangladeshi restaurants busy most "
            "evenings. For a step up, London Street Brasserie beside the Kennet "
            "is the more formal option nearby; Coconut Bar and Kitchen handles "
            "the pan-Asian brief in the town centre."
        ),
        (
            "What is Shed cafe in Reading known for?",
            "Shed at 8 Merchants Place has been making handmade sandwiches and "
            "sourdough toasties since 2012 in an old forge with exposed brick. "
            "It is open Monday to Friday from 8am and Saturday from 10am, "
            "with food until 3pm — a daytime-only cafe with a strong local following."
        ),
        (
            "Does Reading have any Michelin-starred restaurants?",
            "Reading does not currently have any Michelin-starred restaurants, "
            "but London Street Brasserie has held Michelin recognition across "
            "its 25-year history and is the town's most-awarded independent "
            "dining room. For a Michelin star in the wider region, nearby "
            "Bray holds several in a small village within 20 minutes."
        ),
    ],
}
