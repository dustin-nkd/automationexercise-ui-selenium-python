import allure

from pages.guest_page import GuestPage


@allure.feature("Products")
def test_verify_all_products_and_product_detail_page(driver, config):
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

    with allure.step("The products list is visible"):
        assert products_page.is_products_list_visible()

    with allure.step("Click on 'View Product' of first product"):
        product_details_page = products_page.click_view_product_of("Blue Top")

    with allure.step("User is landed to product detail page"):
        assert product_details_page.is_product_details_page_visible()

    with allure.step(
            "Verify that detail detail is visible: product name, category, price, availability, condition, brand"):
        assert product_details_page.are_product_details_visible()