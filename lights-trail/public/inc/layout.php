<?php
/**
 * Shared page chrome for the website. The trail app has its own shell.
 */

declare(strict_types=1);

function event(): array
{
    static $e = null;
    if ($e === null) {
        $e = require __DIR__ . '/event.php';
    }
    return $e;
}

function e(?string $s): string
{
    return htmlspecialchars((string) $s, ENT_QUOTES, 'UTF-8');
}

/** Marks a fact that still needs confirming, visibly, on the page. */
function todo(string $s): string
{
    return '<mark class="todo">' . e($s) . '</mark>';
}

const NAV = [
    ''            => 'Home',
    'whats-on'    => "What's on",
    'visiting'    => 'Visiting',
    'charity'     => 'The collection',
    'blog'        => 'News',
];

function page_head(string $title, string $description, string $current = ''): void
{
    $ev = event();
    $full = $title === '' ? $ev['name'] : $title . ' · ' . $ev['name'];
    ?>
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#2e2b25">
<title><?= e($full) ?></title>
<meta name="description" content="<?= e($description) ?>">
<meta property="og:title" content="<?= e($full) ?>">
<meta property="og:description" content="<?= e($description) ?>">
<meta property="og:type" content="website">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Caprasimo&family=Figtree:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/tokens.css">
<link rel="stylesheet" href="assets/site.css">
</head>
<body>
<header class="site-head">
  <div class="wrap">
    <a class="brand" href="./">
      <span class="bulbs"><i></i><i></i><i></i></span>
      <?= e($ev['name']) ?>
    </a>
    <nav class="site-nav" aria-label="Main">
      <?php foreach (NAV as $slug => $label): ?>
        <a href="<?= $slug === '' ? './' : e($slug) . '.php' ?>"
           <?= $slug === $current ? 'aria-current="page"' : '' ?>><?= e($label) ?></a>
      <?php endforeach; ?>
      <a class="cta" href="trail.php">Open the trail</a>
    </nav>
  </div>
</header>
<main>
<?php
}

function page_foot(): void
{
    $ev = event();
    ?>
</main>
<footer class="site-foot">
  <div class="wrap">
    <div><?= e($ev['name']) ?> · <?= e($ev['town']) ?>, <?= e($ev['county']) ?></div>
    <div><a href="trail.php">Open the trail</a> · <a href="charity.php">The collection</a></div>
  </div>
</footer>
</body>
</html>
<?php
}

/** Line-drawn icons for the What's on blocks. */
function icon(string $name): string
{
    $paths = [
        'trail' => '<path d="M12 3 4 20h16L12 3Z"/><path d="M12 20v2"/>',
        'gift'  => '<path d="M4 11h16v10H4z"/><path d="M2 7h20v4H2z"/><path d="M12 7v14"/><path d="M12 7S9 3 7 4s0 3 5 3Zm0 0s3-4 5-3-.5 3-5 3Z"/>',
        'deer'  => '<path d="M7 4 5 2M7 4 4 5M7 4l1 3M17 4l2-2M17 4l3 1M17 4l-1 3"/><path d="M12 22a5 5 0 0 0 5-5v-3a5 5 0 0 0-10 0v3a5 5 0 0 0 5 5Z"/><path d="M10 13h.01M14 13h.01"/>',
        'cup'   => '<path d="M4 8h13v7a5 5 0 0 1-5 5H9a5 5 0 0 1-5-5V8Z"/><path d="M17 10h2a2 2 0 0 1 0 5h-2"/><path d="M8 2v3M12 2v3"/>',
        'heart' => '<path d="M12 20s-7-4.5-7-9a4 4 0 0 1 7-2.6A4 4 0 0 1 19 11c0 4.5-7 9-7 9Z"/>',
    ];
    return '<svg viewBox="0 0 24 24" aria-hidden="true">' . ($paths[$name] ?? '') . '</svg>';
}
