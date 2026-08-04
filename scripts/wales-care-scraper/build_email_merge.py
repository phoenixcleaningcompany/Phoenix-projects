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

SUBJECT_TEMPLATE = "LEV testing / TR19 compliance — {site_label}"
BODY_TEMPLATE = """Hi there,

I run Phoenix Duct Clean — TR19 kitchen extraction cleaning and LEV/COSHH testing for care homes and nurseries across the UK, 15+ years doing it.

Two things I find get missed at sites like {site_label}:
- LEV testing is a legal requirement enforced by the HSE under COSHH, not just best practice.
- TR19 kitchen extraction cleaning is tied to fire risk assessments and insurance validity under the Fire Safety Order 2005 -- a missing certificate is a common reason a fire claim gets challenged.

If it's due, or you're not sure when it was last done, happy to send a no-obligation price. Every clean comes with a dated certificate, before/after photos, and an access report -- no hidden extras, no out-of-hours charge.

Worth a reply either way, even if it's "not needed right now."

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
