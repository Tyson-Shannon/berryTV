from flask import Flask, render_template_string, request
from pynput.mouse import Controller as MouseController, Button
from pynput.keyboard import Controller as KeyboardController
import threading

class Remote:
    def __init__(self):
        self.app = Flask(__name__)
        self.mouse = MouseController()
        self.keyboard = KeyboardController()
        self.shutdown_event = threading.Event()

        # HTML template with virtual trackpad
        self.HTML_TEMPLATE = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>berryTV Remote</title>
            <style>
                body {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    background-color: #f4f4f4;
                    margin: 0;
                    font-family: Arial, sans-serif;
                }
                .container {
                    text-align: center;
                    width: 90%;
                    max-width: 400px;
                    background: white;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
                }
                button {
                    width: 100%;
                    padding: 15px;
                    font-size: 18px;
                    border: none;
                    background-color: #5E17EB;
                    color: white;
                    border-radius: 5px;
                    cursor: pointer;
                    margin-top: 10px;
                }
                button:hover {
                    background-color: rgb(82, 17, 212);
                }
                input {
                    width: 100%;
                    padding: 10px;
                    font-size: 16px;
                    margin: 10px 0;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                }
                #trackpad {
                    width: 100%;
                    height: 200px;
                    background: #eee;
                    border: 2px dashed #ccc;
                    border-radius: 10px;
                    margin-bottom: 20px;
                    touch-action: none;
                }
            </style>
            <script>
                function sendAction(action, data = "") {
                    fetch("/action", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ action, data })
                    });
                }

                function typeText() {
                    const input = document.getElementById("key");
                    sendAction("type", input.value);
                    input.value = "";
                }

                // Trackpad logic
                let isTouching = false;
                let lastX = 0;
                let lastY = 0;

                function handleMove(x, y) {
                    if (!isTouching) return;
                    const dx = x - lastX;
                    const dy = y - lastY;
                    if (Math.abs(dx) > 1 || Math.abs(dy) > 1) {
                        sendAction("move", { dx: dx, dy: dy });
                        lastX = x;
                        lastY = y;
                    }
                }

                window.onload = () => {
                    const trackpad = document.getElementById("trackpad");

                    trackpad.addEventListener("mousedown", (e) => {
                        isTouching = true;
                        lastX = e.clientX;
                        lastY = e.clientY;
                    });

                    trackpad.addEventListener("mousemove", (e) => {
                        if (isTouching) handleMove(e.clientX, e.clientY);
                    });

                    trackpad.addEventListener("mouseup", () => {
                        isTouching = false;
                    });

                    trackpad.addEventListener("mouseleave", () => {
                        isTouching = false;
                    });

                    trackpad.addEventListener("touchstart", (e) => {
                        isTouching = true;
                        const touch = e.touches[0];
                        lastX = touch.clientX;
                        lastY = touch.clientY;
                    });

                    trackpad.addEventListener("touchmove", (e) => {
                        const touch = e.touches[0];
                        handleMove(touch.clientX, touch.clientY);
                    });

                    trackpad.addEventListener("touchend", () => {
                        isTouching = false;
                    });
                };
            </script>
        </head>
        <body>
            <div class="container">
                <h2>berryTV Remote</h2>
                <h3>Trackpad</h3>
                <div id="trackpad"></div>
                <button onclick="sendAction('click')">Left Click</button>
                <button onclick="sendAction('right_click')">Right Click</button>
                <button onclick="sendAction('scroll_up')">Scroll Up</button>
                <button onclick="sendAction('scroll_down')">Scroll Down</button>
                <input type="text" id="key" placeholder="Type">
                <button onclick="typeText()">Type</button>
            </div>
        </body>
        </html>
        """

        self.app.add_url_rule("/", "index", self.index)
        self.app.add_url_rule("/action", "action", self.action, methods=["POST"])

    def index(self):
        return render_template_string(self.HTML_TEMPLATE)

    def action(self):
        data = request.get_json()
        action = data.get("action")
        key_data = data.get("data", "")

        if action == "move":
            dx = key_data.get("dx", 0)
            dy = key_data.get("dy", 0)
            x, y = self.mouse.position
            self.mouse.position = (x + dx, y + dy)
        elif action == "click":
            self.mouse.click(Button.left, 1)
        elif action == "right_click":
            self.mouse.click(Button.right, 1)
        elif action == "scroll_up":
            self.mouse.scroll(0, 2)
        elif action == "scroll_down":
            self.mouse.scroll(0, -2)
        elif action == "type" and key_data:
            self.keyboard.type(key_data)

        return "OK"

    def shutdown(self):
        self.shutdown_event.set()
        return "Shutting down server..."

    def run(self):
        server_thread = threading.Thread(target=self._run_server)
        server_thread.start()
        self.shutdown_event.wait()
        print("Remote Flask server shut down.")
        
    def _run_server(self):
        self.app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)

#remove after debug———————————————————————
if __name__ == "__main__":
    remote = Remote()
    remote.run()