import time
from flask import Flask, jsonify
from multiprocessing import Process, Manager, Value
import requests
import xml.etree.ElementTree as ET 
from selenium import webdriver
from ctypes import c_char_p
import os


app = Flask(__name__)

SOUNDCLOUD_ID = client_id=os.environ.get("SOUNDCLOUD_ID")

@app.route('/songs', methods=['GET'])
def get_songs():
   global song_queue
   new_obj = {}
   new_obj['current_song'] = song_queue['current_song'][0]
   new_obj['songs'] = list(song_queue['songs'])
   return jsonify(new_obj)

@app.route('/add_song/url=<path:name>', methods = ['GET'])
def add_song(name):
    global song_queue
    print(f"Adding {name}")
    song_queue['songs'].append(name)
    print(song_queue['songs'])
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

def record_loop(song_queue):
    def currentSong():
        return song_queue['current_song'][0]
    def setCurrentSong(new_song):
        song_queue['current_song'][0] = new_song
    def clearCurrentSong():
        setCurrentSong(None)

    time.sleep(3)
    while True:
        songs = song_queue['songs']

        print(f"Song queue len: {len(songs)}")
        if currentSong() == None and len(songs) > 0:
            setCurrentSong(songs[0])
            songs.pop(0)
            
            print(f"Starting to play {currentSong()}")
            playSong(currentSong())

            clearCurrentSong()

        time.sleep(1)


if __name__ == "__main__":
    with Manager() as manager:
        song_queue = manager.dict()

        song_queue['current_song'] = manager.list([None])
        song_queue['songs'] = manager.list([])

        p = Process(target=record_loop, args=(song_queue,))
        p.start()  
        app.run(debug=True, use_reloader=False)
        p.join()