#!/usr/bin/env python
# Turn a RSS feed into a json object.
import argparse
import doctest
import sys
import json

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
    parser.add_argument("filename", action="append", nargs="*")
    args = parser.parse_args(args)
    return args

if __name__ == '__main__':
    args = build_parser(sys.argv[1:])

    if args.verbose == True:
        doctest.testmod(verbose=args.verbose)
    main(args)
