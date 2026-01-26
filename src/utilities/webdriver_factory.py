"""
Features:
    - Supports Chrome, Firefox, and Edge
    - Supports headless mode
    - Supports remote Selenium Grid
    - Automatic driver download (via webdriver-manager)
    - Comprehensive logging
"""
from typing import Dict

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from utilities.logger import get_logger

logger = get_logger(__name__)


class WebDriverFactory:
    """
    Factory for initializing the WebDriver with options configured from config.yaml
    Example config:
        browser: chrome
        headless: false
        remote_url: null
        implicit_wait: 5
    """

    def __init__(self, config: Dict, download_dir: str | None = None) -> None:
        self.config = config
        self.download_dir = download_dir
        logger.info("WebDriverFactory initalized with config: %s download_dir: %s", config, download_dir)

    def get_driver(self) -> webdriver.Remote:
        """
        Initialize the WebDriver based on the configuration
        :return: WebDriver instance
        """
        browser = self.config.get("browser", "chrome").lower()

        if self.config.get("remote_url"):
            logger.info("Creating remote driver: %s", browser)
            return self._create_remote_driver(browser)

        match browser:
            case "chrome":
                return self._create_chrome_driver()
            case "firefox":
                return self._create_firefox_driver()
            case "edge":
                return self._create_edge_driver()
            case _:
                raise ValueError(f"Unsupported browser: {browser}")

    def _create_chrome_driver(self) -> webdriver.Chrome:
        logger.info("Initializing chrome driver (local)...")
        ChromeDriverManager().install()

        options = ChromeOptions()
        if self.config.get("headless"):
            options.add_argument("--headless=new")

        options.add_argument("--disable-notifications")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        options.add_argument("--start-maximized")

        if self.download_dir:
            prefs = {
                "download.default_directory": self.download_dir,
                "download.prompt_for_downloads": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True,
            }
            options.add_experimental_option("prefs", prefs)

        driver = webdriver.Chrome(options=options)
        self._post_setup(driver)
        return driver

    def _create_firefox_driver(self) -> webdriver.Firefox:
        logger.info("Initializing firefox driver (local)...")
        GeckoDriverManager().install()

        options = FirefoxOptions()
        if self.config.get("headless"):
            options.add_argument("-headless")

        driver = webdriver.Firefox(options=options)
        self._post_setup(driver)
        return driver

    def _create_edge_driver(self) -> webdriver.Edge:
        logger.info("Initializing edge driver (local)...")
        EdgeChromiumDriverManager().install()

        options = EdgeOptions()
        if self.config.get("headless"):
            options.add_argument("--headless=new")

        driver = webdriver.Edge(options=options)
        self._post_setup(driver)
        return driver

    def _create_remote_driver(self, browser: str) -> webdriver.Remote:
        remote_url = self.config.get("remote_url")
        logger.info("Connecting to remote Selenium Grid: %s", remote_url)

        if browser == "chrome":
            options = ChromeOptions()
        elif browser == "firefox":
            options = FirefoxOptions()
        elif browser == "edge":
            options = EdgeOptions()
        else:
            raise ValueError(f"Unsupported browser: {browser}")

        if self.config.get("headless"):
            if browser == "firefox":
                options.add_argument("-headless")
            else:
                options.add_argument("--headless=new")

        options.set_capability("browserName", browser)

        driver = webdriver.Remote(
            command_executor=remote_url,
            options=options
        )

        self._post_setup(driver)
        return driver

    def _post_setup(self, driver) -> None:
        """
        Common setup for all browsers
        """
        implicit = self.config.get("implicit_wait", 5)
        driver.implicitly_wait(implicit)
        logger.info("Driver initialized with implicit_wait: %s", implicit)