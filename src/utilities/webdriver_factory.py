from typing import Dict, Any

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from utilities.logger import get_logger

logger = get_logger(__name__)


class WebDriverFactory:
    """
    Factory for initializing the WebDriver with centralized options management.
    """

    def __init__(self, config: Dict[str, Any], download_dir: str | None = None) -> None:
        self.config = config
        self.download_dir = download_dir
        logger.info("WebDriverFactory initalized for browser: %s", config.get("browser"))

    def get_driver(self) -> webdriver.Remote:
        """Initializes the WebDriver based on local or remote configuration."""
        browser = self.config.get("browser", "chrome").lower()
        remote_url = self.config.get("remote_url")

        if remote_url:
            return self._create_remote_driver(browser, remote_url)

        match browser:
            case "chrome":
                return self._create_chrome_driver()
            case "firefox":
                return self._create_firefox_driver()
            case "edge":
                return self._create_edge_driver()
            case _:
                raise ValueError(f"Unsupported browser: {browser}")

    def _get_chrome_options(self) -> ChromeOptions:
        options = ChromeOptions()
        if self.config.get("headless"):
            options.add_argument("--headless=new")

        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")

        if self.download_dir:
            options.add_experimental_option("prefs", {
                "download.default_directory": self.download_dir,
                "download.prompt_for_downloads": False,
                "safebrowsing.enabled": True,
            })
        return options

    def _get_firefox_options(self) -> FirefoxOptions:
        options = FirefoxOptions()
        if self.config.get("headless"):
            options.add_argument("-headless")
        return options

    def _get_edge_options(self) -> EdgeOptions:
        options = EdgeOptions()
        if self.config.get("headless"):
            options.add_argument("--headless=new")
        return options

    def _create_chrome_driver(self) -> webdriver.Chrome:
        logger.info("Initializing Chrome (local)...")
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=self._get_chrome_options())
        self._post_setup(driver)
        return driver

    def _create_firefox_driver(self) -> webdriver.Firefox:
        logger.info("Initializing Firefox (local)...")
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=self._get_firefox_options())
        self._post_setup(driver)
        return driver

    def _create_edge_driver(self) -> webdriver.Edge:
        logger.info("Initializing Edge (local)...")
        service = EdgeService(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service, options=self._get_edge_options())
        self._post_setup(driver)
        return driver

    def _create_remote_driver(self, browser: str, remote_url: str) -> webdriver.Remote:
        logger.info("Initializing Remote Driver (%s) at %s", browser, remote_url)

        options_map = {
            "chrome": self._get_chrome_options,
            "firefox": self._get_firefox_options,
            "edge": self._get_edge_options,
        }

        get_options_func = options_map.get(browser)

        if not get_options_func:
            raise ValueError(f"Unsupported remote browser: {browser}")

        options = get_options_func()

        driver = webdriver.Remote(command_executor=remote_url, options=options)
        self._post_setup(driver)
        return driver

    def _post_setup(self, driver: webdriver.Remote) -> None:
        implicit_wait = self.config.get("implicit_wait", 5)
        driver.implicitly_wait(implicit_wait)
        logger.info("Driver setup complete. Implicit wait: %ss", implicit_wait)
