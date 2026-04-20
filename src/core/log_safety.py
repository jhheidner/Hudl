"""Helpers so logs never echo secrets (tokens in URLs, passwords, PII in fields)."""

from __future__ import annotations

from urllib.parse import urlparse, urlunparse


def redact_url_for_logs(url: str) -> str:
    """
    Safe to log: scheme, host, port, path — no userinfo, query, or fragment.

    Query strings often carry OAuth state; netloc may embed grid credentials (user:pass@host).
    """
    try:
        parsed = urlparse(url)
        host = parsed.hostname or ""
        if parsed.port and host:
            netloc = f"{host}:{parsed.port}"
        elif host:
            netloc = host
        else:
            netloc = parsed.netloc.split("@")[-1] if "@" in parsed.netloc else parsed.netloc
        return urlunparse((parsed.scheme, netloc, parsed.path, parsed.params, "", ""))
    except Exception:
        return "<url redacted>"
