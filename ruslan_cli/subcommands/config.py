"""``ruslan config`` subcommand parser.

Extracted verbatim from ``ruslan_cli/main.py:main()`` (god-file Phase 2).
Handler injected to avoid importing ``main``.
"""

from __future__ import annotations

from typing import Callable


def build_config_parser(subparsers, *, cmd_config: Callable) -> None:
    """Attach the ``config`` subcommand to ``subparsers``."""
    # =========================================================================
    # config command
    # =========================================================================
    config_parser = subparsers.add_parser(
        "config",
        help="View and edit configuration",
        description="Manage Ruslan Agent configuration",
    )
    config_subparsers = config_parser.add_subparsers(dest="config_command")

    # config show (default)
    config_subparsers.add_parser("show", help="Показать текущую конфигурацию")

    # config edit
    config_subparsers.add_parser("edit", help="Открыть файл конфигурации в редакторе")

    # config set
    config_set = config_subparsers.add_parser("set", help="Установить значение конфигурации")
    config_set.add_argument(
        "key", nargs="?", help="Ключ конфигурации (например: model, terminal.backend)"
    )
    config_set.add_argument("value", nargs="?", help="Значение для установки")

    # config path
    config_subparsers.add_parser("path", help="Показать путь к файлу конфигурации")

    # config env-path
    config_subparsers.add_parser("env-path", help="Показать путь к файлу .env")

    # config check
    config_subparsers.add_parser("check", help="Проверить конфигурацию на ошибки")

    # config migrate
    config_subparsers.add_parser("migrate", help="Обновить конфигурацию (добавить новые опции)")

    config_parser.set_defaults(func=cmd_config)
