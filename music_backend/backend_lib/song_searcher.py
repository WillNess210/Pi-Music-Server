from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import random

class SongSearcher:
    
    def __init__(self, headless=True):
        options = Options()
        options.headless = headless
        self.browser = webdriver.Firefox(options=options)
        self.browser.get('https://soundcloud.com/search')
        self.searching = False

        def returnElementByCSS(css_selector, i=0):
            els = []
            timeout = 40
            while len(els) == 0 and timeout >= 0:
                els = self.browser.find_elements_by_css_selector(css_selector)
                timeout -= 1
                time.sleep(0.25)
            return print("Not Found") if len(els) == 0 else els[i]
        def clickOnElement(el, css=''):
            if el == None: 
                el = returnElementByCSS(css)
            time.sleep(1)
            el.click()
            return el
        clickOnElement(returnElementByCSS('.searchOptions__navigationLink', i=2))

    def searchFor(self, search_term):
        if self.searching == True:
            return {'success': False}
        self.searching = True
        search_term = str(search_term)
        print(f'Search Term: |{search_term}|')

        def returnElementsByCSS(css_selector):
            return self.browser.find_elements_by_css_selector(css_selector)

        def returnElementByCSS(css_selector, i=0):
            els = []
            timeout = 20
            while len(els) == 0 and timeout >= 20:
                els = self.browser.find_elements_by_css_selector(css_selector)
                timeout -= 1
                time.sleep(0.25)
            return print("Not Found") if len(els) == 0 else els[i]

        def typeInElement(el, msg, css=''):
            if el == None:
                el = returnElementByCSS(css)
            time.sleep(1)
            el.clear()
            time.sleep(1 + random.random() * 1)
            for key in msg:
                time.sleep(0.05 + random.random() * 0.1)
                el.send_keys(key)
            return el

        def clickOnElement(el, css=''):
            if el == None: 
                el = returnElementByCSS(css)
            time.sleep(1)
            el.click()
            return el

        typeInElement(None, search_term, '.headerSearch__input')
        clickOnElement(None, '.headerSearch__submit')
        time.sleep(2)
        self.browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(0.5)
        self.browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(1.5)

        obj_results = []
        search_items = returnElementsByCSS('.sound.searchItem__trackItem')
        for item in search_items:
            #artwork_url
            obj = item.find_element_by_css_selector('.sc-artwork.image__full')
            style = obj.get_attribute('style')
            if 'background-image' not in style:
                continue
            artwork_url = style.split('url("')[1][:-3]
            #title & url
            obj = item.find_element_by_css_selector('.soundTitle__title')
            title = obj.text
            url = obj.get_attribute('href')
            #artist
            obj = item.find_element_by_css_selector('.soundTitle__usernameText')
            artist = obj.text
            obj_results.append({
                'url': url,
                'platform': 'soundcloud',
                'title': title,
                'artist': artist,
                'artwork_url': artwork_url,
            })
            
        self.searching = False
        return obj_results
        

        
