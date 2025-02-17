from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import webbrowser

class addApp(QDialog):
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
        #set app name
        self.nameLabel = QLabel("Name of App", self)
        layout.addWidget(self.nameLabel)
        self.nameInput = QLineEdit(self)
        layout.addWidget(self.nameInput)
        #URL/File?
        self.radioGroup = QButtonGroup(self)
        self.radio_url = QRadioButton("URL")
        self.radio_file = QRadioButton("File")
        self.radioGroup.addButton(self.radio_url)
        self.radioGroup.addButton(self.radio_file)
        radio_layout = QHBoxLayout()
        radio_layout.addWidget(self.radio_url)
        radio_layout.addWidget(self.radio_file)
        layout.addLayout(radio_layout)
        #pick browser (disabled by default)
        self.browserLabel = QLabel("Pick Browser", self)
        layout.addWidget(self.browserLabel)
        self.combobox = QComboBox()
        self.combobox.addItems(self.get_available_browsers())
        self.combobox.setEnabled(False)
        layout.addWidget(self.combobox)
        #input field (disabled by default)
        self.inputField = QLineEdit()
        self.inputField.setPlaceholderText("Enter URL or select a file...")
        self.inputField.setEnabled(False)
        layout.addWidget(self.inputField)
        #file picker button (hidden by default)
        self.fileButton = QPushButton("Select File")
        self.fileButton.setEnabled(False)
        self.fileButton.clicked.connect(self.select_file)
        layout.addWidget(self.fileButton)
        #connect radio buttons to enable input field
        self.radio_url.toggled.connect(self.toggle_input)
        self.radio_file.toggled.connect(self.toggle_input)
        #ok button
        self.okButton = QPushButton("Add", self)
        self.okButton.clicked.connect(self.add_app)
        layout.addWidget(self.okButton)

        self.setLayout(layout)

    def get_available_browsers(self):
        #Get available browsers
        browsers = []
        for browser in ["chrome", "firefox", "safari", "opera", "edge"]:
            try:
                if webbrowser.get(browser):
                    browsers.append(browser)
            except webbrowser.Error:
                pass
        return browsers if browsers else ["Default"]
    
    def toggle_input(self):
        #Enable/Disable input field based on selection
        if self.radio_url.isChecked():
            self.inputField.setEnabled(True)
            self.fileButton.setEnabled(False)
            self.combobox.setEnabled(True)
        elif self.radio_file.isChecked():
            self.inputField.setEnabled(True)
            self.fileButton.setEnabled(True)
            self.combobox.setEnabled(False)
    
    def select_file(self):
        #Open file dialog to select a file
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*)")
        if file_path:
            self.inputField.setText(file_path)


    def add_app(self):
        #add data to Database.txt
        name = self.nameInput.text()
        browser = self.combobox.currentText()
        location = self.inputField.text()
        inputType = "URL" if self.radio_url.isChecked() else "File"
        with open("Database.txt", "a") as f:
            f.write(name+", "+browser+", "+location+", "+inputType+"\n")
            f.close()
        self.close()