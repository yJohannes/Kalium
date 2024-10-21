from PySide6.QtCore import QThread, Signal, QObject, QTimer
from PySide6.QtWidgets import QApplication

class StyleLoaderWorker(QObject):
    style_loaded = Signal(str)  # Signal to send the loaded stylesheet back to the main thread

    def __init__(self, theme_manager, style_folder_path):
        super().__init__()
        self.theme_manager = theme_manager
        self.style_folder_path = style_folder_path

    def load_stylesheet(self):
        stylesheet = self._load_stylesheet()

        # Load the palette from the theme manager
        palette = self.theme_manager.get_data()["custom"]

        # Replace placeholders with actual colors
        for placeholder, color in palette.items():
            stylesheet = stylesheet.replace(f'[{placeholder}]', color)

        # Emit the loaded stylesheet as a signal
        self.style_loaded.emit(stylesheet)

    def _load_stylesheet(self):
        # Your actual stylesheet loading logic (e.g., loading from a file)
        # Assuming `load_and_concatenate` is a function that loads your stylesheet
        return load_and_concatenate(self.style_folder_path)


class YourMainClass:
    def __init__(self):
        self.update_timer = QTimer()

        # Setup worker for stylesheet loading
        self.thread = QThread()
        self.worker = StyleLoaderWorker(self.theme_manager, self.style_folder_path)

        # Move worker to the new thread
        self.worker.moveToThread(self.thread)

        # Connect signals
        self.worker.style_loaded.connect(self.apply_stylesheet)
        self.thread.started.connect(self.worker.load_stylesheet)

        # Start the thread but keep it running for future updates
        self.thread.start()

    def request_style_update(self):
        """Call this to start the stylesheet loading process in the background."""
        if not self.thread.isRunning():
            self.thread.start()

    def apply_stylesheet(self, stylesheet):
        """This function will run on the main thread to apply the stylesheet."""
        QApplication.instance().setStyleSheet(stylesheet)
        # Once applied, you can stop the thread if desired
        self.thread.quit()