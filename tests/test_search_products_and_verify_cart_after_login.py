import allure

from pages.guest_page import GuestPage
from utilities.data_generator import DataGenerator


@allure.feature("Search")
def test_search_products_and_verify_cart_after_login(driver, config):
    base_url = config.get("base_url")
    guest_page = GuestPage(driver)
    name = DataGenerator.unique_username("user")
    email = DataGenerator.unique_email("user")

    with allure.step("Navigate to url 'https://automationexercise.com'"):
        guest_page.navigate_to(base_url)

    with allure.step("Click on 'Products' button"):
        products_page = guest_page.navigate_to_products_page()

    with allure.step("Verify user is navigated to ALL PRODUCTS page successfully"):
        assert products_page.is_products_page_visible()

    with allure.step("Enter product name in search input and click search button"):
        products_page.search("Jeans")

    with allure.step("Verify 'SEARCHED PRODUCTS' is visible"):
        assert products_page.is_searched_products_visible()

    with allure.step("Verify all the products related to search are visible"):
        assert products_page.are_all_products_related_to_search("Jeans")
        searched_products = products_page.get_displayed_product_names()

    with allure.step("Add those products to cart"):
        products_page.add_all_displayed_products_to_cart()

    with allure.step("Click 'Cart' button and verify that products are visible in cart"):
        cart_page = guest_page.navigate_to_cart_page()
        assert cart_page.are_products_in_cart(searched_products)

    with allure.step("Click 'Signup / Login' button and submit login details"):
        login_page = guest_page.navigate_to_signup_login_page()
        signup_page = login_page.sign_up(name, email)
        signup_page.create_account(config["user_profile"])

    with allure.step("Again, go to Cart page"):
        cart_page = guest_page.navigate_to_cart_page()

    with allure.step("Verify that those products are visible in cart after login as well"):
        assert cart_page.are_products_in_cart(searched_products)