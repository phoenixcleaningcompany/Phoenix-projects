# Bradford — web-researched 2026-06-22
# Four venues confirmed currently trading via live web checks.
# Sources recorded per venue below.

TOWNS = {}

TOWNS["bradford"] = {
    "region": "West Yorkshire",
    "population": "350K",
    "nearby": ["Halifax", "Keighley", "Shipley"],
    "meta_title": "Best Places to Eat in Bradford: Local Food Guide",
    "meta_description": (
        "Where to eat in Bradford: a desi breakfast since 1964, coffee "
        "in the Wool Exchange, a historic karahi house and a CAMRA "
        "cellar bar. Read the guide."
    ),
    "trust_strip": (
        "From a 1964 desi breakfast institution to Bradford's oldest curry "
        "house, the UK Curry Capital feeds a city with real depth and story"
    ),
    "snapshot": (
        "For a fast answer: Sweet Centre on Lumb Lane for the iconic desi "
        "breakfast and chana puri in Bradford's 1964 original, Tiffin Coffee "
        "inside the Grade I-listed Wool Exchange for the city's best flat "
        "white, Karachi Restaurant on Neal Street for the lamb karahi that "
        "Rick Stein filmed, and The Exchange Craft Beer House under the Wool "
        "Exchange for CAMRA-winning cask ale in Victorian vaulted cellars. "
        "Four moods, one city that takes food seriously."
    ),
    "stats": [
        ("350K", "Population (approx)"),
        ("1964", "Year Sweet Centre first opened on Lumb Lane"),
        ("200+", "Asian restaurants in the UK Curry Capital"),
        ("4", "Hand-picked independents"),
    ],
    "pivot_variant": "high-volume",
    "pivot_local_hook": (
        "Bradford's curry houses fire tawas and karahis over high heat "
        "through lunch and dinner, while the city's high-volume South Asian "
        "kitchens run charcoal grills and deep fryers round the clock - "
        "throwing a heavy load of grease-laden vapour into their canopies "
        "every service."
    ),
    "venues": [
        {
            "type": "Curry House",
            "name": "Sweet Centre",
            "area": "110-114 Lumb Lane, Manningham",
            "cuisine": "Pakistani, Kashmiri, desi breakfasts",
            "body": (
                "Bradford's most storied restaurant opened in December 1964 "
                "when brothers Abdul Rehman, Mohammed Bashir and Abdul Aziz "
                "set up a halal sweet and provisions shop on Lumb Lane to "
                "serve the textile and engineering workers flooding into "
                "Manningham from South Asia. The sweets became breakfasts, "
                "the breakfasts became legend. Six decades later, run by the "
                "third generation, Sweet Centre still draws queues for its "
                "desi breakfast: a golden plate of halwa puri - soft fried "
                "bread, sweet semolina pudding and spiced chana - eaten with "
                "desi chai. The samosas are a three-generation family recipe; "
                "the seekh kebab comes off the charcoal grill. This is the "
                "dish Bradford is quietly proudest of, and the place that "
                "started it all."
            ),
            "known_for": "The desi breakfast - halwa puri and chana - since 1964",
            "good_for": "An iconic Bradford breakfast or a lunch of charcoal grills",
            "source_url": "https://sweetcentrebradford.co.uk/",
            "verified": "2026-06-22",
        },
        {
            "type": "Cafe",
            "name": "Tiffin Coffee",
            "area": "The Wool Exchange, 22 Bank Street, city centre",
            "cuisine": "Speciality coffee, cakes and light bites",
            "body": (
                "Few cafes in England have a room like this. Tiffin Coffee "
                "trades inside the Bradford Wool Exchange, the Gothic Revival "
                "landmark built between 1864 and 1867 by Lockwood and Mawson "
                "- the architects behind Saltaire - and Grade I-listed for its "
                "soaring Venetian-Gothic interior with carved stone arcades "
                "and a dramatic central hall. The foundation stone was laid by "
                "Prime Minister Lord Palmerston. Tiffin sets up under that "
                "ceiling with serious espresso, freshly brewed filter, and "
                "homemade cakes including local favourites like Yorkshire "
                "scoundrels. It holds a 4.6-star Google rating from over 600 "
                "reviews and is open seven days. Order a flat white and look up."
            ),
            "known_for": "Speciality coffee inside a Grade I-listed Victorian wool hall",
            "good_for": "A serious coffee break in Bradford's most spectacular room",
            "source_url": "https://www.tiffincoffee.co.uk/wool-exchange",
            "verified": "2026-06-22",
        },
        {
            "type": "Restaurant",
            "name": "Karachi Restaurant",
            "area": "15 Neal Street, city centre",
            "cuisine": "Pakistani, karahi curries",
            "body": (
                "The Karachi opened in the early 1960s on Neal Street and is "
                "widely recognised as Bradford's oldest curry house. It is a "
                "cafe-style, unlicensed room - plain tables, an open kitchen "
                "visible from your seat - and the food is the reason to come. "
                "In 2002, Rick Stein visited with a film crew for his "
                "television series Food Heroes and was shown how to make the "
                "house speciality: a lamb and spinach karahi curry, cooked in "
                "the bowl and brought to the table in it. The dish featured in "
                "his subsequent cookbook. The Karachi is bring-your-own-drink, "
                "cash-friendly, and the karahi - thick masala, coriander, "
                "slow-cooked meat - is still the order to make. Unpretentious, "
                "historic and genuinely Bradford."
            ),
            "known_for": "Bradford's oldest curry house and Rick Stein's lamb karahi",
            "good_for": "An authentic, no-frills karahi curry in a Bradford original",
            "source_url": "https://www.yelp.com/biz/karachi-restaurant-bradford",
            "verified": "2026-06-22",
        },
        {
            "type": "Pub",
            "name": "Exchange Craft Beer House",
            "area": "The Wool Exchange, Hustlergate, city centre",
            "cuisine": "Cask and craft ale, bar snacks",
            "body": (
                "Opened in November 2018 by the owner of Hebden Bridge's "
                "Nightjar Brewery, the Exchange occupies the vaulted Victorian "
                "cellars directly beneath the Wool Exchange building. The room "
                "is open-plan under a brick barrel ceiling, lit warmly enough "
                "that it feels lively rather than dim, with an island bar "
                "carrying seven hand-pulls of rotating cask ale - at least one "
                "always a Nightjar pour, the rest sourced from smaller local "
                "and regional Yorkshire breweries. Since Hustlergate was "
                "pedestrianised in 2025, the pub also spills onto the street "
                "in good weather. It was named CAMRA Bradford Branch Pub of "
                "the Year, Overall Winner, in 2025 - the strongest endorsement "
                "the real-ale world offers. Come for a pint and a proper look "
                "at those ceilings."
            ),
            "known_for": "CAMRA Pub of the Year 2025, seven rotating cask ales in Victorian vaults",
            "good_for": "A serious pint under Victorian brickwork with a Yorkshire-focused tap list",
            "source_url": "https://exchangecraftbeer.co.uk/",
            "verified": "2026-06-22",
        },
    ],
    "food_scene": [
        (
            "Bradford's food identity is built on its South Asian heritage. "
            "When the wool mills needed workers in the 1950s and 60s, the "
            "city recruited from Pakistan and Kashmir, and those communities "
            "brought their kitchens with them. Sweet Centre opened on Lumb "
            "Lane in 1964; the Karachi was already on Neal Street. Manningham "
            "and its long axis of Lumb Lane became Bradford's curry corridor, "
            "the dense stretch of Pakistani and Kashmiri restaurants that "
            "earned the city its Curry Capital title - held for six "
            "consecutive years in the English Curry Awards."
        ),
        (
            "The city centre has its own layer. The Grade I-listed Wool "
            "Exchange on Bank Street, built in the 1860s at the peak of "
            "Bradford's textile wealth and once the trading floor for the "
            "global wool market, now holds Tiffin Coffee in its Gothic main "
            "hall and the Exchange Craft Beer House in its Victorian cellars. "
            "A short walk underground, Sunbridge Wells - a restored network "
            "of Victorian tunnels opened in 2016 - holds independent bars and "
            "a candlelit Italian pizzeria, adding a genuinely eccentric dimension "
            "to the city's after-dark offer."
        ),
        (
            "Bradford was UK City of Culture for 2025, and the year brought "
            "fresh energy to a scene that needed little push. Over 200 "
            "independent Asian restaurants remain active across the district, "
            "from the BYOB karahi houses of the city centre to the desi "
            "breakfast cafes of Manningham. The food geography runs from the "
            "narrow streets around Neal Street and White Abbey Road to the "
            "Victorian grandeur of Bank Street and Hustlergate - you can eat "
            "a three-generation samosa recipe and a CAMRA award-winning pale "
            "ale within five minutes of each other."
        ),
    ],
    "visit": [
        (
            "Much of this guide clusters in a compact area. The Wool Exchange "
            "on Bank Street is the anchor: Tiffin Coffee is inside the building, "
            "the Exchange Craft Beer House is in the cellars below, and the "
            "Karachi on Neal Street is a short walk south. Bradford Interchange "
            "and Forster Square stations both sit within ten minutes on foot. "
            "Sweet Centre in Manningham is about a mile north of the city "
            "centre, an easy taxi or bus ride up Manningham Lane."
        ),
        (
            "Time it right and the day flows naturally. Start with a desi "
            "breakfast at Sweet Centre - halwa puri and desi chai - then walk "
            "or bus into the centre for a flat white at Tiffin Coffee under "
            "the Wool Exchange ceiling. Head to the Karachi for a proper lunch "
            "karahi with bread, then end the afternoon in the Exchange's "
            "vaulted cellars with a pint of Yorkshire cask ale. Sweet Centre "
            "and the Karachi are unlicensed - bring your own drink, or plan "
            "around them. Book nothing; both curry houses are walk-in."
        ),
    ],
    "checklist": [
        "Arrive early at Sweet Centre for the desi breakfast - halwa puri sells out",
        "Take a flat white at Tiffin Coffee and look up at the Wool Exchange vaulted ceiling",
        "Head to the Karachi on Neal Street for the lamb karahi - BYOB and cash-friendly",
        "Finish in the Exchange cellar bar - seven hand-pulls of rotating Yorkshire cask ale",
        "Walk Hustlergate and Lumb Lane to take in the food geography of Bradford",
    ],
    "what_to_order": (
        "Order with intent. At Sweet Centre, the desi breakfast: halwa puri, "
        "chana and desi chai, or a seekh kebab off the charcoal grill. At "
        "Tiffin Coffee, a flat white and a Yorkshire scoundrel cake - or "
        "whichever seasonal bake is behind the counter. At the Karachi, the "
        "lamb and spinach karahi with naan, eaten from the bowl it was cooked "
        "in. At the Exchange Craft Beer House, ask the bar what Nightjar has "
        "on the hand-pull that day, and look at those Victorian brick ceilings."
    ),
    "glance": [
        ("Best for a quick bite", "Sweet Centre, for halwa puri and chai in Bradford's 1964 original"),
        ("Best for an occasion", "Karachi Restaurant, for the historic lamb karahi Rick Stein filmed"),
        ("Best for atmosphere", "Exchange Craft Beer House in the Victorian vaulted cellars"),
    ],
    "faq": [
        (
            "Why is Bradford called the Curry Capital of Britain?",
            "Bradford held the Curry Capital of Britain title for six consecutive "
            "years in the English Curry Awards, reflecting the city's deep South "
            "Asian food heritage. Over 200 independent Asian restaurants operate "
            "across the district, a legacy of the Pakistani and Kashmiri "
            "communities who settled here from the 1950s to work in the wool mills.",
        ),
        (
            "Where can I get a desi breakfast in Bradford?",
            "Sweet Centre on Lumb Lane in Manningham, open since 1964, is the "
            "city's most famous desi breakfast spot. The halwa puri - soft fried "
            "bread, sweet semolina and spiced chickpeas - is the order to make, "
            "alongside samosas made from a three-generation family recipe.",
        ),
        (
            "Which is Bradford's oldest curry house?",
            "Karachi Restaurant on Neal Street, open since the early 1960s, is "
            "widely recognised as Bradford's oldest curry house. Rick Stein "
            "visited in 2002 for his Food Heroes television series and filmed "
            "the lamb and spinach karahi, which appeared in his subsequent "
            "cookbook. It is unlicensed and cash-friendly.",
        ),
        (
            "Where is the best independent coffee in Bradford?",
            "Tiffin Coffee at the Wool Exchange on Bank Street is Bradford's "
            "most celebrated independent coffee stop, trading inside the Grade "
            "I-listed Gothic Revival wool-trading hall built in 1864-67. It "
            "holds a 4.6-star Google rating and is open seven days a week.",
        ),
        (
            "Which Bradford pub won CAMRA Pub of the Year?",
            "The Exchange Craft Beer House, in the Victorian vaulted cellars "
            "beneath the Wool Exchange on Hustlergate, was named CAMRA Bradford "
            "Branch Pub of the Year, Overall Winner, in 2025. It carries seven "
            "rotating hand-pulls of cask ale, including Nightjar Brewery pours "
            "and local Yorkshire independents.",
        ),
        (
            "Can you do a Bradford food day on foot?",
            "Mostly. Tiffin Coffee, the Exchange Craft Beer House and the Karachi "
            "Restaurant are all within a short walk of Bradford city centre and "
            "both main stations. Sweet Centre is about a mile north in Manningham "
            "- an easy bus ride up Manningham Lane or a ten-minute taxi.",
        ),
    ],
}
