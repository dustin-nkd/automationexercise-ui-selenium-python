from selenium.webdriver.common.by import By

from utilities.logger import get_logger

logger = get_logger(__name__)


class AddToCartComponent:
    """
    Modal displayed after adding product to cart
    """

    MODAL_CONTAINER = (By.CSS_SELECTOR, ".modal-content")
    BTN_CONTINUE_SHOPPING = (By.XPATH, "//button[normalize-space()='Continue Shopping']")
    BTN_VIEW_CART = (By.XPATH, "//u[normalize-space()='View Cart']")

    def __init__(self, base_page):
        self.base = base_page

    # ---------- Visibility ----------

    def is_visible(self) -> bool:
        """
        Checks if the modal displayed after adding product to cart is visible
        """
        logger.info("Checking Add to Cart modal visibility")
        return self.base.is_displayed(self.MODAL_CONTAINER)

    # ---------- Actions ----------

    def click_continue_shopping(self) -> None:
        """
        Click Continue Shopping
        """
        logger.info("Continue Shopping")
        self.base.click(self.BTN_CONTINUE_SHOPPING)

    def click_view_cart(self) -> None:
        """
        Click view cart
        """
        logger.info("Clicking view cart")
        self.base.click(self.BTN_VIEW_CART)