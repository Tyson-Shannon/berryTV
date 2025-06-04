'''
Berry TV
v0.01
By Tyson Shannon

An application to turn your Raspberry Pi into a smart TV
'''
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import os

import GUI
import Remote

class intro(QWidget):
   def __init__(self, parent = None):
      #intro screen
      super(intro, self).__init__(parent)
      width = 1000
      height = 800
      self.setWindowTitle("berryTV")
      self.setStyleSheet("background-color: #5E17EB;") 
      self.label = QLabel(self)
      self.pixmap = QPixmap('berryTV.png')
      self.label.setPixmap(self.pixmap)
      self.label.resize(width, height)
      self.label.move(100, 0)
      QTimer.singleShot(5000, self.load)
      
   def load(self):
      self.mainWindow = GUI.window()
      self.mainWindow.showFullScreen()
      self.close()

def main():
   app = QApplication(sys.argv)
   introWindow = intro()
   introWindow.showMaximized()
   sys.exit(app.exec_())

if __name__ == '__main__':
   main()