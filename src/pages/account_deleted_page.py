from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utilities.logger import get_logger

logger = get_logger(__name__)


class AccountDeletedPage(BasePage):
    """
    Page Object for AutomationExcercise Account Deleted Page
    URL: https://automationpractice.com/delete_account
    """

    LBL_ACCOUNT_DELETED = (By.XPATH, "//b[contains(text(),'Account Deleted!')]")
    BTN_CONTINUE = (By.XPATH, "//a[@data-qa='continue-button']")

    def get_account_deleted_message(self) -> str:
        """
        Get account deleted message
        """
        logger.info("Getting account deleted message")
        return self.get_text(self.LBL_ACCOUNT_DELETED)

    def click_continue(self) -> None:
        """
        Clicks continue button
        """
        logger.info("Clicking continue")
        self.click(self.BTN_CONTINUE)