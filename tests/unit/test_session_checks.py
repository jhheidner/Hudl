"""Unit tests for Auth0 / session URL helpers."""

from __future__ import annotations

import pytest

from src.core.session_checks import (
    AUTH0_LOGIN_PATH_FRAGMENTS,
    AUTH0_UNIVERSAL_LOGIN_HOST,
    assert_left_auth0_universal_login,
)


def test_assert_left_auth0_passes_for_www_hudl() -> None:
    assert_left_auth0_universal_login("https://www.hudl.com/home")


def test_assert_left_auth0_passes_for_app_subdomain() -> None:
    assert_left_auth0_universal_login("https://app.hudl.com/org/team")


def test_assert_left_auth0_fails_on_identity_host() -> None:
    with pytest.raises(AssertionError, match=AUTH0_UNIVERSAL_LOGIN_HOST):
        assert_left_auth0_universal_login("https://identity.hudl.com/authorize?client=x")


def test_assert_left_auth0_fails_on_login_path_markers() -> None:
    for fragment in AUTH0_LOGIN_PATH_FRAGMENTS:
        with pytest.raises(AssertionError, match="Still on Auth0 login path"):
            assert_left_auth0_universal_login(f"https://www.hudl.com{fragment}?state=abc")
