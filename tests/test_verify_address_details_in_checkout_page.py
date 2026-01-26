import allure

from pages.guest_page import GuestPage
from utilities.assertions import assert_text_contains
from utilities.data_generator import DataGenerator


@allure.feature("Checkout")
def test_verify_address_details_in_checkout_page(driver, config):
    base_url = config.get("base_url")
    guest_page = GuestPage(driver)
    name = DataGenerator.unique_username("user")
    email = DataGenerator.unique_email("user")

    with allure.step("Navigate to url 'https://automationexercise.com'"):
        guest_page.navigate_to(base_url)

    with allure.step("Verify that home page is visible successfully"):
        assert guest_page.is_home_page_visible()

    with allure.step("Click 'Signup / Login' button"):
        login_page = guest_page.navigate_to_signup_login_page()

    with allure.step("Fill all details in Signup and create account"):
        sign_up_page = login_page.sign_up(name, email)
        account_created_page = sign_up_page.create_account(config["user_profile"])

    with allure.step("6. Verify 'ACCOUNT CREATED!' and click 'Continue' button"):
        actual_text = account_created_page.get_account_created_message()
        assert_text_contains(actual_text=actual_text,
                             expected_text="ACCOUNT CREATED!",
                             message="ACCOUNT CREATED! is not visible",
                             driver=driver)
        home_page = account_created_page.click_continue()

    with allure.step("Verify ' Logged in as username' at top"):
        assert home_page.is_logged_user_visible()

    with allure.step("Add products to cart"):
        home_page.products.add_product_to_cart_by_item("Blue Top")
        home_page.add_to_cart_modal.click_continue_shopping()

    with allure.step("Click 'Cart' button"):
        cart_page = guest_page.navigate_to_cart_page()

    with allure.step("Verify that cart page is displayed"):
        assert cart_page.is_cart_page_visible()
        assert cart_page.is_cart_table_visible()

    with allure.step("Click Proceed To Checkout"):
        chekcout_page = cart_page.proceed_to_checkout()

    with allure.step("Verify Address Details and Review Your Order"):
        assert chekcout_page.is_checkout_page_valid()

    with allure.step("Click 'Delete Account' button"):
        account_deleted_page = home_page.delete_account()

    with allure.step("Verify 'ACCOUNT DELETED!' and click 'Continue' button"):
        actual_text = account_deleted_page.get_account_deleted_message()
        assert_text_contains(actual_text=actual_text,
                             expected_text="ACCOUNT DELETED!",
                             message="ACCOUNT DELETED! is not visible",
                             driver=driver)
        account_deleted_page.click_continue()