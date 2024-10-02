import os

from PySide6.QtGui import QIcon

class StyleManager:
    def load_icon(self, icon_path) -> QIcon:
        return QIcon(icon_path)

    def load_styles(self, folder_path) -> str:
        stylesheet = ""
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                with open(file_path, 'r') as file:
                    stylesheet += file.read() + "\n"  # Concatenate stylesheets
        
        return stylesheet
    