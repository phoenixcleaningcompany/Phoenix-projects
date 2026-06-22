# --------------------------------------------------------------------------
# LIVERPOOL — web-researched June 2026
# Four venues confirmed currently trading 2026-06-22.
# Nearby: Birkenhead, Bootle, Wallasey — all on eat_towns.csv, all
# geographically close (across the Mersey or adjacent north Liverpool).
# --------------------------------------------------------------------------
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
