import time
from flask import Flask, jsonify
from multiprocessing import Process, Manager, Value
import requests
import xml.etree.ElementTree as ET 
import os
import soundcloud
import json

from backend_lib import Song, SongPlayer, generateSoundcloudSongObject
from backend_lib import getInitDictionary, GlobalState

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

SOUNDCLOUD_ID = os.getenv("SOUNDCLOUD_ID")
global_id_count = 0
will_songs = []

song_player = SongPlayer(SOUNDCLOUD_ID)

@app.route('/songs', methods=['GET'])
def get_songs():
    global global_state_obj
    global_state = GlobalState(global_state_obj)
    return jsonify(global_state.getSongsEndpointRep())

@app.route('/add_song/url=<path:track_url>', methods = ['GET'])
def add_song(track_url):
    global global_state_obj
    GlobalState(global_state_obj).addSong(generateSoundcloudSongObject(SOUNDCLOUD_ID, track_url))
    return jsonify({'success': True})

@app.route('/remove_song/<track_key>', methods = ['GET'])
def remove_song(track_key):
    global global_state_obj
    success = GlobalState(global_state_obj).removeSong(track_key)
    return jsonify({'success': success})

@app.route('/skip_song', methods = ['GET'])
def skip_song():
    global global_state_obj
    success = GlobalState(global_state_obj).submitSkip()
    return jsonify({'success': success})

@app.route('/pause_play', methods = ['GET'])
def toggle_pause_play():
    global global_state_obj
    success = GlobalState(global_state_obj).togglePlaying()
    return jsonify({'success': success})

@app.route('/will_likes', methods = ['GET'])
def return_will_likes():
    global will_songs
    return {'songs': [s.dictRep() for s in will_songs]}

def record_loop(global_state_obj):
    global song_player

    def currentSong():
        return global_state_obj['current_song'][0]
    def setCurrentSong(new_song):
        global_state_obj['current_song'][0] = new_song
    def clearCurrentSong():
        setCurrentSong(None)

    time.sleep(3)
    while True:
        songs = global_state_obj['songs']

        print(f"Song queue len: {len(songs)}")
        if currentSong() == None and len(songs) > 0:
            setCurrentSong(songs[0])
            songs.pop(0)
            
            print(f"Starting to play {currentSong()}")
            global_state_obj["playing"] = True
            song_player.playSong(global_state_obj, currentSong())

            clearCurrentSong()
            global_state_obj["playing"] = False

        time.sleep(1)

def loadWillsSongs():
    global will_songs
    page_size = 200

    client = soundcloud.Client(client_id=SOUNDCLOUD_ID)
    response = client.get('/users/79333503/favorites', limit=page_size, linked_partitioning=1).__dict__['obj']
    
    while True:
        for song in response['collection']:
            will_songs.append(Song(
                platform='soundcloud',
                url=song["permalink_url"],
                title=song["title"],
                artist=song["user"]["username"],
                artwork_url=song["artwork_url"],
            ))
        if('next_href' not in response):
            break
        response = json.loads(requests.get(response['next_href']).content)
    print(f"Finished adding wills liked songs, {len(will_songs)} total.")

if __name__ == "__main__":
    loadWillsSongs()
    with Manager() as manager:
        global_state_obj = manager.dict(getInitDictionary(manager))

        p = Process(target=record_loop, args=(global_state_obj,))
        p.start()  
        app.run(debug=True, use_reloader=False)
        p.join()