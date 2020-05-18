from backend_lib import Song, SongPlayer, generateSoundcloudSongObject

import os
from dotenv import load_dotenv
load_dotenv()



SOUNDCLOUD_ID = os.getenv("SOUNDCLOUD_ID")


song = generateSoundcloudSongObject(SOUNDCLOUD_ID, 'https://soundcloud.com/lijofficial/ramen-cups')

print(song.__dict__)