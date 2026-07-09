iNeedWorkwear content site — cPanel deploy notes
================================================
UPLOAD: copy every .html file AND the assets/ folder in this folder to the docroot of
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
  https://www.ineedworkwear.com/collections/anti-static-esd
  https://www.ineedworkwear.com/collections/aprons
  https://www.ineedworkwear.com/collections/arc-flash
  https://www.ineedworkwear.com/collections/bags
  https://www.ineedworkwear.com/collections/beanies
  https://www.ineedworkwear.com/collections/belts
  https://www.ineedworkwear.com/collections/bib-brace-overalls
  https://www.ineedworkwear.com/collections/blouses
  https://www.ineedworkwear.com/collections/bodywarmers-gilets
  https://www.ineedworkwear.com/collections/caps
  https://www.ineedworkwear.com/collections/chainsaw-and-forestry
  https://www.ineedworkwear.com/collections/chefswear
  https://www.ineedworkwear.com/collections/chem-splash
  https://www.ineedworkwear.com/collections/cleaning
  https://www.ineedworkwear.com/collections/coats-jackets
  https://www.ineedworkwear.com/collections/coldstore
  https://www.ineedworkwear.com/collections/construction
  https://www.ineedworkwear.com/collections/consumables
  https://www.ineedworkwear.com/collections/coveralls
  https://www.ineedworkwear.com/collections/disposable
  https://www.ineedworkwear.com/collections/dresses
  https://www.ineedworkwear.com/collections/face-masks-covers
  https://www.ineedworkwear.com/collections/flame-retardant
  https://www.ineedworkwear.com/collections/fleece-jackets
  https://www.ineedworkwear.com/collections/footwear
  https://www.ineedworkwear.com/collections/gloves-ppe
  https://www.ineedworkwear.com/collections/gloves-winter
  https://www.ineedworkwear.com/collections/headwear
  https://www.ineedworkwear.com/collections/healthcare
  https://www.ineedworkwear.com/collections/helmets
  https://www.ineedworkwear.com/collections/hi-vis
  https://www.ineedworkwear.com/collections/hivis
  https://www.ineedworkwear.com/collections/hoodies
  https://www.ineedworkwear.com/collections/hospitality
  https://www.ineedworkwear.com/collections/jackets
  https://www.ineedworkwear.com/collections/joggers
  https://www.ineedworkwear.com/collections/knitwear
  https://www.ineedworkwear.com/collections/lab-medical-coats
  https://www.ineedworkwear.com/collections/maternity
  https://www.ineedworkwear.com/collections/offshore-clothing
  https://www.ineedworkwear.com/collections/overalls
  https://www.ineedworkwear.com/collections/painter-decorator-clothing
  https://www.ineedworkwear.com/collections/polo-shirts
  https://www.ineedworkwear.com/collections/ppe
  https://www.ineedworkwear.com/collections/rail-spec
  https://www.ineedworkwear.com/collections/scarves
  https://www.ineedworkwear.com/collections/schoolwear
  https://www.ineedworkwear.com/collections/scrubs
  https://www.ineedworkwear.com/collections/security
  https://www.ineedworkwear.com/collections/shirts
  https://www.ineedworkwear.com/collections/shorts
  https://www.ineedworkwear.com/collections/skirts
  https://www.ineedworkwear.com/collections/socks
  https://www.ineedworkwear.com/collections/softshell-jackets
  https://www.ineedworkwear.com/collections/sports-teamwear
  https://www.ineedworkwear.com/collections/suits-tailoring
  https://www.ineedworkwear.com/collections/sustainable
  https://www.ineedworkwear.com/collections/sweatshirts
  https://www.ineedworkwear.com/collections/tabards
  https://www.ineedworkwear.com/collections/thermals-base-layers
  https://www.ineedworkwear.com/collections/ties
  https://www.ineedworkwear.com/collections/tote-bags
  https://www.ineedworkwear.com/collections/towelling
  https://www.ineedworkwear.com/collections/trousers
  https://www.ineedworkwear.com/collections/tshirts
  https://www.ineedworkwear.com/collections/tunics
  https://www.ineedworkwear.com/collections/waistcoats
  https://www.ineedworkwear.com/collections/welding-workwear
  https://www.ineedworkwear.com/pages/trade-accounts

Canonical category list: docs/shop-categories.csv (from workwear_inventory.pdf)
