# Фаза 2: Исполнение — Готово ✅

## Что сделано

### Шаг 2.1: Создан `ruslan_cli/locales.py` (новый, 28 KB)
- 158 ключей, EN↔RU паритет 100%
- Категории: `cli.banner.*`, `cli.welcome.*`, `cli.help.*`, `cli.cmd.*.description`,
  `cli.tools.*`, `cli.setup.*`, `cli.error.*`, `common.*`
- API: `t(key, locale, **kwargs)`, `get_locale(config, env)`
- Дефолт: **ru** (DEFAULT_LOCALE = "ru")
- Поддержка `LANG=ru_RU.UTF-8` env
- Безопасный fallback: неизвестный ключ → сам ключ, неизвестная локаль → ru

### Шаг 2.1a: `ruslan_cli/banner_i18n.py` → deprecated обёртка
- Сохранена полная обратная совместимость со старым `banner_i18n.t` API
- BANNER_STRINGS, SUPPORTED_LOCALES, get_locale — все re-exported

### Шаг 2.2: Баннер + приветствие
- `cli.py:12160-12175` — приветствие берётся из `t("cli.welcome.text", locale)`
- `banner.py:622` — fallback `locale = "en"` → `locale = "ru"`
- `build_welcome_banner()` уже использовал `_banner_t` — продолжает работать через обновлённый `banner_i18n`
- ✅ Smoke-тест: баннер показывает "Доступные инструменты", "Доступные навыки", "(и ещё 9 наборов...)", "0 tools · 71 skills · команды: /help"

### Шаг 2.3: /help — категории + описания команд
- `cli.py:5967-6040` — `show_help()` использует `t()`:
  - Заголовок: `cli.help.title` → "(^_^)? Доступные команды"
  - Категории: `cli.help.category.<Name>` → "Настройка", "Память", "Навыки", "Сессия", "Модель"...
  - Описания: `cli.cmd.<name>.description` → 20+ команд переведены
  - Skill/Bundle/Quick заголовки: `cli.help.skill_commands` и т.д.
  - Подсказки: `cli.help.tip_chat`, `cli.help.tip_multiline`, `cli.help.tip_draft`, `cli.help.tip_paste_image`, `cli.help.tip_attach_image`

### Шаг 2.4: /tools + /toolsets
- `cli.py:6040-6115` — `show_tools()` и `show_toolsets()` используют `t()`:
  - `cli.tools.title`, `cli.tools.no_tools`, `cli.tools.total`
  - `cli.toolsets.title`

### Шаг 2.5: Setup-визард
- `ruslan_cli/setup.py` — добавлен import `from ruslan_cli.locales import t as _t, get_locale as _get_locale`
- Helper `_t()` доступен во всём файле
- **Точечно** локализованы 2 строки (Press Ctrl+C, Reconfigure header)
- ⚠ Полная локализация setup.py (3383 строк) — **отдельная задача** для Фазы 4.
  Прямой перевод всех prompt-строк слишком рискованный (можно сломать интерактивный ввод).

### Шаг 2.6: Дефолтная локаль = ru
- `locales.DEFAULT_LOCALE = "ru"`
- `banner.py:622` — fallback `en` → `ru`
- `banner_i18n.t()` дефолт — `en` → `ru` (обратная совместимость: `t(key, "en")` всё ещё работает)

### Шаг 2.7: Smoke-тесты
- `ruslan_cli/tests/test_locales.py` — 16 тестов, **16 passed, 0 failed**:
  - Паритет ключей EN↔RU
  - Паритет плейсхолдеров
  - Default locale = ru
  - get_locale приоритеты
  - t() с базовыми ключами + плейсхолдерами
  - Short-key compat (для banner_i18n обратной совместимости)
  - Fallback на неизвестный ключ / локаль
  - Все категории /help переведены
  - Все описания команд переведены
  - Защита от регрессий: кириллица в EN, ASCII в RU

## Изменённые файлы

| Файл | Изменения |
|------|-----------|
| `ruslan_cli/locales.py` | **новый**, 28 KB, 158 ключей EN+RU |
| `ruslan_cli/banner_i18n.py` | deprecated обёртка → новый API |
| `ruslan_cli/banner.py` | 1 строка: fallback `en` → `ru` |
| `cli.py` | 3 блока: приветствие, show_help, show_tools/show_toolsets |
| `ruslan_cli/setup.py` | +import _t helper, 2 точечные локализации |
| `ruslan_cli/tests/test_locales.py` | **новый**, 16 тестов |

## Что НЕ переведено (осознанно)

- **Slash-команды** (`/help`, `/model`, `/new`, `/compress`...) — идентификаторы, EN
- **Имена тулзов** (`terminal`, `read_file`) — EN
- **Имена тулсетов** (`web`, `file`, `terminal`) — EN
- **CLI-команды** (`ruslan`, `ruslan-cli`) — EN
- **ID/имена env-переменных** (`OPENROUTER_API_KEY`) — EN
- **Имена моделей** (`claude-opus-4.6`) — EN
- **setup.py** (главный объём визарда, 3383 строк) — **отдельная задача** для Фазы 4
- **Skin-файлы** (если есть) — отдельная задача
- **README.md и прочая документация** — отдельная задача
- **Сообщения об ошибках из logger.error** — оставлены EN (это логи, не UI)

## Smoke-тест: ручная проверка

```bash
cd ~/Desktop/ruslan-agent-main
python3 -c "from rich.console import Console; import os; from ruslan_cli.banner import build_welcome_banner; Console().print(build_welcome_banner(Console(), 'minimax-m3', os.getcwd(), locale='ru'))"
# Должно показать баннер с "Доступные инструменты" и т.д.
```

## Следующий шаг

Фаза 3: проверка GLM-5.2.
