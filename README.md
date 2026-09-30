# free-claude-code

Unlimited FREE AI coding. Connect Claude Code, Codex, Cursor, Cline, Copilot, and similar workflows to free provider backends via a resilient routing layer.

This repository captures the server/runtime pieces we worked on earlier, including:

- the CLI entrypoint and server supervisor
- custom runtime shutdown/logging hooks for Uvicorn
- regression tests covering logging behavior across restarts

## Highlights

- provider fallback and routing support for free model endpoints
- graceful runtime shutdown before long-lived HTTP work completes
- structured logging to file output while optionally mirroring to console
- restart-aware behavior and regression coverage

## Project structure

```text
src/
  free_claude_code/
    cli/
      commands.py
      uvicorn_server.py

tests/
  cli/
    test_server_logging.py
```

## Notes

This is a minimal scaffold based on the code and tests captured in the earlier implementation session. It is intended to be expanded into the full command-line product and provider bridge.
