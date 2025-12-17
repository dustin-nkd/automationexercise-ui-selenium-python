import allure

from pages.guest_page import GuestPage
from utilities.assertions import assert_text_contains


@allure.feature("Login")
def test_login_user_with_correct_email_and_password(driver, config, registered_user):
    base_url = config.get("base_url")
    guest_page = GuestPage(driver)

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

    with allure.step("Enter correct email address and password"):
        login_page.enter_login_email(registered_user["email"])
        login_page.enter_password(registered_user["password"])

    with allure.step("Click 'login' button"):
        home_page = login_page.click_login()

    with allure.step("Verify that 'Logged in as username' is visible"):
        assert home_page.is_logged_user_visible()

    with allure.step("Click 'Delete Account' button"):
        account_deleted_page = home_page.click_delete_account()

    with allure.step("Verify that 'ACCOUNT DELETED!' is visible"):
        actual_text = account_deleted_page.get_account_deleted_message()

        assert_text_contains(actual_text=actual_text,
                             expected_text="ACCOUNT DELETED!",
                             message="ACCOUNT DELETED! is not visible",
                             driver=driver)