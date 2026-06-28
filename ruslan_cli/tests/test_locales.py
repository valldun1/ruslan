"""Тесты локализации Ruslan Agent: EN↔RU паритет ключей, плейсхолдеров, smoke-вызовы.

Запуск: pytest ruslan_cli/tests/test_locales.py -v
Или:    python3 -m ruslan_cli.tests.test_locales
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# Путь к ruslan_cli (для запуска не из pytest)
_RUSLAN_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_RUSLAN_ROOT) not in sys.path:
    sys.path.insert(0, str(_RUSLAN_ROOT))

from ruslan_cli.locales import t, get_locale, STRINGS, SUPPORTED_LOCALES, DEFAULT_LOCALE


# ============================================================================
# Паритет ключей EN↔RU
# ============================================================================

def test_key_parity():
    """EN и RU должны иметь одинаковый набор ключей."""
    en_keys = set(STRINGS["en"].keys())
    ru_keys = set(STRINGS["ru"].keys())

    missing_in_ru = en_keys - ru_keys
    missing_in_en = ru_keys - en_keys

    assert not missing_in_ru, f"Отсутствуют в RU ({len(missing_in_ru)}):\n  " + "\n  ".join(sorted(missing_in_ru))
    assert not missing_in_en, f"Отсутствуют в EN ({len(missing_in_en)}):\n  " + "\n  ".join(sorted(missing_in_en))


def test_placeholder_parity():
    """Плейсхолдеры в EN и RU должны совпадать для каждого ключа."""
    problems = []
    for key in sorted(STRINGS["en"].keys() & STRINGS["ru"].keys()):
        en_val = STRINGS["en"][key]
        ru_val = STRINGS["ru"][key]
        en_ph = sorted(re.findall(r"\{(\w+)\}", en_val))
        ru_ph = sorted(re.findall(r"\{(\w+)\}", ru_val))
        if en_ph != ru_ph:
            problems.append((key, en_ph, ru_ph))

    assert not problems, (
        f"Расхождение плейсхолдеров ({len(problems)}):\n"
        + "\n".join(f"  {k}: EN={e}, RU={r}" for k, e, r in problems)
    )


# ============================================================================
# Default locale
# ============================================================================

def test_default_locale_is_ru():
    """Дефолтная локаль = ru."""
    assert DEFAULT_LOCALE == "ru"


def test_supported_locales():
    """Поддерживаемые локали: ru, en."""
    assert "ru" in SUPPORTED_LOCALES
    assert "en" in SUPPORTED_LOCALES


def test_get_locale_priority():
    """get_locale: config > env > default."""
    # Из config
    assert get_locale({"locale": "ru"}, {}) == "ru"
    assert get_locale({"locale": "en"}, {}) == "en"
    assert get_locale({"language": "ru"}, {}) == "ru"

    # Из LANG
    assert get_locale(None, {"LANG": "ru_RU.UTF-8"}) == "ru"
    assert get_locale(None, {"LC_ALL": "en_US.UTF-8"}) == "en"

    # Default = ru
    assert get_locale(None, {}) == "ru"
    assert get_locale({}, {}) == "ru"

    # Неизвестная локаль → default
    assert get_locale({"locale": "fr"}, {}) == "ru"


# ============================================================================
# Smoke tests: t() с реальными ключами
# ============================================================================

def test_t_basic_keys():
    """Базовые ключи переводятся правильно."""
    # Баннер
    assert t("cli.banner.available_tools", locale="ru") == "Доступные инструменты"
    assert t("cli.banner.available_tools", locale="en") == "Available Tools"

    # Приветствие
    assert t("cli.welcome.text", locale="ru").startswith("Добро пожаловать")
    assert t("cli.welcome.text", locale="en").startswith("Welcome")

    # Help
    assert t("cli.help.title", locale="ru") == "Доступные команды"
    assert "Available" in t("cli.help.title", locale="en")

    # Команды
    assert t("cli.cmd.help.description", locale="ru") == "Показать эту справку"
    assert t("cli.cmd.help.description", locale="en") == "Show this help message"


def test_t_with_placeholders():
    """Плейсхолдеры подставляются."""
    # n
    assert t("cli.banner.more_toolsets", locale="ru", n=9) == "(и ещё 9 наборов...)"
    assert t("cli.banner.more_toolsets", locale="en", n=5) == "(and 5 more toolsets...)"

    # cmd
    cmd_msg = t("cli.banner.update_run_cmd", locale="ru", cmd="ruslan update")
    assert "ruslan update" in cmd_msg
    assert "выполните" in cmd_msg

    # provider
    api_msg = t("cli.setup.ask_api_key", locale="ru", provider="OpenAI")
    assert api_msg == "Введите API-ключ для OpenAI:"

    # error
    err = t("cli.error.network", locale="ru", error="timeout")
    assert "timeout" in err
    assert "Ошибка сети" in err


def test_t_short_key_compat():
    """Короткие ключи (без префикса) работают для обратной совместимости с banner_i18n."""
    # Как старый banner_i18n API
    result = t("available_tools", locale="ru")
    assert result == "Доступные инструменты"

    result = t("update_run_cmd", locale="ru", cmd="test")
    assert "test" in result


def test_t_unknown_key_fallback():
    """Неизвестный ключ возвращает сам ключ (безопасный fallback)."""
    assert t("cli.unknown.key", locale="ru") == "cli.unknown.key"
    assert t("totally.random.key") == "totally.random.key"


def test_t_unknown_locale_fallback():
    """Неизвестная локаль → default (ru)."""
    assert t("cli.banner.available_tools", locale="fr") == "Доступные инструменты"
    assert t("cli.banner.available_tools", locale=None) == "Доступные инструменты"


def test_t_no_placeholder_but_kwargs():
    """Если kwargs переданы, но в строке нет плейсхолдеров — kwargs игнорируются, без падения."""
    # Не должно упасть
    result = t("cli.welcome.text", locale="ru", extra="ignored")
    assert result == "Добро пожаловать в Руслан! Введите сообщение или /help для списка команд."


# ============================================================================
# Категории и команды
# ============================================================================

def test_all_command_descriptions_have_translation():
    """Все описания команд (primary, не алиасы) из COMMANDS_BY_CATEGORY имеют RU-перевод."""
    try:
        from ruslan_cli.commands import COMMANDS_BY_CATEGORY
    except ImportError:
        # Если не можем импортировать — fallback на старый hardcoded список
        common_cmds = ["help", "model", "new", "compress", "title", "history",
                       "resume", "tools", "skills", "exit", "setup", "update",
                       "memory", "gateway", "paste", "clear", "status", "config",
                       "version", "doctor"]
    else:
        # Соберём ВСЕ primary имена команд (пропуская алиасы)
        common_cmds = set()
        for category, cmds in COMMANDS_BY_CATEGORY.items():
            for cmd_full, desc in cmds.items():
                if "(alias for" in desc:
                    continue  # алиасы не нужны отдельно
                common_cmds.add(cmd_full.lstrip('/'))
        common_cmds = sorted(common_cmds)

    missing = []
    for cmd in common_cmds:
        key = f"cli.cmd.{cmd}.description"
        val = t(key, locale="ru")
        if not val or val == key:
            missing.append(f"{key} (для команды /{cmd})")

    assert not missing, (
        f"Нет переводов для {len(missing)} команд:\n  "
        + "\n  ".join(missing[:20])
        + (f"\n  ... и ещё {len(missing)-20}" if len(missing) > 20 else "")
    )


def test_all_help_categories_have_translation():
    """Все категории /help из COMMANDS_BY_CATEGORY имеют RU-перевод."""
    try:
        from ruslan_cli.commands import COMMANDS_BY_CATEGORY
        required_categories = sorted(COMMANDS_BY_CATEGORY.keys())
    except ImportError:
        required_categories = [
            "Setup", "Memory", "Skills", "Session", "Model",
            "Tools", "Misc", "Plugins", "Profiles", "Gateway", "Dangerous",
        ]

    missing = []
    for cat in required_categories:
        key = f"cli.help.category.{cat}"
        val = t(key, locale="ru")
        if not val or val == key:
            missing.append(key)

    assert not missing, f"Нет переводов категорий: {missing}"


def test_locale_ru_phrase_count():
    """Должно быть минимум 200 RU-строк (sanity check после расширения)."""
    assert len(STRINGS["ru"]) >= 200, f"Только {len(STRINGS['ru'])} RU-строк — слишком мало"


def test_no_cyrillic_in_en():
    """В EN-словаре не должно быть кириллицы (защита от копипаста).

    Исключение: двуязычные строки для выбора языка (intentionally bilingual).
    """
    # Явно разрешённые двуязычные EN-строки (содержат кириллицу намеренно)
    BILINGUAL_WHITELIST = {
        "cli.setup.choose_language",  # "Choose language / Выберите язык:"
    }
    for key, val in STRINGS["en"].items():
        if key in BILINGUAL_WHITELIST:
            continue
        has_cyrillic = any(0x0400 <= ord(c) <= 0x04FF for c in val)
        assert not has_cyrillic, f"EN-строка {key} содержит кириллицу: {val!r}"


def test_no_latin_in_ru_for_descriptions():
    """В RU-описаниях команд не должно быть чистого ASCII-мусора (защита от непереведённого)."""
    # Это soft-проверка: некоторые RU-строки могут содержать ASCII (команды, имена), но
    # основная часть должна быть кириллицей.
    suspicious = []
    for key, val in STRINGS["ru"].items():
        if key.startswith("cli.cmd.") and key.endswith(".description"):
            # Описания команд: должны содержать хотя бы немного кириллицы
            cyrillic_count = sum(1 for c in val if 0x0400 <= ord(c) <= 0x04FF)
            if cyrillic_count < 3:
                suspicious.append(f"{key}: {val!r}")
    assert not suspicious, (
        "Подозрительно мало кириллицы в RU-описаниях:\n  "
        + "\n  ".join(suspicious)
    )


# ============================================================================
# Runner
# ============================================================================

if __name__ == "__main__":
    # Простой runner для запуска без pytest
    import traceback
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    passed = 0
    failed = 0
    for test in tests:
        try:
            test()
            print(f"  ✅ {test.__name__}")
            passed += 1
        except Exception as e:
            print(f"  ❌ {test.__name__}: {e}")
            failed += 1
    print(f"\n{passed} passed, {failed} failed (всего {len(tests)})")
    sys.exit(0 if failed == 0 else 1)
