class BasePage:

    def __init__(self, url, browser):
        self.url = url
        self.browser = browser

    def load(self):
        self.browser.get(self.url)
