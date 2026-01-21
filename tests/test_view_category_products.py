import allure

from pages.guest_page import GuestPage
from utilities.assertions import assert_text_contains


@allure.feature("Category")
def test_view_category_products(driver, config):
    base_url = config.get("base_url")
    guest_page = GuestPage(driver)

    with allure.step("Navigate to url 'https://automationexercise.com'"):
        guest_page.navigate_to(base_url)

    with allure.step("Verify that categories are visible on left side bar"):
        assert guest_page.category_sidebar.is_visible()

    with allure.step("Click on 'Women' category"):
        guest_page.category_sidebar.expand_category("Women")

    with allure.step("Click on any category link under 'Women' category, for example: Dress"):
        guest_page.category_sidebar.click_sub_category("Dress")

    with allure.step("Verify that category page is displayed and confirm text 'WOMEN - TOPS PRODUCTS'"):
        actual_text = guest_page.category_sidebar.get_category_title()
        assert_text_contains(actual_text=actual_text,
                             expected_text="WOMEN - DRESS PRODUCTS",
                             message="Title not visible",
                             driver=driver)

    with allure.step("On left side bar, click on any sub-category link of 'Men' category"):
        guest_page.category_sidebar.expand_category("Men")
        guest_page.category_sidebar.click_sub_category("Jeans")

    with allure.step("Verify that user is navigated to that category page"):
        actual_text = guest_page.category_sidebar.get_category_title()
        assert_text_contains(actual_text=actual_text,
                             expected_text="MEN - JEANS PRODUCTS",
                             message="Title not visible",
                             driver=driver)