// iNeedWorkwear cluster QA gates — run over a generated cluster's output.
// Enforces the plan's pre-publish gates so nothing thin/duplicate/doorway ships.
// Usage: node gates.mjs out            (reads out/_manifest.json + the HTML files)
import { readFileSync } from 'node:fs';
import { resolve, join } from 'node:path';

const outDir = resolve(process.argv[2] || 'out');
const manifest = JSON.parse(readFileSync(join(outDir, '_manifest.json'), 'utf8'));

// ---- tunable thresholds ----
const T = {
  simMax: 0.50,          // max 8-gram Jaccard between any two sibling pages
  minWords: 350,         // min visible words per page
  minDataBlocks: 1,      // min "data" components (table/cards/steps/keyfacts) per page
  maxShopPer1k: 12,      // max shop links per 1,000 words (doorway ceiling)
  minInternalLinks: 2,   // min internal cluster links per page
};

// ---- load + parse pages ----
const pages = manifest.pages.map(p => {
  const html = readFileSync(join(outDir, p.slug + '.html'), 'utf8');
  const body = html.replace(/<script[\s\S]*?<\/script>/g, '').replace(/<style[\s\S]*?<\/style>/g, '');
  const text = body.replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim();
  const words = text.toLowerCase().split(' ').filter(Boolean);
  const grams = new Set(); for (let i = 0; i <= words.length - 8; i++) grams.add(words.slice(i, i + 8).join(' '));
  return {
    ...p, html, words,
    grams,
    titleCount: (html.match(/<title>/g) || []).length,
    h1Count: (html.match(/<h1[ >]/g) || []).length,
    canonical: /<link rel="canonical"/.test(html),
    jsonld: (html.match(/application\/ld\+json/g) || []).length,
    breadcrumb: /"BreadcrumbList"/.test(html),
    dataBlocks: (html.match(/class="tbl-scroll"|class="kit"|class="steps"|class="keyfacts"/g) || []).length,
    shopLinks: (html.match(/ineedworkwear\.com/g) || []).length,
    internalLinks: (html.match(/href="[a-z0-9-]+\.html"/g) || []).length,
  };
});

const results = [];
const add = (page, gate, pass, detail) => results.push({ page, gate, pass, detail });

// ---- per-page gates ----
for (const p of pages) {
  add(p.slug, 'unique-title', p.titleCount === 1, `${p.titleCount} <title>`);
  add(p.slug, 'single-h1', p.h1Count === 1, `${p.h1Count} <h1>`);
  add(p.slug, 'canonical', p.canonical, p.canonical ? 'present' : 'MISSING');
  add(p.slug, 'schema', p.jsonld >= 2 && p.breadcrumb, `${p.jsonld} JSON-LD, breadcrumb=${p.breadcrumb}`);
  add(p.slug, 'thin-content:words', p.words.length >= T.minWords, `${p.words.length} words (min ${T.minWords})`);
  add(p.slug, 'thin-content:data-blocks', p.dataBlocks >= T.minDataBlocks, `${p.dataBlocks} data blocks (min ${T.minDataBlocks})`);
  const shopPer1k = p.words.length ? (p.shopLinks / p.words.length) * 1000 : 0;
  add(p.slug, 'doorway:shop-ratio', shopPer1k <= T.maxShopPer1k, `${shopPer1k.toFixed(1)} shop links / 1k words (max ${T.maxShopPer1k})`);
  add(p.slug, 'interlinking', p.internalLinks >= T.minInternalLinks, `${p.internalLinks} internal links (min ${T.minInternalLinks})`);
}

// ---- cross-page gates ----
// unique titles across the cluster
const titles = pages.map(p => (p.html.match(/<title>([^<]*)<\/title>/) || [])[1]);
add('cluster', 'titles-distinct', new Set(titles).size === titles.length, `${new Set(titles).size}/${titles.length} distinct`);

// hub<->spoke interlinking wired both ways.
// Clusters with an external hub (an existing site page) can only be checked
// spoke→hub here; the hub→spoke links are added on the live hub page itself.
const hub = pages.find(p => p.role === 'hub') || (manifest.externalHub ? { ...manifest.externalHub, external: true } : undefined);
if (!hub) throw new Error('No hub page in manifest and no externalHub declared');
const spokes = pages.filter(p => p.role !== 'hub');
let wired = true, wireDetail = [];
for (const s of spokes) {
  const spokeToHub = s.html.includes(`href="${hub.slug}.html"`);
  const hubToSpoke = hub.external ? true : hub.html.includes(`href="${s.slug}.html"`);
  if (!spokeToHub || !hubToSpoke) { wired = false; wireDetail.push(`${s.slug}: ->hub=${spokeToHub} hub->=${hubToSpoke}`); }
}
add('cluster', 'hub-spoke-wired', wired, wired ? (hub.external ? `all spokes → external hub ${hub.slug}.html` : 'all spokes ↔ hub') : wireDetail.join(' | '));

// pairwise similarity (8-gram Jaccard)
let maxSim = 0, maxPair = '';
for (let i = 0; i < pages.length; i++) for (let j = i + 1; j < pages.length; j++) {
  const a = pages[i].grams, b = pages[j].grams;
  let inter = 0; for (const g of a) if (b.has(g)) inter++;
  const jac = inter / (a.size + b.size - inter || 1);
  if (jac > maxSim) { maxSim = jac; maxPair = `${pages[i].slug} vs ${pages[j].slug}`; }
}
add('cluster', 'similarity', maxSim <= T.simMax, `max ${(maxSim * 100).toFixed(0)}% (${maxPair}); ceiling ${T.simMax * 100}%`);

// ---- report ----
const fails = results.filter(r => !r.pass);
console.log(`\n=== Cluster QA gates: ${manifest.cluster} (${pages.length} pages) ===`);
for (const r of results) console.log(`  ${r.pass ? 'PASS' : 'FAIL'}  ${(r.page + ' · ' + r.gate).padEnd(46)} ${r.detail}`);
console.log(`\n${fails.length ? `❌ ${fails.length} gate(s) FAILED` : '✅ ALL GATES PASSED'} — ${results.length} checks.`);
process.exit(fails.length ? 1 : 0);
