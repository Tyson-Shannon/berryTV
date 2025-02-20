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

import InitSetup
import ActivateVenv
import GUI

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

def is_venv_created(venv_path):
    #Check if a virtual environment exists at the specified path.
    if os.name == "nt":  # Windows
        expected_dirs = ["Scripts", "Lib"]
    else:  # macOS/Linux
        expected_dirs = ["bin", "lib"]
    # Check if the required directories exist
    return all(os.path.isdir(os.path.join(venv_path, d)) for d in expected_dirs)

def main():
   app = QApplication(sys.argv)
   introWindow = intro()
   introWindow.showMaximized()
   sys.exit(app.exec_())

if __name__ == '__main__':
   #MAY NOT WORK ---------------------------------------------------
   #check if virtual environment exists with needed packages
   venv_location = os.path.join(os.getcwd(), ".venv")  # Path to the "venv" directory
   if is_venv_created(venv_location) == False:
      # Required packages
      required_packages = ["pyqt5", "requests", "bs4"]  # List of packages to install
      # Create and set up the virtual environment
      InitSetup.create_and_setup_venv(venv_location, required_packages)

   #activate virtual environment
   ActivateVenv.activateVenv(venv_location) #permission denied error
   #----------------------------------------------------------------
   main()