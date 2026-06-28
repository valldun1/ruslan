"""Локализация баннера Ruslan Agent CLI.

Минимальная i18n для ASCII-баннера приветствия. Содержит 12 строк
на двух языках (en, ru). Fallback — на en.

Полная локализация через locales/*.yaml была бы правильнее, но требует
16 файлов и общего i18n API. Здесь — компактный точечный фикс.

Использование:
    from ruslan_cli.banner_i18n import t
    text = t("cli.banner.available_tools", locale="ru")
    text = t("cli.banner.update_run_cmd", locale="ru", cmd="ruslan update")
"""

from __future__ import annotations

from typing import Any

# Доступные локали баннера. Если в конфиге указана локаль, которой нет
# в этом словаре — fallback на en.
SUPPORTED_LOCALES = ("en", "ru")

BANNER_STRINGS: dict[str, dict[str, str]] = {
    "en": {
        "available_tools": "Available Tools",
        "available_skills": "Available Skills",
        "mcp_servers": "MCP Servers",
        "more_toolsets": "(and {n} more toolsets...)",
        "no_skills": "No skills installed",
        "skills_disabled": "Skills toolset disabled",
        "summary_help": "/help for commands",
        "commits_behind_one": "\u26a0 1 commit behind",
        "commits_behind_many": "\u26a0 {n} commits behind",
        "update_available": "\u26a0 update available",
        "update_run_cmd": " \u2014 run {cmd} to update",
        "commit": "commit",
        "commits": "commits",
    },
    "ru": {
        "available_tools": "Доступные инструменты",
        "available_skills": "Доступные навыки",
        "mcp_servers": "MCP-серверы",
        "more_toolsets": "(и ещё {n} наборов...)",
        "no_skills": "Навыки не установлены",
        "skills_disabled": "Набор навыков отключён",
        "summary_help": "команды: /help",
        "commits_behind_one": "\u26a0 отстаёт на 1 коммит",
        "commits_behind_many": "\u26a0 отстаёт на {n} коммитов",
        "update_available": "\u26a0 доступно обновление",
        "update_run_cmd": " \u2014 выполните {cmd} для обновления",
        "commit": "коммит",
        "commits": "коммитов",
    },
}


def t(key: str, locale: str = "en", **kwargs: Any) -> str:
    """Получить локализованную строку баннера.

    Args:
        key: ключ в формате "cli.banner.<name>" или просто "<name>".
             Префикс "cli.banner." опциональный — отбрасывается автоматически.
        locale: "en" или "ru". Неизвестная локаль → fallback на "en".
        **kwargs: именованные плейсхолдеры для подстановки (например, n=5, cmd="...").

    Returns:
        Локализованная строка с подставленными плейсхолдерами.
        Если ключ не найден ни в одной локали — возвращает сам ключ
        (для безопасности, чтобы баннер не сломался).
    """
    # Нормализация: отбрасываем префикс "cli.banner." если есть
    if key.startswith("cli.banner."):
        short_key = key[len("cli.banner."):]
    else:
        short_key = key

    # Fallback на en для неизвестной локали
    if locale not in BANNER_STRINGS:
        locale = "en"

    table = BANNER_STRINGS[locale]
    template = table.get(short_key)
    if template is None:
        # Ключ не найден в запрошенной локали → en
        template = BANNER_STRINGS["en"].get(short_key, key)

    # Подставляем плейсхолдеры. Если kwargs нет — возвращаем как есть.
    try:
        return template.format(**kwargs)
    except (KeyError, IndexError):
        return template


def get_locale(config: dict | None = None) -> str:
    """Извлечь локаль из конфига Ruslan.

    Args:
        config: распарсенный config.yaml (dict). Если None — возвращает "en".

    Returns:
        "en" или "ru". Любая другая локаль или отсутствие → "en".
    """
    if not config:
        return "en"
    locale = str(config.get("locale", "en")).strip().lower()
    if locale in SUPPORTED_LOCALES:
        return locale
    return "en"
