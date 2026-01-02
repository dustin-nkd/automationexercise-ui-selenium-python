import allure

from pages.guest_page import GuestPage
from utilities.data_generator import DataGenerator


@allure.feature("Subscription")
def test_verify_subcription_in_cart_page(driver, config):
    base_url = config.get("base_url")
    guest_page = GuestPage(driver)
    email = DataGenerator.unique_email("subscribe")

    with allure.step("Navigate to url 'https://automationexercise.com'"):
        guest_page.navigate_to(base_url)

    with allure.step("Verify that home page is visible successfully"):
        guest_page.is_home_page_visible()

    with allure.step("Click 'Cart' button"):
        cart_page = guest_page.navigate_to_cart_page()

    with allure.step("Scroll down to footer"):
        pass

    with allure.step("Verify text 'SUBSCRIPTION'"):
        assert cart_page.footer.is_subscription_visible()

    with allure.step("Enter email address in input and click arrow button"):
        cart_page.footer.subscribe(email)

    with allure.step("Verify success message 'You have been successfully subscribed!' is visible"):
        assert cart_page.footer.is_success_message_visible()