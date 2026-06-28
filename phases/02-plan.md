# 02 — Plan: перевод баннера Ruslan

## Решение: Вариант A (минимально-инвазивный)

Полная локализация через YAML требует 16 файлов + новый API в `ruslan_cli/i18n.py`.
Это большой рефактор. **Делаем компактный гибрид:**

1. Создаём `ruslan_cli/banner_i18n.py` (новый, ~50 строк) — словарь `BANNER_STRINGS`
   с локалями `en` / `ru` (и fallback на en).
2. В `banner.py` точечно заменяем 12 хардкод-строк на `t("cli.banner.available_tools")` итд.
3. Локаль читается из `~/.ruslan/config.yaml` → `locale: ru` (уже стоит).
4. `en.yaml` и `ru.yaml` НЕ трогаем (чтобы не плодить ключи в общем пуле).

## Что переводим (12 строк, все видимые пользователю)

| # | Ключ | EN | RU |
|---|------|----|----|
| 1 | `available_tools` | `Available Tools` | `Доступные инструменты` |
| 2 | `available_skills` | `Available Skills` | `Доступные навыки` |
| 3 | `mcp_servers` | `MCP Servers` | `MCP-серверы` |
| 4 | `more_toolsets` | `(and N more toolsets...)` | `(и ещё N наборов...)` |
| 5 | `no_skills` | `No skills installed` | `Навыки не установлены` |
| 6 | `skills_disabled` | `Skills toolset disabled` | `Набор навыков отключён` |
| 7 | `summary_help` | `/help for commands` | `/help — список команд` |
| 8 | `summary_separator` | ` · ` | ` · ` (то же) |
| 9 | `commits_behind_one` | `⚠ 1 commit behind` | `⚠ 1 коммит позади` |
| 10 | `commits_behind_many` | `⚠ N commits behind` | `⚠ N коммитов позади` |
| 11 | `update_available` | `⚠ update available` | `⚠ доступно обновление` |
| 12 | `update_run_cmd` | ` — run {cmd} to update` | ` — выполните {cmd} для обновления` |

## Что НЕ переводим

- ASCII-арт (рисуется, читается одинаково)
- `Profile:`, `Runtime:`, `Session:`, `YOLO mode` — оставляем на EN (это бренды/идентификаторы)
- Имена tools/skills/categories — это идентификаторы кода
- `{count} tool(s)`, `{count} MCP servers` — оставляем (это runtime-числа)
- `pip install not officially supported` — глубоко техническое, для dev, не блокирует тест

## Файлы

- **Новый:** `ruslan_cli/banner_i18n.py` — словарь + функция `t(key, **kwargs)`
- **Изменён:** `ruslan_cli/banner.py` — 12 замен (1-3 строки кода на правку)
- **Без изменений:** `locales/*.yaml`, `config.yaml`

## Чек-лист

1. Создать `ruslan_cli/banner_i18n.py` со словарём `BANNER_STRINGS = {"en": {...}, "ru": {...}}` и функцией `t(key, locale, **kwargs)`.
2. В `banner.py` импортировать `t` и передавать текущую локаль (читать из `~/.ruslan/config.yaml` → ключ `locale`).
3. Заменить 12 строк в `banner.py` (строки ~666, 723, 734, 764, 778, 791, 798, 829, 831, 832, 839).
4. Локальный тест: `cd ~/Руслан && source .venv/bin/activate && ruslan --help` (или просто `ruslan`) — увидеть переведённый баннер.
5. Если ОК — коммит + push в `valldun1/ruslan`.
6. В чате: пользователь делает `git pull` в `~/Руслан` и видит русский баннер.
7. GLM-5.2 review: проверить, что перевод естественный и не сломал ASCII-арт.

## Что делать с подписями MCP-статусов (`connected`, `connecting`, `configured`, `failed`, `disabled`)?

Оставляю на EN в этом коммите — это 5 слов, dev-tooling. Если пользователь попросит — добавим отдельно.

## Риски

- ✅ Минимальный риск: меняется только баннер, не логика
- ⚠️ Если `config.yaml` не имеет ключа `locale` — fallback на `en`
- ⚠️ Если `banner_i18n.py` не импортируется — except и fallback на хардкод

## После фикса

Пользователь делает:
```bash
cd ~/Руслан && git pull origin master
ruslan
```
И видит русский баннер.
