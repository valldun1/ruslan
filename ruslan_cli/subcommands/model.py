"""``ruslan model`` subcommand parser.

Extracted verbatim from ``ruslan_cli/main.py:main()`` (god-file Phase 2).
Handler injected to avoid importing ``main``.
"""

from __future__ import annotations

from typing import Callable


def build_model_parser(subparsers, *, cmd_model: Callable) -> None:
    """Attach the ``model`` subcommand to ``subparsers``."""
    # =========================================================================
    # model command
    # =========================================================================
    model_parser = subparsers.add_parser(
        "model",
        help="Select default model and provider",
        description="Выбрать модель и провайдера по умолчанию",
    )
    model_parser.add_argument(
        "--refresh",
        action="store_true",
        help="Wipe the model picker disk cache and re-fetch every provider's live /v1/models list.",
    )
    model_parser.add_argument(
        "--portal-url",
        help="Базовый URL портала для входа Nous (по умолчанию: production portal)",
    )
    model_parser.add_argument(
        "--inference-url",
        help="Базовый URL API инференции для входа Nous (по умолчанию: production inference API)",
    )
    model_parser.add_argument(
        "--client-id",
        default=None,
        help="OAuth client id to use for Nous login (default: ruslan-cli)",
    )
    model_parser.add_argument(
        "--scope", default=None, help="OAuth scope для запроса for Nous login"
    )
    model_parser.add_argument(
        "--no-browser",
        action="store_true",
        help="Не открывать браузер автоматически during Nous login",
    )
    model_parser.add_argument(
        "--manual-paste",
        action="store_true",
        help=(
            "For loopback OAuth providers (xai-oauth, ...): skip the local "
            "callback listener and paste the failed callback URL from your "
            "browser instead. Use on browser-only remotes (Cloud Shell, "
            "Codespaces, EC2 Instance Connect, ...). See #26923."
        ),
    )
    model_parser.add_argument(
        "--timeout",
        type=float,
        default=15.0,
        help="Таймаут HTTP-запроса в секундах для входа Nous (по умолчанию: 15)",
    )
    model_parser.add_argument(
        "--ca-bundle", help="Путь к CA bundle PEM-файлу для проверки TLS Nous"
    )
    model_parser.add_argument(
        "--insecure",
        action="store_true",
        help="Отключить проверку TLS для входа Nous (только для тестирования)",
    )
    model_parser.set_defaults(func=cmd_model)
