import time
from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
from multiprocessing import Process, Manager, Value
import requests
import xml.etree.ElementTree as ET 
from selenium import webdriver
from ctypes import c_char_p
import os
import soundcloud

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'

cors = CORS(app, resources={r"/foo": {"origins": "http://localhost:5000"}})

SOUNDCLOUD_ID = os.getenv("SOUNDCLOUD_ID")
global_id_count = 0
browser = webdriver.Firefox()
browser.get('http://google.com')

@app.route('/songs', methods=['GET'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def get_songs():
    global song_queue
    new_obj = {}
    new_obj['current_song'] = song_queue['current_song'][0]
    new_obj['songs'] = list(song_queue['songs'])
    new_obj['rep'] = '1' if new_obj['current_song'] != None else '0'
    for song in new_obj['songs']:
        new_obj['rep'] += str(len(song['url']))
    new_obj['rep'] = int(new_obj['rep'])
    return jsonify(new_obj)

@app.route('/add_song/url=<path:track_url>', methods = ['GET'])
def add_song(track_url):
    global song_queue
    print(f"Adding {track_url}")
    song_queue['songs'].append(createSongObject(track_url))
    print(song_queue['songs'])
    return jsonify({'success': True})

@app.route('/remove_song/<track_key>', methods = ['GET'])
def remove_song(track_key):
    global song_queue
    for s in song_queue['songs']:
        if(int(s['key']) == int(track_key)):
            song_queue['songs'].remove(s)
            return jsonify({'success': True})
        else:
            print(f"{s['key']} != {track_key}")
    return jsonify({'success': False})

@app.route('/skip_song', methods = ['GET'])
def skip_song():
    global song_queue
    song_queue['skip_flag'] = True
    return jsonify({'success': song_queue['current_song'][0] != None})


def getPlayerURL(track_url):
    url_to_query = f"https://soundcloud.com/oembed?url={track_url}&client_id={SOUNDCLOUD_ID}"
    resp = ET.fromstring(requests.get(url_to_query).content)
    return resp.find('html').text.split("src=\"")[1].split("\"><")[0]

def playSong(track_url, song_queue):
    global browser
    player_url = getPlayerURL(track_url)
    
    browser.get(player_url)
    
    def isLoaded():
        return len(browser.find_elements_by_class_name('playButton')) > 0
                
    # ensure browser has loaded before clicking
    while(not isLoaded()):
        time.sleep(1)
        
    playButton = browser.find_elements_by_class_name('playButton')[0]
    def isSongOver():
        return playButton.get_property('title') == 'Play' or song_queue['skip_flag']
    
    # clicking
    playButton.click()
    time.sleep(1)
    
    while not isSongOver():
        time.sleep(1)

    song_queue['skip_flag'] = False

    browser.get('http://google.com')

def record_loop(song_queue):
    def currentSong():
        return song_queue['current_song'][0]
    def setCurrentSong(new_song):
        song_queue['current_song'][0] = new_song
    def clearCurrentSong():
        setCurrentSong(None)

    time.sleep(3)
    while True:
        songs = song_queue['songs']

        print(f"Song queue len: {len(songs)}")
        if currentSong() == None and len(songs) > 0:
            setCurrentSong(songs[0])
            songs.pop(0)
            
            print(f"Starting to play {currentSong()}")
            playSong(currentSong()['url'], song_queue)

            clearCurrentSong()

        time.sleep(1)


def createSongObject(soundcloud_url):
    global global_id_count
    to_ret = {
        'url': soundcloud_url,
        'key': global_id_count,
    }
    global_id_count += 1
    client = soundcloud.Client(client_id=SOUNDCLOUD_ID)
    track = client.get('/resolve', url=soundcloud_url)
    to_ret['title'] = track.title
    to_ret['artist'] = track.user['username']
    to_ret['artwork_url'] = track.artwork_url

    return to_ret

if __name__ == "__main__":
    with Manager() as manager:
        song_queue = manager.dict({
            'current_song': manager.list([None]),
            'songs': manager.list([]),
            'skip_flag': False,
        })

        p = Process(target=record_loop, args=(song_queue,))
        p.start()  
        app.run(debug=True, use_reloader=False)
        p.join()