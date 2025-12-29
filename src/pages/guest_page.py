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

    def navigate_to_contact_us_page(self):
        """
        Navigate to Contact Us Page
        :return: ContactUsPage
        """
        logger.info("Navigating to Contact Us Page via header")
        self.header.click_contact_us()

        from pages.contact_us_page import ContactUsPage
        return ContactUsPage(self.driver)

    def navigate_to_test_cases_page(self):
        """
        Navigate to Test Cases Page
        :return: TestCasesPage
        """
        logger.info("Navigating to Test Cases Page via header")
        self.header.click_test_cases()

        from pages.test_cases_page import TestCasesPage
        return TestCasesPage(self.driver)

    def navigate_to_products_page(self):
        """
        Navigate to Products Page
        :return: ProductsPage
        """
        logger.info("Navigating to Products Page via header")
        self.header.click_products()

        from pages.products_page import ProductsPage
        return ProductsPage(self.driver)

    def is_home_page_visible(self) -> bool:
        """
        Verify that the Home Page is displayed successfully
        """
        logger.info("Verifying Home Page is visible via header")
        return self.header.is_header_visible()