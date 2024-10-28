import os

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor

from PySide6.QtWidgets import (
    QApplication, QMainWindow,
    QSplitter, QHBoxLayout, QVBoxLayout, QButtonGroup,
    QWidget, QPushButton, QRadioButton, QCheckBox,
    QPlainTextEdit, QLineEdit, QLabel,
    QSizePolicy, QProgressBar, QToolBar,
    QGraphicsDropShadowEffect
)

from utils.resource_helpers import load_and_concatenate, resource_path
from utils.json_manager import JSONManager
from widgets import ColorPicker, ColorForm, HistoryScroll, MacroTable

class WindowUI:
    def __init__(self) -> None:
        self.style_folder_path = resource_path("src/ui/styles")
        theme_path = resource_path("config/theme.json")

        self.cached_stylesheet = None
        self.theme_manager = JSONManager(theme_path)
        self.mode = self.theme_manager.get_section("mode")
        self.load_style(self.mode)

        self.update_time = 300
        self.update_timer = QTimer()
        self.update_timer.setSingleShot(False)
        self.update_timer.stop()
        self.update_timer.timeout.connect(lambda: self.load_style(self.mode))

        self.finish_time = 500
        self.finish_timer = QTimer() 
        self.finish_timer.setSingleShot(True)
        self.finish_timer.timeout.connect(self.stop_loading)

    def request_style_update(self):
        if not self.update_timer.isActive():
            self.update_timer.start(self.update_time)
        self.finish_timer.start(self.finish_time)

    def stop_loading(self):
        if self.update_timer.isActive():
            self.update_timer.stop()
        self.load_style(self.mode)

    def _load_stylesheet(self):
        if not self.cached_stylesheet:
            self.cached_stylesheet = load_and_concatenate(self.style_folder_path)
        return self.cached_stylesheet

    def load_style(self, mode: str = "dark") -> None:
        self.mode = mode
        stylesheet = self._load_stylesheet()
        palette = self.theme_manager.get_section(mode)
        for placeholder, color in palette.items():
            stylesheet = stylesheet.replace(f'[{placeholder}]', color)

        QApplication.instance().setStyleSheet(stylesheet)
        return
    
    def save_colors(self):
        self.theme_manager.set_section("mode", self.mode)
        self.theme_manager.save_data()

    def init_ui(self, window: QMainWindow):
        self._init_toolbar(window)
        self._init_io()
        self._init_settings(window)
        self._init_history()
        self._init_theme(window)
        self._finish_init(window)
        self._set_graphics_effects()
        return
    
    def _init_toolbar(self, window):
        tb_layout = QHBoxLayout()
        tb_layout.setContentsMargins(0,0,0,0)
        tb_layout.setSpacing(0)

        tb_widget_container = QWidget()
        tb_widget_container.setLayout(tb_layout)

        self.settings_button = QPushButton("Settings")
        self.settings_button.setProperty("class", "toolbutton")

        self.history_button = QPushButton("History")
        self.history_button.setProperty("class", "toolbutton")

        self.theme_button  = QPushButton("Theme")
        self.theme_button.setProperty("class", "toolbutton")

        self.about_button = QPushButton("About")
        self.about_button.setProperty("class", "toolbutton")

        self.info_button = QPushButton("Info")
        self.info_button.setProperty("class", "toolbutton")

        tb_layout.addWidget(self.settings_button)
        tb_layout.addWidget(self.history_button)
        tb_layout.addWidget(self.theme_button)
        tb_layout.addWidget(self.about_button)
        tb_layout.addWidget(self.info_button)
        tb_layout.addStretch()

        self.toolbar = QToolBar()
        self.toolbar.setMovable(False)
        self.toolbar.addWidget(tb_widget_container)
        self.toolbar.setContextMenuPolicy(Qt.PreventContextMenu)
        window.addToolBar(Qt.BottomToolBarArea, self.toolbar)

    def _init_io(self):
        io_layout = QVBoxLayout()
        io_layout.setContentsMargins(0,0,0,0)
        io_layout.setAlignment(Qt.AlignCenter)

        self.io_panel = QWidget()
        self.io_panel.setLayout(io_layout)

        self.progressbar = QProgressBar(self.io_panel)
        self.progressbar.setRange(0, 100)
        self.progressbar.setFixedHeight(4)

        io_widget_container = QVBoxLayout()
        io_widget_container.setContentsMargins(14,7,14,14)

        self.quick_button = QPushButton("Quick")
        self.paste_button = QPushButton("Paste")
        self.copy_button  = QPushButton("Copy")

        self.i_text_edit  = QPlainTextEdit()
        self.i_text_edit.setPlaceholderText("LATEX")
        
        self.o_text_edit = QPlainTextEdit()
        self.o_text_edit.setPlaceholderText("TRANSLATION")

        button_layout1 = QHBoxLayout()
        button_layout1.addWidget(self.quick_button)
        button_layout1.addWidget(self.paste_button)

        spacing = 12
        io_widget_container.addLayout(button_layout1)
        io_widget_container.addSpacing(spacing)
        io_widget_container.addWidget(self.i_text_edit)
        io_widget_container.addSpacing(spacing)
        io_widget_container.addWidget(self.copy_button)
        io_widget_container.addSpacing(spacing)
        io_widget_container.addWidget(self.o_text_edit)
        
        io_layout.addWidget(self.progressbar)
        io_layout.addLayout(io_widget_container)
        io_layout.addStretch()
        return

    def _init_settings(self, window):
        settings_layout = QVBoxLayout()
        settings_layout.setAlignment(Qt.AlignTop)
        self.settings_panel = QWidget()
        self.settings_panel.setLayout(settings_layout)
        self.settings_panel.setProperty("class", "panel")

        settings_header = QLabel("<h3><b>Settings</b></h3>")
        settings_header.setAlignment(Qt.AlignCenter)

        mode_layout = QVBoxLayout()
        mode_field = QWidget()

        mode_field.setLayout(mode_layout)
        mode_field.setProperty("class", "field")

        self.mode_header = QLabel("Translation mode")

        mode_button_layout = QHBoxLayout()
        self.mode_button_group = QButtonGroup(window)
        self.mode_button_group.setExclusive(True)

        self.default_button = QPushButton("Default")
        self.default_button.setProperty("mode", "default")
        self.default_button.setCheckable(True)

        self.cas_button = QPushButton("TI-Nspire")
        self.cas_button.setProperty("mode", "cas")
        self.cas_button.setCheckable(True)

        self.sc_button = QPushButton("SpeedCrunch")
        self.sc_button.setProperty("mode", "speencrunch")
        self.sc_button.setCheckable(True)

        self.mode_button_group.addButton(self.cas_button)
        self.mode_button_group.addButton(self.sc_button)
        self.mode_button_group.addButton(self.default_button)

        mode_button_layout.addWidget(self.cas_button)
        mode_button_layout.addWidget(self.sc_button)

        mode_layout.addWidget(self.mode_header)
        mode_layout.addWidget(self.default_button)
        mode_layout.addLayout(mode_button_layout)

        macro_layout = QVBoxLayout()
        self.macro_field = QWidget()
        self.macro_field.setLayout(macro_layout)
        self.macro_field.setProperty("class", "field")

        macro_control_layout = QHBoxLayout()
        macro_control_layout.setContentsMargins(0,0,0,0)
        macro_control_layout.setSpacing(0)

        macro_label = QLabel("Macros")

        self.show_macros_button = QPushButton("✕")
        self.show_macros_button.setProperty("class", "toolbutton")
        self.show_macros_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)


        macro_control_layout.addWidget(macro_label)
        macro_control_layout.addStretch()
        macro_control_layout.addWidget(self.show_macros_button)

        macro_layout.addLayout(macro_control_layout)

        self.macro_table = MacroTable()
        self.macro_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        macro_btn_layout = QHBoxLayout()
        self.add_macro = QPushButton("+")
        self.open_macros_btn = QPushButton("Edit file")

        macro_btn_layout.addWidget(self.add_macro, stretch=7)
        macro_btn_layout.addWidget(self.open_macros_btn, stretch=2)

        macro_layout.addWidget(self.macro_table)
        macro_layout.addLayout(macro_btn_layout)

        legacy_layout = QVBoxLayout()
        legacy_field = QWidget()
        legacy_field.setLayout(legacy_layout)
        legacy_field.setProperty("class", "field")

        legacy_control_layout = QHBoxLayout()
        legacy_control_layout.setContentsMargins(0,0,0,0)
        legacy_control_layout.setSpacing(0)

        legacy_label = QLabel("TI-Nspire extras")

        self.show_legacy = QPushButton("✕")
        self.show_legacy.setProperty("class", "toolbutton")
        self.show_legacy.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        legacy_control_layout.addWidget(legacy_label)
        legacy_control_layout.addStretch()
        legacy_control_layout.addWidget(self.show_legacy)

        legacy_layout.addLayout(legacy_control_layout)

        self.legacy_buttons = QButtonGroup()
        self.legacy_buttons.setExclusive(False)

        const_g_layout = QHBoxLayout()
        self.constants = QPushButton("Nspire constants")
        self.constants.setCheckable(True)
        self.g = QPushButton("g to _g")
        self.g.setCheckable(True)
        const_g_layout.addWidget(self.constants, stretch=10)
        const_g_layout.addWidget(self.g, stretch=3)

        ei_layout = QHBoxLayout()
        self.e = QPushButton("e to @e")
        self.i = QPushButton("i to @i")
        self.e.setCheckable(True)
        self.i.setCheckable(True)
        ei_layout.addWidget(self.e)
        ei_layout.addWidget(self.i)
        
        self.legacy_buttons.addButton(self.constants)
        self.legacy_buttons.addButton(self.g)
        self.legacy_buttons.addButton(self.e)
        self.legacy_buttons.addButton(self.i)

        legacy_layout.addLayout(const_g_layout)
        legacy_layout.addLayout(ei_layout)

        settings_layout.addWidget(settings_header)
        settings_layout.addSpacing(5)
        settings_layout.addWidget(mode_field)
        settings_layout.addWidget(self.macro_field)
        settings_layout.addWidget(legacy_field)
        return

    def _init_history(self):
        self.history_layout = QVBoxLayout()
        self.history_panel = QWidget()
        self.history_panel.setLayout(self.history_layout)
        self.history_panel.setProperty("class", "panel")

        history_header = QLabel("<h3><b>History</b></h3>")
        history_header.setAlignment(Qt.AlignCenter)

        scroll_layout = QVBoxLayout()
        scroll_field = QWidget()
        scroll_field.setLayout(scroll_layout)
        scroll_field.setProperty("class", "field")

        scroll_btn_layout = QHBoxLayout()
        self.history_del = QPushButton("Erase translation")
        self.history_del.setCheckable(True)
        self.history_del.setProperty("class", "danger-small")

        self.history_clear = QPushButton("Clear history")
        self.history_clear.setProperty("class", "danger-big")

        scroll_btn_layout.addWidget(self.history_del)
        scroll_btn_layout.addWidget(self.history_clear)

        self.history_scroll = HistoryScroll()

        scroll_layout.addLayout(scroll_btn_layout)
        scroll_layout.addWidget(self.history_scroll)

        self.history_layout.addWidget(history_header)
        self.history_layout.addSpacing(8)
        self.history_layout.addWidget(scroll_field)

    def _init_theme(self, window):
        theme_layout = QVBoxLayout()
        self.theme_panel = QWidget()
        self.theme_panel.setLayout(theme_layout)
        self.theme_panel.setProperty("class", "panel")

        theme_header = QLabel("<h3><b>Theme</b></h3>")
        theme_header.setAlignment(Qt.AlignCenter)

        picker_layout = QVBoxLayout()
        picker_field = QWidget()
        picker_field.setLayout(picker_layout)
        picker_field.setProperty("class", "field")

        h_picker_layout = QHBoxLayout()
        self.color_line = QLineEdit()
        self.color_line.setPlaceholderText("COLOR")
        self.color_line.setAlignment(Qt.AlignCenter)

        self.copy_color_button = QPushButton("⧉")
        self.copy_color_button.setMinimumWidth(35)

        h_picker_layout.addWidget(self.color_line)
        h_picker_layout.addWidget(self.copy_color_button)

        self.color_picker = ColorPicker()
        self.color_picker.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        picker_layout.addWidget(self.color_picker)
        picker_layout.addLayout(h_picker_layout)

        self.color_form = ColorForm()
        form_layout = QVBoxLayout()
        self.form_container = QWidget()
        self.form_container.setLayout(form_layout)
        self.form_container.setProperty("class", "field")

        form_layout.addWidget(self.color_form)

        accent      = self.theme_manager.get_property(self.mode, "accent")
        primary     = self.theme_manager.get_property(self.mode, "primary")
        secondary   = self.theme_manager.get_property(self.mode, "secondary")
        tertiary    = self.theme_manager.get_property(self.mode, "tertiary")
        input_      = self.theme_manager.get_property(self.mode, "input")
        field_hover = self.theme_manager.get_property(self.mode, "field-hover")
        text        = self.theme_manager.get_property(self.mode, "text")
        focus       = self.theme_manager.get_property(self.mode, "focus")
        toolbar     = self.theme_manager.get_property(self.mode, "toolbar")

        # Object names must be the same as in theme.json
        self.color_form.create_row("Accent:",    "accent",    QColor(accent))
        self.color_form.create_row("Primary:",   "primary",   QColor(primary))
        self.color_form.create_row("Secondary:", "secondary", QColor(secondary))
        self.color_form.create_row("Tertiary:",  "tertiary",  QColor(tertiary))
        self.color_form.create_row("Input:",     "input",     QColor(input_))
        self.color_form.create_row("Field hover:", "field-hover", QColor(field_hover))
        self.color_form.create_row("Text:",      "text",      QColor(text))
        self.color_form.create_row("Focus:",     "focus",     QColor(focus))
        self.color_form.create_row("Toolbar:",   "toolbar",   QColor(toolbar))

        theme_mode_layout = QHBoxLayout()
        self.theme_mode_field = QWidget()
        self.theme_mode_field.setProperty("class", "field")

        mode_label = QLabel("Mode")

        self.dark = QRadioButton("Dark")
        self.light = QRadioButton("Light")

        self.dark.setFocusPolicy(Qt.TabFocus)
        self.light.setFocusPolicy(Qt.TabFocus)

        mode_group = QButtonGroup(window)
        mode_group.setExclusive(True)
        mode_group.addButton(self.dark)
        mode_group.addButton(self.light)

        match self.mode:
            case "dark": self.dark.setChecked(True); self.color_form.lock_boxes(True)
            case "light": self.light.setChecked(True); self.color_form.lock_boxes(True)

        theme_mode_layout.addWidget(self.dark, alignment=Qt.AlignCenter)
        theme_mode_layout.addWidget(self.light, alignment=Qt.AlignCenter)

        self.theme_mode_field.setLayout(theme_mode_layout)

        theme_layout.addWidget(theme_header)
        theme_layout.addWidget(picker_field)
        theme_layout.addWidget(self.form_container)
        theme_layout.addWidget(mode_label)
        theme_layout.addWidget(self.theme_mode_field)
        return

    def _finish_init(self, window):
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.setSizes([4, 3]) # initial split ratio

        self.splitter.addWidget(self.io_panel)
        self.splitter.addWidget(self.settings_panel)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.splitter)

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)

        window.setProperty("class", "window")
        window.setCentralWidget(self.central_widget)

        for widget in QApplication.allWidgets():
            if isinstance(widget, QPushButton):
                widget.setFocusPolicy(Qt.TabFocus)
                widget.setAutoDefault(True)
            elif isinstance(widget, QCheckBox):
                widget.setFocusPolicy(Qt.TabFocus)
        return

    def _set_graphics_effects(self):
        self.progressbar.setGraphicsEffect(self._get_shadow(self.progressbar, QColor("#78a2de")))

    def _get_shadow(self, parent, color: QColor, radius=20) -> QGraphicsDropShadowEffect:
        shadow_effect = QGraphicsDropShadowEffect(parent)
        shadow_effect.setBlurRadius(radius)
        shadow_effect.setXOffset(0)
        shadow_effect.setYOffset(0)
        shadow_effect.setColor(color)
        return shadow_effect
    