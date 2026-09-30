"""CLI entrypoints for free-claude-code."""

from __future__ import annotations

import argparse


def main() -> None:
    parser = argparse.ArgumentParser(description="free-claude-code CLI")
    parser.add_argument("--version", action="store_true", help="Show version and exit")
    args = parser.parse_args()

    if args.version:
        from free_claude_code import __version__
        print(__version__)
        return

    print("free-claude-code CLI initialized")


if __name__ == "__main__":
    main()
