from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utilities.logger import get_logger

logger = get_logger(__name__)


class OrderPlacedPage(BasePage):
    """
    Page Object for AutomationExcercise Order Placed Page
    URL: https://automationpractice.com/payment_done/0
    """

    LBL_ORDER_PLACED = (By.XPATH, "//b[normalize-space()='Order Placed!']")
    BTN_CONTINUE = (By.XPATH, "//a[normalize-space()='Continue']")
    MSG_SUCCESS = (By.XPATH, "//p[normalize-space()='Congratulations! Your order has been confirmed!']")

    # ---------- Verifications ----------

    def is_order_success_visible(self) -> bool:
        """
        Verify order placed success message
        """
        logger.info("Verifying order placed success message")
        return self.is_displayed(self.LBL_ORDER_PLACED)

    # ---------- Getters ----------

    def get_order_success_message(self) -> str:
        """
        Verify order placed success message
        """
        logger.info("Verifying order placed success message")
        return self.get_text(self.MSG_SUCCESS)

    # ---------- Actions ----------

    def click_continue(self):
        """
        Click continue button
        """
        logger.info("Click continue button")
        self.click(self.BTN_CONTINUE)

        from pages.home_page import HomePage
        return HomePage(self.driver)