from __future__ import annotations

import contextlib
import os
import signal
import threading
import time
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import uvicorn

from free_claude_code.config.settings import Settings
from free_claude_code.runtime.bootstrap import build_asgi_app
from free_claude_code.runtime.runtime import Runtime

from .uvicorn_server import RuntimeServer, uvicorn_log_config


@dataclass
class ServerSupervisor:
    """Owns a Uvicorn server process and wiring for runtime lifecycle events."""

    console_logging: bool = True
    _server: RuntimeServer | None = None
    _thread: threading.Thread | None = None

    def _run_bound(
        self,
        settings: Settings,
        extra: list[str],
        *,
        open_admin_browser: bool,
        restart_generation: int,
    ) -> None:
        """Boot the runtime server with the configured settings."""
        from free_claude_code.runtime.bootstrap import build_asgi_app

        asgi_app = build_asgi_app(
            settings,
            extra=extra,
            open_admin_browser=open_admin_browser,
            restart_generation=restart_generation,
        )

        server = RuntimeServer(
            config=uvicorn.Config(
                app=asgi_app,
                host=settings.host,
                port=settings.port,
                log_level="debug",
                log_config=(
                    uvicorn.config.LOGGING_CONFIG if self._console_logging else None
                ),
                log_config=uvicorn_log_config(console=self._console_logging),
                timeout_graceful_shutdown=SERVER_GRACEFUL_SHUTDOWN_SECONDS,
            )
        )

        self._server = server
        self._thread = threading.Thread(target=server.run, daemon=True)
        self._thread.start()

        while not server.started and not server.should_exit:
            time.sleep(0.05)

    def start(self, settings: Settings, *, open_admin_browser: bool = False) -> None:
        self._run_bound(
            settings,
            [],
            open_admin_browser=open_admin_browser,
            restart_generation=0,
        )

    def stop(self) -> None:
        if self._server is not None:
            self._server.should_exit = True
        if self._thread is not None:
            self._thread.join(timeout=5)
