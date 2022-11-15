import selenium.webdriver
from pages.sign_in import SignInPage
from pages.accounts import TestAccount


def make_default_browser():
    options = selenium.webdriver.FirefoxOptions()
    options.add_argument('headless')
    browser = selenium.webdriver.Firefox(options=options)

    browser.implicitly_wait(10)

    return browser


def make_authenticated_browser():
    options = selenium.webdriver.FirefoxOptions()
    options.add_argument('headless')
    browser = selenium.webdriver.Firefox(options=options)

    browser.implicitly_wait(10)

    sign_in_page = SignInPage(browser)
    sign_in_page.load()

    username = TestAccount.username
    password = TestAccount.password

    sign_in_page.sign_in(username=username,
                         password=password)

    cookie = browser.get_cookie('sessionid')

    if cookie:
        return browser
    else:
        raise ValueError('Sign-In Failed')
