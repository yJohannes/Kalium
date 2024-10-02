import sys
from PySide6.QtCore import Qt
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create the QML engine
    engine = QQmlApplicationEngine()

    # Load the QML file
    engine.load(r"C:\dev\py\detex\tests\main.qml")

    # Check for errors
    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())
