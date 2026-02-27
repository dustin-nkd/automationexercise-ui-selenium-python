import allure

from utilities.assertions import assert_true
from utilities.data_generator import DataGenerator


@allure.feature("Cart")
@allure.story("Search and Cart Persistence After Login")
def test_search_products_and_verify_cart_after_login(app, config, user_profile):
    """
    Test Case 20: Search Products and Verify Cart After Login
    Verifies that products added as a guest remain in the cart after registration/login.
    """
    base_url = config.get("base_url")
    search_keyword = "Jeans"
    username = DataGenerator.unique_username("persist")
    email = DataGenerator.unique_email("persist")

    with allure.step("Launch browser and navigate to home page"):
        home_page = app.open_site(base_url)

    with allure.step("Click on 'Products' button"):
        products_page = home_page.header.click_products()

    with allure.step("Verify user is navigated to ALL PRODUCTS page successfully"):
        assert_true(products_page.is_products_page_visible(),
                    "All Products page is not visible", products_page)

    with allure.step(f"Search for '{search_keyword}' and verify results"):
        products_page.search_product(search_keyword)
        assert_true(products_page.is_searched_products_visible(),
                    "'SEARCHED PRODUCTS' header not visible", products_page)
        assert_true(products_page.are_all_products_related_to_search(search_keyword),
                    f"Results not related to '{search_keyword}'", products_page)
        searched_products = products_page.get_displayed_product_names()

    with allure.step("Add all searched products to cart"):
        products_page.add_all_displayed_products_to_cart()

    with allure.step("Navigate to Cart and verify products are present"):
        cart_page = home_page.header.click_cart()
        assert_true(cart_page.are_products_in_cart(searched_products),
                    "Products not found in cart before login", cart_page)

    with allure.step("Register a new user (to trigger login session)"):
        login_page = home_page.header.click_signup_login()
        login_page.enter_name(username)
        login_page.enter_signup_email(email)
        signup_page = login_page.click_signup()

        user_profile["name"] = username
        account_created_page = signup_page.create_account(user_profile)
        home_page = account_created_page.click_continue()

    with allure.step("Go to Cart page again and verify products persist"):
        cart_page = home_page.header.click_cart()
        assert_true(cart_page.are_products_in_cart(searched_products),
                    "Products disappeared from cart after login", cart_page)
