"""``ruslan webhook`` subcommand parser.

Extracted verbatim from ``ruslan_cli/main.py:main()`` (god-file Phase 2).
Handler injected to avoid importing ``main``.
"""

from __future__ import annotations

from typing import Callable


def build_webhook_parser(subparsers, *, cmd_webhook: Callable) -> None:
    """Attach the ``webhook`` subcommand to ``subparsers``."""
    # =========================================================================
    # webhook command
    # =========================================================================
    webhook_parser = subparsers.add_parser(
        "webhook",
        help="Manage dynamic webhook subscriptions",
        description="Управление динамическими подписками webhook",
    )
    webhook_subparsers = webhook_parser.add_subparsers(dest="webhook_action")

    wh_sub = webhook_subparsers.add_parser(
        "subscribe", aliases=["add"], help="Создать подписку webhook"
    )
    wh_sub.add_argument("name", help="Название маршрута (используется в URL: /webhooks/<name>)")
    wh_sub.add_argument(
        "--prompt", default="", help="Шаблон промпта с ссылками на payload {dot.notation}"
    )
    wh_sub.add_argument(
        "--events", default="", help="Разделённые запятыми типы событий для приёма"
    )
    wh_sub.add_argument("--description", default="", help="Что делает эта подписка")
    wh_sub.add_argument(
        "--skills", default="", help="Разделённые запятыми названия скиллов для загрузки"
    )
    wh_sub.add_argument(
        "--deliver",
        default="log",
        help="Цель доставки: log, telegram, discord, slack и т.д.",
    )
    wh_sub.add_argument(
        "--deliver-chat-id",
        default="",
        help="Целевой chat ID для кросс-платформенной доставки",
    )
    wh_sub.add_argument(
        "--secret", default="", help="HMAC-секрет (автогенерация, если опущен)"
    )
    wh_sub.add_argument(
        "--deliver-only",
        action="store_true",
        help="Пропустить агента — доставить сформированный промпт напрямую как "
        "message. Zero LLM cost. Requires --deliver to be a real target "
        "(not 'log').",
    )

    webhook_subparsers.add_parser(
        "list", aliases=["ls"], help="Список всех динамических подписок"
    )

    wh_rm = webhook_subparsers.add_parser(
        "remove", aliases=["rm"], help="Удалить подписку"
    )
    wh_rm.add_argument("name", help="Название подписки для удаления")

    wh_test = webhook_subparsers.add_parser(
        "test", help="Отправить тестовый POST на маршрут webhook"
    )
    wh_test.add_argument("name", help="Название подписки для тестирования")
    wh_test.add_argument(
        "--payload", default="", help="JSON-payload для отправки (по умолчанию: тестовый)"
    )

    webhook_parser.set_defaults(func=cmd_webhook)
