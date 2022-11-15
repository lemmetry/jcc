from django.test import TestCase
from tests.browser_maker import make_default_browser
from tests.browser_maker import make_authenticated_browser
from pages.home import HomePage


class UserCanNotAccessHomepageWithoutSigningInTestCase(TestCase):
    def setUp(self):
        self.browser = make_default_browser()
        home_page = HomePage(self.browser)
        home_page.load()

    def tearDown(self):
        self.browser.quit()

    def test_user_can_not_access_homepage_without_signing_in(self):
        self.assertEqual(self.browser.current_url, 'http://localhost:8000/signin?next=/')


class UserWithValidCredentialsCanAccessHomepageTestCase(TestCase):
    def setUp(self):
        self.browser = make_authenticated_browser()
        self.homepage = HomePage(self.browser)
        self.homepage.load()

    def tearDown(self):
        self.browser.quit()

    def test_user_with_valid_Credentials_Can_access_homepage(self):
        page_title = self.homepage.get_page_title()
        self.assertEqual(page_title, 'Stations')

        welcome_user_message = self.homepage.get_welcome_user_message()
        self.assertIn('welcome, ', welcome_user_message)

        # TODO assess stations displayed