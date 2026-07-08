"""``ruslan login`` subcommand parser.

Extracted verbatim from ``ruslan_cli/main.py:main()`` (god-file Phase 2).
Handler injected to avoid importing ``main``.
"""

from __future__ import annotations

from typing import Callable


def build_login_parser(subparsers, *, cmd_login: Callable) -> None:
    """Attach the deprecated ``login`` subcommand to ``subparsers``.

    ``ruslan login`` was removed in favor of ``ruslan auth`` / ``ruslan model``
    (the runtime handler in ``ruslan_cli/auth.py::login_command`` just prints a
    deprecation message and exits).  The subparser is kept registered so that
    old scripts/aliases invoking ``ruslan login [--flags]`` still receive the
    actionable deprecation message rather than an argparse ``invalid choice:
    'login'`` error — but:

    - The subparser is registered WITHOUT a ``help=`` kwarg so the row is
      omitted from ``ruslan --help`` (argparse only lists subcommands that
      have a help string).  This hides a command that no longer works (#24756)
      without the ``help=argparse.SUPPRESS`` ``==SUPPRESS==`` leak that
      argparse emits for a top-level subparser on Python 3.12+.
    - ``--provider`` accepts ANY value (no ``choices=``) so that, e.g.,
      ``ruslan login --provider anthropic`` reaches the deprecation handler and
      gets pointed at ``ruslan model`` instead of crashing in argparse with
      ``invalid choice: 'anthropic'`` before the handler can run.
    """
    login_parser = subparsers.add_parser(
        "login",
        description=(
            "Deprecated. Use `ruslan auth` to manage credentials, "
            "`ruslan model` to select a provider, or `ruslan setup` for full setup."
        ),
    )
    # No ``choices=`` on purpose — the handler is a deprecation notice that
    # ignores the value, and a restrictive list would reject providers the user
    # legitimately wants (e.g. ``anthropic``) with an argparse error before the
    # friendly redirect message is ever printed.
    login_parser.add_argument(
        "--provider",
        default=None,
        help="(deprecated) Действие name; ignored — see `ruslan model`",
    )
    login_parser.add_argument(
        "--portal-url", help="URL портала (по умолчанию: продакшн)"
    )
    login_parser.add_argument(
        "--inference-url",
        help="URL inference API (по умолчанию: продакшн)",
    )
    login_parser.add_argument(
        "--client-id", default=None, help="OAuth client id to use (default: ruslan-cli)"
    )
    login_parser.add_argument("--scope", default=None, help="OAuth scope для запроса")
    login_parser.add_argument(
        "--no-browser",
        action="store_true",
        help="Не открывать браузер автоматически",
    )
    login_parser.add_argument(
        "--timeout",
        type=float,
        default=15.0,
        help="Таймаут HTTP-запроса в секундах (по умолчанию: 15)",
    )
    login_parser.add_argument(
        "--ca-bundle", help="Путь к CA bundle PEM для TLS-проверки"
    )
    login_parser.add_argument(
        "--insecure",
        action="store_true",
        help="Отключить проверку TLS (только для тестов)",
    )
    login_parser.set_defaults(func=cmd_login)
