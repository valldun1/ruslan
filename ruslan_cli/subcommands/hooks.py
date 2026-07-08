"""``ruslan hooks`` subcommand parser.

Extracted verbatim from ``ruslan_cli/main.py:main()`` (god-file Phase 2).
Handler injected to avoid importing ``main``.
"""

from __future__ import annotations

from typing import Callable


def build_hooks_parser(subparsers, *, cmd_hooks: Callable) -> None:
    """Attach the ``hooks`` subcommand to ``subparsers``."""
    # =========================================================================
    hooks_parser = subparsers.add_parser(
        "hooks",
        help="Просмотр и управление shell-хуками",
        description=(
            "Inspect shell-script hooks declared in ~/.ruslan/config.yaml, "
            "test them against synthetic payloads, and manage the first-use "
            "consent allowlist at ~/.ruslan/shell-hooks-allowlist.json."
        ),
    )
    hooks_subparsers = hooks_parser.add_subparsers(dest="hooks_action")

    hooks_subparsers.add_parser(
        "list",
        aliases=["ls"],
        help="Список настроенных хуков с matcher, timeout и статусом разрешения",
    )

    _hk_test = hooks_subparsers.add_parser(
        "test",
        help="Запустить все хуки, соответствующие <event>, на синтетическом payload",
    )
    _hk_test.add_argument(
        "event",
        help="Имя события хука (напр. pre_tool_call, pre_llm_call, subagent_stop)",
    )
    _hk_test.add_argument(
        "--for-tool",
        dest="for_tool",
        default=None,
        help=(
            "Only fire hooks whose matcher matches this tool name "
            "(used for pre_tool_call / post_tool_call)"
        ),
    )
    _hk_test.add_argument(
        "--payload-file",
        dest="payload_file",
        default=None,
        help=(
            "Path to a JSON file whose contents are merged into the "
            "synthetic payload before execution"
        ),
    )

    _hk_revoke = hooks_subparsers.add_parser(
        "revoke",
        aliases=["remove", "rm"],
        help="Удалить записи разрешений команды (вступает в силу при следующем перезапуске)",
    )
    _hk_revoke.add_argument(
        "command",
        help="Точная строка команды для отзыва (как объявлено в config.yaml)",
    )

    hooks_subparsers.add_parser(
        "doctor",
        help=(
            "Check each configured hook: exec bit, allowlist, mtime drift, "
            "JSON validity, and synthetic run timing"
        ),
    )

    hooks_parser.set_defaults(func=cmd_hooks)
