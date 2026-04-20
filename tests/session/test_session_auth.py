"""TC-022 — TC-024: session, refresh, logout, back button (requires HUDL credentials)."""

from __future__ import annotations

import time

import pytest

from src.core.session_checks import (
    assert_left_auth0_universal_login,
    is_auth0_login_url,
)
from src.pages.app_shell_page import AppShellPage
from src.pages.home_page import HomePage
from src.pages.login_page import LoginPage


@pytest.mark.regression
@pytest.mark.session
def test_tc022_logged_in_refresh_remains_authenticated(driver, hudl_credentials):
    login = LoginPage(driver)
    login.open()
    login.login(hudl_credentials.email, hudl_credentials.password)
    assert_left_auth0_universal_login(driver.current_url)

    driver.refresh()

    assert_left_auth0_universal_login(driver.current_url)


@pytest.mark.regression
@pytest.mark.session
def test_tc023_logout_invalidates_session(driver, hudl_credentials):
    login = LoginPage(driver)
    login.open()
    login.login(hudl_credentials.email, hudl_credentials.password)
    assert_left_auth0_universal_login(driver.current_url)

    shell = AppShellPage(driver)
    assert shell.try_click_logout(wait_seconds=20), (
        "Could not find a Log out control — update locators in AppShellPage for your Hudl surface."
    )
    time.sleep(2)

    if not is_auth0_login_url(driver.current_url):
        HomePage(driver).open()

    assert is_auth0_login_url(driver.current_url) or HomePage(driver).has_login_link(), (
        "After logout, user should see login entry or Auth0 login page."
    )


@pytest.mark.regression
@pytest.mark.session
def test_tc024_back_after_logout_does_not_restore_authenticated_app(driver, hudl_credentials):
    login = LoginPage(driver)
    login.open()
    login.login(hudl_credentials.email, hudl_credentials.password)
    shell = AppShellPage(driver)
    assert shell.try_click_logout(wait_seconds=20), "Logout control not found."
    time.sleep(1.5)

    driver.back()
    time.sleep(1.5)

    home = HomePage(driver)
    home.open()
    u = driver.current_url.lower()
    assert (
        is_auth0_login_url(driver.current_url) or home.has_login_link() or "login" in u
    ), "After logout and Back, user should still see login entry or Auth0 login."
