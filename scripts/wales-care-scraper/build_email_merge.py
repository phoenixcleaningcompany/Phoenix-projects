#!/usr/bin/env python3
"""
Builds a mail-merge-ready CSV for Email 1 of WALES_COLD_EMAIL_SEQUENCE.md,
from independent_and_small_chain.csv.

Dedupes by email address first: 1,894 rows have a plausible email, but only
1,660 are unique inboxes (153 addresses run more than one site -- 387 rows).
Sending each of those the same email once per site would look like a spam
blast to the one person managing them, so this collapses them into a single
row with a natural site_label ("X" / "X and Y" / "X and 4 other services").

Output: email_merge_batch1.csv, ready for a mail-merge tool (Gmail + a Sheets
add-on such as Yet Another Mail Merge, which respects Gmail's daily send
limits and tracks opens/replies -- do not send this many manually one by one).
"""
import csv
from collections import defaultdict

SOURCE = "independent_and_small_chain.csv"
OUTPUT = "email_merge_batch1.csv"

# Matches WALES_COLD_EMAIL_SEQUENCE.md v3, Email 1. Subject personalizes with
# site_label; body deliberately uses "your site" instead, so nothing needs
# manual editing if these get sent outside a merge tool.
SUBJECT_TEMPLATE = "10 things an EHO checks in a commercial kitchen — {site_label}"
BODY_TEMPLATE = """Hi there,

I'm Damien, I run Phoenix Duct Clean — TR19 kitchen extraction cleaning and laundry duct cleaning, 15+ years doing it for care homes, nursing homes and nurseries across the UK. Thought this might be useful regardless of whether we ever work together.

Ten things an Environmental Health Officer is actually looking at during a food hygiene inspection:

1. Fridge/freezer temperatures and evidence of proper monitoring
2. Date labelling and stock rotation
3. Handwashing facilities and staff hygiene practices
4. Cleaning schedules and records for equipment and surfaces
5. Signs of pests, and how well the kitchen is proofed against them
6. Condition and cleanliness of the extraction canopy, filters and ductwork
7. Structural condition -- walls, floors, ceilings, are they intact and cleanable
8. Waste storage and disposal, kept away from food prep
9. Allergen information and how it's managed
10. A documented food safety management system (e.g. Safer Food Better Business)

Number 6 is the one that gets missed most, because most of it is out of sight above the canopy. A greasy extraction system can count against your food hygiene rating at inspection, separately from the fire-safety side of things.

If it's been a while since your site's extraction system was properly cleaned (not just wiped down) -- or your laundry extraction duct, if you run an on-site laundry -- happy to have a look and give you a no-obligation price. Every clean comes with a dated certificate, before/after photos, and an access report.

Damien
Phoenix Duct Clean
07961 915018 / officeductclean@gmail.com
phoenixductclean.com
"""


def site_label(names):
    names = list(dict.fromkeys(names))  # de-dup, keep order
    if len(names) == 1:
        return names[0]
    if len(names) == 2:
        return f"{names[0]} and {names[1]}"
    return f"{names[0]} and {len(names) - 1} other services you run"


def main():
    with open(SOURCE, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    by_email = defaultdict(list)
    for r in rows:
        email = r["Primary email address"].strip().lower()
        if email and "@" in email:
            by_email[email].append(r)

    with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["email", "site_label", "site_count", "local_authority", "subject", "body"])
        for email, recs in sorted(by_email.items()):
            names = [r["Service Name"] for r in recs]
            label = site_label(names)
            subject = SUBJECT_TEMPLATE.format(site_label=label)
            body = BODY_TEMPLATE.format(site_label=label)
            writer.writerow([email, label, len(recs), recs[0]["Local Authority"], subject, body])

    print(f"Unique recipients written: {len(by_email)}")


if __name__ == "__main__":
    main()
