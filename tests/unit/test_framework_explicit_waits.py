"""TC-039: framework exposes explicit wait helpers (contract test)."""

from __future__ import annotations

from src.core.base_page import BasePage


def test_tc039_base_page_exposes_explicit_wait_primitives():
    assert hasattr(BasePage, "wait_until_visible")
    assert hasattr(BasePage, "webdriver_wait")
    assert hasattr(BasePage, "wait_for_clickable")
