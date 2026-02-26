import allure

from utilities.assertions import assert_text_contains, assert_true


@allure.feature("Order Management")
@allure.story("Place Order: Login before Checkout")
def test_place_order_login_before_checkout(app, config, logged_in_user):
    """
    Test Case 16: Place Order: Login before Checkout
    Uses an existing logged-in session to perform a complete purchase flow.
    """
    home_page = logged_in_user
    target_product = "Blue Top"

    with allure.step("verify 'Logged in as username' at top"):
        assert_true(home_page.header.is_logged_user_visible(),
                    "User should be logged in via fixture", home_page)

    with allure.step(f"Add product '{target_product}' to cart"):
        product_details = home_page.view_product(target_product)
        product_details.click_add_to_cart()
        cart_page = product_details.navigate_to_cart_via_modal()

    with allure.step("Verify that cart page is displayed"):
        assert_true(cart_page.is_cart_page_visible(),
                    "Cart page not visible", cart_page)
        assert_true(cart_page.is_cart_table_visible(),
                    "Cart table is missing", cart_page)

    with allure.step("Click 'Proceed To Checkout'"):
        checkout_page = cart_page.proceed_to_checkout()

    with allure.step("Verify Address Details and Review Your Order"):
        assert_true(checkout_page.is_checkout_page_valid(),
                    "Checkout address/review actions invalid", checkout_page)

    with allure.step("Enter description and click 'Place Order!'"):
        checkout_page.enter_description("Order with pre-logged account")
        payment_page = checkout_page.place_order()

    with allure.step("Enter payment details and confirm order"):
        payment_page.enter_payment_details(
            name_on_card="Dustin SDET",
            card_number="4242424242424242",
            cvc="311",
            expiry_month="12",
            expiry_year="2028"
        )
        order_placed_page = payment_page.click_pay_and_confirm()

    with allure.step("Verify success message"):
        assert_text_contains(actual_text=order_placed_page.get_order_success_message(),
                             expected_text="Congratulations! Your order has been confirmed!",
                             message="Order confirmation failed",
                             page_object=order_placed_page)

    with allure.step("Click 'Delete Account' button"):
        home_page = order_placed_page.click_continue()
        account_deleted_page = home_page.header.click_delete_account()

    with allure.step("Verify 'ACCOUNT DELETED!' and click 'Continue'"):
        assert_text_contains(actual_text=account_deleted_page.get_account_deleted_message(),
                             expected_text="ACCOUNT DELETED!",
                             message="Account deletion flow failed",
                             page_object=account_deleted_page)
        account_deleted_page.click_continue()
