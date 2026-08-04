# Wales care/nursery/boarding-school target list

## Source
`wales_ciw_export.csv` is the official public bulk data export from Care
Inspectorate Wales: https://digital.careinspectorate.wales/directory/search
-> "Download this data" (served at `/api/DataExport`). It's a full snapshot
of every service CIW regulates, refreshed by CIW periodically — re-download
it for a current copy rather than reusing an old one for long.

No scraping or browser automation was needed — CIW publishes this file
directly for exactly this kind of use.

## What `build_target_list.py` does
Filters the export to the three service types relevant to TR19/kitchen
extraction/LEV/laundry duct work (Care Home Service, Childrens Day Care,
Boarding School — 3,169 of 5,062 total Welsh services), then splits into:

- **`independent_and_small_chain.csv`** (2,004 rows, ~95% with email, ~96%
  with phone) — providers with 5 or fewer relevant sites in Wales, and not
  named as a council/local authority. This is the direct cold-outreach list
  — decision sits with the site/registered manager (see OUTREACH_TEMPLATES.md).
- **`large_chains_and_local_authorities.csv`** (1,165 rows) — providers
  above that threshold, or local-authority-run services. These fit the
  facilities-manager relationship motion in OUTREACH_TARGET_LIST.md, not a
  mass individual-site email blast — a chain the size of HC-One should be
  approached once, centrally, not site-by-site.

## Known caveats — read before mass-emailing
- **Site size isn't filtered.** The list includes very small operations —
  e.g. 3-bed supported-living homes — that likely don't have a commercial
  kitchen worth a TR19 clean. `Maximum No. of Places` is included as a
  column specifically so this can be filtered in Excel/Sheets before
  sending anything (e.g. exclude anything under ~10-15 places, adjust to
  taste).
- **The chain/independent split (threshold of 5 Welsh sites) is a judgment
  call**, not an authoritative business classification — spot-check a
  sample before a full send.
- **Email deliverability at volume**: see the caution in OUTREACH_TARGET_LIST.md
  about not blasting thousands from a personal Gmail address at once —
  batch sends.
- **This is Wales only.** England needs the CQC API (requires a free key —
  see OUTREACH_TARGET_LIST.md) and, separately, Ofsted's Early Years
  register for English nurseries.

## Re-running
```
curl -sS -o wales_ciw_export.csv https://digital.careinspectorate.wales/api/DataExport
python3 build_target_list.py
```
