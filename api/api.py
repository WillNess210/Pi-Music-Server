import time
import atexit
import threading
from flask import Flask
import pygame

app = Flask(__name__)

REFRESH_TIME = 5

dataLock = threading.lock()

yourThread = threading.Thread()

def func_to_repeat():
    global yourThread
    print("Eyy")
    yourThread = threading.Timer(REFRESH_TIME, func_to_repeat)
    yourThread.start()

def interrupt():
    global yourThread
    yourThread.cancel()

yourThread = threading.Timer(REFRESH_TIME, func_to_repeat)
yourThread.start()

atexit.register(interrupt)

@app.route('/time')
def get_current_time():
    return {'time' : time.time()}


@app.route("/wav")
def streamwav():
    pygame.mixer.init()
    pygame.mixer.music.load('../public/startup-sound.wav')
    pygame.mixer.music.play()
    return {'success': True};


def createMusicObject(platform, song_id):
    return {
            "platform": platform,
            "song_id": song_id
            }

song_queue = []

@app.route("/addSongToQueue/<platform>/<song_id>")
def addSongToQueue(platform, song_id):
    song_queue.append(createMusicObject(platform, song_id))