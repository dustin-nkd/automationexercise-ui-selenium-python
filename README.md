> [![Built with ChatGPT](https://img.shields.io/badge/Built%20with-ChatGPT-74aa9c?style=flat&logo=openai&logoColor=white)](https://chatgpt.com)
> _This project was built with the assistance of [ChatGPT](https://chatgpt.com)._

# 🚀 Automation Exercise — UI Test Automation Framework (Python)

Enterprise-grade UI automation framework built with **Python, Selenium, Pytest, and Allure**, targeting [automationexercise.com](https://automationexercise.com). Follows **Component-based Page Object Model (POM)** and real-world SDET best practices.

---

## 📌 Tech Stack

| Technology | Version | Purpose |
|---|---|---|
| Python | 3.10+ | Programming language |
| Selenium WebDriver | 4.41.0 | Browser automation |
| Pytest | 9.0.2 | Test framework & fixtures |
| Allure Pytest | 2.15.3 | Test reporting |
| pytest-xdist | 3.8.0 | Parallel test execution |
| pytest-rerunfailures | 16.1 | Auto-retry flaky tests |
| webdriver-manager | 4.0.2 | Automatic driver binary management |
| PyYAML | 6.0.3 | Config & test data loading |
| python-dotenv | 1.2.2 | Environment variable management |

---

## 📂 Project Structure

```text
.
├── src/
│   ├── components/                     # Reusable UI components
│   │   ├── add_to_cart_modal_component.py
│   │   ├── category_sidebar_component.py
│   │   ├── footer_component.py
│   │   ├── header_component.py
│   │   ├── home_products_component.py
│   │   └── scroll_up_component.py
│   │
│   ├── configs/
│   │   └── config.yaml                 # Base configuration
│   │
│   ├── pages/                          # Page Object classes
│   │   ├── base_page.py                # Base class for all Pages + Components
│   │   ├── navigator.py                # Application Controller (entry point)
│   │   ├── home_page.py
│   │   ├── login_page.py
│   │   ├── signup_page.py
│   │   ├── products_page.py
│   │   ├── product_details_page.py
│   │   ├── cart_page.py
│   │   ├── checkout_page.py
│   │   ├── payment_page.py
│   │   ├── order_placed_page.py
│   │   ├── contact_us_page.py
│   │   ├── test_cases_page.py
│   │   ├── account_created_page.py
│   │   └── account_deleted_page.py
│   │
│   ├── test_cases/
│   │   └── automationexercise_testcases.json
│   │
│   └── utilities/
│       ├── assertions.py               # Custom assertions with Allure attachment on failure
│       ├── config_reader.py            # YAML config loader with env merging & caching
│       ├── data_generator.py           # Dynamic test data generation
│       ├── data_loader.py              # YAML test data loader
│       ├── file_utils.py               # File handling utilities
│       ├── logger.py                   # Colorized rotating logger
│       ├── user_action.py              # Reusable business flows (register_user)
│       └── webdriver_factory.py        # WebDriver factory (local + remote)
│
├── tests/
│   ├── conftest.py                     # Pytest fixtures & hooks
│   ├── test_register_user.py
│   ├── test_login_user_with_correct_email_and_password.py
│   ├── test_login_user_with_incorrect_email_and_password.py
│   ├── test_logout_user.py
│   ├── test_register_user_with_existing_email.py
│   ├── test_contact_us_form.py
│   ├── test_verify_test_cases_page.py
│   ├── test_verify_all_products_and_product_detail_page.py
│   ├── test_search_product.py
│   ├── test_verify_subscription_in_home_page.py
│   ├── test_verify_subcription_in_cart_page.py
│   ├── test_add_products_in_cart.py
│   ├── test_verify_product_quantity_in_cart.py
│   ├── test_place_order_register_while_checkout.py
│   ├── test_place_order_register_before_checkout.py
│   ├── test_place_order_login_before_checkout.py
│   ├── test_remove_products_from_cart.py
│   ├── test_view_category_products.py
│   ├── test_view_and_cart_brand_products.py
│   ├── test_search_products_and_verify_cart_after_login.py
│   ├── test_add_review_on_product.py
│   ├── test_add_to_cart_from_recommended_items.py
│   ├── test_verify_address_details_in_checkout_page.py
│   ├── test_download_invoice_after_purchase_order.py
│   ├── test_verify_scroll_up_using_arrow_button_and_scroll_down_functionality.py
│   └── test_verify_scroll_up_without_arrow_button_and_scroll_down_functionality.py
│
├── test_data/
│   ├── user_data.yaml                  # Static user profiles & test data
│   └── upload/                         # Files used for upload tests
│
├── reports/
│   └── allure-results/                 # Allure raw results (auto-generated)
│
├── logs/
│   └── test_run.log                    # Rotating log file (auto-generated)
│
├── pytest.ini                          # Pytest configuration
├── pyproject.toml                      # Project metadata & dependencies
├── requirements.txt                    # Pinned dependencies
└── README.md
```

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│                    Test Layer                       │
│  test_*.py — pure test logic, no WebDriver calls    │
│  uses: app fixture (Navigator) + custom assertions  │
└──────────────────────┬──────────────────────────────┘
                       │ uses
┌──────────────────────▼──────────────────────────────┐
│               Business Flow Layer                   │
│  user_action.py — register_user()                   │
│  conftest.py fixtures — registered_user,            │
│                          logged_in_user             │
└──────────────────────┬──────────────────────────────┘
                       │ uses
┌──────────────────────▼──────────────────────────────┐
│           Page Object + Component Layer             │
│  Navigator  — Application Controller / Entry Point  │
│  BasePage   — shared interactions & component init  │
│  Pages      — page-specific actions & locators      │
│  Components — HeaderComponent, FooterComponent,     │
│               CategorySidebarComponent, etc.        │
└──────────────────────┬──────────────────────────────┘
                       │ uses
┌──────────────────────▼──────────────────────────────┐
│             Infrastructure Layer                    │
│  WebDriverFactory — local & remote driver setup     │
│  ConfigReader     — YAML config with env merging    │
│  DataGenerator    — dynamic test data               │
│  Logger           — colorized rotating file logs    │
└─────────────────────────────────────────────────────┘
```

### Navigation Flow

```python
# conftest.py provides the app fixture (Navigator)
def test_example(app, config):
    home_page = app.open_site(config["base_url"])        # Navigator → HomePage
    login_page = home_page.header.click_signup_login()   # Header handles navigation
    home_page = login_page.login(email, password)        # LoginPage returns HomePage
```

---

## 🧠 Design Principles

- **Page Object Model (POM)** — each page has its own class with locators and actions
- **Component Object Pattern** — shared UI (`HeaderComponent`, `FooterComponent`, `CategorySidebarComponent`) extracted and reused across all pages
- **Navigator (Application Controller)** — centralized entry point, resolves circular import issues cleanly
- **DRY** — no duplicated locators or test logic
- **KISS** — simple, readable test code; no over-engineering
- **YAGNI** — only implement what tests actually need
- **SRP** — each class has a single responsibility

### Key Design Decisions

**Components are initialized in `BasePage`** — every Page gets `header`, `footer`, `add_to_cart_modal`, etc. automatically:

```python
class BasePage:
    def __init__(self, driver):
        self.header = HeaderComponent(self)
        self.footer = FooterComponent(self)
        self.add_to_cart_modal = AddToCartComponent(self)
        self.category_sidebar = CategorySidebarComponent(self)
        self.scroll_up = ScrollUpComponent(self)
```

**`Navigator` solves circular imports** — Pages access other Pages only through `Navigator` via a lazy-loaded property, never via direct cross-imports:

```python
@property
def navigate(self):
    from pages.navigator import Navigator   # lazy import — no circular dependency
    if self._navigate is None:
        self._navigate = Navigator(self.driver)
    return self._navigate
```

**Custom assertions attach evidence to Allure on failure** — no silent failures:

```python
assert_text_contains(actual, expected, message, page_object=page)
# On failure → attaches: comparison text + current URL + screenshot to Allure report
```

---

## ⚙️ Prerequisites

- **Python 3.10+** — `python --version`
- **Chrome / Firefox / Edge** browser installed
- **Allure CLI** for viewing reports — [installation guide](https://allurereport.org/docs/install/)

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/automationexercise-ui-selenium-python.git
cd automationexercise-ui-selenium-python
```

### 2. Create virtual environment

```bash
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔧 Configuration

Main config file: `src/configs/config.yaml`

```yaml
browser: chrome        # chrome | firefox | edge
headless: false        # true for CI/CD pipelines
implicit_wait: 8       # global implicit wait in seconds
remote_url: null       # Selenium Grid URL (null = run locally)
base_url: "https://automationexercise.com"
```

### Environment-specific overrides

Create `src/configs/<env>.yaml` to override base config values:

```yaml
# src/configs/staging.yaml
base_url: "https://staging.automationexercise.com"
headless: true
```

Then run with:

```bash
pytest --env=staging
```

`ConfigReader` deep-merges the environment file over base config — values not overridden are preserved from `config.yaml`.

### Test Data

Static profiles are loaded from `test_data/user_data.yaml`:

```yaml
default_registration_profile:
  password: "password123"
  title: "mr"
  name: "Dustin"
  date_of_birth:
    day: "26"
    month: "6"
    year: "1999"
  personal_info:
    first_name: "Khanh Duy"
    last_name: "Nguyen"
    company: "Trulioo"
  address:
    address1: "70, Lu Gia street, Phu Tho ward"
    country: "Israel"
    ...
```

Dynamic data (unique emails, usernames) is generated at runtime via `DataGenerator`:

```python
email    = DataGenerator.unique_email("test")    # test_20240520_143005_abcd@example.com
username = DataGenerator.unique_username("user") # user_1708456789
```

---

## ▶️ Running Tests

### Run all tests

```bash
pytest
```

### Run a specific test file

```bash
pytest tests/test_register_user.py
```

### Run a specific test function

```bash
pytest tests/test_register_user.py::test_register_user
```

### Run in parallel

```bash
pytest -n 4      # 4 parallel workers
pytest -n auto   # auto-detect based on CPU count
```

### Run with auto-retry for flaky tests

```bash
pytest --reruns 2 --reruns-delay 1
```

### Run against a different environment

```bash
pytest --env=staging
```

### Run with verbose output

```bash
pytest -v
```

> **Note:** `pytest.ini` already sets `-v` and `--alluredir=reports/allure-results` as defaults — Allure results are always generated automatically when running `pytest`.

---

## 📊 Allure Report

### Serve report locally (opens browser)

```bash
allure serve reports/allure-results
```

### Generate static HTML report

```bash
allure generate reports/allure-results -o reports/allure-report --clean
```

### Report features

- **Feature / Story** grouping via `@allure.feature` and `@allure.story` decorators
- **Step-by-step** breakdown via `with allure.step(...)` blocks in every test
- **Screenshot on failure** — automatically attached by the `driver` fixture in `conftest.py`
- **Assertion evidence** — `assert_text_contains()` / `assert_true()` attach comparison details, current URL, and screenshot on every failure

---

## 🧪 Pytest Fixtures

Key fixtures defined in `tests/conftest.py`:

| Fixture | Scope | Description |
|---|---|---|
| `config` | session | Merged YAML config, supports `--env` CLI override |
| `driver` | function | WebDriver instance — auto-attaches screenshot on failure |
| `app` | function | `Navigator` instance — application entry point |
| `download_dir` | function | Temp directory for downloads, auto-cleaned after test |
| `user_profile` | function | Loaded from `test_data/user_data.yaml` |
| `registered_user` | function | Registers account via UI, returns `{email, password, username}` |
| `logged_in_user` | function | Registers + logs in, returns `HomePage` in authenticated state |

### Usage examples

```python
# Background account creation — test focuses only on login flow
def test_login(app, config, registered_user):
    home_page = app.open_site(config["base_url"])
    login_page = home_page.header.click_signup_login()
    home_page = login_page.login(registered_user["email"], registered_user["password"])

# Start test already logged in
def test_add_to_cart(logged_in_user):
    home_page = logged_in_user  # already authenticated, on home page
    products_page = home_page.header.click_products()
    ...
```

---

## 🧩 Component Reference

All components are initialized in `BasePage` and accessible on every Page:

| Attribute | Component | Responsibilities |
|---|---|---|
| `page.header` | `HeaderComponent` | Navigation links, signup/login, logout, delete account |
| `page.footer` | `FooterComponent` | Subscription form |
| `page.add_to_cart_modal` | `AddToCartComponent` | "Added to cart" modal — continue shopping / view cart |
| `page.category_sidebar` | `CategorySidebarComponent` | Category accordion navigation |
| `page.products` | `HomeProductsComponent` | Featured products section on home page |
| `page.scroll_up` | `ScrollUpComponent` | Fixed scroll-to-top arrow button |

```python
# Clean, readable test code — no WebDriver in tests
login_page  = home_page.header.click_signup_login()
home_page   = home_page.header.click_delete_account()
home_page.footer.subscribe(email)
cart_page   = page.add_to_cart_modal.click_view_cart()
```

---

## 🧪 Test Cases Covered

| TC | Test Case | Feature | Status |
|---|---|---|---|
| TC01 | Register User | User Management | ✅ |
| TC02 | Login User with correct credentials | Access Control | ✅ |
| TC03 | Login User with incorrect credentials | Access Control | ✅ |
| TC04 | Logout User | Access Control | ✅ |
| TC05 | Register User with existing email | User Management | ✅ |
| TC06 | Contact Us Form | Content | ✅ |
| TC07 | Verify Test Cases Page | Navigation | ✅ |
| TC08 | Verify All Products and product detail | Products | ✅ |
| TC09 | Search Product | Products | ✅ |
| TC10 | Verify Subscription in home page | Subscription | ✅ |
| TC11 | Verify Subscription in Cart page | Subscription | ✅ |
| TC12 | Add Products in Cart | Cart | ✅ |
| TC13 | Verify Product quantity in Cart | Cart | ✅ |
| TC14 | Place Order: Register while Checkout | Orders | ✅ |
| TC15 | Place Order: Register before Checkout | Orders | ✅ |
| TC16 | Place Order: Login before Checkout | Orders | ✅ |
| TC17 | Remove Products From Cart | Cart | ✅ |
| TC18 | View Category Products | Category | ✅ |
| TC19 | View & Cart Brand Products | Brand | ✅ |
| TC20 | Search Products and Verify Cart After Login | Cart | ✅ |
| TC21 | Add review on product | Review | ✅ |
| TC22 | Add to cart from Recommended items | Cart | ✅ |
| TC23 | Verify address details in checkout page | Checkout | ✅ |
| TC24 | Download Invoice after purchase order | Invoice | ✅ |
| TC25 | Scroll Up using Arrow button | UI | ✅ |
| TC26 | Scroll Up without Arrow button | UI | ✅ |

**Total: 26/26 PASSED ✅**

---

## 📋 Logging

Logs are written to both **console** (colorized by level) and a **rotating file**:

```
logs/test_run.log    # 5MB max per file, 5 backups retained
```

| Level | Output | Color |
|---|---|---|
| DEBUG | File only | Cyan |
| INFO | Console + File | Green |
| WARNING | Console + File | Yellow |
| ERROR | Console + File | Red |

---

## 🚦 CI/CD Ready

Framework supports out-of-the-box:

- **Headless execution** — `headless: true` in config
- **Parallel execution** — `pytest -n auto` via `pytest-xdist`
- **Auto-retry flaky tests** — `pytest --reruns 2` via `pytest-rerunfailures`
- **Remote execution** — `remote_url` in config for Selenium Grid / Docker
- **Environment switching** — `--env=staging` CLI argument
- **Allure results** — generated automatically on every run

---

## ❗ Golden Rules

- Tests interact **only via Page Objects** — no raw `driver` calls in test files
- Pages use **Components** — no duplicated header/footer locators across pages
- **`Navigator`** is the single place that imports all Page classes — prevents circular imports
- **No hardcoded credentials** in tests — all data from `user_data.yaml` or `DataGenerator`
- **Assertion failures always attach evidence** — screenshot + URL + comparison in Allure

---

✅ **Happy Testing!**
