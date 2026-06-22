TOWNS = {}

# --------------------------------------------------------------------------
# ABERDEEN — web-researched 2026-06-22
# --------------------------------------------------------------------------
TOWNS["aberdeen"] = {
    "region": "Scotland",
    "population": "230K",
    "nearby": ["Arbroath", "Elgin", "Dundee"],
    "meta_title": "Best Places to Eat in Aberdeen: Local Food Guide",
    "meta_description": (
        "Aberdeen: 1978 family chippie, zero-waste vegan cafe, "
        "Michelin-recommended modern Scottish seafood and the local craft "
        "brewery tap room. Read the guide."
    ),
    "trust_strip": (
        "From a 1978 harbour-city chippie to a Michelin-recommended seafood "
        "kitchen, Aberdeen's independent food scene punches well above its weight "
        "on the North Sea coast"
    ),
    "snapshot": (
        "For a fast answer: Mike's Famous Fish and Chips on Mugiemoss Road for "
        "a North Sea haddock supper from a family business trading since 1978, "
        "Foodstory on Thistle Street for Aberdeen's favourite zero-waste vegetarian "
        "cafe, Moonfish Cafe on Correction Wynd for Michelin-recommended modern "
        "Scottish cooking, and Fierce Bar on Exchequer Row for craft beer poured "
        "by the city's own award-winning independent brewery. Four moods, one "
        "Granite City."
    ),
    "stats": [
        ("1978", "Year Mike's Famous Fish and Chips first opened"),
        ("2004", "Year Moonfish Cafe opened on Correction Wynd"),
        ("Granite City", "Aberdeen's nickname for its silver-grey granite skyline"),
        ("4", "Hand-picked independents"),
    ],
    "pivot_variant": "coastal",
    "pivot_local_hook": (
        "Aberdeen's kitchens carry a heavy coastal grease load: the North Sea "
        "fishing trade has kept fryers running at full tilt for generations, "
        "and the city's harbour-side and city-centre restaurants push fish and "
        "shellfish through their canopies every service, year-round."
    ),
    "venues": [
        {
            "type": "Takeaway",
            "name": "Mike's Famous Fish and Chips",
            "area": "Mugiemoss Road, Bucksburn (north Aberdeen)",
            "cuisine": "Fish and chips, North Sea haddock",
            "body": (
                "Mike's Famous Fish and Chips has been a family business since 1978, "
                "nearly five decades of cooking some of the best fish suppers in "
                "the north-east of Scotland. The family-run fryer on Mugiemoss Road "
                "sources its haddock daily from the North Sea and has built a "
                "devoted following among Aberdonians who know that the city's "
                "fishing heritage deserves better than a chain. The credentials "
                "are serious: shortlisted in the National Fish and Chip Awards "
                "Top 40 for 2025 and the FRY Awards Top 50 in 2024. The classic "
                "order is a large haddock supper, battered in the traditional "
                "Scottish style and fried golden, with chunky chips and a "
                "generous scatter of salt. The rowie - Aberdeen's own flat, "
                "buttery bread roll - is the local benchmark: this is its "
                "savoury counterpart in fried form."
            ),
            "known_for": "North Sea haddock supper, family-run since 1978, National Fish and Chip Awards Top 40 2025",
            "good_for": "A legendary family chippie supper in Aberdeen's north",
            "source_url": "https://www.tripadvisor.co.uk/Restaurant_Review-g186487-d3258542-Reviews-Mike_s_Famous_Fish_and_Chips-Aberdeen_Aberdeenshire_Scotland.html",
            "verified": "2026-06-22",
        },
        {
            "type": "Cafe",
            "name": "Foodstory",
            "area": "13-15 Thistle Street, west end city centre",
            "cuisine": "Vegetarian and vegan, speciality coffee",
            "body": (
                "Foodstory launched in November 2013 through a Kickstarter campaign "
                "with a simple idea: build a space where anyone could eat great, "
                "healthy food and feel part of a community. The founders made most "
                "of the furniture themselves from salvaged parts and have barely "
                "changed the spirit since. The rambling Thistle Street flagship "
                "serves vegetarian and vegan food made from scratch - soups, "
                "salad bowls, cinnamon rolls, brownies, lentil dishes - alongside "
                "Scottish-roasted speciality coffee. Foodstory now runs a beach "
                "coffee hut, a zero-waste cafe on the university campus and a "
                "satellite in Edinburgh, but the Thistle Street original remains "
                "the heart of it: an open-mic venue on Wednesday evenings and one "
                "of Aberdeen's most genuinely community-minded dining rooms."
            ),
            "known_for": "Scratch-made vegetarian food, speciality coffee, zero-waste ethos since 2013",
            "good_for": "A relaxed, community-minded lunch or coffee in the city-centre west end",
            "source_url": "https://www.yelp.co.uk/biz/foodstory-cafe-aberdeen",
            "verified": "2026-06-22",
        },
        {
            "type": "Restaurant",
            "name": "Moonfish Cafe",
            "area": "9 Correction Wynd, Merchant Quarter",
            "cuisine": "Modern British, seasonal Scottish seafood",
            "body": (
                "Moonfish Cafe opened in 2004 on Correction Wynd, a medieval "
                "lane in Aberdeen's Merchant Quarter overlooked by the 12th-century "
                "Kirk of St Nicholas. Head chef Brian McLeish, a MasterChef: "
                "The Professionals finalist, runs a constantly changing menu of "
                "modern British cooking built on local and seasonal Scottish "
                "produce - wild halibut, baked scallops, grilled hake - "
                "accompanied by a natural and biodynamic wine list and an "
                "extensive gin selection. Michelin-recommended and holding an "
                "AA Rosette, the intimate dining room takes bookings for lunch "
                "Tuesday to Saturday and dinner Tuesday to Saturday, and remains "
                "one of the most consistent small restaurants in Scotland. "
                "For the full picture of what Aberdeen's coast can produce "
                "on a plate, this is the table to book."
            ),
            "known_for": "Michelin-recommended modern Scottish seafood on a medieval lane, open since 2004",
            "good_for": "A special-occasion dinner in Aberdeen's historic Merchant Quarter",
            "source_url": "https://www.yelp.co.uk/biz/moonfish-cafe-aberdeen",
            "verified": "2026-06-22",
        },
        {
            "type": "Pub",
            "name": "Fierce Bar",
            "area": "4-6 Exchequer Row, city centre (off Union Street)",
            "cuisine": "Craft beer, bar snacks",
            "body": (
                "Fierce Beer began in Aberdeen in 2016 when two former oil-and-gas "
                "engineers left their careers to brew the bold, hop-forward craft "
                "beer they felt Scotland was missing. By 2017 they had won Scottish "
                "Brewery of the Year, and by 2018 they had opened Fierce Bar on "
                "Exchequer Row, just off Union Street in the heart of the city. "
                "The tap room pours the Fierce core range and limited releases "
                "across 20 taps, from sessionable pilsners to barrel-aged stouts, "
                "with guest beers and a rare whisky selection alongside. The "
                "brewery - still independently owned and Aberdeen-born - racked "
                "up 35 finalist spots at the 2024 Scottish Beer Awards across "
                "17 categories. For craft beer in the Granite City, there is "
                "nowhere that comes closer to the source."
            ),
            "known_for": "20 taps of Aberdeen-brewed Fierce craft beer, Scottish Brewery of the Year",
            "good_for": "A serious craft beer session in the city's own award-winning brewery bar",
            "source_url": "https://www.tripadvisor.co.uk/Restaurant_Review-g186487-d15795771-Reviews-Fierce_Bar_Aberdeen-Aberdeen_Aberdeenshire_Scotland.html",
            "verified": "2026-06-22",
        },
    ],
    "food_scene": [
        (
            "Aberdeen's food geography runs from the granite-walled city centre outward "
            "to its harbour and coast. Union Street is the main commercial spine, but "
            "the more interesting eating lies in the streets around it: the Belmont "
            "Quarter, where independent cafes and bars have colonised the cobbled lanes, "
            "and the Merchant Quarter around Correction Wynd and Schoolhill, where the "
            "medieval street plan has sheltered small restaurants for decades. The "
            "rowie - a flat, flaky, butter-and-lard roll unique to Aberdeen - is the "
            "city's most totemic food, invented for North Sea fishermen who needed "
            "bread that would last a fortnight at sea without going stale."
        ),
        (
            "Seafood is the strand that runs through everything. Aberdeen spent centuries "
            "as one of Britain's busiest fishing ports, and the North Sea catch still "
            "defines what the city eats: haddock battered and fried in the traditional "
            "Scottish style, line-caught fish on restaurant menus, herring cured and "
            "smoked in the Aberdeenshire tradition. The harbour at Footdee, the "
            "historic fishing village known locally as Fittie, sits at the mouth of "
            "the River Dee and has defined Aberdeen's relationship with the sea for "
            "centuries. The Silver Darling, in the former Customs House on Pocra Quay, "
            "began its story in 1986 as the city's seafood flagship - the restaurant "
            "is named after the herring themselves, once so economically vital they "
            "were called the silver darlings."
        ),
        (
            "Beyond the fish, Aberdeen has developed a credible independent cafe scene "
            "centred on Thistle Street and the west end, a craft-beer culture built "
            "around the Fierce Brewery that launched in 2016, and a quiet but growing "
            "fine-dining ambition anchored by Michelin-recommended Moonfish Cafe. "
            "The city has also embraced the food-market revival: the weekly farmers "
            "market at St Nicholas Market brings local Aberdeenshire producers into "
            "the centre, giving the food scene a regional connection that larger, "
            "more generic cities have lost."
        ),
    ],
    "visit": [
        (
            "The compact city centre makes getting around straightforward. Moonfish Cafe "
            "on Correction Wynd and Fierce Bar on Exchequer Row are both a short walk "
            "from Union Street; Foodstory on Thistle Street is ten minutes west on foot. "
            "Mike's Famous Fish and Chips is on Mugiemoss Road in Bucksburn, about "
            "three miles north of the centre - a short taxi or bus ride, and worth "
            "planning as a standalone stop rather than part of a city-centre loop."
        ),
        (
            "A logical Aberdeen food day might start with coffee and cake at Foodstory, "
            "move to the Merchant Quarter for a look at Correction Wynd and the Kirk "
            "of St Nicholas before booking Moonfish for the evening, then end with "
            "pints at Fierce Bar - its twenty taps and late Fridays and Saturday "
            "hours make it a natural final stop. If you're starting with a fish supper, "
            "Mike's on Mugiemoss Road is best visited at lunchtime when the haddock "
            "is freshest, before heading into the centre."
        ),
    ],
    "checklist": [
        "Begin at Foodstory on Thistle Street for vegetarian brunch and a Scottish-roasted flat white",
        "Walk east to Correction Wynd and book a table at Moonfish Cafe for the evening",
        "Head to Mike's Famous Fish and Chips on Mugiemoss Road for the definitive Aberdeen haddock supper",
        "End the night at Fierce Bar on Exchequer Row with a flight across the 20 Fierce taps",
        "Look out for the Saturday farmers market at St Nicholas Market for local Aberdeenshire produce",
    ],
    "what_to_order": (
        "Order with intent. At Mike's Famous Fish and Chips, a large haddock supper "
        "in traditional Scottish batter with chunky chips - the North Sea fish is "
        "sourced daily and the family have been frying it right since 1978. At "
        "Foodstory, the daily salad bowl with homemade hummus or whatever soup is "
        "on, alongside a flat white from the Scottish-roasted house blend. At "
        "Moonfish Cafe, follow the fish: the wild halibut and baked scallops are "
        "signatures, and the natural wine list is worth exploring. At Fierce Bar, "
        "ask the staff which limited release is on - they know the range "
        "better than anyone - and order a flight to span the pilsners and the "
        "barrel-aged stouts."
    ),
    "glance": [
        ("Best for a quick bite", "Mike's Famous Fish and Chips, for a North Sea haddock supper from a 1978 family fryer"),
        ("Best for an occasion", "Moonfish Cafe, Michelin-recommended modern Scottish cooking on a medieval lane"),
        ("Best for atmosphere", "Fierce Bar, 20 taps of Aberdeen-born craft beer on Exchequer Row"),
    ],
    "faq": [
        (
            "Where can I get the best fish and chips in Aberdeen?",
            "Mike's Famous Fish and Chips on Mugiemoss Road, a family business since "
            "1978, is shortlisted in the National Fish and Chip Awards Top 40 for 2025 "
            "and the FRY Awards Top 50 in 2024. They source haddock daily from the "
            "North Sea and fry it in the traditional Scottish batter."
        ),
        (
            "Which Aberdeen cafe is best for speciality coffee and vegetarian food?",
            "Foodstory on Thistle Street, opened in 2013 via a Kickstarter campaign, "
            "serves scratch-made vegetarian and vegan food alongside Scottish-roasted "
            "speciality coffee. The rambling west-end flagship also hosts open-mic "
            "nights and runs a zero-waste cafe on the university campus."
        ),
        (
            "Does Aberdeen have a Michelin-recommended restaurant?",
            "Yes. Moonfish Cafe at 9 Correction Wynd in the Merchant Quarter has been "
            "Michelin-recommended since its opening in 2004. Chef Brian McLeish runs "
            "a constantly changing modern British menu built on local Scottish seafood "
            "including wild halibut, baked scallops and grilled hake, with a natural "
            "and biodynamic wine list."
        ),
        (
            "What is the best craft beer bar in Aberdeen?",
            "Fierce Bar at 4-6 Exchequer Row, the flagship bar of Aberdeen-born "
            "Fierce Beer (founded 2016), pours 20 taps of its own core range and "
            "limited releases alongside guest beers and rare whisky. Fierce was "
            "named Scottish Brewery of the Year and racked up 35 finalist spots at "
            "the 2024 Scottish Beer Awards."
        ),
        (
            "What is Aberdeen famous for eating?",
            "The rowie - also called a buttery or Aberdeen roll - is the city's most "
            "iconic food: a flat, flaky, salt-forward bread roll made with butter and "
            "lard, originally baked for North Sea fishermen who needed provisions that "
            "would not go stale at sea. Fresh North Sea haddock, fried in traditional "
            "Scottish batter, is the other great Aberdeen staple, and the city's "
            "harbour heritage makes seafood central to the local food identity."
        ),
        (
            "Are there good independent restaurants near Aberdeen city centre?",
            "Yes. Moonfish Cafe on Correction Wynd, Foodstory on Thistle Street and "
            "Fierce Bar on Exchequer Row are all within a short walk of Union Street. "
            "The Belmont Quarter and the Merchant Quarter hold the city's most "
            "characterful independent cafes, bars and restaurants, away from the "
            "chain-dominated main drag."
        ),
    ],
}
