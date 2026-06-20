#!/usr/bin/env bash
# ==============================================
# Руслан — Установка на Linux
# ==============================================
# Одна команда:
#   curl -fsSL https://ruslan.team/linux | bash
# ==============================================

set -e

RED='\033[0;31m'
GRN='\033[0;32m'
YLW='\033[1;33m'
CYN='\033[0;36m'
RST='\033[0m'

echo -e "${CYN}"
echo "╔═══════════════════════════════════════╗"
echo "║     🇷🇺 Руслан — установка на Linux   ║"
echo "╚═══════════════════════════════════════╝"
echo -e "${RST}"

# --- Проверка: Linux? ---
if [ "$(uname)" != "Linux" ]; then
    echo -e "${RED}✗ Скрипт предназначен для Linux!${RST}"
    echo "Для macOS используй: curl -fsSL https://ruslan.team/mac | bash"
    exit 1
fi

RUSLAN_DIR="$HOME/Руслан"

# --- 1. Зависимости ---
echo -e "${YLW}[1/7] Устанавливаю зависимости (python3, pip, git)...${RST}"
if command -v apt-get &>/dev/null; then
    sudo apt-get update -qq && sudo apt-get install -y -qq python3 python3-pip python3-venv git curl 2>&1 | tail -3
elif command -v dnf &>/dev/null; then
    sudo dnf install -y python3 python3-pip git curl 2>&1 | tail -3
elif command -v yum &>/dev/null; then
    sudo yum install -y python3 python3-pip git curl 2>&1 | tail -3
elif command -v pacman &>/dev/null; then
    sudo pacman -Sy --noconfirm python python-pip git curl 2>&1 | tail -3
elif command -v apk &>/dev/null; then
    sudo apk add python3 py3-pip git curl 2>&1 | tail -3
else
    echo -e "${RED}✗ Не удалось определить пакетный менеджер.${RST}"
    echo "  Установи вручную: python3, pip, git, curl"
    exit 1
fi
echo -e "${GRN}  ✔ Зависимости установлены${RST}"

# --- 2. Клонируем Руслан ---
echo -e "${YLW}[2/7] Скачиваю Руслан...${RST}"
if [ -d "$RUSLAN_DIR" ]; then
    echo -e "${CYN}  — Руслан уже есть, обновляю...${RST}"
    cd "$RUSLAN_DIR"
    curl -fsSL https://ruslan.team/download/Руслан.tar.gz -o /tmp/Руслан.tar.gz
    tar -xzf /tmp/Руслан.tar.gz -C "$HOME"
    rm /tmp/Руслан.tar.gz
else
    curl -fsSL https://ruslan.team/download/Руслан.tar.gz -o /tmp/Руслан.tar.gz
    mkdir -p "$RUSLAN_DIR"
    tar -xzf /tmp/Руслан.tar.gz -C "$HOME"
    rm /tmp/Руслан.tar.gz
    echo -e "${GRN}  ✔ Руслан скачан${RST}"
fi

# --- 3. Виртуальное окружение ---
echo -e "${YLW}[3/7] Создаю виртуальное окружение...${RST}"
python3 -m venv "$RUSLAN_DIR/.venv" 2>&1 | tail -1
source "$RUSLAN_DIR/.venv/bin/activate"
echo -e "${GRN}  ✔ Виртуальное окружение создано${RST}"

# --- 4. Установка из исходников ---
echo -e "${YLW}[4/7] Устанавливаю Руслан (pip install -e)...${RST}"
cd "$RUSLAN_DIR"
pip install -e . 2>&1 | tail -3
echo -e "${GRN}  ✔ Руслан установлен${RST}"

# --- 5. Конфигурация ---
echo -e "${YLW}[5/7] Создаю конфигурацию...${RST}"
mkdir -p ~/.config/hermes

if [ ! -f ~/.config/hermes/config.yaml ]; then
    cp "$RUSLAN_DIR/config.yaml.example" ~/.config/hermes/config.yaml
    echo -e "${GRN}  ✔ config.yaml создан (русский язык по умолчанию)${RST}"
else
    echo -e "${CYN}  — config.yaml уже существует, пропускаю${RST}"
fi

