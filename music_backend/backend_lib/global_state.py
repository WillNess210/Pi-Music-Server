class GlobalState:

    def __init__(self, global_state_obj):
        self.global_state = global_state_obj

    def hasCurrentSong(self):
        return not (self.global_state['current_song'][0] == None)

    def getCurrentSong(self):
        return self.global_state['current_song'][0]

    def getSongs(self):
        return list(self.global_state['songs'])

    def isAutoPlayOn(self):
        return self.global_state['auto_play'] 

    def toggleAutoPlay(self):
        self.global_state['auto_play'] = not self.global_state['auto_play']

    def selectNextSong(self):
        # removes first element in song list, sets it to current_song, and returns the song
        next_song = self.global_state['songs'].pop(0)
        self.global_state['current_song'][0] = next_song
        return next_song

    # skip handling

    def shouldSkip(self):
        return self.global_state['skip_flag']

    def submitSkip(self):
        if self.hasCurrentSong():
            self.global_state['skip_flag'] = True
            return True
        return False

    def songStarted(self):
        self.global_state['playing'] = True
    
    def songFinished(self):
        self.global_state['current_song'][0] = None
        self.global_state['skip_flag'] = False
        self.global_state['playing'] = False

    # play/pause handling

    def isPlaying(self):
        return self.global_state['playing']
        
    def togglePlaying(self):
        if not self.hasCurrentSong():
            return False
        self.global_state['playing'] = not self.global_state['playing']
        return True

    # /songs
    def getSongsEndpointRep(self, prev_rep = None):

        hasCurrentSong = self.hasCurrentSong()
        new_obj = {}
        new_obj['current_song'] = None if not hasCurrentSong else self.getCurrentSong().dictRep()
        if hasCurrentSong:
            new_obj['current_song']['playing'] = self.global_state['playing']
        new_obj['songs'] = list(s.dictRep() for s in self.getSongs())
        new_obj['rep'] = ('1' if hasCurrentSong else '0') + ('1' if self.global_state['playing'] else '0') + ('1' if self.isAutoPlayOn() else '0')
        new_obj['rep'] += {True: '1', False: '0'}[self.hasSpotifyKey()]
        for song in new_obj['songs']:
            new_obj['rep'] += str(len(song['url']))
        new_obj['rep'] = int(new_obj['rep'])
        if prev_rep and new_obj['rep'] == int(prev_rep):
            return None # no need to update client
        new_obj['auto_play'] = self.isAutoPlayOn()
        new_obj['updates'] = True
        new_obj['connected_to_spotify'] = self.hasSpotifyKey()
        return new_obj
    
    # /add_song
    def addSong(self, song):
        self.global_state['songs'].append(song)

    def removeSong(self, song_key):
        for i, s in enumerate(self.getSongs()):
            if(int(s.key) == int(song_key)):
                del self.global_state['songs'][i]
                return True
        return False

    def setSpotifyKey(self, spotify_key):
        self.global_state['spotify_key'] = spotify_key

    def getSpotifyKey(self):
        return self.global_state['spotify_key']

    def hasSpotifyKey(self):
        return len(self.global_state['spotify_key']) > 0

def getInitDictionary(manager):
    return {
        'current_song': manager.list([None]),
        'songs': manager.list([]),
        'skip_flag': False,
        'playing': False,
        'auto_play': False,
        'spotify_key': '',
    }