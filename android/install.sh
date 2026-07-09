#!/data/data/com.termux/files/usr/bin/bash
# ==============================================
# Руслан — Установка на Android (Termux)
# ==============================================
# Одна команда:
#   curl -fsSL https://raw.githubusercontent.com/valldun1/ruslan/main/android/install.sh | bash
# ==============================================

set -e

RED='\033[0;31m'
GRN='\033[0;32m'
YLW='\033[1;33m'
CYN='\033[0;36m'
RST='\033[0m'

echo -e "${CYN}"
echo "╔═══════════════════════════════════════╗"
echo "║     🇷🇺 Руслан — установка на Android  ║"
echo "╚═══════════════════════════════════════╝"
echo -e "${RST}"

# --- Проверка: Termux? ---
if [ ! -d /data/data/com.termux ]; then
    echo -e "${RED}✗ Скрипт нужно запускать в Termux!${RST}"
    echo "Скачай Termux из F-Droid: https://f-droid.org/packages/com.termux/"
    exit 1
fi

# --- 1. Обновление пакетов ---
echo -e "${YLW}[1/8] Обновляю пакеты Termux...${RST}"
pkg update -y && pkg upgrade -y

# --- 2. Зависимости ---
echo -e "${YLW}[2/8] Устанавливаю зависимости (python, git, rust, binutils)...${RST}"
pkg install python git rust binutils -y

# --- 3. Клонируем Руслан с GitHub ---
echo -e "${YLW}[3/8] Клонирую Руслан (русская версия Hermes Agent)...${RST}"
if [ -d ~/Руслан ]; then
    echo -e "${CYN}  — Руслан уже есть, обновляю...${RST}"
    cd ~/Руслан && git pull 2>&1 | tail -1
else
    git clone https://github.com/valldun1/ruslan.git ~/Руслан 2>&1 | tail -1
fi

# --- 4. Установка из исходников ---
echo -e "${YLW}[4/8] Устанавливаю Руслан (pip install -e)...${RST}"
pip install -e ~/Руслан 2>&1 | tail -3

# --- 5. Rust-зависимости (ARM64) ---
echo -e "${YLW}[5/8] Компилирую Rust-зависимости (15-40 минут, зависит от телефона)...${RST}"
echo -e "${YLW}  └─ Можно пока выпить кофе ☕${RST}"
export CARGO_BUILD_TARGET=aarch64-linux-android
pip install maturin 2>&1 | tail -3
pip install jiter 2>&1 | tail -3
pip install "pydantic==2.13.4" 2>&1 | tail -3
pip install "openai==2.24.0" 2>&1 | tail -3

# --- 6. discord.py (чтоб не зависал gateway) ---
echo -e "${YLW}[6/8] Предустанавливаю discord.py...${RST}"
pip install discord.py 2>&1 | tail -3

# --- 7. Конфигурация ---
echo -e "${YLW}[7/8] Создаю конфигурацию...${RST}"
mkdir -p ~/.config/hermes

# Копируем русский шаблон конфига
cp ~/Руслан/android/config/config.yaml.example ~/.config/hermes/config.yaml
echo -e "${GRN}  ✔ config.yaml создан (русский язык по умолчанию)${RST}"

# --- 8. .bashrc с авто-запуском ---
echo -e "${YLW}[8/8] Настраиваю .bashrc...${RST}"
BASHRC=~/.bashrc

if ! grep -q "TELEGRAM_BOT_TOKEN" "$BASHRC" 2>/dev/null; then
    cat >> "$BASHRC" << 'BASHRC_EOF'

# ── Руслан на Android ──
export HERMES_ACCEPT_HOOKS=1

# >>> ЗАПОЛНИ СВОИ КЛЮЧИ <<<
export OPENCODE_GO_API_KEY="sk-you...-key"
export TELEGRAM_BOT_TOKEN="токен-от-botfather"
export TELEGRAM_ALLOWED_USERS="твой-telegram-id"
# >>> ЗАПОЛНИ СВОИ КЛЮЧИ <<<

# Авто-запуск при открытии Termux
start-ruslan() {
    cd ~
    while true; do
        echo "[$(date)] Запускаю Руслан..."
        hermes gateway run --accept-hooks --replace 2>&1
        echo "[$(date)] Gateway упал, перезапуск через 5 сек..."
        sleep 5
    done
}

(sleep 10 && start-ruslan &) & disown
BASHRC_EOF
    echo -e "${GRN}  ✔ .bashrc создан${RST}"
    echo -e "${YLW}  ⚠  ОБЯЗАТЕЛЬНО: nano ~/.bashrc — вставь свои API-ключи!${RST}"
else
    echo -e "${CYN}  — .bashrc уже настроен, пропускаю${RST}"
fi

# --- Готово ---
echo ""
echo -e "${GRN}╔══════════════════════════════════════════════════╗${RST}"
echo -e "${GRN}║         🇷🇺  Руслан установлен и готов!        ║${RST}"
echo -e "${GRN}║  Автономный AI-агент от Captain Atlantic Sail  ║${RST}"
echo -e "${GRN}╚══════════════════════════════════════════════════╝${RST}"
echo ""
echo -e "${CYN}Приветствую, капитан! Руслан на борту.${RST}"
echo ""
echo -e "${YLW}Доступные команды:${RST}"
echo ""
echo "  ruslan-setup       Быстрая настройка (модель → Telegram)"
echo "  ruslan setup       Полный мастер настройки"
echo "  ruslan setup model Выбор модели и провайдера"
echo "  ruslan setup tts   Настройка озвучки"
echo "  ruslan setup tools Настройка инструментов"
echo "  ruslan gateway     Запуск шлюза мессенджеров"
echo "  ruslan doctor      Проверка системы"
echo "  ruslan update      Обновление Руслана"
echo "  ruslan status      Статус компонентов"
echo ""
echo -e "${GRN}Для начала:${RST}"
echo "  1. Бесплатная LLM:     openrouter.ai/keys (карта не нужна)"
echo "  2. Быстрый старт:       ruslan-setup"
echo "  3. Или полная настройка: ruslan setup"
echo ""
echo -e "${CYN}Больше информации: https://ruslan.team${RST}"
echo ""
