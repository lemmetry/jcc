from pages.base import BasePage
from selenium.webdriver.common.by import By
import selenium.common.exceptions


class StationsPage(BasePage):

    PATH = '/jcc/stations'

    WELCOME_USER_MESSAGE_LOCATOR = (By.CSS_SELECTOR, 'ol.breadcrumb li:nth-child(2)')

    def get_url(self):
        return self.BASE_URL + self.PATH

    def load(self):
        url = self.get_url()
        self.browser.get(url)

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
