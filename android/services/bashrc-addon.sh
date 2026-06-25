# ==============================================
# .bashrc Addon — for Hermes Auto-Start
# ==============================================
# Append this to your ~/.bashrc file.
# It sets up API keys and auto-starts Hermes
# whenever you open Termux.
# ==============================================

# ── Hermes On Android — Environment ──

# >>> 🔑 YOU MUST EDIT THESE ← YOUR REAL VALUES <<<
export OPENCODE_GO_API_KEY="sk-your-opencode-api-key"
export TELEGRAM_BOT_TOKEN="your-bot-token-from-botfather"
export TELEGRAM_ALLOWED_USERS="your-telegram-user-id"
# >>>   ↑↑↑ REPLACE WITH YOUR REAL VALUES ↑↑↑   <<<

# Optional: Groq key for STT (voice messages)
export GROQ_API_KEY="gsk_your-groq-api-key"

# Tell Hermes it can run hooks
export HERMES_ACCEPT_HOOKS=1

# ── Auto-start gateway (with delay for Termux init) ──
start-hermes() {
    cd ~
    while true; do
        echo "[$(date)] Starting Hermes gateway..."
        hermes gateway run --accept-hooks --replace 2>&1
        echo "[$(date)] Gateway died, restarting in 5s..."
        sleep 5
    done
}

# Launch in background after 10 seconds
(sleep 10 && start-hermes &) & disown
