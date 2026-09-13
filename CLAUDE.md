# Phoenix projects

## Llanwrtyd Lights (`lights-trail/`)

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
- Branding is deliberately not settled. Colours, fonts and spacing are CSS
  custom properties at the top of `public/assets/styles.css` — changing the
  whole look is editing that one block, not a rebuild.

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
