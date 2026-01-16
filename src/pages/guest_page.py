from pages.base_page import BasePage
from utilities.logger import get_logger

logger = get_logger(__name__)


class GuestPage(BasePage):
    """
    Page Object for AutomationExcercise Guest Page
    URL: https://automationpractice.com
    """

    # ---------- Navigation ----------

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

    def navigate_to_cart_page(self):
        """
        Navigate to Cart Page
        :return: CartPage
        """
        logger.info("Navigating to Cart Page via header")
        self.header.click_cart()

        from pages.cart_page import CartPage
        return CartPage(self.driver)

    # ---------- Visibility ----------

    def is_home_page_visible(self) -> bool:
        """
        Verify that the Home Page is displayed successfully
        """
        logger.info("Verifying Home Page is visible via header")
        return self.header.is_header_visible()

    # ---------- Actions ----------

    def scroll_to_footer(self) -> None:
        """
        Scroll down to Footer Page
        """
        logger.info("Scrolling down to Footer Page via header")
        self.footer.scroll_down_to_footer()

    def view_product_from_home(self, name: str):
        """
        Navigate to Products Details page from home
        """
        logger.info("Navigating to Products Details page suggests from home")
        self.products.click_view_product_of(name)

        from pages.product_details_page import ProductDetailsPage
        return ProductDetailsPage(self.driver)

    def add_product_to_cart_by_item_from_home(self, name: str):
        """
        Add product to cart by item from home
        """
        logger.info("Add product to cart by item from home")
        self.products.add_product_to_cart_by_item(name)