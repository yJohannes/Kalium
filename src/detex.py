import os

from windows.main_window import MainWindow

class Detex:
    def __init__(self) -> None:
        self.window = MainWindow()
        self.window.show()

        return