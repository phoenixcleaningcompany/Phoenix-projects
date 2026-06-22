# ============================================================================
# EAT SERIES — TOWNS research data
# Every entry is WEB-RESEARCHED LIVE, never authored from memory, and every
# venue is confirmed currently trading at research time. Append new towns here
# after research (see CLAUDE.md). Nearby trios must all be on eat_towns.csv.
#
# Entry schema (consumed by eat_build.py):
#   region, population, nearby[3],
#   meta_title (<=60, contains town), meta_description (<=155, no apostrophes, CTA),
#   hero_svg_file | hero_svg (optional; generic fallback if absent),
#   trust_strip, snapshot, stats[(val,label) x4],
#   pivot_variant ("high-volume"|"pub-town"|"coastal"|"market-town"),
#   pivot_local_hook,
#   venues[ {type,name,area,cuisine,body,known_for,good_for,
#            source_url,verified(YYYY-MM-DD)} x4 ],
#   food_scene[str], visit[str], checklist[str x5], what_to_order,
#   glance[(head,body) x3], faq[(q,a) >=3]
# ============================================================================

TOWNS = {}

# --------------------------------------------------------------------------
# LONDON — flagship (general-knowledge exception; still venue-verified)
# --------------------------------------------------------------------------
TOWNS["london"] = {
    "region": "Greater London",
    "population": "9M",
    "evidence_exempt": True,
    "evidence_exempt_reason": "general-knowledge flagship (long-established, nationally documented venues)",
    "nearby": ["Croydon", "Bromley", "Watford"],
    "meta_title": "Best Places to Eat in London: Local Food Guide",
    "meta_description": (
        "Where to eat in London: a 24-hour Brick Lane beigel, a Covent Garden "
        "coffee pioneer, the oldest restaurant and a Victorian gin palace. "
        "Read the guide."
    ),
    "hero_svg_file": "eat_hero_london.svg",
    "trust_strip": (
        "From the Northern Quarter coffee bars to a 150-year-old chop house, "
        "London's independent food scene is one of the best anywhere"
    ),
    "snapshot": (
        "For a fast answer: Beigel Bake on Brick Lane for a 24-hour salt beef "
        "beigel, Monmouth Coffee in Covent Garden for London's pioneering "
        "speciality roast, Rules in Covent Garden for British game in the city's "
        "oldest restaurant, and The Princess Louise in Holborn for a pint under "
        "one of Britain's finest Victorian pub interiors. Four moods, one "
        "walkable slice of central and east London."
    ),
    "stats": [
        ("9M", "Greater London population (approx)"),
        ("1798", "Year Rules first opened"),
        ("24/7", "Beigel Bake never closes"),
        ("4", "Hand-picked independents"),
    ],
    "pivot_variant": "high-volume",
    "pivot_local_hook": (
        "In a city this dense, kitchens sit beneath flats, hotels and offices, "
        "and a grease-laden duct is a vertical fire path through the whole "
        "building."
    ),
    "venues": [
        {"type": "Takeaway", "name": "Beigel Bake", "area": "159 Brick Lane, Shoreditch (open 24 hours)",
         "cuisine": "Jewish bakery, salt beef beigels",
         "body": ("The white-fronted bakery at the top of Brick Lane has baked beigels around "
                  "the clock since 1974, and the queue rarely stops. The order to make is the hot "
                  "salt beef beigel: thick hand-carved brisket, a fierce smear of English mustard "
                  "and a pickle, packed into a chewy boiled-and-baked beigel for a couple of "
                  "pounds. It feeds market traders at dawn and club-goers at 3am, and after fifty "
                  "years it is as much a London institution as anything with a star."),
         "known_for": "Hot salt beef beigels, baked on site 24/7",
         "good_for": "A cheap, legendary East End bite at any hour"},
        {"type": "Cafe", "name": "Monmouth Coffee", "area": "27 Monmouth Street, Covent Garden (also Borough Market)",
         "cuisine": "Speciality coffee",
         "body": ("Founded in 1978, Monmouth roasted coffee in a Covent Garden basement long "
                  "before flat whites reached the high street, and it is fair to call it a "
                  "foundation stone of London's speciality scene. The approach has barely changed: "
                  "single-origin beans sourced direct, roasted in Bermondsey, and served as "
                  "carefully made espresso or single-cup filter. The Monmouth Street shop is tiny "
                  "and characterful; the Borough Market branch is the one with the famous queue."),
         "known_for": "Single-origin beans and filter cones since 1978",
         "good_for": "A serious coffee break between Covent Garden and Borough"},
        {"type": "Restaurant", "name": "Rules", "area": "35 Maiden Lane, Covent Garden",
         "cuisine": "Traditional British, game",
         "body": ("Opened by Thomas Rule in 1798 as an oyster bar, Rules is London's oldest "
                  "restaurant and has spent two centuries serving the traditional food of this "
                  "country at its best. The dining room is a vision of old London - dark wood, red "
                  "velvet booths, walls crowded with paintings - and the kitchen specialises in "
                  "game from its own High Pennines estate, alongside oysters, pies and puddings. "
                  "Dickens, Chaplin and Graham Greene all dined here."),
         "known_for": "British game, oysters and puddings since 1798",
         "good_for": "A proper occasion in London's oldest dining room"},
        {"type": "Pub", "name": "The Princess Louise", "area": "208 High Holborn, Holborn",
         "cuisine": "Pub food",
         "body": ("Step inside and the interior does the talking. Built in 1872 and lavishly "
                  "remodelled in 1891, the Princess Louise is one of the finest surviving Victorian "
                  "gin palaces in the country: etched and gilded mirrors, glazed tilework, an "
                  "island bar divided into snugs by mahogany partitions and rare snob screens. It "
                  "is Grade II* listed and run by Samuel Smith's, the independent Yorkshire family "
                  "brewery, so the beer is own-brewed and good value, with no music to compete "
                  "with the conversation."),
         "known_for": "A Grade II* listed 1891 Victorian interior",
         "good_for": "A cheap pint in a genuinely jaw-dropping room"},
    ],
    "food_scene": [
        ("London's food map is really a map of its neighbourhoods. The East End around Brick "
         "Lane carries the Jewish baking and Bangladeshi curry-house traditions that gave the "
         "area its character, and Beigel Bake is the most famous survivor of the former."),
        ("A short way south, Borough Market has become the city's larder, where Monmouth Coffee "
         "arrived in the late 1990s among the cheesemongers and bakers. Covent Garden and Holborn "
         "hold the older layers, with Rules feeding the West End since the eighteenth century and "
         "the Princess Louise pouring pints since the high Victorian age."),
        ("Beyond these anchors, Soho, Bermondsey's railway-arch roasteries and the restaurant "
         "scenes of Hackney and Peckham keep London moving forward at speed - a city where a "
         "24-hour beigel, a pioneering flat white, a 220-year-old game restaurant and a protected "
         "gin-palace pub all sit within a few stops of one another."),
    ],
    "visit": [
        ("The geography is friendlier than London's size suggests. Covent Garden and Holborn are "
         "a ten-minute walk apart, putting Monmouth, Rules and the Princess Louise within easy "
         "reach on foot. Beigel Bake sits east in Shoreditch, a short hop to Liverpool Street and "
         "a walk up Brick Lane."),
        ("Done as a day - a Covent Garden coffee, a historic meal at Rules, a pint amid the "
         "mirrors at the Princess Louise and a salt beef beigel to finish - these four make a "
         "tidy, walkable tour of the London that Londoners are quietly proud of."),
    ],
    "checklist": [
        "Start with coffee at Monmouth on Monmouth Street, or join the Borough Market queue",
        "Book Rules ahead - it is popular and the dining room is not large",
        "Visit the Princess Louise off-peak to take in the tilework",
        "Save Beigel Bake for last; it is the one place serving in the small hours",
        "Use the Central and Northern lines - most of this loop is a few stops apart",
    ],
    "what_to_order": (
        "Order with intent. At Beigel Bake, the hot salt beef with mustard and a pickle. At "
        "Monmouth, ask which single origin is on the espresso that week. At Rules, lean into the "
        "game and the puddings - pheasant or a steak and kidney pie, then a syrup sponge. At the "
        "Princess Louise, a pint of the house bitter in a snug, and look up at the ceiling."
    ),
    "glance": [
        ("Best for a quick bite", "Beigel Bake, for a salt beef beigel at any hour on Brick Lane"),
        ("Best for an occasion", "Rules, for game and history in Covent Garden"),
        ("Best for atmosphere", "The Princess Louise's protected Victorian interior"),
    ],
    "faq": [
        ("Where can I get the best salt beef beigel in London?",
         "Beigel Bake on Brick Lane, open 24 hours since 1974, is the East End institution for "
         "hot salt beef beigels with mustard and pickle, baked on site in Spitalfields."),
        ("Which is the best independent coffee in central London?",
         "Monmouth Coffee, founded in 1978 and a pioneer of London's speciality scene, roasts "
         "single-origin beans in Bermondsey and serves them at its Covent Garden shop and Borough "
         "Market."),
        ("What is the oldest restaurant in London?",
         "Rules in Covent Garden, established in 1798 by Thomas Rule, is London's oldest "
         "restaurant, serving classic British game, oysters, pies and puddings."),
        ("Which London pub has the best interior?",
         "The Princess Louise on High Holborn, built in 1872 with an 1891 interior of etched "
         "glass, tiling and mahogany snob screens, has one of the best-preserved Victorian "
         "gin-palace interiors in Britain. It is Grade II* listed and run by Samuel Smith's."),
        ("Are these London food spots independent?",
         "Beigel Bake, Monmouth Coffee and Rules are all independent businesses. The Princess "
         "Louise is run by Samuel Smith's, an independent family brewery founded in 1758, so none "
         "of the four are faceless chains."),
        ("Can you do a London food day on foot and public transport?",
         "Easily. Beigel Bake (Shoreditch), Monmouth (Covent Garden), Rules (Covent Garden) and "
         "the Princess Louise (Holborn) all sit on or near the Central and Northern lines."),
    ],
}

# --------------------------------------------------------------------------
# BIRMINGHAM — web-researched June 2026
# --------------------------------------------------------------------------
TOWNS["birmingham"] = {
    "region": "the West Midlands",
    "population": "1.15M",
    "nearby": ["Solihull", "West Bromwich", "Walsall"],
    "meta_title": "Best Places to Eat in Birmingham: Local Food Guide",
    "meta_description": (
        "Where to eat in Birmingham: the Balti Triangle, a pioneering coffee "
        "roaster, a two-Michelin-star Indian and a grand former-bank pub. "
        "Read the guide."
    ),
    "hero_svg_brief": (
        "Birmingham skyline in the Phoenix charcoal/slate palette with copper "
        "highlights: cylindrical Rotunda, disc-clad Bullring Selfridges, the "
        "circular Library of Birmingham facade, St Martin in the Bull Ring "
        "spire; a canal and narrowboat across the foreground; copper "
        "plate-and-cutlery motif; banner reading WHERE TO EAT IN BIRMINGHAM."
    ),
    "trust_strip": (
        "From the Balti Triangle to a two-Michelin-star kitchen, Birmingham is "
        "one of the most exciting places to eat outside London"
    ),
    "snapshot": (
        "For a fast answer: Shababs in the Balti Triangle for the city's own "
        "dish cooked the original way, Quarter Horse Coffee for Birmingham's "
        "pioneering independent roast, Opheem for Aktar Islam's two-Michelin-"
        "star modern Indian, and The Old Joint Stock for cask ale and a pie "
        "under the domed ceiling of a Victorian bank. Four moods, one compact "
        "second city."
    ),
    "stats": [
        ("1.15M", "Population (approx)"),
        ("1970s", "Decade the balti was born here"),
        ("Balti Triangle", "Birmingham's curry heartland"),
        ("4", "Hand-picked independents"),
    ],
    "pivot_variant": "high-volume",
    "pivot_local_hook": (
        "Birmingham's signature cooking runs hot: a balti is seared in a "
        "flat-bottomed steel bowl over a fierce open flame, and the city's "
        "high-volume curry houses, fine-dining kitchens and pub kitchens throw "
        "a heavy load of grease-laden vapour into their canopies every service."
    ),
    "venues": [
        {"type": "Balti House", "name": "Shababs", "area": "Ladypool Road, Sparkbrook (the Balti Triangle)",
         "cuisine": "Birmingham balti, Pakistani",
         "body": ("The balti was invented in Birmingham in the mid-1970s, and the Balti Triangle "
                  "around Ladypool Road in Sparkbrook is its home turf. Of the 30-plus balti houses "
                  "that packed the area in its 1990s heyday only a handful survive, and Shababs is "
                  "the standard-bearer. Opened in 1987 by the Hussein family and run by chef Zaf "
                  "Hussain, it cooks the real thing: a one-pot curry seared fast over a high flame "
                  "in a flat-bottomed steel bowl, then served in the same bowl to scoop up with "
                  "naan. It is bring-your-own-booze and easy on the wallet, and the chicken balti, "
                  "lamb tikka and table-sized naan are the orders to make."),
         "known_for": "The authentic Birmingham balti, cooked and served in the bowl",
         "good_for": "Eating the city's own dish where it belongs, BYOB",
         "source_url": "https://www.tripadvisor.com/Restaurant_Review-g186402-d1741396-Reviews-Shababs_Balti_Restaurant-Birmingham_West_Midlands_England.html",
         "verified": "2026-06-22"},
        {"type": "Cafe", "name": "Quarter Horse Coffee", "area": "Jewellery Quarter (built its name on Bristol Street)",
         "cuisine": "Speciality coffee",
         "body": ("Quarter Horse is widely credited with helping kick off Birmingham's speciality "
                  "coffee scene. The independent roaster-cafe built its reputation on Bristol "
                  "Street and now roasts in the Jewellery Quarter, sourcing green beans direct and "
                  "roasting single origins on site in full view of the counter. The coffee is taken "
                  "seriously without the attitude: rotating single-origin espresso, filter, and "
                  "beans and kit to take home. They roast on electric machines part-powered by "
                  "solar, and supply cafes across the country, so a flat white here is as good as "
                  "the city makes."),
         "known_for": "Single-origin beans roasted on site since the city's coffee scene began",
         "good_for": "A serious coffee break and beans to take home",
         "source_url": "https://quarterhorsecoffee.com/",
         "verified": "2026-06-22"},
        {"type": "Restaurant", "name": "Opheem", "area": "Summer Row, city centre",
         "cuisine": "Modern Indian fine dining",
         "body": ("If Shababs is one end of Birmingham's South Asian story, Opheem is the other. "
                  "Chef-owner Aktar Islam grew up in Aston working in his father's restaurant, and "
                  "in 2024 his modern Indian dining room on Summer Row became the first Indian "
                  "restaurant in the UK to be awarded two Michelin stars. The cooking takes the "
                  "techniques and spicing of the subcontinent and reworks them with British produce "
                  "across three-, five- and seven-course menus, with snacks first in the lounge "
                  "before the open-kitchen dining room. Signatures like the salt-aged Aylesbury "
                  "duck show why this is the city's flagship table. Book well ahead."),
         "known_for": "Two-Michelin-star modern Indian from a Birmingham-born chef",
         "good_for": "A landmark special-occasion meal in the second city",
         "source_url": "https://opheem.com/",
         "verified": "2026-06-22"},
        {"type": "Pub", "name": "The Old Joint Stock", "area": "Temple Row West, opposite St Philip's Cathedral",
         "cuisine": "British pub food",
         "body": ("Step inside and you are standing in a Victorian banking hall. Built in 1862 by "
                  "architect J. A. Chatwin and later home to the Birmingham Joint Stock Bank, the "
                  "Grade II-listed building became a pub in 1997 and gained a studio theatre "
                  "upstairs in 2006. The room is genuinely grand: a huge domed skylight over a "
                  "carved wooden island bar, high ceilings, gilded detail and a wraparound balcony. "
                  "It is run by Fuller's, the independent London family brewer, so the cask ale is "
                  "well kept and the kitchen leans into British classics, with the homemade pies "
                  "the thing to order."),
         "known_for": "A domed former-bank interior, cask ale and homemade pies",
         "good_for": "A pint under a remarkable roof, or a pre-theatre meal",
         "source_url": "https://www.oldjointstock.co.uk/",
         "verified": "2026-06-22"},
    ],
    "food_scene": [
        ("Birmingham's food map runs from the back streets of Sparkbrook to the white-tablecloth "
         "dining rooms of the city centre. The Balti Triangle, spread across Ladypool Road, Stoney "
         "Lane and Stratford Road, is where the balti was born in the mid-1970s and remains the "
         "city's curry heartland, even as the original balti houses have thinned out."),
        ("In the centre, the Jewellery Quarter has become the home of Birmingham's independent "
         "coffee scene, with roaster-cafes like Quarter Horse leading the way, while Digbeth's "
         "converted factories now hold street-food halls and bars. The grand Colmore and Temple "
         "Row blocks keep the heritage pubs and the city's fine-dining names."),
        ("And it is fine dining where modern Birmingham has made its loudest noise: the city holds "
         "one of the strongest restaurant scenes outside London, with Opheem's two Michelin stars "
         "at the top of a deep field of chef-owned independents. Eat across all of it and you get "
         "the full range, from a five-pound balti to a tasting menu, within a few miles."),
    ],
    "visit": [
        ("Most of this guide sits in or near the compact city centre. The Old Joint Stock, Opheem "
         "and the Jewellery Quarter are an easy walk apart, with New Street, Snow Hill and the "
         "Metro tram all close by. The Balti Triangle is about two miles south in Sparkbrook, a "
         "short bus or taxi ride from the centre."),
        ("Time it right and the day flows: coffee in the Jewellery Quarter, a pie and a pint under "
         "the dome at the Old Joint Stock, a balti in Sparkbrook, and Opheem saved for the evening "
         "you want to remember. Book Opheem weeks ahead, and remember most Balti Triangle houses "
         "are bring-your-own-booze."),
    ],
    "checklist": [
        "Start with coffee in the Jewellery Quarter at Quarter Horse",
        "Pop into the Old Joint Stock just to see the domed banking hall",
        "Head south to Sparkbrook for a balti at Shababs - bring your own drinks",
        "Book Opheem well in advance; tables go quickly",
        "Use New Street, Snow Hill or the Metro tram - the centre is walkable",
    ],
    "what_to_order": (
        "Order with intent. At Shababs, a chicken or lamb balti with a table-sized naan to scoop "
        "it up, plus tandoori wings or lamb chops off the coals to start. At Quarter Horse, ask "
        "which single origin is on the espresso that week. At Opheem, surrender to a tasting menu "
        "and the salt-aged duck. At the Old Joint Stock, a homemade pie and a pint of cask ale, "
        "taken slowly under the dome."
    ),
    "glance": [
        ("Best for a quick bite", "Shababs, for a balti in the Triangle where the dish was born"),
        ("Best for an occasion", "Opheem, for two-Michelin-star modern Indian"),
        ("Best for atmosphere", "The Old Joint Stock's domed Victorian banking hall"),
    ],
    "faq": [
        ("Where can I eat an authentic balti in Birmingham?",
         "Shababs on Ladypool Road in Sparkbrook, open since 1987, is one of the last original "
         "balti houses in the Balti Triangle. It cooks the Birmingham balti the proper way and is "
         "bring-your-own-booze."),
        ("Why is Birmingham famous for the balti?",
         "The balti was invented in Birmingham in the mid-1970s by the city's Pakistani community "
         "as a fast one-pot curry cooked and served in a flat-bottomed steel bowl. The Balti "
         "Triangle around Sparkbrook became its home and the dish spread worldwide."),
        ("Where is the best independent coffee in Birmingham?",
         "Quarter Horse Coffee, an independent roaster-cafe that helped pioneer the city's "
         "speciality scene, roasts single-origin beans on site and serves espresso, filter and "
         "beans to take home."),
        ("Does Birmingham have a two-Michelin-star restaurant?",
         "Yes. Opheem on Summer Row, the modern Indian restaurant from Birmingham-born chef Aktar "
         "Islam, was awarded two Michelin stars in 2024, the first Indian restaurant in the UK to "
         "hold two."),
        ("Which Birmingham pub has the best interior?",
         "The Old Joint Stock on Temple Row West, a Grade II-listed former bank built in 1862, has "
         "a spectacular domed banking hall over a carved wooden island bar, and serves Fuller's "
         "cask ale and homemade pies with a theatre upstairs."),
        ("Can you do a Birmingham food day on foot and public transport?",
         "Mostly. The Old Joint Stock, Opheem and the Jewellery Quarter are walkable in the centre, "
         "served by New Street, Snow Hill and the Metro tram. The Balti Triangle is about two miles "
         "south in Sparkbrook, a short bus or taxi ride away."),
    ],
}

TOWNS["leeds"] = {
    "region": "West Yorkshire",
    "population": "800K",
    "nearby": ["Pudsey", "Horsforth", "Rothwell"],
    "meta_title": "Best Places to Eat in Leeds: Local Food Guide",
    "meta_description": (
        "Where to eat in Leeds: a Kirkgate Market street-food stall, a "
        "pioneering coffee bar, Michelin-listed Keralan cooking and the "
        "oldest pub. Read the guide."
    ),
    "hero_svg_file": "eat_hero_leeds.svg",
    "hero_svg_brief": (
        "Leeds skyline in the Phoenix charcoal/slate palette with copper "
        "highlights: the clock tower and glass roof of Leeds Town Hall, the "
        "ornate Victorian Corn Exchange dome, the Bridgewater Place tower, "
        "the arched Kirkgate Market facade; the River Aire and a canal "
        "narrowboat across the foreground; copper plate-and-cutlery motif; "
        "banner reading WHERE TO EAT IN LEEDS."
    ),
    "trust_strip": (
        "From the street-food stalls of Kirkgate Market to a 1715 ale house, "
        "Leeds packs a deep independent food scene into a walkable centre"
    ),
    "snapshot": (
        "For a fast answer: Manjit's Kitchen at Kirkgate Market for "
        "vegetarian Punjabi street food that grew from a food truck, Laynes "
        "Espresso by the station for the coffee bar that helped start the "
        "city's speciality scene, Tharavadu for Michelin-listed Keralan "
        "cooking, and Whitelock's Ale House for a pint and a pie in the "
        "oldest pub in Leeds. Four moods, one compact city centre."
    ),
    "stats": [
        ("800K", "Population (approx)"),
        ("1715", "Year Whitelock's first poured a pint"),
        ("Kirkgate Market", "One of Europe's largest covered markets"),
        ("4", "Hand-picked independents"),
    ],
    "pivot_variant": "high-volume",
    "pivot_local_hook": (
        "Leeds cooks at volume and at heat: tandoors and tawas firing dosas "
        "and Punjabi street food, char-grills and fryers running through "
        "lunch and dinner, and busy pub kitchens turning out pies and "
        "battered fish all push a heavy load of grease-laden vapour into "
        "their canopies every service."
    ),
    "venues": [
        {"type": "Street Food", "name": "Manjit's Kitchen", "area": "Kirkgate Market (and 333 Kirkstall Road)",
         "cuisine": "Vegetarian Punjabi street food",
         "body": ("Manjit's Kitchen started as a humble food truck and grew into one of the best-loved "
                  "names in Leeds street food, now trading from a stall in the food hall at Kirkgate "
                  "Market and a bricks-and-mortar kitchen and bar on Kirkstall Road. Everything is "
                  "vegetarian and much of it vegan: Punjabi home cooking done properly, with thalis, "
                  "freshly griddled dosas, samosa chaat, paneer wraps and masala chai. Founder Manjit "
                  "built a largely women-led kitchen, and the food carries that homemade care. Prices "
                  "are gentle and portions generous, which is why the stall draws a lunchtime queue. "
                  "Order the thali for the full spread, or a samosa chaat and a wrap to eat on the move."),
         "known_for": "Vegetarian Punjabi street food that grew from a food truck",
         "good_for": "A fast, cheap, properly spiced lunch in the market",
         "source_url": "https://www.manjitskitchen.com/",
         "verified": "2026-06-22"},
        {"type": "Cafe", "name": "Laynes Espresso", "area": "16 New Station Street, by Leeds station",
         "cuisine": "Speciality coffee and brunch",
         "body": ("Laynes opened in 2011 in a narrow unit on New Station Street, right by the railway "
                  "station, and is widely credited with helping kick off Leeds's independent speciality "
                  "coffee scene. Barista-owned and run, it was one of the first in the city to pour the "
                  "underground roasts and teas that locals now take for granted. Over fifteen years it "
                  "has grown from an espresso bar into one of the best brunch spots in the centre, with "
                  "pastries and bakes from its own Laynes Bakery in Armley. It is consistently rated the "
                  "city's top coffee stop. Grab a flat white and a brunch plate on your way in or out of "
                  "town, or settle in with a filter and a pastry."),
         "known_for": "The coffee bar that helped start the city's speciality scene",
         "good_for": "A serious coffee and brunch by the station",
         "source_url": "https://laynescafe.co.uk/",
         "verified": "2026-06-22"},
        {"type": "Restaurant", "name": "Tharavadu", "area": "7-8 Mill Hill, city centre",
         "cuisine": "Keralan, South Indian",
         "body": ("Tharavadu, meaning ancestral home, was opened in 2014 by Siby Jose and a team of "
                  "Keralan chefs, and has become one of the most respected Indian restaurants in the "
                  "north of England. Tucked on Mill Hill near the station, it cooks the food of Kerala: "
                  "superbly spiced, coastal South Indian dishes built on coconut, curry leaf and "
                  "tamarind rather than the standard curry-house template. It has been recommended by "
                  "the Michelin Guide for several years running, listed in Harden's, and named among the "
                  "UK's top 100. The paper-thin dosas are a signature, and the meen kootan fish curry is "
                  "the most-ordered main. Book ahead, especially at weekends, and go for the seafood and "
                  "the dosas."),
         "known_for": "Michelin-listed Keralan cooking, famous for its dosas",
         "good_for": "A standout South Indian meal in the city centre",
         "source_url": "https://www.tharavadurestaurants.com/",
         "verified": "2026-06-22"},
        {"type": "Pub", "name": "Whitelock's Ale House", "area": "Turk's Head Yard, off Briggate",
         "cuisine": "British pub food, cask ale",
         "body": ("Whitelock's is the oldest pub in Leeds, first licensed as the Turk's Head in 1715 and "
                  "tucked down a narrow yard off Briggate. The Whitelock family took it on in the 1880s "
                  "and remodelled it in 1895 into the long, narrow luncheon bar that largely survives "
                  "today: gleaming brass, etched and stained glass, marble counters and a real fire in "
                  "winter. It was reputedly the first building in the city with electric light, and the "
                  "poet John Betjeman called it the very heart of Leeds. Now Grade II* listed, it pours a "
                  "well-kept range of cask ales and serves proper British food. The beef and ale pie, "
                  "served in its tin, and the Sunday roast are the orders to make."),
         "known_for": "A 1715 luncheon bar interior, cask ale and beef-and-ale pie",
         "good_for": "A pint and a pie in the oldest pub in Leeds",
         "source_url": "https://whitelocksleeds.com/",
         "verified": "2026-06-22"},
    ],
    "food_scene": [
        ("Leeds eats around its Victorian heart. Kirkgate Market, one of the largest covered markets in "
         "Europe and the birthplace of Marks & Spencer, now holds a buzzing food hall where stalls like "
         "Manjit's Kitchen serve street food from around the world, while the domed Corn Exchange nearby "
         "keeps a clutch of independent makers and eateries under its remarkable roof."),
        ("Out from the centre, the city's food districts each have a flavour. Call Lane and the "
         "Briggate yards hold the bars and historic pubs, including Whitelock's down Turk's Head Yard. "
         "Headingley and Chapel Allerton draw the brunch and neighbourhood-restaurant crowd, while the "
         "streets around the station and Mill Hill have become a strong run of independent cafes and "
         "dining rooms."),
        ("It is a genuinely independent scene for its size: a pioneering speciality-coffee culture led "
         "by the likes of Laynes, a deep bench of South Asian cooking from market street food up to "
         "Michelin-listed Keralan dining at Tharavadu, and a heritage pub culture that few cities match. "
         "Eat across all of it and you cover a food truck thali to a tasting-grade fish curry within a "
         "few walkable blocks."),
    ],
    "visit": [
        ("Almost all of this guide sits in the compact, walkable city centre. Kirkgate Market, the Corn "
         "Exchange, Whitelock's down Turk's Head Yard and Tharavadu on Mill Hill are minutes apart on "
         "foot, and Laynes is right by Leeds station, so it works as your first or last stop of the day. "
         "Leeds is exceptionally well connected by rail, so a food day here is easy without a car."),
        ("Time it right and the day flows: a flat white and brunch at Laynes by the station, a thali "
         "from Manjit's in the market for lunch, a pint and a pie under the etched glass at Whitelock's "
         "in the afternoon, and Tharavadu saved for dinner. Book Tharavadu ahead, especially on a "
         "weekend, and arrive at Manjit's market stall a little before the lunchtime rush."),
    ],
    "checklist": [
        "Start with coffee and brunch at Laynes Espresso by the station",
        "Queue for a thali or dosa at Manjit's Kitchen in Kirkgate Market",
        "Duck down Turk's Head Yard to see Whitelock's 1715 interior",
        "Book Tharavadu ahead for the dosas and meen kootan fish curry",
        "Wander the Corn Exchange and market food hall between stops",
    ],
    "what_to_order": (
        "Order with intent. At Manjit's Kitchen, a full thali, or a samosa chaat and a paneer wrap to "
        "eat on the move. At Laynes, a flat white with a pastry from their own bakery, or the brunch "
        "plate. At Tharavadu, the paper-thin dosas and the meen kootan fish curry, with plenty for "
        "vegetarians too. At Whitelock's, the beef and ale pie in its tin with a pint of well-kept cask "
        "ale, or the Sunday roast with Yorkshire puddings."
    ),
    "glance": [
        ("Best for a quick bite", "Manjit's Kitchen, for a thali or dosa in Kirkgate Market"),
        ("Best for an occasion", "Tharavadu, for Michelin-listed Keralan cooking"),
        ("Best for atmosphere", "Whitelock's 1715 luncheon bar down Turk's Head Yard"),
    ],
    "faq": [
        ("Where can I eat good street food in Leeds?",
         "Kirkgate Market's food hall is the place to start, and Manjit's Kitchen is the standout: "
         "vegetarian Punjabi street food, from thalis to freshly griddled dosas, that grew from a food "
         "truck into one of the city's best-loved independents."),
        ("What is the oldest pub in Leeds?",
         "Whitelock's Ale House, down Turk's Head Yard off Briggate, first licensed as the Turk's Head "
         "in 1715. Its narrow 1890s luncheon-bar interior, with etched glass and brass, is Grade II* "
         "listed, and it serves cask ale and British classics like beef and ale pie."),
        ("Where is the best independent coffee in Leeds?",
         "Laynes Espresso on New Station Street, open since 2011 right by the railway station, helped "
         "pioneer the city's speciality coffee scene. It is barista-owned, consistently rated the city's "
         "top coffee stop, and also one of the best brunch spots in the centre."),
        ("Does Leeds have a Michelin-recommended restaurant?",
         "Yes. Tharavadu on Mill Hill, a Keralan restaurant opened in 2014, has been recommended in the "
         "Michelin Guide for several years running and listed among the UK's top 100. It is known for "
         "its paper-thin dosas and the meen kootan fish curry."),
        ("Which Leeds restaurant is best for South Indian food?",
         "Tharavadu cooks the food of Kerala rather than the standard curry-house menu, built on "
         "coconut, curry leaf and tamarind, with strong seafood and dosas. It is a short walk from the "
         "station on Mill Hill; book ahead at weekends."),
        ("Can you do a Leeds food day on foot and public transport?",
         "Easily. Kirkgate Market, the Corn Exchange, Whitelock's and Tharavadu are all minutes apart in "
         "the compact centre, and Laynes sits right by Leeds station, which is one of the best-connected "
         "rail hubs in the north."),
    ],
}

# glasgow ----------------------------------------------------------
TOWNS["glasgow"] = {
    "region": "Scotland",
    "population": "635K",
    "nearby": ["Paisley", "East Kilbride", "Motherwell"],
    "meta_title": "Best Places to Eat in Glasgow: Local Food Guide",
    "meta_description": (
        "Glasgow food picks: East End fish supper since 1939, West End "
        "roaster-cafe, Michelin-starred tasting menu and a Victorian gin "
        "palace bar. Read the guide."
    ),
    "trust_strip": (
        "From a Gallowgate fish supper to a Michelin-starred tasting menu, "
        "Glasgow is one of Britain's most exciting and rewarding cities to eat in"
    ),
    "snapshot": (
        "For a fast answer: Guido's Coronation Restaurant on the Gallowgate for "
        "a Scottish-Italian fish supper from the family that has run the fryer "
        "since 1939, Papercup Coffee on Great Western Road for house-roasted "
        "beans in the West End, Cail Bruich on Great Western Road for Lorna "
        "McNee's one-Michelin-star seasonal Scottish tasting menu, and The Horse "
        "Shoe Bar on Drury Street for a pint under the longest continuous bar in "
        "Britain. Four moods, one fearlessly hungry city."
    ),
    "stats": [
        ("635K", "Population (approx)"),
        ("1939", "Year Guido's Coronation first served a fish supper"),
        ("1884", "Year The Horse Shoe Bar was established"),
        ("4", "Hand-picked independents"),
    ],
    "pivot_variant": "high-volume",
    "pivot_local_hook": (
        "Glasgow's kitchens cook hard and fast: the high-temperature fryers of "
        "East End chippies, the tasting-menu pass of Michelin-starred dining "
        "rooms, and the charcoal grills of Finnieston's dense restaurant strip "
        "all push a heavy, sustained load of grease-laden vapour into their "
        "canopies through every service."
    ),
    "venues": [
        {
            "type": "Takeaway",
            "name": "Guido's Coronation Restaurant",
            "area": "55 Gallowgate, East End (under the railway arches)",
            "cuisine": "Scottish-Italian fish and chips",
            "body": (
                "Tucked beneath the old railway bridge at 55 Gallowgate in "
                "Glasgow's East End, Guido's Coronation Restaurant has been "
                "feeding the city since 1939. It was founded by the Corvi family, "
                "Italian immigrants who brought their frying tradition west from "
                "Bo'ness to Glasgow, and the business has passed through three "
                "generations — from grandfather to Guido, and now to Cristoforo "
                "Corvi, who runs the fryer today. The result is a masterclass in "
                "the Scottish-Italian chippy: haddock in a light, properly made "
                "batter, thick chips, and the curry sauce that regulars swear by. "
                "Haggis with chips sits alongside the classics, and a sit-down "
                "breakfast pulls in locals from early morning. Prices are modest "
                "and the queue on a busy day tells you everything you need to know."
            ),
            "known_for": "Three-generation Italian-Scottish fish supper since 1939",
            "good_for": "A legendary East End fish supper or a no-nonsense breakfast",
            "source_url": "https://guidoscoronationrestaurant.shop/",
            "verified": "2026-06-22",
        },
        {
            "type": "Cafe",
            "name": "Papercup Coffee Company",
            "area": "603 Great Western Road, Hillhead, West End",
            "cuisine": "Speciality coffee and brunch",
            "body": (
                "Founded in 2013 by Graeme Crawford, Papercup Coffee Company is "
                "one of the pioneers of Glasgow's speciality coffee scene, a "
                "compact, character-filled cafe on Great Western Road in the West "
                "End. The roastery sits at Arch 17 on Eastvale Place, just across "
                "the city, and the freshly roasted beans make the short journey "
                "to the cafe counter daily. Everything is house-roasted: the "
                "espresso rotates single origins, and the batch filter is always "
                "worth asking about. A varied brunch menu and homemade cakes have "
                "built a following among Hillhead residents and university staff "
                "alike. The room is unhurried and friendly, open seven days from "
                "nine in the morning — the kind of place a neighbourhood returns "
                "to every week."
            ),
            "known_for": "House-roasted speciality beans and West End brunch since 2013",
            "good_for": "A serious coffee and brunch on Great Western Road",
            "source_url": "https://www.papercupcoffee.co.uk/pages/cafe-great-western-road-glasgow",
            "verified": "2026-06-22",
        },
        {
            "type": "Restaurant",
            "name": "Cail Bruich",
            "area": "725 Great Western Road, West End",
            "cuisine": "Modern Scottish fine dining",
            "body": (
                "Opened in 2008 by siblings Chris and Paul Charalambous, Cail "
                "Bruich takes its name from the Gaelic phrase meaning 'to eat "
                "well', and the kitchen has followed through on that promise ever "
                "since. Head chef Lorna McNee, who joined in 2020 having won "
                "BBC Great British Menu's Champion of Champions, runs a "
                "tasting menu rooted in the seasons and the land: Scottish "
                "produce sourced from named farms and coastal suppliers, presented "
                "with the precision and restraint that earned a Michelin Star in "
                "2021 — still current in the 2026 guide. McNee is Scotland's only "
                "female Michelin-starred chef, and Cail Bruich holds three AA "
                "Rosettes alongside its star. The room on Great Western Road is "
                "relaxed rather than formal; the cooking is the event. Book well "
                "in advance."
            ),
            "known_for": "Scotland's only female Michelin-starred chef, seasonal Scottish tasting menu",
            "good_for": "A landmark special-occasion dinner in the West End",
            "source_url": "https://www.cailbruich.co.uk/",
            "verified": "2026-06-22",
        },
        {
            "type": "Pub",
            "name": "The Horse Shoe Bar",
            "area": "17-19 Drury Street, city centre",
            "cuisine": "Traditional pub food",
            "body": (
                "Step inside 17 Drury Street and the bar does the talking. "
                "Established in 1884 by John Scouller and extended in the early "
                "1900s under John Young Whyte, The Horse Shoe Bar has the longest "
                "continuous bar counter in Britain: 104 feet and three inches of "
                "polished wood sweeping in a horseshoe arc around the island. The "
                "Victorian interior is Category A listed by Historic Environment "
                "Scotland and recognised by CAMRA as having a nationally "
                "important pub interior — ornate tilework, carved gantry, high "
                "mirrored ceilings and period fittings that have changed little in "
                "a century. The pub serves real ale alongside a generous kitchen "
                "menu, runs karaoke seven nights a week, and pours a Guinness "
                "that draws visitors from across the city. It sits two minutes "
                "from Central Station and has been doing so since the Victorian age."
            ),
            "known_for": "Britain's longest continuous bar, Victorian gin-palace interior since 1884",
            "good_for": "A pint in a Category A listed architectural gem near Central Station",
            "source_url": "https://www.yelp.co.uk/biz/horseshoe-bar-glasgow",
            "verified": "2026-06-22",
        },
    ],
    "food_scene": [
        (
            "Glasgow's food map is one of the most layered in Britain. The East End "
            "around the Gallowgate and the Barras market carries the city's "
            "working-class Italian-Scottish cooking tradition, the one that gave "
            "Glasgow its fish suppers, its morning rolls and its appetite for "
            "no-nonsense eating at any hour. Guido's Coronation Restaurant, tucked "
            "under the railway arches since 1939, is the most storied survivor of "
            "that lineage."
        ),
        (
            "A mile or two west, Finnieston has become the most talked-about "
            "restaurant strip in Scotland: a post-industrial stretch of Argyle "
            "Street that transformed in little over a decade into a density of "
            "independent dining rooms, craft bars and seafood counters that rivals "
            "anything in Edinburgh or London. The West End around Great Western "
            "Road and Gibson Street operates at a quieter pitch but with serious "
            "depth, home to Cail Bruich's Michelin-starred kitchen and a clutch "
            "of independent roaster-cafes led by Papercup Coffee."
        ),
        (
            "Downtown, the Merchant City's repurposed Georgian warehouses and the "
            "streets around Central Station hold the city's grand Victorian pub "
            "interiors, with The Horse Shoe Bar at their head. Glasgow also does "
            "haggis better than almost anywhere: served straight with neeps and "
            "tatties, folded into pakora, or piled into a morning roll, it appears "
            "on menus from the simplest cafe to the Michelin table. The city's "
            "cooking is curious, confident and unafraid of scale."
        ),
    ],
    "visit": [
        (
            "The geography rewards a day split between east and west. The "
            "Gallowgate and the Horse Shoe Bar are both close to Glasgow Central "
            "and Queen Street stations, keeping transport easy. The West End — "
            "Papercup and Cail Bruich on Great Western Road — is a twenty-minute "
            "walk or a short taxi from the city centre, with Byres Road and "
            "Ashton Lane nearby for an afternoon wander."
        ),
        (
            "Done as a day: a coffee at Papercup on Great Western Road to start, "
            "lunch at the Horse Shoe Bar under those Victorian arches, a fish "
            "supper at Guido's in the Gallowgate after an afternoon at the Barras "
            "market, and Cail Bruich saved for the evening you want to mark. Book "
            "Cail Bruich well in advance; a tasting menu here is not a table you "
            "walk into."
        ),
    ],
    "checklist": [
        "Book Cail Bruich weeks ahead — the Michelin-starred tasting menu fills quickly",
        "Visit Guido's Coronation mid-morning to avoid the lunchtime chippy queue",
        "Go to the Horse Shoe Bar off-peak to take in the bar and tilework properly",
        "Papercup opens from nine — it is the West End's best coffee before a walk along the Kelvin",
        "Use Glasgow Central or Queen Street stations; the Horse Shoe Bar is two minutes from Central",
    ],
    "what_to_order": (
        "Order with intent. At Guido's Coronation, a haddock supper with the "
        "house curry sauce, or haggis with chips and a mug of tea. At Papercup, "
        "ask which single origin is on the espresso that week and try a slice of "
        "the homemade cake. At Cail Bruich, book the full tasting menu and follow "
        "Lorna McNee's lead on the wine pairing — the sourcing is half the story. "
        "At the Horse Shoe Bar, a proper pint of Guinness or cask ale, taken "
        "slowly at the bar so you can look at the gantry."
    ),
    "glance": [
        ("Best for a quick bite", "Guido's Coronation, for a 1939 Italian-Scottish fish supper on the Gallowgate"),
        ("Best for an occasion", "Cail Bruich, for Scotland's only female Michelin-starred chef on Great Western Road"),
        ("Best for atmosphere", "The Horse Shoe Bar's Category A listed Victorian interior and 104-foot bar"),
    ],
    "faq": [
        (
            "Where can I get the best fish and chips in Glasgow?",
            "Guido's Coronation Restaurant at 55 Gallowgate in the East End has been "
            "run by the Italian-Scottish Corvi family since 1939, serving haddock "
            "suppers, haggis and chips, and a house curry sauce under the old "
            "railway arches. It is one of the city's most loved and longest-running "
            "chippies."
        ),
        (
            "Which Glasgow restaurant has a Michelin star?",
            "Cail Bruich on Great Western Road in the West End holds one Michelin "
            "Star (awarded 2021, retained in the 2026 guide) and three AA Rosettes. "
            "Head chef Lorna McNee is Scotland's only female Michelin-starred chef, "
            "and the menu is a seasonal Scottish tasting menu built around named "
            "local producers."
        ),
        (
            "Where is the best independent coffee in Glasgow?",
            "Papercup Coffee Company at 603 Great Western Road in the West End is "
            "one of the city's pioneering speciality roaster-cafes, founded in 2013. "
            "Beans are roasted at their Eastvale Place roastery and served as "
            "rotating single-origin espresso and filter, with a brunch menu and "
            "homemade cakes."
        ),
        (
            "Which Glasgow pub has the longest bar?",
            "The Horse Shoe Bar on Drury Street in the city centre, established in "
            "1884, holds the record for the longest continuous bar counter in "
            "Britain at 104 feet and three inches. The Category A listed Victorian "
            "interior is recognised by CAMRA as nationally important."
        ),
        (
            "What is the local food to try in Glasgow?",
            "Haggis is the city's signature, served traditionally with neeps and "
            "tatties or inventively as haggis pakora in Glasgow's South Asian-"
            "influenced restaurants. The Scottish-Italian fish supper is the other "
            "great Glasgow tradition, best experienced at a long-running independent "
            "chippy like Guido's Coronation on the Gallowgate."
        ),
        (
            "Can you do a Glasgow food day on foot and public transport?",
            "Easily. The Horse Shoe Bar and Guido's Coronation Restaurant are both "
            "close to Glasgow Central and Queen Street stations. Papercup Coffee "
            "and Cail Bruich on Great Western Road are a short taxi or 20-minute "
            "walk into the West End, served by frequent buses on Byres Road."
        ),
    ],
}

