#!/data/data/com.termux/files/usr/bin/bash
# ==============================================
# Руслан — Установка на Android (Termux)
# ==============================================
# Одна команда:
#   curl -fsSL https://ruslan.team/android | bash
# ==============================================

set -e
TMP_ARCHIVE=~/Руслан.tar.gz

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

# --- Останавливаем старый авто-запуск, чтобы не мешал установке ---
# Убиваем и процесс, и дочерние, и спящие
pkill -9 -f "start-ruslan" 2>/dev/null || true
pkill -9 -f "hermes gateway" 2>/dev/null || true
pkill -9 -f "ruslan-update" 2>/dev/null || true
sleep 2
# Финальная проверка — чтоб точно не висело
kill $(jobs -p) 2>/dev/null || true

# --- 1. Обновление пакетов ---
echo -e "${YLW}[1/8] Обновляю пакеты Termux...${RST}"
pkg update -y && pkg upgrade -y

# --- 2. Зависимости ---
echo -e "${YLW}[2/8] Устанавливаю зависимости (python, git, rust, binutils)...${RST}"
pkg install python git rust binutils -y

# --- 3. Распаковываем Руслан ---
echo -e "${YLW}[3/8] Распаковываю Руслан...${RST}"
# Скачиваем архив
if [ -d ~/Руслан ]; then
    echo -e "${CYN}  — Папка Руслан уже есть, обновляю...${RST}"
    curl -fsSL https://ruslan.team/download/Руслан.tar.gz -o "$TMP_ARCHIVE" || { echo -e "${RED}✗ Ошибка скачивания!${RST}"; exit 1; }
    tar -xzf "$TMP_ARCHIVE" -C ~ || { echo -e "${RED}✗ Ошибка распаковки!${RST}"; rm -f "$TMP_ARCHIVE"; exit 1; }
    rm -f "$TMP_ARCHIVE"
elif [ -d ~/ruslan ]; then
    echo -e "${CYN}  — Старая папка ruslan, создаю симлинк...${RST}"
    curl -fsSL https://ruslan.team/download/Руслан.tar.gz -o "$TMP_ARCHIVE" || { echo -e "${RED}✗ Ошибка скачивания!${RST}"; exit 1; }
    tar -xzf "$TMP_ARCHIVE" -C ~ || { echo -e "${RED}✗ Ошибка распаковки!${RST}"; rm -f "$TMP_ARCHIVE"; exit 1; }
    rm -f "$TMP_ARCHIVE"
    [ -d ~/ruslan ] && rm -rf ~/ruslan
else
    curl -fsSL https://ruslan.team/download/Руслан.tar.gz -o "$TMP_ARCHIVE" || { echo -e "${RED}✗ Ошибка скачивания!${RST}"; exit 1; }
    tar -xzf "$TMP_ARCHIVE" -C ~ || { echo -e "${RED}✗ Ошибка распаковки!${RST}"; rm -f "$TMP_ARCHIVE"; exit 1; }
    rm -f "$TMP_ARCHIVE"
fi

# Если архив распаковал ruslan/ (старый), создаём симлинк
[ -d ~/ruslan ] && [ ! -d ~/Руслан ] && ln -sf ~/ruslan ~/Руслан

# --- 4. Установка из исходников ---
echo -e "${YLW}[4/8] Устанавливаю Руслан (pip install -e)...${RST}"

# Сначала ставим без зависимостей — чтобы entry point (hermes) появился сразу
set +e
pip install --no-deps -e ~/Руслан 2>&1
PIP_EXIT=$?
set -e

# Если entry point не создался — создаём wrapper вручную
if ! command -v hermes &>/dev/null; then
    echo -e "  ${YLW}→ Создаю wrapper для hermes...${RST}"
    mkdir -p ~/.local/bin
    cat > ~/.local/bin/hermes << 'HERMES_WRAPPER'
#!/data/data/com.termux/files/usr/bin/bash
exec python3 -m hermes_cli.main "$@"
HERMES_WRAPPER
    chmod +x ~/.local/bin/hermes
    if command -v hermes &>/dev/null; then
        echo -e "${GRN}  ✔ hermes wrapper создан${RST}"
    else
        # Может PATH ещё не подхватился
        if [ -f ~/.local/bin/hermes ]; then
            echo -e "${GRN}  ✔ hermes wrapper в ~/.local/bin${RST}"
        fi
    fi
else
    echo -e "${GRN}  ✔ Команда hermes установлена${RST}"
fi

# --- Базовые зависимости (без них gateway не запустится) ---
echo -e "  ${YLW}→ Устанавливаю базовые зависимости (yaml, dotenv, typer, httpx, rich)...${RST}"
set +e
pip install pyyaml python-dotenv typer httpx rich 2>&1
set -e
echo ""

# --- 5. Rust-зависимости (ARM64) ---
echo -e "${YLW}[5/8] Компилирую Rust-зависимости...${RST}"
echo -e "${YLW}  Это может занять 15-40 минут (ARM64)${RST}"
export CARGO_BUILD_TARGET=aarch64-linux-android
set +e
pip install maturin 2>&1
pip install jiter 2>&1
pip install "pydantic==2.13.4" 2>&1
pip install "openai==2.24.0" 2>&1
set -e
echo ""

