#!/usr/bin/env python3
"""
Filters religious_charities.csv down to charities that are plausibly a real
physical venue (has a hall/centre/place-of-worship keyword in the name),
dropping restricted funds/bequests/trusts that have no premises to clean
(e.g. "STAPLEY BEQUEST", "ROBERT VELLERS" -- old ecclesiastical charities
named after a historic benefactor, common in this register).

Then segments the survivors into three groups, since a single generic
email doesn't fit well across this population:
  - uniformed_youth: Scout/Guide/Cadet/Brigade groups (checked first --
    some are church-affiliated and would otherwise match christian_default)
  - other_faith: mosques, Islamic centres, synagogues, gurdwaras, Hindu/
    Buddhist/Sikh venues -- needs faith-neutral wording, not "church hall"
  - christian_default: everything else (the majority -- churches, chapels,
    parishes, cathedrals, abbeys, convents, monasteries)

This is a keyword heuristic, not a certain classification -- spot-check
before a full send, same caveat as the chain/independent splits on the
care home lists.
"""
import csv
from collections import defaultdict, Counter

SOURCE = "religious_charities.csv"

VENUE_KEYWORDS = [
    'CHURCH', 'CHAPEL', 'PARISH', 'CATHEDRAL', 'ABBEY', 'MONASTERY', 'CONVENT',
    'MOSQUE', 'ISLAMIC', 'SYNAGOGUE', 'TEMPLE', 'GURDWARA', 'HINDU', 'BUDDHIST', 'SIKH',
    'HALL', 'CENTRE', 'CENTER', 'MISSION', 'ASSEMBLY', 'FELLOWSHIP', 'TABERNACLE',
    'MEETING HOUSE', 'CONGREGATION', 'SCOUT', 'GUIDE', 'CADET', 'BRIGADE',
]
NOISE_HINTS = ['BELLRINGER', 'BELL FUND', 'CHOIR FUND', 'PRIZE FUND', 'SCHOLARSHIP',
               'APPRENTIC', 'ENDOWMENT OF THE VICARAGE', 'AUGMENTATION']
UNIFORMED = ('SCOUT', 'GUIDE', 'CADET', 'BRIGADE')
OTHER_FAITH = ('MOSQUE', 'ISLAMIC', 'SYNAGOGUE', 'GURDWARA', 'HINDU', 'BUDDHIST', 'SIKH')


def is_real_venue(name: str) -> bool:
    upper = name.upper()
    if any(h in upper for h in NOISE_HINTS) and not any(v in upper for v in ('HALL', 'CENTRE')):
        return False
    return any(kw in upper for kw in VENUE_KEYWORDS)


def classify(name: str) -> str:
    upper = name.upper()
    if any(k in upper for k in UNIFORMED):
        return 'uniformed_youth'
    if any(k in upper for k in OTHER_FAITH):
        return 'other_faith'
    return 'christian_default'


def site_label(names):
    names = list(dict.fromkeys(names))
    if len(names) == 1:
        return names[0]
    if len(names) == 2:
        return f"{names[0]} and {names[1]}"
    return f"{names[0]} and {len(names)-1} other charities"


def main():
    with open(SOURCE, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    filtered = [r for r in rows if is_real_venue(r['Name'])]
    print(f"Before filter: {len(rows)}  |  after noise filter: {len(filtered)}")

    for r in filtered:
        r['segment'] = classify(r['Name'])

    emailable = [r for r in filtered if r['Email'].strip()]
    by_email = defaultdict(list)
    for r in emailable:
        by_email[r['Email'].strip().lower()].append(r)

    per_segment = defaultdict(list)
    for email, recs in sorted(by_email.items()):
        seg = Counter(r['segment'] for r in recs).most_common(1)[0][0]
        label = site_label([r['Name'] for r in recs])
        per_segment[seg].append({
            'Email Address': email, 'SITE': label,
            'PHONE': recs[0]['Phone'], 'POSTCODE': recs[0]['Postcode'],
            'SITECOUNT': len(recs),
        })

    for seg, recs in per_segment.items():
        fname = f"mailchimp_{seg}.csv"
        with open(fname, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=['Email Address', 'SITE', 'PHONE', 'POSTCODE', 'SITECOUNT'])
            writer.writeheader()
            writer.writerows(recs)
        print(f"{seg}: {len(recs)} unique recipients -> {fname}")


if __name__ == "__main__":
    main()