# sheffield ----------------------------------------------------------
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

# manchester ----------------------------------------------------------
TOWNS["manchester"] = {
    "region": "Greater Manchester",
    "population": "555,000",
    "nearby": ["Salford", "Stockport", "Oldham"],
    "meta_title": "Best Places to Eat in Manchester: Local Food Guide",
    "meta_description": (
        "Manchester food guide: Bundobust for Gujarati street food, Pollen Bakery for "
        "sourdough, Mughli on the Curry Mile, and the Marble Arch pub. Read the guide."
    ),
    "trust_strip": (
        "From the Northern Quarter to the Curry Mile, Manchester's independent "
        "food scene is among the most diverse and exciting outside London"
    ),
    "snapshot": (
        "For a fast answer: Bundobust on Piccadilly for Gujarati street food and "
        "craft beer brewed on site, Pollen Bakery at Cotton Field Wharf in Ancoats "
        "for sourdough and cruffins that have queued the street since 2016, Mughli "
        "on the Curry Mile for charcoal-pit Indian since 1991, and The Marble Arch "
        "on Rochdale Road for a pint under one of the finest tiled Victorian pub "
        "interiors in the country. Four moods, one brilliant northern city."
    ),
    "stats": [
        ("555K", "City population (approx)"),
        ("1991", "Year Mughli opened on the Curry Mile"),
        ("Curry Mile", "Europe's densest South Asian restaurant strip"),
        ("4", "Hand-picked independents"),
    ],
    "pivot_variant": "high-volume",
    "pivot_local_hook": (
        "Manchester's kitchens run around the clock: the Curry Mile's charcoal pits "
        "and tandoors fire through late-night service, Northern Quarter bars keep "
        "fryers going past midnight, and the city's high-volume independent scene "
        "pushes a heavy grease load through canopies every single day."
    ),
    "venues": [
        {
            "type": "Takeaway/Casual",
            "name": "Bundobust",
            "area": "61 Piccadilly, city centre",
            "cuisine": "Gujarati street food and craft beer",
            "body": (
                "Bundobust arrived in Manchester in 2016, a year after its Leeds launch, "
                "and established itself in a high-ceilinged basement off Piccadilly with "
                "long communal tables, no bookings and twelve taps pouring its own-brewed "
                "craft beer. The concept came from Mayur Patel, whose family runs the "
                "acclaimed Bradford restaurant Prashad, and Marko Husak, a craft beer "
                "specialist: the result is all-vegetarian Gujarati street food — okra fries, "
                "bhel puri, dahi puri, spinach kofta — designed for sharing alongside "
                "Bundobust Brewery lager, IPA and seasonal specials. It is listed in the "
                "Observer Food Monthly OFM 50 and has won Best Innovation at the Casual "
                "Dining Awards. The Brewery taproom on Oxford Street opened in 2021. Open "
                "daily from midday with a two-dish lunch deal until 4pm."
            ),
            "known_for": "Gujarati street food plates and own-brewed craft beer, no bookings",
            "good_for": "A casual, communal, all-vegetarian feast with great beer",
            "source_url": "https://bundobust.com/locations/manchester/",
            "verified": "2026-06-22",
        },
        {
            "type": "Cafe",
            "name": "Pollen Bakery",
            "area": "Cotton Field Wharf, 8 New Union Street, Ancoats",
            "cuisine": "Artisan sourdough, viennoiserie and speciality coffee",
            "body": (
                "Hannah Calvert and Chris Kelly started baking sourdough in their home "
                "kitchen in 2011, launching Pollen commercially from a railway arch behind "
                "Piccadilly Station in 2016. The queues came quickly. They moved to a "
                "light-filled waterside site at Cotton Field Wharf in Ancoats in 2018, "
                "facing New Islington Marina, and added a second cafe at Kampus. Pollen's "
                "sourdough loaves take 28 hours to produce; its cruffins — a croissant "
                "dough baked in a muffin tin — became a Manchester cult object. The Good "
                "Food Guide rates both cafe sites and notes the bakery has established "
                "'cult status in Manchester for its quality viennoiserie and sourdough'. "
                "Open Wednesday to Sunday, with counter seats inside and a terrace beside "
                "the marina."
            ),
            "known_for": "28-hour sourdough loaves and cruffins with Good Food Guide recognition",
            "good_for": "A serious breakfast or mid-morning stop with exceptional pastries",
            "source_url": "https://pollenbakery.com/",
            "verified": "2026-06-22",
        },
        {
            "type": "Restaurant",
            "name": "Mughli Charcoal Pit",
            "area": "30 Wilmslow Road, Rusholme (the Curry Mile)",
            "cuisine": "Indian street food and charcoal-pit grills",
            "body": (
                "Mughli opened on the Curry Mile in 1991, founded by the late Mohammad "
                "Arshad — known to regulars as 'Uncle Peter' — and remains a family-run "
                "restaurant today. While many of its neighbours lean hard into tradition, "
                "Mughli has carved out its own identity: an 'angithi' charcoal pit at "
                "the centre of the kitchen produces tandoori chicken, flame-licked lamb "
                "chops, and punchy prawns with a genuine smoky intensity, alongside "
                "slow-cooked curries, street-food snacks and bold cocktails. Ask Mancunians "
                "for the best butter chicken in the city and many will point to Rusholme. "
                "It opens evenings only (Monday to Saturday from 5pm, Sunday from 2pm) "
                "and takes bookings for the evening sittings through till midnight."
            ),
            "known_for": "Charcoal-pit grills and reimagined curries on the Curry Mile since 1991",
            "good_for": "A special Curry Mile dinner with real smoky depth",
            "source_url": "https://www.mughli.com/",
            "verified": "2026-06-22",
        },
        {
            "type": "Pub",
            "name": "The Marble Arch",
            "area": "73 Rochdale Road, Ancoats/Angel Meadow",
            "cuisine": "Pub food, cask ale and craft beer",
            "body": (
                "Built in 1888 by architects Darbyshire and Smith as a showhouse for "
                "McKenna's Brewery, the Marble Arch is one of the most extraordinary pub "
                "interiors in England: a mosaic-tiled floor that slopes unmistakably "
                "toward the bar, glazed ceramic walls, a barrel-vaulted ceiling of "
                "decorated tile that was hidden behind plasterboard in 1954 and restored "
                "in the 1980s, and a long curved counter beneath it all. It is Grade II "
                "listed and holds an interior of outstanding national historic importance "
                "per CAMRA, appearing in the Good Beer Guide for over 25 consecutive years. "
                "Marble Brewery, founded at the back of the building in 1997 and now based "
                "in Salford, keeps the handpulls supplied with Manchester Bitter, Pint "
                "golden ale and Stout, alongside guest casks. Free live music every Sunday."
            ),
            "known_for": "A Grade II-listed 1888 interior of tiled perfection and Marble Brewery cask ale",
            "good_for": "A pint of Manchester Bitter in one of the country's great pub rooms",
            "source_url": "https://marblebeers.com/the-marble-arch/",
            "verified": "2026-06-22",
        },
    ],
    "food_scene": [
        (
            "Manchester's food geography runs from the city centre outward in all directions. "
            "The Northern Quarter, bordered by Piccadilly and Shudehill, is the hub of "
            "independent cafes, brunch spots and neighbourhood restaurants, and neighbouring "
            "Ancoats — once a Victorian industrial district and now one of the UK's most "
            "exciting dining neighbourhoods — adds Michelin-recognised restaurants, artisan "
            "bakeries and canal-side cafes around Cutting Room Square and New Islington Marina."
        ),
        (
            "Two miles south along Wilmslow Road lies Rusholme, home to the Curry Mile: "
            "the densest concentration of South Asian restaurants in Europe, a strip of neon "
            "signs and aromatic smoke serving Pakistani karahi, Mughlai-style grills, Middle "
            "Eastern shawarma and Bangladeshi curries from early evening until well past "
            "midnight. Manchester's Chinatown, a short walk from Piccadilly Gardens, adds "
            "a compact but long-established cluster of Cantonese, Vietnamese and Thai kitchens."
        ),
        (
            "The city holds a serious fine-dining tier — Mana in Ancoats holds a Michelin "
            "star, and Erst on Blossom Street in Ancoats carries a Bib Gourmand — but what "
            "makes Manchester distinctive is the depth below that level: independent breweries, "
            "Gujarati street-food bars, a bakery scene anchored by Pollen, and a Curry Mile "
            "that has fed the city since the 1950s. A Manchester eating day can move from "
            "a cruffin at a waterside cafe to a charcoal-pit curry without repeating a flavour."
        ),
    ],
    "visit": [
        (
            "The geography is manageable. Bundobust and the city-centre pubs sit around "
            "Piccadilly, while Ancoats — home to Pollen Bakery and a cluster of restaurants "
            "on Blossom Street — is a fifteen-minute walk east along Great Ancoats Street. "
            "The Marble Arch is a short walk north along Rochdale Road. All of this is linked "
            "by the Metrolink tram network and easy walking. Rusholme's Curry Mile is two "
            "miles south: take a bus from Piccadilly Gardens or a short taxi ride."
        ),
        (
            "The natural day runs: a sourdough breakfast at Pollen Bakery beside the marina, "
            "a wander through the Northern Quarter for coffee, Bundobust for lunch with a "
            "Marble Brewery pint, and an evening on the Curry Mile at Mughli, booking ahead "
            "for their late sittings. Pollen keeps weekday hours from Wednesday and closes "
            "at 4pm, so plan the bakery stop for the morning."
        ),
    ],
    "checklist": [
        "Arrive at Pollen Bakery on a weekday morning before the cruffins sell out",
        "Book Mughli for an evening sitting — tables through to midnight, great cocktails too",
        "Head to Bundobust for lunch with no booking; go early to beat the queue",
        "Walk Rochdale Road for The Marble Arch; look up at the tiled ceiling immediately",
        "Use the Metrolink tram or bus for Rusholme — the Curry Mile is two miles south",
    ],
    "what_to_order": (
        "Order with intent. At Bundobust, build a spread: okra fries, bhel puri and a dahi "
        "puri to start, then a kofta or tikka with a Bundobust lager. At Pollen, a cruffin "
        "or croissant while they last, and a sourdough loaf to take home. At Mughli, lead "
        "with the charcoal-pit lamb chops or seekh kebabs from the angithi, then the butter "
        "chicken or a slow karahi. At The Marble Arch, a pint of Manchester Bitter on cask, "
        "taken slowly while you read every tile on the ceiling."
    ),
    "glance": [
        ("Best for a quick bite", "Bundobust, for Gujarati plates and craft beer off Piccadilly"),
        ("Best for an occasion", "Mughli Charcoal Pit, for a long Curry Mile dinner with cocktails"),
        ("Best for atmosphere", "The Marble Arch's Grade II-listed 1888 tiled interior"),
    ],
    "faq": [
        (
            "Where is the best place to eat on Manchester's Curry Mile?",
            "Mughli Charcoal Pit at 30 Wilmslow Road, Rusholme, is the Curry Mile's standout "
            "independent: open since 1991 and still family-run, it centres its kitchen on a "
            "charcoal angithi pit for grills and tandoori, alongside a full curry menu. Book "
            "ahead for evenings; it opens Monday to Saturday from 5pm, Sunday from 2pm."
        ),
        (
            "What is Bundobust and is it suitable for vegetarians?",
            "Bundobust at 61 Piccadilly is an all-vegetarian Gujarati street food restaurant "
            "and craft beer bar. Founded in Leeds in 2014, it opened in Manchester in 2016. "
            "The menu includes okra fries, bhel puri, dahi puri and kofta, designed for "
            "sharing, with beers brewed at the Bundobust Brewery on Oxford Street. "
            "Open daily from midday, no bookings taken."
        ),
        (
            "Which is Manchester's best independent bakery?",
            "Pollen Bakery, at Cotton Field Wharf in Ancoats, is widely regarded as "
            "Manchester's finest artisan bakery. Founded by Hannah Calvert and Chris Kelly "
            "in 2016, it was named by the Good Food Guide as one of the best bakeries in "
            "Britain, with 28-hour sourdough loaves and cruffins that became a city-wide "
            "cult. The waterside Ancoats cafe is open Wednesday to Sunday."
        ),
        (
            "What makes The Marble Arch pub special?",
            "The Marble Arch at 73 Rochdale Road, built in 1888, has one of the most "
            "remarkable pub interiors in England: a mosaic-tiled sloping floor, glazed "
            "ceramic walls and a barrel-vaulted tiled ceiling restored in the 1980s. It "
            "is Grade II listed, holds a CAMRA interior of outstanding national historic "
            "importance, and has appeared in the Good Beer Guide for over 25 consecutive "
            "years. Marble Brewery was founded at the back of the building in 1997."
        ),
        (
            "Which areas of Manchester are best for independent restaurants?",
            "The Northern Quarter and neighbouring Ancoats are the city's strongest "
            "independent dining neighbourhoods, with bakeries, brunch spots, neighbourhood "
            "restaurants and Michelin-recognised venues clustered within a walkable area. "
            "Rusholme's Curry Mile, two miles south along Wilmslow Road, is the place "
            "for South Asian cooking, and Chinatown sits close to Piccadilly Gardens."
        ),
        (
            "Are any of the Manchester picks Michelin-recognised?",
            "Bundobust Manchester Piccadilly has received Michelin recognition as part "
            "of the guide's street food recommendations. Nearby Ancoats also holds two "
            "Michelin-recognised restaurants in the guide: Mana (one star) and Erst "
            "(Bib Gourmand), reflecting the neighbourhood's rise as a serious dining "
            "destination. All four picks in this guide are confirmed currently trading."
        ),
    ],
}

# edinburgh ----------------------------------------------------------
TOWNS["edinburgh"] = {
    "region": "Scotland",
    "population": "530K",
    "nearby": ["Livingston", "Dunfermline", "Musselburgh"],
    "meta_title": "Best Places to Eat in Edinburgh: Local Food Guide",
    "meta_description": (
        "Edinburgh: 1979 halal takeaway, pioneering speciality roaster, "
        "Michelin-starred tasting menu, and a 1747 Leith real-ale pub. "
        "Read the guide."
    ),
    "trust_strip": (
        "From a legendary late-night halal counter to Scotland's oldest "
        "speciality roastery, Edinburgh's independent food scene rewards "
        "every mood and budget"
    ),
    "snapshot": (
        "For a fast answer: Kebab Mahal on Nicolson Square for a tandoori "
        "kebab that has fed the Old Town since 1979, Artisan Roast on "
        "Broughton Street for Scotland's pioneering speciality roast, "
        "Condita on Salisbury Place for a one-Michelin-star surprise tasting "
        "menu built on Scottish produce, and the Malt and Hops on the Shore "
        "in Leith for eight real ales in a bar dating from 1747. Four moods, "
        "one remarkable capital."
    ),
    "stats": [
        ("530K", "City population (approx)"),
        ("1747", "Year the Malt and Hops first poured a pint"),
        ("2007", "Year Artisan Roast opened Scotland's first speciality cafe"),
        ("4", "Hand-picked independents"),
    ],
    "pivot_variant": "high-volume",
    "pivot_local_hook": (
        "Edinburgh's kitchens run a heavy cycle: high-volume tandoors and "
        "charcoal grills in the Old Town, festival-season fryers working "
        "around the clock in August, and the waterfront restaurants of Leith "
        "pushing coastal grease loads through their canopies service after "
        "service."
    ),
    "venues": [
        {
            "type": "Takeaway",
            "name": "Kebab Mahal",
            "area": "7 Nicolson Square, Southside (edge of the Old Town)",
            "cuisine": "Halal Indian, tandoori kebabs",
            "body": (
                "Kebab Mahal has been feeding the Southside since 1979, making it one "
                "of Edinburgh's oldest continuously trading South Asian kitchens. The "
                "no-frills halal cafe-takeaway on Nicolson Square is a short walk from "
                "the Royal Mile and has built a devoted following among students, "
                "locals and late-night revellers across nearly five decades. The menu "
                "keeps it simple and keeps it honest: sizzling tandoori kebabs, "
                "biryanis, bhuna and kofte, all halal, all priced to feed you for "
                "under a fiver. The chicken and lamb sheesh kebabs are the standout "
                "order, pulled from the tandoor and wrapped with freshly made naan. "
                "Open daily until midnight, and until 2am on Fridays and Saturdays."
            ),
            "known_for": "Tandoori kebabs and biryani served since 1979, open until 2am",
            "good_for": "A cheap, honest, late-night meal in the Old Town",
            "source_url": "https://www.kebabmahaledinburgh.co.uk/",
            "verified": "2026-06-22",
        },
        {
            "type": "Cafe",
            "name": "Artisan Roast",
            "area": "57 Broughton Street, New Town",
            "cuisine": "Speciality coffee, homemade cakes",
            "body": (
                "When Artisan Roast opened on Broughton Street in summer 2007, it was "
                "the first speciality coffee roaster in Scotland, and the cluttered, "
                "bohemian room it occupies remains one of the most characterful cafes "
                "in the country. Coffee sacks hang on the walls, bulbs dangle at "
                "table height using cafetieres as lampshades, and the roasting is "
                "done properly: single-origin beans sourced with care and served as "
                "espresso, filter or cold brew. In 2012 Artisan Roast became the "
                "first coffee company ever to win the Glenfiddich Spirit of Scotland "
                "Award. The company now has four shops across the city and roasts in "
                "Peffermill, but the Broughton Street original is where it all began, "
                "and where the spirit of that first cup still lives."
            ),
            "known_for": "Scotland's first speciality roaster, open since 2007 on Broughton Street",
            "good_for": "A serious coffee in Edinburgh's most characterful independent cafe",
            "source_url": "https://artisanroast.co.uk/pages/broughtonstreet-cafe",
            "verified": "2026-06-22",
        },
        {
            "type": "Restaurant",
            "name": "Condita",
            "area": "15 Salisbury Place, Southside",
            "cuisine": "Michelin-starred Scottish tasting menu",
            "body": (
                "Tucked quietly on the Southside, Condita is one of Edinburgh's most "
                "distinctive dining rooms: a small, owner-run shop conversion with "
                "twelve seats at candle-lit Scottish mid-century modern tables, and a "
                "single surprise tasting menu that changes with the season. Chef Tyler "
                "King builds every course around the larder of Scotland: fish from "
                "Hebrides, Orkney, Shetland and the east coast; meat and game from "
                "Fife and the Highlands; produce from the restaurant's own garden and "
                "allotment. The result has held one Michelin star for six consecutive "
                "years, retained in the 2026 Guide. Dinner runs to around two and a "
                "half hours and costs around 160 pounds; bookings essential and "
                "typically taken weeks ahead. Open Tuesday to Saturday evenings only."
            ),
            "known_for": "One-Michelin-star surprise tasting menu using Scottish produce",
            "good_for": "An intimate, landmark special-occasion dinner on the south side",
            "source_url": "https://www.condita.co.uk/",
            "verified": "2026-06-22",
        },
        {
            "type": "Pub",
            "name": "The Malt and Hops",
            "area": "45 The Shore, Leith",
            "cuisine": "Real ale, classic pub food",
            "body": (
                "The Malt and Hops sits on the Shore at the heart of Leith's "
                "waterfront revival, in a building that dates from 1747 and was "
                "trading as the Drawbridge for most of the twentieth century. "
                "Renamed and relaunched in 1992, it is now one of the best real-ale "
                "pubs in Scotland: a CAMRA Good Beer Guide regular that pours eight "
                "handpulled ales at any one time, with more casks racked and ready "
                "behind the bar. The single room is wonderfully old-fashioned, with a "
                "real fire, pump clips from long-gone breweries hanging from the "
                "ceiling alongside hop bines renewed every harvest, and mirrors lining "
                "the walls. Pub food runs to haggis, neeps and tatties, steak pie and "
                "fish and chips. An authentic Leith local."
            ),
            "known_for": "Eight real ales, CAMRA Good Beer Guide, a bar dating from 1747",
            "good_for": "A pint of cask ale in an atmospheric Leith Shore pub",
            "source_url": "https://camra.org.uk/pubs/malt-hops-edinburgh-151306",
            "verified": "2026-06-22",
        },
    ],
    "food_scene": [
        (
            "Edinburgh's food map divides neatly between the Old Town's tourist-facing "
            "Royal Mile strip and the more characterful eating hidden a few streets "
            "away. Grassmarket hosts a Saturday farmers market with local producers, "
            "while Victoria Street and the Cowgate hold some of the city's best "
            "independent restaurants and wine bars tucked into medieval closes. The "
            "Southside, around Nicolson Square and Clerk Street, carries the everyday "
            "neighbourhood eating that feeds the university quarter, including the "
            "beloved Kebab Mahal."
        ),
        (
            "Leith is Edinburgh's most evolved food district: the former port neighbourhood "
            "has spent three decades building a serious restaurant and bar scene along "
            "the Shore and into the back streets, driven by the quality of its seafood "
            "access and a bohemian local culture. The Malt and Hops is one of its "
            "original anchors. Stockbridge, on the New Town edge, has a Sunday market "
            "and a strong run of independent cafes, delis and neighbourhood restaurants "
            "that make it the suburb Edinburghers are most likely to eat in on their "
            "day off."
        ),
        (
            "Beyond the familiar, Edinburgh has developed a serious fine-dining scene "
            "to sit alongside its street-food and pub culture. The 2026 Michelin Guide "
            "saw the city gain two new stars alongside Condita's sixth consecutive "
            "retention, reflecting a depth of talent that makes it one of the strongest "
            "restaurant cities in the UK outside London. The food ranges from the "
            "classic Scottish larder - haggis with neeps and tatties, Cullen skink, "
            "fresh Hebridean fish - to the adventurous cooking of a new generation of "
            "chef-owners working with that same Scottish produce."
        ),
    ],
    "visit": [
        (
            "The city's geography is manageable on foot. Kebab Mahal is a ten-minute "
            "walk south from Waverley station along South Bridge; Artisan Roast sits "
            "in the New Town a fifteen-minute walk north-east of the station via Broughton "
            "Street; and Condita is a twenty-minute walk south from the centre on "
            "Salisbury Place. Leith and the Malt and Hops are a short bus or taxi ride "
            "down Leith Walk, or a twenty-five-minute walk from Princes Street."
        ),
        (
            "Edinburgh rewards a logical order. Start the day with a flat white at "
            "Artisan Roast on Broughton Street, explore the New Town and Old Town, "
            "book Condita for the evening, and end in Leith for a pint at the Malt "
            "and Hops. Kebab Mahal is the answer to late nights and festival weekends: "
            "it trades until 2am on Fridays and Saturdays and has been doing so for "
            "nearly fifty years. Book Condita at least several weeks ahead."
        ),
    ],
    "checklist": [
        "Start at Artisan Roast on Broughton Street for Scotland's original speciality coffee",
        "Walk the Old Town and Grassmarket before doubling back south to Nicolson Square",
        "Book Condita weeks ahead for the surprise tasting menu - it sells out fast",
        "Take the bus or walk down Leith Walk to the Shore for a pint at the Malt and Hops",
        "Kebab Mahal is open until 2am on weekends - the definitive late-night stop",
    ],
    "what_to_order": (
        "Order with intent. At Kebab Mahal, the chicken or lamb sheesh kebab from "
        "the tandoor, wrapped in freshly made naan - they have been the signature for "
        "nearly fifty years. At Artisan Roast, ask what is on the rotating single-origin "
        "espresso, or take a filter and settle into the cluttered, characterful room. "
        "At Condita, there is no menu to choose from: surrender to the surprise, built "
        "around Scottish fish and game. At the Malt and Hops, ask what is on the eight "
        "handpulls and take whichever comes from a smaller Scottish or Lake District "
        "brewery, alongside a bowl of haggis, neeps and tatties."
    ),
    "glance": [
        ("Best for a quick bite", "Kebab Mahal, for a tandoori kebab that has served the Old Town since 1979"),
        ("Best for an occasion", "Condita, for a one-Michelin-star surprise tasting menu on the Southside"),
        ("Best for atmosphere", "The Malt and Hops, an 1747 real-ale pub on Leith Shore"),
    ],
    "faq": [
        (
            "Where can I get a good late-night meal in Edinburgh?",
            "Kebab Mahal on Nicolson Square has been serving halal tandoori kebabs and "
            "biryanis since 1979 and is open until midnight daily, and until 2am on "
            "Fridays and Saturdays. It is a short walk from the Royal Mile and one of "
            "Edinburgh's great budget institutions.",
        ),
        (
            "Which Edinburgh cafe has the best independent coffee?",
            "Artisan Roast on Broughton Street, Scotland's first speciality coffee "
            "roaster, opened in 2007 and won the Glenfiddich Spirit of Scotland Award "
            "in 2012. The Broughton Street original roasts single-origin beans on site "
            "and serves them in one of the city's most characterful cafe interiors.",
        ),
        (
            "Does Edinburgh have a Michelin-starred restaurant?",
            "Yes. Condita on Salisbury Place, an owner-run restaurant with twelve seats "
            "and a surprise tasting menu by chef Tyler King, has held one Michelin star "
            "for six consecutive years, retaining it in the 2026 Guide. It focuses on "
            "Scottish fish, meat and game and books up weeks in advance.",
        ),
        (
            "What is the best pub in Leith for real ale?",
            "The Malt and Hops at 45 The Shore, a CAMRA Good Beer Guide regular in a "
            "building dating from 1747, pours eight handpulled ales at any one time "
            "with more casks ready behind the bar. The single room has a real fire, "
            "historic pump clips and hop bines, and serves haggis and steak pie.",
        ),
        (
            "What food is Edinburgh most famous for?",
            "Scotland's national dish, haggis with neeps and tatties, is found across "
            "the city, alongside Cullen skink (smoked haddock soup), the Scotch pie, "
            "and exceptional fresh seafood from Hebridean and east-coast waters. "
            "Edinburgh's restaurant scene has grown beyond the traditional, with a "
            "new generation of chefs working the same Scottish larder in more "
            "adventurous ways.",
        ),
        (
            "Can you eat well in Edinburgh on a budget?",
            "Easily. Kebab Mahal on Nicolson Square has fed the Southside for nearly "
            "fifty years with halal tandoori meals under a fiver. Artisan Roast on "
            "Broughton Street serves serious speciality coffee without a premium price. "
            "The Malt and Hops in Leith is an honest pub with good real ale and "
            "pub-food classics at pub prices.",
        ),
    ],
}

# liverpool ----------------------------------------------------------
TOWNS["liverpool"] = {
    "region": "Merseyside",
    "population": "500K",
    "nearby": ["Birkenhead", "Bootle", "Wallasey"],
    "meta_title": "Best Places to Eat in Liverpool: Local Food Guide",
    "meta_description": (
        "Where to eat in Liverpool: a community pie bakery in Anfield, a "
        "Bold Street cafe, a Michelin-listed dining room and a historic pub. "
        "Read the guide."
    ),
    "trust_strip": (
        "From a community co-op pie shop in Anfield to a Michelin-listed "
        "fine-dining room in the Georgian Quarter, Liverpool feeds its own "
        "with fierce local pride"
    ),
    "snapshot": (
        "For a fast answer: Homebaked in Anfield for a scouse pie baked by "
        "the city's own community co-op, Maggie May's on Bold Street for a "
        "hearty bowl of scouse and a full breakfast, The Art School on "
        "Sugnall Street for Paul Askew's Michelin-listed modern British, and "
        "Ye Cracke on Rice Street for cask ale in John Lennon's old local. "
        "Four moods, one city with its own language, its own dish and its "
        "own way of doing things."
    ),
    "stats": [
        ("500K", "City population (approx)"),
        ("1913", "Year Homebaked's predecessor bakery first opened in Anfield"),
        ("Bold Street", "Liverpool's independent food and cafe heartland"),
        ("4", "Hand-picked independents"),
    ],
    "pivot_variant": "high-volume",
    "pivot_local_hook": (
        "Liverpool's kitchens run the full register from Anfield pie ovens "
        "to Georgian Quarter fine-dining pass — high-volume services day and "
        "night push a heavy load of grease-laden vapour into canopies across "
        "the city."
    ),
    "venues": [
        {
            "type": "Takeaway/Casual",
            "name": "Homebaked",
            "area": "197-199 Oakfield Road, Anfield",
            "cuisine": "Artisan pies, scouse pie",
            "body": (
                "Homebaked began as a Liverpool Biennial art project in 2010 "
                "and became a fully trading community co-operative bakery in "
                "2013, taking over the century-old Mitchell's bakery shop a "
                "few minutes from Anfield stadium. The scouse pie — braised "
                "beef, potato and onion in a short-crust case — is the "
                "signature and has won multiple prizes at the British Pie "
                "Awards. On match days the queue stretches to the pavement. "
                "The co-op reinvests profits into the Anfield community, "
                "creating jobs for local people and supporting food banks. "
                "Nothing else on this guide tastes as specifically of "
                "Liverpool."
            ),
            "known_for": "Award-winning scouse pie from a community co-operative",
            "good_for": "A proper Anfield bite before or after a match, or any day",
            "source_url": "https://www.tripadvisor.com/Restaurant_Review-g186337-d6778226-Reviews-Homebaked_Anfield-Liverpool_Merseyside_England.html",
            "verified": "2026-06-22",
        },
        {
            "type": "Cafe",
            "name": "Maggie May's",
            "area": "90 Bold Street, city centre",
            "cuisine": "Traditional cafe, scouse, full breakfast",
            "body": (
                "Maggie May's has occupied its corner of Bold Street for "
                "decades, making it one of the oldest continuously trading "
                "independents on one of the city's best-loved streets. The "
                "draw is straightforward: a big bowl of scouse — beef or "
                "lamb stew with potatoes and onions, served with crusty "
                "bread and a side of pickled red cabbage or beetroot — "
                "alongside the kind of full English that powers a morning's "
                "walk around the docks. The room is unpretentious, the "
                "prices are some of the fairest on Bold Street, and regulars "
                "treat it as a canteen. It is the place to try Liverpool's "
                "signature dish in its natural habitat."
            ),
            "known_for": "Traditional scouse stew and hearty breakfasts on Bold Street",
            "good_for": "An affordable, unfussy taste of Liverpool's culinary identity",
            "source_url": "https://www.yelp.co.uk/biz/maggie-mays-liverpool",
            "verified": "2026-06-22",
        },
        {
            "type": "Restaurant",
            "name": "The Art School",
            "area": "1 Sugnall Street, Georgian Quarter",
            "cuisine": "Modern British fine dining",
            "body": (
                "Chef-patron Paul Askew opened The Art School in September "
                "2014 inside a former Victorian building — the 1888 Home for "
                "Destitute Children on Sugnall Street — and has run it as "
                "Liverpool's leading independent fine-dining room ever since. "
                "The restaurant holds Michelin Guide recognition and two AA "
                "Rosettes, and in 2025 was named best restaurant in Liverpool "
                "at the British Restaurant Awards and Hospitality Champion at "
                "the Good Small Business Awards. The cooking is modern "
                "British with French classical technique, with tasting, "
                "excellence and prix fixe menus built around seasonal produce. "
                "Book well ahead; the Georgian Quarter room fills quickly."
            ),
            "known_for": "Michelin-listed modern British dining, two AA Rosettes",
            "good_for": "A landmark special-occasion meal in Liverpool's finest room",
            "source_url": "https://guide.michelin.com/gb/en/merseyside/liverpool/restaurant/the-art-school",
            "verified": "2026-06-22",
        },
        {
            "type": "Pub",
            "name": "Ye Cracke",
            "area": "13 Rice Street, Georgian Quarter",
            "cuisine": "Real ale, pub food",
            "body": (
                "Ye Cracke traces its roots to 1852 — when it was known as "
                "the Ruthin Castle — and took its current name in 1892. The "
                "multi-roomed pub on Rice Street, a short walk from the "
                "Liverpool Institute, is famous as John Lennon's local during "
                "his art college years in the late 1950s: he and Stuart "
                "Sutcliffe were regulars and it was here he courted his first "
                "wife, Cynthia Powell. CAMRA recognises it as a Real Heritage "
                "Pub. Independent owner Mike Girling completed a careful "
                "£200,000 restoration in August 2024 that uncovered worn "
                "wooden floors and preserved the historic War Office snug, "
                "while keeping five rotating cask ales on tap."
            ),
            "known_for": "John Lennon's local, CAMRA heritage pub, rotating cask ales",
            "good_for": "A pint in a slice of genuine Liverpool history",
            "source_url": "https://liverpoolstandard.co.uk/local/liverpool-city-centre/one-of-liverpools-most-famous-pubs-reopens-with-a-new-200k-look/",
            "verified": "2026-06-22",
        },
    ],
    "food_scene": [
        (
            "Liverpool's food geography runs along a handful of distinctive "
            "corridors. Bold Street, rising south from the city centre, is the "
            "independent spine — packed with cafes, casual eateries and wine "
            "bars that have made it the most visited stretch of independent "
            "hospitality in the city. Maggie May's is the elder statesman; "
            "around it cluster Maray's Middle Eastern small plates (opened "
            "2014), speciality roasters such as 92 Degrees Coffee and dozens "
            "of other independents that have seeded themselves over the past "
            "decade."
        ),
        (
            "South of Bold Street, the Baltic Triangle — a former warehousing "
            "district — has become Liverpool's creative and street-food quarter, "
            "home to the Baltic Market, brewery taprooms and converted "
            "industrial spaces. North of the centre, in Anfield, the city's "
            "football culture overlaps with its food culture at Homebaked, the "
            "community bakery co-operative that makes the scouse pie the "
            "neighbourhood has eaten for generations."
        ),
        (
            "The Georgian Quarter around Hope Street and Hardman Street ties "
            "the food scene to the city's architectural heritage. The Art "
            "School on Sugnall Street and a cluster of independent wine bars "
            "and bistros sit among the Grade I listed terraces, a short walk "
            "from both cathedrals. Scouse — a slow-cooked beef or lamb stew "
            "with potatoes, onions and carrots, so tied to the city that "
            "Liverpudlians have been called Scousers for nearly two centuries "
            "— is the dish that connects all of it, from pie-shop counter to "
            "tasting-menu riff."
        ),
    ],
    "visit": [
        (
            "The practical geography is friendly. Bold Street, the Georgian "
            "Quarter and the Baltic Triangle all sit within a ten-minute walk "
            "of Liverpool Central and Lime Street stations. Maggie May's, The "
            "Art School and Ye Cracke form a compact circuit in the "
            "Georgian Quarter end of the city centre, while Homebaked in "
            "Anfield is around two miles north, a short bus ride on the 17 "
            "or 26 from the city centre — or an easy walk from Anfield stadium "
            "on match days."
        ),
        (
            "Time the day well: a breakfast or lunch at Maggie May's, a walk "
            "south through the Baltic Triangle, a pint of cask ale at Ye Cracke "
            "in the afternoon, and The Art School for dinner if the occasion "
            "demands it. Homebaked is best saved for a separate Anfield "
            "excursion, ideally on a match day when the queue and the "
            "atmosphere are at their liveliest."
        ),
    ],
    "checklist": [
        "Visit Homebaked in Anfield for a scouse pie — go on a match day for the full atmosphere",
        "Breakfast or lunch at Maggie May's on Bold Street for traditional scouse stew",
        "Walk Bold Street end to end and explore the Baltic Triangle",
        "Book The Art School well ahead; tables in the Georgian Quarter dining room go quickly",
        "End at Ye Cracke on Rice Street for a heritage pint — find the War Office snug",
    ],
    "what_to_order": (
        "Order with intent. At Homebaked, the scouse pie — beef, potato and "
        "onion in short-crust pastry — is the only order worth making. At "
        "Maggie May's, a bowl of scouse with bread, butter and pickled "
        "cabbage; the full breakfast if you arrive in the morning. At The "
        "Art School, put yourself in Paul Askew's hands with the tasting menu "
        "and let the wine list do the work. At Ye Cracke, a pint of whatever "
        "is on the rotating cask, taken slowly in the War Office snug."
    ),
    "glance": [
        ("Best for a quick bite", "Homebaked, for a scouse pie straight from the Anfield community co-op"),
        ("Best for an occasion", "The Art School, for Michelin-listed modern British in the Georgian Quarter"),
        ("Best for atmosphere", "Ye Cracke, John Lennon's local since the late 1950s, restored and independent"),
    ],
    "faq": [
        (
            "Where can I eat a traditional scouse in Liverpool?",
            "Maggie May's on Bold Street has served traditional scouse stew — "
            "beef or lamb with potatoes, onions and carrots, with pickled red "
            "cabbage and crusty bread — for decades, and is one of the most "
            "straightforward places in the city to try the dish.",
        ),
        (
            "What is scouse and why is it Liverpool's signature dish?",
            "Scouse is a slow-cooked beef or lamb stew, descended from the "
            "Norwegian sailor's dish lobscouse brought to Liverpool by Baltic "
            "and North Sea sailors in the eighteenth and nineteenth centuries. "
            "It fed the port city's working population so reliably that "
            "Liverpudlians themselves became known as Scousers.",
        ),
        (
            "Does Liverpool have a Michelin restaurant?",
            "The Art School on Sugnall Street in the Georgian Quarter is in "
            "the Michelin Guide and holds two AA Rosettes. Chef-patron Paul "
            "Askew opened it in 2014 and it was named best restaurant in "
            "Liverpool at the British Restaurant Awards 2025.",
        ),
        (
            "Which is Liverpool's most historic pub?",
            "Ye Cracke on Rice Street dates to 1852 and is recognised by CAMRA "
            "as a Real Heritage Pub. It was John Lennon's local during his art "
            "college years in the late 1950s, and independent owner Mike "
            "Girling completed a careful restoration in 2024, reopening the "
            "multi-roomed pub with five rotating cask ales.",
        ),
        (
            "What is the Homebaked bakery in Anfield?",
            "Homebaked is a community co-operative bakery on Oakfield Road "
            "near Anfield stadium, trading since 2013 from a building that was "
            "a bakery shop for over a century. It is best known for its "
            "award-winning scouse pie — braised beef, potato and onion in "
            "short-crust pastry — and reinvests profits into the Anfield "
            "community.",
        ),
        (
            "Can you visit all four places on one Liverpool food day?",
            "Three of the four sit within a walkable circuit of Liverpool "
            "Central station: Maggie May's and Ye Cracke are on or near Bold "
            "Street and Rice Street, and The Art School is a short walk into "
            "the Georgian Quarter. Homebaked in Anfield is around two miles "
            "north, best reached by bus or on a match day when the atmosphere "
            "in the neighbourhood is at its best.",
        ),
    ],
}

