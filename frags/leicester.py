TOWNS = {}

# --------------------------------------------------------------------------
# LEICESTER — web-researched 2026-06-22
# Four venues confirmed currently trading via live web search / review
# platforms. Bobby's 50th-anniversary coverage (Feb 2026) confirms trading.
# Leicester Coffee House Company TripAdvisor reviews active 2025-2026.
# Kayal Yelp listing updated June 2026; Welsh & Midlands Curry Award 2025.
# The Globe: TripAdvisor review dated 13 June 2026 + Untappd check-ins.
# --------------------------------------------------------------------------
TOWNS["leicester"] = {
    "region": "the East Midlands",
    "population": "355,000",
    "nearby": ["Loughborough", "Hinckley", "Melton Mowbray"],
    "meta_title": "Best Places to Eat in Leicester: Local Food Guide",
    "meta_description": (
        "Where to eat in Leicester: Gujarati cooking on the Golden Mile, a "
        "city-centre roastery, Kerala cuisine and a pub since 1720. "
        "Read the guide."
    ),
    "trust_strip": (
        "From the Gujarati sweet shops of Belgrave Road to a Kerala kitchen "
        "with a national curry award, Leicester punches well above its weight "
        "as an independent food city"
    ),
    "snapshot": (
        "For a fast answer: Bobby's on Belgrave Road for fifty years of "
        "Gujarati vegetarian cooking on the Golden Mile, Leicester Coffee "
        "House Company on Granby Street for single-origin beans roasted on "
        "site, Kayal on Granby Street for award-winning Kerala seafood and "
        "dosas, and The Globe on Silver Street for a pint in a pub that has "
        "been pulling ale since 1720. Four moods, one compact city centre."
    ),
    "stats": [
        ("355K", "City population (approx)"),
        ("1976", "Year Bobby's first opened on the Golden Mile"),
        ("1720", "Year The Globe first opened on Silver Street"),
        ("4", "Hand-picked independents"),
    ],
    "pivot_variant": "high-volume",
    "pivot_local_hook": (
        "Leicester's high-volume Golden Mile kitchens turn out hundreds of "
        "thalis and dosas every service over fierce gas burners, and the "
        "curry houses, balti pans and tandoor ovens across Belgrave Road and "
        "the city centre push a heavy load of grease-laden vapour into their "
        "canopies night after night."
    ),
    "venues": [
        {
            "type": "Gujarati Restaurant",
            "name": "Bobby's",
            "area": "154-156 Belgrave Road, the Golden Mile",
            "cuisine": "Gujarati vegetarian, South Asian sweets and snacks",
            "body": (
                "Bobby's opened on St Valentine's Day 1976 when Bhagwanjibhai "
                "and Manglaben Lakhani, expelled from Uganda by Idi Amin four "
                "years earlier, saw a need to feed Leicester's fast-growing "
                "South Asian community. Named after the 1973 Bollywood film "
                "that captured the spirit of new beginnings, it became one of "
                "the first dedicated Gujarati vegetarian restaurants in the UK. "
                "Now run by the second generation of the Lakhani family, Bobby's "
                "celebrated its 50th anniversary in February 2026 with the Lord "
                "Lieutenant and the city mayor among the guests. The menu spans "
                "dahi puris, thalis, chaat and a sweet shop of lilo chevdo and "
                "barfi that Leicester has depended on for half a century."
            ),
            "known_for": "Fifty years of Gujarati vegetarian cooking on Belgrave Road",
            "good_for": "A genuine Golden Mile thali or chaat at any time of day",
            "source_url": "https://pukaarnews.com/bobbys-restaurant-celebrates-50-years-at-the-heart-of-leicester/31821/",
            "verified": "2026-06-22",
        },
        {
            "type": "Cafe",
            "name": "Leicester Coffee House Company",
            "area": "110 Granby Street, city centre",
            "cuisine": "Speciality coffee, light food",
            "body": (
                "The name nods to the Leicester Coffee and Cocoa House Company "
                "of 1877, which opened its first shop on the very same street. "
                "The modern incarnation was launched by Gail Brown and Aaron "
                "Keen after two years running a home roastery as a side project, "
                "and it has quickly become the benchmark for speciality coffee in "
                "the city. Beans are sourced direct and roasted in small batches "
                "on a Probat machine behind the counter on pedestrianised Granby "
                "Street, and the result is a cup that draws comparisons, from "
                "regular customers, to the best in London or Dublin. Open weekday "
                "mornings from seven, it catches the commuter and the lingerer "
                "in equal measure."
            ),
            "known_for": "Small-batch in-house roasting on Granby Street",
            "good_for": "A morning flat white or filter, and beans to take home",
            "source_url": "https://www.tripadvisor.com/Restaurant_Review-g186334-d15742367-Reviews-Leicester_Coffee_House_Company-Leicester_Leicestershire_England.html",
            "verified": "2026-06-22",
        },
        {
            "type": "Restaurant",
            "name": "Kayal",
            "area": "153 Granby Street, city centre",
            "cuisine": "Kerala and South Indian, seafood",
            "body": (
                "Kayal has anchored the Kerala end of Leicester's South Asian "
                "dining scene since 2005, and in 2025 the Welsh and Midlands "
                "Curry Awards panel named it Best South Indian Restaurant of the "
                "Year, citing the most authentic South Indian dining experience "
                "outside India. The kitchen specialises in the coastal cooking "
                "of Kerala: properly made dosas with sambar and coconut chutney, "
                "aromatic fish curries, Kerala-style biryani and a prawn moilee "
                "that regulars come back to repeatedly. The dining room is "
                "calm and family-run in feel. With over 1,900 five-star reviews "
                "across platforms, it is the restaurant most Leicester locals "
                "point a visitor towards for a proper sit-down meal."
            ),
            "known_for": "Award-winning Kerala cooking, dosas and coastal seafood",
            "good_for": "A leisurely South Indian meal with a group or as a special occasion",
            "source_url": "https://www.yelp.co.uk/biz/kayal-leicester-2",
            "verified": "2026-06-22",
        },
        {
            "type": "Pub",
            "name": "The Globe",
            "area": "43 Silver Street, city centre",
            "cuisine": "Pub food, real ale",
            "body": (
                "The Globe has been a pub since 1720, making it one of the oldest "
                "continuously licensed premises in Leicester on its original site "
                "and name. Early records from 1718 already show a deed relating "
                "to the building, and quality ale was once brewed here using "
                "spring water drawn from a well beneath the bar that still exists "
                "today. Owned by Everards, the independent Leicester family "
                "brewery, it was the first Everards pub to return to real ale "
                "after a keg-only period and now pours up to seven casks alongside "
                "two changing real ciders. The kitchen turns out honest pub grub "
                "and a home-made Sunday roast every week. Compact, no-frills and "
                "cashless, it sits a short walk from the cathedral quarter and "
                "the St Martin's food scene."
            ),
            "known_for": "A pub since 1720, real ales from Everards, the original spring well",
            "good_for": "A proper cask ale in the heart of the old city",
            "source_url": "https://www.tripadvisor.com/Restaurant_Review-g186334-d1073272-Reviews-The_Globe_Leicester-Leicester_Leicestershire_England.html",
            "verified": "2026-06-22",
        },
    ],
    "food_scene": [
        (
            "Leicester's food map has two distinct gravitational centres. The first "
            "is Belgrave Road and its Golden Mile, a kilometre of South Asian "
            "restaurants, sweet shops, jewellers and sari houses that has served "
            "Leicester's large Gujarati and Punjabi communities since the 1970s. "
            "It is the closest thing in England to an Indian high street: the "
            "restaurants are almost entirely vegetarian, the sweets counters sell "
            "lilo chevdo and barfi by the kilo, and on Diwali night the whole "
            "road closes for one of the largest outdoor festivals in the country."
        ),
        (
            "The second centre is the compact city itself, where Granby Street, "
            "St Martin's Square and the Cathedral Quarter cluster independent "
            "cafes, roasteries and restaurants within a short walk of each other. "
            "Narborough Road, officially the most ethnically diverse street in the "
            "UK according to the London School of Economics, adds a third layer "
            "of global food just west of the centre, with Polish delis, Turkish "
            "grills and Caribbean takeaways running side by side."
        ),
        (
            "The city also has a serious curry-award pedigree: the Leicestershire "
            "Curry Awards regularly surface names unknown outside the East Midlands, "
            "and the city's long tradition of South Indian cooking, shaped by its "
            "large Gujarati population and a substantial Tamil community, means "
            "the dosa and thali are as natural a part of Leicester eating as a "
            "pub pie. For a city of 355,000 the breadth is remarkable."
        ),
    ],
    "visit": [
        (
            "The city centre picks sit close together. The Globe, Kayal and "
            "Leicester Coffee House Company are all within a few minutes of each "
            "other on and around Granby Street, and St Martin's Square is a short "
            "walk away. The Golden Mile is roughly two miles north in Belgrave, "
            "a short bus ride or taxi from the centre along Belgrave Road."
        ),
        (
            "Timing helps. Leicester Coffee House Company is a weekday-morning "
            "operation, so plan that first. Kayal works well for a long lunch or "
            "evening meal. Bobby's on the Golden Mile keeps later hours and suits "
            "the afternoon into evening. The Globe is open daily from midday and "
            "is an easy finish to any food day in the old city quarter."
        ),
    ],
    "checklist": [
        "Start with coffee at Leicester Coffee House Company on pedestrianised Granby Street",
        "Take the short bus ride up Belgrave Road to Bobby's for a thali or chaat",
        "Return to the city centre for Kerala cooking at Kayal on Granby Street",
        "Finish with a cask ale at The Globe on Silver Street - pub since 1720",
        "Visit Belgrave Road on Diwali night if timing allows - one of the largest street celebrations in England",
    ],
    "what_to_order": (
        "Order with intent. At Bobby's, a Gujarati thali with dahi puri and a "
        "box of lilo chevdo from the sweet counter to take home. At Leicester "
        "Coffee House Company, ask which single origin is on the Probat that "
        "week and take a bag of beans away. At Kayal, the dosas are the thing "
        "to start with, then a prawn moilee or a Kerala fish curry. At The "
        "Globe, a pint of Everards cask ale in the bar where a well still sits "
        "beneath the floor."
    ),
    "glance": [
        ("Best for a quick bite", "Bobby's, for a dahi puri or chaat on the Golden Mile"),
        ("Best for an occasion", "Kayal, for award-winning Kerala dining on Granby Street"),
        ("Best for atmosphere", "The Globe on Silver Street, a pub since 1720"),
    ],
    "faq": [
        (
            "Where can I eat authentic Gujarati food in Leicester?",
            "Bobby's at 154 Belgrave Road on the Golden Mile, open since 1976 and "
            "run by the Lakhani family for fifty years, is the city's best-known "
            "Gujarati vegetarian restaurant, serving thalis, chaat, dahi puris "
            "and fresh sweets from its counter.",
        ),
        (
            "What is the Golden Mile in Leicester?",
            "The Golden Mile is the popular name for Belgrave Road in north "
            "Leicester, a stretch of South Asian restaurants, sweet shops, sari "
            "houses and jewellers that has been at the heart of the city's "
            "Gujarati and Punjabi communities since the 1970s. It hosts one of "
            "the UK's largest Diwali street celebrations each autumn.",
        ),
        (
            "Where is the best independent coffee in Leicester?",
            "Leicester Coffee House Company at 110 Granby Street roasts single-"
            "origin beans in small batches on a Probat machine behind the counter "
            "and opens from 7am on weekdays, making it the city centre's "
            "benchmark for speciality coffee.",
        ),
        (
            "Does Leicester have a good South Indian restaurant?",
            "Kayal at 153 Granby Street has served Kerala and South Indian "
            "cuisine since 2005 and won Best South Indian Restaurant of the Year "
            "at the Welsh and Midlands Curry Awards 2025. The dosas, prawn "
            "moilee and Kerala fish curries are the orders to make.",
        ),
        (
            "What is the oldest pub in Leicester city centre?",
            "The Globe on Silver Street has been a pub since 1720 and is one of "
            "the oldest continuously licensed premises in Leicester on its "
            "original site and name. It is an Everards tied house serving up to "
            "seven real ales alongside two real ciders.",
        ),
        (
            "Can you do a Leicester food day on foot?",
            "Mostly. Leicester Coffee House Company, Kayal and The Globe are "
            "all within easy walking distance of each other in the city centre. "
            "Bobby's on the Golden Mile is about two miles north in Belgrave, "
            "a short bus or taxi ride up Belgrave Road.",
        ),
    ],
}
