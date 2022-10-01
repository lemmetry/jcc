from pages.sign_in import SignInPage
from pages.stations import StationsPage
from pages.accounts import TestAccount


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
