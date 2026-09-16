<?php
/**
 * Posts are one PHP file each in posts/, newest first by date. No database
 * and no admin screen: to publish, add a file and upload it.
 */

declare(strict_types=1);

function all_posts(): array
{
    static $posts = null;
    if ($posts !== null) {
        return $posts;
    }
    $posts = [];
    foreach (glob(__DIR__ . '/../posts/*.php') ?: [] as $file) {
        $p = require $file;
        $p['slug'] = basename($file, '.php');
        if (!empty($p['draft'])) {
            continue;
        }
        $posts[] = $p;
    }
    usort($posts, fn($a, $b) => strcmp($b['date'], $a['date']));
    return $posts;
}

function find_post(string $slug): ?array
{
    foreach (all_posts() as $p) {
        if ($p['slug'] === $slug) {
            return $p;
        }
    }
    return null;
}

function post_date(string $iso): string
{
    return date('j F Y', strtotime($iso));
}
