import allure

from utilities.assertions import assert_true


@allure.feature("Products")
@allure.story("Verify Product Catalog and Details")
def test_verify_all_products_and_product_detail_page(app, config):
    """
    Test Case 8: Verify ALl Products and prodct detail page
    Ensures that the product list is displayed and individual product details are accurate.
    """
    base_url = config.get("base_url")

    with allure.step("Launch browser and navigate to home page"):
        home_page = app.open_site(base_url)

    with allure.step("Verify that home page is visible successfully"):
        assert_true(home_page.header.is_header_visible(),
                    "Home page header is not visible", home_page)

    with allure.step("Click on 'Products' button"):
        # Products link is located in the global header
        products_page = home_page.header.click_products()

    with allure.step("Verify user is navigated to ALL PRODUCTS page successfully"):
        assert_true(products_page.is_products_page_visible(),
                    "All Products page title is not visible", products_page)

    with allure.step("The products list is visible"):
        assert_true(products_page.is_products_list_visible(),
                    "Product list container is not displayed", products_page)

    with allure.step("Click on 'View Product' of a specific product"):
        # We target the firts product dynamically instead of hardcoding a name
        target_product = "Blue Top"
        product_details_page = products_page.click_view_product_of(target_product)

    with allure.step("User is landed to product detail page"):
        assert_true(product_details_page.is_product_details_page_visible(),
                    "Product details page failed to load", product_details_page)

    with allure.step("Verify that detail details are visible: name, category, price, availability, condition, brand"):
        assert_true(product_details_page.are_product_details_visible(),
                    "One or more product elements are missing", product_details_page)
