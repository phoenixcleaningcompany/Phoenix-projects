import { writeFileSync } from 'node:fs';

// ---- 15 economic archetypes: each maps to industry mix, lead standards, garments, collections ----
const ARCH = {
  OFF:  {name:'Offshore energy', mix:'Offshore oil & gas | Subsea | Decommissioning | Offshore wind', std:'EN ISO 11612 | EN 1149-5 | EN ISO 11611 | EN 13034 | IEC 61482 | EN ISO 20471 | EN 342', kit:'Multi-norm FR/antistatic coveralls | Hi-vis | Cold & wind | Chemical splash', col:'offshore-coveralls | fr-coveralls | hi-vis | cold-store-thermal'},
  LOG:  {name:'Logistics & distribution', mix:'Warehousing & distribution | Cold-chain | Fulfilment | Haulage', std:'EN ISO 20471 | EN ISO 20345 | EN 342 | EN 511 | EN 388', kit:'Hi-vis (Class 2/3) | S3 safety boots | Cold-store thermals | Cut gloves | Bump caps', col:'hi-vis | safety-footwear | cold-store-thermal | work-gloves'},
  MFG:  {name:'Manufacturing & engineering', mix:'General & precision manufacturing | Engineering | Fabrication', std:'EN ISO 11611 | EN ISO 11612 | EN 388 | EN ISO 20471 | EN ISO 20345', kit:'Coveralls | Cut/heat gloves | Hi-vis | Safety boots | Some FR', col:'coveralls | work-gloves | hi-vis | safety-footwear'},
  AUTO: {name:'Automotive', mix:'Vehicle manufacture | Bodyshops | MOT & fast-fit | Parts', std:'EN 388 | EN 1149-5 | EN ISO 20345 | EN 13034', kit:'Boilersuits/coveralls | Nitrile & cut gloves | Antistatic (paint/ESD) | Safety boots', col:'coveralls | work-gloves | safety-footwear'},
  STEEL:{name:'Steel & metals', mix:'Steel & tube | Foundries | Metals processing', std:'EN ISO 11612 (D/E) | EN ISO 11611 | EN 407 | EN ISO 20345', kit:'FR & molten-metal coveralls | Heat gloves | Foundry boots', col:'fr-coveralls | heat-gloves | safety-footwear'},
  FOOD: {name:'Food & drink processing', mix:'Food manufacturing | Fish & seafood | Meat & poultry | Bakery', std:'Food-safe | EN 342 | EN ISO 20345 | EN 388', kit:'Hygiene wear | Cold-store thermals | Wellingtons | Cut gloves', col:'food-hygiene-wear | cold-store-thermal | wellingtons | work-gloves'},
  AGRI: {name:'Agriculture & rural', mix:'Agriculture | Horticulture | Forestry | Land management', std:'EN 343 | EN ISO 11393 (chainsaw) | EN ISO 20471 | EN ISO 20345', kit:'Waterproofs | Chainsaw trousers | Wellingtons | Hi-vis | Thermals', col:'waterproofs | wellingtons | chainsaw | hi-vis'},
  CON:  {name:'Construction & civils', mix:'Construction | Civil engineering | Groundworks | Regeneration', std:'EN ISO 20471 | EN 397 | EN ISO 20345', kit:'Hi-vis | Hard hats | Cargo trousers | Safety boots | Knee pads', col:'hi-vis | safety-footwear | work-trousers'},
  HOSP: {name:'Tourism & hospitality', mix:'Hotels & hospitality | Tourism | Catering | Events', std:'EN ISO 20347 (SRC) | Food-safe | Industrial-wash', kit:'Chef whites | Aprons | FOH uniforms | Housekeeping tunics | Kitchen shoes', col:'chef-whites | hospitality | aprons'},
  HEAL: {name:'Healthcare & public sector', mix:'NHS & healthcare | Care homes | Public sector | Facilities', std:'Colour-coded tunics | EN ISO 20347 | Industrial-wash', kit:'Scrubs | Tunics | Healthcare footwear | Facilities hi-vis', col:'healthcare-scrubs | tunics | hi-vis'},
  UNI:  {name:'University, research & tech', mix:'Higher education | Research & labs | Tech & life sciences', std:'EN 1149-5 | Food-safe | EN ISO 20471', kit:'Lab coats | Antistatic/ESD | Catering | Estates hi-vis', col:'lab-coats | healthcare | hi-vis'},
  PORT: {name:'Port & maritime', mix:'Ports & docks | Shipping & freight | Marine services', std:'EN ISO 20471 | EN 343 | EN ISO 20345 | EN 342', kit:'Hi-vis | Waterproofs | Cold protection | Safety boots', col:'hi-vis | waterproofs | safety-footwear | cold-store-thermal'},
  CORP: {name:'Corporate, retail & services', mix:'Financial & professional services | Retail | Facilities | Security', std:'Embroidery/branding | EN ISO 20471 (facilities)', kit:'Branded polos & shirts | Retail uniforms | Facilities hi-vis | Security', col:'corporate-wear | hi-vis | security'},
  CHEM: {name:'Chemical, petrochem & pharma', mix:'Chemicals | Petrochemicals | Pharmaceuticals', std:'EN ISO 11612 | EN 1149-5 | EN 13034 | EN 14605', kit:'FR & antistatic coveralls | Chemical suits | Hi-vis', col:'fr-coveralls | chemical-suits | hi-vis'},
  MIX:  {name:'Mixed market town', mix:'Mixed trades | Construction | Retail & services | Light industry', std:'EN ISO 20471 | EN ISO 20345', kit:'Hi-vis | Work trousers | Safety boots | Branded polos | Embroidery', col:'hi-vis | work-trousers | safety-footwear | polo-shirts'},
};

