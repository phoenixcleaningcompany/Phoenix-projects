# Wales Cold Outreach — 3-Email Sequence (v2: value-led)

For the independent/small-chain list (`scripts/wales-care-scraper/independent_and_small_chain.csv` / `mailchimp_contacts.csv`). Plain text only — no images, no attachments, no HTML template. For a first cold email to an unfamiliar recipient, plain text clears spam/security gateways (Mimecast, Proofpoint — common on school/council/NHS-linked domains) far more reliably than anything image- or attachment-heavy, and reads as a real person rather than a marketing platform. Save the designed HTML material (offer email, extraction-clean explainer, trust page) for warm leads who've already replied or been quoted.

Sending plan: manual send across 2 Gmail + 1 Yahoo business accounts, ~300/day comfortably. Still worth a smaller first-day test (e.g. 100-150 across the three accounts) before running the full batch, to catch any bounce/spam-complaint pattern early — same logic as the rugby club test.

Cadence: Email 1 → wait 10-14 days, no reply → Email 2 → wait 10-14 days, no reply → Email 3. Stop the moment someone replies, quotes, or asks to be left alone.

If you publish the fuller version of each list as a page on phoenixductclean.com, link to it from the email ("full checklist: phoenixductclean.com/...") instead of attaching anything — safer for deliverability, and it gives the new site real content to get indexed on.

---

## Email 1 — "10 things health inspectors always look for"

Subject: 10 things an EHO checks in a commercial kitchen — *|SITE|*

Hi there,

I'm Damien, I run Phoenix Duct Clean — TR19 kitchen extraction cleaning and LEV/COSHH testing, 15+ years doing it for care homes and nurseries across the UK. Thought this might be useful regardless of whether we ever work together.

Ten things an Environmental Health Officer is actually looking at during a food hygiene inspection:

1. Fridge/freezer temperatures and evidence of proper monitoring
2. Date labelling and stock rotation
3. Handwashing facilities and staff hygiene practices
4. Cleaning schedules and records for equipment and surfaces
5. Signs of pests, and how well the kitchen is proofed against them
6. Condition and cleanliness of the extraction canopy, filters and ductwork
7. Structural condition — walls, floors, ceilings, are they intact and cleanable
8. Waste storage and disposal, kept away from food prep
9. Allergen information and how it's managed
10. A documented food safety management system (e.g. Safer Food Better Business)

Number 6 is the one that gets missed most, because most of it is out of sight above the canopy. A greasy extraction system can count against your food hygiene rating at inspection, separately from the fire-safety side of things.

If it's been a while since *|SITE|*'s extraction system was properly cleaned (not just wiped down), happy to have a look and give you a no-obligation price. Every clean comes with a dated TR19 certificate, before/after photos, and an access report.

Damien
Phoenix Duct Clean
07961 915018 / officeductclean@gmail.com
phoenixductclean.com

---

## Email 2 — "What you're actually paying for" (10-14 days later, no reply)

Subject: Kitchen extraction cleaning — what's actually included — *|SITE|*

Hi there,

Following up from my last note. Thought I'd explain what a proper TR19 extraction clean actually covers, since "duct cleaning" gets used loosely and it's not always clear what you're paying for.

One system, cleaned end to end — not just the visible canopy:
- Canopy stripped inside and out
- Baffle filters cleaned or replaced
- Plenum (the hidden grease trap most people don't know exists) cleared
- Ductwork cleaned via access hatches along its full run
- Extractor fan degreased, pull restored

The process: survey (inspect and agree scope based on how hard the kitchen runs), strip (filters and panels removed, cookline protected), degrease (canopy to fan, by hand, with before/after photos at each section), certify (dated TR19 certificate plus a next-due date for the fire logbook).

Why it's worth doing properly: a greasy duct is a genuine fire risk under the Fire Safety Order 2005, insurers and EHOs specifically look for a current certificate, and a clean system runs cooler and pulls less power for the same result.

How often it's actually needed comes down to cooking hours, not a fixed calendar date — heavy use (12+ hrs/day) is roughly every 3 months, moderate (6-12 hrs) roughly every 6, light (2-6 hrs) roughly every 12.

If *|SITE|* isn't sure which band it's in or when it was last done properly, happy to take a look — no obligation.

Damien
Phoenix Duct Clean
07961 915018 / officeductclean@gmail.com

---

## Email 3 — "10 hidden risks in a care home" (10-14 days after Email 2)

Subject: 10 hidden risks in a care home — *|SITE|*

Hi there,

Last email from me on this — after this I'll leave it, no more chasing.

Ten things that tend to get missed in a care home because they're out of sight, out of a routine inspection, or just easy to forget:

1. Grease-laden kitchen extraction ductwork — a well-documented way a small kitchen fire spreads fast through a building
2. Lint build-up inside laundry extraction ducts — same fire mechanism, same "nobody sees it" problem
3. LEV systems overdue their statutory COSHH test (a legal HSE requirement, not optional)
4. Fire doors that don't self-close properly, or get wedged open in practice
5. Fire escape routes that have quietly become obstructed
6. Emergency lighting that's failed and nobody knows until a power cut
7. Legionella risk in water outlets that aren't used often
8. Portable appliance (PAT) testing that's lapsed
9. A fire risk assessment that hasn't been reviewed since the last change in layout or resident needs
10. Compliance certificates that turn out to be missing at the exact moment an insurer asks for them after a claim

Numbers 1 and 3 are where I can actually help — TR19 kitchen extraction cleaning and LEV/COSHH testing, done properly, with paperwork that holds up. If either is worth checking at *|SITE|*, I'm easy to find: 07961 915018 or officeductclean@gmail.com. No pressure either way.

All the best,
Damien
Phoenix Duct Clean

---

## Notes
- `*|SITE|*` is the Mailchimp merge tag from `mailchimp_contacts.csv`; if sending manually, substitute the service name by hand or with a simple mail-merge tool.
- Don't use the McDonald's/AWS/BaxterStorey "trusted by" claims here — confirmed genuine, but they belong on warm/trust-stage material, not a cold-open (see conversation for why).
- Nothing in these three emails is an attachment or image — keep it that way for this stage.
- If a recipient replies with any interest, that's the point to switch to the polished HTML material (offer, extraction-clean-explained, trust page) — those are built for exactly that stage.
