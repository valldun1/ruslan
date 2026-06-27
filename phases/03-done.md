# 03 — Done

## Что сделано

**Коммит:** `194716f` — `i18n(ru): add 17 missing ru.yaml keys (resume/status/credits/update)`
**Push:** `valldun1/ruslan` master — `76aa032..194716f` ✅
**Diff:** `locales/ru.yaml | 19 +++++++++++++++++++` (1 file, +19 строк)

## Изменения (17 ключей)

### `gateway.resume.*` (5 новых)
- `parse_error` — «⚠️ Не удалось разобрать аргументы `/resume`...»
- `matrix_blocked_no_origin` — про блокировку cross-room
- `matrix_blocked_other_room` — про сеанс в другой комнате
- `matrix_cross_room_success` — успешное возобновление через границу
- `matrix_no_named_sessions` — нет именованных сеансов

### `gateway.status.*` (10 новых)
- `model` — «**Модель:** \`{model}\`»
- `model_provider` — «**Модель:** \`{model}\` ({provider})»
- `context` — «**Контекст:** {used} / {total} ({pct}%)»
- `context_used` — «**Контекст:** ~{used} токенов»
- `matrix_scope_header` — «**Область Matrix:**»
- `matrix_scope_key/mode/room/room_id/thread` — поля дампа

### `gateway.update.ruslan_cmd_not_found` (1 новый)
- Брендинг с Hermes → Руслан, команда `hermes update` → `ruslan update`

### Новая секция `gateway.credits:` (1 ключ)
- `not_logged_in` — про вход в Nous Portal

## Валидация

- ✅ `yaml.safe_load()` не падает
- ✅ Паритет плейсхолдеров 100% (для всех 17 ключей `{x}` в EN совпадают с RU)
- ✅ Missing in RU: **0** (было 17)
- ✅ Total RU keys: **367** (было 350, +17)
- ✅ `git diff` показывает только `locales/ru.yaml`
- ✅ `git push` HTTP 200, `194716f` на remote
