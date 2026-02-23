import allure

from utilities.assertions import assert_text_contains, assert_true


@allure.feature("Access Control")
@allure.story("Logout functionality")
def test_logout_user(app, config, registered_user):
    """
    Test Case 4: Logout User
    Verifies that a logged-in user can successfully log out and return to the login page.
    """
    base_url = config.get("base_url")

    with allure.step("Launch browser and navigate to home page"):
        home_page = app.open_site(base_url)

    with allure.step("Verify that home page is visible successfully"):
        # Header visibility confirms the page shell is loaded
        assert_true(home_page.header.is_header_visible(),
                    "Home page header is not visible", home_page)

    with allure.step("Click on 'Signup / Login' button"):
        login_page = home_page.header.click_signup_login()

    with allure.step("Verify 'Login to your account' is visible"):
        assert_text_contains(actual_text=login_page.get_login_to_your_account_message(),
                             expected_text="Login to your account",
                             message="Login header mismatch",
                             page_object=login_page)

    with allure.step("Enter correct email address and password"):
        login_page.enter_login_email(registered_user["email"])
        login_page.enter_password(registered_user["password"])

    with allure.step("Click 'login' button"):
        home_page = login_page.click_login()

    with allure.step("Verify that 'Logged in as username' is visible"):
        assert_true(home_page.header.is_header_visible(),
                    f"User {registered_user['username']} failed to login", home_page)

    with allure.step("Click 'Logout' button"):
        # Navigation logic is centralized in the Header component
        login_page = home_page.header.click_logout()

    with allure.step("Verify that user is navigated to login page"):
        # After logout, we check if we are back the Login section
        assert_text_contains(actual_text=login_page.get_login_to_your_account_message(),
                             expected_text="Login to your account",
                             message="User was not redirected to Login page after logout",
                             page_object=login_page)
