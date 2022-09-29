from selenium.webdriver.common.by import By
import selenium.common.exceptions


class StationsPage:

    DOMAIN = 'http://localhost:8000'
    PATH = '/jcc/stations'

    WELCOME_USER_MESSAGE_LOCATOR = (By.CSS_SELECTOR, 'ol.breadcrumb li:nth-child(2)')

    def __init__(self, browser):
        self.browser = browser

    def load(self):
        url = self.DOMAIN + self.PATH
        return self.browser.get(url)

    def get_page_title(self):
        try:
            return self.browser.title
        except selenium.common.exceptions.NoSuchElementException:
            return None

    def get_welcome_user_message(self):
        try:
            welcome_user_message_field = self.browser.find_element(*self.WELCOME_USER_MESSAGE_LOCATOR)
            return welcome_user_message_field.text
        except selenium.common.exceptions.NoSuchElementException:
            return None
