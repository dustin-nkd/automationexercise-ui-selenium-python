import os.path

import allure

from pages.guest_page import GuestPage
from utilities.assertions import assert_text_contains
from utilities.data_generator import DataGenerator
from utilities.file_utils import wait_for_file_download


@allure.feature("Invoice")
def test_download_invoice_after_purchase_order(driver, config, download_dir):
    base_url = config.get("base_url")
    guest_page = GuestPage(driver)
    name = DataGenerator.unique_username("user")
    email = DataGenerator.unique_email("email")

    with allure.step("Navigate to url 'https://automationexercise.com'"):
        guest_page.navigate_to(base_url)

    with allure.step("Verify that home page is visible successfully"):
        assert guest_page.is_home_page_visible()

    with allure.step("Add products to cart"):
        guest_page.add_product_to_cart_by_item_from_home("Blue Top")
        guest_page.add_to_cart_modal.click_view_cart()
        cart_page = guest_page.navigate_to_cart_page()

    with allure.step("Click 'Cart' button"):
        cart_page = guest_page.navigate_to_cart_page()

    with allure.step("Verify that cart page is displayed"):
        assert cart_page.is_cart_page_visible()

    with allure.step("Click Proceed To Checkout"):
        cart_page.proceed_to_checkout()

    with allure.step("Click 'Signup / Login' button"):
        login_page = cart_page.click_register_login()

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

    with allure.step("Click 'Cart' button"):
        cart_page = guest_page.navigate_to_cart_page()

    with allure.step("Click 'Proceed To Checkout' button"):
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

    with allure.step("Click 'Download Invoice' button and verify invoice is downloaded successfully."):
        order_placed_page.download_invoice()
        invoice_file = wait_for_file_download(
            directory=download_dir,
            filename_contains="invoice"
        )
        assert invoice_file is not None, "Invoice file was not downloaded"
        assert os.path.getsize(invoice_file) > 0, "Invoice file is empty"

    with allure.step("Click 'Continue' button"):
        home_page = order_placed_page.click_continue()

    with allure.step("Click 'Delete Account' button"):
        account_deleted_page = home_page.delete_account()

    with allure.step("Verify 'ACCOUNT DELETED!' and click 'Continue' button"):
        actual_text = account_deleted_page.get_account_deleted_message()
        assert_text_contains(actual_text=actual_text,
                             expected_text="ACCOUNT DELETED!",
                             message="ACCOUNT DELETED! is not visible",
                             driver=driver)
        account_deleted_page.click_continue()