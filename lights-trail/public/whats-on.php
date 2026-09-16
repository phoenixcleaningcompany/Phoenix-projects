<?php
declare(strict_types=1);
require __DIR__ . '/inc/layout.php';
$ev = event();
page_head("What's on", 'The lights trail, Santa\'s grotto, the reindeer, food and drink, and the collection.', 'whats-on');
?>
<section class="hero">
  <div class="wrap">
    <div class="kicker"><?= $ev['date_confirmed'] ? e($ev['date_text']) : todo($ev['date_text'] . ' — to confirm') ?> · <?= e($ev['times']) ?></div>
    <h1>What's on</h1>
    <p class="lead">Five things, all within walking distance of each other. Nothing needs booking.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="bills">
      <?php foreach ($ev['attractions'] as $a): ?>
      <article class="bill" id="<?= e($a['slug']) ?>">
        <div class="glyph"><?= icon($a['icon']) ?></div>
        <div class="body">
          <h3><?= e($a['title']) ?></h3>
          <p><?= e($a['lede']) ?></p>
          <p><?= e($a['body']) ?></p>
          <div class="meta">
            <?php foreach ($a['meta'] as $m): ?>
              <span><?= str_starts_with($m, 'CONFIRM') ? todo($m) : e($m) ?></span>
            <?php endforeach; ?>
          </div>
          <?php if ($a['slug'] === 'trail'): ?>
            <div class="actions"><a class="btn" href="<?= u('trail.php') ?>">Open the trail</a></div>
          <?php endif; ?>
        </div>
      </article>
      <?php endforeach; ?>
    </div>
  </div>
</section>
<?php page_foot(); ?>
