import allure

from pages.home_page import HomePage
from utilities.assertions import assert_text_contains
from utilities.data_generator import DataGenerator


@allure.feature("Register User")
def test_register_user(driver, config):
    base_url = config.get("base_url")
    home_page = HomePage(driver)
    username = DataGenerator.unique_username("dustin")
    email = DataGenerator.unique_email("dustin")

    with allure.step("Navigate to url 'https://automationexercise.com'"):
        home_page.navigate_to(base_url)

    with allure.step("Verify that home page is visible successfully"):
        assert home_page.is_home_page_visible()

    with allure.step("Click on 'Signup / Login' button"):
        login_page = home_page.navigate_to_signup_login_page()

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
        signup_page.select_title("mr")
        signup_page.enter_name("DustinOnTheGo")
        signup_page.enter_password("Password")
        signup_page.select_day_of_birth("26")
        signup_page.select_month_of_birth("6")
        signup_page.select_year_of_birth("1999")

    with allure.step("Select checkbox 'Sign up for our newsletter!'"):
        signup_page.select_newsletter()

    with allure.step("Select checkbox 'Receive special offers from our partners!'"):
        signup_page.select_offers()

    with allure.step(
            "Fill details: First name, Last name, Company, Address, Address2, Country, State, City, Zipcode, Mobile Number"):
        signup_page.enter_first_name("Khanh Duy")
        signup_page.enter_last_name("Nguyen")
        signup_page.enter_company("Trulioo")
        signup_page.enter_address("70, Lu Gia street, Phu Tho ward")
        signup_page.enter_address2("Ho Chi Minh")
        signup_page.select_country("Israel")
        signup_page.enter_state("Tel Aviv")
        signup_page.enter_city("Philadelphia")
        signup_page.enter_zipcode("1200")
        signup_page.enter_mobile_number("0912 123 123")

    with allure.step("Click 'Create Account button'"):
        account_created_page = signup_page.click_create_account()

    with allure.step("Verify that 'ACCOUNT CREATED!' is visible"):
        actual_text = account_created_page.get_account_created_message()

        assert_text_contains(actual_text=actual_text,
                             expected_text="ACCOUNT CREATED!",
                             message="ACCOUNT CREATED! is not visible",
                             driver=driver)

    with allure.step("Click 'Continue' button"):
        account_created_page.click_continue()

    with allure.step("Verify that 'Logged in as username' is visible"):
        assert home_page.is_logged_user_visible()

    with allure.step("Click 'Delete Account' button"):
        account_deleted_page = home_page.click_delete_account()

    with allure.step("Verify that 'ACCOUNT DELETED!' is visible and click 'Continue' button"):
        actual_text = account_deleted_page.get_account_deleted_message()

        assert_text_contains(actual_text=actual_text,
                             expected_text="ACCOUNT DELETED!",
                             message="ACCOUNT DELETED! is not visible",
                             driver=driver)

        account_deleted_page.click_continue()