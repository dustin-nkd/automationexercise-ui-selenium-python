from selenium.webdriver.common.by import By

from utilities.logger import get_logger

logger = get_logger(__name__)


class CategorySidebarComponent:
    """
    Left sidebar component for Categories and Brands navigation.
    """

    SIDEBAR_CONTAINER = (By.ID, "accordian")
    LBL_CATEGORY_TITLE = (By.CSS_SELECTOR, ".features_items .title")
    BRANDS_CONTAINER = (By.CLASS_NAME, "brands_products")

    def __init__(self, base_page):
        self.base = base_page

    # ---------- Dynamic Locators ----------

    def _get_category_locator(self, name: str):
        # Finds the main category (Women, Men, Kids)
        return By.XPATH, f"//a[@data-toggle='collapse'][contains(.,'{name}')]"

    def _get_sub_category_locator(self, name: str):
        # Finds the sub-category link (Dress, Tops, Jeans, etc.)
        return By.XPATH, f"//div[@id='accordian']//a[normalize-space()='{name}']"

    # ---------- Visibility ----------

    def is_sidebar_visible(self) -> bool:
        logger.info("Checking if category sidebar is visible")
        return self.base.is_displayed(self.SIDEBAR_CONTAINER)

    # ---------- Actions ----------

    def expand_category(self, category_name: str) -> None:
        """Expands a main category like 'Women' or 'Men'."""
        logger.info(f"Expanding category: {category_name}")
        locator = self._get_category_locator(category_name)
        self.base.scroll_into_view(locator)
        self.base.click(locator)

    def click_sub_category(self, sub_category_name: str) -> None:
        """Clicks on a sub-category link."""
        logger.info(f"Clicking sub-category: {sub_category_name}")
        locator = self._get_sub_category_locator(sub_category_name)
        self.base.click(locator)

    # ---------- Getters ----------

    def get_category_title(self) -> str:
        """Returns the heading text of the filtered products page."""
        logger.info("Getting filtered category title text")
        self.base.wait_until_present(self.LBL_CATEGORY_TITLE)
        return self.base.get_text(self.LBL_CATEGORY_TITLE)
