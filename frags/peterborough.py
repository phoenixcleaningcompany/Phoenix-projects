# Peterborough — web-researched 2026-06-22
# Four venues confirmed currently trading via live web checks.
# Sources recorded per venue below.

TOWNS = {}

TOWNS["peterborough"] = {
    "region": "Cambridgeshire",
    "population": "205K",
    "nearby": ["Spalding", "Stamford", "Corby"],
    "meta_title": "Best Places to Eat in Peterborough: Local Food Guide",
    "meta_description": (
        "Where to eat in Peterborough: a family Italian deli, a Great Taste Award "
        "cafe, a Michelin-listed village inn and a CAMRA Pub of the Year. "
        "Read the guide."
    ),
    "trust_strip": (
        "From a family-run Italian deli rooted in the city's brickyard heritage "
        "to a Michelin-listed village inn, Peterborough punches well above its size"
    ),
    "snapshot": (
        "For a fast answer: The Pasta Shop in Fletton for a plate of fresh Italian "
        "antipasti from the family deli that has served the city since 1992, The "
        "Coffee Hive on Fletton Avenue for Great Taste Award coffee and homemade "
        "bakes, The Chubby Castor in Castor village for Michelin-listed modern "
        "British cooking in a 400-year-old inn, and The Yard of Ale on Oundle Road "
        "for the CAMRA Pub of the Year and wood-fired pizza. Four moods, one "
        "cathedral city."
    ),
    "stats": [
        ("205K", "Population (approx)"),
        ("1950s", "Decade Italian workers arrived at the London Brick Company"),
        ("400 yrs", "Age of The Chubby Castor's village inn"),
        ("4", "Hand-picked independents"),
    ],
    "pivot_variant": "high-volume",
    "pivot_local_hook": (
        "Peterborough's cathedral-city kitchens serve a dense commuter and "
        "tourism crowd through long daily shifts, and the wood-fired pizza ovens "
        "and charcoal grills that draw those crowds push a heavy load of "
        "grease-laden vapour into canopies every service."
    ),
    "venues": [
        {
            "type": "Takeaway/Casual",
            "name": "The Pasta Shop",
            "area": "15 Queens Walk, Fletton",
            "cuisine": "Italian deli, antipasti, fresh pasta",
            "body": (
                "The Pasta Shop is the living legacy of Peterborough's remarkable "
                "Italian community. In the 1950s, the London Brick Company recruited "
                "thousands of workers from Apulia and Campania, making Peterborough "
                "home to the third-largest Italian population in the UK. The Borrillo "
                "family, from southern Italy, opened this deli-cafe in Fletton in 1992, "
                "and Gino Borrillo still runs it today, returning to the family farm in "
                "Italy each year to source ingredients. The deli counter runs to fresh "
                "hams, salamis, aged cheeses and traditional antipasti, alongside fresh "
                "pasta, wines and store-cupboard essentials. Specials are cooked in "
                "the kitchen every day and sandwiches are made to order at the counter "
                "- a proper Italian lunch, served from 8am to 6pm, Monday to Saturday."
            ),
            "known_for": "Family-run Italian deli rooted in Peterborough's brickyard-era community",
            "good_for": "A deli lunch or Italian provisions with a real story behind them",
            "source_url": "https://www.tripadvisor.co.uk/Restaurant_Review-g187045-d4925494-Reviews-Pasta_Shop-Peterborough_Cambridgeshire_England.html",
            "verified": "2026-06-22",
        },
        {
            "type": "Cafe",
            "name": "The Coffee Hive",
            "area": "142 Fletton Avenue, Peterborough",
            "cuisine": "Speciality coffee, homemade bakes",
            "body": (
                "The Coffee Hive is a family-run neighbourhood cafe on Fletton Avenue "
                "with a strong local following and a community-first approach. The "
                "kitchen partners with Jute Coffee, whose beans carry a Great Taste "
                "Award, sourcing an organic blend of Brazilian and Nicaraguan beans "
                "for the espresso bar, and the result is serious coffee without the "
                "metropolitan attitude. Alongside the cups there are homemade bakes, "
                "plated breakfasts and lunches cooked fresh daily. The Hive doubles as "
                "a live-music venue on Friday evenings and hosts a regular quiz night, "
                "making it an anchor for the neighbourhood rather than just a coffee "
                "stop. A five-star food hygiene rating and an active events programme "
                "into 2026 confirm the doors are very much open."
            ),
            "known_for": "Great Taste Award Jute coffee and a genuine community hub",
            "good_for": "A quality flat white and homemade cake in a neighbourhood setting",
            "source_url": "https://welovepeterborough.co.uk/projects/the-coffee-hive/",
            "verified": "2026-06-22",
        },
        {
            "type": "Restaurant",
            "name": "The Chubby Castor",
            "area": "34 Peterborough Road, Castor (5 miles west of the city)",
            "cuisine": "Modern British, seasonal and local",
            "body": (
                "A 400-year-old village inn in the stone village of Castor, just "
                "five miles from Peterborough's cathedral, is not where you might "
                "expect to find the area's most celebrated table. But chef-patron "
                "Adebola Adeshina has turned the Fitzwilliam Arms into exactly that: "
                "a Michelin Guide-listed restaurant holding three AA Rosettes, with a "
                "chocolate-box exterior concealing a smart modern dining room. The "
                "cooking is seasonal modern British, built on local and regional "
                "produce with menus that change as the year turns. A blind menu at "
                "fifty pounds per person and an intimate dining room mean tables go "
                "quickly. Open Wednesday to Saturday for lunch and dinner and Sunday "
                "for lunch, with online bookings through the restaurant's own site."
            ),
            "known_for": "Michelin Guide-listed modern British cooking, three AA Rosettes",
            "good_for": "A serious occasion dinner in a beautiful village inn near the city",
            "source_url": "https://thechubbycastor.com/",
            "verified": "2026-06-22",
        },
        {
            "type": "Pub",
            "name": "The Yard of Ale",
            "area": "72 Oundle Road, Woodston",
            "cuisine": "Real ales, wood-fired pizza (seasonal)",
            "body": (
                "The Yard of Ale on Oundle Road won the Peterborough and District "
                "CAMRA Branch Pub of the Year for 2026 — the branch's overall top "
                "award. Angela and James Hopkin have run this 120-year-old pub, "
                "built on land that was once the stable yard of the nearby Palmerston "
                "Arms, since July 2017, when they refurbished it and gave it its "
                "current name. The beer offer runs to four changing ales alongside "
                "two regulars, including Digfield Chiffchaff from the local Digfield "
                "Ales in Northamptonshire. From April to October a wood-fired pizza "
                "oven fires up in the beer garden on weekend evenings, adding a food "
                "draw to complement the live music. A genuine local, independently "
                "run, with the CAMRA accolade to back it up."
            ),
            "known_for": "CAMRA Peterborough Pub of the Year 2026, local real ales and wood-fired pizza",
            "good_for": "A well-kept pint and a wood-fired pizza in a proper independent local",
            "source_url": "https://camra.org.uk/pubs/yard-of-ale-peterborough-157362",
            "verified": "2026-06-22",
        },
    ],
    "food_scene": [
        (
            "Peterborough's food map is shaped by its remarkable demographic history. "
            "When the London Brick Company recruited thousands of workers from Apulia "
            "and Campania in the 1950s, it planted one of Britain's largest Italian "
            "communities in the Fletton area south of the city, and the legacy runs "
            "through the food scene today: delis, cafes and Italian family restaurants "
            "have been part of the city's fabric for generations. Fletton's Queens Walk "
            "remains the heartland of that tradition."
        ),
        (
            "The city centre clusters around Cathedral Square and Bridge Street, where "
            "a busy market hall, Turkish and South Asian kitchens, and independent cafes "
            "serve the commuter and shopper crowds. Queensgate, the main shopping centre, "
            "anchors a ring of food operators, while Fletton Quays on the riverside "
            "development has added newer bars and cafes to the mix. The independent food "
            "scene has been growing alongside the chains, and the city market on Bridge "
            "Street brings street-food traders from Italian to Caribbean under one roof."
        ),
        (
            "Beyond the city itself, the countryside within a few miles holds some "
            "serious cooking: the stone villages of the Nene Valley, Castor among them, "
            "are home to destination-quality kitchens drawing on the local farms and "
            "rivers. Peterborough is one of England's best-connected cities by rail, "
            "and that access makes the whole area practical for food tourism, with the "
            "cathedral as the natural anchor for a day that moves between city and village."
        ),
    ],
    "visit": [
        (
            "The city centre is compact and walkable. Cathedral Square puts you a "
            "short walk from the Bridge Street market, the Queensgate complex and "
            "the older pub backstreets around North Street. Fletton, where The Pasta "
            "Shop and The Coffee Hive sit, is about a mile and a half south, a "
            "straightforward bus ride or a twenty-minute walk across the river. "
            "Castor village, for The Chubby Castor, is five miles to the west and "
            "most easily reached by car or taxi."
        ),
        (
            "Done as a day: a deli lunch at The Pasta Shop, coffee and a cake at "
            "The Coffee Hive, an evening at The Chubby Castor booked well in advance, "
            "and The Yard of Ale for a pint of Digfield ale on the way back. The "
            "rail connection to London St Pancras in under an hour makes Peterborough "
            "a practical food destination rather than just a stopping point."
        ),
    ],
    "checklist": [
        "Book The Chubby Castor well ahead; the dining room is small and fills quickly",
        "Visit The Pasta Shop on a weekday when the daily specials are freshest",
        "The Yard of Ale pizza oven runs April to October - time your visit accordingly",
        "The Coffee Hive does live music on Fridays - check the events calendar before you go",
        "Cathedral Square is the sensible starting point for the city-centre food loop",
    ],
    "what_to_order": (
        "Order with intent. At The Pasta Shop, take the daily special from the "
        "kitchen or build a plate from the deli counter - fresh bresaola, aged "
        "pecorino and a sandwich made to order. At The Coffee Hive, ask for the "
        "Jute espresso on its own or as a flat white, with one of the homemade "
        "bakes. At The Chubby Castor, trust the blind menu or let the seasonal "
        "carte guide you toward whatever the local farms are offering that week. "
        "At The Yard of Ale, a pint of Digfield Chiffchaff and a wood-fired pizza "
        "from the garden oven, from April onwards."
    ),
    "glance": [
        ("Best for a quick bite", "The Pasta Shop, for an Italian deli lunch in Fletton"),
        ("Best for an occasion", "The Chubby Castor, for Michelin-listed modern British in a village inn"),
        ("Best for atmosphere", "The Yard of Ale, CAMRA Pub of the Year 2026 with pizza in the garden"),
    ],
    "faq": [
        (
            "What is Peterborough known for in terms of food?",
            "Peterborough has a distinctive Italian food culture rooted in the 1950s "
            "arrival of thousands of workers from southern Italy recruited by the London "
            "Brick Company. The Fletton area still holds family-run Italian delis and "
            "cafes, alongside a diverse city-centre scene of Turkish, South Asian and "
            "independent British kitchens.",
        ),
        (
            "Does Peterborough have any Michelin Guide restaurants?",
            "Yes. The Chubby Castor in the village of Castor, five miles west of the "
            "city, is listed in the Michelin Guide and holds three AA Rosettes. Chef-"
            "patron Adebola Adeshina runs the kitchen from a 400-year-old village inn, "
            "open Wednesday to Sunday.",
        ),
        (
            "Where should I go for coffee in Peterborough?",
            "The Coffee Hive on Fletton Avenue is a family-run independent cafe serving "
            "Great Taste Award-winning Jute coffee alongside homemade food and bakes. "
            "It also runs Friday live-music evenings and a regular quiz night.",
        ),
        (
            "What is the best pub in Peterborough for real ale?",
            "The Yard of Ale on Oundle Road in Woodston won the Peterborough and "
            "District CAMRA Branch Pub of the Year for 2026. Run by Angela and James "
            "Hopkin since 2017, it serves four changing ales including Digfield "
            "Chiffchaff from local Digfield Ales, and fires up a wood-fired pizza oven "
            "in the garden from April to October.",
        ),
        (
            "Where can I get authentic Italian food in Peterborough?",
            "The Pasta Shop at 15 Queens Walk in Fletton has been run by the Borrillo "
            "family since 1992, sourcing ingredients from their family farm in southern "
            "Italy. The deli counter offers hams, salamis, cheeses and antipasti, and "
            "the kitchen cooks fresh daily specials with sandwiches made to order.",
        ),
        (
            "Is Peterborough easy to reach for a food day out?",
            "Yes. Peterborough has fast rail links to London St Pancras in under an "
            "hour, and to the East Midlands and Yorkshire. The city centre is walkable "
            "from the station, with Fletton a short bus ride south and Castor village "
            "five miles west by car or taxi.",
        ),
    ],
}
