"""``ruslan claw`` subcommand parser.

Extracted from ``ruslan_cli/main.py:main()`` (god-file Phase 2 follow-up).
Handler injected to avoid importing ``main``.
"""

from __future__ import annotations

from typing import Callable


def build_claw_parser(subparsers, *, cmd_claw: Callable) -> None:
    """Attach the ``claw`` subcommand to ``subparsers``."""
    claw_parser = subparsers.add_parser(
        "claw",
        help="Инструменты миграции OpenClaw",
        description="Migrate settings, memories, skills, and API keys from OpenClaw to Ruslan",
    )
    claw_subparsers = claw_parser.add_subparsers(dest="claw_action")

    # claw migrate
    claw_migrate = claw_subparsers.add_parser(
        "migrate",
        help="Migrate from OpenClaw to Ruslan",
        description="Импорт настроек, памяти, скиллов и API-ключей из установки OpenClaw. "
        "Always shows a preview before making changes.",
    )
    claw_migrate.add_argument(
        "--source", help="Путь к директории OpenClaw (по умолчанию: ~/.openclaw)"
    )
    claw_migrate.add_argument(
        "--dry-run",
        action="store_true",
        help="Только предпросмотр — остановиться после показа что будет мигрировано",
    )
    claw_migrate.add_argument(
        "--preset",
        choices=["user-data", "full"],
        default="full",
        help="Migration preset (default: full). Neither preset imports secrets — "
        "pass --migrate-secrets to include API keys.",
    )
    claw_migrate.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing files (default: refuse to apply when the plan has conflicts)",
    )
    claw_migrate.add_argument(
        "--migrate-secrets",
        action="store_true",
        help="Включить разрешённые секреты (TELEGRAM_BOT_TOKEN, API keys и т.д.). "
        "Required even under --preset full.",
    )
    claw_migrate.add_argument(
        "--no-backup",
        action="store_true",
        help="Skip the pre-migration zip snapshot of ~/.ruslan/ (by default a "
        "single restore-point archive is written to ~/.ruslan/backups/ "
        "before apply; restorable with 'ruslan import').",
    )
    claw_migrate.add_argument(
        "--workspace-target", help="Абсолютный путь для копирования инструкций рабочего пространства"
    )
    claw_migrate.add_argument(
        "--skill-conflict",
        choices=["skip", "overwrite", "rename"],
        default="skip",
        help="Как обрабатывать конфликты имён навыков (по умолчанию: skip)",
    )
    claw_migrate.add_argument(
        "--yes", "-y", action="store_true", help="Пропустить подтверждения"
    )

    # claw cleanup
    claw_cleanup = claw_subparsers.add_parser(
        "cleanup",
        aliases=["clean"],
        help="Архивировать оставшиеся директории OpenClaw после миграции",
        description="Поиск и архивация оставшихся директорий OpenClaw для предотвращения фрагментации состояния",
    )
    claw_cleanup.add_argument(
        "--source", help="Путь к конкретной директории OpenClaw для очистки"
    )
    claw_cleanup.add_argument(
        "--dry-run",
        action="store_true",
        help="Предпросмотр того, что будет архивировано, без изменений",
    )
    claw_cleanup.add_argument(
        "--yes", "-y", action="store_true", help="Пропустить подтверждения"
    )
    claw_parser.set_defaults(func=cmd_claw)
