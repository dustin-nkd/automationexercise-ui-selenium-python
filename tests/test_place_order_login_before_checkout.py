import allure

from pages.guest_page import GuestPage
from utilities.assertions import assert_text_contains


@allure.feature("Order")
def test_place_order_login_before_checkout(driver, config, logged_in_user):
    home_page = logged_in_user
    guest_page = GuestPage(driver)

    with allure.step("Verify 'Logged in as username' at top"):
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
        checkout_page = cart_page.proceed_to_checkout()

    with allure.step("Verify Address Details and Review Your Order"):
        assert checkout_page.is_checkout_page_valid()

    with allure.step("Enter description in comment text area and click 'Place Order'"):
        checkout_page.enter_description("Feedback")
        payment_page = checkout_page.place_order()

    with allure.step("Enter payment details: Name on Card, Card Number, CVC, Expiration date"):
        payment_page.enter_payment_details(
            name_on_card="Nguyen Khanh Duy",
            card_number="123-45-67",
            cvc="123",
            expiry_month="12",
            expiry_year="2020"
        )

    with allure.step("Click 'Pay and Confirm Order' button"):
        order_placed_page = payment_page.click_pay_and_confirm()

    with allure.step("Verify success message 'Your order has been placed successfully!'"):
        actual_text = order_placed_page.get_order_success_message()
        assert_text_contains(actual_text=actual_text,
                             expected_text="Congratulations! Your order has been confirmed!",
                             message="Your order has been placed failed",
                             driver=driver)

    with allure.step("Click 'Delete Account' button"):
        home_page = order_placed_page.click_continue()

    with allure.step("Verify 'ACCOUNT DELETED!' and click 'Continue' button"):
        account_deleted_page = home_page.delete_account()
        actual_text = account_deleted_page.get_account_deleted_message()
        assert_text_contains(actual_text=actual_text,
                             expected_text="ACCOUNT DELETED!",
                             message="ACCOUNT DELETED! is not visible",
                             driver=driver)
        account_deleted_page.click_continue()