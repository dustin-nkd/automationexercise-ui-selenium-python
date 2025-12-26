from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utilities.logger import get_logger

logger = get_logger(__name__)


class AccountCreatedPage(BasePage):
    """
    Page Object for AutomationExcercise Account Created Page
    URL: https://automationpractice.com/account_created
    """

    LBL_ACCOUNT_CREATED = (By.XPATH, "//b[normalize-space()='Account Created!']")
    BTN_CONTINUE = (By.XPATH, "//a[normalize-space()='Continue']")

    def get_account_created_message(self) -> str:
        """
        Get account created message
        """
        logger.info("Getting account created message")
        return self.get_text(self.LBL_ACCOUNT_CREATED)

    def click_continue(self):
        """
        Clicks continue
        """
        logger.info("Clicking continue")
        self.click(self.BTN_CONTINUE)

        from pages.home_page import HomePage
        return HomePage(self.driver)