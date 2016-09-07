#!/bin/bash
python ingest.py http://www.denverpost.com/dont-miss/feed/ --slug dont-miss
python ingest.py http://www.denverpost.com/news/feed/ --slug hard-news
python ingest.py http://www.denverpost.com/sports/feed/ --slug sports
../ftp.bash --dir $REMOTE_DIR --host $REMOTE_HOST
curl -X PURGE http://extras.denverpost.com/app/in-article-promo/dont-miss-1.html
curl -X PURGE http://extras.denverpost.com/app/in-article-promo/dont-miss-2.html
curl -X PURGE http://extras.denverpost.com/app/in-article-promo/dont-miss-3.html
curl -X PURGE http://extras.denverpost.com/app/in-article-promo/dont-miss-4.html
curl -X PURGE http://extras.denverpost.com/app/in-article-promo/dont-miss-5.html
