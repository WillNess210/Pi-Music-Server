import time
from flask_apscheduler import APScheduler
from flask import Flask
import pygame
import webbrowser
import json
import os
import spotipy
import soundcloud
import vlc
from dotenv import load_dotenv
load_dotenv('.env')

REFRESH_SECONDS = 1
SPOTIFY_TOKEN = os.environ.get("SPOTIFY_TOKEN")
SPOTIFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.environ.get("SPOTIFY_REDIRECT_URI")
SPOTIFY_USERNAME = os.environ.get("SPOTIFY_USERNAME")

SOUNDCLOUD_ID = client_id=os.environ.get("SOUNDCLOUD_ID")
client = soundcloud.Client(client_id=SOUNDCLOUD_ID)

def createMusicObject(platform, song_id):
    return {
            "platform": platform,
            "song_id": song_id
            }

song_queue = [
    createMusicObject("file", "../public/startup-sound.mp3"),
    #createMusicObject("spotify", "spotify:track:5f9JYuHSIHjp6rggue13RS")
    #createMusicObject("soundcloud", "786101896"),
    #createMusicObject("file", "../public/startup-sound.mp3")
]

def play_file(file_name):
    pygame.mixer.init()
    pygame.mixer.music.load(file_name)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy(): 
        pygame.time.Clock().tick(10)

def play_spotify(song_id):
    token = spotipy.SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET).get_access_token()
    print(f"Got token {token}")
    url = 'file://' + os.getcwd()[:-3] + f'public/spotify_play.html#{str(token)}~{str(song_id)}'
    print(url)
    webbrowser.open(url,new=1)

def play_soundcloud(song_id):
    # http://api.soundcloud.com/tracks/786101896/stream?client_id=1ad494d1e037642fbff22d251cbc202f
    track = client.get(f'/tracks/{song_id}/')
    stream_url = client.get(track.stream_url, allow_redirects=False).location
    print(stream_url)
    p = vlc.MediaPlayer(stream_url)
    p.play()
    while not p.is_playing():
        t=0
    print(f"STARTED PLAYING : {p.is_playing()}")
    while p.is_playing():
        t=0


song_platform_handlers = {
    "file": play_file,
    "spotify": play_spotify,
    "soundcloud": play_soundcloud
}

addSong = lambda s : song_queue.append(s)

def playSong():
    if len(song_queue) == 0:
        return
    next_song = song_queue.pop(0)
    print(f"Playing song {next_song['song_id']} from {next_song['platform']}")
    song_platform_handlers[next_song['platform']](next_song['song_id'])

class Config(object):
    JOBS = [
        {
            'id': 'job1',
            'func': playSong,
            'args': (),
            'trigger': 'interval',
            'seconds': REFRESH_SECONDS
        }
    ]

    SCHEDULER_API_ENABLED = True



app = Flask(__name__)
app.config.from_object(Config())

scheduler = APScheduler()

scheduler.init_app(app)

scheduler.start()

@app.route('/time')
def get_current_time():
    return {'time' : time.time()}

@app.route("/addSongToQueue")
def addSongToQueue():
    addSong(createMusicObject('file', "../public/startup-sound.mp3"))
    return {'success': True}

@app.route("/addSoundCloudTrack/<song_id>")
def addSoundcloudToQueue(song_id):
    song_queue.append(createMusicObject("soundcloud", song_id))
    return {'success': True}

if __name__ == '__main__':
    app.run()


