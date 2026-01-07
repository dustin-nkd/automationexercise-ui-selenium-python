import allure

from pages.guest_page import GuestPage


@allure.feature("Products")
def test_add_products_in_cart(driver, config):
    base_url = config.get("base_url")
    guest_page = GuestPage(driver)

    with allure.step("Navigate to url 'https://automationexercise.com'"):
        guest_page.navigate_to(base_url)

    with allure.step("Verify that home page is visible successfully"):
        assert guest_page.is_home_page_visible()

    with allure.step("Click 'Products' button"):
        products_page = guest_page.navigate_to_products_page()

    with allure.step("Hover over first product and click 'Add to cart'"):
        products_page.add_product_to_cart_by_item("Blue Top")

    with allure.step("Click 'Continue Shopping' button"):
        products_page.continue_shopping_after_add()

    with allure.step("Hover over second product and click 'Add to cart'"):
        products_page.add_product_to_cart_by_item("Men Tshirt")

    with allure.step("Click 'View Cart' button"):
        cart_page = products_page.click_view_cart()

    with allure.step("Verify both products are added to Cart"):
        assert cart_page.get_cart_item_count() == 2

    with allure.step("Verify their prices, quantity and total price"):
        assert cart_page.are_all_cart_items_price_quantity_correct()