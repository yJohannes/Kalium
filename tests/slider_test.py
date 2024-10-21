from PySide6.QtWidgets import QSlider
from PySide6.QtCore import Qt
from PySide6.QtGui import QMouseEvent

class HueSlider(QSlider):
    def __init__(self, orientation: Qt.Orientation, parent=None):
        super().__init__(orientation, parent)
        self.setRange(0, 359)
        # Set styles to create a small dot handle
        self.setStyleSheet("""
            QSlider:horizontal
            {
                background: darkgray;
                padding: 8px 8px;
            }
                           
            QSlider::groove:horizontal {
                background-color: gray;
                height: 10px;  /* Set groove height */
                width: 0.9;
                margin: 0px -10px; /* half the handle width */
                padding: 0px 0px;
                border-radius: 5px;
            }

                              
                           
            QSlider::handle:horizontal {
                background-color: blue; /* Handle color */
                border: 2px solid white;  /* No border */
                width: 16px;  /* Set width to be small */
                height: 16px;  /* Set height to be small */
                margin: -5px 0px;  /* center the handle */
                border-radius: 10px; /* Make it circular */
            }
        """)

        self.valueChanged.connect(self.changeValue)

    def mousePressEvent(self, ev: QMouseEvent) -> None:
        if ev.button() == Qt.LeftButton:
            # Calculate the value based on the mouse position
            pos = ev.position().x()
            pos = max(0, min(pos, self.width()))  # Clamp to slider width

            value = self.minimum() + (self.maximum() - self.minimum()) * (pos / self.width())
            self.setValue(int(value))
            self.valueChanged.emit(int(value))

        return super().mousePressEvent(ev)

    def changeValue(self, value):
        # Update other components or perform actions based on the slider value
        print(f"Slider value changed: {value}")

# Example of how to use the HueSlider
if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout

    app = QApplication(sys.argv)
    window = QWidget()
    layout = QVBoxLayout()

    hue_slider = HueSlider(Qt.Horizontal)
    hue_slider.setMinimumSize(200, 50)
    layout.addWidget(hue_slider)

    window.setLayout(layout)
    window.show()
    sys.exit(app.exec_())
