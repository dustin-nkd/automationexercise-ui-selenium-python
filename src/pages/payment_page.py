from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utilities.logger import get_logger

logger = get_logger(__name__)


class PaymentPage(BasePage):
    """
    Page Object for AutomationExcercise Payment Page
    URL: https://automationpractice.com/payment
    """

    # ---------- Inputs ----------
    INPUT_NAME_ON_CARD = (By.XPATH, "//input[@name='name_on_card']")
    INPUT_CARD_NUMBER = (By.XPATH, "//input[@name='card_number']")
    INPUT_CVC = (By.XPATH, "//input[contains(@class,'card-cvc')]")
    INPUT_EXPIRY_MONTH = (By.XPATH, "//input[contains(@class,'card-expiry-month')]")
    INPUT_EXPIRY_YEAR = (By.XPATH, "//input[contains(@class,'card-expiry-year')]")

    BTN_PAY_CONFIRM = (By.XPATH, "//button[@id='submit']")

    MSG_SUCCESS = (By.XPATH, "//div[contains(@class, 'alert-success alert')]")

    # ---------- Actions ----------

    def enter_payment_details(
            self,
            name_on_card: str,
            card_number: str,
            cvc: str,
            expiry_month: str,
            expiry_year: str,
    ) -> None:
        """
        Fill payment information
        """
        logger.info("Entering payment details")
        self.send_keys(self.INPUT_NAME_ON_CARD, name_on_card, clear_first=True)
        self.send_keys(self.INPUT_CARD_NUMBER, card_number, clear_first=True)
        self.send_keys(self.INPUT_CVC, cvc, clear_first=True)
        self.send_keys(self.INPUT_EXPIRY_MONTH, expiry_month, clear_first=True)
        self.send_keys(self.INPUT_EXPIRY_YEAR, expiry_year, clear_first=True)

    def click_pay_and_confirm(self):
        """
        Click Page and Confirm Order
        """
        logger.info("Clicking Pay and Confirm Order")
        self.click(self.BTN_PAY_CONFIRM)

        from pages.order_placed_page import OrderPlacedPage
        return OrderPlacedPage(self.driver)

    # ---------- Getters ----------

    def get_success_message(self) -> str:
        """
        Get Success Message
        """
        logger.info("Getting Success Message")
        return self.get_text(self.MSG_SUCCESS)