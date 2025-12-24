from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utilities.logger import get_logger

logger = get_logger(__name__)


class LoginPage(BasePage):
    """
    Page Object for AutomationExcercise Sign Up and Login Page
    URL: https://automationpractice.com/login
    """

    LBL_NEW_USER_SIGNUP = (By.CSS_SELECTOR, "div[class='signup-form'] h2")
    INPUT_NAME = (By.CSS_SELECTOR, "input[placeholder='Name']")
    INPUT_EMAIL = (By.CSS_SELECTOR, "input[data-qa='signup-email']")
    BTN_SIGNUP = (By.CSS_SELECTOR, "button[data-qa='signup-button']")
    LBL_LOGIN_TO_YOUR_ACCOUNT = (By.CSS_SELECTOR, "div[class='login-form'] h2")
    INPUT_EMAIL_ADDRESS = (By.CSS_SELECTOR, "input[data-qa='login-email']")
    INPUT_PASSWORD = (By.CSS_SELECTOR, "input[placeholder='Password']")
    BTN_LOGIN = (By.CSS_SELECTOR, "button[data-qa='login-button']")
    MSG_LOGIN_ERROR = (By.XPATH, "//p[contains(text(),'Your email or password is incorrect!')]")

    def get_new_user_signup_message(self) -> str:
        """
        Get new user signup message
        """
        logger.info("Getting new user signup message")
        return self.get_text(self.LBL_NEW_USER_SIGNUP)

    def enter_name(self, name: str) -> None:
        """
        Enter the name of the user
        """
        logger.info("Entering Name: %s", name)
        self.send_keys(self.INPUT_NAME, name)

    def enter_signup_email(self, email: str) -> None:
        """
        Enter the email of the user
        """
        logger.info("Entering Email: %s", email)
        self.send_keys(self.INPUT_EMAIL, email)

    def click_signup(self):
        """
        Click signup button
        """
        logger.info("Clicking signup button")
        self.click(self.BTN_SIGNUP)

        from pages.signup_page import SignUpPage
        return SignUpPage(self.driver)

    def get_login_to_your_account_message(self) -> str:
        """
        Get login to your account message
        """
        logger.info("Getting login to your account message")
        return self.get_text(self.LBL_LOGIN_TO_YOUR_ACCOUNT)

    def enter_login_email(self, email: str) -> None:
        """
        Enter the email address of the user
        """
        logger.info("Entering email address: %s", email)
        self.send_keys(self.INPUT_EMAIL_ADDRESS, email)

    def enter_password(self, password: str) -> None:
        """
        Enter the password of the user
        """
        logger.info("Entering password: %s", password)
        self.send_keys(self.INPUT_PASSWORD, password)

    def click_login(self):
        """
        Click login button
        """
        logger.info("Clicking login button")
        self.click(self.BTN_LOGIN)

        from pages.home_page import HomePage
        return HomePage(self.driver)

    def get_your_email_or_password_is_incorrect_message(self) -> str:
        """
        Get your email or password is incorrect message
        """
        logger.info("Getting your email or password is incorrect message")
        return self.get_text(self.MSG_LOGIN_ERROR)