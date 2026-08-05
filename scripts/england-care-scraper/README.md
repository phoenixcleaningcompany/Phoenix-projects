# England care/nursing home target list

## Source
`cqc_directory.csv` is CQC's official bulk directory download, published
~weekly/monthly at https://www.cqc.org.uk/about-us/transparency/using-cqc-data
(direct link changes each release — re-fetch for a current copy). This
specific file needs no API key; it's a plain public CSV.

The CQC Syndication API key you got is still useful for supplementary
per-location lookups (ratings, inspection history, changes-since-date) if
that's ever wanted, but wasn't needed to build this list.

## Important gap: no email addresses, and no nurseries
Two differences from the Wales (CIW) list, worth knowing before treating
this the same way:
- **No email column at all** in this CQC file — only phone number and
  (for about half of records) a website. Outreach against this list has to
  be **phone-first**, or a manual/semi-automated per-site website lookup for
  an email address, not a straight mail-merge like Wales.
- **CQC doesn't regulate day nurseries/early years childcare in England** —
  that's Ofsted's Early Years register, a separate dataset not fetched here.
  This list is care/nursing homes only.

## What `build_target_list.py` does
Filters to `Residential homes` and `Nursing homes` (14,899 of 56,976 total
CQC-regulated locations — equivalent to Wales' "Care Home Service"), then
splits by the same logic as Wales:

- **`independent_and_small_chain.csv`** (9,032 rows, 96% with phone, 50%
  with a website) — providers with 5 or fewer relevant English sites, not
  a council. Direct outreach, decision sits with the site/registered
  manager.
- **`large_chains_and_local_authorities.csv`** (5,867 rows) — bigger
  providers or council-run homes. Facilities-manager relationship motion,
  not a mass call/email — see OUTREACH_TARGET_LIST.md.

## Caveats carried over from the Wales list
- Chain/independent split (>5 English sites = chain) is a judgment call —
  spot-check before committing to it at scale.
- No site-size filter — this list isn't narrowed by number of beds, so it
  may include very small homes with a domestic-scale kitchen rather than a
  commercial one worth a TR19 clean.

## Re-running
Find the current file link on the "Using CQC data" page (search the page
HTML for `CQC_directory.csv`), download it, then:
```
python3 build_target_list.py
```
