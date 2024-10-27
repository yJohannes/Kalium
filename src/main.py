import sys
from PySide6 import QtAsyncio
from PySide6.QtWidgets import QApplication

from windows.main_window import MainWindow

# python -m auto_py_to_exe
# https://stackoverflow.com/a/13790741/

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(QtAsyncio.run())