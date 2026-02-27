import os

import allure

from utilities.assertions import assert_text_contains, assert_true
from utilities.data_generator import DataGenerator
from utilities.file_utils import wait_for_file_download


@allure.feature("Order Management")
@allure.story("Download Invoice")
def test_download_invoice_after_purchase_order(app, config, user_profile, download_dir):
    """
    Test Case 24: Download Invoice after purchase order
    Verifies the end-to-end flow from checkout to downloading the generated invoice.
    """
    username = DataGenerator.unique_email("buyer")
    email = DataGenerator.unique_email("buyer")
    base_url = config.get("base_url")

    with allure.step("Launch browser and navigate to home page"):
        home_page = app.open_site(base_url)

    with allure.step("Add products to cart and navigate to Cart page"):
        product_details = home_page.view_product("Blue Top")
        product_details.click_add_to_cart()
        cart_page = product_details.navigate_to_cart_via_modal()

    with allure.step("Verify cart page and proceed to checkout (guest)"):
        assert_true(cart_page.is_cart_page_visible(),
                    "Cart page not visible", cart_page)
        cart_page.proceed_to_checkout()
        login_page = cart_page.click_register_login()

    with allure.step("Create account to continue checkout"):
        login_page.enter_name(username)
        login_page.enter_signup_email(email)
        signup_page = login_page.click_signup()

        user_profile["name"] = username
        account_created_page = signup_page.create_account(user_profile)
        home_page = account_created_page.click_continue()

    with allure.step("Return to cart and proceed to checkout (logged in)"):
        cart_page = home_page.header.click_cart()
        checkout_page = cart_page.proceed_to_checkout()

    with allure.step("Verify details, enter comment and place order"):
        assert_true(checkout_page.is_checkout_page_valid(),
                    "Checkout details invalid", checkout_page)
        checkout_page.enter_description("Requesting invoice download.")
        payment_page = checkout_page.place_order()

    with allure.step("Enter payment details and confirm order"):
        payment_page.enter_payment_details(
            name_on_card=username,
            card_number="424242424242",
            cvc="311",
            expiry_month="12",
            expiry_year="2028"
        )
        order_placed_page = payment_page.click_pay_and_confirm()
        assert_text_contains(actual_text=order_placed_page.get_order_success_message(),
                             expected_text="Congratulations! Your order has been confirmed!",
                             message="Order failed for registered user",
                             page_object=order_placed_page)

    with allure.step("Dowload Invoice and verify file existence"):
        order_placed_page.download_invoice()
        invoice_file = wait_for_file_download(
            directory=download_dir,
            filename_contains="invoice"
        )

        assert_true(invoice_file is not None, "Invoice file was no found in download directory")
        assert_true(os.path.getsize(invoice_file) > 0, f"Downloaded file {invoice_file} is empty")

    with allure.step("Cleanup: Delete account"):
        home_page = order_placed_page.click_continue()
        account_deleted_page = home_page.delete_account()
        assert_text_contains(actual_text=account_deleted_page.get_account_deleted_message(),
                             expected_text="ACCOUNT DELETED",
                             message="Account deletion flow failed",
                             page_object=account_deleted_page)
        account_deleted_page.click_continue()
