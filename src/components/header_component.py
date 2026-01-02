from selenium.webdriver.common.by import By

from utilities.logger import get_logger

logger = get_logger(__name__)


class HeaderComponent:
    """
    Reusable Header component shared across pages
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
        Verify that the Home Page is displayed successfully
        """
        logger.info("Checking header visibility")
        return self.base.is_displayed(self.HDR_MAIN)

    def is_logged_user_visible(self) -> bool:
        """
        Verify that the Logged User Page is displayed successfully
        """
        logger.info("Checking logged user label visibility")
        return self.base.is_displayed(self.LBL_LOGGED_USER)

    # ---------- Actions ----------

    def click_signup_login(self) -> None:
        """
        Click to sign up
        """
        logger.info("Clicking to Signup / Login")
        self.base.click(self.BTN_SIGNUP_LOGIN)

    def click_logout(self) -> None:
        """
        Click to log out
        """
        logger.info("Clicking to Logout")
        self.base.click(self.BTN_LOGOUT)

    def click_delete_account(self) -> None:
        """
        Click to delete account
        """
        logger.info("Clicking to Delete Account")
        self.base.click(self.BTN_DELETE_ACCOUNT)

    def click_contact_us(self) -> None:
        """
        Click to contact us
        """
        logger.info("Clicking to Contact Us")
        self.base.click(self.BTN_CONTACT_US)

    def click_test_cases(self) -> None:
        """
        Click to test cases
        """
        logger.info("Clicking to Test Cases")
        self.base.click(self.BTN_TEST_CASES)

    def click_products(self) -> None:
        """
        Click to products
        """
        logger.info("Clicking to Products")
        self.base.click(self.BTN_PRODUCTS)

    def click_cart(self) -> None:
        """
        Click to cart
        """
        logger.info("Clicking to Cart")
        self.base.click(self.BTN_CART)