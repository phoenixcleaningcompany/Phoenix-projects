<?php
declare(strict_types=1);
require __DIR__ . '/inc/layout.php';
require __DIR__ . '/inc/content.php';
$ev = event();
page_head('Guides', 'Christmas light trails, displays and things to do around ' . $ev['town'] . ' and Mid Wales.', 'guides', 'guides');
$guides = all_guides();
?>
<section class="hero">
  <div class="wrap">
    <h1>Guides</h1>
    <p class="lead">Lights, trails and Christmas in this part of Mid Wales — written by people who live here.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <?php if (!$guides): ?>
      <p class="prose">Nothing here yet.</p>
    <?php else: ?>
      <div class="posts">
        <?php foreach ($guides as $g): ?>
          <a class="post-link" href="<?= u(item_url($g)) ?>">
            <h3><?= e($g['title']) ?></h3>
            <p><?= e($g['summary']) ?></p>
          </a>
        <?php endforeach; ?>
      </div>
    <?php endif; ?>
  </div>
</section>
<?php page_foot(); ?>
