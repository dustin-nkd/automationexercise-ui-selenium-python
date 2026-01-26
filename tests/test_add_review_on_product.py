import allure

from pages.guest_page import GuestPage
from utilities.assertions import assert_text_contains


@allure.feature("Review")
def test_add_review_on_product(driver, config):
    base_url = config.get("base_url")
    guest_page = GuestPage(driver)

    with allure.step("Navigate to url 'https://automationexercise.com'"):
        guest_page.navigate_to(base_url)

    with allure.step("Click on 'Products' button"):
        products_page = guest_page.navigate_to_products_page()

    with allure.step("Verify user is navigated to ALL PRODUCTS page successfully"):
        assert products_page.is_products_page_visible()

    with allure.step("Click on 'View Product' button"):
        product_details_page = products_page.click_view_product_of("Blue Top")

    with allure.step("Verify 'Write Your Review' is visible"):
        assert product_details_page.is_review_section_visible()

    with allure.step("Enter name, email and review"):
        product_details_page.enter_review_name("Dustin")
        product_details_page.enter_review_email("thankyou@mail.com")
        product_details_page.enter_review_content("Good")

    with allure.step("Click 'Submit' button"):
        product_details_page.click_submit()

    with allure.step("Verify success message 'Thank you for your review.'"):
        actual_text = product_details_page.get_success_message()
        assert_text_contains(actual_text=actual_text,
                             expected_text="Thank you for your review.",
                             message="Message is not visible",
                             driver=driver)