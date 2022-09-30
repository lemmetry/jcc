class BasePage:

    BASE_URL = 'http://localhost:8000'

    def __init__(self, url, browser):
        self.url = url
        self.browser = browser

    def make_url(self, path):
        return self.BASE_URL + path

    def load(self):
        self.browser.get(self.url)
