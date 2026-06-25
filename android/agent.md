# agent.md — Hermes Agent на Android (Termux)

**Устройство:** Redmi Note 14 (arm64, Android 15 / HyperOS 2.0, ~8GB RAM)
**Бот:** @gokritobot (ID: 8696327633)
**Дата:** 5 июня 2026
**Статус:** ✅ Работает: Hermes Gateway + Telegram-бот + STT + ADB-управление
**GitHub:** https://github.com/valldun1/hermes-on-android

---

## ⚡ Быстрая проверка

Бот живёт **внутри телефона** и запускается автоматически:

1. **Открой Termux** на телефоне — через 10 сек бот запустится сам
2. **Напиши @gokritobot «тест»** — должен ответить
3. Отправь **голосовое** — распознаёт через Groq Whisper
4. **USB можно отключать** — боту не нужен

Если не работает → `cd && bash start-hermes.sh`

---

## 📡 ADB-управление телефоном

**Статус:** ✅ Беспроводной ADB работает параллельно с USB
**Gateway:** ✅ Запущен, Telegram подключён (polling)

### Подключение
| Параметр | Значение |
|----------|----------|
| IP | `10.252.197.30:5555` |
| Модель | Redmi Note 14 (24117RN76E) |
| Android | 15 |
| HyperOS | V816 |
| Разрешение | 1080×2400 |
| Батарея | 72% |

### Два активных канала
- 🔌 **USB** — `fqfmamo7ceibeetk (usb:20-2)`
- 📡 **TCP (WiFi)** — `10.252.197.30:5555` — работает параллельно

При переключении adbd в TCP-режим и подключении по WiFi — сопряжение не требуется, если телефон уже был авторизован по USB.

### Что установлено и настроено на телефоне (Hermes внутри Termux)

| Компонент | Назначение |
|-----------|-----------|
| ✅ `android-tools` | ADB внутри Termux |
| ✅ `adb-android-control` | Справочник команд + Python-скрипты для контроля телефона |
| ✅ `adb-automation` | Паттерны для Telegram, X, Keep, Alarmy |
| ✅ `termux-services (runit)` | Автоконнект ADB при перезапуске Termux |
| ✅ `~/.termux/boot/` | Boot-скрипт — ADB стартует автоматически при загрузке |
| ✅ `.bashrc` хелперы | `adb-connect`, `adb-reconnect`, `adb-list` — быстрые команды |
| ✅ STT | Groq Whisper — голосовые сообщения работают |

### Примеры ADB-команд (с Mac по WiFi)

```bash
# Подключиться
adb connect 10.252.197.30:5555

# Сделать скриншот
adb shell screencap /sdcard/screen.png
adb pull /sdcard/screen.png

# Тап по координатам
adb shell input tap 540 1200

# Свайп
adb shell input swipe 540 2000 540 500

# Открыть приложение
adb shell am start -n com.termux/.app.TermuxActivity

# Проверить батарею
adb shell dumpsys battery | grep level

# Ввести текст (латиница)
adb shell input text "hello world"
```

> ⚠️ Для русского текста и эмодзи нужен ADBKeyBoard — дополнительная настройка

---

## 📖 ПОЛНАЯ ИНСТРУКЦИЯ С НУЛЯ

### Часть 1. Подготовка

#### 1.1 Включить режим разработчика на телефоне
- Настройки → О телефоне → Нажать «Версия MIUI» 7 раз
- Настройки → Дополнительные → Для разработчиков
- Включить **«Отладка по USB»**
- **ВАЖНО:** Отключить **«Оптимизацию MIUI»** — без этого HyperOS убьёт фоновые процессы (бот умрёт через 10 мин после отключения USB)
- Подключить телефон к Mac кабелем USB

#### 1.2 Настроить ADB на Mac
```bash
# платформенные инструменты
cd /tmp && curl -O https://dl.google.com/android/repository/platform-tools-latest-darwin.zip
unzip platform-tools-latest-darwin.zip

# проверить, что телефон виден
/tmp/platform-tools/adb devices -l
# → должно показать fqfmamo7ceibeetk device
```

#### 1.3 HyperOS — победить блокировку установки APK
```bash
# отключаем проверку установки
/tmp/platform-tools/adb shell settings put global verifier_verify_adb_installs 0
/tmp/platform-tools/adb shell settings put secure install_non_market_apps 1
```

---

### Часть 2. Установка Termux

