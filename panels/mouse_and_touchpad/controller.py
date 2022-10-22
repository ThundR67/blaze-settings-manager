"""Controller for mouse and touchpad panel."""
from xdg.BaseDirectory import xdg_config_home
import yaml

_CONFIG_FILE = f"{xdg_config_home}/blaze/mouse_and_touchpad.yaml"

# General config.
_PRIMARY_BUTTON_CONFIG = "general.primary_button"

# Mouse config.
_MOUSE_SPPEED_CONFIG = "mouse.speed"
_MOUSE_NATURAL_SCROLLING_CONFIG = "mouse.natural_scrolling"

# Touchpad config.
_TOUCHPAD_ENABLED_CONFIG = "touchpad.enabled"
_TOUCHPAD_EDGE_SCROLLING_CONFIG = "touchpad.edge_scrolling"
_TOUCHPAD_NATURAL_SCROLLING_CONFIG = "touchpad.natural_scrolling"
_TOUCHPAD_TAP_TO_CLICK_CONFIG = "touchpad.tap_to_click"
_TOUCHPAD_SPEED_CONFIG = "touchpad.speed"
_TOUCHPAD_TWO_FINGER_SCROLLING_CONFIG = "touchpad.two_finger_scrolling"

_PRIMARY_BUTTONS = ["left", "right"]

class Controller:
    """Controller for mouse and touchpad panel."""
    def __init__(self, config_file=_CONFIG_FILE):
        with open(config_file, 'r', encoding="utf-8") as file:
            self.config = yaml.safe_load(file)

        self.primary_buttons = _PRIMARY_BUTTONS

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

    def set_primary_button(self, value):
        """Sets primary button."""
        self._set(_PRIMARY_BUTTON_CONFIG, value)

    def get_primary_button(self):
        """Returns primary button."""
        return self._get(_PRIMARY_BUTTON_CONFIG)

    def set_mouse_speed(self, value):
        """Sets mouse speed."""
        self._set(_MOUSE_SPPEED_CONFIG, value)

    def get_mouse_speed(self):
        """Returns mouse speed."""
        return self._get(_MOUSE_SPPEED_CONFIG)

    def set_mouse_natural_scrolling(self, value):
        """Sets mouse natural scrolling."""
        self._set(_MOUSE_NATURAL_SCROLLING_CONFIG, value)

    def get_mouse_natural_scrolling(self):
        """Returns mouse natural scrolling."""
        return self._get(_MOUSE_NATURAL_SCROLLING_CONFIG)

    def set_touchpad_enabled(self, value):
        """Sets touchpad enabled."""
        self._set(_TOUCHPAD_ENABLED_CONFIG, value)

    def get_touchpad_enabled(self):
        """Returns touchpad enabled."""
        return self._get(_TOUCHPAD_ENABLED_CONFIG)

    def set_touchpad_edge_scrolling(self, value):
        """Sets touchpad edge scrolling."""
        self._set(_TOUCHPAD_EDGE_SCROLLING_CONFIG, value)

    def get_touchpad_edge_scrolling(self):
        """Returns touchpad edge scrolling."""
        return self._get(_TOUCHPAD_EDGE_SCROLLING_CONFIG)

    def set_touchpad_natural_scrolling(self, value):
        """Sets touchpad natural scrolling."""
        self._set(_TOUCHPAD_NATURAL_SCROLLING_CONFIG, value)

    def get_touchpad_natural_scrolling(self):
        """Returns touchpad natural scrolling."""
        return self._get(_TOUCHPAD_NATURAL_SCROLLING_CONFIG)

    def set_touchpad_tap_to_click(self, value):
        """Sets touchpad tap to click."""
        self._set(_TOUCHPAD_TAP_TO_CLICK_CONFIG, value)

    def get_touchpad_tap_to_click(self):
        """Returns touchpad tap to click."""
        return self._get(_TOUCHPAD_TAP_TO_CLICK_CONFIG)

    def set_touchpad_speed(self, value):
        """Sets touchpad speed."""
        self._set(_TOUCHPAD_SPEED_CONFIG, value)

    def get_touchpad_speed(self):
        """Returns touchpad speed."""
        return self._get(_TOUCHPAD_SPEED_CONFIG)

    def set_touchpad_two_finger_scrolling(self, value):
        """Sets touchpad two finger scrolling."""
        self._set(_TOUCHPAD_TWO_FINGER_SCROLLING_CONFIG, value)

    def get_touchpad_two_finger_scrolling(self):
        """Returns touchpad two finger scrolling."""
        return self._get(_TOUCHPAD_TWO_FINGER_SCROLLING_CONFIG)
