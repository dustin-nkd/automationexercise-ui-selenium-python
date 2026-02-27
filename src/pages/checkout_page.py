from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utilities.logger import get_logger

logger = get_logger(__name__)


class CheckoutPage(BasePage):
    """
    Page Object for AutomationExcercise Checkout Page.
    Handles address verification and order review before payment.
    """

    # ---------- Address Locators ----------
    LBL_DELIVERY_ADDRESS = (By.XPATH, "//h2[text()='Address Details']")
    DELIVERY_ADDRESS_LIST = (By.CSS_SELECTOR, "#address_delivery li")
    BILLING_ADDRESS_LIST = (By.CSS_SELECTOR, "#address_invoice li")

    # ---------- Review Order Locators ----------
    LBL_REVIEW_ORDER = (By.XPATH, "//h2[text()='Review Your Order']")
    ROW_ORDER_ITEMS = (By.CSS_SELECTOR, "table tbody tr[id^='product-']")

    INPUT_DESCRIPTION = (By.NAME, "message")
    BTN_PLACE_ORDER = (By.CSS_SELECTOR, ".check_out")

    # ---------- Visibility & Validation ----------

    def is_checkout_page_valid(self) -> bool:
        """
        Verify key section of the checkout page are visible.
        """
        logger.info("Validating Checkout page visibility")
        return (
                self.is_displayed(self.LBL_DELIVERY_ADDRESS) and
                self.is_displayed(self.LBL_REVIEW_ORDER)
        )

    # ---------- Data Extraction (Getters) ----------

    def get_delivery_address_details(self) -> list[str]:
        """
        Returns a list of strings containing delivery address lines.
        Expected: [Title, Name, Company, Address1, Address2, City, State, Zip, Country, Phone]
        """
        logger.info("Extracting delivery address details")
        elements = self.find_all(self.DELIVERY_ADDRESS_LIST)
        return [el.text.strip() for el in elements if el.text.strip()][1:]

    def get_billing_address_details(self) -> list[str]:
        """
        Returns a list of strings containing billing address lines.
        """
        logger.info("Extracting billing address details")
        elements = self.find_all(self.BILLING_ADDRESS_LIST)
        return [el.text.strip() for el in elements if el.text.strip()][1:]

    # ---------- Actions ----------

    def enter_description(self, message: str) -> None:
        """Enter comments in the text area."""
        logger.info(f"Adding order comment: {message}")
        self.send_keys(self.INPUT_DESCRIPTION, message, clear_first=True)

    def place_order(self):
        """
        Click Place Order and navigate to PaymentPage.
        """
        logger.info("Clicking 'Place Order' button")
        self.click(self.BTN_PLACE_ORDER)
        return self.navigate.payment_page
