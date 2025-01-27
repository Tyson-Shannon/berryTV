import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class window(QMainWindow):
   def __init__(self, parent = None):
      #main screen
      super(window, self).__init__(parent)
      self.setWindowTitle("berryTV")
      self.setStyleSheet("background-color: #FFFFFF;") 

      layout = QVBoxLayout()

      #top bar
      tb = self.addToolBar("Tool Bar")
      tb.setStyleSheet("background-color: #5E17EB;")
      tb.setIconSize(QSize(50, 50))
      tb.setMovable(False)
      tb.setFloatable(False)
      #logo display
      logo = QAction(QIcon("berryLogo.png"), "berryTV", self)
      tb.addAction(logo)
      #time display
      self.time_label = QLabel()
      font = QFont("Arial", 20)
      self.time_label.setFont(font) 
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
      new = QAction(QIcon("add.png"), "new", self)
      sb.addAction(new)
      settings = QAction(QIcon("setting.png"), "settings", self)
      sb.addAction(settings)
      exit = QAction(QIcon("leave.png"), "exit", self)
      sb.addAction(exit)
      sb.actionTriggered[QAction].connect(self.sideBarBut)

      self.setLayout(layout)

   def sideBarBut(self, button):
      #side bar button actions
      if button.text() == "exit":
         self.close()
   
   def update_time(self):
      #update time display
      current_time = QTime.currentTime().toString("hh:mm:ss")
      self.time_label.setText(current_time)