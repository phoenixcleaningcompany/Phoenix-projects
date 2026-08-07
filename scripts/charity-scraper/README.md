# Religious charities (churches, Salvation Army, other faith venues)

## Source
Charity Commission for England & Wales official bulk data extract —
https://register-of-charities.charitycommission.gov.uk/register/full-register-download
(daily extract, JSON, no API key needed, served from Azure blob storage).
Two files used: `publicextract.charity.json` (name/contact/status per
charity) and `publicextract.charity_classification.json` (activity
categories per charity).

This covers every Church of England parish (each parish's Parochial
Church Council is a separate registered charity), Catholic parishes, the
Salvation Army, and other faith venues — broader than just "churches",
which is useful since many run halls with kitchens for community events,
lunches, and functions.

## What `build_religious_charities.py` does
Filters the ~397,826 total charity register entries to the ~185,460 with
`charity_registration_status == "Registered"`, cross-referenced against
the ~51,205 charities classified `"Religious Activities"`, giving
**39,166 registered religious-activity charities** — 80% with email,
94% with phone.

`religious_charities.csv` is the full filtered set (email or not).
`mailchimp_contacts.csv` is deduped by email address (**30,043 unique
recipients**) — the ready-to-send list.

## Salvation Army specifically
Registered as a single national charity (214779), not per-corps — so
this gives one central contact (info@salvationarmy.org.uk / UK
Territorial HQ), not individual corps/centres. If per-location Salvation
Army contacts matter, that needs a different source (their own
"find a church" locator, which is JS-rendered and wasn't cracked — see
the main marketing strategy doc).

## Caveats
- Not filtered by whether the charity actually has a hall/kitchen — this
  includes some small grant-making trusts and endowments alongside real
  physical venues (parish churches, Salvation Army centres, etc.).
  Filtering to entries with an email address already skews toward active,
  real organizations rather than dormant historic trusts, but it's not a
  guarantee.
- No chain/independent split applied (unlike the care home lists) —
  each entry here is already an independent legal charity, there's no
  equivalent of a corporate chain to filter out.
- The register updates daily; re-download both source files for a
  current copy if re-running later.

## Re-running
```
curl -sSL -o /tmp/charity.zip "https://ccewuksprdoneregsadata1.blob.core.windows.net/data/json/publicextract.charity.zip"
curl -sSL -o /tmp/charity_class.zip "https://ccewuksprdoneregsadata1.blob.core.windows.net/data/json/publicextract.charity_classification.zip"
unzip -o /tmp/charity.zip -d /tmp/charity_extract
unzip -o /tmp/charity_class.zip -d /tmp/charity_class_extract
python3 build_religious_charities.py
```
