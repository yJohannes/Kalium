import sys
import asyncio
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
from qasync import QEventLoop, asyncSlot

class Detex(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Detex Application")
        self.setGeometry(100, 100, 400, 200)

        # Set up the central widget and layout
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)

        # Create a label to display results
        self.label = QLabel("Click the button to run async task.", self)
        layout.addWidget(self.label)

        # Create a button to trigger the async function
        self.button = QPushButton("Run Animation", self)
        self.button.clicked.connect(lambda: self.start_animation(self.animation))  # Correctly passing the function
        layout.addWidget(self.button)

        # List to keep track of async tasks
        self.async_tasks = []

    @asyncSlot()
    async def animation(self):
        """Simulate a long-running animation."""
        for i in range(5):
            self.label.setText(f"Animation Step {i + 1}...")
            await asyncio.sleep(1)  # Simulate a time-consuming task
        self.label.setText("Animation completed!")

    def start_animation(self, animation: "function"):
        """Start a new animation task, cancelling any previous ones."""
        loop = asyncio.get_event_loop()  # Get the current event loop

        # Cancel any existing tasks
        for task in self.async_tasks:
            if not task.done():
                task.cancel()
        self.async_tasks.clear()  # Clear the list after cancellation

        # Create a new task for the animation passed as an argument
        new_task = loop.create_task(animation())  # Call the animation coroutine
        self.async_tasks.append(new_task)

if __name__ == '__main__':
    app = QApplication(sys.argv)  # Create the QApplication instance
    loop = QEventLoop(app)  # Create the QEventLoop from the app

    with loop:  # Start the loop
        detex = Detex()  # Instantiate your main window
        detex.show()  # Show the main window
        loop.run_forever()  # Start the event loop
