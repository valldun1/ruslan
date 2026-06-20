#!/usr/bin/env bash
# ==============================================
# Руслан — Установка на macOS
# ==============================================
# Одна команда:
#   curl -fsSL https://ruslan.team/mac | bash
# ==============================================

set -e

RED='\033[0;31m'
GRN='\033[0;32m'
YLW='\033[1;33m'
CYN='\033[0;36m'
RST='\033[0m'

echo -e "${CYN}"
echo "╔═══════════════════════════════════════╗"
echo "║     🇷🇺 Руслан — установка на macOS    ║"
echo "╚═══════════════════════════════════════╝"
echo -e "${RST}"

# --- Проверка: macOS? ---
if [ "$(uname)" != "Darwin" ]; then
    echo -e "${RED}✗ Скрипт предназначен для macOS!${RST}"
    echo "Для Linux используй: curl -fsSL https://ruslan.team/linux | bash"
    exit 1
fi

RUSLAN_DIR="$HOME/Руслан"

# --- 1. Проверка Homebrew ---
echo -e "${YLW}[1/6] Проверяю Homebrew...${RST}"
if ! command -v brew &>/dev/null; then
    echo -e "${CYN}  — Homebrew не найден, устанавливаю...${RST}"
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)" 2>&1 | tail -3
fi
echo -e "${GRN}  ✔ Homebrew готов${RST}"

# --- 2. Зависимости ---
echo -e "${YLW}[2/6] Устанавливаю зависимости (python3, git)...${RST}"
brew install python3 git curl 2>&1 | tail -3
echo -e "${GRN}  ✔ Зависимости установлены${RST}"

# --- 3. Скачиваем Руслан ---
echo -e "${YLW}[3/6] Скачиваю Руслан...${RST}"
if [ -d "$RUSLAN_DIR" ]; then
    echo -e "${CYN}  — Руслан уже есть, обновляю...${RST}"
    curl -fsSL https://ruslan.team/download/Руслан.tar.gz -o /tmp/Руслан.tar.gz
    tar -xzf /tmp/Руслан.tar.gz -C "$HOME"
    rm /tmp/Руслан.tar.gz
else
    curl -fsSL https://ruslan.team/download/Руслан.tar.gz -o /tmp/Руслан.tar.gz
    tar -xzf /tmp/Руслан.tar.gz -C "$HOME"
    rm /tmp/Руслан.tar.gz
fi
echo -e "${GRN}  ✔ Руслан скачан${RST}"

# --- 4. Виртуальное окружение ---
echo -e "${YLW}[4/6] Создаю виртуальное окружение...${RST}"
python3 -m venv "$RUSLAN_DIR/.venv"
source "$RUSLAN_DIR/.venv/bin/activate"
echo -e "${GRN}  ✔ Виртуальное окружение создано${RST}"

# --- 5. Установка ---
echo -e "${YLW}[5/6] Устанавливаю Руслан...${RST}"
cd "$RUSLAN_DIR"
pip install -e . 2>&1 | tail -3

mkdir -p ~/.config/hermes
if [ ! -f ~/.config/hermes/config.yaml ]; then
    cp "$RUSLAN_DIR/config.yaml.example" ~/.config/hermes/config.yaml
fi
echo -e "${GRN}  ✔ Руслан установлен${RST}"

# --- 6. .zshrc (macOS по умолчанию использует zsh) ---
echo -e "${YLW}[6/6] Настраиваю .zshrc...${RST}"
ZSHRC="$HOME/.zshrc"

if ! grep -q "TELEGRAM_BOT_TOKEN" "$ZSHRC" 2>/dev/null; then
    cat >> "$ZSHRC" << 'ZSHRC_EOF'

# ── Руслан на macOS ──
export HERMES_ACCEPT_HOOKS=1

# >>> ЗАПОЛНИ СВОИ КЛЮЧИ <<<
export OPENCODE_GO_API_KEY="sk-y...port TELEGRAM_BOT_TOKEN="токе...port TELEGRAM_ALLOWED_USERS="твой-telegram-id"
# >>> ЗАПОЛНИ СВОИ КЛЮЧИ <<<

# Алиас для мастера настройки (провайдер, ключи, Telegram)
alias ruslan-setup='cd ~/Руслан && source .venv/bin/activate && hermes setup'

alias ruslan='cd ~/Руслан && source .venv/bin/activate && hermes gateway run --accept-hooks --replace'

# Обновление — одна команда
alias ruslan-update='cd && curl -fsSL https://ruslan.team/mac | bash'
ZSHRC_EOF
    echo -e "${GRN}  ✔ .zshrc обновлён${RST}"
    echo -e "${YLW}  ⚠  ОБЯЗАТЕЛЬНО: nano ~/.zshrc — вставь свои API-ключи!${RST}"
else
    echo -e "${CYN}  — .zshrc уже настроен, пропускаю${RST}"
fi

# --- Готово ---
echo ""
echo -e "${GRN}╔═══════════════════════════════════════╗${RST}"
echo -e "${GRN}║  🇷🇺 Руслан установлен и готов!       ║${RST}"
echo -e "${GRN}╚═══════════════════════════════════════╝${RST}"
echo ""
echo "Что дальше:"
echo "  1. Вставь ключи:       nano ~/.zshrc"
echo "  2. Проверь конфиг:     nano ~/.config/hermes/config.yaml"
echo "  3. Мастер настройки:   source ~/.zshrc && ruslan-setup"
echo "     (выбери провайдера, введи API-ключ, настрой Telegram)"
echo "  4. Запуск:             source ~/.zshrc && ruslan"
echo "  5. Обновление:          ruslan-update  (или перезапусти установщик)"
echo ""
echo "🚀 Что делать дальше: https://ruslan.team/docs/post-install/"
echo "   Telegram ID, Bot Token, провайдер — 4 шага до работающего бота"
echo ""
echo "🔑 Бесплатная LLM за 5 минут:"
echo "  Регистрируйся на openrouter.ai/keys (карта не нужна)"
echo "  nano ~/.config/hermes/config.yaml  — смени модель на qwen/qwen3-coder:free"
echo "  Подробнее: ~/Руслан/FREE_LLM.md"
