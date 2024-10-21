import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QToolBar, QPushButton, QWidget, QVBoxLayout, QLabel,
    QHBoxLayout, QLineEdit, QSizePolicy
)
from PySide6.QtGui import QFont


# Uncomment the following line for PySide6
# from PySide6.QtWidgets import QApplication, QMainWindow, QToolBar, QPushButton, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QSizePolicy

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Scale Widgets Example")
        self.setGeometry(100, 100, 600, 400)

        # Create a central widget
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Layout for central widget
        self._layout = QVBoxLayout(self.central_widget)

        # Add a few widgets
        self.label = QLabel("This is a label")
        self.line_edit = QLineEdit("This is a line edit")
        self.button = QPushButton("This is a button")

        # Set size policies
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.line_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        # Add widgets to the layout
        self._layout.addWidget(self.label)
        self._layout.addWidget(self.line_edit)
        self._layout.addWidget(self.button)
        self._layout.addStretch(0)

        # Toolbar with scaling buttons
        self.toolbar = QToolBar("Scaling Toolbar", self)
        self.addToolBar(self.toolbar)

        # Create + and - buttons
        self.btn_scale_up = QPushButton("+", self)
        self.btn_scale_down = QPushButton("-", self)

        # Connect buttons to scaling functions
        self.btn_scale_up.clicked.connect(self.scale_up)
        self.btn_scale_down.clicked.connect(self.scale_down)

        # Add buttons to the toolbar
        self.toolbar.addWidget(self.btn_scale_up)
        self.toolbar.addWidget(self.btn_scale_down)

        # Initial scale factor
        self.scale_factor = 1.0

    def scale_up(self):
        self.scale_factor += 0.1
        self.scale_widgets()

    def scale_down(self):
        if self.scale_factor > 0.2:  # Prevent too small scaling
            self.scale_factor -= 0.1
            self.scale_widgets()

    def scale_widgets(self):
        # Adjust the font size for all widgets
        font_size = int(10 * self.scale_factor)  # Base font size is 10
        for widget in self.central_widget.findChildren(QWidget):
            font: QFont = widget.font()
            font.setPointSize(font_size)
            widget.setFont(font)

        # Update the layout to reflect the changes
        self.central_widget.update()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
