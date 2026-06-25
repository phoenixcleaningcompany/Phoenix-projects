# TC research-agent spec (read in full before writing)

You research real local telecoms / network-installation context for a set of UK
towns and WRITE a JSON file of entries for the TC workwear-page generator. Do
REAL web research (search the web) for accurate, verifiable proper nouns.

## Output: write ONE JSON file
Write a UTF-8 JSON object mapping each town's lowercase key (exactly as spelled in
the ALLOWED LIST below, e.g. "stoke-on-trent", "newcastle upon tyne") to an entry
with EXACTLY these fields, in this order:

```
{
  "<key>": {
    "region": "...",
    "nearby": ["...", "...", "..."],
    "snapshot": "...",
    "s1_head": "...",
    "s1loc": ["...", "..."],
    "kit_loc": "...",
    "s2_intro": "..."
  }
}
```

It MUST be valid JSON (double-quoted keys/strings, no trailing commas, no comments).
After writing, reply with one line per town: `<town>: nearby=[a,b,c]` and nothing else.

## Field specs
- **region**: `"{Town} and {county/area}"` e.g. "Derby and Derbyshire", "Hull and East Yorkshire".
- **nearby**: exactly 3 OTHER towns, geographically close, ALL present in the ALLOWED LIST
  below, spelled EXACTLY. A wrong/off-list value FAILS the build. Name one of them in s2_intro.
- **snapshot**: 60-75 words; names the town and BOTH ordering routes - the fleet / trade-account
  route AND the sole-trader / direct-online (no account) route.
- **s1_head**: short, e.g. "Kitting the field engineers of {county/area}".
- **s1loc**: EXACTLY 2 paragraphs, ~80-110 words each, BOTH genuinely local and proper-noun-rich.
  - para1 = the local full-fibre / network build picture: name the networks actually building there
    (Openreach, CityFibre if it is a CityFibre town, and the real alt-nets present - e.g.
    Netomnia/YouFibre, nexfibre/Virgin Media O2, Hyperoptic, Gigaclear, Ogi (Wales), Quickline
    (Yorks/Humber), GoFibre (Scotland), Freedom Fibre, brsk, Toob (Hants), Jurassic Fibre (SW),
    County Broadband (Essex/Suffolk), Community Fibre (London), KCOM/MS3 (Hull only)) and real
    DISTRICTS / areas. ONLY name networks genuinely active in that town.
  - para2 = the local commercial / structured-cabling + CCTV scene with SPECIFIC named business
    parks, universities, districts. Do NOT write a generic "every size of business" paragraph.
  - If unsure of a private firm's name, do NOT invent one - use real networks + districts + parks.
- **kit_loc**: short phrase like "across the town's streets, cabinets and customer premises"
  (use "city's" for cities, "borough's" for London boroughs / metropolitan boroughs).
- **s2_intro**: `"Whether you are a build contractor with crews across {Town}, a structured-cabling
  firm or a one-van broadband installer toward {a nearby}"` - NO trailing punctuation.

## Style gold (match tone and length)
- Birmingham p1: "Birmingham and the wider West Midlands are in the middle of a huge network build. Openreach has thousands of engineers across the Midlands pushing full fibre out through the city and into Sandwell, Wolverhampton and Solihull, CityFibre and the alternative networks are building alongside through contractors like Kelly Group and Morrison Telecom, and Virgin Media and the mobile operators keep upgrading on top. Around the big build sit local cabling firms like Midland Telecom Networks and a long tail of broadband, CCTV and structured-cabling installers."
- Birmingham p2: "And it runs on every size of business. The national build contractors field whole crews of engineers and buy through procurement, while a large layer of small subcontractors, ex-BT sole traders and independent broadband and CCTV installers take on work across the city and need just a few branded pieces. A workwear supplier here has to serve the fleet and the one-van installer alike, which is why we run trade accounts and direct online ordering side by side."
- Leeds p1: "Leeds is a CityFibre Gigabit City, with full fibre going in across the city and the major build contractors, from Openreach delivery partners to civils firms like OCU, working through Chapel Allerton, Holbeck, Pudsey, Morley and Beeston. Alongside the residential rollout sits a strong commercial scene: structured-cabling and fibre-optic firms such as Express Data, Eurocoms and Leeds Communications wiring offices, schools and multi-site businesses in Cat5e, Cat6 and fibre across Yorkshire."
- Leeds p2: "And the trade runs the full range of sizes. The build contractors put crews of engineers on the street and buy centrally, while commercial cabling firms, CCTV installers and ex-BT sole-trader telephone and broadband engineers take on work for homes and businesses around the city. A workwear supplier has to kit the fleet and the one-person installer alike, which is why we run trade accounts for the crews and direct online ordering, with no account, for everyone else."

