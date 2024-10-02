import os

from PySide6.QtCore import Qt, QPoint, QEvent
from PySide6.QtGui import QColor, QFont, QMouseEvent

from PySide6.QtWidgets import (
    QApplication, QMainWindow,
    QDockWidget, QSplitter, QHBoxLayout, QVBoxLayout,
    QWidget, QPushButton, QTextEdit, QLineEdit, QLabel,
    QProgressBar, QToolBar, QMenu, QWidgetAction,
    QGraphicsDropShadowEffect, QGraphicsColorizeEffect
)

from managers.style_manager import StyleManager

class WindowUI:
    def _init_style(self, window: QMainWindow) -> None:
        self.cwd = os.path.dirname(__file__)
        style_folder_path = os.path.join(self.cwd, 'styles')
        self.style_manager = StyleManager()
        
        icon_path = os.path.join(self.cwd, '..', '..', 'img', 'logo_light.png')
        icon = self.style_manager.load_icon(icon_path) # Noto Sans Bold 270
        window.setWindowIcon(icon)
        
        stylesheet = self.style_manager.load_styles(style_folder_path)
        window.setStyleSheet(stylesheet)
        return

    def init_ui(self, window: QMainWindow):
        self._init_style(window)
        shadow_color = QColor("#78a2de")

        self.central_widget = QWidget()
        self.central_widget.setObjectName("central")
        # self.central_widget.setGraphicsEffect(self._get_colorize(self.central_widget, QColor(255, 0, 0)))

        window.setCentralWidget(self.central_widget)

        layout = QVBoxLayout(self.central_widget)
        layout.setContentsMargins(0, 0, 0, 0)

        bar_layout = QHBoxLayout()
        bar_layout.setContentsMargins(0,0,0,0)
        bar_layout.setSpacing(0)

        toolbar_widget = QWidget()
        toolbar_widget.setLayout(bar_layout)

        self.theme_button  = QPushButton("Button")
        self.history_button = QPushButton("Button 2")

        self.theme_menu = QMenu()
        action = QWidgetAction(self.theme_menu)
        theme_widget = QWidget()
        theme_layout = QVBoxLayout()
        theme_widget.setLayout(theme_layout)
        theme_widget.mousePressEvent = lambda event: None # prevent menu from closing

        btn = QPushButton("Button")
        theme_layout.addWidget(btn)

        action.setDefaultWidget(theme_widget)
        self.theme_menu.addAction(action)
        self.theme_button.setMenu(self.theme_menu)

        button_size = 40
        self.minimize = QPushButton("‒")
        self.minimize.setFixedWidth(button_size)

        self.close = QPushButton("×")
        self.close.setFixedWidth(button_size)
        self.close.setObjectName("close")
        # minimize.hide(); close.hide()
        
        bar_layout.addWidget(self.theme_button)
        bar_layout.addWidget(self.history_button)
        bar_layout.addStretch()
        bar_layout.addWidget(self.minimize)
        bar_layout.addWidget(self.close)

        self.toolbar = QToolBar("Main Toolbar", window)
        self.toolbar.setAllowedAreas(Qt.TopToolBarArea | Qt.BottomToolBarArea)
        self.toolbar.setFloatable(False)
        self.toolbar.addWidget(toolbar_widget)


        io_layout = QVBoxLayout()
        io_layout.setContentsMargins(20,20,20,20)
        io_panel = QWidget(self.central_widget)
        io_panel.setObjectName("io")
        io_panel.setLayout(io_layout)
                


        self.progressbar = QProgressBar(self.central_widget)
        self.progressbar.setRange(0, 100)
        self.progressbar.setFixedHeight(4)


        self.quick_button = QPushButton("Quick Translate")
        self.paste_button = QPushButton("Paste LaTeX")
        self.copy_button  = QPushButton("Copy")

        self.i_text_edit  = QTextEdit()
        self.i_text_edit.setPlaceholderText("LATEX")
        
        self.o_text_edit = QTextEdit()
        self.o_text_edit.setPlaceholderText("TRANSLATION")

        button_layout1 = QHBoxLayout()
        button_layout1.addWidget(self.quick_button)
        button_layout1.addWidget(self.paste_button)

        spacing = 12
        io_layout.addWidget(self.progressbar)
        io_layout.addLayout(button_layout1)
        io_layout.addSpacing(spacing)
        io_layout.addWidget(self.i_text_edit)
        io_layout.addSpacing(spacing)
        io_layout.addWidget(self.copy_button)
        io_layout.addSpacing(spacing)
        io_layout.addWidget(self.o_text_edit)

        settings_layout = QVBoxLayout()
        settings_panel = QWidget()
        settings_panel.setObjectName("settings")
        settings_panel.setLayout(settings_layout)

        field_container = QWidget()
        container_layout = QVBoxLayout()
        field_container.setLayout(container_layout)
        field_container.setObjectName("field")

        mode_field = QWidget()
        mode_layout = QVBoxLayout()
        mode_field.setLayout(mode_layout)

        self.mode_header = QLabel()
        self.mode_header.setText("Translation mode")

        mode_button_layout = QHBoxLayout()

        self.cas_button = QPushButton("CAS")
        self.cas_button.setCheckable(True)

        self.sc_button = QPushButton("SpeedCrunch")
        self.sc_button.setCheckable(True)

        mode_button_layout.addWidget(self.cas_button)
        mode_button_layout.addWidget(self.sc_button)

        mode_layout.addWidget(self.mode_header)
        mode_layout.addLayout(mode_button_layout)

        container_layout.addWidget(mode_field)

        settings_layout.addWidget(field_container)

        settings_layout.addStretch()

        splitter = QSplitter(Qt.Horizontal)
        splitter.setSizes([4, 3]) # initial split ratio

        splitter.addWidget(io_panel)
        splitter.addWidget(settings_panel)

        window.addToolBar(self.toolbar)
        layout.addWidget(splitter)
        layout.addStretch()



        # self.dock = QDockWidget("Options", window)
        # self.dock.setWidget(settings_panel)
        # self.dock.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)

        # window.addDockWidget(Qt.RightDockWidgetArea, self.dock)

        # self.ui.dock.closeEvent = lambda event: event.ignore()


        # GRAPHICS EFFECTS
        self.progressbar.setGraphicsEffect(self._shadow(self.progressbar, shadow_color))
        self.i_text_edit.setGraphicsEffect(self._shadow(self.i_text_edit, shadow_color))
        self.o_text_edit.setGraphicsEffect(self._shadow(self.o_text_edit, shadow_color))

    def _shadow(self, parent, color: QColor, radius=20) -> QGraphicsDropShadowEffect:
        shadow_effect = QGraphicsDropShadowEffect(parent)
        shadow_effect.setBlurRadius(radius)
        shadow_effect.setXOffset(0)
        shadow_effect.setYOffset(0)
        shadow_effect.setColor(color)
        return shadow_effect

    def _get_colorize(self, parent, color: QColor) -> QGraphicsColorizeEffect:
        colorize_effect = QGraphicsColorizeEffect(parent)
        colorize_effect.setColor(color)
        return colorize_effect