<?php
// We store two main lists: One of the active URLs we're promoting,
// the other of all the article URLs and their corresponding headline and section and image URL.
class Api {
    // Handle file writing and reading
    public $items = '';
    public $filename = '';

    public function __construct($filename)
    {
        $this->filename = $filename;
        $this->json = file_get_contents($filename . '.json');
        $this->items = json_decode($this->json);
    }

    public function get() { 
        return $this->json;
    }

    public function post() {
    }

}

class Article {
    // Handle getting and storing detailed article information
    public $url;

    public function __construct($url)
    {
        $this->url = $url;
    }

    public function retrieve() {
    }

}


$articles_live = new Api('articles_live');
$articles_db = new Api('articles_db');

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
