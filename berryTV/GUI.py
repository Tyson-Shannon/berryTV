from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import webbrowser
import subprocess
import os
import socket
import threading

import Settings
import AddApp
import RemoveApp
import Remote

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
      #spacer
      spacer = QWidget()
      spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
      tb.addWidget(spacer)
      #url display for remote
      self.ip_label = QLabel()
      ip_font = QFont("Arial", 20)
      self.ip_label.setFont(ip_font) 
      self.ip_label.setStyleSheet("color: #FFFFFF;")
      tb.addWidget(self.ip_label)
      self.ip_label.setText("Remote: http://"+self.get_local_ip()+":5000")

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
      remove = QAction(QIcon("remove.png"), "remove app", self)
      sb.addAction(remove)
      refresh = QAction(QIcon("refresh.png"), "refresh", self)
      sb.addAction(refresh)
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
         self.remote.shutdown()#shutdown server for remote
         self.close()
      if button.text() == "settings":
         self.setWindow = Settings.settings()
         self.setWindow.exec_()
      if button.text() == "refresh":
         self.reel.close()
         self.reel = QStackedWidget()
         self.populate_reel()
         layout = self.centralWidget().layout()
         layout.itemAt(0).layout().removeWidget(self.reel)
         layout.itemAt(0).layout().insertWidget(1, self.reel)
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
         if app[3] == "URL\n":
            image_location = os.path.join("appImages", f"{app[0]}.png")
            image_label = QLabel()
            pixmap = QPixmap(image_location)
            image_label.setPixmap(pixmap.scaled(800, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            image_label.setAlignment(Qt.AlignCenter)
            layout = QVBoxLayout()
            layout.addWidget(image_label, alignment=Qt.AlignCenter)
         elif app[3] == "File\n":
            image_label = QLabel()
            pixmap = QPixmap("berryLogo.png")
            image_label.setPixmap(pixmap.scaled(800, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            image_label.setAlignment(Qt.AlignCenter)
            layout = QVBoxLayout()
            layout.addWidget(image_label, alignment=Qt.AlignCenter)
         #button
         button = QPushButton("Open")
         button.setStyleSheet("background-color: #5E17EB; color: white; padding: 10px; border-radius: 5px;")
         button.clicked.connect(lambda checked, b=app[1], l=app[2], t=app[3]: self.scrollButton(b, l, t))
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

   def get_local_ip(self):
      # Start Flask server in a new thread
      self.remote = Remote.Remote()
      threading.Thread(target=self.remote.run, daemon=True).start()

      #get ip for the remote control webserver
      s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
      try:
         s.connect(("8.8.8.8", 80))  # Connects to Google's DNS to get local IP
         ip = s.getsockname()[0]
      except Exception:
         ip = "Unable to get IP"
      finally:
         s.close()
      return ip