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
<link rel="stylesheet" href="assets/leaflet/leaflet.css">
<link rel="stylesheet" href="assets/tokens.css">
<link rel="stylesheet" href="assets/app.css?v=2">
</head>
<body>

<div id="app" class="app" aria-busy="true">
  <div class="loading"><span class="bulb"><span class="bulb"><span class="bulb"></div>
</div>

<template id="tpl-nav">
  <nav class="nav">
    <button data-screen="trail"><svg viewBox="0 0 24 24"><path d="M12 3 4 20h16L12 3Z"/><path d="M12 20v2"/></svg><em data-en="Trail" data-cy="Llwybr"></em></button>
    <button data-screen="map"><svg viewBox="0 0 24 24"><path d="m9 4-6 3v13l6-3 6 3 6-3V4l-6 3Z"/><path d="M9 4v13M15 7v13"/></svg><em data-en="Map" data-cy="Map"></em></button>
    <button data-screen="vote"><svg viewBox="0 0 24 24"><path d="M3 13h18v7H3z"/><path d="m7 13 2-9h6l2 9"/><path d="M11 8h2"/></svg><em data-en="Vote" data-cy="Pleidlais"></em></button>
    <button data-screen="results"><svg viewBox="0 0 24 24"><path d="M8 21h8"/><path d="M12 17v4"/><path d="M7 4h10v5a5 5 0 0 1-10 0V4Z"/><path d="M17 5h3v2a3 3 0 0 1-3 3M7 5H4v2a3 3 0 0 0 3 3"/></svg><em data-en="Results" data-cy="Canlyniadau"></em></button>
    <button data-screen="info"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 11v5"/><path d="M12 8h.01"/></svg><em data-en="Info" data-cy="Gwybodaeth"></em></button>
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
<script src="assets/leaflet/leaflet.js"></script>
<script src="assets/app.js?v=2"></script>
</body>
</html>
