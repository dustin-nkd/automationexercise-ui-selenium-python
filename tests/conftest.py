"""
Features:
    - Adds CLI option --env
    - Provides 'config' fixture (merges base + env)
    - Provides 'driver' fixture (create WebDriver via WebDriverFactory)
    - On test failure: attach screenshot, page source, browser logs to Allure
    - Uses centralized logger
"""
import os

import allure
import pytest
from selenium.common.exceptions import WebDriverException

from utilities.config_reader import ConfigReader
from utilities.logger import get_logger
from utilities.user_action import register_user
from utilities.webdriver_factory import WebDriverFactory

logger = get_logger(__name__)


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
    Hook that attaches the result of each test phase to the test item
    We store the report object so fixture can inspect test outcome
    """
    outcome = yield
    rep = outcome.get_result()

    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture(scope="session")
def config(pytestconfig):
    """
    Returns merged config dictionary
    Priority for environment:
        1) CLI --env value
        2) environment variable TEST_ENV
        3) default 'dev' inside ConfigReader
    """
    cli_env = pytestconfig.getoption("env")
    if cli_env:
        os.environ["TEST_ENV"] = cli_env
        logger.info("Overriding TEST_ENV via CLI: %s", cli_env)

    cfg = ConfigReader().get_config()
    return cfg


@pytest.fixture()
def driver(request, config):
    """
    Creates WebDriver using WebDriverFactory and yields it to the test
    On teardown, if test failed, attaches screenshot/page source/browser logs to Allure
    Always quits the browser at the end
    """
    factory = WebDriverFactory(config)
    driver = factory.get_driver()

    # Optional: maximize for consistent view (some drivers ignore start-maximized)
    try:
        driver.maximize_window()
    except WebDriverException:
        logger.debug("maximize_window not supported by driver/platform")

    # yield to test
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
            print(f"Failed to capture screenshot: {e}")

    driver.quit()


@pytest.fixture
def registered_user(driver, config):
    user = register_user(
        driver=driver,
        base_url=config["base_url"],
        user_profile=config["user_profile"]
    )

    yield user