#!/usr/bin/env python3
# Use Python 3 interpreter located by env.

import RPi.GPIO as GPIO      # Library to control Raspberry Pi GPIO pins
import time                  # For tracking button press duration
import threading             # To run shutdown/reboot without blocking main loop
import subprocess            # To execute system commands (shutdown, reboot)

# GPIO pin number (BCM numbering) where the button is connected.
BUTTON = 3  # Single button on GPIO3 (PIN 5)

# Disable GPIO warnings (useful if script restarts and pins are already in use).
GPIO.setwarnings(False)

# Use BCM numbering (GPIO numbers, not physical pin numbers).
GPIO.setmode(GPIO.BCM)

# Configure the button pin as input with an internal pull-up resistor.
# This means: unpressed = HIGH, pressed = LOW (connected to GND).
GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Thresholds for interpreting button press length.
REBOOT_PRESS   = 1.0   # Seconds: long press → reboot
SHUTDOWN_PRESS = 0.3   # Seconds: short press → shutdown (used for info)

# Variables to track state of button press.
press_start = None      # Time when button was pressed down
action_fired = False    # To prevent both shutdown and reboot from firing

# ---- REAL ACTIONS ----

def do_shutdown():
    """
    Perform system shutdown (halt).
    Runs 'sudo shutdown -h now'.
    """
    subprocess.run(["sudo", "shutdown", "-h", "now"])

def do_reboot():
    """
    Perform system reboot.
    Runs 'sudo reboot'.
    """
    subprocess.run(["sudo", "reboot"])

# ---- FALLING EDGE: BUTTON PRESSED ----

def handle_press(channel):
    """
    Callback that runs when the button is pressed (falling edge).
    Records the start time of the press and resets action_fired flag.
    """
    global press_start, action_fired
    # Confirm the button is actually LOW (pressed).
    if GPIO.input(BUTTON) == 0:
        press_start = time.time()  # Record the time when button was pressed
        action_fired = False       # Allow an action to be fired for this press

# Detect falling edge (HIGH -> LOW) on the button pin.
# When button is pressed, call handle_press.
# bouncetime=50 helps to ignore mechanical noise (debouncing).
GPIO.add_event_detect(BUTTON, GPIO.FALLING, callback=handle_press, bouncetime=50)

# ---- MAIN LOOP ----

try:
    # Run forever until the script is stopped.
    while True:
        # If a press has started AND the button is still being held down:
        if press_start is not None and GPIO.input(BUTTON) == 0:

            # Calculate how long the button has been pressed.
            press_duration = time.time() - press_start

            # LONG PRESS → REBOOT (triggers immediately when threshold reached)
            if press_duration >= REBOOT_PRESS and not action_fired:
                action_fired = True  # Mark action as fired to avoid double trigger
                # Run reboot in a separate thread so the loop isn't blocked.
                threading.Thread(target=do_reboot, daemon=True).start()

        # If the button was pressed before but is now released:
        elif press_start is not None and GPIO.input(BUTTON) == 1:

            # Calculate total press duration.
            press_duration = time.time() - press_start

            # SHORT PRESS → SHUTDOWN
            # Only run if no long-press action already executed.
            if not action_fired:
                threading.Thread(target=do_shutdown, daemon=True).start()

            # Reset state for next press.
            press_start = None
            action_fired = False

        # Small sleep to reduce CPU usage.
        time.sleep(0.01)

# When script is stopped with Ctrl+C, clean up GPIO state.
except KeyboardInterrupt:
    GPIO.cleanup()
