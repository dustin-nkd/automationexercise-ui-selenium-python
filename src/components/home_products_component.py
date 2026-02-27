from selenium.webdriver.common.by import By

from utilities.logger import get_logger

logger = get_logger(__name__)


class HomeProductsComponent:
    """
    Reusable Product component representing the product lists and recommened carousel.
    """

    LBL_RECOMMENDED_TITLE = (By.XPATH, "//h2[normalize-space()='recommended items']")
    PRODUCT_CARDS = (By.CLASS_NAME, "product-image-wrapper")
    RECOMMENDED_ITEMS_SECTION = (By.CSS_SELECTOR, ".recommended_items")

    def __init__(self, base_page):
        self.base = base_page

    # ---------- Dynamic Locators ----------

    def _get_product_container(self, name: str):
        # Locator for the whole product card to hover
        return By.XPATH, f"//div[@class='single-products'][.//p[normalize-space()='{name}']]"

    def _get_view_product_btn(self, name: str):
        # Locator for 'View Product' link based on name
        return f"//div[@class='product-image-wrapper'][.//p[normalize-space()='{name}']]//a[contains(text(),'View Product')]"

    def _get_add_to_cart_overlay_btn(self, name: str):
        # Locator for 'Add to cart' inside the hover overlay
        return f"//div[@class='overlay-content'][.//p[normalize-space()='{name}']]//a[contains(@class,'add-to-cart')]"

    def _get_recommended_add_btn(self, name: str):
        # Locator for 'Add to cart' in the Recommended Carousel section
        return By.XPATH, f"//div[@id='recommended-item-carousel']//p[text()='{name}']/following-sibling::a"

    # ---------- Visibility ----------

    def is_recommended_itemes_visible(self) -> bool:
        """Verifies if the 'recommended items' section title is displayed."""
        logger.info("Verifying recommended items visibility")
        return self.base.is_displayed(self.LBL_RECOMMENDED_TITLE)

    # ---------- Actions ----------

    def click_view_product_of(self, name: str):
        """
        Clicks on 'View Product' and returns ProductDetailsPage instance.
        """
        logger.info(f"Navigating to details for product: {name}")
        locator = self._get_view_product_btn(name)
        self.base.scroll_into_view(locator)
        self.base.click(locator)

    def add_product_to_cart(self, name: str) -> None:
        """
        Standard product add: Scrolled -> Hover -> Click 'Add to cart' in overlay.
        """
        logger.info(f"Adding standard product to cart: {name}")
        container = self._get_product_container(name)
        add_btn = self._get_add_to_cart_overlay_btn(name)

        self.base.scroll_into_view(container)
        self.base.hover(container)
        self.base.click(add_btn)

    def add_recommended_item_to_cart(self, name: str) -> None:
        """
        Adds item from the Recommended carousel section.
        """
        logger.info(f"Adding recommended product to cart: {name}")
        locator = self._get_recommended_add_btn(name)
        self.scroll_to_recommended_item()
        self.base.click(locator)

    def scroll_to_recommended_item(self) -> None:
        logger.info("Scrolling to Recommended Items section")
        self.base.scroll_into_view(self.RECOMMENDED_ITEMS_SECTION)