## HARD RULES (these are gates - breaking them fails the build)
- Plain ASCII only. No non-ASCII characters. No HTML entities. No ampersands - write "and"
  (e.g. write "V and A Dundee", not "V&A"). No em-dashes - use " - ". Straight apostrophes only.
  Write money as "80 million pound", never the pound sign.
- No delivery-timescale claims (never "next day", "same day", "24 hour", "48 hour").
- Do NOT use ANY of these words/phrases ANYWHERE (cross-series bleed + banned terms):
  scrubs, veterinary, tunic, vet nurse, kennel, cattery, equine, **wellington** (avoid even as a
  place name - use another district), barber, hairdressing, beautician, clog, hoodie, spa day,
  courier, multidrop, owner-driver, parcel round, "Chapter 8", "National Highways", "sector
  scheme", "body armour", ballistic, "stab vest", epaulette, SIA, "BS 7858", hairnet, "hygiene
  coat", BRCGS, HACCP, "high-care", snood, "beard net", tabard, "convenience store", "garden
  centre", forecourt, "farm shop", stockroom, gym, athleisure, "club crest", matchday, tracksuit,
  "solar panel", "EV charging", "EV charge", "heat pump", "MCS-certified", "MCS-registered",
  chainsaw, arborist, "tree surgery", LANTRA, NPTC, Ofsted, KCSIE, "Care Quality Commission",
  CQC, "Care Inspectorate", RCV, "refuse collection", "bin lorry", "kerbside collection", HWRC,
  COSHH, "colour-coded cleaning".
- These ARE allowed (core TC vocabulary): softshell, hi-vis, polo, cargo, fleece, waterproof,
  safety boots, telecoms, network, fibre, broadband, cabling, CCTV, engineer, installer.

