#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Convert times in a large swath of text to a different timezone
# See https://github.com/denverpost/wordpress-helpers/issues/1
import sys
import argparse
import re
import string
import doctest

class Timezoner:

    def __init__(self):
        """
            """
        self.times = []
        self.patterns = [
                # 3-7 p.m. & 12:30-1:30 a.m.
                '(([0-9]{1,2})([:0-9]{3})?-([0-9]{1,2})([:0-9]{3})?\ ?([ap]+\.m\.))',
                # 8 a.m.-6 p.m. & 10:30 a.m.-3 p.m. & 11 a.m.-1 a.m.
                '(([0-9]{1,2})([:0-9]{3})? ?([ap]+\.m\.)-([0-9]{1,2})([:0-9]{3})?\ ?([ap]+\.m\.))',
                # Noon-5 p.m. & Noon-3:30 a.m.
                #'Noon-([0-9]{1,2})([:0-9]{3})?\ ?([ap]+\.m\.)',
                # 9 a.m.-Midnight
                #'([0-9]{1,2})([:0-9]{3})?\ ?([ap]+\.m\.)',
                ]

    def replace_midnights(self, text):
        """ Replace all noons and midnights in the text with 12 p.m. and 12 a.m.,
            or vice versa.
            We know which way we want to replace if there are no instances of noon/midnight.
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
            parts = regex.findall(text)
            print parts

    def change_timezone(self, timezone):
        """ Takes the hour-difference (+2, -3, etc.) and converts the times we've extracted.
            Returns an updated dict.
            """
        pass

    def rewrite_text(self, text):
        """ Updates the text with the new times. Returns the text.
            """
        pass

def main(args):
    """ This method fires when we run this from the command line, and it's an
        example of how you might run it if you include the script elsewhere.
        """
    tz = Timezoner()
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
