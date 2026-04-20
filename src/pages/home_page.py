"""Page object for hudl.com home page."""

from __future__ import annotations

from selenium.webdriver.common.by import By

from src.core.base_page import BasePage


class HomePage(BasePage):
    LOGIN_LINK = (
        By.XPATH,
        "//a[contains(@href, '/login') "
        "or contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'log in') "
        "or contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'login')]",
    )

    def open(self) -> None:
        self.visit("/")

    def click_login(self) -> None:
        self.click(self.LOGIN_LINK)

    def has_login_link(self) -> bool:
        candidates = self.driver.find_elements(*self.LOGIN_LINK)
        return any(element.is_displayed() for element in candidates)
