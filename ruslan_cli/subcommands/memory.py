"""``ruslan memory`` subcommand parser.

Extracted from ``ruslan_cli/main.py:main()`` (god-file Phase 2 follow-up).
Handler injected to avoid importing ``main``.
"""

from __future__ import annotations

from typing import Callable


def build_memory_parser(subparsers, *, cmd_memory: Callable) -> None:
    """Attach the ``memory`` subcommand to ``subparsers``."""
    memory_parser = subparsers.add_parser(
        "memory",
        help="Настроить внешнего провайдера памяти",
        description=(
            "Set up and manage external memory provider plugins.\n\n"
            "Available providers: honcho, openviking, mem0, hindsight,\n"
            "holographic, retaindb, byterover.\n\n"
            "Only one external provider can be active at a time.\n"
            "Built-in memory (MEMORY.md/USER.md) is always active."
        ),
    )
    memory_sub = memory_parser.add_subparsers(dest="memory_command")
    _setup_parser = memory_sub.add_parser(
        "setup", help="Интерактивный выбор и настройка провайдера"
    )
    _setup_parser.add_argument(
        "provider",
        nargs="?",
        default=None,
        help="Действие to configure directly (e.g. honcho), skipping the picker",
    )
    memory_sub.add_parser("status", help="Show current memory provider config")
    memory_sub.add_parser("off", help="Показать текущую конфигурацию провайдера памяти")
    _reset_parser = memory_sub.add_parser(
        "reset",
        help="Стереть всю встроенную память (MEMORY.md и USER.md)",
    )
    _reset_parser.add_argument(
        "--yes",
        "-y",
        action="store_true",
        help="Пропустить подтверждение",
    )
    _reset_parser.add_argument(
        "--target",
        choices=["all", "memory", "user"],
        default="all",
        help="Какой хранилище сбросить: 'all' (по умолчанию), 'memory' или 'user'",
    )
    memory_parser.set_defaults(func=cmd_memory)
