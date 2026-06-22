TOWNS = {}

# --------------------------------------------------------------------------
# GLASGOW — web-researched 2026-06-22
# Four venues confirmed currently trading via live web checks.
# Nearby towns all verified against eat_towns.csv.
# --------------------------------------------------------------------------
TOWNS["glasgow"] = {
    "region": "Scotland",
    "population": "635K",
    "nearby": ["Paisley", "East Kilbride", "Motherwell"],
    "meta_title": "Best Places to Eat in Glasgow: Local Food Guide",
    "meta_description": (
        "Glasgow food picks: East End fish supper since 1939, West End "
        "roaster-cafe, Michelin-starred tasting menu and a Victorian gin "
        "palace bar. Read the guide."
    ),
    "trust_strip": (
        "From a Gallowgate fish supper to a Michelin-starred tasting menu, "
        "Glasgow is one of Britain's most exciting and rewarding cities to eat in"
    ),
    "snapshot": (
        "For a fast answer: Guido's Coronation Restaurant on the Gallowgate for "
        "a Scottish-Italian fish supper from the family that has run the fryer "
        "since 1939, Papercup Coffee on Great Western Road for house-roasted "
        "beans in the West End, Cail Bruich on Great Western Road for Lorna "
        "McNee's one-Michelin-star seasonal Scottish tasting menu, and The Horse "
        "Shoe Bar on Drury Street for a pint under the longest continuous bar in "
        "Britain. Four moods, one fearlessly hungry city."
    ),
    "stats": [
        ("635K", "Population (approx)"),
        ("1939", "Year Guido's Coronation first served a fish supper"),
        ("1884", "Year The Horse Shoe Bar was established"),
        ("4", "Hand-picked independents"),
    ],
    "pivot_variant": "high-volume",
    "pivot_local_hook": (
        "Glasgow's kitchens cook hard and fast: the high-temperature fryers of "
        "East End chippies, the tasting-menu pass of Michelin-starred dining "
        "rooms, and the charcoal grills of Finnieston's dense restaurant strip "
        "all push a heavy, sustained load of grease-laden vapour into their "
        "canopies through every service."
    ),
    "venues": [
        {
            "type": "Takeaway",
            "name": "Guido's Coronation Restaurant",
            "area": "55 Gallowgate, East End (under the railway arches)",
            "cuisine": "Scottish-Italian fish and chips",
            "body": (
                "Tucked beneath the old railway bridge at 55 Gallowgate in "
                "Glasgow's East End, Guido's Coronation Restaurant has been "
                "feeding the city since 1939. It was founded by the Corvi family, "
                "Italian immigrants who brought their frying tradition west from "
                "Bo'ness to Glasgow, and the business has passed through three "
                "generations — from grandfather to Guido, and now to Cristoforo "
                "Corvi, who runs the fryer today. The result is a masterclass in "
                "the Scottish-Italian chippy: haddock in a light, properly made "
                "batter, thick chips, and the curry sauce that regulars swear by. "
                "Haggis with chips sits alongside the classics, and a sit-down "
                "breakfast pulls in locals from early morning. Prices are modest "
                "and the queue on a busy day tells you everything you need to know."
            ),
            "known_for": "Three-generation Italian-Scottish fish supper since 1939",
            "good_for": "A legendary East End fish supper or a no-nonsense breakfast",
            "source_url": "https://guidoscoronationrestaurant.shop/",
            "verified": "2026-06-22",
        },
        {
            "type": "Cafe",
            "name": "Papercup Coffee Company",
            "area": "603 Great Western Road, Hillhead, West End",
            "cuisine": "Speciality coffee and brunch",
            "body": (
                "Founded in 2013 by Graeme Crawford, Papercup Coffee Company is "
                "one of the pioneers of Glasgow's speciality coffee scene, a "
                "compact, character-filled cafe on Great Western Road in the West "
                "End. The roastery sits at Arch 17 on Eastvale Place, just across "
                "the city, and the freshly roasted beans make the short journey "
                "to the cafe counter daily. Everything is house-roasted: the "
                "espresso rotates single origins, and the batch filter is always "
                "worth asking about. A varied brunch menu and homemade cakes have "
                "built a following among Hillhead residents and university staff "
                "alike. The room is unhurried and friendly, open seven days from "
                "nine in the morning — the kind of place a neighbourhood returns "
                "to every week."
            ),
            "known_for": "House-roasted speciality beans and West End brunch since 2013",
            "good_for": "A serious coffee and brunch on Great Western Road",
            "source_url": "https://www.papercupcoffee.co.uk/pages/cafe-great-western-road-glasgow",
            "verified": "2026-06-22",
        },
        {
            "type": "Restaurant",
            "name": "Cail Bruich",
            "area": "725 Great Western Road, West End",
            "cuisine": "Modern Scottish fine dining",
            "body": (
                "Opened in 2008 by siblings Chris and Paul Charalambous, Cail "
                "Bruich takes its name from the Gaelic phrase meaning 'to eat "
                "well', and the kitchen has followed through on that promise ever "
                "since. Head chef Lorna McNee, who joined in 2020 having won "
                "BBC Great British Menu's Champion of Champions, runs a "
                "tasting menu rooted in the seasons and the land: Scottish "
                "produce sourced from named farms and coastal suppliers, presented "
                "with the precision and restraint that earned a Michelin Star in "
                "2021 — still current in the 2026 guide. McNee is Scotland's only "
                "female Michelin-starred chef, and Cail Bruich holds three AA "
                "Rosettes alongside its star. The room on Great Western Road is "
                "relaxed rather than formal; the cooking is the event. Book well "
                "in advance."
            ),
            "known_for": "Scotland's only female Michelin-starred chef, seasonal Scottish tasting menu",
            "good_for": "A landmark special-occasion dinner in the West End",
            "source_url": "https://www.cailbruich.co.uk/",
            "verified": "2026-06-22",
        },
        {
            "type": "Pub",
            "name": "The Horse Shoe Bar",
            "area": "17-19 Drury Street, city centre",
            "cuisine": "Traditional pub food",
            "body": (
                "Step inside 17 Drury Street and the bar does the talking. "
                "Established in 1884 by John Scouller and extended in the early "
                "1900s under John Young Whyte, The Horse Shoe Bar has the longest "
                "continuous bar counter in Britain: 104 feet and three inches of "
                "polished wood sweeping in a horseshoe arc around the island. The "
                "Victorian interior is Category A listed by Historic Environment "
                "Scotland and recognised by CAMRA as having a nationally "
                "important pub interior — ornate tilework, carved gantry, high "
                "mirrored ceilings and period fittings that have changed little in "
                "a century. The pub serves real ale alongside a generous kitchen "
                "menu, runs karaoke seven nights a week, and pours a Guinness "
                "that draws visitors from across the city. It sits two minutes "
                "from Central Station and has been doing so since the Victorian age."
            ),
            "known_for": "Britain's longest continuous bar, Victorian gin-palace interior since 1884",
            "good_for": "A pint in a Category A listed architectural gem near Central Station",
            "source_url": "https://www.yelp.co.uk/biz/horseshoe-bar-glasgow",
            "verified": "2026-06-22",
        },
    ],
    "food_scene": [
        (
            "Glasgow's food map is one of the most layered in Britain. The East End "
            "around the Gallowgate and the Barras market carries the city's "
            "working-class Italian-Scottish cooking tradition, the one that gave "
            "Glasgow its fish suppers, its morning rolls and its appetite for "
            "no-nonsense eating at any hour. Guido's Coronation Restaurant, tucked "
            "under the railway arches since 1939, is the most storied survivor of "
            "that lineage."
        ),
        (
            "A mile or two west, Finnieston has become the most talked-about "
            "restaurant strip in Scotland: a post-industrial stretch of Argyle "
            "Street that transformed in little over a decade into a density of "
            "independent dining rooms, craft bars and seafood counters that rivals "
            "anything in Edinburgh or London. The West End around Great Western "
            "Road and Gibson Street operates at a quieter pitch but with serious "
            "depth, home to Cail Bruich's Michelin-starred kitchen and a clutch "
            "of independent roaster-cafes led by Papercup Coffee."
        ),
        (
            "Downtown, the Merchant City's repurposed Georgian warehouses and the "
            "streets around Central Station hold the city's grand Victorian pub "
            "interiors, with The Horse Shoe Bar at their head. Glasgow also does "
            "haggis better than almost anywhere: served straight with neeps and "
            "tatties, folded into pakora, or piled into a morning roll, it appears "
            "on menus from the simplest cafe to the Michelin table. The city's "
            "cooking is curious, confident and unafraid of scale."
        ),
    ],
    "visit": [
        (
            "The geography rewards a day split between east and west. The "
            "Gallowgate and the Horse Shoe Bar are both close to Glasgow Central "
            "and Queen Street stations, keeping transport easy. The West End — "
            "Papercup and Cail Bruich on Great Western Road — is a twenty-minute "
            "walk or a short taxi from the city centre, with Byres Road and "
            "Ashton Lane nearby for an afternoon wander."
        ),
        (
            "Done as a day: a coffee at Papercup on Great Western Road to start, "
            "lunch at the Horse Shoe Bar under those Victorian arches, a fish "
            "supper at Guido's in the Gallowgate after an afternoon at the Barras "
            "market, and Cail Bruich saved for the evening you want to mark. Book "
            "Cail Bruich well in advance; a tasting menu here is not a table you "
            "walk into."
        ),
    ],
    "checklist": [
        "Book Cail Bruich weeks ahead — the Michelin-starred tasting menu fills quickly",
        "Visit Guido's Coronation mid-morning to avoid the lunchtime chippy queue",
        "Go to the Horse Shoe Bar off-peak to take in the bar and tilework properly",
        "Papercup opens from nine — it is the West End's best coffee before a walk along the Kelvin",
        "Use Glasgow Central or Queen Street stations; the Horse Shoe Bar is two minutes from Central",
    ],
    "what_to_order": (
        "Order with intent. At Guido's Coronation, a haddock supper with the "
        "house curry sauce, or haggis with chips and a mug of tea. At Papercup, "
        "ask which single origin is on the espresso that week and try a slice of "
        "the homemade cake. At Cail Bruich, book the full tasting menu and follow "
        "Lorna McNee's lead on the wine pairing — the sourcing is half the story. "
        "At the Horse Shoe Bar, a proper pint of Guinness or cask ale, taken "
        "slowly at the bar so you can look at the gantry."
    ),
    "glance": [
        ("Best for a quick bite", "Guido's Coronation, for a 1939 Italian-Scottish fish supper on the Gallowgate"),
        ("Best for an occasion", "Cail Bruich, for Scotland's only female Michelin-starred chef on Great Western Road"),
        ("Best for atmosphere", "The Horse Shoe Bar's Category A listed Victorian interior and 104-foot bar"),
    ],
    "faq": [
        (
            "Where can I get the best fish and chips in Glasgow?",
            "Guido's Coronation Restaurant at 55 Gallowgate in the East End has been "
            "run by the Italian-Scottish Corvi family since 1939, serving haddock "
            "suppers, haggis and chips, and a house curry sauce under the old "
            "railway arches. It is one of the city's most loved and longest-running "
            "chippies."
        ),
        (
            "Which Glasgow restaurant has a Michelin star?",
            "Cail Bruich on Great Western Road in the West End holds one Michelin "
            "Star (awarded 2021, retained in the 2026 guide) and three AA Rosettes. "
            "Head chef Lorna McNee is Scotland's only female Michelin-starred chef, "
            "and the menu is a seasonal Scottish tasting menu built around named "
            "local producers."
        ),
        (
            "Where is the best independent coffee in Glasgow?",
            "Papercup Coffee Company at 603 Great Western Road in the West End is "
            "one of the city's pioneering speciality roaster-cafes, founded in 2013. "
            "Beans are roasted at their Eastvale Place roastery and served as "
            "rotating single-origin espresso and filter, with a brunch menu and "
            "homemade cakes."
        ),
        (
            "Which Glasgow pub has the longest bar?",
            "The Horse Shoe Bar on Drury Street in the city centre, established in "
            "1884, holds the record for the longest continuous bar counter in "
            "Britain at 104 feet and three inches. The Category A listed Victorian "
            "interior is recognised by CAMRA as nationally important."
        ),
        (
            "What is the local food to try in Glasgow?",
            "Haggis is the city's signature, served traditionally with neeps and "
            "tatties or inventively as haggis pakora in Glasgow's South Asian-"
            "influenced restaurants. The Scottish-Italian fish supper is the other "
            "great Glasgow tradition, best experienced at a long-running independent "
            "chippy like Guido's Coronation on the Gallowgate."
        ),
        (
            "Can you do a Glasgow food day on foot and public transport?",
            "Easily. The Horse Shoe Bar and Guido's Coronation Restaurant are both "
            "close to Glasgow Central and Queen Street stations. Papercup Coffee "
            "and Cail Bruich on Great Western Road are a short taxi or 20-minute "
            "walk into the West End, served by frequent buses on Byres Road."
        ),
    ],
}
