import time
from flask import Flask
import pygame

app = Flask(__name__)

@app.route('/time')
def get_current_time():
    return {'time' : time.time()}


@app.route("/wav")
def streamwav():
    pygame.mixer.init()
    pygame.mixer.music.load('../public/startup-sound.wav')
    pygame.mixer.music.play()
    return {'success': True};
