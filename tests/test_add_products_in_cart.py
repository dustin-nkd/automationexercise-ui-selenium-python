import allure

from utilities.assertions import assert_true, assert_equal


@allure.feature("Cart")
@allure.story("Add Multiple Products to Cart")
def test_add_products_in_cart(app, config):
    """
    Test Case 12: Add Products in Cart
    Ensures that multiple products can be added and verified in the cart.
    """
    base_url = config.get("base_url")
    product1 = "Blue Top"
    product2 = "Men Tshirt"

    with allure.step("Launch browser and navigate to home page"):
        home_page = app.open_site(base_url)

    with allure.step("Verify taht home page is visible successfully"):
        assert_true(home_page.header.is_header_visible(),
                    "Home page failed to load", home_page)

    with allure.step("Click 'Products' button"):
        products_page = home_page.header.click_products()

    with allure.step(f"Hover over '{product1}' and click 'Add to cart'"):
        products_page.add_product_to_cart(product1)

    with allure.step("Click 'Continue Shopping' button"):
        products_page.continue_shopping()

    with allure.step(f"Hover over '{product2}' and click 'Add to cart'"):
        products_page.add_product_to_cart(product2)

    with allure.step("Click 'View Cart' button"):
        cart_page = products_page.click_view_cart()

    with allure.step("Verify both products are added to Cart"):
        actual_count = cart_page.get_cart_item_count()
        assert_equal(actual_count, 2, "Cart item count mismatch", cart_page)

    with allure.step("Verify their prices, quantity and total price"):
        assert_true(cart_page.are_all_cart_items_price_quantity_correct(),
                    "Price, quantity or total calculation is incorrect in cart", cart_page)
