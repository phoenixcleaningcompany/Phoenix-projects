<?php
/**
 * Llanwrtyd Lights — settings.
 *
 * This is the only file you need to edit. Everything you fill in here comes
 * from cPanel > MySQL Databases, after you create a database and a user.
 */

return [
    // ---- Database ---------------------------------------------------------
    // On GoDaddy these look like: phoenix_lights / phoenix_lightsuser
    'db_host'     => 'localhost',
    'db_name'     => 'CHANGE_ME_database_name',
    'db_user'     => 'CHANGE_ME_database_user',
    'db_pass'     => 'CHANGE_ME_password',

    // ---- Event ------------------------------------------------------------
    'event_name_en' => 'Llanwrtyd Lights',
    'event_name_cy' => 'Golau Llanwrtyd',
    'event_date_en' => 'Thursday 18 December, 6–10pm',
    'event_date_cy' => 'Nos Iau 18 Rhagfyr, 6–10yh',

    // Voting closes at this time. After it, the ballot locks and results
    // stay visible. Use 24-hour time, server timezone below.
    'voting_closes' => '2025-12-18 22:30:00',
    'timezone'      => 'Europe/London',

    // Show the live running totals to the public before voting closes?
    // false keeps the result a surprise until the end.
    'live_results'  => true,

    // ---- Security ---------------------------------------------------------
    // Any long random string. Used to hash IP addresses so we never store
    // one in the clear. Change it once, then leave it alone — changing it
    // later resets the flood protection.
    'salt'          => 'CHANGE_ME_to_a_long_random_string',
];
