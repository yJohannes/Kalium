import os

from PySide6.QtCore import Qt

from PySide6.QtGui import QPixmap, QIcon, QTransform, QFont, QColor

from PySide6.QtWidgets import QWidget, QScrollArea, QLabel, QPushButton
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QSizePolicy
from PySide6.QtWidgets import QColorDialog, QDialog

from PySide6.QtWidgets import QTableView, QHeaderView
from PySide6.QtGui import QStandardItemModel, QStandardItem


class AboutWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        cwd = os.path.dirname(os.path.abspath(__file__))
        self.logo_path = os.path.join(cwd, '..', '..', 'img', 'logo2.png')

        self.setWindowTitle("About Kalium")
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

        image_label = QLabel(self)
        pixmap = QPixmap(self.logo_path)
        resize_factor = 0.5
        transform = QTransform().scale(resize_factor, resize_factor)
        resized_pixmap = pixmap.transformed(transform, Qt.SmoothTransformation)

        image_label.setPixmap(resized_pixmap)
        image_label.setAlignment(Qt.AlignCenter)
        scroll_layout.addWidget(image_label)

        text = QLabel(
"""
<h2><b>Kalium</h2>
<p>v1.0.0 (PySide6)</p>

<p><b>Developer</b><br>
Johannes Ylinen</p>

<p>This tool was made during high school years to minimize time spent on
manual rewriting and to reduce interruptions caused by context switching.</p>

<h2>MIT License</h2>

<p>Copyright (c) 2024 Johannes Ylinen</p>

<p>Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:</p>

<p>The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.</p>

<p>THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.</p>
"""
        )
        text.setAlignment(Qt.AlignCenter)
        text.setTextInteractionFlags(Qt.TextSelectableByMouse)
        text.setWordWrap(True)
        text.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        close_button = QPushButton("Close")
        close_button.setFocusPolicy(Qt.TabFocus)
        close_button.setAutoDefault(True)
        close_button.clicked.connect(self.close)
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(close_button)

        scroll_layout.addWidget(text)
        
        layout = QVBoxLayout()
        layout.addWidget(scroll_area)
        layout.addLayout(button_layout)
        self.setLayout(layout)

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
            ("Ctrl + ,  /  Ctrl + O", "Open settings tab"),
            ("Ctrl + H", "Open history tab"),
            ("Ctrl + T", "Open theme tab"),
            ("Ctrl + K", "Copy color picker color"),
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

#         text = QLabel(
# """


# <style>
#     .table {
#         border-collapse: collapse;
#         width: 200%;
#         border: 2px solid #191919;
#         border-radius: 10px;
#         overflow: hidden;
#     }
#     .header {
#         padding: 8px;
#         background-color: #131313;
#         border: 1px solid #131313;
#         color: white;
#     }
#     .cell {
#         padding: 8px;
#         border: 1px solid #131313;

#     }
# </style>
# <table class="table">
#     <tr>
#         <th class="header">Key Combination</th>
#         <th class="header">Action</th>
#     </tr>
#     <tr>
#         <td class="cell">Ctrl + R</td>
#         <td class="cell">Copy result</td>
#     </tr>
#     <tr>
#         <td class="cell">Ctrl + Shift + C</td>
#         <td class="cell"></td>
#     </tr>
#     <tr>
#         <td class="cell">Ctrl + P</td>
#         <td class="cell">Paste clipboard text</td>
#     </tr>
#     <tr>
#         <td class="cell">Ctrl + Q</td>
#         <td class="cell">Quick translate — paste + copy</td>
#     </tr>
#     <tr>
#         <td class="cell">Ctrl + ,</td>
#         <td class="cell">Open settings tab</td>
#     </tr>
#     <tr>
#         <td class="cell">Ctrl + O</td>
#         <td class="cell"></td>
#     </tr>
#     <tr>
#         <td class="cell">Ctrl + H</td>
#         <td class="cell">Open history tab</td>
#     </tr>
#     <tr>
#         <td class="cell">Ctrl + T</td>
#         <td class="cell">Open theme tab</td>
#     </tr>
#     <tr>
#         <td class="cell">Ctrl + K</td>
#         <td class="cell">Copy color picker color</td>
#     </tr>
# </table>

# """
#         )
#         text.setAlignment(Qt.AlignCenter)
#         text.setTextInteractionFlags(Qt.TextSelectableByMouse)
#         text.setWordWrap(True)
#         text.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

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

def color_dialog(parent) -> str:
        color = QColorDialog.getColor(QColor(255,255,255), parent, "Select Color")
        if color.isValid():
             return f"rgb({color.red()},{color.green()},{color.blue()})"
        
if __name__ == '__main__':
    ...