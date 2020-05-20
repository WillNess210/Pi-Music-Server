import os
from dotenv import load_dotenv
load_dotenv()
SOUNDCLOUD_ID = os.getenv("SOUNDCLOUD_ID")

def getSoundcloudKey():
    return SOUNDCLOUD_ID

def get_env_val(key):
    return os.getenv(key)