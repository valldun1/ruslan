#!/data/data/com.termux/files/usr/bin/bash
# ==============================================
# Руслан — Установка на Android (Termux)
# ==============================================
# Одна команда:
#   curl -fsSL https://ruslan.team/android | bash
# ==============================================

set -e

# Termux: фикс для Rust/C компиляции (pydantic-core и аналоги)
export ANDROID_API_LEVEL=24

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
pkill -9 -f "ruslan gateway" 2>/dev/null || true
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

# --- 3. Клонируем Руслан (с историей для обновлений через git pull) ---
echo -e "${YLW}[3/8] Клонирую Руслан с GitHub...${RST}"

if [ -d ~/Руслан ]; then
    if [ -d ~/Руслан/.git ]; then
        # Git-репозиторий — быстро обновляем
        echo -e "${CYN}  — Обновляю существующий репозиторий...${RST}"
        cd ~/Руслан && git fetch --depth=1 origin master 2>&1 && git reset --hard FETCH_HEAD
    else
        # Не git — удаляем и клонируем заново
        echo -e "${YLW}  — Старая версия без git, клонирую заново...${RST}"
        rm -rf ~/Руслан
        git clone --depth=1 https://github.com/valldun1/ruslan.git ~/Руслан 2>&1
    fi
else
    git clone --depth=1 https://github.com/valldun1/ruslan.git ~/Руслан 2>&1
fi

# Совместимость: старая папка ruslan/ — симлинк
[ -d ~/ruslan ] && [ ! -L ~/ruslan ] && rm -rf ~/ruslan
[ -d ~/Руслан ] && [ ! -d ~/ruslan ] && ln -sf ~/Руслан ~/ruslan

# --- 4. Установка из исходников ---
echo -e "${YLW}[4/8] Устанавливаю Руслан (pip install -e)...${RST}"

# Сначала ставим без зависимостей — чтобы entry point (ruslan) появился сразу
set +e
pip install --no-deps -e ~/Руслан 2>&1
PIP_EXIT=$?
set -e

# Если entry point не создался — создаём wrapper вручную
if ! command -v ruslan &>/dev/null; then
    echo -e "  ${YLW}→ Создаю wrapper для руслана...${RST}"
    mkdir -p ~/.local/bin
    cat > ~/.local/bin/ruslan << 'HERMES_WRAPPER'
#!/data/data/com.termux/files/usr/bin/bash
exec python3 -m hermes_cli.main "$@"
HERMES_WRAPPER
    chmod +x ~/.local/bin/ruslan
    if command -v ruslan &>/dev/null; then
        echo -e "${GRN}  ✔ руслан wrapper создан${RST}"
    else
        # Может PATH ещё не подхватился
        if [ -f ~/.local/bin/ruslan ]; then
            echo -e "${GRN}  ✔ руслан wrapper в ~/.local/bin${RST}"
        fi
    fi
else
    echo -e "${GRN}  ✔ Команда руслан установлена${RST}"
fi

# --- Базовые зависимости (без них gateway не запустится) ---
# Manual install: только критичные pure-Python пакеты (без C-компиляции, быстро на ARM64).
# Версии пиннятся как в pyproject.toml для согласованности.
# - prompt_toolkit==3.0.52 + wcwidth — для TUI cli.py (`ruslan` без этого падает ModuleNotFoundError)
# - rich уже нужен для gateway; typer — для командной строки; httpx — для API; pyyaml/dotenv — для конфига.
echo -e "  ${YLW}→ Устанавливаю базовые зависимости (yaml, dotenv, typer, httpx, rich, prompt_toolkit)...${RST}"
set +e
pip install --no-deps pyyaml python-dotenv typer httpx rich wcwidth "prompt_toolkit==3.0.52" 2>&1
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

# --- 6b. Остальные pure-Python зависимости (без C-компиляции) ---
# Удаляем левый пакет jwt, если он был установлен ранее.
pip uninstall jwt -y 2>/dev/null || true
# ВНИМАНИЕ: при добавлении новой зависимости в pyproject.toml — добавь её сюда.
# Без этого `ruslan` падает ModuleNotFoundError на agent.model_metadata и других модулях.
# ВАЖНО: НЕ ставим `PyJWT[crypto]` (тянет cryptography — Rust) и `uvicorn[standard]` (тянет uvloop — C).
# Если эти extra-фичи нужны — ставь их отдельно после компиляции Rust-зависимостей (шаг 5).
# --prefer-binary: берём wheel вместо source. Все эти пакеты имеют manylinux/aarch64 wheels.
echo -e "${YLW}[6b/8] Ставлю оставшиеся pure-Python зависимости...${RST}"
set +e
pip install --prefer-binary --no-cache-dir \
  fire ruamel.yaml requests jinja2 croniter "Markdown>=3.5" PyJWT \
  tenacity pathspec ptyprocess 2>&1
