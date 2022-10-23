"""Helper class to create preferences for panels."""

from enum import Enum
import gi

gi.require_version(namespace='Gtk', version='4.0')
gi.require_version(namespace='Adw', version='1')

from gi.repository import Adw, Gtk

class PreferenceType(Enum):
    """Preference types."""
    SWITCH = 0
    SLIDER = 1
    DROPDOWN = 2
    FONT = 3
    ENTRY = 4

class Preference:
    """Helper class to create preferences for panels."""
    def __init__(self, preference_type, title, path, config, subtitle=None, values=None):
        self.preference_type = preference_type
        self.title = title
        self.config = config
        self.path = path
        self.subtitle = subtitle
        self.values = values

    def _on_change(self, widget, *_):
        """Handle changes to @self."""
        value = None
        if self.preference_type == PreferenceType.SWITCH:
            value = widget.get_active()
        elif self.preference_type == PreferenceType.SLIDER:
            value = widget.get_value()
        elif self.preference_type == PreferenceType.DROPDOWN:
            value = self.values[widget.get_selected()]
        elif self.preference_type == PreferenceType.FONT:
            font = widget.get_font()
            font_size = int(font.split(" ")[-1])
            font_name = " ".join(font.split(" ")[:-1])
            value = (font_name, font_size)

        self.config.set(self.path, value)
        self.config.save()

    def _base(self, gtk_widget, action_name):
        """Return a base widget."""
        gtk_widget.set_valign(Gtk.Align.CENTER)
        gtk_widget.connect(action_name, self._on_change)

        return gtk_widget

    def get_widget(self):
        """Return the widget."""
        row = Adw.ActionRow.new()
        if self.preference_type == PreferenceType.DROPDOWN:
            row = Adw.ComboRow.new()

        row.set_title(self.title)
        if self.subtitle:
            row.set_subtitle(self.subtitle)

        if self.preference_type == PreferenceType.SWITCH:
            widget = self._base(Gtk.Switch.new(), "notify::active")
            widget.set_active(self.config.get(self.path))

        elif self.preference_type == PreferenceType.SLIDER:
            widget = self._base(Gtk.Scale.new_with_range(0, 100, 1), "value-changed")
            widget.set_value(self.config.get(self.path))

        elif self.preference_type == PreferenceType.DROPDOWN:
            model = Gtk.StringList.new([i.capitalize() for i in self.values])
            row.set_model(model)
            row.set_selected(self.values.index(self.config.get(self.path)))
            row.connect("notify::selected", self._on_change)
            return row

        elif self.preference_type == PreferenceType.FONT:
            font_name, font_size = self.config.get(self.path)
            widget = Gtk.FontButton.new_with_font(f"{font_name} {font_size}")
            widget = self._base(widget, "font-set")
            widget.set_font(f"{font_name} {font_size}")

        row.add_suffix(widget)

        return row
