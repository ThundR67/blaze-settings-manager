"""Module to manage connection to blaze config file"""
from xdg.BaseDirectory import xdg_config_home
import yaml

_CONFIG_FILE = f"{xdg_config_home}/blaze/config.yaml"

class Config:
    """Manages connection to config file"""
    def __init__(self, config_file=_CONFIG_FILE):
        with open(config_file, 'r', encoding="utf-8") as file:
            self.config = yaml.safe_load(file)

    def set(self, path, value):
        """Sets value for key in config file"""
        keys = path.split('.')

        config = self.config
        for key in keys[:-1]:
            config = config[key]

        config[keys[-1]] = value

    def get(self, path):
        """Gets value for key in config file"""
        keys = path.split('.')

        config = self.config
        for key in keys:
            config = config[key]

        return config

    def save(self):
        """Saves config file"""
        with open(_CONFIG_FILE, 'w', encoding="utf-8") as file:
            yaml.safe_dump(self.config, file, default_flow_style=False)
