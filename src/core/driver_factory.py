"""WebDriver creation and teardown helpers."""

from __future__ import annotations

import logging
from typing import Type

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from config.settings import settings
from src.core.log_safety import redact_url_for_logs


logger = logging.getLogger(__name__)


class DriverFactory:
    """Factory class for creating and quitting WebDriver instances."""

    @staticmethod
    def _create_driver(
        options,
        service_class: Type,
        driver_class: Type,
        manager: Type
    ) -> webdriver.Remote:
        """
        Internal helper to create either a local or remote driver.
        """
        if settings.remote_url:
            logger.info(
                "Starting REMOTE %s driver at %s",
                settings.browser,
                redact_url_for_logs(settings.remote_url),
            )
            driver = webdriver.Remote(
                command_executor=settings.remote_url,
                options=options
            )
        else:
            logger.info("Starting LOCAL driver")
            service = service_class(manager().install())
            driver = driver_class(service=service, options=options)

        return driver

    @staticmethod
    def create_driver(browser: str | None = None) -> webdriver.Remote:
        """
        Create a WebDriver instance based on configuration.

        :param browser: Override ``settings.browser`` (e.g. ``firefox`` for cross-browser tests).
        """
        browser = (browser or settings.browser).lower()
        logger.info("Initializing driver for browser: %s", browser)

        if browser == "chrome":
            options = ChromeOptions()

            if settings.headless:
                options.add_argument("--headless=new")

            for arg in settings.browser_args:
                options.add_argument(arg)

            driver = DriverFactory._create_driver(
                options,
                ChromeService,
                webdriver.Chrome,
                ChromeDriverManager
            )

        elif browser == "firefox":
            options = FirefoxOptions()

            if settings.headless:
                options.add_argument("-headless")

            for arg in settings.browser_args:
                options.add_argument(arg)

            driver = DriverFactory._create_driver(
                options,
                FirefoxService,
                webdriver.Firefox,
                GeckoDriverManager
            )

            # Firefox fallback if window-size not provided
            if not any("window-size" in arg for arg in settings.browser_args):
                driver.set_window_size(1920, 1080)

        elif browser == "edge":
            options = EdgeOptions()

            if settings.headless:
                options.add_argument("--headless=new")

            for arg in settings.browser_args:
                options.add_argument(arg)

            driver = DriverFactory._create_driver(
                options,
                EdgeService,
                webdriver.Edge,
                EdgeChromiumDriverManager
            )

        else:
            raise ValueError(
                f"Unsupported browser '{browser}'. Use chrome, firefox, or edge."
            )

        # Page load timeout
        driver.set_page_load_timeout(settings.page_load_timeout)

        # Optional maximize (useful for local debugging)
        if not settings.headless:
            try:
                driver.maximize_window()
            except Exception:
                logger.warning(
                    "Could not maximize window (likely remote or headless environment)"
                )

        logger.info("Driver successfully initialized")
        return driver

    @staticmethod
    def quit_driver(driver: webdriver.Remote) -> None:
        """
        Safely quit the WebDriver instance.
        """
        if driver:
            logger.info("Quitting driver")
            driver.quit()