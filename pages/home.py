from pages.base import BasePage
from selenium.webdriver.common.by import By
import selenium.common.exceptions


class HomePage(BasePage):

    PATH = '/'

    SIGNED_IN_USER_LOCATOR = (By.ID, 'signed_in_user')
    STATION_CONTAINER_LOCATOR = (By.CLASS_NAME, 'station_container')
    STATION_LINK_LOCATOR = (By.CLASS_NAME, 'station_link')
    STATION_LOGO_LOCATOR = (By.CLASS_NAME, 'station_logo')
    STATION_NAME_LOCATOR = (By.CLASS_NAME, 'station_name')

    def __init__(self, browser, base_url):
        url = base_url + self.PATH
        BasePage.__init__(self, url, browser)

    def get_page_title(self):
        try:
            return self.browser.title
        except selenium.common.exceptions.NoSuchElementException:
            return None

    def get_signed_in_user(self):
        try:
            signed_in_user_element = self.browser.find_element(*self.SIGNED_IN_USER_LOCATOR)
            return signed_in_user_element.text
        except selenium.common.exceptions.NoSuchElementException:
            return None

    def get_stations(self):
        stations = []
        stations_elements = self.browser.find_elements(*self.STATION_CONTAINER_LOCATOR)

        for station_element in stations_elements:
            station_link_element = station_element.find_element(*self.STATION_LINK_LOCATOR)
            station_logo_element = station_element.find_element(*self.STATION_LOGO_LOCATOR)
            station_name_element = station_element.find_element(*self.STATION_NAME_LOCATOR)
            stations.append({
                'name': station_name_element.text,
                'url': station_link_element.get_attribute('href'),
                'logo_src': station_logo_element.get_attribute('src')
            })

        return stations
