"""Page object for Hudl login (Auth0 Universal Login on identity.hudl.com)."""

from __future__ import annotations

from selenium.webdriver.common.by import By

from config.settings import settings
from src.core.base_page import BasePage
from src.core.session_checks import is_auth0_login_url, is_likely_authenticated


class LoginPage(BasePage):
    # Locators: prefer stable hooks where possible; XPath text fallbacks are isolated here.
    HUDL_LOGO = (
        By.XPATH,
        "//*[@id='custom-prompt-logo' and @title='Hudl']"
        "|//img[contains(translate(@alt, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'hudl')]"
        "|//a[contains(translate(@aria-label, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'hudl')]"
        "|//*[@data-qa-id='hudl-logo' or contains(@class, 'logo')][self::a or self::img or self::div]",
    )
    EMAIL_INPUT = (
        By.XPATH,
        "//input[@id='email' or @name='email' or @type='email' or @name='username' or @autocomplete='username']",
    )
    PASSWORD_INPUT = (
        By.XPATH,
        "//input[@id='password' or @name='password' or @type='password' or @autocomplete='current-password']",
    )
    CONTINUE_BUTTON = (
        By.XPATH,
        "//button[@type='submit' "
        "or contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'continue') "
        "or contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'next')]",
    )
    LOGIN_BUTTON = (
        By.XPATH,
        "//button[@id='logIn' or @type='submit' "
        "or contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'log in') "
        "or contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'login') "
        "or contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'sign in')]",
    )
    PRIMARY_SUBMIT = (By.CSS_SELECTOR, "button[type='submit'][data-action-button-primary='true']")
    PRIVACY_LINK = (
        By.XPATH,
        "//a[contains(@href, '/privacy') or contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'privacy')]",
    )
    TERMS_LINK = (
        By.XPATH,
        "//a[contains(@href, '/terms') or contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'terms')]",
    )
    CONTINUE_WITH_GOOGLE = (
        By.XPATH,
        "//button[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'google')]"
        "|//a[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'google')]",
    )
    CONTINUE_WITH_FACEBOOK = (
        By.XPATH,
        "//button[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'facebook')]"
        "|//a[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'facebook')]",
    )
    CONTINUE_WITH_APPLE = (
        By.XPATH,
        "//button[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'apple')]"
        "|//a[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'apple')]",
    )
    CREATE_ACCOUNT_LINK = (
        By.XPATH,
        "//a[contains(@href, 'signup') or contains(@href, 'register') "
        "or contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'create account')]",
    )
    FORGOT_PASSWORD_LINK = (
        By.XPATH,
        "//a[contains(@href, 'password-reset') or contains(@href, 'reset-password') or contains(@href, '/recovery') "
        "or contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'forgot')]",
    )
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-qa-id='error-display']")

    def open(self) -> None:
        self.visit("/login")

    def login(self, email: str, password: str) -> None:
        self.type(self.EMAIL_INPUT, email)
        if self.find_first_visible(self.PASSWORD_INPUT) is None:
            self.click(self.CONTINUE_BUTTON)
        self.wait_until_visible(self.PASSWORD_INPUT)
        self.type(self.PASSWORD_INPUT, password)
        self._click_primary_submit()
        self._wait_for_login_outcome()

    def _wait_for_login_outcome(self, timeout_seconds: int | None = None) -> None:
        """Wait until redirect away from Auth0 login, or validation/error is shown (failed attempt)."""
        timeout = timeout_seconds if timeout_seconds is not None else max(settings.explicit_wait, 45)

        def _resolved(driver) -> bool:
            url = driver.current_url
            if is_likely_authenticated(url):
                return True
            if not is_auth0_login_url(url):
                return True
            return bool(self.visible_validation_messages())

        self.webdriver_wait(timeout).until(_resolved)

    def _click_primary_submit(self) -> None:
        primary = self.find_first_visible(self.PRIMARY_SUBMIT)
        if primary is not None:
            self.click_element(primary)
            return
        self.click(self.LOGIN_BUTTON)

    def is_login_button_visible(self) -> bool:
        return self.find_first_visible(self.PRIMARY_SUBMIT) is not None or self.find_first_visible(self.LOGIN_BUTTON) is not None

    def visible_validation_messages(self) -> list[str]:
        messages: list[str] = []
        for css in (".ulp-error-info", "[data-qa-id='error-display']", "[role='alert']"):
            for text in self.visible_texts_under_css(css):
                if text not in messages:
                    messages.append(text)
        for fragment, max_len in (
            ("Incorrect username or password", 200),
            ("Wrong email or password", 200),
        ):
            xpath = f"//*[contains(normalize-space(.), '{fragment}')]"
            for element in self.find_all_now((By.XPATH, xpath)):
                if not element.is_displayed():
                    continue
                text = (element.text or "").strip()
                if not text or len(text) > max_len:
                    continue
                if fragment.lower() in text.lower() and text not in messages:
                    messages.append(text)
        return messages

    def wait_for_validation_containing(self, fragment: str, timeout_seconds: int | None = None) -> None:
        fragment_lower = fragment.lower()
        wait = self.webdriver_wait(timeout_seconds)

        def _predicate(_):
            return any(fragment_lower in msg.lower() for msg in self.visible_validation_messages())

        wait.until(_predicate)

    def submit_identifier_step(self, email: str | None = None) -> None:
        if email is not None:
            self.type(self.EMAIL_INPUT, email)
        self.click(self.CONTINUE_BUTTON)

    def advance_to_password_step(self, email: str) -> None:
        self.submit_identifier_step(email)
        self.wait_until_visible(self.PASSWORD_INPUT)

    def submit_password_step_without_password(self) -> None:
        self.wait_until_visible(self.PASSWORD_INPUT)
        self._click_primary_submit()

    def has_expected_login_elements(self) -> bool:
        has_logo = self.find_first_visible(self.HUDL_LOGO) is not None or "hudl" in self.title.lower()
        return all(
            [
                has_logo,
                self.find_first_visible(self.EMAIL_INPUT) is not None,
                self.find_first_visible(self.CONTINUE_BUTTON) is not None,
            ]
        )

    def open_privacy_page_from_login(self) -> str:
        return self.click_and_wait_for_url(self.PRIVACY_LINK, ("/privacy",))

    def open_terms_page_from_login(self) -> str:
        return self.click_and_wait_for_url(self.TERMS_LINK, ("/terms",))

    def start_google_auth_flow(self) -> str:
        return self.click_and_wait_for_url(self.CONTINUE_WITH_GOOGLE, ("google", "oauth"))

    def start_facebook_auth_flow(self) -> str:
        return self.click_and_wait_for_url(self.CONTINUE_WITH_FACEBOOK, ("facebook", "oauth"))

    def start_apple_auth_flow(self) -> str:
        return self.click_and_wait_for_url(self.CONTINUE_WITH_APPLE, ("apple", "oauth"))

    def open_create_account_from_login(self) -> str:
        return self.click_and_wait_for_url(self.CREATE_ACCOUNT_LINK, ("signup", "register"))

    def open_forgot_password_reset(self, email: str) -> str:
        self.open()
        self.advance_to_password_step(email)
        return self.click_and_wait_for_url(
            self.FORGOT_PASSWORD_LINK,
            ("password-reset", "reset-password", "forgot-password", "/recovery", "resetpassword"),
        )

    def get_error_message(self) -> str:
        if self.is_visible(self.ERROR_MESSAGE):
            return self.get_text(self.ERROR_MESSAGE)
        messages = self.visible_validation_messages()
        return messages[0] if messages else ""
