from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import random
import time

class Browser:
    def __init__(self, headless=True, landing_page='http://google.com'):
        options = Options()
        options.headless = headless
        options.set_preference('media.emp.enabled', True)
        options.set_preference('media.gmp-manager.updateEnabled', True)
        #profile = webdriver.FirefoxProfile(get_firefox_profile_loc())
        self.browser = webdriver.Firefox(options=options)
        self.browser.get(landing_page)

    def goToURL(self, url):
        self.browser.get(url)

    def sendKeyToBrowser(self, key, post_sleep = None):
        actions = ActionChains(self.browser)
        actions.send_keys(key)
        actions.perform()
        if post_sleep != None and post_sleep > 0:
            time.sleep(post_sleep)

    def returnElementsByCSS(self, css_selector):
        return self.browser.find_elements_by_css_selector(css_selector)

    def returnElementByCSS(self, css_selector, i=0, timeout_seconds=10):
        els = []
        timeout = max(0, timeout_seconds * 4) # since we sleep in 0.25s increments
        while len(els) == 0 and timeout >= 0:
            els = self.browser.find_elements_by_css_selector(css_selector)
            timeout -= 1
            time.sleep(0.25)
        return print("Not found") if len(els) == 0 else els[i]

    def clickOnElement(self, el, css='', i=0, timeout_seconds=10):
        el = self.returnElementByCSS(css, i=i, timeout_seconds=timeout_seconds) if el == None else el
        time.sleep(1)
        el.click()
        return el

    def typeInElement(self, el, msg, css=''):
        el = self.returnElementByCSS(css) if el == None else el
        time.sleep(1)
        el.click()
        el.clear()
        for key in msg:
            time.sleep(0.1 + 0.2 * random.random())
            el.send_keys(key)
