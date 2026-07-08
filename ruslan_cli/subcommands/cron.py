"""``ruslan cron`` subcommand parser.

Extracted verbatim from ``ruslan_cli/main.py:main()`` — same arguments, same
``func=cmd_cron`` dispatch. The handler is injected so this module does not
import ``main`` (cycle avoidance).
"""

from __future__ import annotations

from typing import Callable

from ruslan_cli.subcommands._shared import add_accept_hooks_flag


def build_cron_parser(subparsers, *, cmd_cron: Callable) -> None:
    """Attach the ``cron`` subcommand (and its sub-actions) to ``subparsers``."""
    cron_parser = subparsers.add_parser(
        "cron", help="Управление cron-задачами", description="Manage scheduled tasks"
    )
    cron_subparsers = cron_parser.add_subparsers(dest="cron_command")

    # cron list
    cron_list = cron_subparsers.add_parser("list", help="List scheduled jobs")
    cron_list.add_argument("--all", action="store_true", help="Список запланированных задач")

    # cron create/add
    cron_create = cron_subparsers.add_parser(
        "create", aliases=["add"], help="Создать запланированную задачу"
    )
    cron_create.add_argument(
        "schedule", help="Расписание: '·30m', '·every 2h', или '·0 9 * * *'"
    )
    cron_create.add_argument(
        "prompt", nargs="?", help="Опциональный промпт или инструкция задачи"
    )
    cron_create.add_argument("--name", help="Опциональное человеко-читаемое название задачи")
    cron_create.add_argument(
        "--deliver",
        help="Цель доставки: origin, local, telegram, discord, signal, или platform:chat_id",
    )
    cron_create.add_argument("--repeat", type=int, help="Опциональное количество повторов")
    cron_create.add_argument(
        "--skill",
        dest="skills",
        action="append",
        help="Подключить скилл. Повторите для добавления нескольких скиллов.",
    )
    cron_create.add_argument(
        "--script",
        help=(
            "Path to a script under ~/.ruslan/scripts/. Default mode: "
            "script stdout is injected into the agent's prompt each run. "
            "With --no-agent: the script IS the job and its stdout is "
            "delivered verbatim. .sh/.bash files run via bash, everything "
            "else via Python."
        ),
    )
    cron_create.add_argument(
        "--no-agent",
        dest="no_agent",
        action="store_true",
        default=False,
        help=(
            "Skip the LLM entirely — run --script on schedule and deliver "
            "its stdout directly. Empty stdout = silent. Classic watchdog "
            "pattern (memory alerts, disk alerts, CI pings)."
        ),
    )
    cron_create.add_argument(
        "--workdir",
        help="Absolute path for the job to run from. Injects AGENTS.md / CLAUDE.md / .cursorrules from that directory and uses it as the cwd for terminal/file/code_exec tools. Omit to preserve old behaviour (no project context files).",
    )

    # cron edit
    cron_edit = cron_subparsers.add_parser(
        "edit", help="Edit an existing scheduled job"
    )
    cron_edit.add_argument("job_id", help="Job ID to edit")
    cron_edit.add_argument("--schedule", help="New schedule")
    cron_edit.add_argument("--prompt", help="New prompt/task instruction")
    cron_edit.add_argument("--name", help="New job name")
    cron_edit.add_argument("--deliver", help="New delivery target")
    cron_edit.add_argument("--repeat", type=int, help="Редактировать запланированную задачу")
    cron_edit.add_argument(
        "--skill",
        dest="skills",
        action="append",
        help="Заменить скиллы задачи этим набором. Повторите для добавления нескольких скиллов.",
    )
    cron_edit.add_argument(
        "--add-skill",
        dest="add_skills",
        action="append",
        help="Добавить скилл без замены существующего списка. Можно повторять.",
    )
    cron_edit.add_argument(
        "--remove-skill",
        dest="remove_skills",
        action="append",
        help="Удалить конкретный скилл. Можно повторять.",
    )
    cron_edit.add_argument(
        "--clear-skills",
        action="store_true",
        help="Удалить все скиллы из задачи",
    )
    cron_edit.add_argument(
        "--script",
        help=(
            "Path to a script under ~/.ruslan/scripts/. Pass empty string to clear. "
            "With --no-agent the script IS the job; otherwise its stdout is "
            "injected into the agent's prompt each run."
        ),
    )
    cron_edit.add_argument(
        "--no-agent",
        dest="no_agent",
        action="store_const",
        const=True,
        default=None,
        help=(
            "Enable no-agent mode on this job (requires --script or an "
            "existing script on the job)."
        ),
    )
    cron_edit.add_argument(
        "--agent",
        dest="no_agent",
        action="store_const",
        const=False,
        help="Disable no-agent mode on this job (reverts to LLM-driven execution).",
    )
    cron_edit.add_argument(
        "--workdir",
        help="Absolute path for the job to run from (injects AGENTS.md etc. and sets terminal cwd). Pass empty string to clear.",
    )

    # lifecycle actions
    cron_pause = cron_subparsers.add_parser("pause", help="Pause a scheduled job")
    cron_pause.add_argument("job_id", help="Приостановить задачу")

    cron_resume = cron_subparsers.add_parser("resume", help="Resume a paused job")
    cron_resume.add_argument("job_id", help="Возобновить приостановленную задачу")

    cron_run = cron_subparsers.add_parser(
        "run", help="Запустить задачу в следующем тике планировщика"
    )
    cron_run.add_argument("job_id", help="ID задачи для запуска")
    add_accept_hooks_flag(cron_run)

    cron_remove = cron_subparsers.add_parser(
        "remove", aliases=["rm", "delete"], help="Удалить запланированную задачу"
    )
    cron_remove.add_argument("job_id", help="ID задачи для удаления")

    # cron status
    cron_subparsers.add_parser("status", help="Проверить, запущен ли cron-планировщик")

    # cron tick (mostly for debugging)
    cron_tick = cron_subparsers.add_parser("tick", help="Запустить подходящие задачи один раз и выйти")
    add_accept_hooks_flag(cron_tick)
    add_accept_hooks_flag(cron_parser)
    cron_parser.set_defaults(func=cmd_cron)
