# 🛡 Руслан — российский AI-агент

**Руслан** — это автономный AI-агент с открытым исходным кодом.  
Работает в Telegram, Discord, IRC, Slack и Mattermost.  
Русский язык — из коробки. Установка — одна команда.

---

## 🚀 Быстрый старт

**Linux / macOS / Windows (WSL):**

```bash
curl -fsSL https://ruslan.team/linux | bash
```

**Android (Termux):**

```bash
curl -fsSL https://ruslan.team/android | bash
```

После установки:

```bash
ruslan gateway run --accept-hooks
```

Мастер сам спросит провайдера и API-ключ. Подробнее: [Руслан.team](https://ruslan.team)

---

## 💡 Возможности

| | |
|---|---|
| 🇷🇺 **Русский язык** | Интерфейс, команды, промпты, ошибки — всё на русском |
| 🤖 **Автономный агент** | Пишет код, работает с файлами, управляет cron, запускает команды |
| 💬 **5 мессенджеров** | Telegram, Discord, IRC, Slack, Mattermost |
| 🔄 **Мультимодельность** | DeepSeek, GLM, YandexGPT, GigaChat, Claude, GPT — разные модели для разных задач |
| 🆓 **Бесплатные LLM** | OpenRouter :free + Ollama (локально, без ключа) |
| 📱 **Все платформы** | Linux, macOS, Windows, Android (Termux) |
| 🎯 **Скиллы** | 320+ готовых навыков из библиотеки |
| 🔓 **Open Source (MIT)** | Полностью открытый код |

---

## 📦 Что внутри

```ascii
ruslan/
├── hermes/                 ← Ядро агента
├── skin/ruslan/           ← Брендирование, переводы, промпты
├── android/               ← Установщик для Termux
├── website/               ← Сайт ruslan.team
├── plugins/               ← Плагины (YandexGPT, GigaChat, память…)
├── config.yaml.example    ← Шаблон конфига
└── FREE_LLM.md            ← Бесплатные LLM-модели
```

---

## 🌐 Сообщество

- **Сайт:** [ruslan.team](https://ruslan.team)
- **GitHub:** [github.com/ruslan-team](https://github.com/ruslan-team)
- **Telegram-чат:** скоро
- **Документация:** [ruslan.team/docs/](https://ruslan.team/docs/)

---

## 📜 Лицензия

Проект распространяется под **MIT License**.  
Основан на открытом коде [Hermes Agent](https://github.com/NousResearch/hermes-agent) (MIT) © Nous Research.

Дополнительные компоненты — их собственные лицензии.

---

*Сделано в России. Для русскоязычных.* 🛡
