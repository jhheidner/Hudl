"""TC-029: mobile viewport login UI."""

from __future__ import annotations

import pytest

from src.pages.login_page import LoginPage


@pytest.mark.regression
@pytest.mark.mobile
def test_tc029_mobile_viewport_login_usable(driver):
    driver.set_window_size(390, 844)
    login = LoginPage(driver)
    login.open()
    assert login.find_first_visible(login.EMAIL_INPUT) is not None
    assert login.find_first_visible(login.CONTINUE_BUTTON) is not None
    driver.set_window_size(1920, 1080)
