import allure

from utilities.assertions import assert_text_contains, assert_true
from utilities.data_loader import DataLoader


@allure.feature("Access Control")
@allure.story("Login with invalid credentials")
def test_login_user_with_incorrect_email_and_password(app, config):
    """
    Test Case 3: Login User with incorrect email and password
    Verifies that the system displays an error message for invalid credentials.
    """
    # 1. Load invalid user data from the new test_data system
    user_data = DataLoader.get_user_data()
    invalid_credentials = user_data["test_user"]
    base_url = config.get("base_url")

    with allure.step("Launch browser and navigate to home page"):
        home_page = app.open_site(base_url)

    with allure.step("Verify that home page is visbile successfully"):
        assert_true(home_page.header.is_header_visible(),
                    "Home page header is not visible", home_page)

    with allure.step("Click on 'Signup / Login' button"):
        login_page = home_page.header.click_signup_login()

    with allure.step("Verify 'Login to your account' is visible"):
        assert_text_contains(actual_text=login_page.get_login_to_your_account_message(),
                             expected_text="Login to your account",
                             message="Login section header mismmatch",
                             page_object=login_page)

    with allure.step("Enter incorrect email address and password"):
        login_page.enter_login_email(invalid_credentials["invalid_user"])
        login_page.enter_password(invalid_credentials["invalid_password"])

    with allure.step("Click 'login' button"):
        # W stay on the login page because of the failure
        login_page.click_login()

    with allure.step("Verify error 'Your email or password is incorrect!' is visible"):
        error_message = login_page.get_your_email_or_password_is_incorrect_message()
        assert_text_contains(actual_text=error_message,
                             expected_text="Your email or password is incorrect!",
                             message="Error message for invalid login not found",
                             page_object=login_page)
