# Wales hotels — Google Places API pipeline

## Source
Same approach as the restaurant/pub pipelines: Google Places API (New),
Text Search, "hotels in {town}, Wales" for all 216 towns.

## Pipeline
1. `fetch_hotels.py` — 12,554 raw results, 84% with website, 634 API
   requests. Heaviest overlap of the three Wales verticals so far — even
   tiny villages hit the 60-result cap, since "hotels" is a rarer category
   and Google widens the search radius well beyond the town itself.
2. `filter_chains.py` — dedupes to 3,338 unique hotels, keyword-filters
   chain brands (Premier Inn, Holiday Inn, Best Western, Travelodge,
   etc. — 122 excluded), leaving **3,216 independent/small hotels, 75%
   with website.**
3. `find_emails.py` — **1,308 emails found from 2,410 sites (54% hit
   rate)** — the best of the three Wales verticals, likely because hotels
   are more likely to run a proper business website with a booking/contact
   email than a small independent restaurant or pub.
4. Deduped by email → **`mailchimp_contacts.csv`, 1,156 unique recipients.**

## Caveats
- **Not filtered by hotel size/type.** Google's "hotels" search pulled in
  a lot of small B&Bs, guest houses, hostels, and self-catering cottages
  alongside genuine hotels (see the email-discovery log — "The Miners
  b&b", "Trallwm Forest Cottages", "Tyncornel hostel"). A 4-room B&B
  likely doesn't have a commercial kitchen or laundry system worth a
  TR19 clean the way a full hotel with a restaurant/banqueting kitchen
  would. There's no field in the Places API response to filter on this
  automatically — worth a manual pass before a full send if it matters.
- Same chain-keyword-list caveat as pubs: judgment call, not exhaustive.
- Not filtered for the "avoid heavy-use" preference from the original brief.

## Re-running
```
export PLACES_API_KEY=xxx
python3 fetch_hotels.py --towns towns_full.txt --out hotels_full.csv --max-pages 3
python3 filter_chains.py
python3 find_emails.py --limit 0 --out found_emails_full.csv --commit-every 100
```
