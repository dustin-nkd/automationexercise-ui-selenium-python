import allure

from utilities.assertions import assert_true, assert_text_contains
from utilities.data_generator import DataGenerator


@allure.feature("Subscription")
@allure.story("Verify Subscription in Cart Page")
def test_verify_subscription_in_cart_page(app, config):
    """
    Test Case 11: Verify Subscription in Cart page
    Ensures that the subscription feature works correctly when accessed from the Cart page.
    """
    base_url = config.get("base_url")
    email = DataGenerator.unique_email("cart_subscribe")

    with allure.step("Launch browser and navigate to home page"):
        home_page = app.open_site(base_url)

    with allure.step("Verify that home page is visible successfully"):
        assert_true(home_page.header.is_header_visible(),
                    "Home page failed to load", home_page)

    with allure.step("Click 'Cart' button"):
        # Navigation via Header
        cart_page = home_page.header.click_cart()

    with allure.step("Scroll down to footer"):
        # Reusing the same FooterComponent method
        cart_page.footer.scroll_to_footer()

    with allure.step("Verify text 'SUBSCRIPTION'"):
        assert_true(cart_page.footer.is_subscription_label_visible(),
                    "'SUBSCRIPTION' label not found on Cart page footer", cart_page)

    with allure.step("Enter email address and click subscribe button"):
        cart_page.footer.subscribe("email")

    with allure.step("Verify success message 'You have been successfully subscribed!' is visible"):
        actual_msg = cart_page.footer.get_success_message_text()
        assert_text_contains(actual_text=actual_msg,
                             expected_text="You have been successfully subscribed!",
                             message="Subscription success message mismatch",
                             page_object=home_page)
