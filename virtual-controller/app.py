#FilePath /home/vinay/kiosk-control/app.py

from flask import Flask, request, send_from_directory
import subprocess
import requests
import json
import websocket

app = Flask(__name__)

CHROME_DEBUG = "http://127.0.0.1:9222/json"

# ---------------- UI ----------------

@app.route("/")
def index():
    return send_from_directory("templates", "index.html")

# ---------------- NAVIGATION ----------------
def get_active_tab():
    tabs = requests.get(CHROME_DEBUG, timeout=2).json()
    for tab in tabs:
        if tab.get("type") == "page":
            return tab["webSocketDebuggerUrl"]
    return None

def devtools_navigate(url):
    ws_url = get_active_tab()
    if not ws_url:
        return False

    ws = websocket.create_connection(ws_url)
    ws.send(json.dumps({
        "id": 1,
        "method": "Page.navigate",
        "params": {"url": url}
    }))
    ws.close()
    return True

@app.route("/navigate")
def navigate():
    url = request.args.get("url")
    if not url:
        return "No URL", 400

    if not url.startswith("http"):
        url = "https://" + url

    ok = devtools_navigate(url)
    return "OK" if ok else ("No Tab", 500)

@app.route("/reload")
def reload_page():
    devtools_navigate("javascript:location.reload()")
    return "OK"

# ---------------- MOUSE ----------------

@app.route("/mouse_move", methods=["POST"])
def mouse_move():
    data = request.get_json(force=True)
    dx = int(data.get("dx", 0))
    dy = int(data.get("dy", 0))
    subprocess.call(["xdotool", "mousemove_relative", "--", str(dx), str(d>
    return "OK"

@app.route("/mouse_click", methods=["POST"])
def mouse_click():
    subprocess.call(["xdotool", "click", "1"])
    return "OK"

@app.route("/scroll", methods=["POST"])
def scroll():
    data = request.get_json(force=True)
    dy = int(data.get("dy", 0))
    key = "Down" if dy > 0 else "Up"
    for _ in range(abs(dy) // 30 + 1):
        subprocess.call(["xdotool", "key", key])
    return "OK"

# ---------------- PLAYER CONTROLS ----------------

@app.route("/left")
def left():
    subprocess.call(["xdotool", "key", "Left"])
    return "OK"

@app.route("/right")
def right():
    subprocess.call(["xdotool", "key", "Right"])
    return "OK"

@app.route("/playpause")
def playpause():
    subprocess.call(["xdotool", "key", "space"])
    return "OK"

@app.route("/volup")
def volup():
    subprocess.call(["xdotool", "key", "Up"])
    return "OK"

@app.route("/voldown")
def voldown():
    subprocess.call(["xdotool", "key", "Down"])
    return "OK"

@app.route("/back")
def back():
    subprocess.call(["xdotool", "key", "Escape"])
    return "OK"

# ---------------- SYSTEM ----------------

@app.route("/reboot")
def reboot():
    subprocess.call(["sudo", "reboot"])
    return "OK"

@app.route("/shutdown")
def shutdown():
    subprocess.call(["sudo", "shutdown", "-h", "now"])
    return "OK"

# ---------------- START ----------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
