#!/usr/bin/env bash
# ==============================================
# 🇷🇺 Руслан — Установка на macOS / Linux
# ==============================================
# Одна команда:
#   curl -fsSL https://raw.githubusercontent.com/valldun1/ruslan/main/install/install.sh | bash
# ==============================================

set -e

RED='\033[0;31m'
GRN='\033[0;32m'
YLW='\033[1;33m'
CYN='\033[0;36m'
BLU='\033[0;34m'
RST='\033[0m'

echo -e "${CYN}"
echo "╔═══════════════════════════════════════╗"
echo "║     🇷🇺 Руслан — установка            ║"
echo "║     AI-агент для русскоязычных        ║"
echo "╚═══════════════════════════════════════╝"
echo -e "${RST}"

# ── Определение ОС ──
OS="$(uname -s)"
case "$OS" in
    Darwin)  OS_NAME="macOS" ;;
    Linux)   OS_NAME="Linux" ;;
    *)       echo -e "${RED}✗ Неизвестная ОС: $OS${RST}"; exit 1 ;;
esac
echo -e "${CYN}  → Определена ОС: $OS_NAME${RST}"

# ── Проверка python3 ──
echo ""
echo -e "${YLW}[1/6] Проверяю Python...${RST}"
if ! command -v python3 &>/dev/null; then
    echo -e "${RED}  ✗ Python 3 не найден${RST}"
    if [ "$OS_NAME" = "macOS" ]; then
        if command -v brew &>/dev/null; then
            echo -e "${CYN}  → Устанавливаю через Homebrew...${RST}"
            brew install python
        else
            echo -e "${RED}  ✗ Homebrew не найден. Установи сначала:${RST}"
            echo "    /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
            echo "    Потом запусти скрипт снова."
            exit 1
        fi
    else
        echo -e "${CYN}  → Устанавливаю через apt...${RST}"
        sudo apt update && sudo apt install -y python3 python3-pip python3-venv
    fi
else
    echo -e "${GRN}  ✔ Python $(python3 --version 2>&1 | awk '{print $2}')${RST}"
fi

# ── Проверка pip ──
if ! command -v pip3 &>/dev/null && ! python3 -m pip --version &>/dev/null; then
    echo -e "${YLW}  → Устанавливаю pip...${RST}"
    if [ "$OS_NAME" = "Linux" ]; then
        sudo apt install -y python3-pip
    else
        curl -fsSL https://bootstrap.pypa.io/get-pip.py | python3
    fi
fi

# ── Проверка git ──
echo ""
echo -e "${YLW}[2/6] Проверяю Git...${RST}"
if ! command -v git &>/dev/null; then
    if [ "$OS_NAME" = "macOS" ]; then
        if command -v brew &>/dev/null; then
            brew install git
        else
            echo -e "${RED}  ✗ Установи Git вручную: https://git-scm.com${RST}"
            exit 1
        fi
    else
        sudo apt install -y git
    fi
fi
echo -e "${GRN}  ✔ Git $(git --version 2>&1 | awk '{print $3}')${RST}"

# ── Клонирование репозитория ──
echo ""
echo -e "${YLW}[3/6] Клонирую Руслан с GitHub...${RST}"
RUSLAN_DIR="$HOME/Руслан"
if [ -d "$RUSLAN_DIR" ]; then
    echo -e "${CYN}  — Руслан уже есть, обновляю...${RST}"
    cd "$RUSLAN_DIR" && git pull 2>&1 | tail -1
else
    git clone https://github.com/valldun1/ruslan.git "$RUSLAN_DIR" 2>&1 | tail -1
fi

# ── Установка ──
echo ""
echo -e "${YLW}[4/6] Устанавливаю Руслан (pip install -e)...${RST}"
cd "$RUSLAN_DIR"

# Пробуем разные варианты pip
if command -v pip3 &>/dev/null; then
    PIP_CMD="pip3"
elif python3 -m pip --version &>/dev/null; then
    PIP_CMD="python3 -m pip"
else
    echo -e "${RED}  ✗ pip не найден${RST}"
    exit 1
fi

# На некоторых Linux системах нужен --break-system-packages
$PIP_CMD install -e . 2>&1 | tail -5 || (
    echo -e "${YLW}  → Пробую с --break-system-packages...${RST}"
    $PIP_CMD install -e . --break-system-packages 2>&1 | tail -5
)

# ── Конфигурация ──
echo ""
echo -e "${YLW}[5/6] Создаю конфигурацию...${RST}"
mkdir -p "$HOME/.hermes"

if [ ! -f "$HOME/.hermes/config.yaml" ]; then
    cp "$RUSLAN_DIR/config.yaml.example" "$HOME/.hermes/config.yaml"
    echo -e "${GRN}  ✔ config.yaml создан (русский язык + скин Руслан)${RST}"
else
    echo -e "${CYN}  — config.yaml уже есть, не меняю${RST}"
fi

if [ ! -f "$HOME/.hermes/SOUL.md" ]; then
    cp "$RUSLAN_DIR/SOUL.md" "$HOME/.hermes/SOUL.md"
    echo -e "${GRN}  ✔ SOUL.md создан (русская персона)${RST}"
else
    echo -e "${CYN}  — SOUL.md уже есть, не меняю${RST}"
fi

# ── Готово ──
echo ""
echo -e "${GRN}╔═══════════════════════════════════════╗${RST}"
echo -e "${GRN}║  🇷🇺 Руслан установлен и готов!       ║${RST}"
echo -e "${GRN}╚═══════════════════════════════════════╝${RST}"
echo ""
echo -e "${BLU}Что дальше:${RST}"
echo "  1. Настрой провайдера:    nano ~/.hermes/config.yaml"
echo "  2. Создай .env с ключами: nano ~/.hermes/.env"
echo "  3. Запусти:               hermes gateway run --accept-hooks"
echo ""
echo -e "${BLU}Бесплатная LLM за 5 минут:${RST}"
echo "  Регистрируйся на openrouter.ai/keys (карта не нужна)"
echo "  Подробнее: cat ~/Руслан/FREE_LLM.md"
echo ""
echo -e "${CYN}  GitHub: https://github.com/valldun1/ruslan${RST}"
echo -e "${CYN}  Сайт:   https://ruslan.team${RST}"
echo ""
