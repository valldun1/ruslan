"""DEPRECATED: локализация баннера Ruslan Agent CLI.

⚠ Этот модуль сохранён для обратной совместимости.
Новая локализация — в `ruslan_cli.locales` (158 ключей, полное покрытие).

Использование (старый API, всё ещё работает):
    from ruslan_cli.banner_i18n import t
    text = t("cli.banner.available_tools", locale="ru")

Рекомендуемое использование (новый API):
    from ruslan_cli.locales import t
    text = t("cli.banner.available_tools", locale="ru")
    text = t("cli.setup.ask_api_key", locale="ru", provider="OpenAI")
"""

from __future__ import annotations

# Импортируем новый модуль как источник истины
from ruslan_cli.locales import t as _locales_t, SUPPORTED_LOCALES, STRINGS

# Обратная совместимость: BANNER_STRINGS теперь ссылается на общий словарь
# Только баннер-ключи (для старого кода, который мог импортировать напрямую)
BANNER_STRINGS: dict[str, dict[str, str]] = {
    locale: {
        k.replace("cli.banner.", ""): v
        for k, v in STRINGS[locale].items()
        if k.startswith("cli.banner.")
    }
    for locale in SUPPORTED_LOCALES
}


def t(key: str, locale: str = "ru", **kwargs) -> str:
    """Получить локализованную строку баннера (обратная совместимость).

    Дефолтная локаль изменена с "en" на "ru" для совпадения с новым API.
    Старый код, передававший locale="en" явно, продолжает работать.
    """
    return _locales_t(key, locale=locale, **kwargs)


# Re-export get_locale из нового модуля для обратной совместимости
from ruslan_cli.locales import get_locale  # noqa: E402, F401
