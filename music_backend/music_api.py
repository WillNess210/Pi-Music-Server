import time
from flask import Flask, jsonify
from multiprocessing import Process, Manager
import requests
import xml.etree.ElementTree as ET 
from selenium import webdriver
import os


app = Flask(__name__)

SOUNDCLOUD_ID = client_id=os.environ.get("SOUNDCLOUD_ID")

@app.route('/songs', methods=['GET'])
def get_songs():
   global song_pass
   return jsonify({'songs': list(song_pass)})

@app.route('/add_song/url=<path:name>', methods = ['GET'])
def add_song(name):
    global song_pass
    print(f"Adding {name}")
    song_pass.append(name)
    return jsonify({'success': True})


def getPlayerURL(track_url):
    client_id = SOUNDCLOUD_ID
    url_to_query = f"https://soundcloud.com/oembed?url={track_url}&client_id={client_id}"
    resp = ET.fromstring(requests.get(url_to_query).content)
    return resp.find('html').text.split("src=\"")[1].split("\"><")[0]

def playSong(track_url):
    player_url = getPlayerURL(track_url)
    browser = webdriver.Firefox()
    browser.get(player_url)
    
    def isLoaded():
        return len(browser.find_elements_by_class_name('playButton')) > 0
                
    # ensure browser has loaded before clicking
    while(not isLoaded()):
        time.sleep(1)
        
    playButton = browser.find_elements_by_class_name('playButton')[0]
    def isSongOver():
        return playButton.get_property('title') == 'Play'
    
    # clicking
    playButton.click()
    time.sleep(1)
    
    while not isSongOver():
        time.sleep(1)
    
    browser.quit()

def record_loop(songs):
    time.sleep(3)
    current_song = None
    while True:
        print(f"Current songs: {songs}")
        if current_song == None and len(songs) > 0:
           current_song = songs[0]
           songs.pop(0)
           print(f"Starting to play {current_song}")
           playSong(current_song)
           current_song = None
        time.sleep(1)


if __name__ == "__main__":
    with Manager() as manager:
        song_pass = manager.list([])
        p = Process(target=record_loop, args=(song_pass,))
        p.start()  
        app.run(debug=True, use_reloader=False)
        p.join()