from pages.base_page import BasePage
from utilities.logger import get_logger

logger = get_logger(__name__)


class GuestPage(BasePage):
    """
    Page Object for AutomationExcercise Guest Page
    URL: https://automationpractice.com
    """

    def navigate_to_signup_login_page(self):
        """
        Navigate from Home Page to Signup / Login Page
        :return: LoginPage
        """
        logger.info("Navigating to Signup / Login Page via header")
        self.header.click_signup_login()

        from pages.login_page import LoginPage
        return LoginPage(self.driver)

    def is_home_page_visible(self) -> bool:
        """
        Verify that the Home Page is displayed successfully
        """
        logger.info("Verifying Home Page is visible via header")
        return self.header.is_header_visible()