from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.signup_page import SignUpPage
from utilities.logger import get_logger

logger = get_logger(__name__)


class LoginPage(BasePage):
    """
    Page Object for AutomationExcercise Sign Up and Login Page
    URL: https://automationpractice.com/login
    """
    LABEL_NEW_USER_SIGNUP = (By.CSS_SELECTOR, "div[class='signup-form'] h2")
    INPUT_NAME = (By.CSS_SELECTOR, "input[placeholder='Name']")
    INPUT_EMAIL = (By.CSS_SELECTOR, "input[data-qa='signup-email']")
    BTN_SIGNUP = (By.CSS_SELECTOR, "button[data-qa='signup-button']")

    def get_new_user_signup_message(self) -> str:
        """
        Get new user signup message
        """
        logger.info("Getting new user signup message")
        return self.get_text(self.LABEL_NEW_USER_SIGNUP)

    def enter_name(self, name: str) -> None:
        """
        Enter the name of the user
        """
        logger.info("Entering Name: %s", name)
        self.send_keys(self.INPUT_NAME, name)

    def enter_email(self, email: str) -> None:
        """
        Enter the email of the user
        """
        logger.info("Entering Email: %s", email)
        self.send_keys(self.INPUT_EMAIL, email)

    def click_signup(self) -> SignUpPage:
        """
        Click signup button
        """
        logger.info("Clicking signup button")
        self.click(self.BTN_SIGNUP)
        return SignUpPage(self.driver)