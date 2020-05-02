import time
from flask import Flask
from playsound import playsound

app = Flask(__name__)

@app.route('/time')
def get_current_time():
    return {'time' : time.time()}


@app.route("/wav")
def streamwav():
    playsound('../public/startup-sound.mp3')