# bristol ----------------------------------------------------------
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

# cardiff ----------------------------------------------------------
TOWNS["cardiff"] = {
    "region": "Wales",
    "population": "390K",
    "nearby": ["Newport", "Penarth", "Barry"],
    "meta_title": "Best Places to Eat in Cardiff: Local Food Guide",
    "meta_description": (
        "Wood-fired pizza in the Victorian Market, an arcade teahouse, "
        "Cardiff first Michelin star and Welsh craft ale. "
        "Four independents. Read the guide."
    ),
    "trust_strip": (
        "From wood-fired pizza in a Victorian market to Cardiff's first "
        "Michelin-starred tasting menu, the Welsh capital punches well above "
        "its weight for independent food"
    ),
    "snapshot": (
        "For a fast answer: Ffwrnes Pizza at Cardiff Central Market for "
        "wood-fired Neapolitan with Welsh toppings, Waterloo Tea in the "
        "Wyndham Arcade for one of the finest teahouses in Britain, Gorse "
        "on Kings Road in Pontcanna for Cardiff's first Michelin-starred "
        "Welsh tasting menu, and Tiny Rebel on Westgate Street for craft "
        "ale from Wales's Supreme Champion Beer of Britain brewery. Four "
        "moods, one walkable Welsh capital."
    ),
    "stats": [
        ("390K", "Cardiff population (approx)"),
        ("2025", "Year Cardiff earned its first Michelin star"),
        ("5", "Cardiff's Victorian and Edwardian shopping arcades"),
        ("4", "Hand-picked independents"),
    ],
    "pivot_variant": "high-volume",
    "pivot_local_hook": (
        "Cardiff's food scene runs from wood-fired pizza ovens in a Victorian "
        "market to the tasting-menu kitchens of Pontcanna, each service "
        "pushing a heavy load of grease-laden vapour into canopies above "
        "the pass."
    ),
    "venues": [
        {
            "type": "Takeaway",
            "name": "Ffwrnes Pizza",
            "area": "Cardiff Central Market, St Mary Street (first floor stalls)",
            "cuisine": "Wood-fired Neapolitan pizza, Welsh ingredients",
            "body": (
                "Ffwrnes (Welsh for 'oven') began as a Piaggio van called Smokey Pete "
                "in 2014, when friends Ieuan Harry and Jeremy Phillips took their "
                "wood-fired rig to events across Wales. With a Development Bank of "
                "Wales micro-loan they graduated to a permanent stall on the first "
                "floor of Cardiff's Victorian Central Market, opening there in 2018. "
                "The set-up is deliberately simple: a short list of twelve Neapolitan-"
                "style pizzas made with Welsh produce — salt-marsh lamb, local chorizo, "
                "Welsh cheese — fired in a proper wood oven, then eaten standing at a "
                "counter or taken away. The 'Pizza Boys', as they are known from a BBC "
                "series and the Welsh-language Bois y Pizza on S4C, have become one of "
                "Cardiff's most-loved food stories. The food hygiene check confirmed "
                "them trading in February 2026."
            ),
            "known_for": "Welsh-ingredient wood-fired Neapolitan pizza in a Victorian market",
            "good_for": "A fast, characterful lunch in a historic setting",
            "source_url": "https://ratings.food.gov.uk/business/1076564/ffwrnes-pizza-cardiff",
            "verified": "2026-06-22",
        },
        {
            "type": "Cafe",
            "name": "Waterloo Tea",
            "area": "Wyndham Arcade, Mill Lane, city centre",
            "cuisine": "Speciality tea and coffee, all-day cafe",
            "body": (
                "Kasim Ali founded Waterloo Tea in Penylan in 2008 and within a year "
                "the tea house had been named Best Cafe in the UK by the Beverage "
                "Standards Association, after three unannounced visits. The Wyndham "
                "Arcade branch, which opened in 2014, sits inside one of the city's "
                "oldest covered arcades — iron-and-glass Victorian vaulting, built in "
                "1887 — and offers a selection of more than 60 loose-leaf teas sourced "
                "from India, China, Sri Lanka, Taiwan and Japan, alongside speciality "
                "coffee roasted locally by Hard Lines. The two-floor space is calm and "
                "unhurried, with an afternoon tea of handmade sandwiches, scones with "
                "clotted cream and seasonal cakes. January 2026 reviews confirm it is "
                "actively trading with consistently high ratings."
            ),
            "known_for": "60-plus loose-leaf teas, UK's Best Cafe award, Victorian arcade setting",
            "good_for": "A long, relaxed tea break or afternoon tea in a remarkable room",
            "source_url": "https://waterlootea.com/pages/city-centre",
            "verified": "2026-06-22",
        },
        {
            "type": "Restaurant",
            "name": "Gorse",
            "area": "186-188 Kings Road, Pontcanna",
            "cuisine": "Modern Welsh fine dining, tasting menu",
            "body": (
                "Tom Waters trained at The Square and at Heston Blumenthal's Fat Duck "
                "before returning to his native Wales to open Gorse in Pontcanna in "
                "May 2024. Less than nine months later, in February 2025, it became "
                "Cardiff's first ever Michelin-starred restaurant. The small dining "
                "room — an open kitchen, a handful of tables, handcrafted Welsh "
                "ceramics on every surface — serves a tasting menu of seven or ten "
                "courses built around micro-seasonal Welsh produce: seaweed from the "
                "Pembrokeshire coast, mountain lamb, foraged herbs. Waters describes "
                "his aim as putting the best of Wales on the plate, and the 2026 "
                "Michelin Guide confirmed the star retained. Book well ahead; the "
                "restaurant opens Wednesday evenings and Thursday to Saturday for "
                "lunch and dinner."
            ),
            "known_for": "Cardiff's first Michelin star, modern Welsh seasonal tasting menu",
            "good_for": "A landmark occasion meal rooted in Welsh landscape and produce",
            "source_url": "https://guide.michelin.com/gb/en/south-glamorgan/cardiff/restaurant/gorse",
            "verified": "2026-06-22",
        },
        {
            "type": "Pub",
            "name": "Tiny Rebel Cardiff",
            "area": "25 Westgate Street, city centre (by Principality Stadium)",
            "cuisine": "Craft beer, pub food",
            "body": (
                "Tiny Rebel was founded in Newport in 2012 by brothers-in-law Bradley "
                "Cummings and Gareth Williams. Their Cwtch red ale won Supreme "
                "Champion Beer of Britain in 2015 — the youngest brewery and the first "
                "from Wales to take the title. The Cardiff bar opened in 2013 in a "
                "Grade II listed building on Westgate Street — a late-Victorian county "
                "club with heavy iron shutters on the original treasury windows — just "
                "yards from the Principality Stadium. Two floors of quirky rooms pour "
                "Tiny Rebel's own beers alongside rotating craft lines and up to four "
                "Welsh ciders. May 2026 reviews confirm it is open and busy, with "
                "quiz nights, vinyl evenings and an accessible food menu running "
                "Monday to Saturday until 9pm."
            ),
            "known_for": "Cwtch, Supreme Champion Beer of Britain 2015, Grade II listed building",
            "good_for": "A pint of award-winning Welsh craft ale in a characterful listed pub",
            "source_url": "https://www.tinyrebel.co.uk/bars/cardiff",
            "verified": "2026-06-22",
        },
    ],
    "food_scene": [
        (
            "Cardiff's food map is shaped by its Victorian heritage and its position as a "
            "young, outward-looking capital. The city centre is threaded by five covered "
            "arcades — more Victorian and Edwardian covered walkways than any other city "
            "in the UK — and these have become home to some of its most creative "
            "independent food businesses, from loose-leaf tea rooms to deli counters. "
            "Cardiff Central Market, built in 1891 inside an ornate iron-and-glass "
            "structure, hosts wood-fired pizza, pierogi and souvlaki stalls alongside "
            "the oldest fishmongers and butchers in the city."
        ),
        (
            "A short walk west, the neighbourhoods of Pontcanna and Canton have become "
            "Cardiff's most settled food quarter. Kings Road and Pontcanna Street hold "
            "independent brunch cafes, neighbourhood bistros and, since 2024, the city's "
            "first Michelin-starred restaurant. City Road in Roath plays a different role: "
            "an international food mile where Syrian, Korean, Lebanese and Chinese "
            "kitchens stand shoulder to shoulder, reflecting Cardiff's historic port "
            "diversity. Cardiff Bay adds waterfront dining to the mix."
        ),
        (
            "Welsh produce runs through the best kitchens: laverbread — an edible seaweed "
            "harvested from Welsh shores and pan-fried with bacon — is one of the city's "
            "signature breakfast ingredients, and Cardiff Market sells it fresh. Salt-marsh "
            "lamb from the Gower, Pembrokeshire shellfish and Welsh dairy appear across "
            "menus at every price point, and the craft-beer scene anchored by Newport "
            "brewery Tiny Rebel gives the city a distinctly Welsh drinking character."
        ),
    ],
    "visit": [
        (
            "The city centre is compact and walkable. The arcades, Cardiff Central Market "
            "and Westgate Street are within ten minutes of each other on foot, making it "
            "easy to take in the Victorian covered walkways before settling in for lunch. "
            "Pontcanna is a twenty-minute walk west of the centre along Cathedral Road, "
            "or a short taxi ride from Cardiff Central station."
        ),
        (
            "Time a visit well and the day shapes itself: a tea at Waterloo in the Wyndham "
            "Arcade, pizza at Ffwrnes in the Central Market, an evening tasting menu at "
            "Gorse, and a nightcap of Welsh craft ale at Tiny Rebel before the walk back "
            "to the station. Book Gorse weeks ahead; Tiny Rebel and Ffwrnes take walk-ins."
        ),
    ],
    "checklist": [
        "Walk the Victorian arcades from the Royal Arcade (1858) through to Wyndham, then take tea at Waterloo",
        "Head to Cardiff Central Market for Ffwrnes pizza at the first-floor stall",
        "Book Gorse in Pontcanna well in advance — it opens four services a week and fills quickly",
        "Tiny Rebel is two minutes from Cardiff Central station, a natural last stop",
        "Cardiff Central station has direct trains to Newport, Barry and Penarth for a day trip extension",
    ],
    "what_to_order": (
        "Order with intent. At Ffwrnes, the salt-marsh lamb or Welsh cheese pizza fresh from "
        "the wood oven. At Waterloo Tea, ask which single-origin is on filter that day, then "
        "settle in for a full afternoon tea if time allows. At Gorse, trust the ten-course menu "
        "and whatever micro-seasonal Welsh produce Waters is working with that week. At Tiny "
        "Rebel, a pint of Cwtch red ale — the beer that put Welsh craft brewing on the national "
        "map — and the pub food menu if you need something to eat."
    ),
    "glance": [
        ("Best for a quick bite", "Ffwrnes Pizza, for a wood-fired Welsh pizza at Cardiff Central Market"),
        ("Best for an occasion", "Gorse, for Cardiff's first Michelin-starred Welsh tasting menu in Pontcanna"),
        ("Best for atmosphere", "Waterloo Tea in the Wyndham Arcade, under Victorian iron-and-glass vaulting"),
    ],
    "faq": [
        (
            "Where can I get the best independent pizza in Cardiff?",
            "Ffwrnes Pizza at Cardiff Central Market has been serving wood-fired Neapolitan "
            "pizza with Welsh ingredients — salt-marsh lamb, local cheese — from the "
            "Victorian market's first floor since 2018, and its food hygiene rating was "
            "renewed in February 2026 confirming it is trading.",
        ),
        (
            "Which is the best cafe or tea room in Cardiff city centre?",
            "Waterloo Tea at the Wyndham Arcade is widely regarded as one of the finest "
            "in Wales. Founded in Penylan in 2008 by Kasim Ali, it was named Best Cafe "
            "in the UK by the Beverage Standards Association and the Wyndham Arcade "
            "branch offers over 60 loose-leaf teas in a beautifully preserved Victorian "
            "arcade setting.",
        ),
        (
            "Does Cardiff have any Michelin-starred restaurants?",
            "Yes. Gorse on Kings Road in Pontcanna, opened by chef Tom Waters in May 2024, "
            "became Cardiff's first Michelin-starred restaurant in February 2025 and "
            "retained its star in the 2026 guide. Waters previously trained at The Square "
            "and Heston Blumenthal's Fat Duck, and the menu is built entirely around "
            "seasonal Welsh produce.",
        ),
        (
            "What is the best pub for real ale and craft beer in Cardiff?",
            "Tiny Rebel on Westgate Street is the flagship bar of the Newport brewery "
            "whose Cwtch red ale won Supreme Champion Beer of Britain in 2015 — the "
            "first Welsh brewery to take the title. The Cardiff bar opened in 2013 in a "
            "Grade II listed Victorian building a short walk from the Principality Stadium "
            "and confirmed open as of May 2026.",
        ),
        (
            "What traditional Welsh food can I try in Cardiff?",
            "Laverbread — seaweed harvested from Welsh shores, pan-fried and traditionally "
            "served with smoked bacon — is a Cardiff breakfast staple available at Cardiff "
            "Market stalls. Welsh salt-marsh lamb, Pembrokeshire shellfish and Welsh rarebit "
            "appear across city-centre menus. Ffwrnes Pizza uses Welsh produce, and Gorse "
            "sources almost entirely from small Welsh farms and fishermen.",
        ),
        (
            "Are Cardiff's best food spots easy to reach without a car?",
            "Very. Cardiff Central Market, Waterloo Tea and Tiny Rebel are all within "
            "ten minutes on foot from Cardiff Central station. Pontcanna (for Gorse) is "
            "a twenty-minute walk or a short taxi ride. Newport, Penarth and Barry are "
            "all reachable by direct train in under thirty minutes.",
        ),
    ],
}

# leicester ----------------------------------------------------------
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

# bradford ----------------------------------------------------------
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

# coventry ----------------------------------------------------------
TOWNS["coventry"] = {
    "region": "the West Midlands",
    "population": "345K",
    "nearby": ["Nuneaton", "Rugby", "Kenilworth"],
    "meta_title": "Best Places to Eat in Coventry: Local Food Guide",
    "meta_description": (
        "Where to eat in Coventry: hand-pulled noodles at FarGo Village, "
        "speciality espresso, Korean BBQ and a 1451 pub with seven handpulls. "
        "Read the guide."
    ),
    "trust_strip": (
        "From a Shaanxi noodle bar in the city's creative quarter to a pub "
        "that has poured cask ale since 1451, Coventry has a food scene "
        "worth seeking out"
    ),
    "snapshot": (
        "For a fast answer: BiB Noodle Bar at FarGo Village for hand-pulled "
        "biang biang noodles made fresh in front of you, Warwick Row Espresso "
        "for Coventry's best independent speciality coffee, Jinseon Korean BBQ "
        "for charcoal tabletop grilling in the city centre, and The Old Windmill "
        "on Spon Street for a pint of real ale in England's oldest licensed pub "
        "building. Four moods, one compact city."
    ),
    "stats": [
        ("345K", "Population (approx)"),
        ("1451", "Year The Old Windmill was first licensed"),
        ("FarGo Village", "Coventry's creative and food quarter"),
        ("4", "Hand-picked independents"),
    ],
    "pivot_variant": "high-volume",
    "pivot_local_hook": (
        "Coventry's kitchens run the full spectrum from steel charcoal grills "
        "firing Korean bulgogi at tabletop heat to the high-volume pub kitchens "
        "and noodle bars of the city centre, all pushing a heavy load of "
        "grease-laden vapour into their canopies every service."
    ),
    "venues": [
        {
            "type": "Street Food",
            "name": "BiB Noodle Bar",
            "area": "FarGo Village, Far Gosford Street (Creative Quarter)",
            "cuisine": "Shaanxi-style hand-pulled noodles, dumplings",
            "body": (
                "Tucked inside FarGo Village, Coventry's repurposed industrial "
                "creative quarter, BiB Noodle Bar does something you rarely see "
                "outside a Chinese city: it pulls noodles by hand, right at the "
                "counter, stretching and folding the dough into wide, chewy biang "
                "biang ribbons before your eyes. The cooking is rooted in Shaanxi "
                "province in north-west China, bold with garlic, dried chilli and "
                "the numbing tingle of Sichuan pepper, and the menu adds dumplings, "
                "fermented vegetables and house-made chilli pastes. The unit is small "
                "and unfussy, with a short menu that changes with what is fresh. "
                "Open Thursday to Sunday, the bar fills quickly on weekend lunchtimes "
                "with students, food lovers and anyone who has discovered that the "
                "best bowl in Coventry is hidden down a creative-quarter corridor."
            ),
            "known_for": "Hand-pulled biang biang noodles made fresh at the counter",
            "good_for": "A quick, vivid, genuinely authentic noodle lunch",
            "source_url": "https://www.tripadvisor.com/Restaurant_Review-g186403-d20344622-Reviews-BiB_Noodle_Bar-Coventry_West_Midlands_England.html",
            "verified": "2026-06-22",
        },
        {
            "type": "Cafe",
            "name": "Warwick Row Espresso",
            "area": "25 Warwick Row, city centre",
            "cuisine": "Speciality coffee, in-house baked cakes",
            "body": (
                "A short walk from Coventry railway station, Warwick Row Espresso "
                "is the city centre's most focused independent coffee shop: a small, "
                "light-filled room run by a tight-knit team that takes single-origin "
                "espresso seriously. The beans rotate, the food is made in-house "
                "each morning, and the cakes are baked on site. Expect bacon bagels, "
                "smashed avocado, eggs benedict and freshly made toasties alongside "
                "a well-kept espresso menu that includes spiced chai, good filter "
                "and seasonal specials. The cafe is laptop-friendly, has USB charging "
                "at every seat, and opens seven days a week, giving the city centre "
                "a proper all-day independent anchor before the chains. A 4.7 Google "
                "rating from a loyal and growing regular crowd tells its own story."
            ),
            "known_for": "Single-origin espresso and in-house baked cakes near the station",
            "good_for": "A proper independent coffee stop, all day, seven days",
            "source_url": "https://www.tripadvisor.co.uk/Restaurant_Review-g186403-d23568297-Reviews-Warwick_Row_Espresso-Coventry_West_Midlands_England.html",
            "verified": "2026-06-22",
        },
        {
            "type": "Restaurant",
            "name": "Jinseon Korean BBQ",
            "area": "Unit 5 Priory Place, Fairfax Street, city centre",
            "cuisine": "Charcoal Korean barbecue",
            "body": (
                "Jinseon brought something new to the Midlands when it opened in "
                "Coventry's city centre: every table is fitted with a state-of-the-art "
                "ventilated charcoal grill, and the experience is as much about cooking "
                "as eating. Choose your cuts of locally sourced meat, seafood and "
                "vegetables, receive a steel cauldron of glowing coals, and cook to "
                "your own timing while the sides, sauces and banchan dishes arrive "
                "alongside. Guardian critic Jay Rayner visited in October 2022 and "
                "praised the restaurant for its real depth and unalloyed enthusiasm, "
                "calling it a very good time for anyone up for the joys of cooking "
                "their own food. Open daily for lunch and dinner, Jinseon takes "
                "bookings and fills tables most evenings; the beef bulgogi, galbi "
                "short ribs and the banchan spread are the orders to build a meal around."
            ),
            "known_for": "Charcoal tabletop Korean BBQ, Jay Rayner-reviewed in the Guardian",
            "good_for": "A sociable, interactive dinner with real Korean charcoal grilling",
            "source_url": "https://www.tripadvisor.com/Restaurant_Review-g186403-d12513463-Reviews-Jinseon_Korean_BBQ_Restaurant_Bar-Coventry_West_Midlands_England.html",
            "verified": "2026-06-22",
        },
        {
            "type": "Pub",
            "name": "The Old Windmill",
            "area": "22 Spon Street, medieval city centre",
            "cuisine": "Real ale, locally sourced pork pies and cheeseboard",
            "body": (
                "The building at 22 Spon Street is one of the oldest licensed premises "
                "in England, dating from 1451, and the interior has barely moved since "
                "its inter-war refurbishment: three fireplaces, worn wooden panelling, "
                "a snug, a main room and a yard that incorporates the remnants of an old "
                "brewery. The heart of the pub is its cask ale: seven handpulls offer "
                "four regular beers and three rotating guests, and two annual beer "
                "festivals pack the yard. The Old Windmill has been CAMRA Coventry Pub "
                "of the Year in 2015 and 2017, won the Great British Pub Awards in "
                "2022, and took the Stonegate Best Community Pub accolade in 2025. "
                "Food is kept to locally sourced pork pies and a cheeseboard with "
                "farmhouse cheeses from Somerset and Snowdonia. The music is live and "
                "folk; the conversation is the draw."
            ),
            "known_for": "A 1451 building, seven handpulls and multiple CAMRA awards",
            "good_for": "A pint of cask ale in one of England's oldest pubs",
            "source_url": "https://www.yelp.com/biz/the-old-windmill-coventry",
            "verified": "2026-06-22",
        },
    ],
    "food_scene": [
        (
            "Coventry's food map has three distinct layers. The medieval streetscape "
            "of Spon Street, with its timber-framed buildings dating to the thirteenth "
            "century, holds the Old Windmill and Turmeric Gold, the award-winning Indian "
            "restaurant set inside a 400-year-old building. A five-minute walk east, the "
            "repurposed industrial sheds of FarGo Village on Far Gosford Street have "
            "become the city's creative food quarter: independent noodle bars, a craft "
            "brewery tap house, vegan kitchens and street-food traders operating from "
            "permanent units and a covered outdoor terrace."
        ),
        (
            "In the city centre, the cathedral quarter and the streets around Priory "
            "Place have attracted a new generation of independent restaurants, from "
            "Jinseon's charcoal Korean grills to specialist coffee shops. Earlsdon, "
            "the residential suburb a mile south-west of the centre, adds its own "
            "independent scene: Turkish restaurants, Italian trattorias, and the "
            "intimate Earlsdon Supper Club, where chef Tobias Reutt runs a "
            "zero-waste tasting menu using produce from his own allotment."
        ),
        (
            "Coventry was the UK City of Culture in 2021, a designation that "
            "accelerated investment in the independent food sector and brought new "
            "venues to the creative quarter and cathedral precinct. The legacy is "
            "a city that punches well above its weight for a UK city of 345,000: "
            "a food scene spanning Shaanxi noodles, charcoal Korean BBQ, speciality "
            "espresso and a medieval cask-ale pub, within a ten-minute walk of one another."
        ),
    ],
    "visit": [
        (
            "The geography is compact and walkable. The Old Windmill on Spon Street "
            "sits a few minutes from the ring road, and FarGo Village is a ten-minute "
            "walk north-east along Far Gosford Street, through the creative quarter. "
            "Warwick Row Espresso is close to the station, making it an easy first "
            "stop off the train, and Jinseon Korean BBQ is a short walk further into "
            "the city centre near the Belgrade Theatre."
        ),
        (
            "Time it well and a day flows naturally: coffee at Warwick Row Espresso "
            "on arrival, a bowl of hand-pulled noodles at BiB for lunch, a wander "
            "through the medieval Spon Street quarter, an evening of charcoal grilling "
            "at Jinseon, and a final pint of cask ale at the Old Windmill before the "
            "train home. The city centre is flat and compact; Coventry station sits "
            "on the West Coast Main Line, giving fast connections to Birmingham and London."
        ),
    ],
    "checklist": [
        "Start at Warwick Row Espresso near the station for a single-origin flat white",
        "Book BiB Noodle Bar or turn up early - the FarGo noodle bar fills at lunch",
        "Book Jinseon ahead for the evening; tables for charcoal grilling go quickly",
        "Walk Spon Street to take in the medieval timber-framed buildings",
        "End the night at the Old Windmill with a pint of cask ale - no music, just conversation",
    ],
    "what_to_order": (
        "Order with intent. At BiB Noodle Bar, the biang biang noodles with chilli "
        "oil and a portion of dumplings on the side. At Warwick Row Espresso, ask "
        "which single-origin bean is on the espresso that week and add an in-house "
        "baked cake. At Jinseon, build the table around beef bulgogi and galbi short "
        "ribs, and let the banchan dishes fill the gaps. At the Old Windmill, a pint "
        "of whichever guest ale is on the third handpull, and a slice of local pork pie."
    ),
    "glance": [
        ("Best for a quick bite", "BiB Noodle Bar, for hand-pulled biang biang noodles at FarGo Village"),
        ("Best for an occasion", "Jinseon Korean BBQ, for charcoal grilling and a Guardian-reviewed night out"),
        ("Best for atmosphere", "The Old Windmill's 1451 timber rooms and seven handpulls on Spon Street"),
    ],
    "faq": [
        (
            "Where can I eat authentic hand-pulled noodles in Coventry?",
            "BiB Noodle Bar at FarGo Village, Far Gosford Street, pulls biang biang "
            "noodles by hand at the counter, serving them with Shaanxi-style chilli "
            "oil, garlic and Sichuan pepper. Open Thursday to Sunday."
        ),
        (
            "What is the best independent cafe in Coventry city centre?",
            "Warwick Row Espresso on Warwick Row, a short walk from the railway "
            "station, serves rotating single-origin espresso alongside in-house baked "
            "cakes, bagels and cooked breakfasts, seven days a week."
        ),
        (
            "Which Coventry restaurant was reviewed by Jay Rayner in the Guardian?",
            "Jinseon Korean BBQ at Priory Place was reviewed by Jay Rayner in October "
            "2022, who praised its real depth and called it a very good time. Each "
            "table has a ventilated charcoal grill for tabletop Korean barbecue."
        ),
        (
            "What is the oldest pub in Coventry?",
            "The Old Windmill at 22 Spon Street, dating from 1451, is Coventry's "
            "oldest pub and one of the oldest licensed premises in England. The "
            "Grade II-listed building has inter-war panelling, three fireplaces and "
            "seven handpulls of cask ale."
        ),
        (
            "What is FarGo Village in Coventry?",
            "FarGo Village on Far Gosford Street is Coventry's creative and food "
            "quarter, housed in repurposed industrial buildings. It is home to "
            "independent food businesses including BiB Noodle Bar, Twisted Barrel "
            "Ale Brewery and Tap House, and other independent traders."
        ),
        (
            "Is Coventry a good place to eat out independently?",
            "Yes. Coventry has a concentrated independent food scene across a "
            "walkable city centre: Spon Street's medieval buildings hold a "
            "fifteenth-century pub and an award-winning Indian restaurant, FarGo "
            "Village hosts Shaanxi noodle bars and a craft brewery, and the "
            "cathedral quarter has charcoal Korean BBQ and speciality coffee."
        ),
    ],
}

# nottingham ----------------------------------------------------------
TOWNS["nottingham"] = {
    "region": "the East Midlands",
    "population": "330K",
    "nearby": ["Beeston", "West Bridgford", "Arnold"],
    "meta_title": "Best Places to Eat in Nottingham: Local Food Guide",
    "meta_description": (
        "Four top Nottingham independents: a Bib Gourmand izakaya, "
        "award-winning deli, a Michelin-starred carriage house and "
        "a cave pub. Read the guide."
    ),
    "trust_strip": (
        "From a Bib Gourmand izakaya to a Michelin-starred Victorian carriage "
        "house, Nottingham punches well above its weight on the national food stage"
    ),
    "snapshot": (
        "For a fast answer: Kushi-ya in the city centre for Michelin Bib Gourmand "
        "Japanese izakaya skewers, Delilah Fine Foods on Victoria Street for "
        "the city's finest deli-cafe and cheese counter, Alchemilla on Derby Road "
        "for Alex Bond's one-Michelin-star tasting menus in a Victorian carriage "
        "house, and Ye Olde Trip to Jerusalem for a pint in a sandstone cave "
        "beneath Nottingham Castle. Four moods, one compact city centre."
    ),
    "stats": [
        ("330K", "Population (approx)"),
        ("1189", "The year Ye Olde Trip to Jerusalem claims to date from"),
        ("Hockley", "The city's creative eating and drinking quarter"),
        ("4", "Hand-picked independents"),
    ],
    "pivot_variant": "high-volume",
    "pivot_local_hook": (
        "Nottingham's kitchens run hard: the city centre's izakayas, "
        "Michelin-starred tasting rooms and high-volume pub kitchens fire "
        "continuously through lunch and dinner, pushing a heavy load of "
        "grease-laden vapour through their canopies at every service."
    ),
    "venues": [
        {
            "type": "Casual Dining",
            "name": "Kushi-ya",
            "area": "Enfield Chambers, city centre",
            "cuisine": "Japanese izakaya, yakitori and kushiyaki",
            "body": (
                "Opened in 2018 by chef-owner Simon Carlin on a tucked-away alleyway "
                "off Long Row, Kushi-ya built its reputation as the city's most "
                "exciting Japanese kitchen before moving to larger premises in Enfield "
                "Chambers in late 2024. It holds a Michelin Bib Gourmand in the 2026 "
                "Guide, the inspector's mark for outstanding quality at a sensible price, "
                "and was named among the UK's top 25 restaurants by Square Meal. The "
                "menu is built around the charcoal grill: whole free-range birds broken "
                "down into different cuts each day, rendered as tsukune (minced chicken "
                "skewer with egg yolk) or thigh and oyster cuts alongside set-lunch deals "
                "that critics have called absurdly good value. No bookings at lunch; "
                "arrive early or queue."
            ),
            "known_for": "Michelin Bib Gourmand Japanese yakitori and kushiyaki skewers",
            "good_for": "A high-quality, affordable Japanese lunch or a serious dinner",
            "source_url": "https://guide.michelin.com/gb/en/nottingham-region/nottingham/restaurant/kushi-ya",
            "verified": "2026-06-22",
        },
        {
            "type": "Cafe",
            "name": "Delilah Fine Foods",
            "area": "12 Victoria Street, city centre",
            "cuisine": "Deli-cafe, artisan cheeses, charcuterie, all-day cafe",
            "body": (
                "Sangita Tryner opened Delilah in a small Middle Pavement shop in 2005, "
                "and the move to a grand former bank on Victoria Street in 2011 gave the "
                "business the stage it deserved: more than 3,000 square feet of elegant "
                "plasterwork and high ceilings now houses over 150 cheeses (including "
                "Colston Bassett Stilton, made just 14 miles away), a vast charcuterie "
                "counter and a cafe that runs from fry-ups at nine to cheese fondues and "
                "lamb kofta at lunch. In 2025 Delilah won Best Delicatessen in the UK and "
                "Retailer of the Year at the Farm Shop and Deli Awards, two decades after "
                "first claiming the top accolade. No table bookings; first come, first "
                "served."
            ),
            "known_for": "Over 150 cheeses including Nottinghamshire Stilton, Farm Shop & Deli Awards winner",
            "good_for": "A leisurely all-day cafe stop with the city's best cheese counter",
            "source_url": "https://delilahfinefoods.co.uk/",
            "verified": "2026-06-22",
        },
        {
            "type": "Restaurant",
            "name": "Alchemilla",
            "area": "192 Derby Road, Park area",
            "cuisine": "Modern British fine dining, tasting menu",
            "body": (
                "Chef Alex Bond opened Alchemilla in August 2017 inside six red-brick "
                "vaulted arches of a Victorian carriage house that once served the lace "
                "merchants' district on Derby Road. The restaurant earned a Michelin star "
                "in the 2020 Guide and has retained it ever since, ranking 27th in the "
                "UK's top 100 restaurants for 2026. Bond's cooking is plant-forward and "
                "technique-led, built around fermentation, pickling and the transformative "
                "handling of British produce; a tasting menu might move from fermented "
                "vegetables to aged Nottinghamshire beef, with each plate balancing sweet, "
                "sour and salt in ways that made Alchemilla the second restaurant in "
                "Nottinghamshire ever to hold a star. Book well ahead."
            ),
            "known_for": "One Michelin star, plant-forward tasting menus in a Victorian carriage house",
            "good_for": "A landmark special-occasion dinner in one of England's best dining rooms",
            "source_url": "https://www.alchemillarestaurant.uk/",
            "verified": "2026-06-22",
        },
        {
            "type": "Pub",
            "name": "Ye Olde Trip to Jerusalem",
            "area": "Brewhouse Yard, beneath Nottingham Castle",
            "cuisine": "British pub food",
            "body": (
                "Cut into the sandstone cliff on which Nottingham Castle stands, Ye Olde "
                "Trip to Jerusalem is one of England's most astonishing pub spaces. The "
                "building's timber frame dates from the 1670s and the pub was first "
                "recorded in 1760, though the sign above the door boasts 1189 in reference "
                "to the Crusades. Today it is run by Greene King and serves classic British "
                "pub food including steak and ale pie, fish and chips and a Great British "
                "cheese toastie in the Rock Bar - open daily from 11am to 10pm. The real "
                "draw is the building itself: rooms carved into living rock, a sandstone "
                "cave cellar used for centuries to store ale, and a Grade II listed "
                "exterior that no visitor to Nottingham should miss."
            ),
            "known_for": "Cave rooms carved from Nottingham sandstone beneath the castle cliff",
            "good_for": "A pint and a pie in the most atmospheric pub room in the East Midlands",
            "source_url": "https://www.greeneking.co.uk/pubs/nottinghamshire/ye-olde-trip-to-jerusalem",
            "verified": "2026-06-22",
        },
    ],
    "food_scene": [
        (
            "Nottingham's food map is shaped by three distinct zones. The city centre "
            "proper - around Market Square, the Lace Market and Hockley - holds the "
            "bulk of the independent restaurants, from Kushi-ya's izakaya counter to "
            "the tasting-menu kitchens. Hockley, affectionately called the Soho of "
            "Nottingham, is the creative quarter where hip cafes, wine bars and "
            "ambitious Indies cluster in Victorian and Edwardian shopfronts."
        ),
        (
            "A short walk east, Sneinton Market has transformed since 2015 from a "
            "derelict fruit-market site into Nottingham's most talked-about food and "
            "craft destination, with street-food kitchens, brewery tap rooms and a "
            "Saturday vegan market among the restored wholesale buildings. The "
            "regional food story is anchored by Stilton: Nottinghamshire holds two "
            "of the six authorised Stilton dairies, including Colston Bassett, which "
            "has hand-ladled its curd since 1913."
        ),
        (
            "At the top of the table, Nottingham has an unexpectedly strong Michelin "
            "presence for a city of its size: Restaurant Sat Bains holds two stars "
            "on the edge of town, Alchemilla holds one on Derby Road, and Kushi-ya "
            "and Raymond's both carry Bib Gourmands in the 2026 Guide. Twelve "
            "Nottingham restaurants in total appear in the 2026 Michelin Guide - a "
            "depth that most cities twice the size would envy."
        ),
    ],
    "visit": [
        (
            "The geography is friendlier than it looks. Kushi-ya, Delilah and the "
            "Trip to Jerusalem are all within a ten-minute walk of each other in or "
            "just below the city centre, served by Nottingham station and the NET "
            "tram. Alchemilla is a mile west on Derby Road, a short tram ride on the "
            "Phoenix line or a flat walk through the Park estate."
        ),
        (
            "A day flows naturally: an all-day breakfast or cheese platter at Delilah, "
            "a lunchtime queue at Kushi-ya, an afternoon pint in the cave rooms at Ye "
            "Olde Trip, and Alchemilla saved for the evening you want to remember. "
            "Book Alchemilla weeks ahead. Kushi-ya takes no bookings at lunch."
        ),
    ],
    "checklist": [
        "Arrive early at Kushi-ya for a no-reservation lunch - or book well ahead for dinner",
        "Browse the 150-cheese counter at Delilah and pick up Colston Bassett Stilton",
        "Walk down to Brewhouse Yard to see the cave rooms at Ye Olde Trip",
        "Book Alchemilla at least three to four weeks in advance; tables go fast",
        "Use Nottingham station and the NET tram - the centre and Derby Road are well served",
    ],
    "what_to_order": (
        "Order with intent. At Kushi-ya, let the set lunch do the talking - tsukune "
        "skewer, yakitori thigh and a cold Sapporo - or go a la carte for the prawn "
        "katsu sando at dinner. At Delilah, a fondue for two or the lamb kofta with "
        "a glass from the all-day wine list. At Alchemilla, surrender to the tasting "
        "menu and trust Alex Bond's fermentation and pickling to surprise you. At "
        "Ye Olde Trip, a pint of cask ale and the steak and ale pie, taken slowly "
        "in a sandstone room that has been pouring beer since the eighteenth century."
    ),
    "glance": [
        ("Best for a quick bite", "Kushi-ya, for Michelin Bib Gourmand yakitori skewers at lunch"),
        ("Best for an occasion", "Alchemilla, for a one-Michelin-star tasting menu on Derby Road"),
        ("Best for atmosphere", "Ye Olde Trip to Jerusalem's cave rooms beneath the castle cliff"),
    ],
    "faq": [
        (
            "Where can I eat well in Nottingham city centre on a budget?",
            "Kushi-ya in Enfield Chambers, a Michelin Bib Gourmand izakaya, offers a "
            "set lunch that critics describe as outstanding value. No bookings at lunch - "
            "arrive early to secure a spot at the charcoal-grill counter.",
        ),
        (
            "Does Nottingham have any Michelin-starred restaurants?",
            "Yes. Alchemilla on Derby Road holds one Michelin star in the 2026 Guide, "
            "awarded to chef-patron Alex Bond for his plant-forward, fermentation-led "
            "tasting menus in a Victorian carriage house. Restaurant Sat Bains, on the "
            "outskirts of the city, holds two Michelin stars.",
        ),
        (
            "What is the best deli or cafe in Nottingham?",
            "Delilah Fine Foods at 12 Victoria Street, founded in 2005, won Best "
            "Delicatessen in the UK at the 2025 Farm Shop and Deli Awards. The former "
            "bank building houses over 150 cheeses, a charcuterie counter and an "
            "all-day cafe. No table bookings; seats are first come, first served.",
        ),
        (
            "Is Ye Olde Trip to Jerusalem really England's oldest pub?",
            "The pub claims the date 1189, though historians note the timber frame "
            "dates from the 1670s and the first documented record as a public house "
            "is from 1760. Whatever the true date, it is one of England's most "
            "extraordinary pub rooms, carved into the sandstone cliff beneath "
            "Nottingham Castle and run today by Greene King.",
        ),
        (
            "Which Nottingham neighbourhood has the best independent food scene?",
            "Hockley - known as the Soho of Nottingham - is the city's creative "
            "quarter, packed with independent cafes, wine bars and restaurants. "
            "Sneinton Market, a short walk east, has become a major street-food "
            "and craft-beer destination since its 2015 revival.",
        ),
        (
            "Is Stilton cheese made near Nottingham?",
            "Yes. Nottinghamshire holds two of the six authorised Stilton dairies, "
            "including Colston Bassett Dairy, which has been making hand-ladled Blue "
            "Stilton since 1913. Delilah Fine Foods in the city centre stocks "
            "Colston Bassett Stilton and stocks from the other regional dairies.",
        ),
    ],
}

