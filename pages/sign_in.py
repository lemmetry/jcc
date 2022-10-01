from pages.base import BasePage
from selenium.webdriver.common.by import By


class SignInPage(BasePage):

    PATH = '/jcc/signin'

    USERNAME_FIELD_LOCATOR = (By.ID, 'inputUsername')
    PASSWORD_FIELD_LOCATOR = (By.ID, 'inputPassword')
    SIGN_IN_BUTTON_LOCATOR = (By.CSS_SELECTOR, 'button[type="submit"]')

    def __init__(self, browser):
        url = self.make_url(self.PATH)
        BasePage.__init__(self, url, browser)

    def sign_in(self, username, password):
        username_field = self.browser.find_element(*self.USERNAME_FIELD_LOCATOR)
        username_field.send_keys(username)

        password_field = self.browser.find_element(*self.PASSWORD_FIELD_LOCATOR)
        password_field.send_keys(password)

        sign_in_button = self.browser.find_element(*self.SIGN_IN_BUTTON_LOCATOR)
        sign_in_button.click()
