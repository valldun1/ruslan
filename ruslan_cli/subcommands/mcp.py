"""``ruslan mcp`` subcommand parser.

Extracted from ``ruslan_cli/main.py:main()`` (god-file Phase 2 follow-up).
Handler injected to avoid importing ``main``.
"""

from __future__ import annotations

import argparse
from typing import Callable

from ruslan_cli.subcommands._shared import add_accept_hooks_flag


def build_mcp_parser(subparsers, *, cmd_mcp: Callable) -> None:
    """Attach the ``mcp`` subcommand to ``subparsers``."""
    mcp_parser = subparsers.add_parser(
        "mcp",
        help="Manage MCP servers and run Ruslan as an MCP server",
        description=(
            "Manage MCP server connections and run Ruslan as an MCP server.\n\n"
            "MCP servers provide additional tools via the Model Context Protocol.\n"
            "Use 'ruslan mcp add' to connect to a new server, or\n"
            "'ruslan mcp serve' to expose Ruslan conversations over MCP."
        ),
    )
    mcp_sub = mcp_parser.add_subparsers(dest="mcp_action")

    mcp_serve_p = mcp_sub.add_parser(
        "serve",
        help="Run Ruslan as an MCP server (expose conversations to other agents)",
    )
    mcp_serve_p.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Включить подробное логирование в stderr",
    )
    add_accept_hooks_flag(mcp_serve_p)

    mcp_add_p = mcp_sub.add_parser(
        "add", help="Добавить MCP-сервер (установка с обнаружением)"
    )
    mcp_add_p.add_argument("name", help="Имя сервера (используется как ключ конфига)")
    mcp_add_p.add_argument("--url", help="HTTP/SSE endpoint URL")
    # dest="mcp_command" so this flag does not clobber the top-level
    # subparser's args.command attribute, which the dispatcher reads to
    # route to cmd_mcp.  Without an explicit dest, argparse derives
    # dest="command" from the flag name and sets it to None when the
    # flag is omitted, causing `ruslan mcp add ...` to fall through to
    # interactive chat.
    mcp_add_p.add_argument(
        "--command", dest="mcp_command", help="Stdio команда (напр. npx)"
    )
    mcp_add_p.add_argument(
        "--args",
        nargs=argparse.REMAINDER,
        default=[],
        help="Аргументы для stdio команды; must be the last option",
    )
    mcp_add_p.add_argument("--auth", choices=["oauth", "header"], help="Метод авторизации")
    mcp_add_p.add_argument("--preset", help="Known MCP preset name")
    mcp_add_p.add_argument(
        "--env",
        nargs="*",
        default=[],
        help="Переменные окружения для stdio серверов (KEY=VALUE)",
    )

    mcp_rm_p = mcp_sub.add_parser("remove", aliases=["rm"], help="Remove an MCP server")
    mcp_rm_p.add_argument("name", help="Удалить MCP-сервер")

    mcp_sub.add_parser("list", aliases=["ls"], help="Список настроенных MCP-серверов")

    mcp_test_p = mcp_sub.add_parser("test", help="Test MCP server connection")
    mcp_test_p.add_argument("name", help="Имя сервера для тестирования")

    mcp_cfg_p = mcp_sub.add_parser(
        "configure", aliases=["config"], help="Переключить выбор инструментов"
    )
    mcp_cfg_p.add_argument("name", help="Имя сервера для настройки")

    mcp_login_p = mcp_sub.add_parser(
        "login",
        help="Форсировать повторную авторизацию для OAuth-сервера MCP",
    )
    mcp_login_p.add_argument("name", help="Имя сервера для повторной авторизации")

    # ── Catalog (Nous-approved MCPs shipped with the repo) ─────────────────
    mcp_sub.add_parser(
        "picker",
        help="Interactive catalog picker (also the default for `ruslan mcp`)",
    )
    mcp_sub.add_parser(
        "catalog",
        help="List Nous-approved MCPs available for one-click install",
    )
    mcp_install_p = mcp_sub.add_parser(
        "install",
        help="Install a catalog MCP by name (e.g. `ruslan mcp install n8n`)",
    )
    mcp_install_p.add_argument(
        "identifier",
        help="Catalog entry name (or `official/<name>`)",
    )

    add_accept_hooks_flag(mcp_parser)
    mcp_parser.set_defaults(func=cmd_mcp)
