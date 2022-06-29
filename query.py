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

    qstring = '+'.join(quote(arg) for arg in args)
    print("Search query: " + qstring)
    if qstring == "":
        qstring = "car"
        print("Using default query string: " + qstring)
       
    myapikey = 'b593f7edbd42fe8106a2bb85ad4f8f91'
    url = urllib.parse.urljoin('https://api.musixmatch.com/ws/1.1/track.search', '?q_lyrics=' + qstring + '&f_lyrics_language=en&apikey=' + myapikey)
    try:
#       Using urllib module.    
        response = urllib.request.urlopen(url)
        resHeaders = response.info()
        resBody = response.read()
        jsonResponse = json.loads(resBody.decode("utf-8"))
        strJsonResponse = str(jsonResponse)

   
    except urllib.error.HTTPError as err:
        print(err.code)

     
  
    for k_message, v_message in jsonResponse.items():
        for k_body in v_message:
            v_body = v_message['body']
            for k_track_list in v_body:
                v_track_list = v_body['track_list']
                for k_track in v_track_list:
                   v_track = v_track_list['track']
                   print (v_track)
                    
#    for track in jsonResponse['message']['body']['track_list']['track']:
#        print (jsonResponse['message']['body']['track_list']['track']['track_name'])
        
#    for key, value in jsonResponse['message']['body']['track_list'].items():
#        print(key, ":", value)
                
#        print(jsonResponse.get("track_name"))
    
    with open('response.txt', 'w', encoding="utf-8") as f:
        f.write(strJsonResponse)
        
    with open('tracks.csv', 'w', encoding="utf-8") as f:
        write = csv.writer(f)
        write.writerows(v_track_list)

        
#   Not Using urllib module ###        
#        f.write(headers)
#        f.write(textData)
        

if __name__ == '__main__':
    main(sys.argv[1:])
