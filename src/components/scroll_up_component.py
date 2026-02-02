from selenium.webdriver.common.by import By

from utilities.logger import get_logger

logger = get_logger(__name__)


class ScrollUpComponent:
    """
    Scroll up button component
    """

    BTN_SCROLL_UP = (By.XPATH, "//a[@id='scrollUp']")

    def __init__(self, base_page):
        self.base = base_page

    # ---------- Visibility ----------

    def click_scroll_up(self) -> None:
        """
        Click scroll up button
        """
        logger.info("Clicking scroll up button")
        self.base.click(self.BTN_SCROLL_UP)