"""``ruslan insights`` subcommand parser.

Extracted from ``ruslan_cli/main.py:main()`` (god-file Phase 2 follow-up).
Handler injected to avoid importing ``main``.
"""

from __future__ import annotations

from typing import Callable


def build_insights_parser(subparsers, *, cmd_insights: Callable) -> None:
    """Attach the ``insights`` subcommand to ``subparsers``."""
    insights_parser = subparsers.add_parser(
        "insights",
        help="Показать аналитику использования и статистику",
        description="Анализ истории сессий для показа использования токенов, стоимости, шаблонов инструментов и трендов активности",
    )
    insights_parser.add_argument(
        "--days", type=int, default=30, help="Количество дней для анализа (по умолчанию: 30)"
    )
    insights_parser.add_argument(
        "--source", help="Фильтр по платформе (cli, telegram, discord, и т.д.)"
    )
    insights_parser.set_defaults(func=cmd_insights)
