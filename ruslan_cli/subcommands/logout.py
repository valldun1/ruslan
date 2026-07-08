"""``ruslan logout`` subcommand parser.

Extracted verbatim from ``ruslan_cli/main.py:main()`` (god-file Phase 2).
Handler injected to avoid importing ``main``.
"""

from __future__ import annotations

from typing import Callable


def build_logout_parser(subparsers, *, cmd_logout: Callable) -> None:
    """Attach the ``logout`` subcommand to ``subparsers``."""
    # =========================================================================
    # logout command
    # =========================================================================
    logout_parser = subparsers.add_parser(
        "logout",
        help="Clear authentication for an inference provider",
        description="Очистить авторизацию",
    )
    logout_parser.add_argument(
        "--provider",
        choices=["nous", "openai-codex", "xai-oauth", "spotify"],
        default=None,
        help="Провайдер (по умолчанию: активный)",
    )
    logout_parser.set_defaults(func=cmd_logout)
