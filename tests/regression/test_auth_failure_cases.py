"""Negative and validation tests for login and create-account flows."""

from __future__ import annotations

import pytest

from src.pages.create_account_page import CreateAccountPage
from src.pages.login_page import LoginPage


@pytest.mark.regression
@pytest.mark.negative
def test_login_identifier_requires_email(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.submit_identifier_step(email=None)
    login_page.wait_for_validation_containing("Enter an email address")


@pytest.mark.regression
@pytest.mark.negative
def test_login_identifier_rejects_invalid_email_format(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.submit_identifier_step(email="not-a-valid-email")
    login_page.wait_for_validation_containing("valid email")


@pytest.mark.regression
@pytest.mark.negative
def test_login_password_step_requires_password(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.advance_to_password_step("no-real-user-12345@example.com")
    login_page.submit_password_step_without_password()
    login_page.wait_for_validation_containing("Enter your password")


@pytest.mark.regression
@pytest.mark.negative
def test_login_wrong_password_shows_error(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login("no-real-user-12345@example.com", "DefinitelyWrongPassword!1")
    assert login_page.get_error_message(), "Expected an error after submitting a wrong password."


@pytest.mark.regression
@pytest.mark.negative
def test_create_account_requires_name_and_email(driver):
    page = CreateAccountPage(driver)
    page.open_via_login()
    page.submit_continue()
    page.wait_for_validation_containing("first name")
    page.wait_for_validation_containing("last name")
    page.wait_for_validation_containing("email address")


@pytest.mark.regression
@pytest.mark.negative
def test_create_account_rejects_invalid_email(driver):
    page = CreateAccountPage(driver)
    page.open_via_login()
    page.fill_signup_identifier(first_name="Test", last_name="User", email="notanemailformat")
    page.submit_continue()
    page.wait_for_validation_containing("valid email", timeout=20)


@pytest.mark.regression
@pytest.mark.negative
def test_create_account_requires_names_when_email_provided(driver):
    page = CreateAccountPage(driver)
    page.open_via_login()
    page.fill_signup_identifier(email="someone@example.com")
    page.submit_continue()
    page.wait_for_validation_containing("first name")
    page.wait_for_validation_containing("last name")
