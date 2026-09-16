<?php
/**
 * Generated rather than hand-maintained, so it cannot drift out of date as
 * content is added. Point search engines at /sitemap.php.
 */
declare(strict_types=1);
require __DIR__ . '/inc/layout.php';
require __DIR__ . '/inc/content.php';

$ev   = event();
$root = rtrim($ev['site_url'], '/');
$urls = [['', '1.0'], ['whats-on', '0.8'], ['visiting', '0.8'], ['charity', '0.7'],
         ['guides', '0.7'], ['news', '0.6']];

foreach (all_guides() as $g) { $urls[] = [item_url($g), '0.7']; }
foreach (all_posts()  as $p) { $urls[] = [item_url($p), '0.5']; }

header('Content-Type: application/xml; charset=utf-8');
echo '<?xml version="1.0" encoding="UTF-8"?>', "\n";
echo '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">', "\n";
foreach ($urls as [$path, $priority]) {
    printf("  <url><loc>%s</loc><priority>%s</priority></url>\n",
        htmlspecialchars($root . '/' . $path, ENT_XML1), $priority);
}
echo '</urlset>', "\n";
