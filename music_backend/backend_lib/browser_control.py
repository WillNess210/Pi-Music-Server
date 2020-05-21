from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import random
import time

class Browser:
    def __init__(self, headless=True, landing_page='http://google.com'):
        options = Options()
        options.headless = headless
        self.browser = webdriver.Firefox(options=options)
        self.browser.get(landing_page)

    def goToURL(self, url):
        self.browser.get(url)

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
