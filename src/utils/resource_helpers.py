import os
import sys

def exe_dir_path(relative_path):
    relative_path = relative_path.replace("/", "\\")

    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def resource_path(relative_path):
    """Get absolute path to resource in dev and in exe"""
    relative_path = relative_path.replace("/", "\\")
    try:
        # PyInstaller creates a temp folder and stores the path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def load_and_concatenate(folder_path) -> str:
    content = ""
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                content += file.read() + "\n"
    
    return content