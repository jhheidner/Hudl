# Selenium Page Object Model Framework (Hudl)

Python-based Selenium WebDriver framework for testing `hudl.com` using Page Object Model (POM), pytest fixtures, and reusable utilities.

## Tech Stack
- Python 3.10+
- Selenium WebDriver
- Pytest
- WebDriver Manager
- Pytest HTML reports
- Allure Report (optional CLI to view rich reports)

## Project Structure
```
.
|-- config/
|   `-- settings.py
|-- src/
|   |-- core/
|   |   |-- base_page.py
|   |   `-- driver_factory.py
|   `-- pages/
|       |-- home_page.py
|       `-- login_page.py
|-- tests/
|   |-- smoke/
|   |   `-- test_home_page.py
|   |-- regression/
|   |   `-- test_login_page.py
|   `-- conftest.py
|-- artifacts/
|   |-- reports/
|   `-- screenshots/
|-- requirements.txt
`-- pytest.ini
```

## Quick Start

Use a **virtual environment** so `pip` and `pytest` use the same Python (avoids `ModuleNotFoundError` after installing packages).

**PowerShell (Windows), from the repo root:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pytest
```

Or without activating, always invoke the venv explicitly:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest
```

Smoke only:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/smoke -m smoke
```

**Avoid wrong-Python issues:** from the repo root you can use the wrappers (they always use `.venv`):

```powershell
.\run_tests.ps1 -m smoke
```

```bat
run_tests.bat -m smoke
```

### If you see `ModuleNotFoundError` (e.g. `selenium`, `pytest`)

That usually means packages were installed for a **different** Python than the one running `pytest` (for example a user install under `AppData\Roaming\Python\...`). Fix: use **`python -m pip`** and **`python -m pytest`** inside the **same** `.venv** as above—not a global `pytest` on `PATH`.

`allure-pytest` is optional for running tests; use it when you want `--alluredir` Allure output (see **Allure** below).

### Allure CLI (`allure serve` does nothing)

The **Python** package is `allure-pytest` (report data). The **`allure`** terminal command is the **separate [Allure commandline](https://github.com/allure-framework/allure2/releases)** (needs **Java**). Download it, unpack, and add the `bin` folder to your `PATH`, or call it by full path, then run `allure serve allure-results`.

## Browser & Environment Options
Default settings are in `config/settings.py`.

You can override runtime values with environment variables:
- `BROWSER` (`chrome`, `firefox`, `edge`)
- `HEADLESS` (`true` or `false`)
- `BASE_URL` (default `https://www.hudl.com`)
- `IMPLICIT_WAIT`
- `EXPLICIT_WAIT`

Example (venv active or use `.\.venv\Scripts\python.exe -m pytest`):

- PowerShell: `$env:HEADLESS="true"; python -m pytest`

## Reports

### Pytest HTML
- `artifacts/reports/report.html` (self-contained)

### Allure (optional)
`pytest.ini` does **not** require Allure by default, so `pytest` works even if `allure-pytest` is not installed. To record Allure data, install dependencies (includes `allure-pytest`) and pass:

```powershell
python -m pytest --alluredir=allure-results --clean-alluredir
```

You can combine with any test selection, e.g. `python -m pytest -m smoke --alluredir=allure-results --clean-alluredir`.

**Install the [Allure commandline](https://github.com/allure-framework/allure2/releases)** (requires a Java runtime), then from the project root:

- **Open a local report UI:** `allure serve allure-results`
- **Generate static HTML:** `allure generate allure-results -o allure-report --clean` and open `allure-report/index.html`

When Allure is enabled (`allure-pytest` installed and `--alluredir` used), failed UI tests attach a **screenshot** and truncated **page source** to the Allure report.

### Screenshots on disk
Failed tests also save PNGs under `artifacts/screenshots/`.

### GitHub Actions
The workflow in `.github/workflows/ci.yml` runs the smoke suite, then uploads **`allure-results`** and the pytest HTML report as workflow artifacts. Download the artifact and run `allure serve` on the folder, or add a later step using your preferred Allure publish action.
