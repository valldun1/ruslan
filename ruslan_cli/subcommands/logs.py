"""``ruslan logs`` subcommand parser.

Extracted verbatim from ``ruslan_cli/main.py:main()`` (god-file Phase 2).
Handler injected to avoid importing ``main``.
"""

from __future__ import annotations

import argparse
from typing import Callable


def build_logs_parser(subparsers, *, cmd_logs: Callable) -> None:
    """Attach the ``logs`` subcommand to ``subparsers``."""
    # =========================================================================
    # logs command
    # =========================================================================
    logs_parser = subparsers.add_parser(
        "logs",
        help="View and filter Ruslan log files",
        description="Просмотр, tail и фильтрация agent.log / errors.log / gateway.log / gui.log / desktop.log",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
    ruslan logs                    Show last 50 lines of agent.log
    ruslan logs -f                 Follow agent.log in real time
    ruslan logs errors             Show last 50 lines of errors.log
    ruslan logs gateway -n 100     Show last 100 lines of gateway.log
    ruslan logs gui -f             Follow gui.log in real time
    ruslan logs desktop -f         Follow desktop.log (Electron app boot/backend)
    ruslan logs --level WARNING    Only show WARNING and above
    ruslan logs --session abc123   Filter by session ID
    ruslan logs --component tools  Only show tool-related lines
    ruslan logs --since 1h         Lines from the last hour
    ruslan logs --since 30m -f     Follow, starting from 30 min ago
    ruslan logs list               List available log files with sizes
""",
    )
    logs_parser.add_argument(
        "log_name",
        nargs="?",
        default="agent",
        help="Log to view: agent (default), errors, gateway, gui, or 'list' to show available files",
    )
    logs_parser.add_argument(
        "-n",
        "--lines",
        type=int,
        default=50,
        help="Количество строк для показа (по умолчанию: 50)",
    )
    logs_parser.add_argument(
        "-f",
        "--follow",
        action="store_true",
        help="Следить за логом в реальном времени (как tail -f)",
    )
    logs_parser.add_argument(
        "--level",
        metavar="LEVEL",
        help="Минимальный уровень логирования для показа (DEBUG, INFO, WARNING, ERROR)",
    )
    logs_parser.add_argument(
        "--session",
        metavar="ID",
        help="Фильтр по подстроке ID сессии",
    )
    logs_parser.add_argument(
        "--since",
        metavar="TIME",
        help="Показать строки с времени TIME назад (напр. 1h, 30m, 2d)",
    )
    logs_parser.add_argument(
        "--component",
        metavar="NAME",
        help="Фильтр по компоненту: gateway, agent, tools, cli, cron, gui",
    )
    logs_parser.set_defaults(func=cmd_logs)
