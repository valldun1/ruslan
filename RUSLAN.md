# Руслан — Российская адаптация Hermes Agent

**Форк:** Nous Research Hermes Agent (MIT License)  
**Репозиторий:** [github.com/valldun1/ruslan](https://github.com/valldun1/ruslan)  
**Тестовый домен:** [hermes.sailor.bar](https://hermes.sailor.bar)  
**Цель:** Адаптировать Hermes Agent под русскоязычных пользователей — максимально простой запуск, встроенная поддержка российских LLM, русский язык по умолчанию.

---

## Структура проекта

```
~/Desktop/Руслан/
├── hermes_cli/             ← Исходники CLI (патч: локализация команд)
│   ├── commands.py         ← telegram_bot_commands() + _localized_telegram_desc()
│   ├── default_soul.py     ← DEFAULT_SOUL_MD_RU — русский system prompt
│   └── config.py           ← _ensure_default_soul_md() — определяет язык
│
├── agent/
│   └── i18n.py             ← Система локалей (t(), get_language())
│
├── locales/
│   ├── en.yaml             ← Английский каталог
│   └── ru.yaml             ← Русский каталог (357 строк + telegram_cmd:)
│
├── config.yaml             ← display.language: ru (включён русский)
├── SOUL.md                 ← System prompt (seed: русский при language: ru)
├── landing.html            ← Концепт сайта-витрины
├── RUSLAN.md               ← Этот файл
│
├── android/                ← Деплой на Android (Termux)
│   ├── README.md           ← Документация на русском + английском
│   ├── agent.md            ← Полная инструкция (русский)
│   ├── install.sh          ← Одна команда установки
│   ├── scripts/
│   │   ├── setup-hermes.sh ← Автоматическая настройка
│   │   ├── hyperos-fix.sh  ← Фикс HyperOS (Xiaomi)
│   │   └── start-gateway.sh← Автоперезапуск gateway
│   ├── services/
│   │   ├── bashrc-addon.sh ← .bashrc шаблон
│   │   └── boot-script.sh  ← Автозапуск Termux:Boot
│   └── config/
│       └── config.yaml.example ← Шаблон конфига (DeepSeek/openCode)
│
├── skills/                 ← Скиллы (как в оригинале)
├── gateway/                ← Шлюз
├── plugins/                ← Плагины
├── tools/                  ← Инструменты
└── ... (остальные файлы Hermes)
```

## Что уже сделано

### Локализация Telegram-команд ✅
- `hermes_cli/commands.py`: функция `_localized_telegram_desc()` через `agent.i18n.t()`
- `locales/ru.yaml`: раздел `telegram_cmd:` с переводами для **45 команд**
- `config.yaml`: `display.language: ru` — автоматическое определение языка

### Русский system prompt ✅
- `hermes_cli/default_soul.py`: добавлен `DEFAULT_SOUL_MD_RU`
- `hermes_cli/config.py`: `_ensure_default_soul_md()` определяет язык при первом запуске
- При `display.language: ru` создаётся русский SOUL.md автоматически
- Персона: **«Руслан»** — AI-агент на русском языке

### Сайт-витрина (концепт) ✅
- `landing.html` — тёмная тема, 4 платформы, команды установки

### Android-деплой ✅
- `android/` — полный репозиторий `hermes-on-android` с документацией и скриптами

## План

- [x] Локализация Telegram-команд
- [x] Русский system prompt
- [x] Сайт-витрина (концепт)
- [x] **Установщики под все платформы** — macOS, Linux, Windows (install/)
- [x] **Брендирование** — замена Hermes → Руслан в UI (скин ruslan)
- [x] **Предустановленные провайдеры** — DeepSeek, YandexGPT, GigaChat, OpenRouter, OpenCode
- [x] **Инструкция: бесплатная LLM** — `FREE_LLM.md` (OpenRouter за 5 минут)
- [ ] **Документация на русском** — README, wiki
- [ ] **Брендирование** — замена Hermes → Руслан в UI
- [ ] **Сборка для Termux** — скрипт установки через curl
- [ ] **Деплой на сервер брата** — тестирование

## Как установить

**macOS / Linux:**
```bash
curl -fsSL https://raw.githubusercontent.com/valldun1/ruslan/main/install/install.sh | bash
```

**Windows (PowerShell 7+):**
```powershell
iwr -Uri https://raw.githubusercontent.com/valldun1/ruslan/main/install/install.bat -OutFile install.bat; .\install.bat
```

**Android (Termux):**
```bash
curl -fsSL https://raw.githubusercontent.com/valldun1/ruslan/main/android/install.sh | bash
```

**WSL:**
```bash
curl -fsSL https://raw.githubusercontent.com/valldun1/ruslan/main/android/install.sh | bash
```

---

**Статус:** 17 июня 2026 — сборка проекта, подготовка к деплою на сервер брата.
**Лицензия:** MIT (исходный Hermes Agent © Nous Research)
