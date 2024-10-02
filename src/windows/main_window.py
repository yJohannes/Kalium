import asyncio

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import Qt, QPoint, QEvent

from ui.ui import WindowUI

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.app_ref = QApplication.instance()
        self.setGeometry(100, 100, 1000, 600)
        self.setWindowTitle("Detex")
        # self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint) # | Qt.WindowTitleHint)

        self.async_tasks = []

        self.ui = WindowUI()
        self.ui.init_ui(self)
        self._init_signals()
        return
    
    def _init_signals(self):
        tb = self.ui.toolbar
        tb.mousePressEvent   = self.drag_start
        tb.mouseMoveEvent    = self.drag
        tb.mouseReleaseEvent = self.drag_end
        
        self.ui.minimize.clicked.connect(self.showMinimized)
        self.ui.close.clicked.connect(self.close)

        ie_ref = self.ui.i_text_edit
        ie_ref.keyPressEvent = lambda event: self._tab_event(ie_ref, event)
        ie_ref.textChanged.connect(lambda: self.start_animation(self.animate_progressbar))

        oe_ref = self.ui.o_text_edit
        oe_ref.keyPressEvent = lambda event: self._tab_event(oe_ref, event)


    def start_animation(self, animation: "function"):
        loop = asyncio.get_event_loop()

        for task in self.async_tasks:
            if not task.done():
                task.cancel()
            self.async_tasks.remove(task)

        new_task = loop.create_task(animation())
        self.async_tasks.append(new_task)

        print(self.async_tasks)
        return 

    async def animate_progressbar(self):
        def ease_out(t, end, degree):
            return int(t ** degree / end ** (degree - 1))

        try:
            await asyncio.sleep(0.1)
            for t in range(101):
                self.ui.progressbar.setValue(ease_out(t, 100, 4))
                await asyncio.sleep(0.0025)
            await asyncio.sleep(0.2)
    
            self.ui.progressbar.setLayoutDirection(Qt.RightToLeft)

            for t in range(100, -1, -1):
                self.ui.progressbar.setValue(ease_out(t, 100, 4))
                await asyncio.sleep(0.002)

            self.ui.progressbar.setValue(0)
            self.ui.progressbar.setLayoutDirection(Qt.LeftToRight)
            
        except asyncio.CancelledError:
            self.ui.progressbar.setValue(0)
            self.ui.progressbar.setLayoutDirection(Qt.LeftToRight)
            raise

    def _tab_event(self, window_widget, event: QEvent):
        if event.key() == Qt.Key_Tab:
            self.focusNextChild()
            event.accept()
            
        elif event.key() == Qt.Key_Backtab:
            self.focusPreviousChild()
            event.accept()
        else:
            # For all other keys, call the base class implementation
            type(window_widget).keyPressEvent(window_widget, event)

    def drag_start(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = event.globalPos()
        return super(QMainWindow, self).mousePressEvent(event)

    def drag(self, event):
        if self.old_pos is not None and not self.ui.toolbar.isFloating():
            delta = QPoint(event.globalPos() - self.old_pos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPos()
        return super(QMainWindow, self).mouseMoveEvent(event)

    def drag_end(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = None
        return super(QMainWindow, self).mouseReleaseEvent(event)
