"""
Top-level argparse construction for the ruslan CLI.

Lives in its own module so other modules (e.g. ``relaunch.py``) can
introspect the parser to discover which flags exist without running the
``main`` fn.

Only the top-level parser and the ``chat`` subparser live here. Every other
subparser (model, gateway, sessions, …) is built inline in ``main.py``
because its dispatch is tightly coupled to module-level ``cmd_*`` functions.
"""

import argparse


# `--profile` / `-p` is consumed by ``main._apply_profile_override`` before
# argparse runs (it sets ``RUSLAN_HOME`` and strips itself from ``sys.argv``),
# so it isn't on the parser. Listed here so all "carry over on relaunch"
# metadata lives in one file.
PRE_ARGPARSE_INHERITED_FLAGS: list[tuple[str, bool]] = [
    ("--profile", True),
    ("-p", True),
]


def _inherited_flag(parser, *args, **kwargs):
    """Register a flag that ``ruslan_cli.relaunch`` should carry over when
    the CLI re-execs itself (e.g. after ``sessions browse`` picks a session,
    or after the setup wizard launches chat).

    Equivalent to ``parser.add_argument(...)`` plus tagging the resulting
    Action with ``inherit_on_relaunch = True`` so the relaunch table builder
    can find it via introspection.
    """
    action = parser.add_argument(*args, **kwargs)
    action.inherit_on_relaunch = True
    return action


_EPILOGUE = """
Examples:
    ruslan                        Start interactive chat
    ruslan chat -q "Hello"        Single query mode
    ruslan --tui                  Launch the modern TUI (or set display.interface: tui)
    ruslan --cli                  Force the classic REPL (overrides display.interface: tui)
    ruslan -c                     Resume the most recent session
    ruslan -c "my project"        Resume a session by name (latest in lineage)
    ruslan --resume <session_id>  Resume a specific session by ID
    ruslan setup                  Run setup wizard
    ruslan logout                 Clear stored authentication
    ruslan auth add <provider>    Add a pooled credential
    ruslan auth list              List pooled credentials
    ruslan auth remove <p> <t>    Remove pooled credential by index, id, or label
    ruslan auth reset <provider>  Clear exhaustion status for a provider
    ruslan model                  Select default model
    ruslan fallback [list]        Show fallback provider chain
    ruslan fallback add           Add a fallback provider (same picker as `ruslan model`)
    ruslan fallback remove        Remove a fallback provider from the chain
    ruslan config                 View configuration
    ruslan config edit            Edit config in $EDITOR
    ruslan config set model gpt-4 Set a config value
    ruslan gateway                Run messaging gateway
    ruslan -s ruslan-agent-dev,github-auth
    ruslan -w                     Start in isolated git worktree
    ruslan gateway install        Install gateway background service
    ruslan sessions list          List past sessions
    ruslan sessions browse        Interactive session picker
    ruslan sessions rename ID T   Rename/title a session
    ruslan logs                   View agent.log (last 50 lines)
    ruslan logs -f                Follow agent.log in real time
    ruslan logs errors            View errors.log
    ruslan logs --since 1h        Lines from the last hour
    ruslan debug share             Upload debug report for support
    ruslan update                 Update to latest version
    ruslan dashboard              Start web UI dashboard (port 9119)
    ruslan dashboard --stop       Stop running dashboard processes
    ruslan dashboard --status     List running dashboard processes

For more help on a command:
    ruslan <command> --help
"""


