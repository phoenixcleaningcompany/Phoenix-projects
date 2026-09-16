<?php
declare(strict_types=1);
require __DIR__ . '/inc/layout.php';
require __DIR__ . '/inc/content.php';

$slug  = preg_replace('/[^a-z0-9-]/', '', (string) ($_GET['g'] ?? ''));
$guide = $slug === '' ? null : find_item('guides', $slug);

if (!$guide) {
    http_response_code(404);
    page_head('Not found', 'That guide does not exist.', 'guides');
    echo '<section class="hero"><div class="wrap"><h1>Not found</h1>'
       . '<p class="lead">That page is not here. <a href="' . u('guides') . '">All the guides</a>.</p>'
       . '</div></section>';
    page_foot();
    exit;
}

page_head($guide['title'], $guide['summary'], 'guides', item_url($guide));
$more = related($guide);
?>
<section class="hero">
  <div class="wrap">
    <h1><?= e($guide['title']) ?></h1>
    <p class="lead"><?= e($guide['summary']) ?></p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <article class="article"><?= $guide['body'] ?></article>

    <?php if ($more): ?>
      <div class="prose" style="margin-top:var(--space-8)">
        <h2>Read next</h2>
        <div class="posts">
          <?php foreach ($more as $m): ?>
            <a class="post-link" href="<?= u(item_url($m)) ?>">
              <h3><?= e($m['title']) ?></h3>
              <p><?= e($m['summary']) ?></p>
            </a>
          <?php endforeach; ?>
        </div>
      </div>
    <?php endif; ?>
  </div>
</section>
<?php page_foot(); ?>
