from selenium.webdriver.common.by import By

from pages.base_page import BasePage, logger


class ProductsPage(BasePage):
    """
    Page Object for AutomationExcercise Products Page
    URL: https://automationpractice.com/products
    """

    LBL_ALL_PRODUCTS_TITLE = (By.XPATH, "//h2[normalize-space()='All Products']")
    LST_PRODUCT_ITEMS = (By.XPATH, "//div[@class='single-products']")
    INPUT_SEARCH = (By.XPATH, "//input[@id='search_product']")
    BTN_SEARCH = (By.XPATH, "//button[@id='submit_search']")
    LBL_SEARCHED_PRODUCTS = (By.XPATH, "//h2[normalize-space()='Searched Products']")
    LBL_PRODUCT_NAMES = (By.CSS_SELECTOR, ".productinfo p")
    BTN_CONTINUE_SHOPPING = (By.XPATH, "//button[normalize-space()='Continue Shopping']")
    BTN_VIEW_CART = (By.XPATH, "//u[normalize-space()='View Cart']")

    # ---------- Visibility ----------

    def is_products_page_visible(self) -> bool:
        """
        Verify Products page is visible
        """
        logger.info("Verifying Products page is visible")
        return self.is_displayed(self.LBL_ALL_PRODUCTS_TITLE)

    def is_products_list_visible(self) -> bool:
        """
        Verify Products list is visible
        """
        logger.info("Verifying Products list is visible")
        return self.is_displayed(self.LST_PRODUCT_ITEMS)

    def is_searched_products_visible(self) -> bool:
        """
        Verify Searched products list is visible
        """
        logger.info("Verifying Searched products list is visible")
        return self.is_displayed(self.LBL_SEARCHED_PRODUCTS)

    def are_all_products_related_to_search(self, keyword: str) -> bool:
        """
        Verify all products related to search
        """
        logger.info("Verifying all products related to search: %s", keyword)
        product_names = self.get_displayed_product_names()
        if not product_names:
            logger.warning("No products displayed after search")
            return False
        keyword_lower = keyword.lower()
        return all(keyword_lower in name.lower() for name in product_names)

    # ---------- Dynamic Locators ----------

    def _btn_view_product(self, item: str):
        return (
            By.XPATH,
            f"//div[contains(@class,'product-image-wrapper')]"
            f"[.//p[normalize-space()='{item}']]"
            f"//a[normalize-space()='View Product']"
        )

    def _product(self, item: str):
        return (
            By.XPATH,
            f"//p[contains(.,'{item}')]/parent::div[contains(@class ,'productinfo')]"
        )

    def _btn_add_to_cart_by_item(self, item: str):
        return (
            By.XPATH,
            f"//p[normalize-space()='{item}']/parent::div[@class='overlay-content']//a[contains(@class,'add-to-cart')]"
        )

    # ---------- Actions / Navigation ----------

    def click_view_product_of(self, item: str):
        """
        Click view product of item
        """
        logger.info("Clicking view product of item")
        self.scroll_into_view(self._btn_view_product(item))
        self.click(self._btn_view_product(item))

        from pages.product_details_page import ProductDetailsPage
        return ProductDetailsPage(self.driver)

    def search(self, product: str) -> None:
        """
        Search product
        """
        logger.info("Searching product: %s", product)
        self.send_keys(self.INPUT_SEARCH, product, clear_first=True)
        self.click(self.BTN_SEARCH)

    def get_displayed_product_names(self) -> list[str]:
        """
        Get all displayed product names
        """
        logger.info("Getting all displayed product names")
        elems = self.find_all(self.LBL_PRODUCT_NAMES)
        return [elem.text.strip() for elem in elems if elem.text.strip()]

    def add_product_to_cart_by_item(self, item: str) -> None:
        """
        Hover over product and click Add to cart
        """
        logger.info("Adding product %s to cart", item)
        self.scroll_into_view(self._product(item))
        self.hover(self._product(item))
        self.click(self._btn_add_to_cart_by_item(item))

    def click_continue_shopping(self) -> None:
        """
        Click Continue Shopping
        """
        logger.info("Continue Shopping")
        self.click(self.BTN_CONTINUE_SHOPPING)

    def click_view_cart(self):
        """
        Click view cart
        """
        logger.info("Clicking view cart")
        self.click(self.BTN_VIEW_CART)

        from pages.cart_page import CartPage
        return CartPage(self.driver)