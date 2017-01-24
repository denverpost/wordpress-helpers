#!/bin/bash

# Add the articles
python2.7 ingest.py http://www.denverpost.com/dont-miss/feed/ --slug dont-miss
python2.7 ingest.py http://www.denverpost.com/news/feed/ --slug hard-news
python2.7 ingest.py http://www.denverpost.com/sports/feed/ --slug sports
python2.7 ingest.py http://www.denverpost.com/sports/denver-broncos/feed/ --slug broncos 
python2.7 ingest.py http://www.denverpost.com/ask-amy/feed/ --slug ask-amy
python2.7 ingest.py http://www.denverpost.com/travel/feed/ --slug travel
python2.7 ingest.py http://www.denverpost.com/lifestyle/food-drink/feed/ --slug food
python2.7 ingest.py http://www.denverpost.com/lifestyle/food-drink/feed/ --slug food-drink
python2.7 ingest.py http://www.denverpost.com/lifestyle/restaurants/feed/ --slug restaurants
python2.7 ingest.py http://www.denverpost.com/entertainment/books/feed/ --slug books
python2.7 ingest.py http://www.denverpost.com/entertainment/movies/feed/ --slug movies
python2.7 ingest.py http://www.denverpost.com/lifestyle/home-garden/feed/ --slug home-garden
python2.7 ingest.py http://www.denverpost.com/entertainment/feed/ --slug entertainment
python2.7 ingest.py http://www.denverpost.com/news/yourhub/feed/ --slug yourhub
python2.7 ingest.py http://www.denverpost.com/news/marijuana/feed/ --slug marijuana
python2.7 ingest.py http://www.denverpost.com/opinion/editorials/feed/ --slug editorials
python2.7 ingest.py http://www.denverpost.com/politics/feed/ --slug politics
python2.7 ingest.py http://www.denverpost.com/business/colorado-real-estate/feed/ --slug real-estate
python2.7 ingest.py http://www.denverpost.com/business/feed/ --slug business
python2.7 ingest.py http://www.denverpost.com/business/colorado-technology/feed/ --slug tech
python2.7 ingest.py http://www.denverpost.com/tag/featured-homes/feed/ --slug featured-homes
python2.7 ingest.py http://www.denverpost.com/season-to-share/feed/ --slug season-to-share
python2.7 ingest.py http://www.denverpost.com/tag/national-western-stock-show/feed/ --slug stock-show
python2.7 ingest.py http://www.denverpost.com/politics/colorado-legislature/feed/ --slug colorado-legislature
#python2.7 ingest.py  --slug 

# Bust the fast.ly cache
../ftp.bash --dir $REMOTE_DIR --host $REMOTE_HOST
for SECTION in dont-miss sports hard-news broncos ask-amy travel restaurants books movies home-garden entertainment yourhub marijuana editorials politics real-estate business tech food featured-homes food-drink season-to-share stock-show colorado-legislature; do
    for ITEM in {1..5}; do
        URL="https://extras.denverpost.com/app/in-article-promo/$SECTION-$ITEM.html"
        echo $URL
        curl -X PURGE $URL
        curl $URL > /dev/null
    done
done
