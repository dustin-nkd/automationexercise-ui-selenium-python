import allure

from pages.guest_page import GuestPage


@allure.feature("Product")
def test_verify_product_quantity_in_cart(driver, config):
    base_url = config.get("base_url")
    guest_page = GuestPage(driver)
    quantity = "4"

    with allure.step("Navigate to url 'https://automationexercise.com'"):
        guest_page.navigate_to(base_url)

    with allure.step("Verify that home page is visible successfully"):
        assert guest_page.is_home_page_visible()

    with allure.step("Click 'View Product' for any product on home page"):
        product_details_page = guest_page.view_product_from_home("Blue Top")

    with allure.step("Verify product detail is opened"):
        assert product_details_page.are_product_details_visible()

    with allure.step("Increase quantity to 4"):
        product_details_page.set_quantity(quantity)

    with allure.step("Click 'Add to cart' button"):
        pass

    with allure.step("Click 'View Cart' button"):
        cart_page = product_details_page.add_to_cart_and_view_cart()

    with allure.step("Verify that product is displayed in cart page with exact quantity"):
        assert cart_page.get_quantity_of_item("Blue Top") == quantity