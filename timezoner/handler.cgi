#!/usr/bin/env python
import cgi
import cgitb
from timezoner import Timezoner
cgitb.enable()

if __name__ == '__main__':
    form = cgi.FieldStorage()
    content = form.getvalue('content')
    print content, form
