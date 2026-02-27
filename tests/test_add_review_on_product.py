import allure

from utilities.assertions import assert_text_contains, assert_true


@allure.feature("Product")
@allure.story("Add Review on Product")
def test_add_review_on_product(app, config):
    """
    Test Case 21: Add review on product
    Ensures that users can successfully submit a review for a specific product.
    """
    base_url = config.get("base_url")
    target_product = "Blue Top"
    reviewer_name = "Dustin SDET"
    reviewer_email = "dustin_sdet@example.com"
    review_content = "Execellent product quality! Higly recommend to everyone."

    with allure.step("Launch browser and navigate to home page"):
        home_page = app.open_site(base_url)

    with allure.step("Click on 'Products' button"):
        products_page = home_page.header.click_products()

    with allure.step("Verify user is navigated to ALL PRODUCTS page successfully"):
        assert_true(products_page.is_products_page_visible(),
                    "All Products page is not visible", products_page)

    with allure.step(f"Click on 'View Product' fof '{target_product}'"):
        product_details_page = products_page.click_view_product_of(target_product)

    with allure.step("Verify 'Write Your Review' section is visible"):
        assert_true(product_details_page.is_review_section_visible(),
                    "Write Your Review' section is missing", product_details_page)

    with allure.step("Enter name, email, and review content"):
        product_details_page.enter_review_name(reviewer_name)
        product_details_page.enter_review_email(reviewer_email)
        product_details_page.enter_review_content(review_content)

    with allure.step("Click 'Submit' button"):
        product_details_page.click_submit()

    with allure.step("Verify success message 'Thank you for your review.'"):
        actual_message = product_details_page.get_review_success_message()
        assert_text_contains(actual_text=actual_message,
                             expected_text="Thank you for your review.",
                             message="Review submission success message mismatch",
                             page_object=product_details_page)
