"""Panel to customize default applications."""
import gi

gi.require_version(namespace='Gtk', version='4.0')
gi.require_version(namespace='Adw', version='1')

from gi.repository import Adw, Gtk


class DefaultApplications:
    """Panel to customize default applications."""
    def __init__(self):
        self.name = "Default Applications"
        self.icon = "org.gnome.Settings-default-apps-symbolic"

    def get_widget(self):
        """Returns page widget for default application panel."""
        bin = Adw.Bin.new()

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
        grid.set_valign(Gtk.Align.FILL)
        grid.set_halign(Gtk.Align.FILL)

        label = Gtk.Label.new("Web")
        label.set_css_classes(["dim-label"])



        app_chooser = Gtk.AppChooserButton.new(content_type="x-scheme-handler/http")



        


        grid.attach(label, 0, 0, 1, 1)
        grid.attach_next_to(app_chooser, label, Gtk.PositionType.RIGHT, 1, 1)


        box.append(grid)
        bin.set_child(box)

        return bin
