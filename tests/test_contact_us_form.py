import allure

from pages.guest_page import GuestPage
from utilities.assertions import assert_text_contains
from utilities.data_generator import DataGenerator


@allure.feature("Contact")
def test_contact_us_form(driver, config):
    base_url = config.get("base_url")
    guest_page = GuestPage(driver)

    name = DataGenerator.unique_username("dustin")
    email = DataGenerator.unique_email("dustin")

    with allure.step("Navigate to url 'https://automationexercise.com'"):
        guest_page.navigate_to(base_url)

    with allure.step("Verify that home page is visible successfully"):
        assert guest_page.is_home_page_visible()

    with allure.step("Click on 'Contact Us' button"):
        contact_us_page = guest_page.navigate_to_contact_us_page()

    with allure.step("Verify 'GET IN TOUCH' is visible"):
        actual_text = contact_us_page.get_get_in_touch_message()
        assert_text_contains(actual_text=actual_text,
                             expected_text="GET IN TOUCH",
                             message="GET IN TOUCH message is not visible",
                             driver=driver)

    with allure.step("Enter name, email, subject and message"):
        contact_us_page.enter_name(name)
        contact_us_page.enter_email(email)
        contact_us_page.enter_subject("Sample text")
        contact_us_page.enter_message("Sample message")

    with allure.step("Upload file"):
        contact_us_page.upload_attachment("test_data/upload/sample.txt")

    with allure.step("Click 'Submit' button"):
        contact_us_page.click_submit()

    with allure.step("Click OK button"):
        contact_us_page.accept_alert()

    with allure.step("Verify success message 'Success! Your details have been submitted successfully.' is visible"):
        actual_text = contact_us_page.get_success_submitted_message()
        assert_text_contains(actual_text=actual_text,
                             expected_text="Success! Your details have been submitted successfully",
                             message="Success! Your details have been submitted successfully is not visible",
                             driver=driver)

    with allure.step("Click 'Home' button and verify that landed to home page successfully"):
        guest_page = contact_us_page.click_home()
        assert guest_page.is_home_page_visible()