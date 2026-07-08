"""``ruslan tools`` subcommand parser.

Extracted from ``ruslan_cli/main.py:main()`` (god-file Phase 2 follow-up).
Handler injected to avoid importing ``main``.
"""

from __future__ import annotations

from typing import Callable


def build_tools_parser(subparsers, *, cmd_tools: Callable) -> None:
    """Attach the ``tools`` subcommand to ``subparsers``."""
    tools_parser = subparsers.add_parser(
        "tools",
        help="Настроить какие инструменты включены по платформе",
        description=(
            "Enable, disable, or list tools for CLI, Telegram, Discord, etc.\n\n"
            "Built-in toolsets use plain names (e.g. web, memory).\n"
            "MCP tools use server:tool notation (e.g. github:create_issue).\n\n"
            "Run 'ruslan tools' with no subcommand for the interactive configuration UI."
        ),
    )
    tools_parser.add_argument(
        "--summary",
        action="store_true",
        help="Вывести сводку включённых инструментов по платформам и выйти",
    )
    tools_sub = tools_parser.add_subparsers(dest="tools_action")

    # ruslan tools list [--platform cli]
    tools_list_p = tools_sub.add_parser(
        "list",
        help="Показать все инструменты и их статус вкл/откл",
    )
    tools_list_p.add_argument(
        "--platform",
        default="cli",
        help="Платформа для показа (по умолчанию: cli)",
    )

    # ruslan tools disable <name...> [--platform cli]
    tools_disable_p = tools_sub.add_parser(
        "disable",
        help="Отключить наборы инструментов или MCP-инструменты",
    )
    tools_disable_p.add_argument(
        "names",
        nargs="+",
        metavar="NAME",
        help="Имя набора инструментов (напр. web) или MCP-инструмент в форме server:tool",
    )
    tools_disable_p.add_argument(
        "--platform",
        default="cli",
        help="Платформа для применения (по умолчанию: cli)",
    )

    # ruslan tools enable <name...> [--platform cli]
    tools_enable_p = tools_sub.add_parser(
        "enable",
        help="Включить наборы инструментов или MCP-инструменты",
    )
    tools_enable_p.add_argument(
        "names",
        nargs="+",
        metavar="NAME",
        help="Имя набора инструментов или MCP-инструмент в форме server:tool",
    )
    tools_enable_p.add_argument(
        "--platform",
        default="cli",
        help="Платформа для применения (по умолчанию: cli)",
    )

    # ruslan tools post-setup <key>
    tools_postsetup_p = tools_sub.add_parser(
        "post-setup",
        help="Run a provider's post-setup install hook (npm/pip/binary)",
        description=(
            "Run the install/bootstrap hook a tool backend declares — the\n"
            "same step `ruslan tools` runs after you pick a provider that\n"
            "needs extra dependencies (browser Chromium, Camofox, cua-driver,\n"
            "KittenTTS/Piper, ddgs, Spotify, Langfuse, xAI). Stable,\n"
            "non-interactive target the dashboard spawns to drive backend\n"
            "setup. Keys: agent_browser, camofox, cua_driver, kittentts,\n"
            "piper, ddgs, spotify, langfuse, xai_grok."
        ),
    )
    tools_postsetup_p.add_argument(
        "post_setup_key",
        metavar="KEY",
        help="Post-setup hook key (e.g. agent_browser, camofox, kittentts)",
    )
    tools_parser.set_defaults(func=cmd_tools)
