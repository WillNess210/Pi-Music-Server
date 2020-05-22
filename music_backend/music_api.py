import time
from flask import Flask, jsonify
from multiprocessing import Process, Manager, Value

from .backend_lib import Song, SongPlayer, SongSearcher, generateSoundcloudSongObject
from .backend_lib import getInitDictionary, GlobalState, getSoundcloudKey, get_env_val

from .endpoints.will_soundcloud import createWillSoundcloudBluePrint, getRandomLikedSong

SOUNDCLOUD_KEY = getSoundcloudKey()
HOST_VAL = get_env_val('HOST')
print(f'Attempting to start on {HOST_VAL}')

app = Flask(__name__)
app.register_blueprint(createWillSoundcloudBluePrint())

song_player = SongPlayer(SOUNDCLOUD_KEY, headless=True)
song_searcher = SongSearcher()

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
    return jsonify(result if result != None else {'rep': rep, 'updates': False,})

@app.route('/add_song/url=<path:track_url>', methods = ['GET'])
def add_song(track_url):
    global global_state_obj
    GlobalState(global_state_obj).addSong(generateSoundcloudSongObject(SOUNDCLOUD_KEY, track_url))
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

def record_loop(global_state_obj):
    global song_player
    global_state = GlobalState(global_state_obj)
    time.sleep(2)
    while True:
        songs = global_state.getSongs()
        print(f"Song queue len: {len(songs)}")
        if len(songs) == 0 and global_state.isAutoPlayOn():
            global_state.addSong(getRandomLikedSong())
        if len(songs) > 0:
            current_song = global_state.selectNextSong()
            print(f"Starting to play {current_song.title}")            
            song_player.playSong(global_state, current_song)
        time.sleep(1)

if __name__ == "__main__":
    with Manager() as manager:
        global_state_obj = manager.dict(getInitDictionary(manager))

        p = Process(target=record_loop, args=(global_state_obj,))
        p.start()  
        app.run(debug=True, use_reloader=False, host=HOST_VAL)
        p.join()