# newcastle-upon-tyne ----------------------------------------------------------
TOWNS["newcastle upon tyne"] = {
    "region": "the North East",
    "population": "300K",
    "nearby": ["Gateshead", "South Shields", "Tynemouth"],
    "meta_title": "Best Places to Eat in Newcastle upon Tyne: Food Guide",
    "meta_description": (
        "Where to eat in Newcastle: a seasonal Ouseburn bistro, a speciality "
        "roaster, a Michelin-star table and a Bib Gourmand pub. Read the guide."
    ),
    "trust_strip": (
        "From a converted-container bistro in the Ouseburn to a Michelin-star "
        "merchant's townhouse on the Quayside, Newcastle eats seriously well"
    ),
    "snapshot": (
        "For a fast answer: Cook House on Foundry Lane for Anna Hedworth's "
        "seasonal Ouseburn cooking, Pink Lane Coffee near Central Station for "
        "Newcastle's pioneering speciality roast, House of Tides on the "
        "Quayside for Kenny Atkinson's Michelin-star modern British tasting "
        "menu, and The Broad Chare for a pint and a hearty plate in a "
        "Bib Gourmand Quayside pub. Four moods, one compact city."
    ),
    "stats": [
        ("300K", "Population (approx)"),
        ("1835", "Year Grainger Market opened"),
        ("Quayside", "Newcastle's historic dining and bar mile"),
        ("4", "Hand-picked independents"),
    ],
    "pivot_variant": "high-volume",
    "pivot_local_hook": (
        "Newcastle's pub kitchens, Quayside fine-dining rooms and Ouseburn "
        "bistros cook hard across long services, and the city's love of "
        "hearty, punchily flavoured food means canopies accumulate heavy "
        "grease loads that demand a regular extraction-cleaning schedule."
    ),
    "venues": [
        {
            "type": "Casual Dining",
            "name": "Cook House",
            "area": "Foundry Lane, Ouseburn Valley",
            "cuisine": "Modern British, seasonal",
            "body": (
                "Anna Hedworth trained as an architect and taught herself to cook, "
                "starting a supper club inside a pair of shipping containers on "
                "Ouse Street in 2014. Cook House moved to its permanent home on "
                "Foundry Lane in late 2018, a stripped-back industrial space with "
                "a terrace overlooking the Ouseburn. The menu shifts with the "
                "season and the day's produce: breakfast and brunch at weekends, "
                "a dinner centred on the hibachi barbecue Wednesday to Saturday. "
                "Hedworth's book of the same name appeared in 2019 and the "
                "restaurant is listed in the Michelin Guide. A small deli counter "
                "sells sourdough, milk and pickles to take away, and the adjacent "
                "Wren bar opened in November 2025."
            ),
            "known_for": "Seasonal hibachi cooking and a relaxed Ouseburn terrace",
            "good_for": "A weekend brunch or an unfussy weekday dinner in Newcastle's bohemian quarter",
            "source_url": "https://www.cookhouse.org/",
            "verified": "2026-06-22",
        },
        {
            "type": "Cafe",
            "name": "Pink Lane Coffee",
            "area": "Pink Lane, city centre (near Central Station)",
            "cuisine": "Speciality coffee, roasted on site",
            "body": (
                "Pink Lane Coffee opened its lane-side cafe in 2012, a few steps "
                "from Newcastle Central Station, and has been roasting its own "
                "beans on site ever since. The collective sources single-origin "
                "coffees scoring at least 80 points on the speciality grading "
                "scale, roasting to pull out natural sweetness rather than "
                "bitterness, and supplies cafes, hotels and restaurants across "
                "the UK. All Pink Lane managers hold a stake in the business, "
                "and the sourcing runs to Northumberland dairy for the milk. "
                "Espresso, filter, pour-over and a full menu of food run "
                "alongside the coffee, and updated branding launched in 2024 "
                "marked twelve years of trading on the same lane."
            ),
            "known_for": "On-site roasted single-origin coffee, a Newcastle institution since 2012",
            "good_for": "A serious pre-train or mid-city coffee stop",
            "source_url": "https://www.pinklanecoffee.co.uk/",
            "verified": "2026-06-22",
        },
        {
            "type": "Restaurant",
            "name": "House of Tides",
            "area": "28-30 The Close, Quayside",
            "cuisine": "Modern British, tasting menu",
            "body": (
                "Kenny Atkinson and his wife Abbie opened House of Tides in "
                "February 2014 in a Grade I listed 16th-century merchant's "
                "townhouse on the historic Quayside. The building's original "
                "flagstones and exposed beams frame a first-floor dining room "
                "with an open fireplace and river views. Atkinson's kitchen "
                "runs a modern British tasting menu of seasonal, sustainably "
                "sourced food, and the restaurant has held a Michelin star every "
                "year since 2014 - retaining it for a twelfth consecutive year "
                "in the 2026 Guide. It also holds four AA rosettes. Atkinson is "
                "now also chef-patron of the one-star Solstice nearby, making "
                "him the first chef to hold two separate Michelin stars within a "
                "single city. Book well ahead."
            ),
            "known_for": "Michelin star retained 2026 (12 consecutive years), 16th-century Quayside setting",
            "good_for": "A landmark tasting-menu occasion on the Newcastle Quayside",
            "source_url": "https://newcastlemagazine.com/kenny-atkinsons-newcastle-restaurants-celebrate-michelin-star-success-at-2026-ceremony/",
            "verified": "2026-06-22",
        },
        {
            "type": "Pub",
            "name": "The Broad Chare",
            "area": "25 Broad Chare, Quayside",
            "cuisine": "British pub food",
            "body": (
                "The Broad Chare opened in 2011 in a converted Victorian "
                "red-brick building beside Live Theatre on the Quayside, the "
                "result of a partnership between restaurateur Terry Laybourne's "
                "21 Hospitality group and the theatre company. It was awarded a "
                "Michelin Bib Gourmand in its opening year and has held it ever "
                "since, including in the 2026 Guide. The ground floor is a "
                "proper pubby bar with over 50 beers and snacks; upstairs the "
                "rustic dining room serves hearty, confident cooking - haggis on "
                "toast, grilled calves liver with bacon and crispy onion, game "
                "terrine with hedgerow jelly - that earns its place alongside "
                "the beer list. Bookings were showing as selling fast for late "
                "June 2026."
            ),
            "known_for": "Michelin Bib Gourmand since 2011, over 50 beers, hearty Quayside cooking",
            "good_for": "A pint and a plate with serious food credentials in a genuinely pubby setting",
            "source_url": "https://www.tripadvisor.co.uk/Restaurant_Review-g186394-d2109025-Reviews-The_Broad_Chare-Newcastle_upon_Tyne_Tyne_and_Wear_England.html",
            "verified": "2026-06-22",
        },
    ],
    "food_scene": [
        (
            "Newcastle's food map runs from the Victorian trading halls of Grainger "
            "Market - opened by John Dobson in 1835, voted Britain's favourite "
            "market in 2020 - to the Michelin-star dining rooms tucked inside "
            "16th-century merchant houses on the Quayside. The stottie cake, a "
            "dense flat bread born in the working-class bakeries of the North "
            "East, remains the city's defining street food, most powerfully in "
            "the ham and pease-pudding stottie that sustained generations of "
            "shipyard and colliery workers."
        ),
        (
            "The Quayside is the city's most atmospheric dining and bar mile, "
            "running below the Tyne Bridge with restaurants, bars and the Sunday "
            "outdoor market stretching along the river. Two Michelin-recognised "
            "venues anchor it: House of Tides in the Grade I listed townhouse "
            "and The Broad Chare gastropub in the converted Victorian warehouse. "
            "A short walk upstream, Ouseburn is Newcastle's bohemian quarter - "
            "studios, music venues and Cook House's industrial bistro on Foundry "
            "Lane, the creative heart of the independent food scene."
        ),
        (
            "Jesmond, a mile to the north, hosts the Armstrong Bridge food "
            "market on the third Saturday of each month and a cluster of "
            "independent restaurants along Jesmond Road. City centre coffee is "
            "anchored by Pink Lane Coffee, whose lane-side roastery near Central "
            "Station helped establish Newcastle's speciality scene in 2012. "
            "Grainger Market in the centre brings it all together: over a hundred "
            "traders, ten cuisines, artisan bakers and the kind of affordable "
            "fresh produce that keeps independent restaurants stocked."
        ),
    ],
    "visit": [
        (
            "The Quayside and the city centre sit within easy walking distance "
            "of Central Station and the Metro network. House of Tides, The Broad "
            "Chare and the Quayside Sunday market are a short riverside walk from "
            "one another, with Grainger Market and Pink Lane Coffee ten minutes "
            "north up the hill. Ouseburn is a pleasant twenty-minute walk or a "
            "short taxi from the centre."
        ),
        (
            "Time it right and the day composes itself: a flat white at Pink Lane "
            "off the train, a loop through Grainger Market for the stalls, lunch "
            "at The Broad Chare with one of its fifty beers, dinner at Cook House "
            "if you have booked ahead, and House of Tides kept for the evening "
            "you want to remember longest. Book House of Tides weeks in advance."
        ),
    ],
    "checklist": [
        "Start with coffee at Pink Lane, steps from Central Station",
        "Walk through Grainger Market - pick up a ham and pease pudding stottie",
        "Lunch at The Broad Chare on the Quayside for the Bib Gourmand menu and fifty beers",
        "Head up to Ouseburn for dinner at Cook House - book ahead and check their seasonal menu",
        "Reserve House of Tides weeks in advance for the tasting menu in the 16th-century townhouse",
    ],
    "what_to_order": (
        "Order with intent. At Cook House, follow whatever Hedworth is firing on "
        "the hibachi that evening - the menu changes daily but the cooking is "
        "always fiercely seasonal. At Pink Lane, ask what single origin is on the "
        "espresso and try a filter if there is time. At House of Tides, surrender "
        "to the full tasting menu and ask about the wine flight. At The Broad "
        "Chare, a pint of whatever is freshest on the bar, haggis on toast to "
        "start, and something from the grill for the main."
    ),
    "glance": [
        ("Best for a quick bite", "Cook House deli counter or a ham stottie from Grainger Market"),
        ("Best for an occasion", "House of Tides, for twelve years of Michelin-star cooking in a 16th-century Quayside townhouse"),
        ("Best for atmosphere", "The Broad Chare - Bib Gourmand pub with 50 beers and a proper pubby bar"),
    ],
    "faq": [
        (
            "Does Newcastle have a Michelin-star restaurant?",
            "Yes. House of Tides on the Quayside, opened by Kenny and Abbie Atkinson in 2014 inside "
            "a Grade I listed 16th-century merchant townhouse, has held a Michelin star every year "
            "since 2014, retaining it for a twelfth consecutive year in the 2026 Guide. Kenny Atkinson "
            "also holds a separate star for Solstice nearby."
        ),
        (
            "What is the local food to try in Newcastle?",
            "The stottie cake is the city's defining bread - a dense, flat round from the working-class "
            "bakery tradition, best eaten filled with boiled ham and pease pudding, a savoury split-pea "
            "spread that has fed the North East for generations. You can find both at Grainger Market "
            "in the city centre."
        ),
        (
            "What is the best independent coffee in Newcastle?",
            "Pink Lane Coffee, open since 2012 near Central Station, roasts single-origin beans on site "
            "and helped establish Newcastle's speciality coffee scene. The collective is worker-owned and "
            "sources its milk from a Northumberland dairy farm."
        ),
        (
            "Where is the best pub for food in Newcastle?",
            "The Broad Chare on the Quayside, a Michelin Bib Gourmand since it opened in 2011, splits "
            "its operation between a ground-floor bar with over 50 beers and an upstairs dining room "
            "serving hearty, well-judged dishes from haggis on toast to grilled calves liver."
        ),
        (
            "What is Ouseburn and why is it good for food?",
            "Ouseburn is Newcastle's bohemian creative quarter, a short walk east of the Quayside along "
            "the Tyne. It is home to studios, music venues and Cook House on Foundry Lane, Anna "
            "Hedworth's Michelin-listed bistro that started as a supper club in a shipping container "
            "in 2014 and now runs a terrace, deli counter and the adjacent Wren bar."
        ),
        (
            "Is Newcastle a good city for independent restaurants?",
            "Yes. The city has two Michelin-star restaurants, a cluster of Bib Gourmand and Michelin "
            "Guide-listed independents, a 190-year-old covered market, and a growing creative food "
            "scene in Ouseburn, making it one of the strongest eating cities in the north of England."
        ),
    ],
}

# sunderland ----------------------------------------------------------
TOWNS["sunderland"] = {
    "region": "Tyne and Wear",
    "population": "275K",
    "nearby": ["South Shields", "Washington", "Seaham"],
    "meta_title": "Best Places to Eat in Sunderland: Local Food Guide",
    "meta_description": (
        "Four Sunderland independents: a seafront chippy, a Sunniside arts cafe, "
        "a Good Food Guide restaurant, and an Edwardian gin palace. Read the guide."
    ),
    "trust_strip": (
        "From a 1950s seafront chippy to a Good Food Guide dining room, "
        "Sunderland's independent food scene punches well above its weight"
    ),
    "snapshot": (
        "For a fast answer: Minchella's on Dykelands Road in Seaburn for "
        "fresh-fried cod and homemade Italian ice cream beside the North Sea, "
        "Sonny's at Pop Recs on High Street West for the city's best "
        "independent coffee and seasonal kitchen in the Sunniside arts quarter, "
        "Ember at Sheepfolds Stables for chef Tamir Hassan's monthly-changing "
        "tasting menu in the Good Food Guide 2025, and the Dun Cow on High "
        "Street West for cask ale under one of the finest Edwardian gin-palace "
        "interiors in the North East. Four moods, one Wearside city."
    ),
    "stats": [
        ("275K", "Population (approx)"),
        ("1901", "Year the Dun Cow was rebuilt in Edwardian baroque"),
        ("1950s", "Decade Minchella's opened on the Seaburn seafront"),
        ("4", "Hand-picked independents"),
    ],
    "pivot_variant": "coastal",
    "pivot_local_hook": (
        "Sunderland's seafront fryers run flat-out through the summer season, "
        "while the city-centre kitchens behind the cultural quarter carry a "
        "year-round grease load from breakfast service through late-night covers "
        "- a combination that makes regular extraction cleaning a coastal "
        "operator's most pressing compliance task."
    ),
    "venues": [
        {
            "type": "Fish and Chips",
            "name": "Minchella's Fish and Chips",
            "area": "Dykelands Road, Seaburn seafront",
            "cuisine": "Fish and chips, homemade Italian ice cream",
            "body": (
                "The Minchella family came to the North East from Italy in the early "
                "twentieth century, and the Seaburn shop on Dykelands Road has stood "
                "opposite the promenade since the 1950s. Run today by Paolo Minchella, "
                "whose parents Trevor and Sandra took over from his uncle, it is a "
                "family-run coastal chippy in the best tradition: fresh cod fried to "
                "order in a crisp batter, thick-cut chips, and a seat at an outside "
                "table with the North Sea in front of you. The homemade ice cream, "
                "churned on site in the Italian fashion and served in everything from "
                "a tub to a classic cone, is as good a reason to visit as the fish. "
                "Open every day through the summer season, it is the Seaburn institution "
                "locals have queued at for three generations."
            ),
            "known_for": "Fresh-fried cod and handmade Italian-style ice cream since the 1950s",
            "good_for": "A classic coastal fish supper with a scoop to follow",
            "source_url": "https://www.tripadvisor.co.uk/Restaurant_Review-g227059-d5961336-Reviews-Minchella_s_Fish_and_Chips-Sunderland_Tyne_and_Wear_England.html",
            "verified": "2026-06-22",
        },
        {
            "type": "Cafe",
            "name": "Sonny's at Pop Recs",
            "area": "172-175 High Street West, Sunniside quarter",
            "cuisine": "Speciality coffee, seasonal kitchen",
            "body": (
                "Pop Recs began in 2013 as a pop-up record shop run by members of "
                "indie-pop band Frankie & The Heartstrings, and grew into one of "
                "Sunderland's most-loved community arts spaces - a music venue, "
                "gallery, cinema room and cafe all folded into a terrace of "
                "restored Georgian merchant houses on High Street West. The cafe "
                "side trades as Sonny's, named in tribute to a founder's family, "
                "and is open Monday to Saturday from 9am to 3pm. The coffee is "
                "among the best in the city, and the kitchen turns out a short "
                "seasonal menu of dishes like Turkish eggs, curried parsnip soup "
                "and freshly baked focaccia. On Fridays and Saturdays, whole "
                "focaccia loaves are baked to order. Dog-friendly, fully accessible, "
                "and loud with conversation."
            ),
            "known_for": "Speciality coffee and a seasonal kitchen inside Sunderland's leading arts venue",
            "good_for": "A morning coffee or brunch in the heart of the Sunniside cultural quarter",
            "source_url": "https://poprecs.co.uk/",
            "verified": "2026-06-22",
        },
        {
            "type": "Restaurant",
            "name": "Ember",
            "area": "Sheepfolds Stables, Easington Street, Monkwearmouth",
            "cuisine": "Modern British, monthly-changing tasting menu",
            "body": (
                "Ember opened in August 2024 inside the restored Sheepfolds Stables, "
                "a Victorian stable complex on the north bank of the Wear that was "
                "revived with a four-million-pound investment. Head chef and Gordon "
                "Ramsay protege Tamir Hassan runs a monthly-changing menu that has "
                "already moved through Tokyo, Paris, Istanbul and Mexico, finding "
                "the city's cooking a different lens each time. Within a year of "
                "opening, Ember earned a place in The Good Food Guide 2025 and is "
                "rated 4.8 on OpenTable from over 460 diners. The contemporary "
                "dining room sits around an open kitchen, the Sunday lunch sells "
                "out weeks ahead, and the restaurant has been described as "
                "Sunderland's most ambitious table. Book well in advance."
            ),
            "known_for": "Monthly-changing modern menu, The Good Food Guide 2025",
            "good_for": "A special-occasion dinner in the city's most talked-about new dining room",
            "source_url": "https://www.tripadvisor.co.uk/Restaurant_Review-g227059-d28668419-Reviews-Ember-Sunderland_Tyne_and_Wear_England.html",
            "verified": "2026-06-22",
        },
        {
            "type": "Pub",
            "name": "The Dun Cow",
            "area": "9 High Street West, city centre",
            "cuisine": "Cask ale and small plates",
            "body": (
                "Step inside and the interior does the talking. Built in 1901-02 "
                "in Edwardian baroque for Edinburgh brewer Robert Deuchars, the Dun "
                "Cow is a Grade II-listed gin palace with two Dutch gables, a "
                "copper-domed corner tower housing two clocks, and a bar-back that "
                "CAMRA has described as one of the most stunning in Britain. The "
                "three-section back bar is carved with delicate Art Nouveau "
                "woodwork and plaster reliefs; the building sits on CAMRA's National "
                "Inventory of Historic Pub Interiors. Restored in partnership with "
                "Camerons Brewery in 2014 and a national winner of the CAMRA and "
                "Historic England Pub Design Awards 2015, it pours a rotating "
                "selection of cask ales and craft beers, leaning on north-east "
                "microbreweries, alongside a small plates and sharing platters menu."
            ),
            "known_for": "A Grade II-listed 1901 Edwardian interior on CAMRA's National Inventory",
            "good_for": "A pint under a remarkable carved bar-back, or pre-theatre drinks before the Empire",
            "source_url": "https://camra.org.uk/pubs/dun-cow-sunderland-192670",
            "verified": "2026-06-22",
        },
    ],
    "food_scene": [
        (
            "Sunderland's food map stretches from the North Sea seafront to the "
            "revitalised city centre a mile inland. At the coast, the Seaburn and "
            "Roker promenades carry the seaside-chippy tradition the city has run "
            "for generations, with Minchella's the most enduring name. Fish and "
            "chips eaten on the sea wall with a scoop of Italian ice cream is as "
            "Wearside as the stottie or the pink slice."
        ),
        (
            "In the city centre, the Sunniside quarter on High Street West has "
            "become the focus of Sunderland's independent culture and food scene, "
            "with Pop Recs leading the way. Nearby, the restored Sheepfolds Stables "
            "on the north bank of the Wear - once derelict Victorian stable blocks - "
            "now host Ember alongside a courtyard of independent bars and food "
            "businesses and a monthly Sunday market. The city also holds a rich pub "
            "heritage: the Dun Cow on High Street West is among the finest preserved "
            "Edwardian interiors in the country."
        ),
        (
            "Beyond these anchors, Sunderland Restaurant Week (running since 2019) "
            "has drawn Michelin-starred guest chefs and put the city's independent "
            "operators on a wider map. The Ashbrooke neighbourhood south of the "
            "centre is home to several neighbourhood cafes and dining rooms, and "
            "the Roker Hotel seafront development has added hotel dining to the "
            "coastal strip. A city that once defined itself by shipbuilding and "
            "glass is quietly building a food identity to match its waterfront."
        ),
    ],
    "visit": [
        (
            "The city centre venues sit close together. The Dun Cow and Pop Recs "
            "are both on High Street West in the Sunniside quarter, a few minutes "
            "apart on foot. Sheepfolds Stables is a fifteen-minute walk or a short "
            "bus ride north across the River Wear into Monkwearmouth. Seaburn and "
            "Minchella's are three miles north of the centre, easily reached by "
            "the Metro tram to Seaburn station."
        ),
        (
            "Done as a day: a morning coffee at Sonny's in Pop Recs, a walk up to "
            "the Dun Cow at opening time to see the carved bar-back, an afternoon "
            "at Sheepfolds to book ahead at Ember for that evening, then the Metro "
            "north to Seaburn for fish and chips and ice cream on the seafront "
            "before the return. The Metro runs from the city centre to Seaburn "
            "in under fifteen minutes."
        ),
    ],
    "checklist": [
        "Book Ember well in advance - the Sunday lunch and weekend evenings sell out weeks ahead",
        "Visit the Dun Cow at opening time to take in the bar-back without the crowd",
        "Catch Sonny's at Pop Recs on a Friday or Saturday for fresh-baked whole focaccia loaves",
        "Take the Metro to Seaburn station for Minchella's - it is a two-minute walk from the platform",
        "Check the Sheepfolds Sunday Market (second Sunday of the month) for local artisan producers",
    ],
    "what_to_order": (
        "Order with intent. At Minchella's, fresh cod in crisp batter with thick-cut chips and a "
        "tub of the house Italian ice cream, eaten at a table on the promenade. At Sonny's, ask "
        "what single origin is on the espresso and order the Turkish eggs or the soup with focaccia. "
        "At Ember, follow the tasting menu wherever the month's theme leads - the chef changes it "
        "every four weeks. At the Dun Cow, a pint of the rotating north-east cask ale, ordered "
        "slowly so you have time to look at the woodcarving."
    ),
    "glance": [
        ("Best for a quick bite", "Minchella's, for a fresh-fried fish supper on the Seaburn seafront"),
        ("Best for an occasion", "Ember, for chef Tamir Hassan's monthly-changing menu at Sheepfolds"),
        ("Best for atmosphere", "The Dun Cow's 1901 Edwardian gin-palace interior on CAMRA's National Inventory"),
    ],
    "faq": [
        (
            "Where can I get the best fish and chips in Sunderland?",
            "Minchella's on Dykelands Road in Seaburn is the city's most celebrated "
            "coastal chippy, open since the 1950s and run by the same Italian family. "
            "Fresh cod fried to order, thick-cut chips and handmade ice cream on the "
            "promenade is the Wearside seafront experience."
        ),
        (
            "Does Sunderland have any Good Food Guide restaurants?",
            "Yes. Ember at Sheepfolds Stables on Easington Street earned a place in "
            "The Good Food Guide 2025 within a year of opening in August 2024. "
            "Chef Tamir Hassan changes the menu monthly and the dining room is "
            "consistently rated 4.8 on OpenTable."
        ),
        (
            "Which Sunderland pub has the best interior?",
            "The Dun Cow at 9 High Street West, a Grade II-listed Edwardian gin "
            "palace built in 1901, features one of the most ornate carved bar-backs "
            "in Britain and sits on CAMRA's National Inventory of Historic Pub "
            "Interiors. It was the national winner of the CAMRA and Historic England "
            "Pub Design Awards in 2015."
        ),
        (
            "What is the best independent cafe in Sunderland city centre?",
            "Sonny's at Pop Recs, 172-175 High Street West in the Sunniside "
            "quarter, is consistently recommended as the city's best independent "
            "coffee and brunch spot. It is open Monday to Saturday 9am to 3pm, "
            "dog-friendly, and part of the wider Pop Recs community arts venue."
        ),
        (
            "What are Sunderland's traditional local foods?",
            "The stottie - a flat, dense round loaf - is the region's most-loved "
            "bread. Panackelty is a hearty miners' casserole of layered meat, "
            "potato and onion, once cooked on Mondays from Sunday leftovers. "
            "The pink slice - shortbread with jam and thick pink icing - is "
            "Sunderland's most distinctly local sweet treat."
        ),
        (
            "Can you do a Sunderland food day on foot and public transport?",
            "Yes. Pop Recs and the Dun Cow are both on High Street West and "
            "walkable from the city centre. Sheepfolds Stables is a fifteen-minute "
            "walk north across the Wear. The Metro to Seaburn runs in under fifteen "
            "minutes and Minchella's is two minutes from the station."
        ),
    ],
}

# brighton ----------------------------------------------------------
TOWNS["brighton"] = {
    "region": "East Sussex",
    "population": "275K",
    "nearby": ["Hove", "Worthing", "Shoreham-by-Sea"],
    "meta_title": "Best Places to Eat in Brighton: Local Food Guide",
    "meta_description": (
        "Where to eat in Brighton: a 1926 chippy, an on-site coffee "
        "roastery, a BRAVO-winning vegetarian kitchen and a "
        "Good Beer Guide real ale pub. Read the guide."
    ),
    "trust_strip": (
        "From a 1926 seafront chippy to a BRAVO-winning vegetarian kitchen, "
        "Brighton has one of the most distinctive independent food scenes on the south coast"
    ),
    "snapshot": (
        "For a fast answer: Bardsley's on Baker Street for a century-old "
        "fish supper, Trading Post Coffee Roasters in the Lanes for a "
        "single-origin flat white roasted on site, terre a terre on East "
        "Street for a landmark vegetarian dinner, and The Evening Star on "
        "Surrey Street for a pint in Brighton's finest real ale free house. "
        "Four moods, one compact seafront city."
    ),
    "stats": [
        ("275K", "Population (approx)"),
        ("1926", "Year Bardsley's first fried fish on Baker Street"),
        ("30+", "Years terre a terre has led the UK vegetarian scene"),
        ("4", "Hand-picked independents"),
    ],
    "pivot_variant": "coastal",
    "pivot_local_hook": (
        "A coastal town running flat-out through summer means seafront fryers, "
        "beachside burger units and busy restaurant kitchens all pushing a heavy "
        "load of grease-laden vapour into their canopies from Easter through "
        "September, accumulating faster than a monthly clean cycle can clear."
    ),
    "venues": [
        {
            "type": "Takeaway",
            "name": "Bardsley's of Baker Street",
            "area": "22-23a Baker Street, near the seafront",
            "cuisine": "Fish and chips",
            "body": (
                "Ben Bardsley, a blacksmith from Lancashire, arrived in Brighton "
                "during the Depression and opened his fish and chip shop on Baker "
                "Street in 1926. A century later, the same family is still frying "
                "in the same spot, now in its fourth generation, and Bardsley's is "
                "firmly established as one of the great British chippies. The formula "
                "has not changed: fresh cod and haddock in a crisp, grease-free batter, "
                "hand-cut chips, mushy peas and a dash of malt vinegar. It runs as a "
                "sit-down restaurant and takeaway counter, open Tuesday to Saturday, "
                "fully licensed, and just a short walk from the seafront. Come for the "
                "fish, stay for the family room and the hundred years of practice behind "
                "every portion."
            ),
            "known_for": "Classic fish and chips served by the same family since 1926",
            "good_for": "A proper seafront fish supper rooted in Brighton history",
            "source_url": "https://bardsleys-fishandchips.co.uk/",
            "verified": "2026-06-22",
        },
        {
            "type": "Cafe",
            "name": "Trading Post Coffee Roasters",
            "area": "36 Ship Street, The Lanes",
            "cuisine": "Speciality coffee, all-day brunch",
            "body": (
                "Trading Post opened its Ship Street roastery-cafe in January 2017, "
                "becoming one of the first on-site roasters in Brighton and a "
                "cornerstone of the city's speciality coffee scene. The original "
                "Pertoncini roaster sits in plain sight behind the counter, turning "
                "batches of high-altitude Arabica while the bar pours its house Black "
                "Pearl blend as espresso, flat white and filter. The menu runs to a "
                "thoroughly modern all-day brunch: avocado on sourdough, vegan rarebit, "
                "full English and stacks of pancakes with bacon and maple syrup, all "
                "using locally sourced ingredients where possible. Two floors of seating "
                "and outdoor tables in the narrow Lanes alley make it as good for "
                "a lingering weekend brunch as a quick shot on the way to the beach."
            ),
            "known_for": "On-site roasted speciality coffee in the heart of The Lanes since 2017",
            "good_for": "A serious coffee or a leisurely brunch between the Lanes and the seafront",
            "source_url": "https://www.tradingpostcoffee.co.uk/pages/trading-post-coffee-roasters-brighton-ship-street",
            "verified": "2026-06-22",
        },
        {
            "type": "Restaurant",
            "name": "terre a terre",
            "area": "71 East Street, The Lanes",
            "cuisine": "Pioneering vegetarian and vegan",
            "body": (
                "Classically trained chefs Amanda Powley and Philip Taylor opened "
                "terre a terre in Brighton in 1993 with a simple aim: to prove that "
                "vegetarian food could be as technically demanding and flavour-driven "
                "as any meat kitchen. More than thirty years on, the East Street "
                "restaurant is one of the most celebrated vegetarian destinations in "
                "the country. The menu changes constantly, built around seasonal "
                "British produce with global technique: Korean fried cauliflower, "
                "kombu dashi risotto with shiitake tempura, walnut and tamarind pastry "
                "parcels. The restaurant completed a full interior refurbishment in "
                "early 2025 and emerged with a fresher dining room of green tones and "
                "wood panelling. It was voted Brighton's Best Restaurant at the BRAVO "
                "Awards in both 2024 and 2026. Book ahead."
            ),
            "known_for": "Over 30 years pioneering serious vegetarian cooking, BRAVO Best Restaurant 2026",
            "good_for": "A landmark vegetarian dinner in one of the UK's finest independent restaurants",
            "source_url": "https://terreaterre.co.uk/",
            "verified": "2026-06-22",
        },
        {
            "type": "Pub",
            "name": "The Evening Star",
            "area": "55-56 Surrey Street, city centre",
            "cuisine": "Real ale, cider",
            "body": (
                "The Evening Star has occupied its corner of Surrey Street, a brisk "
                "two-minute walk from Brighton station, since 1854, built originally "
                "for railway workers. In 1994 the pub launched what became the Dark "
                "Star Brewing Company from a microbrewery in the cellar, making it "
                "the birthplace of one of Sussex's best-loved independent breweries. "
                "Dark Star long since outgrew the cellar and moved to Partridge Green, "
                "but the Evening Star remains the free house that defined the city's "
                "real ale scene. It keeps seven hand pumps of cask-conditioned beer, "
                "rotating through the best independents including Burning Sky Aurora "
                "and Plateau, plus three naturally still ciders and twelve keg taps "
                "of craft beer from the UK, Czech Republic and Bavaria. It is a Good "
                "Beer Guide regular of 33-plus years and was voted Brighton and South "
                "Downs CAMRA Pub of the Year. No food beyond crisps, but the beer "
                "list is the point."
            ),
            "known_for": "The pub that launched Dark Star brewery; a 33-year Good Beer Guide regular",
            "good_for": "The finest real ale pint in Brighton, two minutes from the station",
            "source_url": "https://www.eveningstarpub.co.uk/",
            "verified": "2026-06-22",
        },
    ],
    "food_scene": [
        (
            "Brighton's food map divides between two distinct quarters and a seafront "
            "that joins them. The Lanes, the medieval warren of narrow alleys that "
            "predates the rest of the city, holds many of the most serious independent "
            "restaurants and cafes, from terre a terre's vegetarian kitchen to Trading "
            "Post's roastery-cafe. North Laine, the Victorian grid of streets to the "
            "north, is the city's independent shopping and eating heartland, where "
            "owner-run restaurants and cafes pack every block."
        ),
        (
            "Kemptown, stretching east from the city centre along St James's Street "
            "and down to Brighton Marina, is the neighbourhood for local cooking: "
            "small restaurants where the chef and owner are often the same person, "
            "serving whatever they know best. The seafront itself runs from the "
            "regenerated Shelter Hall food market near the Palace Pier to the fish "
            "and chip tradition that has defined Brighton's eating since the Victorian "
            "holiday trade, with Bardsley's on Baker Street the family name that has "
            "outlasted them all."
        ),
        (
            "Brighton has a strong vegetarian and vegan tradition unusual for its size, "
            "led historically by terre a terre and now joined by a second wave of "
            "plant-based independents. It also has a deeply-rooted real ale culture, "
            "and the craft beer scene centred on the Evening Star and the pubs around "
            "it is among the best on the south coast. The city's food is an honest "
            "reflection of its character: independent, argumentative and better than "
            "it needs to be."
        ),
    ],
    "visit": [
        (
            "The Lanes and city centre are compact and walkable. Trading Post on Ship "
            "Street, terre a terre on East Street and the Evening Star on Surrey Street "
            "sit within ten minutes on foot, with Brighton station close by for the "
            "pub. Bardsley's is a short walk south towards the seafront on Baker Street. "
            "Brighton is served directly from London Victoria and London Bridge in "
            "under an hour, making a full food day straightforward without a car."
        ),
        (
            "The day works well in layers: a morning coffee and brunch at Trading Post "
            "in the Lanes, a wander to Bardsley's for a fish lunch by the seafront, "
            "terre a terre reserved for the evening with a booking made well ahead, "
            "and The Evening Star for a nightcap pour of whatever Burning Sky has on "
            "the hand pump. Book terre a terre in advance and arrive at Bardsley's "
            "before the lunchtime queue builds."
        ),
    ],
    "checklist": [
        "Book terre a terre well ahead - tables fill quickly, especially at weekends",
        "Arrive at Bardsley's before 1pm on a Saturday to beat the queue",
        "Ask the Evening Star bar staff which cask beer is at its best that session",
        "Trading Post opens at 7:30am daily - good for an early coffee before the Lanes get busy",
        "Brighton station is a short walk from Surrey Street - the Evening Star works as a first or last stop",
    ],
    "what_to_order": (
        "Order with intent. At Bardsley's, cod or haddock in batter with hand-cut chips, "
        "mushy peas and malt vinegar - the formula that has not changed since 1926. At "
        "Trading Post, a flat white made from the house-roasted Black Pearl blend, or ask "
        "what single origin is on filter that week. At terre a terre, surrender to the "
        "changing seasonal menu and let the kitchen decide - whatever involves kombu, "
        "tamarind or shiitake tempura is usually the order to make. At the Evening Star, "
        "a pint of Burning Sky Aurora or Plateau, slowly, at the bar."
    ),
    "glance": [
        ("Best for a quick bite", "Bardsley's, for a century-old fish supper near the seafront"),
        ("Best for an occasion", "terre a terre, for 30 years of pioneering vegetarian cooking"),
        ("Best for atmosphere", "The Evening Star, birthplace of Dark Star brewery, Good Beer Guide regular"),
    ],
    "faq": [
        (
            "Where can I get the best fish and chips in Brighton?",
            "Bardsley's of Baker Street, trading since 1926 and now in its fourth generation, "
            "is the standard-bearer for Brighton fish and chips. Fresh cod and haddock in "
            "crisp batter, hand-cut chips, mushy peas and malt vinegar, a short walk from "
            "the seafront. Open Tuesday to Saturday as restaurant and takeaway."
        ),
        (
            "Is there a good vegetarian restaurant in Brighton?",
            "terre a terre on East Street in the Lanes has been Brighton's landmark "
            "vegetarian and vegan restaurant since 1993. Classically trained founders "
            "Amanda Powley and Philip Taylor built it into one of the best in the country, "
            "and it was voted Brighton's Best Restaurant at the BRAVO Awards in 2024 and "
            "2026. Book ahead."
        ),
        (
            "Where is the best independent coffee in Brighton?",
            "Trading Post Coffee Roasters on Ship Street in the Lanes, open since January "
            "2017, roasts its beans on-site in a classic Pertoncini roaster visible from "
            "the counter. It serves the house Black Pearl blend as espresso and filter, "
            "with a full all-day brunch menu alongside."
        ),
        (
            "Which Brighton pub is best for real ale?",
            "The Evening Star on Surrey Street, two minutes from Brighton station, is a "
            "33-plus-year Good Beer Guide regular and the pub where the Dark Star Brewing "
            "Company was born in 1994. It keeps seven hand pumps of rotating cask ales, "
            "including regular pours from Burning Sky, plus cider and twelve keg craft taps."
        ),
        (
            "What is Brighton's food scene known for?",
            "Brighton has an unusually strong vegetarian and vegan tradition for its size, "
            "a deep seafood and fish and chip culture rooted in the Victorian holiday trade, "
            "and a real ale and craft beer scene centred around independent free houses like "
            "the Evening Star. The Lanes, North Laine and Kemptown are the main eating districts."
        ),
        (
            "Can you do a Brighton food day on foot and public transport?",
            "Easily. The Lanes venues are walkable from Brighton station, and the station "
            "itself is served directly from London Victoria and London Bridge in under an "
            "hour. Bardsley's, Trading Post, terre a terre and the Evening Star all sit "
            "within a ten-minute walk of each other in the city centre."
        ),
    ],
}

