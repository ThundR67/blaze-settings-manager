"""Panel to customize the terminal."""
from dataclasses import dataclass
import gi

gi.require_version(namespace='Gtk', version='4.0')
gi.require_version(namespace='Adw', version='1')

from gi.repository import Adw, Gtk

from . import constants
from ..common import preference, config

class Terminal:
    """Panel to customize terminal."""
    def __init__(self):
        self.config = config.Config(constants.CONFIG_NAME)

        self.name = constants.PANEL_NAME
        self.icon = constants.PANEL_ICON
        self.widget = Adw.Bin.new()

        page = Adw.PreferencesPage.new()
        page.add(self.text_group())

        self.widget.set_child(page)

    def text_group(self):
        """Return the text group."""
        group = Adw.PreferencesGroup.new()
        group.set_title("Appearance")

        # Font selector.
        font_selector = preference.Preference(
            preference.PreferenceType.FONT,
            "Font",
            constants.FONT_NAME_PATH,
            self.config,
        )

        # Cursor shape selector.
        cursor_shape_selector = preference.Preference(
            preference.PreferenceType.DROPDOWN,
            "Cursor shape",
            constants.CURSOR_SHAPE_PATH,
            self.config,
            values=constants.CURSOR_SHAPES,
        )

        # Cursor blink selector.
        cursor_blink_selector = preference.Preference(
            preference.PreferenceType.SWITCH,
            "Cursor blink",
            constants.CURSOR_BLINK_PATH,
            self.config,
        )

        # Confirm window close selector.
        confirm_selector = preference.Preference(
            preference.PreferenceType.SWITCH,
            "Enable confirmation dialoge when closing",
            constants.CONFIRM_WINDOW_CLOSE_PATH,
            self.config,
        )

        group.add(font_selector.get_widget())
        group.add(cursor_shape_selector.get_widget())
        group.add(cursor_blink_selector.get_widget())
        group.add(confirm_selector.get_widget())

        return group
