import asyncio

from PySide6.QtCore import Qt, QPoint, QEvent, Signal
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6.QtGui import QClipboard, QKeySequence, QShortcut, QIcon, QColor

from ui.ui import WindowUI
from widgets.message_boxes import new_error_box
from windows.sub_windows import AboutWindow, InfoWindow, EditorWindow
from utils.json_manager import JSONManager
from utils.resource_helpers import resource_path, exe_dir_path
from engine.old_engine import translate

class MainWindow(QMainWindow):
    old_pos = None
    clipboard = QClipboard()
    async_tasks = []
    splitter_save = []
    split = [100,100] 

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kalium")
        self.setMinimumSize(340, 435)
        icon = QIcon(resource_path("img/logo2.png"))
        QApplication.instance().setWindowIcon(icon)
        QApplication.instance().setAttribute(Qt.AA_EnableHighDpiScaling)

        settings = exe_dir_path("config/settings.json")
        history = exe_dir_path("data/history.json")
        macros = exe_dir_path("data/macros.json")

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
        self._setup_toolbar_signals()
        self._setup_text_edit_signals()
        self._setup_macro_signals()
        self._setup_misc_controls()
        self._setup_history_signals()
        self._setup_theme_signals()
        self._setup_shortcuts()
        self.installEventFilter(self)
        return
    
    def _setup_misc_controls(self):
        self.ui.mode_button_group.buttonToggled.connect(self._on_translation_mode_changed)
        self.ui.macro_table.macrosChanged.connect(lambda: self._start_translation())

        self.ui.paste_button.clicked.connect(self._paste_text)
        self.ui.copy_button.clicked.connect(self._copy_text)
        self.ui.quick_button.clicked.connect(self._quick_translate)

        self.ui.show_legacy.clicked.connect(lambda: self._toggle_legacy_controls(not self.ui.g.isVisible()))
        self.ui.legacy_buttons.buttonToggled.connect(self._start_translation)

        return

    def _setup_toolbar_signals(self):
        tb = self.ui.toolbar
        tb.mousePressEvent = self.drag_start
        tb.mouseMoveEvent = self.drag
        tb.mouseReleaseEvent = self.drag_end

        self.ui.settings_button.clicked.connect(lambda: self._change_panel(self.ui.settings_panel))
        self.ui.history_button.clicked.connect(lambda: self._change_panel(self.ui.history_panel))
        self.ui.theme_button.clicked.connect(lambda: self._change_panel(self.ui.theme_panel))
        self.ui.about_button.clicked.connect(lambda: self._open_sub_window(AboutWindow))
        self.ui.info_button.clicked.connect(lambda: self._open_sub_window(InfoWindow))

        self.ui.panel_toggle.toggled.connect(self._toggle_panel)
        return

    def _setup_text_edit_signals(self):
        ie_ref = self.ui.i_text_edit
        oe_ref = self.ui.o_text_edit
        
        ie_ref.keyPressEvent = lambda event: self.tab_event(ie_ref, event)
        oe_ref.keyPressEvent = lambda event: self.tab_event(oe_ref, event)
        ie_ref.textChanged.connect(lambda: self._start_translation())
        return

    def _setup_theme_signals(self):
        self.ui.copy_color_button.clicked.connect(self._copy_picker_color)
        def on_picker_color_changed(color):
            self.ui.color_form.set_focused_box_color(color),
            self.ui.color_line.setText(color.name())

        self.ui.color_picker.colorChanged.connect(on_picker_color_changed)
        self.ui.color_form.boxPressed.connect(lambda box: self.ui.color_picker.set_color(self.ui.color_form.get_box_color(box)))
        self.ui.dark.toggled.connect(lambda: self._choose_theme_mode("dark"))
        self.ui.light.toggled.connect(lambda: self._choose_theme_mode("light"))
        return

    def _setup_history_signals(self):
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
        return

    def _setup_macro_signals(self):
        self.ui.open_macros_btn.clicked.connect(lambda: self._open_file_editor(exe_dir_path("data/macros.json"), self._update_macro_table))
        self.ui.macro_table.macrosChanged.connect(lambda data: self.macro_manager.set_data(data))
        self.ui.show_macros_button.clicked.connect(lambda: self._toggle_macros(not self.ui.macro_table.isVisible()))
        self.ui.add_macro.clicked.connect(lambda _: self.ui.macro_table.add_row())
        return

    def _open_file_editor(self, file_path, callback):
        editor = EditorWindow(parent=self, file_path=file_path)
        editor.fileSaved.connect(lambda: callback(editor.backup))
        editor.show()
        return

    def _setup_shortcuts(self):
        key_map = {
            "Ctrl+Shift+C": self._copy_text,
            "Ctrl+R":       self._copy_text,
            "Ctrl+P":       self._paste_text,
            "Ctrl+Q":       self._quick_translate,
            "Ctrl+B":       lambda: self.ui.panel_toggle.toggle(), # activates the toggled Signal
            "Alt+Z":        lambda: self.ui.settings_button.setFocus(),
            "Ctrl+,":       lambda: self._change_panel(self.ui.settings_panel),
            "Ctrl+O":       lambda: self._change_panel(self.ui.settings_panel),
            "Ctrl+1":       lambda: self.ui.default_button.setChecked(True),
            "Ctrl+2":       lambda: self.ui.cas_button.setChecked(True),
            "Ctrl+3":       lambda: self.ui.sc_button.setChecked(True),
            "Ctrl+H":       lambda: self._change_panel(self.ui.history_panel),
            "Ctrl+T":       lambda: self._change_panel(self.ui.theme_panel),
            "Ctrl+Shift+T": self._copy_picker_color,
            "Ctrl+Shift+D": lambda: self.ui.dark.setChecked(True),
            "Ctrl+Shift+L": lambda: self.ui.light.setChecked(True),
            "Ctrl+K":       lambda: self.ui.constants.setChecked(not self.ui.constants.isChecked()),
            "Ctrl+G":       lambda: self.ui.g.setChecked(not self.ui.g.isChecked()),
            "Ctrl+E":       lambda: self.ui.e.setChecked(not self.ui.e.isChecked()),
            "Ctrl+I":       lambda: self.ui.i.setChecked(not self.ui.i.isChecked())
        }

        for (key, connection) in key_map.items():
            QShortcut(QKeySequence(key), self).activated.connect(connection)
        return

    def _copy_picker_color(self) -> None:
        return self.clipboard.setText(self.ui.color_line.text())

    def _choose_theme_mode(self, mode: str):
        if self.ui.mode == mode: return
        match mode:
            case "dark" | "light":
                self.ui.color_form.lock_boxes(True)
            case "custom":
                self.ui.color_form.lock_boxes(False)
        
        self.ui.load_style(mode)
        self.ui.color_form.set_box_colors([QColor(color) for color in self.ui.theme_manager.get_section(mode).values()])
        return

    def _copy_text(self):
        _in = self.ui.i_text_edit.toPlainText()
        _out = self.ui.o_text_edit.toPlainText()
        self.clipboard.setText(_out)
        if _out:
            self.history_manager.append([_in, _out])
            self.ui.history_scroll.append(_in, _out)
        return
    
    def _paste_text(self):
        self.ui.i_text_edit.setPlainText(QApplication.clipboard().text())
        return

    def _quick_translate(self):
        self._paste_text()
        self._copy_text()
        return

    def _start_translation(self):
        translation = translate(
            self.ui.i_text_edit.toPlainText(),
            TI_on=self.ui.cas_button.isChecked(),
            SC_on=self.ui.sc_button.isChecked(),
            constants_on=self.ui.constants.isChecked(),
            g_on=self.ui.g.isChecked(),
            i_on=self.ui.i.isChecked(),
            e_on=self.ui.e.isChecked()
        )
        
        if self.ui.coul.isChecked():
            translation = translation.replace("k", "_Cc")

        for macro in self.ui.macro_table.get_data():
            if macro[2] and macro[0] != "":
                translation = translation.replace(macro[0], macro[1])
        self.ui.o_text_edit.setPlainText(translation)
        self._start_animation(self._animate_progressbar)
        try:
            self.ui.o_text_edit.setPlainText(self.ooga)
        except:
            pass
        return

    def _on_translation_mode_changed(self, btn, on):
        if on:
            self.translation_mode = btn.property("mode")
            self._start_translation()
        return
    
    def _update_macro_table(self, backup):
        self.macro_manager.update()
        try:
            self.ui.macro_table.set_data(self.macro_manager.data)
        except Exception:
            self.ui.macro_table.set_data(backup)
            new_error_box(self, "Invalid JSON structure. Changes not saved.")
        return

    def _toggle_macros(self, show: bool):
        self.ui.show_macros_button.setText("✕") if show else self.ui.show_macros_button.setText("☰")
        self.ui.macro_table.setVisible(show)
        self.ui.add_macro.setVisible(show)
        self.ui.open_macros_btn.setVisible(show)
        return

    def _toggle_legacy_controls(self, show: bool):
        self.ui.show_legacy.setText("✕") if show else self.ui.show_legacy.setText("☰")
        self.ui.constants.setVisible(show)
        self.ui.g.setVisible(show)
        self.ui.e.setVisible(show)
        self.ui.i.setVisible(show)
        return

    def _load_data(self):
        x, y = self.settings_manager.get_property("window", "position")
        w, h = self.settings_manager.get_property("window", "dimensions")
        self.setGeometry(x, y, w, h)
        split = self.settings_manager.get_property("window", "split")
        self.split = split
        toggle = self.ui.panel_toggle
        if split[0] == 0: toggle.setChecked(True)
        elif split[1] == 0: toggle.setChecked(False)
        else: toggle.setChecked(True)

        self.ui.splitter.setSizes(split)

        self.translation_mode = self.settings_manager.get_property("settings", "mode")
        for btn in self.ui.mode_button_group.buttons():
            if btn.property("mode") == self.translation_mode:
                btn.setChecked(True)

        self._toggle_legacy_controls(self.settings_manager.get_property("toggles", "legacy"))
        self._toggle_macros(self.settings_manager.get_property("toggles", "macros"))
        
        self.ui.constants.setChecked(self.settings_manager.get_property("legacy", "constants"))
        self.ui.g.setChecked(self.settings_manager.get_property("legacy", "g"))
        self.ui.e.setChecked(self.settings_manager.get_property("legacy", "e"))
        self.ui.i.setChecked(self.settings_manager.get_property("legacy", "i"))

        self.ui.history_scroll.append_list(self.history_manager.data)
        self.ui.macro_table.set_data(self.macro_manager.data)
        return

    def _save_data(self):
        self.ui.save_colors()
        self.history_manager.set_data(self.ui.history_scroll.get_history_data())
        
        s_manager = self.settings_manager
        geo = self.normalGeometry()

        s_manager.set_property("window", "position", [geo.x(), geo.y()])
        s_manager.set_property("window", "dimensions", [geo.width(), geo.height()])
        s_manager.set_property("window", "split", self.ui.splitter.sizes())
        
        s_manager.set_property("settings", "mode", self.translation_mode)

        s_manager.set_property("toggles", "macros", self.ui.macro_table.isVisible())
        s_manager.set_property("toggles", "legacy", self.ui.g.isVisible())

        s_manager.set_property("legacy", "g", self.ui.g.isChecked())
        s_manager.set_property("legacy", "e", self.ui.e.isChecked())
        s_manager.set_property("legacy", "i", self.ui.i.isChecked())
        s_manager.set_property("legacy", "constants", self.ui.constants.isChecked())

        s_manager.save_data()
        self.history_manager.save_data()
        self.macro_manager.save_data()
        return

    def _toggle_panel(self, show: bool):
        """Called when toggle_panel button is toggled"""
        splitter = self.ui.splitter
        toggle = self.ui.panel_toggle
        
        io_sz, panel_sz = splitter.sizes()
        if show:
            # set button text to hide panel
            toggle.setText("-")
            # splitter.setSizes(self.split)
            splitter.setSizes([0.5 * io_sz,  0.5 * io_sz])
        else:
            # set button text to show panel
            self.split = splitter.sizes()
            toggle.setText("+")
            splitter.setSizes([1, 0])

    def _change_panel(self, panel: QWidget):

        splitter = self.ui.splitter
        toggle = self.ui.panel_toggle
        minus = toggle.isChecked()
        plus = not minus

        # both panels showing
        if minus and splitter.widget(1) is panel:
            panel.setFocus()
            return

        io_sz, panel_sz = splitter.sizes()
        io_vis = io_sz > 0
        panel_vis = panel_sz > 0

        # if both vis
        if io_vis and panel_vis and splitter.widget(1) is not panel:
            self.split = splitter.sizes()
            splitter.replaceWidget(1, panel)
            splitter.setSizes(splitter.sizes()) # magik 
            panel.setFocus()
            return
        
        # only panel showing (- on toggle)
        if minus and not io_vis:
            splitter.replaceWidget(1, panel)
            panel.setFocus()
            return

        # if only io showing (+ on toggle)
        if plus:
            self.split = splitter.sizes()
            toggle.blockSignals(True)
            toggle.setChecked(True) # toggle to (-) change sign 
            toggle.setText("-")
            toggle.blockSignals(False)
            splitter.setSizes([0, 1]) # toggle changes sizes but this overrides them
            splitter.replaceWidget(1, panel)

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

    def _open_sub_window(self, sub_type: AboutWindow | InfoWindow | EditorWindow, *args, **kwargs):
        self.sub: QWidget = sub_type(self, *args, **kwargs)
        
        if isinstance(self.sub, AboutWindow):
            self.sub.exec()
        else:
            self.sub.show()
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

    def eventFilter(self, source, event) -> bool:
        if event.type() == QEvent.MouseButtonPress:
            self.clearFocus()
            # Set focus back to the main window
            self.setFocus(Qt.OtherFocusReason)  
            return True # Event handled
        return super().eventFilter(source, event)