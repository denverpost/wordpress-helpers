<?php
// We store two main lists: One of the active URLs we're promoting,
// the other of all the article URLs and their corresponding headline and section and image URL.
class Api {
    // Handle file writing and reading
    public $items = '';
    public $filename = '';

    public function get() { }
    public function post() { }

}

class Article {
    // Handle getting and storing detailed article information
    public $url;

    public function retrieve() {
    }

}

$live_articles = file_get_contents('articles.json');
if($_SERVER['REQUEST_METHOD'] === 'POST') {
    $articlesDecoded = json_decode($articles, true);
    $articlesDecoded[] = [
        'id'      => round(microtime(true) * 1000),
        'url'  => $_POST['url']
    ];

    $articles = json_encode($articlesDecoded, JSON_PRETTY_PRINT);
    file_put_contents('articles.json', $articles);
}
header('Content-Type: application/json');
header('Cache-Control: no-cache');
header('Access-Control-Allow-Origin: *');
echo $articles;
