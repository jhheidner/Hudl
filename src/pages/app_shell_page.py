"""Post-login Hudl surfaces: logout and lightweight checks (locators may evolve)."""

from __future__ import annotations

import time

from selenium.webdriver.common.by import By

from src.core.base_page import BasePage


class AppShellPage(BasePage):
    """Best-effort locators after successful login; UI varies by product area."""

    LOG_OUT = (
        By.XPATH,
        "//a[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'log out')]"
        "|//button[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'log out')]"
        "|//a[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'sign out')]"
        "|//button[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'sign out')]"
        "|//*[@data-qa-id='logout' or @data-testid='logout' or contains(@href, 'logout')]",
    )
    ACCOUNT_OR_PROFILE_MENU = (
        By.XPATH,
        "//button[contains(@aria-label, 'Account') or contains(@aria-label, 'Profile') "
        "or contains(@aria-label, 'Menu') or contains(@data-qa-id, 'account')]",
    )

    def try_click_logout(self, wait_seconds: float = 8.0) -> bool:
        """End the session: try in-app controls first, then GET /logout (Hudl sign-out route)."""
        # Post-login redirects vary; global chrome is more likely on home.
        self.visit("/home")
        time.sleep(0.75)
        deadline = time.monotonic() + wait_seconds
        while time.monotonic() < deadline:
            logout = self.find_first_visible(self.LOG_OUT)
            if logout is not None:
                self.click_element(logout)
                return True
            menu = self.find_first_visible(self.ACCOUNT_OR_PROFILE_MENU)
            if menu is not None:
                self.click_element(menu)
                time.sleep(0.4)
                continue
            time.sleep(0.25)

        # Documented server-side sign-out when account menu locators don't match this build.
        self.visit("/logout")
        time.sleep(1.2)
        return True
