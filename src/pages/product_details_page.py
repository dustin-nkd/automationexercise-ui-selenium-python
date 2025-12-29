from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utilities.logger import get_logger

logger = get_logger(__name__)


class ProductDetailsPage(BasePage):
    """
    Page Object for AutomationExcercise Product Detail Page
    URL: https://automationpractice.com/product_details
    """

    PRODUCT_INFORMATION_CONTAINER = (By.XPATH, "//div[@class='product-information']")

    LBL_PRODUCT_NAME = (By.CSS_SELECTOR, "div[class='product-information'] h2")
    LBL_CATEGORY = (By.XPATH, "//p[contains(text(),'Category')]")
    LBL_PRICE = (By.XPATH, "//span[contains(text(),'Rs.')]")
    LBL_AVAILABILITY = (By.XPATH, "//b[contains(text(),'Availability')]")
    LBL_CONDITION = (By.XPATH, "//b[normalize-space()='Condition:']")
    LBL_BRAND = (By.XPATH, "//b[normalize-space()='Brand:']")

    def is_product_details_page_visible(self) -> bool:
        """
        Verify product detail page is visible
        """
        logger.info("Verifying product detail page is visible")
        return self.is_displayed(self.PRODUCT_INFORMATION_CONTAINER)

    def is_product_name_visible(self) -> bool:
        """
        Verify product name is visible
        """
        logger.info("Verifying product name is visible")
        return self.is_displayed(self.LBL_PRODUCT_NAME)

    def is_product_category_visible(self) -> bool:
        """
        Verify product category is visible
        """
        logger.info("Verifying product category is visible")
        return self.is_displayed(self.LBL_CATEGORY)

    def is_product_price_visible(self) -> bool:
        """
        Verify product price is visible
        """
        logger.info("Verifying product price is visible")
        return self.is_displayed(self.LBL_PRICE)

    def is_product_availability_visible(self) -> bool:
        """
        Verify product availability is visible
        """
        logger.info("Verifying product availability is visible")
        return self.is_displayed(self.LBL_AVAILABILITY)

    def is_product_condition_visible(self) -> bool:
        """
        Verify product condition is visible
        """
        logger.info("Verifying product condition is visible")
        return self.is_displayed(self.LBL_CONDITION)

    def is_product_brand_visible(self) -> bool:
        """
        Verify product brand is visible
        """
        logger.info("Verifying product brand is visible")
        return self.is_displayed(self.LBL_BRAND)

    def are_product_details_visible(self) -> bool:
        """
        Verify product details are visible
        """
        logger.info("Verifying product details are visible")
        return all([
            self.is_product_name_visible(),
            self.is_product_category_visible(),
            self.is_product_price_visible(),
            self.is_product_availability_visible(),
            self.is_product_condition_visible(),
            self.is_product_brand_visible()
        ])