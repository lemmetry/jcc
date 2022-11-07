import pytest
import selenium.webdriver
from pages.sign_in import SignInPage
from pages.accounts import TestAccount


def make_browser():
    options = selenium.webdriver.FirefoxOptions()
    options.add_argument('headless')
    browser = selenium.webdriver.Firefox(options=options)

    browser.implicitly_wait(10)

    return browser


@pytest.fixture
def default_browser():
    browser = make_browser()

    yield browser

    browser.quit()


@pytest.fixture
def authenticated_browser():
    browser = make_browser()

    sign_in_page = SignInPage(browser)
    sign_in_page.load()

    username = TestAccount.username
    password = TestAccount.password

    sign_in_page.sign_in(username=username,
                         password=password)

    cookie = browser.get_cookie('sessionid')

    if cookie:
        yield browser
        browser.quit()
    else:
        browser.quit()
        raise ValueError('Sign-In Failed')
