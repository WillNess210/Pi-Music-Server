import spotipy
from selenium.webdriver.common.keys import Keys
import os

from . global_state import GlobalState
from . browser_control import Browser
from . song import Song


class SpotifyPlayer(Browser):

    def __init__(self, device_name, headless=True):
        super().__init__(headless=headless, landing_page='about:preferences')
        self.device_name = device_name
        self.clickOnElement(None, css='#playDRMContent')
        self.clickOnElement(None, css='#autoplaySettingsButton')
        self.key = None
        self.sp = None

        self.sendKeyToBrowser(Keys.UP, post_sleep=1)
        for _ in range(4):
            self.sendKeyToBrowser(Keys.TAB, post_sleep=1)
        self.sendKeyToBrowser(Keys.ENTER)


    def loadKey(self, key):
        self.key = key
        self.sp = spotipy.Spotify(auth=key)

    def loadSpotifyDevice(self, global_state):
        self.loadKey(global_state.getSpotifyKey())
        file_url = f'file://{os.getcwd()}/music_backend/backend_lib/spotify_player.html?device-name={self.device_name.replace(" ", "%20")}&token={self.key}'
        print(f'FILE_URL: {file_url}')
        self.goToURL(file_url)

    def getLikes(self):
        liked_tracks = self.sp.current_user_saved_tracks(limit=5)['items']
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
        return {'songs': [s.dictRep() for s in songs]}