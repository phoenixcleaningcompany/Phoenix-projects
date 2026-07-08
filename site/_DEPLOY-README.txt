iNeedWorkwear content site — cPanel deploy notes
================================================
UPLOAD: copy every .html file in this folder to the docroot of
https://www.ineedworkwear.uk (public_html or the subdomain root).
Pages are fully self-contained (inline CSS/JS, Google Fonts only).

STAGING (while you tweak):
1. cPanel -> Directory Privacy -> password the docroot  (primary protection)
2. Optionally rename htaccess-staging.txt -> .htaccess   (adds noindex header)
Do NOT add a robots.txt Disallow — see plan section 6.4 for why.

LAUNCH CHECKLIST (per plan section 6.4):
[ ] Shopify collections live at ineedworkwear.com (hi-vis, fr-coveralls,
    trade-accounts page) so shop links resolve
[ ] Remove Directory Privacy
[ ] DELETE .htaccess noindex (and this file + htaccess-staging.txt)
[ ] Submit sitemap in Search Console, confirm indexing

CURRENT SHOP LINK TARGETS (create these on Shopify, or tell Claude the
real handles and we re-point the links):
  https://www.ineedworkwear.com/collections/hi-vis
  https://www.ineedworkwear.com/collections/fr-coveralls
  https://www.ineedworkwear.com/collections/offshore-coveralls
  https://www.ineedworkwear.com/collections/cold-store-thermal
  https://www.ineedworkwear.com/collections/hospitality
  https://www.ineedworkwear.com/collections/chef-whites
  https://www.ineedworkwear.com/pages/trade-accounts
