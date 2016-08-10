#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Convert times in a large swath of text to a different timezone
# See https://github.com/denverpost/wordpress-helpers/issues/1
import sys
import argparse
import re
import string
import doctest
from datetime import datetime, time, timedelta

class Timezoner:
    """ Convert a times in any amount of text to a different timezone.
        Times replaced are those that follow the Associated Press style for
        time ranges. Note that because we want named dicts on the regex search,
        and that named patterns aren't supported by re.findall, that only the
        first time range on each line will be matched.

        Because of this it's necessary to run the search and replace until
        there are no matches left.
        """

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
        """ Extract all the times and time ranges, build the replacement strings,
            and return the number of times matched / processed.
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
            >>> tz = Timezoner()
            >>> tz.timezone = -3
            >>> tz.set_timedelta()
            True
            >>> print tz.extract_parts("Golf Central Live From the Olympics, 5-6:30 a.m. & 3-5 p.m.; Women's Golf - 3rd Round (LIVE), 6:30 a.m.-3 p.m.")
            2
            >>> print tz.times[0]['converted']
            '2-3:30 a.m.'
            """
        if text == '':
            text = self.text

        # Add each result, as well as its converted time, to self.times
        for pattern in self.patterns:
            regex = re.compile(pattern)
            r = regex.search(text)
            parts = regex.match(text)
            d = r.groupdict()

            d = self.change_timezone(d)
            d['converted'] = self.datetime_to_string(d['from_time'], d['to_time'])
            self.times.append(d)

        return len(self.times)

    def change_timezone(self, d):
        """ Take a dict of the original time (both the full string and the parts,
            and assuming self.timezone is set to the hour difference (+2, -3, etc.),
            it converts the times we've extracted.
            This is what a dict may look like:
                {'from_minute': ':35', 'original': '12:35-1:35 a.m.', 'to_ampm': 'a.m.', 'from_hour': '12', 'to_hour': '1', 'to_minute': ':35'}
            Or
                {'from_minute': None, 'original': '7 p.m.-12 a.m.', 'to_ampm': 'a.m.', 'from_hour': '7', 'from_ampm': 'p.m.', 'to_hour': '12', 'to_minute': None}
            Returns the d dict with values added for from_time and to_time.
            >>> tz = Timezoner()
            >>> tz.timezone = -3
            >>> tz.set_timedelta()
            True
            >>> d = {'from_minute': ':35', 'original': '12:35-1:35 a.m.', 'to_ampm': 'a.m.', 'from_hour': '12', 'to_hour': '1', 'to_minute': ':35'}
            >>> d = tz.change_timezone(d)
            >>> print d['from_time'].hour, d['from_time'].minute
            9 35
            """
        d['from_minute'] = self.clean_minute(d['from_minute'])
        d['to_minute'] = self.clean_minute(d['to_minute'])

        if 'from_ampm' not in d:
            d['from_ampm'] = d['to_ampm']

        # Adjust the hour for the pm times.
        if d['from_ampm'] == 'p.m.':
            d['from_hour'] = int(d['from_hour']) + 12
        elif d['from_ampm'] == 'a.m.' and int(d['from_hour']) == 12:
            d['from_hour'] = 0
        if d['to_ampm'] == 'p.m.':
            d['to_hour'] = int(d['to_hour']) + 12
        elif d['to_ampm'] == 'a.m.' and int(d['to_hour']) == 12:
            d['to_hour'] = 0
        
        # Timedelta only works on dates, but we only need times, but timedelta
        # only works on dates, so we just use today's date for the time calculation.
        t = datetime.today()
        d['from_time'] = datetime(year=t.year, month=t.month, day=t.day, hour=int(d['from_hour']), minute=d['from_minute']) + self.timedelta
        d['to_time'] = datetime(year=t.year, month=t.month, day=t.day, hour=int(d['to_hour']), minute=d['to_minute']) + self.timedelta

        return d


    def datetime_to_string(self, from_time, to_time):
        """ Convert the datetime objects into strings we can output, ala
            '12:35-1:35 a.m.' or '7 p.m.-12 a.m.'
            We need both the from_time and the to_time because we omit the
            "a.m./p.m." on time ranges that share a.m./p.m.'s.
            >>> tz = Timezoner()
            >>> t = datetime.today()
            >>> fr = datetime(year=t.year, month=t.month, day=t.day, hour=12)
            >>> to = fr + timedelta(hours=5)
            >>> tz.datetime_to_string(fr, to)
            '12 p.m.-5 p.m.'
            """
        # We have a custom ampm string. This is how we do the custom ampm.
        if from_time.hour < 12 and to_time.hour < 12:
            ampms = { 'from': '', 'to': ' a.m.' }
        if from_time.hour >= 12 and to_time.hour >= 12:
            ampms = { 'from': '', 'to': ' p.m.' }
        if from_time.hour < 12 and to_time.hour >= 12:
            ampms = { 'from': ' a.m.', 'to': ' p.m.' }
        if from_time.hour >= 12 and to_time.hour < 12:
            ampms = { 'from': ' p.m.', 'to': ' a.m.' }

        # If we have a midnight or a noon in the from we use the full string.
        # This is so replace_midnights() needs the full string to work.
        # We only need this on the from time because the to time always has ampm.
        if from_time.hour in [0, 12] and from_time.minute == 0:
            ampms['from'] = ' p.m.'
            if from_time.hour == 0:
                ampms['from'] = ' a.m.'

        if from_time.minute == 0:
            from_time = '%s%s' % (from_time.strftime('%-I'), ampms['from'])
        else:
            from_time = '%s%s' % (from_time.strftime('%-I:%M'), ampms['from'])
        if to_time.minute == 0:
            to_time = '%s%s' % (to_time.strftime('%-I'), ampms['to'])
        else:
            to_time = '%s%s' % (to_time.strftime('%-I:%M'), ampms['to'])
        dt = '%s-%s' % (from_time, to_time)
        return dt
        

    def clean_minute(self, m):
        """ Minute strings come in as None and as ":30" or ":35", this standardizes that.
            >>> tz = Timezoner()
            >>> tz.clean_minute(None)
            0
            >>> tz.clean_minute(":30")
            30
            """
        if m:
            m = int(m.lstrip(':'))
        else:
            m = 0
        return m

    def rewrite_text(self, text):
        """ Updates the text with the new times. Returns the text.
            """
        for item in self.times:
            text = text.replace(item['original'], item['converted'])

        print text

def main(args):
    """ This method fires when we run this from the command line, and it's an
        example of how you might run it if you include the script elsewhere.
        """
    tz = Timezoner()
    tz.timezone = -2
    tz.set_timedelta()
    tz.text = tz.replace_midnights(" Gold Medal Final, 7 p.m.-Midnight. Women's Gymnastics - Team Competition, 12:35-1:35 a.m.")
    changes = 1
    while changes > 0:
        changes = tz.extract_parts()
        tz.rewrite_text(tz.text)
        


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
