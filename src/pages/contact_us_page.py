from pathlib import Path
from typing import Union

from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utilities.logger import get_logger

logger = get_logger(__name__)


class ContactUsPage(BasePage):
    """
    Page Object for Automation Excercise Contact Us Page
    URL: https://automationexercise.com/contact_us
    """

    LBL_GET_IN_TOUCH = (By.XPATH, "//h2[normalize-space()='Get In Touch']")
    INPUT_NAME = (By.CSS_SELECTOR, "input[placeholder='Name']")
    INPUT_EMAIL = (By.CSS_SELECTOR, "input[placeholder='Email']")
    INPUT_SUBJECT = (By.CSS_SELECTOR, "input[placeholder='Subject']")
    INPUT_MESSAGE = (By.ID, "message")
    BTN_UPLOAD_FILE = (By.CSS_SELECTOR, "input[name='upload_file']")
    BTN_SUBMIT = (By.CSS_SELECTOR, "input[value='Submit']")
    MSG_SUCCESS_SUBMITTED = (By.XPATH, "//div[@class='status alert alert-success']")
    BTN_HOME = (By.CSS_SELECTOR, ".btn.btn-success")

    def get_get_in_touch_message(self) -> str:
        """
        Get In Touch
        """
        logger.info("Getting get in touch message")
        return self.get_text(self.LBL_GET_IN_TOUCH)

    def enter_name(self, name: str) -> None:
        """
        Enter name
        """
        logger.info("Entering name")
        self.send_keys(self.INPUT_NAME, name)

    def enter_email(self, email: str) -> None:
        """
        Enter email
        """
        logger.info("Entering email")
        self.send_keys(self.INPUT_EMAIL, email)

    def enter_subject(self, subject: str) -> None:
        """
        Enter subject
        """
        logger.info("Entering subject")
        self.send_keys(self.INPUT_SUBJECT, subject)

    def enter_message(self, message: str) -> None:
        """
        Enter message
        """
        logger.info("Entering message")
        self.send_keys(self.INPUT_MESSAGE, message)

    def upload_attachment(self, file_path: Union[str, Path]) -> None:
        """
        Upload attachment file in Contact Us form
        """
        logger.info("Uploading file: %s", file_path)
        self.upload_file(self.BTN_UPLOAD_FILE, file_path)

    def click_submit(self) -> None:
        """
        Click submit button
        """
        logger.info("Clicking submit button")
        self.click(self.BTN_SUBMIT)

    def get_success_submitted_message(self) -> str:
        """
        Get Success! Your details have been submitted successfully message
        """
        logger.info("Getting Success! Your details have been submitted successfully message")
        return self.get_text(self.MSG_SUCCESS_SUBMITTED)

    def click_home(self) -> "GuestPage":
        """
        Click home button
        """
        logger.info("Clicking home button")
        self.click(self.BTN_HOME)

        from pages.guest_page import GuestPage
        return GuestPage(self.driver)