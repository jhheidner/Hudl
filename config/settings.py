"""Central configuration for the test framework."""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


def _as_bool(value: str, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y"}
def _as_list(value:str | None) -> list [str]:
    if not value:
        return[]
    return [item.strip() for item in value.split(",") if item.strip()]


@dataclass(frozen=True)
class FrameworkSettings:
    base_url: str = os.getenv("BASE_URL", "https://www.hudl.com")
    browser: str = os.getenv("BROWSER", "chrome").lower()
    headless: bool = _as_bool(os.getenv("HEADLESS"), default=False)
    explicit_wait: int = int(os.getenv("EXPLICIT_WAIT", "15"))
    page_load_timeout: int = int(os.getenv("PAGE_LOAD_TIMEOUT", "30"))
    remote_url:str | None = os.getenv("REMOTE_URL")
    browser_args: list[str] = tuple(_as_list(os.getenv("BROWSER_ARGS")))

settings = FrameworkSettings()
