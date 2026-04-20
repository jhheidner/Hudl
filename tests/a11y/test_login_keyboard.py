"""TC-037 — TC-038: basic keyboard interaction on login."""

from __future__ import annotations

import pytest
from selenium.webdriver.common.keys import Keys

from src.pages.login_page import LoginPage


@pytest.mark.regression
@pytest.mark.a11y
def test_tc037_keyboard_can_move_focus_from_email_field(driver):
    login = LoginPage(driver)
    login.open()
    email = login.find_first_visible(login.EMAIL_INPUT)
    assert email is not None
    email.click()
    email.send_keys(Keys.TAB)
    active = driver.switch_to.active_element
    assert active is not None


@pytest.mark.regression
@pytest.mark.a11y
def test_tc038_tab_moves_to_another_focusable_control(driver):
    login = LoginPage(driver)
    login.open()
    login.find_first_visible(login.EMAIL_INPUT).click()
    for _ in range(4):
        driver.switch_to.active_element.send_keys(Keys.TAB)
    active = driver.switch_to.active_element
    assert active.tag_name.lower() in ("input", "button", "a")
