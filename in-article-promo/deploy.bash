#!/bin/bash
python2.7 ingest.py http://www.denverpost.com/dont-miss/feed/ --slug dont-miss
python2.7 ingest.py http://www.denverpost.com/news/feed/ --slug hard-news
python2.7 ingest.py http://www.denverpost.com/sports/feed/ --slug sports

../ftp.bash --dir $REMOTE_DIR --host $REMOTE_HOST
for SECTION in dont-miss sports hard-news; do
    for ITEM in {1..5}; do
        curl -X PURGE http://extras.denverpost.com/app/in-article-promo/$SECTION-$ITEM.html
    done
done
