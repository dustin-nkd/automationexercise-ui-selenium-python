import allure

from pages.guest_page import GuestPage
from utilities.assertions import assert_text_contains


@allure.feature("Login")
def test_login_user_with_incorrect_email_and_password(driver, config, registered_user):
    base_url = config.get("base_url")
    guest_page = GuestPage(driver)
    user = config["test_user"]

    with allure.step("Navigate to url 'https://automationexercise.com'"):
        guest_page.navigate_to(base_url)

    with allure.step("Verify that home page is visible successfully"):
        assert guest_page.is_home_page_visible()

    with allure.step("Click on 'Signup / Login' button"):
        login_page = guest_page.navigate_to_signup_login_page()

    with allure.step("Verify 'Login to your account' is visible"):
        actual_text = login_page.get_login_to_your_account_message()

        assert_text_contains(actual_text=actual_text,
                             expected_text="Login to your account",
                             message="Login to your account is not visible",
                             driver=driver)

    with allure.step("Enter incorrect email address and password"):
        login_page.enter_login_email(registered_user["email"])
        login_page.enter_password(user["invalid_password"])

    with allure.step("Click 'login' button"):
        login_page.click_login()

    with allure.step("Verify error 'Your email or password is incorrect!' is visible"):
        actual_text = login_page.get_your_email_or_password_is_incorrect_message()

        assert_text_contains(actual_text=actual_text,
                             expected_text="Your email or password is incorrect!",
                             message="Your email or password is incorrect is not visible!",
                             driver=driver)