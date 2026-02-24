from pathlib import Path
from typing import Union
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utilities.logger import get_logger

logger = get_logger(__name__)


class ContactUsPage(BasePage):
    """
    Page Object for Automation Excercise Contact Us Page.
    URL: https://automationexercise.com/contact_us
    """

    # ---------- Locators ----------
    LBL_GET_IN_TOUCH = (By.XPATH, "//h2[normalize-space()='Get In Touch']")
    INPUT_NAME = (By.CSS_SELECTOR, "input[placeholder='Name']")
    INPUT_EMAIL = (By.CSS_SELECTOR, "input[placeholder='Email']")
    INPUT_SUBJECT = (By.CSS_SELECTOR, "input[placeholder='Subject']")
    INPUT_MESSAGE = (By.ID, "message")
    BTN_UPLOAD_FILE = (By.CSS_SELECTOR, "input[name='upload_file']")
    BTN_SUBMIT = (By.CSS_SELECTOR, "input[value='Submit']")
    MSG_SUCCESS_SUBMITTED = (By.XPATH, "//div[@class='status alert alert-success']")
    BTN_HOME = (By.CSS_SELECTOR, ".btn.btn-success")

    # ---------- Verifications ----------

    def get_get_in_touch_message(self) -> str:
        """Retrieves the 'Get In Touch' header text."""
        logger.info("Getting 'Get In Touch' message")
        return self.get_text(self.LBL_GET_IN_TOUCH)

    def get_success_submitted_message(self) -> str:
        """Retrieves the success message after form submission."""
        logger.info("Getting success submission message")
        return self.get_text(self.MSG_SUCCESS_SUBMITTED)

    # ---------- Individual Actions ----------

    def enter_name(self, name: str) -> None:
        self.send_keys(self.INPUT_NAME, name)

    def enter_email(self, email: str) -> None:
        self.send_keys(self.INPUT_EMAIL, email)

    def enter_subject(self, subject: str) -> None:
        self.send_keys(self.INPUT_SUBJECT, subject)

    def enter_message(self, message: str) -> None:
        self.send_keys(self.INPUT_MESSAGE, message)

    def upload_attachment(self, file_path: Union[str, Path]) -> None:
        """Uploads a file by sending the absolute path to the file input."""
        logger.info(f"Uploading file: {file_path}")
        self.upload_file(self.BTN_UPLOAD_FILE, str(file_path))

    def click_submit(self) -> None:
        """Clicks the submit button."""
        logger.info("Clicking submit button")
        self.click(self.BTN_SUBMIT)

    # ---------- Combined Actions ----------

    def fill_contact_form(self, name: str, email: str, subject: str, message: str) -> None:
        """
        High-levl method to fill all text fields in the contact form.
        """
        logger.info(f"Filling contact form for: {name}")
        self.enter_name(name)
        self.enter_email(email)
        self.enter_subject(subject)
        self.enter_message(message)

    # ---------- Navigation ----------

    def click_home(self):
        """
        Clicks the Home button and returns the HomePage instance via Navigator.
        """
        logger.info("Clicking home button to return to Home Page")
        self.click(self.BTN_HOME)
        # Use Navigator for consistent page transitions
        return self.navigate.home_page