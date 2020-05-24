import spotipy
from selenium.webdriver.common.keys import Keys
from . global_state import GlobalState
from . browser_control import Browser
import os

class SpotifyPlayer(Browser):

    def __init__(self, device_name, headless=True):
        super().__init__(headless=headless, landing_page='about:preferences')
        self.device_name = device_name
        self.clickOnElement(None, css='#playDRMContent')
        self.clickOnElement(None, css='#autoplaySettingsButton')
        
        self.sendKeyToBrowser(Keys.UP, post_sleep=1)
        for _ in range(4):
            self.sendKeyToBrowser(Keys.TAB, post_sleep=1)
        self.sendKeyToBrowser(Keys.ENTER)


    def loadSpotifyDevice(self, global_state):
        file_url = f'file://{os.getcwd()}/music_backend/backend_lib/spotify_player.html?device-name={self.device_name.replace(" ", "%20")}&token={global_state.getSpotifyKey()}'
        print(f'FILE_URL: {file_url}')
        self.goToURL(file_url)