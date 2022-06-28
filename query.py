#! /usr/bin/env python3

"""Script to search lyrics with musixmatch

Usage:
    python3 query.py [search terms]
"""

import sys
import os
import urllib.parse
import urllib.request
import urllib.error
import json
#import webbrowser


def main(args):
    def quote(arg):
        if ' ' in arg:
            arg = '"%s"' % arg
        return urllib.parse.quote_plus(arg)

    qstring = '+'.join(quote(arg) for arg in args)
    myapikey = 'b593f7edbd42fe8106a2bb85ad4f8f91'
    url = urllib.parse.urljoin('https://api.musixmatch.com/ws/1.1/track.search', '?q_lyrics=' + qstring + '&apikey=' + myapikey)
#    webbrowser.open(url)
    response = urllib.request.urlopen(url)
    headers = str(response.info())
    data = str(response.read())
    
    with open('response.txt', 'w', encoding="utf-8") as f:
        f.write(headers)
        f.write(data)
        

if __name__ == '__main__':
    main(sys.argv[1:])
