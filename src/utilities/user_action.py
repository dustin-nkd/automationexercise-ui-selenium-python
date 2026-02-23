from utilities.data_generator import DataGenerator
from utilities.logger import get_logger

logger = get_logger(__name__)


def register_user(app, base_url, user_profile):
    """
    Business action to register a new user via the UI.
    Now uses the 'app' (Navigator) fixture directly.
    """
    logger.info("Starting background user registration process")

    # 1. Open Site directly from the app controller
    home_page = app.open_site(base_url)

    # 2. Navigate to Log in/Signup Page via Header
    login_page = home_page.header.click_signup_login()

    # 3. Generate unique credentials
    username = DataGenerator.unique_username("user")
    email = DataGenerator.unique_email("reg")
    password = user_profile["password"]

    logger.info(f"Registerting user with email: {email}")

    # 4. Initial Sigup
    login_page.enter_name(username)
    login_page.enter_signup_email(email)
    signup_page = login_page.click_signup()

    # 5. Fill Signup Form using high-level method
    user_profile["name"] = username
    account_created_page = signup_page.create_account(user_profile)

    # 6. Finalize and Clean up
    home_page = account_created_page.click_continue()
    home_page.header.click_logout()

    logger.info("User registration completed successfully")

    return {
        "email": email,
        "password": password,
        "username": username
    }
