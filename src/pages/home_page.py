from selenium.webdriver.common.by import By

from pages.account_deleted_page import AccountDeletedPage
from pages.base_page import BasePage
from utilities.logger import get_logger

logger = get_logger(__name__)


class HomePage(BasePage):
    """
    Page Object for AutomationExcercise Home Page
    URL: https://automationpractice.com
    """
    HEADER = (By.CSS_SELECTOR, ".header-middle")
    LABEL_LOGGED_USER = (By.XPATH, "//li[a[contains(., 'Logged in as')]]")
    BTN_DELETE_ACCOUNT = (By.CSS_SELECTOR, "a[href='/delete_account']")
    BTN_LOGOUT = (By.CSS_SELECTOR, "a[href='/logout']")

    def is_home_page_visible(self) -> bool:
        """
        Verify that the Home Page is displayed successfully
        """
        logger.info("Verifying Home Page is visible")
        return self.is_displayed(self.HEADER)

    def is_logged_user_visible(self) -> bool:
        """
        Verify that the page logged user is displayed successfully
        """
        logger.info("Verifying logged user is visible")
        return self.is_displayed(self.LABEL_LOGGED_USER)

    def click_delete_account(self) -> AccountDeletedPage:
        """
        Click Delete Account
        """
        logger.info("Clicking Delete Account")
        self.click(self.BTN_DELETE_ACCOUNT)
        return AccountDeletedPage(self.driver)

    def click_logout(self):
        """
        Click Logout
        """
        logger.info("Clicking Logout")
        self.click(self.BTN_LOGOUT)
        from pages.login_page import LoginPage
        return LoginPage(self.driver)