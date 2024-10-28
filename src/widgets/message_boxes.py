from PySide6.QtWidgets import QMessageBox

def new_message_box(parent, title: str, text: str, buttons_flag: int, default_flag: int):
        q = QMessageBox(parent)
        q.setWindowTitle(title)
        q.setText(text)
        q.setStandardButtons(buttons_flag)
        q.setDefaultButton(default_flag)
        q.setIcon(QMessageBox.NoIcon)
        return q.exec()

def new_error_box(parent, error_msg):
    return new_message_box(parent, "Error", error_msg, QMessageBox.Ok, QMessageBox.Ok)
