"""Panel to customize the terminal."""
from dataclasses import dataclass
import gi

gi.require_version(namespace='Gtk', version='4.0')
gi.require_version(namespace='Adw', version='1')

from gi.repository import Adw, Gtk, Gdk

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
        page.add(self.sound_group())
        page.add(self.color_group())
        page.add(self.color_pallete_group())

        self.widget.set_child(page)

    def text_group(self):
        """Return the text group."""
        group = Adw.PreferencesGroup.new()
        group.set_title("Appearance")

        # Font selector.
        font_selector = preference.Preference(
            preference.PreferenceType.FONT,
            "Font",
            constants.FONT_PATH,
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

    def sound_group(self):
        """Return the sound group."""
        group = Adw.PreferencesGroup.new()
        group.set_title("Sound")

        # Bell selector.
        bell_selector = preference.Preference(
            preference.PreferenceType.SWITCH,
            "Enable terminal bell",
            constants.BELL_PATH,
            self.config,
        )

        group.add(bell_selector.get_widget())

        return group

    def color_group(self):
        """Return the color group."""
        group = Adw.PreferencesGroup.new()
        group.set_title("Colors")

        background_selector = preference.Preference(
            preference.PreferenceType.COLOR,
            "Background",
            constants.BACKGROUND_COLOR_PATH,
            self.config,
        )

        foreground_selector = preference.Preference(
            preference.PreferenceType.COLOR,
            "Foreground",
            constants.FOREGROUND_COLOR_PATH,
            self.config,
        )

        cursor_selector = preference.Preference(
            preference.PreferenceType.COLOR,
            "Cursor",
            constants.CURSOR_COLOR_PATH,
            self.config,
        )

        cursor_text_selector = preference.Preference(
            preference.PreferenceType.COLOR,
            "Cursor text",
            constants.CURSOR_TEXT_COLOR_PATH,
            self.config,
        )


        group.add(background_selector.get_widget())
        group.add(foreground_selector.get_widget())
        group.add(cursor_selector.get_widget())
        group.add(cursor_text_selector.get_widget())

        return group

    def color_pallete_group(self):
        """Return the color pallete group."""
        group = Adw.PreferencesGroup.new()
        group.set_title("Color Pallete")

        clamp = Adw.Clamp.new()
        clamp.set_css_classes(["card"])



        column = Gtk.FlowBox.new()
        column.set_css_classes(["box"])
        column.set_selection_mode(Gtk.SelectionMode.NONE)
        column.set_max_children_per_line(8)
        column.set_min_children_per_line(8)
        column.set_homogeneous(True)
        column.set_activate_on_single_click(True)

        column.set_margin_top(12)
        column.set_margin_bottom(12)
        column.set_margin_start(12)
        column.set_margin_end(12)

        for index in range(16):
            color = self.config.get(
                f"{constants.COLOR_PALLETE_PATH}{index}"
            )
            rbga = Gdk.RGBA()
            rbga.parse(color)

            widget = Gtk.ColorButton.new()
            widget.set_rgba(rbga)
            widget.connect("color-set", self.on_color_set, index)

            column.append(widget)

        clamp.set_child(column)

        group.add(clamp)
        return group

    def on_color_set(self, widget, index):
        """Set the color pallete."""
        self.config.set(
            f"{constants.COLOR_PALLETE_PATH}{index}",
            widget.get_rgba().to_string(),
        )
        self.config.save()
