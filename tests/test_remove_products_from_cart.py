import allure

from utilities.assertions import assert_true


@allure.feature("Cart")
@allure.story("Remove Products From Cart")
def test_remove_products_from_cart(app, config):
    """
    Test Case 17: Remove Products From Cart
    Ensures taht clicking the 'X' button removes the specific item from the cart table.
    """
    base_url = config.get("base_url")
    target_item = "Blue Top"

    with allure.step("Launch browser and navigate to url"):
        home_page = app.open_site(base_url)

    with allure.step("Verify that home page is visible successfully"):
        assert_true(home_page.header.is_header_visible(),
                    "Home page header not visible", home_page)

    with allure.step(f"Add product '{target_item}' to cart"):
        product_details = home_page.view_product(target_item)
        product_details.click_add_to_cart()
        product_details.add_to_cart_modal.click_continue_shopping()

    with allure.step("Click 'Cart' button"):
        cart_page = home_page.header.click_cart()

    with allure.step("Verify that cart page is displayed"):
        assert_true(cart_page.is_cart_page_visible(),
                    "Cart page is not displayed", cart_page)
        assert_true(cart_page.is_cart_table_visible(),
                    "Cart table is not visible", cart_page)

    with allure.step(f"Click 'X' button corresponding to '{target_item}'"):
        cart_page.remove_item(target_item)

    with allure.step(f"Verify that '{target_item}' is removed from the cart"):
        assert_true(cart_page.is_item_removed(target_item),
                    f"Product '{target_item}' was not removed from cart", cart_page)
