"""Regression tests for login page navigation and sign-in options."""

from __future__ import annotations

import pytest

from src.pages.login_page import LoginPage


@pytest.mark.regression
def test_login_page_loads_with_logo_email_and_continue(driver):
    login_page = LoginPage(driver)
    login_page.open()

    assert login_page.has_expected_login_elements(), (
        "Expected login page to show Hudl logo, email input, and continue button."
    )


@pytest.mark.regression
def test_login_page_privacy_link_opens_privacy_page(driver):
    login_page = LoginPage(driver)
    login_page.open()
    current_url = login_page.open_privacy_page_from_login().lower()

    assert "hudl.com/privacy" in current_url, "Expected Privacy link to navigate to Hudl privacy page."


@pytest.mark.regression
def test_login_page_terms_link_opens_terms_page(driver):
    login_page = LoginPage(driver)
    login_page.open()
    current_url = login_page.open_terms_page_from_login().lower()

    assert "hudl.com/terms" in current_url, "Expected Terms link to navigate to Hudl terms page."


@pytest.mark.regression
def test_login_page_continue_with_google_starts_google_flow(driver):
    login_page = LoginPage(driver)
    login_page.open()
    current_url = login_page.start_google_auth_flow().lower()

    assert "google" in current_url or "oauth" in current_url, (
        "Expected Google option to start Google/OAuth auth flow."
    )


@pytest.mark.regression
def test_login_page_continue_with_facebook_starts_facebook_flow(driver):
    login_page = LoginPage(driver)
    login_page.open()
    current_url = login_page.start_facebook_auth_flow().lower()

    assert "facebook" in current_url or "oauth" in current_url, (
        "Expected Facebook option to start Facebook/OAuth auth flow."
    )


@pytest.mark.regression
def test_login_page_continue_with_apple_starts_apple_flow(driver):
    login_page = LoginPage(driver)
    login_page.open()
    current_url = login_page.start_apple_auth_flow().lower()

    assert "apple" in current_url or "oauth" in current_url, (
        "Expected Apple option to start Apple/OAuth auth flow."
    )


@pytest.mark.regression
def test_login_page_create_account_opens_signup_page(driver):
    login_page = LoginPage(driver)
    login_page.open()
    current_url = login_page.open_create_account_from_login().lower()

    assert "signup" in current_url or "register" in current_url, (
        "Expected Create Account option to navigate to signup/registration flow."
    )


@pytest.mark.regression
def test_login_page_forgot_password_opens_reset_flow(driver):
    login_page = LoginPage(driver)
    current_url = login_page.open_forgot_password_reset("noreply_pw_reset_probe@example.com").lower()

    assert any(
        fragment in current_url
        for fragment in (
            "password-reset",
            "reset-password",
            "forgot-password",
            "/recovery",
            "resetpassword",
        )
    ), f"Expected forgot-password link to open a reset or recovery URL; got {current_url!r}."
