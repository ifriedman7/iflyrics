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
import csv
import json



def main(args):
    def quote(arg):
        if ' ' in arg:
            arg = '"%s"' % arg
        return urllib.parse.quote_plus(arg)

    if os.path.isfile('tracks.csv'):
        os.remove('tracks.csv')

    qstring = '+'.join(quote(arg) for arg in args)
    print("Search query: " + qstring)
    if qstring == "":
        qstring = "car"
        print("Using default query string: " + qstring)
       
    myapikey = 'b593f7edbd42fe8106a2bb85ad4f8f91'
    url = urllib.parse.urljoin('https://api.musixmatch.com/ws/1.1/track.search', '?q_lyrics=' + qstring + '&f_lyrics_language=en&apikey=' + myapikey)
    try:
        response = urllib.request.urlopen(url)
        resHeaders = response.info()
        resBody = response.read()
        jsonResponse = json.loads(resBody.decode("utf-8"))
        strJsonResponse = str(jsonResponse)

    except urllib.error.HTTPError as err:
        print(err.code)

  
    track_list = jsonResponse['message']['body']['track_list']
    n = 0
    for track in track_list:
        track = track_list[n]['track']
        if "album_id" in track:
            v_album_id = track_list[n]['track']['album_id']
            v_track_name = track_list[n]['track']['track_name'] 
            v_album_name = track_list[n]['track']['album_name']
            v_artist_name = track_list[n]['track']['artist_name']
            v_share_url = track_list[n]['track']['track_share_url']
#            print('"' + v_track_name + '","' + v_artist_name + '","' + v_album_name + '","' + v_share_url + '"')
            with open('tracks.csv', 'a', encoding="utf-8") as f:
                write = csv.writer(f)
                write.writerows(v_track_name, v_artist_name, v_album_name, v_share_url)
        n=n+1
        
    
    with open('response.txt', 'w', encoding="utf-8") as f:
        f.write(strJsonResponse)
        


              

if __name__ == '__main__':
    main(sys.argv[1:])
