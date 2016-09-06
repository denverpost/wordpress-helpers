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

    public function save() {
        $this->json = json_encode($this->items);
        file_put_contents($this->filename . '.json', $this->json);
        return True;
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
$articles_details = new Api('articles_detail');

if($_SERVER['REQUEST_METHOD'] === 'POST') {
    $articles_working = $articles_live->items;
    $articles_working[] = [
        'id'      => round(microtime(true) * 1000),
        'url'  => htmlspecialchars($_POST['url'])
    ];

    $articles_live->items = $articles_working;
    $articles_live->json = json_encode($articles_working, JSON_PRETTY_PRINT);
    $articles_live->save();
}
header('Content-Type: application/json');
header('Cache-Control: no-cache');
header('Access-Control-Allow-Origin: *');
echo $articles_live->json;
