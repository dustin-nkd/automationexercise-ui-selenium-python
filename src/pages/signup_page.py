from selenium.webdriver.common.by import By

from pages.account_created_page import AccountCreatedPage
from pages.base_page import BasePage
from utilities.logger import get_logger

logger = get_logger(__name__)


class SignUpPage(BasePage):
    """
    Page Object for AutomationExcercise Sign Up and Login Page
    URL: https://automationpractice.com/signup
    """
    LABEL_ENTER_ACCOUNT_INFORMATION = (By.XPATH, "//b[normalize-space()='Enter Account Information']")
    RADIO_BTN_MR = (By.XPATH, "//input[@id='id_gender1']")
    RADIO_BTN_MRS = (By.XPATH, "//input[@id='id_gender2']")
    INPUT_NAME = (By.XPATH, "//input[@id='name']")
    INPUT_PASSWORD = (By.XPATH, "//input[@id='password']")
    DROPDOWN_DAY_OF_BIRTH = (By.XPATH, "//select[@id='days']")
    DROPDOWN_MONTH_OF_BIRTH = (By.XPATH, "//select[@id='months']")
    DROPDOWN_YEAR_OF_BIRTH = (By.XPATH, "//select[@id='years']")
    CHECKBOX_NEWSLETTER = (By.XPATH, "//input[@id='newsletter']")
    CHECKBOX_OFFERS = (By.XPATH, "//input[@id='optin']")
    INPUT_FIRST_NAME = (By.XPATH, "//input[@id='first_name']")
    INPUT_LAST_NAME = (By.XPATH, "//input[@id='last_name']")
    INPUT_COMPANY = (By.XPATH, "//input[@id='company']")
    INPUT_ADDRESS = (By.XPATH, "//input[@id='address1']")
    INPUT_ADDRESS2 = (By.XPATH, "//input[@id='address2']")
    DROPDOWN_COUNTRY = (By.XPATH, "//select[@id='country']")
    INPUT_STATE = (By.XPATH, "//input[@id='state']")
    INPUT_CITY = (By.XPATH, "//input[@id='city']")
    INPUT_ZIPCODE = (By.XPATH, "//input[@id='zipcode']")
    INPUT_MOBILE_NUMBER = (By.XPATH, "//input[@id='mobile_number']")
    BTN_CREATE_ACCOUNT = (By.XPATH, "//button[contains(text(),'Create Account')]")

    def get_enter_account_information_message(self) -> str:
        """
        Get enter account information message
        """
        logger.info("Getting enter account information message")
        return self.get_text(self.LABEL_ENTER_ACCOUNT_INFORMATION)

    def select_title(self, title: str) -> None:
        """
        Selects title
        """
        logger.info("Selecting title")
        if title.lower() == "mr":
            self.click(self.RADIO_BTN_MR)
        elif title.lower() == "mrs":
            self.click(self.RADIO_BTN_MRS)

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

    def select_day_of_birth(self, day: str) -> None:
        """
        Selects day of birth
        """
        logger.info("Selecting day of birth")
        self.select_dropdown_by_value(self.DROPDOWN_DAY_OF_BIRTH, day)

    def select_month_of_birth(self, month: str) -> None:
        """
        Selects month of birth
        """
        logger.info("Selecting month of birth")
        self.select_dropdown_by_value(self.DROPDOWN_MONTH_OF_BIRTH, month)

    def select_year_of_birth(self, year: str) -> None:
        """
        Selects year of birth
        """
        logger.info("Selecting year of birth")
        self.select_dropdown_by_value(self.DROPDOWN_YEAR_OF_BIRTH, year)

    def select_newsletter(self) -> None:
        """
        Selects newsletter
        """
        logger.info("Selecting newsletter")
        if not self.is_selected(self.CHECKBOX_NEWSLETTER):
            self.click(self.CHECKBOX_NEWSLETTER)

    def select_offers(self) -> None:
        """
        Selects offers
        """
        logger.info("Selecting offers")
        if not self.is_selected(self.CHECKBOX_OFFERS):
            self.click(self.CHECKBOX_OFFERS)

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
        self.select_dropdown_by_value(self.DROPDOWN_COUNTRY, country)

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

    def click_create_account(self) -> AccountCreatedPage:
        """
        Clicks create account
        """
        logger.info("Clicking create account")
        self.click(self.BTN_CREATE_ACCOUNT)
        return AccountCreatedPage(self.driver)