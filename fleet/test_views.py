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

        Station.objects.bulk_create([
            Station(station_id=i) for i in range(1, 7)
        ])

        self.browser = make_authenticated_browser(base_url=self.live_server_url,
                                                  username=username,
                                                  password=password)

    def tearDown(self):
        self.browser.quit()

    def test_user_with_valid_credentials_can_access_homepage(self):
        homepage = HomePage(browser=self.browser,
                            base_url=self.live_server_url)
        homepage.load()
        self.assertEqual(self.browser.current_url, '%s%s' % (self.live_server_url, '/'))

        page_title = homepage.get_page_title()
        self.assertEqual(page_title, 'Stations')

        welcome_user_message = homepage.get_welcome_user_message()
        self.assertEqual(f'welcome, {self.test_user.username}', welcome_user_message)

        stations_names_in_db = [station.get_name() for station in Station.objects.all()]
        stations_names_on_the_page = homepage.get_stations_names()
        self.assertListEqual(stations_names_in_db, stations_names_on_the_page)
