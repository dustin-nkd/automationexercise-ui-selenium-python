import allure

from pages.guest_page import GuestPage
from utilities.data_generator import DataGenerator


@allure.feature("Subcription")
def test_verify_subscription_in_home_page(driver, config):
    base_url = config.get('base_url')
    guest_page = GuestPage(driver)
    email = DataGenerator.unique_email("subcribe")

    with allure.step("Navigate to url 'https://automationexercise.com'"):
        guest_page.navigate_to(base_url)

    with allure.step("Verify that home page is visible successfully"):
        guest_page.navigate_to(base_url)

    with allure.step("Scroll down to footer"):
        pass

    with allure.step("Verify text 'SUBSCRIPTION'"):
        assert guest_page.footer.is_subcription_visible()

    with allure.step("Enter email address in input and click arrow button"):
        guest_page.footer.subcribe(email)

    with allure.step("Verify success message 'You have been successfully subscribed!' is visible"):
        assert guest_page.footer.is_success_message_visible()