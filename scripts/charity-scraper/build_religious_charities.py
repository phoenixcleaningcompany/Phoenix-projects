#!/usr/bin/env python3
"""
Builds a target list of "Religious Activities" registered charities
(England & Wales) from the Charity Commission's official public bulk data
extract (https://register-of-charities.charitycommission.gov.uk/register/full-register-download,
served from Azure blob storage, updated daily, no API key needed).

This covers Church of England parishes (each parish's Parochial Church
Council is a separate registered charity), Catholic parishes, the
Salvation Army, and other faith venues -- broader than just "churches",
which is useful since many of these run halls with kitchens for community
events, lunches, and functions.

Requires two files already downloaded to /tmp:
  /tmp/charity_extract/publicextract.charity.json
  /tmp/charity_class_extract/publicextract.charity_classification.json
(re-download both from the URLs above if missing/stale -- the register is
updated daily, so re-fetch for a current copy.)
"""
import csv
import ijson

CHARITY_FILE = "/tmp/charity_extract/publicextract.charity.json"
CLASS_FILE = "/tmp/charity_class_extract/publicextract.charity_classification.json"
TARGET_CLASSIFICATION = "Religious Activities"


def get_religious_charity_numbers():
    numbers = set()
    with open(CLASS_FILE, "rb") as f:
        f.read(3)  # UTF-8 BOM
        for obj in ijson.items(f, "item"):
            if obj.get("classification_description") == TARGET_CLASSIFICATION:
                numbers.add(obj["registered_charity_number"])
    return numbers


def main():
    religious_numbers = get_religious_charity_numbers()
    print(f"Charity numbers classified '{TARGET_CLASSIFICATION}': {len(religious_numbers)}")

    rows = []
    with open(CHARITY_FILE, "rb") as f:
        f.read(3)
        for obj in ijson.items(f, "item"):
            if obj.get("charity_registration_status") != "Registered":
                continue
            if obj["registered_charity_number"] not in religious_numbers:
                continue
            rows.append({
                "Name": obj.get("charity_name") or "",
                "Address1": obj.get("charity_contact_address1") or "",
                "Address2": obj.get("charity_contact_address2") or "",
                "Town": obj.get("charity_contact_address4") or "",
                "Postcode": obj.get("charity_contact_postcode") or "",
                "Phone": obj.get("charity_contact_phone") or "",
                "Email": obj.get("charity_contact_email") or "",
                "Website": obj.get("charity_contact_web") or "",
                "CharityNumber": obj["registered_charity_number"],
            })

    fieldnames = ["Name", "Address1", "Address2", "Town", "Postcode", "Phone", "Email", "Website", "CharityNumber"]
    with open("religious_charities.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    has_email = sum(1 for r in rows if r["Email"])
    has_phone = sum(1 for r in rows if r["Phone"])
    print(f"Registered religious-activity charities: {len(rows)}")
    print(f"With email: {has_email} ({has_email/len(rows):.0%})")
    print(f"With phone: {has_phone} ({has_phone/len(rows):.0%})")


if __name__ == "__main__":
    main()
