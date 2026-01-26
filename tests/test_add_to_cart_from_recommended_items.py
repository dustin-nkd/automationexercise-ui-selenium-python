import allure

from pages.cart_page import CartPage
from pages.guest_page import GuestPage


@allure.feature("Product")
def test_add_to_cart_from_recommended_items(driver, config):
    base_url = config.get("base_url")
    guest_page = GuestPage(driver)

    with allure.step("Navigate to url 'https://automationexercise.com'"):
        guest_page.navigate_to(base_url)

    with allure.step("Scroll to bottom of page"):
        guest_page.products.add_recommended_item_to_cart("Winter Top")

    with allure.step("Verify 'RECOMMENDED ITEMS' are visible"):
        assert guest_page.products.is_recommened_itemes_visible()

    with allure.step("Click on 'View Cart' button"):
        guest_page.add_to_cart_modal.click_view_cart()
        cart_page = CartPage(driver)

    with allure.step("Verify that product is displayed in cart page"):
        assert cart_page.is_item_visible("Winter Top")