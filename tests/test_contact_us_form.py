from pathlib import Path

import allure
import pytest

from utilities.assertions import assert_text_contains, assert_true
from utilities.data_generator import DataGenerator
from utilities.data_loader import DataLoader


@allure.feature("Customer Support")
@allure.story("Contact Us Form Submission")
def test_contact_us_form(app, config):
    """
    Test Case 6: Contact Us Form
    Tests the contact form including file upload and JS alert handling.
    """
    base_url = config.get("base_url")
    name = DataGenerator.unique_username("contact_user")
    email = DataGenerator.unique_email(prefix="support")

    # Resolve the upload file path dynamically using DataLoader's root
    # Ensuring the file exists before starting the test
    upload_file_path = DataLoader.UPLOAD_DIR / "sample.txt"

    file_to_upload = str(upload_file_path.resolve())

    with allure.step("Launch browser and navigate to home page"):
        home_page = app.open_site(base_url)

    with allure.step("Verify that home page is visible successfully"):
        assert_true(home_page.header.is_header_visible(),
                    "Home page header is not visible", home_page)

    with allure.step("Click on 'Contact Us' button"):
        # Navigation to Contact Us is usually in the Header
        contact_us_page = home_page.header.click_contact_us()

    with allure.step("Verify 'GET IN TOUCH' is visible"):
        assert_text_contains(actual_text=contact_us_page.get_get_in_touch_message(),
                             expected_text="GET IN TOUCH",
                             message="Contact page header mismatch",
                             page_object=contact_us_page)

    with allure.step("Enter name, email, subject and message"):
        contact_us_page.fill_contact_form(
            name=name,
            email=email,
            subject="Automation Test Inquiry",
            message="This is a sample automated message for testing purpose"
        )

    with allure.step("Upload file"):
        # Check if file exists to prevent hard-to-debug Selenium errors
        if not Path(upload_file_path).exists():
            pytest.fail(f"Upload file not found at: {file_to_upload}")
        contact_us_page.upload_attachment(file_to_upload)

    with allure.step("Click 'Submit' button"):
        contact_us_page.click_submit()

    with allure.step("Click OK button on Javascript Alert"):
        # This handles the browser popup
        contact_us_page.accept_alert()

    with allure.step("Verify success message is visible"):
        success_msg = "Success! Your details have been submitted successfully."
        assert_text_contains(actual_text=contact_us_page.get_success_submitted_message(),
                             expected_text=success_msg,
                             message="Contact form submission failed or success message not shown",
                             page_object=contact_us_page)

    with allure.step("Click 'Home' button and verify return to home page"):
        home_page = contact_us_page.click_home()
        assert_true(home_page.header.is_header_visible(),
                    "Failed to return to Home Page after contact submission", home_page)
