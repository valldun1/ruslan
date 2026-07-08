"""``ruslan update`` subcommand parser.

Extracted verbatim from ``ruslan_cli/main.py:main()`` (god-file Phase 2).
Handler injected to avoid importing ``main``.
"""

from __future__ import annotations

from typing import Callable


def build_update_parser(subparsers, *, cmd_update: Callable) -> None:
    """Attach the ``update`` subcommand to ``subparsers``."""
    # =========================================================================
    # update command
    # =========================================================================
    update_parser = subparsers.add_parser(
        "update",
        help="Update Ruslan Agent to the latest version",
        description="Обновить Руслана",
    )
    update_parser.add_argument(
        "--gateway",
        action="store_true",
        default=False,
        help="Режим шлюза: IPC через файлы вместо stdin",
    )
    update_parser.add_argument(
        "--check",
        action="store_true",
        default=False,
        help="Проверить наличие обновления без установки",
    )
    update_parser.add_argument(
        "--no-backup",
        action="store_true",
        default=False,
        help="Skip the pre-update backup for this run (overrides updates.pre_update_backup)",
    )
    update_parser.add_argument(
        "--backup",
        action="store_true",
        default=False,
        help="Force a pre-update backup for this run (off by default; overrides updates.pre_update_backup)",
    )
    update_parser.add_argument(
        "--yes",
        "-y",
        action="store_true",
        default=False,
        help="Assume yes for interactive prompts (config migration, stash restore). API-key entry is skipped; run 'ruslan config migrate' separately for those.",
    )
    update_parser.add_argument(
        "--branch",
        default=None,
        metavar="NAME",
        help=(
            "Обновить из этой ветки вместо ветки по умолчанию (master). "
            "If the local checkout is on a different branch, ruslan will "
            "switch to the requested branch first (auto-stashing any "
            "uncommitted changes)."
        ),
    )
    update_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Windows: proceed with the update even when another ruslan.exe is detected. The concurrent process will likely cause WinError 32 warnings and may leave a reboot-deferred .exe replacement.",
    )
    update_parser.set_defaults(func=cmd_update)
