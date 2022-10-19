"""Controller for terminal panel."""
from xdg.BaseDirectory import xdg_config_home
import yaml

_CONFIG_FILE = f"{xdg_config_home}/blaze/terminal.yaml"

_CURSOR_BLINK_CONFIG = "cursor.blink"
_CURSOR_SHAPE_CONFIG = "cursor.shape"
_FONT_NAME_CONFIG = "fonts.font_family"
_FONT_SIZE_CONFIG = "fonts.font_size"

_CONFIRM_WINDOW_CLOSE_CONFIG = "misc.confirm_os_window_close"


class Controller:
    """Controller for terminal panel."""
    def __init__(self, config_file=_CONFIG_FILE):
        with open(config_file, 'r', encoding="utf-8") as file:
            self.config = yaml.safe_load(file)

        self.cursor_shapes = ["block", "beam", "underline"]


    def _set(self, path, value):
        """Sets value for key in config file and saved it."""
        keys = path.split('.')

        config = self.config
        for key in keys[:-1]:
            config = config[key]

        config[keys[-1]] = value

        with open(_CONFIG_FILE, 'w', encoding="utf-8") as file:
            yaml.safe_dump(self.config, file, default_flow_style=False)


    def _get(self, path):
        """Gets value for key in config file"""
        keys = path.split('.')

        config = self.config
        for key in keys:
            config = config[key]

        return config

    def get_cursor_blink(self):
        """Get cursor blink."""
        return self._get(_CURSOR_BLINK_CONFIG)

    def get_cursor_shape(self):
        """Get cursor shape."""
        return self._get(_CURSOR_SHAPE_CONFIG)

    def get_confirm_window_close(self):
        """Get confirm window close."""
        return self._get(_CONFIRM_WINDOW_CLOSE_CONFIG)

    def get_font(self):
        """Get font."""
        return self._get(_FONT_NAME_CONFIG), self._get(_FONT_SIZE_CONFIG)

    def set_cursor_blink(self, value):
        """Set cursor blink."""
        self._set(_CURSOR_BLINK_CONFIG, value)

    def set_cursor_shape(self, value):
        """Set cursor shape."""
        self._set(_CURSOR_SHAPE_CONFIG, value)

    def set_confirm_window_close(self, value):
        """Set confirm window close."""
        self._set(_CONFIRM_WINDOW_CLOSE_CONFIG, value)

    def set_font(self, font_name, font_size):
        """Set font."""
        self._set(_FONT_NAME_CONFIG, font_name)
        self._set(_FONT_SIZE_CONFIG, font_size)
