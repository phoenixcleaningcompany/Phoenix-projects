<?php
declare(strict_types=1);
require __DIR__ . '/lib.php';

$c = cfg();
device_id(); // sets the cookie on first visit, before any output

// A QR scan lands here as /?c=TOKEN. Hand it to the page; app.js posts it
// to the API and then cleans the address bar so a refresh can't re-trigger.
$scan = preg_match('/^[A-Z0-9]{6,24}$/', (string) ($_GET['c'] ?? '')) ? $_GET['c'] : '';
?>
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#2e2b25">
<title><?= htmlspecialchars($c['event_name_en']) ?></title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Caprasimo&family=Figtree:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/styles.css?v=1">
</head>
<body>

<div id="app" class="app" aria-busy="true">
  <div class="loading"><span class="bulb"></span><span class="bulb"></span><span class="bulb"></span></div>
</div>

<template id="tpl-nav">
  <nav class="nav">
    <button data-screen="trail"><span>🎄</span><em data-en="Trail" data-cy="Llwybr"></em></button>
    <button data-screen="vote"><span>🗳️</span><em data-en="Vote" data-cy="Pleidlais"></em></button>
    <button data-screen="results"><span>🏆</span><em data-en="Results" data-cy="Canlyniadau"></em></button>
    <button data-screen="info"><span>ℹ️</span><em data-en="Info" data-cy="Gwybodaeth"></em></button>
  </nav>
</template>

<script>
window.LLT = {
  scan: <?= json_encode($scan) ?>,
  event: {
    name: { en: <?= json_encode($c['event_name_en']) ?>, cy: <?= json_encode($c['event_name_cy']) ?> },
    date: { en: <?= json_encode($c['event_date_en']) ?>, cy: <?= json_encode($c['event_date_cy']) ?> }
  }
};
</script>
<script src="assets/app.js?v=1"></script>
</body>
</html>
