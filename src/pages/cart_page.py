from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utilities.logger import get_logger

logger = get_logger(__name__)


class CartPage(BasePage):
    """
    Page Object for AutomationExcercise Cart Page
    URL: https://automationpractice.com/view_cart
    """

    ROW_CART_ITEMS = (By.CSS_SELECTOR, "td.cart_product")
    PRICE_BY_INDEX = lambda self, i: (By.XPATH, f"(//td[@class='cart_price'])[{i}]")
    QUANTITY_BY_INDEX = lambda self, i: (By.XPATH, f"(//td[@class='cart_quantity']/button)[{i}]")
    TOTAL_BY_INDEX = lambda self, i: (By.XPATH, f"(//td[@class='cart_total'])[{i}]")

    def _parse_price(self, text: str) -> int:
        return int(text.replace("Rs.", "").strip())

    # ---------- Getters ----------

    def get_cart_item_count(self) -> int:
        """
        Get number of products in cart
        """
        logger.info(f"Getting number of cart items")
        return len(self.find_all(self.ROW_CART_ITEMS))

    # ---------- Verifications ----------

    def verify_product_price_quantity_total(self, index: int) -> bool:
        """
        Verify price, quantity and total price for a product row
        """
        price = self._parse_price(self.get_text(self.PRICE_BY_INDEX(index)))
        total = self._parse_price(self.get_text(self.TOTAL_BY_INDEX(index)))
        quantity = int(self.get_text(self.QUANTITY_BY_INDEX(index)))
        return total == quantity * price

    def are_all_cart_items_price_quantity_correct(self) -> bool:
        """
        Verify price == quantity * total for all cart items\
        """
        return all(self.verify_product_price_quantity_total(i)
                   for i in range(1, self.get_cart_item_count() + 1)
                   )