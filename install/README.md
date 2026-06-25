# 🇷🇺 Руслан — Установка

| Платформа    | Команда |
|-------------|---------|
| **macOS / Linux** | `curl -fsSL https://raw.githubusercontent.com/valldun1/ruslan/main/install/install.sh \| bash` |
| **Windows** (PowerShell 7+) | `iwr -Uri https://raw.githubusercontent.com/valldun1/ruslan/main/install/install.bat -OutFile install.bat; .\install.bat` |
| **Android** (Termux) | `curl -fsSL https://raw.githubusercontent.com/valldun1/ruslan/main/android/install.sh \| bash` |
| **WSL** | `curl -fsSL https://raw.githubusercontent.com/valldun1/ruslan/main/android/install.sh \| bash` |

## Системные требования

- **macOS**: macOS 10.13+, Python 3.9+, Git
- **Linux**: Ubuntu 20.04+ / Debian 11+, Python 3.9+, Git
- **Windows**: Windows 10+, PowerShell 7+, Python 3.9+, Git
- **Android**: Termux из F-Droid (не Google Play)

## После установки

1. Отредактируй `~/.hermes/config.yaml` — выбери провайдера
2. Создай `~/.hermes/.env` с API-ключами
3. Запусти: `hermes gateway run --accept-hooks`

Бесплатный старт: [OpenRouter](https://openrouter.ai/keys) — регистрация за 2 минуты, карта не нужна.
