import os
from dotenv import load_dotenv
load_dotenv()
SOUNDCLOUD_ID = os.getenv("SOUNDCLOUD_ID")

def getSoundcloudKey():
    return SOUNDCLOUD_ID

def get_env_val(key):
    return os.getenv(key)

def get_spotify_creds():
    return {
        'SPOTIFY_CLIENT_ID': os.getenv('SPOTIFY_CLIENT_ID'),
        'SPOTIFY_CLIENT_SECRET': os.getenv('SPOTIFY_CLIENT_SECRET'),
        'REDIRECT_URI': os.getenv('REDIRECT_URI'),
        'DEVICE_NAME': os.getenv('DEVICE_NAME'),
    }