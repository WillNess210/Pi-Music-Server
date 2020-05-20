from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time

class SongSearcher:
    
    def __init__(self, headless=True):
        options = Options()
        options.headless = headless
        self.browser = webdriver.Firefox(options=options)
        self.browser.get('https://google.com')



    def searchFor(self, search_term):

        def findFirstElementByClass(class_name):
            return self.browser.find_element_by_class_name(class_name)

        def findFirstElementByClassWithTextValue(class_name, val):
            els = self.browser.find_elements_by_class_name(class_name)
            for el in els:
                if el.text == val:
                    return el
        
        def waitUntilLoadClass(class_name):
            breakCount = 50
            while breakCount >= 0 and findFirstElementByClass(class_name) == None:
                time.sleep(0.1)
                breakCount -= 1

        self.browser.get('https://soundcloud.com/search')
        waitUntilLoadClass('headerSearch__input')
        search_box = findFirstElementByClass('headerSearch__input')
        search_box.send_keys('Aries')
