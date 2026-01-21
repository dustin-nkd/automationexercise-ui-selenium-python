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
    LBL_CART_TITLE = (By.XPATH, "//li[@class='active' and normalize-space()='Shopping Cart']")
    TABLE_CART = (By.ID, "cart_info_table")
    BTN_CHECKOUT = (By.XPATH, "//a[normalize-space()='Proceed To Checkout']")
    BTN_REGISTER_LOGIN = (By.XPATH, "//u[normalize-space()='Register / Login']")

    def _parse_price(self, text: str) -> int:
        return int(text.replace("Rs.", "").strip())

    # ---------- Dynamic Locators ----------

    def _quantity_of_item(self, name: str):
        return (
            By.XPATH,
            f"//h4/a[contains(text(),'{name}')]/ancestor::td[@class='cart_description']/following-sibling::td[@class='cart_quantity']/button"
        )

    def _btn_remove_by_item(self, name: str):
        return (
            By.XPATH,
            f"//a[contains(text(),'{name}')]/ancestor::td[@class='cart_description']/following-sibling::td[@class='cart_delete']//a"
        )

    def _cart_row_by_item(self, name: str):
        return (
            By.XPATH,
            f"//h4/a[normalize-space()='{name}']/ancestor::tr"
        )

    def _cart_item_names(self):
        return (
            By.CSS_SELECTOR,
            "td.cart_description h4 a"
        )

    # ---------- Getters ----------

    def get_cart_item_count(self) -> int:
        """
        Get number of products in cart
        """
        logger.info(f"Getting number of cart items")
        return len(self.find_all(self.ROW_CART_ITEMS))

    def get_quantity_of_item(self, name: str) -> str:
        """
        Get number of products in cart
        """
        logger.info(f"Getting number of product {name}")
        return self.get_text(self._quantity_of_item(name))

    def get_cart_product_names(self) -> list[str]:
        """
        Get all product names in cart
        """
        logger.info("Getting all product names in cart")
        elems = self.find_all(self._cart_item_names())
        return [elem.text.strip() for elem in elems if elem.text.strip()]

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

    def are_products_in_cart(self, expected_products: list[str]) -> bool:
        """
        Verify all expected products are present in cart
        """
        cart_products = self.get_cart_product_names()
        logger.info("Expected products: %s", expected_products)
        logger.info("Cart products: %s", cart_products)
        return all(
            product in cart_products
            for product in expected_products
        )

    # ---------- Visibility ----------

    def is_cart_page_visible(self) -> bool:
        """
        Verify if cart page is visible
        """
        logger.info("Verifying if cart page is visible")
        return self.is_displayed(self.LBL_CART_TITLE)

    def is_cart_table_visible(self) -> bool:
        """
        Verify if cart table is visible
        """
        logger.info("Verifying if cart table is visible")
        return self.is_displayed(self.TABLE_CART)

    def is_item_removed(self, name: str) -> bool:
        """
        Verify if item is removed
        """
        logger.info("Verifying if item is removed")
        return not self.is_present(self._cart_row_by_item(name))

    # ---------- Actions ----------

    def proceed_to_checkout(self):
        """
        Click proceed to checkout
        """
        logger.info("Proceed to checkout")
        self.click(self.BTN_CHECKOUT)

        from pages.checkout_page import CheckoutPage
        return CheckoutPage(self.driver)

    def click_register_login(self):
        """
        Click register login
        """
        logger.info("Click register login")
        self.click(self.BTN_REGISTER_LOGIN)

        from pages.login_page import LoginPage
        return LoginPage(self.driver)

    def remove_item(self, name: str) -> None:
        """
        Click remove item
        """
        logger.info("Click remove item")
        self.click(self._btn_remove_by_item(name))
        self.wait_until_not_present(self._cart_row_by_item(name))