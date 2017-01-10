# Wordpress Helpers
Small apps to help streamline article production

## How To's

### How to add a new feed to the in-article-promo

1. Add the feed URL to in-article-promo/deploy.bash on its own line, ala `python2.7 ingest.py http://www.denverpost.com/news/feed/ --slug hard-news`
2. Add the slug to the list of slugs in the "Bust the fast.ly cache" portion of deploy.bash
