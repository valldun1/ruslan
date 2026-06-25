#!/data/data/com.termux/files/usr/bin/bash
# ==============================================
# HyperOS / MIUI Background Process Fix
# ==============================================
# Run from ADB (host machine) or directly in Termux.
# Prevents the phone from killing Hermes when:
#   - Screen turns off
#   - USB is unplugged
#   - Phone goes to sleep
# ==============================================

RED='\033[0;31m'
GRN='\033[0;32m'
YLW='\033[1;33m'
RST='\033[0m'

# ── Check if running inside Termux or via ADB ──
if [ -d /data/data/com.termux ]; then
    # Running in Termux
    RUN=""
    echo -e "${YLW}Running inside Termux — some commands need ADB from a host computer${RST}"
else
    # Running from ADB
    RUN="adb shell"
    echo -e "${GRN}Running via ADB from host${RST}"
fi

echo ""
echo -e "${CYN}╔═══════════════════════════════════════╗${RST}"
echo -e "${CYN}║    HyperOS / MIUI — Background Fix    ║${RST}"
echo -e "${CYN}╚═══════════════════════════════════════╝${RST}"
echo ""

# ── 1. Disable MIUI Optimization (CRITICAL) ──
echo -e "${YLW}[1/4] Disabling MIUI Optimization...${RST}"
echo -e "  ${RED}MANUAL STEP (on your phone):${RST}"
echo "  Settings → Developer Options → MIUI Optimization → OFF"
echo "  (If you can't find it, search 'MIUI Optimization' in Settings)"
echo ""

# ── 2. Disable APK verification ──
echo -e "${YLW}[2/4] Disabling APK verification...${RST}"
$RUN settings put global verifier_verify_adb_installs 0
$RUN settings put secure install_non_market_apps 1
echo -e "${GRN}  ✔ APK verification disabled${RST}"
echo ""

# ── 3. Deviceidle whitelist (prevent doze kill) ──
echo -e "${YLW}[3/4] Adding Termux to deviceidle whitelist...${RST}"
$RUN cmd deviceidle whitelist +com.termux
$RUN appops set com.termux RUN_ANY_IN_BACKGROUND allow
$RUN appops set com.termux RUN_IN_BACKGROUND allow
echo -e "${GRN}  ✔ Termux whitelisted from doze${RST}"
echo ""

# ── 4. Verify ──
echo -e "${YLW}[4/4] Verifying...${RST}"
if [ -n "$RUN" ]; then
    echo "  Deviceidle whitelist:"
    $RUN dumpsys deviceidle whitelist | grep termux || echo "  (not found in whitelist)"
fi
echo ""

echo -e "${GRN}╔═══════════════════════════════════════╗${RST}"
echo -e "${GRN}║     ✅ Fix applied!                    ║${RST}"
echo -e "${GRN}╚═══════════════════════════════════════╝${RST}"
echo ""
echo "Next: Make sure your boot script has termux-wake-lock:"
echo "  mkdir -p ~/.termux/boot"
echo "  # Copy the boot script from services/boot-script.sh"
echo ""
