import requests
import xml.etree.ElementTree as ET 
import soundcloud

song_id_counter = 0

class Song:
    def __init__(self, platform, url, title, artist, artwork_url):
        # setting song key
        global song_id_counter
        self.key = song_id_counter
        song_id_counter += 1
        # loading in rest of parameters
        self.platform = platform
        self.url = url
        self.title = title
        self.artist = artist
        self.artwork_url = artwork_url
        self.playing = False

    def fetchSoundcloudPlayerURL(self, client_id):
        url_to_query = f"https://soundcloud.com/oembed?url={self.url}&client_id={client_id}"
        resp = ET.fromstring(requests.get(url_to_query).content)
        return resp.find('html').text.split("src=\"")[1].split("\"><")[0]

    def dictRep(self):
        return self.__dict__

def generateSoundcloudSongObject(soundcloud_key, track_url):
    client = soundcloud.Client(client_id=soundcloud_key)
    track = client.get('/resolve', url=track_url)
    return Song('soundcloud', track_url, track.title, track.user['username'], track.artwork_url)