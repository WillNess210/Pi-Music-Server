import time
from . global_state import GlobalState
from . browser_control import Browser

class SongPlayer(Browser):

    def __init__(self, soundcloud_key, headless=True):
        super().__init__(headless=headless)
        self.soundcloud_key = soundcloud_key

    def playSong(self, global_state, song):
        global_state.songStarted()
        if(song.platform == 'soundcloud'):
            self.playSongSoundcloud(global_state, song)
        global_state.songFinished()

    def playSongSoundcloud(self, global_state, song):
        soundcloud_embed_url = song.fetchSoundcloudPlayerURL(self.soundcloud_key)
        self.goToURL(soundcloud_embed_url)
        
        playButton = self.returnElementByCSS('.playButton')
        lastPlaying = True # always initially playing

        def getButtonTitle():
            return playButton.get_property('title')
        def isSongOver():
            return (getButtonTitle() == 'Play' and global_state.isPlaying() and lastPlaying) or global_state.shouldSkip()
        def checkAndDismissTeaser():
            teaserObj = self.returnElementByCSS('teaser__dismiss', timeout_seconds=0)
            if teaserObj == None: return
            teaserObj.click()
            time.sleep(1)

        playButton.click()
        time.sleep(1)

        while not isSongOver():
            # if user paused song, but we haven't paused yet - pause
            if not global_state.isPlaying() and getButtonTitle() != 'Play':
                playButton.click()
            # if user resumed song, but we haven't resumed yet - resume
            elif getButtonTitle() == 'Play' and global_state.isPlaying():
                # check if teaser popup exists & get rid of
                checkAndDismissTeaser()
                # resume song
                playButton.click()
            
            lastPlaying = global_state.isPlaying()
            time.sleep(1)