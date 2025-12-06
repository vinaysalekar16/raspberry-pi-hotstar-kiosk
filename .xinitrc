#!/bin/sh
# Use /bin/sh as the shell to run this script.

# ---------- Prevent screen blank ----------

# Disable DPMS (Energy Star) features so the screen doesn't power down.
xset -dpms

# Disable the screen saver.
xset s off

# Disable screen blanking.
xset s noblank

# ---------- Launch Hotstar Kiosk ----------

# Start Chromium in full-screen kiosk mode and open Hotstar home.
# "exec" replaces the current shell with chromium-browser process.
exec chromium \
  --kiosk \                           # Full-screen kiosk mode (no window decorations)
  --noerrdialogs \                    # Suppress error dialogs
  --disable-infobars \                # Hide 'Chrome is being controlled' info bar
  --disable-features=TranslateUI \    # Disable built-in translate popup
  --start-maximized \                 # Start maximized (for safety with kiosk)
  --autoplay-policy=document-user-activation-required \     # Control autoplay policy
  --disable-background-media-suspend \                      # Keep media running in background
  --disable-backgrounding-occluded-windows \                # Prevent throttling when window not visible
  --disable-features=MediaSessionService \                # Disable certain media session features
  https://www.hotstar.com/in/home # URL to open on startup
