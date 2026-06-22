# frags/rochdale.py — web-researched 2026-06-22
# Four venues confirmed currently trading:
#   Cuckoo's (takeaway) — FSA inspection 31 Mar 2025, open daily, Uber Eats live
#   SiRo' Mangia Bevi (cafe-bistro) — active summer/autumn 2025 per Rochdale Style + TripAdvisor
#   Wild Ginger (restaurant) — FSA 5-star Dec 2024, TripAdvisor reviews Jan/Apr 2025, ARTA 2025 nominee
#   The Baum (pub) — CAMRA Nat'l Pub of Year 2012, new ownership May 2025, Rochdale Style summer 2025

TOWNS["rochdale"] = {
    "region": "Greater Manchester",
    "population": "95,000",
    "nearby": ["Oldham", "Bury", "Heywood"],
    "meta_title": "Best Places to Eat in Rochdale: Local Food Guide",
    "meta_description": (
        "Rochdale food guide: karahi on Milkstone Road, Italian bistro on Baillie "
        "Street, an Indian grill and a CAMRA pub of the year. Read the guide."
    ),
    "trust_strip": (
        "From the South Asian karahi kitchens of Milkstone Road to a CAMRA national "
        "pub of the year on the birthplace of the Co-operative movement, Rochdale "
        "has one of Greater Manchester's most characterful independent food scenes"
    ),
    "snapshot": (
        "For a fast answer: Cuckoo's on Milkstone Road for a Pakistani karahi and "
        "roti in the heart of Rochdale's South Asian quarter, SiRo' Mangia Bevi on "
        "Baillie Street for authentic Italian small plates in a candlelit bistro, "
        "Wild Ginger in Littleborough for contemporary Indian with sizzling tandoori "
        "and saffron biryani, and The Baum on Toad Lane for seven rotating real ales "
        "in a former CAMRA national pub of the year. Four moods, one compact mill "
        "town with serious food credentials."
    ),
    "stats": [
        ("1844", "Year the Co-operative movement was born on Toad Lane"),
        ("Milkstone Road", "Heart of Rochdale's South Asian food quarter"),
        ("2012", "The Baum named CAMRA National Pub of the Year"),
        ("4", "Hand-picked independents"),
    ],
    "pivot_variant": "high-volume",
    "pivot_local_hook": (
        "Rochdale's South Asian takeaways and restaurant kitchens cook at high "
        "heat for long hours, with karahi and balti-style dishes throwing a dense "
        "load of spiced grease-laden vapour into canopies that run through the "
        "evening service and well beyond."
    ),
    "venues": [
        {
            "type": "Takeaway",
            "name": "Cuckoo's",
            "area": "42 Milkstone Road, Rochdale town centre",
            "cuisine": "Pakistani, halal karahi and curries",
            "body": (
                "Milkstone Road is the spine of Rochdale's South Asian food "
                "quarter, and Cuckoo's has been one of its most reliable draws "
                "for years. A no-frills halal takeaway open every day from "
                "11am to 11pm, it is built around the slow-cooked Pakistani "
                "classics that regulars drive across the borough for: a chicken "
                "or lamb karahi thick with tomato and spice, a chana daal that "
                "is rich and well-seasoned, shami kebabs and masala fish to "
                "start. The naans are freshly made and the portion sizes are "
                "not shy. Inspected by the Food Standards Agency in March 2025 "
                "and active on Uber Eats, Cuckoo's is a staple of a food street "
                "with more history than its strip-lit frontage suggests."
            ),
            "known_for": "Chicken and lamb karahi, shami kebabs and chana daal",
            "good_for": "A late-night halal takeaway that the locals swear by",
            "source_url": "https://www.ubereats.com/gb/store/cuckoos-takeway/bWg7FeJvS8O3DIHBPUfqiw",
            "verified": "2026-06-22",
        },
        {
            "type": "Cafe",
            "name": "SiRo' Mangia Bevi",
            "area": "16 Baillie Street, Rochdale town centre",
            "cuisine": "Italian cafe-bistro, small plates, wine",
            "body": (
                "Tucked into Baillie Street in the heart of Rochdale's emerging "
                "independent quarter, SiRo' Mangia Bevi opened around 2024 and "
                "quickly became the town's most talked-about Italian. The name "
                "means roughly eat-drink, and that is the brief: owner Danilo, "
                "who worked front-of-house at the respected San Carlo group, "
                "and chef Luca turn out authentic Italian small plates with "
                "bold, clean flavours. Risotto, antipasti, freshly made pasta "
                "and daily specials are the order of the day, all served in a "
                "warm, candlelit room with a carefully chosen wine list. It won "
                "a Rochdale Business Award for best start-up and has a near "
                "perfect TripAdvisor rating. Open Tuesday to Saturday; book ahead."
            ),
            "known_for": "Authentic Italian small plates, risotto and a serious wine list",
            "good_for": "An evening meal with real Italian soul in Rochdale town centre",
            "source_url": "https://www.tripadvisor.com/Restaurant_Review-g580426-d32977735-Reviews-SiRo_Mangia_Bevi_Cafe_Bistrot-Rochdale_Greater_Manchester_England.html",
            "verified": "2026-06-22",
        },
        {
            "type": "Restaurant",
            "name": "Wild Ginger",
            "area": "78-80 Church Street, Littleborough (5 miles east of Rochdale)",
            "cuisine": "Contemporary Indian, tandoori grill",
            "body": (
                "Wild Ginger occupies a stone-built terrace on the high street "
                "of Littleborough, the Pennine village on Rochdale's eastern "
                "edge, and it has built a following well beyond the postcode. "
                "The restaurant emerged from the site of a long-running Indian "
                "on Church Street and was reimagined as a contemporary grill "
                "with a creative menu: bao buns filled with tandoori chicken, "
                "saffron-kissed biryani, vegetarian dishes like Aloo Brie and "
                "Veg Manchurian Ball alongside traditional curries in generous "
                "bowl portions. A Food Standards Agency 5-star rating in "
                "December 2024 and a nomination for ARTA Regional Restaurant "
                "of the Year North West 2025 confirmed it as one of the most "
                "serious Indian tables in the borough. Evening only; "
                "reservations strongly advised."
            ),
            "known_for": "Contemporary Indian grill, saffron biryani and creative small plates",
            "good_for": "A proper sit-down Indian with real ambition, worth the drive",
            "source_url": "https://www.tripadvisor.com/Restaurant_Review-g580426-d31178527-Reviews-Wild_Ginger-Rochdale_Greater_Manchester_England.html",
            "verified": "2026-06-22",
        },
        {
            "type": "Pub",
            "name": "The Baum",
            "area": "33-37 Toad Lane, Rochdale Heritage Quarter",
            "cuisine": "Modern British pub food, seven rotating real ales",
            "body": (
                "Few pubs in England have a more evocative address than Toad "
                "Lane, the cobbled street in Rochdale's Heritage Quarter where "
                "the Rochdale Pioneers opened their first co-operative store in "
                "1844. The Baum sits a few doors down, a free-of-tie independent "
                "converted from a hardware store in the early 1980s and named, "
                "from the German, simply The Tree. It was crowned CAMRA National "
                "Pub of the Year in 2012 and has been a regional CAMRA winner "
                "multiple times since. Under new ownership from May 2025, it "
                "continues to pour up to seven rotating hand-pulled real ales "
                "and guest ciders alongside a menu built on quality British "
                "pub classics: hearty pies, bangers and mash, a rag pudding and "
                "a beef and bone marrow burger. Bare wood floors, green-painted "
                "snugs and a walled beer garden to the rear."
            ),
            "known_for": "Seven rotating real ales, CAMRA pedigree and Toad Lane location",
            "good_for": "A proper pint yards from where the Co-op movement began",
            "source_url": "https://camra.org.uk/pubs/baum-rochdale-152799",
            "verified": "2026-06-22",
        },
    ],
    "food_scene": [
        (
            "Rochdale's food map splits between two very different worlds. "
            "Milkstone Road and the streets radiating south from the town "
            "centre form one of Greater Manchester's most concentrated South "
            "Asian food corridors: Pakistani karahi houses, Bangladeshi "
            "restaurants and South Asian sweet shops that have served the "
            "borough's substantial Muslim community for decades. The area "
            "reflects a Rochdale that is roughly 34 per cent South Asian "
            "by heritage, one of the highest proportions in the north-west."
        ),
        (
            "In the town centre, Baillie Street and the alleys around it "
            "have become home to an emerging cluster of independent bars and "
            "restaurants with genuine ambition. Wine bar Vicolo Del Vino "
            "pours eighty wines in a candlelit brick cellar; La Mancha "
            "serves tapas off a cobbled lane. The Rochdale BID has pushed "
            "the town as a foodie destination on a par with Altrincham and "
            "Stockport, and the comparison is not entirely fanciful."
        ),
        (
            "A short journey into the borough opens up further layers. "
            "Littleborough to the east sits in the Pennines with its own "
            "restaurant scene; the Hollingworth Lake area draws weekend "
            "walkers in need of food. And through it all, the historic "
            "Toad Lane still pulses on a Friday night, the CAMRA pubs "
            "and pizza cellars keeping company with the museum that marks "
            "the street where fair commerce was reinvented in 1844."
        ),
    ],
    "visit": [
        (
            "Rochdale town centre is compact and walkable. The Baum on "
            "Toad Lane, Baillie Street and the Milkstone Road corridor "
            "are all within fifteen minutes on foot of one another and "
            "a short walk from the Metrolink tram stop. Wild Ginger in "
            "Littleborough is five miles east: drive, or take the train "
            "from Rochdale station (the Calder Valley line stops at "
            "Littleborough)."
        ),
        (
            "Plan a varied day: a daytime Italian lunch at SiRo' on "
            "Baillie Street, a wander up to the Rochdale Pioneers Museum "
            "on Toad Lane, then a pint at The Baum next door. An evening "
            "booking at Wild Ginger in Littleborough makes a worthy "
            "second stop. The karahi houses on Milkstone Road are open "
            "late for a no-frills finish."
        ),
    ],
    "checklist": [
        "Book Wild Ginger in Littleborough in advance - it fills quickly at weekends",
        "Walk Toad Lane before your pint at The Baum - the Pioneers Museum is next door",
        "SiRo' Mangia Bevi does not open Sunday or Monday; plan accordingly",
        "Cuckoo's on Milkstone Road is open until 11pm every day for a late bite",
        "Take the Metrolink into Rochdale centre and the Calder Valley train to Littleborough",
    ],
    "what_to_order": (
        "Order with intent. At Cuckoo's, a lamb or chicken karahi with naan "
        "and a portion of chana daal, eaten warm. At SiRo' Mangia Bevi, "
        "ask the specials and lean into the risotto or pasta of the day with "
        "a glass from their wine list. At Wild Ginger, the saffron biryani or "
        "a tandoori mixed grill and one of the creative bao bun starters. "
        "At The Baum, a pint of whichever real ale has just come on the "
        "hand-pull, taken in a wooden snug or the walled beer garden."
    ),
    "glance": [
        ("Best for a quick bite", "Cuckoo's on Milkstone Road, for a karahi and naan any day until 11pm"),
        ("Best for an occasion", "Wild Ginger in Littleborough, for contemporary Indian with real ambition"),
        ("Best for atmosphere", "The Baum on Toad Lane, a CAMRA pub of the year on the most storied street in Rochdale"),
    ],
    "faq": [
        (
            "Where can I eat authentic Pakistani food in Rochdale?",
            "Milkstone Road in the town centre is the heart of Rochdale's South "
            "Asian food quarter. Cuckoo's at number 42 is a long-standing halal "
            "takeaway open every day until 11pm, known for its karahi, shami "
            "kebabs and chana daal."
        ),
        (
            "What is The Baum and why is it famous?",
            "The Baum is a free-of-tie real ale pub on Toad Lane in Rochdale's "
            "Heritage Quarter. It was crowned CAMRA National Pub of the Year in "
            "2012, has been a regional CAMRA winner multiple times, and pours up "
            "to seven rotating hand-pulled ales. It sits a few doors from the "
            "Rochdale Pioneers Museum, where the co-operative movement began in 1844."
        ),
        (
            "Is there a good Italian restaurant in Rochdale?",
            "SiRo' Mangia Bevi at 16 Baillie Street is an authentic Italian "
            "cafe-bistro run by Danilo, a San Carlo group alumnus, and chef Luca. "
            "It won a Rochdale Business Award for best start-up and earns near-"
            "perfect reviews for its small plates, risotto and wine list. "
            "Open Tuesday to Saturday."
        ),
        (
            "What Indian restaurant should I visit near Rochdale?",
            "Wild Ginger at 78-80 Church Street, Littleborough, five miles east "
            "of Rochdale town centre, is a contemporary Indian grill with a "
            "5-star Food Standards Agency rating (December 2024) and a nomination "
            "for ARTA Regional Restaurant of the Year North West 2025. Book ahead."
        ),
        (
            "What is Rochdale famous for in terms of food and history?",
            "Rochdale is the birthplace of the modern co-operative movement: the "
            "Rochdale Pioneers opened their first store on Toad Lane in 1844, "
            "selling unadulterated food at fair prices. The town also has one of "
            "Greater Manchester's most concentrated South Asian food corridors on "
            "Milkstone Road, and a growing independent bar and restaurant scene "
            "in the Baillie Street Quarter."
        ),
        (
            "Can I reach Rochdale and Littleborough by public transport?",
            "Yes. Rochdale town centre is on the Manchester Metrolink tram "
            "network. Littleborough, home to Wild Ginger, is five miles east "
            "and served by the Calder Valley rail line from Rochdale station, "
            "with regular trains throughout the day and evening."
        ),
    ],
}
