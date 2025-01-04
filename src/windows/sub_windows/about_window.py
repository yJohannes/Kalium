from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QTransform
from PySide6.QtWidgets import QWidget, QScrollArea, QLabel, QPushButton
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QSizePolicy
from PySide6.QtWidgets import QDialog

from utils.resource_helpers import resource_path

class AboutWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.logo_path = resource_path("img/logo2.png")

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
        transform = QTransform().scale(0.5, 0.5)
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