LAUNCH PACK — deploy on go-live day only, never to password-protected staging.

WHAT: robots.txt (AI crawlers explicitly welcomed), sitemap.xml + 9
segmented sitemaps (the canary instrument — watch indexation per segment in
GSC), and llms.txt (a curated map for AI assistants).

HOW: copy every file in this folder to the docroot alongside the site files,
then submit sitemap.xml in Google Search Console. The segmented files let you
read indexation ratio per content family from week one.

WHY NOT NOW: a sitemap pointing at password-walled pages just generates GSC
errors, and robots.txt has nothing to say until crawlers can get in.
Regenerate before launch if pages have been added:
node scratchpad/gen-launch.mjs (or ask Claude).
