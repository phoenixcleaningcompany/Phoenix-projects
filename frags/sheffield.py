# Sheffield — web-researched 2026-06-22
# Four venues confirmed currently trading via live web checks.
# Sources recorded per venue below.

TOWNS = {}

TOWNS["sheffield"] = {
    "region": "South Yorkshire",
    "population": "585K",
    "nearby": ["Rotherham", "Barnsley", "Chesterfield"],
    "meta_title": "Best Places to Eat in Sheffield: Local Food Guide",
    "meta_description": (
        "Where to eat in Sheffield: a 130-year-old chippy, a Kiwi-inspired "
        "coffee house, a Michelin-starred mill and a 1931 heritage pub. "
        "Read the guide."
    ),
    "trust_strip": (
        "From a Sharrow Vale chippy open since 1895 to Sheffield's first "
        "Michelin-starred restaurant in a decade, the Steel City eats well"
    ),
    "snapshot": (
        "For a fast answer: Two Steps on Sharrow Vale Road for Sheffield's "
        "oldest fish and chip shop, Tamper Coffee at Sellers Wheel for a "
        "Kiwi-inspired flat white in a former silversmiths, JORO at "
        "Oughtibridge Mill for the city's Michelin-starred tasting menu, "
        "and The Bath Hotel on Victoria Street for a pint in one of "
        "Britain's finest intact 1930s pub interiors. Four moods, one "
        "Sheffield day."
    ),
    "stats": [
        ("585K", "Population of Sheffield (approx)"),
        ("1895", "Year Two Steps first opened its fryers"),
        ("1 Michelin star", "JORO awarded 2026, first in Sheffield for a decade"),
        ("4", "Hand-picked independents"),
    ],
    "pivot_variant": "high-volume",
    "pivot_local_hook": (
        "Sheffield's kitchens cook at high volume and fierce heat: fish "
        "fryers running through the lunch and evening service on Sharrow "
        "Vale Road, the open-kitchen grill at JORO pushing seasonal "
        "proteins hard through every tasting menu, and busy pub kitchens "
        "city-wide loading their canopies with grease-laden vapour "
        "every service."
    ),
    "venues": [
        {
            "type": "Takeaway",
            "name": "Two Steps",
            "area": "249 Sharrow Vale Road, Broomhill",
            "cuisine": "Fish and chips",
            "body": (
                "Two Steps is Sheffield's oldest fish and chip shop, "
                "trading from the same address on Sharrow Vale Road since "
                "1895, when it was listed in the trades directory under "
                "James Bolton as a fried fish dealer. The name dates from "
                "the 1920s: with five chippies in the area, soldiers from "
                "the nearby barracks used to say 'go to the one with two "
                "steps', and it stuck. Current owner Laggy Kafetzis, who "
                "bought the shop in 2001, has over forty years in the "
                "trade and keeps the formula straightforward: properly "
                "fried cod and haddock, chips praised for their crisp "
                "exterior and floury interior, and classic Yorkshire "
                "accompaniments including mushy pea fritters and a chip "
                "butty. It sits in the heart of Sharrow Vale, Sheffield's "
                "independent-minded neighbourhood quarter, and is open "
                "lunchtimes and evenings Monday to Saturday."
            ),
            "known_for": "Sheffield's oldest chippy, trading since 1895 on Sharrow Vale Road",
            "good_for": "Classic Yorkshire fish and chips with 130 years of form",
            "source_url": "https://www.yorkshirepost.co.uk/business/two-steps-sheffield-the-oldest-fish-and-chip-shop-in-yorkshire-that-has-stood-the-test-of-time-for-130-years-5098862",
            "verified": "2026-06-22",
        },
        {
            "type": "Cafe",
            "name": "Tamper Coffee",
            "area": "149 Arundel Street, Cultural Industries Quarter (Sellers Wheel)",
            "cuisine": "Speciality coffee, Kiwi-inspired brunch",
            "body": (
                "Tamper was opened in 2011 by New Zealander Jon Perry and "
                "his Sheffield-born wife Natalie, who wanted to bring the "
                "relaxed cafe culture of Auckland to a city they felt was "
                "underserved by quality coffee. They found a perfect home "
                "in Sellers Wheel, a white-washed 19th-century former "
                "silversmiths on Arundel Street in the Cultural Industries "
                "Quarter, and the exposed brick and reclaimed timber of "
                "the original workshop made the space. Coffee comes from "
                "Ozone Coffee Roasters, fellow New Zealanders, and the "
                "kitchen delivers Australasian-inflected brunch: "
                "crab scrambled eggs, French toast, and the mince on "
                "toast that is considered quintessentially Kiwi. Tamper "
                "won a Good Food Award in 2025 and is consistently rated "
                "among the city's best. The bar licence means it runs "
                "into the evenings too."
            ),
            "known_for": "Kiwi-inspired coffee and brunch in a 19th-century former silversmiths",
            "good_for": "A serious flat white and brunch in the Cultural Industries Quarter",
            "source_url": "https://www.tampercoffee.co.uk/",
            "verified": "2026-06-22",
        },
        {
            "type": "Restaurant",
            "name": "JORO",
            "area": "Oughtibridge Mill, Main Road, Wharncliffe Side (north Sheffield)",
            "cuisine": "Modern British tasting menu, Nordic-Japanese influence",
            "body": (
                "Chef-owners Luke and Stacey Sherwood French built JORO's "
                "reputation in a shipping container in Kelham Island, then "
                "in 2024 moved the restaurant into a 19th-century paper "
                "mill at Oughtibridge, six miles north of the city centre, "
                "transforming a derelict industrial building into one of "
                "the most ambitious dining destinations in the north of "
                "England. In February 2026, JORO was awarded a Michelin "
                "star, the first in Sheffield for a decade, with inspectors "
                "citing its focused, flavourful and confidently creative "
                "tasting menus. The cooking draws on Nordic and Japanese "
                "techniques and uses seasonal, locally sourced produce "
                "across a signature multi-course menu, served at 11 tables "
                "open to the kitchen. The mill terrace and bar open "
                "Wednesday to Sunday; tasting menus run Thursday to "
                "Saturday with a midweek dinner option from Wednesday. "
                "Book well ahead."
            ),
            "known_for": "Sheffield's only Michelin-starred restaurant (2026), in a converted 19th-century mill",
            "good_for": "A landmark tasting-menu occasion in the Steel City",
            "source_url": "https://jororestaurant.co.uk/",
            "verified": "2026-06-22",
        },
        {
            "type": "Pub",
            "name": "The Bath Hotel",
            "area": "66-68 Victoria Street, city centre",
            "cuisine": "Cask ale, craft beer, light snacks",
            "body": (
                "The Bath Hotel is one of only two pubs in Sheffield to "
                "hold a three-star rating on the CAMRA National Inventory "
                "of Historic Pub Interiors, designating it of exceptional "
                "national historic importance. The building dates to around "
                "1868 as a corner beerhouse and grocers; acquired by Ind "
                "Coope in 1914, it was remodelled in 1931 and its layout "
                "and fittings have been barely altered since. Inside are "
                "two rooms: the bar counter is faced in distinctive "
                "orangey-brown tiles with leaded glazing above, and the "
                "lounge snug retains its curving leatherette bench seating, "
                "simply-patterned leaded windows and a hole-in-the-wall "
                "hatch to the servery. A CAMRA conservation award recognised "
                "the careful restoration of this 1930s interior. Now a "
                "freehouse since 2022, after a decade with Thornbridge "
                "Brewery, it pours three regular and three changing cask "
                "ales, and has been CAMRA Sheffield City Centre Pub of the "
                "Year for 2024 and 2025."
            ),
            "known_for": "A three-star CAMRA National Inventory 1931 interior, cask ale",
            "good_for": "A pint in one of Britain's most intact 1930s pub interiors",
            "source_url": "https://thebathhotelpub.com/",
            "verified": "2026-06-22",
        },
    ],
    "food_scene": [
        (
            "Sheffield's food map follows the grain of the city's "
            "neighbourhoods. Sharrow Vale Road, running south-west from "
            "the centre through Broomhill, is the city's most independent "
            "high street, lined with a butcher, a fishmonger, a bakery and "
            "an organic greengrocer alongside restaurants and cafes; Two "
            "Steps has anchored it since 1895. On the other side of the "
            "ring road, the Cultural Industries Quarter clusters around "
            "the Millennium Gallery and the Crucible Theatre, and it is "
            "here that Tamper Coffee set the tone for the city's "
            "independent cafe scene."
        ),
        (
            "Kelham Island, the former industrial heartland where water "
            "wheels and steel forges once ran on the River Don, has "
            "become Sheffield's most-visited food and drink district. "
            "The Peddler Market packs a former warehouse with street food "
            "stalls and craft beer on the first Friday and Saturday of "
            "each month. The Fat Cat and the Kelham Island Tavern, both "
            "CAMRA-celebrated ale houses, anchor the pub scene, while "
            "restaurant openings have steadily added to the neighbourhood. "
            "It is also where JORO first made its name, before the "
            "restaurant outgrew the container and moved to Oughtibridge."
        ),
        (
            "Sheffield has always eaten seriously, but the 2026 Michelin "
            "award for JORO marked a new confidence: the first star in "
            "the city for a decade and a signal that the Steel City's "
            "culinary ambition has caught up with its identity. Add the "
            "historic pub interiors, the independent coffee scene "
            "operating from repurposed workshops, and a Sharrow Vale "
            "chippy that has been frying since the Victorian era, and "
            "you have a food city that rewards proper exploration."
        ),
    ],
    "visit": [
        (
            "The city centre is compact and walkable. Tamper Coffee at "
            "Sellers Wheel and The Bath Hotel on Victoria Street are "
            "minutes apart on foot, and both sit close to Sheffield's "
            "main tram stops at Castle Square and West Street. Sharrow "
            "Vale is a short bus ride or a twenty-minute walk south-west "
            "of the centre, while Two Steps opens lunchtimes and evenings "
            "Monday to Saturday. JORO at Oughtibridge is six miles north "
            "and is best reached by car or taxi; allow the evening for it."
        ),
        (
            "A Sheffield food day falls naturally into two halves. Start "
            "in the Cultural Industries Quarter with a flat white and "
            "brunch at Tamper, then head to Sharrow Vale at lunchtime "
            "for a proper fish supper at Two Steps. Afternoon suits a "
            "circuit of the city's real-ale pubs, beginning with the "
            "1931 interior of the Bath Hotel, and the evening is "
            "made for JORO, where tasting menus run from 7pm on "
            "Wednesdays and from midday on Thursdays to Saturdays. "
            "Book JORO weeks in advance."
        ),
    ],
    "checklist": [
        "Start with a flat white and brunch at Tamper in the Sellers Wheel silversmiths",
        "Head to Two Steps on Sharrow Vale Road at lunch or evening - closed Sundays",
        "See the 1931 tiled interior of The Bath Hotel on Victoria Street",
        "Book JORO at Oughtibridge Mill well in advance; tasting menus fill up fast",
        "Catch the tram to Kelham Island and explore the Peddler Market on a first Friday or Saturday",
    ],
    "what_to_order": (
        "Order with intent. At Two Steps, a large cod or haddock with "
        "proper Sheffield chips and a mushy pea fritter, or a classic "
        "chip butty. At Tamper, ask what is on the Ozone espresso, "
        "and add crab scrambled eggs or the mince on toast for the "
        "full Kiwi experience. At JORO, surrender to the signature "
        "multi-course menu and let the open kitchen set the pace. "
        "At The Bath Hotel, a pint of well-kept cask ale in the "
        "leaded-glass lounge snug, taken slowly."
    ),
    "glance": [
        ("Best for a quick bite", "Two Steps, for Sheffield's oldest fish and chips on Sharrow Vale Road"),
        ("Best for an occasion", "JORO, for the Michelin-starred tasting menu in a converted mill"),
        ("Best for atmosphere", "The Bath Hotel's intact 1931 tiled pub interior on Victoria Street"),
    ],
    "faq": [
        (
            "Where can I get the best fish and chips in Sheffield?",
            "Two Steps at 249 Sharrow Vale Road has been frying since 1895 "
            "and is widely regarded as Sheffield's oldest and best chippy. "
            "The current owner Laggy has over forty years in the trade; "
            "the chips are praised for their crisp exterior and the cod "
            "and haddock are freshly fried to order. Open lunchtimes and "
            "evenings, Monday to Saturday.",
        ),
        (
            "Where is the best independent coffee in Sheffield?",
            "Tamper Coffee at Sellers Wheel, 149 Arundel Street, opened "
            "in 2011 and helped pioneer the city's speciality scene. "
            "Founded by New Zealanders Jon and Natalie Perry, it serves "
            "Ozone Coffee Roasters beans in a former 19th-century "
            "silversmiths in the Cultural Industries Quarter, with "
            "Kiwi-inspired brunch to match. It won a Good Food Award "
            "in 2025.",
        ),
        (
            "Does Sheffield have a Michelin-starred restaurant?",
            "Yes. JORO at Oughtibridge Mill, six miles north of the city "
            "centre, was awarded a Michelin star in February 2026, the "
            "first in Sheffield for a decade. Chef-owners Luke and Stacey "
            "Sherwood French serve creative tasting menus in a converted "
            "19th-century paper mill. Bookings at jororestaurant.co.uk.",
        ),
        (
            "Which Sheffield pub has the best interior?",
            "The Bath Hotel at 66-68 Victoria Street holds a three-star "
            "rating on the CAMRA National Inventory of Historic Pub "
            "Interiors, one of only two in the city. Its 1931 refit by "
            "Ind Coope survives largely intact: tiled bar counter, "
            "leaded-glass lounge snug and curving leatherette seating. "
            "It is a freehouse and CAMRA Sheffield City Centre Pub of "
            "the Year for 2024 and 2025.",
        ),
        (
            "What is the best area to eat in Sheffield?",
            "Sharrow Vale Road is the city's most independent food "
            "street, running through Broomhill with butchers, fishmongers "
            "and cafes alongside Two Steps. Kelham Island is the "
            "liveliest district for restaurants, bars and the monthly "
            "Peddler Market. The Cultural Industries Quarter has the "
            "best independent coffee, anchored by Tamper.",
        ),
        (
            "Can you do a Sheffield food day on foot and public transport?",
            "Mostly. Tamper and The Bath Hotel are minutes apart in the "
            "centre, both close to Castle Square and West Street tram "
            "stops. Two Steps is a short bus ride south-west to Broomhill. "
            "JORO at Oughtibridge Mill is six miles north and needs a "
            "car or taxi, so save it for the evening.",
        ),
    ],
}
