import time
from flask import Flask, jsonify
from multiprocessing import Process, Manager, Value
import requests
import json

from .backend_lib import Song, SongPlayer, SongSearcher, SpotifyPlayer, generateSoundcloudSongObject, generateSpotifySongObject
from .backend_lib import getInitDictionary, GlobalState, getSoundcloudKey, get_env_val, get_spotify_creds

from .endpoints.will_soundcloud import createWillSoundcloudBluePrint, getRandomLikedSong

SOUNDCLOUD_KEY = getSoundcloudKey()
SPOTIFY_CREDS = get_spotify_creds()
HOST_VAL = get_env_val('HOST')
print(f'Attempting to start on {HOST_VAL}')

app = Flask(__name__)
app.register_blueprint(createWillSoundcloudBluePrint())

song_player = SongPlayer(SOUNDCLOUD_KEY, headless=True)
song_searcher = SongSearcher()
spotify_player = SpotifyPlayer(SPOTIFY_CREDS['DEVICE_NAME'], headless=True)


@app.route('/songs', methods=['GET'])
def get_songs():
    global global_state_obj
    global_state = GlobalState(global_state_obj)
    return jsonify(global_state.getSongsEndpointRep())

@app.route('/songs/<rep>', methods=['GET'])
def get_songs_repcheck(rep):
    global global_state_obj
    global_state = GlobalState(global_state_obj)
    result = global_state.getSongsEndpointRep(prev_rep=rep)
    return jsonify(result if result != None else {'rep': int(rep)})

@app.route('/add_song/url=<path:track_url>', methods = ['GET'])
def add_song(track_url):
    global global_state_obj
    global spotify_player
    global_state = GlobalState(global_state_obj)
    platform = 'soundcloud' if 'soundcloud' in track_url else 'spotify'
    global_state.addSong(
        generateSoundcloudSongObject(SOUNDCLOUD_KEY, track_url) if platform == 'soundcloud' else 
        generateSpotifySongObject(global_state, track_url, spotify_player)
    )
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

@app.route('/toggle_autoplay', methods = ['GET'])
def toggle_autoplay():
    global global_state_obj
    GlobalState(global_state_obj).toggleAutoPlay()
    return jsonify({'success': True})

@app.route('/search/<search_term>', methods = ['GET'])
def search_for(search_term):
    global song_searcher
    return jsonify({'songs': song_searcher.searchFor(search_term)})

@app.route('/send_spotify_key/<auth_code>', methods = ['GET'])
def receive_key(auth_code):
    global global_state_obj
    global spotify_player
    global_state = GlobalState(global_state_obj)
    # convert from auth code to access token
    access_token = json.loads(requests.post('https://accounts.spotify.com/api/token', data = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': SPOTIFY_CREDS['REDIRECT_URI'],
        'client_id': SPOTIFY_CREDS['SPOTIFY_CLIENT_ID'],
        'client_secret': SPOTIFY_CREDS['SPOTIFY_CLIENT_SECRET'],
    }).text)['access_token']
    global_state.setSpotifyKey(access_token)
    spotify_player.loadSpotifyDevice(global_state.getSpotifyKey())
    return jsonify({'success': True})

@app.route('/spotify_likes', methods = ['GET'])
def send_spotify_likes():
    global global_state_obj
    global spotify_player
    global_state = GlobalState(global_state_obj)
    return jsonify(spotify_player.getLikes(global_state))

def record_loop(global_state_obj):
    global song_player
    global spotify_player
    global_state = GlobalState(global_state_obj)
    time.sleep(2)
    while True:
        songs = global_state.getSongs()
        #print(f"Song queue len: {len(songs)}")
        if len(songs) == 0 and global_state.isAutoPlayOn():
            global_state.addSong(getRandomLikedSong())
        if len(songs) > 0:
            current_song = global_state.selectNextSong()
            print(f"Starting to play {current_song.title}") 
            if current_song.platform == 'soundcloud':           
                song_player.playSong(global_state, current_song)
            else:
                spotify_player.startPlayingSong(global_state, current_song)
        time.sleep(1)

if __name__ == "__main__":
    with Manager() as manager:
        global_state_obj = manager.dict(getInitDictionary(manager))
        p = Process(target=record_loop, args=(global_state_obj,))
        p.start()  
        app.run(debug=True, use_reloader=False, host=HOST_VAL)
        p.join()
