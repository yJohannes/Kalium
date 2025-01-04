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
        self.cellChanged.connect(lambda: self.update_data())
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("QTableWidget::item:selected { background-color: transparent; }")
        self.setHorizontalHeaderLabels(["From", "To", "", ""])
        self.setDragEnabled(True)
        self.setDragDropMode(QAbstractItemView.InternalMove)
        self.setSelectionBehavior(QTableWidget.SelectRows)
        self.setCornerButtonEnabled(False)
        self.setEditTriggers(QAbstractItemView.AllEditTriggers) # Set the table to allow editing with a single click

        self.setColumnWidth(2, self.row_h+40)
        self.setColumnWidth(3, self.row_h)

        vh = self.verticalHeader()
        vh.setFixedWidth(32)
        vh.setSectionsClickable(False)
        vh.setSectionsMovable(True)
        vh.setCursor(Qt.SizeVerCursor) # does not apply
        vh.setSectionResizeMode(QHeaderView.Fixed)
        vh.setDefaultSectionSize(self.row_h)
        vh.sectionClicked.connect(self.toggle_row)
        vh.sectionMoved.connect(self._move_row)

        hh = self.horizontalHeader()
        hh.setFixedHeight(38)
        hh.setSectionsClickable(False)
        hh.setSectionResizeMode(QHeaderView.Stretch)
        hh.setSectionResizeMode(2, QHeaderView.Fixed)
        hh.setSectionResizeMode(3, QHeaderView.Fixed)
        return

    def add_row(self, from_to_state: list[str, str, bool]=['','', True], update_data=True):
        self.blockSignals(True) # block self.cellChanged

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
        self.blockSignals(False)

        if update_data:
            self.update_data(silent=True)
        return
    
    def remove_row(self, button: QPushButton):
        index = self.indexAt(button.pos())
        self.blockSignals(True) # block self.cellChanged
        if index.isValid():
            self.removeRow(index.row())
        self.blockSignals(False)
        self.update_data()
        return
    
    def remove_all_rows(self, update_data=False):
        self.blockSignals(True)  # Prevent signals from firing during row removal
        for row in reversed(range(self.rowCount())):
            self.removeRow(row)
        self.blockSignals(False)
        if update_data:
            self.update_data()

    def toggle_row(self, button: QPushButton):
        index = self.indexAt(button.pos())
        if index.isValid():
            if button.isChecked():
                button.setText("ON")
            else:
                button.setText("OFF")
            self.data[index.row()][2] = not self.data[index.row()][2]
            self.macrosChanged.emit(self.data)
            # or just self.update_data()...
        return
    
    def update_data(self, silent=False):
        self.data = []
        for row in range(self.rowCount()):
            if (widget := self.cellWidget(row, 2)) is not None: # unknown bug
                self.data.append([self.item(row, 0).text(), self.item(row, 1).text(), widget.isChecked()])
        if not silent:
            self.macrosChanged.emit(self.data)
        return
    
    def get_data(self):
        return self.data
    
    def add_data(self, data):
        for d in data:
            self.add_row(d, update_data=False)
        self.update_data()
        return
    
    def set_data(self, data):
        self.remove_all_rows()
        for d in data:
            self.add_row(d, update_data=False)
        self.update_data()
        return

    def _move_row(self, logical, old_visual, new_visual):
        h = self.verticalHeader()
        h.blockSignals(True)
        self.blockSignals(True)
        h.moveSection(new_visual, old_visual)

        old0 = self.item(old_visual, 0)
        old1 = self.item(old_visual, 1)

        new0 = self.item(new_visual, 0)
        new1 = self.item(new_visual, 1)

        old0t = old0.text()
        old1t = old1.text()

        new0t = new0.text()
        new1t = new1.text()

        old0.setText(new0t)
        old1.setText(new1t)

        new0.setText(old0t)
        new1.setText(old1t)

        h.blockSignals(False)
        self.blockSignals(False)
        self.update_data()
        return

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MacroTable()
    window.show()
    sys.exit(app.exec_())