// ---- town list: [name, region, pcArea, primaryArchetype, secondaryArchetype|'', confidence H/M/L] ----
// Confidence: H = well-known economic identity, M = plausible, L = default/verify against ONS/NOMIS.
const T = [
// Scotland
['Aberdeen','North East Scotland','AB','OFF','PORT','H'],['Dundee','Tayside','DD','UNI','FOOD','M'],['Edinburgh','Lothian','EH','CORP','UNI','H'],
['Glasgow','Strathclyde','G','MFG','CORP','M'],['Inverness','Highland','IV','HOSP','AGRI','M'],['Perth','Tayside','PH','AGRI','HOSP','M'],
['Stirling','Central Scotland','FK','UNI','HOSP','M'],['Falkirk','Central Scotland','FK','MFG','LOG','M'],['Grangemouth','Central Scotland','FK','CHEM','PORT','H'],
['Livingston','Lothian','EH','MFG','LOG','M'],['Paisley','Renfrewshire','PA','MFG','CORP','M'],['East Kilbride','South Lanarkshire','G','MFG','LOG','M'],
['Dunfermline','Fife','KY','MFG','CORP','L'],['Kirkcaldy','Fife','KY','MFG','MIX','L'],['Ayr','Ayrshire','KA','HOSP','AGRI','M'],
['Kilmarnock','Ayrshire','KA','MFG','MIX','M'],['Greenock','Inverclyde','PA','PORT','MFG','M'],['Motherwell','Lanarkshire','ML','STEEL','MFG','M'],
['Peterhead','Aberdeenshire','AB','FOOD','PORT','H'],['Fraserburgh','Aberdeenshire','AB','FOOD','PORT','H'],['Elgin','Moray','IV','AGRI','FOOD','M'],
['Dumfries','Dumfries & Galloway','DG','AGRI','FOOD','M'],['Aberdeenshire (Westhill)','Aberdeenshire','AB','OFF','MFG','M'],['Livingston (Bathgate)','Lothian','EH','LOG','MFG','L'],
// North East England
['Newcastle upon Tyne','Tyne & Wear','NE','CORP','UNI','M'],['Sunderland','Tyne & Wear','SR','AUTO','MFG','H'],['Gateshead','Tyne & Wear','NE','MFG','LOG','M'],
['Middlesbrough','Teesside','TS','CHEM','STEEL','H'],['Stockton-on-Tees','Teesside','TS','CHEM','LOG','M'],['Darlington','County Durham','DL','MFG','LOG','M'],
['Durham','County Durham','DH','UNI','HEAL','M'],['Hartlepool','Teesside','TS','PORT','MFG','M'],['South Shields','Tyne & Wear','NE','PORT','MIX','L'],
['Washington','Tyne & Wear','NE','AUTO','LOG','M'],['Blyth','Northumberland','NE','OFF','PORT','M'],['Redcar','Teesside','TS','STEEL','CHEM','M'],
// North West England
['Manchester','Greater Manchester','M','CORP','LOG','M'],['Liverpool','Merseyside','L','PORT','CORP','H'],['Preston','Lancashire','PR','MFG','CORP','M'],
['Blackpool','Lancashire','FY','HOSP','MIX','H'],['Bolton','Greater Manchester','BL','MFG','LOG','M'],['Warrington','Cheshire','WA','LOG','CHEM','H'],
['Wigan','Greater Manchester','WN','LOG','MFG','M'],['Blackburn','Lancashire','BB','MFG','MIX','M'],['Burnley','Lancashire','BB','MFG','AUTO','M'],
['Bury','Greater Manchester','BL','MFG','MIX','L'],['Rochdale','Greater Manchester','OL','MFG','LOG','M'],['Oldham','Greater Manchester','OL','MFG','MIX','L'],
['Stockport','Greater Manchester','SK','MFG','CORP','L'],['Salford','Greater Manchester','M','LOG','CORP','M'],['Bootle','Merseyside','L','PORT','LOG','M'],
['Birkenhead','Merseyside','CH','PORT','MFG','M'],['Ellesmere Port','Cheshire','CH','AUTO','CHEM','H'],['Runcorn','Cheshire','WA','CHEM','LOG','H'],
['Widnes','Cheshire','WA','CHEM','MFG','M'],['Chester','Cheshire','CH','HOSP','CORP','M'],['Crewe','Cheshire','CW','AUTO','LOG','H'],
['Lancaster','Lancashire','LA','UNI','HOSP','M'],['Barrow-in-Furness','Cumbria','LA','MFG','PORT','H'],['Carlisle','Cumbria','CA','AGRI','LOG','M'],
['Kendal','Cumbria','LA','AGRI','HOSP','M'],['Southport','Merseyside','PR','HOSP','MIX','M'],['St Helens','Merseyside','WA','MFG','LOG','M'],
// Yorkshire & Humber
['Leeds','West Yorkshire','LS','CORP','MFG','H'],['Sheffield','South Yorkshire','S','STEEL','MFG','H'],['Bradford','West Yorkshire','BD','MFG','FOOD','M'],
['Hull','East Yorkshire','HU','PORT','FOOD','H'],['York','North Yorkshire','YO','HOSP','UNI','M'],['Harrogate','North Yorkshire','HG','HOSP','HEAL','H'],
['Doncaster','South Yorkshire','DN','LOG','MFG','H'],['Rotherham','South Yorkshire','S','STEEL','MFG','H'],['Barnsley','South Yorkshire','S','MFG','LOG','M'],
['Wakefield','West Yorkshire','WF','LOG','MFG','M'],['Huddersfield','West Yorkshire','HD','MFG','MIX','M'],['Halifax','West Yorkshire','HX','MFG','CORP','M'],
['Grimsby','Lincolnshire','DN','FOOD','PORT','H'],['Scunthorpe','Lincolnshire','DN','STEEL','LOG','H'],['Immingham','Lincolnshire','DN','PORT','CHEM','H'],
['Scarborough','North Yorkshire','YO','HOSP','AGRI','M'],['Castleford','West Yorkshire','WF','LOG','MFG','M'],['Keighley','West Yorkshire','BD','MFG','MIX','L'],
['Dewsbury','West Yorkshire','WF','MFG','LOG','L'],['Beverley','East Yorkshire','HU','HOSP','AGRI','L'],['Selby','North Yorkshire','YO','FOOD','AGRI','M'],
// West Midlands
['Birmingham','West Midlands','B','MFG','CORP','H'],['Coventry','West Midlands','CV','AUTO','MFG','H'],['Wolverhampton','West Midlands','WV','MFG','AUTO','M'],
['Stoke-on-Trent','Staffordshire','ST','MFG','LOG','H'],['Solihull','West Midlands','B','AUTO','CORP','H'],['Dudley','West Midlands','DY','MFG','MIX','M'],
['Walsall','West Midlands','WS','MFG','LOG','M'],['West Bromwich','West Midlands','B','MFG','MIX','M'],['Telford','Shropshire','TF','MFG','LOG','H'],
['Worcester','Worcestershire','WR','MFG','HOSP','M'],['Redditch','Worcestershire','B','MFG','LOG','M'],['Kidderminster','Worcestershire','DY','MFG','MIX','L'],
['Nuneaton','Warwickshire','CV','LOG','MFG','M'],['Rugby','Warwickshire','CV','LOG','MFG','H'],['Tamworth','Staffordshire','B','LOG','MFG','M'],
['Cannock','Staffordshire','WS','LOG','MFG','M'],['Stafford','Staffordshire','ST','MFG','MIX','M'],['Burton upon Trent','Staffordshire','DE','FOOD','LOG','H'],
['Shrewsbury','Shropshire','SY','AGRI','HOSP','M'],['Hereford','Herefordshire','HR','AGRI','FOOD','H'],['Leamington Spa','Warwickshire','CV','UNI','CORP','M'],
['Warwick','Warwickshire','CV','CORP','UNI','M'],['Halesowen','West Midlands','B','MFG','MIX','L'],['Smethwick','West Midlands','B','MFG','MIX','L'],
// East Midlands
['Nottingham','Nottinghamshire','NG','CORP','UNI','M'],['Leicester','Leicestershire','LE','MFG','LOG','H'],['Derby','Derbyshire','DE','MFG','AUTO','H'],
['Northampton','Northamptonshire','NN','LOG','MFG','H'],['Corby','Northamptonshire','NN','LOG','FOOD','H'],['Kettering','Northamptonshire','NN','LOG','MFG','M'],
['Wellingborough','Northamptonshire','NN','LOG','MFG','M'],['Lincoln','Lincolnshire','LN','MFG','AGRI','M'],['Boston','Lincolnshire','PE','AGRI','FOOD','H'],
['Mansfield','Nottinghamshire','NG','LOG','MFG','M'],['Chesterfield','Derbyshire','S','MFG','LOG','M'],['Loughborough','Leicestershire','LE','UNI','MFG','M'],
['Grantham','Lincolnshire','NG','LOG','FOOD','M'],['Spalding','Lincolnshire','PE','FOOD','AGRI','H'],['Newark-on-Trent','Nottinghamshire','NG','LOG','AGRI','M'],
['Daventry','Northamptonshire','NN','LOG','MFG','H'],['Ilkeston','Derbyshire','DE','MFG','MIX','L'],['Worksop','Nottinghamshire','S','LOG','MFG','M'],
['Skegness','Lincolnshire','PE','HOSP','AGRI','M'],['Hinckley','Leicestershire','LE','LOG','MFG','M'],['Coalville','Leicestershire','LE','LOG','MFG','M'],
// East of England
['Peterborough','Cambridgeshire','PE','LOG','FOOD','H'],['Cambridge','Cambridgeshire','CB','UNI','CORP','H'],['Norwich','Norfolk','NR','CORP','FOOD','M'],
['Ipswich','Suffolk','IP','PORT','LOG','M'],['Luton','Bedfordshire','LU','AUTO','LOG','H'],['Bedford','Bedfordshire','MK','LOG','MFG','M'],
['Milton Keynes','Buckinghamshire','MK','LOG','CORP','H'],['Colchester','Essex','CO','CORP','HOSP','M'],['Chelmsford','Essex','CM','CORP','CON','M'],
['Basildon','Essex','SS','MFG','LOG','M'],['Southend-on-Sea','Essex','SS','HOSP','CORP','M'],['Harlow','Essex','CM','MFG','LOG','M'],
['Watford','Hertfordshire','WD','CORP','LOG','M'],['Stevenage','Hertfordshire','SG','MFG','CORP','M'],['Hemel Hempstead','Hertfordshire','HP','LOG','MFG','M'],
['St Albans','Hertfordshire','AL','CORP','MIX','M'],['Great Yarmouth','Norfolk','NR','OFF','HOSP','H'],['Lowestoft','Suffolk','NR','OFF','FOOD','H'],
['King\'s Lynn','Norfolk','PE','FOOD','AGRI','M'],['Wisbech','Cambridgeshire','PE','FOOD','AGRI','H'],['Felixstowe','Suffolk','IP','PORT','LOG','H'],
['Braintree','Essex','CM','LOG','MFG','L'],['Welwyn Garden City','Hertfordshire','AL','MFG','CORP','M'],['Huntingdon','Cambridgeshire','PE','LOG','MFG','L'],
['Thetford','Norfolk','IP','FOOD','LOG','M'],['Bury St Edmunds','Suffolk','IP','FOOD','HOSP','M'],['Clacton-on-Sea','Essex','CO','HOSP','MIX','L'],
// London & South East
['London (City)','Greater London','EC','CORP','','H'],['Croydon','Greater London','CR','CORP','CON','M'],['Hounslow','Greater London','TW','LOG','CORP','M'],
['Dartford','Kent','DA','LOG','CON','M'],['Reading','Berkshire','RG','CORP','UNI','H'],['Slough','Berkshire','SL','LOG','MFG','H'],
['Oxford','Oxfordshire','OX','UNI','HEAL','H'],['Southampton','Hampshire','SO','PORT','UNI','H'],['Portsmouth','Hampshire','PO','PORT','MFG','H'],
['Brighton','East Sussex','BN','HOSP','CORP','H'],['Crawley','West Sussex','RH','LOG','CORP','H'],['Guildford','Surrey','GU','CORP','UNI','M'],
['Basingstoke','Hampshire','RG','LOG','CORP','M'],['Maidstone','Kent','ME','CORP','AGRI','M'],['Canterbury','Kent','CT','UNI','HOSP','M'],
['Ashford','Kent','TN','LOG','CON','M'],['Dover','Kent','CT','PORT','HOSP','H'],['Folkestone','Kent','CT','HOSP','MIX','M'],
['Gillingham','Kent','ME','MFG','LOG','L'],['Chatham','Kent','ME','PORT','MFG','M'],['Tunbridge Wells','Kent','TN','CORP','HOSP','M'],
['Woking','Surrey','GU','CORP','MIX','M'],['Farnborough','Hampshire','GU','MFG','CORP','M'],['Aldershot','Hampshire','GU','MFG','MIX','L'],
['Eastbourne','East Sussex','BN','HOSP','HEAL','M'],['Hastings','East Sussex','TN','HOSP','MIX','M'],['Worthing','West Sussex','BN','CORP','HOSP','M'],
['Bognor Regis','West Sussex','PO','HOSP','AGRI','M'],['Chichester','West Sussex','PO','HOSP','AGRI','M'],['Horsham','West Sussex','RH','CORP','MIX','L'],
['Winchester','Hampshire','SO','CORP','HEAL','M'],['Bracknell','Berkshire','RG','CORP','LOG','M'],['Newbury','Berkshire','RG','CORP','AGRI','M'],
['Gravesend','Kent','DA','PORT','LOG','M'],['Sittingbourne','Kent','ME','LOG','FOOD','M'],['Margate','Kent','CT','HOSP','MIX','L'],
['High Wycombe','Buckinghamshire','HP','MFG','CORP','M'],['Aylesbury','Buckinghamshire','HP','LOG','MFG','M'],['Banbury','Oxfordshire','OX','FOOD','LOG','H'],
['Andover','Hampshire','SP','LOG','MFG','M'],['Havant','Hampshire','PO','MFG','LOG','L'],['Fareham','Hampshire','PO','MFG','MIX','L'],
['Redhill','Surrey','RH','CORP','LOG','L'],['Epsom','Surrey','KT','CORP','HEAL','L'],['Staines','Surrey','TW','LOG','CORP','M'],
// South West
['Bristol','Bristol','BS','CORP','MFG','H'],['Plymouth','Devon','PL','PORT','MFG','H'],['Exeter','Devon','EX','UNI','HEAL','M'],
['Gloucester','Gloucestershire','GL','MFG','HEAL','M'],['Cheltenham','Gloucestershire','GL','CORP','HOSP','M'],['Swindon','Wiltshire','SN','LOG','AUTO','H'],
['Bournemouth','Dorset','BH','HOSP','CORP','H'],['Poole','Dorset','BH','MFG','PORT','H'],['Bath','Somerset','BA','HOSP','UNI','H'],
['Taunton','Somerset','TA','AGRI','HEAL','M'],['Yeovil','Somerset','BA','MFG','AGRI','H'],['Weston-super-Mare','Somerset','BS','HOSP','MIX','M'],
['Truro','Cornwall','TR','HEAL','HOSP','M'],['Newquay','Cornwall','TR','HOSP','AGRI','H'],['Penzance','Cornwall','TR','HOSP','FOOD','M'],
['St Austell','Cornwall','PL','AGRI','HOSP','M'],['Torquay','Devon','TQ','HOSP','MIX','H'],['Barnstaple','Devon','EX','AGRI','HOSP','M'],
['Salisbury','Wiltshire','SP','HOSP','AGRI','M'],['Chippenham','Wiltshire','SN','MFG','LOG','M'],['Trowbridge','Wiltshire','BA','MFG','MIX','L'],
['Weymouth','Dorset','DT','HOSP','MIX','M'],['Bridgwater','Somerset','TA','MFG','LOG','H'],['Stroud','Gloucestershire','GL','MFG','AGRI','L'],
['Dorchester','Dorset','DT','AGRI','HOSP','L'],['Falmouth','Cornwall','TR','PORT','HOSP','M'],['Redruth','Cornwall','TR','MFG','MIX','L'],
// Wales
['Cardiff','South Wales','CF','CORP','UNI','H'],['Swansea','South Wales','SA','MFG','UNI','M'],['Newport','South Wales','NP','STEEL','LOG','H'],
['Wrexham','North Wales','LL','MFG','LOG','H'],['Port Talbot','South Wales','SA','STEEL','CHEM','H'],['Bridgend','South Wales','CF','AUTO','LOG','M'],
['Barry','South Wales','CF','CHEM','PORT','M'],['Llanelli','South Wales','SA','MFG','MIX','L'],['Merthyr Tydfil','South Wales','CF','MFG','LOG','M'],
['Rhyl','North Wales','LL','HOSP','MIX','L'],['Bangor','North Wales','LL','UNI','HOSP','M'],['Aberystwyth','Mid Wales','SY','UNI','AGRI','M'],
['Cwmbran','South Wales','NP','MFG','LOG','M'],['Pontypridd','South Wales','CF','MFG','MIX','L'],['Neath','South Wales','SA','MFG','MIX','L'],
['Deeside','North Wales','CH','MFG','AUTO','H'],['Colwyn Bay','North Wales','LL','HOSP','MIX','L'],['Haverfordwest','West Wales','SA','AGRI','CHEM','M'],
// Northern Ireland
['Belfast','Northern Ireland','BT','MFG','PORT','H'],['Londonderry','Northern Ireland','BT','MFG','HEAL','M'],['Lisburn','Northern Ireland','BT','MFG','LOG','M'],
['Newtownabbey','Northern Ireland','BT','MFG','LOG','L'],['Bangor (NI)','Northern Ireland','BT','CORP','HOSP','L'],['Craigavon','Northern Ireland','BT','FOOD','LOG','M'],
['Ballymena','Northern Ireland','BT','MFG','AGRI','M'],['Newry','Northern Ireland','BT','LOG','AGRI','M'],['Coleraine','Northern Ireland','BT','AGRI','HOSP','L'],
['Omagh','Northern Ireland','BT','AGRI','MIX','L'],['Enniskillen','Northern Ireland','BT','AGRI','HOSP','L'],['Antrim','Northern Ireland','BT','MFG','LOG','L'],
];

