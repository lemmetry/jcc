from pages.base import BasePage
from selenium.webdriver.common.by import By
import selenium.common.exceptions


class StationsPage(BasePage):

    PATH = '/'

    WELCOME_USER_MESSAGE_LOCATOR = (By.ID, 'welcome_user_message')

    def __init__(self, browser):
        url = self.make_url(self.PATH)
        BasePage.__init__(self, url, browser)

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
