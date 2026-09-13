<?php
/**
 * Shared plumbing: database, device identity, light-touch flood protection.
 */

declare(strict_types=1);

function cfg(): array
{
    static $cfg = null;
    if ($cfg === null) {
        // config.local.php lets you keep real credentials out of version
        // control, and is what the development sqlite setup uses.
        $local = __DIR__ . '/config.local.php';
        $cfg = require is_readable($local) ? $local : __DIR__ . '/config.php';
        date_default_timezone_set($cfg['timezone'] ?? 'Europe/London');
    }
    return $cfg;
}

function db(): PDO
{
    static $pdo = null;
    if ($pdo !== null) {
        return $pdo;
    }
    $c = cfg();

    // A local sqlite file is used for development; GoDaddy gets MySQL.
    if (($c['db_name'] ?? '') === 'sqlite') {
        $pdo = new PDO('sqlite:' . ($c['db_path'] ?? __DIR__ . '/../dev.sqlite'));
        $pdo->exec('PRAGMA foreign_keys = ON');
    } else {
        $dsn = sprintf('mysql:host=%s;dbname=%s;charset=utf8mb4', $c['db_host'], $c['db_name']);
        $pdo = new PDO($dsn, $c['db_user'], $c['db_pass']);
    }
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    $pdo->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_ASSOC);
    return $pdo;
}

/**
 * Every phone gets a random id, kept in a cookie for a year. No accounts,
 * no names, no personal data — it exists only so one phone counts once.
 */
function device_id(): string
{
    if (!empty($_COOKIE['llt_device']) && preg_match('/^[a-f0-9]{32}$/', $_COOKIE['llt_device'])) {
        return $_COOKIE['llt_device'];
    }
    $id = bin2hex(random_bytes(16));
    setcookie('llt_device', $id, [
        'expires'  => time() + 31536000,
        'path'     => '/',
        'secure'   => !empty($_SERVER['HTTPS']),
        'httponly' => false, // the page reads it too, so results can highlight "your" picks
        'samesite' => 'Lax',
    ]);
    $_COOKIE['llt_device'] = $id;
    return $id;
}

function ip_hash(): string
{
    $ip = $_SERVER['HTTP_CF_CONNECTING_IP'] ?? $_SERVER['REMOTE_ADDR'] ?? '';
    return hash('sha256', cfg()['salt'] . '|' . $ip);
}

function voting_open(): bool
{
    $closes = cfg()['voting_closes'] ?? null;
    return $closes === null || time() < strtotime($closes);
}

function now(): string
{
    return date('Y-m-d H:i:s');
}

/**
 * Crude but sufficient: cap how many writes one address can make per minute.
 * A whole family on one wifi is fine; a script hammering the ballot is not.
 */
function rate_ok(string $bucket, int $limit = 30): bool
{
    $key  = $bucket . ':' . ip_hash();
    $file = sys_get_temp_dir() . '/llt_' . hash('sha256', $key);
    $now  = time();
    $hits = [];
    if (is_readable($file)) {
        $hits = array_filter(
            explode(',', (string) file_get_contents($file)),
            fn($t) => is_numeric($t) && $now - (int) $t < 60
        );
    }
    if (count($hits) >= $limit) {
        return false;
    }
    $hits[] = $now;
    @file_put_contents($file, implode(',', $hits), LOCK_EX);
    return true;
}

function json_out($data, int $status = 200): never
{
    http_response_code($status);
    header('Content-Type: application/json; charset=utf-8');
    header('Cache-Control: no-store');
    echo json_encode($data, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
    exit;
}
