#!/data/data/com.termux/files/usr/bin/bash
# ==============================================
# Termux:Boot — Hermes Autostart
# ==============================================
# Place in: ~/.termux/boot/hermes-gateway
# Make executable: chmod +x ~/.termux/boot/hermes-gateway
#
# This script runs automatically ~10 seconds
# after your phone boots (requires Termux:Boot).
# ==============================================

# ── Wait for network & Termux init ──
sleep 10

# ── Prevent phone from sleeping Termux ──
if command -v termux-wake-lock &>/dev/null; then
    termux-wake-lock
fi

# ── Go home ──
cd /data/data/com.termux/files/home || exit 1

# ── Load environment ──
export HERMES_ACCEPT_HOOKS=1

# Source credentials from .bashrc
if [ -f "$HOME/.bashrc" ]; then
    source "$HOME/.bashrc"
fi

# ── Start gateway with auto-restart ──
while true; do
    hermes gateway run --accept-hooks --replace
    sleep 5
done
