# England hotels — Google Places API pipeline

## Source
Same pipeline as the rest of the England/Wales batch: Google Places API
(New), Text Search, "hotels in {town}, England" for all 446 towns.

## Pipeline
1. `fetch_hotels.py` — 26,527 raw results, 87% with website, 1,330 API
   requests. Heaviest overlap of the England batch (consistent with Wales
   hotels) — even small towns hit the 60-result cap.
2. `filter_chains.py` — dedupes to 13,049 unique, keyword-filters chain
   brands (Premier Inn, Holiday Inn, Best Western, Travelodge, etc.) —
   1,763 excluded, leaving **11,286 independent/small hotels, 81% with
   website (9,164).**
3. `find_emails.py` — **4,989 emails found (54% hit rate)** — best hit
   rate of the England batch, consistent with Wales (hotels tend to run
   proper business websites with booking/contact emails more reliably
   than small independent restaurants/pubs).
4. Deduped by email → **`mailchimp_contacts.csv`, 4,220 unique recipients.**

## Caveats
- Same as Wales hotels: not filtered by hotel size/type — includes small
  B&Bs, guest houses, and self-catering places alongside genuine hotels
  with commercial kitchens/laundries. Worth a manual size pass before a
  full send.
- Chain keyword list judgment call, not exhaustive.
- Not filtered for the "avoid heavy-use" preference from the original brief.

## Re-running
```
export PLACES_API_KEY=xxx
python3 fetch_hotels.py --towns towns_full.txt --out hotels_full.csv --max-pages 3
python3 filter_chains.py
python3 find_emails.py --limit 0 --out found_emails_full.csv --commit-every 200
```
