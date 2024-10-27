from PySide6.QtCore import Qt, Signal, QPoint, QPointF
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout
from PySide6.QtWidgets import QWidget, QLabel, QSlider
from PySide6.QtGui import QColor, QMouseEvent, QPaintEvent, QPainter, QLinearGradient, QBrush

class ColorPort(QWidget):
    """A widget that allows for color selection with a gradient."""
    colorChanged = Signal(QColor)

    def __init__(self):

        super().__init__()

        self.reticle = QWidget(self)
        self.reticle.setFixedSize(16, 16)
        self.reticle.setCursor(Qt.PointingHandCursor)

        self.hue      = 359
        self.color    = QColor(0, 0, 255)
        self.position = QPointF(self.width(), 0)
        self.reticle.move(self.position.x(), self.position.y())
        return

    def paintEvent(self, event):
        painter = QPainter(self)

        # Linear gradient from top-left (white) to top-right (full hue color)
        self.gradient = QLinearGradient(0, 0, self.width(), 0)
        self.gradient.setColorAt(0, QColor(255, 255, 255))
        self.gradient.setColorAt(1, QColor.fromHsv(self.hue, 255, 255))

        # Create a brush with the gradient and fill the top
        painter.setBrush(QBrush(self.gradient))
        painter.setPen(Qt.NoPen)
        painter.drawRect(self.rect())

        # Add a black gradient from top to bottom to make it fade to black
        black_gradient = QLinearGradient(0, 0, 0, self.height())
        black_gradient.setColorAt(0, Qt.transparent) # Transparent at the top
        black_gradient.setColorAt(1, QColor(0, 0, 0))

        painter.setBrush(QBrush(black_gradient))
        painter.drawRect(self.rect())

    def select_color(self):
        x = min(max(0, self.position.x()), self.width())
        y = min(max(0, self.position.y()), self.height())

        x_ratio = x / self.width()
        y_ratio = y / self.height()

        self.reticle.move(QPoint(x, y) - QPoint(self.reticle.width() // 2, self.reticle.height() // 2))

        saturation = int(x_ratio * 255.0)
        value = int((1.0 - y_ratio) * 255.0)

        self.color = QColor.fromHsv(self.hue, saturation, value)

        r, g, b = self.color.red(), self.color.green(), self.color.blue()
        self.reticle.setStyleSheet(
            f"""
            border: 2px solid white;
            border-radius: 8px;
            background-color: rgb({r}, {g}, {b});
            """
        )

        self.colorChanged.emit(self.color)
        return

    def set_color(self, color: QColor):
        s, v = color.saturation(), color.value()
        x_ratio = s / 255.0
        y_ratio = 1.0 - v / 255.0
        x = x_ratio * self.width()
        y = y_ratio * self.height()
        pos = QPoint(x, y)
        self.position = pos
        self.reticle.move(pos - QPoint(self.reticle.width() // 2, self.reticle.height() // 2))
        # Prevent gradient from becoming grayscale
        self.set_hue(self.hue) if s == 0 else self.set_hue(color.hue())
        return

    def set_hue(self, hue: int):
        self.hue = hue
        self.select_color()
        self.update()
        return

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.position = event.position()
            self.select_color()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.position = event.position()
            self.select_color()

class HueSlider(QSlider):
    def __init__(self, orientation: Qt.Orientation, parent=None):
        super().__init__(orientation, parent)
        self.setRange(0, 359)
        self.setFixedHeight(30)
        self.setFocusPolicy(Qt.NoFocus)

        self.hue_stops = {
            0  : QColor(255, 0,   0, ),
            10 : QColor(255, 154, 0, ),
            20 : QColor(208, 222, 33,),
            30 : QColor(79,  220, 74,),
            40 : QColor(63,  218, 216),
            50 : QColor(47,  201, 226),
            60 : QColor(28,  127, 238),
            70 : QColor(95,  21,  242),
            80 : QColor(186, 12,  248),
            90 : QColor(251, 7,   217),
            100: QColor(255, 0,   0, ) 
        }

        self.groove_style = """
            QSlider::groove:horizontal
            {
                height: 10px;
                margin: 0px, -8px;
                border-radius: 5px;
            """

        gradient = "\nbackground: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,"

        for stop, color in self.hue_stops.items():
            gradient = gradient + f"\nstop: {stop / 100.0} {color.name()},"

        gradient += ");\n}" 
        self.groove_style += gradient

        self.setStyleSheet(self.groove_style)
        self.valueChanged.connect(self.set_hue)
        return

    def set_hue(self, value):
        self.setValue(value)
        p = self.value() / self.maximum()
        color = self.interpolate(p)
        r, g, b = color.red(), color.green(), color.blue()
        bg = f"rgb({r}, {g}, {b})"

        self.setStyleSheet(
            self.groove_style + f"""\n
                QSlider::handle:horizontal
                {{
                    background-color: {bg};
                    border: 2px solid white;
                    width: 14px;
                    height: 14px;
                    margin: -4px 0px;  /* center the handle */
                    border-radius: 8px; /* uhh why not 8px? */
                }}
            """
        )

    def interpolate(self, p: float) -> QColor:
        start = int(p * 10) * 10
        end = start + 10 if start <= 90 else start

        c1 = self.hue_stops[start]
        c2 = self.hue_stops[end]

        r1, g1, b1 = c1.red(), c1.green(), c1.blue()
        r2, g2, b2 = c2.red(), c2.green(), c2.blue()

        dr, dg, db = r2 - r1, g2 - g1, b2 - b1

        q = (int(p * 100) - start) / 10.0
        ir, ig, ib = q * dr, q * dg, q * db

        return QColor(r1 + ir, g1 + ig, b1 + ib)

    def mousePressEvent(self, ev: QMouseEvent) -> None:
        if ev.button() == Qt.LeftButton:
            # value = self.minimum() + (self.maximum() - self.minimum()) * ev.position().x() / self.width()
            # min = 0
            x = ev.position().x()
            value = self.maximum() * x / self.width()
            self.setValue(int(value))
            self.valueChanged.emit(int(value))
        return super().mousePressEvent(ev)

class ColorDisplay(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.color: QColor = QColor(0,0,0)
        return

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.fillRect(self.rect(), self.color)
        return

    def set_color(self, color: QColor) -> None:
        self.color = color
        self.repaint()
        return

class ColorPicker(QWidget):
    colorChanged = Signal(QColor)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        self.setLayout(layout)

        self.color_port = ColorPort()
        self.color_display = ColorDisplay()
        self.color_display.setMinimumHeight(120)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.color_display)
        h_layout.addWidget(self.color_port)
        h_layout.setStretch(0, 4)
        h_layout.setStretch(1, 7)

        self.hue_slider = HueSlider(Qt.Horizontal)
        self.hue_slider.setValue(359)
        self.hue_slider.valueChanged.connect(self._hue_changed)
        self.color_port.colorChanged.connect(self._color_changed)

        layout.addLayout(h_layout)
        layout.addWidget(self.hue_slider)

        self.colorChanged = self.color_port.colorChanged
        return
    
    def set_color(self, color: QColor | str) -> None:
        self.color_port.set_color(color)
        # Prevent gradient from becoming grayscale
        if color.saturation() == 0:
            self.hue_slider.set_hue(self.color_port.hue)
        else:
            self.hue_slider.set_hue(color.hue())
        return

    def _hue_changed(self, hue) -> None:
        self.color_port.set_hue(hue)
        self.color_display.set_color(self.color_port.color)
        return
    
    def _color_changed(self, color) -> None:
        self.color_display.set_color(color)
        return
    
if __name__ == '__main__':
    class MainWindow(QMainWindow):
        def __init__(self):
            super().__init__()

            color_picker = ColorPicker(self)

            layout = QVBoxLayout()
            layout.addWidget(color_picker)
            layout.addWidget(QLabel("Hue"))

            container = QWidget()
            container.setLayout(layout)
            self.setCentralWidget(container)

    app = QApplication([])
    window = MainWindow()
    window.setWindowTitle("Google-Style Color Picker")
    window.show()
    app.exec()
