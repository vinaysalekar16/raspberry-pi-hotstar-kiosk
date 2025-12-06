#!/bin/bash
# This script runs at login (for interactive shells).
# We use it to start X (graphical session) automatically on tty1.

# Check if the current terminal is /dev/tty1
if [ "$(tty)" = "/dev/tty1" ]; then
    # If yes, launch the X server and run ~/.xinitrc
    startx
fi
