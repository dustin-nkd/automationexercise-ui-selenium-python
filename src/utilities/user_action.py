from pages.guest_page import GuestPage
from utilities.data_generator import DataGenerator


def register_user(driver, base_url, user_profile):
    username = DataGenerator.unique_username("login")
    email = DataGenerator.unique_email("login")
    password = user_profile["password"]

    guest_page = GuestPage(driver)
    guest_page.navigate_to(base_url)

    login_page = guest_page.navigate_to_signup_login_page()
    login_page.enter_name(username)
    login_page.enter_signup_email(email)

    signup_page = login_page.click_signup()

    signup_page.select_title(user_profile["title"])
    signup_page.enter_name(username)
    signup_page.enter_password(password)

    dob = user_profile["date_of_birth"]
    signup_page.select_date_of_birth(dob["day"], dob["month"], dob["year"])

    personal = user_profile["personal_info"]
    signup_page.enter_first_name(personal["first_name"])
    signup_page.enter_last_name(personal["last_name"])
    signup_page.enter_company(personal["company"])

    address = user_profile["address"]
    signup_page.enter_address(address["address1"])
    signup_page.enter_address2(address["address2"])
    signup_page.select_country(address["country"])
    signup_page.enter_state(address["state"])
    signup_page.enter_city(address["city"])
    signup_page.enter_zipcode(address["zipcode"])

    contact = user_profile["contact"]
    signup_page.enter_mobile_number(contact["mobile_number"])

    account_created_page = signup_page.click_create_account()

    home_page = account_created_page.click_continue()
    home_page.logout()

    return {
        "email": email,
        "password": password,
        "username": username
    }