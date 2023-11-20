import json

class JsonDictionaryManager:
    def __init__(self, json_filename):
        self.json_filename = json_filename
        self.data = None

    def load_dictionary_from_file(self):
        """
        Load an existing dictionary from a JSON file or create an empty one if the file doesn't exist.
        """
        try:
            with open(self.json_filename, "r") as file:
                self.data = json.load(file)
        except FileNotFoundError:
            print(f"{self.json_filename} not found, creating empty dictionary")
            self.data = {}

    def save_dictionary_to_file(self):
        """
        Save the dictionary to a JSON file.
        """
        if self.data is not None:
            with open(self.json_filename, "w") as file:
                json.dump(self.data, file)
    
    def set_value(self, key, value):
        """
        Set a key-value pair in the dictionary and save it to the JSON file.
        """
        self.data[key] = value
        self.save_dictionary_to_file()

    def get_value(self, key, default=None):
        """
        Get the value associated with a key in the dictionary.
        """
        return self.data.get(key, default)
    
    def delete_key(self, key):
        """
        Delete a key from the dictionary and save the updated dictionary to the JSON file.
        """
        if key in self.data:
            del self.data[key]
            self.save_dictionary_to_file()
