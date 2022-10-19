"""Panel to customize the terminal."""
from dataclasses import dataclass
import gi

gi.require_version(namespace='Gtk', version='4.0')
gi.require_version(namespace='Adw', version='1')

from gi.repository import Adw, Gtk

from .controller import Controller

class Terminal:
    """Panel to customize terminal."""
    def __init__(self, controller=Controller()):
        self.controller = controller

        self.name = "Terminal"
        self.icon = "org.gnome.Settings-wacom-symbolic"

        self.widget = Adw.Bin.new()

        preferences_page = Adw.PreferencesPage.new()
        preferences_page.set_title("Terminal")
        preferences_page.set_icon_name("org.gnome.Settings-wacom-symbolic")

        preferences_page.add(self.get_text_group())

        self.widget.set_child(preferences_page)

    def get_text_group(self):
        """Return the text group."""
        group = Adw.PreferencesGroup.new()
        group.set_title("Appearance")

        # Font selector.
        font_action_row = Adw.ActionRow.new()
        font_action_row.set_title("Font")


        font_name, font_size = self.controller.get_font()
        font_button = Gtk.FontButton.new_with_font(f"{font_name} {font_size}")
        font_button.set_valign(Gtk.Align.CENTER)
        font_button.connect("font-set", self.on_font_button_font_set)

        font_action_row.add_suffix(font_button)

        # Cursor shape selector.
        cursor_shape_combo_row = Adw.ComboRow.new()
        cursor_shape_combo_row.set_title("Cursor shape")

        cursor_shape_model = Gtk.StringList.new([i.capitalize() for i in self.controller.cursor_shapes])

        cursor_shape_combo_row.set_model(cursor_shape_model)

        current_shape = self.controller.get_cursor_shape()
        cursor_shape_combo_row.set_selected(self.controller.cursor_shapes.index(current_shape))

        cursor_shape_combo_row.connect("notify::selected", self.on_cursor_shape_combo_row_selected)


        # Cursor blink selector.
        cursor_blink_action_row = Adw.ActionRow.new()
        cursor_blink_action_row.set_title("Enable cursor blink")


        cursor_blink_switch = Gtk.Switch.new()
        cursor_blink_switch.set_valign(Gtk.Align.CENTER)

        cursor_blink_switch.set_active(self.controller.get_cursor_blink())
        cursor_blink_switch.connect("notify::active", self.on_cursor_blink_switch_active)

        cursor_blink_action_row.add_suffix(cursor_blink_switch)

        # Confirm window close selector.
        confirm_window_close_action_row = Adw.ActionRow.new()
        confirm_window_close_action_row.set_title("Enable confirmation dialoge when closing")
        confirm_window_close_switch = Gtk.Switch.new()
        confirm_window_close_switch.set_valign(Gtk.Align.CENTER)

        confirm_window_close_switch.set_active(self.controller.get_confirm_window_close())
        confirm_window_close_switch.connect("notify::active", self.on_confirm_window_close_switch_active)

        confirm_window_close_action_row.add_suffix(confirm_window_close_switch)

        group.add(font_action_row)
        group.add(cursor_shape_combo_row)
        group.add(cursor_blink_action_row)
        group.add(confirm_window_close_action_row)


        return group

    def on_cursor_shape_combo_row_selected(self, widget, _):
        """Callback for cursor shape combo row."""
        selected = widget.get_selected_item().get_string().lower()
        self.controller.set_cursor_shape(selected)

    def on_cursor_blink_switch_active(self, widget, _):
        """Callback for cursor blink switch."""
        self.controller.set_cursor_blink(widget.get_active())

    def on_font_button_font_set(self, widget):
        """Callback for font button."""
        font = widget.get_font()
        font_size = int(font.split(" ")[-1])
        font_name = " ".join(font.split(" ")[:-1])
        self.controller.set_font(font_name, font_size)

    def on_confirm_window_close_switch_active(self, widget, _):
        """Callback for confirm window close switch."""
        self.controller.set_confirm_window_close(widget.get_active())