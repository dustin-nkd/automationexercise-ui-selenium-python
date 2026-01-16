from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utilities.logger import get_logger

logger = get_logger(__name__)


class CheckoutPage(BasePage):
    """
    Page Object for AutomationExcercise Checkout Page
    URL: https://automationpractice.com/checkout
    """

    # ---------- Address Details ----------
    LBL_DELIVERY_ADDRESS = (By.XPATH, "//h3[normalize-space()='Your delivery address']")
    LBL_BILLING_ADDRESS = (By.XPATH, "//h3[normalize-space()='Your billing address']")

    ADDRESS_BLOCK = (By.CSS_SELECTOR, "ul.address")

    # ---------- Review Your Order ----------
    LBL_REVIEW_ORDER = (By.XPATH, "//h2[normalize-space()='Review Your Order']")
    ROW_ORDER_ITEMS = (By.XPATH, "//tr[contains(@id,'product')]")

    INPUT_DESCRIPTION = (By.XPATH, "//textarea[@name='message']")
    BTN_PLACE_ORDER = (By.XPATH, "//a[normalize-space()='Place Order']")

    # ---------- Verifications ----------

    def is_address_details_visible(self) -> bool:
        """
        Verify Delivery & Billing address sections are visible
        """
        logger.info(f"Verifying address details section")
        return (
                self.is_displayed(self.LBL_DELIVERY_ADDRESS)
                and self.is_displayed(self.LBL_BILLING_ADDRESS)
                and len(self.find_all(self.ADDRESS_BLOCK)) >= 2
        )

    def is_review_order_visible(self) -> bool:
        """
        Verify Review Your Order section is visible
        """
        logger.info(f"Verifying review order section")
        return (
                self.is_displayed(self.LBL_REVIEW_ORDER)
                and len(self.find_all(self.ROW_ORDER_ITEMS)) > 0
        )

    def is_checkout_page_valid(self) -> bool:
        """
        Verify Address Details & Review Order are visible
        """
        logger.info("Verify checkout page")
        return self.is_address_details_visible() and self.is_review_order_visible()

    # ---------- Actions ----------

    def enter_description(self, message: str) -> None:
        """
        Enter the description of the checkout page
        """
        logger.info(f"Entering description")
        self.send_keys(self.INPUT_DESCRIPTION, message, clear_first=True)

    def place_order(self):
        """
        Place order
        """
        logger.info("Placing order")
        self.click(self.BTN_PLACE_ORDER)

        from pages.payment_page import PaymentPage
        return PaymentPage(self.driver)