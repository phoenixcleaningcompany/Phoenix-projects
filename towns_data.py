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
