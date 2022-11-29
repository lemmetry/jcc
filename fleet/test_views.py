from django.test import LiveServerTestCase
from django.contrib.auth.models import User
from tests.browser_maker import make_default_browser
from tests.browser_maker import make_authenticated_browser
from fleet.models import Station
from pages.home import HomePage


class UserCanNotAccessHomepageWithoutSigningInTestCase(LiveServerTestCase):
    def setUp(self):
        self.browser = make_default_browser()

    def tearDown(self):
        self.browser.quit()

    def test_user_can_not_access_homepage_without_signing_in(self):
        homepage = HomePage(browser=self.browser,
                            base_url=self.live_server_url)
        homepage.load()

        redirect_to_sign_in_url = '%s%s' % (self.live_server_url, '/signin?next=/')
        self.assertEqual(self.browser.current_url, redirect_to_sign_in_url)


class UserWithValidCredentialsCanAccessHomepageTestCase(LiveServerTestCase):
    def setUp(self):
        username = 'test_user'
        password = 'Pa$$w0rd'
        self.test_user = User.objects.create_user(username=username,
                                                  password=password)
        Station.objects.create(station_id=1)
        Station.objects.create(station_id=2)

        self.browser = make_authenticated_browser(base_url=self.live_server_url,
                                                  username=username,
                                                  password=password)

    def tearDown(self):
        self.browser.quit()

    def test_user_with_valid_credentials_can_access_homepage(self):
        homepage = HomePage(browser=self.browser,
                            base_url=self.live_server_url)
        homepage.load()
        self.assertEqual(self.browser.current_url, f'{self.live_server_url}/')

        page_title = homepage.get_page_title()
        self.assertEqual(page_title, 'Stations')

        signed_in_user = homepage.get_signed_in_user()
        self.assertEqual(self.test_user.username, signed_in_user)

        stations = homepage.get_stations()
        self.assertEqual(len(stations), 2)

        stations_logos = [station['logo_src'] for station in stations]
        for station_logo in stations_logos:
            self.assertEqual(station_logo, f'{self.live_server_url}/static/fleet/logo_jcc.png')

        stations_names_in_db = [station.get_name() for station in Station.objects.all()]
        stations_names_on_the_page = [station['name'] for station in stations]
        self.assertListEqual(stations_names_in_db, stations_names_on_the_page)

    def test_user_can_access_station_orders_dashboard_page_for_every_respective_station_on_the_homepage(self):
        homepage = HomePage(browser=self.browser,
                            base_url=self.live_server_url)
        homepage.load()

        stations = homepage.get_stations()
        for station in stations:
            station_order_dashboard_url = station['url']
            self.browser.get(station_order_dashboard_url)
            self.assertEqual(self.browser.current_url, station_order_dashboard_url)
