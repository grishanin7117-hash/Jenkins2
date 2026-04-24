import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selene import Browser, Config
from dotenv import load_dotenv

from utils import attach

DEFAULT_BROWSER_VERSION = "100.0"


load_dotenv()


def pytest_addoption(parser):
    parser.addoption(
        '--browser_version',
        default='128.0'
    )


@pytest.fixture(scope='function')
def setup_browser(request):
    browser_version = request.config.getoption('--browser_version')
    browser_version = browser_version if browser_version else DEFAULT_BROWSER_VERSION

    options = Options()


    options.set_capability("browserName", "chrome")
    options.set_capability("browserVersion", browser_version)
    options.set_capability("selenoid:options", {
        "enableVNC": True,
        "enableVideo": True
    })

    login = os.getenv('LOGIN')
    password = os.getenv('PASSWORD')

    print("LOGIN:", login)
    print("PASSWORD:", password)

    driver = webdriver.Remote(
        command_executor="http://selenoid.autotests.cloud/wd/hub",
        options=options
    )


    browser = Browser(Config(driver=driver))

    yield browser

    # 📎 Allure attachments
    attach.add_html(browser)
    attach.add_screenshot(browser)
    attach.add_logs(browser)
    attach.add_video(browser)

    browser.quit()