#### 2.1 Скачать и установить Termux
```bash
# скачиваем APK (F-Droid версия — она стабильнее)
cd /tmp && curl -L -o termux.apk \
  "https://github.com/termux/termux-app/releases/download/v0.118.3/termux-app_v0.118.3+github-debug_arm64-v8a.deb.apk"

# устанавливаем
/tmp/platform-tools/adb install termux.apk
```

#### 2.2 Запустить Termux и обновить
```bash
# открыть Termux на телефоне
/tmp/platform-tools/adb shell am start -n com.termux/.app.TermuxActivity

# дать ему 10-20 сек на инициализацию (скачает bootstrap)

# обновить пакеты
/tmp/platform-tools/adb shell run-as com.termux sh -c \
  'export PATH=/data/data/com.termux/files/usr/bin:$PATH; \
   apt update -y && apt full-upgrade -y'

# если зависло на конфиге — решить: dpkg --force-confnew --configure <пакет>
```

#### 2.3 Установить зависимости
```bash
/tmp/platform-tools/adb shell run-as com.termux sh -c \
  'export PATH=/data/data/com.termux/files/usr/bin:$PATH; \
   pkg install python git openssh rust binutils -y'
```

#### 2.4 Разрешить Termux доступ к файлам
```bash
/tmp/platform-tools/adb shell pm grant com.termux android.permission.READ_EXTERNAL_STORAGE
/tmp/platform-tools/adb shell pm grant com.termux android.permission.WRITE_EXTERNAL_STORAGE
```

---

### Часть 3. Установка Hermes

#### 3.1 Установить Hermes из pip
```bash
/tmp/platform-tools/adb shell run-as com.termux \
  /data/data/com.termux/files/usr/bin/pip install hermes-agent
```

#### 3.2 Или установить из git (редактируемый режим)
```bash
/tmp/platform-tools/adb shell run-as com.termux sh -c \
  'export PATH=/data/data/com.termux/files/usr/bin:$PATH; \
   cd && git clone https://github.com/NousResearch/hermes-agent.git && \
   cd hermes-agent && pip install -e .'
```

#### 3.3 Rust-зависимости — pydantic-core и jiter
⚠️ **Самый медленный шаг.** На arm64 нет pre-built wheels — Rust компилируется 15-40 минут.

```bash
# Установить maturin (тоже компилируется ~5 мин) и pydantic/openai
/tmp/platform-tools/adb shell run-as com.termux sh -c \
  'export PATH=/data/data/com.termux/files/usr/bin:$PATH; \
   export CARGO_BUILD_TARGET=aarch64-linux-android; \
   pip install maturin && \
   pip install jiter && \
   pip install "pydantic==2.13.4" && \
   pip install "openai==2.24.0"'
```

Если компиляция падает по памяти — попробовать по одному:
```bash
pip install maturin   # ~5 мин
pip install jiter     # ~10-15 мин
pip install pydantic  # ~10 мин
pip install openai    # быстро
```

#### 3.4 Установить discord.py (чтобы lazy-deps не вис)
```bash
/tmp/platform-tools/adb shell run-as com.termux sh -c \
  'export PATH=/data/data/com.termux/files/usr/bin:$PATH; \
   pip install discord.py'
```

---

### Часть 4. Настройка

#### 4.1 Создать файлы конфигурации

**~/.config/hermes/config.yaml** — основной конфиг:
```yaml
model:
  default: deepseek-v4-flash
  provider: opencode-go
  base_url: https://opencode.ai/zen/go/v1
  api_mode: chat_completions

providers: {}

terminal:
  backend: local
  cwd: /data/data/com.termux/files/home
  timeout: 180

toolsets:
  - hermes-cli

memory:
  memory_enabled: false

display:
  compact: true
  streaming: false

telegram:
  enabled: true
  require_mention: false
```

Записать через Python (наследовать не работает через run-as):
```bash
/tmp/platform-tools/adb shell run-as com.termux \
  /data/data/com.termux/files/usr/bin/python3 -c "
import os
os.makedirs(os.path.expanduser('~/.config/hermes'), exist_ok=True)
config = open('/dev/stdin').read()
with open(os.path.expanduser('~/.config/hermes/config.yaml'), 'w') as f:
    f.write(config)
" << 'CONFIG'
model:
  default: deepseek-v4-flash
  provider: opencode-go
  base_url: https://opencode.ai/zen/go/v1
  api_mode: chat_completions
...

telegram:
  enabled: true
  require_mention: false
CONFIG
```

