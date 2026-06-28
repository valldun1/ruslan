# Фаза 0: Контекст — Русификация Ruslan Agent

## Проект
- **Путь:** `~/Desktop/ruslan-agent-main/`
- **Тип:** upstream-клон Ruslan Agent v0.17.0 (форк nousresearch/hermes-agent, брендинг → Ruslan)
- **Git:** upstream 024c0456, local 7afcdf71 (+4 commits ahead) — уже с локальными правками

## Что уже есть на русском
- `ruslan_cli/banner_i18n.py` — 13 строк RU/EN (заголовки баннера: "Доступные инструменты", "и ещё N наборов...", "команды: /help", "выполните {cmd} для обновления")
- Баннер **частично** показывается на русском — заголовки секций + обновления
- Приветствие в `cli.py:12164-12167` — "Welcome to Ruslan Agent! Type your message or /help for commands." (EN, через skin branding)
- `show_help()` (cli.py:5967) — все категории/описания EN, единственная RU-строка "Нет доступных инструментов" в show_tools

## Чего НЕТ на русском (объём работы)
- `show_help()` — категории "Setup", "Memory", "Skills", "Session", все описания команд
- `show_tools()` / `show_toolsets()` — заголовки, метки `[toolset]`, подсказки
- `ruslan_cli/setup.py` — 3383 строки, приглашения setup-визарда
- `ruslan_cli/subcommands/setup.py` — subcommand setup
- Приветствие "Welcome to Ruslan Agent!..."
- Команды в `ruslan_cli/commands.py` (COMMANDS_BY_CATEGORY) — описания
- `ruslan_cli/skin_engine.py` — `welcome`, `help_header` дефолты
- ~30+ skin-файлов с EN-строками
- Сообщения об ошибках в `setup.py` и CLI

## Архитектура i18n
- **Текущая модель:** inline-словари в `banner_i18n.py` + skin-system
- **Планируемая:** расширить `banner_i18n.py` → полноценный `ruslan_cli/locales/{en,ru}.py` с категориями:
  - `cli.banner.*` (уже есть, 13 ключей)
  - `cli.help.*` (категории и описания команд)
  - `cli.welcome.*` (приветствие)
  - `cli.setup.*` (все строки визарда)
  - `cli.tools.*` (show_tools заголовки)
  - `cli.errors.*` (общие ошибки)
- Локаль берётся из `config.get("locale", "en")` или `LANG` env

## Ограничения
- STRICT: без изменений upstream GitHub без явного "давай"
- Slash-команды (`/help`, `/model`, `/compress`) остаются на EN — это идентификаторы
- Имена тулзов (`terminal`, `read_file`) — EN
- Бренды (Hermes → Ruslan) — перевод контекстный, код Ruslan остаётся
- Команды CLI (ruslan / ruslan-cli) — EN

## Безопасность
- Не трогать токены / секреты
- Не ломать обратной совместимости (если locale="en" — всё как раньше)
- ru.yaml-стиль: паритет плейсхолдеров (см. memory rules)