# fastapi/uvicorn тянут за собой pydantic-core (Rust).
# Ставим отдельно, чтобы не блокировать остальные пакеты.
echo -e "  ${YLW}→ fastapi + uvicorn (может потребоваться компиляция Rust)...${RST}"
pip install --prefer-binary --no-cache-dir "fastapi>=0.104.0,<1" "uvicorn>=0.24.0,<1" 2>&1
set -e
echo ""

# --- 6c. psutil (C-extension, не поддерживает Android в pip) ---
echo -e "${YLW}[6c/8] Устанавливаю psutil...${RST}"
set +e
pip install --no-cache-dir psutil 2>/dev/null \
  || pip install --no-cache-dir --no-build-isolation psutil 2>/dev/null \
  || pip install --no-cache-dir "psutil==5.9.5" 2>/dev/null \
  || (echo -e "  ${YLW}→ psutil через pkg...${RST}" && pkg install python-psutil -y 2>/dev/null) \
  || echo -e "${YLW}  ⚠ psutil не установлен (некритично, будет доустановлен позже)${RST}"
# Предупреждение: ошибка py3compile после pkg install — некритичный баг Termux, psutil установлен.
echo -e "  ${GRN}✔ psutil: установка завершена (предупреждение py3compile можно игнорировать)${RST}"
set -e
echo ""

# --- 6d-fix. cryptography: если стоит сломанный pip-вариант, переставляем на termux-собранный ---
echo -e "${YLW}[6d/8] Проверяю криптографию...${RST}"
set +e
python3 -c "import cryptography" 2>/dev/null
CRYPTO_OK=$?
set -e
if [ "$CRYPTO_OK" -ne 0 ]; then
    echo -e "  ${YLW}→ cryptography сломан, переставляю через pkg...${RST}"
    set +e
    pip uninstall cryptography -y 2>/dev/null || true
    pkg install python-cryptography -y 2>/dev/null || true
    set -e
fi
echo ""

# --- 6e. Верификация импортов (fail-fast с автодоустановкой) ---
echo -e "${YLW}[6e/8] Проверяю импорты...${RST}"
python3 -c "
missing = []
for mod in ['requests','fire','ruamel.yaml','jinja2','croniter','markdown','jwt',
            'tenacity','pathspec','psutil','fastapi','uvicorn','ptyprocess']:
    try:
        __import__(mod)
    except ImportError:
        missing.append(mod)
if missing:
    print('MISSING: ' + ' '.join(missing))
    raise SystemExit(1)
print('ALL IMPORTS OK')
" 2>&1 || {
    MISSING=$(python3 -c "
import sys
missing = []
for mod in ['requests','fire','ruamel.yaml','jinja2','croniter','markdown','jwt',
            'tenacity','pathspec','psutil','fastapi','uvicorn','ptyprocess']:
    try:
        __import__(mod)
    except ImportError:
        missing.append(mod)
for m in missing:
    sys.stdout.write(m + ' ')
" 2>/dev/null)
    echo -e "${YLW}  ⚠ Отсутствуют: $MISSING"
    echo -e "${YLW}  → Доустанавливаю по одному...${RST}"
    for pkg in $MISSING; do
        # Маппинг: module name → pip package name
        case "$pkg" in
            jwt)       pip_name="PyJWT" ;;
            ruamel.yaml) pip_name="ruamel.yaml" ;;
            psutil)    pip_name="psutil" ;;
            *)         pip_name="$pkg" ;;
        esac
        echo -e "  ${YLW}→ pip install $pip_name${RST}"
        # Перед установкой PyJWT удаляем левый пакет jwt, если он был
        if [ "$pkg" = "jwt" ]; then
            pip uninstall jwt -y 2>/dev/null || true
        fi
        pip install --prefer-binary --no-cache-dir "$pip_name" 2>&1 || true
        # psutil не поддерживает Android в pip — fallback на pkg
        if [ "$pkg" = "psutil" ] && ! python3 -c "import psutil" 2>/dev/null; then
            echo -e "  ${YLW}→ psutil через pkg...${RST}"
            pkg update -y 2>/dev/null || true
            pkg install python-psutil -y 2>/dev/null || true
        fi
    done
    # Финальная проверка
    python3 -c "
for mod in ['requests','fire','ruamel.yaml','jinja2','croniter','markdown','jwt',
            'tenacity','pathspec','psutil','fastapi','uvicorn','ptyprocess']:
    __import__(mod)
print('ALL IMPORTS OK')
" 2>&1 || {
        echo -e "${RED}✗ Не удалось установить некоторые пакеты.${RST}"
        echo -e "${YLW}  Запустите вручную: pip install <имя-пакета>${RST}"
        exit 1
    }
}
echo ""

# --- 7. Конфигурация ---
echo -e "${YLW}[7/8] Создаю конфигурацию...${RST}"
mkdir -p ~/.hermes

# Копируем русский шаблон конфига
cp ~/Руслан/android/config/config.yaml.example ~/.hermes/config.yaml
echo -e "${GRN}  ✔ config.yaml создан (русский язык по умолчанию)${RST}"

# --- 8. .bashrc с авто-запуском ---
echo -e "${YLW}[8/8] Настраиваю .bashrc...${RST}"
BASHRC=~/.bashrc

