<?php
/**
 * Two kinds of writing live on this site and they are deliberately separate.
 *
 *   posts/   dated news — entries opening, this year's line-up, how the night
 *            went. Shown newest first; ages naturally and that is fine.
 *   guides/  evergreen articles — light trails in the area, how to build a
 *            display, what else is on over Christmas in Mid Wales. No date on
 *            the page, because a date stamp makes a useful guide look stale
 *            long before it is.
 *
 * Both are one PHP file each. To publish, add a file and upload it.
 */

declare(strict_types=1);

function content_items(string $dir): array
{
    static $cache = [];
    if (isset($cache[$dir])) {
        return $cache[$dir];
    }
    $items = [];
    foreach (glob(__DIR__ . '/../' . $dir . '/*.php') ?: [] as $file) {
        $item = require $file;
        $item['slug'] = basename($file, '.php');
        $item['kind'] = $dir === 'posts' ? 'news' : 'guides';
        if (!empty($item['draft'])) {
            continue;
        }
        $items[] = $item;
    }
    // News reads newest first. Guides carry an explicit order, then title.
    usort($items, $dir === 'posts'
        ? fn($a, $b) => strcmp($b['date'] ?? '', $a['date'] ?? '')
        : fn($a, $b) => [$a['order'] ?? 99, $a['title']] <=> [$b['order'] ?? 99, $b['title']]);

    return $cache[$dir] = $items;
}

function all_posts(): array  { return content_items('posts'); }
function all_guides(): array { return content_items('guides'); }

function find_item(string $dir, string $slug): ?array
{
    foreach (content_items($dir) as $i) {
        if ($i['slug'] === $slug) {
            return $i;
        }
    }
    return null;
}

function post_date(string $iso): string
{
    return date('j F Y', strtotime($iso));
}

/**
 * Pretty URL for a piece of content. The .htaccess rewrites map these onto
 * the real scripts; if mod_rewrite is ever off, the query form still works.
 */
function item_url(array $item): string
{
    return $item['kind'] . '/' . $item['slug'];
}

/** Related reading, so guides link to each other rather than sitting alone. */
function related(array $item, int $limit = 3): array
{
    $tags = $item['tags'] ?? [];
    $pool = array_merge(all_guides(), all_posts());
    $scored = [];
    foreach ($pool as $other) {
        if ($other['slug'] === $item['slug']) {
            continue;
        }
        $overlap = count(array_intersect($tags, $other['tags'] ?? []));
        if ($overlap > 0) {
            $scored[] = [$overlap, $other];
        }
    }
    usort($scored, fn($a, $b) => $b[0] <=> $a[0]);
    return array_column(array_slice($scored, 0, $limit), 1);
}
