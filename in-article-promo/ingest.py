#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Turn a RSS feed into a json object.
# Take a few entries from the json object and turn them into promos.
import argparse
import doctest
import sys
import json
import feedparser
import random
import string

def parse_template(data, template):
    """ Given the data and a template, return a string.
        """
    img_html = """<div class="thumb-wrap"><div class="thumb-holder"></div><a href="{{URL}}" target="_top"><div class="thumb-img" style="background-image:url('{{IMG}}');"></div></a></div>"""
    template = template.replace('{{URL}}', data['link'].replace('http:','https:'))
    template = template.replace('{{URLX}}', data['link'])
    template = template.replace('{{TITLE}}', data['title'])
    #template = template.replace('{{BLURB}}', data['summary'])
    img_html = img_html.replace('{{URL}}', data['link'].replace('http:','https:'))
    if hasattr(data, 'tags') and len(data['tags']) > 0:
        template = template.replace('{{SECTION}}', data['tags'][0]['term'])
    else:
        template = template.replace('<h2><a href="{{URL}}" target="_top">{{SECTION}}</a></h2>', '')
    if hasattr(data, 'media_content') and len(data['media_content']) > 0:
        template = template.replace('{{IMG}}', '%s?w=150' % data['media_content'][0]['url'].replace('http:','https:'))
    else:
        template = template.replace(img_html, '')

    return template

def main(args):
    fh = open('html/single.html', 'rb')
    template = fh.read()
    entries = []
    extras = ['dont-miss', 'hard-news', 'sports']
    extras = ['dont-miss']
    extras = []
    if args.slug in extras:
        jsonh = open('json/urls_live-%s.json' % args.slug)   
        entries.append(json.load(jsonh))

    for url in args.urls[0]:
        f = feedparser.parse(url)
        entries.append(f['entries'])

    random.shuffle(f['entries'])
    i = 1
    while i <= args.limit:
        if len(f['entries']) <= i:
            break
        print f['entries'][i-1]['link']
        fh = open('output/%s-%d.html' % (args.slug, i), 'wb')
        fh.write(parse_template(f['entries'][i-1], template).encode('utf-8', 'replace'))
        i += 1
            
            

def build_parser(args):
    """ This method allows us to test the args.
        >>> parser = build_parser(['-v'])
        >>> print args.verbose
        True
        """
    parser = argparse.ArgumentParser(usage='$ python ingest.py http://url-for-the-feed',
                                     description='Turn a feed into a json file.',
                                     epilog='')
    parser.add_argument("-v", "--verbose", dest="verbose", default=False, action="store_true",
                        help="Run doctests, display more info.")
    parser.add_argument("-s", "--slug", dest="slug", default="default",
                        help="What to name the output files")
    parser.add_argument("-l", "--limit", dest="limit", default=5,
                        help="How many files to write")
    parser.add_argument("urls", action="append", nargs="*")
    args = parser.parse_args(args)
    return args

if __name__ == '__main__':
    args = build_parser(sys.argv[1:])

    if args.verbose == True:
        doctest.testmod(verbose=args.verbose)
    main(args)
