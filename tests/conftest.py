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
def pytest_runtest_makereport(item):
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

    try:
        # test outcome is available on request.node
        rep_call = getattr(request.node, "rep_call", None)
        failed = rep_call.failed if rep_call is not None else False

        if failed:
            logger.error("Test %s failed - collecting artifacts", request.node.name)

            # 1) Screenshot
            try:
                png = driver.get_screenshot_as_png()
                allure.attach(png, name=f"screenshot-{request.node.name}",
                attachment_type=allure.attachment_type.PNG)
                logger.debug("Attached screenshot for %s", request.node.name)
            except Exception as e:
                logger.exception("Failed to capture screenshot: %s", e)
    finally:
        # Always quit the driver
        try:
            driver.quit()
            logger.info("Driver quit successfully for test %s", request.node.name)
        except Exception as e:
            logger.exception("Error quitting driver for %s: %s", request.node.name, e)