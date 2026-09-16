<?php
declare(strict_types=1);
require __DIR__ . '/inc/layout.php';

// Gate QR codes may point at the site root. Send those straight to the trail
// so a printed code keeps working whatever else changes here.
if (isset($_GET['c'])) {
    header('Location: trail.php?c=' . urlencode((string) $_GET['c']), true, 302);
    exit;
}

$ev = event();
page_head('', $ev['tagline'] . ' ' . $ev['town'] . ', ' . $ev['date_text'] . '.', '');
?>

<section class="hero">
  <div class="wrap">
    <div class="kicker"><?= e($ev['town']) ?> · <?= e($ev['county']) ?></div>
    <h1><?= e($ev['name']) ?></h1>
    <p class="when">
      <?= $ev['date_confirmed'] ? e($ev['date_text']) : todo($ev['date_text'] . ' — to confirm') ?>,
      <?= e($ev['times']) ?>
    </p>
    <p class="lead">
      Twelve houses across the town switch their displays on for one night only.
      Walk the trail, meet the reindeer, queue for the grotto, and put something
      in a tin on the way round. Then vote for the display you liked best.
    </p>
    <div class="actions">
      <a class="btn" href="trail.php">Open the trail</a>
      <a class="btn ghost" href="whats-on.php">See what's on</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <h2>What happens on the night</h2>
    <p>Everything is within walking distance. Come when you like and leave when you like — there is no set start.</p>
    <div class="bills">
      <?php foreach ($ev['attractions'] as $a): ?>
      <article class="bill">
        <div class="glyph"><?= icon($a['icon']) ?></div>
        <div class="body">
          <h3><?= e($a['title']) ?></h3>
          <p><?= e($a['lede']) ?></p>
          <div class="meta">
            <?php foreach ($a['meta'] as $m): ?>
              <span><?= str_starts_with($m, 'CONFIRM') ? todo($m) : e($m) ?></span>
            <?php endforeach; ?>
          </div>
        </div>
      </article>
      <?php endforeach; ?>
    </div>
    <div class="actions">
      <a class="btn ghost" href="whats-on.php">Full details</a>
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <div class="body">
      <h2>It is all for the collection</h2>
      <p>
        Every tin on the trail goes to <?= $ev['charity_confirmed'] ? e($ev['charity']) : todo($ev['charity'] . ' — to confirm') ?>.
        <?php if ($ev['raised_last_year']): ?>
          Last year the town raised <?= e($ev['raised_last_year']) ?>.
        <?php endif; ?>
        The houses do the work, the town turns out, and the money stays here.
      </p>
      <div class="actions"><a class="btn ghost" href="charity.php">How to give</a></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <h2>Before you come</h2>
    <dl class="facts">
      <div class="fact"><dt>When</dt><dd><?= $ev['date_confirmed'] ? e($ev['date_text']) : todo('To confirm') ?></dd></div>
      <div class="fact"><dt>Time</dt><dd><?= e($ev['times']) ?></dd></div>
      <div class="fact"><dt>Cost</dt><dd>Free to walk</dd></div>
      <div class="fact"><dt>On foot</dt><dd>About 90 minutes</dd></div>
    </dl>
    <div class="actions"><a class="btn ghost" href="visiting.php">Parking, access and what to wear</a></div>
  </div>
</section>

<?php page_foot(); ?>
