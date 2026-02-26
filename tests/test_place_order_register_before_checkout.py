import allure

from utilities.assertions import assert_text_contains, assert_true
from utilities.data_generator import DataGenerator


@allure.feature("Order Management")
@allure.story("Place Order: Register before Checkout")
def test_place_order_register_before_checkout(app, config, user_profile):
    """
    Test Case 15: Place Order: Register before Checkout
    Ensures an authenticated user can complete the purchase flow seamlessly.
    """
    username = DataGenerator.unique_username("buyer")
    email = DataGenerator.unique_email("buyer")
    base_url = config.get("base_url")
    target_product = "Blue Top"

    with allure.step("Launch browser and navigate to home page"):
        home_page = app.open_site(base_url)

    with allure.step("Verify taht home page is visible successfully"):
        assert_true(home_page.header.is_header_visible(),
                    "Home page header is not visible", home_page)

    with allure.step("Click 'Signup / Login' button"):
        login_page = home_page.header.click_signup_login()

    with allure.step("Fill all details in Signup and create account"):
        login_page.enter_name(username)
        login_page.enter_signup_email(email)
        signup_page = login_page.click_signup()

        user_profile["name"] = user_profile
        account_created_page = signup_page.create_account(user_profile)

    with allure.step("Verify 'ACCOUNT CREATED' and click 'Continue' button"):
        assert_text_contains(actual_text=account_created_page.get_account_created_message(),
                             expected_text="ACCOUNT CREATED",
                             message="Account creation message mismatch",
                             page_object=account_created_page)
        account_created_page.click_continue()

    with allure.step(f"Verify 'Logged in as {username}' at top"):
        assert_true(home_page.header.is_logged_user_visible(),
                    "User should be logged in after registration", home_page)

    with allure.step(f"Add product '{target_product}' to cart"):
        product_details = home_page.view_product(target_product)
        product_details.click_add_to_cart()
        cart_page = product_details.navigate_to_cart_via_modal()

    with allure.step("Verify taht cart page is displayed"):
        assert_true(cart_page.is_cart_page_visible(),
                    "Cart page not visible", cart_page)

    with allure.step("Click 'Proceed To Checkout'"):
        checkout_page = cart_page.proceed_to_checkout()

    with allure.step("Verify Address Details and Review Your Order"):
        assert_true(checkout_page.is_checkout_page_valid(),
                    "Checkout page details are missing", checkout_page)

    with allure.step("Enter desciption and click 'Place Order'"):
        checkout_page.enter_description("Registered User Order")
        payment_page = checkout_page.place_order()

    with allure.step("Enter payment details and confirm order"):
        payment_page.enter_payment_details(
            name_on_card=username,
            card_number="4242424242424242",
            cvc="311",
            expiry_month="12",
            expiry_year="2030"
        )
        order_placed_page = payment_page.click_pay_and_confirm()

    with allure.step("Verify success message"):
        assert_text_contains(actual_text=order_placed_page.get_order_success_message(),
                             expected_text="Congratulations! Your order has been confirmed!",
                             message="Order failed for registered user",
                             page_object=order_placed_page)

    with allure.step("Click 'Delete Account' button"):
        account_deleted_page = home_page.header.click_delete_account()

    with allure.step("Verify 'ACCOUNT DELETED' and click 'Continue'"):
        assert_text_contains(actual_text=account_deleted_page.get_account_deleted_message(),
                             expected_text="ACCOUNT DELETED",
                             message="Account deletion flow failed",
                             page_object=account_deleted_page)
    account_deleted_page.click_continue()
