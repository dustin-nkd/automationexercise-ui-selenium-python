import allure

from utilities.assertions import assert_true, assert_equal


@allure.feature("Cart")
@allure.story("Product Quantity Validation")
def test_verify_product_quantity_in_cart(app, config):
    """
    Test Case 13: Verify Product quantiy in Cart
    Ensures that the selected quantity on the details page matches the quantity in the cart.
    """
    base_url = config.get("base_url")
    target_product = "Blue Top"
    target_quantity = "4"

    with allure.step("Launch browser and navigate to home page"):
        home_page = app.open_site(base_url)

    with allure.step("Verify that home page is visible successfully"):
        assert_true(home_page.header.is_header_visible(),
                    "Home page failed to load", home_page)

    with allure.step(f"Click 'View Product' for '{target_product}' on home page"):
        # We navigate from home to product details via the product's view button
        product_details_page = home_page.view_product(target_product)

    with allure.step("Verify product detail is opened"):
        assert_true(product_details_page.is_product_details_page_visible(),
                    "Product details page not displayed", product_details_page)

    with allure.step(f"Increase quantity to {target_quantity}"):
        # This method handles clearing the field and typing the new value
        product_details_page.set_quantity(target_quantity)

    with allure.step("Click 'Add to cart' button"):
        product_details_page.click_add_to_cart()

    with allure.step("Click 'View Cart' button"):
        # Navigating via the shared Modal component
        cart_page = product_details_page.navigate_to_cart_via_modal()

    with allure.step("Verify that product is displayed in cart page with exact quantity"):
        actual_quantity = cart_page.get_quantity_of_item(target_product)
        assert_equal(actual_quantity, target_quantity,
                     f"Quantiy mismatch for {target_product}", cart_page)