# plymouth ----------------------------------------------------------
TOWNS["plymouth"] = {
    "region": "Devon",
    "population": "265K",
    "nearby": ["Torquay", "Newton Abbot", "Saltash"],
    "meta_title": "Best Places to Eat in Plymouth: Local Food Guide",
    "meta_description": (
        "Plymouth food guide: award-winning Barbican fish and chips, a "
        "16th-century coffee house, a Michelin-listed brasserie and a "
        "Beryl Cook pub. Read the guide."
    ),
    "trust_strip": (
        "From a cobbled Barbican chippy to the two-AA-rosette brasserie inside "
        "the Plymouth Gin Distillery, Plymouth eats far better than its size suggests"
    ),
    "snapshot": (
        "For a fast answer: Harbourside Fish and Chips on Southside Street for "
        "award-winning battered fish straight off the Barbican quay, The Mad "
        "Merchant Coffee House for speciality coffee inside a 16th-century "
        "merchant's house on New Street, Barbican Kitchen for the Tanner "
        "brothers' two-AA-rosette brasserie inside the Plymouth Gin Distillery, "
        "and the Dolphin Hotel for Bass poured straight from the cask in a "
        "Beryl Cook painting come to life. Four moods, one historic waterfront."
    ),
    "stats": [
        ("265K", "Plymouth population (approx)"),
        ("1620", "Year the Mayflower sailed from the Barbican"),
        ("1970s", "Decade Harbourside Fish and Chips first opened"),
        ("4", "Hand-picked independents"),
    ],
    "pivot_variant": "coastal",
    "pivot_local_hook": (
        "Plymouth's kitchens run hardest on the day-boat catch: frying cod and "
        "hake in deep fat through a full summer service at the Barbican's "
        "fish shops, or searing scallops and monkfish in a busy Sutton Harbour "
        "kitchen, drives some of the heaviest grease loads in South West England."
    ),
    "venues": [
        {
            "type": "Takeaway",
            "name": "Harbourside Fish and Chips",
            "area": "35 Southside Street, Barbican",
            "cuisine": "Traditional fish and chips",
            "body": (
                "The Barbican's landmark chippy has been feeding Plymouth since "
                "the 1970s and the accolades back it up: 3rd Best Fish and Chip "
                "Shop in the UK at the 2018 National Fish and Chip Awards, South "
                "West Regional Winner in 2015, and a 5-star hygiene rating. "
                "The location is hard to beat — 35 Southside Street, a few steps "
                "from the Mayflower Steps where the Pilgrim Fathers sailed in "
                "1620. The fish is locally landed and battered to order; the "
                "portions are generous and the queue on a summer evening is half "
                "the fun. A sister Gluten Free shop operates next door at number "
                "36, with a fully dedicated fryer and its own menu."
            ),
            "known_for": "Award-winning fish and chips on the historic Barbican quay",
            "good_for": "A proper Devon seafood supper eaten on the harbourside",
            "source_url": "https://harboursidefishandchips.co.uk/",
            "verified": "2026-06-22",
        },
        {
            "type": "Cafe",
            "name": "The Mad Merchant Coffee House",
            "area": "37 New Street, Barbican",
            "cuisine": "Speciality coffee, fresh light lunches",
            "body": (
                "New Street is Plymouth's oldest cobbled lane and the building "
                "at number 37 dates to the 16th century, one of the few "
                "Elizabethan merchant's houses in the Barbican to survive largely "
                "intact. The Mad Merchant Coffee House makes the most of the "
                "space: a ground-floor coffee bar, a cosy first-floor lounge "
                "and a walled Mediterranean garden that opens in summer. The "
                "coffee is taken seriously — a rotating menu of speciality beans "
                "brewed as espresso and filter — alongside freshly cooked "
                "breakfasts and lunch dishes made with local and specialist "
                "ingredients. Open Wednesday to Sunday, making it a destination "
                "rather than a habit; the building alone is worth the detour."
            ),
            "known_for": "Speciality coffee in a 16th-century Elizabethan merchant's house",
            "good_for": "A slow coffee break in Plymouth's oldest lane",
            "source_url": "https://www.visitplymouth.co.uk/food-and-drink/the-mad-merchant-coffee-house-p2360503",
            "verified": "2026-06-22",
        },
        {
            "type": "Restaurant",
            "name": "Barbican Kitchen",
            "area": "60 Southside Street, Plymouth Gin Distillery, Barbican",
            "cuisine": "Modern British brasserie",
            "body": (
                "Chris and James Tanner opened Barbican Kitchen in 2006 inside "
                "the Plymouth Gin Distillery — one of the oldest working gin "
                "distilleries in the world, producing Plymouth Gin since 1793 — "
                "and the combination of setting and cooking has since earned two "
                "AA Rosettes (upgraded September 2025) and a place in the "
                "Michelin Guide. The menu is grounded in the West Country larder: "
                "day-boat fish from Plymouth market, locally reared meats and "
                "Devon vegetables turned into confident brasserie dishes at a "
                "realistic price. At least one Tanner brother is in the kitchen "
                "most services. Book ahead at weekends; the gin distillery "
                "setting draws visitors year-round."
            ),
            "known_for": "Two-AA-rosette brasserie inside a working gin distillery since 1793",
            "good_for": "A proper restaurant occasion on the Barbican, Michelin-listed",
            "source_url": "https://barbicankitchen.com/",
            "verified": "2026-06-22",
        },
        {
            "type": "Pub",
            "name": "The Dolphin Hotel",
            "area": "14 The Barbican, Plymouth",
            "cuisine": "Real ale pub",
            "body": (
                "The Dolphin is Plymouth's most singular pub: a Grade II-listed "
                "early-19th-century building on The Barbican whose walls are hung "
                "with original paintings by the late Beryl Cook, who was a "
                "regular here and immortalised its characters on canvas. Up to "
                "eight beers are poured by gravity straight from the cask, and "
                "Bass — rare on draught anywhere in England — has been a fixture "
                "for years. Plymouth CAMRA has named it City Pub of the Year in "
                "2020 and 2022 and runner-up across nearly every other year in "
                "the last decade. The Tolpuddle Martyrs stopped here on their "
                "return from exile in 1838. Unpretentious, unhurried and "
                "genuinely historic, it is irreplaceable."
            ),
            "known_for": "Beryl Cook originals, Bass from the cask, Plymouth CAMRA Pub of the Year",
            "good_for": "An unhurried pint in Plymouth's most characterful room",
            "source_url": "https://camra.org.uk/pubs/dolphin-hotel-plymouth-154304",
            "verified": "2026-06-22",
        },
    ],
    "food_scene": [
        (
            "Plymouth's eating life is anchored to water. The Barbican and Sutton "
            "Harbour form the historic core — a quarter of Elizabethan warehouses, "
            "cobbled lanes and former merchant's houses ranged around a working "
            "harbour that still lands day-boat catch from the Channel. The fish "
            "market on Sutton Harbour supplies restaurants across the South West; "
            "the catch that does not go to the lorries tends to end up in the "
            "Barbican's kitchens and fryers by lunchtime."
        ),
        (
            "A mile west along the waterfront, Royal William Yard tells a "
            "different story. The Grade I-listed complex of granite victualling "
            "storehouses was built for the Royal Navy by Sir John Rennie between "
            "1826 and 1835 — it once brewed beer, baked bread and slaughtered "
            "meat to provision the fleet. Since its 1990s transfer to civilian "
            "life and subsequent renovation, it has become Plymouth's most "
            "atmospheric dining destination, with restaurants and bars occupying "
            "the vast stone buildings beside a private marina."
        ),
        (
            "Above both sits Plymouth Hoe, the flat limestone promontory with "
            "sweeping views across Plymouth Sound where Drake famously finished "
            "his game of bowls. The wider city centre and Mutley Plain add a "
            "strong independent coffee and bar scene to the mix, but for first-"
            "time visitors the Barbican to Royal William Yard waterfront walk "
            "captures most of what makes Plymouth distinctive — fishing-port "
            "grit, Georgian naval grandeur and a food scene built on what the "
            "sea brings in."
        ),
    ],
    "visit": [
        (
            "The Barbican venues sit within a few minutes of one another on and "
            "around Southside Street and New Street. Harbourside Fish and Chips, "
            "The Mad Merchant Coffee House and the Dolphin Hotel are all within "
            "a short walk, as is Barbican Kitchen inside the Gin Distillery. "
            "The waterbus from Sutton Harbour links to Royal William Yard "
            "without needing a car, or it is a pleasant mile along the "
            "Cremyll Ferry walkway."
        ),
        (
            "A good day's loop runs: coffee in the 16th-century Mad Merchant, "
            "a walk to the Mayflower Steps, fish and chips from Harbourside "
            "eaten on the quayside, an evening meal at Barbican Kitchen, and a "
            "final pint of cask Bass among the Beryl Cook canvases at the "
            "Dolphin. If the Hoe is in the plan, allow an hour for the views "
            "across Plymouth Sound before heading down to the Barbican."
        ),
    ],
    "checklist": [
        "Arrive at the Barbican mid-morning to beat the fish-and-chip queue at Harbourside",
        "Take a coffee at the Mad Merchant on New Street and look at the Elizabethan building",
        "Book Barbican Kitchen for dinner; weekends fill quickly",
        "Head to the Dolphin for last orders and look for the Beryl Cook originals",
        "Walk the Hoe before heading back to the city - the Sound views are worth it",
    ],
    "what_to_order": (
        "Order with intent. At Harbourside, the battered cod or hake with "
        "thick-cut chips, eaten on the quayside if the weather allows. At "
        "The Mad Merchant, ask which filter or espresso is on that week and "
        "pair it with one of the freshly made cakes. At Barbican Kitchen, "
        "follow the fish — whatever has come off the Plymouth day boats that "
        "morning — and do not skip a pudding in the distillery setting. At "
        "the Dolphin, order the Bass or whatever seasonal ale is on the cask "
        "gravity, and take your time."
    ),
    "glance": [
        ("Best for a quick bite", "Harbourside Fish and Chips for award-winning battered fish on the Barbican"),
        ("Best for an occasion", "Barbican Kitchen, two AA rosettes in the Plymouth Gin Distillery"),
        ("Best for atmosphere", "The Dolphin Hotel, Beryl Cook paintings and Bass from the cask"),
    ],
    "faq": [
        (
            "Where is the best fish and chips in Plymouth?",
            "Harbourside Fish and Chips at 35 Southside Street on the Barbican has been "
            "trading since the 1970s and was named 3rd Best Fish and Chip Shop in the UK "
            "at the 2018 National Fish and Chip Awards. The fish is locally landed and "
            "battered to order; a gluten-free shop operates next door.",
        ),
        (
            "What is the best restaurant in Plymouth for a special occasion?",
            "Barbican Kitchen, opened by the Tanner brothers in 2006 inside the Plymouth Gin "
            "Distillery on Southside Street, holds two AA Rosettes (awarded September 2025) "
            "and a place in the Michelin Guide. The menu is built around the West Country "
            "larder and day-boat fish from Plymouth market.",
        ),
        (
            "Which Plymouth pub has the most character?",
            "The Dolphin Hotel on The Barbican is Grade II-listed, hung with original "
            "paintings by the late Beryl Cook, and serves Bass and up to eight other ales "
            "by gravity straight from the cask. Plymouth CAMRA named it City Pub of the "
            "Year in 2020 and 2022.",
        ),
        (
            "Is there good independent coffee in Plymouth?",
            "The Mad Merchant Coffee House at 37 New Street on the Barbican serves "
            "speciality coffee and freshly cooked food inside a 16th-century Elizabethan "
            "merchant's house on Plymouth's oldest cobbled street. Open Wednesday to Sunday.",
        ),
        (
            "What are the best areas to eat in Plymouth?",
            "The Barbican and Sutton Harbour are the historic core, with the most "
            "independent restaurants, cafes and pubs. Royal William Yard, the restored "
            "naval victualling yard a mile west along the waterfront, offers a second "
            "cluster of restaurants in Grade I-listed granite buildings beside a marina.",
        ),
        (
            "Is Plymouth good for seafood?",
            "Yes. Plymouth has one of the South West's most active working harbours at "
            "Sutton Harbour, with a fish market supplying restaurants and fishmongers "
            "across Devon and Cornwall. The Barbican's independent restaurants and fish "
            "fryers are built around day-boat landings from the Channel.",
        ),
    ],
}

# hull ----------------------------------------------------------
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

# derby ----------------------------------------------------------
TOWNS["derby"] = {
    "region": "the East Midlands",
    "population": "260K",
    "nearby": ["Ilkeston", "Long Eaton", "Burton-on-Trent"],
    "meta_title": "Best Places to Eat in Derby: Local Food Guide",
    "meta_description": (
        "Where to eat in Derby: gyros at the Market Hall, speciality coffee "
        "on Iron Gate, two-AA-Rosette dining and the world oldest railway pub. "
        "Read the guide."
    ),
    "trust_strip": (
        "From the real-ale capital of England to a two-AA-Rosette kitchen, "
        "Derby eats and drinks well above its weight"
    ),
    "snapshot": (
        "For a fast answer: Tony's Greek Street Food at Derby Market Hall for "
        "gyros and souvlaki cooked to order, BEAR at Iron Gate for speciality "
        "coffee in a grand Victorian banking hall, The Pepperpot on London Road "
        "for two-AA-Rosette modern dining in a restored infirmary building, and "
        "the Brunswick Inn on Railway Terrace for 16 cask ales and on-site "
        "brewed ales in the world's oldest railway pub. Four moods, one "
        "compact city."
    ),
    "stats": [
        ("260K", "Population (approx)"),
        ("1841", "Year the Brunswick Inn first opened"),
        ("Real Ale Capital", "Lonely Planet's verdict on Derby"),
        ("4", "Hand-picked independents"),
    ],
    "pivot_variant": "pub-town",
    "pivot_local_hook": (
        "Derby's pub-town heritage means dozens of kitchens run long hours "
        "through lunch and dinner service; a real-ale city with an on-site "
        "brewery pub, a street-food hall and a fine-dining kitchen all "
        "generating heavy grease-laden vapour loads into their canopies "
        "every day."
    ),
    "venues": [
        {
            "type": "Takeaway",
            "name": "Tony's Greek Street Food",
            "area": "Derby Market Hall, Osnabruck Square, city centre",
            "cuisine": "Greek street food, gyros, souvlaki",
            "body": (
                "Tony brings more than 35 years of food experience in Greece and "
                "the UK to his stall at the refurbished Derby Market Hall, which "
                "reopened in May 2025 after a pound-35-million restoration. Founded "
                "in 2017 as a mobile food stall and previously nominated for the "
                "Best British Kebab Awards, Tony's is the standout independent at "
                "the hall's street-food hall, turning out hand-carved gyros piled "
                "into pitta with tzatziki, souvlaki skewers hot off the grill, "
                "halloumi wraps and moussaka made to a family recipe. The hall "
                "links the Cathedral Quarter to the Becketwell development, and "
                "Tony's is the go-to stop for a quick, honest, cooked-to-order "
                "lunch in the heart of the city."
            ),
            "known_for": "Authentic gyros and souvlaki cooked to order at Derby Market Hall",
            "good_for": "A fast, filling lunch in the newly restored city-centre market",
            "source_url": "https://www.derbymarkethall.co.uk/traders/tonys-greek-street-food/",
            "verified": "2026-06-22",
        },
        {
            "type": "Cafe",
            "name": "BEAR",
            "area": "7 Iron Gate, Cathedral Quarter",
            "cuisine": "Speciality coffee, brunch, seasonal small plates",
            "body": (
                "BEAR opened its Derby branch in 2017 inside a former Victorian "
                "banking hall on Iron Gate that had stood empty for nine years. "
                "The two founders spent their teenage years in the city, and the "
                "Derby branch quickly became the independent coffee anchor of the "
                "Cathedral Quarter. The brand, founded in 2014 and now spanning "
                "seven locations and over 150 jobs, roasts sustainably sourced "
                "single-origin beans and serves them as espresso, filter and a "
                "signature Espresso Martini that blurs the line between the coffee "
                "and cocktail menus. By day it runs all-day brunch and locally "
                "sourced seasonal food; by Friday and Saturday evenings the "
                "kitchen extends late and cocktails take over the grand room. "
                "Dog-friendly, with outdoor seating on Iron Gate."
            ),
            "known_for": "Speciality coffee and a signature Espresso Martini in a Victorian banking hall",
            "good_for": "A morning coffee, an all-day brunch or a Friday-evening cocktail",
            "source_url": "https://bemorebear.co/pages/iron-gate-derby",
            "verified": "2026-06-22",
        },
        {
            "type": "Restaurant",
            "name": "The Pepperpot",
            "area": "London Road, Nightingale Quarter",
            "cuisine": "Modern British, two AA Rosettes",
            "body": (
                "The Pepperpot opened on Valentine's Day 2024 inside a beautifully "
                "restored wing of the 130-year-old Derbyshire Royal Infirmary on "
                "London Road. The art deco renovation, with its glass extension to "
                "the rear looking over the Nightingale Quarter development, set the "
                "stage for a kitchen that earned one AA Rosette within its first "
                "year and a second in February 2026, a striking pace. Head chef "
                "Dan Fincher, a member of The Master Chefs of Great Britain, runs "
                "the kitchen across breakfast, lunch and dinner seven days a week. "
                "The restaurant was named Restaurant of the Year 2025 at the "
                "Marketing Derby Food and Drink Awards. Book ahead for dinner; "
                "the weekend brunch is popular with the Nightingale Quarter crowd."
            ),
            "known_for": "Two AA Rosettes (2026), housed in a restored Victorian infirmary",
            "good_for": "A special-occasion dinner or a landmark brunch in a heritage setting",
            "source_url": "https://www.pepperpotderby.co.uk/",
            "verified": "2026-06-22",
        },
        {
            "type": "Pub",
            "name": "The Brunswick Inn",
            "area": "1 Railway Terrace, Railway Village",
            "cuisine": "Pub food, cask ales and on-site brewed ales",
            "body": (
                "Built in 1841 and Grade II-listed, the Brunswick Inn is the oldest "
                "purpose-built railway pub in the world, erected at the end of the "
                "original Derby Station platforms as the drinking house for "
                "railwaymen and second-class passengers. Threatened with clearance "
                "in the 1970s, it was saved as part of the Railway Conservation "
                "Area and reopened as a real-ale house in 1987; the on-site "
                "Brunswick Brewery, Derby's oldest, was added in 1991 and brews "
                "White Feather, Triple Hop, Second Brew and Railway Porter among "
                "its regulars. Today the pub carries 16 cask ales and 16 real "
                "ciders simultaneously, is owned by Everards and was named Derby "
                "CAMRA Pub of the Year 2026, retaining the Cider Pub of the Year "
                "title it has held for ten years running. Jazz every Thursday; "
                "annual October beer festival. Two hundred metres from the station."
            ),
            "known_for": "Oldest railway pub in the world (1841), CAMRA Derby Pub of the Year 2026, on-site brewery",
            "good_for": "A serious real-ale session steps from Derby Station in a living piece of railway history",
            "source_url": "https://everards.co.uk/news/brunswick-inn-crowned-derby-camra-pub-of-the-year-and-we-couldnt-be-prouder",
            "verified": "2026-06-22",
        },
    ],
    "food_scene": [
        (
            "Derby's food map runs from the Cathedral Quarter at its heart outward "
            "to the Nightingale Quarter on London Road and the historic Railway "
            "Village to the south-east. The Cathedral Quarter, centred on Iron "
            "Gate, Sadler Gate and the Market Place, is where the city's "
            "independent cafes, delis and restaurants cluster among Georgian and "
            "Victorian shopfronts, with BEAR's Iron Gate banking hall one of the "
            "quarter's most striking rooms. The refurbished Derby Market Hall, "
            "reopened in 2025 after a thirty-five-million-pound restoration, "
            "links the Cathedral Quarter to Becketwell and gives the city a "
            "proper street-food hall for the first time."
        ),
        (
            "Derby's most celebrated food-and-drink identity is its real-ale "
            "heritage. Lonely Planet named it the best place to drink real ale "
            "in the world, and the Derby CAMRA branch's annual Beer Census has "
            "confirmed the city as the real-ale capital of Britain per head of "
            "population. Three major Victorian breweries - Offilers, Strettons "
            "and Altons - once supplied the city's extraordinary density of "
            "pubs, and Derby had one ale house for every forty people as far "
            "back as 1588. The Brunswick's on-site brewery keeps that tradition "
            "alive in the Railway Village today."
        ),
        (
            "Fine dining arrived quietly but firmly with The Pepperpot's two AA "
            "Rosettes in 2026, adding a high-end option to complement the "
            "city's established Michelin-Guide listed Darleys at Darley Abbey "
            "Mills. The food geography is compact enough to walk: a market-hall "
            "gyros, a Cathedral Quarter flat white, a celebrated dinner and a "
            "railway-history pint are all within a mile and a half of one another."
        ),
    ],
    "visit": [
        (
            "The Cathedral Quarter and Derby Market Hall are at the walkable "
            "centre of the food trail, with BEAR on Iron Gate and Tony's at "
            "the Market Hall less than five minutes apart on foot. The Pepperpot "
            "is a fifteen-minute walk south on London Road, or a short bus ride. "
            "The Brunswick Inn is a ten-minute walk east from the city centre, "
            "or two hundred metres from Derby Station - making it a natural start "
            "or finish for visitors arriving by rail."
        ),
        (
            "A day flows naturally: a speciality coffee or brunch at BEAR in the "
            "morning, a gyros at the Market Hall for lunch, The Pepperpot saved "
            "for dinner and the Brunswick for a final pint in the Railway Village. "
            "Book The Pepperpot well ahead, especially at weekends. The Brunswick "
            "needs no reservation and is open every day."
        ),
    ],
    "checklist": [
        "Start with coffee or brunch at BEAR in the Victorian banking hall on Iron Gate",
        "Walk to Derby Market Hall and order a gyros or souvlaki at Tony's for lunch",
        "Browse the Cathedral Quarter streets around Sadler Gate between stops",
        "Book The Pepperpot in advance - weekend dinner and brunch fill quickly",
        "End at the Brunswick Inn near Derby Station for a pint from the on-site brewery",
    ],
    "what_to_order": (
        "Order with intent. At Tony's Greek Street Food, the hand-carved gyros in "
        "pitta with tzatziki and a souvlaki skewer on the side. At BEAR, ask what "
        "single origin is on the espresso that morning, or book an evening slot "
        "for the signature Espresso Martini. At The Pepperpot, surrender to the "
        "dinner menu and let Dan Fincher's kitchen set the pace - the tasting "
        "format shows off the two-Rosette cooking at its best. At the Brunswick, "
        "a pint of Railway Porter or Triple Hop from the in-house brewery, "
        "taken slowly in the original Victorian railway-village pub."
    ),
    "glance": [
        ("Best for a quick bite", "Tony's Greek Street Food for gyros at the restored Derby Market Hall"),
        ("Best for an occasion", "The Pepperpot, for two-AA-Rosette modern dining in a Victorian infirmary"),
        ("Best for atmosphere", "The Brunswick Inn - the world's oldest railway pub, CAMRA Pub of the Year 2026"),
    ],
    "faq": [
        (
            "Where can I get good street food in Derby city centre?",
            "Derby Market Hall, reopened in May 2025 after a pound-35-million "
            "restoration, is the city centre's best street-food destination. "
            "Tony's Greek Street Food, a trader there since the hall reopened, "
            "serves gyros, souvlaki and halloumi wraps cooked to order.",
        ),
        (
            "Is Derby really the real-ale capital of England?",
            "Derby CAMRA's annual Beer Census has consistently confirmed Derby "
            "as the real-ale capital of Britain per head of population, and "
            "Lonely Planet named it the best place to drink real ale in the "
            "world. The Brunswick Inn on Railway Terrace won Derby CAMRA Pub "
            "of the Year 2026 and carries 16 cask ales plus its own brewery.",
        ),
        (
            "Which is the best independent cafe in Derby?",
            "BEAR at 7 Iron Gate, in the Cathedral Quarter, is Derby's leading "
            "independent speciality coffee venue. The brand, founded in 2014, "
            "opened in a restored Victorian banking hall in 2017 and serves "
            "sustainably sourced espresso, filter coffee and brunch all day.",
        ),
        (
            "Does Derby have any award-winning fine-dining restaurants?",
            "Yes. The Pepperpot on London Road holds two AA Rosettes for "
            "Culinary Excellence, awarded in February 2026 - a remarkable "
            "achievement for a restaurant that only opened in February 2024. "
            "It was also named Restaurant of the Year 2025 at the Marketing "
            "Derby Food and Drink Awards.",
        ),
        (
            "What is the history of the Brunswick Inn in Derby?",
            "Built in 1841 as part of the Midland Railway Village, the Brunswick "
            "is the oldest purpose-built railway pub in the world and is Grade "
            "II-listed. It was restored in the 1980s and reopened as a real-ale "
            "pub in 1987. The on-site brewery was added in 1991 and still brews "
            "Railway Porter, Triple Hop and White Feather on the premises.",
        ),
        (
            "Can I do a Derby food day on foot?",
            "Easily. BEAR on Iron Gate, Tony's at Derby Market Hall and the "
            "Cathedral Quarter are all within a five-minute walk of one another. "
            "The Pepperpot is fifteen minutes south on London Road. The Brunswick "
            "Inn is ten minutes east of the centre, or two hundred metres from "
            "Derby Station - ideal if you are arriving by rail.",
        ),
    ],
}

# southampton ----------------------------------------------------------
TOWNS["southampton"] = {
    "region": "Hampshire",
    "population": "255,000",
    "nearby": ["Eastleigh", "Fareham", "Winchester"],
    "meta_title": "Best Places to Eat in Southampton: Local Food Guide",
    "meta_description": (
        "Where to eat in Southampton: Thai tapas near the Guildhall, a gallery "
        "cafe, an AA Rosette Italian and a medieval brewpub. Read the guide."
    ),
    "trust_strip": (
        "From a medieval wool warehouse brewpub to an AA Rosette Italian on the "
        "waterfront, Southampton's independent food scene punches well above its size"
    ),
    "snapshot": (
        "For a fast answer: Mango Thai Tapas on Above Bar for sharing plates "
        "of Thai tapas in a Tudor building, Coffeelogy on Vincents Walk for "
        "independent coffee inside a not-for-profit art gallery, Ennios at Town "
        "Quay for AA Rosette modern Italian in a Victorian dockside warehouse, "
        "and Dancing Man Brewery in the Grade I-listed medieval Wool House for "
        "craft ales brewed on site. Four moods, one walkable waterfront city."
    ),
    "stats": [
        ("255,000", "City population (approx)"),
        ("1338", "Year the Wool House was built by Cistercian monks"),
        ("2007", "Year Mango Thai first opened in Southampton"),
        ("4", "Hand-picked independents"),
    ],
    "pivot_variant": "coastal",
    "pivot_local_hook": (
        "Southampton's kitchens serve a city that has fed travellers and "
        "seafarers since the Wool House quay was loading ships in the "
        "fourteenth century — cruise-season surges and a year-round port "
        "economy push canopy grease loads high from the waterfront bistros "
        "to the busy Above Bar dining strip."
    ),
    "venues": [
        {
            "type": "Takeaway/Casual",
            "name": "Mango Thai Tapas",
            "area": "Above Bar Street, city centre (Cultural Quarter)",
            "cuisine": "Thai tapas, sharing plates",
            "body": (
                "Mango Thai is proudly independent, family-owned, and has been "
                "part of the Southampton food scene since the original Portswood "
                "restaurant opened in 2007. The Above Bar branch followed in "
                "March 2012, set over two floors of a Tudor building near "
                "Guildhall Square in the city's Cultural Quarter. The concept is "
                "sharing: small plates of authentic Thai-inspired dishes — "
                "satay, pad thai, green and red curries, sticky ribs — ordered "
                "so the whole table eats together in the traditional way. Tropical "
                "cocktails complete the picture. Three locations and nearly two "
                "decades later, Mango Thai remains the city's most loved "
                "independent for casual Thai food, well reviewed into 2025 and 2026."
            ),
            "known_for": "Sharing-style Thai tapas in a Tudor Above Bar building since 2007",
            "good_for": "A casual group meal with cocktails in the city centre",
            "source_url": "https://www.mangothai.co.uk/mango-above-bar",
            "verified": "2026-06-22",
        },
        {
            "type": "Cafe",
            "name": "Coffeelogy",
            "area": "1 Vincents Walk, city centre",
            "cuisine": "Speciality coffee, all-day breakfast",
            "body": (
                "Tucked into Vincents Walk in the heart of Southampton, "
                "Coffeelogy is unlike any other coffee shop in the city: an "
                "independent cafe running in support of a not-for-profit art "
                "gallery, where the walls change exhibition every few weeks. "
                "The coffee is sourced from local independent roasters and "
                "served with genuine care, alongside Turkish bagels, cinnamon "
                "swirls, all-day breakfast and freshly baked croissants. The "
                "gallery work is curated by design studio Inco Architecture, "
                "giving the room a calm, interesting quality that suits both a "
                "working morning and a slow afternoon. Rated 4.6 of 5 on "
                "Tripadvisor and listed in 2026 Southampton coffee guides as the "
                "best pick for a quiet central city brew."
            ),
            "known_for": "Independent coffee inside a rotating not-for-profit art gallery",
            "good_for": "A quiet coffee with something to look at",
            "source_url": "https://www.coffeelogy.co.uk/",
            "verified": "2026-06-22",
        },
        {
            "type": "Restaurant",
            "name": "Ennios",
            "area": "Town Quay Road, Old Town waterfront",
            "cuisine": "Modern Italian, fresh seafood and pasta",
            "body": (
                "Ennios occupies the ground floor of a Victorian dockside "
                "warehouse designed by architect John Geddes, where the sea "
                "once reached the foundations so boats could unload directly "
                "inside. The spacious split-level restaurant and bar is now one "
                "of Southampton's most atmospheric rooms: exposed brick, high "
                "ceilings and a harbour outlook. The kitchen cooks modern "
                "Italian with a clear preference for fresh pasta and the catch "
                "of the day — seafood specials change daily, and the pasta is "
                "made on site. Ennios holds an AA Rosette (awarded 2023, "
                "confirmed current) and was voted best Italian in Hampshire by "
                "Corriere della Sera. From May 2026 open for lunch midday seven "
                "days a week."
            ),
            "known_for": "AA Rosette modern Italian and fresh seafood in a Victorian dockside warehouse",
            "good_for": "A proper occasion meal on the Southampton waterfront",
            "source_url": "https://mustanggroup.co.uk/venues/ennios/",
            "verified": "2026-06-22",
        },
        {
            "type": "Pub",
            "name": "Dancing Man Brewery",
            "area": "The Wool House, Town Quay, Old Town",
            "cuisine": "Craft ales brewed on site, British pub food",
            "body": (
                "The Wool House is Southampton's most remarkable building: a "
                "Grade I-listed medieval stone warehouse built in 1338 by "
                "Cistercian monks from Beaulieu Abbey, when the city was one of "
                "England's leading wool ports. Spanish and French prisoners of "
                "war held here in the 1700s carved inscriptions into the original "
                "roof timbers that can still be read today. Since 2015 the "
                "building has housed Dancing Man Brewery, an independent 1,000-"
                "litre brewpub that brews four regular and a rotating range of "
                "craft ales on site. The 110-seat restaurant serves hearty food "
                "with strong vegan and vegetarian options. CAMRA listed, well "
                "reviewed in 2025-2026 for beer range and atmosphere."
            ),
            "known_for": "Craft ales brewed in a Grade I-listed medieval wool warehouse built 1338",
            "good_for": "A craft pint inside seven centuries of Southampton history",
            "source_url": "https://dancingmanbrewery.co.uk/",
            "verified": "2026-06-22",
        },
    ],
    "food_scene": [
        (
            "Southampton's food map is shaped by its port. Oxford Street and Above Bar "
            "hold the city's main independent dining strip, where restaurants spill "
            "onto pedestrianised pavements and cover everything from Thai tapas to "
            "Italian and Afro-Caribbean. Bedford Place, one street north, offers "
            "a quieter but equally committed line of independents. These two streets "
            "are where the city eats on a weeknight."
        ),
        (
            "The Old Town, tucked behind the medieval walls along Town Quay, is a "
            "different register: quieter, older and defined by its waterfront. "
            "Ennios and Dancing Man Brewery both sit here, in Victorian and medieval "
            "buildings that were loading cargo centuries before the first restaurant "
            "opened. The Titanic connection runs deep — three quarters of the ship's "
            "crew came from Southampton, and Oxford Street pubs like the White Star "
            "Tavern take their name directly from the shipping line."
        ),
        (
            "The wider city adds University Road in Portswood for student-friendly "
            "independents, and Ocean Village Marina for waterfront dining with a "
            "more international flavour. There is no single signature dish — "
            "Southampton is a port city that has absorbed cooking from everywhere — "
            "but fresh seafood from the south coast, Thai tapas and Italian pasta "
            "come closest to defining what locals reach for."
        ),
    ],
    "visit": [
        (
            "The geography is compact. Mango Thai and Coffeelogy both sit in or "
            "near the city centre, a few minutes walk apart. Ennios and Dancing "
            "Man Brewery are a ten-minute walk south along the waterfront at "
            "Town Quay, passing through the medieval Bar Gate and along the old "
            "walls. Southampton Central station is close; most of this guide "
            "is walkable from the platform."
        ),
        (
            "A good day runs: morning coffee at Coffeelogy with the gallery, Thai "
            "tapas at Mango for lunch or a casual dinner, and then an evening "
            "choice between Ennios for a proper sit-down Italian meal or a craft "
            "ale inside the seven-century-old Wool House at Dancing Man. Both "
            "Ennios and Dancing Man are best booked ahead for evenings."
        ),
    ],
    "checklist": [
        "Start at Coffeelogy on Vincents Walk for coffee inside the gallery",
        "Walk up to Above Bar for Mango Thai tapas -- book ahead for evenings",
        "Head south through the Bar Gate to the Old Town waterfront",
        "Book Ennios ahead for the Italian tasting, or call Dancing Man for brewery tours",
        "Allow time to walk the medieval walls between Town Quay and the Bar Gate",
    ],
    "what_to_order": (
        "Order with intent. At Mango Thai, work the sharing menu: satay sticks, "
        "a green curry, pad thai and sticky ribs split across the table with a "
        "tropical cocktail. At Coffeelogy, ask which local roaster is on the "
        "espresso machine and pair it with a cinnamon swirl. At Ennios, lead "
        "with the fresh seafood special of the day and a handmade pasta, and "
        "finish Italian-style. At Dancing Man, take a tasting paddle of the "
        "brewer's rotating ales and stay for a pie in the medieval hall."
    ),
    "glance": [
        ("Best for a quick bite", "Mango Thai Tapas on Above Bar for Thai sharing plates"),
        ("Best for an occasion", "Ennios for AA Rosette Italian in a Victorian dockside warehouse"),
        ("Best for atmosphere", "Dancing Man Brewery inside the 1338 Grade I-listed Wool House"),
    ],
    "faq": [
        (
            "Where can I eat good Thai food in Southampton city centre?",
            "Mango Thai Tapas on Above Bar Street has been serving sharing-style "
            "Thai tapas in Southampton since 2007. The Above Bar branch opened in "
            "2012 in a Tudor building near Guildhall Square and is family-owned "
            "and independent, with tropical cocktails alongside the food.",
        ),
        (
            "What is the best independent coffee shop in Southampton?",
            "Coffeelogy on Vincents Walk is a standout: an independent cafe "
            "running inside a not-for-profit art gallery, serving coffee from "
            "local roasters alongside all-day breakfast and freshly baked "
            "croissants, with the gallery exhibiting changing work from local artists.",
        ),
        (
            "Is there a good restaurant on Southampton waterfront?",
            "Ennios at Town Quay Road occupies a Victorian dockside warehouse "
            "where the sea once came up to the foundations. It holds an AA "
            "Rosette for its modern Italian cooking, with fresh pasta made on "
            "site and daily-changing seafood specials from the south coast catch.",
        ),
        (
            "What is the Dancing Man Brewery and where is it?",
            "Dancing Man Brewery is an independent 1,000-litre brewpub in the "
            "Wool House on Town Quay -- a Grade I-listed medieval stone warehouse "
            "built in 1338 by Cistercian monks. It brews four regular ales and "
            "a rotating range on site, and the building still has prisoner-of-war "
            "carvings from the 1700s in its original roof timbers.",
        ),
        (
            "Does Southampton have a signature dish?",
            "Southampton has no single signature dish -- its port history has "
            "made it one of the most diverse food cities in the South. Fresh "
            "south coast seafood, Thai tapas and Italian pasta define the "
            "independent scene best, with fish and chips close behind as a "
            "waterfront staple.",
        ),
        (
            "What are the main eating areas in Southampton?",
            "Oxford Street and Above Bar are the main independent dining strips, "
            "with restaurants and cafes spilling onto pedestrianised pavements. "
            "The Old Town along Town Quay holds the heritage waterfront venues "
            "including Dancing Man Brewery and Ennios. Bedford Place adds a "
            "quieter row of independents one street north of the city centre.",
        ),
    ],
}

