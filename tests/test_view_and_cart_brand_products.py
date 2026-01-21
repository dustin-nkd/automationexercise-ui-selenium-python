import allure

from pages.guest_page import GuestPage
from utilities.assertions import assert_text_contains


@allure.feature("Category")
def test_view_and_cart_brand_products(driver, config):
    base_url = config.get("base_url")
    guest_page = GuestPage(driver)

    with allure.step("Navigate to url 'https://automationexercise.com'"):
        guest_page.navigate_to(base_url)

    with allure.step("Click on 'Products' button"):
        products_page = guest_page.navigate_to_products_page()

    with allure.step("Verify that Brands are visible on left side bar"):
        assert products_page.category_sidebar.is_brands_list_visible()

    with allure.step("Click on any brand name"):
        products_page.category_sidebar.click_brand("Polo")

    with allure.step("Verify that user is navigated to brand page and brand products are displayed"):
        actual_text = products_page.category_sidebar.get_category_title()
        assert_text_contains(actual_text=actual_text,
                             expected_text="BRAND - POLO PRODUCTS",
                             message="Title not visible",
                             driver=driver)

    with allure.step("On left side bar, click on any other brand link"):
        products_page.category_sidebar.click_brand("Madame")

    with allure.step("Verify that user is navigated to that brand page and can see products"):
        actual_text = products_page.category_sidebar.get_category_title()
        assert_text_contains(actual_text=actual_text,
                             expected_text="BRAND - MADAME PRODUCTS",
                             message="Title not visible",
                             driver=driver)