from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QScrollArea, QLabel, QPushButton
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QSizePolicy
from PySide6.QtWidgets import QDialog

from PySide6.QtWidgets import QTableView, QHeaderView
from PySide6.QtGui import QStandardItemModel, QStandardItem

class InfoWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Info window")
        self.setGeometry(400, 50, 450, 600)
        self.setMinimumSize(300, 300)
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)

        self._init_ui()

    def _init_ui(self):
        self.setProperty("class", "window")

        scroll_layout = QVBoxLayout()
        scroll_layout.setAlignment(Qt.AlignTop)
        scroll_container = QWidget()
        scroll_container.setLayout(scroll_layout)

        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(scroll_container)

        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['Key Combination', 'Action'])

        self.table_view = QTableView()
        self.table_view.setModel(self.model)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_view.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_view.verticalHeader().setVisible(False)  # Hide row numbers

        data = [
            ("Ctrl + R  /  Ctrl + Shift + C", "Copy result"),
            ("Ctrl + P", "Paste clipboard text"),
            ("Ctrl + Q", "Quick translate"),
            ("Ctrl + Shift + Z", "Focus / unfocus tab bar"),
            ("Ctrl + ,  /  Ctrl + O", "Open settings tab"),
            ("Ctrl + 1", "Use default translation mode"),
            ("Ctrl + 2", "Use TI-Nspire translation mode"),
            ("Ctrl + 3", "Use SpeedCrunch translation mode"),
            ("Ctrl + H", "Open history tab"),
            ("Ctrl + T", "Open theme tab"),
            ("Ctrl + Shift + T", "Copy color picker color"),
            ("Ctrl + Shift + D", "Set dark mode"),
            ("Ctrl + Shift + L", "Set light mode"),
            ("TI-Nspire extra hotkeys", ""),
            ("Ctrl + K", "Apply TI-Nspire constants"),
            ("Ctrl + G", "Translate g to _g"),
            ("Ctrl + E", "Translate e to @e"),
            ("Ctrl + I", "Translate i to @i")
        ]

        for key_combination, action in data:
            key_item = QStandardItem(key_combination)
            action_item = QStandardItem(action)
            self.model.appendRow([key_item, action_item])

        row_count = self.model.rowCount()
        total_height = 0 + 2
        for row in range(row_count):
            total_height += self.table_view.rowHeight(row)
        header_height = self.table_view.horizontalHeader().height() * 2
        total_height += header_height

        self.table_view.setFixedHeight(total_height)
        self.table_view.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.table_view.setEditTriggers(QTableView.NoEditTriggers)
        self.table_view.setSelectionMode(QTableView.NoSelection)
        self.table_view.setFocusPolicy(Qt.NoFocus)

        header = QLabel("""<h2>Keyboard shortcuts</h2>""")

        close_button = QPushButton("Close")
        close_button.setFocusPolicy(Qt.TabFocus)
        close_button.setAutoDefault(True)
        close_button.clicked.connect(self.close)
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(close_button)

        # scroll_layout.addWidget(text)
        scroll_layout.addWidget(self.table_view)
        
        layout = QVBoxLayout()
        layout.addWidget(header)
        layout.addWidget(scroll_area)
        layout.addLayout(button_layout)
        self.setLayout(layout)