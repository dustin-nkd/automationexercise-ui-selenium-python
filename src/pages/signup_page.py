from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utilities.logger import get_logger

logger = get_logger(__name__)


class SignUpPage(BasePage):
    """
    Page Object for AutomationExcercise Sign Up and Login Page
    URL: https://automationpractice.com/signup
    """

    LBL_ENTER_ACCOUNT_INFORMATION = (By.XPATH, "//b[normalize-space()='Enter Account Information']")

    # ---------- Title ----------
    RAD_TITLE_MR = (By.XPATH, "//input[@id='id_gender1']")
    RAD_TITLE_MRS = (By.XPATH, "//input[@id='id_gender2']")

    # ---------- Account ----------
    INPUT_NAME = (By.XPATH, "//input[@id='name']")
    INPUT_PASSWORD = (By.XPATH, "//input[@id='password']")

    # ---------- Date of Birth ----------
    DDL_DAY = (By.XPATH, "//select[@id='days']")
    DDL_MONTH = (By.XPATH, "//select[@id='months']")
    DDL_YEAR = (By.XPATH, "//select[@id='years']")

    # ---------- Preferences ----------
    CHK_NEWSLETTER = (By.XPATH, "//input[@id='newsletter']")
    CHK_OFFERS = (By.XPATH, "//input[@id='optin']")

    # ---------- Address ----------
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
        Get enter account information message
        """
        logger.info("Getting enter account information message")
        return self.get_text(self.LBL_ENTER_ACCOUNT_INFORMATION)

    # ---------- Actions ----------

    def select_title(self, title: str) -> None:
        """
        Selects title
        """
        logger.info("Selecting title")
        if title.lower() == "mr":
            self.click(self.RAD_TITLE_MR)
        elif title.lower() == "mrs":
            self.click(self.RAD_TITLE_MRS)
        else:
            raise ValueError(f"Invalid title: {title}")

    def enter_name(self, name: str) -> None:
        """
        Enters name
        """
        logger.info("Entering name")
        self.send_keys(self.INPUT_NAME, name)

    def enter_password(self, password: str) -> None:
        """
        Enters password
        """
        logger.info("Entering password")
        self.send_keys(self.INPUT_PASSWORD, password)

    def select_date_of_birth(self, day: str, month: str, year: str) -> None:
        """
        Selects date of birth
        """
        logger.info("Selecting date of birth")
        self.select_dropdown_by_value(self.DDL_DAY, day)
        self.select_dropdown_by_value(self.DDL_MONTH, month)
        self.select_dropdown_by_value(self.DDL_YEAR, year)

    def select_newsletter(self) -> None:
        """
        Selects newsletter
        """
        logger.info("Selecting newsletter")
        if not self.is_selected(self.CHK_NEWSLETTER):
            self.click(self.CHK_NEWSLETTER)

    def select_offers(self) -> None:
        """
        Selects offers
        """
        logger.info("Selecting offers")
        if not self.is_selected(self.CHK_OFFERS):
            self.click(self.CHK_OFFERS)

    def enter_first_name(self, first_name: str) -> None:
        """
        Enters first name
        """
        logger.info("Entering first name")
        self.send_keys(self.INPUT_FIRST_NAME, first_name)

    def enter_last_name(self, last_name: str) -> None:
        """
        Enters last name
        """
        logger.info("Entering last name")
        self.send_keys(self.INPUT_LAST_NAME, last_name)

    def enter_company(self, company: str) -> None:
        """
        Enters company
        """
        logger.info("Entering company")
        self.send_keys(self.INPUT_COMPANY, company)

    def enter_address(self, address: str) -> None:
        """
        Enters address
        """
        logger.info("Entering address")
        self.send_keys(self.INPUT_ADDRESS, address)

    def enter_address2(self, address2: str) -> None:
        """
        Enters address2
        """
        logger.info("Entering address2")
        self.send_keys(self.INPUT_ADDRESS2, address2)

    def select_country(self, country: str) -> None:
        """
        Selects country
        """
        logger.info("Selecting country")
        self.select_dropdown_by_value(self.DDL_COUNTRY, country)

    def enter_state(self, state: str) -> None:
        """
        Enters state
        """
        logger.info("Entering state")
        self.send_keys(self.INPUT_STATE, state)

    def enter_city(self, city: str) -> None:
        """
        Enters city
        """
        logger.info("Entering city")
        self.send_keys(self.INPUT_CITY, city)

    def enter_zipcode(self, zipcode: str) -> None:
        """
        Enters zipcode
        """
        logger.info("Entering zipcode")
        self.send_keys(self.INPUT_ZIPCODE, zipcode)

    def enter_mobile_number(self, mobile_number: str) -> None:
        """
        Enters mobile number
        """
        logger.info("Entering mobile number")
        self.send_keys(self.INPUT_MOBILE_NUMBER, mobile_number)

    def click_create_account(self):
        """
        Clicks create account
        """
        logger.info("Clicking create account")
        self.click(self.BTN_CREATE_ACCOUNT)

        from pages.account_created_page import AccountCreatedPage
        return AccountCreatedPage(self.driver)

    def create_account(self, user_profile: dict):
        """
        Fill all signup details and create account
        """
        logger.info("Creating account with full user profile")

        # ---------- Title & Password ----------
        self.select_title(user_profile["title"])
        self.enter_password(user_profile["password"])

        # ---------- Date of Birth ----------
        dob = user_profile["date_of_birth"]
        self.select_date_of_birth(
            day=dob["day"],
            month=dob["month"],
            year=dob["year"]
        )

        # ---------- Preferences ----------
        self.select_newsletter()
        self.select_offers()

        # ---------- Personal Info ----------
        personal = user_profile["personal_info"]
        self.enter_first_name(personal["first_name"])
        self.enter_last_name(personal["last_name"])
        self.enter_company(personal["company"])

        # ---------- Address ----------
        address = user_profile["address"]
        self.enter_address(address["address1"])
        self.enter_address2(address["address2"])
        self.select_country(address["country"])
        self.enter_state(address["state"])
        self.enter_city(address["city"])
        self.enter_zipcode(address["zipcode"])

        # ---------- Contact ----------
        contact = user_profile["contact"]
        self.enter_mobile_number(contact["mobile_number"])

        # ---------- Submit ----------
        self.click_create_account()

        from pages.account_created_page import AccountCreatedPage
        return AccountCreatedPage(self.driver)