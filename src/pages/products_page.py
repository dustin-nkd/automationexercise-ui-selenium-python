from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utilities.logger import get_logger

logger = get_logger(__name__)


class ProductsPage(BasePage):
    """
    Page Object for AutomationExcercise Products Page.
    Handles product litsting, searching, and adding products to cart.
    URL: https://automationpractice.com/products
    """

    # ---------- Static Locators ----------
    LBL_ALL_PRODUCTS_TITLE = (By.XPATH, "//h2[normalize-space()='All Products']")
    LST_PRODUCT_ITEMS = (By.XPATH, "//div[@class='single-products']")
    INPUT_SEARCH = (By.XPATH, "//input[@id='search_product']")
    BTN_SEARCH = (By.XPATH, "//button[@id='submit_search']")
    LBL_SEARCHED_PRODUCTS = (By.XPATH, "//h2[normalize-space()='Searched Products']")
    LBL_PRODUCT_NAMES = (By.CSS_SELECTOR, ".productinfo p")

    # ---------- Visibility Checks ----------

    def is_products_page_visible(self) -> bool:
        """Verifies if the 'All Products' page is successfully loaded."""
        logger.info("Verifying Products page visibility")
        return self.is_displayed(self.LBL_ALL_PRODUCTS_TITLE)

    def is_products_list_visible(self) -> bool:
        """Checks if the product grid container is displayed."""
        logger.info("Verifying Products list visibility")
        return self.is_displayed(self.LST_PRODUCT_ITEMS)

    def is_searched_products_visible(self) -> bool:
        """Verifies if the 'Searched Products' header is displayed after a search."""
        logger.info("Verifying Searched Products section visibility")
        return self.is_displayed(self.LBL_SEARCHED_PRODUCTS)

    # ---------- Dynamic Locator Generators ----------

    def _get_btn_view_product(self, item_name: str):
        """Generates locator for 'View Product' button based on product name."""
        return By.XPATH, f"//div[contains(@class,'product-image-wrapper')][.//p[normalize-space()='{item_name}']]//a[normalize-space()='View Product']"

    def _get_product_container(self, item_name: str):
        """Generates locator for the main product container box."""
        return By.XPATH, f"//p[contains(.,'{item_name}')]/parent::div[contains(@class ,'productinfo')]"

    def _get_btn_add_to_cart(self, item_name: str):
        """Generates locator for 'Add to Cart' button (usually in the hover overlay)."""
        return By.XPATH, f"//p[normalize-space()='{item_name}']/parent::div[@class='overlay-content']//a[contains(@class,'add-to-cart')]"

    # ---------- Search Actions ----------

    def search_product(self, product_name: str) -> None:
        """
        Performs a product search.
        :param product_name: The string to search for.
        """
        logger.info(f"Searching for product: {product_name}")
        self.send_keys(self.INPUT_SEARCH, product_name, clear_first=True)
        self.click(self.BTN_SEARCH)

    def get_displayed_product_names(self) -> list[str]:
        """Returns a list of all product names currently visible on the page."""
        logger.info("Retrieves all visible product names")
        elements = self.find_all(self.LBL_PRODUCT_NAMES)
        return [el.text.strip() for el in elements if el.text.strip()]

    def are_all_products_related_to_search(self, keyword: str) -> bool:
        """
        Validates that all displayed products contain search keyword.
        """
        logger.info(f"Validating search results for keyword: {keyword}")
        names = self.get_displayed_product_names()
        if not names:
            logger.warning("No products found to validate.")
            return False
        return all(keyword.lower() in name.lower() for name in names)

    # ---------- Navigation & Cart Actions ----------

    def click_view_product_of(self, item_name: str):
        """
        Navigates to the details page of a specific product.
        """
        logger.info(f"Navigating to details of: {item_name}")
        locator = self._get_btn_view_product(item_name)
        self.scroll_into_view(locator)
        self.click(locator)
        return self.navigate.product_details_page

    def add_product_to_cart(self, item_name: str) -> None:
        """
        Hovers over a product and clicks 'Add to Cart'.
        """
        logger.info(f"Adding '{item_name}' to cart")
        product_box = self._get_product_container(item_name)
        add_btn = self._get_btn_add_to_cart(item_name)

        self.scroll_into_view(product_box)
        self.hover(product_box)
        self.click(add_btn)

    def add_all_displayed_products_to_cart(self) -> None:
        """
        Iterates through all displayed products and adds them to cart.
        """
        logger.info("Adding all displayed products to cart")
        names = self.get_displayed_product_names()
        for i, name in enumerate(names):
            self.add_product_to_cart(name)
            # Use shared modal component via Navigator/Base context
            if i < len(names) - 1:
                self.add_to_cart_modal.click_continue_shopping()

    def click_view_cart(self):
        """
        Navigates to the Cart page via the success modal.
        """
        logger.info("Navigating to Cart page")
        self.add_to_cart_modal.click_view_cart()
        return self.navigate.cart_page

    def continue_shopping(self) -> None:
        """Clicks 'Continue Shopping' on the success modal."""
        logger.info("Continuing shopping flow")
        self.add_to_cart_modal.click_continue_shopping()
