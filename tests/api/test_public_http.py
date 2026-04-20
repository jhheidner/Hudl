"""
Public HTTP surface checks — support UI coverage, do not replace browser tests.

Uses the same ``BASE_URL`` as Selenium (``config.settings``). No auth headers,
no guessed internal routes.
"""

from __future__ import annotations

from urllib.parse import urlparse

import pytest
import requests

from config.settings import settings


@pytest.mark.api
def test_public_home_returns_200() -> None:
    """Top-level marketing/app entry responds successfully."""
    url = settings.base_url.rstrip("/") + "/"
    response = requests.get(url, timeout=30)
    assert response.status_code == 200, f"GET {url!r} expected 200, got {response.status_code}"


@pytest.mark.api
def test_login_path_responds_without_client_error() -> None:
    """Login route is reachable (SPA may return 200; some stacks redirect first)."""
    base = settings.base_url.rstrip("/")
    url = f"{base}/login"
    response = requests.get(url, timeout=30, allow_redirects=False)
    assert response.status_code in (200, 301, 302, 303, 307, 308), (
        f"GET {url!r} expected 2xx/redirect family, got {response.status_code}"
    )


@pytest.mark.api
def test_login_follow_redirects_ends_on_hudl_host() -> None:
    """Following redirects for /login lands on a hudl.com host (app or identity)."""
    base = settings.base_url.rstrip("/")
    url = f"{base}/login"
    response = requests.get(url, timeout=30, allow_redirects=True)
    assert response.status_code == 200, f"After redirects, expected 200, got {response.status_code}"
    final_host = urlparse(response.url).hostname or ""
    assert final_host.endswith("hudl.com"), (
        f"Expected final URL on a *.hudl.com host after /login; got {response.url!r}"
    )
