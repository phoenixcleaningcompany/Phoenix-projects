<?php
declare(strict_types=1);
require __DIR__ . '/inc/layout.php';
$ev = event();
page_head('Visiting', 'Getting to ' . $ev['town'] . ', parking, accessibility, and what to wear.', 'visiting');
?>
<section class="hero">
  <div class="wrap">
    <h1>Visiting</h1>
    <p class="lead">It is a December night in mid-Wales. A little planning makes it a much better evening.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="prose">
      <h2>Getting here</h2>
      <p><?= e($ev['town']) ?> is on the A483 between Builth Wells and Llandovery. The railway station is on the Heart of Wales line, and the trail starts a few minutes' walk from it — <?= todo('check the last train home before you plan around it') ?>.</p>

      <h2>Parking</h2>
      <p><?= todo('Parking arrangements to confirm — where, whether it is free, and how many spaces.') ?> The streets on the trail are narrow and people will be walking on them in the dark, so please park once and walk rather than driving between stops.</p>

      <h2>Getting round</h2>
      <p>The full trail is about <?= todo('distance to confirm') ?> and takes roughly ninety minutes at an easy pace with stops. Most of it is on pavement. Two stretches are not: the lane at <?= todo('confirm which stops' ) ?> is unlit and uneven, and one drive is steep. Both are flagged on the trail itself as you get to them.</p>

      <h2>Accessibility</h2>
      <p>Most of the route is manageable with a wheelchair or pushchair, and the trail marks which houses have a level approach. <?= todo('Accessible toilet location to confirm.') ?> If you need to do a shorter version, the houses in the centre of town are close together and make a decent half-hour loop on their own.</p>

      <h2>What to bring</h2>
      <p>Warm layers, and more than you think — you will be standing still looking at things. A torch for the unlit stretch. Cash as well as a card, because signal is patchy and card readers sulk. Wellies if it has been raining.</p>

      <h2>Dogs</h2>
      <p><?= todo('Dog policy to confirm — particularly around the reindeer, where they are usually not allowed anywhere near.') ?></p>

      <h2>Toilets</h2>
      <p><?= todo('Toilet locations and opening times to confirm.') ?></p>
    </div>
  </div>
</section>
<?php page_foot(); ?>
