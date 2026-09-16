<?php
declare(strict_types=1);
require __DIR__ . '/inc/layout.php';
require __DIR__ . '/inc/content.php';

$slug = preg_replace('/[^a-z0-9-]/', '', (string) ($_GET['p'] ?? ''));
$post = $slug === '' ? null : find_item('posts', $slug);

if (!$post) {
    http_response_code(404);
    page_head('Not found', 'That post does not exist.', 'news');
    echo '<section class="hero"><div class="wrap"><h1>Not found</h1>'
       . '<p class="lead">That post is not here. <a href="' . u('news') . '">All the news</a>.</p>'
       . '</div></section>';
    page_foot();
    exit;
}

page_head($post['title'], $post['summary'], 'news', item_url($post));
?>
<section class="hero">
  <div class="wrap">
    <div class="kicker"><?= e(post_date($post['date'])) ?></div>
    <h1><?= e($post['title']) ?></h1>
    <p class="lead"><?= e($post['summary']) ?></p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <article class="article"><?= $post['body'] ?></article>
    <div class="actions"><a class="btn ghost" href="<?= u('news') ?>">All the news</a></div>
  </div>
</section>
<?php page_foot(); ?>
