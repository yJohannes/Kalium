import sys
from PySide6 import QtAsyncio
from PySide6.QtWidgets import QApplication

from windows.main_window import MainWindow
# make saveable custom themes
 
# display translation time

# theme forms laita headereit 

# make an executable using pyinstaller and put it in the inno installer
# https://chatgpt.com/c/671663db-3748-8007-9ae1-f48bd786df01


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(QtAsyncio.run())