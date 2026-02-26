import allure

from utilities.assertions import assert_text_contains, assert_true


@allure.feature("Product Category")
@allure.story("View Category Products")
def test_view_category_products(app, config):
    """
    Test Case 18: View Category Products
    Verifies that products are correctly filtered when selecting categories from the sidebar.
    """
    base_url = config.get("base_url")

    with allure.step("Launch browser and navigate to home page"):
        home_page = app.open_site(base_url)

    with allure.step("Verify that categories are visible on left side bar"):
        assert_true(home_page.category_sidebar.is_sidebar_visible(),
                    "Category sidebar is not visible", home_page)

    with allure.step("Click on 'Women' category and select 'Dress'"):
        home_page.category_sidebar.expand_category("Women")
        home_page.category_sidebar.click_sub_category("Dress")

    with allure.step("Verify taht category page is displayed and confirms 'WOMEN - DRESS PRODUCT'"):
        actual_text = home_page.category_sidebar.get_category_title()
        assert_text_contains(actual_text=actual_text,
                             expected_text="WOMEN - DRESS PRODUCT",
                             message="Category title mismatch for Women-Dress",
                             page_object=home_page)

    with allure.step("On the left side bar, click on 'Men' -> 'Jeans'"):
        home_page.category_sidebar.expand_category("Men")
        home_page.category_sidebar.click_sub_category("Jeans")

    with allure.step("Verify that user is navigated to 'MEN - JEANS PRODUCTS' page"):
        actual_text = home_page.category_sidebar.get_category_title()
        assert_text_contains(actual_text=actual_text,
                             expected_text="MEN - JEANS PRODUCTS",
                             message="Category title mismatch for Men-Jeans",
                             page_object=home_page)
