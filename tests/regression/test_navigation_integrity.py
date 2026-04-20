"""TC-040 — TC-041: direct URLs and unauthenticated access."""

from __future__ import annotations

import os

import pytest

from config.settings import settings
from src.pages.login_page import LoginPage


@pytest.mark.regression
@pytest.mark.navigation
def test_tc040_direct_login_path_loads(driver):
    driver.get(f"{settings.base_url.rstrip('/')}/login")
    login = LoginPage(driver)
    assert login.find_first_visible(login.EMAIL_INPUT) is not None


@pytest.mark.regression
@pytest.mark.navigation
def test_tc041_deep_link_redirects_when_not_logged_in(driver):
    path = os.getenv("PROTECTED_ROUTE", "/home")
    driver.get(f"{settings.base_url.rstrip('/')}{path}")
    url = driver.current_url.lower()
    assert (
        "identity.hudl.com" in url
        or "/login" in url
        or "login" in url
        or "sign" in url
    ), "Expected redirect toward authentication for a protected or app entry URL when logged out."
