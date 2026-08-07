# Religious Charities — 3-Email Sequence (3 segments, shared template)

For the filtered/segmented lists in `scripts/charity-scraper/`:
- `mailchimp_christian_default.csv` — 14,897 unique recipients (churches, chapels, parishes, cathedrals, abbeys, convents, monasteries)
- `mailchimp_other_faith.csv` — 1,081 unique recipients (mosques, Islamic centres, synagogues, gurdwaras, Hindu/Buddhist/Sikh venues)
- `mailchimp_uniformed_youth.csv` — 294 unique recipients (Scout, Guide, Cadet, Brigade groups)

19,825 of the original 39,166 charity entries were filtered out first as noise — restricted funds/bequests/trusts named after a historic benefactor with no physical premises (e.g. "STAPLEY BEQUEST"), not real outreach targets. See `filter_and_segment.py` for the exact heuristic.

Only kitchen extraction is pitched here, not laundry duct — halls in this category don't typically run commercial laundries. Plain text only, same reasoning as every other sequence: clears spam/security filters better than HTML on a first cold contact, reads as a real person.

Emails 2 and 3 are near-identical across all three segments (just the word for the venue changes); Email 1 is genuinely different per segment since that's where first-contact context matters most.

`*|SITE|*` merge tag in subjects only, same convention as the other sequences.

---

## Email 1 — Initial contact (segment-specific)

### Christian churches/chapels/parishes/abbeys

Subject: Kitchen extraction cleaning for your hall — *|SITE|*

Hi there,

I'm Damien, I run Phoenix Duct Clean — TR19 kitchen extraction cleaning for church, chapel and parish halls across the UK, 15+ years doing it.

If your hall runs coffee mornings, lunch clubs, harvest suppers, or community meals, the kitchen extraction system is doing more work than it might look like — and it's easy for a volunteer-run hall to lose track of when it was last properly cleaned, if ever. A greasy extraction system is a genuine fire risk, and it's the kind of thing that only gets noticed after something's gone wrong.

Happy to give a no-obligation price if it's worth checking. Every clean comes with a dated certificate, before/after photos, and an access report.

Damien
Phoenix Duct Clean
07961 915018 / officeductclean@gmail.com
phoenixductclean.com

### Other faith venues (mosques, Islamic centres, synagogues, gurdwaras, Hindu/Buddhist/Sikh)

Subject: Kitchen extraction cleaning for your centre — *|SITE|*

Hi there,

I'm Damien, I run Phoenix Duct Clean — TR19 kitchen extraction cleaning for community and faith centres across the UK, 15+ years doing it.

If your centre's kitchen is used for community meals or shared events, the extraction system is doing more work than it might look like — and it's easy for a volunteer-run centre to lose track of when it was last properly cleaned, if ever. A greasy extraction system is a genuine fire risk, and it's the kind of thing that only gets noticed after something's gone wrong.

Happy to give a no-obligation price if it's worth checking. Every clean comes with a dated certificate, before/after photos, and an access report.

Damien
Phoenix Duct Clean
07961 915018 / officeductclean@gmail.com
phoenixductclean.com

### Scout/Guide/Cadet/Brigade groups

Subject: Kitchen extraction cleaning for your hut/hall — *|SITE|*

Hi there,

I'm Damien, I run Phoenix Duct Clean — TR19 kitchen extraction cleaning for scout huts, guide halls and cadet buildings across the UK, 15+ years doing it.

If your hut or hall has a kitchen used for camps, events, or regular meetings, the extraction system is doing more work than it might look like — and it's easy for a volunteer-run group to lose track of when it was last properly cleaned, if ever. A greasy extraction system is a genuine fire risk, and it's the kind of thing that only gets noticed after something's gone wrong.

Happy to give a no-obligation price if it's worth checking. Every clean comes with a dated certificate, before/after photos, and an access report.

Damien
Phoenix Duct Clean
07961 915018 / officeductclean@gmail.com
phoenixductclean.com

---

## Email 2 — Follow-up (10-14 days later, no reply) — shared, swap [venue]

Subject: Re: Kitchen extraction cleaning for your [hall/centre/hut] — *|SITE|*

Hi there,

Following up on my last note in case it got buried.

Quick version: I clean kitchen extraction systems to TR19 standard, mainly for community and volunteer-run buildings where nobody's specifically responsible for tracking when it was last done. If that sounds like your [hall/centre/hut], happy to give a no-obligation price. If it's already sorted, just let me know and I'll stop chasing.

Damien
Phoenix Duct Clean
07961 915018 / officeductclean@gmail.com

`[hall/centre/hut]` → "hall" for Christian and (informally) other-faith segments, "hut" for the uniformed/youth segment — adjust to match Email 1's wording for that segment.

---

## Email 3 — Final, low-pressure close (10-14 days after Email 2) — shared, swap [venue]

Subject: Last note — kitchen extraction cleaning — *|SITE|*

Hi there,

Last email from me on this — after this I'll leave it, no more chasing.

If your [hall/centre/hut]'s kitchen extraction is ever worth a proper clean, I'm easy to find: 07961 915018 or officeductclean@gmail.com. No pressure either way.

All the best,
Damien
Phoenix Duct Clean

---

## Notes
- Deliberately avoids naming specific religious practices (e.g. langar, iftar) in the "other faith" version, since that segment is a mixed bucket across several different faiths — a term correct for one (e.g. langar for Sikh gurdwaras) would be wrong or confusing for another (mosques, synagogues, Hindu/Buddhist centres) in the same list. Generic "community meals/shared events" is the safer, still-accurate choice across the whole segment.
- The noise filter and segmentation are keyword heuristics, not certain — spot-check a sample from each CSV before a full send, same caveat as the chain/independent splits elsewhere in this repo.
- No laundry duct cleaning pitched in this vertical — not a typical feature of these buildings.
