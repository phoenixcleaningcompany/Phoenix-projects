# Hull — web-researched 2026-06-22
# Four venues confirmed currently trading via live web checks.
# Sources recorded per venue below.

TOWNS = {}

TOWNS["hull"] = {
    "region": "East Yorkshire",
    "population": "260K",
    "nearby": ["Beverley", "Cottingham", "Hessle"],
    "meta_title": "Best Places to Eat in Hull: Local Food Guide",
    "meta_description": (
        "Where to eat in Hull: an 1888 chippy for the Hull pattie, "
        "a Fruit Market cafe, a Michelin Guide restaurant and the "
        "oldest pub in the city. Read the guide."
    ),
    "trust_strip": (
        "From an 1888 pattie-and-chip shop on Trinity House Lane to Hull's "
        "first Michelin Guide entry in years, the city eats better than its "
        "reputation suggests"
    ),
    "snapshot": (
        "For a fast answer: Bob Carvers on Trinity House Lane for the "
        "Hull pattie and proper fish and chips since 1888, Thieving "
        "Harry's on Humber Street for a brunch in a converted Fruit Market "
        "warehouse overlooking the marina, Hearth on King Street for the "
        "Michelin Guide bakery and sharing-plate restaurant in the Old "
        "Town, and Ye Olde Black Boy on High Street for a pint in "
        "Hull's oldest pub with a CAMRA-listed historic interior. Four "
        "moods, one walkable Old Town."
    ),
    "stats": [
        ("260K", "City population (approx)"),
        ("1888", "Year Bob Carvers first traded"),
        ("1729", "Licensed date of Hull's oldest pub"),
        ("4", "Hand-picked independents"),
    ],
    "pivot_variant": "coastal",
    "pivot_local_hook": (
        "Hull's kitchens carry a coastal load: a working-port fryer runs "
        "hot oil through long service hours, and the fish-and-chip houses "
        "along Hessle Road and the Old Town push dense grease-laden vapour "
        "into their canopies every day the trawlers land."
    ),
    "venues": [
        {
            "type": "Chippy",
            "name": "Bob Carvers",
            "area": "9 Trinity House Lane, Old Town",
            "cuisine": "Fish and chips, Hull pattie",
            "body": (
                "Bob Carver started selling fish from a canvas stall in Hull's "
                "open-air market in 1888, and the family business that grew from "
                "that stall is still feeding the city from Trinity House Lane in "
                "the Old Town. The order to make is the Hull pattie: mashed "
                "potato bound with sage and onion, coated in breadcrumbs and "
                "deep-fried, served alongside proper fish and chips from a busy "
                "counter. Mint sauce and vinegar-soaked fresh onions sit on the "
                "counter as the traditional local accompaniments, and a shake of "
                "chip spice - the seasoned salt introduced to Hull in 1979 and "
                "now inseparable from the city's chippy tradition - is the final "
                "local touch. A food hygiene inspection in January 2026 confirms "
                "the place is still running."
            ),
            "known_for": "The Hull pattie and chip spice since 1888",
            "good_for": "The authentic Hull chippy experience in the Old Town",
            "source_url": "https://ratings.food.gov.uk/business/192194",
            "verified": "2026-06-22",
        },
        {
            "type": "Cafe",
            "name": "Thieving Harry's",
            "area": "73 Humber Street, Fruit Market",
            "cuisine": "Brunch, burgers, craft beer, artisan coffee",
            "body": (
                "Thieving Harry's started life as a pop-up in 2011 and has "
                "grown into one of Hull's most-loved independent venues, housed "
                "in a converted 1940s fruit and vegetable warehouse on the "
                "corner of Humber Street and Humber Place. The old Gibson "
                "Bishop and Co lettering is still stencilled above the first-"
                "floor windows, and inside the mix of mismatched furniture, "
                "exposed brick and huge windows looking out over the bobbing "
                "masts of Hull Marina gives the place real character. The menu "
                "runs from a full breakfast and brunch through lunch to weekend "
                "burgers and craft beer in the evenings. It has earned a 4.5 "
                "rating from over 1,400 Google reviews and is a recognised "
                "anchor of the regenerated Fruit Market quarter."
            ),
            "known_for": "Brunch in a converted warehouse overlooking the marina",
            "good_for": "A relaxed daytime bite or weekend evening in the Fruit Market",
            "source_url": "https://www.thievingharrys.co.uk/",
            "verified": "2026-06-22",
        },
        {
            "type": "Restaurant",
            "name": "Hearth",
            "area": "10.5 King Street, Old Town (opposite Hull Minster)",
            "cuisine": "Modern British, bakery and sharing plates",
            "body": (
                "Hearth opened in 2022 when chef Ryan Telford, head baker "
                "Caitlin Ogden and manager Ian Pexton converted former Hull "
                "Minster offices on King Street into a ground-floor bakery and "
                "a first-floor restaurant. The bakery trades Thursday to Sunday "
                "and turns out sourdough loaves, almond croissants and a brunch "
                "menu; the restaurant operates in the evenings, with Telford - "
                "who has cooked under Bruce Poole and Phil Howard - building "
                "menus of small and large sharing plates centred on the open "
                "hearth grill that gives the place its name. In 2024 Hearth "
                "became Hull's only entry in the Michelin Guide, described by "
                "inspectors as a buzzy spot, and the first Hull listing in the "
                "guide since 2018. Book ahead for the restaurant; the bakery is "
                "walk-in."
            ),
            "known_for": "Hull's sole Michelin Guide entry; bakery and hearth-grilled sharing plates",
            "good_for": "A proper dinner in the Old Town, or a bakery brunch before exploring",
            "source_url": "https://guide.michelin.com/gb/en/kingston-upon-hull-region/kingston-upon-hull/restaurants",
            "verified": "2026-06-22",
        },
        {
            "type": "Pub",
            "name": "Ye Olde Black Boy",
            "area": "150 High Street, Old Town",
            "cuisine": "Real ale, cider, traditional pub",
            "body": (
                "Licensed since 1729 on a site that has traded as a coffee "
                "house and a Victorian wine merchant, Ye Olde Black Boy on "
                "Hull's medieval cobbled High Street is the oldest continuously "
                "licensed pub in the city. CAMRA has awarded it a Three Star "
                "Historic Pub Interior rating, recognising the 1926 refit by "
                "T Linsley and Co that left the pub with a front snug of bare "
                "floorboards, original leaded glass windows, a wood-carved head "
                "of the eponymous Black Boy above the fireplace and a serving "
                "hatch in dark-varnished panelling. Beyond the snug a second "
                "bar and an upstairs room extend the space, and a roof terrace "
                "adds modern breathing room. Up to three changing real ales, "
                "typically from Yorkshire breweries such as Black Sheep and Wye "
                "Valley, are on the pumps alongside cider and a wide spirits "
                "selection. The name is believed to derive from a Moroccan boy "
                "who worked in the building during its coffee-house days."
            ),
            "known_for": "Hull's oldest pub and a CAMRA Three Star Historic Interior",
            "good_for": "A pint in an untouched 1929 interior on the medieval High Street",
            "source_url": "https://www.yeoldeblackboy.com/",
            "verified": "2026-06-22",
        },
    ],
    "food_scene": [
        (
            "Hull's food map is anchored by three distinct zones: the medieval "
            "Old Town running along the cobbled High Street and Trinity House "
            "Lane, the regenerated Fruit Market quarter centred on pedestrianised "
            "Humber Street, and the working-class chippy culture of Hessle Road "
            "stretching west from the centre. The city's signature dish is the "
            "Hull pattie - a breadcrumbed, deep-fried mashed potato cake - and "
            "its defining condiment is chip spice, a seasoned salt introduced in "
            "1979 that now appears on every chippy counter in the city."
        ),
        (
            "The Fruit Market has been the most visible change in Hull's food "
            "scene over the past decade. The former wholesale market district "
            "around Humber Street has been reimagined as a cultural and "
            "hospitality quarter, with converted warehouses housing cafes, "
            "tapas bars, a gin distillery, street-food traders and music venues. "
            "Thieving Harry's was an early anchor; it has since been joined by "
            "Ambiente Tapas, Butler Whites and the Humber Street Distillery Co, "
            "all drawing the city's creative and professional crowds to the "
            "waterfront."
        ),
        (
            "In the Old Town, a quieter but deeper food culture has survived "
            "in the lanes around Hull Minster. Bob Carvers has been frying fish "
            "and patties since 1888, and Hearth arrived in 2022 to bring a "
            "Michelin Guide listing back to the city for the first time since "
            "2018. The cluster of heritage pubs along High Street - including "
            "Ye Olde Black Boy and the Lion and Key - preserves a real-ale "
            "tradition that CAMRA has formally recognised. Hull was UK City of "
            "Culture in 2017, and the confidence that came with it is still "
            "visible in the independent businesses that have put down roots "
            "since."
        ),
    ],
    "visit": [
        (
            "Almost everything in this guide is within easy walking distance "
            "of the other. Bob Carvers, Hearth and Ye Olde Black Boy all sit "
            "in or just off the Old Town's medieval High Street, a flat ten-"
            "minute walk from Hull Paragon railway station. Thieving Harry's "
            "is a further ten-minute stroll south through the old streets to "
            "the Fruit Market on Humber Street, where the marina and the river "
            "open up behind it."
        ),
        (
            "Time the day well and it flows naturally. Start with a bakery "
            "brunch at Hearth on King Street, pick up chips and a pattie from "
            "Bob Carvers for lunch, explore the Old Town pubs - Ye Olde Black "
            "Boy is two minutes from both - and finish the afternoon in the "
            "Fruit Market at Thieving Harry's with a craft beer and the view "
            "across the marina. Book Hearth's evening restaurant a week ahead "
            "if you want dinner; the bakery is walk-in Thursday to Sunday."
        ),
    ],
    "checklist": [
        "Try the Hull pattie with chip spice at Bob Carvers on Trinity House Lane",
        "Walk the cobbled medieval High Street and look for the old merchant houses",
        "Book the Hearth restaurant upstairs at least a week ahead for evenings",
        "Allow time in Ye Olde Black Boy to read the history of the carved Black Boy head",
        "End the day in the Fruit Market on Humber Street as the marina catches the light",
    ],
    "what_to_order": (
        "Order with intent. At Bob Carvers, the pattie and chips with a shake "
        "of chip spice and mint sauce - the full local combination. At Thieving "
        "Harry's, the weekend brunch is the pick: a full breakfast or avocado "
        "plate with a flat white. At Hearth, let the kitchen lead and take the "
        "sharing plates off the hearth grill, and an almond croissant from the "
        "bakery if you visit on a weekend morning. At Ye Olde Black Boy, a pint "
        "of whatever Yorkshire ale is on the pump, taken slowly in the front "
        "snug with the fire going."
    ),
    "glance": [
        ("Best for a quick bite", "Bob Carvers, for a Hull pattie and chips since 1888 on Trinity House Lane"),
        ("Best for an occasion", "Hearth, for Michelin Guide sharing plates by the hearth grill in the Old Town"),
        ("Best for atmosphere", "Ye Olde Black Boy's CAMRA-listed 1926 interior on the medieval High Street"),
    ],
    "faq": [
        (
            "What is a Hull pattie and where can I eat one?",
            "A Hull pattie is a breadcrumbed deep-fried mashed potato cake, often flavoured with "
            "sage and onion, and served alongside fish and chips with chip spice and mint sauce. "
            "Bob Carvers on Trinity House Lane in the Old Town, trading since 1888, is the "
            "city's most storied place to try one.",
        ),
        (
            "What is chip spice and is it unique to Hull?",
            "Chip spice is a seasoned salt introduced to Hull in 1979 and now found on almost "
            "every chippy counter in the city. It is applied to chips and patties in the same "
            "way others use salt and vinegar, and is strongly associated with Hull's chippy "
            "culture - visitors often bring a pot home as a food souvenir.",
        ),
        (
            "Does Hull have a Michelin Guide restaurant?",
            "Yes. Hearth on King Street in the Old Town, opened in 2022 by chef Ryan Telford "
            "and head baker Caitlin Ogden, was listed in the 2025 Michelin Guide as Hull's "
            "only entry and the first Hull listing since 2018. The ground-floor bakery is open "
            "Thursday to Sunday; the upstairs restaurant operates in the evenings.",
        ),
        (
            "What is the oldest pub in Hull?",
            "Ye Olde Black Boy at 150 High Street in the Old Town, licensed since 1729, is the "
            "oldest continuously licensed pub in Hull. It holds a CAMRA Three Star Historic "
            "Pub Interior rating for its 1926 refit, with original leaded glass, bare "
            "floorboards and a carved Black Boy head above the fireplace.",
        ),
        (
            "Where is the Fruit Market and what is it known for?",
            "Hull's Fruit Market is the regenerated waterfront quarter centred on pedestrianised "
            "Humber Street, south of the city centre beside the marina. The former wholesale "
            "market has been converted into a neighbourhood of independent cafes, restaurants, "
            "bars and cultural venues, with Thieving Harry's in a converted 1940s warehouse "
            "as one of its anchors.",
        ),
        (
            "Can you do a Hull food day on foot?",
            "Easily. Bob Carvers, Hearth and Ye Olde Black Boy are all within the Old Town, "
            "a short walk from Hull Paragon station. Thieving Harry's in the Fruit Market is "
            "a further ten-minute walk south. The whole circuit is flat and compact, making "
            "Hull one of the easier food-day cities in the north of England.",
        ),
    ],
}
