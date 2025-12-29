from selenium.webdriver.common.by import By

from pages.base_page import BasePage, logger


class ProductsPage(BasePage):
    """
    Page Object for AutomationExcercise Products Page
    URL: https://automationpractice.com/products
    """

    LBL_ALL_PRODUCTS_TITLE = (By.XPATH, "//h2[normalize-space()='All Products']")
    LST_PRODUCT_ITEMS = (By.XPATH, "//div[@class='single-products']")

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

    # ---------- Dynamic Locators ----------

    def _btn_view_product(self, item: str):
        return (
            By.XPATH,
            f"//div[contains(@class,'product-image-wrapper')]"
            f"[.//p[normalize-space()='{item}']]"
            f"//a[normalize-space()='View Product']"
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