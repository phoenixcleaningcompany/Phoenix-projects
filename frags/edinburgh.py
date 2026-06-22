TOWNS = {}

# --------------------------------------------------------------------------
# EDINBURGH — web-researched June 2026
# --------------------------------------------------------------------------
TOWNS["edinburgh"] = {
    "region": "Scotland",
    "population": "530K",
    "nearby": ["Livingston", "Dunfermline", "Musselburgh"],
    "meta_title": "Best Places to Eat in Edinburgh: Local Food Guide",
    "meta_description": (
        "Edinburgh: 1979 halal takeaway, pioneering speciality roaster, "
        "Michelin-starred tasting menu, and a 1747 Leith real-ale pub. "
        "Read the guide."
    ),
    "trust_strip": (
        "From a legendary late-night halal counter to Scotland's oldest "
        "speciality roastery, Edinburgh's independent food scene rewards "
        "every mood and budget"
    ),
    "snapshot": (
        "For a fast answer: Kebab Mahal on Nicolson Square for a tandoori "
        "kebab that has fed the Old Town since 1979, Artisan Roast on "
        "Broughton Street for Scotland's pioneering speciality roast, "
        "Condita on Salisbury Place for a one-Michelin-star surprise tasting "
        "menu built on Scottish produce, and the Malt and Hops on the Shore "
        "in Leith for eight real ales in a bar dating from 1747. Four moods, "
        "one remarkable capital."
    ),
    "stats": [
        ("530K", "City population (approx)"),
        ("1747", "Year the Malt and Hops first poured a pint"),
        ("2007", "Year Artisan Roast opened Scotland's first speciality cafe"),
        ("4", "Hand-picked independents"),
    ],
    "pivot_variant": "high-volume",
    "pivot_local_hook": (
        "Edinburgh's kitchens run a heavy cycle: high-volume tandoors and "
        "charcoal grills in the Old Town, festival-season fryers working "
        "around the clock in August, and the waterfront restaurants of Leith "
        "pushing coastal grease loads through their canopies service after "
        "service."
    ),
    "venues": [
        {
            "type": "Takeaway",
            "name": "Kebab Mahal",
            "area": "7 Nicolson Square, Southside (edge of the Old Town)",
            "cuisine": "Halal Indian, tandoori kebabs",
            "body": (
                "Kebab Mahal has been feeding the Southside since 1979, making it one "
                "of Edinburgh's oldest continuously trading South Asian kitchens. The "
                "no-frills halal cafe-takeaway on Nicolson Square is a short walk from "
                "the Royal Mile and has built a devoted following among students, "
                "locals and late-night revellers across nearly five decades. The menu "
                "keeps it simple and keeps it honest: sizzling tandoori kebabs, "
                "biryanis, bhuna and kofte, all halal, all priced to feed you for "
                "under a fiver. The chicken and lamb sheesh kebabs are the standout "
                "order, pulled from the tandoor and wrapped with freshly made naan. "
                "Open daily until midnight, and until 2am on Fridays and Saturdays."
            ),
            "known_for": "Tandoori kebabs and biryani served since 1979, open until 2am",
            "good_for": "A cheap, honest, late-night meal in the Old Town",
            "source_url": "https://www.kebabmahaledinburgh.co.uk/",
            "verified": "2026-06-22",
        },
        {
            "type": "Cafe",
            "name": "Artisan Roast",
            "area": "57 Broughton Street, New Town",
            "cuisine": "Speciality coffee, homemade cakes",
            "body": (
                "When Artisan Roast opened on Broughton Street in summer 2007, it was "
                "the first speciality coffee roaster in Scotland, and the cluttered, "
                "bohemian room it occupies remains one of the most characterful cafes "
                "in the country. Coffee sacks hang on the walls, bulbs dangle at "
                "table height using cafetieres as lampshades, and the roasting is "
                "done properly: single-origin beans sourced with care and served as "
                "espresso, filter or cold brew. In 2012 Artisan Roast became the "
                "first coffee company ever to win the Glenfiddich Spirit of Scotland "
                "Award. The company now has four shops across the city and roasts in "
                "Peffermill, but the Broughton Street original is where it all began, "
                "and where the spirit of that first cup still lives."
            ),
            "known_for": "Scotland's first speciality roaster, open since 2007 on Broughton Street",
            "good_for": "A serious coffee in Edinburgh's most characterful independent cafe",
            "source_url": "https://artisanroast.co.uk/pages/broughtonstreet-cafe",
            "verified": "2026-06-22",
        },
        {
            "type": "Restaurant",
            "name": "Condita",
            "area": "15 Salisbury Place, Southside",
            "cuisine": "Michelin-starred Scottish tasting menu",
            "body": (
                "Tucked quietly on the Southside, Condita is one of Edinburgh's most "
                "distinctive dining rooms: a small, owner-run shop conversion with "
                "twelve seats at candle-lit Scottish mid-century modern tables, and a "
                "single surprise tasting menu that changes with the season. Chef Tyler "
                "King builds every course around the larder of Scotland: fish from "
                "Hebrides, Orkney, Shetland and the east coast; meat and game from "
                "Fife and the Highlands; produce from the restaurant's own garden and "
                "allotment. The result has held one Michelin star for six consecutive "
                "years, retained in the 2026 Guide. Dinner runs to around two and a "
                "half hours and costs around 160 pounds; bookings essential and "
                "typically taken weeks ahead. Open Tuesday to Saturday evenings only."
            ),
            "known_for": "One-Michelin-star surprise tasting menu using Scottish produce",
            "good_for": "An intimate, landmark special-occasion dinner on the south side",
            "source_url": "https://www.condita.co.uk/",
            "verified": "2026-06-22",
        },
        {
            "type": "Pub",
            "name": "The Malt and Hops",
            "area": "45 The Shore, Leith",
            "cuisine": "Real ale, classic pub food",
            "body": (
                "The Malt and Hops sits on the Shore at the heart of Leith's "
                "waterfront revival, in a building that dates from 1747 and was "
                "trading as the Drawbridge for most of the twentieth century. "
                "Renamed and relaunched in 1992, it is now one of the best real-ale "
                "pubs in Scotland: a CAMRA Good Beer Guide regular that pours eight "
                "handpulled ales at any one time, with more casks racked and ready "
                "behind the bar. The single room is wonderfully old-fashioned, with a "
                "real fire, pump clips from long-gone breweries hanging from the "
                "ceiling alongside hop bines renewed every harvest, and mirrors lining "
                "the walls. Pub food runs to haggis, neeps and tatties, steak pie and "
                "fish and chips. An authentic Leith local."
            ),
            "known_for": "Eight real ales, CAMRA Good Beer Guide, a bar dating from 1747",
            "good_for": "A pint of cask ale in an atmospheric Leith Shore pub",
            "source_url": "https://camra.org.uk/pubs/malt-hops-edinburgh-151306",
            "verified": "2026-06-22",
        },
    ],
    "food_scene": [
        (
            "Edinburgh's food map divides neatly between the Old Town's tourist-facing "
            "Royal Mile strip and the more characterful eating hidden a few streets "
            "away. Grassmarket hosts a Saturday farmers market with local producers, "
            "while Victoria Street and the Cowgate hold some of the city's best "
            "independent restaurants and wine bars tucked into medieval closes. The "
            "Southside, around Nicolson Square and Clerk Street, carries the everyday "
            "neighbourhood eating that feeds the university quarter, including the "
            "beloved Kebab Mahal."
        ),
        (
            "Leith is Edinburgh's most evolved food district: the former port neighbourhood "
            "has spent three decades building a serious restaurant and bar scene along "
            "the Shore and into the back streets, driven by the quality of its seafood "
            "access and a bohemian local culture. The Malt and Hops is one of its "
            "original anchors. Stockbridge, on the New Town edge, has a Sunday market "
            "and a strong run of independent cafes, delis and neighbourhood restaurants "
            "that make it the suburb Edinburghers are most likely to eat in on their "
            "day off."
        ),
        (
            "Beyond the familiar, Edinburgh has developed a serious fine-dining scene "
            "to sit alongside its street-food and pub culture. The 2026 Michelin Guide "
            "saw the city gain two new stars alongside Condita's sixth consecutive "
            "retention, reflecting a depth of talent that makes it one of the strongest "
            "restaurant cities in the UK outside London. The food ranges from the "
            "classic Scottish larder - haggis with neeps and tatties, Cullen skink, "
            "fresh Hebridean fish - to the adventurous cooking of a new generation of "
            "chef-owners working with that same Scottish produce."
        ),
    ],
    "visit": [
        (
            "The city's geography is manageable on foot. Kebab Mahal is a ten-minute "
            "walk south from Waverley station along South Bridge; Artisan Roast sits "
            "in the New Town a fifteen-minute walk north-east of the station via Broughton "
            "Street; and Condita is a twenty-minute walk south from the centre on "
            "Salisbury Place. Leith and the Malt and Hops are a short bus or taxi ride "
            "down Leith Walk, or a twenty-five-minute walk from Princes Street."
        ),
        (
            "Edinburgh rewards a logical order. Start the day with a flat white at "
            "Artisan Roast on Broughton Street, explore the New Town and Old Town, "
            "book Condita for the evening, and end in Leith for a pint at the Malt "
            "and Hops. Kebab Mahal is the answer to late nights and festival weekends: "
            "it trades until 2am on Fridays and Saturdays and has been doing so for "
            "nearly fifty years. Book Condita at least several weeks ahead."
        ),
    ],
    "checklist": [
        "Start at Artisan Roast on Broughton Street for Scotland's original speciality coffee",
        "Walk the Old Town and Grassmarket before doubling back south to Nicolson Square",
        "Book Condita weeks ahead for the surprise tasting menu - it sells out fast",
        "Take the bus or walk down Leith Walk to the Shore for a pint at the Malt and Hops",
        "Kebab Mahal is open until 2am on weekends - the definitive late-night stop",
    ],
    "what_to_order": (
        "Order with intent. At Kebab Mahal, the chicken or lamb sheesh kebab from "
        "the tandoor, wrapped in freshly made naan - they have been the signature for "
        "nearly fifty years. At Artisan Roast, ask what is on the rotating single-origin "
        "espresso, or take a filter and settle into the cluttered, characterful room. "
        "At Condita, there is no menu to choose from: surrender to the surprise, built "
        "around Scottish fish and game. At the Malt and Hops, ask what is on the eight "
        "handpulls and take whichever comes from a smaller Scottish or Lake District "
        "brewery, alongside a bowl of haggis, neeps and tatties."
    ),
    "glance": [
        ("Best for a quick bite", "Kebab Mahal, for a tandoori kebab that has served the Old Town since 1979"),
        ("Best for an occasion", "Condita, for a one-Michelin-star surprise tasting menu on the Southside"),
        ("Best for atmosphere", "The Malt and Hops, an 1747 real-ale pub on Leith Shore"),
    ],
    "faq": [
        (
            "Where can I get a good late-night meal in Edinburgh?",
            "Kebab Mahal on Nicolson Square has been serving halal tandoori kebabs and "
            "biryanis since 1979 and is open until midnight daily, and until 2am on "
            "Fridays and Saturdays. It is a short walk from the Royal Mile and one of "
            "Edinburgh's great budget institutions.",
        ),
        (
            "Which Edinburgh cafe has the best independent coffee?",
            "Artisan Roast on Broughton Street, Scotland's first speciality coffee "
            "roaster, opened in 2007 and won the Glenfiddich Spirit of Scotland Award "
            "in 2012. The Broughton Street original roasts single-origin beans on site "
            "and serves them in one of the city's most characterful cafe interiors.",
        ),
        (
            "Does Edinburgh have a Michelin-starred restaurant?",
            "Yes. Condita on Salisbury Place, an owner-run restaurant with twelve seats "
            "and a surprise tasting menu by chef Tyler King, has held one Michelin star "
            "for six consecutive years, retaining it in the 2026 Guide. It focuses on "
            "Scottish fish, meat and game and books up weeks in advance.",
        ),
        (
            "What is the best pub in Leith for real ale?",
            "The Malt and Hops at 45 The Shore, a CAMRA Good Beer Guide regular in a "
            "building dating from 1747, pours eight handpulled ales at any one time "
            "with more casks ready behind the bar. The single room has a real fire, "
            "historic pump clips and hop bines, and serves haggis and steak pie.",
        ),
        (
            "What food is Edinburgh most famous for?",
            "Scotland's national dish, haggis with neeps and tatties, is found across "
            "the city, alongside Cullen skink (smoked haddock soup), the Scotch pie, "
            "and exceptional fresh seafood from Hebridean and east-coast waters. "
            "Edinburgh's restaurant scene has grown beyond the traditional, with a "
            "new generation of chefs working the same Scottish larder in more "
            "adventurous ways.",
        ),
        (
            "Can you eat well in Edinburgh on a budget?",
            "Easily. Kebab Mahal on Nicolson Square has fed the Southside for nearly "
            "fifty years with halal tandoori meals under a fiver. Artisan Roast on "
            "Broughton Street serves serious speciality coffee without a premium price. "
            "The Malt and Hops in Leith is an honest pub with good real ale and "
            "pub-food classics at pub prices.",
        ),
    ],
}
