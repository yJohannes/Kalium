import sys
from PySide6 import QtAsyncio
from PySide6.QtWidgets import QApplication

from windows.main_window import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(QtAsyncio.run())