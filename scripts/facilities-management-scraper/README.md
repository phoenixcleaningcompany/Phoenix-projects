# Facilities management companies — IWFM directory

## Source
IWFM (Institute of Workplace and Facilities Management) — the UK trade body
for facilities management, equivalent role to TPI for block management —
publishes a public supplier directory at
https://www.iwfm.org.uk/suppliers.html. Same situation as TPI: plain
server-rendered, paginated (`?category=&region=&page=`), no bot protection,
Cloudflare email-obfuscation decoded via the same standard reversible
algorithm.

## Scope
Categories: **FM Management** and **FM Service Supplier** only — the two
closest to "facilities management companies" as a lead type. Skipped:
Product Supplier, Recruitment, Consultant, End User (not the right kind of
contact for this).

Regions: London, South West, South, North, Midlands, Home Counties, East,
Wales (England/Wales only; Scotland, Ireland, UAE, No Region excluded).

## Result
**78 unique companies, 94% with email, 94% with phone.**

Noticeably smaller than TPI's 370 block management companies — IWFM's
directory is a narrower corporate-supplier listing, not general membership
(IWFM has ~17,000 individual professional members, but that's a different,
inaccessible-to-this-use population, not companies to approach).

## Caveats
- Same as TPI: this is IWFM's directory, not every FM company in the
  country. Non-listed firms won't appear.
- Includes some large national players (e.g. Arcus FM, 4,500+ staff) —
  no chain-size filtering applied given the small overall size (78 doesn't
  need it the way thousands of care homes did).

## Re-running
```
python3 scrape_iwfm.py
```
