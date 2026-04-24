import os
import base64
import pytest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.remote_connection import RemoteConnection


DEFAULT_BROWSER_VERSION = "100.0"


def pytest_addoption(parser):
    parser.addoption(
        "--browser_version",
        default=None,
        help="Browser version"
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

    # 🔑 берём креды из Jenkins
    login = os.getenv("LOGIN")
    password = os.getenv("PASSWORD")

    print("LOGIN:", login)
    print("PASSWORD:", "***")

    # 💥 фикс 401 через Basic Auth header
    auth = base64.b64encode(f"{login}:{password}".encode()).decode()

    executor = RemoteConnection(
        "http://selenoid.autotests.cloud/wd/hub",
        resolve_ip=False
    )

    executor.set_headers({
        "Authorization": f"Basic {auth}"
    })

    driver = webdriver.Remote(
        command_executor=executor,
        options=options
    )

    # чтобы selene/selenium работал стабильно
    driver.maximize_window()

    yield driver

    driver.quit()