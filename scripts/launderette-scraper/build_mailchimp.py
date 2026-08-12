#!/usr/bin/env python3
"""
Builds the Mailchimp-ready contact list from found_emails_full.csv: dedupes
by lowercased email address, merges site names for an email shared across
multiple listed sites.
"""
import csv
from collections import defaultdict

SOURCE = "found_emails_full.csv"
OUT = "mailchimp_contacts.csv"


def site_label(sites):
    sites = list(dict.fromkeys(sites))  # dedupe, keep order
    if len(sites) == 1:
        return sites[0]
    if len(sites) == 2:
        return f"{sites[0]} and {sites[1]}"
    return f"{sites[0]} and {len(sites) - 1} other launderettes"


def main():
    by_email = defaultdict(list)
    with open(SOURCE, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            email = r["Email"].strip().lower()
            if not email:
                continue
            by_email[email].append(r)

    rows = []
    for email, recs in by_email.items():
        sites = [r["Name"] for r in recs]
        phone = next((r["Phone"] for r in recs if r["Phone"]), "")
        town = next((r["Town"] for r in recs if r["Town"]), "")
        country = next((r["Country"] for r in recs if r["Country"]), "")
        rows.append({
            "Email Address": email,
            "SITE": site_label(sites),
            "PHONE": phone,
            "TOWN": town,
            "COUNTRY": country,
            "SITECOUNT": len(set(sites)),
        })

    rows.sort(key=lambda r: r["Email Address"])
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Email Address", "SITE", "PHONE", "TOWN", "COUNTRY", "SITECOUNT"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Unique contacts: {len(rows)}")


if __name__ == "__main__":
    main()
