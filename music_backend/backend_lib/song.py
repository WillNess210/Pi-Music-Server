import requests
import xml.etree.ElementTree as ET 


class Song:
    def __init__(self, platform, url):
        self.platform = platform
        self.url = url

    def fetchSoundcloudPlayerURL(self, client_id):
        url_to_query = f"https://soundcloud.com/oembed?url={self.url}&client_id={client_id}"
        resp = ET.fromstring(requests.get(url_to_query).content)
        return resp.find('html').text.split("src=\"")[1].split("\"><")[0]