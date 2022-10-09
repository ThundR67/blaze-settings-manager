"""Panel to customize default applications."""
import gi

gi.require_version(namespace='Gtk', version='4.0')
gi.require_version(namespace='Adw', version='1')

from gi.repository import Adw, Gtk


LABELS = {
    "Web": "x-scheme-handler/http",
    "Mail": "x-scheme-handler/mailto",
    "Calendar": "text/calendar",
    "Music": "audio/x-vorbis+ogg",
    "Videos": "video/x-ogm+ogg",
    "Photos": "image/jpeg",
}

class DefaultApplications:
    """Panel to customize default applications."""
    def __init__(self):
        self.name = "Default Applications"
        self.icon = "org.gnome.Settings-default-apps-symbolic"

    def get_widget(self):
        """Returns page widget for default application panel."""
        adw_bin = Adw.Bin.new()

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


        for index, (label_name, mime_type) in enumerate(LABELS.items()):
            label = Gtk.Label.new(label_name)
            label.set_css_classes(["dim-label"])

            app_chooser = Gtk.AppChooserButton.new(content_type=mime_type)
            
            grid.attach(label, 0, index, 1, 1)
            grid.attach_next_to(app_chooser, label, Gtk.PositionType.RIGHT, 1, 1)


        box.append(grid)
        adw_bin.set_child(box)

        return adw_bin
