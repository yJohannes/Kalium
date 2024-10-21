from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import QApplication, QTextEdit, QVBoxLayout, QWidget, QPushButton
import time

# Main Window class
class MainWindow(QWidget):
    # Define the signal at the class level
    translation_done = Signal(str)

    def __init__(self):
        super().__init__()

        # Set up the layout and widgets
        layout = QVBoxLayout(self)

        # Input and Output QTextEdits
        self.ie_ref = QTextEdit(self)
        self.oe_ref = QTextEdit(self)

        # Button to trigger translation
        self.translate_button = QPushButton("Translate", self)
        self.translate_button.clicked.connect(self.start_translation)

        # Add widgets to the layout
        layout.addWidget(self.ie_ref)
        layout.addWidget(self.translate_button)
        layout.addWidget(self.oe_ref)

        # Connect the signal to update output
        self.translation_done.connect(self.update_output)
        

        self.setWindowTitle("Translation Example with Threads")

    def start_translation(self):
        expr = self.ie_ref.toPlainText()  # Get the input text

        # Create a new thread
        self.thread = QThread()

        # Connect the thread's started signal to the translation function
        self.thread.started.connect(lambda: self.run_translation(expr))

        # Connect the finished signal to cleanup
        self.thread.finished.connect(self.thread.deleteLater)  # Clean up the thread

        # Start the thread
        self.thread.start()

    def run_translation(self, expr):
        # Simulated translation function
        time.sleep(2)  # Simulate a long-running task
        translated_text = f"Translated: {expr}"  # Perform the translation
        self.translation_done.emit(translated_text)  # Emit the result to update the UI

    def update_output(self, translated_text):
        # This method is called on the main thread to update the UI
        self.oe_ref.setPlainText(translated_text)

# Main Application
if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
