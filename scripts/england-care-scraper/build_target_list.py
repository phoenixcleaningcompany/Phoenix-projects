#!/usr/bin/env python3
"""
Builds an England outreach target list from CQC's official bulk directory
CSV (https://www.cqc.org.uk/about-us/transparency/using-cqc-data -- updated
~weekly/monthly, no API key needed for this file specifically).

Note: unlike the Wales (CIW) export, this file has NO email address column
-- only phone number and (sometimes) a website. Outreach against this list
has to be phone-first, or website-lookup for email on a per-site basis.

CQC regulates health & social care -- it does NOT cover day nurseries/early
years childcare in England (that's Ofsted's Early Years register, a
separate dataset not fetched here).

Filters to 'Residential homes' and 'Nursing homes' (the CQC service types
equivalent to Wales' 'Care Home Service'), then splits into:
  - independent_and_small_chain.csv: providers with a small number of
    English sites -> direct cold outreach
  - large_chains_and_local_authorities.csv: bigger providers or councils ->
    facilities-manager relationship motion instead (see OUTREACH_TARGET_LIST.md)
"""
import csv
from collections import Counter
from io import StringIO

SOURCE_CSV = "cqc_directory.csv"
HEADER_LINE_INDEX = 4  # first 4 lines are title/blank/date/blank
RELEVANT_TYPES = {"Residential homes", "Nursing homes"}
CHAIN_THRESHOLD = 5
LOCAL_AUTHORITY_MARKERS = ("council", "county borough", "city and county", "county council")

OUTPUT_COLUMNS = [
    "Name", "Address", "Postcode", "Phone number", "Service's website (if available)",
    "Service types", "Local authority", "Region", "Provider name",
]


def is_local_authority(provider_name: str) -> bool:
    name = provider_name.lower()
    return any(marker in name for marker in LOCAL_AUTHORITY_MARKERS)


def main():
    with open(SOURCE_CSV, encoding="utf-8-sig", errors="replace") as f:
        lines = f.readlines()
    data = "".join(lines[HEADER_LINE_INDEX:])
    rows = list(csv.DictReader(StringIO(data)))

    relevant = [
        r for r in rows
        if RELEVANT_TYPES & {t.strip() for t in r["Service types"].split("|")}
    ]
    provider_counts = Counter(r["Provider name"] for r in relevant)

    independent, chains = [], []
    for r in relevant:
        provider = r["Provider name"].strip()
        is_chain = provider_counts[r["Provider name"]] > CHAIN_THRESHOLD
        is_la = is_local_authority(provider)
        (chains if (is_chain or is_la) else independent).append(r)

    def write(path, records):
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=OUTPUT_COLUMNS, extrasaction="ignore")
            writer.writeheader()
            for r in records:
                writer.writerow(r)

    write("independent_and_small_chain.csv", independent)
    write("large_chains_and_local_authorities.csv", chains)

    has_phone = sum(1 for r in independent if r["Phone number"].strip())
    has_website = sum(1 for r in independent if r["Service's website (if available)"].strip())

    print(f"Relevant services total: {len(relevant)}")
    print(f"Independent/small-chain (direct outreach): {len(independent)}")
    print(f"  - with phone: {has_phone} ({has_phone/len(independent):.0%})")
    print(f"  - with website: {has_website} ({has_website/len(independent):.0%})")
    print(f"Large chains / local authorities: {len(chains)}")


if __name__ == "__main__":
    main()
