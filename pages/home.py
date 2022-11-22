from pages.base import BasePage
from selenium.webdriver.common.by import By
import selenium.common.exceptions


class HomePage(BasePage):

    PATH = '/'

    WELCOME_USER_MESSAGE_LOCATOR = (By.ID, 'welcome_user_message')
    STATIONS_NAMES_LOCATOR = (By.ID, 'station_name')

    def __init__(self, browser, base_url):
        url = base_url + self.PATH
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

    def get_stations_names(self):
        try:
            station_names_fields = self.browser.find_elements(*self.STATIONS_NAMES_LOCATOR)
            return [station_names.text for station_names in station_names_fields]
        except selenium.common.exceptions.NoSuchElementException:
            return None
