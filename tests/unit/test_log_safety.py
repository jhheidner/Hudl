"""Unit tests for URL redaction used in logging."""

from __future__ import annotations

from src.core.log_safety import redact_url_for_logs


def test_redact_url_strips_query_and_fragment():
    url = "https://identity.example.com/u/login?state=SECRET_TOKEN&foo=1#frag"
    assert "SECRET" not in redact_url_for_logs(url)
    assert "state=" not in redact_url_for_logs(url)
    assert "identity.example.com" in redact_url_for_logs(url)


def test_redact_url_strips_userinfo_from_netloc():
    url = "http://user:password123@grid.example.com:4444/wd/hub"
    safe = redact_url_for_logs(url)
    assert "password123" not in safe
    assert "user:" not in safe
    assert "grid.example.com:4444" in safe
