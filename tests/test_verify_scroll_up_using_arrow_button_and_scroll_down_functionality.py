import allure

from utilities.assertions import assert_true, assert_text_contains


@allure.feature("Navigation")
@allure.story("Scroll Up and Down Functionality")
def test_verify_scroll_up_using_arrow_button_and_scroll_down_functionality(app, config):
    """
    Test Case 25: Verify Scroll Up using 'Arrow' button and Scroll Down functionality
    """
    base_url = config.get("base_url")
    expected_slider_text = "Full-Fledged practice website for Automation Engineers"

    with allure.step("Launch browser and navigate to home page"):
        home_page = app.open_site(base_url)

    with allure.step("Verify that home page is visible successfully"):
        assert_true(home_page.header.is_header_visible(),
                    "Home page failed to load", home_page)

    with allure.step("Scroll down page to bottom"):
        home_page.footer.scroll_to_footer()

    with allure.step("Verify 'SUBSCRIPTION' is visible"):
        assert_true(home_page.footer.is_subscription_label_visible(),
                    "Subscription footer not visible after scrolling down", home_page)

    with allure.step("Click on arrow at bottom right side to move upward"):
        home_page.scroll_up.click_scroll_up()

    with allure.step("Verify that page is scrolled up and slider text is visible"):
        actual_text = home_page.get_slider_text()
        assert_text_contains(actual_text=actual_text,
                             expected_text=expected_slider_text,
                             message="Page did not scroll up correctly to the slider section",
                             page_object=home_page)