# --- 6. discord.py (чтоб не зависал gateway) ---
echo -e "${YLW}[6/8] Предустанавливаю discord.py...${RST}"
set +e
pip install discord.py 2>&1
set -e
echo ""

# --- 7. Конфигурация ---
echo -e "${YLW}[7/8] Создаю конфигурацию...${RST}"
mkdir -p ~/.config/hermes

# Копируем русский шаблон конфига
cp ~/Руслан/android/config/config.yaml.example ~/.config/hermes/config.yaml
echo -e "${GRN}  ✔ config.yaml создан (русский язык по умолчанию)${RST}"

# --- 8. .bashrc с авто-запуском ---
echo -e "${YLW}[8/8] Настраиваю .bashrc...${RST}"
BASHRC=~/.bashrc

# Удаляем старую секцию Руслана (если есть) — чтобы обновить
if grep -q "Руслан на Android" "$BASHRC" 2>/dev/null; then
    # Если нет PATH — удаляем и пересоздаём
    if ! grep -q '\.local/bin' "$BASHRC" 2>/dev/null; then
        echo -e "${YLW}  — Обновляю .bashrc (добавляю PATH)...${RST}"
        # Удаляем старый блок (от маркера до end of heredoc)
        sed -i '/^# ── Руслан на Android ──$/,/^BASHRC_EOF$/d' "$BASHRC"
    else
        echo -e "${CYN}  — .bashrc уже в порядке, пропускаю${RST}"
    fi
fi

# Если секции нет — создаём
if ! grep -q "Руслан на Android" "$BASHRC" 2>/dev/null; then
    cat >> "$BASHRC" << 'BASHRC_EOF'

# ── Руслан на Android ──
export HERMES_ACCEPT_HOOKS=1
export PATH="$HOME/.local/bin:$PATH"

# Мастер настройки (провайдер, API-ключ, Telegram Bot Token)
alias ruslan-setup='hermes setup'

# Запуск Руслана
alias ruslan='hermes gateway run --accept-hooks --replace'

# Обновление Руслана — одна команда
alias ruslan-update='cd ~/Руслан && curl -fsSL https://ruslan.team/android | bash'

# Авто-запуск при открытии Termux (если конфиг уже есть)
if [ -f ~/.config/hermes/config.yaml ]; then
start-ruslan() {
    cd ~/Руслан
    while true; do
        echo "[$(date)] Запускаю Руслан..."
        hermes gateway run --accept-hooks --replace 2>&1
        echo "[$(date)] Gateway упал, перезапуск через 5 сек..."
        sleep 5
    done
}
(sleep 10 && start-ruslan &) & disown
else
echo "🛡 Руслан готов. Запусти: ruslan-setup (мастер) → ruslan (запуск)"
fi
BASHRC_EOF
    echo -e "${GRN}  ✔ .bashrc создан${RST}"
    echo -e "${GRN}  ✔ Запустите ruslan-setup для настройки${RST}"
else
    echo -e "${CYN}  — .bashrc уже настроен, пропускаю${RST}"
fi

# --- Активируем PATH в текущей сессии ---
export PATH="$HOME/.local/bin:$PATH"
hash -r 2>/dev/null || true

# --- Проверка: нашёлся ли hermes ---
echo -e "${YLW}  └─ Проверяю: hermes готов к запуску...${RST}"
if command -v hermes &>/dev/null; then
    echo -e "${GRN}    ✔ hermes найден в PATH${RST}"
else
    echo -e "${YLW}    ⚠ hermes не найден — проверяю вручную...${RST}"
    if [ -f "$HOME/.local/bin/hermes" ]; then
        echo -e "${GRN}    ✔ hermes есть в ~/.local/bin (обнови терминал или source ~/.bashrc)${RST}"
    fi
fi

# --- Готово ---
echo ""
echo -e "${GRN}╔═══════════════════════════════════════╗${RST}"
echo -e "${GRN}║  🇷🇺 Руслан установлен и готов!       ║${RST}"
echo -e "${GRN}╚═══════════════════════════════════════╝${RST}"
echo ""
echo "Что дальше:"
echo "  1. Мастер настройки:  ruslan-setup"
echo "     (выбери провайдера, введи API-ключ, настрой Telegram)"
echo "  2. Запуск:            ruslan"
echo "     (запуск gateway после настройки)"
echo "  3. Обновление:          ruslan-update"
echo ""
echo "🚀 Что делать дальше: https://ruslan.team/docs/post-install/"
echo "   Telegram ID, Bot Token, провайдер — 4 шага до работающего бота"
echo ""
echo "Для авто-запуска при загрузке телефона:"
echo "  pkg install termux-boot"
echo "  mkdir -p ~/.termux/boot"
echo "  cp ~/Руслан/android/services/boot-script.sh ~/.termux/boot/"
echo ""
