class StationsPage:

    def __init__(self, browser):
        self.browser = browser

    def get_page_title(self):
        return self.browser.title
