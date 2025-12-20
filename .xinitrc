#!/bin/sh
# use to open script - nano /home/vinay/.xinitrc.

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
exec chromium --kiosk \                           # Full-screen kiosk mode (no window decorations)
  --remote-debugging-port=9222 \
  --remote-allow-origins=http://127.0.0.1:9222 \
  --noerrdialogs \                    # Suppress error dialogs
  --disable-infobars \                # Hide 'Chrome is being controlled' info bar
  --disable-features=TranslateUI \    # Disable built-in translate popup
  --start-maximized \                 # Start maximized (for safety with kiosk)
  --disable-features=MediaEngagementBypassAutoplayPolicies,MediaSessionService,PreloadMediaEngagementData \
  --autoplay-policy=document-user-activation-required \     # Control autoplay policy
  --disable-background-media-suspend \                      # Keep media running in background
  --disable-backgrounding-occluded-windows \                # Prevent throttling when window not visible
  --disable-features=MediaSessionService \                # Disable certain media session features
  --site-per-process \
 https://www.hotstar.com/in/onboarding/device-restriction?ref=%2Fin%2Fmypage # URL to open on startup
