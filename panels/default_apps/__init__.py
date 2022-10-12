"""Panel to customize default applications."""
from dataclasses import dataclass
import gi

gi.require_version(namespace='Gtk', version='4.0')
gi.require_version(namespace='Adw', version='1')

from gi.repository import Adw, Gtk


LABELS = {
    "x-scheme-handler/http": ["Web", ["text/html", "application/xhtml+xml", "x-scheme-handler/https"]],
    "x-scheme-handler/mailto": ["Mail", []],
    "text/calendar": ["Calendar", []],
    "audio/x-vorbis+ogg": ["Music", ["audio/"]],
    "video/x-ogm+ogg": ["Videos", ["video/"]],
    "image/jpeg": ["Photos", ["image/"]],
}

class DefaultApplications:
    """Panel to customize default applications."""
    def __init__(self):
        self.name = "Default Applications"
        self.icon = "org.gnome.Settings-default-apps-symbolic"

        self.widget = Adw.Bin.new()

        box = Gtk.Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        box.set_hexpand(True)
        box.set_vexpand(True)
        box.set_halign(Gtk.Align.CENTER)
        box.set_valign(Gtk.Align.START)
        box.set_margin_top(32)
        box.set_margin_bottom(32)
        box.set_margin_start(24)
        box.set_margin_end(24)

        grid = Gtk.Grid.new()
        grid.set_column_spacing(12)
        grid.set_row_spacing(12)
        grid.set_valign(Gtk.Align.FILL)
        grid.set_halign(Gtk.Align.FILL)


        for index, (mime_type, mime_info) in enumerate(LABELS.items()):
            label = Gtk.Label.new(mime_info[0])
            label.set_css_classes(["dim-label"])

            app_chooser = Gtk.AppChooserButton.new(content_type=mime_type)
            app_chooser.set_show_default_item(True)

            app_chooser.connect("changed", self.on_app_chooser_changed)

            grid.attach(label, 0, index, 1, 1)
            grid.attach_next_to(app_chooser, label, Gtk.PositionType.RIGHT, 1, 1)


        box.append(grid)

        self.widget.set_child(box)

    def on_app_chooser_changed(self, widget):
        """Callback for when app chooser is changed."""
        info = widget.get_app_info()
        mime_type = widget.get_content_type()
        info.set_as_default_for_type(mime_type)

        for extra_types in LABELS[mime_type][1]:
            for supported_type in info.get_supported_types():
                if supported_type.startswith(extra_types):
                    info.set_as_default_for_type(supported_type)
