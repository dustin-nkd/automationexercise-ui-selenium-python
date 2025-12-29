import allure

from pages.guest_page import GuestPage


@allure.feature("Test Cases")
def test_verify_test_cases_page(driver, config):
    base_url = config.get("base_url")
    guest_page = GuestPage(driver)

    with allure.step("Navigate to url 'https://automationexercise.com'"):
        guest_page.navigate_to(base_url)

    with allure.step("Verify that home page is visible successfully"):
        assert guest_page.is_home_page_visible()

    with allure.step("Click on 'Test Cases' button"):
        test_cases_page = guest_page.navigate_to_test_cases_page()

    with allure.step("Verify user is navigated to test cases page successfully"):
        assert test_cases_page.is_test_cases_page_visible()