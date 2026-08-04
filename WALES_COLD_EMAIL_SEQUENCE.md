# Wales Cold Outreach — 3-Email Sequence

For the independent/small-chain list (`scripts/wales-care-scraper/independent_and_small_chain.csv`). Plain text, not HTML — matches how a real one-person business emails, and avoids the spam signals a designed template triggers from an unfamiliar sender.

Cadence: Email 1 → wait 10-14 days, no reply → Email 2 → wait 10-14 days, no reply → Email 3. Stop the sequence the moment someone replies, quotes, or asks to be left alone.

Note on why a sequence, not a single email: the rugby club send (500 emails, single touch) got 3 quotes. A second and third touch to non-responders typically lifts replies further, since a first cold email is often just missed or deprioritized rather than rejected — it's not that the recipient said no.

---

## Email 1 — Initial contact

Subject: LEV testing / TR19 compliance — [Service Name]

Hi [Name / "there" if no contact name],

I run Phoenix Duct Clean — TR19 kitchen extraction cleaning and LEV/COSHH testing for care homes and nurseries across the UK, 15+ years doing it.

Two things I find get missed at sites like yours:
- LEV testing is a legal requirement enforced by the HSE under COSHH, not just best practice.
- TR19 kitchen extraction cleaning is tied to fire risk assessments and insurance validity under the Fire Safety Order 2005 — a missing certificate is a common reason a fire claim gets challenged.

If it's due, or you're not sure when it was last done, happy to send a no-obligation price. Every clean comes with a dated certificate, before/after photos, and an access report — no hidden extras, no out-of-hours charge.

Worth a reply either way, even if it's "not needed right now."

[Name]
Phoenix Duct Clean
07961 915018 / officeductclean@gmail.com
phoenixductclean.com

---

## Email 2 — Follow-up (10-14 days later, no reply)

Subject: Re: LEV testing / TR19 compliance — [Service Name]

Hi [Name],

Following up on the note below in case it got buried.

Quick version: I clean kitchen extraction systems and test LEV to HSE/COSHH standard for care homes and nurseries, and wanted to check if [Service Name] is up to date on either.

If you already have someone doing this, no problem — just let me know so I stop chasing. If not, a price takes a couple of minutes to put together.

[Name]
Phoenix Duct Clean
07961 915018 / officeductclean@gmail.com

---

## Email 3 — Final, low-pressure close (10-14 days after Email 2)

Subject: Last one from me — [Service Name]

Hi [Name],

Last email on this from me — don't want to keep filling your inbox.

If TR19 extraction cleaning or LEV testing is something [Service Name] needs at some point, I'm easy to find: 07961 915018 or officeductclean@gmail.com. Happy to help whenever it's actually due, no pressure before then.

All the best,
[Name]
Phoenix Duct Clean

---

## Notes
- `[Service Name]` comes straight from the CSV — makes it look like you looked at their specific site, not a mail-merge blast, without needing a real contact name (which the CSV mostly won't have).
- Don't use the McDonald's/AWS/BaxterStorey-style "trusted by" claims here until confirmed genuine (see conversation) — nothing in this draft references them.
- Keep formatting plain: no images, no HTML template, no tracking pixels if avoidable — all of that increases spam-filter risk for cold mail from a personal Gmail address.
- Respect the batching caution already in OUTREACH_TARGET_LIST.md — don't fire all ~2,000 Email 1s in one day from officeductclean@gmail.com.
