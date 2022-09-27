from pages.sign_in import SignInPage
from pages.stations import StationsPage


def test_user_can_login(browser):
    sign_in_page = SignInPage(browser)

    sign_in_page.load()
    sign_in_page.log_in()

    stations_page = StationsPage(browser)
    stations_page_title = stations_page.get_page_title()

    assert stations_page_title == 'Stations'
