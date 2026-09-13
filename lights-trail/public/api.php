<?php
/**
 * Single endpoint for the whole app: ?action=state|checkin|vote|results
 */

declare(strict_types=1);
require __DIR__ . '/lib.php';

$action = $_GET['action'] ?? 'state';
$device = device_id();

try {
    switch ($action) {

        // Everything the page needs on load: the trail, your progress, your picks.
        case 'state': {
            $houses = db()->query(
                'SELECT id, stop_no, name, address, blurb_en, blurb_cy, note_en, note_cy
                   FROM houses WHERE active = 1 ORDER BY stop_no'
            )->fetchAll();

            $cats = db()->query(
                'SELECT id, slug, label_en, label_cy FROM categories ORDER BY sort_order, id'
            )->fetchAll();

            $st = db()->prepare('SELECT house_id FROM checkins WHERE device_id = ?');
            $st->execute([$device]);
            $visited = array_map('intval', array_column($st->fetchAll(), 'house_id'));

            $st = db()->prepare('SELECT category_id, house_id FROM votes WHERE device_id = ?');
            $st->execute([$device]);
            $picks = [];
            foreach ($st->fetchAll() as $r) {
                $picks[(int) $r['category_id']] = (int) $r['house_id'];
            }

            json_out([
                'ok'           => true,
                'houses'       => $houses,
                'categories'   => $cats,
                'visited'      => $visited,
                'picks'        => (object) $picks,
                'voting_open'  => voting_open(),
                'live_results' => (bool) cfg()['live_results'],
            ]);
        }

        // Arriving at a gate: the QR code carries ?c=<token>.
        case 'checkin': {
            if (!rate_ok('checkin', 40)) {
                json_out(['ok' => false, 'error' => 'slow_down'], 429);
            }
            $token = trim((string) ($_POST['token'] ?? $_GET['c'] ?? ''));
            if ($token === '') {
                json_out(['ok' => false, 'error' => 'no_token'], 400);
            }

            $st = db()->prepare('SELECT id, stop_no, name FROM houses WHERE token = ? AND active = 1');
            $st->execute([$token]);
            $house = $st->fetch();
            if (!$house) {
                json_out(['ok' => false, 'error' => 'unknown_token'], 404);
            }

            // Scanning the same gate twice is normal and must not error.
            $ins = db()->prepare(
                db()->getAttribute(PDO::ATTR_DRIVER_NAME) === 'sqlite'
                    ? 'INSERT OR IGNORE INTO checkins (device_id, house_id, created_at, ip_hash) VALUES (?, ?, ?, ?)'
                    : 'INSERT IGNORE INTO checkins (device_id, house_id, created_at, ip_hash) VALUES (?, ?, ?, ?)'
            );
            $ins->execute([$device, (int) $house['id'], now(), ip_hash()]);

            $st = db()->prepare('SELECT COUNT(*) AS n FROM checkins WHERE device_id = ?');
            $st->execute([$device]);

            json_out([
                'ok'      => true,
                'house'   => ['id' => (int) $house['id'], 'stop_no' => (int) $house['stop_no'], 'name' => $house['name']],
                'visited' => (int) $st->fetch()['n'],
                'fresh'   => $ins->rowCount() > 0,
            ]);
        }

        // Casting or changing a vote in one category.
        case 'vote': {
            if (!voting_open()) {
                json_out(['ok' => false, 'error' => 'voting_closed'], 403);
            }
            if (!rate_ok('vote', 30)) {
                json_out(['ok' => false, 'error' => 'slow_down'], 429);
            }
            $cat   = (int) ($_POST['category_id'] ?? 0);
            $house = (int) ($_POST['house_id'] ?? 0);

            $st = db()->prepare('SELECT 1 FROM categories WHERE id = ?');
            $st->execute([$cat]);
            if (!$st->fetch()) {
                json_out(['ok' => false, 'error' => 'bad_category'], 400);
            }
            $st = db()->prepare('SELECT 1 FROM houses WHERE id = ? AND active = 1');
            $st->execute([$house]);
            if (!$st->fetch()) {
                json_out(['ok' => false, 'error' => 'bad_house'], 400);
            }

            $sql = db()->getAttribute(PDO::ATTR_DRIVER_NAME) === 'sqlite'
                ? 'INSERT INTO votes (device_id, category_id, house_id, created_at, updated_at, ip_hash)
                   VALUES (:d, :c, :h, :t, :t, :i)
                   ON CONFLICT (device_id, category_id) DO UPDATE SET house_id = :h2, updated_at = :t2'
                : 'INSERT INTO votes (device_id, category_id, house_id, created_at, updated_at, ip_hash)
                   VALUES (:d, :c, :h, :t, :t, :i)
                   ON DUPLICATE KEY UPDATE house_id = :h2, updated_at = :t2';
            $st = db()->prepare($sql);
            $st->execute([
                ':d' => $device, ':c' => $cat, ':h' => $house, ':t' => now(),
                ':i' => ip_hash(), ':h2' => $house, ':t2' => now(),
            ]);

            json_out(['ok' => true, 'category_id' => $cat, 'house_id' => $house]);
        }

        // Live tally. Hidden until close if the organiser wants a reveal.
        case 'results': {
            if (!cfg()['live_results'] && voting_open()) {
                json_out(['ok' => true, 'hidden' => true, 'results' => []]);
            }
            $rows = db()->query(
                'SELECT c.id AS category_id, c.slug, h.id AS house_id, h.name, h.stop_no,
                        COUNT(v.id) AS votes
                   FROM categories c
                   CROSS JOIN houses h
                   LEFT JOIN votes v ON v.category_id = c.id AND v.house_id = h.id
                  WHERE h.active = 1
                  GROUP BY c.id, c.slug, h.id, h.name, h.stop_no
                  ORDER BY c.sort_order, votes DESC, h.stop_no'
            )->fetchAll();

            $out = [];
            foreach ($rows as $r) {
                $out[$r['slug']][] = [
                    'house_id' => (int) $r['house_id'],
                    'name'     => $r['name'],
                    'stop_no'  => (int) $r['stop_no'],
                    'votes'    => (int) $r['votes'],
                ];
            }
            $st = db()->query('SELECT COUNT(DISTINCT device_id) AS n FROM votes');
            json_out([
                'ok'      => true,
                'hidden'  => false,
                'results' => $out,
                'voters'  => (int) $st->fetch()['n'],
                'open'    => voting_open(),
            ]);
        }

        default:
            json_out(['ok' => false, 'error' => 'unknown_action'], 404);
    }
} catch (Throwable $e) {
    error_log('[lights-trail] ' . $e->getMessage());
    json_out(['ok' => false, 'error' => 'server_error'], 500);
}
