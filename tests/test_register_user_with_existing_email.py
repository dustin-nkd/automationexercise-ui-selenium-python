import allure

from pages.guest_page import GuestPage
from utilities.assertions import assert_text_contains
from utilities.data_generator import DataGenerator


@allure.feature("Register")
def test_register_user_with_existing_email(driver, config, registered_user):
    base_url = config.get("base_url")
    guest_page = GuestPage(driver)

    name = DataGenerator.unique_username("existing")

    with allure.step("Navigate to url 'https://automationexercise.com'"):
        guest_page.navigate_to(base_url)

    with allure.step("Verify that home page is visible successfully"):
        assert guest_page.is_home_page_visible()

    with allure.step("Click on 'Signup / Login' button"):
        login_page = guest_page.navigate_to_signup_login_page()

    with allure.step("Verify 'New User Signup!' is visible"):
        actual_text = login_page.get_new_user_signup_message()
        assert_text_contains(actual_text=actual_text,
                             expected_text="New User Signup!",
                             message="New User Signup! is not visible",
                             driver=driver)

    with allure.step("Enter name and already registered email address"):
        login_page.enter_name(name)
        login_page.enter_signup_email(registered_user["email"])

    with allure.step("Click 'Signup' button"):
        login_page.click_signup()

    with allure.step("Verify error 'Email Address already exist!' is visible"):
        actual_text = login_page.get_email_address_already_exist_message()
        assert_text_contains(actual_text=actual_text,
                             expected_text="Email Address already exist!",
                             message="Email Address already exist! is not visible",
                             driver=driver)