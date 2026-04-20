"""Base page object with robust Selenium actions."""

from __future__ import annotations

import logging
from typing import Tuple, Iterable

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

from config.settings import settings
from src.core.log_safety import redact_url_for_logs


logger = logging.getLogger(__name__)

Locator = Tuple[By, str]


class BasePage:
    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, settings.explicit_wait)

    # ---------- Navigation ----------

    def visit(self, path: str = "") -> None:
        url = (
            f"{settings.base_url.rstrip('/')}/{path.lstrip('/')}"
            if path else settings.base_url
        )
        logger.info("Navigating to: %s", redact_url_for_logs(url))
        self.driver.get(url)

    # ---------- Wait Helpers ----------

    def wait_for_visible(self, locator: Locator) -> WebElement:
        return self.wait.until(EC.visibility_of_element_located(locator))

    def wait_for_clickable(self, locator: Locator) -> WebElement:
        return self.wait.until(EC.element_to_be_clickable(locator))

    def wait_for_present(self, locator: Locator) -> WebElement:
        return self.wait.until(EC.presence_of_element_located(locator))

    # ---------- Element Finders ----------

    def find(self, locator: Locator) -> WebElement:
        return self.wait_for_visible(locator)

    def find_all(self, locator: Locator) -> list[WebElement]:
        return self.wait.until(lambda d: d.find_elements(*locator))

    def find_first_visible(self, locator: Locator) -> WebElement | None:
        elements = self.driver.find_elements(*locator)
        for el in elements:
            if el.is_displayed():
                return el
        return None

    def find_all_now(self, locator: Locator) -> list[WebElement]:
        """All matches right now (no implicit wait). Use for polling UI state."""
        return self.driver.find_elements(*locator)

    def webdriver_wait(self, timeout_seconds: int | None = None) -> WebDriverWait:
        return WebDriverWait(self.driver, timeout_seconds if timeout_seconds is not None else settings.explicit_wait)

    def wait_until_visible(self, locator: Locator, timeout_seconds: int | None = None) -> WebElement:
        return self.webdriver_wait(timeout_seconds).until(EC.visibility_of_element_located(locator))

    def click_element(self, element: WebElement) -> None:
        """Click an already-resolved element (scroll into view first)."""
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", element)
        element.click()

    def visible_texts_under_css(self, css_selector: str) -> list[str]:
        texts: list[str] = []
        for el in self.find_all_now((By.CSS_SELECTOR, css_selector)):
            if el.is_displayed():
                t = (el.text or "").strip()
                if t:
                    texts.append(t)
        return texts

    # ---------- Actions ----------

    def click(self, locator: Locator) -> None:
        logger.info(f"Clicking element: {locator}")
        element = self.wait_for_clickable(locator)
        self.click_element(element)

    def type(self, locator: Locator, value: str, clear_first: bool = True) -> None:
        # Never log `value` — may be a password, token, or PII.
        logger.info("Typing into element: %s", locator)
        element = self.wait_for_visible(locator)
        if clear_first:
            element.clear()
        element.send_keys(value)

    def get_text(self, locator: Locator) -> str:
        text = self.wait_for_visible(locator).text.strip()
        # Never log `text` — may contain messages with account details or tokens.
        logger.info("Read text from element: %s (length=%s)", locator, len(text))
        return text

    # ---------- State Checks ----------

    def is_visible(self, locator: Locator) -> bool:
        try:
            self.wait_for_visible(locator)
            return True
        except TimeoutException:
            return False

    # ---------- Advanced Actions ----------

    def click_and_wait_for_url(
        self,
        locator: Locator,
        fragments: Iterable[str],
        timeout: int | None = None
    ) -> str:
        """
        Click an element and wait for URL change or new window/tab.
        """
        timeout = timeout or settings.explicit_wait
        wait = WebDriverWait(self.driver, timeout)

        before_handles = set(self.driver.window_handles)

        self.click(locator)

        wait.until(
            lambda d: any(f in d.current_url.lower() for f in fragments)
            or len(set(d.window_handles) - before_handles) > 0
        )

        new_handles = list(set(self.driver.window_handles) - before_handles)
        if new_handles:
            logger.info("Switching to new browser window/tab")
            self.driver.switch_to.window(new_handles[0])

        wait.until(lambda d: any(f in d.current_url.lower() for f in fragments))
        logger.info("Navigated to: %s", redact_url_for_logs(self.driver.current_url))

        return self.driver.current_url

    # ---------- Properties ----------

    @property
    def title(self) -> str:
        return self.driver.title