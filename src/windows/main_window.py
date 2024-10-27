import sys
import os
import asyncio

from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QSizePolicy
from PySide6.QtCore import Qt, QPoint, QEvent
from PySide6.QtGui import QClipboard, QKeySequence, QShortcut, QIcon, QColor

from ui.ui import WindowUI
from windows.sub_windows import AboutWindow, InfoWindow, EditorWindow
from utils.json_manager import JSONManager
from utils.resource_helpers import resource_path
from engine.old_engine import translate

class MainWindow(QMainWindow):
    clipboard = QClipboard()
    async_tasks = []
    dialogs = []

    def __init__(self):
        super().__init__()
        QApplication.instance().setAttribute(Qt.AA_EnableHighDpiScaling)
        self.setWindowTitle("Kalium")
        
        icon = QIcon(resource_path("img\logo2.png"))
        QApplication.instance().setWindowIcon(icon)

        settings = resource_path("config/settings.json")
        history = resource_path("data/history.json")
        macros = resource_path("data/macros.json")

        self.settings_manager = JSONManager(settings)
        self.history_manager = JSONManager(history)
        self.macro_manager = JSONManager(macros)

        self.ui = WindowUI()
        self.ui.init_ui(self)
        self._init_signals()
        self._load_data()
        self.setFocus()
        return
    
    def _init_signals(self):
        tb = self.ui.toolbar
        tb.mousePressEvent   = self.drag_start
        tb.mouseMoveEvent    = self.drag
        tb.mouseReleaseEvent = self.drag_end
        
        ie_ref = self.ui.i_text_edit
        oe_ref = self.ui.o_text_edit
        
        ie_ref.keyPressEvent = lambda event: self.tab_event(ie_ref, event)
        oe_ref.keyPressEvent = lambda event: self.tab_event(oe_ref, event)

        def start_translation():
            translation = translate(
                ie_ref.toPlainText(),
                TI_on=self.ui.cas_button.isChecked(),
                SC_on=self.ui.sc_button.isChecked(),
                constants_on=self.ui.constants.isChecked(),
                g_on=self.ui.g.isChecked()
            )
            for macro in self.ui.macro_table.get_data():
                if macro[2] and macro[0] != "":
                    translation = translation.replace(macro[0], macro[1])
            oe_ref.setPlainText(translation)
            self._start_animation(self._animate_progressbar)
            print("aliutettu")
            return
        
        def mode_changed(btn, on):
            if on:
                self.translation_mode = btn.property("mode")
                start_translation()
            return

        ie_ref.textChanged.connect(lambda: start_translation())
        self.ui.mode_button_group.buttonToggled.connect(mode_changed)
        self.ui.macro_table.macrosChanged.connect(lambda: start_translation())

        def copy() -> None:
            _in = self.ui.i_text_edit.toPlainText()
            _out = self.ui.o_text_edit.toPlainText()
            self.clipboard.setText(_out)
            if _out:
                self.history_manager.append([_in, _out])
                self.ui.history_scroll.append(_in, _out)
            return

        paste = lambda: self.ui.i_text_edit.setPlainText(QApplication.clipboard().text())
        quick = lambda: (paste(), copy()) # input edit textChanged gets connected in between

        self.ui.paste_button.clicked.connect(paste)
        self.ui.copy_button.clicked.connect(copy)
        self.ui.quick_button.clicked.connect(quick)

        def show_macros():
            vis = self.ui.macro_table.isVisible()
            self.ui.show_macros_button.setText("☰") if vis else self.ui.show_macros_button.setText("✕")
            self.ui.macro_table.setVisible(not vis)
            self.ui.add_macro.setVisible(not vis)
            self.ui.open_macros_btn.setVisible(not vis)

        self.ui.show_macros_button.clicked.connect(show_macros)
        self.ui.add_macro.clicked.connect(lambda _: self.ui.macro_table.add_row())

        def open_file_editor(file_path, callback):
            editor = EditorWindow(self, file_path=file_path)
            editor.fileSaved.connect(callback)
            editor.show()

        def update_macro_table():
            self.macro_manager.update()
            self.ui.macro_table.set_data(self.macro_manager.data)

        self.ui.open_macros_btn.clicked.connect(lambda: open_file_editor(resource_path("data/macros.json"), update_macro_table))
        self.ui.macro_table.macrosChanged.connect(lambda data: self.macro_manager.set_data(data))

        def show_legacy():
            vis = self.ui.g.isVisible()
            self.ui.show_legacy.setText("☰") if vis else self.ui.show_legacy.setText("✕")
            # self.ui.legacy.setVisible(not vis)
            self.ui.constants.setVisible(not vis)
            self.ui.g.setVisible(not vis)
        self.ui.show_legacy.clicked.connect(show_legacy)

        open_settings = lambda: self._change_panel(self.ui.settings_panel)
        open_history = lambda: self._change_panel(self.ui.history_panel)
        open_theme = lambda: self._change_panel(self.ui.theme_panel)

        self.ui.settings_button.clicked.connect(open_settings)
        self.ui.history_button.clicked.connect(open_history)
        self.ui.theme_button.clicked.connect(open_theme)
        self.ui.about_button.clicked.connect(lambda: self._open_sub_window(AboutWindow))
        self.ui.info_button.clicked.connect(lambda: self._open_sub_window(InfoWindow))

        copy_color = lambda: self.clipboard.setText(self.ui.color_line.text())
        self.ui.copy_color_button.clicked.connect(copy_color)

        def on_picker_color_changed(color):
            self.ui.color_form.set_focused_box_color(color),
            self.ui.color_line.setText(color.name())

        self.ui.color_picker.colorChanged.connect(on_picker_color_changed)
        self.ui.color_form.boxPressed.connect(lambda box: self.ui.color_picker.set_color(self.ui.color_form.get_box_color(box)))

        def update_color(target, color):
            self.ui.theme_manager.set_property("custom", target, color.name())
            self.ui.request_style_update()

        self.ui.color_form.colorChanged.connect(update_color)

        def choose_mode(mode: str):
            if self.ui.mode == mode: return
            match mode:
                case "dark" | "light":
                    self.ui.color_form.lock_boxes(True)
                case "custom":
                    self.ui.color_form.lock_boxes(False)
            
            self.ui.load_style(mode)
            print(mode)
            self.ui.color_form.set_box_colors([QColor(color) for color in self.ui.theme_manager.get_section(mode).values()])
            return

        self.ui.dark.toggled.connect(lambda: choose_mode("dark"))
        self.ui.light.toggled.connect(lambda: choose_mode("light"))
        # self.ui.custom.toggled.connect(lambda: choose_mode("custom"))

        def load_history_text(data):
            latex, translation = data
            self.ui.i_text_edit.blockSignals(True)
            self.ui.i_text_edit.setPlainText(latex)
            self.ui.o_text_edit.setPlainText(translation)
            self.ui.i_text_edit.blockSignals(False)
            return

        self.ui.history_scroll.itemPressed.connect(load_history_text)
        self.ui.history_scroll.historyCleared.connect(lambda: self.ui.history_del.setChecked(False))
        self.ui.history_del.toggled.connect(self.ui.history_scroll.deleting_mode)
        self.ui.history_clear.pressed.connect(self.ui.history_scroll.clear)

        key_map = {
            "Ctrl+Shift+C": copy,
            "Ctrl+R": copy,
            "Ctrl+P": paste,
            "Ctrl+Q": quick,
            "Ctrl+Shift+Z": lambda: self.ui.settings_button.setFocus(),
            "Ctrl+,": open_settings,
            "Ctrl+O": open_settings,
            "Ctrl+1": lambda: self.ui.default_button.setChecked(True),
            "Ctrl+2": lambda: self.ui.cas_button.setChecked(True),
            "Ctrl+3": lambda: self.ui.sc_button.setChecked(True),
            "Ctrl+H": open_history,
            "Ctrl+T": open_theme,
            "Ctrl+Shift+T": copy_color,
            "Ctrl+Shift+D": lambda: self.ui.dark.setChecked(True),
            "Ctrl+Shift+L": lambda: self.ui.light.setChecked(True),
            "Ctrl+G": lambda: self.ui.g.setChecked(not self.ui.g.isChecked()),
            "Ctrl+K": lambda: self.ui.constants.setChecked(not self.ui.constants.isChecked())
        }

        for (key, connection) in key_map.items():
            QShortcut(QKeySequence(key), self).activated.connect(connection)

        self.installEventFilter(self)
        return
    
    def _load_data(self):
        x, y = self.settings_manager.get_property("window", "position")
        w, h = self.settings_manager.get_property("window", "dimensions")
        self.setGeometry(x, y, w, h)
        self.translation_mode = self.settings_manager.get_property("settings", "mode")
        for btn in self.ui.mode_button_group.buttons():
            if btn.property("mode") == self.translation_mode:
                btn.setChecked(True)
        
        # self.ui.legacy.setChecked(self.settings_manager.get_property("legacy", "hotkeys"))
        self.ui.constants.setChecked(self.settings_manager.get_property("legacy", "constants"))
        self.ui.g.setChecked(self.settings_manager.get_property("legacy", "g"))

        self.ui.history_scroll.append_list(self.history_manager.data)
        self.ui.macro_table.set_data(self.macro_manager.data)

    def _save_data(self):
        self.ui.save_colors()
        self.history_manager.set_data(self.ui.history_scroll.get_history_data())
        
        geo = self.normalGeometry()
        self.settings_manager.set_property("window", "position", [geo.x(), geo.y()])
        self.settings_manager.set_property("window", "dimensions", [geo.width(), geo.height()])
        self.settings_manager.set_property("settings", "mode", self.translation_mode)
        # self.settings_manager.set_property("legacy", "hotkeys", self.ui.legacy.isChecked())
        self.settings_manager.set_property("legacy", "g", self.ui.g.isChecked())
        self.settings_manager.set_property("legacy", "constants", self.ui.constants.isChecked())

        self.settings_manager.save_data()
        self.history_manager.save_data()
        self.macro_manager.save_data()


    def _change_panel(self, panel: QWidget):
        if self.ui.splitter.widget(1) is not panel:
            self.ui.splitter.replaceWidget(1, panel)
        panel.setFocus()
        return

    def _start_animation(self, animation: "function"):
        loop = asyncio.get_event_loop()

        for task in self.async_tasks:
            if not task.done():
                task.cancel()
            self.async_tasks.remove(task)

        new_task = loop.create_task(animation())
        self.async_tasks.append(new_task)
        return 

    async def _animate_progressbar(self):
        try:
            end = 100
            degree = 4
            denominator = end ** (degree - 1)

            ease = lambda t: int(t ** degree / denominator)

            for t in range(101):
                self.ui.progressbar.setValue(ease(t))
                await asyncio.sleep(0.003)
    
            self.ui.progressbar.setLayoutDirection(Qt.RightToLeft)

            for t in range(100, -1, -1):
                self.ui.progressbar.setValue(ease(t))
                await asyncio.sleep(0.002)

            self.ui.progressbar.setValue(0)
            self.ui.progressbar.setLayoutDirection(Qt.LeftToRight)
            
        except asyncio.CancelledError:
            self.ui.progressbar.setValue(0)
            self.ui.progressbar.setLayoutDirection(Qt.LeftToRight)
            raise

    def eventFilter(self, source, event) -> bool:
        if event.type() == QEvent.MouseButtonPress:
            self.clearFocus()
            # Set focus back to the main window
            self.setFocus(Qt.OtherFocusReason)  
            return True  # Event handled
        
        return super().eventFilter(source, event)

    def _open_sub_window(self, sub_type: AboutWindow | InfoWindow | EditorWindow, *args, **kwargs):
        self.sub: QWidget = sub_type(self, *args, **kwargs)
        
        if isinstance(self.sub, AboutWindow):
            self.sub.exec()
        else:
            self.sub.show()
        return

    def tab_event(self, window_widget, event: QEvent):
        if event.key() == Qt.Key_Tab:
            self.focusNextChild()
            event.accept()
            
        elif event.key() == Qt.Key_Backtab:
            self.focusPreviousChild()
            event.accept()
        else:
            # For all other keys, call the base class implementation
            type(window_widget).keyPressEvent(window_widget, event)
        return

    def drag_start(self, event):
        if event.button() == Qt.LeftButton and not self.isMaximized():
            self.old_pos = event.globalPos()
        return super(QMainWindow, self).mousePressEvent(event)

    def drag(self, event):
        if self.old_pos is not None:
            delta = QPoint(event.globalPos() - self.old_pos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPos()
        return super(QMainWindow, self).mouseMoveEvent(event)

    def drag_end(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = None
        return super(QMainWindow, self).mouseReleaseEvent(event)

    def closeEvent(self, event):
        self._save_data()
        event.accept()