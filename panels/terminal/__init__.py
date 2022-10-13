"""Panel to customize the terminal."""
from dataclasses import dataclass
import gi

gi.require_version(namespace='Gtk', version='4.0')
gi.require_version(namespace='Adw', version='1')

from gi.repository import Adw, Gtk

_CURSOR_BLINK_CONFIG = "terminal.cursor.blink"
_CURSOR_SHAPE_CONFIG = "terminal.cursor.shape"
_FONT_NAME_CONFIG = "terminal.fonts.font_family"
_FONT_SIZE_CONFIG = "terminal.fonts.font_size"

_CONFIRM_WINDOW_CLOSE_CONFIG = "terminal.misc.confirm_os_window_close"

_CURSOR_SHAPES = ["block", "beam", "underline"]


class Terminal:
    """Panel to customize terminal."""
    def __init__(self, config):
        self.config = config

        self.name = "Terminal"
        self.icon = "org.gnome.Settings-wacom-symbolic"

        self.widget = Adw.Bin.new()

        box = Gtk.Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        box.set_hexpand(True)
        box.set_vexpand(True)
        box.set_margin_top(32)
        box.set_margin_bottom(32)
        box.set_margin_start(24)
        box.set_margin_end(24)

        preferences_page = Adw.PreferencesPage.new()
        preferences_page.set_title("Terminal")
        preferences_page.set_icon_name("org.gnome.Settings-wacom-symbolic")

        preferences_page.add(self.get_text_group())

        box.append(preferences_page)
        self.widget.set_child(box)

    def get_text_group(self):
        """Return the text group."""
        group = Adw.PreferencesGroup.new()
        group.set_title("Appearance")

        # Font selector.
        font_action_row = Adw.ActionRow.new()
        font_action_row.set_title("Font")

        font_button = Gtk.FontButton.new_with_font(
            self.config.get(_FONT_NAME_CONFIG) + " " + str(self.config.get(_FONT_SIZE_CONFIG))
        )
        font_button.set_valign(Gtk.Align.CENTER)
        font_button.connect("font-set", self.on_font_button_font_set)


        font_action_row.add_suffix(font_button)

        # Cursor shape selector.
        cursor_shape_combo_row = Adw.ComboRow.new()
        cursor_shape_combo_row.set_title("Cursor shape")

        cursor_shape_model = Gtk.StringList.new([i.capitalize() for i in _CURSOR_SHAPES])

        cursor_shape_combo_row.set_model(cursor_shape_model)

        current_shape = self.config.get(_CURSOR_SHAPE_CONFIG)
        cursor_shape_combo_row.set_selected(_CURSOR_SHAPES.index(current_shape))

        cursor_shape_combo_row.connect("notify::selected", self.on_cursor_shape_combo_row_selected)


        # Cursor blink selector.
        cursor_blink_action_row = Adw.ActionRow.new()
        cursor_blink_action_row.set_title("Enable cursor blink")


        cursor_blink_switch = Gtk.Switch.new()
        cursor_blink_switch.set_valign(Gtk.Align.CENTER)

        cursor_blink_switch.set_active(self.config.get(_CURSOR_BLINK_CONFIG))
        cursor_blink_switch.connect("notify::active", self.on_cursor_blink_switch_active)

        cursor_blink_action_row.add_suffix(cursor_blink_switch)

        # Confirm window close selector.
        confirm_window_close_action_row = Adw.ActionRow.new()
        confirm_window_close_action_row.set_title("Enable confirmation dialoge when closing")
        confirm_window_close_switch = Gtk.Switch.new()
        confirm_window_close_switch.set_valign(Gtk.Align.CENTER)

        confirm_window_close_switch.set_active(_CONFIRM_WINDOW_CLOSE_CONFIG)
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
        self.config.set(_CURSOR_SHAPE_CONFIG, selected)
        self.config.save()

    def on_cursor_blink_switch_active(self, widget, _):
        """Callback for cursor blink switch."""
        self.config.set(_CURSOR_BLINK_CONFIG, widget.get_active())
        self.config.save()

    def on_font_button_font_set(self, widget):
        """Callback for font button."""
        font = widget.get_font()
        font_size = int(font.split(" ")[-1])
        font_name = " ".join(font.split(" ")[:-1])
        self.config.set(_FONT_NAME_CONFIG, font_name)
        self.config.set(_FONT_SIZE_CONFIG, font_size)
        self.config.save()

    def on_confirm_window_close_switch_active(self, widget, _):
        """Callback for confirm window close switch."""
        self.config.set(_CONFIRM_WINDOW_CLOSE_CONFIG, widget.get_active())
        self.config.save()
