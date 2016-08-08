#!/usr/bin/env python
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
        pass

    def extract_parts(self, text):
        """ Extract all the times and time ranges, returns a dict.
            Dict will include original and replacement strings.
            Regex will seek out times that match these patterns:
                8 a.m.-6 p.m.
                12:30-1:30 a.m.
                Noon-5 p.m.
                3-7 p.m.
            """
        pass

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
