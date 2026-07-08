"""``ruslan plugins`` subcommand parser.

Extracted from ``ruslan_cli/main.py:main()`` (god-file Phase 2 follow-up).
Handler injected to avoid importing ``main``.
"""

from __future__ import annotations

from typing import Callable


def build_plugins_parser(subparsers, *, cmd_plugins: Callable) -> None:
    """Attach the ``plugins`` subcommand to ``subparsers``."""
    plugins_parser = subparsers.add_parser(
        "plugins",
        help="Управление плагинами — установка, обновление, удаление, список",
        description="Установка плагинов из Git-репозиториев, обновление, удаление или список.",
    )
    plugins_subparsers = plugins_parser.add_subparsers(dest="plugins_action")

    plugins_install = plugins_subparsers.add_parser(
        "install", help="Установить плагин из Git URL или owner/repo"
    )
    plugins_install.add_argument(
        "identifier",
        help="Git URL or owner/repo shorthand (e.g. anpicasso/ruslan-plugin-chrome-profiles)",
    )
    plugins_install.add_argument(
        "--force",
        "-f",
        action="store_true",
        help="Удалить существующий плагин и переустановить",
    )
    _install_enable_group = plugins_install.add_mutually_exclusive_group()
    _install_enable_group.add_argument(
        "--enable",
        action="store_true",
        help="Auto-enable the plugin after install (skip confirmation prompt)",
    )
    _install_enable_group.add_argument(
        "--no-enable",
        action="store_true",
        help="Install disabled (skip confirmation prompt); enable later with `ruslan plugins enable <name>`",
    )

    plugins_update = plugins_subparsers.add_parser(
        "update", help="Загрузить последние изменения для установленного плагина"
    )
    plugins_update.add_argument("name", help="Имя плагина для обновления")

    plugins_remove = plugins_subparsers.add_parser(
        "remove", aliases=["rm", "uninstall"], help="Удалить установленный плагин"
    )
    plugins_remove.add_argument("name", help="Имя директории плагина для удаления")

    plugins_list = plugins_subparsers.add_parser(
        "list", aliases=["ls"], help="Список установленных плагинов"
    )
    plugins_list.add_argument(
        "--enabled",
        action="store_true",
        help="Show only enabled plugins",
    )
    plugins_list.add_argument(
        "--user",
        action="store_true",
        help="Show only user-installed plugins (including git plugins)",
    )
    plugins_list.add_argument(
        "--no-bundled",
        action="store_true",
        help="Hide bundled plugins",
    )
    plugins_list.add_argument(
        "--plain",
        action="store_true",
        help="Print compact plain-text output instead of a Rich table",
    )
    plugins_list.add_argument(
        "--json",
        action="store_true",
        help="Print machine-readable JSON",
    )

    plugins_enable = plugins_subparsers.add_parser(
        "enable", help="Включить отключённый плагин"
    )
    plugins_enable.add_argument("name", help="Имя плагина для включения")

    plugins_disable = plugins_subparsers.add_parser(
        "disable", help="Отключить плагин без удаления"
    )
    plugins_disable.add_argument("name", help="Имя плагина для отключения")
    plugins_parser.set_defaults(func=cmd_plugins)