## ALLOWED LIST (nearby must come from here, exact spelling)
London, Birmingham, Leeds, Glasgow, Sheffield, Manchester, Edinburgh, Liverpool, Bristol, Cardiff, Leicester, Bradford, Coventry, Nottingham, Newcastle upon Tyne, Sunderland, Brighton, Plymouth, Hull, Derby, Southampton, Stoke-on-Trent, Wolverhampton, Swansea, Milton Keynes, Aberdeen, Reading, Northampton, Luton, Portsmouth, Peterborough, Bolton, Dudley, Norwich, Swindon, Croydon, Bournemouth, Southend-on-Sea, Walsall, Warrington, Slough, Huddersfield, Telford, Newport, Oxford, Poole, Dundee, Cambridge, York, Blackpool, Ipswich, Middlesbrough, Gloucester, Exeter, Solihull, Colchester, Cheltenham, Gateshead, High Wycombe, Blackburn, Maidstone, Basingstoke, Crawley, Chelmsford, Preston, Walthamstow, Basildon, Dartford, Bedford, Doncaster, Worthing, Rotherham, Mansfield, Eastbourne, Oldham, Wigan, Sutton Coldfield, Lincoln, Worcester, Salford, St Helens, Wembley, Hemel Hempstead, Watford, Stockport, Rochdale, Hove, Ilford, Barnsley, Darlington, Hastings, Hartlepool, Birkenhead, Bath, Stevenage, Grimsby, Southport, Halifax, Eltham, Hounslow, Bromley, Nuneaton, Redditch, Harlow, Harrow, St Albans, Stockton-on-Tees, Gosport, Scunthorpe, Chesterfield, Ashford, Guildford, Lewisham, Woolwich, Weston-super-Mare, West Bromwich, Edgware, Bury, Tamworth, Chatham, Paisley, Carlisle, Crewe, Bootle, Harrogate, Maidenhead, Newcastle-under-Lyme, Burnley, Enfield, Gravesend, East Kilbride, South Shields, Burton-on-Trent, Shrewsbury, Rugby, Stafford, Taunton, Tynemouth, Cannock, Farnborough, Torquay, Inverness, Wrexham, Loughborough, Stourbridge, Ellesmere Port, Dewsbury, Widnes, Runcorn, Rochester, Twickenham, Scarborough, Orpington, Wallasey, Hayes, Aylesbury, Hereford, Merthyr Tydfil, Halesowen, Tunbridge Wells, Dunfermline, Livingston, Barrow-in-Furness, Bebington, Smethwick, Horsham, Washington, Hornchurch, Kettering, Brierley Hill, Corby, Bracknell, Leamington Spa, Kidderminster, Weymouth, Canterbury, Barry, Hamilton, Folkestone, Crosby, Keighley, Eastleigh, Lancaster, Macclesfield, Cumbernauld, Perth, Cheshunt, Wellingborough, Kingston upon Thames, Andover, Llanelli, Neath, Bridgend, Cwmbran, Christchurch, Romford, Barnet, Paignton, Kirkcaldy, Batley, Yeovil, Welwyn Garden City, Carlton, West Bridgford, Beckenham, Sutton, Banbury, Winchester, Beeston, Ayr, Kilmarnock, Bridgwater, Salisbury, Havant, Hinckley, Middleton, Ashton-under-Lyne, Sutton-in-Ashfield, Chippenham, Caerphilly, Coatbridge, Lytham St Annes, Worksop, Leigh, Bexhill-on-Sea, Altrincham, Urmston, Grantham, Boston, Newbury, Cleethorpes, Bicester, Ramsgate, Margate, Sittingbourne, Hatfield, Bishop's Stortford, Wokingham, Feltham, Farnham, Fareham, Chorley, Castleford, Ilkeston, Cramlington, Glenrothes, Herne Bay, Arnold, Blyth, Leyland, Skelmersdale, Canvey Island, Long Eaton, Abingdon, North Shields, Falkirk, Chester-le-Street, Wednesbury, Denton, Port Talbot, Aldershot, Airdrie, Accrington, Exmouth, Redcar, Whitley Bay, Houghton le Spring, Amesbury, Warwick, Erith, Billericay, Coalville, Hitchin, Dunstable, Wickford, Bridlington, Beverley, Dover, Morecambe, Trowbridge, Barnstaple, Sidcup, Hyde, Billingham, Oldbury, Irvine, Aberdare, Lichfield, Letchworth, Haywards Heath, Uxbridge, Whitstable, Strood, Glossop, Stretford, Dumfries, Motherwell, Borehamwood, Burgess Hill, Hucknall, Brighouse, Windsor, Pudsey, Bedworth, Rayleigh, Loughton, Rutherglen, Epsom, Staines, Chichester, Deal, Sevenoaks, Tonbridge, Rushden, Pontefract, Camberley, Kendal, Ruislip, Malvern, Bromsgrove, Stratford-upon-Avon, Spalding, Newark, Brentwood, Redhill, Bramhall, Ashton-in-Makerfield, Heywood, Littlehampton, Darwen, Colwyn Bay, Pontypridd, Harpenden, Wishaw, Nelson, Radcliffe, Fleet, Witney, Willenhall, Ashington, Shipley, Frome, Gosforth, Pontypool, Bilston, Sedgley, Tipton, Hertford, Totton, Burntwood, Farnworth, Jarrow, Penarth, Congleton, East Grinstead, Didcot, Melton Mowbray, Clydebank, Daventry, Thatcham, Kingswinford, Bloxwich, Fleetwood, Bushey, Newton Abbot, Rhyl, Thornton Cleveleys, Bognor Regis, Seaford, Whitehaven, Droitwich, Evesham, Ormskirk, Blackwood, Fulwood, St Austell, Consett, Newton Aycliffe, Thornaby-on-Tees, Portishead, Ferndown, Broadstairs, Hoddesdon, Wilmslow, Grays Thurrock, Upminster, New Milton, Rothwell, Formby, Alfreton, Arbroath, Elgin, Rugeley, Oadby, Kidsgrove, Bishop Auckland, Chapeltown, Stalybridge, Workington, Walton-on-Thames, Esher, Whitefield, Potters Bar, Kenilworth, Buxton, Market Harborough, Garforth, Droylsden, Newquay, Truro, Falmouth, Camborne, Tiverton, Stamford, Retford, Belper, Dronfield, Guiseley, Rawtenstall, Hindley, Royton, Clevedon, Reigate, Horley, Godalming, Sandhurst, Woodley, Crowborough, Caterham, Wellington, Bathgate, Musselburgh, Penzance, Melksham, Seaham, Horwich, Hailsham, Chesham, Gainsborough, Renfrew, Bellshill, Shoreham-by-Sea, Llandudno, Poulton-le-Fylde, Stourport-on-Severn, Skegness, Biddulph, Dorchester, Atherton, Failsworth, Colne, Bingley, Mirfield, Yeadon, Peterlee, Faversham, Burnham-on-Sea, Northwich, Bangor, Maesteg, Buckley, Hythe, Berkhamsted, Dumbarton, Alloa, Ripley, Spennymoor, Kempston, Lancing, Prestatyn, Horsforth, Goole, Oswestry, Sandbach, Normanton, Stanley, Cottingham, Ossett, Maltby, Ripon, Guisborough, Saltash, Bideford, Penrith, Northallerton, Featherstone, Mexborough, Bedlington, Morpeth, Hessle, Selby, Knaresborough, Clitheroe, Neston, Bromborough, Bodmin, Heswall, Prudhoe, Ulverston, Prescot, Newport (Isle of Wight), Ryde, Cowes, Shanklin, Sandown

(Note: "Wellington" appears on the list but you must NOT write the word "wellington" in page
text - if it would be a nearby, pick a different on-list town instead.)
