import allure

from pages.guest_page import GuestPage
from utilities.assertions import assert_text_contains
from utilities.data_generator import DataGenerator


@allure.feature("Register")
def test_register_user(driver, config):
    base_url = config.get("base_url")
    guest_page = GuestPage(driver)

    username = DataGenerator.unique_username("dustin")
    email = DataGenerator.unique_email("dustin")
    user = config["user_profile"]

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

    with allure.step("Enter name and email address"):
        login_page.enter_name(username)
        login_page.enter_signup_email(email)

    with allure.step("Click 'Signup' button"):
        signup_page = login_page.click_signup()

    with allure.step("Verify that 'ENTER ACCOUNT INFORMATION' is visible"):
        actual_text = signup_page.get_enter_account_information_message()
        assert_text_contains(actual_text=actual_text,
                             expected_text="ENTER ACCOUNT INFORMATION",
                             message="ENTER ACCOUNT INFORMATION is not visible",
                             driver=driver)

    with allure.step("Fill details: Title, Name, Email, Password, Date of birth"):
        signup_page.select_title(user["title"])
        signup_page.enter_name(user["name"])
        signup_page.enter_password(user["password"])

        dob = user["date_of_birth"]
        signup_page.select_date_of_birth(dob["day"], dob["month"], dob["year"])
        # signup_page.select_day_of_birth(dob["day"])
        # signup_page.select_month_of_birth(dob["month"])
        # signup_page.select_year_of_birth(dob["year"])

    with allure.step("Select checkbox 'Sign up for our newsletter!'"):
        signup_page.select_newsletter()

    with allure.step("Select checkbox 'Receive special offers from our partners!'"):
        signup_page.select_offers()

    with allure.step("Fill address and contact information"):
        personal = user["personal_info"]
        address = user["address"]
        contact = user["contact"]

        signup_page.enter_first_name(personal["first_name"])
        signup_page.enter_last_name(personal["last_name"])
        signup_page.enter_company(personal["company"])

        signup_page.enter_address(address["address1"])
        signup_page.enter_address2(address["address2"])
        signup_page.select_country(address["country"])
        signup_page.enter_state(address["state"])
        signup_page.enter_city(address["city"])
        signup_page.enter_zipcode(address["zipcode"])

        signup_page.enter_mobile_number(contact["mobile_number"])

    with allure.step("Click 'Create Account button'"):
        account_created_page = signup_page.click_create_account()

    with allure.step("Verify that 'ACCOUNT CREATED!' is visible"):
        actual_text = account_created_page.get_account_created_message()
        assert_text_contains(actual_text=actual_text,
                             expected_text="ACCOUNT CREATED!",
                             message="ACCOUNT CREATED! is not visible",
                             driver=driver)

    with allure.step("Click 'Continue' button"):
        home_page = account_created_page.click_continue()

    with allure.step("Verify that 'Logged in as username' is visible"):
        assert home_page.is_logged_user_visible()

    with allure.step("Click 'Delete Account' button"):
        account_deleted_page = home_page.delete_account()

    with allure.step("Verify that 'ACCOUNT DELETED!' is visible and click 'Continue' button"):
        actual_text = account_deleted_page.get_account_deleted_message()
        assert_text_contains(actual_text=actual_text,
                             expected_text="ACCOUNT DELETED!",
                             message="ACCOUNT DELETED! is not visible",
                             driver=driver)

        account_deleted_page.click_continue()