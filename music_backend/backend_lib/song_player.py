from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time

class SongPlayer:

    def __init__(self, soundcloud_key, headless=True):
        options = Options()
        options.headless = headless
        self.browser = webdriver.Firefox(options=options)
        self.browserGoHome()
        self.soundcloud_key = soundcloud_key

    def browserGoHome(self):
        self.browserGoTo('http://google.com')

    def browserGoTo(self, url):
        self.browser.get(url)

    def playSong(self, global_obj, song):
        if(song.platform == 'soundcloud'):
            self.playSongSoundcloud(global_obj, song)

    def playSongSoundcloud(self, global_obj, song):
        soundcloud_embed_url = song.fetchSoundcloudPlayerURL(self.soundcloud_key)
        self.browserGoTo(soundcloud_embed_url)

        def isLoaded():
            return len(self.browser.find_elements_by_class_name('playButton')) > 0

        while(not isLoaded()):
            time.sleep(1)

        lastPlaying = True

        playButton = self.browser.find_elements_by_class_name('playButton')[0]
        def getButtonTitle():
            return playButton.get_property('title')
        def isSongOver():
            return (getButtonTitle() == 'Play' and global_obj['playing'] and lastPlaying) or global_obj['skip_flag']
        def checkAndDismissTeaser():
            teaserObjs = self.browser.find_elements_by_class_name('teaser__dismiss')
            if(len(teaserObjs) == 0):
                return
            teaserObj = teaserObjs[0]
            teaserObj.click()
            time.sleep(1)

        playButton.click()
        time.sleep(1)

        while not isSongOver():
            # if user paused song, but we haven't paused yet - pause
            if not global_obj['playing'] and getButtonTitle() != 'Play':
                playButton.click()
            # if user resumed song, but we haven't resumed yet - resume
            elif getButtonTitle() == 'Play' and global_obj['playing']:
                # check if teaser popup exists & get rid of
                checkAndDismissTeaser()
                # resume song
                playButton.click()
            
            lastPlaying = global_obj['playing']
            time.sleep(1)

        global_obj['skip_flag'] = False
        self.browserGoHome()