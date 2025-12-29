from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utilities.logger import get_logger

logger = get_logger(__name__)


class TestCasesPage(BasePage):
    """
    Page Object for AutomationExcercise Test Cases Page
    URL: https://automationpractice.com/test_cases
    """

    LBL_TEST_CASES_TITLE = (By.XPATH, "//b[normalize-space()='Test Cases']")

    def is_test_cases_page_visible(self):
        """
        Verify Test Cases page is visible
        """
        logger.info("Verifying Test Cases page is visible")
        return self.is_displayed(self.LBL_TEST_CASES_TITLE)