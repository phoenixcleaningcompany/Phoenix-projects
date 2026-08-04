#!/usr/bin/env python3
"""
Builds a Wales outreach target list from the official CIW public data export
(https://digital.careinspectorate.wales/directory/search -> "Download this data" -> /api/DataExport).

Filters to service types relevant to TR19 kitchen extraction, LEV testing and
laundry duct cleaning (care homes, children's day care, boarding schools),
then splits into:
  - independent_and_small_chain.csv: providers with a small number of Welsh
    sites -> direct cold outreach to the site/registered manager
  - large_chains_and_local_authorities.csv: providers above the site-count
    threshold, or named as a council/local authority -> better suited to the
    facilities-manager relationship motion (see OUTREACH_TARGET_LIST.md),
    not a mass individual-site email blast

CHAIN_THRESHOLD and the local-authority name match are judgment calls, not
absolute science. Note that CQC/Ofsted covers England; this is Wales-only.
"""
import csv
from collections import Counter

SOURCE_CSV = "wales_ciw_export.csv"
RELEVANT_TYPES = {"Care Home Service", "Childrens Day Care", "Boarding School"}
CHAIN_THRESHOLD = 5  # providers with more than this many relevant WALES sites are treated as a "chain"
LOCAL_AUTHORITY_MARKERS = ("council", "county borough", "city and county")

OUTPUT_COLUMNS = [
    "Service Name", "Service Type", "Service Sub-Type", "Provision For",
    "Service Address Line 1", "Service Address Line 2", "Service Town/City",
    "Service Postcode", "Local Authority", "Maximum No. of Places",
    "Primary telephone number", "Primary email address", "Website",
    "Provider Name", "Provider No. of Approved Services",
]


def is_local_authority(provider_name: str) -> bool:
    name = provider_name.lower()
    return any(marker in name for marker in LOCAL_AUTHORITY_MARKERS)


def main():
    with open(SOURCE_CSV, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))

    relevant = [r for r in rows if r["Service Type"] in RELEVANT_TYPES]
    provider_counts = Counter(r["Provider Name"] for r in relevant)

    independent, chains = [], []
    for r in relevant:
        provider = r["Provider Name"].strip()
        is_chain = provider_counts[r["Provider Name"]] > CHAIN_THRESHOLD
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

    has_email = sum(1 for r in independent if r["Primary email address"].strip())
    has_phone = sum(1 for r in independent if r["Primary telephone number"].strip())

    print(f"Relevant services total: {len(relevant)}")
    print(f"Independent/small-chain (direct outreach): {len(independent)}")
    print(f"  - with email: {has_email} ({has_email/len(independent):.0%})")
    print(f"  - with phone: {has_phone} ({has_phone/len(independent):.0%})")
    print(f"Large chains / local authorities (separate motion): {len(chains)}")


if __name__ == "__main__":
    main()
