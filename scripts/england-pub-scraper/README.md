# England pubs — Google Places API pipeline

## Source
Same pipeline as Wales/England restaurants: Google Places API (New), Text
Search, "pubs in {town}, England" for all 446 towns.

## Pipeline
1. `fetch_pubs.py` — 19,964 raw results, 81% with website, 1,110 API
   requests.
2. `filter_chains.py` — dedupes to 19,047 unique, keyword-filters chain
   brands (restaurant chain list plus pub-specific brands: Greene King,
   Marston's Inns, Stonegate, Hungry Horse, Sizzling Pub, Chef & Brewer,
   Craft Union, etc.) — 389 excluded, leaving **18,658 independent/small
   pubs, 80% with website (14,875).**
3. `find_emails.py` — **6,623 emails found (45% hit rate)**, using the
   already-fixed extraction logic (TLD allowlist applied at source, no
   file-extension false positives this time — no cleanup pass needed).
4. Deduped by email → **`mailchimp_contacts.csv`, 5,221 unique recipients.**

## Caveats
- Same as every other pub/restaurant list: chain keyword list is a
  judgment call, not exhaustive; not filtered for the "avoid heavy-use"
  preference from the original brief.
- Ran across multiple container restarts over several hours — checkpointing
  held up throughout, minimal progress lost each time.

## Re-running
```
export PLACES_API_KEY=xxx
python3 fetch_pubs.py --towns towns_full.txt --out pubs_full.csv --max-pages 3
python3 filter_chains.py
python3 find_emails.py --limit 0 --out found_emails_full.csv --commit-every 200
```
