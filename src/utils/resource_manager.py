import os

def load_and_concatenate(folder_path) -> str:
    content = ""
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                content += file.read() + "\n"
    
    return content