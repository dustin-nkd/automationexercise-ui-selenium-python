from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utilities.logger import get_logger

logger = get_logger(__name__)


class ProductDetailsPage(BasePage):
    """
    Page Object for AutomationExcercise Product Detail Page
    Handles detailed product information and review submission.
    """

    # ---------- Locators ----------
    PRODUCT_INFO_CONTAINER = (By.CLASS_NAME, "product-information")
    LBL_PRODUCT_NAME = (By.CSS_SELECTOR, ".product-information h2")
    LBL_CATEGORY = (By.XPATH, "//p[contains(text(),'Category')]")
    LBL_PRICE = (By.XPATH, "//span[contains(text(),'Rs.')]")
    LBL_AVAILABILITY = (By.XPATH, "//b[contains(text(),'Availability')]")
    LBL_CONDITION = (By.XPATH, "//b[normalize-space()='Condition:']")
    LBL_BRAND = (By.XPATH, "//b[normalize-space()='Brand:']")

    # Input & Buttons
    INPUT_QUANTITY = (By.ID, "quantity")
    BTN_ADD_TO_CART = (By.CSS_SELECTOR, "button.cart")

    # Review Section
    LBL_REVIEW_TITLE = (By.XPATH, "//a[normalize-space()='Write Your Review']")
    INPUT_REVIEW_NAME = (By.ID, "name")
    INPUT_REVIEW_EMAIL = (By.ID, "email")
    INPUT_REVIEW_CONTENT = (By.ID, "review")
    BTN_SUBMIT_REVIEW = (By.ID, "button-review")
    MSG_REVIEW_SUCCESS = (By.CSS_SELECTOR, ".alert-success span")

    # ---------- Visibility Checks ----------

    def is_product_details_page_visible(self) -> bool:
        """Verifies if the product details container is displayed."""
        logger.info("Verifying product detail page is visible")
        return self.is_displayed(self.PRODUCT_INFO_CONTAINER)

    def are_product_details_visible(self) -> bool:
        """
        Comprehensive check for all key product attributes.
        Used in Test 8 and 13
        """
        logger.info("Checking visibility of all product detail elements")
        elemets = [
            self.LBL_PRODUCT_NAME, self.LBL_CATEGORY, self.LBL_PRICE,
            self.LBL_AVAILABILITY, self.LBL_CONDITION, self.LBL_BRAND
        ]
        return all(self.is_displayed(loc) for loc in elemets)

    def is_review_section_visible(self) -> bool:
        """
        Check if the 'Write Your Review' section is displayed.
        """
        logger.info("Verifying review section visibility")
        self.scroll_into_view(self.LBL_REVIEW_TITLE)
        return self.is_displayed(self.LBL_REVIEW_TITLE)

    # ---------- Actions ----------

    def set_quantity(self, quantity: str) -> None:
        """Enters the desired quantity into the input field."""
        logger.info(f"Setting product quantity to: {quantity}")
        self.send_keys(self.INPUT_QUANTITY, quantity, clear_first=True)

    def click_add_to_cart(self) -> None:
        """
        Clicks the 'Add to cart' button.
        Triggers the AddToCartModal component.
        """
        logger.info("Clicking 'Add to cart' button")
        self.click(self.BTN_ADD_TO_CART)

    def submit_product_review(self, name: str, email: str, content: str) -> None:
        """
        Fills out and submits the product review form.
        """
        logger.info(f"Submitting review for user: {email}")
        self.send_keys(self.INPUT_REVIEW_NAME, name)
        self.send_keys(self.INPUT_REVIEW_EMAIL, email)
        self.send_keys(self.INPUT_REVIEW_CONTENT, content)
        self.click(self.BTN_SUBMIT_REVIEW)

    def enter_review_name(self, name: str):
        self.send_keys(self.INPUT_REVIEW_NAME, name)

    def enter_review_email(self, email: str):
        self.send_keys(self.INPUT_REVIEW_EMAIL, email)

    def enter_review_content(self, content: str):
        self.send_keys(self.INPUT_REVIEW_CONTENT, content)

    def click_submit(self):
        logger.info("Clicking Submit Review button")
        self.click(self.BTN_SUBMIT_REVIEW)

    # ---------- Navigation & Combined Actions ----------

    def add_to_cart_and_view_cart(self):
        """
        Combined action: Adds to cart and navigates directly to Cart page via the modal component.
        """
        self.click_add_to_cart()
        return self.add_to_cart_modal.click_view_cart()

    def navigate_to_cart_via_modal(self):
        self.add_to_cart_modal.click_view_cart()
        return self.navigate.cart_page

    # ---------- Getters ----------

    def get_review_success_message(self) -> str:
        """Retrieves the success message text after submitting a review."""
        return self.get_text(self.MSG_REVIEW_SUCCESS)
