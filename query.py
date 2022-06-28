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
import requests
import json



def main(args):
    def quote(arg):
        if ' ' in arg:
            arg = '"%s"' % arg
        return urllib.parse.quote_plus(arg)

    qstring = '+'.join(quote(arg) for arg in args)
    print("Search query: " + qstring)
    if qstring == "":
        qstring = "car"
        print("Using default query string: " + qstring)
       
    myapikey = 'b593f7edbd42fe8106a2bb85ad4f8f91'
    url = urllib.parse.urljoin('https://api.musixmatch.com/ws/1.1/track.search', '?q_lyrics=' + qstring + '&f_lyrics_language=en&apikey=' + myapikey)
    try:
#       Using urllib module. Not best for json parsing ###    
#        response = urllib.request.urlopen(url)
#        headers = str(response.info())
#        textData = str(response.read())
####    
        Response = requests.get(url)
        Response.raise_for_status
        jsonResponse = Response.json()
        strJsonResponse = str(jsonResponse)
#   Not Using urllib module ###    
#    except urllib.error.HTTPError as err:
#        print(err.code)

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')        
        
    for key, value in jsonResponse.items():
        print(jsonResponse["track_name"])
    
    with open('response.txt', 'w', encoding="utf-8") as f:
        f.write(strJsonResponse)

        
#   Not Using urllib module ###        
#        f.write(headers)
#        f.write(textData)
        

if __name__ == '__main__':
    main(sys.argv[1:])
