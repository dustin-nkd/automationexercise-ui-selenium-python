import allure

from pages.guest_page import GuestPage


@allure.feature("Scroll")
def test_verify_scroll_up_using_arrow_button_and_scroll_down_functionality(driver, config):
    base_url = config.get("base_url")
    guest_page = GuestPage(driver)

    with allure.step("Navigate to url 'https://automationexercise.com'"):
        guest_page.navigate_to(base_url)

    with allure.step("Verify that home page is visible successfully"):
        assert guest_page.is_home_page_visible()

    with allure.step("Scroll down page to bottom"):
        pass

    with allure.step("Verify 'SUBSCRIPTION' is visible"):
        assert guest_page.footer.is_subscription_visible()

    with allure.step("Click on arrow at bottom right side to move upward"):
        guest_page.scroll_up.click_scroll_up()

    with allure.step(
            "Verify that page is scrolled up and 'Full-Fledged practice website for Automation Engineers' text is visible on screen"):
        assert guest_page.is_label_slider_visible()