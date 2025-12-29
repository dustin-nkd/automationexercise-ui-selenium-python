from pages.base_page import BasePage
from utilities.logger import get_logger

logger = get_logger(__name__)


class HomePage(BasePage):
    """
    Page Object for AutomationExcercise Home Page
    URL: https://automationpractice.com
    """

    # ---------- Verifications ----------

    def is_home_page_visible(self) -> bool:
        """
        Verify that the Home Page is displayed successfully
        """
        logger.info("Verifying Home Page is visible")
        return self.header.is_header_visible()

    def is_logged_user_visible(self) -> bool:
        """
        Verify that the page logged user is displayed successfully
        """
        logger.info("Verifying logged user is visible")
        return self.header.is_logged_user_visible()

    # ---------- Actions / Navigation ----------

    def delete_account(self):
        """
        Delete account and navigate to AccountDeletePage
        """
        logger.info("Deleting account via header")
        self.header.click_delete_account()

        from pages.account_deleted_page import AccountDeletedPage
        return AccountDeletedPage(self.driver)

    def logout(self):
        """
        Logout user and navigate to LoginPage
        """
        logger.info("Logging out via header")
        self.header.click_logout()

        from pages.login_page import LoginPage
        return LoginPage(self.driver)