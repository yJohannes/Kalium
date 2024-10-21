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
        self.content_layout.setContentsMargins(9, 9, 9, 9)
        self.content_layout.setHorizontalSpacing(0)
        
        self.content_widget = QWidget()
        self.content_widget.setLayout(self.content_layout)
        self.setWidget(self.content_widget)
        self.setWidgetResizable(True)
        self.row_count = 0
        return

    def createRow(self, text: str, obj_name: str, color: QColor, line_size: QSize = QSize(90, 30), box_size: QSize = QSize(30, 30)) -> None:
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

        box.mousePressEvent = lambda ev: self.boxMousePressEvent(ev, box)
        box.focusOutEvent = lambda ev: self.boxFocusOutEvent(ev, box)

        self.content_layout.addWidget(label, self.row_count, 0)
        self.content_layout.addWidget(line, self.row_count, 1)
        self.content_layout.addWidget(box, self.row_count, 2)

        self.lines.append(line)
        self.boxes.append(box)

        self.row_count += 1
        return

    def lock_boxes(self, lock: bool) -> None:
        self.locked_boxes = lock
        return

    def getBox(self, index: int) -> QWidget:
        return self.boxes[index]

    def getBoxColor(self, box):
        i = self.boxes.index(box)
        return QColor(self.lines[i].text())

    def setBoxColor(self, color: QColor) -> None:
        if self.focused_box:
            name = color.name()
            self.focused_box.setStyleSheet(f"QWidget {{ background-color: {name}; }}")
            i = self.boxes.index(self.focused_box)
            line = self.lines[i]
            line.setText(name)
            self.colorChanged.emit(line.objectName(), color)

    def boxMousePressEvent(self, ev, box: QWidget):
        if not self.locked_boxes:
            self.boxPressed.emit(box)
            self.focused_box = box
        return

    def boxFocusOutEvent(self, ev, box: QWidget):
        self.focused_box = None
        QWidget.focusOutEvent(box, ev)

    def resizeEvent(self, resize_event):
        super(ColorForm, self).resizeEvent(resize_event)
