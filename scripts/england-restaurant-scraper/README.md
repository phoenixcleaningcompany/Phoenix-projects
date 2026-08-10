# England restaurants — Google Places API pipeline

## Source
Same pipeline as Wales: Google Places API (New), Text Search, "restaurants
in {town}, England" for all 446 towns in the England-filtered top-500 UK
towns list (54 Scottish/Welsh towns excluded — see `scripts/england_towns_full.txt`).

## Pipeline
1. `fetch_restaurants.py` — 26,055 raw results, 89% with website, 1,323 API
   requests. (First attempt was lost to a git-stash mistake mid-run and had
   to be re-run from scratch — see repo history for details.)
2. `filter_chains.py` — dedupes to 24,089 unique, keyword-filters chain
   brands (built directly on the keyword approach this time, having
   already learned from the Wales pub/hotel name-repeat failures) — 1,215
   chain locations excluded (PizzaExpress, McDonald's, M&S Foodhall,
   Morrisons Cafe, Popeyes, Chaiiwala, Prezzo, Carluccio's, etc.), leaving
   **22,874 independent/small restaurants, 87% with website (19,964).**
3. `find_emails.py` — **9,459 emails found (47% hit rate)**, run against
   all 19,964 websites, with `--commit-every 200` auto-checkpointing (this
   run survived multiple container restarts across several hours cleanly).
4. Deduped by email → **`mailchimp_contacts.csv`, 7,370 unique recipients.**

## Caveats
- Chain keyword list is a judgment call, not exhaustive at England scale —
  spot-check before a full send.
- Not filtered for the "avoid heavy-use/12+ hour sites" preference from
  the original brief.
- Runtime was long (~13 hours across several sessions/restarts) purely due
  to volume (19,964 sites) — not a sign anything was wrong.

## Re-running
```
export PLACES_API_KEY=xxx
python3 fetch_restaurants.py --towns towns_full.txt --out restaurants_full.csv --max-pages 3
python3 filter_chains.py
python3 find_emails.py --limit 0 --out found_emails_full.csv --commit-every 200
```
