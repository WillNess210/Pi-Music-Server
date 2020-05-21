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

        lmap = lambda func, origin_list : list(map(func, origin_list))
        lfilter = lambda func, origin_list : list(filter(func, origin_list))

        urls = lmap(lambda a : a.get_attribute('href'), returnElementsByCSS('.soundTitle__title'))
        platforms = ['soundcloud' for url in urls]
        titles = lmap(lambda a : a.text, returnElementsByCSS('.soundTitle__title'))
        artists = lmap(lambda a : a.text, returnElementsByCSS('.soundTitle__usernameText'))
        artwork_urls = lmap(lambda a : a.get_attribute('style'), returnElementsByCSS('span.sc-artwork'))
        artwork_urls = lfilter(lambda a : 'background-image' in a, artwork_urls)
        artwork_urls = lmap(lambda a : a.split('url("')[1].split('");')[0], artwork_urls)

        def_lists = {
            'url': urls,
            'platform': platforms,
            'title': titles,
            'artist': artists,
            'artwork_url': artwork_urls,
        }

        obj_results = []
        cols = list(def_lists.keys())
        for i in range(len(urls)):
            to_add = {}
            for col in cols:
                to_add[col] = def_lists[col][i]
            obj_results.append(to_add)

        return obj_results
        

        