# stoke-on-trent ----------------------------------------------------------
TOWNS["stoke-on-trent"] = {
    "region": "Staffordshire",
    "population": "255K",
    "nearby": ["Newcastle-under-Lyme", "Stafford", "Kidsgrove"],
    "meta_title": "Best Places to Eat in Stoke-on-Trent: Local Food Guide",
    "meta_description": (
        "Where to eat in Stoke-on-Trent: a hand-rolled oatcake shop, a canal-side "
        "pottery cafe, a long-loved Italian, and the Titanic brewery tap. "
        "Read the guide."
    ),
    "trust_strip": (
        "From the Staffordshire oatcake to a canal-side pottery cafe, Stoke-on-Trent "
        "is a city of six towns and one fiercely independent food culture"
    ),
    "snapshot": (
        "For a fast answer: Staffordshire Oatcakes UK in Hanley for the city's own "
        "street food made by hand, The Packing House Cafe at Middleport Pottery for "
        "a canalside lunch in a working Victorian factory, La Bella Napoli on "
        "Piccadilly for 35 years of family Italian in the heart of Hanley, and "
        "The Bulls Head in Burslem for Titanic Brewery cask ales at the original "
        "brewery tap. Six towns, one appetite."
    ),
    "stats": [
        ("255K", "Population (approx)"),
        ("6", "Towns that make up the Potteries"),
        ("1889", "Year Middleport Pottery opened on the Trent and Mersey canal"),
        ("4", "Hand-picked independents"),
    ],
    "pivot_variant": "high-volume",
    "pivot_local_hook": (
        "Stoke-on-Trent's oatcake shops, curry houses and pub kitchens run long "
        "service hours across six towns, and the thick, yeasty oatcake batter "
        "sizzling on a griddle sends a steady load of grease-laden vapour into "
        "canopies every morning from opening time."
    ),
    "venues": [
        {
            "type": "Takeaway/Oatcake Shop",
            "name": "Staffordshire Oatcakes UK",
            "area": "112 Broad Street, Hanley",
            "cuisine": "Staffordshire oatcakes, traditional takeaway",
            "body": (
                "The Staffordshire oatcake is the city's own street food: a soft, "
                "yeasty pancake made from oatmeal and flour, cooked on a griddle and "
                "filled with cheese, bacon or a full breakfast. Jason opened this "
                "freshly fitted shop on Broad Street in Hanley in August 2019, "
                "returning to a trade he learned as a teenager helping in his "
                "mother's oatcake shop. He makes every oatcake by hand, one of the "
                "few remaining shops in the city to do so, and ships them UK-wide as "
                "well as serving them fresh at the counter. The shop appeared on "
                "BBC1's Antiques Road Trip, drawing national attention to what "
                "locals have always known. It had a food hygiene inspection in "
                "October 2025, confirming it is fully operational. A plain oatcake "
                "with cheese, or filled with bacon and egg, is the order to make."
            ),
            "known_for": "Hand-rolled Staffordshire oatcakes, the Potteries street food",
            "good_for": "A warm, filled oatcake fresh off the griddle",
            "source_url": "https://vinsights.co.uk/Business/1215533",
            "verified": "2026-06-22",
        },
        {
            "type": "Cafe",
            "name": "The Packing House Cafe",
            "area": "Middleport Pottery, Port Street, Burslem",
            "cuisine": "Cafe, locally sourced British",
            "body": (
                "Middleport Pottery on the Trent and Mersey canal in Burslem has "
                "been the home of Burleigh since 1889, and is one of the last "
                "working Victorian pottery factories in the country. The Packing "
                "House Cafe is built into the original packing warehouse, with "
                "exposed brickwork, a wood-burning stove for winter visits and "
                "outdoor canal-side seating for summer. The menu centres on locally "
                "sourced and freshly prepared dishes including Staffordshire "
                "oatcakes and traditional lobby (a Potteries beef broth), alongside "
                "soups, sandwiches and good cake. It was Highly Commended in the "
                "Visit Staffordshire and Stoke-on-Trent Tourism Awards Tea Room and "
                "Coffee Shop of the Year 2026. Open daily 10am to 4pm."
            ),
            "known_for": "Canal-side cafe in a working Victorian pottery, Staffordshire oatcakes and lobby",
            "good_for": "Lunch by the Trent and Mersey canal with a slice of Potteries history",
            "source_url": "https://re-form.org/heritage-buildings/middleport-pottery/the-packing-house-cafe/",
            "verified": "2026-06-22",
        },
        {
            "type": "Restaurant",
            "name": "La Bella Napoli",
            "area": "46-48 Piccadilly, Hanley",
            "cuisine": "Italian, traditional Neapolitan",
            "body": (
                "La Bella Napoli has been feeding Hanley since 1988, making it one "
                "of the longest-serving independent restaurants in the Potteries. "
                "The family-owned Italian moved to its current site on Piccadilly, "
                "directly opposite the Regent Theatre, and the combination of "
                "reliable pre-theatre dining, an authentic Neapolitan kitchen and "
                "daily-made tiramisu has kept it busy ever since. The menu runs "
                "from classic pizzas and handmade pasta to fish and meat mains, "
                "all cooked without shortcuts. The tiramisu is made in limited "
                "quantities each day, so it is worth asking early. The company "
                "filed active accounts to November 2024 and recent reviews confirm "
                "it is trading in 2025. Book ahead, especially on theatre nights."
            ),
            "known_for": "35 years of family Italian, daily-made tiramisu, pre-theatre dining",
            "good_for": "A dependable occasion dinner opposite the Regent Theatre",
            "source_url": "https://www.labellanapoli.co.uk/",
            "verified": "2026-06-22",
        },
        {
            "type": "Pub",
            "name": "The Bulls Head",
            "area": "14 St Johns Square, Burslem",
            "cuisine": "British pub, real ale",
            "body": (
                "Titanic Brewery was founded in Burslem in 1985, and The Bulls Head "
                "on St Johns Square is its original brewery tap, the first pub the "
                "brewery acquired and still its flagship. In the mother town of the "
                "Potteries, the pub has been in the CAMRA Good Beer Guide since "
                "2007 and won the CAMRA Potteries Pub of the Year in 2022. The "
                "cellar runs to nine rotating real ales plus up to ten real ciders, "
                "a wide choice of single malt whiskies and a range of bottled "
                "Belgian beers. Traditional pub games including bar billiards and "
                "table skittles are still played. It is the unofficial home end for "
                "Port Vale supporters on home match days, with a BBQ set up outside. "
                "Confirmed open with current 2026 hours listed on the Titanic "
                "Brewery website."
            ),
            "known_for": "Titanic Brewery tap, nine rotating real ales, CAMRA Good Beer Guide since 2007",
            "good_for": "Real ale in the Potteries, pub games, and a proper cask-ale cellar",
            "source_url": "https://www.titanicbrewery.co.uk/pubs-and-bods/pubs/the-bulls-head",
            "verified": "2026-06-22",
        },
    ],
    "food_scene": [
        (
            "Stoke-on-Trent is not one town but six — Hanley, Burslem, Longton, "
            "Fenton, Tunstall and Stoke itself — federated in 1910 into what "
            "Reginald Haggar called the Potteries. Each has its own high street "
            "and its own character, and eating here means moving between them. "
            "Hanley is the commercial centre where most restaurants cluster; "
            "Burslem, the mother town of the Potteries, keeps a more independent "
            "feel with the Titanic Brewery and Middleport Pottery close by."
        ),
        (
            "The signature food of the city is the Staffordshire oatcake: a soft, "
            "yeasty pancake made from oatmeal batter, cooked on a griddle and "
            "filled to order. It has been a Potteries staple since the nineteenth "
            "century, when potters ate them wrapped around a canteen filling for "
            "warmth and convenience. The independent oatcake shops that sold them "
            "through a hole in the wall were once counted in the dozens; a handful "
            "survive, and they are a local institution visited before most other "
            "food stops. Alongside the oatcake, traditional lobby "
            "a slow-cooked beef and vegetable broth "
            "is the other Potteries comfort dish, still served in a few cafes."
        ),
        (
            "The Cultural Quarter around Piccadilly and the Regent Theatre is "
            "where independent cafes, Italian restaurants and small bars have "
            "settled, while the Spode Creative Village in Stoke town has become "
            "a post-industrial destination with the Quarter at Potbank occupying "
            "the original pottery factory. Titanic Brewery, founded in Burslem in "
            "1985, now supplies pubs across the region and runs several of its own, "
            "with the Potteries well represented in the CAMRA Good Beer Guide. The "
            "city is not a foodie destination in the London or Birmingham mould, "
            "but its independent streak and its oatcake tradition make it genuinely "
            "its own."
        ),
    ],
    "visit": [
        (
            "The six towns are spread across a few miles of the A500 corridor, so "
            "a food day here involves a little navigation. Hanley is the natural "
            "centre: the oatcake shop, La Bella Napoli and the Cultural Quarter "
            "cafes are all within easy walking distance. Burslem is about two miles "
            "north, reachable by bus or a short drive, with Middleport Pottery and "
            "The Bulls Head both worth the trip."
        ),
        (
            "The best approach is to start early in Hanley with a fresh oatcake, "
            "head to Burslem for the Packing House Cafe at Middleport Pottery for "
            "lunch by the canal, then return to Hanley for dinner at La Bella Napoli "
            "before finishing the evening at The Bulls Head in Burslem. "
            "Titanic Brewery runs tours and their ales are on at the tap. "
            "Most of Hanley is pedestrianised; Burslem has free on-street parking "
            "near the pottery."
        ),
    ],
    "checklist": [
        "Start the morning with a filled oatcake fresh off the griddle at Staffordshire Oatcakes UK on Broad Street",
        "Head to Burslem for lunch at the Packing House Cafe beside the Trent and Mersey canal",
        "Walk or drive to Middleport Pottery to see the working Victorian factory and Burleigh shop",
        "Book La Bella Napoli in Hanley for dinner, especially on Regent Theatre nights",
        "End at The Bulls Head in Burslem for a pint of Titanic cask ale at the original brewery tap",
    ],
    "what_to_order": (
        "Order with the city in mind. At Staffordshire Oatcakes UK, a plain oatcake "
        "filled with mature cheese or a full breakfast filling — eat it hot at the "
        "counter. At the Packing House Cafe, the Staffordshire oatcakes with lobby "
        "or a freshly made soup beside the canal. At La Bella Napoli, a classic "
        "Neapolitan pizza or handmade pasta, and ask for the tiramisu before it "
        "runs out. At The Bulls Head, work through Titanic's rotating cask ales "
        "and ask the bar which is freshest."
    ),
    "glance": [
        ("Best for a quick bite", "Staffordshire Oatcakes UK, for a warm filled oatcake in Hanley"),
        ("Best for an occasion", "La Bella Napoli, for 35 years of family Italian opposite the Regent Theatre"),
        ("Best for atmosphere", "The Packing House Cafe, in a working Victorian pottery beside the canal"),
    ],
    "faq": [
        (
            "What is a Staffordshire oatcake?",
            "A Staffordshire oatcake is a soft, yeasty pancake made from oatmeal "
            "batter and cooked on a griddle. It has been a Potteries staple since "
            "the nineteenth century, when potters ate them filled with a hot "
            "canteen filling. They are filled to order with cheese, bacon, egg "
            "or a combination and eaten fresh. Staffordshire Oatcakes UK on Broad "
            "Street in Hanley is one of the few shops to still make them entirely "
            "by hand."
        ),
        (
            "Where can I buy a Staffordshire oatcake in Stoke-on-Trent?",
            "Staffordshire Oatcakes UK at 112 Broad Street, Hanley, is a dedicated "
            "oatcake shop that makes them by hand and fills them to order at the "
            "counter. It also ships oatcakes and oatcake mix UK-wide. Other "
            "independent oatcake shops operate across the six towns, and the "
            "Packing House Cafe at Middleport Pottery also serves them as part "
            "of a traditional Potteries menu."
        ),
        (
            "What is the best pub for real ale in Stoke-on-Trent?",
            "The Bulls Head on St Johns Square in Burslem is Titanic Brewery's "
            "original brewery tap and has been in the CAMRA Good Beer Guide since "
            "2007. It runs nine rotating cask ales plus up to ten real ciders, "
            "single malts and Belgian bottles, alongside traditional pub games "
            "including bar billiards and table skittles."
        ),
        (
            "What is Middleport Pottery and why should I visit?",
            "Middleport Pottery in Burslem is one of the last working Victorian "
            "pottery factories in England and has been the home of Burleigh since "
            "1889. It sits beside the Trent and Mersey canal and offers factory "
            "tours, a Burleigh shop and the Packing House Cafe, which was Highly "
            "Commended in the Visit Staffordshire Tourism Awards 2026. The cafe "
            "is open daily 10am to 4pm."
        ),
        (
            "Is La Bella Napoli in Stoke-on-Trent a good restaurant?",
            "La Bella Napoli has been one of Hanley's most reliable independent "
            "restaurants since 1988, making it the longest-serving Italian in the "
            "city centre. It is now at 46-48 Piccadilly opposite the Regent "
            "Theatre and is popular for pre-theatre dining. The tiramisu is made "
            "daily in limited quantities and is the dessert to order."
        ),
        (
            "Can you eat well in Stoke-on-Trent on a day trip?",
            "Yes. Start with a hand-rolled oatcake at Staffordshire Oatcakes UK "
            "in Hanley, then head to Burslem for lunch at the Packing House Cafe "
            "beside the Trent and Mersey canal. Return to Hanley for dinner at "
            "La Bella Napoli, and finish at The Bulls Head in Burslem for Titanic "
            "Brewery cask ales. Bus routes connect the six towns, and Hanley is "
            "largely pedestrianised."
        ),
    ],
}

# wolverhampton ----------------------------------------------------------
TOWNS["wolverhampton"] = {
    "region": "the West Midlands",
    "population": "265K",
    "nearby": ["Walsall", "Dudley", "Bilston"],
    "meta_title": "Best Places to Eat in Wolverhampton: Local Food Guide",
    "meta_description": (
        "Where to eat in Wolverhampton: homemade-batter fish bar, artisan "
        "sourdough bakery, two-AA-Rosette Indian and a Victorian real-ale pub. "
        "Read the guide."
    ),
    "trust_strip": (
        "From a Holden's-tied Victorian railway pub to the two-AA-Rosette "
        "fine dining of The Bilash, Wolverhampton offers a proper Black Country "
        "food crawl hiding in plain sight"
    ),
    "snapshot": (
        "For a fast answer: Seagull Fish Bar in Finchfield for freshly battered "
        "fish and chips from a family-run chip shop, Medicine Bakery in the "
        "Chubb Building for hand-shaped sourdough and pastries, The Bilash on "
        "Cheapside for two-AA-Rosette Bengali fine dining open since 1982, and "
        "The Great Western near the station for Holden's cask ales in a Grade "
        "II railway pub that won CAMRA National Pub of the Year."
    ),
    "stats": [
        ("265K", "Population (approx)"),
        ("1982", "Year The Bilash first opened on Cheapside"),
        ("Black Country", "The food tradition Wolverhampton is rooted in"),
        ("4", "Hand-picked independents"),
    ],
    "pivot_variant": "high-volume",
    "pivot_local_hook": (
        "Wolverhampton's kitchens run hard: the city's balti houses and "
        "high-volume curry restaurants sear spiced oil at fierce heat every "
        "service, while the pub and chippy fryers run continuous cycles through "
        "busy match days and market-day crowds, loading canopies with a heavy "
        "accumulation of grease-laden vapour."
    ),
    "venues": [
        {
            "type": "Takeaway",
            "name": "Seagull Fish Bar",
            "area": "16 Finchfield Road West, Finchfield",
            "cuisine": "Fish and chips",
            "body": (
                "Finchfield locals have been lining up at the Seagull for "
                "years, drawn by a formula the kitchen does not tamper with: "
                "cod, haddock and plaice coated in the house homemade batter "
                "and cooked to order, served with proper chips and the "
                "chippy's own mushy peas and curry sauce. The fish bar earned "
                "a five-star food hygiene rating from Wolverhampton City "
                "Council in February 2024, and customer reviews consistently "
                "praise the freshness of the fish and the generosity of the "
                "portions. It is a no-frills, family-run operation on the "
                "western fringe of the city, open Tuesday to Saturday from "
                "late afternoon into the evening. The Black Country's chippy "
                "tradition is as old as its ironworks, and the Seagull keeps "
                "it alive without any fuss."
            ),
            "known_for": "Homemade batter, freshly cooked fish, five-star hygiene rating",
            "good_for": "A proper Black Country chippy supper, families",
            "source_url": "https://www.tripadvisor.co.uk/Restaurant_Review-g190762-d9789753-Reviews-Seagull_Fish_Bar-Wolverhampton_West_Midlands_England.html",
            "verified": "2026-06-22",
        },
        {
            "type": "Cafe",
            "name": "Medicine Bakery",
            "area": "Chubb Building, Fryer Street, city centre",
            "cuisine": "Artisan sourdough, pastries, brunch",
            "body": (
                "Medicine started life in the nighttime bars of Birmingham's "
                "Digbeth before evolving into one of the West Midlands' most "
                "distinctive independent bakery groups. Its production "
                "headquarters now occupies Unit 6 of the historic Chubb "
                "Building on Fryer Street, a converted Victorian lock "
                "factory a short walk from Wolverhampton's town centre. "
                "Bakers work through the night handcrafting sourdough loaves, "
                "brioche and laminated pastries that land on the counter by "
                "opening time. The grab-and-go counter runs every day from "
                "8 a.m. to 4 p.m., turning out espresso drinks alongside "
                "the day's bake. It is a working production space as much "
                "as a cafe, which gives it an energy that a coffee-chain "
                "concession cannot replicate."
            ),
            "known_for": "Hand-shaped sourdough loaves and pastries baked overnight on site",
            "good_for": "Morning coffee and a fresh pastry, bread to take home",
            "source_url": "https://medicinebakery.co.uk/",
            "verified": "2026-06-22",
        },
        {
            "type": "Restaurant",
            "name": "The Bilash",
            "area": "2 Cheapside, city centre",
            "cuisine": "Modern Indian and Bengali fine dining",
            "body": (
                "Sitab Khan opened The Bilash on Cheapside in 1982, and more "
                "than four decades later he still runs the kitchen while his "
                "son Mohammed manages the dining room. The restaurant holds "
                "two AA Rosettes, retained in the 2025 inspection cycle and "
                "confirmed in the AA Restaurant Guide 2026, and has been "
                "listed in the Hardens restaurant guide and the Which? Good "
                "Food Guide over the years. The cooking draws on Bengali and "
                "North Indian technique, with signature dishes including "
                "the lamb rogan josh, the house Bilash Super curry, and "
                "a range of carefully spiced tandoori preparations. The "
                "restaurant relaunched its lunchtime service in May 2025 "
                "after a five-year hiatus, with a lighter midday menu "
                "running alongside the full evening carte."
            ),
            "known_for": "Two AA Rosettes, family-run Bengali fine dining since 1982",
            "good_for": "A special-occasion dinner, the best Indian cooking in the city",
            "source_url": "https://www.tripadvisor.co.uk/Restaurant_Review-g190762-d698162-Reviews-Bilash-Wolverhampton_West_Midlands_England.html",
            "verified": "2026-06-22",
        },
        {
            "type": "Pub",
            "name": "The Great Western",
            "area": "Corn Hill, near the railway station",
            "cuisine": "Holden's cask ales, cobs and pork pies",
            "body": (
                "Tucked under the railway arches at the far end of Corn Hill, "
                "the Great Western is one of the finest real-ale pubs in the "
                "West Midlands by any measure. The Grade II-listed Victorian "
                "building became part of Holden's Brewery in 1987 and won "
                "CAMRA National Pub of the Year in 1991. The interior divides "
                "into four areas - a front bar, long lounge, snug and a "
                "conservatory extension - lined with railway memorabilia and "
                "Wolves FC photographs, warmed in winter by open fires. Five "
                "regular Holden's cask ales plus two rotating guests are "
                "always on; the pub featured in CAMRA's Good Beer Guide 2026 "
                "and marked the Wolverhampton branch's 50th anniversary with "
                "a special Holden's mild in the same year. Simple food - "
                "cobs, pork pies - is served at lunchtimes."
            ),
            "known_for": "Five Holden's cask ales, Grade II Victorian railway pub, CAMRA National Pub of Year 1991",
            "good_for": "A serious pint of real ale, heritage pub interior, pre-match",
            "source_url": "https://camra.org.uk/pubs/great-western-wolverhampton-127008",
            "verified": "2026-06-22",
        },
    ],
    "food_scene": [
        (
            "Wolverhampton's food map has always been shaped by the Black Country "
            "industrial tradition and the waves of South Asian settlement that "
            "followed it. The city has a strong concentration of independent "
            "Indian and Bengali restaurants, with The Bilash on Cheapside at "
            "the top of the fine-dining tier and a cluster of balti houses and "
            "curry houses spread across the suburbs. Faggots and peas - the "
            "Black Country's own dish, meatballs of pork offal baked in gravy "
            "and served with mushy peas - remain a fixture on traditional menus."
        ),
        (
            "The city centre and Chapel Ash corridor hold most of the independent "
            "cafes and bistros, including the artisan production bakery of Medicine "
            "in the converted Chubb Building on Fryer Street. The Grand Theatre "
            "and Wolverhampton Art Gallery draw pre- and post-show trade to the "
            "Lichfield Street area, where The Posada - a CAMRA-listed Victorian "
            "pub with some of the rarest surviving snob screens in the country - "
            "anchors the heritage pub circuit."
        ),
        (
            "Away from the centre, Finchfield and Penn to the west have a quiet "
            "concentration of independent chip shops and neighbourhood restaurants, "
            "while Tettenhall offers a more suburban dining scene. The railway "
            "station end of town, down Corn Hill, is Great Western country: a "
            "tucked-away Holden's pub that rewards anyone who takes the five-minute "
            "walk from the platforms."
        ),
    ],
    "visit": [
        (
            "The Bilash, Medicine Bakery and The Great Western form a tight triangle "
            "around the city centre: Cheapside, Fryer Street and Corn Hill are all "
            "within ten minutes on foot of each other and of Wolverhampton railway "
            "station. The Metro tram and main bus stops at the city centre serve "
            "the same hub, making it easy to move between venues without a car."
        ),
        (
            "Seagull Fish Bar sits about two miles west in the Finchfield area, "
            "a short taxi or bus ride on the Penn Road corridor. A practical "
            "Wolverhampton day might run: a morning pastry at Medicine, lunch or "
            "an afternoon pint at The Great Western, an early-evening chippy run "
            "to Seagull, and a special-occasion dinner booking at The Bilash "
            "secured well in advance."
        ),
    ],
    "checklist": [
        "Pick up a sourdough loaf or pastry from Medicine Bakery in the Chubb Building",
        "Walk five minutes to Corn Hill and try a Holden's pint at the Great Western",
        "Book The Bilash for dinner - the two-AA-Rosette Bengali cooking needs advance planning",
        "Head to Finchfield for a fish supper at Seagull Fish Bar on a weekday evening",
        "Catch the Metro or walk - the city centre venues are all within ten minutes of the station",
    ],
    "what_to_order": (
        "Order with focus. At Seagull Fish Bar, cod or haddock in the homemade batter "
        "with proper chips and their own mushy peas - keep it simple. At Medicine "
        "Bakery, whichever sourdough loaf is freshest that morning plus a laminated "
        "pastry to eat in. At The Bilash, the lamb rogan josh is a reliable signature, "
        "the Bilash Super is the house special worth trying, and the tandoori dishes "
        "show the kitchen's range - the lunchtime menu is a lower-stakes way to "
        "explore. At The Great Western, a pint of Holden's Golden Glow or Black "
        "Country Mild, with a cob if you are hungry."
    ),
    "glance": [
        ("Best for a quick bite", "Seagull Fish Bar, for fresh Black Country chippy fish in homemade batter"),
        ("Best for an occasion", "The Bilash, for two-AA-Rosette Bengali fine dining on Cheapside"),
        ("Best for atmosphere", "The Great Western's Victorian railway-pub interior under Corn Hill arches"),
    ],
    "faq": [
        (
            "What is the best restaurant in Wolverhampton?",
            "The Bilash at 2 Cheapside is the city's most decorated independent "
            "restaurant: a family-run Bengali and Indian fine-dining room open since "
            "1982, holding two AA Rosettes (retained in the 2025 inspection cycle and "
            "listed in the AA Restaurant Guide 2026). Book ahead for the evening; the "
            "lunchtime menu relaunched in May 2025 is a more accessible entry point.",
        ),
        (
            "Does Wolverhampton have any award-winning pubs?",
            "Yes. The Great Western on Corn Hill, a Holden's-tied Grade II Victorian "
            "pub near the railway station, won CAMRA National Pub of the Year in 1991 "
            "and has featured in the CAMRA Good Beer Guide for many years, including "
            "the 2026 edition. The Posada on Lichfield Street, a CAMRA National "
            "Inventory Grade II* listed pub built in 1886, is another heritage standout.",
        ),
        (
            "Where can I get a good coffee in Wolverhampton city centre?",
            "Medicine Bakery at the Chubb Building on Fryer Street is Wolverhampton's "
            "most distinctive independent cafe-bakery, serving espresso drinks alongside "
            "sourdough bread and pastries baked on site overnight, open every day "
            "from 8 a.m.",
        ),
        (
            "What is the local food of Wolverhampton and the Black Country?",
            "Faggots and peas is the Black Country signature: pork offal meatballs "
            "baked in gravy and served with mushy peas, a working-class staple that "
            "survived well past the end of the ironworks era. Grey peas (locally called "
            "pays) and bacon is another traditional dish; pork scratchings are the "
            "classic bar snack. The fish and chip shop remains central to the local "
            "eating tradition.",
        ),
        (
            "Is The Bilash still in the Michelin Guide?",
            "The Bilash was listed in the Michelin Guide from 2001 until 2022. It "
            "subsequently retained two AA Rosettes, which were confirmed in the October "
            "2025 inspection cycle and in the AA Restaurant Guide 2026, making it still "
            "one of the most formally recognised independent restaurants in the city.",
        ),
        (
            "How do I get around the Wolverhampton eating spots on this guide?",
            "The Bilash, Medicine Bakery and The Great Western are all within ten "
            "minutes on foot of Wolverhampton railway station and the city-centre "
            "Metro stop. Seagull Fish Bar is about two miles west in Finchfield "
            "and is easiest reached by taxi or the Penn Road bus services.",
        ),
    ],
}

# swansea ----------------------------------------------------------
TOWNS["swansea"] = {
    "region": "South Wales",
    "population": "245K",
    "nearby": ["Neath", "Llanelli", "Port Talbot"],
    "meta_title": "Best Places to Eat in Swansea: Local Food Guide",
    "meta_description": (
        "Where to eat in Swansea: award-winning fish and chips, a seafront "
        "ice cream cafe, a Michelin-listed Welsh kitchen and a CAMRA brewery "
        "pub. Read the guide."
    ),
    "trust_strip": (
        "From Penclawdd cockles at the market to a Michelin-listed former-dock "
        "kitchen, Swansea has one of the most characterful independent food "
        "scenes in Wales"
    ),
    "snapshot": (
        "For a fast answer: Hiks on Neath Road for Swansea's best-loved "
        "award-winning fish and chips, Verdi's on the Mumbles seafront for "
        "fresh-cream Italian ice cream and views across Swansea Bay, The Shed "
        "at SA1 for Michelin-listed seasonal Welsh cooking from a former St "
        "John head chef, and The Pilot Inn in Mumbles for three-times CAMRA "
        "Pub of the Year ales brewed on site. Four moods, one coastal city."
    ),
    "stats": [
        ("245K", "City population (approx)"),
        ("1849", "Year The Pilot Inn was built"),
        ("Penclawdd", "Source of the Gower estuary cockles sold in the market"),
        ("4", "Hand-picked independents"),
    ],
    "pivot_variant": "coastal",
    "pivot_local_hook": (
        "Swansea's kitchens fry hard and long: the bay's fish and chip "
        "restaurants run fryers through lunch and dinner all week, the "
        "Mumbles seafront trade peaks every summer weekend, and the SA1 "
        "dock-conversion kitchens push a steady load of grease-laden vapour "
        "into their canopies every service."
    ),
    "venues": [
        {
            "type": "Takeaway",
            "name": "Hiks",
            "area": "235-240 Neath Road, Plasmarl",
            "cuisine": "Fish and chips, takeaway and restaurant",
            "body": (
                "Hiks on Neath Road in Plasmarl has grown from a local chippy into "
                "one of the most celebrated fish and chip establishments in Wales. "
                "The business now combines a modern 41-seat restaurant with its "
                "takeaway counter on the same site, drawing a loyal crowd across "
                "the week with generous portions of well-battered fish and properly "
                "cooked chips. It was named Takeaway of the Year at the Food Awards "
                "Wales 2018 and reached the shortlist of the National Fish and Chip "
                "Awards 2019, placing it among the top fish and chip shops in the "
                "country at that time. The menu stays close to the classics: battered "
                "cod and plaice, pies, and homemade sauces, with a grassed area "
                "outside for eating in. For a proper Swansea fish supper, this is "
                "the address."
            ),
            "known_for": "Award-winning fish and chips, named Wales Takeaway of the Year 2018",
            "good_for": "A proper fish supper, eat in or take away, any day of the week",
            "source_url": "https://www.tripadvisor.co.uk/Restaurant_Review-g186466-d4108568-Reviews-Hiks-Swansea_Swansea_County_South_Wales_Wales.html",
            "verified": "2026-06-22",
        },
        {
            "type": "Cafe",
            "name": "Verdi's",
            "area": "Mumbles Road, Mumbles (seafront)",
            "cuisine": "Italian ice cream, coffee, pizza and pasta",
            "body": (
                "Verdi's has anchored the Mumbles seafront for decades as an Italian "
                "family-run cafe, ice cream parlour and licensed restaurant, with "
                "indoor and outdoor seating for up to 400 people, every seat with "
                "panoramic views across Swansea Bay. The draw is the fresh-cream "
                "Italian ice cream: up to 30 flavours are churned daily using local "
                "dairy milk and cream, and all breads, cakes, scones, pastries and "
                "desserts are made in house. The wider menu covers authentic pizza "
                "and pasta alongside coffee, and the place fills steadily from "
                "morning until evening throughout the year, reaching a peak in summer "
                "when Mumbles itself buzzes with day-trippers from the city. It is "
                "open seven days a week and has become as much a part of the Mumbles "
                "identity as the pier itself."
            ),
            "known_for": "Fresh-cream Italian ice cream in up to 30 flavours, with views across Swansea Bay",
            "good_for": "A coffee or ice cream stop on the Mumbles seafront, any day of the year",
            "source_url": "https://www.verdis-cafe.co.uk/",
            "verified": "2026-06-22",
        },
        {
            "type": "Restaurant",
            "name": "The Shed",
            "area": "J Shed Arcade, Kings Road, SA1 Waterfront",
            "cuisine": "Seasonal Welsh, farm-to-table",
            "body": (
                "The Shed opened in February 2024 in a converted Victorian dock "
                "building at the SA1 Waterfront, bringing to Swansea one of the "
                "most pedigreed chefs Wales has produced. Jonathan Woolway, a "
                "native of Gorseinon, spent thirteen years at Fergus Henderson's "
                "St John in London, becoming head chef in 2014 and chef director "
                "in 2021, before returning home to open on his own terms. The "
                "kitchen runs a daily-changing menu built entirely on Welsh and "
                "border produce: Pembrokeshire crab and lobster, Gower asparagus, "
                "new season's lamb, and whatever the farms and coast have at their "
                "seasonal prime. The room is industrial and airy, with exposed "
                "brickwork, riveted metal pillars and a theatrical open kitchen. "
                "The Shed is listed in the current Michelin Guide and has quickly "
                "become Swansea's destination table. Book ahead."
            ),
            "known_for": "Michelin-listed seasonal Welsh cooking by a former St John chef director",
            "good_for": "A serious occasion meal in a converted Victorian dock building at SA1",
            "source_url": "https://guide.michelin.com/en/swansea/swansea/restaurant/the-shed-1211070",
            "verified": "2026-06-22",
        },
        {
            "type": "Pub",
            "name": "The Pilot Inn",
            "area": "726 Mumbles Road, Mumbles",
            "cuisine": "Real ale, craft beer, pub food",
            "body": (
                "Built in 1849 and set next to the coastal path at the foot of "
                "Mumbles, The Pilot Inn has been named Swansea CAMRA Pub of the "
                "Year 2026 -- the third time the honour has gone to this address. "
                "The pub houses its own on-site Pilot Brewery, which began "
                "producing real ales in 2013, and usually keeps three rotating "
                "house beers on alongside four guest ales and a range of bottled "
                "ciders, making seven ales always available at the bar. The "
                "interior is traditional and uncluttered -- dark wood, stone-flagged "
                "floors, no television, no music, no games machines -- a deliberate "
                "commitment to good beer and good conversation. It draws an "
                "eclectic crowd of lifeboatmen, locals, real ale fans, coastal-path "
                "walkers and cyclists, and sits just a short walk from Verdi's on "
                "the seafront. For a proper pint in Mumbles, there is nowhere better."
            ),
            "known_for": "Swansea CAMRA Pub of the Year 2026 (third time), on-site Pilot Brewery since 2013",
            "good_for": "A real ale pint by the coastal path in Mumbles, with no distractions",
            "source_url": "https://camra.org.uk/pubs/pilot-inn-mumbles-183760",
            "verified": "2026-06-22",
        },
    ],
    "food_scene": [
        (
            "Swansea's food story begins at the market. The covered Swansea Market, "
            "the largest indoor market in Wales, has been the city's larder since "
            "the nineteenth century and remains the place to find fresh Penclawdd "
            "cockles -- harvested from the Loughor estuary on the edge of the Gower "
            "Peninsula and sold from stalls that have traded for generations. Cockles "
            "and laverbread, the dark mineral-rich seaweed paste that goes alongside "
            "them, are Swansea on a plate and appear in some form on many of the "
            "city's independent menus."
        ),
        (
            "The Italian connection runs almost as deep. Italian families settled "
            "in Swansea more than a century ago and shaped the city's cafe and ice "
            "cream culture in ways that still persist: Verdi's on the Mumbles "
            "seafront is the best-known example, but the city's taste for quality "
            "ice cream and honest pizza-and-pasta dining goes back that far. The "
            "Mumbles strip -- the Victorian fishing village at the southern end of "
            "Swansea Bay with its pier, independent shops and seafront cafes -- "
            "acts as the city's leisure quarter and the focus of its summer trade."
        ),
        (
            "More recently, the converted dock buildings of the SA1 Waterfront "
            "have become the address for a newer wave of serious, chef-owned "
            "independents. The Shed is the flagship, but the district holds "
            "several strong kitchens alongside the marina. Dylan Thomas, who grew "
            "up in the Uplands district before escaping to London, once called "
            "Swansea an ugly, lovely town; the food scene is proving the second "
            "part right."
        ),
    ],
    "visit": [
        (
            "The city and its best eating are spread across a short stretch of "
            "coast. Hiks sits north of the centre on Neath Road in Plasmarl, "
            "a quick drive or bus ride from the city. The SA1 Waterfront, where "
            "The Shed is located, is a short walk east of the city centre and "
            "within easy reach by foot. Mumbles is three miles south-west of "
            "the city along the bay, reached by bus on the Swansea Bay route "
            "or a cycle path that follows the seafront all the way."
        ),
        (
            "Done as a day, the route flows naturally. A fish and chip lunch "
            "at Hiks, an afternoon at The Shed for a serious meal or a visit "
            "saved for the evening, and then the Mumbles bus for ice cream at "
            "Verdi's and a pint at The Pilot while the tide comes in across "
            "Swansea Bay. Book The Shed well ahead; Verdi's and The Pilot are "
            "walk-in friendly."
        ),
    ],
    "checklist": [
        "Try the cockle stall at Swansea Market before heading anywhere else",
        "Go to Hiks mid-week to avoid the weekend lunchtime queue",
        "Book The Shed at SA1 well in advance -- it fills quickly",
        "Take the seafront bus or cycle path down to Mumbles for ice cream at Verdi's",
        "Finish at The Pilot Inn for on-site brewed real ale by the coastal path",
    ],
    "what_to_order": (
        "Order with intent. At Hiks, a large battered cod with chips and their "
        "homemade tartare sauce, eaten in or taken to the outdoor benches. At "
        "Verdi's, a scoop or two of fresh-cream Italian ice cream -- pick from "
        "whatever the 30-flavour daily rotation has on -- with a coffee alongside. "
        "At The Shed, follow the daily-changing menu wherever the season points: "
        "Pembrokeshire crab when it is running, Gower lamb in spring, and whatever "
        "the open kitchen is making a point of that week. At The Pilot, one of the "
        "rotating house beers brewed on site -- ask what is freshest -- and settle "
        "in with no television to distract you."
    ),
    "glance": [
        ("Best for a quick bite", "Hiks, for award-winning fish and chips on Neath Road"),
        ("Best for an occasion", "The Shed, for Michelin-listed Welsh cooking at SA1"),
        ("Best for atmosphere", "The Pilot Inn, a CAMRA pub of the year with its own brewery in Mumbles"),
    ],
    "faq": [
        (
            "Where can I get the best fish and chips in Swansea?",
            "Hiks at 235-240 Neath Road in Plasmarl is the city's most-awarded "
            "fish and chip operation, named Wales Takeaway of the Year at the "
            "Food Awards Wales 2018 and shortlisted for the National Fish and "
            "Chip Awards 2019. It combines a 41-seat restaurant with the "
            "takeaway counter and is open seven days a week."
        ),
        (
            "What is the food Swansea is most famous for?",
            "Cockles and laverbread -- the combination of Penclawdd cockles from "
            "the Loughor estuary on the edge of the Gower Peninsula and dark, "
            "mineral-rich cooked seaweed paste -- is the city's signature dish. "
            "Both are sold fresh at Swansea Market, the largest indoor market in "
            "Wales, and appear on many local menus."
        ),
        (
            "Does Swansea have a Michelin Guide restaurant?",
            "Yes. The Shed at the SA1 Waterfront, opened in February 2024 by "
            "Jonathan Woolway -- formerly chef director at St John in London -- "
            "is listed in the current Michelin Guide. It serves a daily-changing "
            "menu built on Welsh and border produce in a converted Victorian dock "
            "building. Book well in advance."
        ),
        (
            "Which pub in Swansea has the best real ale?",
            "The Pilot Inn at 726 Mumbles Road in Mumbles has been named Swansea "
            "CAMRA Pub of the Year 2026 -- the third time the award has gone there. "
            "It has its own on-site Pilot Brewery, which has been brewing since "
            "2013, and keeps seven ales on the bar at any one time, with no "
            "television or music to distract from the beer."
        ),
        (
            "Is Verdi's in Mumbles worth visiting?",
            "Verdi's is a Swansea institution: a family-run Italian ice cream "
            "parlour, cafe and restaurant on the Mumbles seafront producing up "
            "to 30 flavours of fresh-cream ice cream daily from local dairy "
            "milk, with panoramic views across Swansea Bay. It is open seven "
            "days a week year-round and seats up to 400."
        ),
        (
            "Can I do a Swansea food day without a car?",
            "Largely yes. Hiks on Neath Road is served by city buses from the "
            "centre, The Shed at SA1 is walkable from the city centre, and "
            "Mumbles -- for Verdi's and The Pilot -- is three miles south-west "
            "along the bay, reached by frequent bus or a flat cycle path that "
            "runs along the seafront the whole way."
        ),
    ],
}

