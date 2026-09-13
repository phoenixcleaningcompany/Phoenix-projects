<?php
/**
 * Fills the database with the twelve houses and the three award categories,
 * giving each house a random check-in token for its QR code.
 *
 * Run once:  php tools/seed.php
 * Re-runs are safe — existing houses keep their tokens so printed QR codes
 * stay valid. Pass --reset-tokens only if you need to reprint everything.
 */

declare(strict_types=1);
require __DIR__ . '/../public/lib.php';

$resetTokens = in_array('--reset-tokens', $argv, true);

// NOTE: these twelve houses are placeholder content from the design
// prototype, and the coordinates are rough points around Llanwrtyd Wells
// picked to make the map previewable. None of it is surveyed. Replace the
// whole block when the real entrants are confirmed.
$houses = [
    [1,  'Bryn Awel',     'Dolecoed Road',    'The whole front garden is a lit-up sheep field, with a nativity in the porch and a soundtrack of carols on a loop.', 'Card reader at the gate', '4 min', 52.104, -3.6355],
    [2,  'Tŷ Gwyn',       'Irfon Terrace',    'Icicle lights across the whole terrace front and a fifteen-foot tree in the yard. Second year running.',            'Wheelchair-friendly pavement', '3 min', 52.107, -3.6295],
    [3,  'The Old Bakery','Zion Street',      'Warm-white only. Bread ovens lit from inside the old shop window with a moving baker silhouette.',                   'Quiet display, no music', '5 min', 52.1063, -3.632],
    [4,  'Llwyn Onn',     'Station Crescent', 'The big one. Roofline animation timed to music, 8,000 bulbs and a postbox for letters to the North Pole.',            'Music every 10 minutes', '6 min', 52.109, -3.627],
    [5,  "Gwesty'r Afon", 'Victoria Road',    'Lit archway over the path and a courtyard of lanterns. Mulled wine and hot chocolate from 6.30pm.',                   'Refreshments · card reader', '3 min', 52.1055, -3.634],
    [6,  'Cae Rhedyn',    'Garth Road',       'Inflatable snowman family, one of them enormous and slightly deflated, plus a llama in a Santa hat.',                 'Kids favourite', '7 min', 52.1085, -3.623],
    [7,  'Y Felin',       'Neuadd Road',      'The old mill wheel turning under blue light, with a lit stream running down to the road.',                            'Steep drive, watch your step', '4 min', 52.1045, -3.63],
    [8,  'Penlan',        'Ffos Road',        'Every window a different scene, done by the four children of the house. Judge them kindly.',                          'Collection tin in the porch', '8 min', 52.103, -3.638],
    [9,  'Hafod',         'Cwm Irfon Lane',   'Lanterns the whole length of the lane, then a lit barn at the end. Bring a torch for the dark stretch.',              'Refreshments · unlit lane', '9 min', 52.112, -3.652],
    [10, 'Rose Cottage',  'Dolecoed Road',    'A single tree, done properly, and about four hundred candles in jam jars along the wall.',                            'Quiet display, no music', '3 min', 52.1038, -3.635],
    [11, 'Nant y Coed',   'Chapel Street',    'Full brass band recording, a light show on the chapel gable, and a choir at 8pm if enough turn up.',                  'Live choir at 8pm', '5 min', 52.1068, -3.631],
    [12, 'Arwel',         'Wellington Road',  'A dinosaur in fairy lights. No explanation offered, none needed.',                                                    'Kids favourite', null, 52.105, -3.6285],
];

$categories = [
    ['best',  'Best overall display', 'Yr arddangosfa orau',  1],
    ['fun',   'Funniest',             'Y mwyaf doniol',       2],
    ['music', 'Best soundtrack',      'Y gerddoriaeth orau',  3],
];

$pdo = db();

foreach ($houses as [$stop, $name, $addr, $blurb, $note, $walk, $lat, $lng]) {
    $st = $pdo->prepare('SELECT id, token FROM houses WHERE stop_no = ?');
    $st->execute([$stop]);
    $existing = $st->fetch();

    if ($existing && !$resetTokens) {
        $up = $pdo->prepare(
            'UPDATE houses SET name = ?, address = ?, blurb_en = ?, note_en = ?, walk_en = ?, lat = ?, lng = ? WHERE id = ?'
        );
        $up->execute([$name, $addr, $blurb, $note, $walk, $lat, $lng, $existing['id']]);
        echo "updated  {$stop}  {$name}\n";
        continue;
    }

    $token = strtoupper(substr(bin2hex(random_bytes(8)), 0, 10));
    if ($existing) {
        $up = $pdo->prepare('UPDATE houses SET name=?, address=?, blurb_en=?, note_en=?, walk_en=?, lat=?, lng=?, token=? WHERE id=?');
        $up->execute([$name, $addr, $blurb, $note, $walk, $lat, $lng, $token, $existing['id']]);
        echo "retokened {$stop}  {$name}  {$token}\n";
    } else {
        $in = $pdo->prepare(
            'INSERT INTO houses (stop_no, name, address, blurb_en, note_en, walk_en, lat, lng, token, active)
             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1)'
        );
        $in->execute([$stop, $name, $addr, $blurb, $note, $walk, $lat, $lng, $token]);
        echo "added    {$stop}  {$name}  {$token}\n";
    }
}

foreach ($categories as [$slug, $en, $cy, $order]) {
    $st = $pdo->prepare('SELECT id FROM categories WHERE slug = ?');
    $st->execute([$slug]);
    if ($st->fetch()) {
        $pdo->prepare('UPDATE categories SET label_en=?, label_cy=?, sort_order=? WHERE slug=?')
            ->execute([$en, $cy, $order, $slug]);
    } else {
        $pdo->prepare('INSERT INTO categories (slug, label_en, label_cy, sort_order) VALUES (?,?,?,?)')
            ->execute([$slug, $en, $cy, $order]);
    }
    echo "category {$slug}\n";
}

echo "\nDone. Run tools/qr-links.php to get the twelve gate URLs.\n";
