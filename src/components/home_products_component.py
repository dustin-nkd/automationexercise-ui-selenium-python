from selenium.webdriver.common.by import By

from utilities.logger import get_logger

logger = get_logger(__name__)


class HomeProductsComponent:
    """
    Reusable Product component shared across pages
    """

    def __init__(self, base_page):
        self.base = base_page

    LBL_RECOMMENDED_ITEMS = (By.XPATH, "//h2[normalize-space()='recommended items']")

    # ---------- Dynamic Locators ----------

    def _product(self, name: str):
        return (
            By.XPATH,
            f"//p[normalize-space()='{name}']/parent::div[contains(@class,'productinfo')]"
        )

    def _btn_view_product(self, name: str):
        return (
            By.XPATH,
            f"//div[contains(@class,'product-image-wrapper')]"
            f"[.//p[normalize-space()='{name}']]"
            f"//a[normalize-space()='View Product']"
        )

    def _btn_add_to_cart_by_item(self, item: str):
        return (
            By.XPATH,
            f"//p[normalize-space()='{item}']/parent::div[@class='overlay-content']//a[contains(@class,'add-to-cart')]"
        )

    def _btn_add_to_cart_recommended_item(self, name: str):
        return (
            By.XPATH,
            f"//div[@class='recommended_items']//div[@class='single-products']//p[contains(text(),'{name}')]/following-sibling::a[contains(.,'Add to cart')]"
        )

    # ---------- Actions ----------

    def click_view_product_of(self, name: str):
        """
        Click view product of item
        """
        logger.info("Clicking view product of item")
        self.base.scroll_into_view(self._btn_view_product(name))
        self.base.click(self._btn_view_product(name))

    def add_product_to_cart_by_item(self, item: str) -> None:
        """
        Hover over product and click Add to cart
        """
        logger.info("Adding product %s to cart", item)
        self.base.scroll_into_view(self._product(item))
        self.base.hover(self._product(item))
        self.base.click(self._btn_add_to_cart_by_item(item))

    def add_recommended_item_to_cart(self, item: str) -> None:
        """
        Scroll to item and click Add to cart
        """
        logger.info("Scrolling to item %s", item)
        self.base.scroll_into_view(self._btn_add_to_cart_recommended_item(item))
        self.base.click(self._btn_add_to_cart_recommended_item(item))

    def is_recommened_itemes_visible(self) -> bool:
        """
        Verify if recommended items are visible
        """
        logger.info("Verifying if recommended items are visible")
        return self.base.is_displayed(self.LBL_RECOMMENDED_ITEMS)