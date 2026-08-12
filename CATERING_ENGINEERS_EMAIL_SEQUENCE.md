# Catering Engineers / Commercial Kitchen Installers — 3-Email Sequence

For `scripts/england-catering-engineers-scraper/mailchimp_contacts.csv` (531 unique contacts). Different angle from every other sequence in this repo — this audience isn't a direct buyer of extraction cleaning, they're a **referral/subcontract partner**: engineers who install, service and repair commercial catering equipment, and periodically get asked by their own customers to sort extraction cleaning alongside the kitchen work. The pitch is a working relationship, not a one-off sale.

Extraction only — no laundry duct content, this trade has no reason to touch laundry ductwork.

`*|SITE|*` merge tag in subjects only, same convention as the other sequences.

Cadence: Email 1 → wait 10-14 days, no reply → Email 2 → wait 10-14 days, no reply → Email 3.

---

## Email 1 — Initial contact

Subject: A TR19 extraction cleaning partner for your installs and servicing — *|SITE|*

Hi there,

I run Phoenix Duct Clean — TR19 kitchen extraction cleaning across the UK, 15+ years doing it. I'm not a catering equipment company and don't install or sell any of the equipment you work on, so there's no overlap with what you do.

Reason I'm getting in touch: we regularly pick up work referred by catering engineers whose customers need the extraction system properly cleaned and certified — either before a new install goes in, or because a service visit turns up ductwork that hasn't been done in a while. It's outside most engineers' scope, but customers often ask anyway, and it's a straightforward thing to hand off to someone who does it as their main job.

Happy to be that point of contact — I can work directly with your customer, or quietly in the background if you'd rather keep the relationship in your hands. Either way you get a compliance certificate to pass on, and one less thing to say no to.

Worth a quick call to see if it's useful?

Damien
Phoenix Duct Clean
07961 915018 / officeductclean@gmail.com
phoenixductclean.com

---

## Email 2 — Follow-up (10-14 days later, no reply)

Subject: Re: A TR19 extraction cleaning partner for your installs and servicing — *|SITE|*

Hi there,

Following up in case my last note got buried.

Quick version: when a customer asks about getting the extraction ductwork cleaned — not just the equipment you're servicing, but the ducting itself — I'm happy to take that off your hands. No cost to you, no commitment, just someone reliable to point people to when it comes up. I'll deal with scheduling and give your customer (or you, whichever's easier) a proper TR19 certificate at the end of it.

If this isn't something that comes up for you, no worries at all — just let me know and I'll leave it there.

Damien
Phoenix Duct Clean
07961 915018 / officeductclean@gmail.com

---

## Email 3 — Final, low-pressure close (10-14 days after Email 2)

Subject: Last note — extraction cleaning if it's ever useful — *|SITE|*

Hi there,

Last email from me on this one.

If it's ever useful to have someone to refer extraction cleaning work to — now or down the line — I'm easy to find: 07961 915018 or officeductclean@gmail.com. Happy to work UK-wide, on whatever basis suits you best.

All the best,
Damien
Phoenix Duct Clean

---

## Notes
- This list is noisier at the sourcing stage than the other verticals — "catering equipment" search terms also pull in wholesalers, cutlery retailers and unrelated trades, so `filter_chains.py` in this scraper's folder does more filtering work than the equivalent script elsewhere. Worth a skim of `catering_engineers_excluded.csv` if response rates look off, in case a genuinely relevant business got filtered out for having a generic name.
- No compliance-scare-tactic content here (unlike the pub/care home sequences) — this audience already knows TR19 exists, and the pitch is about making their own customer interactions easier, not educating them on fire risk.
- Plain text, no images/attachments, same reasoning as every other sequence in this repo.
