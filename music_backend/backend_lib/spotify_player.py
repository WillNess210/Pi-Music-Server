import spotipy
from selenium.webdriver.common.keys import Keys
import os
import time

from . browser_control import Browser
from . song import Song


class SpotifyPlayer(Browser):

    def __init__(self, device_name, headless=True):
        super().__init__(headless=headless, landing_page='about:preferences')
        self.device_name = device_name
        self.clickOnElement(None, css='#playDRMContent')
        self.clickOnElement(None, css='#autoplaySettingsButton')
        self.cached_songs = None

        self.sendKeyToBrowser(Keys.UP, post_sleep=0.3)
        for _ in range(4):
            self.sendKeyToBrowser(Keys.TAB, post_sleep=0.3)
        self.sendKeyToBrowser(Keys.ENTER)


    def loadKey(self, key):
        self.key = key
        self.sp = spotipy.Spotify(auth=key)
        print("!!! LOADED SP ---")

    def loadSpotifyDevice(self, key):
        self.loadKey(key)
        file_url = f'file://{os.getcwd()}/music_backend/backend_lib/spotify_player.html?device-name={self.device_name.replace(" ", "%20")}&token={self.key}'
        print(f'FILE_URL: {file_url}')
        self.goToURL(file_url)
        pi_device = None
        for _ in range(10):
            time.sleep(1)
            devices = self.sp.devices()['devices']
            for device in devices:
                if device['name'] == self.device_name:
                    pi_device = device['id']
            if pi_device != None:
                print('Switched to new device for spotify!')
                break

        self.sp.transfer_playback(pi_device, force_play=False)

    def startPlayingSong(self, global_state, song):
        print(f"playing from spotify: |{song.url}|")
        global_state.songStarted()
        sp = spotipy.Spotify(auth=global_state.getSpotifyKey())
        sp.start_playback(uris=[song.url])
        playing = True
        while True:
            changedThisTurn = False
            if not global_state.isPlaying() and playing:
                sp.pause_playback()
                playing = False
                changedThisTurn = True
            elif global_state.isPlaying() and not playing:
                sp.start_playback()
                playing = True
                changedThisTurn = True
            if global_state.shouldSkip():
                sp.pause_playback()
                break
            if not changedThisTurn:
                playing_track = sp.current_user_playing_track()
                if playing and not playing_track['is_playing']:
                    sp.pause_playback()
                    break
            time.sleep(1)
        global_state.songFinished()

    def getSongObjectFromSpotifyUri(self, global_state, song_uri):
        sp = spotipy.Spotify(auth=global_state.getSpotifyKey())
        song = sp.track(song_uri)
        return Song(
                    platform='spotify',
                    url=song['uri'],
                    title=song['name'],
                    artist=song['artists'][0]['name'],
                    artwork_url=song['album']['images'][0]['url'],
                )

    def getLikes(self, global_state):
        if self.cached_songs != None:
            return self.cached_songs
        sp = spotipy.Spotify(auth=global_state.getSpotifyKey())
        liked_tracks = sp.current_user_saved_tracks(limit=5)['items']
        songs = []
        for song in liked_tracks:
            song = song['track']
            songs.append(
                Song(
                    platform='spotify',
                    url=song['uri'],
                    title=song['name'],
                    artist=song['artists'][0]['name'],
                    artwork_url=song['album']['images'][0]['url'],
                )
        )
        self.cached_songs = {'songs': [s.dictRep() for s in songs]}
        return self.cached_songs