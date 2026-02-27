import allure

from utilities.assertions import assert_true, assert_text_contains


@allure.feature("Navigation")
@allure.story("Manual Scroll Up and Down")
def test_verify_scroll_up_without_arrow_button_and_scroll_down_functionality(app, config):
    """
    Test Case 26: Verify Scroll Up without 'Arrow' button and Scroll Down functionality
    Verifies that manual scrolling using JavaScript or Actions works correctly.
    """
    base_url = config.get("base_url")
    expected_slider_text = "Full-Fledged practice website for Automation Engineers"

    with allure.step("Launch browser and navigate to home page"):
        home_page = app.open_site(base_url)

    with allure.step("Verify taht home page is visible successfully"):
        assert_true(home_page.header.is_header_visible(),
                    "Home page failed to load", home_page)

    with allure.step("Scroll down page to bottom"):
        home_page.footer.scroll_to_footer()

    with allure.step("Verify 'SUBSCRIPTION' label is visible"):
        assert_true(home_page.footer.is_subscription_label_visible(),
                    "Subscription footer not visible after scrolling down", home_page)

    with allure.step("Scroll up page to top manually"):
        home_page.header.scroll_up()

    with allure.step("Verify that page is scrolled up and slider text is visible"):
        actual_text = home_page.get_slider_text()
        assert_text_contains(actual_text=actual_text,
                             expected_text=expected_slider_text,
                             message="Page did not scroll up manually to the slide section",
                             page_object=home_page)
