# Phoenix projects

## Llanwrtyd Lights (`lights-trail/`)

Two things in one site, sharing one visual identity:

- **The website** (`index.php` and the content pages) — what draws people to the
  event beforehand: what's on, visiting, the collection, and a news section for
  content that brings search traffic in.
- **The trail app** (`trail.php`) — what people use on the night.

A website for a Christmas lights trail: twelve houses, one night, walk the
route, scan a QR code at each gate, vote in three categories, watch live
results. Welsh and English.

Built as plain PHP + MySQL to run on GoDaddy Linux/cPanel hosting, so the
public can open it on any phone with no account and no app. No build step.

**Status:** working and tested, not yet deployed. See `lights-trail/README.md`
for the cPanel setup steps.

### Deferred work

**Offline support — agreed, to be built later.** Right now every feature needs
a live connection; lose signal and the app is a blank screen. Mid-Wales
coverage is patchy and the trail's own content flags Cwm Irfon Lane as a dark
unlit stretch at the edge of town, which is likely the worst reception on the
route. The plan:

- A service worker caching the app shell, house list, descriptions and ballot,
  so all reading works offline.
- Check-ins and votes queued in local storage and synced when signal returns.
- Live results stay online-only by nature — show the viewer's own picks and a
  "totals update when you're back in signal" note.
- Known limitation: a service worker only helps someone who has loaded the site
  at least once. Needs an organisational fix too — a "Start here" QR at stop
  one, or wifi at the village hall.
- Open question for the organiser: should a vote cast offline before the close
  time but synced after it still count? Recommendation is yes, judged on when
  it was cast.

### December handover — what to send

Entrants are not confirmed until early December, and the organiser sends the
list here rather than editing anything (decided; no admin page was built).
For each house:

```
Stop order:   1
Name:         Bryn Awel
Address:      Dolecoed Road
Description:  one or two sentences, as it should read on the phone
Note:         optional - "card reader at the gate", "quiet display", "steep drive"
Walk:         optional - minutes on to the NEXT stop
Coordinates:  52.104, -3.6355
```

Coordinates are the only fiddly one. In Google Maps, right-click the house and
the latitude/longitude at the top of the menu copies to the clipboard. Twelve
of those is about five minutes and is far more reliable than geocoding rural
Welsh addresses, which routinely lands on the wrong lane.

Then: update `tools/seed.php`, re-run it, and re-print the QR sheet. Existing
check-in tokens survive a re-run, so only genuinely new houses get new codes.

### Open decisions (need the organiser, not code)

- The twelve houses are invented placeholder content from the design prototype,
  and their coordinates are rough points around Llanwrtyd Wells chosen only to
  make the map previewable. Nothing there is surveyed.
- House descriptions have no Welsh translation. The interface is fully
  bilingual; `blurb_cy` and `note_cy` columns are ready and empty.
- The map uses OpenStreetMap tiles, which need a connection. Llanwrtyd is small
  enough to pre-cache the whole town when the offline layer is built.
- Nobody has walked the route checking phone signal at each gate. That result
  decides how urgent the offline layer is.
- Branding is deliberately not settled. The entire visual identity is in
  `public/assets/tokens.css` — changing the whole look, website and app, is
  editing that one file.
- **The event date is not confirmed.** `inc/event.php` currently says Friday 18
  December 2026 with `date_confirmed => false`, which makes every mention of it
  render as a visible "to confirm" marker. Last year's was Thursday 18 December
  2025. Set the real date and flip the flag.
- Lots of event facts are unknown and deliberately marked rather than invented:
  grotto times and price, reindeer times, parking, toilets, dog policy, trail
  distance, last year's fundraising total, online giving link, and who to
  contact to enter a house. Search the codebase for `todo(` and `CONFIRM` to
  find every one.
- Content is written here in Claude and committed, not self-published, so no
  admin screen is needed (settled).

### Writing content

Content is the plan for bringing people to the site: Christmas lights, light
trails, Christmas events in the area, and related subjects — all linking back
to the event.

**Two separate kinds, deliberately.**

- `public/posts/` — **dated news**. Entries opening, this year's line-up, how
  the night went. Newest first, dated on the page, ages naturally. Lives at
  `/news/<slug>`.
- `public/guides/` — **evergreen articles**. No date shown, because a date
  makes a useful guide look stale long before it is. Ordered by an `order`
  key. Lives at `/guides/<slug>`.

Both are one PHP file each, discovered automatically. `'draft' => true` keeps
one out of the lists. `tags` drive the "Read next" block, so give every piece
two or three shared tags or it will sit unlinked.

**The bar.** The organiser asked specifically for non-templated, non-thin,
genuinely useful pages. What earns its place is what only someone here can
write: the actual town, the actual route, real local knowledge, practical
advice with specifics in it. What does not is anything that could appear on a
thousand other sites — generic Christmas filler ranks for nothing and makes
the rest look worse. Where a page needs a fact nobody has confirmed, mark it
with `todo()` rather than inventing it; that rule matters more in content than
anywhere else on the site.

**Images** go in `public/assets/img/`. Every one needs real alt text. Resize
before uploading — a 4MB phone photo on a page people open on mobile data in
a field is a genuine problem, not a nicety.

### URLs

Settled before publishing, because changing them afterwards costs rankings and
needs redirects:

- `/`, `/whats-on`, `/visiting`, `/charity`, `/guides`, `/news`
- `/guides/<slug>`, `/news/<slug>`
- `/trail.php` — the app; a gate QR at the site root redirects here

`.htaccess` rewrites map these onto the real scripts, and the query-string
forms still work if mod_rewrite is ever unavailable. **The rewrites have never
run against Apache** — there is none in the dev container — so check them on
the real host before relying on them. `page_head()` emits a canonical link,
but only once `site_url_confirmed` is true in `inc/event.php`.

`/sitemap.php` generates itself from the content files.

### Conventions

- Design tokens came from the original design-canvas prototype
  (artifact `a7efc5de-547e-4243-b7f4-041df8782b87`): amber `#f6a06b` on warm
  dark `#2e2b25`, sage `#ccdbb2` for confirmation, Caprasimo + Figtree.
  Committed single dark theme — it is used outdoors at night.
- Never change a house's check-in `token` once QR codes are printed;
  `tools/seed.php` preserves existing tokens on re-run for exactly this reason.
- Real database credentials belong in `public/config.local.php`, which is
  gitignored. `public/config.php` is the committed template.
- A tap-through preview (localStorage, no server) is published at
  https://claude.ai/code/artifact/0d719bfc-5014-4986-9cb6-8ca99089a506
