#!/bin/sh
# use to open script - nano /home/vinay/.xinitrc.

# ---------- Prevent screen blank ----------

set -e

# Disable DPMS (Energy Star) features so the screen doesn't power down.
xset -dpms

# Disable the screen saver.
xset s off

# Disable screen blanking.
xset s noblank

# ---------- Launch Hotstar Kiosk ----------

openbox &

sleep 2

exec chromium \
  --kiosk \
  --noerrdialogs \
  --disable-infobars \
  --disable-session-crashed-bubble \
  --disable-translate \
  --disable-features=TranslateUI \
  --start-fullscreen \
  --no-sandbox \
  --disable-gpu \
  --disable-dev-shm-usage \
  --disable-background-networking \
  --disable-sync \
  --no-first-run \
  --fast-start \
  https://www.hotstar.com/in/onboarding/device-restriction?ref=%2Fin%2Fmypage # URL to open on startup
  https://www.youtube.com/results?search_query=abp+maza+live+
  https://www.google.com

