from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QSizePolicy, QLayout
from PySide6.QtWidgets import QWidget, QPushButton, QLabel, QScrollArea 
from PySide6.QtGui import QColor

class HistoryScroll(QScrollArea):
    """Signal itemPressed emits the latex and translation the item has"""
    itemPressed = Signal(list)
    historyCleared = Signal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.num_buttons = 0
        self.max_buttons = 100

        self.content_layout = QVBoxLayout()
        self.content_layout.setAlignment(Qt.AlignTop)
        self.content_layout.setSpacing(0)

        self.content_widget = QWidget()
        self.content_widget.setLayout(self.content_layout)

        self.setWidget(self.content_widget)
        self.setWidgetResizable(True)
        self.setFocusPolicy(Qt.NoFocus)

        self.deleting = False
        self._update_stylesheet()
        return
    
    def _update_stylesheet(self):
        # NÄÄ ON SAMA KUIN DANGER-SMALL!
        self.setStyleSheet("""
            QWidget[delete="true"] QLabel:hover {
                background: 1px solid #FF4242;
                color: white;
            }

            QWidget[delete="true"] QLabel:focus {
                outline: none;
                border: 1px solid #FF4242;
            }
        """)
    
    def _label_pressed(self, label: QLabel):
        if self.deleting:
            self.delete(label)
        else:
            self.itemPressed.emit([label.property("latex"), label.text()])

    def _label_key_press(self, event, label: QLabel):
        # Check for Enter/Return key
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self._label_pressed(label)

    def deleting_mode(self, deleting: bool):
        self.deleting = deleting
        self.setProperty("delete", deleting)
        self._update_stylesheet()

    def delete(self, widget: QWidget):
        next = self.content_layout.indexOf(widget) + 1
        if next_item := self.content_layout.itemAt(next):
            next_item.widget().setFocus()
        elif prev_item := self.content_layout.itemAt(next - 2):
            prev_item.widget().setFocus()
        else:
            self.setFocus()

        self.content_layout.removeWidget(widget)
        widget.deleteLater()
        self.num_buttons -= 1
        if self.content_layout.count() == 0:
            self.historyCleared.emit()
        return

    def clear(self):
        while self.content_layout.count() > 0:
            item = self.content_layout.itemAt(0)
            widget = item.widget()
            if widget:
                self.delete(widget)
        return

    def append(self, expression: str, translation: str) -> None:
        label = QLabel(translation)
        label.setProperty("latex", expression)
        label.setProperty("class", "toolbutton")
        label.setObjectName(str(self.num_buttons))
        label.setCursor(Qt.PointingHandCursor)
        label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        label.setFocusPolicy(Qt.TabFocus)

        label.setWordWrap(True)
        label.setMinimumWidth(5)
        label.mousePressEvent = lambda ev: self._label_pressed(label)
        label.keyPressEvent = lambda ev: self._label_key_press(ev, label)

        self.content_layout.insertWidget(0, label)

        for i in range(1, self.content_layout.count()):
            current_widget = self.content_layout.itemAt(i - 1).widget()
            next_widget = self.content_layout.itemAt(i).widget()
            self.content_widget.setTabOrder(current_widget, next_widget)

        if self.num_buttons >= self.max_buttons:
            oldest = self.content_layout.itemAt(self.max_buttons).widget()
            self.delete(oldest)
        else:
            self.num_buttons += 1
        return

    def append_list(self, data: list[list[str]]) -> None:
        for item in data:
            self.append(item[0], item[1])
        return

    def get_history_data(self) -> list[list[str]]:
        data = []
        for item in self.content_widget.findChildren(QLabel):
            data.append([item.property("latex"), item.text()])
        return data

"""


class HistoryScroll(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.num_buttons = 0

        self.m_layout = QVBoxLayout(self)
        self.m_layout.setContentsMargins(0, 0, 0, 0)
        self.m_layout.setAlignment(Qt.AlignTop)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.content_layout = QVBoxLayout()
        self.content_widget = QWidget()
        self.content_widget.setLayout(self.content_layout)
        self.content_widget.setStyleSheet("background-color: transparent;")
        self.scroll_area.setWidget(self.content_widget)

        self.m_layout.addWidget(self.scroll_area)

    def create_button(self, latex: str, translation: str) -> None:
        button = QPushButton(translation)
        button.setProperty("latex", latex)
        button.setProperty("class", "toolbutton")
        button.setObjectName(str(self.num_buttons))
        button.setCursor(Qt.PointingHandCursor)
        button.setStyleSheet("text-align:left; vertical-align:top;")

        self.content_layout.addWidget(button)
        self.num_buttons += 1

    def create_buttons(self, data: list[list[str, str]]) -> None:
        for item in data:
            self.create_button(item[0], item[1])
        return

"""