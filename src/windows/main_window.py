import os
import asyncio

from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6.QtCore import Qt, QPoint, QSize, QEvent
from PySide6.QtGui import QClipboard, QKeySequence, QShortcut, QIcon

from ui.ui import WindowUI
from windows.sub_windows import AboutWindow, InfoWindow
from utils.json_manager import JSONManager
from kalium.engine import translate

class MainWindow(QMainWindow):
    clipboard = QClipboard()
    async_tasks = []


    def __init__(self):
        super().__init__()
        QApplication.instance().setAttribute(Qt.AA_EnableHighDpiScaling)
        self.setWindowTitle("Kalium")
        cwd = os.path.dirname(__file__)
        
        icon_path = os.path.join(cwd, '..', '..', 'img', 'logo2.png')
        icon = QIcon(icon_path) # Noto Sans Bold 270
        QApplication.instance().setWindowIcon(icon)
    
        settings = os.path.join(cwd, '..', '..', 'config', 'settings.json')
        history = os.path.join(cwd, '..', '..', 'data', 'history.json')

        self.settings_manager = JSONManager(settings)
        self.history_manager = JSONManager(history)

        x, y = self.settings_manager.get_property("window", "position")
        w, h = self.settings_manager.get_property("window", "dimensions")

        self.setGeometry(x, y, w, h)


        self.ui = WindowUI()
        self.ui.init_ui(self)
        self._init_signals()
        return
    
    def _init_signals(self):
        tb = self.ui.toolbar
        tb.mousePressEvent   = self.drag_start
        tb.mouseMoveEvent    = self.drag
        tb.mouseReleaseEvent = self.drag_end
        
        ie_ref = self.ui.i_text_edit
        oe_ref = self.ui.o_text_edit
        me_ref = self.ui.macro_edit
        
        ie_ref.keyPressEvent = lambda event: self.tab_event(ie_ref, event)
        oe_ref.keyPressEvent = lambda event: self.tab_event(oe_ref, event)
        me_ref.keyPressEvent = lambda event: self.tab_event(me_ref, event)

        def start_translation(expr):
            translation = translate(expr, TI_on=self.ui.cas_button.isChecked(), SC_on=self.ui.sc_button.isChecked())
            oe_ref.setPlainText(translation)
            self._start_animation(self._animate_progressbar)

        ie_ref.textChanged.connect(lambda: start_translation(ie_ref.toPlainText()))
        # self.ui.cas_button.pressed.connect(lambda: start_translation(ie_ref.toPlainText()))
        # self.ui.sc_button.pressed.connect(lambda: start_translation(ie_ref.toPlainText()))

        self.ui.mode_button_group.buttonToggled.connect(lambda: start_translation(ie_ref.toPlainText()))

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

        show_macros = lambda: (
            me_ref.setVisible(not me_ref.isVisible()),
            self.ui.macro_field.updateGeometry(),
            self.ui.show_macros_button.setText("✕") if me_ref.isVisible() else self.ui.show_macros_button.setText("☰"),
        )

        self.ui.show_macros_button.clicked.connect(show_macros)

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
        self.ui.color_picker.colorChanged.connect(lambda color: (
            self.ui.color_form.setBoxColor(color),
            self.ui.color_line.setText(color.name())
        ))
        
        self.ui.color_form.boxPressed.connect(lambda box: self.ui.color_picker.setColor(self.ui.color_form.getBoxColor(box)))

        def dwd(target, color):
            self.ui.theme_manager.set_property("custom", target, color.name())
            self.ui.request_style_update()

        self.ui.color_form.colorChanged.connect(dwd)

        def choose_mode(mode: str):
            if self.ui.mode == mode: return
            match mode:
                case "dark" | "light":
                    self.ui.color_form.lock_boxes(True)
                    self.ui.load_style(mode)
                case "custom":
                    self.ui.color_form.lock_boxes(False)
                    self.ui.load_style(mode)
            return

        self.ui.dark.clicked.connect(lambda: choose_mode("dark"))
        self.ui.light.clicked.connect(lambda: choose_mode("light"))
        self.ui.custom.clicked.connect(lambda: choose_mode("custom"))

        def load_history_text(data):
            self.ui.i_text_edit.blockSignals(True)
            self.ui.i_text_edit.setPlainText(data[0])
            self.ui.o_text_edit.setPlainText(data[1])
            self.ui.i_text_edit.blockSignals(False)
            return

        self.ui.history_scroll.append_list(self.history_manager.data)

        self.ui.history_scroll.itemPressed.connect(load_history_text)
        self.ui.history_scroll.historyCleared.connect(lambda: self.ui.history_del.setChecked(False))
        self.ui.history_del.toggled.connect(self.ui.history_scroll.deleting_mode)
        self.ui.history_clear.pressed.connect(self.ui.history_scroll.clear)

        key_map = {
            "Ctrl+Shift+C": copy,
            "Ctrl+R": copy,
            "Ctrl+P": paste,
            "Ctrl+Q": quick,
            "Ctrl+,": open_settings,
            "Ctrl+O": open_settings,
            "Ctrl+H": open_history,
            "Ctrl+T": open_theme,
            "Ctrl+K": copy_color
        }

        for (key, connection) in key_map.items():
            QShortcut(QKeySequence(key), self).activated.connect(connection)

        self.installEventFilter(self)
        self.setFocus()

        
        return
    
    def _save_all(self):
        self.ui.save_colors()
        self.history_manager.set_data(self.ui.history_scroll.get_history_data())
        
        geo = self.normalGeometry()
        self.settings_manager.set_property("window", "position", [geo.x(), geo.y()])
        self.settings_manager.set_property("window", "dimensions", [geo.width(), geo.height()])
        
        # make a class for kalium 
        # mode = self.ui.mode_button_group.checkedButton().text().lower() # make btn have a property instead of this

        # self.settings_manager.set_property("settings", "mode", mode)
        self.settings_manager.save_data()




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

    def _open_sub_window(self, sub_type: AboutWindow | InfoWindow):
        self.sub: QWidget = sub_type(self)
        
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
        self._save_all()
        event.accept()