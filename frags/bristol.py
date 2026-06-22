TOWNS = {}

# --------------------------------------------------------------------------
# BRISTOL — web-researched June 2026
# --------------------------------------------------------------------------
TOWNS["bristol"] = {
    "region": "the South West",
    "population": "470K",
    "nearby": ["Bath", "Weston-super-Mare", "Portishead"],
    "meta_title": "Best Places to Eat in Bristol: Local Food Guide",
    "meta_description": (
        "Where to eat in Bristol: harbourside pizza, a Stokes Croft "
        "brunch cafe, a Michelin-starred farm bistro and a West Country "
        "cider freehouse. Read the guide."
    ),
    "trust_strip": (
        "From a 1834 cider freehouse on Spike Island to the UK's Restaurant "
        "of the Year 2026, Bristol is one of the most exciting food cities in Britain"
    ),
    "snapshot": (
        "For a fast answer: Bertha's Pizza at Wapping Wharf for "
        "wood-fired sourdough pizza on the harbourside, The Crafty Egg "
        "on Stokes Croft for Bristol's best-loved brunch cafe, Wilsons "
        "on Chandos Road for a Michelin-starred farm-to-table bistro, "
        "and The Orchard Inn on Spike Island for West Country cider in "
        "an independent freehouse that has been pouring since 1834. "
        "Four moods across four of the city's most distinct neighbourhoods."
    ),
    "stats": [
        ("470K", "Population (approx)"),
        ("1743", "Year St Nicholas Market was founded"),
        ("Wapping Wharf", "Bristol's harbourside independent food quarter"),
        ("4", "Hand-picked independents"),
    ],
    "pivot_variant": "high-volume",
    "pivot_local_hook": (
        "Bristol's kitchens run at volume and variety: wood-fired pizza ovens, "
        "high-turnover brunch grills, tasting-menu stoves and pub fry-ups all "
        "push a heavy load of grease-laden vapour into their canopies "
        "every service across the city's many distinct food quarters."
    ),
    "venues": [
        {
            "type": "Takeaway/Casual",
            "name": "Bertha's Pizza",
            "area": "Wapping Wharf, harbourside",
            "cuisine": "Neapolitan sourdough pizza",
            "body": (
                "Bertha's story begins in a London back garden with a Sheffield steel "
                "wood-fired oven, a craving for change and a yellow Land Rover. Graham, "
                "Kate and Meg toured Bristol's markets with the wood-fired oven in the back "
                "before opening a permanent home at Wapping Wharf in summer 2016, inside "
                "the converted old jail stables on the harbourside. The pizza is Neapolitan "
                "in spirit: slow-fermented sourdough bases charred in a wood-fired oven, "
                "topped simply with quality ingredients, and finished with homemade gelato "
                "or tiramisu. It is a family-run operation in the truest sense, with walk-ins "
                "welcome and takeaway available at the bar. Dine with the floating harbour "
                "in view and the M Shed across the water."
            ),
            "known_for": "Wood-fired sourdough pizza and homemade gelato since 2016",
            "good_for": "A casual harbourside dinner, walk-ins welcome",
            "source_url": "https://berthas.co.uk/",
            "verified": "2026-06-22",
        },
        {
            "type": "Cafe",
            "name": "The Crafty Egg",
            "area": "113 Stokes Croft",
            "cuisine": "Brunch, locally sourced all-day cafe",
            "body": (
                "The Crafty Egg opened in February 2016 on Stokes Croft with a single hot "
                "plate, a toaster and a cheat-sheet on the difference between a latte and a "
                "cappuccino. Ten years on, it is one of Bristol's most fiercely loved "
                "neighbourhood cafes, drawing weekend queues that stretch down the pavement "
                "of the city's most colourful street. The menu is rooted in locally sourced "
                "produce: eggs done every way, hearty griddle-pan dishes, creative vegetarian "
                "and vegan options, and freshly brewed coffee. The decor is vivid and "
                "welcoming, the atmosphere is pure Stokes Croft, and a second branch in "
                "Fishponds opened in 2022. Open daily from 8am, walk-ins only."
            ),
            "known_for": "Bristol's best-loved brunch queue, eggs and local produce since 2016",
            "good_for": "A weekend brunch in the heart of Bristol's creative quarter",
            "source_url": "https://www.thecraftyegg.co.uk/stokes-croft",
            "verified": "2026-06-22",
        },
        {
            "type": "Restaurant",
            "name": "Wilsons",
            "area": "24 Chandos Road, Redland",
            "cuisine": "Farm-to-table modern British",
            "body": (
                "Jan Ostle and Mary Wilson opened their 24-cover neighbourhood bistro on "
                "Chandos Road in 2016 with a simple ambition: to cook the produce of a "
                "working market garden with skill and care. The two-acre garden at Barrow "
                "Gurney, twenty minutes from the restaurant, supplies nearly all the "
                "vegetables, herbs and fruit for a six-course tasting menu that changes "
                "entirely with the seasons. The rewards have accumulated: a Michelin Green "
                "Star in 2022, a full Michelin Star in February 2025, and in January 2026 "
                "the accolade of SquareMeal UK Restaurant of the Year. A more affordable "
                "menu du jour runs at lunch Wednesday to Friday. Book well ahead."
            ),
            "known_for": "Michelin Star and Green Star, farm-grown produce, UK Restaurant of Year 2026",
            "good_for": "A landmark meal in a quiet Redland dining room; book early",
            "source_url": "https://www.wilsonsbristol.co.uk/",
            "verified": "2026-06-22",
        },
        {
            "type": "Pub",
            "name": "The Orchard Inn",
            "area": "12 Hanover Place, Spike Island",
            "cuisine": "West Country cider, real ale, bar food",
            "body": (
                "Tucked on the corner of Spike Island by the floating harbour, The Orchard "
                "Inn has been pulling pints since at least 1834, when it traded as the "
                "White Horse. Today it is one of Bristol's few remaining freehouses and the "
                "city's most celebrated cider pub, stocking around fifteen still and seven "
                "sparkling West Country ciders on any given day, alongside two regular cask "
                "ales and a guest. The Hecks house cider is poured from gravity. Multiple "
                "CAMRA Regional Cider Pub of the Year awards and a national title in 2009 "
                "confirm what regulars already know: this is the place to drink real cider "
                "in Bristol. Blues jams most weeks, doorstop sandwiches behind the bar, "
                "and a dog-friendly policy round out one of the best unassuming pubs in "
                "the South West."
            ),
            "known_for": "Up to 15 West Country ciders on gravity, CAMRA national award winner",
            "good_for": "A proper cider education in a historic harbourside freehouse",
            "source_url": "https://camra.org.uk/pubs/orchard-inn-bristol-114074",
            "verified": "2026-06-22",
        },
    ],
    "food_scene": [
        (
            "Bristol's food map is really a map of its neighbourhoods. Wapping Wharf, the "
            "converted shipping container quarter on the south side of the floating harbour, "
            "holds an absurd concentration of independent restaurants, bakeries and bars "
            "within a few hundred metres of the water. It sits alongside the historic "
            "M Shed museum and next to Spike Island, where The Orchard Inn has been "
            "pouring West Country cider since the early Victorian era."
        ),
        (
            "North of the centre, Stokes Croft and Gloucester Road form the city's most "
            "independent high street: independent traders have deliberately kept the chains "
            "out, and the result is a kilometre-long run of cafes, delis, breweries and "
            "restaurants that changes faster than anywhere else in Bristol. The Crafty Egg "
            "is the district's totemic brunch spot; Extract Coffee and Triple Co Roast "
            "supply serious speciality beans to the wider city."
        ),
        (
            "St Nicholas Market, founded in 1743 and housed in an 18th-century Exchange "
            "building, remains Bristol's indoor street-food heart, with traders serving "
            "everything from Syrian falafel to Pieminister's award-winning pies. And in "
            "the residential streets of Redland and Clifton, neighbourhood bistros like "
            "Wilsons and Dongnae show that Bristol's most exciting dining now happens "
            "far from the city centre, in small rooms with big kitchens."
        ),
    ],
    "visit": [
        (
            "Bristol is a city of hills and distinct quarters, each with its own food "
            "character. Wapping Wharf and Spike Island sit on the south bank of the "
            "floating harbour and are an easy walk from the city centre or a short "
            "ride from Bristol Temple Meads station. Stokes Croft is a mile north "
            "along the Gloucester Road corridor, well served by buses from the centre."
        ),
        (
            "A day shaped around this guide flows naturally: brunch at The Crafty Egg "
            "on Stokes Croft, an afternoon exploring the harbourside at Wapping Wharf "
            "with pizza from Bertha's, cider at The Orchard Inn on Spike Island, and "
            "Wilsons held back for a special evening booking. Reserve Wilsons weeks "
            "in advance; everything else is walk-in friendly."
        ),
    ],
    "checklist": [
        "Arrive early at The Crafty Egg on weekdays to avoid the famous weekend queues",
        "Book Wilsons well ahead - 24 covers fill fast and the lunch menu is the best-value entry point",
        "Visit The Orchard Inn in the afternoon for the full cider list at its best",
        "Walk the floating harbour between Wapping Wharf and Spike Island - it is a fine short route",
        "Bristol Temple Meads is the train hub; Wapping Wharf and the centre are a 20-minute walk",
    ],
    "what_to_order": (
        "Order with intent. At Bertha's Pizza, a wood-fired sourdough pizza fresh from the oven "
        "and a scoop of homemade gelato to finish. At The Crafty Egg, whatever egg dish is "
        "on that morning alongside a flat white. At Wilsons, surrender to the full six-course "
        "tasting menu and let the kitchen's garden drive the choices. At The Orchard Inn, "
        "ask the bar for a recommendation from the cider board and take a doorstop sandwich "
        "to go with it."
    ),
    "glance": [
        ("Best for a quick bite", "Bertha's Pizza at Wapping Wharf, wood-fired and walk-in"),
        ("Best for an occasion", "Wilsons, Michelin-starred and UK Restaurant of Year 2026"),
        ("Best for atmosphere", "The Orchard Inn, 190 years of West Country cider on Spike Island"),
    ],
    "faq": [
        (
            "What is the best restaurant in Bristol right now?",
            "Wilsons on Chandos Road in Redland was named SquareMeal UK Restaurant of the Year "
            "2026 and holds a Michelin Star and Green Star. The 24-cover bistro, run by Jan Ostle "
            "and Mary Wilson since 2016, grows most of its produce at its own market garden and "
            "offers a six-course tasting menu that changes with the seasons."
        ),
        (
            "Where should I eat in Stokes Croft?",
            "The Crafty Egg at 113 Stokes Croft is Bristol's best-loved brunch cafe, open daily "
            "from 8am with locally sourced eggs, griddle-pan dishes and freshly brewed coffee. "
            "It has been drawing weekend queues since it opened in 2016."
        ),
        (
            "What is the best pub in Bristol for cider?",
            "The Orchard Inn on Hanover Place, Spike Island, is Bristol's most celebrated cider "
            "pub and a multiple CAMRA award winner. As one of the city's few remaining freehouses "
            "it stocks around fifteen West Country ciders on any given day, poured from gravity."
        ),
        (
            "Where can I get good pizza in Bristol?",
            "Bertha's Pizza at Wapping Wharf is a family-run Bristol independent that has been "
            "firing Neapolitan-inspired sourdough pizzas in a wood-fired oven since 2016. "
            "Walk-ins are welcome and takeaway is available at the bar."
        ),
        (
            "Where is the best place to eat on the Bristol harbourside?",
            "Wapping Wharf on the south bank of the floating harbour houses a cluster of "
            "independent restaurants and bars, with Bertha's Pizza among the best. Spike Island "
            "next door is home to The Orchard Inn, one of the finest cider pubs in Britain."
        ),
        (
            "Does Bristol have any Michelin-starred restaurants?",
            "Yes. Wilsons on Chandos Road in Redland holds both a Michelin Star (awarded 2025) "
            "and a Michelin Green Star for sustainability. Dongnae, also on Chandos Road, is "
            "Michelin-recommended and was named Chef to Watch by the Good Food Guide in 2026."
        ),
    ],
}
