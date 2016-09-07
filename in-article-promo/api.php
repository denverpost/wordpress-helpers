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
        $this->json = file_get_contents('json/' . $filename . '.json');
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
        file_put_contents('json/' . $this->filename . '.json', $this->json);
        return True;
    }

}

class Url {
    // Handle retrieving detailed url information
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
        if ( $this->article['title'] == NULL ):
            preg_match('/<title>([^<]+)<\/title/', $markup, $matches);
            $this->article['title'] = trim($matches[1]);
        endif;
        preg_match('#<meta name="twitter:image" content="([^?]+)\?w=640"#', $markup, $matches);
        $this->article['image'] = $matches[1];
        if ( $this->article['image'] == NULL ):
            $this->article['image'] = 'http://www.denverpost.com/wp-content/themes/denverpost/static/images/noimage.jpg';
        endif;
        preg_match("#'Section' : '([^']+)',#", $markup, $matches);
        $this->article['section'] = $matches[1];
        $this->article['link'] = $this->url;

        return $this->article;
    }

}


$urls_live = [ 
                'dont-miss' => new Api('urls_live-dont-miss'),
                'hard-news' => new Api('urls_live-hard-news'),
                'sports' => new Api('urls_live-sports')
            ];
$urls_detail = new Api('urls_detail');

if ( $_SERVER['REQUEST_METHOD'] === 'POST'):
    $url = htmlspecialchars($_POST['url']);
    $action = htmlspecialchars($_POST['action']);
    $articles_working = $urls_live['dont-miss']->items;


    // See if we already have metadata for this URL in our details json file.
    $detail = $urls_detail->find($url);
    if ( $detail === False ):
        $article = new Url($url);
        $detail = $article->retrieve();
        $detail['id'] = round(microtime(true) * 1000);
        $urls_detail->items[] = $detail;
        $urls_detail->save();
    endif;

    if ( $action == 'delete' ):
        $articles_tmp = [];
        foreach ( $articles_working as $key => $value ):
            if ( $url !== $value->url ):
                $articles_tmp[] = $value;
            endif;
        endforeach;
        $articles_working = $articles_tmp;
    else:
        $articles_working[] = $detail;
    endif;


    $urls_live['dont-miss']->items = $articles_working;
    $urls_live['dont-miss']->json = json_encode($articles_working, JSON_PRETTY_PRINT);
    $urls_live['dont-miss']->save();
endif;

header('Content-Type: application/json');
header('Cache-Control: no-cache');
header('Access-Control-Allow-Origin: *');
echo $urls_live['dont-miss']->json;
