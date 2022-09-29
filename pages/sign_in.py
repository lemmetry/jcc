from selenium.webdriver.common.by import By
from pages.accounts import TestAccount


class SignInPage:

    DOMAIN = 'http://localhost:8000'
    PATH = '/jcc/signin'

    USERNAME_FIELD_LOCATOR = (By.ID, 'inputUsername')
    PASSWORD_FIELD_LOCATOR = (By.ID, 'inputPassword')
    SIGN_IN_BUTTON_LOCATOR = (By.CSS_SELECTOR, 'button[type="submit"]')

    def __init__(self, browser):
        self.browser = browser

    def get_url(self):
        return self.DOMAIN + self.PATH

    def load(self):
        url = self.get_url()
        self.browser.get(url)

    def log_in(self):
        username_field = self.browser.find_element(*self.USERNAME_FIELD_LOCATOR)
        username_field.send_keys(TestAccount.username)

        password_field = self.browser.find_element(*self.PASSWORD_FIELD_LOCATOR)
        password_field.send_keys(TestAccount.password)

        sign_in_button = self.browser.find_element(*self.SIGN_IN_BUTTON_LOCATOR)
        sign_in_button.click()

    def sign_in_with_credentials(self, username, password):
        username_field = self.browser.find_element(*self.USERNAME_FIELD_LOCATOR)
        username_field.send_keys(username)

        password_field = self.browser.find_element(*self.PASSWORD_FIELD_LOCATOR)
        password_field.send_keys(password)

        sign_in_button = self.browser.find_element(*self.SIGN_IN_BUTTON_LOCATOR)
        sign_in_button.click()
