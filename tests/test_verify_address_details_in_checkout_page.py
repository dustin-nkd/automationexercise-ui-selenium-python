import allure

from utilities.assertions import assert_true, assert_text_contains
from utilities.data_generator import DataGenerator


@allure.feature("Checkout")
@allure.story("Verify Address Details")
def test_verify_address_details_in_checkout_page(app, config, user_profile):
    """
    Test Case 23: Verify address details in checkout page
    """
    base_url = config.get("base_url")
    username = DataGenerator.unique_username("addr")
    email = DataGenerator.unique_email("addr")

    with allure.step("Launch browser and navigate to home page"):
        hom_page = app.open_site(base_url)

    with allure.step("Click 'Signup / Login' and create account"):
        login_page = hom_page.header.click_signup_login()
        login_page.enter_name(username)
        login_page.enter_signup_email(email)
        signup_page = login_page.click_signup()

        user_profile["name"] = username
        account_created_page = signup_page.create_account(user_profile)
        home_page = account_created_page.click_continue()

    with allure.step("Verify 'Logged in as username'"):
        assert_true(home_page.header.is_logged_user_visible(),
                    "User not logged in", home_page)

    with allure.step("Add products to cart and proceed to checkout"):
        product_details = home_page.view_product("Blue Top")
        product_details.click_add_to_cart()
        cart_page = product_details.navigate_to_cart_via_modal()
        checkout_page = cart_page.proceed_to_checkout()

    with allure.step("Verify Delivery Address matches registration details"):
        delivery_address = checkout_page.get_delivery_address_details()
        assert_text_contains(delivery_address[0], "Mr. Khanh Duy Nguyen", "Delivery Name mismatch")
        assert_text_contains(delivery_address[2], "70, Lu Gia street, Phu Tho ward", "Delivery Address1 mismatch")
        assert_text_contains(delivery_address[5], "Israel", "Delivery Country mismatch")

    with allure.step("Verify Billing Address matches registration details"):
        billing_address = checkout_page.get_billing_address_details()
        assert_text_contains(billing_address[0], "Mr. Khanh Duy Nguyen", "Billing Name mismatch")
        assert_text_contains(billing_address[2], "70, Lu Gia street, Phu Tho ward", "Billing Address1 mismatch")

    with allure.step("Click 'Delete Account' button"):
        account_deleted_page = home_page.header.click_delete_account()

    with allure.step("Verify 'ACCOUNT DELETED' and click 'Continue'"):
        assert_text_contains(actual_text=account_deleted_page.get_account_deleted_message(),
                             expected_text="ACCOUNT DELETED",
                             message="Account deletion flow failed",
                             page_object=account_deleted_page)
    account_deleted_page.click_continue()
