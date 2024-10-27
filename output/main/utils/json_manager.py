import json
import os

class JSONManager():
    def __init__(self, filepath=None):
        self.filepath = filepath
        if self.filepath:
            self.data: dict | list = self.load_data(self.filepath)
        return
    
    def update(self):
        self.data = self.load_data(self.filepath)
    
    def set_data(self, data):
        self.data = data
        return
    
    def set_data_from_file(self, path) -> None:
        self.data = self.load_data(path)
        return
    
    def append(self, data):
        """if list append data to it"""
        self.data.append(data)

    def remove(self, index):
        """if list remove data at index"""
        del self.data[index]
    
    def get_data(self):
        return self.data

    def load_data(self, path):
        self.filepath = path
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as file:
                return json.load(file)
        else:
            self._create_default_data_file()
            return self.load_data()

    def save_data(self) -> None:
        """Method for writing to data file."""
        with open(self.filepath, 'w', encoding='utf-8') as file:
            json.dump(self.data, file, indent='\t')
        return

    def set_section(self, section: str, value) -> None:
        if section in self.data:
            self.data[section] = value
        return
    
    def get_section(self, section: str) -> list | dict:
        if section in self.data:
            return self.data[section]

    def set_property(self, section: str, key: str, value) -> None:
        """General method to update any setting. DOES NOT SAVE THE FILE"""
        if section in self.data and key in self.data[section]:
            self.data[section][key] = value
            return
        else:
            raise KeyError(f"Invalid property: {section}.{key}")

    def get_property(self, section: str, key: str):
        if section in self.data and key in self.data[section]:
            return self.data[section][key]
        else:
            raise KeyError(f"Invalid property: {section}.{key}")

    def set_default_data(self, data: str):
        self.default_data = data
        return

    def _create_default_data_file(self) -> None:
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        with open(self.filepath, 'w', encoding='utf-8') as json_file:
            json.dump(self.default_data, json_file, indent='\t')
        return