#!/bin/bash
python ingest.py http://www.denverpost.com/dont-miss/feed/
../ftp.bash --dir $REMOTE_DIR --host $REMOTE_HOST
curl -X PURGE http://extras.denverpost.com/app/in-article-promo/dont-miss-1.html
curl -X PURGE http://extras.denverpost.com/app/in-article-promo/dont-miss-2.html
curl -X PURGE http://extras.denverpost.com/app/in-article-promo/dont-miss-3.html
curl -X PURGE http://extras.denverpost.com/app/in-article-promo/dont-miss-4.html
curl -X PURGE http://extras.denverpost.com/app/in-article-promo/dont-miss-5.html
