"""``ruslan profile`` subcommand parser.

Extracted verbatim from ``ruslan_cli/main.py:main()`` (god-file Phase 2).
Handler injected to avoid importing ``main``.
"""

from __future__ import annotations

from typing import Callable


def build_profile_parser(subparsers, *, cmd_profile: Callable) -> None:
    """Attach the ``profile`` subcommand to ``subparsers``."""
    # =========================================================================
    # profile command
    # =========================================================================
    profile_parser = subparsers.add_parser(
        "profile",
        help="Manage profiles — multiple isolated Ruslan instances",
    )
    profile_subparsers = profile_parser.add_subparsers(dest="profile_action")

    profile_subparsers.add_parser("list", help="Список всех профилей")
    profile_use = profile_subparsers.add_parser(
        "use", help="Установить профиль по умолчанию"
    )
    profile_use.add_argument("profile_name", help="Действие (or 'default')")

    profile_create = profile_subparsers.add_parser(
        "create", help="Создать новый профиль"
    )
    profile_create.add_argument(
        "profile_name", help="Действие (lowercase, alphanumeric)"
    )
    profile_create.add_argument(
        "--clone",
        action="store_true",
        help="Copy config.yaml, .env, SOUL.md, and skills from active profile",
    )
    profile_create.add_argument(
        "--clone-all",
        action="store_true",
        help="Full copy of active profile (all state, excluding per-profile history)",
    )
    profile_create.add_argument(
        "--clone-from",
        metavar="SOURCE",
        help="Source profile to clone from; implies --clone unless --clone-all is set",
    )
    profile_create.add_argument(
        "--no-alias", action="store_true", help="Пропустить создание скрипта-обёртки"
    )
    profile_create.add_argument(
        "--no-skills",
        action="store_true",
        help="Create an empty profile with no bundled skills (opts out of `ruslan update` skill sync)",
    )
    profile_create.add_argument(
        "--description",
        default=None,
        help="One- or two-sentence description of what this profile is good at. "
             "Used by the kanban decomposer to route tasks based on role instead "
             "of profile name alone. Skip and add later via `ruslan profile describe`.",
    )

    profile_delete = profile_subparsers.add_parser("delete", help="Delete a profile")
    profile_delete.add_argument("profile_name", help="Удалить профиль")
    profile_delete.add_argument(
        "-y", "--yes", action="store_true", help="Пропустить подтверждение"
    )

    profile_describe = profile_subparsers.add_parser(
        "describe",
        help="Read or set a profile's description (used by the kanban orchestrator)",
    )
    profile_describe.add_argument(
        "profile_name",
        nargs="?",
        default=None,
        help="Profile to describe (omit + use --all --auto to sweep)",
    )
    profile_describe.add_argument(
        "--text",
        default=None,
        help="Set description to this exact text (overwrites any existing description)",
    )
    profile_describe.add_argument(
        "--auto",
        action="store_true",
        help="Auto-generate description via the auxiliary LLM "
             "(uses auxiliary.profile_describer)",
    )
    profile_describe.add_argument(
        "--overwrite",
        action="store_true",
        help="With --auto, replace user-authored descriptions too (default: only "
             "fill in missing or previously-auto descriptions)",
    )
    profile_describe.add_argument(
        "--all",
        dest="all_missing",
        action="store_true",
        help="With --auto, run on every profile missing a description",
    )

    profile_show = profile_subparsers.add_parser("show", help="Show profile details")
    profile_show.add_argument("profile_name", help="Показать детали профиля")

    profile_alias = profile_subparsers.add_parser(
        "alias", help="Управление скриптами-обёртками"
    )
    profile_alias.add_argument("profile_name", help="Действие")
    profile_alias.add_argument(
        "--remove", action="store_true", help="Удалить скрипт-обёртку"
    )
    profile_alias.add_argument(
        "--name",
        dest="alias_name",
        metavar="NAME",
        help="Пользовательское имя алиаса (по умолчанию: имя профиля)",
    )

    profile_rename = profile_subparsers.add_parser("rename", help="Rename a profile")
    profile_rename.add_argument("old_name", help="Current profile name")
    profile_rename.add_argument("new_name", help="Переименовать профиль")

    profile_export = profile_subparsers.add_parser(
        "export", help="Экспорт профиля в архив"
    )
    profile_export.add_argument("profile_name", help="Профиль для экспорта")
    profile_export.add_argument(
        "-o", "--output", default=None, help="Быстрое резервное копирование (default: <name>.tar.gz)"
    )

    profile_import = profile_subparsers.add_parser(
        "import", help="Импорт профиля из архива"
    )
    profile_import.add_argument("archive", help="Путь к .tar.gz архиву")
    profile_import.add_argument(
        "--name",
        dest="import_name",
        metavar="NAME",
        help="Действие (default: inferred from archive)",
    )

    # ---------- Distribution subcommands (issue #20456) ----------
    profile_install = profile_subparsers.add_parser(
        "install",
        help="Install a profile distribution from a git URL or local directory",
        description=(
            "Install a Ruslan profile distribution. SOURCE can be a git URL "
            "(github.com/user/repo, https://..., git@...) or a local "
            "directory containing distribution.yaml at its root."
        ),
    )
    profile_install.add_argument(
        "source",
        help="Distribution source (git URL or local directory)",
    )
    profile_install.add_argument(
        "--name", dest="install_name", metavar="NAME",
        help="Override profile name (default: read from manifest)",
    )
    profile_install.add_argument(
        "--alias", action="store_true",
        help="Create a shell wrapper alias for the installed profile",
    )
    profile_install.add_argument(
        "--force", action="store_true",
        help="Overwrite an existing profile of the same name (user data preserved)",
    )
    profile_install.add_argument(
        "-y", "--yes", action="store_true",
        help="Skip manifest preview confirmation",
    )

    profile_update = profile_subparsers.add_parser(
        "update",
        help="Re-pull a distribution and apply updates (user data preserved)",
        description=(
            "Fetch the distribution from its recorded source and overwrite "
            "distribution-owned files (SOUL.md, skills/, cron/, mcp.json). "
            "User data (memories, sessions, auth, .env) is never touched. "
            "config.yaml is preserved unless --force-config is passed."
        ),
    )
    profile_update.add_argument("profile_name", help="Profile to update")
    profile_update.add_argument(
        "--force-config", action="store_true",
        help="Also overwrite config.yaml (normally preserved to keep user overrides)",
    )
    profile_update.add_argument(
        "-y", "--yes", action="store_true",
        help="Пропустить подтверждение",
    )

    profile_info = profile_subparsers.add_parser(
        "info",
        help="Show a profile's distribution manifest (version, requirements, source)",
    )
    profile_info.add_argument("profile_name", help="Profile to inspect")

    profile_parser.set_defaults(func=cmd_profile)
