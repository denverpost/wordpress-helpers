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

    public function find($value, $field='url') { 
        foreach ( $this->items as $key => $val ):
           if ( $this->items[$key]->$field == $value ):
                return $this->items[$key];
            endif;
        endforeach;
        return False;
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
    // Handle retrieving detailed article information
    public $url;
    public $article;

    public function __construct($url)
    {
        $this->url = $url;
    }

    public function retrieve() {
        // Download the markup, then process it.       
        $url = str_replace('&amp;','&',$this->url);
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $url);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
        curl_setopt($ch, CURLOPT_FOLLOWLOCATION, 1);
        $markup = curl_exec($ch);
        curl_close($ch);

        preg_match('/<meta property="og:title" content="([^"]+)" \/>/', $markup, $matches);
        $this->article['title'] = trim($matches[1]);
        preg_match('#<meta name="twitter:image" content="([^?]+)\?w=640"#', $markup, $matches);
        $this->article['image'] = $matches[1];
        preg_match("#'Section' : '([^']+)',#", $markup, $matches);
        $this->article['section'] = $matches[1];

        return $this->article;
    }

}


$articles_live = new Api('articles_live');
$articles_detail = new Api('articles_detail');

if ( $_SERVER['REQUEST_METHOD'] === 'POST'):
    $url = htmlspecialchars($_POST['url']);
    $action = htmlspecialchars($_POST['action']);
    $articles_working = $articles_live->items;


    // See if we already have metadata for this URL in our details json file.
    $detail = $articles_detail->find($url);
    if ( $detail === False ):
        $article = new Article($url);
        $detail = $article->retrieve();
        $articles_detail->items[] = $detail;
        $articles_detail->save();
    endif;

    if ( $action == 'delete' ):
        $articles_tmp = [];
        foreach ( $articles_working as $key => $value ):
            var_dump($value);
            if ( $url !== $value->url ):
                $articles_tmp[] = $value;
            endif;
        endforeach;
        $articles_working = $articles_tmp;
    else:
        $detail['id'] = round(microtime(true) * 1000);
        $detail['url'] = $url;
        $articles_working[] = $detail;
    endif;


    $articles_live->items = $articles_working;
    $articles_live->json = json_encode($articles_working, JSON_PRETTY_PRINT);
    $articles_live->save();
endif;
header('Content-Type: application/json');
header('Cache-Control: no-cache');
header('Access-Control-Allow-Origin: *');
echo $articles_live->json;
