from flask import Blueprint
import soundcloud
import json
import requests
import random

from ..backend_lib import Song


will_songs = []


def createWillSoundcloudBluePrint(soundcloud_key):
    will_soundcloud = Blueprint('will_soundcloud', __name__)

    loadWillsSongs(soundcloud_key)

    @will_soundcloud.route('/will_likes')
    def get_will_likes():
        global will_songs
        return {'songs': [s.dictRep() for s in will_songs]}

    return will_soundcloud

def loadWillsSongs(soundcloud_key):
    global will_songs
    page_size = 200

    client = soundcloud.Client(client_id=soundcloud_key)
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


def getRandomLikedSong():
    global will_songs
    if len(will_songs) == 0:
        return None
    return random.choice(will_songs)