# Удаляем старую секцию Руслана (если есть) — чтобы обновить
if grep -q "Руслан на Android" "$BASHRC" 2>/dev/null; then
    echo -e "${YLW}  — Обновляю секцию .bashrc...${RST}"
    sed -i '/^# ── Руслан на Android ──$/,/^BASHRC_EOF$/d' "$BASHRC"
fi

# Если секции нет — создаём
if ! grep -q "Руслан на Android" "$BASHRC" 2>/dev/null; then
    cat >> "$BASHRC" << 'BASHRC_EOF'

# ── Руслан на Android ──
export RUSLAN_ACCEPT_HOOKS=1
export PATH="$HOME/.local/bin:$PATH"

# Мастер настройки (провайдер, API-ключ, Telegram Bot Token)
# Команды ruslan-setup и ruslan-update — wrapper'ы в ~/.local/bin, alias'ы не нужны.

# Обновление Руслана — одна команда
# (wrapper ruslan-update уже есть в ~/.local/bin)

# Настоящие скрипты (wrapper'ы) в ~/.local/bin
mkdir -p ~/.local/bin
for cmd in ruslan ruslan-setup ruslan-update; do
    if curl -fsSL "https://ruslan.team/download/scripts/$cmd" -o "$HOME/.local/bin/$cmd" 2>/dev/null; then
        chmod +x "$HOME/.local/bin/$cmd"
    fi
done
# Кириллические версии
for cmd in руслан руслан-setup руслан-update; do
    lat="${cmd//руслан/ruslan}"
    if curl -fsSL "https://ruslan.team/download/scripts/$lat" -o "$HOME/.local/bin/$cmd" 2>/dev/null; then
        chmod +x "$HOME/.local/bin/$cmd"
    fi
done

# Авто-запуск ВЫКЛЮЧЁН по умолчанию.
# После настройки запускай ручную: ruslan
# Для авто-запуска через Termux:Boot создай файл:
#   ~/.termux/boot/start-ruslan.sh
# с содержимым:
#   #!/data/data/com.termux/files/usr/bin/sh
#   . "$HOME/.bashrc"
#   ruslan
#
# ПРОКСИ и VPN:
# Если Telegram не подключается (Россия) — используй режим "Только прокси" в V2RayTun:
#   export ALL_PROXY=socks5://127.0.0.1:10808
if [ ! -f ~/.hermes/config.yaml ]; then
echo "🛡 Руслан готов. Запусти: ruslan-setup (мастер) → ruslan (запуск)"
fi
BASHRC_EOF
    echo -e "${GRN}  ✔ .bashrc создан${RST}"
    echo -e "${GRN}  ✔ Запусти 'ruslan-setup' для настройки${RST}"
else
    echo -e "${CYN}  — .bashrc уже настроен, пропускаю${RST}"
fi

# --- Активируем PATH в текущей сессии ---
export PATH="$HOME/.local/bin:$PATH"
hash -r 2>/dev/null || true

# --- Скачиваем обёртки сразу (не ждём .bashrc) ---
mkdir -p ~/.local/bin
echo -e "${YLW}  └─ Скачиваю обёртки команд...${RST}"
for cmd in ruslan ruslan-setup ruslan-update; do
    curl -fsSL "https://ruslan.team/download/scripts/$cmd" -o "$HOME/.local/bin/$cmd" 2>/dev/null && chmod +x "$HOME/.local/bin/$cmd"
done
for cmd in руслан руслан-setup руслан-update; do
    lat="${cmd//руслан/ruslan}"
    curl -fsSL "https://ruslan.team/download/scripts/$lat" -o "$HOME/.local/bin/$cmd" 2>/dev/null && chmod +x "$HOME/.local/bin/$cmd"
done

# --- Проверка: нашёлся ли руслан ---
echo -e "${YLW}  └─ Проверяю: руслан готов к запуску...${RST}"
if command -v ruslan &>/dev/null; then
    echo -e "${GRN}    ✔ руслан найден в PATH${RST}"
else
    echo -e "${YLW}    ⚠ руслан не найден — проверяю вручную...${RST}"
    if [ -f "$HOME/.local/bin/ruslan" ]; then
        echo -e "${GRN}    ✔ руслан есть в ~/.local/bin (обнови терминал или source ~/.bashrc)${RST}"
    fi
fi

# --- Готово ---
echo ""
echo -e "${GRN}╔══════════════════════════════════════════════════╗${RST}"
echo -e "${GRN}║         🇷🇺  Руслан установлен и готов!        ║${RST}"
echo -e "${GRN}║            от команды Ruslan.team              ║${RST}"
echo -e "${GRN}╚══════════════════════════════════════════════════╝${RST}"
echo ""
echo -e "${CYN}Руслан приветствует вас!${RST}"
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
echo -e "${YLW}Авто-запуск при загрузке телефона:${RST}"
echo "  pkg install termux-boot"
echo "  mkdir -p ~/.termux/boot"
echo "  cp ~/Руслан/android/services/boot-script.sh ~/.termux/boot/"
echo ""
