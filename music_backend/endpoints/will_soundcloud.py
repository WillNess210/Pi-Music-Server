from flask import Flask, Blueprint, render_template, url_for, jsonify
import soundcloud
import json
import requests
import random
import os


from ..backend_lib import Song

will_songs = []


def createWillSoundcloudBluePrint():
    will_soundcloud = Blueprint('will_soundcloud', __name__)

    loadWillsSongs()

    @will_soundcloud.route('/will_likes')
    def get_will_likes():
        global will_songs
        return jsonify({'songs': [s.dictRep() for s in will_songs]})

    return will_soundcloud

def loadWillsSongs():
    global will_songs

    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "", "res/wills_likes.json")
    will_likes = json.load(open(json_url))

    for song in will_likes:
        will_songs.append(
            Song(
                platform=song['platform'],
                url=song['url'],
                title=song['title'],
                artist=song['artist'],
                artwork_url=song['artwork_url'],
            )
        )


def getRandomLikedSong():
    global will_songs
    if len(will_songs) == 0:
        return None
    return random.choice(will_songs)