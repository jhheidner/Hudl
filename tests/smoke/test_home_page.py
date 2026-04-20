"""Smoke tests for Hudl home page."""

from __future__ import annotations

import pytest

from src.pages.home_page import HomePage


@pytest.mark.smoke
def test_home_page_displays_login_link(driver):
    home_page = HomePage(driver)
    home_page.open()

    assert home_page.has_login_link(), "Expected login link to be visible on the home page."
