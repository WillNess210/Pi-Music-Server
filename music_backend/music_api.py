import time
from flask import Flask, jsonify
from multiprocessing import Process, Manager, Value
import requests
import xml.etree.ElementTree as ET 
import os
import soundcloud
import json

from backend_lib import SongPlayer
from backend_lib import Song

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

SOUNDCLOUD_ID = os.getenv("SOUNDCLOUD_ID")
global_id_count = 0
will_songs = []

song_player = SongPlayer(SOUNDCLOUD_ID)

@app.route('/songs', methods=['GET'])
def get_songs():
    global song_queue
    new_obj = {}
    new_obj['current_song'] = song_queue['current_song'][0]
    if new_obj['current_song'] != None:
        new_obj['current_song']['playing'] = song_queue['playing']
    new_obj['songs'] = list(song_queue['songs'])
    new_obj['rep'] = ('1' if new_obj['current_song'] != None else '0') + ('1' if song_queue['playing'] else '0')
    for song in new_obj['songs']:
        new_obj['rep'] += str(len(song['url']))
    new_obj['rep'] = int(new_obj['rep'])
    return jsonify(new_obj)

@app.route('/add_song/url=<path:track_url>', methods = ['GET'])
def add_song(track_url):
    global song_queue
    print(f"Adding {track_url}")
    song_queue['songs'].append(createSongObjectFromSoundcloud(track_url))
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

@app.route('/pause_play', methods = ['GET'])
def toggle_pause_play():
    global song_queue
    if song_queue['current_song'][0] != None:
        song_queue['playing'] = not song_queue['playing']
    return jsonify({'success': song_queue['current_song'][0] != None})

@app.route('/will_likes', methods = ['GET'])
def return_will_likes():
    global will_songs
    return {'songs': will_songs}

def getPlayerURL(track_url):
    url_to_query = f"https://soundcloud.com/oembed?url={track_url}&client_id={SOUNDCLOUD_ID}"
    resp = ET.fromstring(requests.get(url_to_query).content)
    return resp.find('html').text.split("src=\"")[1].split("\"><")[0]

def record_loop(song_queue):
    global song_player

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
            song_queue["playing"] = True
            cur_song = currentSong()
            new_song_obj = Song('soundcloud', cur_song['url'])
            song_player.playSong(song_queue, new_song_obj)

            clearCurrentSong()
            song_queue["playing"] = False

        time.sleep(1)

def createSongObject(url, title, artist, artwork_url):
    global global_id_count
    to_ret = {
        'url': url,
        'key': global_id_count,
        'title': title,
        'artist': artist,
        'artwork_url': artwork_url,
    }
    global_id_count += 1
    return to_ret

def createSongObjectFromSoundcloud(soundcloud_url):
    client = soundcloud.Client(client_id=SOUNDCLOUD_ID)
    track = client.get('/resolve', url=soundcloud_url)
    return createSongObject(soundcloud_url, track.title, track.user['username'], track.artwork_url)

def loadWillsSongs():
    global will_songs
    page_size = 200

    client = soundcloud.Client(client_id=SOUNDCLOUD_ID)
    response = client.get('/users/79333503/favorites', limit=page_size, linked_partitioning=1).__dict__['obj']
    
    while True:
        for song in response['collection']:
            will_songs.append(createSongObject(
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
        song_queue = manager.dict({
            'current_song': manager.list([None]),
            'songs': manager.list([]),
            'skip_flag': False,
            'playing': False,
        })

        p = Process(target=record_loop, args=(song_queue,))
        p.start()  
        app.run(debug=True, use_reloader=False)
        p.join()