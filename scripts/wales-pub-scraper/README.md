# Wales pubs — Google Places API pipeline

## Source
Same approach as `scripts/wales-restaurant-scraper/`: Google Places API
(New), Text Search, queried as "pubs in {town}, Wales" for all 216 towns.

## Pipeline
1. `fetch_pubs.py` — 3,568 raw results, 70% with website, 294 API requests.
2. `filter_chains.py` — dedupes by (Name, Address) to 2,868 unique pubs,
   then filters chains **by keyword match, not name-repeat count** (see
   below for why) — 28 genuine chain locations excluded, **2,840
   independent/small pubs remain, 1,971 with website.**
3. `find_emails.py` — same website-scraping approach as every other list
   — **838 emails found (43% hit rate)**.
4. Deduped by email → **`mailchimp_contacts.csv`, 729 unique recipients.**

## Why the restaurant chain-filter method doesn't work for pubs
The restaurant list used a name-repeat count (a name appearing at 4+
distinct addresses = chain). That fails badly for pubs in both directions:
- **False positives**: traditional pub names (Red Lion, Farmers Arms,
  Royal Oak, Swan Inn, White Lion, Castle Inn) repeat constantly across
  genuinely unrelated independent pubs — nothing to do with a real chain,
  just common historic naming. The name-repeat method flagged ~112 pubs
  this way before the fix.
- **False negatives**: real UK pub-restaurant chains (Toby Carvery,
  Harvester, Brewers Fayre, Marston's Inns) usually give each location a
  distinct name ("Harvester Gowerton" vs "Harvester Pontypool"), so they
  never repeat exactly and were missed entirely by a repeat-count filter.

`filter_chains.py` instead matches a keyword list of known UK chain
brands (Wetherspoon, Toby Carvery, Beefeater, Brewers Fayre, Marston's
Inns, Harvester, Hungry Horse, etc.) directly against the name. This is
still a judgment-call list, not exhaustive — spot-check before a full
send, same caveat as everywhere else in this repo.

## Caveats
- Not filtered for the "avoid heavy-use/12+ hour food service" preference
  from the original brief — same caveat as the restaurant list.
- Chain keyword list may miss smaller/regional chains not included in it.

## Re-running
```
export PLACES_API_KEY=xxx
python3 fetch_pubs.py --towns towns_full.txt --out pubs_full.csv --max-pages 3
python3 filter_chains.py
python3 find_emails.py --limit 0 --out found_emails_full.csv --commit-every 100
```
