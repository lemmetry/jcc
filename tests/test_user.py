from pages.sign_in import SignInPage
from pages.stations import StationsPage
from pages.accounts import TestAccount
import pytest


def test_user_can_sign_in(browser):
    sign_in_page = SignInPage(browser)
    sign_in_page.load()

    username = TestAccount.username
    password = TestAccount.password

    sign_in_page.sign_in(username=username,
                         password=password)

    stations_page = StationsPage(browser)
    stations_page_title = stations_page.get_page_title()

    assert stations_page_title == 'Stations'


def test_user_cant_sign_in_with_invalid_password(browser):
    sign_in_page = SignInPage(browser)
    sign_in_page.load()

    username = TestAccount.username
    invalid_password = 'Invalid_Pa$$w0rd'

    sign_in_page.sign_in(username=username,
                         password=invalid_password)

    sign_in_page_url = sign_in_page.url
    assert browser.current_url == sign_in_page_url

    stations_page = StationsPage(browser)
    stations_page.load()

    station_page_title = stations_page.get_page_title()
    assert station_page_title == 'Sign In'

    welcome_user_message = stations_page.get_welcome_user_message()
    assert welcome_user_message is None

    redirect_to_sign_in_url = '%s?next=%s' % (sign_in_page_url, StationsPage.PATH)
    assert browser.current_url == redirect_to_sign_in_url


@pytest.fixture()
def get_authentication_cookie(browser):
    sign_in_page = SignInPage(browser)
    sign_in_page.load()

    username = TestAccount.username
    password = TestAccount.password

    sign_in_page.sign_in(username=username,
                         password=password)

    stations_page = StationsPage(browser)
    stations_page_title = stations_page.get_page_title()

    if stations_page_title == 'Stations':
        cookie = browser.get_cookie('sessionid')
        browser.delete_all_cookies()
        yield cookie
    else:
        raise ValueError('Sign-In Failed')

    browser.quit()


class TestSignInWithCookie:
    def test_user_can_access_stations_page(self, browser, get_authentication_cookie):
        sign_in_page = SignInPage(browser)
        sign_in_page.load()

        cookie = get_authentication_cookie

        browser.add_cookie({
            "name": cookie["name"],
            "value": cookie["value"]
        })

        stations_page = StationsPage(browser)
        stations_page.load()
        stations_page_title = stations_page.get_page_title()

        assert stations_page_title == 'Stations'
