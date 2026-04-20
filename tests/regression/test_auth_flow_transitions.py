"""TC-035 — TC-036: Auth0 multi-step transitions."""

from __future__ import annotations

import pytest

from src.pages.login_page import LoginPage


@pytest.mark.regression
@pytest.mark.auth_flow
def test_tc035_refresh_on_password_step_still_usable(driver):
    login = LoginPage(driver)
    login.open()
    login.advance_to_password_step("flow-refresh-probe@example.com")
    driver.refresh()
    login.wait_until_visible(login.PASSWORD_INPUT)
    assert login.find_first_visible(login.PASSWORD_INPUT) is not None


@pytest.mark.regression
@pytest.mark.auth_flow
def test_tc036_back_from_password_returns_to_identifier(driver):
    login = LoginPage(driver)
    login.open()
    login.advance_to_password_step("flow-back-probe@example.com")
    driver.back()
    login.wait_until_visible(login.EMAIL_INPUT)
    assert login.find_first_visible(login.EMAIL_INPUT) is not None