// ---- batch 2: broader coverage (mostly smaller/commuter/coastal/rural towns) ----
const T2 = [
// Greater London & fringe
['Croydon (Purley)','Greater London','CR','CORP','CON','L'],['Bromley','Greater London','BR','CORP','MIX','L'],['Enfield','Greater London','EN','LOG','MFG','L'],
['Ealing','Greater London','W','CORP','MIX','L'],['Harrow','Greater London','HA','CORP','MIX','L'],['Barnet','Greater London','EN','CORP','MIX','L'],
['Kingston upon Thames','Greater London','KT','CORP','HOSP','L'],['Sutton','Greater London','SM','CORP','MIX','L'],['Romford','Greater London','RM','CORP','LOG','L'],
['Ilford','Greater London','IG','CORP','MIX','L'],['Uxbridge','Greater London','UB','LOG','CORP','L'],['Barking','Greater London','IG','LOG','CON','L'],
['Wembley','Greater London','HA','CON','CORP','L'],['Feltham','Greater London','TW','LOG','MFG','L'],['Orpington','Greater London','BR','CORP','MIX','L'],
// South East fringe & market towns
['Sevenoaks','Kent','TN','CORP','MIX','L'],['Tonbridge','Kent','TN','CORP','MIX','L'],['Royal Tunbridge Wells (Southborough)','Kent','TN','CORP','HOSP','L'],
['Haywards Heath','West Sussex','RH','CORP','MIX','L'],['Burgess Hill','West Sussex','RH','MFG','CORP','L'],['Littlehampton','West Sussex','BN','HOSP','MIX','L'],
['Gosport','Hampshire','PO','MFG','PORT','M'],['Waterlooville','Hampshire','PO','CORP','MIX','L'],['Petersfield','Hampshire','GU','AGRI','CORP','L'],
['Fleet','Hampshire','GU','CORP','MIX','L'],['Camberley','Surrey','GU','CORP','MIX','L'],['Leatherhead','Surrey','KT','CORP','MIX','L'],
['Dorking','Surrey','RH','CORP','AGRI','L'],['Reigate','Surrey','RH','CORP','MIX','L'],['Godalming','Surrey','GU','CORP','MIX','L'],
['Bicester','Oxfordshire','OX','LOG','CORP','M'],['Witney','Oxfordshire','OX','MFG','AGRI','L'],['Abingdon','Oxfordshire','OX','UNI','MFG','M'],
['Didcot','Oxfordshire','OX','UNI','LOG','M'],['Chesham','Buckinghamshire','HP','CORP','MIX','L'],['Amersham','Buckinghamshire','HP','CORP','MIX','L'],
['Marlow','Buckinghamshire','SL','CORP','HOSP','L'],['Wokingham','Berkshire','RG','CORP','MIX','L'],['Maidenhead','Berkshire','SL','CORP','LOG','M'],
['Windsor','Berkshire','SL','HOSP','CORP','M'],['Deal','Kent','CT','HOSP','MIX','L'],['Herne Bay','Kent','CT','HOSP','MIX','L'],
['Faversham','Kent','ME','FOOD','AGRI','M'],['Sheerness','Kent','ME','PORT','LOG','M'],['Ramsgate','Kent','CT','PORT','HOSP','M'],
['Whitstable','Kent','CT','HOSP','FOOD','L'],['Newhaven','East Sussex','BN','PORT','MFG','M'],['Bexhill-on-Sea','East Sussex','TN','HOSP','HEAL','L'],
// South West fringe & coastal
['Frome','Somerset','BA','MFG','AGRI','L'],['Wells','Somerset','BA','HOSP','AGRI','L'],['Glastonbury','Somerset','BA','HOSP','AGRI','L'],
['Clevedon','Somerset','BS','CORP','HOSP','L'],['Portishead','Somerset','BS','CORP','MIX','L'],['Keynsham','Somerset','BS','MFG','CORP','L'],
['Yate','Gloucestershire','BS','MFG','LOG','L'],['Cirencester','Gloucestershire','GL','AGRI','HOSP','M'],['Tewkesbury','Gloucestershire','GL','LOG','MFG','M'],
['Newton Abbot','Devon','TQ','AGRI','LOG','L'],['Paignton','Devon','TQ','HOSP','MIX','M'],['Brixham','Devon','TQ','FOOD','HOSP','M'],
['Tiverton','Devon','EX','AGRI','MFG','L'],['Bideford','Devon','EX','PORT','AGRI','L'],['Bridport','Dorset','DT','MFG','HOSP','L'],
['Wimborne Minster','Dorset','BH','CORP','AGRI','L'],['Christchurch','Dorset','BH','HOSP','MFG','L'],['Camborne','Cornwall','TR','MFG','MIX','L'],
['Bodmin','Cornwall','PL','AGRI','LOG','L'],['Saltash','Cornwall','PL','MIX','CON','L'],['Cirencester (Tetbury)','Gloucestershire','GL','AGRI','HOSP','L'],
// East fringe & fenland
['Ely','Cambridgeshire','CB','AGRI','HOSP','L'],['St Neots','Cambridgeshire','PE','LOG','CORP','L'],['March','Cambridgeshire','PE','FOOD','AGRI','M'],
['Newmarket','Suffolk','CB','AGRI','HOSP','M'],['Stowmarket','Suffolk','IP','FOOD','LOG','M'],['Sudbury','Suffolk','CO','MFG','AGRI','L'],
['Haverhill','Suffolk','CB','MFG','LOG','M'],['Diss','Norfolk','IP','AGRI','FOOD','L'],['Dereham','Norfolk','NR','FOOD','AGRI','M'],
['Cromer','Norfolk','NR','HOSP','FOOD','L'],['Saffron Walden','Essex','CB','AGRI','CORP','L'],['Bishop\'s Stortford','Hertfordshire','CM','CORP','LOG','L'],
['Hitchin','Hertfordshire','SG','CORP','MIX','L'],['Letchworth Garden City','Hertfordshire','SG','MFG','CORP','L'],['Royston','Hertfordshire','SG','MFG','AGRI','L'],
['Biggleswade','Bedfordshire','SG','LOG','AGRI','M'],['Leighton Buzzard','Bedfordshire','LU','LOG','MFG','L'],['Dunstable','Bedfordshire','LU','LOG','MFG','M'],
['Rushden','Northamptonshire','NN','LOG','MFG','M'],['Ramsgate (Broadstairs)','Kent','CT','HOSP','MIX','L'],['Sandy','Bedfordshire','SG','AGRI','LOG','L'],
// Midlands fringe
['Melton Mowbray','Leicestershire','LE','FOOD','AGRI','H'],['Market Harborough','Leicestershire','LE','CORP','LOG','L'],['Oakham','Rutland','LE','AGRI','HOSP','L'],
['Ashby-de-la-Zouch','Leicestershire','LE','LOG','MFG','M'],['Long Eaton','Derbyshire','NG','MFG','LOG','M'],['Buxton','Derbyshire','SK','HOSP','MFG','M'],
['Matlock','Derbyshire','DE','HOSP','AGRI','L'],['Belper','Derbyshire','DE','MFG','MIX','L'],['Swadlincote','Derbyshire','DE','MFG','LOG','M'],
['Newcastle-under-Lyme','Staffordshire','ST','MFG','UNI','M'],['Leek','Staffordshire','ST','MFG','AGRI','L'],['Rugeley','Staffordshire','WS','LOG','MFG','L'],
['Lichfield','Staffordshire','WS','CORP','HOSP','L'],['Bromsgrove','Worcestershire','B','MFG','CORP','L'],['Droitwich Spa','Worcestershire','WR','MFG','HOSP','L'],
['Malvern','Worcestershire','WR','UNI','HOSP','M'],['Ludlow','Shropshire','SY','HOSP','AGRI','M'],['Oswestry','Shropshire','SY','AGRI','LOG','L'],
['Bridgnorth','Shropshire','WV','AGRI','MFG','L'],['Market Drayton','Shropshire','TF','FOOD','AGRI','M'],['Stamford','Lincolnshire','PE','HOSP','CORP','L'],
['Sleaford','Lincolnshire','NG','FOOD','AGRI','M'],['Louth','Lincolnshire','LN','FOOD','AGRI','L'],['Gainsborough','Lincolnshire','DN','MFG','AGRI','M'],
['Retford','Nottinghamshire','DN','LOG','AGRI','L'],['Sutton-in-Ashfield','Nottinghamshire','NG','LOG','MFG','L'],['Kirkby-in-Ashfield','Nottinghamshire','NG','LOG','MFG','L'],
// North West fringe
['Accrington','Lancashire','BB','MFG','MIX','L'],['Nelson','Lancashire','BB','MFG','MIX','L'],['Clitheroe','Lancashire','BB','FOOD','AGRI','M'],
['Chorley','Lancashire','PR','LOG','MFG','M'],['Leyland','Lancashire','PR','AUTO','LOG','M'],['Skelmersdale','Lancashire','WN','LOG','MFG','M'],
['Ormskirk','Lancashire','L','UNI','AGRI','L'],['Northwich','Cheshire','CW','CHEM','LOG','M'],['Winsford','Cheshire','CW','MFG','LOG','L'],
['Sandbach','Cheshire','CW','LOG','FOOD','L'],['Congleton','Cheshire','CW','MFG','MIX','L'],['Macclesfield','Cheshire','SK','CHEM','CORP','M'],
['Wilmslow','Cheshire','SK','CORP','MIX','L'],['Ashton-under-Lyne','Greater Manchester','OL','MFG','LOG','L'],['Hyde','Greater Manchester','SK','MFG','MIX','L'],
['Sale','Greater Manchester','M','CORP','MIX','L'],['Altrincham','Greater Manchester','WA','CORP','MIX','L'],['Eccles','Greater Manchester','M','MFG','LOG','L'],
['Workington','Cumbria','CA','MFG','PORT','M'],['Whitehaven','Cumbria','CA','MFG','PORT','M'],['Penrith','Cumbria','CA','AGRI','LOG','M'],
['Ulverston','Cumbria','LA','MFG','AGRI','L'],['Windermere','Cumbria','LA','HOSP','AGRI','M'],['Middlewich','Cheshire','CW','FOOD','LOG','L'],
// Yorkshire fringe
['Pontefract','West Yorkshire','WF','FOOD','LOG','M'],['Normanton','West Yorkshire','WF','LOG','MFG','M'],['Batley','West Yorkshire','WF','MFG','LOG','L'],
['Brighouse','West Yorkshire','HD','MFG','LOG','L'],['Morley','West Yorkshire','LS','MFG','LOG','L'],['Pudsey','West Yorkshire','LS','MFG','MIX','L'],
['Ilkley','West Yorkshire','LS','CORP','HOSP','L'],['Skipton','North Yorkshire','BD','AGRI','HOSP','M'],['Ripon','North Yorkshire','HG','HOSP','AGRI','L'],
['Northallerton','North Yorkshire','DL','AGRI','HEAL','L'],['Thirsk','North Yorkshire','YO','AGRI','HOSP','L'],['Malton','North Yorkshire','YO','FOOD','AGRI','M'],
['Whitby','North Yorkshire','YO','HOSP','FOOD','M'],['Bridlington','East Yorkshire','YO','HOSP','FOOD','M'],['Goole','East Yorkshire','DN','PORT','LOG','M'],
['Mexborough','South Yorkshire','S','MFG','LOG','L'],['Penistone','South Yorkshire','S','AGRI','MFG','L'],['Stocksbridge','South Yorkshire','S','STEEL','MFG','M'],
// North East fringe
['Chester-le-Street','County Durham','DH','CORP','LOG','L'],['Consett','County Durham','DH','MFG','MIX','L'],['Seaham','County Durham','SR','MFG','PORT','L'],
['Peterlee','County Durham','SR','MFG','LOG','M'],['Newton Aycliffe','County Durham','DL','MFG','LOG','M'],['Bishop Auckland','County Durham','DL','MIX','AGRI','L'],
['Cramlington','Northumberland','NE','MFG','LOG','M'],['Ashington','Northumberland','NE','MFG','MIX','L'],['Morpeth','Northumberland','NE','CORP','AGRI','L'],
['Hexham','Northumberland','NE','AGRI','HOSP','M'],['Berwick-upon-Tweed','Northumberland','TD','AGRI','HOSP','M'],['Billingham','Teesside','TS','CHEM','LOG','H'],
['Yarm','Teesside','TS','CORP','MIX','L'],['Guisborough','Teesside','TS','MIX','AGRI','L'],['Saltburn-by-the-Sea','Teesside','TS','HOSP','MIX','L'],
// Scotland fringe
['Airdrie','North Lanarkshire','ML','MFG','LOG','L'],['Coatbridge','North Lanarkshire','ML','MFG','LOG','L'],['Hamilton','South Lanarkshire','ML','CORP','MFG','L'],
['Wishaw','North Lanarkshire','ML','MFG','MIX','L'],['Cumbernauld','North Lanarkshire','G','LOG','MFG','M'],['Clydebank','West Dunbartonshire','G','MFG','PORT','M'],
['Dumbarton','West Dunbartonshire','G','MFG','MIX','L'],['Renfrew','Renfrewshire','PA','MFG','LOG','L'],['Johnstone','Renfrewshire','PA','MFG','MIX','L'],
['Rutherglen','South Lanarkshire','G','MFG','LOG','L'],['Cambuslang','South Lanarkshire','G','LOG','MFG','L'],['Bathgate','West Lothian','EH','LOG','MFG','M'],
['Musselburgh','East Lothian','EH','CORP','MIX','L'],['Dalkeith','Midlothian','EH','LOG','AGRI','L'],['Alloa','Clackmannanshire','FK','MFG','FOOD','L'],
['Arbroath','Angus','DD','FOOD','PORT','M'],['Forfar','Angus','DD','AGRI','FOOD','L'],['Montrose','Angus','DD','OFF','PORT','M'],
['Stonehaven','Aberdeenshire','AB','OFF','HOSP','M'],['Inverurie','Aberdeenshire','AB','OFF','AGRI','M'],['Ellon','Aberdeenshire','AB','OFF','AGRI','M'],
['Nairn','Highland','IV','HOSP','AGRI','L'],['Forres','Moray','IV','AGRI','FOOD','L'],['Wick','Highland','KW','OFF','AGRI','M'],
['Thurso','Highland','KW','OFF','AGRI','M'],['Oban','Argyll & Bute','PA','HOSP','FOOD','M'],['Fort William','Highland','PH','HOSP','AGRI','M'],
['Galashiels','Scottish Borders','TD','MFG','AGRI','L'],['Hawick','Scottish Borders','TD','MFG','AGRI','M'],['Stranraer','Dumfries & Galloway','DG','PORT','AGRI','M'],
// Wales fringe
['Caerphilly','South Wales','CF','MFG','LOG','L'],['Pontypool','South Wales','NP','MFG','MIX','L'],['Ebbw Vale','South Wales','NP','MFG','MIX','L'],
['Abergavenny','South Wales','NP','AGRI','HOSP','M'],['Chepstow','South Wales','NP','MFG','HOSP','L'],['Aberdare','South Wales','CF','MFG','MIX','L'],
['Porthcawl','South Wales','CF','HOSP','MIX','L'],['Penarth','South Wales','CF','CORP','HOSP','L'],['Carmarthen','West Wales','SA','AGRI','HEAL','M'],
['Llandudno','North Wales','LL','HOSP','MIX','H'],['Caernarfon','North Wales','LL','HOSP','AGRI','M'],['Holyhead','North Wales','LL','PORT','HOSP','M'],
['Prestatyn','North Wales','LL','HOSP','MIX','L'],['Mold','North Wales','CH','LOG','MFG','L'],['Newtown','Mid Wales','SY','MFG','AGRI','L'],
['Welshpool','Mid Wales','SY','AGRI','LOG','L'],['Brecon','Mid Wales','LD','AGRI','HOSP','M'],['Milford Haven','West Wales','SA','CHEM','PORT','H'],
['Tenby','West Wales','SA','HOSP','FOOD','M'],['Ammanford','West Wales','SA','MFG','AGRI','L'],['Bridgend (Pencoed)','South Wales','CF','AUTO','MFG','M'],
// NI fringe
['Larne','Northern Ireland','BT','PORT','MFG','M'],['Carrickfergus','Northern Ireland','BT','MFG','MIX','L'],['Armagh','Northern Ireland','BT','AGRI','FOOD','M'],
['Portadown','Northern Ireland','BT','FOOD','LOG','M'],['Banbridge','Northern Ireland','BT','LOG','AGRI','L'],['Newtownards','Northern Ireland','BT','MFG','LOG','L'],
['Cookstown','Northern Ireland','BT','FOOD','AGRI','M'],['Dungannon','Northern Ireland','BT','FOOD','AGRI','M'],['Magherafelt','Northern Ireland','BT','AGRI','MFG','L'],
['Ballymoney','Northern Ireland','BT','AGRI','FOOD','L'],['Limavady','Northern Ireland','BT','AGRI','MFG','L'],['Strabane','Northern Ireland','BT','MFG','AGRI','L'],
];

