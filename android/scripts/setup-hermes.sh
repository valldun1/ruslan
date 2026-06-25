#!/data/data/com.termux/files/usr/bin/bash
# ==============================================
# Hermes On Android — Full Automated Setup
# ==============================================
# Run AFTER install.sh completes.
# Configures: config.yaml, .env, STT, gateway
# ==============================================

set -e

RED='\033[0;31m'
GRN='\033[0;32m'
YLW='\033[1;33m'
CYN='\033[0;36m'
RST='\033[0m'

echo -e "${CYN}╔═══════════════════════════════════════╗${RST}"
echo -e "${CYN}║    Hermes On Android — Setup          ║${RST}"
echo -e "${CYN}╚═══════════════════════════════════════╝${RST}"

# --- 1. Install skills ---
echo -e "${YLW}[1/4] Installing Hermes skills...${RST}"
hermes skills install voice-transcription 2>/dev/null || echo "  └─ (skill may already be installed)"
hermes skills install telegram-voice-stt 2>/dev/null || true
echo -e "${GRN}  ✔ Skills installed${RST}"

# --- 2. Create config.yaml ---
echo -e "${YLW}[2/4] Creating config.yaml...${RST}"

CONFIG_DIR="$HOME/.config/hermes"
mkdir -p "$CONFIG_DIR"

if [ ! -f "$CONFIG_DIR/config.yaml" ]; then
    cat > "$CONFIG_DIR/config.yaml" << 'CONFIG_EOF'
# ── Hermes On Android — Config ──
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

# ── Telegram ──
telegram:
  enabled: true
  require_mention: false

# ── STT (Speech-to-Text) ──
stt:
  provider: groq
  groq:
    api_key: "${GROQ_API_KEY}"
    model: whisper-large-v3
CONFIG_EOF
    echo -e "${GRN}  ✔ config.yaml created${RST}"
    echo -e "${YLW}  ⚠  Edit your GROQ_API_KEY in .bashrc if not set${RST}"
else
    echo -e "${CYN}  – config.yaml already exists, skipping${RST}"
fi

# --- 3. Create .env template ---
echo -e "${YLW}[3/4] Creating .env template...${RST}"
ENV_DIR="$HOME/.hermes"
mkdir -p "$ENV_DIR"

if [ ! -f "$ENV_DIR/.env" ]; then
    cat > "$ENV_DIR/.env" << 'ENV_EOF'
# ── Hermes Secrets ──
# Fill in your real keys here (or set them in .bashrc)
GROQ_API_KEY="gsk_your-groq-api-key"
ENV_EOF
    echo -e "${GRN}  ✔ .env template created${RST}"
else
    echo -e "${CYN}  – .env already exists, skipping${RST}"
fi

# --- 4. Verify Hermes works ---
echo -e "${YLW}[4/4] Verifying Hermes installation...${RST}"
VERSION=$(hermes --version 2>/dev/null || echo "unknown")
echo -e "  Version: ${GRN}$VERSION${RST}"

# Check if key env vars are set
if [ -z "$TELEGRAM_BOT_TOKEN" ] || [ "$TELEGRAM_BOT_TOKEN" = "your-bot-token-from-botfather" ]; then
    echo -e "${RED}  ⚠  TELEGRAM_BOT_TOKEN not set!${RST}"
    echo "     Edit ~/.bashrc and add your token"
fi
if [ -z "$OPENCODE_GO_API_KEY" ] || [ "$OPENCODE_GO_API_KEY" = "sk-your-opencode-api-key" ]; then
    echo -e "${RED}  ⚠  OPENCODE_GO_API_KEY not set!${RST}"
    echo "     Edit ~/.bashrc and add your key"
fi

echo ""
echo -e "${GRN}╔═══════════════════════════════════════╗${RST}"
echo -e "${GRN}║        ✅ Setup Complete!             ║${RST}"
echo -e "${GRN}╚═══════════════════════════════════════╝${RST}"
echo ""
echo "To start Hermes gateway:"
echo "  hermes gateway run --accept-hooks"
echo ""
echo "For 24/7 auto-restart mode:"
echo "  cd && while true; do hermes gateway run --accept-hooks --replace; sleep 5; done"
echo ""
