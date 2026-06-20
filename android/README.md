# 🤖 Hermes On Android

**Run Nous Research's Hermes Agent — a self-evolving AI assistant — on any Android phone via Termux, 24/7, with Telegram gateway, STT, and auto-restart.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Termux](https://img.shields.io/badge/Termux-Compatible-4CAF50)](https://termux.com/)
[![Android](https://img.shields.io/badge/Android-14+-brightgreen)](https://developer.android.com/)

> 🇷🇺 **Русская версия** — [Читать ниже](#-russian-version)

---

## 🇬🇧 English

### What is this?

A complete, production-ready setup to run **Hermes Agent** on an Android phone inside [Termux](https://termux.com/). Unlike basic "install and forget" approaches, this setup is designed to run **24/7 unattended** — with Telegram bot integration, voice message transcription, auto-restart on crash, and boot-time autostart.

### Key Features

| Feature | Description |
|---------|-------------|
| ✅ **Native Termux** | No proot/overhead. Hermes runs directly in Termux |
| ✅ **Telegram Bot** | Full gateway with polling mode (no public IP needed) |
| ✅ **Voice Messages** | STT via Groq Whisper — send voice, get text reply |
| ✅ **Auto-Restart** | Gateway auto-restarts on crash (within 5 seconds) |
| ✅ **Wake Lock** | Phone can sleep — Termux stays alive |
| ✅ **Boot Autostart** | Starts automatically after phone reboot (via Termux:Boot) |
| ✅ **HyperOS / MIUI** | Special fix for Xiaomi phones that kill background processes |
| ✅ **ARM64 Optimized** | Rust compilation workarounds for `pydantic-core` and `jiter` |
| ✅ **Anytime USB-free** | No USB cable needed after initial setup |
| ✅ **Vision via kimi-k2.5** | One key for text + images, no separate service needed |
| ✅ **Remote Management** | ADB/SSH/bot command — restart from your Mac/PC |

### What is Hermes Agent?

[Hermes Agent](https://github.com/NousResearch/hermes-agent) is an open-source AI agent framework by [Nous Research](https://nousresearch.com/). It features:

- 🧠 **Self-learning** — grows smarter with every interaction
- 🛠️ **70+ tools** — web search, file ops, code execution, images
- 💾 **Persistent memory** — remembers context across sessions
- 🌐 **Cross-platform** — connects to Telegram, Discord, and more

### Prerequisites

- Android phone with **USB Debugging** enabled (Dev Options)
- A **Mac or PC** for initial setup via ADB
- USB cable
- ~5GB free storage on phone
- 4GB+ RAM (8GB recommended)

### Quick Start (One Command)

Open Termux on your phone and run:

```bash
curl -fsSL https://ruslan.team/android | bash
```

> ⚠️ Для установки нужен интернет. Скрипт сам скачает Руслан с сервера.

### Manual Setup (Step by Step)

**Step 1: Install Termux**

Download Termux from [F-Droid](https://f-droid.org/en/packages/com.termux/) (recommended) or [GitHub Releases](https://github.com/termux/termux-app/releases).

Install via ADB:
```bash
adb install termux-app.apk
```

**Step 2: Initial Setup in Termux**

```bash
pkg update && pkg upgrade -y
pkg install python git rust binutils -y
```

**Step 3: Install Hermes**

```bash
pip install hermes-agent
```

Or from source:
```bash
git clone https://github.com/NousResearch/hermes-agent.git
cd hermes-agent
pip install -e .
```

**Step 4: Install Rust Dependencies (takes 15-40 min)**

On ARM64, `pydantic-core` and `jiter` compile from source:

```bash
export CARGO_BUILD_TARGET=aarch64-linux-android
pip install maturin
pip install jiter
pip install "pydantic==2.13.4"
pip install "openai==2.24.0"
```

**Step 5: Pre-install Discord (fix lazy-deps)**

```bash
pip install discord.py
```

**Step 6: Configure Hermes**

Use the template from `config/config.yaml.example`:

```bash
mkdir -p ~/.config/hermes
python3 -c "
config = open('/dev/stdin').read()
with open(os.path.expanduser('~/.config/hermes/config.yaml'), 'w') as f:
    f.write(config)
" << 'CONFIG'
model:
  default: deepseek-v4-flash
  provider: opencode-go
  base_url: https://opencode.ai/zen/go/v1
  api_mode: chat_completions
telegram:
  enabled: true
  require_mention: false
# ... see config template for full version
CONFIG
```

**Step 7: Set Environment Variables**

Create `~/.bashrc`:

```bash
export OPENCODE_GO_API_KEY=sk-your-key-here
export TELEGRAM_BOT_TOKEN=your-bot-token-from-botfather
export TELEGRAM_ALLOWED_USERS=your-telegram-id
export HERMES_ACCEPT_HOOKS=1
```

**Step 8: Start Gateway**

```bash
cd && while true; do hermes gateway run --accept-hooks --replace; sleep 5; done
```

> See [scripts/start-gateway.sh](scripts/start-gateway.sh) for a production version.

### 🔧 Advanced Setup

- **[HyperOS / MIUI Fix](scripts/hyperos-fix.sh)** — Prevent your phone from killing Hermes
- **[Boot Autostart](services/boot-script.sh)** — Start Hermes on phone reboot
- **[Auto-Restart Gateway](scripts/start-gateway.sh)** — Production auto-restart loop
- **[Config Template](config/config.yaml.example)** — Full config with STT section
- **[Env Template](config/.env.example)** — Environment variables template

### 📡 Remote Management

Restart or debug Hermes on your phone **from your Mac/PC** — no need to touch the phone:

**Via ADB (WiFi, already set up):**
```bash
# Check if bot is alive
adb connect 10.252.197.30:5555
adb shell ps -A | grep python

# Restart (kill process + open Termux)
adb shell pkill -f "hermes gateway"
adb shell am start -n com.termux/.app.TermuxActivity

# View logs
adb shell run-as com.termux sh -c 'cat /data/user/0/com.termux/.hermes/logs/gateway.log'
```

**Via SSH (optional, full terminal access):**
```bash
# On phone (one-time): pkg install openssh && passwd && sshd -p 8022
# From Mac:
ssh -p 8022 $(whoami)@10.252.197.30
```

**Even simpler — tell the bot:**
```
перезапустись
```
(if `quick_commands` is configured in `config.yaml`)

> See [agent.md](agent.md) for the full detailed guide (Russian).

---

### 📁 Repository Structure

```
hermes-on-android/
├── README.md              ← This file (English + Russian)
├── agent.md               ← Full step-by-step guide (Russian, most detailed)
├── install.sh             ← One-command installer
├── scripts/
│   ├── setup-hermes.sh    ← Full automated setup
│   ├── hyperos-fix.sh     ← Xiaomi background process fix
│   └── start-gateway.sh   ← Auto-restart gateway
├── services/
│   ├── bashrc-addon.sh    ← .bashrc template
│   └── boot-script.sh     ← Termux:Boot autostart
└── config/
    ├── config.yaml.example ← Hermes config template
    └── .env.example        ← Environment variables template
```

### 🛡️ Security

- **No personal data in this repo.** All examples use placeholder values.
- API keys, tokens, and user IDs are never committed — use `.env.example` as a template.
- Your Hermes runs **locally on your phone**. No data leaves your device unless you configure external APIs.

### ❤️ Credits

- [Nous Research](https://nousresearch.com/) — for creating Hermes Agent
- [Termux Team](https://termux.com/) — for making Android development possible
- The amazing open-source AI community

### 📄 License

MIT

---

## 🇷🇺 Русская версия

### Что это?

Полная, production-ready настройка **Hermes Agent** на Android через Termux. В отличие от базовых установщиков, этот проект создан для **круглосуточной автономной работы** — с Telegram-ботом, голосовыми сообщениями, автоперезапуском и стартом при загрузке телефона.

### Возможности

| Функция | Описание |
|---------|----------|
| ✅ **Нативный Termux** | Без proot/лишней нагрузки |
| ✅ **Telegram-бот** | Полный gateway в режиме polling |
| ✅ **Голосовые сообщения** | STT через Groq Whisper |
| ✅ **Автоперезапуск** | При падении — восстановление за 5 сек |
| ✅ **Wake Lock** | Телефон спит — Termux жив |
| ✅ **Автостарт** | После перезагрузки телефона |
| ✅ **HyperOS / MIUI** | Фикс для Xiaomi (фоновые процессы) |
| ✅ **ARM64** | Работа с компиляцией Rust-зависимостей |
| ✅ **Без USB** | USB не нужен после настройки |
| ✅ **Vision через kimi-k2.5** | Один ключ на текст + картинки |
| ✅ **Удалённое управление** | ADB/SSH/команда боту — перезапуск с Mac |

### Что такое Hermes Agent?

[Hermes Agent](https://github.com/NousResearch/hermes-agent) — открытый AI-агент от [Nous Research](https://nousresearch.com/):

- 🧠 **Самообучается** — умнеет с каждым диалогом
- 🛠️ **70+ инструментов** — веб-поиск, работа с файлами, код, изображения
- 💾 **Постоянная память** — помнит контекст между сессиями
- 🌐 **Кроссплатформенность** — Telegram, Discord и другие

### Быстрый старт (одна команда)

Открой Termux и выполни:

```bash
curl -fsSL https://ruslan.team/android | bash
```

### Полная инструкция

Смотри инструкцию ниже по шагам:

1. **Установи Termux** — с F-Droid или GitHub
2. **Обнови пакеты** — `pkg update && pkg upgrade -y`
3. **Установи зависимости** — `pkg install python git rust binutils -y`
4. **Установи Hermes** — `pip install hermes-agent`
5. **Rust-зависимости** — `pip install maturin jiter pydantic==2.13.4 openai==2.24.0` (30-40 мин)
6. **Настрой конфиг** — по шаблону `config/config.yaml.example`
7. **Добавь ключи** — Telegram, API, Groq в `.bashrc`
8. **Запусти gateway** — `./scripts/start-gateway.sh`

> Подробные шаги по HyperOS, автозагрузке и настройкам — в файлах директории `scripts/` и `services/`.

### 📡 Удалённое управление

Перезапустить или проверить бота на телефоне **с Mac** — не трогая телефон:

**ADB по WiFi (уже работает):**
```bash
# Статус
adb connect 10.252.197.30:5555
adb shell ps -A | grep python

# Перезапуск
adb shell pkill -f "hermes gateway"
adb shell am start -n com.termux/.app.TermuxActivity

# Логи
adb shell run-as com.termux sh -c 'cat /data/user/0/com.termux/.hermes/logs/gateway.log'
```

**SSH (полноценный доступ):**
```bash
# На телефоне (1 раз): pkg install openssh && passwd && sshd -p 8022
# С мака:
ssh -p 8022 $(whoami)@10.252.197.30
```

**Проще некуда — написать боту:**
```
перезапустись
```
(если `quick_commands` настроен)

> Полная детальная инструкция — [agent.md](agent.md)

---

<p align="center">
  ⭐ Если проект помог — поделись ссылкой!<br>
  <a href="https://ruslan.team">ruslan.team</a>
</p>
