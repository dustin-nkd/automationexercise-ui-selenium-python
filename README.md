# 🚀 Selenium Python Automation Framework

Enterprise-grade UI automation framework built with **Python, Selenium, Pytest, and Allure**, following **Component-based Page Object Model (POM)** and best practices used in real-world projects.

---

## 📌 Tech Stack

- Python 3.10+
- Selenium WebDriver
- Pytest
- Allure Report
- YAML (configuration)
- webdriver-manager

---

## 📂 Project Structure

```text
.
├── tests/                  # Test cases (business flows)
│   ├── test_register_user.py
│   ├── test_login_user.py
│   └── ...
│
├── src/
│   ├── pages/              # Page Objects
│   ├── components/         # Reusable UI components (Header, etc.)
│   ├── utilities/          # Logger, assertions, data generator
│   ├── config/             # config.yaml, env configs
│   └── base/               # BasePage, WebDriverFactory
│
├── conftest.py             # Pytest fixtures & hooks
├── pytest.ini              # Pytest configuration
├── requirements.txt        # Dependencies
├── README.md               # This document
├── ARCHITECTURE.md         # Framework architecture
└── .gitignore
```

---

## 🧠 Design Principles

- **Page Object Model (POM)**
- **Component-based UI abstraction**
- **DRY** – Don’t Repeat Yourself
- **KISS** – Keep It Simple
- **YAGNI** – You Aren’t Gonna Need It
- **SRP** – Single Responsibility Principle

📘 See full design details in **ARCHITECTURE.md**.

---

## ⚙️ Setup Instructions

### 1️⃣ Create virtual environment

```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate         # Windows
```

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔧 Configuration

Main config file: `config/config.yaml`

Example:

```yaml
browser: chrome
headless: false
implicit_wait: 8
base_url: "https://automationexercise.com"

test_user:
  email: "test@example.com"
  password: "password"

user_profile:
  password: "password123"
  title: "mr"
```

You can override environment via CLI:

```bash
pytest --env=staging
```

---

## ▶️ Run Tests

### Run all tests

```bash
pytest
```

### Run a specific test

```bash
pytest tests/test_login_user.py
```

### Run with verbose output

```bash
pytest -v
```

---

## 📊 Allure Report

### Generate report

```bash
pytest --alluredir=reports/allure-results
```

### View report

```bash
allure serve reports/allure-results
```

📸 Screenshots are automatically attached on failures.

---

## 🧪 Test Data Strategy

- Static data → `config.yaml`
- Dynamic data → `DataGenerator`
- User lifecycle handled via pytest fixtures (e.g. `registered_user`)

No hardcoded credentials inside tests.

---

## 🧩 Component-Based Design

Shared UI elements (e.g. Header) are implemented as **Components** and reused across pages.

✔ Pages own navigation  
✔ Components own UI actions  
❌ Components never return Page Objects  

---

## ❗ Golden Rules

- Tests talk only to **Page Objects**
- Pages use **Components**
- Components never navigate
- No WebDriver usage inside tests
- No duplicated locators

---

## 🧼 Code Quality

- Centralized logging
- Clean assertions
- No circular imports
- CI-ready architecture

---

## 🚦 CI/CD Ready

Framework supports:

- Parallel execution
- Selenium Grid
- Dockerized execution
- GitHub Actions / GitLab CI / Jenkins

---

## 👥 Contribution

Before contributing, please read:

- `ARCHITECTURE.md`
- Follow naming & design conventions

---

## 📌 Author Notes

This framework reflects **real enterprise automation practices**, not tutorial-style demos.

Built for:
- Scalability
- Maintainability
- Team collaboration
- Senior SDET standards

---

✅ **Happy Testing!**