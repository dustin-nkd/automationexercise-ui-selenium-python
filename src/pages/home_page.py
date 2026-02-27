from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utilities.logger import get_logger

logger = get_logger(__name__)


class HomePage(BasePage):
    """
    Page Object for AutomationExcercise Home Page
    """

    # ---------- Locators ----------
    def _get_view_product_btn(self, product_name: str):
        return By.XPATH, f"//div[@class='features_items']//p[text()='{product_name}']/ancestor::div[@class='product-image-wrapper']//a[text()='View Product']"

    # ---------- Verifications ----------

    def is_home_page_visible(self) -> bool:
        logger.info("Verifying Home Page visibility via header")
        return self.header.is_header_visible()

    def is_logged_user_visible(self) -> bool:
        return self.header.is_logged_user_visible()

    # ---------- Actions / Navigation ----------
    def view_product(self, product_name: str):
        """
        Clicks on 'View Product' for a specific product on the Home Page.
        """
        logger.info(f"Viewing product details for {product_name} from Home Page")
        locator = self._get_view_product_btn(product_name)
        self.scroll_into_view(locator)
        self.click(locator)
        return self.navigate.product_details_page

    def delete_account(self):
        logger.info("Deleting account via header")
        self.header.click_delete_account()
        return self.navigate.account_deleted_page

    def logout(self):
        logger.info("Logging out via header")
        self.header.click_logout()
        return self.navigate.login_page

    def navigate_to_cart_via_modal(self):
        self.add_to_cart_modal.click_view_cart()
        return self.navigate.cart_page
