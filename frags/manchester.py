TOWNS = {}

# --------------------------------------------------------------------------
# MANCHESTER — web-researched 2026-06-22
# Four venues confirmed currently trading via live web search/review platforms.
# --------------------------------------------------------------------------
TOWNS["manchester"] = {
    "region": "Greater Manchester",
    "population": "555,000",
    "nearby": ["Salford", "Stockport", "Oldham"],
    "meta_title": "Best Places to Eat in Manchester: Local Food Guide",
    "meta_description": (
        "Manchester food guide: Bundobust for Gujarati street food, Pollen Bakery for "
        "sourdough, Mughli on the Curry Mile, and the Marble Arch pub. Read the guide."
    ),
    "trust_strip": (
        "From the Northern Quarter to the Curry Mile, Manchester's independent "
        "food scene is among the most diverse and exciting outside London"
    ),
    "snapshot": (
        "For a fast answer: Bundobust on Piccadilly for Gujarati street food and "
        "craft beer brewed on site, Pollen Bakery at Cotton Field Wharf in Ancoats "
        "for sourdough and cruffins that have queued the street since 2016, Mughli "
        "on the Curry Mile for charcoal-pit Indian since 1991, and The Marble Arch "
        "on Rochdale Road for a pint under one of the finest tiled Victorian pub "
        "interiors in the country. Four moods, one brilliant northern city."
    ),
    "stats": [
        ("555K", "City population (approx)"),
        ("1991", "Year Mughli opened on the Curry Mile"),
        ("Curry Mile", "Europe's densest South Asian restaurant strip"),
        ("4", "Hand-picked independents"),
    ],
    "pivot_variant": "high-volume",
    "pivot_local_hook": (
        "Manchester's kitchens run around the clock: the Curry Mile's charcoal pits "
        "and tandoors fire through late-night service, Northern Quarter bars keep "
        "fryers going past midnight, and the city's high-volume independent scene "
        "pushes a heavy grease load through canopies every single day."
    ),
    "venues": [
        {
            "type": "Takeaway/Casual",
            "name": "Bundobust",
            "area": "61 Piccadilly, city centre",
            "cuisine": "Gujarati street food and craft beer",
            "body": (
                "Bundobust arrived in Manchester in 2016, a year after its Leeds launch, "
                "and established itself in a high-ceilinged basement off Piccadilly with "
                "long communal tables, no bookings and twelve taps pouring its own-brewed "
                "craft beer. The concept came from Mayur Patel, whose family runs the "
                "acclaimed Bradford restaurant Prashad, and Marko Husak, a craft beer "
                "specialist: the result is all-vegetarian Gujarati street food — okra fries, "
                "bhel puri, dahi puri, spinach kofta — designed for sharing alongside "
                "Bundobust Brewery lager, IPA and seasonal specials. It is listed in the "
                "Observer Food Monthly OFM 50 and has won Best Innovation at the Casual "
                "Dining Awards. The Brewery taproom on Oxford Street opened in 2021. Open "
                "daily from midday with a two-dish lunch deal until 4pm."
            ),
            "known_for": "Gujarati street food plates and own-brewed craft beer, no bookings",
            "good_for": "A casual, communal, all-vegetarian feast with great beer",
            "source_url": "https://bundobust.com/locations/manchester/",
            "verified": "2026-06-22",
        },
        {
            "type": "Cafe",
            "name": "Pollen Bakery",
            "area": "Cotton Field Wharf, 8 New Union Street, Ancoats",
            "cuisine": "Artisan sourdough, viennoiserie and speciality coffee",
            "body": (
                "Hannah Calvert and Chris Kelly started baking sourdough in their home "
                "kitchen in 2011, launching Pollen commercially from a railway arch behind "
                "Piccadilly Station in 2016. The queues came quickly. They moved to a "
                "light-filled waterside site at Cotton Field Wharf in Ancoats in 2018, "
                "facing New Islington Marina, and added a second cafe at Kampus. Pollen's "
                "sourdough loaves take 28 hours to produce; its cruffins — a croissant "
                "dough baked in a muffin tin — became a Manchester cult object. The Good "
                "Food Guide rates both cafe sites and notes the bakery has established "
                "'cult status in Manchester for its quality viennoiserie and sourdough'. "
                "Open Wednesday to Sunday, with counter seats inside and a terrace beside "
                "the marina."
            ),
            "known_for": "28-hour sourdough loaves and cruffins with Good Food Guide recognition",
            "good_for": "A serious breakfast or mid-morning stop with exceptional pastries",
            "source_url": "https://pollenbakery.com/",
            "verified": "2026-06-22",
        },
        {
            "type": "Restaurant",
            "name": "Mughli Charcoal Pit",
            "area": "30 Wilmslow Road, Rusholme (the Curry Mile)",
            "cuisine": "Indian street food and charcoal-pit grills",
            "body": (
                "Mughli opened on the Curry Mile in 1991, founded by the late Mohammad "
                "Arshad — known to regulars as 'Uncle Peter' — and remains a family-run "
                "restaurant today. While many of its neighbours lean hard into tradition, "
                "Mughli has carved out its own identity: an 'angithi' charcoal pit at "
                "the centre of the kitchen produces tandoori chicken, flame-licked lamb "
                "chops, and punchy prawns with a genuine smoky intensity, alongside "
                "slow-cooked curries, street-food snacks and bold cocktails. Ask Mancunians "
                "for the best butter chicken in the city and many will point to Rusholme. "
                "It opens evenings only (Monday to Saturday from 5pm, Sunday from 2pm) "
                "and takes bookings for the evening sittings through till midnight."
            ),
            "known_for": "Charcoal-pit grills and reimagined curries on the Curry Mile since 1991",
            "good_for": "A special Curry Mile dinner with real smoky depth",
            "source_url": "https://www.mughli.com/",
            "verified": "2026-06-22",
        },
        {
            "type": "Pub",
            "name": "The Marble Arch",
            "area": "73 Rochdale Road, Ancoats/Angel Meadow",
            "cuisine": "Pub food, cask ale and craft beer",
            "body": (
                "Built in 1888 by architects Darbyshire and Smith as a showhouse for "
                "McKenna's Brewery, the Marble Arch is one of the most extraordinary pub "
                "interiors in England: a mosaic-tiled floor that slopes unmistakably "
                "toward the bar, glazed ceramic walls, a barrel-vaulted ceiling of "
                "decorated tile that was hidden behind plasterboard in 1954 and restored "
                "in the 1980s, and a long curved counter beneath it all. It is Grade II "
                "listed and holds an interior of outstanding national historic importance "
                "per CAMRA, appearing in the Good Beer Guide for over 25 consecutive years. "
                "Marble Brewery, founded at the back of the building in 1997 and now based "
                "in Salford, keeps the handpulls supplied with Manchester Bitter, Pint "
                "golden ale and Stout, alongside guest casks. Free live music every Sunday."
            ),
            "known_for": "A Grade II-listed 1888 interior of tiled perfection and Marble Brewery cask ale",
            "good_for": "A pint of Manchester Bitter in one of the country's great pub rooms",
            "source_url": "https://marblebeers.com/the-marble-arch/",
            "verified": "2026-06-22",
        },
    ],
    "food_scene": [
        (
            "Manchester's food geography runs from the city centre outward in all directions. "
            "The Northern Quarter, bordered by Piccadilly and Shudehill, is the hub of "
            "independent cafes, brunch spots and neighbourhood restaurants, and neighbouring "
            "Ancoats — once a Victorian industrial district and now one of the UK's most "
            "exciting dining neighbourhoods — adds Michelin-recognised restaurants, artisan "
            "bakeries and canal-side cafes around Cutting Room Square and New Islington Marina."
        ),
        (
            "Two miles south along Wilmslow Road lies Rusholme, home to the Curry Mile: "
            "the densest concentration of South Asian restaurants in Europe, a strip of neon "
            "signs and aromatic smoke serving Pakistani karahi, Mughlai-style grills, Middle "
            "Eastern shawarma and Bangladeshi curries from early evening until well past "
            "midnight. Manchester's Chinatown, a short walk from Piccadilly Gardens, adds "
            "a compact but long-established cluster of Cantonese, Vietnamese and Thai kitchens."
        ),
        (
            "The city holds a serious fine-dining tier — Mana in Ancoats holds a Michelin "
            "star, and Erst on Blossom Street in Ancoats carries a Bib Gourmand — but what "
            "makes Manchester distinctive is the depth below that level: independent breweries, "
            "Gujarati street-food bars, a bakery scene anchored by Pollen, and a Curry Mile "
            "that has fed the city since the 1950s. A Manchester eating day can move from "
            "a cruffin at a waterside cafe to a charcoal-pit curry without repeating a flavour."
        ),
    ],
    "visit": [
        (
            "The geography is manageable. Bundobust and the city-centre pubs sit around "
            "Piccadilly, while Ancoats — home to Pollen Bakery and a cluster of restaurants "
            "on Blossom Street — is a fifteen-minute walk east along Great Ancoats Street. "
            "The Marble Arch is a short walk north along Rochdale Road. All of this is linked "
            "by the Metrolink tram network and easy walking. Rusholme's Curry Mile is two "
            "miles south: take a bus from Piccadilly Gardens or a short taxi ride."
        ),
        (
            "The natural day runs: a sourdough breakfast at Pollen Bakery beside the marina, "
            "a wander through the Northern Quarter for coffee, Bundobust for lunch with a "
            "Marble Brewery pint, and an evening on the Curry Mile at Mughli, booking ahead "
            "for their late sittings. Pollen keeps weekday hours from Wednesday and closes "
            "at 4pm, so plan the bakery stop for the morning."
        ),
    ],
    "checklist": [
        "Arrive at Pollen Bakery on a weekday morning before the cruffins sell out",
        "Book Mughli for an evening sitting — tables through to midnight, great cocktails too",
        "Head to Bundobust for lunch with no booking; go early to beat the queue",
        "Walk Rochdale Road for The Marble Arch; look up at the tiled ceiling immediately",
        "Use the Metrolink tram or bus for Rusholme — the Curry Mile is two miles south",
    ],
    "what_to_order": (
        "Order with intent. At Bundobust, build a spread: okra fries, bhel puri and a dahi "
        "puri to start, then a kofta or tikka with a Bundobust lager. At Pollen, a cruffin "
        "or croissant while they last, and a sourdough loaf to take home. At Mughli, lead "
        "with the charcoal-pit lamb chops or seekh kebabs from the angithi, then the butter "
        "chicken or a slow karahi. At The Marble Arch, a pint of Manchester Bitter on cask, "
        "taken slowly while you read every tile on the ceiling."
    ),
    "glance": [
        ("Best for a quick bite", "Bundobust, for Gujarati plates and craft beer off Piccadilly"),
        ("Best for an occasion", "Mughli Charcoal Pit, for a long Curry Mile dinner with cocktails"),
        ("Best for atmosphere", "The Marble Arch's Grade II-listed 1888 tiled interior"),
    ],
    "faq": [
        (
            "Where is the best place to eat on Manchester's Curry Mile?",
            "Mughli Charcoal Pit at 30 Wilmslow Road, Rusholme, is the Curry Mile's standout "
            "independent: open since 1991 and still family-run, it centres its kitchen on a "
            "charcoal angithi pit for grills and tandoori, alongside a full curry menu. Book "
            "ahead for evenings; it opens Monday to Saturday from 5pm, Sunday from 2pm."
        ),
        (
            "What is Bundobust and is it suitable for vegetarians?",
            "Bundobust at 61 Piccadilly is an all-vegetarian Gujarati street food restaurant "
            "and craft beer bar. Founded in Leeds in 2014, it opened in Manchester in 2016. "
            "The menu includes okra fries, bhel puri, dahi puri and kofta, designed for "
            "sharing, with beers brewed at the Bundobust Brewery on Oxford Street. "
            "Open daily from midday, no bookings taken."
        ),
        (
            "Which is Manchester's best independent bakery?",
            "Pollen Bakery, at Cotton Field Wharf in Ancoats, is widely regarded as "
            "Manchester's finest artisan bakery. Founded by Hannah Calvert and Chris Kelly "
            "in 2016, it was named by the Good Food Guide as one of the best bakeries in "
            "Britain, with 28-hour sourdough loaves and cruffins that became a city-wide "
            "cult. The waterside Ancoats cafe is open Wednesday to Sunday."
        ),
        (
            "What makes The Marble Arch pub special?",
            "The Marble Arch at 73 Rochdale Road, built in 1888, has one of the most "
            "remarkable pub interiors in England: a mosaic-tiled sloping floor, glazed "
            "ceramic walls and a barrel-vaulted tiled ceiling restored in the 1980s. It "
            "is Grade II listed, holds a CAMRA interior of outstanding national historic "
            "importance, and has appeared in the Good Beer Guide for over 25 consecutive "
            "years. Marble Brewery was founded at the back of the building in 1997."
        ),
        (
            "Which areas of Manchester are best for independent restaurants?",
            "The Northern Quarter and neighbouring Ancoats are the city's strongest "
            "independent dining neighbourhoods, with bakeries, brunch spots, neighbourhood "
            "restaurants and Michelin-recognised venues clustered within a walkable area. "
            "Rusholme's Curry Mile, two miles south along Wilmslow Road, is the place "
            "for South Asian cooking, and Chinatown sits close to Piccadilly Gardens."
        ),
        (
            "Are any of the Manchester picks Michelin-recognised?",
            "Bundobust Manchester Piccadilly has received Michelin recognition as part "
            "of the guide's street food recommendations. Nearby Ancoats also holds two "
            "Michelin-recognised restaurants in the guide: Mana (one star) and Erst "
            "(Bib Gourmand), reflecting the neighbourhood's rise as a serious dining "
            "destination. All four picks in this guide are confirmed currently trading."
        ),
    ],
}
