#!/usr/bin/env python
# Convert times in a large swath of text to a different timezone
# See https://github.com/denverpost/wordpress-helpers/issues/1
import sys
import argparse
import re
import string
import doctest

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
