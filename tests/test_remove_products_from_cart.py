import allure

from pages.guest_page import GuestPage


@allure.feature("Cart")
def test_remove_products_from_cart(driver, config):
    base_url = config.get("base_url")
    guest_page = GuestPage(driver)
    item = "Blue Top"

    with allure.step("Navigate to url 'https://automationexercise.com'"):
        guest_page.navigate_to(base_url)

    with allure.step("Verify that home page is visible successfully"):
        assert guest_page.is_home_page_visible()

    with allure.step("Add products to cart"):
        guest_page.products.add_product_to_cart_by_item(item)
        guest_page.add_to_cart_modal.click_continue_shopping()

    with allure.step("Click 'Cart' button"):
        cart_page = guest_page.navigate_to_cart_page()

    with allure.step("Verify that cart page is displayed"):
        assert cart_page.is_cart_page_visible()
        assert cart_page.is_cart_table_visible()

    with allure.step("Click 'X' button corresponding to particular product"):
        cart_page.remove_item(item)

    with allure.step("Verify that product is removed from the cart"):
        assert cart_page.is_item_removed(item)