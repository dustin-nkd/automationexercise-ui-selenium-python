import allure

from utilities.assertions import assert_true


@allure.feature("Products")
@allure.story("Search Product Functionality")
def test_search_product(app, config):
    """
    Test Case 9: Search Product
    Verifies that searching for a product displays only relevant results.
    """
    base_url = config.get("base_url")
    search_keyword = "top"

    with allure.step("Launch browser and navigate to home page"):
        home_page = app.open_site(base_url)

    with allure.step("Verify that home page is visible successfully"):
        assert_true(home_page.header.is_header_visible(),
                    "Home page header is not visible", home_page)

    with allure.step("Click on 'Products' button"):
        # Navigation handled by Header component
        products_page = home_page.header.click_products()

    with allure.step("Verify user is navigated to ALL PRODUCTS page successfully"):
        assert_true(products_page.is_products_page_visible(),
                    "All Products page failed to load", products_page)

    with allure.step(f"Enter product name '{search_keyword}' in search input and click search button"):
        # Using the refactored search_product method
        products_page.search_product(search_keyword)

    with allure.step("Verify 'SEARCH PRODUCTS' header is visible"):
        assert_true(products_page.is_searched_products_visible(),
                    "'SEARCHED PRODUCTS' section is not displayed", products_page)

    with allure.step("Verify all the products related to search are visible"):
        # This checks if all displayed product names contain the keyword
        assert_true(products_page.are_all_products_related_to_search(search_keyword),
                    f"Some products found do not match the keyword: {search_keyword}", products_page)
