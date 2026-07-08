"""``ruslan gateway`` and ``ruslan proxy`` subcommand parsers.

Extracted verbatim from ``ruslan_cli/main.py:main()`` (god-file Phase 2).
Both parsers are built together because they shared one inline block (the
``gateway`` section also defined ``proxy``). Handlers injected to avoid
importing ``main``.
"""

from __future__ import annotations

import argparse
from typing import Callable

from ruslan_cli.subcommands._shared import add_accept_hooks_flag


def _add_compat_platform_flag(parser: argparse.ArgumentParser) -> None:
    """Accept stale `gateway <verb> --platform X` docs without advertising it.

    Gateway service lifecycle commands operate on the gateway process, not a
    single messaging adapter.  Photon briefly printed a per-platform start
    command during setup; keep that command parseable so users following the
    old hint don't get blocked by argparse before the gateway can start.
    """
    parser.add_argument(
        "--platform",
        dest="platform",
        help=argparse.SUPPRESS,
    )


def build_gateway_parser(
    subparsers, *, cmd_gateway: Callable, cmd_proxy: Callable, cmd_gateway_enroll: Callable
) -> None:
    """Attach the ``gateway`` and ``proxy`` subcommands to ``subparsers``."""
    # =========================================================================
    # gateway command
    # =========================================================================
    gateway_parser = subparsers.add_parser(
        "gateway",
        help="Messaging gateway management",
        description="Manage the messaging gateway (Telegram, Discord, WhatsApp, Weixin, and more)",
    )
    gateway_subparsers = gateway_parser.add_subparsers(dest="gateway_command")

    # gateway run (default)
    gateway_run = gateway_subparsers.add_parser(
        "run", help="Запустить шлюз в переднем плане (рекомендуется для WSL, Docker, Termux)"
    )
    gateway_run.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Увеличить детализацию логов stderr (-v=INFO, -vv=DEBUG)",
    )
    gateway_run.add_argument(
        "-q", "--quiet", action="store_true", help="Подавить все логи stderr"
    )
    gateway_run.add_argument(
        "--replace",
        action="store_true",
        help="Заменить любой существующий экземпляр шлюза (полезно для systemd)",
    )
    gateway_run.add_argument(
        "--force",
        action="store_true",
        help=(
            "Start a foreground gateway even when a systemd/launchd/s6 service "
            "already supervises this profile. Without --force, the command "
            "refuses because a second dispatcher escapes the service and can "
            "corrupt shared gateway state."
        ),
    )
    gateway_run.add_argument(
        "--no-supervise",
        action="store_true",
        help=(
            "Inside the s6-overlay Docker image, normally `gateway run` is "
            "automatically redirected to the supervised s6 service (so the "
            "gateway gets auto-restart on crash, plus a supervised dashboard "
            "if RUSLAN_DASHBOARD is set). Pass --no-supervise to opt out and "
            "get the historical pre-s6 foreground behavior: the gateway is "
            "the container's main process and the container exits with the "
            "gateway's exit code. No effect outside an s6 container."
        ),
    )
    add_accept_hooks_flag(gateway_run)
    add_accept_hooks_flag(gateway_parser)

    # gateway start
    gateway_start = gateway_subparsers.add_parser(
        "start", help="Запустить установленную фоновую службу systemd/launchd"
    )
    gateway_start.add_argument(
        "--system",
        action="store_true",
        help="Целить системную Linux-службу шлюза",
    )
    gateway_start.add_argument(
        "--all",
        action="store_true",
        help="Убить ВСЕ устаревшие процессы шлюза во всех профилях перед запуском",
    )
    _add_compat_platform_flag(gateway_start)

    # gateway stop
    gateway_stop = gateway_subparsers.add_parser("stop", help="Остановить службу шлюза")
    gateway_stop.add_argument(
        "--system",
        action="store_true",
        help="Целить системную Linux-службу шлюза",
    )
    gateway_stop.add_argument(
        "--all",
        action="store_true",
        help="Остановить ВСЕ процессы шлюза во всех профилях",
    )

    # gateway restart
    gateway_restart = gateway_subparsers.add_parser(
        "restart", help="Перезапустить службу шлюза"
    )
    gateway_restart.add_argument(
        "--system",
        action="store_true",
        help="Целить системную Linux-службу шлюза",
    )
    gateway_restart.add_argument(
        "--all",
        action="store_true",
        help="Убить ВСЕ процессы шлюза во всех профилях перед перезапуском",
    )
    _add_compat_platform_flag(gateway_restart)

    # gateway status
    gateway_status = gateway_subparsers.add_parser("status", help="Show gateway status")
    gateway_status.add_argument("--deep", action="store_true", help="Показать статус шлюза")
    gateway_status.add_argument(
        "-l",
        "--full",
        action="store_true",
        help="Show full, untruncated service/log output where supported",
    )
    gateway_status.add_argument(
        "--system",
        action="store_true",
        help="Целить системную Linux-службу шлюза",
    )
    _add_compat_platform_flag(gateway_status)

    # gateway install
    gateway_install = gateway_subparsers.add_parser(
        "install", help="Установить шлюз как фоновую службу systemd/launchd"
    )
    gateway_install.add_argument("--force", action="store_true", help="Принудительная переустановка")
    gateway_install.add_argument(
        "--system",
        action="store_true",
        help="Установить как системную Linux-службу (запуск при загрузке)",
    )
    gateway_install.add_argument(
        "--run-as-user",
        dest="run_as_user",
        help="Учетная запись пользователя, от имени которой должна работать системная Linux-служба",
    )
    gateway_install.add_argument(
        "--start-now",
        dest="start_now",
        action="store_true",
        default=None,
        help=argparse.SUPPRESS,
    )
    gateway_install.add_argument(
        "--no-start-now",
        dest="start_now",
        action="store_false",
        help=argparse.SUPPRESS,
    )
    gateway_install.add_argument(
        "--start-on-login",
        dest="start_on_login",
        action="store_true",
        default=None,
        help=argparse.SUPPRESS,
    )
    gateway_install.add_argument(
        "--no-start-on-login",
        dest="start_on_login",
        action="store_false",
        help=argparse.SUPPRESS,
    )
    gateway_install.add_argument(
        "--elevated-handoff",
        dest="elevated_handoff",
        action="store_true",
        help=argparse.SUPPRESS,
    )

    # gateway uninstall
    gateway_uninstall = gateway_subparsers.add_parser(
        "uninstall", help="Деинсталлировать службу шлюза"
    )
    gateway_uninstall.add_argument(
        "--system",
        action="store_true",
        help="Целить системную Linux-службу шлюза",
    )

    # gateway list
    gateway_subparsers.add_parser("list", help="Список всех профилей and their gateway status")

    # gateway setup
    gateway_subparsers.add_parser("setup", help="Настроить платформы сообщений")

    # gateway migrate-legacy
    gateway_migrate_legacy = gateway_subparsers.add_parser(
        "migrate-legacy",
        help="Remove legacy ruslan.service units from pre-rename installs",
        description=(
            "Stop, disable, and remove legacy Ruslan gateway unit files "
            "(e.g. ruslan.service) left over from older installs. Profile "
            "units (ruslan-gateway-<profile>.service) and unrelated "
            "third-party services are never touched."
        ),
    )
    gateway_migrate_legacy.add_argument(
        "--dry-run",
        dest="dry_run",
        action="store_true",
        help="Показать, что будет удалено, без изменений",
    )
    gateway_migrate_legacy.add_argument(
        "-y",
        "--yes",
        dest="yes",
        action="store_true",
        help="Пропустить подтверждение",
    )

    # gateway enroll — enroll a self-hosted gateway with a relay connector
    # (connector⇄gateway auth). Redeems a single-use enrollment token for the
    # per-gateway secret + per-tenant delivery key and writes them to .env.
    # See docs/relay-connector-contract.md (and the connector repo's
    # docs/connector-gateway-auth-design.md). EXPERIMENTAL.
    gateway_enroll = gateway_subparsers.add_parser(
        "enroll",
        help="Enroll this gateway with a relay connector (writes relay auth creds to .env)",
        description=(
            "Redeem a single-use enrollment token with a relay connector. "
            "Authenticates as your Nous Portal account (the connector derives the "
            "authoritative tenant from it), mints this gateway's per-gateway secret "
            "and per-tenant delivery key, and writes GATEWAY_RELAY_ID / "
            "GATEWAY_RELAY_SECRET / GATEWAY_RELAY_DELIVERY_KEY into ~/.ruslan/.env. "
            "Requires being logged in (ruslan setup). Not available in managed installs."
        ),
    )
    gateway_enroll.add_argument(
        "--token",
        default=None,
        help=(
            "The single-use enrollment token from the connector (delivered with "
            "your gateway config). Also settable via GATEWAY_RELAY_ENROLL_TOKEN."
        ),
    )
    gateway_enroll.add_argument(
        "--connector-url",
        dest="connector_url",
        default=None,
        help=(
            "The connector base/relay URL, e.g. wss://connector.example.com/relay "
            "or https://connector.example.com. Also settable via GATEWAY_RELAY_URL "
            "/ gateway.relay_url in config.yaml."
        ),
    )
    gateway_enroll.add_argument(
        "--gateway-id",
        dest="gateway_id",
        default=None,
        help=(
            "A stable id for this gateway instance (kill-switch granularity). "
            "Defaults to gw-<hostname>."
        ),
    )
    gateway_enroll.set_defaults(func=cmd_gateway_enroll)

    # =========================================================================
    # proxy command — local OpenAI-compatible proxy that attaches the user's
    # OAuth-authenticated provider credentials to outbound requests. Lets
    # external apps (OpenViking, Karakeep, Open WebUI, ...) ride a logged-in
    # subscription without copy-pasting static API keys.
    # =========================================================================
    proxy_parser = subparsers.add_parser(
        "proxy",
        help="Local OpenAI-compatible proxy to OAuth providers",
        description=(
            "Run a local HTTP server that forwards OpenAI-compatible requests "
            "to an OAuth-authenticated provider (e.g. Nous Portal). External "
            "apps can point at the proxy with any bearer token; the proxy "
            "attaches your real credentials."
        ),
    )
    proxy_subparsers = proxy_parser.add_subparsers(dest="proxy_command")

    proxy_start = proxy_subparsers.add_parser(
        "start", help="Run the proxy in the foreground"
    )
    proxy_start.add_argument(
        "--provider",
        default="nous",
        help="Upstream provider: nous or xai (default: nous). See `ruslan proxy providers`.",
    )
    proxy_start.add_argument(
        "--host",
        default=None,
        help="Bind address (default: 127.0.0.1). Use 0.0.0.0 to expose on LAN.",
    )
    proxy_start.add_argument(
        "--port",
        type=int,
        default=None,
        help="Bind port (default: 8645)",
    )

    proxy_subparsers.add_parser(
        "status", help="Show which proxy upstreams are ready"
    )
    proxy_subparsers.add_parser(
        "providers", help="List available proxy upstream providers"
    )
    proxy_parser.set_defaults(func=cmd_proxy)
    gateway_parser.set_defaults(func=cmd_gateway)
