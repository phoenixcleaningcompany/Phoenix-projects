<?php
declare(strict_types=1);
require __DIR__ . '/inc/layout.php';
require __DIR__ . '/inc/posts.php';

$slug = preg_replace('/[^a-z0-9-]/', '', (string) ($_GET['p'] ?? ''));
$post = $slug === '' ? null : find_post($slug);

if (!$post) {
    http_response_code(404);
    page_head('Not found', 'That post does not exist.', 'blog');
    echo '<section class="hero"><div class="wrap"><h1>Not found</h1>'
       . '<p class="lead">That post is not here. <a href="blog.php">All the news</a>.</p>'
       . '</div></section>';
    page_foot();
    exit;
}

page_head($post['title'], $post['summary'], 'blog');
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
    <div class="actions"><a class="btn ghost" href="blog.php">All the news</a></div>
  </div>
</section>
<?php page_foot(); ?>
