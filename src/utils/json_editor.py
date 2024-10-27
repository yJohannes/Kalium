import json

from PySide6.QtCore import Qt, QRegularExpression, QSize, QRect
from PySide6.QtGui import QColor, QTextCharFormat, QSyntaxHighlighter, QTextFormat, QPainter, QFontMetrics, QTextCursor
from PySide6.QtWidgets import QPlainTextEdit, QTextEdit, QWidget

try:
    from utils.json_manager import JSONManager
except:
    from json_manager import JSONManager

class SyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.default = QTextCharFormat()
        self.default.setForeground(QColor("#FFFFFF"))

        self.keyword_purple = QTextCharFormat()
        self.keyword_purple.setForeground(QColor("#C586E0"))

        self.keyword_blue = QTextCharFormat()
        self.keyword_blue.setForeground(QColor("#569CD6"))

        self.string = QTextCharFormat()
        self.string.setForeground(QColor("#CE9178"))

        self.number = QTextCharFormat()
        self.number.setForeground(QColor("#B5CEA8"))

        self.bool = QTextCharFormat()
        self.bool.setForeground(QColor("#569CD6"))

        self.null = QTextCharFormat()
        self.null.setForeground(QColor("#569CD6"))

        self.comment = QTextCharFormat()
        self.comment.setForeground(QColor("#6A6A6A"))

        self.py_kw_purple = [
            'False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await',
            'break', 'class', 'continue', 'def', 'del', 'elif', 'else',
            'except', 'finally', 'for', 'if', 'import', 'is', 'lambda',
            'raise', 'return', 'try', 'while', 'with', 'yield'
        ]

        self.py_kw_blue = [
            'global', 'nonlocal', 'not', 'or', 'in', 'pass'
        ]

    def highlightBlock(self, text):
        self.setFormat(0, len(text), self.default)
        patterns = [
            (self.keyword_purple, QRegularExpression(fr'\b({"|".join(self.py_kw_purple)})\b')),
            (self.keyword_blue, QRegularExpression(fr'\b({"|".join(self.py_kw_blue)})\b')),
            (self.string,  QRegularExpression(r'"([^"\\]*(\\.[^"\\]*)*)"')),
            (self.number,  QRegularExpression(r'\b[0-9]+(\.[0-9]+)?\b')),
            (self.bool,    QRegularExpression(r'\b(true|false)\b')),
            (self.null,    QRegularExpression(r'\bnull\b')),
            (self.comment, QRegularExpression(r'//.*|/\*[\s\S]*?\*/'))
        ]

        for format, pattern in patterns:
            iterator = pattern.globalMatch(text)
            while iterator.hasNext():
                match = iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), format)

class CodeEditorOld(QPlainTextEdit):
    def __init__(self, file_path: str):
        super().__init__()
        self.file_path = file_path
        self.json_manager = JSONManager(file_path)
        self.highlighter = SyntaxHighlighter(self.document())
        self.setStyleSheet(self.styleSheet() + "background-color: #1f1f1f; outline: none; border: none;")
        self._load_json()
        self.cursorPositionChanged.connect(self.highlight_current_line)

    def _load_json(self):
        data = self.json_manager.get_data()
        self.setPlainText(json.dumps(data, indent=4))
    
    def save_file(self):
        json_data: dict | list = json.loads(self.toPlainText())
        self.json_manager.set_data(json_data)
        self.json_manager.save_data()

    def highlight_current_line(self):
        extraSelections = []
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            highlight = QColor("#262626")
            selection.format.setBackground(highlight)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)            
            # Create a cursor and clear the selection for full line highlighting
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)
        self.setExtraSelections(extraSelections)

