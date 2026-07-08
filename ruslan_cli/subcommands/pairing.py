"""``ruslan pairing`` subcommand parser.

Extracted from ``ruslan_cli/main.py:main()`` (god-file Phase 2 follow-up).
Handler injected to avoid importing ``main``.
"""

from __future__ import annotations

from typing import Callable


def build_pairing_parser(subparsers, *, cmd_pairing: Callable) -> None:
    """Attach the ``pairing`` subcommand to ``subparsers``."""
    pairing_parser = subparsers.add_parser(
        "pairing",
        help="Управление кодами паринга DM для авторизации пользователей",
        description="Подтверждение или отзыв доступа пользователя через коды сопряжения",
    )
    pairing_sub = pairing_parser.add_subparsers(dest="pairing_action")

    pairing_sub.add_parser("list", help="Показать ожидающих + одобренных пользователей")

    pairing_approve_parser = pairing_sub.add_parser(
        "approve", help="Одобрить код паринга"
    )
    pairing_approve_parser.add_argument(
        "platform", help="Имя платформы (telegram, discord, slack, whatsapp)"
    )
    pairing_approve_parser.add_argument("code", help="Код паринга для одобрения")

    pairing_revoke_parser = pairing_sub.add_parser("revoke", help="Revoke user access")
    pairing_revoke_parser.add_argument("platform", help="Platform name")
    pairing_revoke_parser.add_argument("user_id", help="Отзыв доступа пользователя")

    pairing_sub.add_parser("clear-pending", help="Очистить все ожидающие коды")
    pairing_parser.set_defaults(func=cmd_pairing)
