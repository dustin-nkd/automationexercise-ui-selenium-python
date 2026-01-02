import allure

from pages.guest_page import GuestPage


@allure.feature("Product")
def test_search_product(driver, config):
    base_url = config.get("base_url")
    guest_page = GuestPage(driver)

    with allure.step("Navigate to url 'https://automationexercise.com'"):
        guest_page.navigate_to(base_url)

    with allure.step("Verify that home page is visible successfully"):
        assert guest_page.is_home_page_visible()

    with allure.step("Click on 'Products' button"):
        products_page = guest_page.navigate_to_products_page()

    with allure.step("Verify user is navigated to ALL PRODUCTS page successfully"):
        assert products_page.is_products_page_visible()

    with allure.step("Enter product name in search input and click search button"):
        products_page.search("top")

    with allure.step("Verify 'SEARCHED PRODUCTS' is visible"):
        assert products_page.is_searched_products_visible()

    with allure.step("Verify all the products related to search are visible"):
        assert products_page.are_all_products_related_to_search("top")