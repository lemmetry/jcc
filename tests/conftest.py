import pytest
import selenium.webdriver


@pytest.fixture
def browser():
    options = selenium.webdriver.FirefoxOptions()
    options.add_argument('headless')
    browser = selenium.webdriver.Firefox(options=options)

    browser.implicitly_wait(10)

    yield browser

    browser.quit()
