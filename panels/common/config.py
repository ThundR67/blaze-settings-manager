"""Module to manages reading and writting to BlazeDE's config file."""
from xdg.BaseDirectory import xdg_config_home
import yaml

class Config:
    """Manages reading and writting to BlazeDE's config file."""
    def __init__(self, config_name):
        self.config_file = f"{xdg_config_home}/blaze/{config_name}.yaml"

        with open(self.config_file, 'r', encoding="utf-8") as file:
            self.config = yaml.safe_load(file)

    def set(self, path, value):
        """
        Sets value at @path of @self.config to @ value.
        @path is a string of keys separated by a dot.
        For example, if @self.config is:
        {
            "a": {
                "b": {
                    "c": 1
                }
            }
        }
        and @path is "a.b.c", this function will set @self.config["a"]["b"]["c"] to @value.
        """
        keys = path.split('.')

        config = self.config
        for key in keys[:-1]:
            config = config[key]

        config[keys[-1]] = value

    def get(self, path):
        """
        Returns value at @path of @self.config
        @path is a string of keys separated by a dot.
        For example, if @self.config is:
        {
            "a": {
                "b": {
                    "c": 1
                }
            }
        }
        and @path is "a.b.c", this function will return value of @self.config["a"]["b"]["c"].
        """
        config = self.config
        for key in path.split('.'):
            config = config[key]

        return config

    def save(self):
        """Saves the config file"""
        with open(self.config_file, 'w', encoding="utf-8") as file:
            yaml.safe_dump(self.config, file, default_flow_style=False)
