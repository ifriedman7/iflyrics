from flask import Flask, request, render_template

"""    With Flask as webapp
"""


import sys
import os
import datetime
import time
import urllib.parse
import urllib.request
import urllib.error
import json


# Initialize Flask app with the template folder address
app = Flask(__name__, template_folder='templates')

@app.route('/')
def app_route():
    return render_template('index.html')

@app.route('/my_query/', methods=['POST'])
def my_query():
    args = request.form["query_text"]
    def quote(arg):
        if ' ' in arg:
            arg = '"%s"' % arg
        return urllib.parse.quote_plus(arg)

    if os.path.isfile('tracks.csv'):
        os.remove('tracks.csv')

#    qstring = '+'.join(quote(arg) for arg in args)
    qstring = urllib.parse.quote_plus(args)

    print("Search query: " + qstring)
    if qstring == "":
        qstring = "car"
        print("Using default query string: " + qstring)
       
    myapikey = 'b593f7edbd42fe8106a2bb85ad4f8f91'
    start_date = time.strptime("2010-01-01", "%Y-%m-%d")
    
    url = urllib.parse.urljoin('https://api.musixmatch.com/ws/1.1/track.search', '?q_lyrics=' + qstring + '&f_lyrics_language=en&apikey=' + myapikey)
    try:
        response = urllib.request.urlopen(url)
        
    except urllib.error.HTTPError as err:
        print(err.code)

   
    resHeaders = response.info()
    resBody = response.read()
    jsonResponse = json.loads(resBody.decode("utf-8"))
    strJsonResponse = str(jsonResponse)


    track_list = jsonResponse['message']['body']['track_list']
    n = 0
    for track in track_list:
        track = track_list[n]['track']
        #check if song has album
        if "album_id" in track:         
            v_album_id = track_list[n]['track']['album_id']
            
            #check album release date
            album_get_url = urllib.parse.urljoin('https://api.musixmatch.com/ws/1.1/album.get', '?album_id=' + str(v_album_id) + '&apikey=' + myapikey)
            try:
                albumResponse = urllib.request.urlopen(album_get_url)       
            except urllib.error.HTTPError as err:
                print(err.code)  
            albumJson = json.loads(albumResponse.read().decode("utf-8"))
            albumDateStr = albumJson['message']['body']['album']['album_release_date']
            try:
                albumDateTime = time.strptime(albumDateStr, "%Y-%m-%d")
            except ValueError:
                try: 
                    albumDateTime = time.strptime(albumDateStr, "%Y-%m")
                except ValueError:
                    try:
                        albumDateTime = time.strptime(albumDateStr, "%Y")
                    except ValueError:
                        albumDateTime = time.strptime("1900", "%Y")
                    
            if albumDateTime < start_date:
                print(albumDateStr)
                v_track_name = track_list[n]['track']['track_name'] 
                v_album_name = track_list[n]['track']['album_name']
                v_artist_name = track_list[n]['track']['artist_name']
                v_share_url = track_list[n]['track']['track_share_url']
                row = str('"' + v_track_name + '","' + v_artist_name + '","' + v_album_name + '","' + v_share_url + '"')
                with open('tracks.csv', 'a', encoding="utf-8") as f:
                    f.write(row + "\n")
        n=n+1
        
    
    with open('response.txt', 'w', encoding="utf-8") as f:
        f.write(qstring + "\n")
        f.write(strJsonResponse)
       
    return render_template('display.html')
# Listen on external IPs
# Listen to port 3001 so you can just run 'python app.py' to start the server
if __name__ == '__main__':
    # listen on external IPs
    app.run(host='0.0.0.0', port=3001, debug=True)
