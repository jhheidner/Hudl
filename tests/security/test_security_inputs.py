"""TC-025 — TC-027: abuse-oriented and injection-style inputs."""

from __future__ import annotations

import os
import time

import pytest

from src.core.session_checks import assert_left_auth0_universal_login
from src.pages.login_page import LoginPage


@pytest.mark.regression
@pytest.mark.security
@pytest.mark.rate_limit
@pytest.mark.skipif(
    not os.getenv("RUN_RATE_LIMIT_TESTS"),
    reason="Set RUN_RATE_LIMIT_TESTS=1 to run (may trigger throttling or lockout).",
)
def test_tc025_repeated_failed_logins_surface_protection(driver):
    login = LoginPage(driver)
    email = "rate-limit-probe-not-a-user@example.com"
    for _ in range(5):
        login.open()
        login.login(email, "WrongPassword!1")
    messages = login.visible_validation_messages()
    body = driver.find_element("tag name", "body").text.lower()
    assert messages or "incorrect" in body or "too many" in body or "try again" in body or "lock" in body


@pytest.mark.regression
@pytest.mark.security
def test_tc026_email_field_script_like_input_does_not_execute(driver):
    login = LoginPage(driver)
    login.open()
    payload = "<script>alert(1)</script>@example.com"
    login.submit_identifier_step(payload)
    time.sleep(0.5)
    try:
        alert = driver.switch_to.alert
        text = alert.text
        alert.dismiss()
        pytest.fail(f"Unexpected alert from script-like input: {text}")
    except Exception:
        pass


@pytest.mark.regression
@pytest.mark.security
def test_tc027_login_accepts_complex_password_characters(driver, hudl_credentials):
    """Uses real credentials (often include special characters) — behavioral check only."""
    login = LoginPage(driver)
    login.open()
    login.login(hudl_credentials.email, hudl_credentials.password)

    assert_left_auth0_universal_login(driver.current_url)
