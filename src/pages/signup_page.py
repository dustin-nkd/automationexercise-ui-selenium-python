from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utilities.logger import get_logger

logger = get_logger(__name__)


class SignUpPage(BasePage):
    """
    Page Object for AutomationExcercise Sign Up Information Page.
    Handles the detailed registration form.
    """

    # ---------- Locators ----------
    LBL_ENTER_ACCOUNT_INFORMATION = (By.XPATH, "//b[normalize-space()='Enter Account Information']")

    # Title
    RAD_TITLE_MR = (By.XPATH, "//input[@id='id_gender1']")
    RAD_TITLE_MRS = (By.XPATH, "//input[@id='id_gender2']")

    # Account info
    INPUT_NAME = (By.XPATH, "//input[@id='name']")
    INPUT_PASSWORD = (By.XPATH, "//input[@id='password']")

    # Date of Birth
    DDL_DAY = (By.XPATH, "//select[@id='days']")
    DDL_MONTH = (By.XPATH, "//select[@id='months']")
    DDL_YEAR = (By.XPATH, "//select[@id='years']")

    # Preferences
    CHK_NEWSLETTER = (By.XPATH, "//input[@id='newsletter']")
    CHK_OFFERS = (By.XPATH, "//input[@id='optin']")

    # Address & Contact
    INPUT_FIRST_NAME = (By.XPATH, "//input[@id='first_name']")
    INPUT_LAST_NAME = (By.XPATH, "//input[@id='last_name']")
    INPUT_COMPANY = (By.XPATH, "//input[@id='company']")
    INPUT_ADDRESS = (By.XPATH, "//input[@id='address1']")
    INPUT_ADDRESS2 = (By.XPATH, "//input[@id='address2']")
    DDL_COUNTRY = (By.XPATH, "//select[@id='country']")
    INPUT_STATE = (By.XPATH, "//input[@id='state']")
    INPUT_CITY = (By.XPATH, "//input[@id='city']")
    INPUT_ZIPCODE = (By.XPATH, "//input[@id='zipcode']")
    INPUT_MOBILE_NUMBER = (By.XPATH, "//input[@id='mobile_number']")

    BTN_CREATE_ACCOUNT = (By.XPATH, "//button[contains(text(),'Create Account')]")

    # ---------- Verification ----------

    def get_enter_account_information_message(self) -> str:
        """
        Retrives the 'Enter Account Information' header text.
        """
        logger.info("Getting 'Enter Account Information' header text")
        return self.get_text(self.LBL_ENTER_ACCOUNT_INFORMATION)

    # ---------- Individual Actions ----------

    def select_title(self, title: str) -> None:
        """
        Selects the gender based on the provided string (Mr/Mrs).
        """
        logger.info(f"Selecting title: {title}")
        if title.lower() == "mr":
            self.click(self.RAD_TITLE_MR)
        elif title.lower() in ["mrs", "ms"]:
            self.click(self.RAD_TITLE_MRS)
        else:
            raise ValueError(f"Invalid title provided: {title}")

    def enter_name(self, name: str) -> None:
        """
        Enters the user's name.
        """
        logger.info(f"Entering name: {name}")
        self.send_keys(self.INPUT_NAME, name)

    def enter_password(self, password: str) -> None:
        """
        Enters the user's password.
        """
        logger.info("Entering password")
        self.send_keys(self.INPUT_PASSWORD, password)

    def select_date_of_birth(self, day: str, month: str, year: str) -> None:
        """
        Selects the full date of birth from dropdowns.
        """
        logger.info(f"Selecting DOB: {day}/{month}/{year}")
        self.select_dropdown_by_value(self.DDL_DAY, day)
        self.select_dropdown_by_value(self.DDL_MONTH, month)
        self.select_dropdown_by_value(self.DDL_YEAR, year)

    def select_newsletter(self) -> None:
        """
        Checks the newsletter subscription checkbox if not already selected.
        """
        logger.info("Selecting newsletter checkbox")
        if not self.is_selected(self.CHK_NEWSLETTER):
            self.click(self.CHK_NEWSLETTER)

    def select_offers(self) -> None:
        """
        Checks the special offers checkbox if not already selected.
        """
        logger.info("Selecting special offers checkbox")
        if not self.is_selected(self.CHK_OFFERS):
            self.click(self.CHK_OFFERS)

    def select_country(self, country: str) -> None:
        """
        Selects the country from the dropdown.
        """
        logger.info(f"Selecting country: {country}")
        self.select_dropdown_by_value(self.DDL_COUNTRY, country)

    def fill_address_details(self, personal_info: dict, address_info: dict, contact_info: dict) -> None:
        """
        Helper method to fill all address and contact related fields.
        """
        logger.info("Filling address and contact information")
        self.send_keys(self.INPUT_FIRST_NAME, personal_info["first_name"])
        self.send_keys(self.INPUT_LAST_NAME, personal_info["last_name"])
        self.send_keys(self.INPUT_COMPANY, personal_info["company"])
        self.send_keys(self.INPUT_ADDRESS, address_info["address1"])
        self.send_keys(self.INPUT_ADDRESS2, address_info["address2"])
        self.select_country(address_info["country"])
        self.send_keys(self.INPUT_STATE, address_info["state"])
        self.send_keys(self.INPUT_CITY, address_info["city"])
        self.send_keys(self.INPUT_ZIPCODE, address_info["zipcode"])
        self.send_keys(self.INPUT_MOBILE_NUMBER, contact_info["mobile_number"])

    def click_create_account(self):
        """
        Clicks the 'Create Account' button and returns the AccountCreatedPage.
        """
        logger.info("Clicking 'Create Account' button")
        self.click(self.BTN_CREATE_ACCOUNT)
        return self.navigate.account_created_page

    # ---------- Combined Business Logic ----------

    def create_account(self, user_profile: dict, subscribe_newsletter: bool = False, receive_offers: bool = False):
        """
        Comprehensive method to fill the entire signup and submit.
        Returns the AccountCreatedPage instance via Navigator.
        """
        logger.info("Performing full content account creation flow")

        # 1. Title, Name, Password
        self.select_title(user_profile["title"])
        # Name is usually autofilled from previous step, but we can re-render if needed
        self.enter_name(user_profile["name"])
        self.enter_password(user_profile["password"])

        # 2. Date of Birth
        dob = user_profile["date_of_birth"]
        self.select_date_of_birth(dob["day"], dob["month"], dob["year"])

        # 3. Optional Checkboxes
        if subscribe_newsletter:
            self.select_newsletter()
        if receive_offers:
            self.select_offers()

        # 4. Address & Contact
        self.fill_address_details(
            personal_info=user_profile["personal_info"],
            address_info=user_profile["address"],
            contact_info=user_profile["contact"]
        )

        # 5. Submit and return next page context
        return self.click_create_account()
