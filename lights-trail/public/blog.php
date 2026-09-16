<?php
declare(strict_types=1);
require __DIR__ . '/inc/layout.php';
require __DIR__ . '/inc/content.php';
$ev = event();
page_head('News', 'Updates about ' . $ev['name'] . ' — entries, plans and news from the trail.', 'news', 'news');
$posts = all_posts();
?>
<section class="hero">
  <div class="wrap">
    <h1>News</h1>
    <p class="lead">What is happening in the run-up, and what happened afterwards.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <?php if (!$posts): ?>
      <p class="prose">Nothing posted yet.</p>
    <?php else: ?>
      <div class="posts">
        <?php foreach ($posts as $p): ?>
          <a class="post-link" href="<?= u(item_url($p)) ?>">
            <h3><?= e($p['title']) ?></h3>
            <span class="date"><?= e(post_date($p['date'])) ?></span>
            <p><?= e($p['summary']) ?></p>
          </a>
        <?php endforeach; ?>
      </div>
    <?php endif; ?>
  </div>
</section>
<?php page_foot(); ?>
