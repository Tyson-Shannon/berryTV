from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import sys
import os
import subprocess

SERVICE_NAME = "berryTV"
SERVICE_PATH = f"/etc/systemd/system/{SERVICE_NAME}.service"
PYTHON_EXEC = "/usr/bin/python3"
SCRIPT_PATH = os.getcwd()+"Main.py"  



class settings(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Settings")
        self.setGeometry(200, 200, 300, 200)
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.label = QLabel("Checking startup status...", self)
        self.button = QPushButton("Open On Startup", self)
        self.button.clicked.connect(self.toggle_startup)

        layout = QVBoxLayout()
        #exit button
        self.close_button = QPushButton("X", self) 
        self.close_button.setGeometry(5, 5, 30, 30)
        self.close_button.clicked.connect(self.close)

        layout.addWidget(self.label)
        layout.addWidget(self.button)

        self.setLayout(layout)

        self.update_status()

    def is_service_enabled(self):
        """Check if the systemd service is enabled."""
        try:
            result = subprocess.run(
                ["systemctl", "is-enabled", SERVICE_NAME],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            return result.stdout.strip() == "enabled"
        except Exception as e:
            return False

    def enable_startup(self):
        """Create and enable the systemd service for startup."""
        service_content = f"""[Unit]
Description=Auto-start Python App
After=network.target

[Service]
ExecStart={PYTHON_EXEC} {SCRIPT_PATH}
Restart=always
User={os.getlogin()}

[Install]
WantedBy=multi-user.target
"""

        try:
            # Ensure we're running with sudo
            if os.geteuid() != 0:
                self.label.setText("Please run with sudo!")
                return

            # Write the service file
            with open(SERVICE_PATH, "w") as f:
                f.write(service_content)

            # Set correct permissions for the service file
            subprocess.run(["sudo", "chmod", "644", SERVICE_PATH])

            # Reload systemd, enable and start the service persistently
            subprocess.run(["sudo", "systemctl", "daemon-reload"])
            subprocess.run(["sudo", "systemctl", "enable", SERVICE_NAME])
            subprocess.run(["sudo", "systemctl", "start", SERVICE_NAME])

            self.label.setText("Startup Enabled")

        except Exception as e:
            self.label.setText(f"Error enabling startup: {e}")

    def disable_startup(self):
        """Disable and remove the systemd service."""
        try:
            subprocess.run(["sudo", "systemctl", "disable", SERVICE_NAME])
            subprocess.run(["sudo", "systemctl", "stop", SERVICE_NAME])
            os.remove(SERVICE_PATH)  # Remove service file
            subprocess.run(["sudo", "systemctl", "daemon-reload"])
        except Exception as e:
            self.label.setText(f"Error disabling startup: {e}")

    def toggle_startup(self):
        """Toggle startup enable/disable based on current status."""
        if self.is_service_enabled():
            self.disable_startup()
            self.label.setText("Startup Disabled")
        else:
            self.enable_startup()
            self.label.setText("Startup Enabled")

    def update_status(self):
        """Update label text based on startup status."""
        if self.is_service_enabled():
            self.label.setText("Startup Enabled")
        else:
            self.label.setText("Startup Disabled") 

        