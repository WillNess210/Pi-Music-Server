from . browser_control import Browser
import time

class SongSearcher(Browser):
    
    def __init__(self, headless=True):
        super().__init__(headless=headless, landing_page='https://soundcloud.com/search')
       	while(len(self.returnElementsByCSS('.searchOptions__navigationLink')) == 0):
               time.sleep(1)
    
	    self.clickOnElement(None, '.searchOptions__navigationLink', i=2, timeout_seconds=30)
        self.searching = False
        
    def searchFor(self, search_term):
        if self.searching == True:
            return {'success': False}
        self.searching = True
        search_term = str(search_term)
        print(f'Search Term: |{search_term}|')

        self.typeInElement(None, search_term, '.headerSearch__input')
        self.clickOnElement(None, '.headerSearch__submit')
        time.sleep(2)
        self.browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(0.5)
        self.browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(1.5)

        obj_results = []
        search_items = self.returnElementsByCSS('.sound.searchItem__trackItem')
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
        

        
