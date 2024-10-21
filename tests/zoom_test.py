from PySide6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Set up layout
        layout = QVBoxLayout(self)

        # Create a button
        self.button = QPushButton("Click Me", self)

        # Apply QSS to simulate the focus rectangle around the entire button
        self.button.setStyleSheet("""
            QPushButton {
                border: 2px solid #8f8f91;  /* Normal border */
                border-radius: 6px;
                padding: 5px;
            }
            QPushButton:focus {
                border: 2px solid #8f8f91;  /* Keep the original border */
                box-shadow: 0 0 0 3px #3465A4;  /* Simulate outline by using box-shadow */
            }
        """)

        # Add button to layout
        layout.addWidget(self.button)

        # Set window title
        self.setWindowTitle("Focus Outline Example")

# Main application
app = QApplication([])
window = MainWindow()
window.show()
app.exec()
