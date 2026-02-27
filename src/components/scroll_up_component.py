from selenium.webdriver.common.by import By

from utilities.logger import get_logger

logger = get_logger(__name__)


class ScrollUpComponent:
    """
    Component for the scroll-to-top arrow button.
    """

    BTN_SCROLL_UP = (By.ID, "scrollUp")

    def __init__(self, base_page):
        self.base = base_page

    def click_scroll_up(self) -> None:
        """Clicks the scroll up arrow at the bottom right."""
        logger.info("Clicking the scroll-up arrow button")
        self.base.click(self.BTN_SCROLL_UP)
