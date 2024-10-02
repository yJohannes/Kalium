import sys
from PySide6 import QtAsyncio # https://stackoverflow.com/a/78803138
from PySide6.QtWidgets import QApplication

from detex import Detex

# USE QTHREAD FOR TRANSLATION THREAD

if __name__ == '__main__':
    app = QApplication(sys.argv)
    detex = Detex()
    sys.exit(QtAsyncio.run())