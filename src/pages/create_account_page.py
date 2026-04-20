"""Page object for Hudl create-account (Auth0 signup identifier) flow."""

from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from config.settings import settings
from src.core.base_page import BasePage
from src.pages.login_page import LoginPage


class CreateAccountPage(BasePage):
    FIRST_NAME = (By.ID, "first-name")
    LAST_NAME = (By.ID, "last-name")
    EMAIL = (By.ID, "email")
    CONTINUE = (By.CSS_SELECTOR, "button._button-signup-id[data-action-button-primary='true']")

    def open_via_login(self) -> None:
        login_page = LoginPage(self.driver)
        login_page.open()
        login_page.click_and_wait_for_url(login_page.CREATE_ACCOUNT_LINK, ("signup", "register"))
        self.wait_until_visible(self.EMAIL)

    def submit_continue(self) -> None:
        self.click(self.CONTINUE)

    def fill_signup_identifier(
        self,
        first_name: str | None = None,
        last_name: str | None = None,
        email: str | None = None,
    ) -> None:
        if first_name is not None:
            self.type(self.FIRST_NAME, first_name)
        if last_name is not None:
            self.type(self.LAST_NAME, last_name)
        if email is not None:
            self.type(self.EMAIL, email)
            self.find(self.EMAIL).send_keys(Keys.TAB)

    def visible_validation_messages(self) -> list[str]:
        return self.visible_texts_under_css(".ulp-error-info")

    def wait_for_validation_containing(self, fragment: str, timeout: int | None = None) -> None:
        fragment_lower = fragment.lower()
        wait = self.webdriver_wait(timeout if timeout is not None else settings.explicit_wait)

        def _predicate(_):
            return any(fragment_lower in msg.lower() for msg in self.visible_validation_messages())

        wait.until(_predicate)
