# 00 — Контекст

**Проект:** `ruslan-agent` v0.17.0
**GitHub:** `https://github.com/valldun1/ruslan` (private, branch `master`, коммит `76aa032`)
**Локально:** `~/Desktop/ruslan-agent-main/` (форк/исходники для установки)
**Установка:** `~/Руслан/` (alias `ruslan`), venv `~/Руслан/.venv/`, конфиг `~/.ruslan/`

## Локализация

- Файл: `locales/ru.yaml` (YAML, **не PO**)
- EN-источник: `locales/en.yaml` (293 ключа)
- Текущее состояние RU: 350 ключей (на 57 больше за счёт под-секций)
- **Пропущено:** 17 ключей (gate.* / credits / resume.* / status.* / update.*)
- **Same-as-EN:** 16 ключей — форматтеры, метки, не требуют перевода

## Цель пользователя

Тестировать v0.17.0 локально (CLI + Telegram gateway), увидеть корректный русский язык
во всех местах, где сейчас падает в английский. Стиль — как в существующем `ru.yaml`:
короткие фразы, технический русский, с эмодзи/разметкой как в оригинале.

## Установка для тестирования (17-я, через симлинк)

```bash
# Запуск CLI
cd ~/Руслан && source .venv/bin/activate && ruslan

# Запуск Telegram gateway
cd ~/Руслан && source .venv/bin/activate && ruslan gateway run --accept-hooks --replace

# Версия
~/Руслан/.venv/bin/ruslan --version  # → Ruslan Agent v0.17.0 (2026.6.19)
```

После перевода `ru.yaml` нужно:
1. Пуш в GitHub
2. На стороне пользователя: `cd ~/Руслан && git pull && source .venv/bin/activate && ruslan` — переустановка не нужна, локализация подхватывается на лету
3. Проверить в Telegram-боте: `/status`, `/resume`, `/update`, `/credits` — все 17 ключей должны появиться на русском

## Связанные файлы

- `locales/en.yaml` — source of truth
- `locales/ru.yaml` — целевой файл
- `locales/{de,es,fr,uk,...}.yaml` — стиль соседних локалей
- `phases/02-plan.md` — план перевода
- `phases/03-done.md` — что переведено
- `phases/04-review.md` — ревью
