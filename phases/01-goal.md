# Фаза 1: Цель — Русификация Ruslan Agent

## Что делаем
Перевести максимум пользовательского текста Ruslan Agent CLI на русский, сохранив
EN как fallback. Цель: при `locale="ru"` (или `LANG=ru_RU`) пользователь видит
полностью русский интерфейс — баннер, приветствие, /help, /tools, setup-визард,
сообщения об ошибках.

## Что НЕ трогаем
- Slash-команды: `/help`, `/model`, `/new`, `/compress`, `/skill`, `/tools`, `/paste`
  (это идентификаторы — менять = сломать существующие алиасы)
- Имена тулзов: `terminal`, `read_file`, `write_file`, `web_search`
- Имена тулсетов: `file`, `web`, `terminal`
- CLI-команды: `ruslan`, `ruslan-cli`, `ruslan-gateway`
- Имена файлов и путей
- ID, ключи, секреты

## Границы (scope)
- ✅ Баннер: заголовки секций, обновления, нижние строки (уже частично)
- ✅ Приветствие: "Welcome to..." → "Добро пожаловать в Руслан..."
- ✅ /help: категории (Setup/Memory/Skills → Настройка/Память/Навыки) + описания команд
- ✅ /tools: заголовок "Available Tools" → "Доступные инструменты", метки
- ✅ Setup-визард: все приглашения ("Enter API key:", "Select provider:") → RU
- ✅ Сообщения об ошибках (validated, common)
- ❌ Технические логи (logger.error) — оставить EN
- ❌ Документация (README.md, .md файлы) — отдельная задача

## Метрика успеха
1. `locale="ru"` → весь видимый пользователем текст на русском
2. `locale="en"` → всё как сейчас (регрессии = 0)
3. `locale="ru"` → количество непереведённых EN-строк в UI = 0 (или только сознательно оставленные: команды, тулзы, ID)
4. Каждый RU-перевод сохраняет плейсхолдеры (`{n}`, `{cmd}`, `{count}`)
5. Существующий i18n-механизм `banner_i18n.t(key, locale)` расширен, не сломан

## План реализации (на согласование)

### Шаг 1: Расширить `ruslan_cli/locales.py` (новый файл)
- Категории: `banner.*`, `help.*`, `welcome.*`, `tools.*`, `setup.*`, `errors.*`
- Функция `t(key, locale, **kwargs)` — обратная совместимость с `banner_i18n.t`
- `banner_i18n.py` → deprecated alias на `locales.t`

### Шаг 2: Приветствие и баннер
- `cli.py:12164-12167` — брать текст из `locales.t("cli.welcome.text", locale)`
- `show_help()` — категории и описания из `locales.t("cli.help.*")`
- `show_tools()` / `show_toolsets()` — заголовки

### Шаг 3: Команды (`ruslan_cli/commands.py`)
- Каждая команда имеет `description` — вынести в `locales.ru["cli.commands.<name>.description"]`
- Категории — `locales.ru["cli.category.<name>"]`

### Шаг 4: Setup-визард
- `ruslan_cli/setup.py` (3383 строки) — все `_cprint`, `prompt`, `console.print` через `t()`
- Поиск: `console.print\(["']` + ручная категоризация

### Шаг 5: Тест
- `ruslan --locale ru` показывает RU
- `ruslan --locale en` показывает EN
- `/help`, `/tools`, setup-визард — RU при `locale=ru`

### Шаг 6: Сборка
- `python3 -c "from ruslan_cli.locales import t; print(t('cli.welcome.text', 'ru'))"`
- `ruslan --locale ru` → первый экран

## Жду от тебя
- ✅ "давай" → запускаю Фазу 2 (исполнение, ~4-6 часов)
- 🔧 или скорректировать: scope, приоритеты, добавить/убрать шаги
