import allure

from utilities.assertions import assert_true


@allure.feature("Cart")
@allure.story("Add to cart from Recommended items")
def test_add_to_cart_from_recommended_items(app, config):
    """
    Test Case 22: Add to cart from Recommended items
    Verifies that products from the recommended carousel can be added to the cart successfully.
    """
    base_url = config.get("base_url")
    target_item = "Blue Top"

    with allure.step("Launch browser and navigate to home page"):
        home_page = app.open_site(base_url)

    with allure.step("Scroll to bottom of page and verify 'RECOMMENDED ITEMS' visibility"):
        home_page.products.scroll_to_recommended_item()
        assert_true(home_page.products.is_recommended_itemes_visible(),
                    "'RECOMMENDED ITEMS' section is not visible", home_page)

    with allure.step(f"Add recommended product '{target_item}' to cart"):
        home_page.products.add_recommended_item_to_cart(target_item)

    with allure.step("Click on 'View Cart' button via modal"):
        cart_page = home_page.navigate_to_cart_via_modal()

    with allure.step(f"Verify that '{target_item}' is displayed in cart page"):
        assert_true(cart_page.is_item_visible(target_item),
                    f"Product '{target_item}' not found in cart", cart_page)