# --- 6. Системный сервис (systemd) ---
echo -e "${YLW}[6/7] Настраиваю systemd-сервис (опционально)...${RST}"
if command -v systemctl &>/dev/null; then
    SERVICE_PATH="/etc/systemd/system/ruslan.service"
    if [ ! -f "$SERVICE_PATH" ]; then
        sudo tee "$SERVICE_PATH" > /dev/null << 'SERVICE'
[Unit]
Description=Руслан — Russian AI Agent
After=network.target

[Service]
Type=simple
User=%i
WorkingDirectory=%h/Руслан
ExecStart=%h/Руслан/.venv/bin/hermes gateway run --accept-hooks --replace
Restart=always
RestartSec=10
Environment=HERMES_ACCEPT_HOOKS=1

[Install]
WantedBy=default.target
SERVICE
        echo -e "${GRN}  ✔ systemd-сервис создан${RST}"
        echo -e "${YLW}  └─ Запусти: sudo systemctl enable --now ruslan@$USER${RST}"
    else
        echo -e "${CYN}  — Сервис уже существует, пропускаю${RST}"
    fi
else
    echo -e "${CYN}  — systemd не найден, пропускаю (можно запустить вручную)${RST}"
fi

# --- 7. .bashrc с авто-запуском ---
echo -e "${YLW}[7/7] Настраиваю .bashrc...${RST}"
BASHRC="$HOME/.bashrc"

if ! grep -q "TELEGRAM_BOT_TOKEN" "$BASHRC" 2>/dev/null; then
    cat >> "$BASHRC" << 'BASHRC_EOF'

# ── Руслан на Linux ──
export HERMES_ACCEPT_HOOKS=1

# >>> ЗАПОЛНИ СВОИ КЛЮЧИ <<<
export OPENCODE_GO_API_KEY="sk-you...-key"
export TELEGRAM_BOT_TOKEN="токен-от-botfather"
export TELEGRAM_ALLOWED_USERS="твой-telegram-id"
# >>> ЗАПОЛНИ СВОИ КЛЮЧИ <<<

# Алиас для мастера настройки (провайдер, ключи, Telegram)
alias ruslan-setup='cd ~/Руслан && source .venv/bin/activate && hermes setup'

# Алиас для запуска
alias ruslan='cd ~/Руслан && source .venv/bin/activate && hermes gateway run --accept-hooks --replace'

# Обновление Руслана — одна команда
alias ruslan-update='cd && curl -fsSL https://ruslan.team/linux | bash'
BASHRC_EOF
    echo -e "${GRN}  ✔ .bashrc обновлён${RST}"
    echo -e "${YLW}  ⚠  ОБЯЗАТЕЛЬНО: nano ~/.bashrc — вставь свои API-ключи!${RST}"
else
    echo -e "${CYN}  — .bashrc уже настроен, пропускаю${RST}"
fi

# --- Готово ---
echo ""
echo -e "${GRN}╔═══════════════════════════════════════╗${RST}"
echo -e "${GRN}║  🇷🇺 Руслан установлен и готов!       ║${RST}"
echo -e "${GRN}╚═══════════════════════════════════════╝${RST}"
echo ""
echo "Что дальше:"
echo "  1. Вставь ключи:       nano ~/.bashrc"
echo "  2. Проверь конфиг:     nano ~/.config/hermes/config.yaml"
echo "  3. Мастер настройки:   source ~/.bashrc && ruslan-setup"
echo "     (выбери провайдера, введи API-ключ, настрой Telegram)"
echo "  4. Запуск:             source ~/.bashrc && ruslan"
echo "  5. Обновление:          ruslan-update  (или перезапусти установщик)"
echo ""
echo "🚀 Что делать дальше: https://ruslan.team/docs/post-install/"
echo "   Telegram ID, Bot Token, провайдер — 4 шага до работающего бота"
echo ""
echo "Для автозапуска через systemd:"
echo "  sudo systemctl enable --now ruslan@$USER"
echo ""
echo "🔑 Бесплатная LLM за 5 минут:"
echo "  Регистрируйся на openrouter.ai/keys (карта не нужна)"
echo "  nano ~/.config/hermes/config.yaml  # смени model на qwen/qwen3-coder:free"
echo "  Подробнее: ~/Руслан/FREE_LLM.md"
