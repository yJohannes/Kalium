from PySide6.QtCore import QThread, Signal, QMutex, QMutexLocker

class TranslationThread(QThread):
    # Class attribute
    translation_done = Signal(str)

    def __init__(self):
        super().__init__()
        self._running = True  # Control flag
        self._mutex = QMutex()  # To protect access to _running

    def run(self, expr):
        # Simulated translation function

        # Emit translation result if still running
        if self.is_running():
            ...

    def stop(self):
        with QMutexLocker(self._mutex):
            self._running = False  # Set the flag to False

    def is_running(self):
        with QMutexLocker(self._mutex):
            return self._running


"""


        def invoke_translation(expr) -> None:
            self.thread = QThread()
            self.thread.run = lambda: run_translation(expr)
            self.thread.started.connect(self.thread.run)
            self.thread.finished.connect(self.thread.deleteLater)
            self.thread.start()
            return

        def run_translation(expr) -> None:
            self.translation_done.emit(translate(expr))
            return

        def finish_translation(expr) -> None:
            return
        self.translation_done.connect(finish_translation)
"""