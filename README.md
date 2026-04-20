# Hudl Selenium Automation Framework

Python-based Selenium WebDriver framework for validating authentication flows on **Hudl.com**, built with **pytest** and the **Page Object Model (POM)**.

The suite focuses on practical test design: session validation, resilience checks, and maintainable patterns (explicit waits, shared session URL helpers, opt-in risky scenarios).

---

## 🚀 Tech stack

- Python 3.10+
- Selenium WebDriver
- pytest
- WebDriver Manager
- pytest HTML reports
- Allure reporting (optional)

---

## 📌 Test coverage (high level)

- **Authentication** — login, signup entry, password recovery, SSO entry points  
- **Session** — refresh while logged in, logout, back navigation after sign-out  
- **Validation** — identifier/password rules, boundary inputs  
- **Security-oriented** — safe input handling; rate-limit tests **opt-in** (`RUN_RATE_LIMIT_TESTS`)  
- **Cross-browser** — Chrome (default), Firefox, Edge via `BROWSER` / fixtures  
- **Responsive** — mobile viewport sizing  
- **Accessibility** — keyboard navigation, basic focus order  
- **Framework** — URL redaction, explicit-wait contracts  

Canonical case IDs and notes live in `docs/TEST_PLAN.docx` (not all details are duplicated here).

---

## 🧱 Project structure

```
.
├── .github/workflows/     # CI (smoke on PR/push)
├── config/
│   └── settings.py        # dotenv + env-driven settings
├── docs/                  # Test plan (e.g. TEST_PLAN.docx)
├── src/
│   ├── core/
│   │   ├── base_page.py
│   │   ├── driver_factory.py
│   │   ├── log_safety.py
│   │   └── session_checks.py
│   └── pages/
│       ├── app_shell_page.py
│       ├── create_account_page.py
│       ├── home_page.py
│       └── login_page.py
├── tests/
│   ├── a11y/
│   ├── conftest.py
│   ├── cross_browser/
│   ├── regression/
│   ├── resilience/
│   ├── responsive/
│   ├── security/
│   ├── session/
│   ├── smoke/
│   ├── support/
│   └── unit/
├── artifacts/
│   ├── reports/           # pytest HTML (gitignored contents)
│   └── screenshots/       # failures (gitignored)
├── pytest.ini
├── requirements.txt
├── run_tests.ps1 / run_tests.bat
└── .env.example
```

---

## ⚙️ Setup

### 1. Clone and virtual environment

```powershell
git clone https://github.com/jhheidner/Hudl.git
cd Hudl

python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

On macOS/Linux, activate with `source .venv/bin/activate`.

### 2. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

Prefer **`python -m pip`** and **`python -m pytest`** inside the same venv so you do not mix global and venv interpreters.

---

## 🔐 Environment variables

**Required for tests that log in** (copy `.env.example` to `.env` and fill in):

| Variable | Purpose |
|----------|---------|
| `HUDL_EMAIL` | Account email |
| `HUDL_PASSWORD` | Account password |

**Optional overrides:**

| Variable | Example | Purpose |
|----------|---------|---------|
| `BROWSER` | `chrome`, `firefox`, `edge` | Browser (see `driver_factory`) |
| `HEADLESS` | `true` / `false` | Headless mode (CI uses `true`) |
| `BASE_URL` | `https://www.hudl.com` | Site under test |
| `PROTECTED_ROUTE` | `/home` | TC-041 deep-link guard |
| `RUN_RATE_LIMIT_TESTS` | `1` | Enable rate-limit test (use with care) |

Never commit `.env` or real credentials.

---

## ▶️ Running tests

**Smoke (fast, matches CI):**

```powershell
python -m pytest tests/smoke -m smoke
```

**Full suite** (longer; needs credentials for session/login tests):

```powershell
python -m pytest
```

**Wrappers** (always use project `.venv`):

```powershell
.\run_tests.ps1 -m smoke
```

```bat
run_tests.bat -m smoke
```

### If you see `ModuleNotFoundError`

Install packages and run pytest with the **same** interpreter, e.g. `.\.venv\Scripts\python.exe -m pytest`.

---

## 📊 Reporting

### pytest HTML

- Output: `artifacts/reports/report.html` (self-contained; path configured in `pytest.ini`)

### Allure (optional)

Record raw results:

```powershell
python -m pytest --alluredir=allure-results --clean-alluredir
```

View the report (requires **[Allure command-line](https://github.com/allure-framework/allure2/releases)** and a **Java** runtime):

```powershell
allure serve allure-results
```

When Allure is enabled, failed UI tests can attach screenshots and truncated page source.

---

## 📸 Debugging artifacts

- **PNG screenshots** on failure: `artifacts/screenshots/`  
- **Allure**: step-level structure, attachments as above  

---

## 🔄 CI/CD

- **GitHub Actions** (`.github/workflows/ci.yml`) runs the **smoke** suite on **push** and **pull_request** to `main` / `master`, with **HEADLESS=true**.
- Workflow **artifacts**: pytest HTML report and `allure-results` folder for local `allure serve`.
- **Full regression** is intended for **local** or **scheduled** runs (not wired as a nightly job in this repo by default).

---

## 🧠 Design notes

- **Page Object Model** for UI interaction and reuse.  
- **Explicit waits** via `BasePage` / `WebDriverWait`; `LoginPage.login()` waits for Auth0 outcome instead of assuming instant redirect.  
- **Post-login checks** use `assert_left_auth0_universal_login()` (host + path) rather than URL-only heuristics in isolation.  
- **Rate-limit** and similar tests stay **off** unless explicitly enabled.  

---

## ⚠️ Notes

- Do **not** commit credentials; use `.env` locally and CI secrets for automation accounts if you extend CI.  
- **Rate-limit** tests can affect real accounts—keep them opt-in on production.  
- **Allure CLI** is separate from the Python `allure-pytest` plugin and needs Java.  
- Third-party OAuth flows are covered at **entry** only, not full IdP completion.
