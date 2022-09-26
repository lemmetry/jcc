from selenium.webdriver.common.by import By
from pages.accounts import TestAccount


class SignInPage:

    URL = 'http://localhost:8000/jcc/signin'

    USERNAME_FIELD_LOCATOR = (By.ID, 'inputUsername')
    PASSWORD_FIELD_LOCATOR = (By.ID, 'inputPassword')
    SIGN_IN_BUTTON_LOCATOR = (By.CSS_SELECTOR, 'button[type="submit"]')

    def __init__(self, browser):
        self.browser = browser

    def load(self):
        self.browser.get(self.URL)

    def log_in(self):
        username_field = self.browser.find_element(*self.USERNAME_FIELD_LOCATOR)
        username_field.send_keys(TestAccount.username)

        password_field = self.browser.find_element(*self.PASSWORD_FIELD_LOCATOR)
        password_field.send_keys(TestAccount.password)

        sign_in_button = self.browser.find_element(*self.SIGN_IN_BUTTON_LOCATOR)
        sign_in_button.click()
