from selenium.webdriver.remote.webdriver import WebDriver

from pages.account_created_page import AccountCreatedPage
from pages.account_deleted_page import AccountDeletedPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.contact_us_page import ContactUsPage
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.order_placed_page import OrderPlacedPage
from pages.payment_page import PaymentPage
from pages.product_details_page import ProductDetailsPage
from pages.products_page import ProductsPage
from pages.signup_page import SignUpPage
from pages.test_cases_page import TestCasesPage


# Import all Page Objects here
# Since Navigator is independent, these imports won't casue circular dependencies


class Navigator:
    """
    Centralized place to initialize and access all Page Objects
    Act as an Application Controller to manage the flow of the entire system.
    """

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def open_site(self, url: str) -> HomePage:
        """
        Opens the browser with the given URL and returns the HomePage.
        This is the entry point of the test application.
        """
        self.driver.get(url)
        return self.home_page

    # ---------- Page Object Properties ----------

    @property
    def login_page(self) -> LoginPage:
        return LoginPage(self.driver)

    @property
    def signup_page(self) -> SignUpPage:
        return SignUpPage(self.driver)

    @property
    def home_page(self) -> HomePage:
        return HomePage(self.driver)

    @property
    def cart_page(self) -> CartPage:
        return CartPage(self.driver)

    @property
    def products_page(self) -> ProductsPage:
        return ProductsPage(self.driver)

    @property
    def product_details_page(self) -> ProductDetailsPage:
        return ProductDetailsPage(self.driver)

    @property
    def contact_us_page(self) -> ContactUsPage:
        return ContactUsPage(self.driver)

    @property
    def checkout_page(self) -> CheckoutPage:
        return CheckoutPage(self.driver)

    @property
    def payment_page(self) -> PaymentPage:
        return PaymentPage(self.driver)

    @property
    def order_placed_page(self) -> OrderPlacedPage:
        return OrderPlacedPage(self.driver)

    @property
    def account_created_page(self) -> AccountCreatedPage:
        return AccountCreatedPage(self.driver)

    @property
    def account_deleted_page(self) -> AccountDeletedPage:
        return AccountDeletedPage(self.driver)

    @property
    def test_cases_page(self) -> TestCasesPage:
        return TestCasesPage(self.driver)
