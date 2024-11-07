import yaml
import os

class Config:
    def __init__(self, config_file='config/config.yaml'):
        self.config_file = config_file
        self.load_config()

    def load_config(self):
        if not os.path.exists(self.config_file):
            raise FileNotFoundError(f"Configuration file '{self.config_file}' not found.")

        with open(self.config_file, 'r') as file:
            try:
                self.config = yaml.safe_load(file)
            except yaml.YAMLError as e:
                raise Exception(f"Error parsing the configuration file: {e}")

    def get(self, key, default=None):
        return self.config.get(key, default)

    def reload(self):
        self.load_config()

    # Methods to retrieve supported formats
    def get_supported_image_formats(self):
        return self.config.get('supported_image_formats', [])

    def get_supported_video_formats(self):
        return self.config.get('supported_video_formats', []) 