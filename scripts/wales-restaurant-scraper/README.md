# Wales restaurants — Google Places API pipeline

## Source
Google Places API (New), Text Search endpoint (`places.googleapis.com/v1/places:searchText`),
queried as "restaurants in {town}, Wales" for all 216 towns in `towns_full.txt`
(the user-supplied list of Welsh towns/areas by population). Requires a
Places API (New) key with billing enabled (Google Cloud Console) — not free
data, but cheap: ~512 requests for full 216-town coverage.

## Pipeline
1. `fetch_restaurants.py` — pulls raw results per town (up to 60/town via
   pagination). **9,122 raw rows.**
2. `dedupe_and_filter.py` — dedupes by (Name, Address) since neighboring
   towns' search radii overlap heavily (**4,810 unique restaurants**), then
   filters out names appearing at 4+ distinct addresses nationally as
   probable chains (McDonald's, Pepe's, supermarket cafes, etc. — 92 rows
   excluded). **4,718 independent/small restaurants remain, 78% with website.**
3. `find_emails.py` — same website-scraping approach as the care home
   lists (home/contact/contact-us pages, mailto: + regex email extraction).
   Run against the 3,689 with a website: **1,428 emails found (39% hit
   rate)**, lower than care homes' 49% — many independent restaurants use a
   Facebook page as their "website" rather than a real site with a contact
   address.
4. Deduped by email → **`mailchimp_contacts.csv`, 1,153 unique recipients.**

## Caveats
- **Chain filter is a name-repeat heuristic** (4+ distinct addresses =
  chain) and has real false positives on generic traditional pub/takeaway
  names that aren't actual chains (The Red Lion, White Lion, Royal Oak,
  Farmers Arms, Golden Dragon, Jade Garden) — affects ~2% of the list,
  judged an acceptable tradeoff.
- **No further filtering for the "avoid heavy-use/12+ hour sites" ICP** —
  this list is independent restaurants generally, not screened for
  opening-hours intensity the way the original brief asked to avoid. Worth
  a manual pass before a full send if that distinction matters here.
- Google's search radius for small towns pulled in more results than
  expected (e.g. Tregaron, population ~1,200, returned 11 restaurants,
  likely including surrounding villages) — town boundaries aren't exact.

## Auto-checkpointing
`find_emails.py` for this list includes `--commit-every N` (default 100),
which runs `git add/commit/push` automatically during a run — added after
this environment's container restarted mid-run multiple times and lost
uncommitted progress. Worth carrying this pattern into any future
long-running scrape in this repo rather than relying on manual checkpoints.

## Re-running
```
export PLACES_API_KEY=xxx
python3 fetch_restaurants.py --towns towns_full.txt --out restaurants_full.csv --max-pages 3
python3 dedupe_and_filter.py
python3 find_emails.py --limit 0 --out found_emails_full.csv --commit-every 100
```
