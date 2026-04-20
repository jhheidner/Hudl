"""Helpers to reason about Auth0 / Hudl session from URLs (no secrets)."""

from __future__ import annotations

from urllib.parse import urlparse

AUTH0_UNIVERSAL_LOGIN_HOST = "identity.hudl.com"
AUTH0_LOGIN_PATH_FRAGMENTS = ("/u/login/identifier", "/u/login/password")


def is_auth0_login_url(url: str) -> bool:
    u = url.lower()
    return "identity.hudl.com" in u and "/u/login" in u


def is_likely_authenticated(url: str) -> bool:
    """Heuristic: not on Auth0 identifier/password steps."""
    return not is_auth0_login_url(url)


def assert_left_auth0_universal_login(current_url: str) -> None:
    """
    Assert the browser has left Auth0 Universal Login after a successful Hudl app login.

    Checks (1) hostname is not ``identity.hudl.com`` and (2) path markers for the
    identifier/password steps are not present. Use for post-login expectations; keep
    ``is_likely_authenticated`` inside ``LoginPage`` wait loops where mid-flow URLs differ.
    """
    host = (urlparse(current_url).hostname or "").lower()
    if host == AUTH0_UNIVERSAL_LOGIN_HOST:
        raise AssertionError(
            "Expected to leave Auth0 Universal Login "
            f"({AUTH0_UNIVERSAL_LOGIN_HOST!s}) after successful login; "
            f"authenticated app should load on a Hudl application host. Got host: {host!r}"
        )
    url_lower = current_url.lower()
    for fragment in AUTH0_LOGIN_PATH_FRAGMENTS:
        if fragment in url_lower:
            raise AssertionError(
                "Still on Auth0 login path after successful login "
                f"({fragment!r}). URL: {current_url}"
            )
