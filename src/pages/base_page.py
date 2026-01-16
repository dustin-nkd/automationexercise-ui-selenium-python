import time
from pathlib import Path
from typing import Tuple, Optional, Any

import allure
from selenium.common.exceptions import (
    NoSuchElementException,
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
from components.footer_component import FooterComponent
from components.header_component import HeaderComponent
from components.home_products_component import HomeProductsComponent
from utilities.logger import get_logger

Locator = Tuple[str, str]  # (By.CSS_SELECTOR, "selector") or (By.XPATH, "//...")

logger = get_logger(__name__)


class BasePage:
    """
    Page Object should receive the WebDriver when being initialized
    def __init__(self, driver: WebDriver):
        super().__init__(driver)
    """

    # ---------- Constants ----------

    DEFAULT_TIMEOUT: int = 10
    POLL_FREQUENCY: float = 0.25

    # ---------- Initialization ----------

    def __init__(self, driver: WebDriver, timeout: Optional[int] = None) -> None:
        """
        :param driver: WebDriver instance
        :param timeout: default wait timeout (seconds)
        """
        self.driver = driver
        self.header = HeaderComponent(self)
        self.footer = FooterComponent(self)
        self.products = HomeProductsComponent(self)
        self.add_to_cart_modal = AddToCartComponent(self)
        self.timeout = timeout or self.DEFAULT_TIMEOUT
        logger.debug("BasePage initialized with timeout=%s", self.timeout)

    # ---------- Wait Helpers ----------

    def _wait_for(self, condition, timeout: Optional[int] = None) -> Any:
        """
        Internal helper using WebDriverWait
        :param condition: ExpectedCondition instance
        :param timeout: override default timeout
        """
        _timeout = timeout or self.timeout
        logger.debug("Waiting for condition %s with timeout=%s", condition, _timeout)
        return WebDriverWait(self.driver, _timeout, self.POLL_FREQUENCY).until(condition)

    # ---------- Find Elements ----------

    def find(self, locator: Locator, timeout: Optional[int] = None) -> WebElement:
        """
        Finds an element and returns a WebElement
        Throws a TimoutException if the element is not found
        """
        by, value = locator
        logger.debug("Finding element by=%s value=%s", by, value)
        return self._wait_for(EC.presence_of_element_located((by, value)), timeout)

    def find_visible(self, locator: Locator, timeout: Optional[int] = None) -> WebElement:
        """
        Finds an element is visible (visible & displayed)
        Throws a TimoutException if the element is not found
        """
        by, value = locator
        logger.debug("Finding element by=%s value=%s", by, value)
        return self._wait_for(EC.visibility_of_element_located((by, value)), timeout)

    def find_all(self, locator: Locator, timeout: Optional[int] = None) -> list[WebElement]:
        """
        Returns a list of WebElements (which may be empty if none are found within the timeout)
        """
        by, value = locator
        logger.debug("Finding all elements by=%s value=%s", by, value)
        _timeout = timeout or self.timeout
        end = time.time() + _timeout
        while time.time() < end:
            try:
                elems = self.driver.find_elements(by, value)
                if elems:
                    logger.debug("Found %d elements", len(elems))
                    return elems
            except WebDriverException:
                pass
            time.sleep(self.POLL_FREQUENCY)
        logger.debug("No elements found for locator after timeout")
        return []

    # ---------- Click Actions ----------

    def click(self, locator: Locator, timeout: Optional[int] = None) -> None:
        """
        Safely clicks an element (waits until it is visible and clickable)
        Throws a TimoutException if the element cannot be found or clicked
        """
        elem = self._wait_for(EC.element_to_be_clickable(locator), timeout)
        logger.info("Clicking element %s", locator)
        elem.click()

    def safe_click(self, locator: Locator, retries: int = 2, timeout: Optional[int] = None) -> bool:
        """
        Attempts to click with retries when encountering Stale or Intercepted exceptions
        Returns True if the click is successful, False if it fails
        """
        attempt = 0
        while attempt <= retries:
            try:
                self.click(locator, timeout)
                logger.debug("Click succeeded on attempt &s for &s", attempt + 1, locator)
                return True
            except (StaleElementReferenceException, ElementClickInterceptedException, WebDriverException) as e:
                logger.warning("Click attempt %s failed: %s", attempt + 1, e)
                time.sleep(0.5)
                attempt += 1
            except TimeoutException as e:
                logger.error("Timeout on click after  %s attempts %s", attempt + 1, e)
                return False
        logger.error("safe_click failed after %s attempts for %s", retries + 1, locator)
        return False

    # ---------- Input Actions ----------

    def send_keys(self, locator: Locator, text: str, clear_first: bool = True, timeout: Optional[int] = None) -> None:
        """
        Types text into the input field. If clear_first=True, the field is cleard before typing
        Throws a TimeOutException if the element cannot be found
        """
        elem = self.find_visible(locator, timeout)
        logger.info("Sending keys to %s (len=%s)", locator, len(text or ""))
        if clear_first:
            elem.clear()
        elem.send_keys(text)

    # ---------- Getters ----------

    def get_text(self, locator: Locator, timeout: Optional[int] = None) -> str:
        """
        Retrieves the text of the element (trims whitespace)
        Throws a TimeOutException if the element cannot be found
        """
        elem = self.find_visible(locator, timeout)
        text = elem.text or ""
        logger.debug("Got text from %s: %s", locator, text.strip())
        return text.strip()

    def get_attribute(self, locator: Locator, attribute: str, timeout: Optional[int] = None) -> Optional[str]:
        """
        Retrieves an attribute from the element. Returns None if the attribute does not exist
        """
        elem = self.find(locator, timeout)
        value = elem.get_attribute(attribute)
        logger.debug("Attribute '%s' of %s = %s", attribute, locator, value)
        return value

    # ---------- State Checks ----------

    def is_displayed(self, locator: Locator, timeout: Optional[int] = None) -> bool:
        """
        Checks whether the element is visible (True/False)
        """
        try:
            self.find_visible(locator, timeout)
            logger.debug("Element %s is displayed", locator)
            return True
        except TimeoutException:
            logger.debug("Element %s is not displayed", locator)
            return False

    def is_present(self, locator: Locator, timeout: Optional[int] = None) -> bool:
        """
        Checks whehter the element is present in the DOM
        """
        try:
            self.find(locator, timeout)
            logger.debug("Element %s is present", locator)
            return True
        except TimeoutException:
            logger.debug("Element %s is not present", locator)
            return False

    def is_selected(self, locator: Locator, timeout: Optional[int] = None) -> bool:
        """
        Checks whether the element is selected
        """
        logger.debug("Checking if element is selected: %s", locator)
        try:
            elem = self.find_visible(locator, timeout)
            selected = elem.is_selected()
            logger.info("Element %s selected state: %s", locator, selected)
            return selected
        except Exception as e:
            logger.error("Failed to check selected state for %s: %s", locator, e)
            return False

    def is_message_visible(self, locator: Locator, expected_text: str, timeout: Optional[int] = None) -> bool:
        """
        Verify that an element is visible and contains the expected text
        """
        logger.info("Verifying message '%s' is visbile", expected_text)
        try:
            elem = self.find_visible(locator, timeout)
            actual_text = self.get_text(locator, timeout)
            logger.debug("Actual message text='%s', Expected='%s'", actual_text, expected_text)
            return expected_text in actual_text
        except Exception as e:
            logger.error("Message '%s' is not visible or text mismatch: %s", expected_text, e)
            return False

    def wait_until_not_present(self, locator: Locator, timeout: Optional[int] = None) -> None:
        """
        Waits until the element is not present on the DOM
        """
        logger.info("Waits until element is not present: %s", locator)
        wait_time = timeout or self.timeout
        self._wait_for(EC.invisibility_of_element_located(locator))

    # ---------- JavaScript / Scroll ----------

    def scroll_into_view(self, locator: Locator, timeout: Optional[int] = None) -> None:
        """
        Scrolls the element into the viewport using JavaScript
        """
        elem = self.find(locator, timeout)
        logger.debug("Scrolling element into viewport %s", locator)
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center', inline:'center'});", elem)

    def execute_script(self, script: str, *args) -> Any:
        """
        Executes a JavaScript script and returns the result
        """
        logger.debug("Executing script %s", script)
        return self.driver.execute_script(script, *args)

    def hover(self, locator: Locator, timeout: Optional[int] = None) -> None:
        """
        Hover over element using real mouse movement
        """
        elem = self.find_visible(locator, timeout)
        logger.info("Hovering over element %s using ActionChains", locator)
        ActionChains(self.driver).move_to_element(elem).perform()

    # ---------- Navigation ----------

    def navigate_to(self, url: str) -> None:
        """
        Navigates to a URL
        """
        logger.info("Navigating to URL: %s", url)
        self.driver.get(url)

    # ---------- Dropdown / Upload ----------

    def select_dropdown_by_value(self, locator: Locator, value: str, timeout: Optional[int] = None) -> None:
        """
        Select an option from a <select> dropdown by value attribute
        """
        logger.info("Selecting value '%s' from dropdown", value, locator)
        elem = self.find_visible(locator, timeout)
        try:
            dropdown = Select(elem)
            dropdown.select_by_value(value)
            logger.debug("Dropdown value '%s' selected successfully", value)
        except NoSuchElementException:
            logger.error("Value '%s' is not found in dropdown %s", value, locator)
            raise

    def upload_file(self, locator: Locator, file_path: str, timeout: Optional[int] = None) -> None:
        """
        Upload file using input[type=file]
        """
        absolute_path = str(Path(file_path).resolve())
        self.send_keys(locator, absolute_path)

    # ---------- Alerts ----------

    def wait_for_alert(self, timeout: Optional[int] = None) -> Alert:
        """
        Wait until alert is present
        """
        try:
            return self._wait_for(EC.alert_is_present(), timeout)
        except TimeoutException:
            raise AssertionError("Expected alert to be present, but it was not shown")

    def accept_alert(self, timeout: Optional[int] = None) -> None:
        """
        Accept (OK) browser alert
        """
        alert = self.wait_for_alert()
        alert_text = alert.text
        alert.accept()
        logger.info("Accepted alert with text: %s", alert_text)

    def dismiss_alert(self, timeout: Optional[int] = None) -> None:
        """
        Dismiss (Cancel) browser alert
        """
        alert = self.wait_for_alert()
        alert_text = alert.text
        alert.dismiss()
        logger.info("Dismissed alert with text: %s", alert_text)

    def get_aler_text(self, timeout: Optional[int] = None) -> str:
        """
        Get alert text
        """
        alert = self.wait_for_alert()
        return alert.text

    # ---------- Screenshots / Allure ----------

    def take_screenshot(self, name: Optional[str] = None) -> bytes:
        """
        Takes a screenshot and returns the image bytes (PNG). The file can be attached to Allure
        """
        name = name or f"screenshot_{int(time.time() * 1000)}.png"
        try:
            png = self.driver.get_screenshot_as_png()
            logger.info("Captured screenshot %s (%d bytes", name, len(png))
            return png
        except WebDriverException as e:
            logger.exception("Failed to capture screenshot: %s", e)
            return b""

    def attach_screenshot_to_allure(self, name: Optional[str] = None) -> None:
        """
        Automatically takes a screenshot and attaches it to the Allure report
        """
        png = self.take_screenshot(name)
        if png:
            allure.attach(png, name=name or "screenshot", attachment_type=allure.attachment_type.PNG)
            logger.debug("Attached screenshot to Allure %s", name)

    # ---------- Frame / Context Switching ----------

    def switch_to_frame(self, locator: Locator, timeout: Optional[int] = None) -> None:
        """
        Switches to an iframe using a locator
        """
        elem = self.find(locator, timeout)
        logger.debug("Switching to frame %s", locator)
        self.driver.switch_to.frame(elem)

    def switch_to_default(self) -> None:
        """
        Switches back to the default content
        """
        logger.debug("Switching to default content")
        self.driver.switch_to.default_content()

    # ---------- Composite / Safe Actions ----------

    def wait_and_click(self, locator: Locator, timeout: Optional[int] = None) -> bool:
        """
        Waits for the element to become clickable and the clicks it, returning True/False
        """
        try:
            self.safe_click(locator, timeout)
            return True
        except Exception as e:
            logger.exception("wait_and_click failed for %s: %s", locator, e)
            self.attach_screenshot_to_allure(f"wait_and_click_failure_{int(time.time())}")
            return False

    def wait_and_send_keys(self, locator: Locator, text: str, timeout: Optional[int] = None) -> bool:
        """
        Waits until the element is visiblee, then enters text, returning True/False
        """
        try:
            self.send_keys(locator, text, timeout=timeout)
            return True
        except Exception as e:
            logger.exception("wait_and_send_keys failed for %s: %s", locator, e)
            self.attach_screenshot_to_allure(f"wait_and_send_key_failure_{int(time.time())}")
            return False