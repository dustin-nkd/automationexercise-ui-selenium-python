import allure

from utilities.assertions import assert_text_contains, assert_true
from utilities.data_generator import DataGenerator


@allure.feature("User Management")
@allure.story("Register User")
def test_register_user(app, config, user_profile):
    """
    Test Case 1: Register User successfully with full details
    """
    # 1. Prepare dynamic data
    username = DataGenerator.unique_username("dustin")
    email = DataGenerator.unique_email("dustin")
    base_url = config.get("base_url")

    # 2. Start Test Flow
    with allure.step("Launch browser and navigate to url"):
        home_page = app.open_site(base_url)

    with allure.step("Verify that home page is visible successfully"):
        assert_true(home_page.header.is_header_visible(),
                    "Home page header is not visible", home_page)

    with allure.step("Click on Signup / Login button"):
        # Header handle transition to LoginPage
        login_page = home_page.header.click_signup_login()

    with allure.step("Verify 'New User Signup!' is visible"):
        assert_text_contains(actual_text=login_page.get_new_user_signup_message(),
                             expected_text="New User Signup!",
                             message="New User Signup! message mismatch",
                             page_object=login_page)

    with allure.step("Enter name and email address for signup"):
        login_page.enter_name(username)
        login_page.enter_signup_email(email)
        signup_page = login_page.click_signup()

    with allure.step("Verify that 'ENTER ACCOUNT INFORMATION' is visible"):
        assert_text_contains(actual_text=signup_page.get_enter_account_information_message(),
                             expected_text="ENTER ACCOUNT INFORMATION",
                             message="Signup page was not loaded correctly",
                             page_object=signup_page)

    with allure.step("Fill details and select checkboxes"):
        # We can update our user_profile dict with the dynamic username
        user_profile["name"] = username
        # Use the high-level method we created to fill the whole form
        account_create_page = signup_page.create_account(user_profile,
                                                         subscribe_newsletter=True,
                                                         receive_offers=True)

    with allure.step("Verify that'ACCOUNT CREATED' is visible"):
        assert_text_contains(actual_text=account_create_page.get_account_created_message(),
                             expected_text="ACCOUNT CREATED",
                             message="Account creation failed",
                             page_object=account_create_page)

    with allure.step("Click 'Continue' button"):
        home_page = account_create_page.click_continue()

    with allure.step("Verify that 'Logged in as username' is visible"):
        assert_true(home_page.header.is_header_visible(),
                    f"Expected 'Logged in as {username}' but not found", home_page)

    with allure.step("Click 'Delete Account' button"):
        # Navigation handled by Header
        account_deleted_page = home_page.header.click_delete_account()

    with allure.step("Verify 'ACCOUNT DELETED' is visible and click 'Continue'"):
        assert_text_contains(actual_text=account_deleted_page.get_account_deleted_message(),
                             expected_text="ACCOUNT DELETED",
                             message="Account deletion failed",
                             page_object=account_deleted_page)

        account_deleted_page.click_continue()
