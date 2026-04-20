"""TC-028: login flow on Firefox."""

from __future__ import annotations

import pytest

from src.pages.login_page import LoginPage


@pytest.mark.regression
@pytest.mark.cross_browser
def test_tc028_login_identifier_step_works_on_firefox(driver_firefox):
    login = LoginPage(driver_firefox)
    login.open()
    assert login.has_expected_login_elements(), "Expected identifier UI on Firefox."
