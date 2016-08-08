#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Convert times in a large swath of text to a different timezone
# See https://github.com/denverpost/wordpress-helpers/issues/1
import sys
import argparse
import re
import string
import doctest
from datetime import time, timedelta

class Timezoner:

    def __init__(self):
        """
            """
        self.times = []
        self.timezone = 0
        self.timedelta = timedelta()
        self.patterns = [
                # 3-7 p.m. & 12:30-1:30 a.m.
                #'(([0-9]{1,2})([:0-9]{3})?-([0-9]{1,2})([:0-9]{3})?\ ?([ap]+\.m\.))',
                '(?P<original>(?P<from_hour>[0-9]{1,2})(?P<from_minute>[:0-9]{3})?-(?P<to_hour>[0-9]{1,2})(?P<to_minute>[:0-9]{3})?\ ?(?P<to_ampm>[ap]+\.m\.))',
                # 8 a.m.-6 p.m. & 10:30 a.m.-3 p.m. & 11 a.m.-1 a.m.
                #'(([0-9]{1,2})([:0-9]{3})? ?([ap]+\.m\.)-([0-9]{1,2})([:0-9]{3})?\ ?([ap]+\.m\.))',
                '(?P<original>(?P<from_hour>[0-9]{1,2})(?P<from_minute>[:0-9]{3})? ?(?P<from_ampm>[ap]+\.m\.)-(?P<to_hour>[0-9]{1,2})(?P<to_minute>[:0-9]{3})?\ ?(?P<to_ampm>[ap]+\.m\.))',
                ]

    def set_timedelta(self):
        """ Once self.timezone is set, run this to create the self.timedelta
            object.
            >>> tz = Timezoner()
            >>> tz.timezone = -3
            >>> tz.set_timedelta()
            True
            """
        self.timedelta = timedelta(hours=self.timezone)
        return True

    def replace_midnights(self, text):
        """ Replace all noons and midnights in the text with 12 p.m. and 12 a.m.,
            or vice versa.
            We know which way we want to replace if there are no instances of noon/midnight.
            >>> tz = Timezoner()
            >>> tz.replace_midnights("Hi it's Midnight again. No, it's Noon.")
            "Hi it's 12 a.m. again. No, it's 12 p.m.."
            >>> tz.replace_midnights("Hi it's again. No, it's.")
            "Hi it's again. No, it's."
            >>> tz.replace_midnights("Hi it's 12 a.m. again. No, it's 12 p.m..")
            "Hi it's Midnight again. No, it's Noon."
            """
        if 'Noon' not in text and 'Midnight' not in text:
            text = text.replace('12 a.m.', 'Midnight')
            text = text.replace('12 p.m.', 'Noon')
        else:
            text = text.replace('Midnight', '12 a.m.')
            text = text.replace('Noon', '12 p.m.')
        return text

    def extract_parts(self, text=''):
        """ Extract all the times and time ranges, returns a dict.
            Dict will include original and replacement strings.
            Regex will seek out times that match these patterns:
                3-7 p.m.
                12:30-1:30 a.m.
                8 a.m.-6 p.m.
                10:30 a.m.-3 p.m.
                11 a.m.-1 a.m.
                12:30 p.m.-11 p.m.
                12 p.m.-5 p.m.
                #Noon-3:30 a.m.
                #9 a.m.-Midnight
                #8 p.m.-Midnight
                #Noon-Midnight
            """
        if text == '':
            text = self.text

        for pattern in self.patterns:
            regex = re.compile(pattern)
            r = regex.search(text)
            parts = regex.match(text)
            d = r.groupdict()

            # Add each result to self.times
            #d = {'original': item[0], 'parts': item[1:], 'converted': ''}
            #print d
            #d.converted = self.change_timezone(d)

    def change_timezone(self, d):
        """ Take a dict of the original time (both the full string and the parts,
            and assuming self.timezone is set to the hour difference (+2, -3, etc.),
            it converts the times we've extracted.
            This is what a dict may look like:
                {'from_minute': ':35', 'original': '12:35-1:35 a.m.', 'to_ampm': 'a.m.', 'from_hour': '12', 'to_hour': '1', 'to_minute': ':35'}
            Or
                {'from_minute': None, 'original': '7 p.m.-12 a.m.', 'to_ampm': 'a.m.', 'from_hour': '7', 'from_ampm': 'p.m.', 'to_hour': '12', 'to_minute': None}
            Returns the converted time string.
            """
        d['from_minutes'] = self.clean_minutes(d['from_minutes'])
        d['to_minutes'] = self.clean_minutes(d['to_minutes'])
        from_time = time(hours=d['from_hour'], minutes=d['from_minutes'])

    def clean_minutes(self, m):
        """ Minute strings come in as None and as ":30" or ":35", this standardizes that.
            >>> tz = Timezoner()
            >>> tz.clean_minutes(None)
            0
            >>> tz.clean_minutes(":30")
            '30'
            """
        if m:
            m = m.lstrip(':')
        else:
            m = 0
        return m

    def rewrite_text(self, text):
        """ Updates the text with the new times. Returns the text.
            """
        pass

def main(args):
    """ This method fires when we run this from the command line, and it's an
        example of how you might run it if you include the script elsewhere.
        """
    tz = Timezoner()
    tz.timezone = -2
    tz.set_timedelta()
    tz.text = tz.replace_midnights(" Gold Medal Final, 7 p.m.-Midnight. Women's Gymnastics - Team Competition, 12:35-1:35 a.m.")
    tz.extract_parts()
        


def build_parser(args):
    """ This method allows us to test the args.
        >>> args = build_parser(['--verbose'])
        >>> print args.verbose
        True
        """
    parser = argparse.ArgumentParser(usage='$ python timezoner.py',
                                     description='Convert the timezone in a large swath of unstructured text.',
                                     epilog='Examply use: python timezoner.py')
    parser.add_argument("-v", "--verbose", dest="verbose", default=False, action="store_true")
    args = parser.parse_args(args)
    return args

if __name__ == '__main__':
    args = build_parser(sys.argv[1:])

    if args.verbose == True:
        doctest.testmod(verbose=args.verbose)
    main(args)
