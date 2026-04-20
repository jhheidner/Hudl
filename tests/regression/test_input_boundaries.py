"""TC-032 — TC-034: email boundary and normalization."""

from __future__ import annotations

import time

import pytest

from src.core.session_checks import assert_left_auth0_universal_login
from src.pages.login_page import LoginPage


@pytest.mark.regression
def test_tc032_whitespace_around_email_advances_or_validates(driver):
    login = LoginPage(driver)
    login.open()
    login.submit_identifier_step("  whitespace-probe@example.com  ")
    time.sleep(1.2)
    advanced = login.find_first_visible(login.PASSWORD_INPUT) is not None
    msgs = login.visible_validation_messages()
    assert advanced or msgs, "Expected password step after trim, or validation feedback."


@pytest.mark.regression
def test_tc033_email_case_login_attempt(driver, hudl_credentials):
    login = LoginPage(driver)
    login.open()
    mixed = hudl_credentials.email.upper()
    login.login(mixed, hudl_credentials.password)
    assert_left_auth0_universal_login(driver.current_url)


@pytest.mark.regression
def test_tc034_very_long_local_part_email_handled(driver):
    login = LoginPage(driver)
    login.open()
    long_local = "a" * 200
    login.submit_identifier_step(f"{long_local}@x.co")
    time.sleep(1.2)
    msgs = login.visible_validation_messages()
    on_pw = login.find_first_visible(login.PASSWORD_INPUT) is not None
    assert msgs or on_pw
