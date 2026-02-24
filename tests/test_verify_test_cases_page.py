import allure

from utilities.assertions import assert_true


@allure.feature("Navigation")
@allure.story("Verify Test Cases Page")
def test_verify_test_cases_page(app, config):
    """
    Test Case 7: Verify Test Cases Page
    Ensures that the 'Test Cases' button correctly redirects the user.
    """
    base_url = config.get("base_url")

    with allure.step("Launch browser and navigate to home page"):
        home_page = app.open_site(base_url)

    with allure.step("Verify that home page is visibile successfully"):
        # We use the header as a proxy for home page presence
        assert_true(home_page.header.is_header_visible(),
                    "Home page header is not visible", home_page)

    with allure.step("Click on 'Test Cases' button"):
        # The 'Test Cases' link is in the header
        test_cases_page = home_page.header.click_test_cases()

    with allure.step("Verify user is navigated to test cases page successfully"):
        # Checking for the presence of the 'TEST CASES' title or specific indicator
        assert_true(test_cases_page.is_test_cases_page_visible(),
                    "Test Cases page is not visible after navigation", test_cases_page)
