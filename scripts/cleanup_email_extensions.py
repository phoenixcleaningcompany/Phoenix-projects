#!/usr/bin/env python3
"""
Shared cleanup: removes emails whose domain suffix isn't a standard,
recognized TLD -- fixes the extraction regex bug where things like
logo@2x.png (from responsive image markup: srcset="logo@2x.png") or
sprite@1x.svg got matched as if they were email addresses, since the
regex didn't distinguish a TLD from a file extension.

Usage: python3 cleanup_email_extensions.py <found_emails_full.csv>
Rewrites the file in place, blanking Email/"Found on page" for anything
that fails the allowlist. Run rebuild_mailchimp.py after this to
regenerate the deduped Mailchimp file from the cleaned data.
"""
import csv
import sys

ALLOWED_TLDS = {
    'com', 'org', 'net', 'biz', 'info', 'me', 'uk',
    'co.uk', 'org.uk', 'net.uk', 'ltd.uk', 'plc.uk', 'gov.uk', 'ac.uk', 'sch.uk', 'nhs.uk',
}


def valid_email_tld(email):
    email = email.lower()
    if email.count('@') != 1:
        return False
    domain = email.split('@', 1)[1]
    parts = domain.split('.')
    if len(parts) < 2:
        return False
    two_label = '.'.join(parts[-2:])
    one_label = parts[-1]
    return two_label in ALLOWED_TLDS or one_label in ALLOWED_TLDS


def main():
    path = sys.argv[1]
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    before = sum(1 for r in rows if r.get('Email', '').strip())
    removed = []
    for r in rows:
        email = r.get('Email', '').strip()
        if email and not valid_email_tld(email):
            removed.append(email)
            r['Email'] = ''
            if 'Found on page' in r:
                r['Found on page'] = ''

    after = sum(1 for r in rows if r.get('Email', '').strip())
    print(f"{path}: {before} -> {after} emails ({len(removed)} removed)")
    if removed[:8]:
        print("  sample removed:", removed[:8])

    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
