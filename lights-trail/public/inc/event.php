<?php
/**
 * Every fact about the event lives here, so the pages stay about wording and
 * layout. Anything still unconfirmed is wrapped in todo() so it shows up
 * clearly on the page instead of reading as settled.
 */

return [
    'name'      => 'Llanwrtyd Lights',
    'name_cy'   => 'Golau Llanwrtyd',
    'tagline'   => 'One night. Twelve lit-up houses. The whole town out walking.',

    // CONFIRM: 18 December 2026 is a Friday. Last year's was a Thursday.
    'date_text' => 'Friday 18 December 2026',
    'date_iso'  => '2026-12-18',
    'times'     => '6pm – 10pm',
    'date_confirmed' => false,

    'town'      => 'Llanwrtyd Wells',
    'county'    => 'Powys',

    'charity'        => 'the local primary school',
    'charity_confirmed' => false,
    'raised_last_year'  => null, // CONFIRM: last year's total, if you want it on the page

    'attractions' => [
        [
            'slug'  => 'trail',
            'title' => 'The lights trail',
            'lede'  => 'Twelve houses across the town switch their displays on for one night only.',
            'body'  => 'Walk the route at your own pace — about an hour and a half if you stop and look properly. Scan the code on each gatepost as you arrive and the trail ticks itself off on your phone. At the end you vote for the best display, the funniest, and the best soundtrack.',
            'meta'  => ['All evening', 'Free', 'On foot'],
            'icon'  => 'trail',
        ],
        [
            'slug'  => 'grotto',
            'title' => "Santa's grotto",
            'lede'  => 'For the little ones, before it gets too late.',
            'body'  => 'Every child comes away with a present. Expect a queue at the start of the evening — it is usually quieter after eight.',
            'meta'  => ['CONFIRM times', 'CONFIRM price', 'CONFIRM location'],
            'icon'  => 'gift',
        ],
        [
            'slug'  => 'reindeer',
            'title' => 'The reindeer',
            'lede'  => 'Real ones, in a pen, being extremely calm about the whole thing.',
            'body'  => 'Come and meet them. Please do not feed them anything — they are on a strict diet and their handlers will tell you off.',
            'meta'  => ['CONFIRM times', 'Free', 'CONFIRM location'],
            'icon'  => 'deer',
        ],
        [
            'slug'  => 'food',
            'title' => 'Food and drink',
            'lede'  => 'Mulled wine, hot chocolate, and something hot to eat.',
            'body'  => 'Several houses on the trail put on refreshments at the gate, and there is more in the centre of town. Bring cash as well as a card — signal can be patchy and card readers do not always cooperate.',
            'meta'  => ['From 6pm', 'Cash and card'],
            'icon'  => 'cup',
        ],
        [
            'slug'  => 'collection',
            'title' => 'The collection',
            'lede'  => 'The reason the whole thing happens.',
            'body'  => 'Every collection tin on the trail goes to the same place. Several houses have a card reader at the gate if you are not carrying cash.',
            'meta'  => ['All evening'],
            'icon'  => 'heart',
        ],
    ],
];
