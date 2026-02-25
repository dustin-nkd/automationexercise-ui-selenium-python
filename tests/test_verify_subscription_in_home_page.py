import allure

from utilities.assertions import assert_true, assert_text_contains
from utilities.data_generator import DataGenerator


@allure.feature("Subscription")
@allure.story("Verify Subscription in Home Page")
def test_verify_subscription_in_home_page(app, config):
    """
    Test Case 10: Verify Subscription in home page
    Ensures the newsletter subscription in the footer works correctly.
    """
    base_url = config.get("base_url")
    email = DataGenerator.unique_email("subscribe")

    with allure.step("Launch browser and navigate to home page"):
        home_page = app.open_site(base_url)

    with allure.step("Verify that home page is visible successfully"):
        assert_true(home_page.header.is_header_visible(),
                    "Home page failed to load", home_page)

    with allure.step("Scroll down to footer"):
        # We scroll to the subscription element to ensure it's interactable
        home_page.footer.scroll_to_footer()

    with allure.step("Verify text 'SUBSCRIPTION'"):
        assert_true(home_page.footer.is_subscription_label_visible(),
                    "'SUBSCRIPTION' label is not visible in footer", home_page)

    with allure.step("Enter email address and click subscribe"):
        home_page.footer.subscribe(email)

    with allure.step("Verify success message 'You have been successfully subscribed!'"):
        actual_msg = home_page.footer.get_success_message_text()
        assert_text_contains(actual_text=actual_msg,
                             expected_text="You have been successfully subscribed!",
                             message="Subscription success message mismatch",
                             page_object=home_page)
