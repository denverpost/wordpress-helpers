#!/bin/bash
python2.7 ingest.py http://www.denverpost.com/dont-miss/feed/ --slug dont-miss
python2.7 ingest.py http://www.denverpost.com/news/feed/ --slug hard-news
python2.7 ingest.py http://www.denverpost.com/sports/feed/ --slug sports
python2.7 ingest.py http://www.denverpost.com/sports/denver-broncos/feed/ --slug broncos 

../ftp.bash --dir $REMOTE_DIR --host $REMOTE_HOST
for SECTION in dont-miss sports hard-news broncos; do
    for ITEM in {1..5}; do
        URL="http://extras.denverpost.com/app/in-article-promo/$SECTION-$ITEM.html"
        echo $URL
        curl -X PURGE $URL
        curl $URL > /dev/null
    done
done
