
import sys
from PySide6.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QHeaderView, QVBoxLayout, QPushButton, QWidget, QSizePolicy
from PySide6.QtWidgets import QAbstractItemView
from PySide6.QtCore import Qt, Signal

class MacroTable(QTableWidget):
    macrosChanged = Signal(list)
    def __init__(self):
        super().__init__(0, 4)
        self.data: list[list[str]] = []
        self.row_h = 30
        self.cellChanged.connect(self.update_data)
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("QTableWidget::item:selected { background-color: transparent; }")
        self.setHorizontalHeaderLabels(["From", "To", "", ""])
        self.setColumnWidth(2, self.row_h+20)
        self.setColumnWidth(3, self.row_h)
        self.setSelectionBehavior(QTableWidget.SelectRows)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.horizontalHeader().setSectionResizeMode(2, QHeaderView.Fixed)
        self.horizontalHeader().setSectionResizeMode(3, QHeaderView.Fixed)
        self.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.verticalHeader().setDefaultSectionSize(self.row_h)
        self.verticalHeader().setFixedWidth(32)
        self.verticalHeader().sectionClicked.connect(self.toggle_row)
        self.horizontalHeader().setSectionsClickable(False)
        self.verticalHeader().setSectionsClickable(False)
        self.setCornerButtonEnabled(False)
        self.setEditTriggers(QAbstractItemView.AllEditTriggers) # Set the table to allow editing with a single click
        return
        
    def add_row(self, from_to_state: list[str, str, bool]=['','', True]):
        row_position = self.rowCount()
        self.insertRow(row_position)
        self.setRowHeight(row_position, self.row_h)

        item1 = QTableWidgetItem()
        item2 = QTableWidgetItem()

        item1.setText(from_to_state[0])
        item2.setText(from_to_state[1])

        self.setItem(row_position, 0, item1)
        self.setItem(row_position, 1, item2)

        text = "ON" if from_to_state[2] else "OFF"

        toggle_btn = QPushButton(text, self)
        toggle_btn.setProperty("class", "toolbutton")
        toggle_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        toggle_btn.setFocusPolicy(Qt.TabFocus)
        toggle_btn.setAutoDefault(True)

        toggle_btn.setCheckable(True)
        toggle_btn.setChecked(from_to_state[2])
        toggle_btn.clicked.connect(lambda: self.toggle_row(toggle_btn))
        self.setCellWidget(row_position, 2, toggle_btn)

        remove_btn = QPushButton("━", self)
        remove_btn.setProperty("class", "toolbutton")
        remove_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        remove_btn.setFocusPolicy(Qt.TabFocus)
        remove_btn.setAutoDefault(True)

        remove_btn.clicked.connect(lambda: self.remove_row(remove_btn))
        self.setCellWidget(row_position, 3, remove_btn)
        self.update_data()
        return
    
    def remove_row(self, button: QPushButton):
        index = self.indexAt(button.pos())
        if index.isValid():
            self.removeRow(index.row())
        self.update_data()
        return

    def toggle_row(self, button: QPushButton):
        index = self.indexAt(button.pos())
        if index.isValid():
            if button.isChecked():
                button.setText("ON")
            else:
                button.setText("OFF")
            self.update_data()
        return
    
    def update_data(self):
        self.data = []
        for row in range(self.rowCount()):
            if (widget := self.cellWidget(row, 2)) is not None: # unknown bug
                self.data.append([self.item(row, 0).text(), self.item(row, 1).text(), widget.isChecked()])
        self.macrosChanged.emit(self.data)
        return
    
    def get_data(self):
        return self.data
    
    def set_data(self, data):
        for d in data:
            self.add_row(d)
        return

    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MacroTable()
    window.show()
    sys.exit(app.exec_())