def build_top_level_parser():
    """Build the top-level parser, the subparsers action, and the ``chat`` subparser.

    Returns ``(parser, subparsers, chat_parser)``. The caller wires
    ``chat_parser.set_defaults(func=cmd_chat)`` and continues registering
    other subparsers via ``subparsers.add_parser(...)``.
    """
    parser = argparse.ArgumentParser(
        prog="ruslan",
        description="Ruslan Agent - AI assistant with tool-calling capabilities",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=_EPILOGUE,
    )

    parser.add_argument(
        "--version", "-V", action="store_true", help="Показать версию и выйти"
    )
    parser.add_argument(
        "-z",
        "--oneshot",
        metavar="PROMPT",
        default=None,
        help=(
            "One-shot mode: send a single prompt and print ONLY the final "
            "response text to stdout. No banner, no spinner, no tool "
            "previews, no session_id line. Tools, memory, rules, and "
            "AGENTS.md in the CWD are loaded as normal; approvals are "
            "auto-bypassed. Intended for scripts / pipes."
        ),
    )
    # --model / --provider are accepted at the top level so they can pair
    # with -z without needing the `chat` subcommand.  If neither -z nor a
    # subcommand consumes them, they fall through harmlessly as None.
    # Mirrors `ruslan chat --model ... --provider ...` semantics.
    _inherited_flag(
        parser,
        "-m",
        "--model",
        default=None,
        help=(
            "Model override for this invocation (e.g. anthropic/claude-sonnet-4.6). "
            "Applies to -z/--oneshot and --tui. Also settable via RUSLAN_INFERENCE_MODEL env var."
        ),
    )
    _inherited_flag(
        parser,
        "--provider",
        default=None,
        help=(
            "Provider override for this invocation (e.g. openrouter, anthropic). "
            "Applies to -z/--oneshot and --tui. The persistent provider lives in config.yaml "
            "under model.provider — use `ruslan setup` or edit the file to change it."
        ),
    )
    parser.add_argument(
        "-t",
        "--toolsets",
        default=None,
        help="Список наборов инструментов через запятую for this invocation. Applies to -z/--oneshot and --tui.",
    )
    parser.add_argument(
        "--resume",
        "-r",
        metavar="SESSION",
        default=None,
        help="Возобновить предыдущую сессию по ID или заголовку",
    )
    parser.add_argument(
        "--continue",
        "-c",
        dest="continue_last",
        nargs="?",
        const=True,
        default=None,
        metavar="SESSION_NAME",
        help="Возобновить сессию по имени, или последнюю, если имя не указано",
    )
    parser.add_argument(
        "--worktree",
        "-w",
        action="store_true",
        default=False,
        help="Запустить в изолированном git worktree (для параллельных агентов)",
    )
    _inherited_flag(
        parser,
        "--accept-hooks",
        action="store_true",
        default=False,
        help=(
            "Auto-approve any unseen shell hooks declared in config.yaml "
            "without a TTY prompt.  Equivalent to RUSLAN_ACCEPT_HOOKS=1 or "
            "hooks_auto_accept: true in config.yaml.  Use on CI / headless "
            "runs that can't prompt."
        ),
    )
    _inherited_flag(
        parser,
        "--skills",
        "-s",
        action="append",
        default=None,
        help="Предзагрузить один или несколько скиллов (повтори флаг или через запятую)",
    )
    _inherited_flag(
        parser,
        "--yolo",
        action="store_true",
        default=False,
        help="Обойти все подтверждения опасных команд (на свой страх и риск)",
    )
    _inherited_flag(
        parser,
        "--pass-session-id",
        action="store_true",
        default=False,
        help="Включить ID сессии в системный промпт агента",
    )
    _inherited_flag(
        parser,
        "--ignore-user-config",
        action="store_true",
        default=False,
        help="Ignore ~/.ruslan/config.yaml and fall back to built-in defaults (credentials in .env are still loaded)",
    )
    _inherited_flag(
        parser,
        "--ignore-rules",
        action="store_true",
        default=False,
        help="Пропустить авто-загрузку AGENTS.md, SOUL.md, .cursorrules, памяти и предзагруженных скиллов",
    )
    _inherited_flag(
        parser,
        "--safe-mode",
        action="store_true",
        default=False,
        help="Troubleshooting mode: disable ALL customizations — user config, AGENTS.md/memory injection, plugins, and MCP servers (implies --ignore-user-config and --ignore-rules)",
    )
    _inherited_flag(
        parser,
        "--tui",
        action="store_true",
        default=False,
        help="Запустить современный TUI вместо классического REPL",
    )
    _inherited_flag(
        parser,
        "--cli",
        action="store_true",
        default=False,
        help="Принудительно использовать классический prompt_toolkit REPL (переопределяет display.interface=tui)",
    )
    _inherited_flag(
        parser,
        "--dev",
        dest="tui_dev",
        action="store_true",
        default=False,
        help="С --tui: запустить TypeScript источники через tsx (пропустить сборку dist)",
    )

    subparsers = parser.add_subparsers(dest="command", help="Команда для выполнения")

    # =========================================================================
    # chat command
    # =========================================================================
    chat_parser = subparsers.add_parser(
        "chat",
        help="Интерактивный чат с агентом",
        description="Запустить интерактивный чат с AI-агентом",
    )
    chat_parser.add_argument(
        "-q", "--query", help="Один запрос (неинтерактивный режим)"
    )
    chat_parser.add_argument(
        "--image", help="Опциональный путь к локальному изображению для прикрепления к запросу"
    )
    _inherited_flag(
        chat_parser,
        "-m", "--model", help="Модель (например: anthropic/claude-sonnet-4)",
    )
    chat_parser.add_argument(
        "-t", "--toolsets", help="Список наборов инструментов через запятую"
    )
    _inherited_flag(
        chat_parser,
        "-s",
        "--skills",
        action="append",
        default=argparse.SUPPRESS,
        help="Предзагрузить один или несколько скиллов (повтори флаг или через запятую)",
    )
    _inherited_flag(
        chat_parser,
        "--provider",
        # No `choices=` here: user-defined providers from config.yaml `providers:`
        # are also valid values, and runtime resolution (resolve_runtime_provider)
        # handles validation/error reporting consistently with the top-level
        # `--provider` flag.
        default=None,
        help="Провайдер инференции (по умолчанию: auto). Built-in or a user-defined name from `providers:` in config.yaml.",
    )
    chat_parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        default=argparse.SUPPRESS,
        help="Подробный вывод",
    )
    chat_parser.add_argument(
        "-Q",
        "--quiet",
        action="store_true",
        help="Тихий режим: убрать баннер, спиннер и превью. Только финальный ответ и инфо о сессии.",
    )
    chat_parser.add_argument(
        "--resume",
        "-r",
        metavar="SESSION_ID",
        default=argparse.SUPPRESS,
        help="Возобновить предыдущую сессию по ID (показывается при выходе)",
    )
    chat_parser.add_argument(
        "--continue",
        "-c",
        dest="continue_last",
        nargs="?",
        const=True,
        default=argparse.SUPPRESS,
        metavar="SESSION_NAME",
        help="Возобновить сессию по имени, или последнюю, если имя не указано",
    )
    chat_parser.add_argument(
        "--worktree",
        "-w",
        action="store_true",
        default=argparse.SUPPRESS,
        help="Запустить в изолированном git worktree (для параллельных агентов на одном репо)",
    )
    _inherited_flag(
        chat_parser,
        "--accept-hooks",
        action="store_true",
        default=argparse.SUPPRESS,
        help=(
            "Auto-approve any unseen shell hooks declared in config.yaml "
            "without a TTY prompt (see also RUSLAN_ACCEPT_HOOKS env var and "
            "hooks_auto_accept: in config.yaml)."
        ),
    )
    chat_parser.add_argument(
        "--checkpoints",
        action="store_true",
        default=False,
        help="Включить файловые чекпоинты (используй /rollback для восстановления)",
    )
    chat_parser.add_argument(
        "--max-turns",
        type=int,
        default=None,
        metavar="N",
        help="Максимум итераций вызова инструментов (по умолчанию: 90)",
    )
    _inherited_flag(
        chat_parser,
        "--yolo",
        action="store_true",
        default=argparse.SUPPRESS,
        help="Обойти все подтверждения опасных команд (на свой страх и риск)",
    )
    _inherited_flag(
        chat_parser,
        "--pass-session-id",
        action="store_true",
        default=argparse.SUPPRESS,
        help="Включить ID сессии в системный промпт агента",
    )
    _inherited_flag(
        chat_parser,
        "--ignore-user-config",
        action="store_true",
        default=argparse.SUPPRESS,
        help="Ignore ~/.ruslan/config.yaml and fall back to built-in defaults (credentials in .env are still loaded). Useful for isolated CI runs, reproduction, and third-party integrations.",
    )
    _inherited_flag(
        chat_parser,
        "--ignore-rules",
        action="store_true",
        default=argparse.SUPPRESS,
        help="Пропустить авто-загрузку AGENTS.md, памяти и скиллов. Сочетай с --ignore-user-config.",
    )
    _inherited_flag(
        chat_parser,
        "--safe-mode",
        action="store_true",
        default=argparse.SUPPRESS,
        help="Troubleshooting mode: disable ALL customizations — user config, AGENTS.md/memory injection, plugins, and MCP servers (implies --ignore-user-config and --ignore-rules). Use to isolate whether a problem comes from your setup or from Ruslan itself.",
    )
    chat_parser.add_argument(
        "--source",
        default=None,
        help="Тег источника сессии (по умолчанию: cli). Используй 'tool' для интеграций.",
    )
    _inherited_flag(
        chat_parser,
        "--tui",
        action="store_true",
        default=False,
        help="Запустить современный TUI вместо классического REPL",
    )
    _inherited_flag(
        chat_parser,
        "--cli",
        action="store_true",
        default=False,
        help="Принудительно использовать классический prompt_toolkit REPL (переопределяет display.interface=tui)",
    )
    _inherited_flag(
        chat_parser,
        "--dev",
        dest="tui_dev",
        action="store_true",
        default=False,
        help="С --tui: запустить TypeScript источники через tsx (пропустить сборку dist)",
    )

    return parser, subparsers, chat_parser
