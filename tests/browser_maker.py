import selenium.webdriver
from pages.sign_in import SignInPage


def make_default_browser():
    options = selenium.webdriver.FirefoxOptions()
    options.add_argument('headless')
    browser = selenium.webdriver.Firefox(options=options)

    browser.implicitly_wait(10)

    return browser


def make_authenticated_browser(live_server_url, username, password):
    browser = make_default_browser()

    sign_in_page = SignInPage(browser=browser,
                              live_server_url=live_server_url)
    sign_in_page.load()
    sign_in_page.sign_in(username=username,
                         password=password)

    cookie = browser.get_cookie('sessionid')

    if cookie:
        return browser
    else:
        raise ValueError('Sign-In Failed')
