"""Regression tests for Hudl login behavior."""

from __future__ import annotations

import pytest

from src.core.session_checks import assert_left_auth0_universal_login
from src.pages.login_page import LoginPage


# ---------- Fixtures ----------

@pytest.fixture
def login_page(driver):
    page = LoginPage(driver)
    page.open()
    return page


# ---------- Tests ----------

@pytest.mark.regression
def test_user_sees_login_button_on_login_page(login_page):
    assert login_page.is_login_button_visible(), \
        "Expected login button to be visible on login page."


@pytest.mark.regression
def test_invalid_login_displays_error_message(login_page):
    login_page.login("invalid_user@example.com", "incorrect_password")

    error = login_page.get_error_message()

    assert error, "Expected an error message after invalid login."
    assert any(word in error.lower() for word in ["incorrect", "wrong", "invalid"]), \
        f"Unexpected error message: '{error}'"


@pytest.mark.regression
def test_valid_login_redirects_user(driver, hudl_credentials):
    login_page = LoginPage(driver)
    login_page.open()

    login_page.login(hudl_credentials.email, hudl_credentials.password)

    assert_left_auth0_universal_login(driver.current_url)