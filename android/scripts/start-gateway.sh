#!/data/data/com.termux/files/usr/bin/bash
# ==============================================
# Hermes Gateway — Production Auto-Restart Loop
# ==============================================
# Use this as the actual entry point for Hermes.
# It auto-restarts the gateway if it crashes.
#
# Start manually:   bash start-gateway.sh
# Or use .bashrc:   (sleep 10 && bash start-gateway.sh) &
# ==============================================

# ── Config ──
RESTART_DELAY=5        # seconds between restart attempts
MAX_RESTARTS=0         # 0 = infinite restarts
LOG_FILE="$HOME/hermes-gateway.log"

# ── Source .bashrc (API keys) ──
if [ -f "$HOME/.bashrc" ]; then
    source "$HOME/.bashrc"
fi

# ── Wake lock (prevent Termux from sleeping) ──
if command -v termux-wake-lock &>/dev/null; then
    termux-wake-lock
    echo "[$(date)] Wake lock acquired" >> "$LOG_FILE"
fi

# ── Restart counter ──
RESTART_COUNT=0

cd "$HOME"
echo "[$(date)] Hermes Gateway starting..." >> "$LOG_FILE"
echo "==========================================" >> "$LOG_FILE"

while true; do
    echo "[$(date)] Starting gateway (attempt $((RESTART_COUNT + 1)))..." | tee -a "$LOG_FILE"
    
    # ── Run gateway ──
    hermes gateway run --accept-hooks --replace 2>&1 | tee -a "$LOG_FILE"
    EXIT_CODE=$?
    
    echo "[$(date)] Gateway exited with code $EXIT_CODE" | tee -a "$LOG_FILE"
    
    # ── Check if we should stop ──
    if [ "$MAX_RESTARTS" -gt 0 ] && [ "$RESTART_COUNT" -ge "$MAX_RESTARTS" ]; then
        echo "[$(date)] Max restarts ($MAX_RESTARTS) reached. Stopping." | tee -a "$LOG_FILE"
        break
    fi
    
    RESTART_COUNT=$((RESTART_COUNT + 1))
    
    # ── Wait before restart ──
    echo "[$(date)] Restarting in ${RESTART_DELAY}s..." | tee -a "$LOG_FILE"
    sleep "$RESTART_DELAY"
done
