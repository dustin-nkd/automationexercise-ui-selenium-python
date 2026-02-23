import allure

from utilities.assertions import assert_text_contains, assert_true


@allure.feature("Access Control")
@allure.story("Login with valid credentials")
def test_login_user_with_correct_email_and_password(app, config, registered_user):
    """
    Test Case 2: Login User with correct email and password
    This test uses a pre-registered user created by the 'registered_user' fixture.
    """
    base_url = config.get("base_url")

    with allure.step("Launch browser and navigate to home page"):
        home_page = app.open_site(base_url)

    with allure.step("Verify that home page is visible successfully"):
        # User header visibility as a proxy for home page being loaded
        assert_true(home_page.header.is_header_visible(),
                    "Home page header is not visible", home_page)

    with allure.step("Click on 'Signup / Login' button"):
        # Navigation handled via the Header component
        login_page = home_page.header.click_signup_login()

    with allure.step("Verify 'Login to your account' is visible"):
        assert_text_contains(actual_text=login_page.get_login_to_your_account_message(),
                             expected_text="Login to your account",
                             message="Login section header mismatch",
                             page_object=login_page)

    with allure.step("Enter correct email address and password"):
        # registered_user fixture provides the credentials created in the background
        login_page.enter_login_email(registered_user["email"])
        login_page.enter_password(registered_user["password"])

    with allure.step("Click 'login' button"):
        home_page = login_page.click_login()

    with allure.step("Verify that 'Logged in as username' is visible"):
        assert_true(home_page.header.is_logged_user_visible(),
                    f"User {registered_user['username']} is not logged in", home_page)

    with allure.step("Click 'Delete Account' button"):
        # Deletion is a global action available in the header
        account_deleted_page = home_page.header.click_delete_account()

    with allure.step("Verify that 'ACCOUNT DELETED' is visible"):
        assert_text_contains(actual_text=account_deleted_page.get_account_deleted_message(),
                             expected_text="ACCOUNT DELETED",
                             message="Account deletion confirmation message not found",
                             page_object=account_deleted_page)
