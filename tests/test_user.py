from pages.sign_in import SignInPage
from pages.stations import StationsPage
from pages.accounts import TestAccount


def test_user_can_sign_in(default_browser):
    sign_in_page = SignInPage(default_browser)
    sign_in_page.load()

    username = TestAccount.username
    password = TestAccount.password

    sign_in_page.sign_in(username=username,
                         password=password)

    stations_page = StationsPage(default_browser)
    stations_page_title = stations_page.get_page_title()

    assert stations_page_title == 'Stations'


def test_user_cant_sign_in_with_invalid_password(default_browser):
    sign_in_page = SignInPage(default_browser)
    sign_in_page.load()

    username = TestAccount.username
    invalid_password = 'Invalid_Pa$$w0rd'

    sign_in_page.sign_in(username=username,
                         password=invalid_password)

    sign_in_page_url = sign_in_page.url
    assert default_browser.current_url == sign_in_page_url

    stations_page = StationsPage(default_browser)
    stations_page.load()

    station_page_title = stations_page.get_page_title()
    assert station_page_title == 'Sign In'

    welcome_user_message = stations_page.get_welcome_user_message()
    assert welcome_user_message is None

    redirect_to_sign_in_url = '%s?next=%s' % (sign_in_page_url, StationsPage.PATH)
    assert default_browser.current_url == redirect_to_sign_in_url


def test_signed_in_user_can_open_stations_page(authenticated_browser):
    stations_page = StationsPage(authenticated_browser)
    stations_page.load()

    stations_page_title = stations_page.get_page_title()
    assert stations_page_title == 'Stations'

    welcome_user_message = stations_page.get_welcome_user_message()
    assert 'welcome, ' in welcome_user_message

    # TODO - replace hardcoded names below with actual data from the db
    stations_names_in_db = ['Station 1', 'Station 2', 'Station 3', 'Station 4', 'Station 5', 'Station 6']

    stations_names_on_the_page = stations_page.get_stations_names()
    assert stations_names_in_db == stations_names_on_the_page
