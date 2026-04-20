"""Credentials holder that does not expose secrets in repr/tracebacks."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RedactedHudlCredentials:
    email: str
    password: str

    def __repr__(self) -> str:
        return "RedactedHudlCredentials(email=<redacted>, password=<redacted>)"

    def __str__(self) -> str:
        return self.__repr__()