// ---- emit archetype reference CSV ----
let ref = 'Code,Archetype,Industry mix,Lead standards,Garment families,Shopify collections\n';
for(const [c,a] of Object.entries(ARCH)){
  ref += [c,a.name,a.mix,a.std,a.kit,a.col].map(csv).join(',')+'\n';
}
writeFileSync('/home/user/Phoenix-projects/docs/tranche1-archetypes.csv', ref);

// ---- emit town list CSV (joined to archetype fields) ----
let out = 'Town,Region,Postcode area,Primary archetype,Secondary archetype,Confidence,Industry mix (pre-populated),Lead standards (pre-populated),Garment families,Shopify collections,Verify?\n';
const seen=new Set();
for(const [town,region,pc,p,s,conf] of T.concat(T2)){
  if(seen.has(town)) continue; seen.add(town);
  const A=ARCH[p], B=s?ARCH[s]:null;
  const mix = B? A.mix+' | +'+B.name : A.mix;
  const std = B? mergeStd(A.std,B.std) : A.std;
  const kit = B? A.kit+' | +'+B.name+' kit' : A.kit;
  const col = B? mergeCol(A.col,B.col) : A.col;
  const verify = conf==='L' ? 'YES - verify vs ONS/NOMIS' : (conf==='M'?'check':'');
  out += [town,region,pc,A.name,B?B.name:'',conf,mix,std,kit,col,verify].map(csv).join(',')+'\n';
}
writeFileSync('/home/user/Phoenix-projects/docs/tranche1-town-list.csv', out);

function csv(v){ v=String(v); return /[",\n]/.test(v)? '"'+v.replace(/"/g,'""')+'"' : v; }
function mergeStd(a,b){ const set=new Set([...a.split(' | '),...b.split(' | ')]); return [...set].join(' | '); }
function mergeCol(a,b){ const set=new Set([...a.split(' | '),...b.split(' | ')]); return [...set].join(' | '); }

// ---- summary ----
const byArch={}, byConf={H:0,M:0,L:0};
for(const [t,r,pc,p,s,c] of T.concat(T2)){ byArch[p]=(byArch[p]||0)+1; byConf[c]++; }
console.log('TOWNS:', seen.size);
console.log('CONFIDENCE:', JSON.stringify(byConf));
console.log('BY PRIMARY ARCHETYPE:');
Object.entries(byArch).sort((a,b)=>b[1]-a[1]).forEach(([k,v])=>console.log('  '+k.padEnd(6), v, ARCH[k].name));
