from flask import Flask, render_template_string, request
from pynput.mouse import Controller as MouseController, Button
from pynput.keyboard import Controller as KeyboardController, Key

class Remote:
    def __init__(self):
        self.app = Flask(__name__)
        self.mouse = MouseController()
        self.keyboard = KeyboardController()

        # HTML template for the control interface
        self.HTML_TEMPLATE = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Remote Mouse & Keyboard</title>
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
                .button-grid {
                    display: grid;
                    grid-template-columns: 1fr 1fr 1fr;
                    gap: 10px;
                    justify-content: center;
                    align-items: center;
                }
                .button-grid button {
                    width: 100%;
                    padding: 15px;
                    font-size: 18px;
                    border: none;
                    background-color: #5E17EB;
                    color: white;
                    border-radius: 5px;
                    cursor: pointer;
                }
                .button-grid button:hover {
                    background-color: rgb(82, 17, 212);
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
            </style>
            <script>
                function sendAction(action, data = "") {
                    fetch("/action", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ action, data })
                    });
                }
                function shutdownServer() {
                    fetch("/shutdown", { method: "POST" });
                }
            </script>
        </head>
        <body>
            <div class="container">
                <h2>Remote Mouse & Keyboard</h2>
                <div class="button-grid">
                    <div></div>
                    <button onclick="sendAction('move_up')">Move Up</button>
                    <div></div>
                    <button onclick="sendAction('move_left')">Move Left</button>
                    <button onclick="sendAction('move_down')">Move Down</button>
                    <button onclick="sendAction('move_right')">Move Right</button>
                </div>
                <h2></h2>
                <button onclick="sendAction('click')">Left Click</button>
                <button onclick="sendAction('right_click')">Right Click</button>
                <button onclick="sendAction('scroll_up')">Scroll Up</button>
                <button onclick="sendAction('scroll_down')">Scroll Down</button>
                <input type="text" id="key" placeholder="Type">
                <button onclick="sendAction('type', document.getElementById('key').value)">Type</button>
                <h2></h2>
                <h2></h2>
                <button onclick="shutdownServer()">Turn Off Server</button>
            </div>
        </body>
        </html>
        """

        # Register routes
        self.app.add_url_rule("/", "index", self.index)
        self.app.add_url_rule("/action", "action", self.action, methods=["POST"])
        self.app.add_url_rule("/shutdown", "shutdown", self.shutdown, methods=["POST"])

    def index(self):
        return render_template_string(self.HTML_TEMPLATE)

    def action(self):
        data = request.get_json()
        action = data.get("action")
        key_data = data.get("data", "")
            
        if action == "move_up":
            x, y = self.mouse.position
            self.mouse.position = (x, y - 20)
        elif action == "move_down":
            x, y = self.mouse.position
            self.mouse.position = (x, y + 20)
        elif action == "move_left":
            x, y = self.mouse.position
            self.mouse.position = (x - 20, y)
        elif action == "move_right":
            x, y = self.mouse.position
            self.mouse.position = (x + 20, y)
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
        """Shuts down the Flask server."""
        shutdown_func = request.environ.get("werkzeug.server.shutdown")
        if shutdown_func:
            shutdown_func()
        return "Shutting down server..."

    def run(self):
        self.app.run(host="0.0.0.0", port=5000, debug=True)

if __name__ == "__main__":
    remote = Remote()
    remote.run()
