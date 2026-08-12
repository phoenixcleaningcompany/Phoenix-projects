# Launderettes — 3-Email Sequence

For `scripts/launderette-scraper/mailchimp_contacts.csv` (437 unique contacts, Wales + England). Direct-buyer pitch, laundry duct cleaning only — this trade runs banks of commercial tumble dryers venting almost continuously, and lint-laden ductwork is one of the most common, well-documented causes of commercial laundry fires. Same educational-listicle tone as the pub/care home sequences (independent small-business owner-operators, not portfolio professionals who already know the compliance landscape).

Laundry duct only — no kitchen extraction content, this trade has no commercial kitchen to speak of.

`*|SITE|*` merge tag in subjects only, same convention as the other sequences.

Cadence: Email 1 → wait 10-14 days, no reply → Email 2 → wait 10-14 days, no reply → Email 3.

---

## Email 1 — "What insurers check after a commercial laundry fire"

Subject: What insurers check after a commercial laundry fire — *|SITE|*

Hi there,

I'm Damien, I run Phoenix Duct Clean — laundry duct and dryer vent cleaning for commercial laundries across the UK, 15+ years doing it. Thought this might be worth knowing regardless of whether we ever work together.

Things that commonly get checked after a commercial dryer/laundry fire claim:

1. When the dryer exhaust ductwork was last properly cleaned, and by whom
2. Records showing lint traps were cleared regularly, not just occasionally
3. A fire risk assessment that's actually been reviewed recently, not just filed away
4. Whether the ducting run itself (not just the lint trap on the machine) had ever been inspected
5. Fire extinguishers and fire blankets present, in date, and positioned correctly near the dryers
6. No unrecorded alterations to ducting or ventilation since the last check
7. Evidence that previous fire risk assessment recommendations were actually acted on

Number 1 is where I come in. A launderette running several dryers most of the day builds up duct lint far faster than a domestic setup ever would, and it's one of the most common causes of commercial laundry fires — the lint trap on the machine only catches a fraction of it, the rest collects in the ducting itself over time.

If you're not sure when your dryer ductwork was last properly cleaned rather than just the lint trap emptied, happy to take a look and give you a no-obligation price.

Damien
Phoenix Duct Clean
07961 915018 / officeductclean@gmail.com
phoenixductclean.com

---

## Email 2 — "Landlord or tenant: who's responsible?" (10-14 days later, no reply)

Subject: Landlord or tenant — whose job is duct cleaning? — *|SITE|*

Hi there,

Following up from my last note — a different angle this time.

If you're in a leased unit, it's genuinely common for it to be unclear whether the extraction ductwork is the landlord's responsibility or yours as tenant — it depends on what's actually written into the lease, and in practice that gets missed by both sides more often than you'd think.

Worth two minutes checking your lease if you're not certain. If it turns out it's on you, or it's just easier for you to sort directly rather than chase a landlord, I'm happy to quote either way. And if you're part of a chain or run more than one site, I also work with owners directly across multiple sites on one schedule, if that's more useful.

Damien
Phoenix Duct Clean
07961 915018 / officeductclean@gmail.com

---

## Email 3 — "Lint builds up faster than most people think" (10-14 days after Email 2)

Subject: How fast lint actually builds up in a commercial dryer duct — *|SITE|*

Hi there,

Last email from me on this — after this I'll leave it, no more chasing.

A single domestic tumble dryer duct can build up a fire risk over months of use. A launderette running several commercial dryers most hours of the day builds up the same risk in a fraction of the time — and because the ducting is often out of sight above a suspended ceiling or behind a wall, it's easy for it to go unchecked for years without anyone noticing.

If it's been a while since your dryer ductwork had a proper clean rather than just the lint traps emptied, I'm easy to find: 07961 915018 or officeductclean@gmail.com. No pressure either way.

All the best,
Damien
Phoenix Duct Clean

---

## Notes
- Leads with the insurance/fire-risk angle throughout, same reasoning as the pubs sequence — this audience won't have encountered a TR19-style named standard for laundry duct cleaning specifically, so the insurance/RRFSO 2005 consequence is the sharpest available lever, not a named compliance certificate.
- Roughly 400 of the 3,333 unique businesses found were excluded as national chains (Revolution Laundry, Timpson, Johnsons Cleaners, and Elis — a large B2B industrial linen company that isn't a public launderette at all despite matching the search). See `scripts/launderette-scraper/filter_chains.py` for the exact list.
- One further name got trimmed at the final list stage: a Tesco store's generic customer-service address matched the search by mistake and was removed manually.
- Plain text, no images/attachments, same reasoning as every other sequence in this repo.
