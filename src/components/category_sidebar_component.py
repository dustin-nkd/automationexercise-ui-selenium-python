from selenium.webdriver.common.by import By

from utilities.logger import get_logger

logger = get_logger(__name__)


class CategorySidebarComponent:
    """
    Left sidebar category component
    """

    def __init__(self, base_page):
        self.base = base_page

    CATEGORY_LST = (By.XPATH, "//div[@id='accordian']")
    LBL_CATEGORY_TITLE = (By.XPATH, "//h2[@class='title text-center']")

    # ---------- Dynamic Locators ----------

    def _category(self, name: str):
        return (
            By.XPATH,
            f"//a[normalize-space()='{name}']"
        )

    def _sub_category(self, name: str):
        return (
            By.XPATH,
            f"//a[normalize-space()='{name}']"
        )

    # ---------- Visibility ----------

    def is_visible(self) -> bool:
        """
        Verifies if the sidebar is visible
        """
        logger.info(f"Checking if sidebar is visible")
        return self.base.is_displayed(self.CATEGORY_LST)

    def is_category_page_for(self, category: str, sub_category: str) -> bool:
        """
        Verifies if the sidebar category is in the sidebar component
        """
        logger.info(f"Checking if sidebar category is in sidebar component")
        expected = f"{category.upper()} - {sub_category.upper()} PRODUCTS"
        actual = self.get_category_title()
        return expected in actual

    # ---------- Actions ----------

    def expand_category(self, category: str) -> None:
        """
        Expands the sidebar category component
        """
        logger.info("Expanding sidebar category %s", category)
        self.base.click(self._category(category))

    def click_sub_category(self, sub_category: str) -> None:
        """
        Clicks the sidebar sub category component
        """
        logger.info("Clicking sub category %s", sub_category)
        self.base.click(self._sub_category(sub_category))

    # ---------- Getters ----------

    def get_category_title(self) -> str:
        """
        Returns the title of the sidebar category
        """
        logger.info("Getting title of sidebar category")
        return self.base.get_text(self.LBL_CATEGORY_TITLE)