#### 4.2 Создать .bashrc с автозапуском
```bash
/tmp/platform-tools/adb shell run-as com.termux sh -c \
  'export PATH=/data/data/com.termux/files/usr/bin:$PATH; \
   cat > /data/data/com.termux/files/home/.bashrc << '\''EOF'\''
export OPENCODE_GO_API_KEY=sk-...ваш-ключ...
export HERMES_ACCEPT_HOOKS=1
export TELEGRAM_BOT_TOKEN=...токен-бота...
export TELEGRAM_ALLOWED_USERS=5838842946

start-hermes() {
  cd ~
  while true; do
    echo "[$(date)] Starting Hermes gateway..."
    hermes gateway run --accept-hooks --replace 2>&1
    echo "[$(date)] Gateway died, restarting in 5s..."
    sleep 5
  done
}

# Автозапуск при открытии Termux (с задержкой)
(sleep 10 && start-hermes &) & disown
EOF'
```

#### 4.3 Создать скрипт ручного запуска
```bash
/tmp/platform-tools/adb shell run-as com.termux sh -c \
  'export PATH=/data/data/com.termux/files/usr/bin:$PATH; \
   cat > /data/data/com.termux/files/home/start-hermes.sh << '\''EOF'\''
#!/data/data/com.termux/files/usr/bin/bash
export PATH=/data/data/com.termux/files/usr/bin:$PATH
export OPENCODE_GO_API_KEY=sk-...
export HERMES_ACCEPT_HOOKS=1
export TELEGRAM_BOT_TOKEN=...
export TELEGRAM_ALLOWED_USERS=5838842946
source ~/.bashrc 2>/dev/null
cd ~
while true; do
    echo "[$(date)] Starting Hermes gateway..."
    hermes gateway run --accept-hooks --replace 2>&1
    echo "[$(date)] Gateway died, restarting in 5s..."
    sleep 5
done
EOF
   chmod +x ~/start-hermes.sh'
```

---

### Часть 5. Автостарт при загрузке телефона

#### 5.1 Установить Termux:Boot
```bash
# скачать APK
cd /tmp && curl -L -o termux-boot.apk \
  "https://github.com/termux/termux-boot/releases/download/v0.8.1/termux-boot-app_v0.8.1+github-debug_arm64-v8a.deb.apk"
/tmp/platform-tools/adb install termux-boot.apk
```

#### 5.2 Создать boot-скрипт
```bash
/tmp/platform-tools/adb shell run-as com.termux sh -c \
  'export PATH=/data/data/com.termux/files/usr/bin:$PATH; \
   mkdir -p ~/.termux/boot && \
   cat > ~/.termux/boot/hermes-gateway << '\''EOF'\''
#!/data/data/com.termux/files/usr/bin/bash
sleep 10
termux-wake-lock
cd /data/data/com.termux/files/home
export HERMES_ACCEPT_HOOKS=1
source .bashrc 2>/dev/null
while true; do
    hermes gateway run --accept-hooks --replace
    sleep 5
done
EOF
   chmod +x ~/.termux/boot/hermes-gateway'
```

#### 5.3 Wake-lock — телефон не усыпляет Termux
```bash
/tmp/platform-tools/adb shell cmd deviceidle whitelist +com.termux
/tmp/platform-tools/adb shell appops set com.termux RUN_ANY_IN_BACKGROUND allow
/tmp/platform-tools/adb shell appops set com.termux RUN_IN_BACKGROUND allow
```

---

### Часть 6. STT (голосовые сообщения)

#### 6.1 Настроить Groq Whisper

**~/.hermes/.env**:
```
GROQ_API_KEY=gsk_...ваш-ключ...
```

**config.yaml** добавить секцию:
```yaml
stt:
  provider: groq
  groq:
    api_key: gsk_...
    model: whisper-large-v3
```

#### 6.2 Установить скилы
```bash
# через терминал на телефоне
hermes skills install voice-transcription
hermes skills install vision-analysis
hermes skills install telegram-voice-stt
```

---

### Часть 7. Проверка

