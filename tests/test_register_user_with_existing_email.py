import allure

from utilities.assertions import assert_text_contains, assert_true
from utilities.data_generator import DataGenerator


@allure.feature("User Management")
@allure.story("Register with existing email")
def test_register_user_with_existing_email(app, config, registered_user):
    """
    Test Case 5: Register User with existing email
    Verifies that the system prevents registration with an email that is already in use.
    """
    base_url = config.get("base_url")
    # Generate a fresh name, but use the email from the pre-registered user
    new_name = DataGenerator.unique_username("existing")
    existing_email = registered_user["email"]

    with allure.step("Launch browser and navigate to home page"):
        home_page = app.open_site(base_url)

    with allure.step("Verify that home page is visible successfully"):
        assert_true(home_page.header.is_header_visible(),
                    "Home page header is not visible", home_page)

    with allure.step("Click on 'Signup / Login' button"):
        login_page = home_page.header.click_signup_login()

    with allure.step("Verify 'New User Signup!' is visible"):
        assert_text_contains(actual_text=login_page.get_new_user_signup_message(),
                             expected_text="New User Signup!",
                             message="New User Signup section not found",
                             page_object=login_page)

    with allure.step("Enter name and already registered email address"):
        login_page.enter_name(new_name)
        login_page.enter_signup_email(existing_email)

    with allure.step("Click 'Signup' button"):
        # The system should keep us on the same page and show an error
        login_page.click_signup()

    with allure.step("Verify error 'Email Address already exist!' is visible"):
        error_msg = login_page.get_email_address_already_exist_message()
        assert_text_contains(actual_text=error_msg,
                             expected_text="Email Address already exist!",
                             message="Error message for existing email not displayed",
                             page_object=login_page)
