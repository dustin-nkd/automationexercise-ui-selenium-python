import allure

from utilities.assertions import assert_text_contains, assert_true


@allure.feature("Product Brands")
@allure.story("View Brand Products")
def test_view_and_cart_brand_products(app, config):
    """
    Test Case 19: View & Cart Brand Products
    Verifies that brand-based filtering works correctly from the sidebar.
    """
    base_url = config.get("base_url")

    with allure.step("Launch browser and navigate to home page"):
        home_page = app.open_site(base_url)

    with allure.step("Click on 'Products' button"):
        products_page = home_page.header.click_products()

    with allure.step("Verify that Brands are visible on left side bar"):
        assert_true(products_page.category_sidebar.is_brands_list_visible(),
                    "Brands list is not visible in sidebar", products_page)

    with allure.step("Click on 'Polo' brand name"):
        products_page.category_sidebar.click_brand("Polo")

    with allure.step("Verify user navigated to brand page and 'BRAND - POLO PRODUCTS' is visible"):
        actual_text = products_page.category_sidebar.get_category_title()
        assert_text_contains(actual_text=actual_text,
                             expected_text="BRAND - POLO PRODUCTS",
                             message="Polo brand products page not loaded",
                             page_object=products_page)

    with allure.step("On the left side bar, click on 'Madame' brand link"):
        products_page.category_sidebar.click_brand("Madame")

    with allure.step("Verify user navigated to 'BRAND - MADAME PRODUCTS' page"):
        actual_text = products_page.category_sidebar.get_category_title()
        assert_text_contains(actual_text=actual_text,
                             expected_text="BRAND - MADAME PRODUCTS",
                             message="Madame brand products page not loaded",
                             page_object=products_page)
