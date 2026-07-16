"""Локализация баннера Ruslan Agent CLI.

Обёртка над agent/i18n для обратной совместимости.
Дефолтная локаль изменена с "en" на "ru".
"""

from __future__ import annotations

from agent.i18n import t as _agent_t, get_language

# Словарь для обратной совместимости (старый код мог импортировать напрямую)
BANNER_STRINGS: dict[str, dict[str, str]] = {}


def t(key: str, locale: str | None = "ru", **kwargs) -> str:
    """Получить локализованную строку баннера.

    Параметр locale — для обратной совместимости с banner_i18n API.
    В agent.i18n используется lang, но мы принимаем locale и передаём как lang.

    Args:
        key: Dotted key в каталоге (напр. "cli.banner.available_tools")
        locale: Язык (по умолч. "ru" вместо "en")
        **kwargs: Параметры форматирования

    Returns:
        Локализованная строка или fallback на англ./ключ
    """
    return _agent_t(key, lang=locale, **kwargs)


def get_locale(config=None) -> str:
    """Определить текущую локаль (обратная совместимость с banner_i18n API).

    Args:
        config: Не используется, для обратной совместимости

    Returns:
        Код языка (по умолч. "ru")
    """
    lang = get_language()
    if lang == "en":
        return "ru"  # Для Ruslan дефолт — русский
    return lang
