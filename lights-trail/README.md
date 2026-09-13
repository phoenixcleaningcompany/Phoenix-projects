# Llanwrtyd Lights — trail, check-in and ballot

A small website for the lights trail. People open it on their phone, scan a QR
code at each gate to check that house off, vote in three categories, and watch
the running totals. No app to install, no account to create.

Built to run on ordinary GoDaddy Linux hosting (cPanel + PHP + MySQL). There is
no build step and nothing to compile — the files you upload are the files that
run.

---

## What you need

From cPanel, the two things this uses:

- **MySQL Databases** — to make a database
- **File Manager** (or FTP) — to upload the files

If your GoDaddy plan is "Websites + Marketing" (the drag-and-drop builder) this
will *not* work — that product has no PHP or database. You need their **Linux
Web Hosting** plan, which is the one with cPanel.

---

## Setting it up

### 1. Make the database

cPanel → **MySQL Databases**.

1. Create a database. GoDaddy will name it something like `phoenix_lights`.
2. Create a user, and give it a strong password. Write the password down.
3. Under "Add User To Database", add that user to that database with
   **All Privileges**.

Keep the three values — database name, user name, password — for step 3.

### 2. Create the tables

cPanel → **phpMyAdmin** → click your database on the left → **Import** tab →
choose `db/schema.mysql.sql` from this project → **Go**.

You should see four tables appear: `houses`, `categories`, `checkins`, `votes`.

### 3. Upload and configure

Upload everything inside the `public/` folder to a folder on your site — for
example `public_html/lights/`. Upload the *contents* of `public/`, not the
folder itself, so you end up with `public_html/lights/index.php`.

Then open `config.php` in cPanel's File Manager (right-click → Edit) and fill in
the database name, user and password from step 1. While you are in there, set
`voting_closes` to the real time voting should stop, and change `salt` to any
long random string.

### 4. Add the houses and get your QR codes

The twelve houses and three categories are already written into
`tools/seed.php`. Edit that file if names or descriptions have changed, then run
it once. If your hosting has SSH you can run:

```
php tools/seed.php
php tools/qr-links.php https://yoursite.co.uk/lights
```

If you have no SSH access (most GoDaddy shared plans), upload `tools/seed.php`
and `tools/qr-links.php` into the `lights` folder temporarily, visit them once
each in your browser, then **delete them from the server**. Leaving them there
would let anyone re-roll your check-in codes.

`qr-links.php` prints twelve URLs, one per house. Paste each into any free QR
generator, print it large, laminate it, and tape it to that house's gatepost.

**Keep those URLs private until the night.** Anyone who has one can check in
without walking anywhere.

---

## How it works on the night

- Someone scans the QR code at a gate. Their phone opens the site and that house
  is ticked off. Scanning the same gate twice changes nothing.
- They vote once per category, and can change their mind until voting closes.
- Results update live. Set `live_results` to `false` in `config.php` if you would
  rather keep the totals hidden until the end and announce them.
- At the time in `voting_closes` the ballot locks itself. Results stay readable.

## How people are counted

There are no accounts and no personal data. Each phone is given a random code
stored in a cookie, which is what stops one phone voting twice. No names, no
email addresses, no location tracking, nothing shared with anyone.

This is deliberately light-touch — proportionate for a village event. Someone
determined could clear their cookies and vote again. If that matters for your
prize-giving, tell me and I can add a stronger check.

## Checking the numbers afterwards

phpMyAdmin → your database → the `votes` table. One row per phone per category.
`checkins` is the same for gate scans, so you can see how many people walked the
whole trail.

---

## Editing it later

You can hand this whole folder back to Claude and ask for changes. The pieces:

| File | What it does |
|---|---|
| `public/index.php` | The page people land on |
| `public/api.php` | Check-in, voting and results |
| `public/lib.php` | Database connection and shared helpers |
| `public/config.php` | Your settings — the only file you must edit |
| `public/assets/app.js` | Screens and buttons |
| `public/assets/styles.css` | Colours, fonts, spacing |
| `tools/seed.php` | The twelve houses and three categories |
| `tools/qr-links.php` | Prints the gate URLs for your QR codes |

The colours and fonts come from the original design prototype, so it looks the
same as the mockup.
