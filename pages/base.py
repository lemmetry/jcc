class BasePage:

    BASE_URL = 'http://localhost:8000'

    def __init__(self, browser):
        self.browser = browser
