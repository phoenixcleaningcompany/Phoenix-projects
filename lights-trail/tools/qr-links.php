<?php
/**
 * Prints the check-in URL for every house — one per gate.
 *
 *   php tools/qr-links.php https://yoursite.co.uk/lights
 *
 * Paste each URL into any QR generator, print it big, laminate it, and tape
 * it to the gatepost. Scanning it checks that house in.
 */

declare(strict_types=1);
require __DIR__ . '/../public/lib.php';

$base = rtrim($argv[1] ?? 'https://example.com/lights', '/');
$rows = db()->query('SELECT stop_no, name, token FROM houses WHERE active = 1 ORDER BY stop_no')->fetchAll();

if (!$rows) {
    exit("No houses yet — run tools/seed.php first.\n");
}

printf("%-5s %-18s %s\n", 'STOP', 'HOUSE', 'URL FOR THE QR CODE');
echo str_repeat('-', 86), "\n";
foreach ($rows as $r) {
    printf("%-5s %-18s %s/?c=%s\n", $r['stop_no'], $r['name'], $base, $r['token']);
}
echo "\nKeep these secret until the night — anyone with a URL can check in without visiting.\n";
