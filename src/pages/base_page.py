import time
from pathlib import Path
from typing import Tuple, Optional, Any

import allure
from selenium.common import NoSuchElementException
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    StaleElementReferenceException,
    TimeoutException,
    WebDriverException,
)
from selenium.webdriver import ActionChains
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait

from components.add_to_cart_modal_component import AddToCartComponent
from components.category_sidebar_component import CategorySidebarComponent
from components.footer_component import FooterComponent
from components.header_component import HeaderComponent
from components.home_products_component import HomeProductsComponent
from components.scroll_up_component import ScrollUpComponent
from utilities.logger import get_logger

Locator = Tuple[str, str]  # (By.CSS_SELECTOR, "selector") or (By.XPATH, "//...")

logger = get_logger(__name__)


class BasePage:
    """
    Base class for all Page Objects.
    Provides common interaction methods and centralized navigation
    """

    # ---------- Constants ----------

    DEFAULT_TIMEOUT: int = 10
    POLL_FREQUENCY: float = 0.25

    # ---------- Initialization ----------

    def __init__(self, driver: WebDriver, timeout: Optional[int] = None) -> None:
        """
        Initializes the Page Object with WebDriver and common components.
        """
        self.driver = driver
        self.timeout = timeout or self.DEFAULT_TIMEOUT
        self._navigate = None

        # Components initialization
        self.header = HeaderComponent(self)
        self.footer = FooterComponent(self)
        self.products = HomeProductsComponent(self)
        self.add_to_cart_modal = AddToCartComponent(self)
        self.category_sidebar = CategorySidebarComponent(self)
        self.scroll_up = ScrollUpComponent(self)

        logger.debug("BasePage initialized with timeout=%s", self.timeout)

    @property
    def navigate(self):
        """
        Lazy-loaded property to access the Application Controller (Navigator).
        Allows jumping between pages without circular imports.
        """
        from pages.navigator import Navigator
        if self._navigate is None:
            self._navigate = Navigator(self.driver)
        return self._navigate

    # ---------- Wait Helpers ----------

    def _wait_for(self, condition, timeout: Optional[int] = None) -> Any:
        """
        Internal helper for WebDriverWait.
        """
        _timeout = timeout or self.timeout
        return WebDriverWait(self.driver, _timeout, self.POLL_FREQUENCY).until(condition)

    # ---------- Find Elements ----------

    def find(self, locator: Locator, timeout: Optional[int] = None) -> WebElement:
        """
        Finds an elements present in the DOM.
        """
        by, value = locator
        return self._wait_for(EC.presence_of_element_located((by, value)), timeout)

    def find_visible(self, locator: Locator, timeout: Optional[int] = None) -> WebElement:
        """
        Finds an element that is both present and visible.
        """
        by, value = locator
        return self._wait_for(EC.visibility_of_element_located((by, value)), timeout)

    def find_all(self, locator: Locator, timeout: Optional[int] = None) -> list[WebElement]:
        """
        Returns a list of all elements matching the locator.
        """
        by, value = locator
        _timeout = timeout or self.timeout
        end = time.time() + _timeout
        while time.time() < end:
            try:
                elems = self.driver.find_elements(by, value)
                if elems:
                    return elems
            except WebDriverException:
                pass
            time.sleep(self.POLL_FREQUENCY)
        return []

    # ---------- Interaction Actions ----------

    def click(self, locator: Locator, timeout: Optional[int] = None) -> None:
        """
        Waits for element to be clickable then clicks it.
        """
        elem = self._wait_for(EC.element_to_be_clickable(locator), timeout)
        logger.info("Clicking element %s", locator)
        elem.click()

    def safe_click(self, locator: Locator, retries: int = 2, timeout: Optional[int] = None) -> bool:
        """
        Attempts to click with retries for stale or intercepted elements.
        """
        attempt = 0
        while attempt <= retries:
            try:
                self.click(locator, timeout)
                return True
            except (StaleElementReferenceException, ElementClickInterceptedException, WebDriverException) as e:
                logger.warning("Click attempt %s failed: %s", attempt + 1, e)
                time.sleep(0.5)
                attempt += 1
            except TimeoutException as e:
                return False
        return False

    def send_keys(self, locator: Locator, text: str, clear_first: bool = True, timeout: Optional[int] = None) -> None:
        """
        Sends text to an input field.
        """
        elem = self.find_visible(locator, timeout)
        logger.info("Sending keys to %s", locator)
        if clear_first:
            elem.clear()
        elem.send_keys(text)

    # ---------- Getters & State ----------

    def get_text(self, locator: Locator, timeout: Optional[int] = None) -> str:
        """
        Retrieves and trims text from an element.
        """
        elem = self.find_visible(locator, timeout)
        return (elem.text or "").strip()

    def get_attribute(self, locator: Locator, attribute: str, timeout: Optional[int] = None) -> Optional[str]:
        """
        Retrieves a specific attribute from an element.
        """
        elem = self.find(locator, timeout)
        return elem.get_attribute(attribute)

    def is_displayed(self, locator: Locator, timeout: Optional[int] = None) -> bool:
        """
        Checks if an element is currently visible.
        """
        try:
            self.find_visible(locator, timeout)
            return True
        except TimeoutException:
            return False

    def is_present(self, locator: Locator, timeout: Optional[int] = None) -> bool:
        """
        Checks if an element exists in the DOM.
        """
        try:
            self.find(locator, timeout)
            return True
        except TimeoutException:
            return False

    def is_selected(self, locator: Locator, timeout: Optional[int] = None) -> bool:
        """
        Checks if a checkbox or radio button is selected.
        """
        try:
            elem = self.find_visible(locator, timeout)
            return elem.is_selected()
        except (TimeoutException, NoSuchElementException):
            return False

    def wait_until_not_present(self, locator: Locator, timeout: Optional[int] = None) -> None:
        """
        Waits for an element to disappear from the DOM.
        """
        self._wait_for(EC.visibility_of_element_located(locator), timeout)

    # ---------- JavaScript & Actions ----------

    def scroll_into_view(self, locator: Locator, timeout: Optional[int] = None) -> None:
        """
        Scrolls the element in to the center of the viewport using JS.
        """
        elem = self.find(locator, timeout)
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center', inline:'center'});", elem)

    def hover(self, locator: Locator, timeout: Optional[int] = None) -> None:
        """
        Hover the mouse over an element.
        """
        elem = self.find_visible(locator, timeout)
        ActionChains(self.driver).move_to_element(elem).perform()

    # ---------- Dropdowns & Files ----------

    def select_dropdown_by_value(self, locator: Locator, value: str, timeout: Optional[int] = None) -> None:
        """
        Selects an option from a standard <select> dropdown by value.
        """
        elem = self.find_visible(locator, timeout)
        Select(elem).select_by_value(value)

    def upload_file(self, locator: Locator, file_path: str) -> None:
        """
        Uploads a file to an input[type=filep]
        """
        absolute_path = str(Path(file_path).resolve())
        self.send_keys(locator, absolute_path)

    # ---------- Alerts ----------

    def wait_for_alert(self, timeout: Optional[int] = None) -> Alert:
        """
        Waits for a browser alert to be present.
        """
        return self._wait_for(EC.alert_is_present(), timeout)

    def accept_alert(self, timeout: Optional[int] = None) -> None:
        """
        Accepts the current browser alert.
        """
        self.wait_for_alert().accept()

    def dismiss_alert(self, timeout: Optional[int] = None) -> None:
        """
        Dismissess the current browser alert.
        """
        self.wait_for_alert().dismiss()

    # ---------- Screenshots & Allure ----------

    def take_screenshot(self, name: Optional[str] = None) -> bytes:
        """
        Captures a screenshot as PNG bytes.
        """
        try:
            return self.driver.get_screenshot_as_png()
        except WebDriverException:
            return b""

    def attach_screenshot_to_allure(self, name: Optional[str] = None) -> None:
        """
        Captures and attaches a screenshot to the Allure report.
        """
        png = self.take_screenshot(name)
        if png:
            allure.attach(png, name=name or "screenshot", attachment_type=allure.attachment_type.PNG)

    # ---------- Context Switching ----------

    def switch_to_frame(self, locator: Locator, timeout: Optional[int] = None) -> None:
        """
        Switches context to an iframe.
        """
        elem = self.find(locator, timeout)
        self.driver.switch_to.frame(elem)

    def switch_to_default(self) -> None:
        """
        Switches back to the main document context.
        """
        self.driver.switch_to.default_content()
