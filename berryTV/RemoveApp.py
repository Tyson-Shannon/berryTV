from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class removeApp(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add App")
        self.setGeometry(200, 200, 300, 200)
        self.setWindowFlags(Qt.FramelessWindowHint)

        layout = QVBoxLayout()

        #close button
        self.close_button = QPushButton("X")
        self.close_button.setFixedSize(30, 30)
        self.close_button.clicked.connect(self.close)
        layout.addWidget(self.close_button)
        #pick app
        self.browserLabel = QLabel("Pick App", self)
        layout.addWidget(self.browserLabel)
        self.combobox = QComboBox()
        self.combobox.addItems(self.get_available_apps())
        layout.addWidget(self.combobox)
        #ok button
        self.okButton = QPushButton("Remove", self)
        self.okButton.clicked.connect(self.remove_app)
        layout.addWidget(self.okButton)

        self.setLayout(layout)

    def get_available_apps(self):
        #list of apps in Database.txt
        apps = []
        with open("Database.txt", "r") as f:
            data = f.readlines()
            f.close() 
        data = [line.strip() for line in data]
        for line in data:
            apps.append(line)
        return apps

    def remove_app(self):
        #rewrite Database.txt without picked app
        remove = self.combobox.currentText()
        with open("Database.txt", "r") as f:
            lines = f.readlines()
            f.close()
        with open("Database.txt", "w") as f:
            for line in lines:
                if line.strip() != remove:
                    f.write(line)
            f.close()
        self.close()