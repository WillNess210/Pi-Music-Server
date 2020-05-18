class GlobalState:
    def __init__(self, global_state_obj):
        self.global_state = global_state_obj

    def hasCurrentSong(self):
        return not (self.global_state['current_song'][0] == None)

    def getCurrentSong(self):
        return self.global_state['current_song'][0]

    def getSongs(self):
        return list(self.global_state['songs'])

    # /songs
    def getSongsEndpointRep(self):
        hasCurrentSong = self.hasCurrentSong()
        new_obj = {}
        new_obj['current_song'] = None if not hasCurrentSong else self.getCurrentSong().dictRep()
        if hasCurrentSong:
            new_obj['current_song']['playing'] = self.global_state['playing']
        new_obj['songs'] = list(s.dictRep() for s in self.getSongs())
        new_obj['rep'] = ('1' if hasCurrentSong else '0') + ('1' if self.global_state['playing'] else '0')
        for song in new_obj['songs']:
            new_obj['rep'] += str(len(song['url']))
        new_obj['rep'] = int(new_obj['rep'])
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

def getInitDictionary(manager):
    return {
        'current_song': manager.list([None]),
        'songs': manager.list([]),
        'skip_flag': False,
        'playing': False,
    }