```bash
# проверка версии
adb shell run-as com.termux /data/data/com.termux/files/usr/bin/hermes --version

# проверить версию
adb shell run-as com.termux /data/data/com.termux/files/usr/bin/hermes --version

# запустить диагностику
adb shell run-as com.termux sh -c \
  'export PATH=/data/data/com.termux/files/usr/bin:$PATH; \
   export OPENCODE_GO_API_KEY=sk-...; \
   hermes doctor'

# проверить, что процесс живёт
adb shell ps -A | grep python

# логи гейтвея
adb shell run-as com.termux sh -c \
  'export PATH=/data/data/com.termux/files/usr/bin:$PATH; \
   cat /data/user/0/com.termux/.hermes/logs/gateway.log'
```

---

### Часть 8. Повседневное использование

**✅ Нормальная работа:**
- Телефон на зарядке, Termux открыт → бот работает
- Телефон просто заряжается (экран выкл) → бот живёт благодаря wake-lock
- USB отключён → боту норм, он внутри телефона

**❌ Если бот не отвечает:**
1. Открой Termux — через 10 сек бот запустится
2. Проверь `ps -A | grep python` — есть ли процесс
3. Если нет → `cd && bash start-hermes.sh`

**🔁 После перезагрузки телефона:**
- Termux:Boot запустит бота через ~10-15 сек
- Если не сработало → открыть Termux вручную

---

### 🗺️ Карта файлов на телефоне

| Путь | Назначение |
|------|-----------|
| `~/.bashrc` | Автостарт gateway при открытии Termux |
| `~/.termux/boot/hermes-gateway` | Автостарт при загрузке телефона |
| `~/.config/hermes/config.yaml` | Основной конфиг |
| `~/.hermes/.env` | API ключи |
| `~/start-hermes.sh` | Скрипт ручного запуска с автовосстановлением |
| `~/agent.md` | Этот файл (на Desktop'е Mac) |
| `/data/user/0/com.termux/.hermes/logs/gateway.log` | Логи гейтвея |
| `/data/user/0/com.termux/.hermes/logs/agent.log` | Логи агента |

### 🔑 Ключи, которые нужны

| Что | Где взять |
|-----|-----------|
| `TELEGRAM_BOT_TOKEN` | @BotFather → создать бота |
| `OPENCODE_GO_API_KEY` | opencode.ai → API ключ |
| `GROQ_API_KEY` | console.groq.com → API ключ |

---

### ⚠️ Типичные проблемы и решения

| Проблема | Решение |
|----------|---------|
| `adb install` → `INSTALL_FAILED_VERIFICATION_FAILURE` | HyperOS блокирует. Отключить «Оптимизацию MIUI» в настройках разработчика, либо: `adb shell settings put global verifier_verify_adb_installs 0 && adb shell settings put secure install_non_market_apps 1` |
| Бот умирает через 10-20 мин после отключения USB | HyperOS убивает фоны. Проверить: 1) Оптимизация MIUI выключена, 2) `cmd deviceidle whitelist +com.termux`, 3) в boot-скрипте `termux-wake-lock` |
| `pip install jiter/pydantic-core` висит часами | Rust компиляция. Нормально — ждать до 40 мин. Можно пустить в фоне с `notify_on_complete` |
| Gateway пишет «No messaging platforms enabled» | Нет env-переменных TELEGRAM_BOT_TOKEN/TELEGRAM_ALLOWED_USERS — передать их или добавить в .bashrc |
| Gateway умирает с exit 143 | ADB-сессия завершилась — используй `background=true` и `--replace` |
| `discord.py` устанавливается бесконечно | lazy-deps качает brotlicffi — предустанови `pip install discord.py` заранее |
| Bot doesn't respond to DMs | `require_mention: false` в config.yaml — иначе игнорирует сообщения без @упоминания |

---

### 🤝 Для брата: быстрый старт

Если нужно с нуля на другом телефоне:

1. Включить отладку по USB + отключить Оптимизацию MIUI
2. Подключить к Mac, установить Termux через ADB
3. В Termux: `pkg install python git rust -y && pip install hermes-agent`
4. Компиляция Rust-зависимостей (~30-40 мин, просто ждать)
5. Прописать в .bashrc: ключи + автозапуск
6. Создать boot-скрипт для автостарта при загрузке
7. Включить wake-lock, отключить оптимизацию MIUI

Подробно — шаги из этой инструкции выше. На всё про всё — ~1 час.

---

---

### 📡 Часть 9. Удалённое управление с Mac (когда ты за компом)

Если бот на телефоне лёг, а ты за маком — перезапустить можно **не вставая со стула**. Два способа:

#### 9.1 Быстрый способ — ADB по WiFi (уже настроено)

Вспомогательные скрипты сохрани в `~/.hermes/scripts/phone-hermes.sh` на Mac:

