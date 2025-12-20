
# Raspberry Pi Hotstar Chromium Kiosk with GPIO Shutdown / Reboot Button

This document is a **complete, start-to-finish installation guide**.
Follow it **line by line** on a freshly flashed Raspberry Pi OS and the kiosk will work exactly as intended.

---

## 0. What This Setup Does (Read This Once)

After installation:

* Raspberry Pi boots **directly into Chromium kiosk**
* **No desktop, no LXDE, no lightdm**
* Hotstar opens automatically in full screen
* HDMI audio is forced and stable
* A **single GPIO button** works as:

  * **Short press** → shutdown
  * **Long press (≥1s)** → reboot

---

## 1. Hardware Required

* Raspberry Pi (3 / 4 / 5)
* microSD card (16 GB or more)
* HDMI display (TV or monitor)
* HDMI cable
* Internet connection (Wi-Fi or Ethernet)
* Momentary push button
* 2 jumper wires

### Button Wiring (IMPORTANT)

* One side of button → **GPIO3** (BCM 3, physical pin **5**)
* Other side of button → **GND** (any ground pin)

GPIO3 is used intentionally because it can also wake the Pi on some models.

---

## 2. Flash the Operating System (Fresh Start)

1. Download **Raspberry Pi Imager**
2. Flash **Raspberry Pi OS (32-bit)**
   (Lite or Full both work)
3. In Imager **Advanced Settings**:

   * Set **username** (example used below: `vinay`)
   * Set password
   * Enable **SSH**
   * Configure Wi-Fi (optional)
4. Flash SD card
5. Insert SD card into Pi and boot

---

## 3. First Boot – Basic Setup

### 3.1 Login

If using monitor + keyboard:

* Login with the username you created (example: `vinay`)

If using SSH:

```bash
ssh vinay@<PI_IP_ADDRESS>
```

---

### 3.2 Update System (Do Not Skip)

```bash
sudo apt update
sudo apt full-upgrade -y
sudo reboot
```

Login again after reboot.

---

## 4. Install Required Packages

Install **only what is needed** for kiosk + GPIO.

```bash
sudo apt install -y \
chromium \
xserver-xorg \
xinit \
python3 \
python3-rpi.gpio
```

Reboot after installation:

```bash
sudo reboot
```

---

## 5. Configure Kiosk Startup (X + Chromium)

### 5.1 Create `~/.xinitrc`

This file starts Chromium in kiosk mode.

```bash
nano ~/.xinitrc
```

Paste the **full script exactly file we have**:


Save and exit:

* `Ctrl + O` → Enter
* `Ctrl + X`

Make executable:

```bash
chmod +x ~/.xinitrc
```


### 5.2 Auto-start X on tty1

Create the profile script:

```bash
sudo nano /etc/profile.d/kiosk.sh
```

Paste the **full script exactly file we have**:

Save and exit.

Make executable:

```bash
sudo chmod +x /etc/profile.d/kiosk.sh
```


## 6. Disable Desktop Completely (No GUI)

This ensures **no LXDE / no desktop loads ever**.

```bash
sudo systemctl disable --now lightdm
sudo systemctl set-default multi-user.target
```

---

## 7. Force HDMI Audio at Boot

Edit boot config:

```bash
sudo nano /boot/firmware/config.txt
```

Scroll to the **bottom** and add:

Paste the **full script exactly file we have**:

Save and exit.

---

## 8. GPIO Shutdown / Reboot Button

### 8.1 Create the Python Script

```bash
nano /home/vinay/gpio-shutdown.py
```

Paste the **full script exactly file we have**:

Make executable:

```bash
chmod +x /home/vinay/gpio-shutdown.py
```

---

### 8.2 Create systemd Service

```bash
sudo nano /etc/systemd/system/gpio-powerbutton.service
```

Paste the **full script exactly file we have**:


Enable service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable gpio-powerbutton.service
sudo systemctl start gpio-powerbutton.service
```

Verify:

```bash
systemctl status gpio-powerbutton.service
```

---

## 9. Final Reboot (Critical Step)

```bash
sudo reboot
```

---

## 10. Expected Boot Behavior (Checklist)

✔ No desktop
✔ No login screen
✔ Screen flashes once
✔ Chromium opens full screen
✔ Hotstar loads
✔ HDMI audio works
✔ Short button press → shutdown
✔ Long button press → reboot

If **any one of these fails**, recheck the step above it.

---

## 11. Notes for Future You (Read This)

* Username `vinay` is **hard-coded** in paths
  → If username changes, update:

  * `/home/vinay/gpio-shutdown.py`
  * `gpio-powerbutton.service`
* Do **not** enable lightdm again
* Do **not** install random desktop packages
* Keep this README with the project — it is the source of truth

---

## Done

This setup is **deliberate, minimal, and stable**.
If you reflash the OS, follow this README **top to bottom** and it will work again without debugging.

---

If you want, next we can:

* add a **boot troubleshooting section**
* add **GPIO wiring diagram**
* add **versioned changelog**
* add **one-command install script**

Just say the word.





STEP 1 — Create project folder
mkdir -p /home/vinay/kiosk-control/templates
mkdir -p /home/vinay/kiosk-control/static

STEP 2 — Create virtual environment
cd /home/vinay/kiosk-control
python3 -m venv kiosk-venv


Activate it:

source kiosk-venv/bin/activate

pip install flask requests
pip install websocket-client
sudo apt install xdotool -y

STEP 3 — Create app.py
sudo nano /home/vinay/kiosk-control/app.py

STEP 4 — Create index.html
sudo nano /home/vinay/kiosk-control/templates/index.html

STEP 5 — Create style.css
sudo nano /home/vinay/kiosk-control/static/style.css


STEP 6 — Run the server

Activate virtual env:

cd /home/vinay/kiosk-control
source kiosk-venv/bin/activate
python3 app.py
