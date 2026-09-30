import socket
from collections.abc import Awaitable, Callable
from copy import deepcopy

import uvicorn

from free_claude_code.config.logging_config import InterceptHandler


def uvicorn_log_config(*, console: bool) -> dict[str, object]:
    """Send Uvicorn records to FCC's file and optional standard console handlers."""
    config = deepcopy(uvicorn.config.LOGGING_CONFIG)
    if not console:
        config["formatters"] = {}
        config["handlers"] = {}
    config["handlers"]["fcc"] = {"()": InterceptHandler}
    for name in ("uvicorn", "uvicorn.access"):
        handlers = config["loggers"][name]["handlers"]
        config["loggers"][name]["handlers"] = [*handlers, "fcc"] if console else ["fcc"]
    return config


class RuntimeServer(uvicorn.Server):
    """Notify the runtime before Uvicorn waits for long-lived HTTP responses."""

    def __init__(self, *args: object, **kwargs: object) -> None:
        super().__init__(*args, **kwargs)
        self._startup_complete = False

    def _on_started(self) -> None:
        self._startup_complete = True
        super()._on_started()

    def install_signal_handlers(self) -> None:
        # Keep default behavior and avoid duplicate registrations during test runs.
        return
