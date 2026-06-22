TOWNS = {}

# --------------------------------------------------------------------------
# MILTON KEYNES — web-researched June 2026
# --------------------------------------------------------------------------
TOWNS["milton-keynes"] = {
    "region": "Buckinghamshire",
    "population": "230K",
    "nearby": ["Bedford", "Northampton", "Luton"],
    "meta_title": "Best Places to Eat in Milton Keynes: Local Food Guide",
    "meta_description": (
        "Where to eat in Milton Keynes: Vietnamese pho on 12th Street, a "
        "Stony Stratford cafe, award-winning Indian and a CAMRA Pub of the "
        "Year. Read the guide."
    ),
    "trust_strip": (
        "From a five-star speciality roaster in Stony Stratford to a CAMRA "
        "Pub of the Year in Wolverton, MK's independent food scene runs deeper "
        "than the grid roads suggest"
    ),
    "snapshot": (
        "For a fast answer: Ha Noi on 12th Street for bold Vietnamese pho and "
        "banh mi in the city centre, Mile Zero Coffee on Stony Stratford High "
        "Street for a five-star-rated speciality roast, Maaya at The Hub for "
        "Michelin-listed modern Indian with three consecutive MK Food Awards, "
        "and The Craufurd Arms in Wolverton for CAMRA-accredited real ale and "
        "live music in a 1905 independent. Four moods across MK's most "
        "distinctive quarters."
    ),
    "stats": [
        ("230K", "Population (approx)"),
        ("1967", "Year Milton Keynes was designated a new town"),
        ("Stony Stratford", "MK's oldest independent food quarter"),
        ("4", "Hand-picked independents"),
    ],
    "pivot_variant": "high-volume",
    "pivot_local_hook": (
        "Milton Keynes has grown fast: the city centre grid now packs "
        "restaurant kitchens, hotel dining rooms and late-night bars into "
        "a dense footprint where high-volume cooking and grease-laden "
        "canopies run hard through every service."
    ),
    "venues": [
        {
            "type": "Casual Dining",
            "name": "Ha Noi",
            "area": "14 Savoy Crescent, 12th Street, Central Milton Keynes, MK9 3PU",
            "cuisine": "Vietnamese, Pan-Asian",
            "body": (
                "Opened in August 2025 on the buzzy 12th Street dining strip, Ha "
                "Noi brought a sharp, modern Vietnamese kitchen to the heart of "
                "Central Milton Keynes. The dining room is stylish and relaxed by "
                "day, with a menu built around the classics done well: a clear, "
                "fragrant pho with your choice of protein, fresh banh mi, summer "
                "rolls and sizzling wok dishes from across Southeast Asia, paired "
                "with handcrafted cocktails. From Friday evenings the venue shifts "
                "gear, with late-licence DJs and a party crowd. Still in its first "
                "year and already firmly on MK's independent restaurant map, Ha "
                "Noi is the address for Vietnamese food in the city and holds an "
                "active food hygiene registration with Milton Keynes Council."
            ),
            "known_for": "Fresh pho, banh mi and pan-Asian street food dishes",
            "good_for": "A lively city-centre meal or a late-night cocktail on 12th Street",
            "source_url": "https://www.ha-noi.co.uk/",
            "verified": "2026-06-22",
        },
        {
            "type": "Cafe",
            "name": "Mile Zero Coffee",
            "area": "56 High Street, Stony Stratford, Milton Keynes, MK11 1AQ",
            "cuisine": "Speciality coffee",
            "body": (
                "Stony Stratford's High Street has been Milton Keynes's most "
                "stubbornly independent quarter since before the grid roads were "
                "drawn, and Mile Zero Coffee is its standout cafe. Opened in late "
                "2024, the small-but-serious roaster-cafe on the High Street won a "
                "5-star food hygiene rating from Milton Keynes Council in February "
                "2026, confirming it is firmly established. The name is a nod to "
                "Stony Stratford's old coaching-road past: this was once the "
                "posting point from which distances to London were measured. Today "
                "the focus is speciality espresso and filter from carefully sourced "
                "beans, freshly made treats, and a warm, unhurried atmosphere that "
                "makes it the go-to stop on the High Street before browsing "
                "Odell's Yard or the weekly market."
            ),
            "known_for": "Speciality espresso and filter in a 5-star-rated independent cafe",
            "good_for": "A proper coffee stop in Stony Stratford before exploring the High Street",
            "source_url": "https://www.milezerocoffee.com/",
            "verified": "2026-06-22",
        },
        {
            "type": "Restaurant",
            "name": "Maaya Indian Kitchen & Bar",
            "area": "Brooklyn House, 2 Rillaton Walk, The Hub, Central Milton Keynes, MK9 2FZ",
            "cuisine": "Modern Indian",
            "body": (
                "Maaya is the benchmark independent restaurant at The Hub, Milton "
                "Keynes's purpose-built leisure and dining quarter. The kitchen "
                "draws on 30 years of family cooking experience, sending out a "
                "menu that ranges from street-food starters through classic curries "
                "to chef-special signatures, all halal and made to order. The "
                "awards pile up: Best Asian Restaurant at the Milton Keynes Food "
                "and Leisure Awards for three consecutive years, Best Indian "
                "Restaurant in Buckinghamshire at the Asian Food and Restaurant "
                "Awards, and recognition at the English Curry Awards. The most "
                "recent food hygiene inspection, in February 2025, confirms the "
                "kitchen is active and operational. Book ahead, particularly at "
                "weekends when the Hub fills quickly."
            ),
            "known_for": "Multi-award-winning modern Indian, three consecutive MK Food Award wins",
            "good_for": "A special-occasion meal at MK's most-decorated independent restaurant",
            "source_url": "https://maayamiltonkeynes.com/",
            "verified": "2026-06-22",
        },
        {
            "type": "Pub",
            "name": "The Craufurd Arms",
            "area": "59 Stratford Road, Wolverton, Milton Keynes, MK12 5LT",
            "cuisine": "Pub food, craft ales",
            "body": (
                "Built in 1905 in the Victorian railway town of Wolverton, the "
                "Craufurd Arms has been independently owned and run as one of "
                "Milton Keynes's most loved community pubs for decades. The main "
                "bar has four hand pumps serving the house XT4 ale as a regular "
                "alongside a rotating selection of guests drawn from eight local "
                "breweries, plus a fifth pump for Saxby Ciders. A separate "
                "250-capacity live music room with its own bar has hosted "
                "everything from The Cure and The Specials in the 1980s to "
                "touring indie and rock acts today. The Milton Keynes and North "
                "Bucks CAMRA branch named it their Pub of the Year and Cider Pub "
                "of the Year for 2026, and it appears in CAMRA's Good Beer Guide "
                "2026 — the branch's highest recognition for a pub that keeps "
                "real ale well."
            ),
            "known_for": "CAMRA Pub of the Year 2026, live music since the 1970s, XT ales",
            "good_for": "A well-kept pint and live music in Wolverton's best-loved independent",
            "source_url": "https://camra.org.uk/pubs/craufurd-arms-milton-keynes-130736",
            "verified": "2026-06-22",
        },
    ],
    "food_scene": [
        (
            "Milton Keynes is a planned city built from 1967 on a grid of dual "
            "carriageways and roundabouts, but its food map does not follow the "
            "master plan. The best independent eating happens in the older "
            "villages that were absorbed into the new town: Stony Stratford to "
            "the north-west, with its coaching-road High Street, weekly market "
            "and Odell's Yard courtyard, is the strongest independent food "
            "quarter, while Wolverton's Victorian terraces shelter pubs and "
            "small restaurants that predate the grid roads by generations."
        ),
        (
            "The modern city centre has its own food identity centred on The Hub "
            "and the new 12th Street dining strip, where restaurant-bar concepts "
            "like Ha Noi have opened since 2024. These areas attract a younger "
            "crowd and stay open late, contrasting with the village pace of "
            "Stony Stratford, where Mile Zero Coffee serves a neighbourhood of "
            "over 100 independent shops on the same High Street."
        ),
        (
            "MK lacks a signature dish in the way that Birmingham has the balti "
            "or Whitby has the fish supper, but it has always reflected the "
            "diversity of its planned population: South Asian, Vietnamese and "
            "Mediterranean cooking are all well represented. The food awards "
            "scene has matured too, with the Milton Keynes Food and Leisure "
            "Awards now providing a credible annual benchmark for the city's "
            "best independents."
        ),
    ],
    "visit": [
        (
            "The geography requires a little planning but rewards it. Stony "
            "Stratford is about four miles north-west of the city centre via "
            "the V4 or a direct bus from CMK; allow a morning there for coffee "
            "at Mile Zero and a browse of the High Street. The Hub and 12th "
            "Street are a short walk from Milton Keynes Central station, "
            "putting Maaya and Ha Noi within easy reach on foot."
        ),
        (
            "Wolverton, with the Craufurd Arms, sits between Stony Stratford "
            "and the city centre — a short bus ride or a 20-minute walk from "
            "CMK. A good day strings together a Stony Stratford coffee, a "
            "lunch or dinner at Maaya or Ha Noi in the centre, and a live-music "
            "evening at the Craufurd Arms. Check the Craufurd's gig listings "
            "online before you go; weekends often have ticketed events."
        ),
    ],
    "checklist": [
        "Start in Stony Stratford: coffee at Mile Zero, then explore the High Street and Odell's Yard",
        "Book Maaya at The Hub in advance, especially on weekends and award evenings",
        "Check the Craufurd Arms gig listings before heading to Wolverton for the evening",
        "Ha Noi on 12th Street stays open late Friday and Saturday - good for dinner into the night",
        "Milton Keynes Central station puts The Hub and 12th Street a 10-minute walk away",
    ],
    "what_to_order": (
        "Order with intent. At Ha Noi, the pho is the benchmark - pick your "
        "protein and take your time with it, or go for banh mi if you want "
        "something lighter. At Mile Zero, ask what single origin is on the "
        "espresso and pair it with whatever came in that morning. At Maaya, "
        "surrender to the chef's specials menu and ask the staff what the "
        "kitchen is proud of that week - the award wins are built on details "
        "that change with the season. At the Craufurd Arms, take a pint of "
        "whatever local guest ale is on the hand pump, find a table, and check "
        "the chalkboard for who's playing."
    ),
    "glance": [
        ("Best for a quick bite", "Ha Noi, for Vietnamese pho and banh mi on 12th Street"),
        ("Best for an occasion", "Maaya, for three-times MK Food Award-winning Indian at The Hub"),
        ("Best for atmosphere", "The Craufurd Arms, Wolverton's CAMRA Pub of the Year with live music"),
    ],
    "faq": [
        (
            "Where is the best independent restaurant in Milton Keynes?",
            "Maaya Indian Kitchen and Bar at The Hub in Central Milton Keynes has "
            "won Best Asian Restaurant at the MK Food and Leisure Awards three "
            "years running and has been recognised at the English Curry Awards. "
            "It serves modern Indian cooking using halal ingredients and takes bookings.",
        ),
        (
            "Where can I get the best coffee in Milton Keynes?",
            "Mile Zero Coffee on Stony Stratford High Street is a well-rated "
            "independent speciality roaster-cafe that received a 5-star food "
            "hygiene rating from Milton Keynes Council in February 2026. It sits "
            "on the most characterful independent shopping street in MK.",
        ),
        (
            "What is the best pub in Milton Keynes for real ale?",
            "The Craufurd Arms on Stratford Road in Wolverton was named Pub of "
            "the Year and Cider Pub of the Year by the Milton Keynes and North "
            "Bucks CAMRA branch for 2026, and features in the CAMRA Good Beer "
            "Guide 2026. It has four hand pumps and a rotating selection of "
            "local guest ales.",
        ),
        (
            "Is there a good Vietnamese restaurant in Milton Keynes?",
            "Ha Noi opened on 12th Street in Central Milton Keynes in August "
            "2025 and serves modern Vietnamese cuisine including pho, banh mi "
            "and pan-Asian street food dishes, paired with cocktails. It stays "
            "open late on Friday and Saturday evenings.",
        ),
        (
            "Which part of Milton Keynes has the best independent food scene?",
            "Stony Stratford, on the north-western edge of MK, has the longest "
            "established independent food quarter, with over 100 independent "
            "shops on the High Street, Odell's Yard market courtyard and "
            "specialist cafes and restaurants. The city centre Hub and 12th "
            "Street are the newer dining destinations.",
        ),
        (
            "Can you eat well in Milton Keynes without a car?",
            "Yes. Milton Keynes Central station puts The Hub and 12th Street "
            "within a 10-minute walk, and local buses connect the station to "
            "Stony Stratford and Wolverton. Maaya, Ha Noi and the Craufurd "
            "Arms are all reachable on public transport from the station.",
        ),
    ],
}
