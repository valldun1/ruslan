# 02 — Plan (GLM-5.2 review)

## Стратегия

- **Источник:** `locales/en.yaml` (baseline, 293 ключа)
- **Цель:** `locales/ru.yaml` (сейчас 350, нужно +17 = 367)
- **Стиль:** технический русский, формальное «вы» (как везде в ru.yaml)
- **Плейсхолдеры** `{name}`, `{title}`, `{room}`, `{error}`, `{used}`, `{total}`, `{pct}`,
  `{model}`, `{provider}`, `{session_key}`, `{scope}`, `{room_id}`, `{thread_id}`,
  `{msg_part}` — **1:1 без изменений**
- **Markdown** (`` `код` ``, `**жирный**`, `\n`) — 1:1
- **Идентификаторы** (`room_id`, `thread_id`, `session_key`, `session_scope`) — **не переводятся**
- **Метки** (`Model:`, `Context:`, `Matrix scope:`) — переводятся (`Модель:`, `Контекст:`, `Область Matrix:`)
- **Бренд:** «Ruslan» (не «Hermes»)

## Словарь терминов

| EN | RU |
|----|-----|
| session | сеанс |
| gateway | шлюз |
| model | модель |
| provider | провайдер |
| context | контекст |
| room | комната (Matrix) |
| scope | область |
| credits | кредиты |
| top up | пополнить |
| transcript | беседа |
| parse error | ошибка разбора |
| logged in | выполнен вход |
| PATH | PATH (не переводить) |
| Nous Portal | Nous Portal (бренд) |
| Matrix | Matrix (бренд) |

## Чек-лист (7 шагов)

1. **5× `resume.*`** — вставить блоком после существующих `resume.*` строк
2. **10× `status.*`** — 6 `matrix_scope_*` + 4 (`model`, `model_provider`, `context`, `context_used`)
3. **1× `update.ruslan_cmd_not_found`** — переименовать `hermes_cmd_not_found` → `ruslan_cmd_not_found` + перевести
4. **1× новая секция `credits:`** — `not_logged_in`
5. **YAML валидация:** `yaml.safe_load` не падает
6. **Паритет плейсхолдеров:** для каждого ключа `{x}` в EN есть в RU
7. **Коммит + push** в `valldun1/ruslan` master

## Команды для пользователя (запуск после пуша)

```bash
# CLI
cd ~/Руслан && source .venv/bin/activate && ruslan

# Telegram gateway
cd ~/Руслан && source .venv/bin/activate && ruslan gateway run --accept-hooks --replace

# Проверить русский в боте: /status, /resume, /update, /credits
```