class JSONEditor(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        tab_spaces = 6
        self.setTabStopDistance(tab_spaces * self.fontMetrics().horizontalAdvance(' '))

        self.line_number_area = NumberLine(self)
        self.padding_left = 10
        self.padding_right = 2

        # Set initial highlight
        self.highlighted_line = -1
        self.line_highlight_color        = QColor("#262626")
        self.line_number_color           = QColor("Gray")
        self.highlight_line_number_color = QColor("#FFFFFF")

        self.json_manager = JSONManager()
        self.highlighter = SyntaxHighlighter(self.document())
        self.setStyleSheet(self.styleSheet() + "background-color: #1f1f1f; outline: none; border: none;")
        self.cursorPositionChanged.connect(self.highlight_current_line)

        # Initialize viewport margin and sync signals
        self.update_line_number_area_width(0)
        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.cursorPositionChanged.connect(self.highlight_current_line)
        return

    def load_json(self, path):
        data = self.json_manager.load_data(path)
        self.setPlainText(json.dumps(data, indent="\t"))
    
    def save_json(self):
        json_data: dict | list = json.loads(self.toPlainText())
        self.json_manager.set_data(json_data)
        self.json_manager.save_data()

    def line_number_area_width(self):
        digits = len(str(max(1, self.blockCount())))
        space = 10 + self.fontMetrics().horizontalAdvance('9') * digits + self.padding_left+ self.padding_right
        return space

    def update_line_number_area_width(self, _):
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    def update_line_number_area(self, rect, dy):
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())
        
        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        
        # Resize the line number area widget
        cr = self.contentsRect()
        self.line_number_area.setGeometry(QRect(cr.left(), cr.top(), self.line_number_area_width(), cr.height()))

    def highlight_current_line(self):
        extraSelections = []
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            selection.format.setBackground(self.line_highlight_color)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            # Create a cursor and clear the selection for full line highlighting
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)
        self.setExtraSelections(extraSelections)

    def line_number_area_paint_event(self, event):
        painter = QPainter(self.line_number_area)
        painter.fillRect(event.rect(), QColor("#2B2B2B"))

        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + int(self.blockBoundingRect(block).height())
        font_height = QFontMetrics(self.font()).height()

        # Determine the current line number for highlighting
        current_line = self.textCursor().blockNumber()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)

                # Set color based on whether it’s the current line
                if block_number == current_line:
                    painter.setPen(self.highlight_line_number_color)
                else:
                    painter.setPen(self.line_number_color)

                painter.drawText(
                    -self.padding_right, top, self.line_number_area.width() - 5,font_height,
                    Qt.AlignRight, number
                )
            block = block.next()
            top = bottom
            bottom = top + int(self.blockBoundingRect(block).height())
            block_number += 1

    def block_at_y(self, y):
        """Return the block number at the given y-coordinate."""
        block = self.firstVisibleBlock()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        while block.isValid() and top <= y:
            if top + self.blockBoundingRect(block).height() > y:
                return block.blockNumber()
            block = block.next()
            top += self.blockBoundingRect(block).height()
        return -1

    def select_line(self, block_number):
        """Select the entire line corresponding to the block_number."""
        if block_number < 0:
            return

        cursor = self.textCursor()
        block = self.document().findBlockByNumber(block_number)
        cursor.setPosition(block.position())
        cursor.movePosition(QTextCursor.EndOfBlock, QTextCursor.KeepAnchor)

        self.setTextCursor(cursor)

    def select_lines(self, start_block_number, end_block_number):
        """Select multiple lines from start_block_number to end_block_number."""
        if start_block_number < 0 or end_block_number < 0:
            return

        # Adjust for dragging up or down
        if end_block_number < start_block_number:
            start_block_number, end_block_number = end_block_number, start_block_number

        # Create a cursor from the start to the end block
        cursor = self.textCursor()
        start_block = self.document().findBlockByNumber(start_block_number)
        end_block = self.document().findBlockByNumber(end_block_number)
        cursor.setPosition(start_block.position())
        cursor.setPosition(end_block.position() + end_block.length() - 1, QTextCursor.KeepAnchor)

        self.setTextCursor(cursor)


class NumberLine(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.code_editor = editor
        self.start_block_number = None  # Track the starting line for multi-line selection

    def sizeHint(self):
        return QSize(self.code_editor.line_number_area_width(), 0)

    def paintEvent(self, event):
        self.code_editor.line_number_area_paint_event(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # Set the starting line for selection
            self.start_block_number = self.code_editor.block_at_y(event.pos().y())
            self.code_editor.select_line(self.start_block_number)

    def mouseMoveEvent(self, event):
        # Update selection if dragging
        if self.start_block_number is not None:
            end_block_number = self.code_editor.block_at_y(event.pos().y())
            self.code_editor.select_lines(self.start_block_number, end_block_number)

    def mouseReleaseEvent(self, event):
        # Reset start_block_number on release
        self.start_block_number = None

if __name__ == "__main__":
    import sys
    import os
    from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QLabel
    app = QApplication(sys.argv)

    cwd = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(cwd, "..", "..", "data", "macros.json")

    editor = JSONEditor()
    editor.load_json(json_path)
    editor.show()


    sys.exit(app.exec())
