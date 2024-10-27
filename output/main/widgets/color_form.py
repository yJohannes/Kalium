from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtWidgets import QGridLayout, QWidget, QLabel, QLineEdit, QScrollArea
from PySide6.QtGui import QColor

class ColorForm(QScrollArea):
    boxPressed = Signal(QWidget)
    colorChanged = Signal(str, QColor)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.lines: list[QLineEdit] = []
        self.boxes: list[QWidget] = []
        self.focused_box = None
        self.locked_boxes = False

        self.content_layout = QGridLayout()
        self.content_layout.setHorizontalSpacing(0)
        
        self.content_widget = QWidget()
        self.content_widget.setLayout(self.content_layout)
        self.setWidget(self.content_widget)
        self.setWidgetResizable(True)
        self.row_count = 0
        return

    def create_row(self, text: str, obj_name: str, color: QColor, line_size: QSize = QSize(90, 30), box_size: QSize = QSize(30, 30)):
        label = QLabel(text)
        line = QLineEdit()
        line.setFixedSize(line_size)
        line.setObjectName(obj_name)
        line.setProperty("class", "color-line")
        line.setText(color.name())

        box = QWidget()
        box.setFixedSize(box_size)
        box.setFocusPolicy(Qt.StrongFocus)
        box.setCursor(Qt.PointingHandCursor)
        box.setProperty("class", "color-box")
        box.setStyleSheet(f"QWidget {{ background-color: {color.name()}; }}")

        box.mousePressEvent = lambda ev: self._box_press_event(ev, box)
        box.focusOutEvent = lambda ev: self._box_focus_out_event(ev, box)

        self.content_layout.addWidget(label, self.row_count, 0)
        self.content_layout.addWidget(line, self.row_count, 1)
        self.content_layout.addWidget(box, self.row_count, 2)

        self.lines.append(line)
        self.boxes.append(box)

        self.row_count += 1
        return

    def lock_boxes(self, lock: bool):
        self.locked_boxes = lock
        return

    def get_box(self, index: int) -> QWidget:
        return self.boxes[index]

    def get_box_color(self, box):
        i = self.boxes.index(box)
        return QColor(self.lines[i].text())

    def set_focused_box_color(self, color: QColor):
        if self.focused_box:
            i = self.boxes.index(self.focused_box)
            self.set_box_color(i, color)

    def set_box_color(self, box_index: int, color: QColor):
        name = color.name()
        self.boxes[box_index].setStyleSheet(f"QWidget {{ background-color: {name}; }}")
        line = self.lines[box_index]
        line.setText(name)
        self.colorChanged.emit(line.objectName(), color)

    def set_box_colors(self, colors: list[QColor]):
        for i, color in enumerate(colors):
            self.set_box_color(i, color)

    def _box_press_event(self, ev, box: QWidget):
        if not self.locked_boxes:
            self.boxPressed.emit(box)
            self.focused_box = box
        return

    def _box_focus_out_event(self, ev, box: QWidget):
        self.focused_box = None
        QWidget.focusOutEvent(box, ev)

    def resizeEvent(self, resize_event):
        super(ColorForm, self).resizeEvent(resize_event)