# milton-keynes ----------------------------------------------------------
TOWNS["milton keynes"] = {
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

# aberdeen ----------------------------------------------------------
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

# reading ----------------------------------------------------------
TOWNS["reading"] = {
    "region": "Berkshire",
    "population": "220K",
    "nearby": ["Wokingham", "Maidenhead", "Bracknell"],
    "meta_title": "Best Places to Eat in Reading: Local Food Guide",
    "meta_description": (
        "Where to eat in Reading: pan-Asian plates, a sourdough forge cafe, "
        "a Kennet riverside brasserie and a CAMRA free house. Read the guide."
    ),
    "trust_strip": (
        "From a riverside brasserie that opened the year the Oracle launched "
        "to a CAMRA-celebrated free house on Russell Street, Reading punches "
        "well above its size for independent eating"
    ),
    "snapshot": (
        "For a fast answer: Coconut Bar and Kitchen on St Mary's Butts for "
        "pan-Asian plates and katsu curry at any hour, Shed at the Old Forge "
        "for proper sourdough and handmade sandwiches, London Street Brasserie "
        "for riverside modern-British dining since 2000, and the Nag's Head on "
        "Russell Street for 12 changing real ales and CAMRA's seal of approval. "
        "Four moods, one compact Berkshire town."
    ),
    "stats": [
        ("220K", "Population (approx)"),
        ("2000", "Year London Street Brasserie opened beside the Kennet"),
        ("12", "Changing real ales on the Nag's Head handpumps"),
        ("4", "Hand-picked independents"),
    ],
    "pivot_variant": "high-volume",
    "pivot_local_hook": (
        "Reading's kitchens run long hours: the Oracle Riverside bars and "
        "restaurants turn over multiple services a day, the Oxford Road "
        "curry houses run late-night fryers every evening, and the town's "
        "pan-Asian and brasserie kitchens throw a sustained grease-laden "
        "vapour load into their canopies from lunchtime through last orders."
    ),
    "venues": [
        {
            "type": "Casual",
            "name": "Coconut Bar and Kitchen",
            "area": "St Mary's Butts, town centre",
            "cuisine": "Pan-Asian — Japanese, Korean, Malaysian, Thai",
            "body": (
                "Opened in 2014 on St Mary's Butts, directly opposite the Broad "
                "Street Mall and a five-minute walk from the station, Coconut Bar "
                "and Kitchen draws on half a dozen Asian food traditions without "
                "muddying any of them. The setting is industrial chic — galvanised "
                "metal, exposed pipework, bare-filament bulbs — and the menu "
                "ranges from Japanese katsu curry and Korean bibimbap to Malaysian "
                "rice noodles and Thai chicken wings, with everything cooked fresh. "
                "The chicken katsu with gyudon sauce and shiitake mushrooms on "
                "Japanese rice is the dish most tables order. Bookings are taken "
                "and it opens seven days; the bottomless brunch runs Sunday to "
                "Friday for those who want prosecco with their prawn katsu."
            ),
            "known_for": "Japanese katsu curry, Korean bibimbap and a long pan-Asian menu",
            "good_for": "Casual weekday lunch or a lively evening with a crowd",
            "source_url": "https://www.coconutbarkitchen.co.uk/",
            "verified": "2026-06-22",
        },
        {
            "type": "Cafe",
            "name": "Shed",
            "area": "Merchants Place (The Old Forge), town centre",
            "cuisine": "Handmade sandwiches, sourdough, soup, coffee",
            "body": (
                "Shed started making sandwiches in the summer of 2012 and has "
                "grown quietly into one of Reading's most-recommended lunch stops. "
                "It occupies an old forge in Merchants Place, and the exposed "
                "brick and low ceilings give it exactly the atmosphere the name "
                "suggests. Everything is made in-house and in small batches: "
                "doorstop sourdough sandwiches, stuffed wraps, hearty salad boxes "
                "and home-baked cakes, alongside Italian coffee and quality "
                "loose-leaf teas. They buy local wherever they can and cook what "
                "they cook well rather than expanding the range endlessly. Open "
                "Monday to Friday from 8am and Saturday from 10am, food until "
                "3pm — ideal for a properly assembled lunch rather than a "
                "counter grab."
            ),
            "known_for": "Sourdough toasties, doorstop sandwiches and home-baked cakes in an old forge",
            "good_for": "A proper sit-down lunch in the town centre",
            "source_url": "https://theshedcafe.co.uk/",
            "verified": "2026-06-22",
        },
        {
            "type": "Restaurant",
            "name": "London Street Brasserie",
            "area": "2-4 London Street, beside the Kennet",
            "cuisine": "Modern British brasserie",
            "body": (
                "London Street Brasserie opened in 2000 in a Grade II-listed toll "
                "house built in 1750 on Duke Street bridge, literally cantilevered "
                "out over the River Kennet. Chef-proprietor Paul Clerehugh has "
                "made it Reading's most celebrated independent restaurant: Michelin "
                "recognition, regular best-of listings, and 918 OpenTable reviews "
                "averaging 4.7 stars underline two decades of consistent cooking. "
                "The menu is modern British with a brasserie tempo — good "
                "ingredients, clean flavours, no fuss — served across two rooms "
                "and a small riverside terrace. The set lunch menu (noon to 6pm) "
                "is well-priced for the quality; Sunday lunch fills early. Book "
                "ahead at weekends, especially for the Kennet-facing terrace seats."
            ),
            "known_for": "Two decades of modern-British brasserie cooking beside the Kennet, Michelin-noted",
            "good_for": "A proper occasion meal or a long riverside Sunday lunch",
            "source_url": "https://www.londonstreetbrasserie.co.uk/",
            "verified": "2026-06-22",
        },
        {
            "type": "Pub",
            "name": "The Nag's Head",
            "area": "5 Russell Street, near the station",
            "cuisine": "Real ale and craft cider free house",
            "body": (
                "The Nag's Head on Russell Street is Reading's most-decorated "
                "ale pub: a multiple winner of Reading and Mid-Berkshire CAMRA "
                "Pub of the Year and a recurrent entry in the Good Beer Guide, "
                "the pub has 12 constantly rotating real ales on handpump, a "
                "14-tap craft keg wall and 13 ciders and perries, with the "
                "blackboard noting vessel type and dispense method beside each. "
                "The selection tilts toward local and independent breweries, and "
                "the stock turns fast enough that every visit brings something "
                "different. There is a covered garden for warmer months, board "
                "games on the shelves, and basic hot food to line the stomach. "
                "It is a genuine free house — no tie, no corporate landlord — "
                "and five minutes from the station, which means it is usually "
                "the first stop recommended to anyone arriving in Reading by train."
            ),
            "known_for": "12 rotating real ales, 13 ciders, multiple CAMRA Pub of the Year wins",
            "good_for": "Serious ale and cider drinking close to the station",
            "source_url": "https://camra.org.uk/pubs/nags-head-reading-155710",
            "verified": "2026-06-22",
        },
    ],
    "food_scene": [
        (
            "Reading's food geography divides into three zones. The town centre "
            "clusters around the Oracle shopping complex and its riverside strip "
            "on the Kennet and Avon Canal — a run of bars and restaurants that "
            "fills at lunchtime and again from early evening. London Street and "
            "the waterfront give it the most characterful setting, with the canal "
            "running underneath the oldest buildings. Friar Street and Gun Street "
            "hold the independent bars and late-night venues."
        ),
        (
            "The Oxford Road corridor, running south-west from the centre, is "
            "where Reading's South Asian and global food traditions are strongest. "
            "Curry houses, Bangladeshi restaurants and international kitchens line "
            "the road, and it is busy most evenings. St Mary's Butts and the "
            "surrounding streets form a compact eating district between the Oracle "
            "and the station, with the pan-Asian and casual options. Caversham, "
            "just north across the Thames, has a quieter village-scale food scene "
            "of its own."
        ),
        (
            "Reading does not have one signature dish in the way that Birmingham "
            "has the balti, but its food market — held on the first and third "
            "Saturday of each month at the old cattle market on Great Knollys "
            "Street — gives a good cross-section of what local producers are "
            "growing and making. The town's independent food scene grew notably "
            "across 2024-2025, with more openings than closures and a spread of "
            "kitchens confident enough to specialise rather than try to be "
            "everything to everyone."
        ),
    ],
    "visit": [
        (
            "Shed and Coconut Bar and Kitchen both sit within five minutes of the "
            "station and of each other, making the town centre zone easy on foot. "
            "London Street Brasserie is a short walk east along the Kennet — "
            "follow the riverside path from the Oracle — and the Nag's Head is "
            "a two-minute walk from the station on Russell Street. All four "
            "venues are reachable without a car from Reading railway station, "
            "which sits on the Great Western Main Line with fast links from "
            "London Paddington (25 minutes), Bristol and Oxford."
        ),
        (
            "The Oracle Riverside is the obvious landmark to navigate from — "
            "the Kennet runs underneath the shopping centre and the riverside "
            "walkway connects the Oracle to London Street. Time a visit around "
            "Shed's Monday-to-Friday hours if a daytime sandwich stop is on the "
            "plan; London Street Brasserie's set lunch menu runs noon to 6pm "
            "and is the best-value entry point to the riverside brasserie. "
            "The Nag's Head is the natural finishing point for the evening."
        ),
    ],
    "checklist": [
        "Chicken katsu with gyudon sauce at Coconut Bar and Kitchen",
        "A sourdough doorstop sandwich at Shed in the old forge on Merchants Place",
        "The set lunch menu at London Street Brasserie on the Kennet terrace",
        "A pint of whatever is freshest on the Nag's Head handpumps",
        "The farmers' market on Great Knollys Street (first and third Saturday, 8:15am-noon)",
    ],
    "what_to_order": (
        "Start with the chicken katsu at Coconut for a feel of the town's "
        "pan-Asian range, work through a sourdough lunch at Shed, take the "
        "set lunch at London Street Brasserie for the riverside setting and "
        "modern-British cooking at a sensible price, and end the day at the "
        "Nag's Head with a half of whatever the chalk board says was just "
        "tapped — the rotating cask list is the whole point."
    ),
    "glance": [
        ("Best for a quick bite", "Shed — sourdough sandwiches made to order in an old forge, weekdays only"),
        ("Best for an occasion", "London Street Brasserie — 25 years beside the Kennet, Michelin-noted"),
        ("Best for atmosphere", "The Nag's Head — a free house, 12 handpumps and the town's best ale selection"),
    ],
    "faq": [
        (
            "What is the best independent restaurant in Reading?",
            "London Street Brasserie on London Street has been Reading's most "
            "consistently celebrated independent since it opened in 2000 in a "
            "Grade II-listed toll house beside the River Kennet. Chef-proprietor "
            "Paul Clerehugh has held Michelin recognition and a loyal local "
            "following for over two decades. Book ahead for weekends."
        ),
        (
            "Where should I eat near Reading station?",
            "The Nag's Head on Russell Street is a two-minute walk from the "
            "main entrance and is Reading's top-rated real-ale pub, with 12 "
            "rotating cask ales and 13 ciders. For food, Coconut Bar and "
            "Kitchen on St Mary's Butts is a five-minute walk and open seven days."
        ),
        (
            "Is there a good food market in Reading?",
            "Yes — the farmers' market at the old cattle market on Great Knollys "
            "Street runs on the first and third Saturday of each month from "
            "8:15am to noon. It focuses on local producers from Berkshire and "
            "the surrounding counties selling direct."
        ),
        (
            "Where is the best place to eat on the Oxford Road in Reading?",
            "The Oxford Road corridor is Reading's South Asian and global food "
            "street, with curry houses and Bangladeshi restaurants busy most "
            "evenings. For a step up, London Street Brasserie beside the Kennet "
            "is the more formal option nearby; Coconut Bar and Kitchen handles "
            "the pan-Asian brief in the town centre."
        ),
        (
            "What is Shed cafe in Reading known for?",
            "Shed at 8 Merchants Place has been making handmade sandwiches and "
            "sourdough toasties since 2012 in an old forge with exposed brick. "
            "It is open Monday to Friday from 8am and Saturday from 10am, "
            "with food until 3pm — a daytime-only cafe with a strong local following."
        ),
        (
            "Does Reading have any Michelin-starred restaurants?",
            "Reading does not currently have any Michelin-starred restaurants, "
            "but London Street Brasserie has held Michelin recognition across "
            "its 25-year history and is the town's most-awarded independent "
            "dining room. For a Michelin star in the wider region, nearby "
            "Bray holds several in a small village within 20 minutes."
        ),
    ],
}

# northampton ----------------------------------------------------------
TOWNS["northampton"] = {
    "region": "the East Midlands",
    "population": "215,000",
    "nearby": ["Wellingborough", "Kettering", "Rushden"],
    "meta_title": "Best Places to Eat in Northampton: Local Food Guide",
    "meta_description": (
        "Where to eat in Northampton: wood-fired Neapolitan pizza, a roastery cafe, "
        "authentic Greek from the Peloponnese and a real-ale institution. "
        "Read the guide."
    ),
    "trust_strip": (
        "From a sourdough bakery in the old Boot and Shoe Quarter to a multiple "
        "CAMRA award-winner, Northampton's independent food scene punches well above its size"
    ),
    "snapshot": (
        "For a fast answer: Pala at Derngate for wood-fired Neapolitan pizza and "
        "cicchetti in the Cultural Quarter, The Good Loaf on Overstone Road for "
        "hand-crafted sourdough and locally roasted coffee in a converted shoe factory, "
        "Maniatiko on Wellingborough Road for authentic Peloponnese cooking, and "
        "the Malt Shovel Tavern on Bridge Street for eight real ales in a former "
        "brewery tap with a Northamptonshire CAMRA Pub of the Year pedigree. "
        "Four moods, one compact market town."
    ),
    "stats": [
        ("215,000", "Population (approx)"),
        ("1086", "Year Northampton Market Square was first recorded"),
        ("Boot and Shoe Quarter", "Northampton's Victorian industrial heartland"),
        ("4", "Hand-picked independents"),
    ],
    "pivot_variant": "market-town",
    "pivot_local_hook": (
        "Northampton's kitchens range from the wood-fired pizza deck at Pala "
        "to the high-volume fry stations of the Wellingborough Road dining strip, "
        "and every one of them loads its canopy with grease-laden vapour across "
        "every lunch and dinner service."
    ),
    "venues": [
        {
            "type": "Casual",
            "name": "Pala",
            "area": "7 Derngate, Cultural Quarter",
            "cuisine": "Neapolitan pizza, cicchetti, cocktails",
            "body": (
                "Pala opened in August 2023 as a collaboration between two well-loved "
                "Northampton independents: Santina's Woodfired Pizza Co. and Saints Coffee. "
                "The result is a lively Cultural Quarter room at 7 Derngate serving "
                "proper Neapolitan pizzas from a wood-fired deck alongside small plates "
                "in the Italian cicchetti tradition — arancini, burrata, charcuterie — "
                "and a strong cocktail list. The sourdough bases are charred and blistered "
                "in the Neapolitan way, and the kitchen keeps seasonal toppings coming. "
                "Rated 4.7 out of 5 from nearly 450 reviews and ranked among Northampton's "
                "most talked-about tables within its first year of opening. Open from noon "
                "daily; booking recommended for evenings."
            ),
            "known_for": "Wood-fired Neapolitan pizza and cicchetti in the Cultural Quarter",
            "good_for": "A relaxed evening of pizza and cocktails near the Derngate theatre",
            "source_url": "https://www.tripadvisor.co.uk/Restaurant_Review-g186349-d26787728-Reviews-Pala-Northampton_Northamptonshire_England.html",
            "verified": "2026-06-22",
        },
        {
            "type": "Cafe",
            "name": "The Good Loaf",
            "area": "1-9 Overstone Road, Boot and Shoe Quarter",
            "cuisine": "Artisan sourdough bakery, cafe, locally roasted coffee",
            "body": (
                "The Good Loaf occupies the first floor of a former shoe factory at "
                "the corner of Overstone Road and Clare Street, right in Northampton's "
                "Victorian Boot and Shoe Quarter conservation area. Founded as a social "
                "enterprise — its team blends experienced staff with women on paid work "
                "experience programmes — it hand-crafts its sourdough breads daily at "
                "sunrise, sourcing flour from local mills and coffee from local roasters. "
                "The bakery has won a devoted following for its Marmite and cheese loaves, "
                "homemade cakes, and reliably good lattes. It is listed in the Great Food "
                "Club's independent food guide and holds a 4.7 Google rating across "
                "hundreds of reviews. Open Monday to Saturday from 8:30am."
            ),
            "known_for": "Hand-crafted sourdough baked at sunrise in a converted shoe factory",
            "good_for": "A morning coffee and a proper artisan loaf to take home",
            "source_url": "https://thegoodloaf.co.uk/",
            "verified": "2026-06-22",
        },
        {
            "type": "Restaurant",
            "name": "Maniatiko",
            "area": "157-159a Wellingborough Road, Abington",
            "cuisine": "Traditional Greek, Peloponnese region",
            "body": (
                "Opened in May 2025 by siblings Renato and Stelina Kishta, Maniatiko "
                "takes its name from the family village in the Mani peninsula of the "
                "Peloponnese, known for its olive groves and fierce local traditions. "
                "The kitchen cooks accordingly: slow-roasted lamb, grilled octopus, "
                "moussaka, generous sharing dips (tzatziki, spicy whipped feta), "
                "calamari and halloumi from fresh-sourced ingredients — the food of "
                "southern Greece rather than the generic Greek-restaurant template. "
                "It has been described as a hidden treasure and reached a TripAdvisor "
                "ranking of 130 out of 580 Northampton restaurants within months of "
                "opening. Rated 9.5 out of 10 on TheFork. Open Tuesday to Sunday."
            ),
            "known_for": "Authentic Peloponnese cooking from a family-run Greek kitchen",
            "good_for": "A generous shared Greek feast in a calm, stylish room",
            "source_url": "https://maniatikorestaurant.com/",
            "verified": "2026-06-22",
        },
        {
            "type": "Pub",
            "name": "The Malt Shovel Tavern",
            "area": "121 Bridge Street, town centre",
            "cuisine": "Real ales, real ciders, Belgian beers, bar snacks",
            "body": (
                "The Malt Shovel Tavern occupies the former tap of the Northampton "
                "Brewery Company (NBC) and still faces the modern Carlsberg plant "
                "across Bridge Street, where the old brewery once stood. The NBC "
                "neon star adorns the frontage and a remarkable collection of "
                "breweriana fills the interior. Inside, up to eight rotating real "
                "ales — mostly from local and regional microbreweries — pour alongside "
                "three real ciders and a thoughtful selection of Belgian draught and "
                "bottled beers, with at least one dark ale always on. A multiple winner "
                "of the Northamptonshire CAMRA Pub of the Year and the East Midlands "
                "Regional Pub of the Year award, it hosts a free blues night every "
                "first Wednesday and runs summer and winter beer festivals."
            ),
            "known_for": "Eight rotating real ales in a brewery-heritage tap with a CAMRA pedigree",
            "good_for": "A serious pint of local ale among breweriana and a free blues night",
            "source_url": "https://camra.org.uk/pubs/malt-shovel-tavern-northampton-160658",
            "verified": "2026-06-22",
        },
    ],
    "food_scene": [
        (
            "Northampton's food map is shaped by two Victorian legacies: the great "
            "Market Square, one of the largest in England and in use since the eleventh "
            "century, and the Boot and Shoe Quarter spreading north and east of the centre, "
            "where the town made its name as the capital of the English shoemaking industry. "
            "The old shoe factories have become the most characterful eating addresses in town, "
            "with The Good Loaf baking sourdough in one such converted building on Overstone Road."
        ),
        (
            "The Cultural Quarter around Derngate and Angel Street is where the independent "
            "cafe and restaurant scene has taken firmest root. Yellow Bourbon Coffee Roasters, "
            "founded in 2017 by Steve Peel, roasts on a 2kg shop roaster at 15 Angel Street "
            "in full view of the counter, and Pala has brought a proper wood-fired Neapolitan "
            "pizza operation to the quarter. The Derngate Theatre and the Royal and Derngate "
            "complex draw a reliable evening crowd that keeps the area lively."
        ),
        (
            "Wellingborough Road running east from the town centre is the main dining strip "
            "for neighbourhood restaurants, with cuisines from Greek and Mediterranean to "
            "Turkish and South Asian. Bridge Street and the older inn districts to the south "
            "hold the real-ale pubs, with the Malt Shovel Tavern as the standard-bearer of "
            "a brewing tradition that goes back to the NBC brewery on the same street."
        ),
    ],
    "visit": [
        (
            "The town centre is compact and walkable. The Cultural Quarter venues — Pala "
            "at Derngate and Yellow Bourbon on Angel Street — are a few minutes apart on "
            "foot, and The Good Loaf in the Boot and Shoe Quarter is a ten-minute walk "
            "northeast. Bridge Street and the Malt Shovel Tavern lie south of the Market "
            "Square, a short stroll from the train station."
        ),
        (
            "Time it well and the day writes itself: a morning coffee and sourdough at "
            "The Good Loaf, a wood-fired pizza lunch at Pala, an evening of Peloponnese "
            "lamb and sharing plates at Maniatiko, and a nightcap pint of rotating "
            "microbrewery ale at the Malt Shovel Tavern. Northampton station has direct "
            "trains to London Euston in under an hour."
        ),
    ],
    "checklist": [
        "Start the morning at The Good Loaf in the Boot and Shoe Quarter for sourdough and a latte",
        "Book Pala for lunch or an early evening; tables fill quickly at weekends",
        "Walk the Market Square and the Victorian shoe-factory streets of Overstone Road",
        "Book Maniatiko on Wellingborough Road for a leisurely shared Greek dinner",
        "End at the Malt Shovel Tavern on Bridge Street for a rotating real ale from the pump",
    ],
    "what_to_order": (
        "Order with intent. At Pala, a wood-fired Neapolitan pizza with a blistered "
        "sourdough base, plus a plate of cicchetti to share at the start. At The Good Loaf, "
        "the Marmite and cheese sourdough loaf and whichever single-origin coffee is on the "
        "bar that morning. At Maniatiko, the grilled octopus and the slow-roasted lamb, with "
        "a tzatziki and spicy whipped feta to dip into first. At the Malt Shovel Tavern, "
        "ask what is fresh on the local microbrewery tap, and check the chalkboard for a "
        "dark ale — they keep at least one on at all times."
    ),
    "glance": [
        ("Best for a quick bite", "Pala, for a wood-fired Neapolitan pizza in the Cultural Quarter"),
        ("Best for an occasion", "Maniatiko, for a generous shared Greek feast from the Peloponnese"),
        ("Best for atmosphere", "The Malt Shovel Tavern's breweriana-filled former NBC brewery tap"),
    ],
    "faq": [
        (
            "Where can I eat the best pizza in Northampton?",
            "Pala at 7 Derngate in the Cultural Quarter opened in August 2023 and has "
            "quickly become the go-to for wood-fired Neapolitan pizza in town. The bases "
            "are charred and blistered in the traditional Neapolitan way, and the menu "
            "adds Italian cicchetti small plates and cocktails alongside."
        ),
        (
            "Which Northampton pub is best for real ale?",
            "The Malt Shovel Tavern on Bridge Street is the town's premier real-ale "
            "destination, a former Northampton Brewery Company tap that pours up to eight "
            "rotating ales from local and regional microbreweries, plus three real ciders "
            "and Belgian beers. It is a multiple Northamptonshire CAMRA Pub of the Year winner."
        ),
        (
            "Where can I get artisan bread and good coffee in Northampton?",
            "The Good Loaf on Overstone Road, in the heart of the Victorian Boot and Shoe "
            "Quarter, hand-crafts sourdough breads from locally milled flour every morning "
            "and serves award-winning locally roasted coffee. It is a social enterprise and "
            "is open Monday to Saturday from 8:30am."
        ),
        (
            "Is there a good Greek restaurant in Northampton?",
            "Maniatiko at 157-159a Wellingborough Road opened in May 2025 and is run by "
            "siblings from a village in the Mani peninsula of the Peloponnese. It cooks "
            "authentic southern Greek food including slow-roasted lamb, grilled octopus "
            "and generous sharing dips. It is rated 9.5 out of 10 on TheFork."
        ),
        (
            "What is Northampton famous for in terms of food?",
            "Northampton is primarily famous for its shoemaking heritage rather than a "
            "single dish, but the Boot and Shoe Quarter and the large Market Square "
            "have shaped its eating culture. The town has a strong independent cafe scene "
            "in the Cultural Quarter and a robust real-ale pub tradition dating to the "
            "Northampton Brewery Company era."
        ),
        (
            "Can you do a Northampton food day on foot and public transport?",
            "Easily. The Cultural Quarter, Market Square, Boot and Shoe Quarter and Bridge "
            "Street are all within comfortable walking distance of each other and of "
            "Northampton train station, which has direct services to London Euston in "
            "under an hour and good connections to Birmingham and the East Midlands."
        ),
    ],
}

# luton ----------------------------------------------------------
TOWNS["luton"] = {
    "region": "Bedfordshire",
    "population": "215,000",
    "nearby": ["Dunstable", "St Albans", "Stevenage"],
    "meta_title": "Best Places to Eat in Luton: Local Food Guide",
    "meta_description": (
        "Where to eat in Luton: authentic Pakistani karahi in Bury Park, a Portuguese "
        "family cafe, long-running Thai and a Grade II heritage pub. Read the guide."
    ),
    "trust_strip": (
        "From the South Asian kitchens of Bury Park to a Victorian pub on CAMRA's "
        "National Heritage list, Luton's independent food scene is more layered than "
        "most visitors expect"
    ),
    "snapshot": (
        "For a fast answer: A1 Lahori Zaiqa on Dunstable Road for chicken karahi and "
        "halwa puri in the heart of Bury Park, Cafe Lagoa on High Town Road for "
        "pasteis de nata and Brazilian-roasted coffee at a family Portuguese counter, "
        "Nakorn Thai on Wellington Street for nearly two decades of owner-cooked Thai "
        "in a calm side-street room, and The Great Northern on Bute Street for a pint "
        "of St Austell Tribute inside one of the most intact Victorian pub interiors in "
        "England. Four moods, one town with more going on than the airport strip suggests."
    ),
    "stats": [
        ("215,000", "Population (approx)"),
        ("Bury Park", "Luton's South Asian food quarter"),
        ("Grade II", "Listed heritage status of The Great Northern pub"),
        ("4", "Hand-picked independents"),
    ],
    "pivot_variant": "high-volume",
    "pivot_local_hook": (
        "Luton's kitchens run long and hot: the karahi houses and grill restaurants "
        "of Bury Park cook over fierce heat through lunch and well into the night, "
        "generating a sustained load of grease-laden vapour that demands properly "
        "maintained extraction canopies to stay within TR19 compliance and fire-safety law."
    ),
    "venues": [
        {
            "type": "Takeaway/Casual",
            "name": "A1 Lahori Zaiqa",
            "area": "130 Dunstable Road, Bury Park",
            "cuisine": "Pakistani, halal",
            "body": (
                "Bury Park is the neighbourhood that defines Luton's food identity, and "
                "Dunstable Road is its busiest eating street. A1 Lahori Zaiqa, which has "
                "been serving the community since its incorporation in 2017, is a "
                "Pakistani halal restaurant and takeaway that does the classics properly: "
                "chicken karahi cooked in the wok over high heat, mutton nehari slow-braised "
                "overnight, halwa puri for breakfast and brunch, and chapli kebabs from the "
                "grill. The room is straightforward and the portions are generous; staff "
                "switch between English, Urdu and Punjabi without breaking stride. It is "
                "open from 10 in the morning until midnight on weekdays and from nine at "
                "weekends, which covers most moods. Order the karahi and a tandoori naan "
                "and eat it there -- the difference between fresh-off-the-flame and a "
                "delivery box is significant."
            ),
            "known_for": "Chicken karahi, mutton nehari and halwa puri in the heart of Bury Park",
            "good_for": "A proper Pakistani feed any time from brunch to late evening",
            "source_url": "https://a1-lahori-zaiqa.wheree.com/",
            "verified": "2026-06-22",
        },
        {
            "type": "Cafe",
            "name": "Cafe Lagoa",
            "area": "17 High Town Road, High Town",
            "cuisine": "Portuguese patisserie and coffee",
            "body": (
                "High Town Road sits five minutes' walk from Luton station, and Cafe Lagoa "
                "has made it a destination in its own right. Owners Bruna and Luciano named "
                "the cafe after Alvor Lagoon in the Algarve, and they have brought a genuine "
                "slice of Portugal to High Town: pasteis de nata baked fresh and priced at "
                "under two pounds, bolinhas (Portuguese doughnuts) filled with strawberry "
                "jam or egg custard, and salted cod croquettes for something savoury. Coffee "
                "is made with Brazilian beans roasted in Portugal, pulled through a Cimbali "
                "machine. The room is small and warmly decorated with pictures of Portugal; "
                "there is outdoor seating when the weather cooperates. Open seven days a "
                "week, including early on weekday mornings, it is the kind of neighbourhood "
                "cafe that every town should have but few do."
            ),
            "known_for": "Pasteis de nata, Portuguese doughnuts and Brazilian-roasted coffee",
            "good_for": "A relaxed morning break or an afternoon stop with good pastry",
            "source_url": "https://www.cafelagoa.com/",
            "verified": "2026-06-22",
        },
        {
            "type": "Restaurant",
            "name": "Nakorn Thai",
            "area": "45 Wellington Street, town centre",
            "cuisine": "Authentic Thai",
            "body": (
                "Nakorn Thai opened in 2005 on Wellington Street, a short walk from Luton "
                "town centre, and has held its place as the town's most-trusted restaurant "
                "for close to two decades. It is run by a Thai owner and her English husband "
                "with a team of Thai staff, and the food is cooked to the flavour balance of "
                "the country rather than the mild-and-sweet version common in British high "
                "streets. Aromatic curries, proper fish cakes, tom yum with genuine heat, "
                "and a pad thai that arrives tasting of wok-char rather than sweet ketchup "
                "are the draws. The room is calm and softly lit, the service attentive. "
                "Rated 4.5 on TripAdvisor from over 550 reviews and ranked among the top "
                "four restaurants in Luton, it is the obvious choice when you want a "
                "sit-down dinner that will genuinely impress. Book ahead at weekends."
            ),
            "known_for": "Owner-cooked Thai since 2005, genuine heat and wok-char flavour",
            "good_for": "A reliable special-occasion dinner or a careful weeknight meal out",
            "source_url": "https://www.tripadvisor.com/Restaurant_Review-g190747-d732456-Reviews-Nakorn_Thai_Restaurant-Luton_Bedfordshire_England.html",
            "verified": "2026-06-22",
        },
        {
            "type": "Pub",
            "name": "The Great Northern",
            "area": "63 Bute Street, town centre",
            "cuisine": "Real ale, traditional pub",
            "body": (
                "The Great Northern takes its name from the Great Northern Railway, which "
                "was built on its doorstep in the 1860s, and the pub has changed very little "
                "since. The narrow three-storey brick building on Bute Street is Grade II "
                "listed, and the interior -- green-tiled wainscotting with a tulip relief, "
                "an ornate cast-iron roof pillar, a single bar, just a handful of tables -- "
                "is listed in CAMRA's National Pub Heritage as one of the most intact "
                "Victorian pub interiors in England. Landlord John runs a welcoming house; "
                "regulars and newcomers mix easily at the bar. The ales rotate around a "
                "short, well-kept list with St Austell Tribute a regular fixture and two "
                "changing guests. It is a tiny pub and fills up, so arrive with time to "
                "spare and let the room do the rest."
            ),
            "known_for": "A Grade II listed Victorian interior on CAMRA's National Pub Heritage list",
            "good_for": "A proper pint in one of the most intact old pub rooms in England",
            "source_url": "https://camra.org.uk/pubs/great-northern-luton-118800",
            "verified": "2026-06-22",
        },
    ],
    "food_scene": [
        (
            "Luton's food map runs between two distinct poles. Bury Park, a mile north-west "
            "of the town centre along Dunstable Road and Bury Park Road, is the South Asian "
            "quarter: a dense strip of Pakistani, Bangladeshi and Afghan restaurants, "
            "grocers stocked with imported spices, and sweet shops selling mithai and jalebi. "
            "The cooking here ranges from hole-in-the-wall karahi and grill houses open "
            "until midnight to sit-down restaurants serving slow-braised nihari and "
            "slow-cooked paya. For anyone who wants to understand how a significant part "
            "of Luton eats every day, Bury Park is the place to start."
        ),
        (
            "The town centre and the streets around it hold a different mix: Portuguese "
            "and Eastern European cafes that reflect Luton's postwar and later communities "
            "in High Town, Thai and other Asian restaurants around Wellington Street and "
            "the central streets, and the indoor market food hall on The Mall where stalls "
            "serve West African, Jamaican, Malaysian and South Asian food to office workers "
            "at lunch. The Great Northern pub on Bute Street anchors the heritage end of "
            "the town-centre drinking scene."
        ),
        (
            "Luton does not have a single signature dish in the way Birmingham has the balti "
            "or Leeds has the parmo, but it has something broader: a genuinely multi-origin "
            "food culture shaped by the communities that came to work in its hat and car "
            "manufacturing industries from the 1950s onwards. The result is a town where "
            "you can eat halwa puri for breakfast, Portuguese pasteis de nata mid-morning, "
            "a Malaysian laksa at lunch and Thai green curry for dinner, all within a "
            "mile or two of each other."
        ),
    ],
    "visit": [
        (
            "Most of this guide is spread across a compact area. The Great Northern, Nakorn "
            "Thai and Cafe Lagoa are all within ten to fifteen minutes' walk of Luton "
            "station, and the town centre is easily navigated on foot. Bury Park and A1 "
            "Lahori Zaiqa are about a mile north-west of the centre, a short bus ride on "
            "several routes along Dunstable Road or a twenty-minute walk."
        ),
        (
            "The food day flows naturally: Cafe Lagoa for a Portuguese coffee and nata in "
            "the morning, the indoor market for a look at the town's multicultural lunch "
            "scene, Nakorn Thai for a proper dinner, and The Great Northern for a nightcap "
            "in the Victorian bar. If you want to go to Bury Park, go at lunch or early "
            "evening when A1 Lahori Zaiqa is serving freshly cooked karahi -- the "
            "difference from a reheated takeaway is worth timing for."
        ),
    ],
    "checklist": [
        "Start at Cafe Lagoa on High Town Road for a pastel de nata and a proper coffee",
        "Walk to Bury Park along Dunstable Road to see the South Asian quarter",
        "Order chicken karahi and tandoori naan at A1 Lahori Zaiqa - eat in, not delivery",
        "Book Nakorn Thai ahead for the evening, especially at weekends",
        "Finish at The Great Northern and look properly at the Victorian tilework",
    ],
    "what_to_order": (
        "Order with intent. At A1 Lahori Zaiqa, the chicken karahi is the thing -- request "
        "it with a fresh tandoori naan, and add mutton nehari if you are there for brunch. "
        "At Cafe Lagoa, a pastel de nata and a cappuccino made on Brazilian beans; the "
        "bolinhas are worth adding if they are fresh that morning. At Nakorn Thai, ask the "
        "staff what the kitchen is proud of that week -- the curries and the fish cakes are "
        "consistently strong, and the tom yum is made with real heat. At The Great Northern, "
        "St Austell Tribute if it is on, or ask John what the guest ale is."
    ),
    "glance": [
        ("Best for a quick bite", "A1 Lahori Zaiqa, for karahi and naan in Bury Park"),
        ("Best for an occasion", "Nakorn Thai, for nearly twenty years of careful Thai cooking"),
        ("Best for atmosphere", "The Great Northern's Grade II Victorian bar on Bute Street"),
    ],
    "faq": [
        (
            "Where is the best place to eat South Asian food in Luton?",
            "Bury Park, the neighbourhood along Dunstable Road and Bury Park Road about a "
            "mile north-west of the town centre, is Luton's South Asian quarter. A1 Lahori "
            "Zaiqa at 130 Dunstable Road is a well-regarded Pakistani halal restaurant open "
            "from morning until midnight, known for chicken karahi, mutton nehari and halwa "
            "puri cooked fresh on site.",
        ),
        (
            "Does Luton have a good independent cafe scene?",
            "Yes, particularly in High Town, where Cafe Lagoa at 17 High Town Road has been "
            "serving Portuguese pasteis de nata, bolinhas and coffee made with Brazilian "
            "beans roasted in Portugal for years. It is a family-run place open seven days "
            "a week and one of the most characterful cafes in Bedfordshire.",
        ),
        (
            "What is the best restaurant in Luton for a special occasion?",
            "Nakorn Thai on Wellington Street, open since 2005 and consistently rated among "
            "the top four restaurants in Luton on TripAdvisor, is the most reliable choice "
            "for a sit-down dinner. The Thai owner-chef cooks to genuine Southeast Asian "
            "flavour, not a British-adapted version, and the room is calm and unhurried.",
        ),
        (
            "Is there a historic or heritage pub in Luton?",
            "The Great Northern at 63 Bute Street is one of the best examples of an intact "
            "Victorian pub interior in England. It is Grade II listed and appears on CAMRA's "
            "National Pub Heritage list for its unaltered 1890s fittings: green-tiled "
            "wainscotting, an ornate cast-iron pillar, and a single bar. It serves rotating "
            "cask ales with St Austell Tribute a regular.",
        ),
        (
            "What is Bury Park in Luton?",
            "Bury Park is a neighbourhood about a mile north-west of Luton town centre, "
            "centred on Dunstable Road and Bury Park Road, known for its large South Asian "
            "community and concentration of Pakistani, Bangladeshi and Afghan restaurants, "
            "grocers and sweet shops. It is Luton's most distinctive food district and the "
            "place to go for authentic halal cooking at any time of day.",
        ),
        (
            "How do I get around Luton to visit these places?",
            "Luton station puts you five minutes' walk from Cafe Lagoa in High Town and "
            "fifteen minutes from Nakorn Thai and The Great Northern in the town centre. "
            "Bury Park is about a mile further, served by several bus routes along Dunstable "
            "Road or a twenty-minute walk. The town centre is compact and pedestrian-friendly.",
        ),
    ],
}

# portsmouth ----------------------------------------------------------
TOWNS["portsmouth"] = {
    "region": "Hampshire",
    "population": "208K",
    "nearby": ["Gosport", "Fareham", "Havant"],
    "meta_title": "Best Places to Eat in Portsmouth: Local Food Guide",
    "meta_description": (
        "Portsmouth food guide: pie and vinyl on Castle Road, speciality "
        "coffee, Belgian mussels in Southsea and a CAMRA-champion free "
        "house. Read the guide."
    ),
    "trust_strip": (
        "From a Castle Road pie-and-vinyl cafe to a Belgian bar with a "
        "hundred beers, Portsmouth's independent food scene punches well "
        "above its size on Portsea Island"
    ),
    "snapshot": (
        "For a fast answer: Pie and Vinyl on Castle Road for a hot pie "
        "with mash and vinyl on the turntable, Southsea Coffee Co on "
        "Osborne Road for a speciality flat white from one of the city's "
        "best-loved independent cafes, Huis on Elm Grove for Belgian "
        "mussels and a hundred craft beers, and the Hole in the Wall on "
        "Great Southsea Street for a pint of ever-changing cask ale in "
        "Portsmouth and South East Hampshire CAMRA's multiple Pub of the "
        "Year. Four moods, one island city."
    ),
    "stats": [
        ("208K", "Population (approx)"),
        ("1194", "Year Richard I granted Portsmouth its charter"),
        ("Portsea Island", "The only island city in England"),
        ("4", "Hand-picked independents"),
    ],
    "pivot_variant": "coastal",
    "pivot_local_hook": (
        "Portsmouth's kitchens cook hard for a city built on the sea: "
        "fryers running through summer along the Southsea seafront, busy "
        "harbour-side pub kitchens, and Belgian and Indian restaurants "
        "firing at full tilt all push a heavy load of grease-laden vapour "
        "into their canopies every service."
    ),
    "venues": [
        {"type": "Takeaway/Casual", "name": "Pie and Vinyl", "area": "59-61 Castle Road, Southsea",
         "cuisine": "Artisan pies, mash, cider and craft ale",
         "body": ("Castle Road already had a literary pedigree — Arthur Conan Doyle wrote "
                  "Sherlock Holmes at one end and Peter Sellers was born at the other — and "
                  "when Pie and Vinyl opened in April 2012 it added a new chapter. The "
                  "concept was simple and bold: half a shopfront given over to vinyl records, "
                  "the other half to proper pies with mash, mushy peas and gravy. More than "
                  "a decade on it is one of Southsea's best-loved independents, drawing "
                  "diggers and diners in equal measure. The pies span meat, vegetarian and "
                  "vegan options, including Pieminister classics alongside local suppliers, "
                  "all sourced from Buckwells the Osborne Road butcher. Order the Works: a "
                  "pie of your choice, minty mushy peas, buttery mash and a jug of gravy, "
                  "with a local cider or ale to match."),
         "known_for": "Hot pies with mash and vinyl on the turntable since 2012",
         "good_for": "A hearty, affordable and genuinely different lunch or early dinner",
         "source_url": "https://pandvrecords.co.uk/",
         "verified": "2026-06-22"},
        {"type": "Cafe", "name": "Southsea Coffee Co", "area": "63 Osborne Road, Southsea",
         "cuisine": "Speciality coffee, chef-led brunch",
         "body": ("Husband-and-wife team Tara and Martyn Knight opened Southsea Coffee Co "
                  "in 2013 on Osborne Road, and in thirteen years it has become the "
                  "benchmark for speciality coffee on Portsea Island. The approach is "
                  "rigorous without being evangelical: seasonal espresso alongside rotating "
                  "single-origin filter and hand-poured brews sourced from the UK and "
                  "Europe's best roasters, served with chef-led brunch plates that use "
                  "meat from Buckwells next door. In 2026 the cafe was nominated for the "
                  "Best Coffee Shops UK Top 100, judged on coffee quality, ambience, "
                  "innovation and sustainable practice. The room is warm and unhurried, "
                  "the locals clearly regular. Order the rotating single origin on filter "
                  "and the brunch plate of the week."),
         "known_for": "Single-origin speciality coffee and chef-led brunch since 2013",
         "good_for": "A proper morning coffee break with serious beans and good food",
         "source_url": "https://www.southseacoffee.co.uk/",
         "verified": "2026-06-22"},
        {"type": "Restaurant", "name": "Huis", "area": "62 Elm Grove, Southsea",
         "cuisine": "Belgian bar and kitchen — mussels, beer-braised dishes, waffles",
         "body": ("Simon Docker opened Huis in April 2015 in a Southsea shopfront, and "
                  "the name — Flemish for 'house' — says everything about the intention. "
                  "The interior borrows from a 1960s Belgian living room: padded chairs, "
                  "warm lighting, walls thick with bottles. The beer list runs to around "
                  "a hundred Belgian and European labels, including the house HUIS wheat, "
                  "pilsner and blonde brewed exclusively for them, and the kitchen earns "
                  "its place alongside it. Mussels come in creole and cider variations, "
                  "the beef carbonnade is slow-cooked in three different beers, and the "
                  "pork belly rests in apple beer before arriving with a cider and mustard "
                  "reduction. Book ahead for the evening — Huis fills quickly, and it is "
                  "the kind of place you want to settle into for the duration."),
         "known_for": "Belgian mussels, beer-braised pork and a hundred Belgian craft beers",
         "good_for": "A proper evening out or a long Sunday afternoon with great beer",
         "source_url": "https://www.huissouthsea.co.uk/",
         "verified": "2026-06-22"},
        {"type": "Pub", "name": "The Hole in the Wall", "area": "36 Great Southsea Street, Southsea",
         "cuisine": "Cask ale free house — no kitchen, tuck-shop snacks",
         "body": ("Run by Jonathan and Kerry, the Hole in the Wall on Great Southsea "
                  "Street is a genuine free house and the city's most-decorated cask-ale "
                  "pub: Portsmouth and South East Hampshire CAMRA named it Pub of the Year "
                  "multiple times, including for five consecutive years, and CAMRA awarded "
                  "it a national Gold Award as 'a wood-panelled gem that offers a wide "
                  "range of beers from an ever-changing selection of local and national "
                  "breweries'. The pub aims to pour 500 different real ales across a year, "
                  "with five rotating guests alongside two regulars; the ceiling is thick "
                  "with retired pump clips that tell the history. The room is small, "
                  "wood-beamed and usually packed, with a snug at the back, a tuck-shop "
                  "sweet jar on the counter and cans to take away. Go for the beer; "
                  "stay for the conversation."),
         "known_for": "500 cask ales a year, CAMRA multiple Pub of the Year, a wood-panelled snug",
         "good_for": "Serious real ale in Portsmouth's most-awarded independent free house",
         "source_url": "https://theholeinthewallpub.co.uk/",
         "verified": "2026-06-22"},
    ],
    "food_scene": [
        ("Portsmouth's food map is really a map of Southsea. The Victorian suburb "
         "that fans out south of the city centre, threaded by Osborne Road, Albert "
         "Road, Castle Road and Elm Grove, holds the great majority of the city's "
         "independent restaurants, cafes and pubs. Palmerston Road is the main "
         "shopping strip, but it is the quieter residential streets running off it "
         "that carry the best of the eating."),
        ("Old Portsmouth — the historic core tucked inside the old sea walls, with "
         "the Camber Dock fishing quay and the Point — offers a different mood: "
         "cobbled lanes, harbour views and a handful of traditional pubs. The Camber "
         "has landed fish since the late 1100s and still does; Fish Portsmouth at "
         "White Hart Road sells the catch direct from the day boats. Gunwharf Quays, "
         "the waterfront outlet on the harbour, adds a chain-heavy dining strip below "
         "the Spinnaker Tower, but the character of Portsmouth eating lives in "
         "Southsea."),
        ("Being the only island city in England — Portsea Island is separated from "
         "the mainland by narrow tidal channels — gives Portsmouth a seafood identity "
         "that few English cities can match. Plaice, Dover sole, brill and scallop "
         "from local boats, mussels in a Belgian kitchen on Elm Grove, pie and mash "
         "on Castle Road: the city eats with confidence. The annual Seafood Festival "
         "at Gunwharf Quays celebrates that identity every summer, pulling in "
         "producers from across the Solent coast."),
    ],
    "visit": [
        ("Southsea is compact and walkable. Pie and Vinyl, Southsea Coffee Co, Huis "
         "and the Hole in the Wall all sit within ten minutes of each other on foot, "
         "connected by the same network of Victorian terraces. Portsmouth and Southsea "
         "railway station sits just north of the area, and the seafront — Southsea "
         "Common, the castle and the shingle beach — is a short walk south."),
        ("A good day runs: a morning flat white at Southsea Coffee Co, a browse and "
         "a pie-and-mash lunch at Pie and Vinyl, an evening at Huis with mussels and "
         "a Belgian wheat beer, and a final pint at the Hole in the Wall before the "
         "train home. Book Huis in advance for an evening sitting; the Hole in the "
         "Wall rewards a Friday or Saturday afternoon visit when the pump selection "
         "is at its fullest."),
    ],
    "checklist": [
        "Start with a filter coffee at Southsea Coffee Co on Osborne Road",
        "Head to Pie and Vinyl on Castle Road for lunch — arrive by noon to beat the queue",
        "Book Huis on Elm Grove in advance for dinner; it fills every weekend",
        "Finish at the Hole in the Wall on Great Southsea Street for a pint of rotating cask ale",
        "Allow time to walk the Southsea seafront and the Camber Dock between venues",
    ],
    "what_to_order": (
        "Order with intent. At Pie and Vinyl, the Works: a pie of your choice — try "
        "the meat or a vegan option — with mash, minty mushy peas and a jug of gravy, "
        "alongside a local cider or Hampshire ale. At Southsea Coffee Co, the rotating "
        "single-origin filter and whatever the chef has on the brunch menu that week. "
        "At Huis, start with mussels in the creole broth, follow with the pork belly "
        "slow-roasted in apple beer, and take your time over the beer list — a HUIS "
        "house blonde on draught is the safe opening move. At the Hole in the Wall, "
        "ask what just came on: with five rotating guests, the answer changes daily."
    ),
    "glance": [
        ("Best for a quick bite", "Pie and Vinyl, for a hot pie with mash on Castle Road since 2012"),
        ("Best for an occasion", "Huis, for Belgian mussels and a hundred craft beers on Elm Grove"),
        ("Best for atmosphere", "The Hole in the Wall's wood-panelled CAMRA-champion snug"),
    ],
    "faq": [
        ("Where can I eat an authentic pie and mash in Portsmouth?",
         "Pie and Vinyl at 59-61 Castle Road in Southsea, open since April 2012, "
         "combines a serious vinyl record shop with a cafe serving artisan pies, "
         "buttery mash, mushy peas and gravy sourced from local Hampshire suppliers."),
        ("Which is the best independent coffee shop in Portsmouth?",
         "Southsea Coffee Co at 63 Osborne Road, family-run since 2013 by Tara and "
         "Martyn Knight, serves seasonal espresso and rotating single-origin filter "
         "from the best UK and European roasters, with chef-led brunch plates. "
         "The cafe was nominated for the Best Coffee Shops UK Top 100 in 2026."),
        ("Where can I eat Belgian food and drink Belgian beer in Portsmouth?",
         "Huis at 62 Elm Grove, Southsea, opened in April 2015 and specialises in "
         "Belgian bar and kitchen cooking: mussels, beef carbonnade, pork belly "
         "in apple beer, waffles, and an ever-changing list of around 100 Belgian "
         "and European craft beers, including their own exclusive house lagers and wheat."),
        ("Which Portsmouth pub has the best real ale selection?",
         "The Hole in the Wall at 36 Great Southsea Street, a true free house run "
         "by Jonathan and Kerry, has been named Portsmouth and South East Hampshire "
         "CAMRA Pub of the Year multiple times, including five consecutive wins. "
         "It pours five rotating guest casks alongside two regulars, aiming for "
         "500 different real ales across the year."),
        ("What is Portsmouth known for food-wise?",
         "Portsmouth is the only island city in England, sitting on Portsea Island, "
         "and its proximity to the Solent gives it a strong seafood identity. "
         "Fresh fish lands at the Camber Dock in Old Portsmouth from local day boats. "
         "The independent food scene is concentrated in Southsea, particularly "
         "Osborne Road, Castle Road and Elm Grove, with a strong pub culture."),
        ("Can you do a Portsmouth food day on foot?",
         "Easily. Pie and Vinyl, Southsea Coffee Co, Huis and the Hole in the Wall "
         "all sit within ten minutes of each other in Southsea, reached on foot from "
         "Portsmouth and Southsea station. The seafront and Camber Dock are a short "
         "walk south and west respectively."),
    ],
}

# peterborough ----------------------------------------------------------
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

# bolton ----------------------------------------------------------
TOWNS["bolton"] = {
    "region": "Greater Manchester",
    "population": "195K",
    "nearby": ["Bury", "Wigan", "Leigh"],
    "meta_title": "Best Places to Eat in Bolton: Local Food Guide",
    "meta_description": (
        "Where to eat in Bolton: a pasty bakery since 1938, the Happy Valley "
        "cafe, an ARTA-shortlisted Indian and a CAMRA brewery tap. "
        "Read the guide."
    ),
    "trust_strip": (
        "From a 1938 pasty bakery to a CAMRA-decorated brewery tap, Bolton "
        "has a fiercely independent food scene rooted in Lancashire tradition"
    ),
    "snapshot": (
        "For a fast answer: Carrs Pasties on Halliwell Road for the Bolton "
        "institution baking meat-and-potato pasties since 1938, Amico Cafe "
        "on Corporation Street for the family-run all-day brunch spot made "
        "famous by Happy Valley, Achari on Crook Street for the "
        "ARTA-shortlisted Indian with a modern edge, and Bank Top Brewery "
        "Tap on Belmont Road for nine handpumps of cask ale brewed less than "
        "a mile away. Four moods, one proud Lancashire town."
    ),
    "stats": [
        ("1938", "Year Carrs Pasties first baked on Halliwell Road"),
        ("1855", "Year Bolton Market Hall opened, then the largest in England"),
        ("9", "Handpumps at Bank Top Brewery Tap"),
        ("4", "Hand-picked independents"),
    ],
    "pivot_variant": "market-town",
    "pivot_local_hook": (
        "Bolton's market-hall tradition means high-output frying and grilling "
        "through long trading hours, and the pasty bakeries, food-hall stalls "
        "and busy town-centre kitchens all push heavy grease loads into their "
        "canopies from the first batch to the last service of the day."
    ),
    "venues": [
        {
            "type": "Takeaway",
            "name": "Carrs Pasties",
            "area": "351 Halliwell Road (original shop); also Market Place and Bakery Shop on Manchester Road",
            "cuisine": "Lancashire pasties, baked-fresh daily",
            "body": (
                "Grandma Nellie Carr started selling homemade meat-and-potato "
                "pasties from the family tripe shop on Halliwell Road in 1938, "
                "and a queue of mill workers formed around the block within weeks. "
                "Nearly ninety years later the recipe has barely changed: small "
                "batches, simple ingredients, baked from scratch every morning. "
                "The business has passed through three generations of the Carr "
                "family and now runs four Bolton shops, supplies Bolton Wanderers "
                "home matches at the Toughsheet Community Stadium under a stand "
                "sponsorship extended to 2026-27, and in March 2026 opened its "
                "first outlet outside Bolton. The Bolton pasty barm - a Carr "
                "pastie slipped into a soft barm cake - remains the town's own "
                "street-food invention, invented here around 1950 and still the "
                "order to make."
            ),
            "known_for": "Meat-and-potato pasties baked daily from Grandma Nell's 1938 recipe",
            "good_for": "A cheap, filling, genuinely local bite - the taste Bolton grew up on",
            "source_url": "https://www.bwfc.co.uk/news/carrs-pasties-renew-stand-sponsorship-wanderers",
            "verified": "2026-06-22",
        },
        {
            "type": "Cafe",
            "name": "Amico Cafe",
            "area": "28 Corporation Street, Bolton town centre",
            "cuisine": "All-day breakfast and brunch, speciality coffee",
            "body": (
                "A family-run independent on Corporation Street serving "
                "all-day breakfast, brunch and freshly ground coffee seven "
                "days a week. The cafe came to national attention in January "
                "2023 when the BBC filmed the intense ten-minute confrontation "
                "scene between Sarah Lancashire and Siobhan Finneran for series "
                "three of Happy Valley in its dining room - the production kept "
                "it secret from the staff. Since the episode aired, fans have "
                "travelled across the country to sit in the exact spot where "
                "Lancashire sat, and the team created a Happy Valley sandwich "
                "in honour. Beyond the TV fame, it is a proper neighbourhood "
                "cafe: warm, reliably good, and open from half past eight in "
                "the morning. The loaded fries are also worth knowing about."
            ),
            "known_for": "Family-run all-day breakfast and the Happy Valley filming location",
            "good_for": "A relaxed brunch any day of the week in the heart of Bolton",
            "source_url": "https://www.yelp.co.uk/biz/amico-cafe-bolton",
            "verified": "2026-06-22",
        },
        {
            "type": "Restaurant",
            "name": "Achari",
            "area": "148-152 Crook Street, Bolton",
            "cuisine": "Modern Indian, restaurant and takeaway",
            "body": (
                "Achari sits in a stylishly fitted dining room on Crook Street, "
                "serving modern Indian cooking with mood lighting and an extensive "
                "menu that stretches from clay-oven classics to karahi dishes and "
                "a strong vegetarian selection. The kitchen was shortlisted for "
                "Regional Restaurant of the Year - North West at the 2025 Asian "
                "Restaurant and Takeaway Awards, putting it among the most "
                "recognised Indian restaurants in the region. Open seven days a "
                "week for dine-in and takeaway, with delivery on orders over a "
                "minimum spend, it draws both the Bolton curry crowd and visitors "
                "from across Greater Manchester. The name means pickle in Hindi "
                "and Urdu, a nod to the depth of flavour the kitchen aims for."
            ),
            "known_for": "ARTA 2025 shortlisted North West Indian, modern cooking and clay-oven classics",
            "good_for": "A proper sit-down Indian dinner or a takeaway order to the door",
            "source_url": "https://www.acharibolton.co.uk/",
            "verified": "2026-06-22",
        },
        {
            "type": "Pub",
            "name": "Bank Top Brewery Tap",
            "area": "68-70 Belmont Road, Astley Bridge, Bolton",
            "cuisine": "Real ale, traditional pub",
            "body": (
                "Bank Top Brewery was founded in 1995 in a Grade II-listed "
                "Victorian tennis pavilion in the mill village of Bank Top, and "
                "its tap house on Belmont Road a short walk away is the pub "
                "built to showcase the results. Nine handpumps line the bar, "
                "most pouring Bank Top's own range - Flat Cap, Pavilion Pale "
                "and Dark Mild are the regulars - with one pump always reserved "
                "for a guest brewery. No TV, no jukebox, no fruit machines: just "
                "well-kept cask beer, a dartboard, a large outdoor area and the "
                "kind of conversation a proper Northern pub is built for. The "
                "brewery has won numerous CAMRA awards and features annually in "
                "the Good Beer Guide; the tap is the place to drink it at source, "
                "with the brew plant brewing around 22,000 pints a week less than "
                "a mile away."
            ),
            "known_for": "Nine handpumps of Bank Top cask ale, CAMRA multi-award winner since 1995",
            "good_for": "A serious pint of locally brewed real ale in a no-frills Northern pub",
            "source_url": "https://camra.org.uk/pubs/bank-top-brewery-tap-bolton-122443",
            "verified": "2026-06-22",
        },
    ],
    "food_scene": [
        (
            "Bolton's food identity is rooted in its industrial past. The town "
            "grew on cotton spinning - at its 1920s peak it ran more than 200 "
            "mills - and the workers who fed those mills created a culture of "
            "hearty, cheap, filling food. The pasty barm, a Carrs pastie "
            "wedged into a soft barm cake, was reputedly invented here around "
            "1950, a mill-worker's lunch that never went away. Bolton Market "
            "Hall, opened in 1855 and said at the time to be the largest "
            "covered market in England at 7,000 square yards, remains the "
            "anchor of the town-centre food scene, and its new food hall "
            "opened in 2024 with street-food stalls covering Japanese, "
            "Caribbean, Indian and Italian cooking."
        ),
        (
            "The wider town spreads its eating across distinct pockets. Astley "
            "Bridge in the north shelters Bank Top Brewery Tap and a cluster "
            "of community locals. The town centre around Victoria Square and "
            "Corporation Street holds the independent cafes and the market, "
            "while Crook Street and the surrounding streets carry a strong "
            "South Asian restaurant scene, Achari among the most recognised. "
            "Horwich and the Middlebrook Retail Park to the west add suburban "
            "eating options, but the heart of Bolton's food life is "
            "unmistakably in the old town-centre streets."
        ),
        (
            "Bolton does not chase trends, and that is its strength. The "
            "venues that endure here do so because they are genuinely useful "
            "to the people who live here: a bakery that feeds football crowds, "
            "a cafe that locals choose for a proper breakfast, a pub that "
            "brews its own beer on site. The food hall addition and the "
            "growing recognition of restaurants like Achari suggest the scene "
            "is moving forward without losing what made it worth visiting in "
            "the first place."
        ),
    ],
    "visit": [
        (
            "The town centre is compact and walkable. Amico Cafe on Corporation "
            "Street, the Market Hall a minute's walk away, and Achari on Crook "
            "Street all sit within ten minutes of each other on foot. Bank Top "
            "Brewery Tap is a short bus ride north on Belmont Road in Astley "
            "Bridge, or a ten-minute taxi. Carrs Pasties runs four shops "
            "across Bolton, with the original Halliwell Road shop to the north "
            "and a Market Place outlet in the centre."
        ),
        (
            "Done well, a Bolton food day runs like this: an Amico brunch to "
            "start, a look around the Market Hall and a mid-morning pasty from "
            "the Market Place Carrs shop, an Achari dinner in the evening, and "
            "a pint of Flat Cap at Bank Top Tap to finish. The town is well "
            "served by the rail link into Manchester Victoria and regular bus "
            "routes along Bradshawgate and Deansgate."
        ),
    ],
    "checklist": [
        "Pick up a meat-and-potato pasty at the Carrs Market Place shop or the original Halliwell Road store",
        "Book Achari ahead on busy Friday and Saturday nights - it fills up",
        "Visit Bolton Market Hall to see the 1855 cast-iron and glass roof",
        "Head to Bank Top Brewery Tap early evening for the best choice on the nine handpumps",
        "Amico Cafe is open from 8:30 Monday to Saturday - ideal for a pre-market brunch",
    ],
    "what_to_order": (
        "Order with intent. At Carrs Pasties, a meat-and-potato pastie in a "
        "soft barm cake - the Bolton pasty barm, eaten warm. At Amico Cafe, "
        "the full English or loaded fries, with a flat white to start. At "
        "Achari, work through the clay-oven starters before a karahi main, "
        "and ask the staff what the kitchen is proud of that week. At Bank "
        "Top Brewery Tap, a pint of Flat Cap - the brewery's best-seller and "
        "the reason the tap exists."
    ),
    "glance": [
        ("Best for a quick bite", "Carrs Pasties, for a meat-and-potato pastie barm from the Bolton institution"),
        ("Best for an occasion", "Achari, for ARTA-shortlisted modern Indian on Crook Street"),
        ("Best for atmosphere", "Bank Top Brewery Tap, nine handpumps of local cask with no distractions"),
    ],
    "faq": [
        (
            "What is Bolton famous for in terms of food?",
            "Bolton is famous for the pasty barm - a meat-and-potato pastie "
            "inside a soft barm cake, a working-class staple invented here "
            "around 1950. Carrs Pasties on Halliwell Road, baking since 1938, "
            "is the name most associated with the tradition and still supplies "
            "Bolton Wanderers home matches.",
        ),
        (
            "Where can I get the best pasty in Bolton?",
            "Carrs Pasties, founded in 1938 by Grandma Nellie Carr, runs four "
            "Bolton shops including the original on Halliwell Road and a "
            "central Market Place outlet. The meat-and-potato pastie baked "
            "fresh each morning from a recipe unchanged in nearly ninety years "
            "is the one to order.",
        ),
        (
            "Which Bolton cafe was in Happy Valley?",
            "Amico Cafe on Corporation Street filmed the intense scene between "
            "Sarah Lancashire and Siobhan Finneran for BBC series three of "
            "Happy Valley in January 2023. The family-run independent has been "
            "busy with fans ever since and created a Happy Valley sandwich in "
            "honour of the show.",
        ),
        (
            "Where is the best Indian restaurant in Bolton?",
            "Achari on Crook Street was shortlisted for Regional Restaurant of "
            "the Year - North West at the 2025 Asian Restaurant and Takeaway "
            "Awards (ARTA). The stylish independent serves modern Indian cooking "
            "with clay-oven classics and a strong vegetarian menu, open seven "
            "days a week.",
        ),
        (
            "Where can I drink real ale in Bolton?",
            "Bank Top Brewery Tap on Belmont Road in Astley Bridge is Bolton's "
            "standout real ale pub, with nine handpumps serving the output of "
            "Bank Top Brewery, founded in 1995 in a Grade II-listed Victorian "
            "tennis pavilion. Flat Cap, Pavilion Pale and Dark Mild are the "
            "regulars. The pub features annually in the CAMRA Good Beer Guide.",
        ),
        (
            "Is Bolton Market Hall worth visiting for food?",
            "Yes. The Grade II-listed Market Hall, opened in 1855 and once the "
            "largest covered market in England, houses a food hall opened in "
            "2024 under a £5.9m regeneration programme. Stalls cover Japanese, "
            "Caribbean, Indian and Italian cooking with indoor and outdoor "
            "seating, open from Tuesday to Sunday.",
        ),
    ],
}

# dudley ----------------------------------------------------------
TOWNS["dudley"] = {
    "region": "the Black Country, West Midlands",
    "population": "312K",
    "nearby": ["Stourbridge", "Halesowen", "Brierley Hill"],
    "meta_title": "Best Places to Eat in Dudley: Local Food Guide",
    "meta_description": (
        "Where to eat in Dudley: a balti on the High Street, a Black Country cafe, "
        "a coal-country grill and the CAMRA pub of the year. Read the guide."
    ),
    "trust_strip": (
        "From a High Street balti house to a brewery tap that has poured pints since the "
        "1820s, Dudley has a richer independent food scene than the town gets credit for"
    ),
    "snapshot": (
        "For a fast answer: Twice The Spice on the High Street for authentic balti and "
        "tandoori in the Black Country original, Fountain Arcade Cafe for a proper Black "
        "Country breakfast in a Victorian arcade, Koyla Kitchen at The Thorns for Indian "
        "grill and carvery built on coal-country heritage, and The Vine in Brierley Hill "
        "for Batham's ale and faggots at the CAMRA pub of the year. Four moods, one "
        "compact borough."
    ),
    "stats": [
        ("312K", "Population of the Metropolitan Borough of Dudley"),
        ("1820s", "Decade The Vine in Brierley Hill first poured a pint"),
        ("2025 & 2026", "Consecutive CAMRA pub-of-the-year wins for The Vine"),
        ("4", "Hand-picked independents"),
    ],
    "pivot_variant": "pub-town",
    "pivot_local_hook": (
        "Dudley is Black Country pub territory - multi-room locals, on-site breweries "
        "and kitchens turning out faggots and peas all lunchtime - and that steady, "
        "high-volume cooking loads ductwork and canopies with grease every service."
    ),
    "venues": [
        {
            "type": "Takeaway/Casual",
            "name": "Twice The Spice",
            "area": "97-98 High Street, Dudley town centre (DY1 1QP)",
            "cuisine": "Indian balti and tandoori",
            "body": (
                "The site on Dudley High Street where Twice The Spice now trades has a "
                "longer story than the name suggests: the premises housed what is widely "
                "regarded as the first authentic Indian restaurant in the Black Country, "
                "and in 2006 the current team opened here under the new name, keeping "
                "that tradition alive. The menu is rooted in Punjabi balti and tandoori "
                "cooking - desi chicken tikka, chicken balti, lamb dishes, freshly baked "
                "naans - with the Twice Special Balti the house signature. The dining room "
                "seats up to a hundred, with calming blue walls and leather seating, and "
                "the kitchen also handles takeaway and delivery. Open seven days including "
                "bank holidays, Sunday to Thursday until midnight, Friday and Saturday "
                "until 2am - so it doubles as a late-night option after the town quietens."
            ),
            "known_for": "Dudley's heritage Indian balti site, with the Twice Special Balti",
            "good_for": "A late-evening Black Country balti or takeaway on the High Street",
            "source_url": "https://www.twicethespice.net/",
            "verified": "2026-06-22",
        },
        {
            "type": "Cafe",
            "name": "Fountain Arcade Cafe",
            "area": "Fountain Arcade, Dudley town centre (DY1)",
            "cuisine": "Black Country breakfasts and light lunches",
            "body": (
                "Tucked inside Fountain Arcade - a restored Victorian shopping arcade "
                "near Dudley's market place - the Fountain Arcade Cafe is the kind of "
                "town-centre cafe that Dudley locals actually use. Open Monday to Saturday "
                "from 7.30am, it serves the full Black Country repertoire: mega breakfasts, "
                "filled cobs, ham and cheese omelettes, roast dinners on the right day and "
                "freshly made daily specials. Portions are generous, prices are modest, and "
                "the room has the warm, unhurried feel of a place embedded in its community "
                "- it regularly caters for local groups and events. Reviewers repeatedly "
                "reach for the same word: bostin fittle, the Black Country dialect phrase "
                "for really good food. Closing time is 3pm, so it is firmly a daytime "
                "operation in the best arcade-cafe tradition."
            ),
            "known_for": "Proper Black Country breakfasts and filled cobs in a Victorian arcade",
            "good_for": "A hearty, affordable start to the day in the heart of Dudley",
            "source_url": "https://www.facebook.com/Fountainarcadecafe/",
            "verified": "2026-06-22",
        },
        {
            "type": "Restaurant",
            "name": "Koyla Kitchen at The Thorns",
            "area": "174 Thorns Road, Brierley Hill (Dudley borough, DY5 2JY)",
            "cuisine": "Indian grill, steakhouse and British carvery",
            "body": (
                "The name says it all: koyla is the Punjabi word for coal, and Brierley "
                "Hill was built on the Black Country's coal and ironworking heritage. Koyla "
                "Kitchen rose from the shell of the old Thorns Inn and fused that identity "
                "with an ambitious Indian grill and carvery concept - an unusual combination "
                "that works. The kitchen fires tandoori dishes and chargrilled steaks alongside "
                "a daily carvery, and the menu moves confidently between British roast and "
                "Punjabi spicing. A food hygiene inspection in March 2026 confirmed the "
                "kitchen's active operation. Ranked in the top ten restaurants in the Dudley "
                "borough on TripAdvisor (511 reviews), it draws families as much as date-night "
                "diners, and the team accommodates dietary restrictions without fuss. The "
                "carvery and the house naan bread are the two things regulars return for."
            ),
            "known_for": "Indian grill and carvery fusion built on Black Country coal heritage",
            "good_for": "A relaxed family meal or a chargrilled dinner with a side of history",
            "source_url": "https://www.koylakitchen.com/",
            "verified": "2026-06-22",
        },
        {
            "type": "Pub",
            "name": "The Vine (The Bull and Bladder)",
            "area": "10 Delph Road, Brierley Hill (Dudley borough, DY5 2TN)",
            "cuisine": "Traditional pub food, Black Country faggots and pies",
            "body": (
                "The Vine has been poured pints since the 1820s and rebuilt in 1912 after "
                "subsidence - the four-roomed interior that survived that rebuild is now "
                "rated two stars on CAMRA's National Inventory of Historic Pub Interiors. "
                "The ornate Victorian facade carries a quotation from Shakespeare: "
                "'Blessing of your heart, you brew good ale.' It is the brewery tap for "
                "Batham's, the independent Black Country family brewery that has brewed on "
                "the attached site for over 120 years, and the two Batham's ales - Best "
                "Bitter and Mild - are served in peak condition. Food is unapologetically "
                "old school: faggots and peas, homemade pies and pork scratchings at "
                "lunchtime, generously filled cob rolls all day. The pub won CAMRA's "
                "Dudley and South Staffordshire Pub of the Year for both 2025 and 2026, "
                "with judges citing beer quality, community values and the warmth of the welcome."
            ),
            "known_for": "CAMRA pub of the year 2025 and 2026, Batham's ale and faggots and peas",
            "good_for": "A proper Black Country pint in a nationally listed historic interior",
            "source_url": "https://bathams.co.uk/pubs/the-vine-inn/",
            "verified": "2026-06-22",
        },
    ],
    "food_scene": [
        (
            "Dudley's food map stretches across the borough rather than concentrating in "
            "one quarter. The town centre around the High Street and the Victorian Fountain "
            "Arcade has the day-trade cafes and long-standing balti houses, while Brierley "
            "Hill, three miles south on the canal network, holds the borough's strongest pub "
            "and restaurant names. The Black Country Living Museum, set in the canalside "
            "landscape at Tipton Road, is the area's best-known visitor attraction and gives "
            "a sense of the industrial past that shaped the local diet."
        ),
        (
            "That diet is rooted in the working-class cooking of the ironworking era: faggots "
            "and mushy peas, pork scratchings, filled cobs and meat pies are the Black Country "
            "signatures. But Dudley has also been home to South Asian cooking for decades - the "
            "borough's Indian restaurants and balti houses predate the Birmingham Balti Triangle, "
            "and Twice The Spice on the High Street claims the site of the first Indian restaurant "
            "in the Black Country. That double tradition - old Black Country and South Asian - is "
            "what makes the borough's eating scene genuinely its own."
        ),
        (
            "The borough also has a real-ale identity that gives it distinction beyond food. "
            "Batham's Brewery in Brierley Hill, Holden's in Woodsetton and the now-sought-after "
            "brews of Sarah Hughes in Sedgley mean that a drink with your meal here carries more "
            "provenance than it does in most English towns. The Vine is the flagship, but the "
            "whole borough is dotted with unpretentious locals serving the same tradition."
        ),
    ],
    "visit": [
        (
            "Dudley town centre and Brierley Hill are three miles apart - a short drive or bus "
            "ride. The town centre is compact: Fountain Arcade sits near the market place, and "
            "Twice The Spice is on the main High Street a short walk away. In Brierley Hill, "
            "Koyla Kitchen on Thorns Road and The Vine on Delph Road are close enough to walk "
            "between if you plan ahead."
        ),
        (
            "The Black Country Living Museum is worth the detour if you want context for the "
            "food you are eating - the open-air museum recreates the working-class streetscape "
            "of the 1900s, complete with its own period pub and chain-shop. Pair a morning "
            "there with a lunchtime pint at The Vine (which is five minutes away) and you "
            "have the full flavour of why Dudley eats the way it does."
        ),
    ],
    "checklist": [
        "Start the day at the Fountain Arcade Cafe for a Black Country breakfast before the arcade shops open",
        "Walk to Twice The Spice on the High Street and pick up a menu - note it opens from 5pm",
        "Drive or bus to Brierley Hill; The Vine is on Delph Road and opens from lunchtime",
        "Order faggots and peas at The Vine while the Batham's Best Bitter is poured",
        "Book Koyla Kitchen for dinner - the carvery runs daily and the naan is made fresh",
    ],
    "what_to_order": (
        "Order with intent. At Twice The Spice, the Twice Special Balti with a freshly "
        "baked naan, or the desi chicken tikka for the tandoori smoke. At the Fountain "
        "Arcade Cafe, the mega breakfast with a mug of tea, or a filled cob from the "
        "counter. At Koyla Kitchen, the carvery on a Sunday or a chargrilled main with "
        "a side of their house naan. At The Vine, a pint of Batham's Best Bitter and "
        "the faggots and peas at lunchtime - it is one of the more honest plates of "
        "food in the Black Country."
    ),
    "glance": [
        ("Best for a quick bite", "Twice The Spice, for a balti on Dudley High Street since 2006"),
        ("Best for an occasion", "Koyla Kitchen, for Indian grill and carvery in Brierley Hill"),
        ("Best for atmosphere", "The Vine's CAMRA-listed Victorian interior and Batham's on tap"),
    ],
    "faq": [
        (
            "Where can I eat an authentic balti in Dudley?",
            "Twice The Spice at 97-98 High Street, Dudley, has traded since 2006 on the site "
            "of what is widely regarded as the Black Country's first authentic Indian restaurant. "
            "The Twice Special Balti is the house signature, with freshly baked naans and a full "
            "tandoori menu alongside it.",
        ),
        (
            "What is the best pub in Dudley?",
            "The Vine on Delph Road in Brierley Hill, known locally as the Bull and Bladder, "
            "won CAMRA's Dudley and South Staffordshire Pub of the Year for both 2025 and 2026. "
            "It is the brewery tap for Batham's, dates to the 1820s, and holds a two-star "
            "listing on CAMRA's National Inventory of Historic Pub Interiors.",
        ),
        (
            "What is Black Country food?",
            "The Black Country's traditional cooking grew out of the ironworking era: faggots "
            "and mushy peas, pork scratchings, filled cobs, meat pies and hearty breakfasts. "
            "Faggots (minced offal patties in gravy) are the regional signature - bostin fittle, "
            "as locals say, meaning genuinely good food. The Vine in Brierley Hill serves "
            "them with peas at lunchtime.",
        ),
        (
            "Is Batham's beer only available at The Vine?",
            "No, Batham's distributes to a network of tied and free-trade pubs across the "
            "Black Country, but The Vine in Brierley Hill is the brewery tap and the place "
            "to drink it in the most authentic setting - a Victorian four-roomer attached "
            "to the working brewery itself.",
        ),
        (
            "What is Koyla Kitchen in Brierley Hill?",
            "Koyla Kitchen at The Thorns on Thorns Road in Brierley Hill is an independent "
            "Indian grill, steakhouse and carvery restaurant. The name comes from koyla, the "
            "Punjabi word for coal, a nod to the Black Country's coal-mining heritage. It "
            "ranks in the top ten restaurants in the Dudley borough on TripAdvisor.",
        ),
        (
            "Can I get a good breakfast in Dudley town centre?",
            "Yes. The Fountain Arcade Cafe in the Victorian Fountain Arcade near the market "
            "place opens at 7.30am Monday to Saturday and serves full cooked breakfasts, "
            "filled cobs, omelettes and daily specials until 3pm. It is a long-standing "
            "community cafe with consistently good reviews for its generous portions and "
            "friendly service.",
        ),
    ],
}

# bespoke hero wiring (top-15 by rank): (TOWNS key, svg slug)
for _k, _slug in [('glasgow', 'glasgow'), ('sheffield', 'sheffield'), ('manchester', 'manchester'), ('edinburgh', 'edinburgh'), ('liverpool', 'liverpool'), ('bristol', 'bristol'), ('cardiff', 'cardiff'), ('leicester', 'leicester'), ('bradford', 'bradford'), ('coventry', 'coventry'), ('nottingham', 'nottingham'), ('newcastle upon tyne', 'newcastle-upon-tyne'), ('sunderland', 'sunderland'), ('brighton', 'brighton'), ('plymouth', 'plymouth')]:
    if _k in TOWNS:
        TOWNS[_k]["hero_svg_file"] = "eat_hero_%s.svg" % _slug