```bash
#!/bin/bash
# phone-hermes.sh — управление Hermes на телефоне с Mac
ADB="/tmp/platform-tools/adb"
PHONE="10.252.197.30:5555"

cmd_connect() { $ADB connect $PHONE; }
cmd_status() {
  $ADB shell ps -A | grep python | grep -v grep
  echo "---"
  echo "Gateway log (last 10 lines):"
  $ADB shell run-as com.termux sh -c 'export PATH=/data/data/com.termux/files/usr/bin:$PATH; tail -10 /data/user/0/com.termux/.hermes/logs/gateway.log' 2>/dev/null
}
cmd_restart() {
  # убить старый процесс
  PID=$($ADB shell ps -A | grep python | awk '{print $2}' | head -1)
  [ -n "$PID" ] && $ADB shell kill $PID
  sleep 2
  # открыть Termux (запустит .bashrc → gateway)
  $ADB shell am start -n com.termux/.app.TermuxActivity
  echo "✅ Termux открыт, gateway стартует через 10 сек..."
}
cmd_logs() {
  $ADB shell run-as com.termux sh -c 'export PATH=/data/data/com.termux/files/usr/bin:$PATH; cat /data/user/0/com.termux/.hermes/logs/gateway.log' 2>/dev/null
}
cmd_exec() {
  # выполнить любую команду внутри Termux
  $ADB shell run-as com.termux sh -c "export PATH=/data/data/com.termux/files/usr/bin:\$PATH; $*"
}

case "${1:-status}" in
  connect) cmd_connect ;;
  status|st) cmd_status ;;
  restart|re) cmd_restart ;;
  logs|l) cmd_logs ;;
  exec|e) shift; cmd_exec "$@" ;;
  *) echo "Usage: phone-hermes.sh [connect|status|restart|logs|exec <cmd>]" ;;
esac
```

Сделать исполняемым:
```bash
chmod +x ~/.hermes/scripts/phone-hermes.sh
```

**Примеры использования с Mac:**
```bash
# проверить, жив ли бот
~/.hermes/scripts/phone-hermes.sh status

# перезапустить (убить процесс + открыть Termux)
~/.hermes/scripts/phone-hermes.sh restart

# посмотреть логи
~/.hermes/scripts/phone-hermes.sh logs | tail -30

# подключиться, если WiFi ADB отвалился
~/.hermes/scripts/phone-hermes.sh connect

# выполнить команду внутри Termux
~/.hermes/scripts/phone-hermes.sh exec "hermes --version"
~/.hermes/scripts/phone-hermes.sh exec "ls -la ~/.hermes/logs/"
```

#### 9.2 Продвинутый способ — SSH в Termux (полноценный доступ)

Для тех случаев, когда ADB-команд мало:

**На телефоне (1 раз):**
```bash
pkg install openssh -y
# задать пароль для ssh (или настроить ключи)
passwd
# запустить SSH-сервер
sshd -p 8022
```

**Добавить автостарт SSH в .bashrc** (перед `start-hermes`):
```bash
# SSH-сервер на порту 8022
sshd -p 8022 2>/dev/null

# узнать IP телефона (для подключения)
echo "Phone IP: $(ip -4 addr show wlan0 | grep inet | awk '{print $2}' | cut -d/ -f1)"
```

**Подключение с Mac:**
```bash
ssh -p 8022 $(whoami)@10.252.197.30
# → пароль, который задали через passwd
```

**Без пароля — ключи:**
```bash
# на Mac:
ssh-keygen -t ed25519 -f ~/.ssh/phone-hermes -N ""
ssh-copy-id -p 8022 $(whoami)@10.252.197.30

# теперь логин без пароля:
ssh -p 8022 -i ~/.ssh/phone-hermes $(whoami)@10.252.197.30
```

Если IP телефона меняется (DHCP) — используй ADB способ (9.1), он по ADB-сертификату, не по IP.

#### 9.3 Ещё проще — добавить команду в бота

Добавь в config.yaml на телефоне **алиас на команду «перезапустись»**:

```yaml
# (в .bashrc или quick_commands в config.yaml)
quick_commands:
  перезапустись: "pkill -f \"hermes gateway\"; sleep 2; nohup hermes gateway run --accept-hooks --replace &"
```

Тогда можно просто написать боту **«перезапустись»** и он сам перезапустит свой gateway.

---

*Последнее обновление: 5 июня 2026*
