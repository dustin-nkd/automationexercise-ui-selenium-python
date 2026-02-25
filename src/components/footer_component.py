from selenium.webdriver.common.by import By

from utilities.logger import get_logger

logger = get_logger(__name__)


class FooterComponent:
    """
    Reusable Footer component shared across multiple pages.
    """

    # ---------- Locators ----------
    LBL_SUBSCRIPTION = (By.XPATH, "//h2[normalize-space()='Subscription']")
    INPUT_EMAIL = (By.ID, "susbscribe_email")
    BTN_SUBSCRIBE = (By.ID, "subscribe")
    LBL_SUCCESS_MSG = (By.CSS_SELECTOR, ".alert-success")

    def __init__(self, base_page):
        self.base = base_page

    # ---------- Visibility ----------

    def is_subscription_label_visible(self) -> bool:
        """
        Scrolls to footer and verifies if the 'SUBSCRIPTION' title is visible.
        """
        logger.info("Verifying SUBSCRIPTION label visibility")
        self.base.scroll_into_view(self.LBL_SUBSCRIPTION)
        return self.base.is_displayed(self.LBL_SUBSCRIPTION)

    def is_success_message_visible(self) -> bool:
        """
        Checks ifthe subscription success message is displayed.
        """
        logger.info("Verifying subcription success message visibility")
        return self.base.is_displayed(self.LBL_SUCCESS_MSG)

    def get_success_message_text(self) -> str:
        """
        Returns the text of the success message.
        """
        return self.base.get_text(self.LBL_SUCCESS_MSG)

    # ---------- Actions ----------

    def subscribe(self, email: str) -> None:
        """
        Performs the subscription flow: enters email and clicks the arrow button.
        """
        logger.info(f"Subscribing to newsletter with email {email}")
        self.base.send_keys(self.INPUT_EMAIL, email, clear_first=True)
        self.base.click(self.BTN_SUBSCRIBE)

    def scroll_to_footer(self) -> None:
        """
        Scrolls down to footer.
        """
        logger.info("Scrolling down to footer area")
        self.base.scroll_into_view(self.LBL_SUBSCRIPTION)
