
# Raspberry Pi Hotstar Chromium Kiosk + GPIO Power Button

This project turns a Raspberry Pi into a **full-screen Hotstar kiosk** that:

- Boots **directly into Chromium kiosk** (no desktop, no LXDE)
- Uses **HDMI for audio**, forced at boot
- Starts **Hotstar automatically** in full-screen
- Uses a **single GPIO button**:
  - **Short press** → shutdown
  - **Long press** → reboot
- Runs the GPIO logic as a **systemd service**

---

## 1. Hardware Requirements

- Raspberry Pi (3/4/5 recommended)
- MicroSD card with Raspberry Pi OS (Lite or Full)
- HDMI monitor or TV
- HDMI cable
- One **momentary push button**
- Button wiring:
  - One side → **GPIO3** (BCM 3, physical pin 5)
  - Other side → **GND** (any ground pin)

Note: GPIO3 is convenient because it can also wake the Pi from halt on some models.

---

## 2. Software Requirements

- Raspberry Pi OS with:
  - `chromium-browser`
  - `xserver-xorg`, `xinit`
- Python 3
- `python3-rpi.gpio` package

Install typical dependencies:

```bash
sudo apt update
sudo apt install -y chromium-browser xserver-xorg xinit python3-rpi.gpio
