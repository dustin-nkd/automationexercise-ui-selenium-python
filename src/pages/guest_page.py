from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utilities.logger import get_logger

logger = get_logger(__name__)


class GuestPage(BasePage):
    """
    Page Object for AutomationExcercise Guest Page
    URL: https://automationpractice.com
    """

    BTN_SIGNUP_LOGIN = (By.CSS_SELECTOR, "a[href='/login']")
    HDR_MAIN = (By.CSS_SELECTOR, ".header-middle")

    def navigate_to_signup_login_page(self):
        """
        Navigate from Home Page to Signup / Login Page
        :return: LoginPage object
        """
        logger.info("Navigating to Signup / Login Page")
        self.click(self.BTN_SIGNUP_LOGIN)

        from pages.login_page import LoginPage
        return LoginPage(self.driver)

    def is_home_page_visible(self) -> bool:
        """
        Verify that the Home Page is displayed successfully
        """
        logger.info("Verifying Home Page is visible")
        return self.is_displayed(self.HDR_MAIN)