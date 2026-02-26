import os
import shutil
import tempfile

import allure
import pytest
from selenium.common.exceptions import WebDriverException

from pages.navigator import Navigator
from utilities.config_reader import ConfigReader
from utilities.data_loader import DataLoader
from utilities.logger import get_logger
from utilities.user_action import register_user
from utilities.webdriver_factory import WebDriverFactory

logger = get_logger(__name__)


# --- Pytest Configuration ---

def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default=None,
        help="Environment to run tests against (overrides TEST_ENV). Example: --env=staging"
    )


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture test results for failure reporting (Allure attachments)
    """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


# --- Infrastructure Fixtures ---

@pytest.fixture(scope="session")
def config(pytestconfig):
    """
    Returns merged config dictionary
    """
    cli_env = pytestconfig.getoption("env")
    if cli_env:
        os.environ["TEST_ENV"] = cli_env
        logger.info("Overriding TEST_ENV via CLI: %s", cli_env)

    return ConfigReader().get_config()


@pytest.fixture
def download_dir():
    """
    Temporary directory for file downloads, cleaned up after test
    """
    path = tempfile.mkdtemp(prefix="download_")
    yield path
    shutil.rmtree(path, ignore_errors=True)


@pytest.fixture
def driver(request, config, download_dir):
    """
    Creates WebDriver and handles failure attachments to Allure
    """
    factory = WebDriverFactory(config=config, download_dir=download_dir)
    driver = factory.get_driver()

    try:
        driver.maximize_window()
    except WebDriverException:
        logger.debug("maximize_window not supported by driver/platform")

    yield driver

    rep_call = getattr(request.node, "rep_call", None)
    if rep_call and rep_call.failed:
        try:
            allure.attach(
                driver.get_screenshot_as_png(),
                name=f"screenshot_{request.node.name}",
                attachment_type=allure.attachment_type.PNG,
            )
        except Exception as e:
            logger.error(f"Failed to capture failure screenshot: {e}")

    driver.quit()


@pytest.fixture
def app(driver):
    """
    Returns the Navigator instance (Application Controller)
    """
    return Navigator(driver)


# --- Business Flow Fixtures (Data & State) ---

@pytest.fixture
def registered_user(app, config, user_profile):
    """
    Registers a new user and returns the profile data
    """
    user = register_user(
        app=app,
        base_url=config["base_url"],
        user_profile=user_profile
    )
    yield user


@pytest.fixture
def logged_in_user(app, config, registered_user):
    """
    Navigates to site, performs login, and returns the HomePage instance
    """
    # 1. Open site and get HomePage (as Guest)
    home_page = app.open_site(config["base_url"])

    # 2. Use Navigator to get Login Page and perform Login
    login_page = home_page.header.click_signup_login()
    home_page = login_page.login(
        registered_user["email"],
        registered_user["password"]
    )

    # 3. Quick sanity check
    assert home_page.is_logged_user_visible(), "User should be logged in successfully"
    return home_page


@pytest.fixture
def user_profile():
    # Load profile from test_data
    data = DataLoader.get_user_data()
    profile = data.get("default_registration_profile")

    if profile is None:
        available_keys = list(data.keys())
        error_msg = f"Key 'default_registration_profile' không tồn tại. Các key hiện có trong file: {available_keys}"
        logger.error(error_msg)
        raise ValueError(error_msg)

    return profile.copy()
