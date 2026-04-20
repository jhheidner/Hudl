"""Pytest fixtures and hooks for Selenium tests."""

from __future__ import annotations

from datetime import datetime
import os
from pathlib import Path

import pytest

try:
    import allure
except ImportError:
    allure = None  # type: ignore[misc, assignment]
from _pytest.runner import CallInfo
from selenium.webdriver.remote.webdriver import WebDriver

from src.core.driver_factory import DriverFactory
from tests.support.redacted_credentials import RedactedHudlCredentials


@pytest.fixture(scope="session", autouse=True)
def _create_artifact_dirs() -> None:
    Path("artifacts/reports").mkdir(parents=True, exist_ok=True)
    Path("artifacts/screenshots").mkdir(parents=True, exist_ok=True)
    Path("allure-results").mkdir(parents=True, exist_ok=True)


def _driver_teardown_save_screenshot(request: pytest.FixtureRequest, web_driver: WebDriver) -> None:
    failed = getattr(request.node, "rep_call", None)
    if failed and failed.failed:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = Path("artifacts/screenshots") / f"{request.node.name}_{timestamp}.png"
        web_driver.save_screenshot(str(screenshot_path))


@pytest.fixture()
def driver(request: pytest.FixtureRequest) -> WebDriver:
    web_driver = DriverFactory.create_driver()
    yield web_driver
    _driver_teardown_save_screenshot(request, web_driver)
    DriverFactory.quit_driver(web_driver)


@pytest.fixture()
def driver_firefox(request: pytest.FixtureRequest) -> WebDriver:
    web_driver = DriverFactory.create_driver(browser="firefox")
    yield web_driver
    _driver_teardown_save_screenshot(request, web_driver)
    DriverFactory.quit_driver(web_driver)


@pytest.fixture()
def hudl_credentials() -> RedactedHudlCredentials:
    email = os.getenv("HUDL_EMAIL")
    password = os.getenv("HUDL_PASSWORD")
    if not email or not password:
        pytest.skip("HUDL_EMAIL and HUDL_PASSWORD are required for credentialed login tests.")
    return RedactedHudlCredentials(email=email, password=password)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: CallInfo[None]):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)

    if report.when != "call" or not report.failed:
        return

    driver = item.funcargs.get("driver") or item.funcargs.get("driver_firefox")
    if driver is None:
        return

    if allure is None:
        return

    try:
        allure.attach(
            driver.get_screenshot_as_png(),
            name="failure-screenshot",
            attachment_type=allure.attachment_type.PNG,
        )
    except Exception:
        pass

    try:
        source = driver.page_source
        if source:
            allure.attach(
                source[:500_000],
                name="page-source",
                attachment_type=allure.attachment_type.TEXT,
            )
    except Exception:
        pass
