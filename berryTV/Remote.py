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
            <script>
                function sendAction(action, data = "") {
                    fetch("/action", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ action, data })
                    });
                }
            </script>
        </head>
        <body>
            <h2>Mouse Control</h2>
            <button onclick="sendAction('move_up')">Move Up</button>
            <button onclick="sendAction('move_down')">Move Down</button>
            <button onclick="sendAction('move_left')">Move Left</button>
            <button onclick="sendAction('move_right')">Move Right</button>
            <button onclick="sendAction('click')">Left Click</button>
            <button onclick="sendAction('right_click')">Right Click</button>
            <button onclick="sendAction('scroll_up')">Scroll Up</button>
            <button onclick="sendAction('scroll_down')">Scroll Down</button>
            
            <h2>Keyboard Control</h2>
            <button onclick="sendAction('show_keyboard')">Show Keyboard</button>
            <button onclick="sendAction('hide_keyboard')">Hide Keyboard</button>
            <input type="text" id="key" placeholder="Type a key">
            <button onclick="sendAction('type', document.getElementById('key').value)">Type</button>
        </body>
        </html>
        """

        # Register routes
        self.app.add_url_rule("/", "index", self.index)
        self.app.add_url_rule("/action", "action", self.action, methods=["POST"])

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
        elif action == "show_keyboard":
            self.keyboard.press(Key.cmd)
            self.keyboard.press(Key.space)
            self.keyboard.release(Key.space)
            self.keyboard.release(Key.cmd)
        elif action == "hide_keyboard":
            self.keyboard.press(Key.esc)
            self.keyboard.release(Key.esc)
            
        return "OK"
    
    def shutdown(self):
        """Gracefully shuts down the Flask server."""
        shutdown_func = request.environ.get("werkzeug.server.shutdown")
        if shutdown_func:
            shutdown_func()
        return "Shutting down server..."

    def run(self):
        self.remote = Remote()
        self.app.run(host="0.0.0.0", port=5000, debug=True)

if __name__ == "__main__":
    remote = Remote()
    remote.run()
