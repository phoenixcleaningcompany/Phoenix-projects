<?php
declare(strict_types=1);
require __DIR__ . '/inc/layout.php';
$ev = event();
page_head('The collection', 'Every tin on the trail goes to ' . $ev['charity'] . '.', 'charity');
?>
<section class="hero">
  <div class="wrap">
    <h1>The collection</h1>
    <p class="lead">The lights are the fun part. This is the point of it.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="prose">
      <p>Every collection tin on the trail goes to <?= $ev['charity_confirmed'] ? e($ev['charity']) : todo($ev['charity'] . ' — to confirm') ?>. Nothing is taken out for costs. The households pay for their own electricity and their own decorations, and always have.</p>

      <?php if ($ev['raised_last_year']): ?>
        <p>Last year the town raised <strong><?= e($ev['raised_last_year']) ?></strong>.</p>
      <?php else: ?>
        <p><?= todo('Last year\'s total to confirm — worth putting here, it is the single most persuasive thing on the page.') ?></p>
      <?php endif; ?>

      <h2>How to give on the night</h2>
      <p>There is a tin at every house. Several have a card reader at the gate for anyone not carrying cash — the trail tells you which ones as you walk it. Give at one house or at all twelve; it all ends up in the same place.</p>

      <h2>If you cannot come</h2>
      <p><?= todo('Online giving link to confirm — a JustGiving page or similar, if there is one.') ?></p>

      <h2>Taking part</h2>
      <p>If you live in <?= e($ev['town']) ?> and want to put your house on the trail, <?= todo('who to contact, and the closing date for entries') ?>. Displays are confirmed in early December, and there is no minimum — one tree done properly is as welcome as eight thousand bulbs.</p>
    </div>
  </div>
</section>
<?php page_foot(); ?>
