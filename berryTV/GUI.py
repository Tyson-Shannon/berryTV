from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import webbrowser
import subprocess
import os

import Settings
import AddApp
import RemoveApp

class window(QMainWindow):
   def __init__(self, parent = None):
      #main screen
      super(window, self).__init__(parent)
      self.setWindowTitle("berryTV")
      self.setStyleSheet("background-color: #FFFFFF;") 

      # Set main widget
      central_widget = QWidget()
      self.setCentralWidget(central_widget)
      layout = QVBoxLayout(central_widget)

      #top bar
      tb = self.addToolBar("Tool Bar")
      tb.setStyleSheet("background-color: #5E17EB;")
      tb.setIconSize(QSize(50, 50))
      tb.setMovable(False)
      tb.setFloatable(False)
      #title display
      self.title_label = QLabel()
      title_font = QFont("Classic Console", 30)
      self.title_label.setFont(title_font) 
      self.title_label.setStyleSheet("color: #FFFFFF;")
      tb.addWidget(self.title_label)
      self.title_label.setText("berryTV")
      #time display
      self.time_label = QLabel()
      time_font = QFont("Arial", 20)
      self.time_label.setFont(time_font) 
      self.time_label.setStyleSheet("color: #FFFFFF;")
      tb.addWidget(self.time_label)
      self.timer = QTimer()
      self.timer.timeout.connect(self.update_time)
      #update every second
      self.timer.start(1000)

      #side bar
      sb = self.addToolBar("Side Bar")
      self.addToolBar(Qt.LeftToolBarArea, sb)
      sb.setStyleSheet("background-color: #5E17EB;")
      sb.setIconSize(QSize(50, 50))
      sb.setMovable(False)
      sb.setFloatable(False)
      #buttons
      add = QAction(QIcon("add.png"), "add app", self)
      sb.addAction(add)
      remove = QAction(QIcon("remove.png"), "remove app", self)#change png
      sb.addAction(remove)
      settings = QAction(QIcon("setting.png"), "settings", self)
      sb.addAction(settings)
      exit = QAction(QIcon("leave.png"), "exit", self)
      sb.addAction(exit)
      sb.actionTriggered[QAction].connect(self.sideBarBut)

      #scrollable Center Area
      self.reel = QStackedWidget()
      self.populate_reel()

      #navigation buttons
      nav_layout = QHBoxLayout()
      self.prev_button = QPushButton("<")
      self.prev_button.setFixedSize(50, 50)
      self.prev_button.setStyleSheet("background-color: #5E17EB; color: white; border-radius: 25px;")
      self.prev_button.clicked.connect(self.prev_item)

      self.next_button = QPushButton(">")
      self.next_button.setFixedSize(50, 50)
      self.next_button.setStyleSheet("background-color: #5E17EB; color: white; border-radius: 25px;")
      self.next_button.clicked.connect(self.next_item)

      nav_layout.addWidget(self.prev_button)
      nav_layout.addWidget(self.reel)
      nav_layout.addWidget(self.next_button)

      layout.addLayout(nav_layout)

      self.setLayout(layout)

   def sideBarBut(self, button):
      #side bar button actions
      if button.text() == "exit":
         self.close()
      if button.text() == "settings":
         self.setWindow = Settings.settings()
         self.setWindow.exec_()
      if button.text() == "remove app":
         self.remWindow = RemoveApp.removeApp()
         self.remWindow.exec_()
      if button.text() == "add app":
         self.addWindow = AddApp.addApp()
         self.addWindow.exec_()
   
   def update_time(self):
      #update time display
      current_time = QTime.currentTime().toString("hh:mm:ss")
      self.time_label.setText(" | "+current_time+" | ")

   def populate_reel(self):
      #add Database.txt apps to the scrolling reel
      with open("Database.txt", "r") as f:
            lines = f.readlines()
            lines.sort()
            f.close()
      for i in range(0, len(lines)):
         app = lines[i].split(", ")
         item_widget = QWidget()
         item_layout = QVBoxLayout(item_widget)
         item_widget.setStyleSheet("background-color: white; border-radius: 10px; padding: 20px;")
         #title
         title = QLabel(app[0])
         title.setAlignment(Qt.AlignCenter)
         title.setStyleSheet("font-size: 20px; font-weight: bold;")

         # Image
         image_label = QLabel()
         pixmap = QPixmap(300, 200)  # Placeholder image
         pixmap.fill(QColor("gray"))  # Gray box for demo
         image_label.setPixmap(pixmap)
         image_label.setAlignment(Qt.AlignCenter)
         image_label.setFixedSize(300, 200)

         #button
         button = QPushButton("Open")
         button.setStyleSheet("background-color: #5E17EB; color: white; padding: 10px; border-radius: 5px;")
         button.clicked.connect(lambda checked: self.scrollButton(app[1], app[2], app[3]))

         # Centering
         item_layout.addWidget(title)
         item_layout.addWidget(image_label)
         item_layout.addWidget(button, alignment=Qt.AlignCenter)

         self.reel.addWidget(item_widget)

   def scrollButton(self, browser, location, type):
      #open URL or File
      if type == "URL\n":
         webbrowser.get(browser).open(location) 
      elif type == "File\n":
         if not os.path.exists(location):
            raise FileNotFoundError(f"File not found: {location}")
         
         try:
               subprocess.Popen([location], shell=True)
         except Exception as e:
            print(f"Error launching file: {e}")
   
   def prev_item(self):
      """Go to the previous item in the reel."""
      current_index = self.reel.currentIndex()
      if current_index > 0:
         self.reel.setCurrentIndex(current_index - 1)

   def next_item(self):
      """Go to the next item in the reel."""
      current_index = self.reel.currentIndex()
      if current_index < self.reel.count() - 1:
         self.reel.setCurrentIndex(current_index + 1)