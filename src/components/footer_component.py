from selenium.webdriver.common.by import By

from utilities.logger import get_logger

logger = get_logger(__name__)


class FooterComponent:
    """
    Reusable Footer component shared across pages
    """

    LBL_SUBCRIPTION = (By.XPATH, "//h2[normalize-space()='Subscription']")
    INPUT_EMAIL = (By.XPATH, "//input[@id='susbscribe_email']")
    BTN_SUBSCRIBE = (By.XPATH, "//button[@id='subscribe']")
    MSG_SUCCESS = (By.XPATH, "//input[@id='susbscribe_email']")

    def __init__(self, base_page):
        self.base = base_page

    # ---------- Visibility ----------

    def is_subscription_visible(self) -> bool:
        """
        Verify SUBCRTIPTION title is visible
        """
        logger.info("Verifying SUBCRIPTION title is visible")
        self.base.scroll_into_view(self.LBL_SUBCRIPTION)
        return self.base.is_displayed(self.LBL_SUBCRIPTION)

    def is_success_message_visible(self) -> bool:
        """
        Verify subcription success message is visible
        """
        logger.info("Verifying subcription success message is visible")
        return self.base.is_displayed(self.MSG_SUCCESS)

    # ---------- Actions ----------

    def subscribe(self, email: str) -> None:
        """
        Subscribe with email
        """
        logger.info("Subscribing with email: %s", email)
        self.base.send_keys(self.INPUT_EMAIL, email, clear_first=True)
        self.base.click(self.BTN_SUBSCRIBE)