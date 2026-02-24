from selenium.webdriver.common.by import By

from utilities.logger import get_logger

logger = get_logger(__name__)


class HeaderComponent:
    """
    Reusable Header component shared across pages.
    Handles navigation by returning Page Objects via the Navigator.
    """

    HDR_MAIN = (By.CSS_SELECTOR, ".header-middle")
    BTN_SIGNUP_LOGIN = (By.CSS_SELECTOR, "a[href='/login']")
    BTN_LOGOUT = (By.CSS_SELECTOR, "a[href='/logout']")
    BTN_DELETE_ACCOUNT = (By.CSS_SELECTOR, "a[href='/delete_account']")
    BTN_CONTACT_US = (By.CSS_SELECTOR, "a[href='/contact_us']")
    BTN_TEST_CASES = (By.XPATH, "//a[contains(text(),'Test Cases')]")
    BTN_PRODUCTS = (By.XPATH, "//a[@href='/products']")
    BTN_CART = (By.CSS_SELECTOR, "a[href='/view_cart']")
    LBL_LOGGED_USER = (By.XPATH, "//li[a[contains(., 'Logged in as')]]")

    def __init__(self, base_page):
        self.base = base_page

    # ---------- Visibility ----------

    def is_header_visible(self) -> bool:
        """
        Verify that the header is displayed successfully.
        """
        logger.info("Checking header visibility")
        return self.base.is_displayed(self.HDR_MAIN)

    def is_logged_user_visible(self) -> bool:
        """
        Verify that the Logged-in user label is displayed.
        """
        logger.info("Checking logged user label visibility")
        return self.base.is_displayed(self.LBL_LOGGED_USER)

    # ---------- Actions (Returning Page Objects) ----------

    def click_signup_login(self):
        """
        Click to Signup / Login and return the LoginPage.
        """
        logger.info("Clicking to Signup / Login")
        self.base.click(self.BTN_SIGNUP_LOGIN)
        return self.base.navigate.login_page

    def click_logout(self):
        """
        Click to Log out and return the LoginPage.
        """
        logger.info("Clicking to Logout")
        self.base.click(self.BTN_LOGOUT)
        return self.base.navigate.login_page

    def click_delete_account(self):
        """
        Click to Delete Account and return the AccountDeletedPage.
        """
        logger.info("Clicking to Delete Account")
        self.base.click(self.BTN_DELETE_ACCOUNT)
        return self.base.navigate.account_deleted_page

    def click_contact_us(self):
        """
        Click to Contact Us and return the ContactUsPage.
        """
        logger.info("Clicking to Contact Us")
        self.base.click(self.BTN_CONTACT_US)
        return self.base.navigate.contact_us_page

    def click_test_cases(self):
        """
        Click to Test Cases and return the TestCasesPage.
        """
        logger.info("Clicking to Test Cases")
        self.base.click(self.BTN_TEST_CASES)
        return self.base.navigate.test_cases_page

    def click_products(self):
        """
        Click to Products and return the ProductsPage.
        """
        logger.info("Clicking to Products")
        self.base.click(self.BTN_PRODUCTS)
        return self.base.navigate.products_page

    def click_cart(self):
        """
        Click to Cart and return the CartPage.
        """
        logger.info("Clicking to Cart")
        self.base.click(self.BTN_CART)
        return self.base.navigate.cart_page

    def scroll_up(self) -> None:
        """
        Scroll to the top of the page.
        """
        logger.info("Scrolling up to the header")
        self.base.scroll_into_view(self.HDR_MAIN)
