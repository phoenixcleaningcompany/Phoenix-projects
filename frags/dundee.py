TOWNS = {}

# --------------------------------------------------------------------------
# DUNDEE — web-researched 2026-06-22
# Four venues confirmed currently trading via live web checks.
# Nearby towns all verified against eat_towns.csv.
# --------------------------------------------------------------------------
TOWNS["dundee"] = {
    "region": "Scotland",
    "population": "150K",
    "nearby": ["Perth", "Arbroath", "Kirkcaldy"],
    "meta_title": "Best Places to Eat in Dundee: Local Food Guide",
    "meta_description": (
        "Dundee food picks: Perth Road Turkish gem open since 1982, "
        "West End speciality cafe, Italian steakhouse and a CAMRA "
        "Pub of the Year. Read the guide."
    ),
    "trust_strip": (
        "From a 40-year Turkish institution on Perth Road to a CAMRA Pub of "
        "the Year Edwardian bar, Dundee's independent food scene quietly "
        "punches above its weight on the banks of the Tay"
    ),
    "snapshot": (
        "For a fast answer: Agacan on Perth Road for a Turkish kebab and "
        "meze in the art-crammed institution that has fed the West End since "
        "1982, Pacamara Food and Drink on Perth Road for Dundee's favourite "
        "West End speciality coffee and brunch cafe, Don Padrino on Tay "
        "Square for dry-aged Scottish steaks and fresh local seafood in a "
        "lively Italian brasserie beside Dundee Rep, and the Speedwell Bar "
        "on Perth Road for a pint in a magnificent 1903 Edwardian interior "
        "that Tayside CAMRA has named Pub of the Year multiple times. "
        "Four moods, one Tay-side city of jute, jam and journalism."
    ),
    "stats": [
        ("150K", "Population (approx)"),
        ("1982", "Year Agacan first opened on Perth Road"),
        ("1903", "Year the Speedwell Bar was built"),
        ("4", "Hand-picked independents"),
    ],
    "pivot_variant": "high-volume",
    "pivot_local_hook": (
        "Dundee's kitchens carry a sustained and varied grease load: the "
        "charcoal-grilled kebabs and high-temperature doner rotisseries of "
        "Perth Road, the brunch flat-tops of the West End cafe strip, and "
        "the steak grills and seafood fryers of the waterfront and Tay "
        "Square all push a steady burden of grease-laden vapour through "
        "their canopies across every busy service."
    ),
    "venues": [
        {
            "type": "Takeaway/Casual",
            "name": "Agacan",
            "area": "113 Perth Road, West End",
            "cuisine": "Turkish kebab and meze",
            "body": (
                "Agacan opened on Perth Road in 1982 and has not really "
                "changed since, which is exactly the point. The small "
                "dining room doubles as an art gallery: walls, tables, "
                "chairs and even the doorstep are covered in oils, "
                "watercolours and painted mosaics, giving the place the "
                "feel of an eccentric Turkish sitting room rather than a "
                "restaurant. The menu has remained largely the same for "
                "over forty years: authentic kebabs, meze plates, freshly "
                "baked bread and vegetarian dishes cooked with the same "
                "care as the meat. Thursday to Sunday, 5 to 9:30pm only, "
                "which keeps standards high and demand higher. Regular "
                "diners plan a week ahead for a table. For Dundee food "
                "lovers, this is the place that defines what a neighbourhood "
                "institution looks like: singular, unwavering and "
                "unmissable."
            ),
            "known_for": "Turkish kebab and meze in a 40-year-old art-filled institution on Perth Road",
            "good_for": "An atmospheric and authentic West End supper with real local character",
            "source_url": "https://www.yelp.com/biz/agacan-kebab-house-dundee",
            "verified": "2026-06-22",
        },
        {
            "type": "Cafe",
            "name": "Pacamara Food and Drink",
            "area": "302 Perth Road, West End",
            "cuisine": "Speciality coffee, brunch and lunch",
            "body": (
                "Pacamara sits at the quieter upper end of Perth Road and "
                "has become the West End's go-to for serious coffee and "
                "food cooked with genuine care. The licensed cafe sources "
                "beans from respected UK speciality roasters and takes its "
                "brew methods as seriously as any dedicated espresso bar, "
                "while the food menu lifts well above cafe standard: "
                "shakshuka, Colombian eggs, bubble and squeak benny, "
                "brioche French toast, and a rotating lunch card of "
                "sourdough sandwiches and sweet potato falafel wraps. "
                "The room is small and fills quickly at weekends, when "
                "queues form on the pavement outside. Walk-ins only, open "
                "seven days, breakfast through to mid-afternoon. One of "
                "the West End's most reliably good spots for a sit-down "
                "that does not rush you out."
            ),
            "known_for": "Speciality coffee and creative brunch on Perth Road's West End strip",
            "good_for": "A proper West End coffee and brunch stop, any day of the week",
            "source_url": "https://www.tripadvisor.co.uk/Restaurant_Review-g186518-d9462516-Reviews-Pacamara_Food_Drink-Dundee_Scotland.html",
            "verified": "2026-06-22",
        },
        {
            "type": "Restaurant",
            "name": "Don Padrino",
            "area": "11 Tay Square, city centre (beside Dundee Rep Theatre)",
            "cuisine": "Italian steakhouse and seafood brasserie",
            "body": (
                "Don Padrino opened in January 2025 on the site of the "
                "former Tayberry restaurant at Tay Square, operated by the "
                "experienced Dundee family team behind Don Michele on Perth "
                "Road. The concept is an Italian brasserie with Scottish "
                "ingredients at its core: dry-aged Scottish steaks, fresh "
                "local seafood, handmade pasta and a wine list to match. "
                "The room is lively, the walls hung with vintage cinema "
                "and Rat Pack imagery, and the theatre-adjacent location "
                "makes it a popular pre-show and celebration choice. "
                "The seafood boards and the Sticky Guinness are early "
                "signatures. Book ahead for dinner; the location beside "
                "Dundee Rep means tables are in demand on performance "
                "evenings. Awarded Best Steak and Seafood Restaurant "
                "in Dundee 2026."
            ),
            "known_for": "Dry-aged Scottish steaks, fresh seafood and Italian pasta beside Dundee Rep, opened 2025",
            "good_for": "A celebratory dinner or pre-theatre meal in the city centre",
            "source_url": "https://www.opentable.com/r/don-padrino-restaurant-dundee",
            "verified": "2026-06-22",
        },
        {
            "type": "Pub",
            "name": "Speedwell Bar",
            "area": "165-167 Perth Road, West End (known locally as Mennies)",
            "cuisine": "Real ale, cask beer",
            "body": (
                "Built in 1903 for James Speed and known locally as "
                "Mennies after the family who ran it for more than fifty "
                "years, the Speedwell Bar is one of the finest surviving "
                "Edwardian pub interiors in Scotland. The L-shaped bar is "
                "divided by a part-glazed screen, the mahogany gantry and "
                "counter are original, dado-panelled walls rise to a "
                "Jacobean ceiling, and the whole ensemble is featured in "
                "CAMRA's Scotland's True Heritage Pubs. The real ale is "
                "taken seriously: Tayside CAMRA named it Pub of the Year "
                "in 2017, 2023 and 2024, and it was Scottish Pub of the "
                "Year Runner-Up in 2023. The current custodians keep the "
                "ales in excellent condition, with a focus on Scottish and "
                "UK regional breweries. Open Monday to Sunday; the sort of "
                "pub that makes you stay for a third."
            ),
            "known_for": "Magnificent 1903 Edwardian interior, Tayside CAMRA Pub of the Year 2017, 2023 and 2024",
            "good_for": "A pint in one of Scotland's most beautiful surviving Edwardian pub rooms",
            "source_url": "https://camra.org.uk/pubs/speedwell-bar-dundee-138515",
            "verified": "2026-06-22",
        },
    ],
    "food_scene": [
        (
            "Dundee's food geography pivots on Perth Road, the long spine of "
            "the West End that runs west from the city centre. This is the "
            "neighbourhood that gave Dundee its independent cafe culture and "
            "its most characterful restaurants, from the forty-year Turkish "
            "institution at Agacan to the speciality coffee of Pacamara. "
            "Perth Road has been named the coolest neighbourhood in Scotland, "
            "and its mix of independent shops, bakers, bars and restaurants "
            "is the reason. The waterfront, rebuilt around the V&A Dundee "
            "which opened in 2018, adds a second food cluster at the city's "
            "regenerated Tay-side edge."
        ),
        (
            "Dundee holds a particular place in the history of British food. "
            "The Keiller family's marmalade enterprise, which began when "
            "merchant James Keiller bought a surplus of Seville oranges at "
            "the harbour around 1797 and his wife Janet turned them into a "
            "preserve, became a commercial empire that popularised marmalade "
            "across Britain. Janet Keiller is also credited with developing "
            "Dundee cake - the almond-topped fruit cake that used the candied "
            "peel left over from marmalade production and became one of "
            "Scotland's most distinctive bakes. Jute, jam and journalism: "
            "those three industries defined Dundee for a century, and the "
            "jam half lives on in the city's sweet tooth and in the "
            "artisan bakers who still make the cake today."
        ),
        (
            "The city's modern food scene is unpretentious and genuinely "
            "local. Dundee lacks the tourist density of Edinburgh and the "
            "size of Glasgow, which means its restaurants serve the city "
            "itself rather than visitors, and the quality-to-price ratio "
            "is consistently good. The student population from Dundee "
            "University and Abertay University keeps the independent cafe "
            "and bar scene dynamic, and the proximity to Angus farmland "
            "and the North Sea fishing ports means fresh local produce is "
            "within easy reach of any kitchen that wants it."
        ),
    ],
    "visit": [
        (
            "Most of the guide runs along Perth Road and Tay Square, making "
            "the geography straightforward. Agacan, Pacamara and the Speedwell "
            "Bar are all on Perth Road itself, within comfortable walking "
            "distance of one another. Don Padrino at Tay Square sits at the "
            "east end of the centre near the waterfront and Dundee Rep "
            "Theatre, a short walk or taxi from the Perth Road cluster. "
            "The city centre and waterfront are compact enough to cover "
            "comfortably on foot."
        ),
        (
            "A Dundee food day might start with brunch at Pacamara, followed "
            "by a walk along Perth Road past the independent shops to the "
            "V&A Dundee and the waterfront. In the afternoon, the city "
            "centre is worth an hour before heading to Don Padrino for "
            "dinner - particularly if there is a show at Dundee Rep. End "
            "the evening at the Speedwell Bar with a pint under the "
            "Edwardian ceiling, or return to Perth Road for a late table "
            "at Agacan on a Thursday through Sunday evening. Book Agacan "
            "and Don Padrino ahead; Pacamara is walk-in only."
        ),
    ],
    "checklist": [
        "Start the day at Pacamara on Perth Road for speciality coffee and a creative brunch",
        "Walk the length of Perth Road to see Dundee's best independent street",
        "Book Agacan well ahead - it only opens Thursday to Sunday and fills quickly",
        "Book Don Padrino for dinner, especially if combining with a Dundee Rep show",
        "End at the Speedwell Bar to see one of Scotland's finest Edwardian pub interiors",
    ],
    "what_to_order": (
        "Order with intent. At Agacan, the mixed kebab plate with meze and "
        "freshly baked bread - the meats are carefully sourced and the "
        "vegetable dishes as good as anything on the menu. At Pacamara, the "
        "Colombian eggs or bubble and squeak benny with a flat white from "
        "whichever speciality roaster is on the bar. At Don Padrino, the "
        "dry-aged Scottish steak or the seafood board, with the Sticky "
        "Guinness if it is available. At the Speedwell Bar, a pint of "
        "whatever Scottish regional is on the handpull - the staff know "
        "the range and keep it in exceptional condition."
    ),
    "glance": [
        ("Best for a quick bite", "Pacamara, for speciality coffee and brunch on Perth Road's West End strip"),
        ("Best for an occasion", "Don Padrino, for dry-aged Scottish steaks beside Dundee Rep at Tay Square"),
        ("Best for atmosphere", "Speedwell Bar's 1903 Edwardian interior on Perth Road, Tayside CAMRA Pub of the Year"),
    ],
    "faq": [
        (
            "What is Dundee famous for food?",
            "Dundee has two great food claims: Keiller's marmalade, which "
            "began when merchant James Keiller bought surplus Seville oranges "
            "at the harbour around 1797 and his wife Janet turned them into a "
            "commercial preserve that popularised marmalade across Britain; and "
            "Dundee cake, the almond-topped fruit cake Janet developed using "
            "the candied peel left over from marmalade production. Both remain "
            "made by Dundee bakers today."
        ),
        (
            "Where is the best place to eat on Perth Road in Dundee?",
            "Perth Road in the West End is Dundee's best independent food "
            "street. Agacan at number 113 is the forty-year Turkish institution "
            "famous for its art-covered walls and authentic meze and kebabs, "
            "open Thursday to Sunday evenings. Pacamara Food and Drink at "
            "number 302 is the West End's leading speciality coffee and brunch "
            "cafe, open seven days. The Speedwell Bar at 165-167 is Tayside "
            "CAMRA Pub of the Year."
        ),
        (
            "Where should I eat before a show at Dundee Rep Theatre?",
            "Don Padrino at 11 Tay Square, directly beside Dundee Rep, is the "
            "natural pre-theatre choice. The Italian steakhouse and seafood "
            "brasserie serves dry-aged Scottish steaks, fresh local seafood and "
            "handmade pasta, and the kitchen is experienced with pre-show "
            "timing. Book ahead, particularly on performance evenings."
        ),
        (
            "Which Dundee pub has the best interior?",
            "The Speedwell Bar at 165-167 Perth Road, built in 1903 and known "
            "locally as Mennies, has one of the finest surviving Edwardian pub "
            "interiors in Scotland: an L-shaped bar with a part-glazed screen, "
            "original mahogany gantry and counter, dado-panelled walls and a "
            "Jacobean ceiling. It is listed in CAMRA's Scotland's True Heritage "
            "Pubs and has been Tayside CAMRA Pub of the Year in 2017, 2023 "
            "and 2024."
        ),
        (
            "Are there good independent cafes in Dundee?",
            "Yes. Pacamara Food and Drink at 302 Perth Road is the West End's "
            "leading independent cafe: a licensed, seven-day brunch and lunch "
            "spot sourcing beans from UK speciality roasters and serving "
            "creative food including shakshuka, Colombian eggs and bubble and "
            "squeak benny. It fills quickly at weekends and operates walk-ins "
            "only, so arrive early or mid-week for the best chance of a table."
        ),
        (
            "Can you do a Dundee food day on foot?",
            "Mostly. Agacan, Pacamara and the Speedwell Bar all sit on Perth "
            "Road in the West End, within comfortable walking distance of each "
            "other. Don Padrino is at Tay Square near the waterfront, a short "
            "walk east toward the city centre. The V&A Dundee on the waterfront "
            "is worth visiting en route, and the whole loop from the West End "
            "to the waterfront is no more than a mile and a half."
        ),
    ],
}
